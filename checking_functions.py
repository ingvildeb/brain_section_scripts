# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 11:10:43 2023

@author: ingvieb
"""

from glob import glob
import pandas as pd
from colorama import Fore, Back, Style



   
    

def get_renaming_dict(rename_file):

    rename_scheme = pd.read_excel(rename_file)

    input_names = list(rename_scheme["Input file name"])
    renamed_names = list(rename_scheme["Renamed"])
    
    orig_name_list = []
    new_name_list = []
    
    for name in input_names:
        orig_name = name.split(".")[0]
        orig_name_list.append(orig_name)
        
    for name in renamed_names:
        new_name = name.split(".")[0]
        new_name_list.append(new_name)
        

    dict_of_renaming = dict(zip(orig_name_list, new_name_list))
    
    return dict_of_renaming, orig_name_list, new_name_list

            

def check_files_in_folders(folder1, folder2, folder1ext, folder2ext):
    
    folder1files = glob(folder1 + "*" + folder1ext)
    folder2files = glob(folder2 + "*" + folder2ext)
    
    if len(folder1files) == len(folder2files):
        message = "done"
        print("All files are done!")
        
    else:
        message = "not done"
        print(Back.RED + len(folder2files), " of the", len(folder1files), " files are done")
    
    return message
    
    
def name_files_in_folders(folder1, folder2, folder1ext, folder2ext):
    
    folder1files = glob(folder1 + "*" + folder1ext)
    folder2files = glob(folder2 + "*" + folder2ext)
    
    folder1file_names = []
    
    for file in folder1files: 
        folder1file_name = (file.split("\\")[-1]).split(".")[0]
        
        folder1file_names.append(folder1file_name)
        
        if "_thumbnail" in file:
            folder1file_name = folder1file_name.split("_thumbnail")[0]
        else:
            folder1file_name = folder1file_name  
    
    folder2file_names = []
    
    for file in folder2files: 
        folder2file_name = (file.split("\\")[-1]).split(".")[0]
        
        if "_thumbnail" in file:
            folder2file_name = folder2file_name.split("_thumbnail")[0]
        else:
            folder2file_name = folder2file_name            
            
        folder2file_names.append(folder2file_name)
        
    
    return folder1file_names, folder2file_names
        
        

def identify_missing_files(folder1files, folder2files, dict_of_correspondence = ""):
            
    missing_files = []
    missing_files_renamed = []
    
    if dict_of_correspondence:
    
        for file in folder1files:
            
            folder2file = dict_of_correspondence[file]
            
            if folder2file in folder2files:
                continue
            else:
                missing_files.append(file)
                missing_files_renamed.append(folder2file)
                
        return missing_files, missing_files_renamed
    
    else:
        
        for file in folder1files:
            if file.split(".")[0] in folder2files:
                continue
            else:
                missing_files.append(file)
        return missing_files
            
    
    
    
def create_missing_files_df(missing_files, transformsheet = ""):
    
    if transformsheet:
        read_transformsheet = pd.read_excel(transformsheet)
        df_list = []
        
        for file in missing_files:
            row = read_transformsheet[read_transformsheet['Input file name'].str.contains(file)]
            df_list.append(row)
        
        missing_rows = pd.concat(df_list)    
        
        return missing_rows
    
    else:
        df_list = []
        
        for file in missing_files:
            data = {'Input file name':[file], 'Renamed':[file], 'Rotation CCW':['0'], 'Scale X':['1'], 'Scale Y':['1']}
            row = pd.DataFrame(data)
            df_list.append(row)
            
        missing_rows = pd.concat(df_list)
        
        return missing_rows
    


















