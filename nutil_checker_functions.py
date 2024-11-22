# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:59:47 2024

@author: ingvieb
"""

import glob
import os
import shutil

def flatten_extend(matrix):
     flat_list = []
     for row in matrix:
         flat_list.extend(row)
     return flat_list

def split_list(lst, chunk_size):
    # Use a list comprehension to create chunks
    # For each index 'i' in the range from 0 to the length of the list with step 'chunk_size'
    # Slice the list from index 'i' to 'i + chunk_size'
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def read_nut_transform_file(nutil_file):  

    with open(nutil_file, 'r') as file:
    
        lines = file.readlines()
        
        for line in lines:
            if line.find("transform_input_dir") != -1:
                transform_input_dir = line
                transform_input_dir = transform_input_dir.split("= ")[-1].split("\n")[0]
            if line.find("transform_output_dir") != -1:
                transform_output_dir = line
                transform_output_dir = transform_output_dir.split("= ")[-1].split("\n")[0]
            if line.find("transform_files") != -1:
                transform_files = line
                transform_files = transform_files.split("= ")[-1].split("\n")[0]
            if line.find("only_thumbnails") != -1:
                only_thumbnails = line
                only_thumbnails = only_thumbnails.split("= ")[-1].split("\n")[0]
                
    return transform_input_dir, transform_output_dir, transform_files, only_thumbnails


def read_nut_resize_file(nutil_file):
    
    with open(nutil_file, 'r') as file:
    
        lines = file.readlines()
        
        for line in lines:
            if line.find("resize_input_dir") != -1:
                resize_input_dir = line
                resize_input_dir = resize_input_dir.split("= ")[-1].split("\n")[0]
            if line.find("resize_output_dir") != -1:
                resize_output_dir = line
                resize_output_dir = resize_output_dir.split("= ")[-1].split("\n")[0]
                
    return resize_input_dir, resize_output_dir


def parse_transform_string(transform_string):
        split_transform_string = transform_string.split(",")
        file_parameters = split_list(split_transform_string, 5)
        
        return file_parameters


def find_missing_files(transform_input_dir, transform_output_dir, file_parameters, extension="tif", thumbnails="no"):
    
    files = glob.glob(rf"{transform_output_dir}/*.{extension}")
    
    if thumbnails == "no":
        file_names = [os.path.basename(file).split(".")[0] for file in files]
        
    elif thumbnails == "yes":
        file_names = [os.path.basename(file).split("_thumbnail")[0] for file in files]
        
    missing_files_list = []
    
    for file in file_parameters:
        
            output_name = file[1].split(".")[0]
            if output_name in file_names:
                continue
            else:
                missing_files_list.append(file)

    return missing_files_list

            
def check_nut_file(nut_file):
    
    transform_input_dir, transform_output_dir, transform_files, only_thumbnails = read_nut_transform_file(nut_file)
    thumbs_dir = fr"{transform_output_dir}/thumbnails/"
    file_parameters = parse_transform_string(transform_files)

    if only_thumbnails == "Yes":
        missing_files = find_missing_files(transform_input_dir, thumbs_dir, file_parameters, extension="png", thumbnails="yes")
        
        return missing_files
        
    elif only_thumbnails == "No":
        missing_files = find_missing_files(transform_input_dir, transform_output_dir, file_parameters)
        missing_thumbs = find_missing_files(transform_input_dir, thumbs_dir, file_parameters, extension="png", thumbnails="yes")

        return missing_files, missing_thumbs
            
    
    

def check_nut_resize_file(nut_file, extension):
    resize_input_dir, resize_output_dir = read_nut_resize_file(nut_file)
    
    input_files = glob.glob(f"{resize_input_dir}/*.{extension}")
    output_files = glob.glob(f"{resize_output_dir}/*.{extension}")
    
    if len(input_files) == len(output_files):
        message = "done"
    
    else:
        message = "not done"

    
    return message, len(input_files), len(output_files)
    


def missing_files_to_string(missing_files):
        flat_list = flatten_extend(missing_files)
        nut_string = ",".join(flat_list)
        
        return nut_string
    

                
                
def change_nut_file_files(nut_file, nut_string):
    # Read the file contents into a list of lines
    with open(nut_file, 'r') as file:
        lines = file.readlines()

    # Modify the line that starts with the specific string
    for i, line in enumerate(lines):
        if line.startswith("transform_files"):
            lines[i] = nut_string + '\n'
            break
    else:
        print("No transform files found in the original file.")

    # Write the modified lines back to the file
    with open(nut_file, 'w') as file:
        file.writelines(lines)                
                
                
    
    
    
    
    