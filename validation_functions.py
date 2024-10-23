# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 11:57:31 2024

@author: ingvieb
"""

import pandas as pd
import re


def check(list):
    return all(i == list[0] for i in list)

def validate_transform_parameters(file, number_of_channels):

    transform_sheet = pd.read_excel(file)
    
    snums = []
    
    for i in transform_sheet["Renamed"].tolist():
        snum = re.findall("[s][0-9][0-9][0-9]", i)
        snums.append(snum[0])
    
    transform_sheet['Section'] = snums
    unique_snums = []
    [unique_snums.append(x) for x in snums if x not in unique_snums]
    
    
    for snum in unique_snums:
        
        rows = transform_sheet.loc[transform_sheet["Section"] == snum]

        if len(rows) != number_of_channels:
            print(f"{str(snum)} has {len(rows)} channels!")
            
        rotation = rows["Rotation CCW"].tolist()
        scale_x = rows["Scale X"].tolist()
        scale_y = rows["Scale Y"].tolist()
        
        if check(rotation) == False:
            print(f"{str(snum)} has mismatching rotations!")
    
        if check(scale_x) == False:
            print(f"{str(snum)} has mismatching scale_x!")
    
        if check(scale_y) == False:
            print(f"{str(snum)} has mismatching scale_y!")
            


def check_for_duplicate_names(file):
    
    nameList = pd.read_excel(file)
    nameList = nameList["Renamed"].tolist()
    dup = [x for x in nameList if nameList.count(x) > 1]
    
    if len(dup) > 0:
        print(f"The following duplicate names were found: {dup}. Please inspect and correct manually in renaming scheme.")
    else:
        print("No duplicate names found. Transform sheet good to go.")
            






















