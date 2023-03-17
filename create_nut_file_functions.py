# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 09:52:16 2023

@author: ingvieb
"""




def write_nut_quant_file(filename, storepath, nut_type = "Quantifier", name = "", analysis_type = "QUINT", quantifier_input_dir = "", 
                   quantifier_atlas_dir = "", label_file = "Allen Mouse Brain 2015", custom_label_file = "",
                   xml_anchor_file = "", quantifier_output_dir = "", output_report = "All", extraction_color = "255,0,0,255", 
                   object_splitting = "Yes", object_min_size = "1", global_pixel_scale = "1", quantifier_pixel_scale_unit = "pixels", 
                   use_custom_masks = "No", custom_mask_directory = "", custom_mask_color = "255,255,255,255", output_report_type = "CSV", 
                   custom_region_type = "Default", custom_region_file = "", coordinate_extraction = "All", pixel_density = "1", 
                   display_label_id = "No", output_region_id = "Yes", pattern_match = "_sXXX", files = "", nutil_version = "v0.8.0"):    

    
    file_cells = open(storepath + filename + ".nut", "w+")
    
    file_cells.write(f"type = {nut_type}\n")    
    file_cells.write(f"name = {name}\n")   
    file_cells.write(f"analysis_type = {analysis_type}\n")
    file_cells.write(f"quantifier_input_dir = {quantifier_input_dir}\n")
    file_cells.write(f"quantifier_atlas_dir = {quantifier_atlas_dir}\n")  
    file_cells.write(f"label_file = {label_file}\n")   
    file_cells.write(f"custom_label_file = {custom_label_file}\n")
    file_cells.write(f"xml_anchor_file = {xml_anchor_file}\n")
    file_cells.write(f"quantifier_output_dir = {quantifier_output_dir}\n")
    file_cells.write(f"output_report = {output_report}\n")
    file_cells.write(f"extraction_color = {extraction_color}\n")
    file_cells.write(f"object_splitting = {object_splitting}\n")
    file_cells.write(f"object_min_size = {object_min_size}\n")
    file_cells.write(f"global_pixel_scale = {global_pixel_scale}\n")
    file_cells.write(f"quantifier_pixel_scale_unit = {quantifier_pixel_scale_unit}\n")
    file_cells.write(f"use_custom_masks = {use_custom_masks}\n")
    file_cells.write(f"custom_mask_directory = {custom_mask_directory}\n")
    file_cells.write(f"custom_mask_color = {custom_mask_color}\n")
    file_cells.write(f"output_report_type = {output_report_type}\n")
    file_cells.write(f"custom_region_type = {custom_region_type}\n")
    file_cells.write(f"custom_region_file = {custom_region_file}\n")
    file_cells.write(f"coordinate_extraction = {coordinate_extraction}\n")
    file_cells.write(f"pixel_density = {pixel_density}\n")    
    file_cells.write(f"display_label_id = {display_label_id}\n")    
    file_cells.write(f"output_region_id = {output_region_id}\n")    
    file_cells.write(f"pattern_match = {pattern_match}\n")    
    file_cells.write(f"files = {files}\n")    
    file_cells.write(f"nutil_version = {nutil_version}\n")
    
    file_cells.close()
    
    
    
def write_nut_transform_file(filename, storepath, nut_type = "Transform", name = "", output_compression = "lzw", transform_input_dir = "", 
                             transform_output_dir = "", auto_crop = "yes", transform_background_color = "255,255,255,255",
                             transform_color_spread = "", transform_files = "", only_thumbnails = "No", transform_thumbnail_size = "0.1"):

    file_cells = open(storepath + filename + ".nut", "w+")
    
    file_cells.write(f"type = {nut_type}\n")    
    file_cells.write(f"name = {name}\n")   
    file_cells.write(f"output_compression = {output_compression}\n")
    file_cells.write(f"transform_input_dir = {transform_input_dir}\n")
    file_cells.write(f"transform_output_dir = {transform_output_dir}\n")  
    file_cells.write(f"auto_crop = {auto_crop}\n")   
    file_cells.write(f"transform_background_color = {transform_background_color}\n")
    file_cells.write(f"transform_color_spread = {transform_color_spread}\n")
    file_cells.write(f"transform_files = {transform_files}\n")
    file_cells.write(f"only_thumbnails = {only_thumbnails}\n")
    file_cells.write(f"transform_thumbnail_size = {transform_thumbnail_size}\n")
    
    file_cells.close()    
    
    

#file_cells = open("Y:/Dopamine_receptors/Analysis/nut_files/" + filename + ".nut", "w+")