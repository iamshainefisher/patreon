"""The Patreon About section, written from the post list so it always matches what exists.

make_all.py writes it to output/about.txt, plain text that pastes cleanly into Patreon's About
editor. Adding a post to posts.py updates the parts, start dates and recap line by itself.
A new sub-series needs one line in PARTS below; a new series needs one entry in SERIES.
make_all.py stops and says so if either is missing.
"""
import datetime as dt

# One entry per series. Its posts are the ones whose 'series' value is one of its parts (or Recap).
SERIES = [
    dict(name='Theory in E', start=dt.date(2026, 11, 16),
         parts=['Foundations', 'Modes', 'Eras', 'Exercises']),
]

# One line per part (sub-series), finishing the sentence "Part 1, Foundations, from 16 November: ..."
PARTS = {
    'Foundations': 'the E major scale, chords in E, Nashville numbers, why a fifth higher, and the chords in each mode.',
    'Modes': 'all seven modes, from bright Lydian to unstable Locrian, every one starting on E.',
    'Eras': "a hundred years of music, from 1920s country blues to today's pop and country.",
    'Exercises': 'arpeggios for every chord in E, then runs that go up each chord and come back down its mode.',
}

RECAP = 'Recap'           # a recap post closes the part just before it

INTRO = [
    '{name} is a weekly music theory series for beginners on guitar and keys.',
    'Every Monday you get one idea, small enough to learn in a sitting: the idea in plain words, the notes, '
    'a chord sequence and one thing to try. Every post is in the key of E and ends with the same idea a fifth '
    'higher, in B, so you learn to move it anywhere. No reading music needed.',
]

IN_EACH_POST = [
    'About 300 words of notes (free)',
    'A diagram sheet: fretboard, keyboard and chord boxes in E and B (free)',
    'Two minutes of audio, music only (members)',
    'Guitar tab (members)',
]

START_HERE = '{first} Welcome, the Glossary and the Practice routines all go up on {date}, free for everyone.'


def problems(posts):
    out = []
    known = {p for ser in SERIES for p in ser['parts']} | {RECAP}
    for p in posts:
        if p.get('series') not in known:
            out.append((p['code'], f"sub-series '{p.get('series')}' is not in about.py: add it to SERIES and PARTS"))
    for ser in SERIES:
        for part in ser['parts']:
            if part not in PARTS:
                out.append(('about.py', f"no roadmap line for part '{part}' in PARTS"))
    return out


def _day(d):
    return f'{d.day} {d:%B}'


def _parts(posts, ser):
    """Parts in publishing order: name, first post's date, and whether a recap closes it."""
    parts = []; week = 0; current = None
    for p in posts:
        s = p['series']
        if s != RECAP and s not in ser['parts']:
            continue
        if s == RECAP:
            if current: current['recap'] = True
        elif not current or current['name'] != s:
            current = dict(name=s, start=ser['start'] + dt.timedelta(weeks=week), recap=False)
            parts.append(current)
        week += 1
    return parts


def _recap_line(parts):
    with_recap = [i + 1 for i, p in enumerate(parts) if p['recap']]
    if not with_recap:
        return None
    if len(with_recap) == len(parts):
        who = 'Each part ends'
    elif len(with_recap) == 1:
        who = f'Part {with_recap[0]} ends'
    elif with_recap == list(range(with_recap[0], with_recap[-1] + 1)):
        who = f'Parts {with_recap[0]} to {with_recap[-1]} end'
    else:
        who = 'Parts ' + ', '.join(map(str, with_recap[:-1])) + f' and {with_recap[-1]} end'
    return f'{who} with a recap and a five-question quiz.'


def about_text(posts):
    blocks = []
    for ser in SERIES:
        mine = [p for p in posts if p['series'] in ser['parts'] or p['series'] == RECAP]
        parts = _parts(mine, ser)
        lines = [INTRO[0].format(name=ser['name']), '', INTRO[1], '', "What's in each post", '']
        lines += [f'* {x}' for x in IN_EACH_POST]
        lines += ['', '', 'The roadmap:']
        for i, part in enumerate(parts, 1):
            lines.append(f'Part {i}, {part["name"]}, from {_day(part["start"])}: {PARTS[part["name"]]}')
        recap = _recap_line(parts)
        if recap:
            lines.append(recap)
        lines += ['', 'Start here', START_HERE.format(first=mine[0]['code'], date=_day(ser['start']))]
        blocks.append('\n'.join(lines))
    return '\n\n\n'.join(blocks) + '\n'
