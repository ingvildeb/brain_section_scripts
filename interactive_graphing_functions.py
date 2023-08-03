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
#from matplotlib.pyplot import figure  
from mpl_toolkits.mplot3d import Axes3D
import nutil_scripts.graphing_functions as grf

def unique_list(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


### D1R

## Get custom region names from excel file:

resourcedir = 'Y:/Dopamine_receptors/Analysis/resources//'
customregsfile = resourcedir + 'customregions.csv'
read_customregs = pd.read_csv(customregsfile, sep = ";")


#matplotlib.rcParams.update({'font.size': 22})

color_list = grf.set_region_colors(customregsfile)
color_list_hier = grf.set_region_colors(customregsfile, R_col = "R_hier", G_col = "G_hier", B_col = "B_hier")
color_list_hier = unique_list(color_list_hier)
ls_list_hier = ['-', ':','--', '-.', '-', ':','--', '-.', '-', ':','--', '-.', '-', ':','--', '-.', '-', ':','--', '-.', '-', ':','--', '-.', '-', ':']
region_list = grf.set_region_names(customregsfile)    

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