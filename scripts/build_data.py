"""
FIT3179 DV2 - Australian School Enrolments
Builds the aggregated CSVs used by the Vega-Lite charts.

Sources (raw files in DV2/data/raw):
  A. ACARA Data Access Program - School Profile, School Location, Enrolments by Grade
     https://acara.edu.au/contact-us/acara-data-access
  B. ABS Schools, 2025 (released 5 March 2026)
     https://www.abs.gov.au/statistics/people/education/schools/latest-release

Run:  python scripts/build_data.py
"""

import pandas as pd
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
OUT = Path(__file__).resolve().parent.parent / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

SECTORS = ["Government", "Catholic", "Independent"]
BASE_YEAR, LAST_YEAR = 2020, 2025          # the peak year and the latest year

STATE_NAME = {
    "NSW": "New South Wales", "VIC": "Victoria", "QLD": "Queensland",
    "SA": "South Australia", "WA": "Western Australia", "TAS": "Tasmania",
    "NT": "Northern Territory", "ACT": "Australian Capital Territory",
}


def save(df, name, **kw):
    path = OUT / name
    df.to_csv(path, index=False, **kw)
    print(f"  {name:<34} {len(df):>6} rows  {path.stat().st_size/1024:>7.1f} KB")


# ----------------------------------------------------------------------------
# Load raw
# ----------------------------------------------------------------------------
print("Loading ACARA files ...")
profile = pd.read_excel(RAW / "School_Profile_2008-2025.xlsx",
                        sheet_name="SchoolProfile 2008-2025")
location = pd.read_excel(RAW / "School_Location_2025.xlsx",
                         sheet_name="SchoolLocations 2025")
grades = pd.read_excel(RAW / "Enrolments_by_Grade_2008-2025.xlsx",
                       sheet_name="EnrolmentsByGrade 2008-2025")

# 2025 geography, joined onto every year by the school's ACARA id
GEO_COLS = ["ACARA SML ID", "Latitude", "Longitude", "Statistical Area 4",
            "Statistical Area 4 Name", "Statistical Area 3 Name",
            "ABS Remoteness Area Name", "Local Government Area Name", "Suburb"]
geo = location[GEO_COLS].drop_duplicates("ACARA SML ID")
panel = profile.merge(geo.drop(columns=["Suburb"]), on="ACARA SML ID", how="left")


def gov_share(frame, index):
    """Wide table of enrolments per sector plus the government share."""
    t = frame.pivot_table(index=index, columns="School Sector",
                          values="Total Enrolments", aggfunc="sum")
    for s in SECTORS:
        if s not in t:
            t[s] = 0.0
    t = t[SECTORS].fillna(0.0)
    t["Total"] = t.sum(axis=1)
    t["gov_share"] = (t["Government"] / t["Total"] * 100).round(2)
    return t.reset_index()


# ----------------------------------------------------------------------------
# 1. National trend by sector, 2008-2025  (the headline: the 2020 peak)
# ----------------------------------------------------------------------------
print("\nBuilding CSVs ...")
nat = gov_share(panel, "Calendar Year").rename(columns={"Calendar Year": "year"})
long = nat.melt(id_vars=["year", "Total", "gov_share"],
                value_vars=SECTORS, var_name="sector", value_name="enrolments")
long["share"] = (long["enrolments"] / long["Total"] * 100).round(2)
peak = long[long.sector == "Government"].set_index("year")["enrolments"]
long["indexed"] = long.apply(
    lambda r: round(r["enrolments"] /
                    long[(long.sector == r.sector) & (long.year == 2008)]["enrolments"].iloc[0] * 100, 1),
    axis=1)
save(long[["year", "sector", "enrolments", "share", "indexed"]].sort_values(["sector", "year"]),
     "national_sector_trend.csv")

# Total enrolments each year, for the "the system kept growing" annotation
save(nat[["year", "Total", "gov_share"]].rename(columns={"Total": "total_enrolments"}),
     "national_totals.csv")

# ----------------------------------------------------------------------------
# 2. State level: government share 2020 vs 2025
# ----------------------------------------------------------------------------
two = panel[panel["Calendar Year"].isin([BASE_YEAR, LAST_YEAR])]
st = gov_share(two, ["State", "Calendar Year"])
w = st.pivot(index="State", columns="Calendar Year", values="gov_share")
w.columns = ["gov_share_2020", "gov_share_2025"]
g = st.pivot(index="State", columns="Calendar Year", values="Government")
t = st.pivot(index="State", columns="Calendar Year", values="Total")
w["change_pp"] = (w.gov_share_2025 - w.gov_share_2020).round(2)
w["gov_enrolments_2020"] = g[BASE_YEAR].astype(int)
w["gov_enrolments_2025"] = g[LAST_YEAR].astype(int)
w["gov_pct_change"] = ((g[LAST_YEAR] / g[BASE_YEAR] - 1) * 100).round(1)
w["total_pct_change"] = ((t[LAST_YEAR] / t[BASE_YEAR] - 1) * 100).round(1)
w = w.reset_index()
w["state_name"] = w["State"].map(STATE_NAME)
save(w.rename(columns={"State": "state"}), "state_change.csv")

# Full state x sector x year series, for the small multiples
sty = gov_share(panel, ["State", "Calendar Year"]).rename(
    columns={"State": "state", "Calendar Year": "year"})
sty_long = sty.melt(id_vars=["state", "year", "Total"], value_vars=SECTORS,
                    var_name="sector", value_name="enrolments")
sty_long["share"] = (sty_long.enrolments / sty_long.Total * 100).round(2)
sty_long["state_name"] = sty_long["state"].map(STATE_NAME)
save(sty_long[["state", "state_name", "year", "sector", "enrolments", "share"]]
     .sort_values(["state", "sector", "year"]), "state_sector_trend.csv")

# ----------------------------------------------------------------------------
# 3. SA4 level: the choropleth
# ----------------------------------------------------------------------------
sa4 = gov_share(two.dropna(subset=["Statistical Area 4"]),
                ["Statistical Area 4", "Statistical Area 4 Name", "State", "Calendar Year"])
key = ["Statistical Area 4", "Statistical Area 4 Name", "State"]
s20 = sa4[sa4["Calendar Year"] == BASE_YEAR].set_index(key)
s25 = sa4[sa4["Calendar Year"] == LAST_YEAR].set_index(key)
both = s20[["gov_share", "Total", "Government"]].join(
    s25[["gov_share", "Total", "Government"]], lsuffix="_2020", rsuffix="_2025", how="inner")
both["change_pp"] = (both.gov_share_2025 - both.gov_share_2020).round(2)
both["gov_pct_change"] = ((both.Government_2025 / both.Government_2020 - 1) * 100).round(1)
both["total_pct_change"] = ((both.Total_2025 / both.Total_2020 - 1) * 100).round(1)
both = both.reset_index()
# 901 is Other Territories: Christmas Island, the Cocos Islands, Norfolk Island and
# Jervis Bay. It is scattered across two oceans, so it is dropped from the map data.
both = both[both["Statistical Area 4"].astype(int) != 901]
both["sa4_code"] = both["Statistical Area 4"].astype(int).astype(str)
out = both.rename(columns={"Statistical Area 4 Name": "sa4_name", "State": "state",
                           "Total_2025": "students_2025", "Government_2025": "gov_students_2025"})
save(out[["sa4_code", "sa4_name", "state", "gov_share_2020", "gov_share_2025",
          "change_pp", "gov_pct_change", "total_pct_change",
          "students_2025", "gov_students_2025"]].round(2), "sa4_change.csv")

# ----------------------------------------------------------------------------
# 3b. SA4 by year: the series behind the map's year slider, and behind the
#     detail chart that appears when a region is clicked. The national share is
#     carried on every row so the detail chart can draw its comparison line
#     without a second data source.
# ----------------------------------------------------------------------------
sa4y = gov_share(panel.dropna(subset=["Statistical Area 4"]),
                 ["Statistical Area 4", "Statistical Area 4 Name", "State", "Calendar Year"])
sa4y = sa4y[sa4y["Statistical Area 4"].astype(int) != 901]
nat_share = nat.set_index("year")["gov_share"]
sa4y = sa4y.rename(columns={"Statistical Area 4 Name": "sa4_name", "State": "state",
                            "Calendar Year": "year", "Total": "students"})
sa4y["sa4_code"] = sa4y["Statistical Area 4"].astype(int).astype(str)
sa4y["national_share"] = sa4y["year"].map(nat_share)
save(sa4y[["sa4_code", "sa4_name", "state", "year", "gov_share",
           "national_share", "students"]]
     .sort_values(["sa4_code", "year"]).round(2), "sa4_by_year.csv")

# ----------------------------------------------------------------------------
# 4. Remoteness: the city / country gradient
# ----------------------------------------------------------------------------
ORDER = ["Major Cities", "Inner Regional", "Outer Regional", "Remote", "Very Remote"]
rem = gov_share(panel.dropna(subset=["ABS Remoteness Area Name"]),
                ["ABS Remoteness Area Name", "Calendar Year"])
rem = rem.rename(columns={"ABS Remoteness Area Name": "remoteness", "Calendar Year": "year"})
rem_long = rem.melt(id_vars=["remoteness", "year", "Total", "gov_share"],
                    value_vars=SECTORS, var_name="sector", value_name="enrolments")
rem_long["share"] = (rem_long.enrolments / rem_long.Total * 100).round(2)
rem_long["order"] = rem_long.remoteness.map({n: i for i, n in enumerate(ORDER)})
save(rem_long[["remoteness", "order", "year", "sector", "enrolments", "share", "gov_share"]]
     .sort_values(["order", "sector", "year"]), "remoteness_trend.csv")

# ----------------------------------------------------------------------------
# 5. Year level: separating the shrinking cohort from the sector shift
# ----------------------------------------------------------------------------
GRADES = ["One year before Year 1"] + [f"Year {i}" for i in range(1, 13)]
LABELS = {"One year before Year 1": "Foundation"}
gsub = grades[grades["Calendar Year"].isin([BASE_YEAR, LAST_YEAR])]
rows = []
for i, g_ in enumerate(GRADES):
    col = f"{g_} Enrolments"
    if col not in gsub.columns:
        continue
    agg = gsub.groupby(["Calendar Year", "School Sector"])[col].sum().unstack(0)
    for sector in agg.index:
        a, b = agg.loc[sector, BASE_YEAR], agg.loc[sector, LAST_YEAR]
        if a < 1000:
            continue
        rows.append({"grade": LABELS.get(g_, g_), "grade_order": i, "sector": sector,
                     "enrolments_2020": int(a), "enrolments_2025": int(b),
                     "pct_change": round((b / a - 1) * 100, 1)})
save(pd.DataFrame(rows), "grade_change.csv")

# ----------------------------------------------------------------------------
# 6. ICSEA: who is leaving
#    ICSEA is the ACARA Index of Community Socio-Educational Advantage.
#    Bands are fixed cut points so 2020 and 2025 are compared on the same scale.
# ----------------------------------------------------------------------------
CUTS = [0, 950, 1000, 1050, 3000]
NAMES = ["Under 950", "950 to 1000", "1000 to 1050", "Over 1050"]
ic = panel[panel["Calendar Year"].isin([BASE_YEAR, LAST_YEAR])].dropna(subset=["ICSEA"]).copy()
ic["band"] = pd.cut(ic["ICSEA"], CUTS, labels=NAMES)
b = ic.pivot_table(index=["band", "School Sector"], columns="Calendar Year",
                   values="Total Enrolments", aggfunc="sum", observed=True).reset_index()
b.columns = ["band", "sector", "enrolments_2020", "enrolments_2025"]
b["pct_change"] = ((b.enrolments_2025 / b.enrolments_2020 - 1) * 100).round(1)
b["change"] = (b.enrolments_2025 - b.enrolments_2020).astype(int)
b["band_order"] = b.band.map({n: i for i, n in enumerate(NAMES)})
save(b.sort_values(["band_order", "sector"]), "icsea_change.csv")

# School level ICSEA vs size, for the 2025 distribution chart
c = panel[panel["Calendar Year"] == LAST_YEAR].dropna(subset=["ICSEA", "Total Enrolments"])
save(c[["School Sector", "ICSEA"]].rename(columns={"School Sector": "sector", "ICSEA": "icsea"})
     .round(0), "icsea_distribution.csv")

# ----------------------------------------------------------------------------
# 7. School points, for the symbol map
# ----------------------------------------------------------------------------
pts = panel[panel["Calendar Year"] == LAST_YEAR].dropna(subset=["Latitude", "Longitude"])
ids20 = set(panel[panel["Calendar Year"] == BASE_YEAR]["ACARA SML ID"])
new = pts[~pts["ACARA SML ID"].isin(ids20)].copy()
new = new[["School Name", "Suburb", "State", "School Sector", "School Type",
           "Latitude", "Longitude", "Total Enrolments", "ICSEA",
           "ABS Remoteness Area Name", "Statistical Area 4 Name"]]
new.columns = ["school", "suburb", "state", "sector", "school_type", "lat", "lon",
               "enrolments", "icsea", "remoteness", "sa4_name"]
new["lat"] = new.lat.round(4)
new["lon"] = new.lon.round(4)
save(new.sort_values("enrolments", ascending=False), "new_schools_since_2020.csv")

# Every school, trimmed hard so the file stays small
allp = pts[["School Sector", "Latitude", "Longitude", "Total Enrolments"]].copy()
allp.columns = ["sector", "lat", "lon", "enrolments"]
allp["lat"] = allp.lat.round(3)
allp["lon"] = allp.lon.round(3)
allp["enrolments"] = allp.enrolments.fillna(0).astype(int)
save(allp, "schools_points.csv")

print("\nDone. Processed files in", OUT)
