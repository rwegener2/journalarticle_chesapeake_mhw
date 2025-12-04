chesapeake_mhw
==============================

This repository contains code to support the publication Spatial Variability of Marine Heatwaves in the Chesapeake Bay. It was published in the journal Estuaries and Coasts on May 23rd, 2025 (DOI: [10.1007/s12237-025-01546-9](https://doi.org/10.1007/s12237-025-01546-9)).

### Data Availability

The input and output data for this repository is available in the SEANOE Data repository (DOI [10.17882/105013](https://doi.org/10.17882/105013)). This repository includes the starting satellite SST and Chesapeake Bay Program datasets subset to the Chesapeake Bay region and the 2003-2023 time period for this study. It also includes the outputs of the data processing for both the validation and marine heatwave analyses of this study.

### Environment Setup

With the exception of `notebooks/01_intermediate_processing/01b_MHW_calculation_satellites.ipynb`, all notebooks use the environment documented in `environment.yml`. The `01b_MHW_calculation_satellites.ipynb` requires dask, and uses the environment `chesapeake_mhw_2021dask.yml`.

Create a new conda environment from a file using:
```python
conda env create -f environment.yml
```

Unfortunately, the marineHeatWaves currently has an out of date installation method. It can be installed manually, however, by cloning the repository from the source Github page: https://github.com/ecjoliver/marineHeatWaves. The version used was the commit from May 2022 (SHA d7292bf08ade0af213fa760b0d7e4adfe5f52894).

### Reproducing the pipeline

Overview of Steps:

1. **Download the datasets** There are 4 starting datasets needed for this processing pipeline: Geo-Polar, MUR, OSTIA, Chesepeake Bay Program in situ data. The can be accessed by either:
    a. running the Python files which contain code to search, subset, and download the data. These are located in the `data/00_download_and_crop` folder
   b. Download each of the 4 datasets individually from the SEANOE archive and move them into the `raw` data folder.
3. **Run the analysis notebooks** Run the notebooks in the `notebooks` folder, following the sequential order used in the filenames. This generates the figures and generates the output datasets. If the cropped data was downloaded from the SEANOE repository the scripts in the `data/00_download_and_crop` folder can be skipped.

### Organization

#### `data` Folder

Folders are created to store data throughout the processing pipeline, from raw data to fully processed data. The folder is empty on Github, but will be populated as the notebooks are run.

#### `figures` Folder

Contains the final publication figures that are generated using code in data analysis notebooks. Three figures from the study were made in either Figma or QGIS and are not reproducible in code (paper figures 1, 2, and 3).

#### `notebooks` Folder

Jupyter notebooks written in Python with instructions for processing the data from the `raw` format through the generation of relevant `figures`.
