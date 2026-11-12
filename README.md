# Theory in E: diagram and tab generator

One folder that rebuilds every diagram sheet and every tab for the Theory in E Patreon series.
It replaces the earlier separate scripts (gen.py, gen_tabs.py, f6.py and arp.py).

## Run it

You need Python 3 with matplotlib, Pillow and fontTools (Pillow comes with matplotlib):

```
python3 -m pip install matplotlib fonttools
```

Then, from inside this folder:

```
python3 make_all.py
```

That checks all the music, then writes:

- `output/diagrams/`: every post's diagram sheet, the E1 arpeggio sheets and the summary charts (51 images)
- `output/tabs.md`: every tab for every post, in publishing order
- `output/tables/`: every table in the series doc as an image (55 so far), all 2400 px wide

Other options:

| Command | What it does |
| --- | --- |
| `python3 make_all.py --only F6 E1` | Builds just those posts |
| `python3 make_all.py --check` | Runs the checks and draws nothing |
| `python3 make_all.py --out somewhere` | Writes to another folder |
| `python3 make_all.py --tables` | Builds just the table images |

On Windows, type `python` instead of `python3`.

## What is in the folder

| File | What it holds |
| --- | --- |
| `posts.py` | Every post, in publishing order: its sheet, its tabs and any summary charts. **Edit this to add a post.** |
| `theory.py` | The music: note spellings, the seven modes in E and B, chord shapes, triads, arpeggio and scale positions, and the checks |
| `draw.py` | How everything is drawn: house colours, post sheets, the F6 grid, E1 arpeggio sheets, summary charts |
| `tabs.py` | How tabs are written: chord, scale and arpeggio tabs |
| `tables.py` | Turns every table in the doc into an image of the same width |
| `doc_export/` | The doc's tabs saved as Markdown: the source for the table images |
| `make_all.py` | The one command that checks and builds everything |

## Adding a post

1. Add an entry to `POSTS` in `posts.py`, in the right place in the order. Copy a similar post and change it.
2. If it uses a chord that has no guitar shape yet, add the shape to `SHAPES` in `theory.py`. Shapes are written low E to high e, with `x` for a string not played (for example `'E': '022100'`).
3. Run `python3 make_all.py --only <code>` and look at the images.
4. Export the doc's changed tabs as Markdown into `doc_export/` (same file names), then run `python3 make_all.py --tables`.

If a shape or spelling is wrong, `make_all.py` stops and names the problem before drawing anything.

## The checks

Before drawing, the scripts confirm that:

- every chord shape plays the right notes, with the root on the lowest string
- each of the 14 scales (seven modes in E and B) follows its step pattern and uses each letter once
- each mode's seven triads use only the mode's notes and follow the major, minor, diminished pattern
- each of the 98 arpeggios plays the right pitches, two octaves from the low E string to the high e string, within five frets
- every chord named in `posts.py` has a shape

## Table images

Each table is drawn at its natural size in the house colours: a light blue header row, bold first column and light bands on alternate rows. It is then centred on a white canvas 2400 px wide, the same width as the diagram sheets, so every table image is the same width. Tables too wide for the canvas wrap their text. Links keep their text and lose the address.

Files are named by tab, position and heading, for example `main-07-f3-chords-in-the-key-of-e.png` or `calendar-03-exercises.png`. Numbers follow the order in the doc, so adding a table early in a tab renumbers the ones after it.

To change the width, text size or margins, edit `WIDTH`, `SIZE` and `MARGIN` at the top of `tables.py`.

## Fonts

The published images use the free Inter font (Google Fonts). Without it, the images use DejaVu Sans instead.
