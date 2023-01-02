from fixedWidthParser import parse_SAS_import

f_sas = "2017_2019_FemRespSetup.sas"

with open(f_sas) as FIN:
    raw = FIN.read()

output_yaml = parse_SAS_import(raw)
print(output_yaml)
