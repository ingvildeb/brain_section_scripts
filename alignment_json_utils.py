import json
import glob
from PIL import Image 
import re

# Basic function to read json data

def read_json(json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    return json_data

# Function to parse a QuickNII or VisuAlign JSON into dictionaries of anchorings, markers, widths and heights, with the section nr as the key

def parse_anchoring_data(json_data):
    anchorings_dict = {}
    markers_dict = {}
    widths_dict = {}
    heights_dict = {}

    for s in json_data["slices"]:
        nr = s["nr"]
        anchorings_dict[nr] = s["anchoring"]
        widths_dict[nr] = s["width"]
        heights_dict[nr] = s["height"]
        if "markers" in s:
            markers_dict[nr] = s["markers"]

    return anchorings_dict, markers_dict, widths_dict, heights_dict


# Function to convert VisuAlign markers made on images with a given resolution to images of another resolution.

def convert_markers(old_markers, old_width, old_height, new_width, new_height):
    new_markers = []
    for marker_xy in old_markers:
        xfrom_rel = marker_xy[0] / old_width
        xto_rel = marker_xy[2] / old_width
        yfrom_rel = marker_xy[1] / old_height
        yto_rel = marker_xy[3] / old_height
        
        xfrom_new = new_width * xfrom_rel
        xto_new = new_width * xto_rel
        yfrom_new = new_height * yfrom_rel
        yto_new = new_height * yto_rel
        
        new_markers.append([xfrom_new, yfrom_new, xto_new, yto_new])
    return new_markers

# Function to create a QuickNII JSON dictionary with empty slice data

def create_quicknii_json_dict(name, target, target_resolution):
    return {"name": name, "target": target, "target-resolution": target_resolution, "slices": []}

# Function to create a QuickNII / VisuAlign JSON slice dictionary based on input values

def get_slice_dict(nr, width, height, filename, anchoring=None, markers=None):
    slice_dict = {
        "nr": nr,
        "width": width,
        "height": height,
        "filename": filename,
    }
    if anchoring:
        slice_dict["anchoring"] = anchoring
    if markers:
        slice_dict["markers"] = markers
    return slice_dict

# Function to insert anchorings and / or markers from one JSON into another

def insert_existing_anchorings(old_json, new_json, json_name, target_atlas, target_resolution, same_resolution=True):
    json_dict = create_quicknii_json_dict(json_name, target_atlas, target_resolution)

    old_json_data = read_json(old_json)
    new_json_data = read_json(new_json)
    old_anchorings, old_markers, old_widths, old_heights = parse_anchoring_data(old_json_data)

    for s in new_json_data["slices"]:
        nr = s["nr"]
        width = s["width"]
        height = s["height"]
        filename = s["filename"]

        if nr in old_anchorings:
            anchoring = old_anchorings[nr]
            markers = None
            if nr in old_markers:
                markers_data = old_markers[nr]
                if same_resolution:
                    markers = markers_data
                else:
                    markers = convert_markers(markers_data, old_widths[nr], old_heights[nr], width, height)

            slice_dict = get_slice_dict(nr, width, height, filename, anchoring, markers)
        else:
            slice_dict = get_slice_dict(nr, width, height, filename)

        json_dict["slices"].append(slice_dict)

    return json_dict

# Function to create a QuickNII / VisuAlign JSON file from a folder of .png files

def create_quicknii_slicedict(files_path, name, target, target_resolution):
    files = glob.glob(f"{files_path}*.png")
    slice_dicts = []
    
    for file in files:
        img = Image.open(file) 
          
        width = img.width 
        height = img.height 
        filename = os.path.basename(file)
        nr = re.findall("[s][0-9][0-9][0-9]", filename)
        
        if len(nr) > 1:
            print("error: more than one potential section number in file name!")
            break
        else:
            nr = nr[0]
            nr = re.sub("[s]", "", nr)
            nr = int(nr)
    
        slice_dict = get_slice_dict(nr, width, height, filename)
        
        slice_dicts.append(slice_dict)

    sorted_slices_dicts = sorted(slice_dicts, key=lambda x: (x['nr']))

    return sorted_slices_dicts
    


# Function to split a QuickNII / VisuAlign JSON file based on part of filename
