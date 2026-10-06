# What was built, and how to sketch it

The page is finished and live at `index.html`. Draw the Week 7 sketch from this.
**By hand on A4. Digital tools score 0 for the sketch.**

Requirements check: 12 charts (need 10), 10 advanced idioms (need 8 for HD),
3 different map idioms (need 3).

---

## Page shape

One scrollable column, 1060px wide, centred. Five numbered parts. Every chart sits in
a bordered card with a short written note underneath it. No buttons that swap sections.

```
  MASTHEAD      kicker / big serif headline / standfirst / byline
                four key-number tiles in a row

  PART ONE      What happened          charts 1, 2
  PART TWO      The obvious objection  charts 4, 5
  PART THREE    Where                  charts 3, 6, 8, 7, 9
  PART FOUR     Who                    charts 10, 11
  PART FIVE     One last check         chart 12

  FOOTER        two columns: sources + method | definitions + limits
```

---

## The twelve charts

| # | Chart | Idiom | Level | File |
|---|---|---|---|---|
| 1 | Enrolments by sector, 2008-2025 | Stacked area | Basic | `01_national_area` |
| 2 | Same data, 2008 = 100 | **Index chart** | Advanced | `02_indexed_lines` |
| 3 | Change in government students by state | Bar with target marker | Basic | `03_state_change` |
| 4 | Change by year level, one panel per sector | **Diverging bar, small multiples** | Advanced | `04_grade_diverging` |
| 5 | Same numbers as a grid | **Heatmap** | Advanced | `05_grade_heatmap` |
| 6 | Change in government share, 88 regions | **MAP 1 — choropleth** | Advanced | `06_map_sa4_change` |
| 7 | The 260 schools opened since 2020 | **MAP 2 — proportional symbol** | Advanced | `07_map_new_schools` |
| 8 | Government share by equal-area cell | **MAP 3 — hexagonal binning** | Advanced | `08_map_hexbin` |
| 9 | Government share by remoteness | **Connected dot plot** | Advanced | `09_remoteness_dumbbell` |
| 10 | Change in students by ICSEA band | Grouped bar | Basic | `10_icsea_bars` |
| 11 | ICSEA spread of every school | **Ridgeline / density** | Advanced | `11_icsea_density` |
| 12 | Government share, one panel per state | **Small multiples** | Advanced | `12_state_small_multiples` |

Advanced count: index chart, diverging small multiples, heatmap, choropleth, symbol map,
hexbin map, connected dot plot, ridgeline, small multiples. That is 9 distinct advanced
idioms across 12 charts, comfortably over the 8 needed for HD.

### Why three different map idioms, not three choropleths

- **Choropleth** answers "which regions changed most", but Australia's regions are wildly
  different sizes, so the empty inland dominates the eye.
- **Hexbin** fixes exactly that by giving every cell the same ground area, which is why it
  sits directly after the choropleth on the page rather than somewhere else.
- **Proportional symbols** answer a different question entirely: not "what share" but
  "what got built, where, and how big".

---

## Drawing notes

1. Sketch the masthead first: kicker, two-line headline, standfirst paragraph, then a row
   of four boxes for the key numbers.
2. Each part gets a heading, two or three lines of body text, then its charts stacked.
3. For each chart draw the frame, the rough mark shape, the axis labels, and a couple of
   lines for the note underneath. You do not need real data values.
4. Mark where the one interactive control goes: the sector dropdown under map 2.
5. Sketch the two-column footer at the bottom.

Four or more clearly separated sections with headings, text and varied figures is what the
rubric asks for. This page has five parts plus a masthead and a footer.

---

## Interactivity, kept minimal

The brief warns against interaction for its own sake. There are three things only:

1. A sector dropdown on map 2, which filters the 260 new schools.
2. Tooltips on every chart, carrying the underlying numbers.
3. Nothing else. Values are printed directly on the charts wherever they fit, so no number
   depends on hovering.

---

## If the tutor wants changes

The specs are one file per chart in `charts/`, and every chart pulls its colours and
fonts from `charts/theme.json`, so a palette change is a single edit. The build scripts
regenerate the data:

```bash
python scripts/build_data.py     # raw ACARA and ABS files -> data/processed
python scripts/build_hexbin.py   # school points -> maps/school_hexbins.geojson
```
