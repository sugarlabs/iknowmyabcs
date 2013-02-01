#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright (c) 2009-11 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os


class SVG:
    ''' SVG generators '''

    def __init__(self):
        self._scale = 1
        self._stroke_width = 1
        self._fill = '#FFFFFF'
        self._stroke = '#000000'

    def _svg_style(self, stroke=False, extras=""):
        if stroke:
            return "%s%s%s%s%s%f%s%s%s" % ("style=\"fill:", self._fill,
                                           ";stroke:", "#000000",
                                           ";stroke-width:",
                                           self._stroke_width, ";", extras,
                                           "\" />\n")
        else:
            return "%s%s%s%s%s%f%s%s%s" % ("style=\"fill:", self._fill,
                                           ";stroke:", self._stroke,
                                           ";stroke-width:",
                                           self._stroke_width, ";", extras,
                                           "\" />\n")

    def _svg_text(self, x, y, font_size, text_string, stroke=False,
                  center=False):
        if center:
            align = 'text-align:center;text-anchor:middle'
        else:
            align = ''
        svg_string = "<text x=\"%d\" y=\"%d\" " % (x, y)
        if stroke:
            svg_string += "style=\"font-size:%dpx;font-weight:bold;font-family:Sans;fill:%s;\
stroke:#000000;%s\">" % (font_size, self._stroke, align)
        else:
            svg_string += "style=\"font-size:%dpx;font-weight:bold;font-family:Sans;fill:%s;\
%s\">" % (font_size, self._stroke, align)
        svg_string += "<tspan x=\"%d\" y=\"%d\">%s</tspan></text>" % \
            (x, y, text_string)
        return svg_string

    def _svg_line(self, x1, y1, x2, y2):
        svg_string = "<line x1=\"%f\" y1=\"%f\" x2=\"%f\" y2=\"%f\"\n" % \
                      (x1, y1, x2, y2)
        svg_string += self._svg_style("stroke-linecap:square;")
        return svg_string

    def _svg_rect(self, w, h, rx, ry, x, y, stroke=False):
        svg_string = "       <rect\n"
        svg_string += "          width=\"%f\"\n" % (w)
        svg_string += "          height=\"%f\"\n" % (h)
        svg_string += "          rx=\"%f\"\n" % (rx)
        svg_string += "          ry=\"%f\"\n" % (ry)
        svg_string += "          x=\"%f\"\n" % (x)
        svg_string += "          y=\"%f\"\n" % (y)
        self.set_stroke_width(1.0)
        svg_string += self._svg_style(stroke=stroke)
        return svg_string

    def _background(self, scale, stroke=False):
        return self._svg_rect(79.5 * scale, 59.5 * scale, 1, 1, 0.25, 0.25,
                              stroke=stroke)

    def header(self, scale=1, background=True, stroke=False):
        svg_string = "<?xml version=\"1.0\" encoding=\"UTF-8\""
        svg_string += " standalone=\"no\"?>\n"
        svg_string += "<!-- Created with Emacs -->\n"
        svg_string += "<svg\n"
        svg_string += "   xmlns:svg=\"http://www.w3.org/2000/svg\"\n"
        svg_string += "   xmlns=\"http://www.w3.org/2000/svg\"\n"
        svg_string += "   version=\"1.0\"\n"
        svg_string += "%s%f%s" % ("   width=\"", scale * 80 * self._scale,
                                  "\"\n")
        svg_string += "%s%f%s" % ("   height=\"", scale * 60 * self._scale,
                                  "\">\n")
        svg_string += "%s%f%s%f%s" % ("<g\n       transform=\"matrix(",
                                      self._scale, ",0,0,", self._scale,
                                      ",0,0)\">\n")
        if background:
            svg_string += self._background(scale, stroke=stroke)
        return svg_string

    def footer(self):
        svg_string = "</g>\n"
        svg_string += "</svg>\n"
        return svg_string

    def set_scale(self, scale=1.0):
        self._scale = scale

    def set_colors(self, colors):
        self._stroke = colors[0]
        self._fill = colors[1]

    def set_stroke_width(self, stroke_width=1.0):
        self._stroke_width = stroke_width


def generate_card(string='a', colors=['#FF0000', '#FFFFFF'],
                  background=True, scale=1, stroke=False, center=False,
                  font_size=40):
    svg = SVG()
    svg.set_scale(scale)
    svg.set_colors(colors)
    svg_string = svg.header(background=background, stroke=stroke)
    if center:
        x = 40
    else:
        x = 5
    svg_string += svg._svg_text(x, 45, font_size, string, stroke=stroke,
                                    center=center)
    svg_string += svg.footer()
    return svg_string


def open_file(datapath, filename):
    return file(os.path.join(datapath, filename), "w")


def close_file(f):
    f.close()


def generator(datapath):
    i = 1
    filename = "tile-%d.svg" % (i)
    f = open_file(datapath, filename)
    f.write(generate_card(string='b', background=False))
    close_file(f)


def genblank(w, h, colors, stroke_width=1.0):
    svg = SVG()
    svg.set_scale(1)
    svg.set_colors(colors)
    svg.set_stroke_width(stroke_width)
    svg_string = svg.header(int(w / 80), int(h / 60))
    svg_string += svg.footer()
    return svg_string


def main():
    return 0

if __name__ == "__main__":
    if not os.path.exists(os.path.join(os.path.abspath('.'), 'images')):
        os.mkdir(os.path.join(os.path.abspath('.'), 'images'))
    generator(os.path.join(os.path.abspath('.'), 'images'))
    main()
