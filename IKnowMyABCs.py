#Copyright (c) 2012 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


import gtk

from sugar.activity import activity
try:
    from sugar.graphics.toolbarbox import ToolbarBox, ToolbarButton
    _HAVE_TOOLBOX = True
except ImportError:
    _HAVE_TOOLBOX = False

if _HAVE_TOOLBOX:
    from sugar.activity.widgets import ActivityToolbarButton
    from sugar.activity.widgets import StopButton

from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.combobox import ComboBox
from sugar.graphics.toolcombobox import ToolComboBox
from sugar.datastore import datastore
from sugar import profile

from gettext import gettext as _
import os.path

from page import Page
from utils.grecord import Grecord
from utils.play_audio import play_audio_from_file
from utils.toolbar_utils import separator_factory, label_factory, radio_factory

import logging
_logger = logging.getLogger('iknowmyabcs-activity')


class IKnowMyABCs(activity.Activity):
    ''' Learning the alphabet. 

    Level1: The alphabet appears and the user has the option to click
    on a letter to listen the name of it and the sound of it.

    Level2: The letters appear randomly and the user must place them
    in the correct order.

    Level3: The laptop says a letter and the user must click on the
    correct one. '''

    def __init__(self, handle):
        ''' Initialize the toolbars and the reading board '''
        super(IKnowMyABCs, self).__init__(handle)

        self.reading = False
        self.testing = False
        self.recording = False
        self.grecord = None
        self.datapath = get_path(activity, 'instance')

        if 'LANG' in os.environ:
            language = os.environ['LANG'][0:2]
        elif 'LANGUAGE' in os.environ:
            language = os.environ['LANGUAGE'][0:2]
        else:
            language = 'es'  # default to Spanish

        # FIXME: find some reasonable default situation
        language = 'es'

        if os.path.exists(os.path.join('~', 'Activities',
                                       'IKnowMyABCs.activity')):
            self._lessons_path = os.path.join('~', 'Activities',
                                              'IKnowMyABCs.activity',
                                              'lessons', language)
        else:
            self._lessons_path = os.path.join('.', 'lessons', language)

        self._images_path = self._lessons_path.replace('lessons', 'images')
        self._sounds_path = self._lessons_path.replace('lessons', 'sounds')
        self._setup_toolbars()

        # Create a canvas
        canvas = gtk.DrawingArea()
        width = gtk.gdk.screen_width()
        height = int(gtk.gdk.screen_height())
        canvas.set_size_request(width, height)
        canvas.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#000000"))
        canvas.show()
        self.set_canvas(canvas)

        self.mode = 'letter'

        self._page = Page(canvas, self._lessons_path,
                          self._images_path, self._sounds_path,
                          parent=self)

    def _setup_toolbars(self):
        ''' Setup the toolbars.. '''

        # no sharing
        self.max_participants = 1

        if _HAVE_TOOLBOX:
            toolbox = ToolbarBox()

            # Activity toolbar
            activity_button = ActivityToolbarButton(self)

            toolbox.toolbar.insert(activity_button, 0)
            activity_button.show()

            self.set_toolbar_box(toolbox)
            toolbox.show()
            primary_toolbar = toolbox.toolbar
        else:
            # Use pre-0.86 toolbar design
            primary_toolbar = gtk.Toolbar()
            toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(toolbox)
            toolbox.add_toolbar(_('Page'), primary_toolbar)
            toolbox.show()
            toolbox.set_current_toolbar(1)

            # no sharing
            if hasattr(toolbox, 'share'):
                toolbox.share.hide()
            elif hasattr(toolbox, 'props'):
                toolbox.props.visible = False

        button = radio_factory('letter', primary_toolbar, self._letter_cb,
                               tooltip=_('listen to the letter names'))
        radio_factory('picture', primary_toolbar, self._picture_cb,
                      tooltip=_('listen to the letter names'),
                      group=button)
        '''
        radio_factory('sort', primary_toolbar, self._sort_cb,
                      tooltip=_('sort into abc order'),
                      group=button)
        '''
        radio_factory('find1', primary_toolbar, self._find1_cb,
                      tooltip=_(
                'find the letter that corresponds to the sound'),
                      group=button)
        radio_factory('find2', primary_toolbar, self._find2_cb,
                      tooltip=_(
                'find the letter that corresponds to the sound'),
                      group=button)

        self.status = label_factory(primary_toolbar, '', width=300)

        if _HAVE_TOOLBOX:
            separator_factory(primary_toolbar, True, False)

            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>q'
            toolbox.toolbar.insert(stop_button, -1)
            stop_button.show()

    def _letter_cb(self, event=None):
        ''' click on card to hear the letter name '''
        self.mode = 'letter'
        self.status.set_text(_('Click on a card to hear a sound.'))
        if hasattr(self, '_page'):
            self._page.new_page()
        return

    def _picture_cb(self, event=None):
        ''' click on card to hear the letter name '''
        self.mode = 'picture'
        self.status.set_text(_('Click on a card to hear a sound.'))
        if hasattr(self, '_page'):
            self._page.new_page(cardtype='image')
        return

    def _sort_cb(self, event=None):
        ''' sort cards into ABC order '''
        self.mode = 'sort'
        if hasattr(self, '_page'):
            self._page.new_page()
            # self._page.random_order()
        return

    def _find1_cb(self, event=None):
        ''' letter sound --> letter card '''
        self.mode = 'find by letter'
        if hasattr(self, '_page'):
            _logger.debug('find1 button pushed')
            self._page.new_page()
            self._page.new_target()
        return

    def _find2_cb(self, event=None):
        ''' word sound --> letter card '''
        self.mode = 'find by word'
        if hasattr(self, '_page'):
            _logger.debug('find2 button pushed')
            self._page.new_page()
            self._page.new_target()
        return

    def write_file(self, file_path):
        ''' Write status to the Journal '''
        if not hasattr(self, '_page'):
            return
        self.metadata['page'] = str(self._page.current_card)


def get_path(activity, subpath):
    """ Find a Rainbow-approved place for temporary files. """
    try:
        return(os.path.join(activity.get_activity_root(), subpath))
    except:
        # Early versions of Sugar didn't support get_activity_root()
        return(os.path.join(
                os.environ['HOME'], ".sugar/default", SERVICE, subpath))
