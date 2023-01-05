# NCHS Data Remodeling

Converting NCHS fixed-width datasets to CSV in a reproducible way.

# Known issues

+ The dash instance is fixed, but it needs to be documented.

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

+ Add in a description for each dataset.
+ Import multiple files from SAS import (NAMCS)
+ Import from sas7bdat (NAMCS)

# Datasets
## National Health Care Surveys (1993-2019) [:notebook:](projects/NAMCS.yaml) [:house:](https://www.cdc.gov/nchs/ahcd/index.htm)
_NHAMCS is designed to collect data on the utilization and provision of ambulatory care services in hospital emergency and outpatient departments and ambulatory surgery locations._
+ :no_entry_sign: NAMCS 2019
## National Survey of Family Growth (1973-2019) [:notebook:](projects/NSFG.yaml) [:house:](https://www.cdc.gov/nchs/nsfg/index.htm)
_The National Survey of Family Growth (NSFG) gathers information on family life, marriage and divorce, pregnancy, infertility, use of contraception, and men’s and women’s health._
+ [:notebook:](projects/NSFG/specification/2017_2019_FemRespSetup.yaml) 2017-2019 NSFG Female Response
+ [:notebook:](projects/NSFG/specification/2017_2019_FemPregSetup.yaml) 2017-2019 NSFG Female Pregnant Response
+ [:notebook:](projects/NSFG/specification/2017_2019_MaleSetup.yaml) 2017-2019 NSFG Male Response
+ [:notebook:](projects/NSFG/specification/2015_2017_FemRespSetup.yaml) 2015-2017 NSFG Female Response
+ [:notebook:](projects/NSFG/specification/2015_2017_FemPregSetup.yaml) 2015-2017 NSFG Female Pregnant Response
+ [:notebook:](projects/NSFG/specification/2015_2017_MaleSetup.yaml) 2015-2017 NSFG Male Response
+ [:notebook:](projects/NSFG/specification/2013_2015_FemRespSetup.yaml) 2013-2015 NSFG Female Response
+ [:notebook:](projects/NSFG/specification/2013_2015_FemPregSetup.yaml) 2013-2015 NSFG Female Pregnant Response
+ [:notebook:](projects/NSFG/specification/2013_2015_MaleSetup.yaml) 2013-2015 NSFG Male Response

# Credits

+ Travis Hoppe