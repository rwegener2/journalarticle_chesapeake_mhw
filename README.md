chesapeake_mhw
==============================

This repository contains code to support the publication Spatial Variability of Marine Heatwaves in the Chesapeake Bay. A preprint is available [here](https://doi.org/10.31223/X5299J) (DOI: 10.31223/X5299J). It has been submitted for review to the journal Estuaries and Coasts.

### Data Availability

The input and output data for this repository is available in the SEANOE Data repository (DOI [10.17882/105013](https://doi.org/10.17882/105013)). This repository includes the starting satellite SST and Chesapeake Bay Program datasets subset to the Chesapeake Bay region and the 2003-2023 time period for this study. It also includes the outputs of the data processing for both the validation and marine heatwave analyses of this study.

### Environment Setup

With the exception of `notebooks/01_intermediate_processing/01b_MHW_calculation_satellites.ipynb`, all notebooks use the environment documented in `environment.yml`. The `01b_MHW_calculation_satellites.ipynb` requires dask, and uses the environment `chesapeake_mhw_2021dask.yml`.

The environment for this notebook can be created with `environment.yml`. If you have trouble creating the environment `environment_full.yml` is an environment file that includes the version numbers and build hashes of the exact environment used in processing.

Create a new conda environment from a file using:
```python
conda env create -f environment.yml
```

#### `marineHeatWaves` Package

Marine heatwaves are calculated using the https://github.com/ecjoliver/marineHeatWaves package. This is a great package. Unfortunately the installation method has become out of date and there has not been a release in 9 years. To help with reproducing this analysis a copy of the `marineHeatWaves.py` file that I used has been copied directly into the `notebooks/01_intermediate_processing` directory. This version of the package corresponds to a commit from May 2022 (SHA d7292bf08ade0af213fa760b0d7e4adfe5f52894). The only thing about it that has been changed from that file is that instances of `np.NaN` were changed to `np.nan`, since `np.NaN` ws deprecated with the numpy 2.0 release.

### Reproducing the pipeline

Overview of Steps:

1. **Download the datasets** There are 4 starting datasets needed for this processing pipeline: Geo-Polar, MUR, OSTIA, Chesepeake Bay Program in situ data. The can be accessed by either:
    a. running the Python files which contain code to search, subset, and download the data. These are located in the `data/00_download_and_crop` folder
   b. Download each of the 4 datasets individually from the SEANOE archive and move them into the `raw` data folder.
2. **Generate output data folders** Run the script `output_data_folders.py` with `python output_data_folders.py`. This will create folders for data and figures.
3. **Run the analysis notebooks** Run the notebooks in the `notebooks` folder, following the sequential order used in the filenames. This generates the figures and generates the output datasets. If the cropped data was downloaded from the SEANOE repository the scripts in the `data/00_download_and_crop` folder can be skipped.

#### Notes

1. In almost every script data is either read from or written to a file on the file system. The filepaths in the notebooks are defined relative to the variable `REPO_ROOT`, which is defined at the top of each notebook or script. **Be sure to change this filepath to match the location of this code on your computer before running the notebooks**.
2. Numbers and letters at the beginning of a filename indicate the order in which to run files. Files with the same beginning letters (ex. `00a_` and `00a_`) can be run in any order, but should be run before the next letter (ex. `00b_`).

### Organization

#### `data` Folder

Folders are created to store data throughout the processing pipeline, from raw data to fully processed data. The folder is empty on Github, but will be populated as the notebooks are run.

#### `figures` Folder

Contains the final publication figures that are generated using code in data analysis notebooks. Three figures from the study were made in either Figma or QGIS and are not reproducible in code (paper figures 1, 2, and 3).

#### `notebooks` Folder

Jupyter notebooks written in Python with instructions for processing the data from the `raw` format through the generation of relevant `figures`.
