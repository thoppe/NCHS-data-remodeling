import yaml
from pathlib import Path

output = []

for f_project in Path('projects/').glob('*.yaml'):
    with open(f_project) as FIN:
        info = yaml.safe_load(FIN.read())

    name = info['project_name']
    homepage = info['homepage']
    folder = Path('projects') / info['project_folder']
    
    line = f"## {name} ([homepage]({homepage})"
    output.append(line)
    output.append('\n')

    for dataset in info['collection']:
        f_spec = Path(dataset["SAS_import"]).stem + '.yaml'
        f_spec = folder / 'specification' / f_spec
        line = f"+ {name} ([specs]({f_spec}))"
        output.append(line)

print('\n'.join(output))
