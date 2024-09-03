# 435Assignment-1

The code is in Python, so just run python main.py for compilation.

The annotated screenshots are contained in the repo.

Library used: xml.etree.ElementTree, PIL (Image, ImageDraw), lxml (etree), os

Solution: I use the xml package in Python to read xml files and fix them if needed (such as the ringtone example). Then by reading bounds in the leaf nodes (which is automatically extracted by the xml package), I draw boxes with these bounds as parameters. I save images with _annotated.png suffix.