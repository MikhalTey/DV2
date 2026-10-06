# Moodle submission text

Copy each block into the matching field on the submission template. Fill in the two URLs
once the repository is public.

**URL to the visualisation:** `https://<your-github-username>.github.io/<repo-name>/`
**URL to the sketch PDF:** `https://github.com/<your-github-username>/<repo-name>/blob/main/sketch.pdf`

---

## i. The domain, the why and the who

**Domain.** School education in Australia, specifically enrolment patterns across the
government, Catholic and independent sectors between 2008 and 2025.

**Why.** Australia's school system is growing. It teaches 4.2 million children, about
760,000 more than in 2008, and that single headline number is what usually gets reported.
It hides a turn that happened in 2020: government school enrolments peaked that year at
2.67 million and have fallen every year since, while both non-government sectors kept
growing. The government share of all students had sat almost perfectly flat at 66 percent
for twelve years; it is now 63.2 percent.

This matters because a system can grow and hollow out at the same time, and the decisions
that follow are different in each case. Government school funding, staffing and school
building programmes are planned off enrolment forecasts, so a sustained shift in where
children enrol changes which schools need classrooms and which will have empty ones.
Families making a schooling decision are usually told what a school costs and how it
performs, but not whether the families around them are moving, or where.

The visualisation sets out to answer three questions a reader would reasonably ask once
they see the turn: is this just Australia having fewer babies, where is it happening, and
which families are moving.

**Who.** A general Australian adult audience, with parents of school-age children and
people who follow education policy as the readers most likely to care. No statistical
background is assumed. Every specialised term used on the page is defined on the page:
sector, government share, percentage point, ICSEA, region, remoteness and Foundation all
have plain-English definitions in the footer, and ICSEA is also explained in the section
where it first appears. No chart requires the reader to understand confidence intervals,
significance or standard deviations.

---

## ii. What: the data

Two independent sources are combined, as the brief requires.

**Source A. ACARA Data Access Program.** Published by the Australian Curriculum,
Assessment and Reporting Authority, the body that runs My School and the national schools
data collection. Free public download under the My School terms of use, no application
form needed. <https://acara.edu.au/contact-us/acara-data-access>

Four files are used:

- *School Profile 2008-2025* (171,822 rows): enrolments, ICSEA score, sector, staff counts
  and Indigenous and language-background proportions, for every Australian school in every
  year from 2008 to 2025.
- *School Location 2025* (11,039 rows): latitude, longitude, Statistical Areas Level 2 to
  4, local government area and remoteness classification for every school.
- *Enrolments by Grade 2008-2025* (170,894 rows): the same enrolments broken out by
  individual year level.
- *School Profile 2025*, used to cross-check the 2025 slice.

**Source B. ABS Schools, 2025.** Published by the Australian Bureau of Statistics,
released 5 March 2026, reference period the August 2025 national school census.
<https://www.abs.gov.au/statistics/people/education/schools/latest-release>
Used to verify that the national and state totals computed from the school-level ACARA
files match the official published census figures.

**Source C. Boundaries.** ABS Australian Statistical Geography Standard, Edition 3, for
the 88 Statistical Area Level 4 regions and the eight state and territory outlines.

All three are published under Creative Commons Attribution 4.0.

**Relevance.** ACARA's collection is the national school census: it is a complete
enumeration rather than a survey, so there is no sampling error to explain to the reader,
and it is the same data that sits behind My School. It carries both the sector and the
coordinates of every school, which is what makes it possible to ask the geographic
question at all. 2025 is the most recent year published.

**Creation process.** Two Python scripts in the repository do all of the work and both are
re-runnable from the downloaded source files.

- `scripts/build_data.py` reads the four ACARA spreadsheets and writes twelve aggregated
  CSVs. It joins the 2025 geography back onto earlier years using each school's ACARA
  identifier, which covers 99.3 percent of 2020 enrolments.
- `scripts/build_hexbin.py` bins the 9,755 school locations into hexagons of equal ground
  area and writes them as a GeoJSON polygon layer.

Boundaries were simplified with mapshaper to 2.5 percent of their original detail, keeping
shapes so that no region disappears. The exact command is in the repository README. The
whole page downloads about 850 KB.

**Judgements made, and stated on the page.** ICSEA bands use fixed cut points rather than
quartiles so that 2020 and 2025 are measured on the same scale. The Other Territories are
left off the maps because they are scattered across two oceans and hold well under 0.1
percent of Australian students. Hexagons holding fewer than three schools are dropped,
because one or two schools always reads as 0 or 100 percent government and says nothing
about the local mix. Chart 10 counts students rather than percentages, because one of the
groups is small enough that a percentage would overstate it.

---

## iii. How: idioms and why each one

The page runs in five parts, each answering one question, and the idiom in each case was
chosen for the task the reader has at that point.

**Part one, what happened.** A **stacked area chart** establishes the scene: the system
growing, three sectors, total rising every year. It is deliberately the weaker of the two
charts here, because stacked areas are poor at showing a change in a middle band, and that
is the point being made. An **index chart** follows, resetting each sector to 100 in 2008.
Indexing is what makes the three sectors comparable at all, since government is roughly
three and a half times the size of either other sector, and raw lines would show only the
size gap. On one shared axis the growth rates separate immediately.

**Part two, is it just demographics.** This is the objection that would otherwise sink the
whole argument, so it gets a chart that answers it directly. A **diverging bar chart in
small multiples**, one panel per sector, shows the change at each year level around a
shared zero line. The pattern the reader is asked to compare is a shape, not a value: the
government panel points left at the youngest year levels and right at the oldest, which is
a shrinking birth cohort working its way up a system, while the other two panels point
right everywhere. A **heatmap** then restates the same numbers as a grid, which collapses
the comparison into a single block of colour the reader can take in at a glance. The two
together let the reader check the detail and then see the summary.

**Part three, where.** This part zooms in, and uses three different map idioms because
each answers a different question.

- A **choropleth** of the 88 ABS regions answers "which places have the lowest government
  share". It is the right idiom for a rate attached to a defined area, but Australian regions
  differ enormously in size, so the empty inland dominates the eye. A year slider runs it from
  2008 to 2025, which turns the central claim into something the reader watches happen rather
  than something the text asserts. Clicking a region draws that region's own eighteen-year line
  underneath, against the national line, which answers the question a reader actually has:
  what about where I live.
- A **hexagonal binning map** is placed directly after it to correct exactly that. Every
  cell covers the same amount of ground, so the visual weight follows where schools are
  rather than how large an administrative region happens to be. The reader can compare the
  two maps and see the difference the area bias was making. The hexagons are computed from
  the school coordinates in a Lambert cylindrical equal-area space and written out as real
  polygons, so they tile without gaps once projected.
- A **proportional symbol map** answers a different question: not what share, but what was
  built, where, and how big. Circle area carries the enrolment of each of the 260 schools
  opened since 2020, and colour carries the sector.

All three use an **Albers equal-area conic** projection centred on Australia. Equal area is
the right property here because every question on these maps is about how many students
are somewhere, and a projection that distorts area would be read as a difference in size.

Before the maps, a **bar chart with a target marker** shows the change in each state in
headcount rather than share, with a tick marking where each state's government system
would have landed had it simply grown with its state's student population. After them, a
**connected dot plot** shows the government share by remoteness in 2020 and 2025, where
the length of the connector is the size of the shift and the task is comparing five
changes at once.

**Part four, who.** A **grouped bar chart** by ICSEA band shows the shape of the change
across the advantage range, which turns out to be a U: government schools grew at both
ends and lost through the middle. A **ridgeline plot** then shows the full distribution of
every school's ICSEA score by sector, because the bar chart compares four buckets while
the ridgeline shows the overlap and the tails that bucketing hides.

**Part five, one last check.** **Small multiples** of the government share, one panel per
state and territory on a shared scale, test whether 2020 is a real turning point or an
artefact of averaging eight different trends together. Every panel bends the same way.

**Interactivity**, kept deliberately sparse because the brief warns against adding it for its
own sake. Four things, each tied to a question the story raises:

1. A **year slider** on the region map. The central claim of the piece is that something changed
   in 2020; the slider lets the reader watch it change instead of taking my word for it.
2. **Clicking a region** on that map draws its own trajectory beneath it, against the national
   line. This is the unit's overview-and-detail pattern, and it turns a national story into a
   local one. Richmond - Tweed falls from 67% to 53% while the country moves from 66% to 63%.
3. **Choosing a sector** on the indexed chart fades the other two, so a reader can isolate one
   line without losing the context around it.
4. **A menu** on the new-schools map shows one sector at a time.

Each control sits in a tinted bar directly above the chart it drives, carrying a one-line prompt
beside it. An early version left the controls in Vega's default position underneath, which on a
tall map put the slider most of a screen below the sentence telling the reader to use it, and the
interactivity read as absent.

Values are printed directly on the charts wherever they fit, so no number on the page depends on
hovering to be read. There is no scrollytelling: the brief asks for presentation rather than
exploration and forbids controls that swap major sections, so scroll-driven chart swapping would
work against both.

**Special features.**

- The hexagonal binning layer is custom built. There is no Vega-Lite hexbin transform for
  geographic data, so the lattice, the equal-area binning and the polygon geometry are
  computed in `scripts/build_hexbin.py` and the result is projected as an ordinary GeoJSON
  layer.
- The region and state boundaries share a single TopoJSON topology, so the state outlines
  drawn over the choropleth are generated by dissolving the same arcs rather than being a
  second file, which keeps the two layers exactly aligned and the download small.
- All twelve specifications pull their colours, fonts and mark defaults from one shared theme
  file, `charts/theme.json`, so the page reads as one piece and a palette change is one edit.
- The layout varies its width on purpose: feature charts run the full column, supporting charts
  sit in a narrower centred column, and the geographic section breaks out onto a full-bleed
  tinted band with two maps side by side. The reader is meant to feel a gear change there.
- The three sector colours were checked with a colour-vision-deficiency validator on the
  all-pairs test, the stricter one needed for maps and scatterplots. The worst pair
  separates by a Delta E of 9.2 under deuteranopia, above the threshold of 8. Every chart
  also carries a legend and direct labels, so colour never has to work on its own.

---

## Acknowledgement of AI use

Generative AI (Claude) was used to help write and debug the Vega-Lite chart
specifications and the data build scripts, and to edit the prose on the page and in this
description. All figures were computed directly from the ACARA and ABS source files listed
above; none were produced by the model. The choice of topic, question, story structure and
chart selection are my own.
