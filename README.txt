GIMP plugin: Export layers to CSS
=================================

This plugin gives the option to paste all layers of a graphics file an a web graphics file. 
A CSS stylesheet is generated so that any layer can be used as background on a html
element by simply giving the element the layer's name as class.

Example::

	<div class="graphics-sample Cross"></div>
	
There is also an example HTML file generated for copy-pasting from. 


Should be cross platform, but only tested on GIMP 2.8 on Windows 7.


Installation
------------

Install GIMP 2.8

Copy ``plug-ins/export_layers_to_css.py`` to ``<Your home dir>/.gimp-2.8/plug-ins``


Usage
-----

Open a layered file. You can try ``sample/sample.xcf``.

Any layers that belong to the same element must be grouped in a separate *layer group*.
Make sure that every layer and layer group is properly cropped. You can use **Layer** -> **Autocrop Layer**.

Click **File** -> **Export Layers** -> **To CSS**

Select your web static root, and select the scale.

Click **Ok** to generate the files.

Copy the parts you need for your webpage from the generated HTML.