#########
# This script ...
# start_date, end_date, and scratch_dir must all match 00b_download_crop
# Runtime on my local machine ~seconds
# This script generates the file geopolar_filepaths_{start_date}_{end_date}.txt
# Run TWICE: `python 00a_generate_satellite_urls.py` from the environment
# First time set DATASET = 'geopolar', second time DATASET = 'mur'
#########
import os
from pathlib import Path

import pandas as pd

# Define global variables. To be set by user (or if time made into CLI args)
# Define the dates of the images based on the start and end dates of the analysis
REPO_ROOT = Path('/Users/rwegener/repos/chesapeake_mhw/')
START_DATE, END_DATE = '20030101', '20231231'
DATASET = 'geopolar'  # should be either 'mur' or 'geopolar'
if DATASET not in ['geopolar', 'mur']:
    raise KeyError('Valid options for DATASET are `geopolar` or `mur`')

# scratch directory to save text file with satellite urls
SCRATCH_DIR = REPO_ROOT / 'data/02_interim/scratch'
os.makedirs(SCRATCH_DIR, exist_ok=True)

# Define a function which creates a Geopolar filepath, given a date
def make_geopolar_url(time):
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

# def make_mur_url_OLD(time):
#     '''link used for full dataset download'''
#     yyyymmdd = time.strftime('%Y%m%d')
#     return (
#         'https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-protected/'
#         f'MUR-JPL-L4-GLOB-v4.1/{yyyymmdd}090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0'
#         '-fv04.1.nc'
#     )

# def make_mur_url_opendap(time):
#     yyyymmdd = time.strftime('%Y%m%d')
#     yyyy = time.strftime('%Y')
#     jjj = time.strftime('%j')
#     return (
#         'https://opendap.jpl.nasa.gov/opendap/OceanTemperature/ghrsst/data/GDS2/L4/'
#         f'GLOB/JPL/MUR/v4.1/{yyyy}/{jjj}/{yyyymmdd}090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-'
#         'v02.0-fv04.1.nc'
#     )

def make_mur_url_s3(time):
    yyyymmdd = time.strftime('%Y%m%d')
    return (
        's3://podaac-ops-cumulus-protected/MUR-JPL-L4-GLOB-v4.1/'
        f'{yyyymmdd}090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc'
    )

# Manually define known dates where geopolar data was removed for quality reasons
geopolar_missing_dates = [
    pd.Timestamp(2017, 2, 1), pd.Timestamp(2018, 2, 8), pd.Timestamp(2018, 3, 6), 
    pd.Timestamp(2018, 3, 12), pd.Timestamp(2018, 3, 17), pd.Timestamp(2019, 5, 25), 
    pd.Timestamp(2021, 5, 21)
    ]

mur_missing_dates = [
    pd.Timestamp(2021, 2, 20), pd.Timestamp(2021, 2, 21), pd.Timestamp(2022, 11, 9),
]

# Choose the url function and missing dates list corresponding to the dataset
# being processed
if DATASET == 'geopolar':
    make_url = make_geopolar_url
    missing_dates = geopolar_missing_dates
elif DATASET == 'mur':
    make_url = make_mur_url_s3
    missing_dates = mur_missing_dates
else:
    raise Exception('Invalid value for DATASET')

# Create a list of dates with a daily frequency
dates = pd.date_range(START_DATE, end=END_DATE)
try:
    dates = dates.drop(missing_dates)
except KeyError:
    pass

# Create a list that contains all the filepaths
all_filepaths = [make_url(d) for d in dates]

# Write the names of the filepaths to a text file, each on a new line
output_filename = f'filepaths_{DATASET}_{START_DATE}_{END_DATE}.txt'
output_path = SCRATCH_DIR / output_filename
with open(output_path, 'w') as f:
    f.writelines(filepath + '\n' for filepath in all_filepaths)

print('Generated file ', output_path)
