# Brain section scripts


Scripts for working with large collections of brain sections as part of the QUINT workflow. 

The scripts provide utilities for organizing and speed up processing of data. They are sorted into files according to the part of the workflow they are intended to be used for:

- alignment_json_utils.py - contains functions useful for working with QuickNII and VisuAlign, e.g. creating QuickNII json from file folders, adding new images to an existing QuickNII json, splitting QuickNII json files based on stain names, converting VisuAlign markers to images of different resolutions.
- create_nut_file_functions.py - contains functions useful for working with Nutil, e.g. to create nutil files (transform, resize or quantifier type) and creating a pre-filled transform template based on files in a folder.
- file_naming_functions.py - contains functions useful for common renaming tasks, e.g. renaming raw tiffs exported from the Zen software, changing sequential numbers to numbers reflecting real section numbers.
- nut_postprocessing_functions.py - contains functions useful for post-processing Nutil reports, e.g. compiling data from section reports, interpolating data for missing sections, calculating cell numbers and densities, applying Abercrombie's correction to cell counts.
- nutil_checker_functions.py - contains functions useful for checking that all files in a nutil transform file have been created.
- photoshop_scripting.py - script for running photoshop actions automatically on a folder of images.


Examples of how to use all of these functions for real data can be found in the Github repository for the [CalciMAP project](https://github.com/ingvildeb/CalciMAP).
