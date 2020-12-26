# Copyright (C) 2009, Aleksey Lim
# Copyright (C) 2018, James Cameron <quozl@laptop.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import logging
from queue import Queue
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


Gst.init(None)


class Aplay:
    def __init__(self):
        pipeline = Gst.ElementFactory.make('playbin', 'playbin')
        pipeline.set_property(
            "video-sink",
            Gst.ElementFactory.make('fakesink', 'fakesink'))

        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::eos', self._on_message_eos)
        bus.connect('message::error', self._on_message_error)

        self._pipeline = pipeline
        self._queue = Queue()

    def _dequeue(self):
        if self._queue.empty():
            return
        name = self._queue.get()
        self._pipeline.props.uri = 'file://' + name
        self._pipeline.set_state(Gst.State.PLAYING)

    def _on_message_eos(self, bus, message):
        if self._pipeline:
            self._pipeline.set_state(Gst.State.NULL)
            self._dequeue()

    def _on_message_error(self, bus, message):
        err, debug = message.parse_error()
        logging.error('%s %s', err, debug)
        self._pipeline.set_state(Gst.State.NULL)
        self._dequeue()

    def play(self, name):
        self._queue.put(name)
        if self._pipeline.get_state(Gst.CLOCK_TIME_NONE)[1] == Gst.State.NULL:
            self._dequeue()

    def close(self):
        self._pipeline.set_state(Gst.State.NULL)
        self._pipeline = None


aplay = Aplay()
