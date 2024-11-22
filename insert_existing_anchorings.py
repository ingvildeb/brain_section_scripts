import json

old_json = r"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\test_folder\mouse650_jointAnchoring_final_nonlinear.json"
new_json = r"Y:\2021_Bjerke_DevMouse_projects\QuickNII_registration_workspace\test_folder\mouse650_jointWithPNN.json"


def read_json(json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    return json_data


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


def create_quicknii_json_dict(name, target, target_resolution):
    return {"name": name, "target": target, "target-resolution": target_resolution, "slices": []}


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


def insert_existing_anchorings(old_json, new_json, same_resolution=True):
    json_dict = create_quicknii_json_dict("testing", "DeMBAv2_P35_template.cutlas", [570, 705, 400])

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


json_dict = insert_existing_anchorings(old_json, new_json)
