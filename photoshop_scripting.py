

from photoshop import Session
import photoshop.api as ps
import glob
import os
import re

# Creating a list of the tif files to be photoshopped
# Replace tif_path with the path to your images
tif_path = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\to_photoshop\ready//"
out_path = r"Y:\2021_Bjerke_DevMouse_projects\01_DATA\to_photoshop\done//"
tifs = glob.glob(rf"{tif_path}*.tif")
tifs.extend(glob.glob(rf"{tif_path}*.tiff"))
names = [os.path.basename(tif) for tif in tifs]

# Specifying the location of the unique animal ID in the file name
# Change values based on your file naming convention
underscores_to_ID = 0



# Opens each of the tif files in Photoshop and runs the corresponding action
for name in names:
    
    ID = name.split("_")[underscores_to_ID]
    snum = re.findall("[s][0-9][0-9][0-9]", name)
    
    
    if len(snum) > 1:
        print("error: more than one potential section number in file name!")
        break
    
    elif len(snum) == 0:
        print("error: no section number in file name! please ensure section numbers are provided in the format sXXX.")
    
    else:
        path = rf"{tif_path}{name}"
        outPath = rf"{out_path}{name}"
    
        with Session(path, action="open") as ps:
            ps.app.preferences.rulerUnits = ps.Units.Percent
            ps.app.doAction(action=snum, action_from=ID)
            options = ps.TiffSaveOptions()
            options.imageCompression = 2
            doc = ps.active_document
            doc.saveAs(outPath, options, True)
            
    

