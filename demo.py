import yaml
from pathlib import Path
import requests
import logging
import pandas as pd
from tqdm import tqdm
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
        f_save = self.working_folder / "download" / url

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

    def convert(self, f_spec, f_data):

        with open(f_spec) as FIN:
            spec = yaml.safe_load(FIN.read())

        colspecs = []
        for col in spec["columns"]:
            row = spec["columns"][col]

            # Adjust the counting from SAS -> Python (off by one)
            colspecs.append((row["start"] - 1, row["end"]))

        df = pd.read_fwf(
            f_data,
            colspecs=colspecs,
            header=None,
            names=spec["columns"],
            dtype=object,  # Force reading everything as an object
        )
        return df, spec

    def parse(self, info):

        if "SAS_import" in info:
            f_SAS = self.download(info["SAS_import"])
            f_spec = self.build_specification(f_SAS)

        f_data = self.download(info["fixed_width_data"])
        
        '''
        df, spec = self.convert(f_spec, f_data)
        print(df)

        df.to_csv("example_raw.csv", index=False)

        for col, row in tqdm(spec["columns"].items(), total=len(spec)):
            if "mapping" not in row:
                continue
            df[col] = df[col].map(row["mapping"])

        df.to_csv("example_parsed.csv", index=False)
        '''

#########################################################################


# Load the project information
f_project = "projects/NSFG.yaml"

project = ProjectParser(f_project)

for dataset in project:
    project.parse(dataset)
