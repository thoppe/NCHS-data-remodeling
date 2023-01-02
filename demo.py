import yaml
from pathlib import Path
import requests
import logging
from fixedWidthParser import parse_SAS_import

logging.basicConfig(level=logging.DEBUG)


def mkdir(filename):
    filename.parent.mkdir(exist_ok=True, parents=True)


class ProjectParser:
    def __init__(self, f_project: str):
        # Load the project information
        f_project = "projects/NSFG.yaml"
        with open(f_project) as FIN:
            self.info = yaml.safe_load(FIN.read())

        self.working_folder = Path("projects") / self.info["project_folder"]
        self.base_url = self.info["base_url"]

    def __iter__(self):
        """
        Iterates over all datasets in the project.
        """
        yield from self.info["collection"]

    def download(self, url):
        """
        Downloads and saves a file to the working directory.
        Optionally prepends the base_url to the given url.
        Will skip if the file is already downloaded.

        Returns the name of the local file.
        """
        f_save = self.working_folder / url

        if not f_save.exists():

            url = self.base_url + url
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

    def build_specification(self, f_SAS):
        f_save = self.working_folder / "specification" / (f_SAS.stem + ".yaml")
        if not f_save.exists():
            logging.info(f"Parsing {f_SAS}")

        with open(f_SAS) as FIN:
            raw = FIN.read()
        output_yaml = parse_SAS_import(raw)

        mkdir(f_save)
        with open(f_save, "w") as FOUT:
            FOUT.write(output_yaml)

        return f_save

    def parse(self, info):

        print(info)
        if "SAS_import" in info:
            f_SAS = self.download(info["SAS_import"])
            f_spec = self.build_specification(f_SAS)

        f_data = self.download(info["fixed_width_data"])


#########################################################################


# Load the project information
f_project = "projects/NSFG.yaml"

project = ProjectParser(f_project)

for dataset in project:
    project.parse(dataset)
exit()


# Download files in each collection

for info in project_info["collection"]:
    if "SAS_import" in info:

        f_SAS = download(info["SAS_import"], base_url, working_folder)
        f_spec = build_specification(f_SAS, working_folder)
        f_data = download(info["fixed_width_data"], base_url, working_folder)

        print(f_spec)

    exit()
