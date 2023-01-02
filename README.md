# NCHS Data Remodeling

Converting NCHS fixed-width datasets to CSV in a reproducible way.

# Known issues

The dash instance is done inconsistently. Not sure how to handle ...

```
   value CASEID
      70622-80715="Respondent ID number" ;
   value CASISMK
      0="NEVER SMOKED REGULARLY"
      11="11 YEARS OR YOUNGER"
      12="12 YEARS OLD"
      13="13 YEARS OLD"
      14="14 YEARS OLD"
      15="15 YEARS OLD"
      16="16 YEARS OLD"
      17="17 YEARS OLD"
      18="18 YEARS OLD"
      19="19 YEARS OLD"
      20-24="20-24 YEARS OLD"
      25-29="25-29 YEARS OLD"
```

# Datasets
## National Survey of Family Growth [:house:](https://www.cdc.gov/nchs/nsfg/index.htm)
+ 2017-2019 NSFG Female Response [:notebook:](projects/NSFG/specification/2017_2019_FemRespSetup.yaml)
+ 2017-2019 NSFG Female Pregnant Response [:notebook:](projects/NSFG/specification/2017_2019_FemPregSetup.yaml)
+ 2017-2019 NSFG Male Response [:notebook:](projects/NSFG/specification/2017_2019_MaleSetup.yaml)
+ 2015-2017 NSFG Female Response [:notebook:](projects/NSFG/specification/2015_2017_FemRespSetup.yaml)
+ 2015-2017 NSFG Female Pregnant Response [:notebook:](projects/NSFG/specification/2015_2017_FemPregSetup.yaml)
+ 2015-2017 NSFG Male Response [:notebook:](projects/NSFG/specification/2015_2017_MaleSetup.yaml)

# Credits

+ Travis Hoppe