"""
 aplay.py
 refactored based on Jukebox Activity
 Copyright (C) 2007 Andy Wingo <wingo@pobox.com>
 Copyright (C) 2007 Red Hat, Inc.
 Copyright (C) 2008-2010 Kushal Das <kushal@fedoraproject.org>
 Copyright (C) 2010-11 Walter Bender
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

import os
import subprocess

import logging
_logger = logging.getLogger('iknowmyabcs-activity')


GST_PATHS = ['/usr/bin/gst-launch', '/bin/gst-launch',
             '/usr/local/bin/gst-launch',
             '/usr/bin/gst-launch-1.0', '/bin/gst-launch-1.0',
             '/usr/local/bin/gst-launch-1.0',
             '/usr/bin/gst-launch-0.10', '/bin/gst-launch-0.10',
             '/usr/local/bin/gst-launch-0.10']


def play_audio_from_file(file_path):
    """ Audio media """

    if not hasattr(play_audio_from_file, 'gst_launch'):
        for path in GST_PATHS:
            if os.path.exists(path):
                play_audio_from_file.gst_launch = path
                _logger.debug(path)
                break

    if not hasattr(play_audio_from_file, 'gst_launch'):
        _logger.debug('gst-launch not found')
        return

    command_line = [play_audio_from_file.gst_launch, 'filesrc',
                    'location=' + file_path, '! oggdemux', '! vorbisdec',
                    '! audioconvert', '! alsasink']
    subprocess.check_output(command_line)
