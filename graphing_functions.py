# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 13:17:08 2022

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
import matplotlib.pyplot as plt




def get_descriptive_statistics(inputdf, filename, parameter = "None", sheetname = "Sheet1"):
    
    if parameter == "None":
        descriptives = inputdf.describe()
    else:
        descriptives = inputdf.groupby(parameter).describe()
    
    descriptives.to_excel(filename, sheet_name = sheetname)



def set_region_names(input_file):
    regionnames = pd.read_csv(input_file, sep=';', usecols = ['Region name'])
    regionnames = regionnames.values
    regionnames = regionnames.flatten()
    
    return regionnames
    

def set_region_colors(input_file, R_col = "R", G_col = "G", B_col = "B"):    
    regioncolors = pd.read_csv(input_file, sep=';', usecols = [R_col, G_col, B_col])
    regioncolors = regioncolors / 255
        
    rgb_colors = []

    for index, row in regioncolors.iterrows():
        rgb = (row[R_col], row[G_col], row[B_col])
        rgb_colors.append(rgb)
    
    return rgb_colors


def create_allen_bar_graph(filename, input_dir, color_list, region_list, figsize = (50,10), dpi = 80, ylim = [0, 50000]):

    plt.figure(figsize=(figsize))
    plt.bar(region_list, input_dir, color=color_list)
    plt.xticks(rotation=90) 
    plt.ylim(ylim)

    plt.savefig(filename + '_bar.svg', bbox_inches='tight')
    
    
def create_allen_hbar_graph(filename, input_dir, color_list, region_list, figsize = (10,50), dpi = 80, xlim = [0, 40000]):
    
    plt.figure(figsize=(figsize))
    plt.barh(region_list, input_dir, color=color_list)
    plt.xlim(xlim)
    
    plt.savefig(filename + 'hbar.svg', bbox_inches='tight')
    

# def group_allen_regions():
    
    # Create broader groups of regions based on allen hierarchy
    

# def complete_regions_list():    
    
# ids_to_custom = pd.read_excel(r"Y:\Dopamine_receptors\Analysis\resources\ID_to_custom_Newmaster.xlsx")
# mydict = ids_to_custom.set_index('region ID')['custom region'].to_dict()


# df.columns = ["Region ID", "Deformation in voxels", "Section", "Deformation in um"]
# df['Custom Region'] = df['Region ID'].map(mydict)
# df = df[["Section", "Region ID", "Deformation in voxels", "Deformation in um", "Custom Region"]]
# deformation_per_region = (df.groupby('Custom Region')["Deformation in um"].describe())