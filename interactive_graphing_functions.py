# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 15:10:28 2023

@author: ingvieb
"""

#### CREATE LINE PLOTS FOR HIGHER HIERARCHICAL REGIONS


import pandas as pd
import mpld3
from mpld3 import plugins
from mpld3.utils import get_id
import numpy as np
import collections
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure  
from mpl_toolkits.mplot3d import Axes3D
import nutil_scripts.graphing_functions as grf

def unique_list(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


############### SET UP DATA PATHS

# density data at lowest hierarchy level (custom regions as defined in nutil)
D1R_densities_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D1R_densities.xlsx"
D1R_densities = pd.read_excel(D1R_densities_path)
D1R_densities["Area prostriata"] = np.nan

D2R_densities_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D2R_densities.xlsx"
D2R_densities = pd.read_excel(D2R_densities_path)
D2R_densities["Area prostriata"] = np.nan


# density data at high level of the hierarchy (17 major brain regions as defined in the paper)
D1R_densities_hier_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D1R_hierarchical_densities.xlsx"
D1R_densities_hier = (pd.read_excel(D1R_densities_hier_path)).iloc[0:, 1:]

D2R_densities_hier_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D2R_hierarchical_densities.xlsx"
D2R_densities_hier = (pd.read_excel(D2R_densities_hier_path)).iloc[0:, 1:]

## Get custom region names from excel file:
resourcedir = 'Y:/Dopamine_receptors/Analysis/resources//'
customregsfile = resourcedir + 'customregions.csv'
read_customregs = pd.read_csv(customregsfile, sep = ";")


## Get counts and mean values per age group
D1R_count = (D1R_densities.groupby("age").count()).iloc[0:,2:]
D2R_count = (D2R_densities.groupby("age").count()).iloc[0:,2:]

D1R_densities_mean = D1R_densities.groupby("age").mean()
D2R_densities_mean = D2R_densities.groupby("age").mean()    

D1R_densities_hier_mean = D1R_densities_hier.groupby("age").mean()
D2R_densities_hier_mean = D2R_densities_hier.groupby("age").mean()


### D1R
color_list_hier = grf.set_region_colors(customregsfile, file_type = "csv", R_col = "R_hier", G_col = "G_hier", B_col = "B_hier")
color_list_hier = unique_list(color_list_hier)
ls_list_hier = ['-', ':','--', '-.', '-', ':','--', '-.', '-', ':','--', '-.', '-', ':','--', '-.', '-', ':','--', '-.', '-', ':','--', '-.', '-', ':']

#matplotlib.rcParams.update({'font.size': 22})



fig = plt.figure(figsize = (25,25), dpi=80)

ax1 = fig.add_subplot(2,1,1)

l1 = []
columns = []
for column, color, lstyle in zip(D1R_densities_hier_mean, color_list_hier, ls_list_hier):
    data = D1R_densities_hier_mean[column] 
    l1.append(ax1.plot(data, c = color, linewidth = 2.5, ls = lstyle))
    columns.append(column)
    
ax1.set_ylim(0, 25000)
#ax1.rc('font', size=28)
#plt.legend(loc=(1.04, 0))
plugins.connect(fig, plugins.InteractiveLegendPlugin(l1, columns, ax=ax1,  start_visible=False))
mpld3.save_html(fig, 'bigtest.html')
# plt.savefig('D1R_devplot_wholebrain.svg', bbox_inches='tight')    
# plt.show()    
    
    
### D2R


figure(figsize = (30,30), dpi=80)

for column, color, lstyle in zip(D2R_densities_hier_mean, color_list_hier, ls_list_hier):
    data = D2R_densities_hier_mean[column] 
    plt.plot(data, c = color, label = column, linewidth = 2.5, ls = lstyle)
    
plt.ylim(0, 25000)
plt.rc('font', size=40)
plt.legend(loc=(1.04, 0))
plt.savefig('D2R_devplot_wholebrain.svg', bbox_inches='tight')    
plt.show()    
