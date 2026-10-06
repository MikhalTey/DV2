# Source files

These are the spreadsheets exactly as downloaded, before any processing. They are kept out
of version control because together they come to about 74 MB and never change. Download
them back into this folder and `python scripts/build_data.py` will reproduce every file in
`data/processed` from scratch.

## ACARA Data Access Program

Free public download under the My School terms of use. No application form required.
Landing page: <https://acara.edu.au/contact-us/acara-data-access>

| File in this folder | Download from |
|---|---|
| `School_Profile_2008-2025.xlsx` | <https://dataandreporting.blob.core.windows.net/anrdataportal/Data-Access-Program/School%20Profile%202008-2025.xlsx> |
| `School_Profile_2025.xlsx` | <https://dataandreporting.blob.core.windows.net/anrdataportal/Data-Access-Program/School%20Profile%202025.xlsx> |
| `School_Location_2025.xlsx` | <https://dataandreporting.blob.core.windows.net/anrdataportal/Data-Access-Program/School%20Location%202025.xlsx> |
| `Enrolments_by_Grade_2008-2025.xlsx` | <https://dataandreporting.blob.core.windows.net/anrdataportal/Data-Access-Program/Enrolments%20by%20Grade%202008-2025.xlsx> |

## ABS Schools, 2025

Released 5 March 2026. Reference period is the August 2025 national school census.
Landing page: <https://www.abs.gov.au/statistics/people/education/schools/latest-release>

Data cubes used, all from
`https://www.abs.gov.au/statistics/people/education/schools/2025/`:

- `Table 35b Count of all schools, 2010-2025.xlsx`
- `Table 42b Number of full-time and part-time students, 2006-2025.xlsx`
- `Table 46a Full-time equivalent (FTE) students by ASGS remoteness areas, 2025.xlsx`
- `Table 53a Full-time equivalent (FTE) student to (FTE) teaching staff ratios, 2006-2025.xlsx`
- `Table 64a Capped apparent retention rates (ARR), 2011-2025.xlsx`
- `Table 90a Key information by states and territories, 2024 to 2025.xlsx`

## ABS boundaries

Australian Statistical Geography Standard, Edition 3 (July 2021 to June 2026).
<https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/access-and-downloads/digital-boundary-files>

- `SA4_2021_AUST_SHP_GDA2020.zip`
- `STE_2021_AUST_SHP_GDA2020.zip`

The mapshaper command that turned these into `maps/au_sa4_states.topo.json` is in the
project README.

All of the above are published under Creative Commons Attribution 4.0.
