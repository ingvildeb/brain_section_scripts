# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 12:10:21 2023

@author: ingvieb
"""

import json
import pandas as pd


def unique_list(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]



########## VARIABLES TO CHANGE BEFORE RUNNING: ###############

# enter a prefix for your output file
outfile_prefix = "C19"

#specify the path to your json file
my_json = open(r"Y:/Dopamine_receptors/Analysis/QUINT_analysis/D1R/P70/D1R_P70_M_C19/07_nutil/01_output_cells/Coordinates/3D_combined.json")
customregsfile = r"Y:/Dopamine_receptors/Analysis/resources/customregions.csv"

##############################################################


## Read custom regions file:

read_customregs = pd.read_csv(customregsfile, sep = ";")


## list regions at various levels of hierarchy
hierarchy_regs = (read_customregs['Hierarchy'].unique()).tolist()
major_regs = (read_customregs['Hierarchy_major'].unique()).tolist()
medium_hier_regs = (read_customregs['Hierarchy_medium'].unique()).tolist()


regions_to_hierarchy_dict = dict(zip(read_customregs['Region name'], read_customregs['Hierarchy']))

regions_to_R_dict = dict(zip(read_customregs['Region name'], read_customregs["R_hier"]))
regions_to_G_dict = dict(zip(read_customregs['Region name'], read_customregs["G_hier"]))
regions_to_B_dict = dict(zip(read_customregs['Region name'], read_customregs["B_hier"]))
                            
data = json.load(my_json)

for hreg in hierarchy_regs:
    
    included_regions = [k for k,v in regions_to_hierarchy_dict.items() if v == hreg]
    regions_to_hierarchy_dict[hreg] = included_regions  
    
    r_color_list = []
    g_color_list = []
    b_color_list = []
    
    for reg in included_regions:
        r_color = regions_to_R_dict[reg]
        g_color = regions_to_G_dict[reg]
        b_color = regions_to_B_dict[reg]
        
        r_color_list.append(r_color)
        g_color_list.append(g_color)
        b_color_list.append(b_color)
        
    r_color = r_color_list[0]
    g_color = g_color_list[0]
    b_color = b_color_list[0]

    
    region_list = []

    included_region_data = [i for i in data if i['name'] in included_regions]
    
    for region_data in included_region_data:
            idx = region_data["idx"]
            count = region_data["count"]
            name = region_data["name"]
            triplets = region_data["triplets"]
            dictionary = {"idx": idx, "count": count, "r":r_color, "g":g_color, "b":b_color, "name": name, "triplets": triplets}
            region_list.append(dictionary)
            
            
    with open(outfile_prefix + "_" + hreg + ".json", "w") as outfile:
        json.dump(region_list, outfile)
        
    print("done with " + hreg)













