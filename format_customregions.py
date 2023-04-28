# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 18:43:29 2022

@author: ingvieb
"""

import pandas as pd
import numpy as np
import glob
import os


resourcedir = 'Y:/Dopamine_receptors/Analysis/resources//'
customregsfile = resourcedir + 'customregions.csv'

customregions = r"Y:\Dopamine_receptors\Analysis\resources//" + "CustomRegions_Allen2017_Newmaster.xlsx"


customregions = pd.read_excel(customregions, usecols="B:GY")
customregions = customregions[2:]
customregions = pd.DataFrame(customregions)

regionnames = pd.read_csv(customregsfile, sep=';', usecols =['Region name'])
regionnames = regionnames.values
regionnames = np.insert(regionnames, 0, 'Sections', axis=None)

# convert custom regions into a dataframe with column for id and customregion name

df = pd.DataFrame()

for column in customregions:

    selection = customregions[column]
    selection = pd.DataFrame(selection)
    selection = selection.dropna()
    value = str(selection.columns)
    value = value[8:-19]
    selection.insert(1, "custom region", value)
    selection.columns = ["region ID", "custom region"]
    #print(selection)
    df = pd.concat((df,selection))
    
    
writer = pd.ExcelWriter(resourcedir + "ID_to_custom_Newmaster" + '.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='ID_to_custom_Newmaster', index=False)
writer.save()

# convert the dataframe for custom regions into a dictionary with region ID as the key, used to map ids to names later

mydict = df.set_index('region ID')['custom region'].to_dict()