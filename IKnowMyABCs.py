#Copyright (c) 2012,13 Walter Bender
#Copyright (c) 2012 Ignacio Rodriguez

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from gi.repository import Gtk
from gi.repository import Gdk

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox, ToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton

from gettext import gettext as _
import os.path

from page import Page
from utils.toolbar_utils import separator_factory, label_factory, radio_factory

import logging
_logger = logging.getLogger('iknowmyabcs-activity')


class IKnowMyABCs(activity.Activity):
    ''' Learning the alphabet.

    Level1: The alphabet appears and the user has the option to click
    on a letter to listen the name of it and the sound of it.

    Level2: The laptop says a letter and the user must click on the
    correct one. '''

    def __init__(self, handle):
        ''' Initialize the toolbars and the reading board '''
        super(IKnowMyABCs, self).__init__(handle)

        if 'LANG' in os.environ:
            language = os.environ['LANG'][0:2]
        elif 'LANGUAGE' in os.environ:
            language = os.environ['LANGUAGE'][0:2]
        else:
            language = 'es'  # default to Spanish

        # FIXME: find some reasonable default situation
        language = 'es'

        self.activity_path = activity.get_bundle_path()

        self._lessons_path = os.path.join(self.activity_path,
                                          'lessons', language)
        self._images_path = os.path.join(self.activity_path,
                                          'images', language)
        self._sounds_path = os.path.join(self.activity_path,
                                          'sounds', language)

        self._setup_toolbars()

        # Create a canvas
        canvas = Gtk.DrawingArea()
        width = Gdk.Screen.width()
        height = int(Gdk.Screen.height())
        canvas.set_size_request(width, height)
        canvas.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#000000"))
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

        toolbox = ToolbarBox()

        # Activity toolbar
        activity_button = ActivityToolbarButton(self)

        toolbox.toolbar.insert(activity_button, 0)
        activity_button.show()

        self.set_toolbar_box(toolbox)
        toolbox.show()
        primary_toolbar = toolbox.toolbar
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
