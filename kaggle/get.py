# + tags=["parameters"]
# declare a list tasks whose products you want to use as inputs

upstream = None

import re
import shutil
from pathlib import Path

from kaggle import settings
from kaggle.terminal_commands import run_commands


def configure_kaggle(envs_folder: Path):
    """Copy kaggle.json to ~/.kaggle in order to run kaggle commands."""
    envs_file = envs_folder / 'kaggle.json'
    if not envs_file.exists():
        raise Exception('Kaggle configuration file not found')
    kaggle_folder = Path.home() / '.kaggle'
    kaggle_folder.mkdir(exist_ok=True)
    config_file = kaggle_folder / 'kaggle.json'
    if not config_file.exists():
        shutil.copy(envs_file, config_file)
        return True
    else:
        return False


def download_dataset(owner: str, dataset_name: str, download_folder: Path) -> Path:
    """Will download a dataset, unzip it in the download_folder and return the folder where the
    data was unzipped."""
    dataset = f'{owner}/{dataset_name}'
    folder = download_folder / dataset_name
    folder.mkdir(exist_ok=True)

    command_list = ['kaggle', 'datasets', 'download', dataset, '-p', str(folder), '--unzip']
    results, errors = run_commands(command_list)
    regexp = re.compile(r"Downloading\s([\w-]+\.zip)\sto\s(.+)")
    match = regexp.match(results[0])
    # print('>>', results[0])  # , match.groups(2))

    if match:
        return Path(match.group(2))
    if len(errors) > 1:
        print('-' * 50)
        print('errors')
        for e in errors:
            print(e)


def find_csv_file(folder: Path, csv_name: str) -> Path:
    csvs = folder.glob('**/*.csv')
    for csv in csvs:
        if csv.name == csv_name:
            return csv


if __name__ == '__main__':
    #  kaggle datasets download joebeachcapital/house-prices
    configure_kaggle(settings.ENVS_FOLDER)
    # ds_owner = 'fedesoriano'
    # ds_name = 'california-housing-prices-data-extra-features'
    ds_owner = 'akash14'
    ds_name = 'house-price-dataset'
    data_folder = settings.DATA_FOLDER
    data_folder.mkdir(exist_ok=True)

    fldr = download_dataset(owner=ds_owner, dataset_name=ds_name, download_folder=data_folder)
    print(f'Data folder: {fldr}')
    csv_file = find_csv_file(fldr, 'Train.csv')
    print(f'CSV: {csv_file}')
