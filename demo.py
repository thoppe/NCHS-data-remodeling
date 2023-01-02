import yaml
from pathlib import Path
import requests
import logging
from fixedWidthParser import parse_SAS_import

logging.basicConfig(level=logging.DEBUG)


def mkdir(filename):
    filename.parent.mkdir(exist_ok=True, parents=True)


def download(url, base_url="", working_folder=""):
    """
    Downloads and saves a file to the working directory. Optionally prepends
    the base_url to the given url. Will skip if the file is already downloaded.

    Returns the name of the local file.
    """
    f_save = working_folder / url

    if not f_save.exists():

        url = base_url + url
        logging.info(f"Downloading {url}")

        r = requests.get(url)
        if not r.ok:
            raise ValueError(f"Download of {url} failed with {r.status_code}")

        # Create the working folder if it doesn't exist
        mkdir(f_save)
        with open(f_save, "wb") as FOUT:
            FOUT.write(r.content)

        logging.info(f"Downloaded {len(r.content)} bytes to {f_save}")

    return f_save


def build_specification(f_SAS, working_folder=""):
    f_save = working_folder / "specification" / (f_SAS.stem + ".yaml")
    if not f_save.exists():
        logging.info(f"Parsing {f_SAS}")
        with open(f_SAS) as FIN:
            raw = FIN.read()
        output_yaml = parse_SAS_import(raw)

        mkdir(f_save)
        with open(f_save, "w") as FOUT:
            FOUT.write(output_yaml)

    return f_save


# Load the project information
f_project = "projects/NSFG.yaml"
with open(f_project) as FIN:
    project_info = yaml.safe_load(FIN.read())

working_folder = Path("projects") / project_info["project_folder"]
base_url = project_info["base_url"]

# Download files in each collection

for info in project_info["collection"]:
    if "SAS_import" in info:

        f_SAS = download(info["SAS_import"], base_url, working_folder)
        f_spec = build_specification(f_SAS, working_folder)

        print(f_spec)

    exit()
