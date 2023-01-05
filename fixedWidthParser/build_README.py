import yaml
from pathlib import Path

output = []

for f_project in Path("projects/").glob("*.yaml"):
    with open(f_project) as FIN:
        info = yaml.safe_load(FIN.read())

    name = info["project_name"]
    homepage = info["homepage"]
    folder = Path("projects") / info["project_folder"]

    line = "# Datasets"
    output.append(line)

    line = f"## {name} [:notebook:]({f_project}) [:house:]({homepage})"
    output.append(line)

    for dataset in info["collection"]:
        name = dataset["name"]
        f_spec = Path(dataset["SAS_import"]).stem + ".yaml"
        f_spec = folder / "specification" / f_spec

        # Add a little check for the spec statements
        if f_spec.exists():
            line = f"+ [:notebook:]({f_spec}) {name}"
        else:
            line = f"+ [:no_entry_sign:]() {name}"

        output.append(line)

output = "\n".join(output) + "\n"

with open("README.md") as FIN:
    lines = FIN.read().split("\n")

section_start = None
section_end = None

for k, line in enumerate(lines):
    if section_start and not section_end and line.startswith("# "):
        section_end = k
    if line.startswith("# Datasets"):
        section_start = k

lines = lines[:section_start] + [output] + lines[section_end:]
lines = "\n".join(lines)
print(lines)
with open("README.md", "w") as FOUT:
    FOUT.write(lines)
