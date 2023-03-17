# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 09:45:33 2022

@author: ingvieb
"""

import os
import pandas as pd
import glob
import re
import numpy as np
import xlwt
from xlwt.Workbook import *
from pandas import ExcelWriter
import xlsxwriter
from scipy.interpolate import interp1d
import math



def set_region_names(customregsfile):
    
    regionnames = pd.read_csv(customregsfile, sep=';', usecols =['Region name'])
    list_of_regionnames = regionnames.values
    list_of_regionnames = list_of_regionnames.flatten()
    
    return list_of_regionnames

def create_section_list(all_files_list, split_point_1 = "_s", split_point_2 = "."):
    ## Create list of Section numbers, to be used as index:
        
    list_of_sections = []
    
    for f in all_files_list:
        f = f.split(split_point_1)[1]
        f = f.split(split_point_2)[0]
        f = int(f)
        list_of_sections.append(f)
        
    return list_of_sections

def create_full_section_list(list_of_sections):                    

    complete_section_list = np.arange(1, ((list_of_sections[-1])+1))
    complete_section_list = complete_section_list.tolist()
    
    return complete_section_list

def identify_missing_sections(complete_section_list, list_of_sections):

    list_of_missing_sections = []
    
    for number in complete_section_list:
        if number not in list_of_sections:
            list_of_missing_sections.append(number)
            
    return list_of_missing_sections

def create_missing_sections_df(list_of_missing_sections, list_of_regionnames):
    # Make a dataframe filled with nans for the missing sections 

    missing_sections_df = np.zeros((len(list_of_missing_sections), len(list_of_regionnames)))
    missing_sections_df[:] = np.nan
    missing_sections_df = pd.DataFrame(missing_sections_df)
    missing_sections_df.insert(0, " ", list_of_missing_sections, True)
    missing_sections_df.columns = ["Section", *list_of_regionnames]
    
    return missing_sections_df
     

def format_dataframe(dataframe, list_of_sections, list_of_regionnames, missing_sections_df):
    #add section number column and column names to dataframe:
    
    df_formatted = dataframe.copy()
        
    df_formatted.insert(0, "Section", list_of_sections, True)
    df_formatted.columns = ["Section", *list_of_regionnames]
    
    df_formatted = pd.concat([df_formatted, missing_sections_df])
    df_formatted = df_formatted.sort_values(by=['Section'])
    df_formatted = df_formatted.reset_index(drop=True)
    df_formatted = df_formatted.set_index('Section')
    
    
    return df_formatted

def compile_nut_customregions_reports(list_of_files, column):
    """

    Parameters
    ----------
    list_of_files : TYPE
        DESCRIPTION.
    column : TYPE
        DESCRIPTION.

    Returns
    -------
    compiled_df : TYPE
        DESCRIPTION.

    """
    # CREATE DATAFRAME FROM NUT REPORTS
    
    list_of_columns = []
    
    for f in list_of_files:
        col = pd.read_csv(f, sep=';', usecols=[column])
        list_of_columns.append(col)
    
    compiled_df = pd.concat(list_of_columns, axis=1, join='outer') 
    compiled_df = compiled_df.transpose()
    compiled_df = compiled_df.reset_index(drop=True)  
    
    return compiled_df

def describe_object_sizes(objects_all_file):
    # CREATE DATAFRAME WITH MEAN OBJECT PIXEL SIZE
    
    objects_all = pd.read_csv(objects_all_file, sep=';')

    ### Estimate mean object size per Custom Region:
    object_mean_pixels = (objects_all.groupby('Custom Region')["Object pixels"].describe())
    object_mean_pixels = object_mean_pixels.reset_index('Custom Region')

    object_mean_pixels = object_mean_pixels[['Custom Region', 'mean']]
    
    return object_mean_pixels

def identify_missing_customregions(file, list_of_regionnames):

    added_regions = []

    for region in list_of_regionnames:
        if region not in file['Custom Region'].values:
            added_regions.append(region)
            
    return added_regions

def create_missing_customregions_df(added_regions, column_head):
    
    added_regions = pd.DataFrame(added_regions, columns=['Custom Region'])
    values = np.zeros((len(added_regions), 1))
    values[:] = np.nan
    values = pd.DataFrame(values)
    df = pd.concat([added_regions, values], axis=1)
    df.columns = ["Custom Region", column_head]
    return df

def complete_and_sort_object_counts(objects_file, list_of_regionnames):    
    
    ### ENSURE ALL REGIONS ARE IN OBJECT MEAN SIZES DATAFRAME AND SORTED CORRECTLY
    # The object files and thus the summary statistics only includes information about regions that have objects. To amend this, find the regions that are not in the object pixel reports:

    added_regions = identify_missing_customregions(objects_file, list_of_regionnames)
    added_regions_df = create_missing_customregions_df(added_regions, column_head = "mean")
    all_object_sizes = pd.concat([objects_file, added_regions_df])
    
    #create a mapping column based on the sorting in the reports containing counts and masks (hierarchical sorting according to CCF) for custom sorting of regions:
    mapping_column = pd.DataFrame({'Custom Region': list_of_regionnames})
    sort_mapping = mapping_column.reset_index().set_index('Custom Region')
    
    #apply sorting to dataframe with object mean sizes:
    all_object_sizes['Sorted Regions'] = all_object_sizes['Custom Region'].map(sort_mapping['index'])
    all_object_sizes = all_object_sizes.sort_values('Sorted Regions')
    all_object_sizes = all_object_sizes[['Custom Region', 'mean']]
    
    all_object_sizes = all_object_sizes.transpose()
    
    all_object_sizes = all_object_sizes[1:]
    all_object_sizes.columns = list_of_regionnames
    
    return all_object_sizes

def calculate_object_diameters(object_sizes_file, list_of_regionnames, pixel_size):

    object_mean_areas = object_sizes_file * pixel_size
    object_mean_areas = object_mean_areas.values
    object_mean_areas = object_mean_areas.astype(float)
    object_mean_diameters = 2 * (np.sqrt(object_mean_areas / math.pi))
    
    object_mean_diameters = pd.DataFrame(object_mean_diameters)
    object_mean_diameters.columns = list_of_regionnames
    
    return object_mean_diameters

def get_hidden_mask_load(file, list_of_sections):

    df_hidden_mask_load = pd.read_excel(file)
    
    #select only the rows with section numbers included in the analysis (hidden mask load file may include more because some were excluded at a later stage):
    df_hidden_mask_load = df_hidden_mask_load[df_hidden_mask_load["Section number"].isin(list_of_sections)]          
    
    #fill nan values with zeros and set those with less than 10% mask to zero:                    
    df_hidden_mask_load = df_hidden_mask_load.fillna(0)
    df_hidden_mask_load = np.where(df_hidden_mask_load < 0.1, '0', df_hidden_mask_load)
    
    #convert to dataframe and delete column with section numbers from the hidden mask load file:
    df_hidden_mask_load = pd.DataFrame(df_hidden_mask_load)
    df_hidden_mask_load = df_hidden_mask_load.drop(columns = [0])           

    
    return df_hidden_mask_load



def mask_correction(df_object_counts, df_region_areas, df_mask_load, df_hidden_mask_load, pixel_size, complete_section_list):
    
    #the total mask load is the sum of the mask load extracted from images and the hidden mask load extracted from comparison with "ideal" atlas plates
    totalmaskload = df_mask_load + df_hidden_mask_load
    
    # region areas are multiplied by pixel size to give area in um2. region area is then corrected to account for the hidden areas.
    region_areas = df_region_areas * pixel_size
    maskcorrected_region_area = (region_areas / (1 - df_hidden_mask_load))
    
    # object counts are corrected by the total mask load (visible + hidden). where the total mask load is > 90%, counts are considered not available and value is set to NaN.
    maskcorrected_object_counts = (df_object_counts / (1 - totalmaskload))
    maskcorrected_object_counts[totalmaskload > 0.90] = np.nan
    
    
    return maskcorrected_object_counts, maskcorrected_region_area



def abercrombie_correction(object_mean_diameters, maskcorrected_object_counts, complete_section_list, section_thickness):
    
     # # CORRECT RESULTING OBJECT COUNTS BY ABERCROMBIES FORMULA

     # extend the object diameters by the number of sections
     object_diameters = pd.concat([object_mean_diameters]*len(complete_section_list), ignore_index=True)
     object_diameters.insert(0, "Section", complete_section_list, True)
     object_diameters = object_diameters.set_index('Section')
     
     # correct the raw numbers with Abercrombies formula: (object count*40)/(40+mean object size)
     abcorrected_object_counts = (maskcorrected_object_counts * section_thickness) / (section_thickness + object_diameters)
     
     return abcorrected_object_counts


def calculate_densities(abcorrected_object_counts, maskcorrected_region_area, section_thickness):
    densities_2D = (abcorrected_object_counts / maskcorrected_region_area)
    densities_3D = ((densities_2D / 40)*(10**9))
    
    # replace the nans where the region area is 0 with 0
    replaceNans = maskcorrected_region_area == 0
    densities_2D[replaceNans] = 0
    densities_3D[replaceNans] = 0
    
    return densities_2D, densities_3D
   

def interpolate_data(dataframe, complete_section_list):

    aranged = np.array(complete_section_list)
    for column in dataframe.columns:
        y = dataframe[column].values
        #this lets me remove nan from the interpolation
        valid = np.nonzero(~np.isnan(y))
        if len(valid[0])<=1:
            dataframe[column] = 0 
            continue
        f = interp1d(aranged[valid], y[valid], axis=-1, kind='linear', fill_value='extrapolate')
        y = f(aranged)
        dataframe[column] = y
        
    # less-than-zero values may result from the interpolation. these should be set to 0.
    mask = dataframe < 0
    dataframe[mask] = 0

    return dataframe



















