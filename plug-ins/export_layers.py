#!/usr/bin/env python
# -*- coding: <utf-8> -*-
# Author: Chris Mohler <cr33dog@gmail.com>
# Copyright 2009 Chris Mohler
# "Only Visible" and filename formatting introduced by mh
# License: GPL v3+
# Version 0.5
# GIMP plugin to export layers as PNGs

from gimpfu import *
import os, re

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def format_filename(img, layer):
    imgname = img.name.decode('utf-8')
    layername = layer.name.decode('utf-8')
    regex = re.compile("[^-\w]", re.UNICODE) 
    filename = regex.sub('_', imgname) + '-' + regex.sub('_', layername) + '.png'
    return filename

def get_layers_to_export(img, only_visible):
    layers = []
    for layer in img.layers:
        if only_visible and layer.visible:
            layers.append(layer)
        if not only_visible:
            layers.append(layer)
    return layers

def export_layers(img, drw, path, only_visible=True, flatten=False, remove_offsets=False):
    dupe = img.duplicate()
    savelayers = get_layers_to_export(dupe, only_visible)
    for layer in dupe.layers:
        layer.visible = 0 
    for layer in dupe.layers:
        if layer in savelayers:
            layer.visible = 1
            filename = format_filename(img, layer)
            fullpath = os.path.join(path, filename);
            tmp = dupe.duplicate()
            if (flatten):
                tmp.flatten()
            if (remove_offsets):
                tmp.layers[0].set_offsets(0, 0) 
            pdb.file_png_save(tmp, tmp.layers[0], fullpath, filename, 0, 9, 1, 1, 1, 1, 1)
        dupe.remove_layer(layer)

            
register(
    proc_name=("python-fu-export-layers"),
    blurb=("Export Layers as PNG"),
    help=("Export all layers as individual PNG files."),
    author=("Chris Mohler <cr33dog@gmail.com>"),
    copyright=("Chris Mohler"),
    date=("2009"),
    label=("as _PNG"),
    imagetypes=("*"),
    params=[
        (PF_IMAGE, "img", "Image", None),
        (PF_DRAWABLE, "drw", "Drawable", None),
        (PF_DIRNAME, "path", "Save PNGs here", os.getcwd()),
        (PF_BOOL, "only_visible", "Only Visible Layers?", True),
        (PF_BOOL, "flatten", "Flatten Images?", False),
        (PF_BOOL, "remove_offsets", "Remove Offsets?", False),
        ],
    results=[],
    function=(export_layers), 
    menu=("<Image>/File/E_xport Layers"), 
    domain=("gimp20-python", gimp.locale_directory)
    )

main()