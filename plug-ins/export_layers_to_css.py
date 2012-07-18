#!/usr/bin/env python
# -*- coding: <utf-8> -*-
# Author: Chris Mohler <cr33dog@gmail.com>
# Copyright 2009 Chris Mohler
# "Only Visible" and filename formatting introduced by mh
# License: GPL v3+
# Version 1.0
# GIMP plugin to export layers as PNGs

from gimpfu import *
import os, re

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

class Css(object):
    def css_label(self, text):
        css_chars = re.compile("[^-_\w]") 
        return css_chars.sub('_', text.decode('utf-8').encode('ascii', 'ignore'))
        
    def __init__(self, base_name, scale):
        self.layer_name_count = {}
        self.base_name = base_name
        self.graphics_name = self.css_label(base_name)
        self.image_filename = base_name + ".png"
        self.scale = scale
        self.css = ""
        self.html = ""
        
    def add_layer(self, layer):
        name = self.css_label(layer.name)
        if name in self.layer_name_count:
            self.layer_name_count[name] += 1
            name = "%s-%d" % (name, self.layer_name_count[name])
        else:
            self.layer_name_count[layer.name] = 0
        self.css += """
.{graphics_name}.{layer_name} {{
    background-image: url({image_filename});
    width: {width}px;
    height: {height}px;
    background-position-y: {position_y}px;
}}""".format(graphics_name=self.graphics_name,
             layer_name=name, 
             image_filename=self.image_filename, 
             width=int(layer.width / self.scale),
             height=int(layer.height / self.scale),
             position_y=-int(layer.offsets[1] / self.scale))
        self.html += """
        <tr>
            <td>{layer_name}</td>
            <td><div class="{graphics_name} {layer_name}"></div></td>
        </tr>""".format(graphics_name=self.graphics_name,
                        layer_name=name)
        
    def save(self, path, image_width):
        self.save_css(path, image_width)
        self.save_html(path)
        
    def save_css(self, path, image_width):
        css_filepath = os.path.join(path, self.base_name + ".css");
        self.css += """
.{graphics_name} {{
    background-size: {width}px;
}}""".format(graphics_name=self.graphics_name,
             width=int(image_width / self.scale))
        with open(css_filepath, "wb") as f:
            f.write(self.css)
        
    def save_html(self, path):
        html_filepath = os.path.join(path, self.base_name + ".html");
        self.html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Graphics</title>
<link rel="stylesheet" href="{base_name}.css"></link>

</head>
<p>elements with classes {graphics_name} and ...</p>
<body>
    <table>
        <tr>
            <th>class</th>
            <th>element</th>
        </tr>""".format(base_name=self.base_name, 
                        graphics_name=self.graphics_name) + self.html + """
    </table>
</body>
</html>"""
        with open(html_filepath, "wb") as f:
            f.write(self.html)

def export_layers_to_css(img, drw, path, scale=1):
    base_name = "graphics-" + img.name.rsplit('.', 1)[0]

    dupe = img.duplicate()
    css = Css(base_name=base_name, scale=scale)
    offset_y = 0
    for layer in dupe.layers:
        layer.visible = True
        layer.set_offsets(0, offset_y)
        css.add_layer(layer)
        offset_y += layer.height
    merged_layer = dupe.merge_visible_layers(EXPAND_AS_NECESSARY)
    css.save(path=path, image_width=merged_layer.width)
    image_filename = base_name + ".png"
    image_filepath = os.path.join(path, image_filename);
    pdb.file_png_save(dupe, dupe.layers[0], image_filepath, image_filename, 0, 9, 1, 1, 1, 1, 1)
    gimp.delete(dupe)
            
register(
    proc_name=("python-fu-layers-to-css"),
    blurb=("Export Layers to one PNG with CSS stylesheet"),
    help=("""Export Layers to one PNG with CSS stylesheet
    
    """),
    author=("Per Rosengren"),
    copyright=("Stunning AB"),
    date=("2012"),
    label=("to _CSS"),
    imagetypes=("*"),
    params=[
        (PF_IMAGE, "img", "Image", None),
        (PF_DRAWABLE, "drw", "Drawable", None),
        (PF_DIRNAME, "path", "Save PNG and CSS here", os.getcwd()),
        (PF_INT, "scale", "The scale of the image", 1),
        ],
    results=[],
    function=(export_layers_to_css), 
    menu=("<Image>/File/E_xport Layers"), 
    domain=("gimp20-python", gimp.locale_directory)
    )

main()
