import yaml
from pathlib import Path
import requests
import logging
from fixedWidthParser import parse_SAS_import

logging.basicConfig(level=logging.DEBUG)

"""

f_sas = "2017_2019_FemRespSetup.sas"

with open(f_sas) as FIN:
    raw = FIN.read()

output_yaml = parse_SAS_import(raw)
print(output_yaml)
"""


def mkdir(dest):
    dest.mkdir(exist_ok=True, parents=True)


def download(url, f_save):
    logging.info(f"Downloading {url}")

    r = requests.get(url)
    if not r.ok:
        raise ValueError(f"Download of {url} failed with {r.status_code}")

    mkdir(f_save.parent)

    with open(f_save, "wb") as FOUT:
        FOUT.write(r.content)

    logging.info(f"Downloaded {len(r.content)} bytes to {f_save}")


# Load the project information
f_project = "projects/NSFG.yaml"
with open(f_project) as FIN:
    info = yaml.safe_load(FIN.read())

working_folder = Path("projects") / info["project_folder"]

# Create the working folder if it doesn't exist
# mkdir(working_folder)

base_url = info["base_url"]
print(info["collection"])

for dataset in info["collection"]:
    dset = dataset["dataset"]

    for key in ["fixed_width_data", "SAS_import"]:
        if key in dset:
            f_save = working_folder / "download" / dset[key]
            if not f_save.exists():
                download(base_url + dset[key], f_save)
