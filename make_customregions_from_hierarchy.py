import json
from collections import defaultdict
import pandas as pd

# Load the JSON data
hierarchy_file = r"graphing_demo_data/CCF_v3_ontology.json"

with open(hierarchy_file, 'r') as file:
    json_data = json.load(file)

def group_ids_by_st_level(data):
    st_level_dict = defaultdict(list)

    def recursive_search(node):
        st_level = node['st_level']
        st_level_dict[st_level].append(node['id'])

        # Determine the minimum st_level of the children
        children_levels = sorted(set(child['st_level'] for child in node.get('children', [])))
        
        if children_levels:
            min_child_level = children_levels[0]
            if min_child_level > st_level:
                # Include the parent in all intermediate levels up to but not including min_child_level
                for intermediate_st_level in range(st_level + 1, min_child_level):
                    st_level_dict[intermediate_st_level].append(node['id'])

        for child in node.get('children', []):
            recursive_search(child)

    for entry in data['msg']:
        recursive_search(entry)

    return dict(st_level_dict)

st_level_dict = group_ids_by_st_level(json_data)

def has_children_recursive(node, target_id):
    if node['id'] == target_id:
        return bool(node.get('children'))
    for child in node.get('children', []):
        if has_children_recursive(child, target_id):
            return True
    return False

def has_children(id, data):
    for entry in data['msg']:
        if has_children_recursive(entry, id):
            return True
    return False

def find_childless_ids(st_level_dict, data):
    childless_ids_dict = defaultdict(list)

    for st_level in st_level_dict:
        for id in st_level_dict[st_level]:
            if not has_children(id, data):
                childless_ids_dict[st_level].append(id)

    return dict(childless_ids_dict)

def merge_childless_ids_to_below_levels(childless_ids_dict, total_st_levels):
    merged_childless_ids_dict = defaultdict(list)
    
    for st_level in range(total_st_levels + 1):
        for parent_st_level in range(st_level):
            if parent_st_level in childless_ids_dict:
                merged_childless_ids_dict[st_level].extend(childless_ids_dict[parent_st_level])
        if st_level in childless_ids_dict:
            merged_childless_ids_dict[st_level].extend(childless_ids_dict[st_level])
            
    return dict(merged_childless_ids_dict)

def find_all_children_for_ids(data, target_ids):
    def recursive_collect_children(node, id_to_children_dict):
        if node['id'] in target_ids:
            all_descendants = []
            stack = [node]

            while stack:
                current_node = stack.pop()
                for child in current_node.get('children', []):
                    all_descendants.append(child['id'])
                    stack.append(child)

            id_to_children_dict[node['id']] = all_descendants

        for child in node.get('children', []):
            recursive_collect_children(child, id_to_children_dict)

    id_to_children_dict = {}

    for entry in data['msg']:
        recursive_collect_children(entry, id_to_children_dict)

    return id_to_children_dict

def get_descendants_for_st_level(json_data, st_level):
    grouped_ids = group_ids_by_st_level(json_data)
    ids_at_st_level = set(grouped_ids.get(st_level, []))

    if not ids_at_st_level:
        return {}

    descendants_mapping = find_all_children_for_ids(json_data, ids_at_st_level)

    return descendants_mapping

def merge_descendants_with_childless(descendants_mapping, merged_childless_ids, st_level):
    final_dict = defaultdict(list)
    for key, value in descendants_mapping.items():
        final_dict[key].extend(value)

    if st_level in merged_childless_ids:
        for id in merged_childless_ids[st_level]:
            if id not in final_dict:
                final_dict[id] = []

    return dict(final_dict)

def get_color_mapping(data):
    color_mapping = {}
    def recursive_collect_colors(node):
        color_mapping[node['id']] = node.get('color_hex_triplet', 'FFFFFF')
        for child in node.get('children', []):
            recursive_collect_colors(child)

    for entry in data['msg']:
        recursive_collect_colors(entry)
    
    return color_mapping

def hex_to_rgb(hex_color):
    hex_color = hex_color.strip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"{r};{g};{b}"

def add_rgb_color_row(dataframe, color_mapping):
    colors_row = []

    for column_name in dataframe.columns:
        hex_color = color_mapping.get(int(column_name), 'FFFFFF')
        rgb_color = hex_to_rgb(hex_color)
        colors_row.append(rgb_color)

    dataframe.loc[-1] = colors_row
    dataframe.index = dataframe.index + 1
    dataframe.sort_index(inplace=True)

    return dataframe

def fill_empty_first_row(dataframe):
    row = []
    for (columnName, columnData) in dataframe.items():
        col_name = columnName
        col_ids = columnData.values
        
        if col_ids[0] == 0:
            row.append(int(col_name))
        else:
            row.append(col_ids[0])

    dataframe.loc[0:0] = row

    return dataframe

def replace_zeros_with_empty_cells(dataframe):
    dataframe.replace(0, "", inplace=True)
    return dataframe

def get_name_mapping(data):
    name_mapping = {}
    def recursive_collect_names(node):
        name_mapping[node['id']] = node.get('name', str(node['id']))
        for child in node.get('children', []):
            recursive_collect_names(child)

    for entry in data['msg']:
        recursive_collect_names(entry)
    
    return name_mapping

def replace_column_headers_with_names(dataframe, name_mapping):
    dataframe.rename(columns=lambda x: name_mapping.get(int(x), str(x)), inplace=True)
    return dataframe

def hier_dict_to_custom_regions(hier_dict, color_mapping, name_mapping):
    hier_df = pd.DataFrame.from_dict(hier_dict, orient="index")
    hier_df_transposed = hier_df.transpose()
    hier_df_transposed = hier_df_transposed.fillna(0).astype(int)

    hier_df_transposed = fill_empty_first_row(hier_df_transposed)
    hier_df_transposed = replace_zeros_with_empty_cells(hier_df_transposed)
    hier_df_transposed = add_rgb_color_row(hier_df_transposed, color_mapping)
    hier_df_transposed = replace_column_headers_with_names(hier_df_transposed, name_mapping)

    return hier_df_transposed

def custom_regions_for_hier_level(data, hier_level):
    st_level_dict = group_ids_by_st_level(data)
    color_mapping = get_color_mapping(data)
    name_mapping = get_name_mapping(data)
    total_st_levels = max(st_level_dict.keys())

    if hier_level not in range(total_st_levels + 1):
        print(f"Error: chosen st level not available in hierarchy file. Choose a value between {range(total_st_levels + 1)[0]} and {total_st_levels + 1}.")
    else:
        print(f"Chosen st level is {hier_level}")

        childless_ids_dict = find_childless_ids(st_level_dict, data)
        merged_childless_ids_dict = merge_childless_ids_to_below_levels(childless_ids_dict, total_st_levels)
        descendants_at_st_level = get_descendants_for_st_level(data, hier_level)
        final_dict = merge_descendants_with_childless(descendants_at_st_level, merged_childless_ids_dict, hier_level)
        custom_regions_df = hier_dict_to_custom_regions(final_dict, color_mapping, name_mapping)

        first_col = pd.DataFrame({'Custom brain region': ["RGB colour", "Atlas Ids"]})
        custom_regions_df = pd.concat([first_col, custom_regions_df], axis=1)

        return custom_regions_df, hier_level

# Calculate the total number of levels
total_st_levels = max(group_ids_by_st_level(json_data).keys())

# Generate Excel files for each level
for hier_level in range(total_st_levels):
    custom_regions_df, hier_level = custom_regions_for_hier_level(json_data, hier_level)
    custom_regions_df = custom_regions_df.fillna(0)
    custom_regions_df = replace_zeros_with_empty_cells(custom_regions_df)
    custom_regions_df.to_excel(f"CustomRegions_AllenCCFv3_level{hier_level}.xlsx", index=False)
