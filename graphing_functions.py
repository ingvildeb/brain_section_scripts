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
from matplotlib.pyplot import figure


def unique_list(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


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
    

def set_region_colors(input_file, file_type, R_col = "R", G_col = "G", B_col = "B"):

    if file_type == "csv":    
        regioncolors = pd.read_csv(input_file, sep=';', usecols = [R_col, G_col, B_col])
        
    if file_type == "excel":
        regioncolors = pd.read_excel(input_file, usecols = [R_col, G_col, B_col])
        
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
    



## function to create a dict of maximum values for regions within a hierarchical level


def create_maxval_dict(customregsfile, superregions_col, regions_col, datafiles):
    maxval_list = []
    read_customregs = pd.read_csv(customregsfile, sep = ";")  
    superregion_list = ((read_customregs[superregions_col]).unique()).tolist()
    print(superregion_list)

    
    data = pd.concat(datafiles)
    for sreg in superregion_list:       
        regs_in_superreg = (read_customregs[(read_customregs[superregions_col] == sreg)])[regions_col].tolist()
        flat_list = np.array([data[region].values for region in regs_in_superreg])
        flat_list[np.isnan(flat_list)] = 0        
        maxval = flat_list.max()

        
        maxval_list.append(maxval)
        maxval_dict = dict(zip(superregion_list, maxval_list))
    return(maxval_dict)
    

    



## function to create line graphs per hierarchical level

def create_line_graphs_per_hierarchy_level(customregsfile, superregions_col, regions_col, maxval_dict, datafile, plot_prefix = ""):
    
    read_customregs = pd.read_csv(customregsfile, sep = ";")  
    superregion_list = ((read_customregs[superregions_col]).unique()).tolist()    
    
    for sreg in superregion_list:
        figure(figsize = (20,10), dpi=80)
    
        regs_in_superreg = ((read_customregs[(read_customregs[superregions_col] == sreg)])[regions_col]).tolist()
        regs_in_superreg = unique_list(regs_in_superreg)
                
        ylim = maxval_dict.get(sreg)
   
        for region in regs_in_superreg:            
            data = datafile[region]
            plt.plot(data, label = region)
        
        plt.ylim(0, (ylim + 1000))
        plt.rc('font', size=10)
        plt.legend()
        plt.savefig(plot_prefix + str(sreg) + '.svg', bbox_inches='tight')    
        plt.show()



############# this is a test








# def complete_regions_list():    
    
# ids_to_custom = pd.read_excel(r"Y:\Dopamine_receptors\Analysis\resources\ID_to_custom_Newmaster.xlsx")
# mydict = ids_to_custom.set_index('region ID')['custom region'].to_dict()


# df.columns = ["Region ID", "Deformation in voxels", "Section", "Deformation in um"]
# df['Custom Region'] = df['Region ID'].map(mydict)
# df = df[["Section", "Region ID", "Deformation in voxels", "Deformation in um", "Custom Region"]]
# deformation_per_region = (df.groupby('Custom Region')["Deformation in um"].describe())























