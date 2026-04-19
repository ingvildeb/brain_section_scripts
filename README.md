# Brain section scripts

Utilities for preparing, organizing, validating, and post-processing large collections of brain section images, especially for workflows built around QuickNII, VisuAlign, and Nutil.

This repository is most useful when you are working with serial histological section images and need help with repetitive tasks such as:

- renaming exported microscopy images into a consistent section-based naming scheme
- creating Nutil `.nut` files and transform templates
- checking transform sheets for duplicate names or inconsistent multi-channel parameters
- generating or updating QuickNII / VisuAlign JSON files
- checking whether Nutil transform or resize jobs finished successfully
- post-processing Nutil output into section-wise counts, densities, and interpolated data tables
- generating custom region definitions or simple graphs from atlas-based outputs

## How this repo fits into the broader workflow

These scripts are intended to support image-centric brain section workflows rather than replace the main registration and quantification tools themselves.

A common project flow looks like this:

1. Export microscopy images and rename them so section numbers are encoded consistently, ideally using `_sXXX`.
2. Create transform templates or `.nut` files for Nutil batch processing.
3. Review the image series for order, flipping, rotation, and mounting issues.
4. Apply batch transforms and validate that all channels were treated consistently.
5. Register sections in QuickNII and refine them in VisuAlign.
6. Quantify data in Nutil.
7. Post-process region-wise output for plotting, statistics, interpolation, or downstream analysis.

Several protocols on protocols.io describe the surrounding experimental and image-preparation workflow and point back to scripts in this repository (<https://www.protocols.io/researchers/ingvild-elise-bjerke>)
- Assessing histological image series for errors in serial order, flipping and mounting: <https://www.protocols.io/view/assessing-histological-image-series-for-errors-in-dpan5ide.html>
- Exporting and renaming raw microscopy images: <https://www.protocols.io/view/exporting-and-renaming-raw-microscopy-images-14egn985zl5d/v1>
- Correcting mounting errors in histological images using Photoshop: <https://www.protocols.io/view/correcting-mounting-errors-in-histological-images-4r3l2qj6pl1y/v1>

## Who this is for

This repository may be helpful if your project includes:

- serial coronal, sagittal, or horizontal brain section images
- multiple stains or multiple fluorescence channels per section
- alignment to a reference atlas through QuickNII and VisuAlign
- Nutil-based transformation, resizing, or quantification
- downstream aggregation of atlas-region measurements across sections

You do not need to be using the exact same experimental protocol as the original author. The scripts are most reusable when your own project has similar naming conventions and image-processing steps.

## Script guide

### Reusable helper modules

#### `file_naming_functions.py`

Use this when your exported image names are inconsistent or do not yet encode the true section number in a way that downstream tools can use reliably.

Useful functions include:

- `create_renaming_scheme(...)`: build an Excel renaming table from exported TIFFs
- `find_duplicate_names(...)`: check the proposed naming scheme for collisions
- `rename_files(...)`: apply the renaming table to a folder of files
- `sequential_to_real_sections(...)`: map sequential numbers to real section numbers when sections were sampled at intervals
- `exchange_sequential_sections(...)`: rename files and optionally update a QuickNII JSON file to match the new numbering
- `check_sample_exports(...)`: compare expected TIFF count against exported `.czi` scenes and channels

This is the module most directly connected to the "Exporting and renaming raw microscopy images" protocol.

#### `create_nut_file_functions.py`

Use this when you want to automate creation of Nutil input files instead of building them manually.

Useful functions include:

- `write_nut_transform_file(...)`: create a Nutil transform `.nut` file
- `write_nut_resize_file(...)`: create a Nutil resize `.nut` file
- `write_nut_quant_file(...)`: create a Nutil quantifier `.nut` file
- `create_nut_transform_sheet(...)`: generate a starter Excel transform sheet for a folder of files
- `nut_list_from_files(...)`: generate the `transform_files` string for a folder
- `list_from_transform_sheet(...)`: extract a Nutil-formatted file list from an edited transform sheet

This is especially useful when you need to prepare thumbnails for image review or batch transformations across many sections.

#### `validation_functions.py`

Use this after editing a Nutil transform sheet, especially for multi-channel data.

Useful functions include:

- `validate_transform_parameters(...)`: checks that all channels for a given section have matching rotation and flip parameters
- `check_for_duplicate_names(...)`: checks for duplicate names in the transform sheet

This directly supports the workflow described in the image-series assessment protocol.

#### `alignment_json_utils.py`

Use this when you need to create or update QuickNII / VisuAlign JSON files.

Useful functions include:

- `create_quicknii_slicedict(...)`: build a QuickNII JSON file from a folder of `.png` images
- `insert_existing_anchorings(...)`: transfer anchorings and markers from an older JSON into a new one
- `convert_markers(...)`: rescale VisuAlign markers when image resolution changes
- `split_json(...)`: subset a JSON file by filename pattern, for example by stain or channel

This is helpful when you have re-exported images, added sections, changed resolution, or need to preserve previous alignments while updating project files.

#### `nutil_checker_functions.py`

Use this to check whether Nutil jobs actually produced all expected outputs.

Useful functions include:

- `check_nut_file(...)`: detect missing outputs from a transform job
- `check_nut_resize_file(...)`: compare resize input and output counts
- `missing_files_to_string(...)`: turn missing items back into a Nutil-compatible file string

This can save time when large batch runs partially fail or stop early.

#### `nut_postprocessing_functions.py`

Use this after Nutil quantification when you want section-wise matrices, corrected counts, interpolated values, or densities by region.

Useful functions include:

- `compile_nut_customregions_reports(...)`: combine per-section custom-region reports into one table
- `identify_missing_sections(...)` and `create_missing_sections_df(...)`: mark gaps in a sampled series
- `interpolate_data(...)`: fill section-wise gaps by interpolation
- `describe_object_sizes(...)` and `calculate_object_diameters(...)`: derive object size estimates
- `mask_correction(...)`: correct counts and areas for visible and hidden mask load
- `abercrombie_correction(...)`: apply Abercrombie correction to counts
- `calculate_densities(...)`: compute 2D and 3D densities

This module is a starting point if your main goal is quantitative analysis from Nutil outputs.

#### `graphing_functions.py`

Use this to make quick summary plots and simple hierarchy-based summaries from regional data tables.

Useful functions include:

- `create_allen_bar_graph(...)`
- `create_allen_hbar_graph(...)`
- `create_line_graphs_per_hierarchy_level(...)`
- `group_data_by_hierarchy(...)`
- `calculate_ratio(...)`
- `calculate_relative_expression(...)`

The `graphing_demo_data/` folder includes example atlas hierarchy resources used by some of these workflows.

### More template-like or project-specific scripts

These files can still be useful, but are provided as one-off scripts that require modification of paths.

#### `photoshop_scripting.py`

Automates Photoshop actions on TIFF files. This is most relevant alongside the protocol "Correcting mounting errors in histological images using Photoshop".

Important: this file currently contains hard-coded paths and assumptions about how action sets are named. Users should treat it as a template and edit it for their own project before running it.

#### `make_customregions_from_hierarchy.py`

Generates custom region Excel files from the CCFv3 ontology hierarchy. The current script uses the included `graphing_demo_data/CCF_v3_ontology.json` file and writes one custom-region file per hierarchy level.

This is useful if you want region sets at coarser atlas hierarchy levels for Nutil or downstream summaries.

#### `format_customregions.py`

Older formatting script for converting custom-region resources into ID-to-region tables. It currently contains hard-coded paths and is best treated as an example to adapt.

#### `split_coordinate_clouds.py`

Splits a Nutil combined coordinate JSON into separate files grouped by hierarchy assignments from a custom region table. It also contains hard-coded paths and is best used as a starting point for project-specific adaptation.

## Suggested ways to use the repo in your own project

### 1. Standardize filenames before registration or quantification

If your images come out of imaging software with long instrument-generated names, start with `file_naming_functions.py`.

Typical use:

- generate a renaming scheme spreadsheet
- inspect it manually
- check for duplicates
- apply the rename

This helps keep section numbers synchronized across QuickNII, VisuAlign, Nutil, and any downstream tables.

### 2. Build transform sheets for image review and cleanup

If you are preparing to review a serial image set for order, flipping, rotation, or mounting problems, use `create_nut_file_functions.py` to generate a transform template, then use `validation_functions.py` to check it after editing.

This matches the workflow described in the protocols.io guide on assessing image series.

### 3. Reuse alignments after re-exporting or updating image sets

If you re-exported images at a different resolution, added stains, or produced a new PNG set for QuickNII / VisuAlign, use `alignment_json_utils.py` to preserve existing anchorings and adjust markers as needed.

### 4. Check large Nutil batch jobs before moving on

If a transform or resize run processed many sections, use `nutil_checker_functions.py` to confirm that all expected outputs were created before starting registration or quantification on the results.

### 5. Turn Nutil output into analysis-ready tables

If you already have Nutil reports, use `nut_postprocessing_functions.py` to:

- compile section-wise outputs
- account for missing sections
- interpolate gaps
- estimate densities
- apply mask and Abercrombie corrections


## Dependencies

The repository is a collection of scripts rather than an installable Python package. Depending on which files you use, you may need some or all of the following Python packages:

- `pandas`
- `numpy`
- `Pillow`
- `matplotlib`
- `scipy`
- `openpyxl`
- `xlsxwriter`
- `xlwt`
- `photoshop-python-api` or equivalent Photoshop automation package

Some scripts also assume access to:

- QuickNII
- VisuAlign
- Nutil
- Microsoft Excel-compatible `.xlsx` reading and writing
- Adobe Photoshop for the Photoshop automation workflow (tested with 2023 version)

## Practical notes before reusing code

- Many functions assume section numbers appear in filenames as `s001`, `s145`, and so on.
- Several scripts expect Windows-style paths and are written for a Windows-based workflow.
- Some scripts are safe to import as utility modules; others are meant to be edited and run as standalone scripts (see documentation above).
- A few files contain hard-coded project paths and should be adapted before use.
- It is a good idea to test scripts on a small copy of your dataset before applying them to a full image collection.

## Example projects and related resources

- Example use with real data: <https://github.com/ingvildeb/CalciMAP>
- QuickNII documentation: <https://quicknii.readthedocs.io/>
- QUINT workflow documentation: <https://quint-workflow.readthedocs.io/>
- VisuAlign documentation: <https://visualign.readthedocs.io/>
- Nutil documentation: <https://nutil.readthedocs.io/>

## Get started / help

This repository is currently not being actively maintained, but feel free to open an issue if you are having trouble using the scripts.

## Citation and attribution

If you use these scripts in a project, it is a good idea to cite the relevant software and workflow papers for QuickNII, VisuAlign, Nutil, and QUINT. If you find the scripts and protocols described here useful, please also consider citing the relevant protocols from protocols.io and this repository.
