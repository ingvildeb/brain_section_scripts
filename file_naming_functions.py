# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 13:40:44 2024

@author: ingvieb
"""

from glob import glob
import os
import re
import pandas as pd

def flatten_comprehension(matrix):
    return [item for row in matrix for item in row]


def list_all_files(path="", extension=""):
    
    fileList = glob(fr"{path}*{extension}")
    nameList = []
    
    for file in fileList:
        fileName = os.path.basename(file)
        nameList.append(fileName)

    return nameList


def list_samples_from_czi(underscores=4, path=""):
    cziList = list_all_files(path,".czi")
    sceneList = []
    
    for file in cziList:
        sceneStart = (file.split(".")[0]).split("_")[underscores:]
        sceneList.append(sceneStart)    
        
    sceneList = flatten_comprehension(sceneList)
    sectionList = []
    
    for scene in sceneList:
        num = re.sub('[^0-9]','',scene)
        num = num.zfill(3)
        sectionList.append(num)

    return sectionList
    

def check_sample_exports(cziPath="", tifPath="", numberOfChannels=1):
    sectionList = list_samples_from_czi(path=cziPath)
    numberOfSections = len(sectionList)*numberOfChannels
    tifFiles = glob(fr"{tifPath}*.tif")
    numberOfTifs = len(tifFiles)
    if numberOfTifs > numberOfSections:
        print("More tifs than predicted by czi files")
    elif numberOfTifs < numberOfSections:
        print("Fewer tif files than predicted by czi files")
    elif numberOfTifs == numberOfSections:
        print("Number of tifs same as predicted by czi files")



def clean_tiff_name(file):
    
    fileName = os.path.basename(file)
    fileName = re.sub("-Image Export-[0-9][0-9]","",fileName)
    
    return fileName
        
def create_scene_list(maxScenes):
    sceneList = []
    for i in range(1,maxScenes+1):
        sceneList.append(f"s{i}")
        
    return sceneList

def clean_section_name(name):
    section = re.sub('[^0-9]','',name)
    section = section.zfill(3)
    
    return section



def create_renaming_scheme(tifPath, savePath, prefix, maxScenes, underscores, channels=[], mergeName = ""):
    
    fileList = glob(fr"{tifPath}*.tif")
    
    origNameList = []
    newNameList = []
    
    sceneList = create_scene_list(maxScenes)


    for file in fileList:
        origName = os.path.basename(file)
        origName = origName.split(".")[0]
        origNameList.append(origName)

        fileName = clean_tiff_name(file)
        sectionStart = (fileName.split(".")[0]).split("_")[underscores:]         
        
        
        scenes = [ele for ele in sceneList if(ele in fileName)]

        if scenes != []:
            scenes = int(re.sub('[^0-9]','',"".join(scenes)))
            section = sectionStart[scenes-1]
            
        else:
            section = sectionStart[0]
        
        section = clean_section_name(section)

        if channels:        
            c = [ele for ele in channels if(ele in fileName)]

            if c != []:
                 channel = "".join(c)
            
            else:
                 channel = mergeName

            newName = f"{prefix}_s{section}_{channel}" 

        
        else:
            newName = f"{prefix}_s{section}"            
        
        newNameList.append(newName)
            

    renamingScheme = pd.DataFrame(zip(origNameList,newNameList),columns=["Input file name","Renamed"])
    renamingScheme.to_excel(fr"{savePath}\\{prefix}_renamingScheme.xlsx", index=False)
        
    return(origNameList,newNameList)
            


def find_duplicate_names(renamingScheme):
    
    nameList = pd.read_excel(renamingScheme)
    nameList = nameList["Renamed"].tolist()
    dup = [x for x in nameList if nameList.count(x) > 1]
    
    if len(dup) > 0:
        print(f"The following duplicate names were found: {dup}. Please inspect and correct manually in renaming scheme.")
    else:
        print("No duplicate names found. Renaming scheme good to go.")
    



def rename_files(tifPath, renamingScheme, extension=".tif"):
    
    renamingScheme = pd.read_excel(renamingScheme)
    
    origName = list(renamingScheme["Input file name"])
    newName = list(renamingScheme["Renamed"])
    
    renameDict = dict(zip(origName, newName))

    for key, value in renameDict.items():
        fullpath = f"{tifPath}{os.sep}{key}{extension}"
        outpath = f"{tifPath}{os.sep}{value}{extension}"

        if os.path.exists(fullpath):
            os.rename(fullpath,outpath)


#### Example usage
## Assumptions
##### 1: files to be renamed must have the scene number indicated by "sX". There must not be any other instances of "sX" than the scene name.
##### 2: section numbers corresponding to the scenes are in the file name, separated by underscores from each other and the rest of the file name.

## For max scenes, fill in the maximum number of scenes in any of the tiff files
## For underscores, fill in the number of underscores in front of where the section numbers begin 



ID = "255"
age = "P21"
sex = "F"
stain = "Cresyl_violet"

if stain == "Parvalbumin":
    stain_short = "parv"
elif stain == "Calbindin":
    stain_short = "calb"
elif stain == "Cresyl_violet":
    stain_short = "CV"

basePath = rf"Y:\2021_Bjerke_DevMouse_projects\01_DATA\{age}\{stain}\Mouse{ID}"

origNameList,newNameList = create_renaming_scheme(tifPath = rf"{basePath}\\1_original_tiffs\\",
                                                  savePath = rf"{basePath}\\",
                                                  prefix = f"mouse{ID}_{age}_{sex}_{stain_short}",
                                                  maxScenes = 3,
                                                  underscores = 3)





find_duplicate_names(rf"{basePath}\\mouse{ID}_{age}_{sex}_{stain_short}_renamingScheme.xlsx")



#rename tiffs
rename_files(rf"{basePath}\\1_original_tiffs\\",
             rf"{basePath}\\mouse{ID}_{age}_{sex}_{stain_short}_renamingScheme.xlsx")

#rename thumbs
rename_files(rf"{basePath}\\1_original_tiffs\\thumbnails\\",
             rf"{basePath}\\mouse{ID}_{age}_{sex}_{stain_short}_renamingScheme.xlsx",
             extension="_thumbnail.png")











    