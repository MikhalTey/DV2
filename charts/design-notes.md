# Shared chart settings

Every spec in this folder repeats the same `config` block and the same sector colour
scale, so each file opens and runs on its own.

## Sector colours

| Sector | Hex | Why |
|---|---|---|
| Government | `#2a78d6` | Categorical slot 1 |
| Catholic | `#eb6834` | Categorical slot 2 |
| Independent | `#1baf7a` | Categorical slot 3 |

These three were checked with a colour-vision-deficiency validator on the all-pairs
test, which is the harder one needed for maps and scatterplots. Worst pair separation
is Delta E 9.2 under deuteranopia, above the 8 threshold. Independent green sits at
2.74:1 against the page, below the 3:1 mark, so every chart using it carries a legend
and the line charts carry labels on the lines themselves. Colour never has to work alone.

## Diverging scale, used for any signed change

Three red steps, a neutral grey for no real change, three blue steps.

`#9c2c2b` `#e34948` `#f0a9a8` · `#f0efec` · `#b7d3f6` `#5598e7` `#184f95`

Breaks at -6, -3, -1, +1, +3, +6.

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
