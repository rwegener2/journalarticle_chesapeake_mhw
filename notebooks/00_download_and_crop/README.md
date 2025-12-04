# Accessing Raw Data

At the end of either option all data should be put in a `data/01_raw` folder located in the repository root. (Ex. `journalarticle_chesapeake_mhw/data/01_raw/L4_GHRSST-SSTfnd-Geo_Polar_Blended_Night-GLOB-v02.0-fv01.0_CB_20030101_20231231.nc`)

## Option 1: Download data from the SEANOE repository (recommended)

The cropped data from NOAA Geo-Polar, NASA MUR, Copernicus OSTIA, and the Chesapeake Bay Program are available in the SEANOE data repository (DOI [10.17882/105013](www.doi.org/10.17882/105013)). This is the most dependable way to reproduce the analysis. If the data is downloaded from there you can skip all scripts in this folder and move on to the steps in the `01_intermediate_processing` folder.

This is the recommended way to reproduce the analysis.

### Steps
1. Download data from SEANOE
2. Rename data to match notebook naming conventions, shown below (SEANOE gives arbitrary names on download)
3. Create a `data/01_raw1` folder in the root of the repository and move all data into it
4. Skip to processing in folder `01_intermediate_processing`

### Naming convention

| SEANOE Title | Rename to: |
|--- |--- |
| Water temperature observations from the Chesapeake Bay Program (2003-2023, Traditional Parter Data only) | `WaterQuality_ChesapeakeBayProgram_20030101_20231231_Temp.csv` |
| NOAA Geo-Polar Blended Sea Surface Temperature subset to the Chesapeake Bay region (2003-2023) | `L4_GHRSST-SSTfnd-Geo_Polar_Blended_Night-GLOB-v02.0-fv01.0_CB_20030101_20231231.nc` |
| NASA MUR Sea Surface Temperature subset to the Chesapeake Bay region (2003-2023) | `MUR-JPL-L4_GHRSST-SSTfnd-GLOB-v02.0-fv04.1-CB-20030101_20231231.nc` |
| Copernicus OSTIA Sea Surface Temperature subset to the Chesapeake Bay region (2003-2023) | `METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2_analysed_sst_CB_20070101-20231231.nc` |

## Option 2: Use the scripts provided here

You will need to create accounts with the following services:
* NASA Earthdata
* Copernicus Marine

### 1. Download satellites

**Geo-Polar**

1. Run the `00a_download_crop_geopolar.py` script from the conda environment. Does not depend on any other scripts/notebooks.

```bash
conda activate chesapeake_mhw  # activate environment
cd data/00_download_crop  # make sure you are in the download folder
python 00a_download_crop_geopolar.py  # run the script
```

Files for each individual data of Geo-Polar are downloaded to a `.scratch` folder by running this script. That folder can be deleted at the end of the download if desired.

**MUR**

MUR data must be downloaded from the SEANOE repository.

**OSTIA**

1. Run the notebook `00a_download_OSTIA.ipynb`


### 2. Chesapeake Bay Program

1. Run the notebook `00a_download_CBPWaterQuality.ipynb`. Does not depend on any other notebooks
2. Run `00b_crop_cbp.ipynb` (Must be run after all three satellite datasets are downloaded)
