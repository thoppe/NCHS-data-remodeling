import yaml
from pathlib import Path
import requests
import logging
import pandas as pd
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

    def check_spec(self, spec):
        """
        Checks the spec for anything amiss and records the change.
        Also assigns ranges for downstream processing:

        49-50: 49 years
               49: 49 years
               50: 49 years

        + Checks for any keys in the mapping are not integers
        + Checks that ranges mapped are <= 100

        Returns an updated spec
        """

        # Assigns an empty emapping if it doesn't exist
        for col, row in spec["columns"].items():
            if "mapping" not in row:
                row["mapping"] = {}

        modifications = []

        # Assign any ranges to other mappings
        for col, row in spec["columns"].items():

            # Create a copy since we are modifying it directly
            keys = list(row["mapping"].keys())
            large_range_keys = []
            bad_value_keys = []

            for k in keys:

                if "-" not in k:
                    try:
                        int(k)
                        assert int(k) == float(k)
                    except:
                        bad_value_keys.append(k)
                        continue

                if "-" in k:
                    val = row["mapping"][k]

                    try:
                        start_span, end_span = map(int, k.split("-"))
                    except:
                        bad_value_keys.append(k)
                        continue

                    # If the span is too large skip this one mapping
                    if abs(end_span - start_span) > 100:
                        large_range_keys.append(k)
                        continue

                    # If everything passed, remove the old key and map the new ones
                    del row["mapping"][k]
                    for i in range(start_span, end_span + 1):
                        row["mapping"][str(i)] = val

            for k in large_range_keys:
                modifications.append(
                    {
                        "action": "skipped_mapping",
                        "reason": "large_range",
                        "column": col,
                        "key": k,
                        "value": row["mapping"][k],
                    }
                )
                del row["mapping"][k]

            for k in bad_value_keys:
                modifications.append(
                    {
                        "action": "skipped_mapping",
                        "reason": "bad_key",
                        "column": col,
                        "key": k,
                        "value": row["mapping"][k],
                    }
                )

        return spec, modifications

    def parse(self, info):

        if "SAS_import" in info:
            f_SAS = self.download(info["SAS_import"])
            f_spec = self.build_specification(f_SAS)

        f_data = self.download(info["fixed_width_data"])

        f_save0 = self.working_folder / "csv" / (f_SAS.stem + ".csv.bz2")
        f_save1 = self.working_folder / "csv_mapped" / (f_SAS.stem + ".csv.bz2")

        if not f_save0.exists() or not f_save1.exists():
            logging.info(f"Mapping columns in {f_save0.stem}")
            mkdir(f_save0)
            mkdir(f_save1)
            df, spec = self.convert(f_spec, f_data)

            # Run a sanity check on the columns
            spec, modifications = self.check_spec(spec)

            # TO DO: Ultimately we should save and record this
            # if modifications:
            #    print(modifications)

            df.to_csv(f_save0, index=False, compression="bz2")

            # It is 50x faster to create a new dataframe vs work in place
            columns = spec["columns"]
            data = [df[col].map(row["mapping"]) for col, row in columns.items()]
            df = pd.concat(data, axis=1, keys=columns.keys())

            logging.info(f"Saving {f_save1.stem} compressed")
            df.to_csv(f_save1, index=False, compression="bz2")


#########################################################################

# Load the project information
f_project = "projects/NSFG.yaml"
project = ProjectParser(f_project)

# from dspipe import Pipe
# Pipe(project)(project.parse, -1)


for dataset in project:
    project.parse(dataset)
exit()

for dataset in project:
    try:
        project.parse(dataset)
    except Exception as EX:
        logging.error(f"Failed {dataset}")
        print(EX)
