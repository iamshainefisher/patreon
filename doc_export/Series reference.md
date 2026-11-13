# Series reference

This tab records how Theory in E was built, so a future series can match it without starting again. The main tab holds the post template, and the other tabs hold the glossary, practice routines, recording guide, tabs and calendar.

## House rules

| Setting | What this series used |
| --- | --- |
| Audience | Beginners |
| Instruments | Guitar first, then piano or keys |
| Home key | E, because guitar is the main instrument |
| Comparison key | A fifth higher (B), shown with diagrams and audio at the end of every post |
| Post length | About 300 words of text and about 2 minutes of audio |
| Audio | Music only, no talking: about 1:20 in E, then 0:40 in B |
| Chord names | Letters and Roman numerals in every post; Nashville numbers where they are the subject |
| Open to all patrons | Written notes, diagrams, glossary, practice routines |
| Tier-exclusive | Audio, tabs and video |
| Order | Learning order, with a recap post closing each sub-series |
| Cadence | Weekly on Mondays; audio recorded by the Thursday before |
| Linking | "How it sounds" compares each post with the one before it; every post links to the glossary |

## Diagram style

Every diagram sheet uses the same layout and colours, so patrons learn to read them once.

| Element | Colour | Meaning |
| --- | --- | --- |
| Dark circle | #1f2430 | The root note |
| Light blue circle | #dbe6f7 | A scale note |
| Orange circle | #f4a340 | A note changed from the major scale |
| Blue dot in a chord box | #3b6fb6 | A chord note that is not the root |

Each sheet shows the scale on a 12-fret fretboard and a two-octave keyboard, then chord boxes with Roman numerals and notes, first in E and then in B.

## Checks before anything is published

- [ ] Every chord shape and scale is checked by script against its notes, in both keys.
- [ ] Every song, date and chord claim links to a page that was opened and read.
- [ ] Any date that rests on a mirror site or one weak source is confirmed by a second source.
- [ ] Every diagram is opened and looked at before it goes out.
- [ ] Word counts are actually counted, not estimated.

## Tools that made the materials

One folder, theory\_in\_e, rebuilds every diagram and tab with a single command: `python3 make_all.py`. It checks every scale, chord shape, triad and arpeggio before drawing anything. It is updated every time a post or sub-series is added, so the latest zip sent in chat is always complete. Its README explains setup.

| File | What it holds | When to edit it |
| --- | --- | --- |
| posts.py | Every post in publishing order: its sheet, tabs and summary charts | Every new post: add one entry |
| theory.py | Notes, modes, chord shapes, triads, arpeggio and scale positions, and the checks | A new chord shape, scale or key |
| draw.py | House colours and every kind of diagram | A new kind of diagram |
| tabs.py | Chord, scale and arpeggio tabs | A new kind of tab |
| tables.py | Turns every table in this doc into an image, all 2400 px wide with white padding | To change the table style, width or text size |
| doc\_export/ | This doc's tabs saved as Markdown, the source for the table images | Whenever a table in the doc changes: export the tab again |
| about.py | The Patreon About section, with the roadmap and dates worked out from the post list | A new sub-series or series: add its one-line description |
| make\_all.py | Checks, then builds everything into output/ | Rarely |

## Ideas for future series

These are suggestions, each built on what patrons will know by the end of this series.

| Series idea | Possible posts | Builds on |
| --- | --- | --- |
| Pentatonic and blues scales | Minor and major pentatonic, the blues scale, the five box shapes | ER1, M6 |
| Arpeggios | Major, minor, 7th and diminished arpeggios across the neck | F3, ER2 |
| Rhythm and strumming | Time signatures, swing, syncopation, palm muting | ER2, ER5, ER10 |
| Chord extensions and inversions | 7ths, 9ths, slash chords, voice leading | ER2, ER3, ER8 |
| Ear training | Intervals, hearing major and minor, naming modes by ear | R2 |
| Songwriting through the eras | Writing a verse in each era's style | Eras |
| Genre deep dives | One genre per sub-series: blues, country, jazz | Eras |
