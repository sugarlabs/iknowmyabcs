"""
 aplay.py
 Copyright (C) 2007 Andy Wingo <wingo@pobox.com>
 Copyright (C) 2007 Red Hat, Inc.
 Copyright (C) 2008-2010 Kushal Das <kushal@fedoraproject.org>
 Copyright (C) 2010-11 Walter Bender
 Copyright (C) 2013-14 Aneesh Dogra <lionaneesh@gmail.com>
"""

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst

import logging
import time
_logger = logging.getLogger('iknowabcs-activity')

def play_audio_from_file(file_path, queue=False):
    """ Audio media """
    if hasattr(play_audio_from_file, 'player') and \
       play_audio_from_file.player:
        if queue:
            if hasattr(play_audio_from_file, 'queue'):
                if play_audio_from_file.queue and \
                   file_path in play_audio_from_file.queue:
                    # if we already have that file in the queue
                    # we'll just update the timer.
                    if hasattr(play_audio_from_file, 'queue_timeout'):
                        time.sleep(0.01)
                        GLib.source_remove(play_audio_from_file.queue_timeout)
                        f = Gst.Format(Gst.Format.TIME)
                        duration = play_audio_from_file.player.query_duration(f)[0]
                        timeout = duration / 1000000000.
                        play_audio_from_file.queue_timeout = \
                            GLib.timeout_add(int(timeout * 1000), \
                                            play_audio_from_file, file_path)
                        return
            else:
                play_audio_from_file.queue = []

            time.sleep(0.01)
            f = Gst.Format(Gst.Format.TIME)
            duration = play_audio_from_file.player.query_duration(f)[0]
            timeout = duration / 1000000000.
            play_audio_from_file.queue_timeout = GLib.timeout_add( \
                        int(timeout * 1000), play_audio_from_file, file_path)
            play_audio_from_file.queue.append(file_path)
            return
        else:
            play_audio_from_file.player.set_state(Gst.State.NULL)

    else:
        Gst.init(None)

    play_audio_from_file.player = Gst.parse_launch (
                    'filesrc location=%s ! oggdemux ! vorbisdec ! ' \
                    'audioconvert ! alsasink' % (file_path))

    if not play_audio_from_file.player:
        _logger.warning('unable to play audio file %s' % (file_path))

    else:
        play_audio_from_file.player.set_state(Gst.State.PLAYING)
