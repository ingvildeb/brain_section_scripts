# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 14:35:34 2022

@author: ingvieb
"""


import pandas as pd

resourcedir = 'Y:/Dopamine_receptors/Analysis/resources//'
metadata = resourcedir + "ids_for_nut_files.xlsx"


subjects = pd.read_excel(metadata)




def write_nut_quant_file(filename, nut_type = "Quantifier", name = "", analysis_type = "QUINT", quantifier_input_dir = "", 
                   quantifier_atlas_dir = "", label_file = "Allen Mouse Brain 2015", custom_label_file = "",
                   xml_anchor_file = "", quantifier_output_dir = "", output_report = "All", extraction_color = "255,0,0,255", 
                   object_splitting = "Yes", object_min_size = "1", global_pixel_scale = "1", quantifier_pixel_scale_unit = "pixels", 
                   use_custom_masks = "No", custom_mask_directory = "", custom_mask_color = "255,255,255,255", output_report_type = "CSV", 
                   custom_region_type = "Default", custom_region_file = "", coordinate_extraction = "All", pixel_density = "1", 
                   display_label_id = "No", output_region_id = "Yes", pattern_match = "_sXXX", files = "", nutil_version = "v0.8.0"):    

    
    file_cells = open("Y:/Dopamine_receptors/Analysis/nut_files/" + filename + ".txt", "w+")
    
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
    

ID = subjects["ID"]
genotype = subjects["Genotype"]
age = subjects["Age"]
sex = subjects["Sex"]

# Write files to extract cells:
    
for i, g, a, s in zip(ID, genotype, age, sex):
    if a == "P49" or a == "P70":
        write_nut_quant_file(filename = i + "_cells", quantifier_input_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/05_masked_segmentations", 
                       quantifier_atlas_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/06_atlas_maps",
                       xml_anchor_file = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/00_nonlin_registration_files/" + i + "_nonlinear.json",
                       quantifier_output_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/07_nutil/01_output_cells",
                       custom_region_file = "Y:/Dopamine_receptors/Analysis/resources/CustomRegions_Allen2017_DOPAMAP.xlsx", extraction_color = "255,0,255,255", label_file = "Allen Mouse Brain 2017",
                       object_splitting = "No", object_min_size = "4", custom_region_type = "Custom")
    if a == "P35" or a == "P25" or a == "P17":
        write_nut_quant_file(filename = i + "_cells", quantifier_input_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/05_masked_segmentations", 
                       quantifier_atlas_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/06_atlas_maps",
                       xml_anchor_file = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/00_nonlin_registration_files/" + i + "_nonlinear.json",
                       quantifier_output_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/07_nutil/01_output_cells",
                       custom_region_file = "Y:/Dopamine_receptors/Analysis/resources/CustomRegions_Allen2017_Newmaster.xlsx", extraction_color = "255,0,255,255", label_file = "Custom",
                       custom_label_file = "Y:/Dopamine_receptors/Analysis/resources/atlas_volumes/labels_rev_CCF-colors.txt", object_splitting = "No", object_min_size = "4", custom_region_type = "Custom")
        
        
# Write files to extract masks:
    
for i, g, a, s in zip(ID, genotype, age, sex):
    if a == "P49" or a == "P70":
        write_nut__quantfile(filename = i + "_masks", quantifier_input_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/05_masked_segmentations", 
                       quantifier_atlas_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/06_atlas_maps",
                       xml_anchor_file = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/00_nonlin_registration_files/" + i + "_nonlinear.json",
                       quantifier_output_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/07_nutil/02_output_masks",
                       custom_region_file = "Y:/Dopamine_receptors/Analysis/resources/CustomRegions_Allen2017_DOPAMAP.xlsx", extraction_color = "0,0,0,255", label_file = "Allen Mouse Brain 2017",
                       object_splitting = "No", object_min_size = "4", custom_region_type = "Custom")
    if a == "P35" or a == "P25" or a == "P17":
        write_nut_quant_file(filename = i + "_masks", quantifier_input_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/05_masked_segmentations", 
                       quantifier_atlas_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/06_atlas_maps",
                       xml_anchor_file = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/00_nonlin_registration_files/" + i + "_nonlinear.json",
                       quantifier_output_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/07_nutil/02_output_masks",
                       custom_region_file = "Y:/Dopamine_receptors/Analysis/resources/CustomRegions_Allen2017_Newmaster.xlsx", extraction_color = "0,0,0,255", label_file = "Custom",
                       custom_label_file = "Y:/Dopamine_receptors/Analysis/resources/atlas_volumes/labels_rev_CCF-colors.txt", object_splitting = "No", object_min_size = "4", custom_region_type = "Custom")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        