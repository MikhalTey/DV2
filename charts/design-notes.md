# Shared chart settings

Every spec in this folder repeats the same sector colour scale so each file opens and
runs on its own. Fonts, mark defaults and axis chrome come from `theme.json`, which the
page applies to all twelve.

Chart headlines, standfirsts and source lines are **not** in these specs. They are page
HTML, so they wrap to the figure they sit in, can be selected and searched, and are set
in the same faces as the rest of the page. Hand-wrapped subtitle lines baked into a spec
ran off the edge of the two narrower figures.

## Colour: one hue, one meaning

| Role | Hex | Where it appears |
|---|---|---|
| Government | `#2a78d6` | sector charts, and the government-share ramp on all three maps |
| Catholic | `#d2561f` | sector charts |
| Independent | `#12916a` | sector charts |
| A fall | `#a8322c` | charts 3 and 5, and the page's own down figures |
| A rise | `#7b3fa0` | charts 3 and 5 |

Blue used to carry four different meanings on the page at once: the government sector,
a rise, a high government share, and the year 2025. A reader who learned "blue means
government" in chart 2 then met a chart where blue meant growth, which in that chart was
mostly non-government. Blue is now the government sector and nothing else, which also
lets the sequential map ramps share it honestly.

The fall/rise pair is deliberately not a sector hue. Red already means a fall elsewhere
on the page, and violet appears nowhere else, so neither can be mistaken for a sector in
the figure above.

Two sets have to survive a colour-vision check, because these are the only two that ever
appear inside one chart:

- **Sector trio.** Worst pair Delta E 10.7 under deuteranopia, 25.6 at normal vision.
  All three now clear 3:1 against the page background, so colour is no longer propped
  up by labels alone. Catholic and Independent were darkened a step to get there.
- **Fall and rise.** Delta E 19.2 under protanopia, 19.4 at normal vision.

Across figures the two sets stay apart as well: violet against each sector hue is
17.1, 26.1 and 28.0 at normal vision, all above the 15 floor.

Every chart with two or more series still carries a legend, and the line and density
charts label their lines directly. Colour never has to work alone.

## Diverging scale, used for any signed change

Seven steps: four reds for a fall, the page surface at no change, two violets for a rise.

`#8c2823` `#ab3f36` `#c9776d` `#e3b4ab` · `#efe9df` · `#b9a7d4` `#7b3fa0`

The domain is asymmetric (-6.5 to +2.5) because the data is: falls run three times
deeper than rises, and a symmetric scale would have wasted half the ramp.

## Ink and chrome

| Role | Hex |
|---|---|
| Page and chart surface | `#fcfcfb` |
| Primary text | `#0b0b0b` |
| Secondary text | `#52514e` |
| Axis labels | `#898781` |
| Gridlines | `#e1e0d9` |
| Axis line | `#c3c2b7` |

## Mark rules followed throughout

- Lines 2px with round caps, end dots 9px with a 2px surface ring.
- Bars capped at 22px with a 3px rounded data end.
- Gridlines are solid hairlines, never dashed.
- Text never takes the colour of the data it describes.
- Values are always readable without hovering, through axes or direct labels.

## Projection

All three maps use `albers` with `rotate: [-134, 0]` and `parallels: [-18, -36]`,
an equal-area conic centred on Australia. Equal area matters here because the
question is about how many students sit in a place, so an area distortion would
be read as a difference in size.
