"""
Bins every Australian school into a hexagonal lattice so the third map idiom can
show the local government share without the area bias a choropleth carries. On a
choropleth the empty inland regions dominate the eye; here every cell covers the
same amount of ground.

Binning happens in a Lambert cylindrical equal-area space (x = longitude,
y = sin(latitude)), so the hexagons are equal area on the ground. Each hexagon is
written out as a real polygon in longitude and latitude rather than as a point,
so the cells tile with no gaps once Vega-Lite projects them. Adjacent cells share
vertex coordinates exactly, because the inverse projection depends only on y.

Run after build_data.py:  python scripts/build_hexbin.py
"""

import csv
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "processed"
MAPS = ROOT / "maps"

# Lattice spacing in degrees. 0.6 gives roughly 300 filled cells, fine enough to
# split a capital city into several of them.
HEX_W = 0.9
HEX_H = HEX_W * math.sqrt(3) / 2          # row spacing for a pointy-top lattice
R = HEX_W / math.sqrt(3)                  # circumradius

# sin(latitude) runs -1 to 1; this scales it back into degree-like units so the
# same spacing works on both axes.
Y_SCALE = 180 / math.pi

# Pointy-top hexagon, vertices clockwise from the top. d3-geo, which Vega uses,
# treats a ring as spherical and reads a counter-clockwise exterior ring as the
# whole globe minus the hexagon, so the winding order here is load-bearing.
CORNERS = [(0, R), (HEX_W / 2, R / 2), (HEX_W / 2, -R / 2),
           (0, -R), (-HEX_W / 2, -R / 2), (-HEX_W / 2, R / 2)]


def fwd(lon, lat):
    return lon, math.sin(math.radians(lat)) * Y_SCALE


def inv(x, y):
    return x, math.degrees(math.asin(max(-1.0, min(1.0, y / Y_SCALE))))


def nearest_hex(x, y):
    """Snap a point to the closest centre of the offset-row hexagonal lattice."""
    row = round(y / HEX_H)
    best = None
    for r in (row - 1, row, row + 1):
        offset = (HEX_W / 2) if (r % 2) else 0.0
        col = round((x - offset) / HEX_W)
        cx, cy = col * HEX_W + offset, r * HEX_H
        d = (x - cx) ** 2 + (y - cy) ** 2
        if best is None or d < best[0]:
            best = (d, r, col, cx, cy)
    return best[1], best[2], best[3], best[4]


bins = defaultdict(lambda: {"schools": 0, "students": 0,
                            "Government": 0, "Catholic": 0, "Independent": 0})

with open(OUT / "schools_points.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        r, c, cx, cy = nearest_hex(*fwd(float(row["lon"]), float(row["lat"])))
        b = bins[(r, c)]
        b["schools"] += 1
        b["students"] += int(row["enrolments"])
        b[row["sector"]] += int(row["enrolments"])
        b["cx"], b["cy"] = cx, cy

features = []
for (r, c), b in sorted(bins.items()):
    # A cell holding one or two schools is always near 0 or 100 percent, which
    # says nothing about the local mix. Dropped cells are almost all deep inland.
    if b["schools"] < 3 or b["students"] < 200:
        continue
    ring = [[round(v, 4) for v in inv(b["cx"] + dx, b["cy"] + dy)]
            for dx, dy in CORNERS]
    ring.append(ring[0])
    features.append({
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [ring]},
        "properties": {
            "schools": b["schools"],
            "students": b["students"],
            "gov_share": round(b["Government"] / b["students"] * 100, 1),
            "gov_students": b["Government"],
            "catholic_students": b["Catholic"],
            "independent_students": b["Independent"],
        },
    })

path = MAPS / "school_hexbins.geojson"
path.write_text(json.dumps({"type": "FeatureCollection", "features": features},
                           separators=(",", ":")), encoding="utf-8")

covered = sum(f["properties"]["schools"] for f in features)
shares = [f["properties"]["gov_share"] for f in features]
print(f"  {path.name}  {len(features)} hexagons, {covered} schools, "
      f"{path.stat().st_size/1024:.1f} KB")
print(f"  government share range: {min(shares)} to {max(shares)}")
