# This script creates folders to hold generated data and figures
# Run it before running other notebooks/scripts in this analysis

from pathlib import Path

REPO_ROOT = Path('/Users/rwegener/repos/journalarticle_chesapeake_mhw')

data_dirs = ['data/01_raw', 'data/02_interim', 'data/03_processed']
fig_dirs = ['figures/01_general', 'figures/02_validation', 
            'figures/03_marineheatwaves', 'figures/04_supplementalmaterial']

for dir_path in data_dirs + fig_dirs:
    print('Creating', dir_path)
    full_path = REPO_ROOT / dir_path
    full_path.mkdir(parents=True, exist_ok=True)
