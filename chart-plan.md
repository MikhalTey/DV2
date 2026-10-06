# What was built, and how to sketch it

The page is finished and live at `index.html`. Draw the Week 7 sketch from this.
**By hand on A4. Digital tools score 0 for the sketch.**

Requirements check: 13 figures from 12 spec files (need 10), 9 advanced idioms (need 8 for HD),
3 different map idioms (need 3), 4 interactions.

---

## Page shape

One scrolling column at 1060px, with the width deliberately varied so the page does not read as
twelve identical cards. Part three breaks out onto a full-bleed tinted band.

```
  MASTHEAD        kicker / big serif headline / standfirst / byline
                  four key-number tiles in a row

  PART ONE        What happened
                  [FEATURE, full column]  2  indexed lines   <- sector menu
                  pull quote
                  [NARROW column]         1  stacked area

  PART TWO        The obvious objection
                  [full column]           4  year-level diverging bars
                  [full column]           5  heatmap

  ===== TINTED BAND, FULL BLEED =====
  PART THREE      Where
                  [NARROW column]         3  change by state
                  [FEATURE, full column]  6  map + year slider + click-to-detail
                  [TWO-UP side by side]   8  hexbin  |  9  remoteness
                  [full column]           7  new schools  <- sector menu
  ===== BAND ENDS =====

  PART FOUR       Who
                  [full column]          10  ICSEA bars
                  [full column]          11  ridgeline

  PART FIVE       One last check
                  [full column]          12  small multiples
                  pull quote

  FOOTER          two columns: sources + method | definitions + limits
```

---

## The charts

| # | Figure | Idiom | Level | File |
|---|---|---|---|---|
| 1 | Enrolments by sector, 2008-2025 | Stacked area | Basic | `01_national_area` |
| 2 | Same data, 2008 = 100 | **Index chart** | Advanced | `02_indexed_lines` |
| 3 | Change in government students by state | Bar with target marker | Basic | `03_state_change` |
| 4 | Change by year level, one panel per sector | **Diverging bar, small multiples** | Advanced | `04_grade_diverging` |
| 5 | Same numbers as a grid | **Heatmap** | Advanced | `05_grade_heatmap` |
| 6a | Government share by region, any year | **MAP 1 — choropleth** | Advanced | `06_map_region_explorer` |
| 6b | The clicked region vs the nation | Line chart | Basic | same file |
| 7 | The 260 schools opened since 2020 | **MAP 2 — proportional symbol** | Advanced | `07_map_new_schools` |
| 8 | Government share by equal-area cell | **MAP 3 — hexagonal binning** | Advanced | `08_map_hexbin` |
| 9 | Government share by remoteness | **Connected dot plot** | Advanced | `09_remoteness_dumbbell` |
| 10 | Change in students by ICSEA band | Grouped bar | Basic | `10_icsea_bars` |
| 11 | ICSEA spread of every school | **Ridgeline / density** | Advanced | `11_icsea_density` |
| 12 | Government share, one panel per state | **Small multiples** | Advanced | `12_state_small_multiples` |

6a and 6b live in one spec file because a Vega-Lite selection can only reach views inside the
same specification. They are two figures and read as two on the page.

Advanced idioms: index chart, diverging small multiples, heatmap, choropleth, symbol map,
hexbin map, connected dot plot, ridgeline, small multiples. Nine.

### Why three different map idioms

- **Choropleth** answers "which regions changed most", but Australia's regions are wildly
  different sizes, so the empty inland dominates the eye.
- **Hexbin** fixes exactly that by giving every cell the same ground area, which is why it sits
  directly after the choropleth rather than somewhere else on the page.
- **Proportional symbols** answer a different question: not what share, but what got built,
  where, and how big.

---

## Interaction

Four, each doing different work. All follow patterns from the unit's own teaching examples.

| Where | What it does | Pattern |
|---|---|---|
| Chart 6 | A **year slider** runs 2008 to 2025. Drag it and the colour drains out of the coast after 2020. | Bound range param, dynamic query |
| Chart 6 | **Click any region** and its own eighteen-year line is drawn beneath, against the national line. | Point selection driving a second view (overview and detail) |
| Chart 2 | **Pick a sector** to fade the other two. | Bound select driving a conditional opacity |
| Chart 7 | A **menu** shows one sector of new schools at a time. | Bound select param |

Nothing else. The brief warns against interaction for its own sake, and every value on the page is
printed on the chart or reachable from an axis, so no number depends on hovering.

There is no scrollytelling. The brief asks for presentation rather than exploration and forbids
controls that swap major sections, so scroll-driven chart swapping would fight both.

---

## Drawing notes

1. Sketch the masthead first: kicker, two-line headline, standfirst, then a row of four boxes.
2. Each part gets a heading, two or three lines of body text, then its charts.
3. **Show the width changes.** That is the point of the layout: feature charts run the full
   column, supporting charts sit in a narrower centred column, and part three is a tinted band
   running edge to edge with two charts side by side inside it.
4. Draw the three **control bars**: a tinted strip above charts 2, 6 and 7 holding a short prompt
   and the control itself. Charts 2 and 7 get a menu, chart 6 gets a slider. Also mark that the
   map on chart 6 is clickable.
5. Sketch the two-column footer at the bottom.

---

## Rebuilding

```bash
python scripts/build_data.py     # raw ACARA and ABS files -> data/processed
python scripts/build_hexbin.py   # school points -> maps/school_hexbins.geojson
```

Every chart pulls its colours and fonts from `charts/theme.json`, so a palette change is one edit.
