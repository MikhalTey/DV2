"""
Government share of enrolments at every year level, every year 2008-2025.

Figure 4 used to repeat Figure 3's numbers as a grid. This builds the series it
shows instead: the government share of each year level over the whole period,
so the grid answers "when did it start, and at which year levels" rather than
restating the five-year change.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"

GRADES = ["One year before Year 1"] + [f"Year {i}" for i in range(1, 13)]
LABELS = {"One year before Year 1": "Foundation"}

print("Loading Enrolments by Grade ...")
grades = pd.read_excel(RAW / "Enrolments_by_Grade_2008-2025.xlsx",
                       sheet_name="EnrolmentsByGrade 2008-2025")

rows = []
for i, g_ in enumerate(GRADES):
    col = f"{g_} Enrolments"
    if col not in grades.columns:
        continue
    agg = grades.groupby(["Calendar Year", "School Sector"])[col].sum().unstack("School Sector")
    for year, r in agg.iterrows():
        total = float(r.sum())
        gov = float(r.get("Government", 0))
        if total < 1000:
            continue
        rows.append({"grade": LABELS.get(g_, g_), "grade_order": i,
                     "year": int(year),
                     "gov_students": int(gov), "total_students": int(total),
                     "gov_share": round(gov / total * 100, 2)})

df = pd.DataFrame(rows).sort_values(["grade_order", "year"])

# 2008 is dropped. In the Enrolments by Grade file that year only carries
# government schools, which puts the government share at 98% for every year
# level and is plainly a coverage gap rather than a real reading. The series
# starts at 2009, the first year all three sectors report by year level.
BASE = 2009
df = df[df.year >= BASE].copy()

# Change against each year level's own BASE share, in percentage points. This is
# what the grid is coloured by: a share is a level, and levels differ a lot
# between Foundation and Year 12, so colouring the raw share would show the
# structure of schooling rather than the change in it.
base = df[df.year == BASE].set_index("grade_order")["gov_share"]
df["share_base"] = df["grade_order"].map(base)
df["pp_change"] = (df["gov_share"] - df["share_base"]).round(2)

OUT.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT / "grade_share_by_year.csv", index=False)
print(f"wrote grade_share_by_year.csv  {len(df)} rows  "
      f"{df.year.min()}-{df.year.max()}  pp range {df.pp_change.min()} to {df.pp_change.max()}")
