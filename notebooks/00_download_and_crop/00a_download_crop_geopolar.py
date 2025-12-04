#########
# This script downloads Geo-Polar data for the study date range. It downloads
# each of the files to a scratch directory having cropped them to the Chesapeake
# Bay region. The `.scratch` directory can be deleted after running the script.
# Run with: python 00_download_crop_geopolar.py
# Runtime on my local machine: ~2 hours
# This script generates the file 
# L4_GHRSST-SSTfnd-Geo_Polar_Blended_Night-GLOB-v02.0-fv01.0_CB_{start_date}_{end_date}.nc
# to data/01_raw
#########

import os
import time
from pathlib import Path
import requests
from requests.exceptions import Timeout
from datetime import datetime

import xarray as xr
import pandas as pd
import geopandas as gpd
import rioxarray

# global variables
# Path to a .txt file containing a \n seperated list of filepaths to download
START_DATE = '20030101'
END_DATE = '20231231'
REPO_ROOT = Path('/Users/rwegener/repos/journalarticle_chesapeake_mhw')

scratch_dir = REPO_ROOT / 'data/scratch'
# Make the data folder if it doesn't exist already
scratch_dir.mkdir(parents=True, exist_ok=True)

### -------------------
# 1) Create a file with the target filepaths for download
### -------------------

# Define a function which creates a Geopolar filepath, given a date
def make_url(time):
    yyyy = time.strftime('%Y')
    yyyymmdd = time.strftime('%Y%m%d')

    # Organization swithes from STAR to OSPO in 2017
    if time.year >= 2017:
        org = 'OSPO'
    else:
        org = 'STAR'

    return (
        'https://coastwatch.noaa.gov/pub/socd2/coastwatch/sst_blended/sst5km/'
        f'night/ghrsst/{yyyy}/{yyyymmdd}000000-{org}-L4_GHRSST-SSTfnd-Geo_Polar'
        '_Blended_Night-GLOB-v02.0-fv01.0.nc'
    )

# Manually define known dates where geopolar data was removed for quality reasons
missing_dates = [
    pd.Timestamp(2017, 2, 1), pd.Timestamp(2018, 2, 8), pd.Timestamp(2018, 3, 6), 
    pd.Timestamp(2018, 3, 12), pd.Timestamp(2018, 3, 17), pd.Timestamp(2019, 5, 25), 
    pd.Timestamp(2021, 5, 21)
    ]

# Create a list of dates with a daily frequency
dates = pd.date_range(START_DATE, end=END_DATE)
try:
    dates = dates.drop(missing_dates)
except KeyError:
    pass

# Create a list that contains all the filepaths
all_filepaths = [make_url(d) for d in dates]

# Write the names of the filepaths to a text file, each on a new line
urls_filename = f'filepaths_geopolar_{START_DATE}_{END_DATE}.txt'
urls_path = scratch_dir / urls_filename
with open(urls_path, 'w') as f:
    f.writelines(filepath + '\n' for filepath in all_filepaths)

print('Generated file ', urls_path)

### -------------------
# 2) Download all the files from the text file to a scratch directory
### -------------------

# Build output filepath for downloaded data
def create_cbay_filepath(url):
    # Use original name, with _CB appended
    filename = os.path.basename(url).split('.nc')[0] + '_CB.nc'
    return scratch_dir / filename

# Read the filepaths from the file into a list
with open(urls_path) as f:
    filepaths = f.read().splitlines()

# Check that files were found
if len(filepaths) == 0:
    raise Exception('No lines found in FILEPATHS.TXT')

# Create the geopandas dataframe of the Chesapeake Bay shape for masking
# (Delaware Bay excluded)
cbay_wkt = (
    'POLYGON ((-75.07331635657022 36.69945277755481,' 
    '-75.07331761665449 38.10656782772858, -75.37020665599995 38.29321651673962,'  
    '-75.7561692781297 39.85271304991599, -77.9036114835175 39.860284284356595,'
    '-77.9432159124284 36.7312001366339, -75.07331635657022 36.69945277755481))'
)
cbay_gdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries.from_wkt([cbay_wkt]), 
                            crs='EPSG:4326')

# loop through each file in the list
for url in filepaths:
    print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S] -- Beginning processing for"))
    print(os.path.basename(url))

    # Check if file already exists, skip download and crop if it does
    cbay_path = create_cbay_filepath(url)
    if os.path.exists(cbay_path):
        print(cbay_path, 'aready found. Progressing to the next url.')
        continue

    # Download the file to a temp folder
    # timeout after 30 seconds and retry after a pause
    # if 3 retries fail then raise an error
    max_retries = 3
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout = 30)
        except Timeout:
            print('Caught a timeout error')
            # sleep 10 seconds
            time.sleep(10)
        # If the request succeeds then leave the loop
        break
    else:
        raise TimeoutError('MAX_RETRIES attempted. All timed out.')

    # Raise an error if the there is a bad http response
    response.raise_for_status()

    fullfile_tmp = scratch_dir / os.path.basename(url)
    open(fullfile_tmp, "wb").write(response.content)

    # Open and subset the file
    ds = xr.open_dataset(fullfile_tmp)
    ds.rio.write_crs("epsg:4326", inplace=True)

    ds_chesapeake = ds.sel(lat=slice(36.75, 40), lon=slice(-77.5, -75.5))
    ds_chesapeake = ds_chesapeake.rio.clip(
        cbay_gdf.geometry.values, cbay_gdf.crs, drop=False
    )

    # Save the subset
    ds_chesapeake.to_netcdf(cbay_path)

    # Remove the file from the temp folder
    os.remove(fullfile_tmp)

print('Individual file download complete')
### -------------------
# 3) Roll all the downloaded files together to create a single netcdf
### -------------------
full_year = xr.open_mfdataset(list(scratch_dir.glob('*_CB.nc')), engine='h5netcdf')

### -------------------
# 4) Create the new filename and save the merged file
### -------------------
output_filename = f'L4_GHRSST-SSTfnd-Geo_Polar_Blended_Night-GLOB-v02.0-fv01.0_CB_{START_DATE}_{END_DATE}.nc'
output_dir = REPO_ROOT / 'data/01_raw'
# Make the data folder if it doesn't exist already
output_dir.mkdir(parents=True, exist_ok=True)
# Save to file
full_year.to_netcdf(output_dir / output_filename)
