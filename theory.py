"""Music data and checks for the Theory in E series.

Everything here is plain data or pure functions: note spellings, the seven modes in
E and B, guitar chord shapes, triads for every mode, two-octave arpeggio positions
and one-octave scale positions. check_all() tests every one of them, and make_all.py
refuses to draw anything until it passes.
"""
import re

# ---------------------------------------------------------------- notes
PC = {'C': 0, 'B#': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'E#': 5,
      'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def disp(n):
    """'Bb' -> 'B♭' for display."""
    return n[0] + '♭' if len(n) == 2 and n[1] == 'b' else n


def disp_name(n):
    return n.replace('7b9', '7♭9')


# ---------------------------------------------------------------- modes
ORDER = ['Lydian', 'Ionian', 'Mixolydian', 'Dorian', 'Aeolian', 'Phrygian', 'Locrian']   # brightest to darkest
POST = {'Lydian': 'M3', 'Ionian': 'M2', 'Mixolydian': 'M4', 'Dorian': 'M5', 'Aeolian': 'M6',
        'Phrygian': 'M7', 'Locrian': 'M8'}
SCALES = {
    'E': {'Ionian': 'E F# G# A B C# D#', 'Lydian': 'E F# G# A# B C# D#', 'Mixolydian': 'E F# G# A B C# D',
          'Dorian': 'E F# G A B C# D', 'Aeolian': 'E F# G A B C D', 'Phrygian': 'E F G A B C D',
          'Locrian': 'E F G A Bb C D'},
    'B': {'Ionian': 'B C# D# E F# G# A#', 'Lydian': 'B C# D# E# F# G# A#', 'Mixolydian': 'B C# D# E F# G# A',
          'Dorian': 'B C# D E F# G# A', 'Aeolian': 'B C# D E F# G A', 'Phrygian': 'B C D E F# G A',
          'Locrian': 'B C D E F G A'}}
DEG = {'Ionian': '1 2 3 4 5 6 7', 'Lydian': '1 2 3 #4 5 6 7', 'Mixolydian': '1 2 3 4 5 6 ♭7',
       'Dorian': '1 2 ♭3 4 5 6 ♭7', 'Aeolian': '1 2 ♭3 4 5 ♭6 ♭7',
       'Phrygian': '1 ♭2 ♭3 4 5 ♭6 ♭7', 'Locrian': '1 ♭2 ♭3 4 ♭5 ♭6 ♭7'}
STEPS = {'Ionian': [2, 2, 1, 2, 2, 2, 1], 'Lydian': [2, 2, 2, 1, 2, 2, 1], 'Mixolydian': [2, 2, 1, 2, 2, 1, 2],
         'Dorian': [2, 1, 2, 2, 2, 1, 2], 'Aeolian': [2, 1, 2, 2, 1, 2, 2], 'Phrygian': [1, 2, 2, 2, 1, 2, 2],
         'Locrian': [1, 2, 2, 1, 2, 2, 2]}

# ---------------------------------------------------------------- guitar chord shapes (low E to high e)
SHAPES = {
    'E': '022100', 'A': 'x02220', 'B': 'x24442', 'D': 'xx0232', 'F': '133211', 'C': 'x32010', 'G': '320003',
    'F#': '244322', 'C#': 'x46664',
    'Em': '022000', 'Bm': 'x24432', 'C#m': 'x46654', 'F#m': '244222', 'G#m': '466444', 'D#m': 'x68876',
    'D#dim': 'xx1242', 'A#dim': 'x1232x', 'Edim': 'xx2353', 'Bdim': 'x2343x',
    'E7': '020100', 'A7': 'x02020', 'B7': 'x21202', 'F#7': '242322',
    'F#m7': '242222', 'C#m7': 'x46454', 'Em7': '022030', 'Bm7': 'x24232', 'G#m7': '464444',
    'E6': '022120', 'B6': 'x24444', 'Emaj7': '021100', 'Bmaj7': 'x24342', 'B7b9': 'x2121x', 'F#7b9': 'x9898x',
    'Eadd9': '024100', 'Aadd9': 'x02420', 'Badd9': '799879', 'Bsus4': 'x24452', 'F#sus4': '244422',
    'E5': '022xxx', 'A5': '577xxx', 'G5': '355xxx', 'C5': 'x355xx', 'B5': 'x244xx', 'C#5': 'x466xx',
    'D5': 'x577xx', 'F#5': '244xxx', 'G#5': '466xxx'}
QUAL = {'': [0, 4, 7], 'm': [0, 3, 7], 'dim': [0, 3, 6], '7': [0, 4, 7, 10], 'm7': [0, 3, 7, 10], '6': [0, 4, 7, 9],
        'maj7': [0, 4, 7, 11], '7b9': [0, 4, 7, 10, 1], 'add9': [0, 4, 7, 2], 'sus4': [0, 5, 7], '5': [0, 7]}
OPEN = [4, 9, 2, 7, 11, 4]              # open strings as pitch classes, low E to high e
OPEN_ABS = [40, 45, 50, 55, 59, 64]     # open strings as MIDI numbers
STRING_NAMES = ['E', 'A', 'D', 'G', 'B', 'e']
TONE_OVERRIDE = {'Edim': 'E G B♭', 'C#': 'C# E# G#'}   # spellings the sharp list gets wrong


def parse(name):
    m = re.match(r'^([A-G]#?)(.*)$', name)
    return m.group(1), m.group(2)


def tones(name):
    r, q = parse(name)
    return [(PC[r] + i) % 12 for i in QUAL[q]]


def tone_text(name):
    if name in TONE_OVERRIDE:
        return TONE_OVERRIDE[name]
    return ' '.join(SHARP[p] for p in tones(name))


def shape_notes(name):
    return [None if c == 'x' else (OPEN[i] + int(c)) % 12 for i, c in enumerate(SHAPES[name])]


# ---------------------------------------------------------------- triads in every mode (F6, E1)
ROM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
MAJ = [0, 2, 4, 5, 7, 9, 11]


def triads(key, mode):
    """The seven triads of a mode, spelled from its scale: (name, roman, quality, (root, 3rd, 5th))."""
    notes = SCALES[key][mode].split()
    root = PC[key]
    out = []
    for d in range(7):
        a, b, c = notes[d], notes[(d + 2) % 7], notes[(d + 4) % 7]
        t, f = (PC[b] - PC[a]) % 12, (PC[c] - PC[a]) % 12
        q = {(4, 7): 'maj', (3, 7): 'min', (3, 6): 'dim'}[(t, f)]
        off = (PC[a] - root) % 12 - MAJ[d]
        acc = {0: '', -1: '♭', 1: '#'}[off]
        r = ROM[d] if q == 'maj' else ROM[d].lower()
        r = acc + r + ('°' if q == 'dim' else '')
        name = disp(a) + {'maj': '', 'min': 'm', 'dim': 'dim'}[q]
        out.append((name, r, q, (a, b, c)))
    return out


# ---------------------------------------------------------------- two-octave arpeggios (E1)
ARP_DEG = {'maj': ['1', '3', '5'], 'min': ['1', '♭3', '5'], 'dim': ['1', '♭3', '♭5']}
ARP_IV = {'maj': [0, 4, 7], 'min': [0, 3, 7], 'dim': [0, 3, 6]}


def arpeggio(root_name, q):
    """Root on the low E string, up two octaves (1 3 5 1 3 5 1) to the same fret on the high e string.
    Returns ([(string, fret, degree_index)], root_fret)."""
    f = (PC[root_name] - 4) % 12
    base = 40 + f
    pitches = [base + o * 12 + iv for o in range(2) for iv in ARP_IV[q]] + [base + 24]
    for lo_off, span in ((1, 4), (1, 5), (2, 5)):
        lo = max(0, f - lo_off)
        out, s, ok = [], 0, True
        for i, p in enumerate(pitches):
            hit = None
            for ss in range(s, 6):
                fr = p - OPEN_ABS[ss]
                if lo <= fr <= lo + span:
                    hit = (ss, fr, i % 3)
                    break
            if hit is None:
                ok = False
                break
            out.append(hit)
            s = hit[0]
        if ok:
            break
    assert ok, (root_name, q)
    assert [OPEN_ABS[s] + fr for s, fr, _ in out] == pitches
    assert out[0][0] == 0 and out[-1][0] == 5
    frets = [fr for _, fr, _ in out]
    assert max(frets) - min(frets) <= 5, (root_name, q, frets)
    return out, f


# ---------------------------------------------------------------- one-octave scale positions (tabs)
def scale_positions(key, mode):
    root_abs = 40 if key == 'E' else 47
    start_string = 0 if key == 'E' else 1
    lo = 0 if key == 'E' else 1
    pitches = [root_abs]
    for st in STEPS[mode]:
        pitches.append(pitches[-1] + st)
    out, s = [], start_string
    for p in pitches:
        for span in (4, 5):
            hit = None
            for ss in range(s, 6):
                fr = p - OPEN_ABS[ss]
                if lo <= fr <= lo + span or (fr == 0 and lo == 0):
                    hit = (ss, fr)
                    break
            if hit:
                break
        assert hit, (key, mode, p)
        out.append(hit)
        s = hit[0]
    want = [PC[n] for n in SCALES[key][mode].split()] + [PC[key]]
    got = [(OPEN_ABS[ss] + fr) % 12 for ss, fr in out]
    assert got == want, (key, mode, got, want)
    return out



# ---------------------------------------------------------------- arpeggio up, scale down (E2 to E8)
PARENT_MODES = ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian']


def arp_scale_info(key, degree=0):
    """The chord on a degree of the key's major scale, and the mode that starts on its root."""
    parent = SCALES[key]['Ionian'].split()
    name, roman, q, notes = triads(key, 'Ionian')[degree]
    return dict(chord=name, roman=roman, quality=q, chord_notes=notes, root=notes[0],
                mode=PARENT_MODES[degree], names=parent[degree:] + parent[:degree])


def arp_scale_exercise(key, degree=0):
    """The chord on a degree of the key's major scale: its arpeggio up two octaves from the root on the
    low E string (the E1 shape), then the parent major scale's notes back down two octaves from that root,
    in the same position (which is the mode on that root). Degree 0 is E2.
    Returns [(string, fret, role, note_name)] with role 'arp' or 'scale', 21 notes."""
    info = arp_scale_info(key, degree)
    names = info['names']
    up, _ = arpeggio(info['root'], info['quality'])
    lo = min(fr for _, fr, _ in up)
    top = OPEN_ABS[up[-1][0]] + up[-1][1]
    order = (names[1:][::-1] + [names[0]]) * 2        # the scale down, twice, ending on the low root
    for lo_win, span in ((lo, 4), (lo, 5), (max(0, lo - 1), 5)):
        out = [(s, fr, 'arp', names[[0, 2, 4][d]]) for s, fr, d in up]
        pitch, s, ok = top, up[-1][0], True
        for n in order:
            pitch -= (PC[out[-1][3]] - PC[n]) % 12
            hit = None
            for ss in range(s, -1, -1):
                fr = pitch - OPEN_ABS[ss]
                if lo_win <= fr <= lo_win + span or (fr == 0 and lo_win == 0):
                    hit = (ss, fr); break
            if hit is None:
                ok = False; break
            out.append((hit[0], hit[1], 'scale', n)); s = hit[0]
        if ok:
            break
    assert ok, (key, degree, 'no position found')
    # checks: right pitches, two octaves each way, every note in the parent scale, compact box
    assert pitch == OPEN_ABS[up[0][0]] + up[0][1], (key, degree, 'does not end on the low root')
    assert all((OPEN_ABS[ss] + fr) % 12 == PC[n] for ss, fr, _, n in out)
    assert all(PC[n] in {PC[x] for x in names} for *_, n in out)
    frets = [fr for _, fr, _, _ in out if fr]
    assert max(frets) - min(frets) <= 5, (key, degree, frets)
    assert len(out) == 21
    return out


# ---------------------------------------------------------------- checks
def check_all():
    """Return a list of problems; empty means everything is correct."""
    bad = []
    for name in SHAPES:
        r, q = parse(name)
        t = tones(name)
        sn = [n for n in shape_notes(name) if n is not None]
        need = set(t)
        if q in ('7b9', '7'):
            need = need - {(PC[r] + 7) % 12}   # the fifth may be left out
        if not (set(sn) <= set(t) and need <= set(sn) and sn[0] == PC[r]):
            bad.append(('shape', name, SHAPES[name], [SHARP[n] for n in sn]))
    base = None
    start = {'Ionian': 0, 'Dorian': 1, 'Phrygian': 2, 'Lydian': 3, 'Mixolydian': 4, 'Aeolian': 5, 'Locrian': 6}
    for key in SCALES:
        for mode, txt in SCALES[key].items():
            pcs = [PC[n] for n in txt.split()]
            want = [PC[key]]
            for s in STEPS[mode][:-1]:
                want.append((want[-1] + s) % 12)
            if pcs != want:
                bad.append(('scale', key, mode))
            if len({n[0] for n in txt.split()}) != 7:
                bad.append(('scale letters', key, mode))
            try:
                scale_positions(key, mode)
            except AssertionError as e:
                bad.append(('scale tab', key, mode, str(e)))
            tr = triads(key, mode)
            if base is None:
                base = [q for _, _, q, _ in triads('E', 'Ionian')]
            scale = set(pcs)
            if not all({PC[x] for x in n} <= scale for *_, n in tr):
                bad.append(('triad notes', key, mode))
            if [q for _, _, q, _ in tr] != base[start[mode]:] + base[:start[mode]]:
                bad.append(('triad pattern', key, mode))
            for name, _, q, notes in tr:
                try:
                    arpeggio(notes[0], q)
                except AssertionError as e:
                    bad.append(('arpeggio', key, mode, name, str(e)))
        for degree in range(7):
            try:
                arp_scale_exercise(key, degree)
            except AssertionError as e:
                bad.append(('arpeggio and scale', key, degree, str(e)))
    return bad
