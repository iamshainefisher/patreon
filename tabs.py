"""Guitar tabs for every post, built from the checked shapes and positions in theory.py."""
from theory import SHAPES, ORDER, STRING_NAMES, disp, disp_name, scale_positions, triads, arpeggio, arp_scale_exercise

READ_ME = ('How to read these tabs: the top line is the thinnest string (high e) and the bottom line is the thickest (low E). '
           'A number is the fret to press, and 0 is an open string. In a chord, a string with only a dash is not played. '
           'Chord tabs show one chord per column, in order; strum each for the number of beats in the post. '
           'Scale tabs go up one octave and back down. Arpeggio tabs go up two octaves and back down, one note per beat.')


def chord_tab(chords):
    """One column per chord, high e at the top."""
    cols = []
    for name in chords:
        frets = ['-' if c == 'x' else c for c in SHAPES[name]]
        label = disp_name(name)
        cols.append((label, frets, max(len(label), 2) + 3))
    lines = ['  ' + ''.join(l.ljust(w) for l, _, w in cols)]
    for s in range(5, -1, -1):
        row = STRING_NAMES[s] + '|'
        for _, frets, w in cols:
            row += ('-' + frets[s]).ljust(w, '-')
        lines.append(row + '|')
    return '\n'.join(lines)


def scale_tab(key, mode):
    pos = scale_positions(key, mode)
    seq = pos + pos[-2::-1]
    rows = {s: STRING_NAMES[s] + '|-' for s in range(6)}
    for ss, f in seq:
        for s in range(6):
            rows[s] += (str(f) if s == ss else '').ljust(3, '-')
    return '\n'.join(rows[s] + '|' for s in range(5, -1, -1))


def _arp_system(arps):
    """Two or fewer arpeggios side by side; each goes up two octaves and back down."""
    rows = [n + '|' for n in reversed(STRING_NAMES)]   # e B G D A E
    head = '  '
    for name, pos in arps:
        seq = pos + pos[-2::-1]
        head += name.ljust(3 * len(seq) + 3)
        for r in range(6):
            rows[r] += '-'
        for s, fr in seq:
            for r in range(6):
                rows[r] += (str(fr) if 5 - s == r else '').ljust(3, '-')
        for r in range(6):
            rows[r] += '-|'
    return head.rstrip() + '\n' + '\n'.join(rows)


def arpeggio_tabs(key):
    out = []
    for m in ORDER:
        arps = [(name, [(s, fr) for s, fr, _ in arpeggio(notes[0], q)[0]]) for name, _, q, notes in triads(key, m)]
        systems = [_arp_system(arps[i:i + 2]) for i in range(0, 7, 2)]
        out.append(f'**{key} {m}**\n\n```text\n' + '\n\n'.join(systems) + '\n```\n')
    return '\n'.join(out)


def arp_scale_tab(key, degree=0):
    """Six bars of 4/4, one note per beat; the note names run underneath."""
    ex = arp_scale_exercise(key, degree)
    bars = [ex[i:i + 4] for i in range(0, 20, 4)] + [ex[20:]]
    rows = [n + '|' for n in reversed(STRING_NAMES)]
    names = '  '
    for bar in bars:
        for r in range(6):
            rows[r] += '-'
        names += ' '
        for s, fr, _, n in bar:
            for r in range(6):
                rows[r] += (str(fr) if 5 - s == r else '').ljust(3, '-')
            names += disp(n).ljust(3)
        if len(bar) == 1:
            for r in range(6):
                rows[r] += '-' * 9
            names += ' ' * 9
        for r in range(6):
            rows[r] += '|'
        names += ' '
    return '\n'.join(rows) + '\n' + names.rstrip()


def post_tabs(post):
    out = [f'## {post["code"]}: {post["title"]}\n']
    for heading, item in post.get('tabs', []):
        if isinstance(item, tuple) and item[0] == 'arp_scale':
            out.append(f'**{heading}**\n\n```text\n{arp_scale_tab(*item[1:])}\n```\n')
        elif isinstance(item, tuple) and item[0] == 'arpeggios':
            out.append(f'### {heading}\n\n' + arpeggio_tabs(item[1]))
        elif isinstance(item, tuple):
            out.append(f'**{heading}**\n\n```text\n{scale_tab(*item)}\n```\n')
        else:
            out.append(f'**{heading}**\n\n```text\n{chord_tab(item)}\n```\n')
    return '\n'.join(out)


def all_tabs(posts):
    return '# Theory in E: tabs\n\n' + READ_ME + '\n\n' + '\n'.join(post_tabs(p) for p in posts if p.get('tabs'))
