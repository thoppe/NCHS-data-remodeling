from collections import defaultdict
import re
import yaml


def extract_key_value_pair(line):
    tokens = line.split("=")
    key = tokens[0]
    val = " ".join(tokens[1:])

    key = key.strip()

    val = val.replace("''", "'")
    val = val.strip().rstrip(";").strip().strip("'").strip('"')

    return key, val


def find_section(text, key):

    tokens = None
    for lines in text.split(";"):
        lines = lines.strip()
        if not re.search(f"{key}\n", lines):
            continue

        tokens = lines.split()

        # Remove the matched token
        tokens = tokens[tokens.index(key) + 1 :]

        return tokens

    raise KeyError(f"{key} not found in section")


def parse_LENGTH(section):
    """
    Parse SAS FORMAT STATEMENTS, example below. Returns key/val dictionary.

    * SAS LENGTH STATEMENT;

    LENGTH
       CASEID 6                 RSCRNINF 3               RSCRAGE 3
       RSCRHISP 3               RSCRRACE 3               AGE_A 3
       AGE_R 3                  AGESCRN 3                HISP 3
    """

    tokens = find_section(section, "LENGTH")
    info = {}

    for key, val in zip(tokens[::2], tokens[1::2]):
        info[key] = {"SAS_length": int(val)}

    return info


def parse_FORMAT(section):
    """
    Parse SAS FORMAT STATEMENTS, example below. Returns key/val dictionary.

    * SAS FORMAT STATEMENT;

    /*
    FORMAT
      RSCRNINF Y1N5NALC.       RSCRAGE AGESCRN.         RSCRHISP YESNONAF.
      RSCRRACE RSCRRACE.       AGE_A AGEFMT.            AGE_R AGEFMT.
    """

    tokens = find_section(section, "FORMAT")
    info = {}

    for key, val in zip(tokens[::2], tokens[1::2]):
        val = val.rstrip(".")
        info[key] = {"SAS_format_mapping": val}

    return info


def parse_INPUT(section):
    """
    Parse SAS INPUT STATEMENTS, example below. Returns key/val dictionary.

    * SAS DATA, INFILE, INPUT STATEMENTS;

    DATA;
    INFILE "data-filename" LRECL=3839;
    INPUT
       CASEID  1-5              RSCRNINF  6              RSCRAGE  7-8
       RSCRHISP  9              RSCRRACE  10             AGE_A  11-12
    """

    tokens = find_section(section, "INPUT")
    info = {}

    # SAS uses $ to mark the type of a token, we can drop this
    tokens = [x for x in tokens if x != "$"]

    for key, val in zip(tokens[::2], tokens[1::2]):
        val = val.rstrip(".")

        val = val.split("-")
        if len(val) == 1:
            val = [val[0], val[0]]

        val = list(map(int, val))
        info[key] = {
            "start": val[0],
            "end": val[1],
        }
    return info


def parse_LABEL(section):
    """
    Parse SAS labels, example below. Returns key/val dictionary.

    * SAS LABEL STATEMENT;

    LABEL
      CASEID = "Respondent ID number"
      RSCRNINF = "Whether R was also the screener informant"
    """
    labels = {}
    for line in section.split("\n"):

        if "=" not in line:
            continue
        key, val = extract_key_value_pair(line)
        labels[key] = {"description": val}

    return labels


def parse_PROC(section):
    """
    Mmatch and parse columns with "value" + newline and key/values.
    Assume that each section is split using a semicolon.
    May fail if there is a semicolon in the label.
    Example text:

    * SAS PROC FORMAT;

    value Y1N5NALC
      1 = 'Yes'
      5 = 'No'
      7 = 'Not ascertained' ;
    """

    value_markers = r"""(?sm)^ +(value \$?\w+\n)(.*?);\r?$"""
    info = {}

    for block in re.findall(value_markers, section):
        variable_name = block[0].split()[1].strip()
        info[variable_name] = {}

        for line in block[1].split("\n"):
            key, val = extract_key_value_pair(line)
            info[variable_name][key] = val

    return info


def parse_SAS_import(raw_SAS: str):

    # Look for major sections, demarcated by "* SAS "
    SAS_section_markers = "* SAS "

    sections = raw_SAS.split(SAS_section_markers)

    # Remove first section before section marker
    sections = sections[1:]

    columns = defaultdict(dict)

    for section in sections:
        header = section.split("\n")[0].strip()
        data = None

        if "PROC FORMAT" in header:
            proc_map = parse_PROC(section)
        elif "STATEMENT" in header and "LABEL" in header:
            data = parse_LABEL(section)
        elif "STATEMENT" in header and "INPUT" in header:
            data = parse_INPUT(section)
        elif "STATEMENT" in header and "FORMAT" in header:
            data = parse_FORMAT(section)
        elif "STATEMENT" in header and "LENGTH" in header:
            data = parse_LENGTH(section)
        else:
            raise KeyError(f"Unknown section {header}")

        if data is not None:
            for k, v in data.items():
                columns[k].update(v)

    # Add extra columns if not present
    # for k in columns:
    #    if "validation" not in columns[k]:
    #        columns[k]["validation"] = {}

    # Apply the mapping
    for k in columns:
        if "SAS_format_mapping" in columns[k]:
            sas_key = columns[k]["SAS_format_mapping"]
            columns[k]["mapping"] = proc_map[sas_key]

    spec = {"columns": dict(columns)}
    output_yaml = yaml.safe_dump(spec, sort_keys=False)

    return output_yaml
