import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
from lxml import etree
import os

# fix if needed
folder_path = "./Programming-Assignment-Data/"



'''function for parsing the xml file:
Using the xml.etree.ElementTree to parse the tree, or fix it if needed.
Then return all leaf nodes' bounds as an array for the image processor to draw/
'''
def parse_xml(xml_file):
    # For error: fix the xml file
    try:
        tree = ET.parse(xml_file)
    except Exception:
        try:
            # Use XMLParser with recover=True to fix the broken file
            base_name = os.path.splitext(xml_file)[0]
            output_xml = f'{base_name}_fixed.xml'
            parser = etree.XMLParser(recover=True)
            tree = etree.parse(xml_file, parser)
            # Write it to another xml file and replace te original file with a new name.
            tree.write(output_xml, encoding='utf-8', xml_declaration=True)
            print(f'Due to an exception, file {xml_file} has been fixed and saved as {output_xml}.')
            # Re-parse the tree
            tree = ET.parse(output_xml)
        except etree.XMLSyntaxError as e:
            print(f'XML syntax error in {xml_file}: {e}')

    root = tree.getroot()
    print(f"Successfully parsed {xml_file}")
    leaf_nodes = []   
    
    # A recursive function to find all leaf nodes
    def find_leaf_nodes(node):
        #base case: does not contain any sub arrays
        if (len(list(node)) == 0):
            bounds = node.get('bounds')
            # use .get() to return bounds
            if bounds:
                leaf_nodes.append(bounds)
        else:
            for child in node:
                find_leaf_nodes(child)
    
    find_leaf_nodes(root)
    return leaf_nodes

# The bounds in ET is stored in '[]' format, and we split them and return seperate values to annotate the image
def extract_bounds(bounds_str):
    bounds_str = bounds_str.replace('][', ',').replace('[', '').replace(']', '')
    x1, y1, x2, y2 = map(int, bounds_str.split(','))
    return x1, y1, x2, y2

# Draw bounds on the image with bounds extracted in the previous function
def annotate(image_file, leaf_bounds):
    with Image.open(image_file) as img:
        draw = ImageDraw.Draw(img)
        for bounds_str in leaf_bounds:
            x1, y1, x2, y2 = extract_bounds(bounds_str)
            draw.rectangle([x1, y1, x2, y2], outline="yellow", width=3)
        return img

# main function that calls all helper functions above:
# Read xml first, annotate the image, save the new image to another name
def process_files(xml_file, image_file, output_file):
    leaf_bounds= parse_xml(xml_file)

    annotated_image = annotate(image_file, leaf_bounds)
    annotated_image.save(output_file)


files = os.listdir(folder_path)
xml_files = [name for name in files if name.endswith('.xml')]
png_files = [name for name in files if name.endswith('.png')]


for xml_file in xml_files:
    # Get the base name (without extension)
    base_name = os.path.splitext(xml_file)[0]
        
    # Find the corresponding PNG file
    png_file = f'{base_name}.png'
    new_png = f'{base_name}_annotated.png'
    if png_file in png_files:
        xml_path = os.path.join(folder_path, xml_file)
        png_path = os.path.join(folder_path, png_file)
            
        process_files(xml_path, png_path, new_png)

        
        print(f'Processed {xml_file} and {png_file}')
    else:
        print(f'No matching PNG file for {xml_file}')
