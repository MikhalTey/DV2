# Australian School Enrolments

FIT3179 Data Visualisation 2, Semester 2 2026. Topic 7.

**Author:** Mikhalangelo
**Built:** September 2026
**Question:** Government school enrolments peaked in 2020 and have fallen every year since, while the school system as a whole kept growing. Where is that happening, and who is leaving?

---

## Data sources

Two independent sources, as required by the assignment brief.

### A. ACARA Data Access Program

Australian Curriculum, Assessment and Reporting Authority. Free public download under the
My School terms of use, no application form required.
<https://acara.edu.au/contact-us/acara-data-access>

| File | Reference period | Rows | Used for |
|---|---|---|---|
| `School Profile 2008-2025.xlsx` | 2008 to 2025 | 171,822 | Enrolments, ICSEA and sector for every school, every year |
| `School Location 2025.xlsx` | 2025 | 11,039 | Latitude, longitude, SA2/SA3/SA4, LGA, remoteness area |
| `School Profile 2025.xlsx` | 2025 | 9,755 | Cross-check of the 2025 slice |
| `Enrolments by Grade 2008-2025.xlsx` | 2008 to 2025 | 170,894 | Enrolments split by year level |

### B. ABS Schools, 2025

Australian Bureau of Statistics, catalogue *Schools*, released 5 March 2026.
Reference period is the August 2025 national school census.
<https://www.abs.gov.au/statistics/people/education/schools/latest-release>

Tables used: 35b (school counts), 42b (full-time and part-time students),
46a (FTE students by remoteness area), 53a (student to teaching staff ratios),
64a (apparent retention rates), 90a (key information by state).

### C. Geographic boundaries

ABS Australian Statistical Geography Standard, Edition 3 (July 2021 to June 2026).
`SA4_2021_AUST_SHP_GDA2020` and `STE_2021_AUST_SHP_GDA2020`.
<https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/access-and-downloads/digital-boundary-files>

All three sources are published under Creative Commons Attribution 4.0.

---

## Repository layout

```
DV2/
  index.html                  the visualisation (single page)
  charts/*.vg.json            one Vega-Lite spec per chart, formatted for reading
  charts/theme.json          colours, fonts and mark defaults shared by all twelve
  charts/design-notes.md           why those colours and mark rules were chosen
  data/raw/                   the source files exactly as downloaded
  data/processed/             the aggregated CSVs the charts load
  maps/au_sa4_states.topo.json  88 regions and 8 state outlines, sharing one topology
  maps/school_hexbins.geojson   equal-area hexagons holding the local sector mix
  scripts/build_data.py       turns data/raw into data/processed
  scripts/build_grade_share.py  government share per year level per year, for chart 5
  scripts/build_hexbin.py     turns the school points into the hexagon layer
  chart-plan.md               what each chart is, the interactions, and how to sketch the page
  submission-text.md          the Moodle description: domain, why, who, what, how
  test.html                   development harness; not part of the deliverable
```

## Processed data dictionary

| File | Rows | Contents |
|---|---|---|
| `national_sector_trend.csv` | 54 | Year, sector, enrolments, share of all students, indexed to 2008 = 100 |
| `national_totals.csv` | 18 | Year, total enrolments, government share |
| `state_change.csv` | 8 | Government share in 2020 and 2025 per state, change in percentage points |
| `state_sector_trend.csv` | 432 | State, year, sector, enrolments and share, 2008 to 2025 |
| `sa4_change.csv` | 88 | Per SA4: government share 2020 and 2025, change, student counts |
| `sa4_by_year.csv` | 1,584 | Per SA4 per year 2008-2025: government share, the national share for that year, and student count. Backs the map's year slider and the region detail chart |
| `remoteness_trend.csv` | 270 | Remoteness area, year, sector, enrolments and share |
| `grade_change.csv` | 39 | Year level and sector, enrolments 2020 and 2025, percent change |
| `grade_share_by_year.csv` | 221 | Year level by year 2009-2025, government share and its change in percentage points against that year level's own 2009 share |
| `icsea_change.csv` | 12 | ICSEA band and sector, enrolments 2020 and 2025, percent change |
| `icsea_distribution.csv` | 9,620 | One row per school in 2025: sector and ICSEA |
| `new_schools_since_2020.csv` | 260 | Schools open in 2025 but not 2020, with coordinates |
| `schools_points.csv` | 9,755 | Every school in 2025: sector, coordinates, enrolments |

Two map files sit alongside these: `au_sa4_states.topo.json` (452 KB, both the 88 regions
and the 8 state outlines in one topology so they share arcs) and `school_hexbins.geojson`
(69 KB, 221 equal-area hexagons).

The page downloads about **933 KB** in total, including the chart specifications themselves,
well inside the limit. `national_totals.csv`, `sa4_change.csv` and `schools_points.csv` are
intermediate files used by the build scripts and are not fetched by the page.

### Terms used

- **Sector.** Government, Catholic or Independent. Catholic and Independent together are the
  non-government sector.
- **Government share.** Government students divided by all students in that area or year,
  as a percentage. A fall of one *percentage point* means the share moved from, say, 66 to 65.
- **ICSEA.** ACARA's Index of Community Socio-Educational Advantage. A score built from parents'
  occupation and education plus the school's location. The national average is set to 1000.
  A higher score means a more advantaged school community.
- **SA4.** ABS Statistical Area Level 4. There are 88 of them covering Australia, each holding
  roughly 100,000 to 500,000 people. Used here because state borders are too coarse to show
  where the change is happening.
- **Remoteness area.** The ABS classification from Major Cities through to Very Remote.

### Choices worth knowing about

- Geography comes from the 2025 School Location file and is joined back onto earlier years by
  the school's ACARA ID. Coverage for 2020 is 99.3 percent. Schools that closed before 2025
  have no SA4 and are left out of the map only.
- The SA4 code `901 Other Territories` (Christmas Island, the Cocos Islands, Norfolk Island and
  Jervis Bay) is in the ABS geography but is scattered across the Indian and Pacific Oceans, so
  it is excluded from the maps. It holds well under 0.1 percent of Australian students.
- ICSEA bands use fixed cut points (under 950, 950 to 1000, 1000 to 1050, over 1050) rather than
  quartiles, so 2020 and 2025 are compared on the same scale.
- Boundaries are simplified to 2.5 percent of their original detail with mapshaper, and islands
  under 8 square kilometres are dropped, to keep the page fast. Shapes are preserved so no SA4
  disappears.

### Hexagon binning

The third map divides Australia into hexagons of equal ground area rather than using the
official regions, because the regions differ enormously in size and a region map therefore
flatters the empty inland. Binning is done in a Lambert cylindrical equal-area space
(x = longitude, y = sine of latitude) and each hexagon is written out as a real polygon in
longitude and latitude, so the cells tile without gaps once the map is projected. Cells
holding fewer than three schools are dropped, because one or two schools always reads as
0 or 100 percent and says nothing about the local mix. The 221 cells that survive hold
9,444 of the 9,755 schools.

## Rebuilding

```bash
python scripts/build_data.py
python scripts/build_hexbin.py
```

The first reads `data/raw` and writes `data/processed`; it needs pandas and openpyxl and
takes about ninety seconds, most of it spent opening the two 30 MB spreadsheets. The second
reads `data/processed/schools_points.csv` and writes the hexagon layer; it is pure standard
library and runs instantly.

The boundary files were produced from the ABS shapefiles with
[mapshaper](https://mapshaper.org) 0.7:

```bash
mapshaper SA4_2021_AUST_GDA2020.shp   -filter 'SA4_CODE21 !== "ZZZ" && SA4_CODE21 !== "901" && !/9[79]$/.test(SA4_CODE21)'   -filter-fields SA4_CODE21,SA4_NAME21,STE_NAME21   -filter-islands min-area=8km2 remove-empty   -simplify visvalingam weighted 2.5% keep-shapes -clean   -rename-fields sa4_code=SA4_CODE21,sa4_name=SA4_NAME21,state_name=STE_NAME21   -rename-layers sa4 -dissolve2 state_name + name=states   -o format=topojson target=* au_sa4_states.topo.json
```

The filter drops the twenty pseudo-regions the ABS includes for people with no usual
address or who were offshore on census night.

---

## Interaction

Four interactions, each tied to a question the story raises rather than added for its own sake.

- **Year slider** on the region map (`06_map_region_explorer`), 2008 to 2025. The map is driven
  by `sa4_by_year.csv` filtered to the slider's value, so dragging it shows the government share
  draining out of the populated coast after 2020.
- **Click a region** on the same map and a line chart beneath draws that region's own eighteen
  years against the national line. The selection and the view it drives have to live in one
  specification, because a Vega-Lite selection parameter cannot reach across separate charts.
- **Click a sector in the legend** of the indexed trend chart to fade the other two.
- **A menu** on the new-schools map shows one sector at a time.

Every value on the page is also printed on the chart or readable from an axis, so nothing
depends on hovering.
