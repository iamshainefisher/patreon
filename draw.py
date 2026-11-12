"""Drawing for the Theory in E series: post diagram sheets, the F6 chord grid,
the E1 arpeggio sheets and the summary charts. All music comes from theory.py."""
import os, math, logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Wedge

from theory import (PC, disp, disp_name, SCALES, DEG, STEPS, SHAPES, OPEN, ORDER, POST, STRING_NAMES,
                    parse, tone_text, triads, arpeggio, ARP_DEG, ARP_IV, arp_scale_exercise, arp_scale_info)

# Inter matches the published images; any machine without it falls back to DejaVu Sans quietly.
matplotlib.rcParams['font.family'] = ['Inter', 'DejaVu Sans', 'sans-serif']
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

OUT = 'output/diagrams'   # make_all.py sets this

# ---------------------------------------------------------------- house colours
INK = '#1f2430'; MUTE = '#6b7280'; LINE = '#9aa3b2'; TONE = '#dbe6f7'; TONE_E = '#3b6fb6'
ACC = '#f4a340'; ACC_E = '#b96a00'; BG = '#ffffff'; PANEL = '#f7f8fb'


class Canvas:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.fig = plt.figure(figsize=(W / 100, H / 100), dpi=200)
        self.ax = self.fig.add_axes([0, 0, 1, 1]); self.ax.set_xlim(0, W); self.ax.set_ylim(H, 0)
        self.ax.axis('off'); self.fig.patch.set_facecolor(BG)

    def text(self, x, y, s, size=14, weight='normal', color=INK, ha='left', va='center', **k):
        self.ax.text(x, y, s, fontsize=size * 0.72, fontweight=weight, color=color, ha=ha, va=va, **k)

    def rect(self, x, y, w, h, fc=BG, ec='none', lw=1, z=1, r=0):
        if r:
            p = FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r, boxstyle=f'round,pad={r}', fc=fc, ec=ec, lw=lw, zorder=z)
        else:
            p = Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=z)
        self.ax.add_patch(p)

    def line(self, x1, y1, x2, y2, c=LINE, lw=1, z=2):
        self.ax.plot([x1, x2], [y1, y2], color=c, lw=lw, zorder=z, solid_capstyle='butt')

    def dot(self, x, y, r, kind, label=None, size=9.5, z=5):
        fc, ec, tc, lw = {'root': (INK, INK, '#ffffff', 1.2), 'tone': (TONE, TONE_E, INK, 1.2), 'chg': (ACC, ACC_E, INK, 2.2),
                          'plain': (TONE_E, TONE_E, '#ffffff', 1.0)}[kind]
        self.ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=lw, zorder=z))
        if label:
            self.text(x, y + 0.5, label, size=size, weight='bold', color=tc, ha='center', va='center', zorder=z + 1)

    def save(self, name):
        self.fig.savefig(os.path.join(OUT, name), dpi=200, facecolor=BG); plt.close(self.fig)
        return name


def header(c, title, sub):
    c.text(34, 44, title, size=25, weight='bold'); c.text(34, 74, sub, size=13, color=MUTE)
    c.text(c.W - 34, 44, 'Theory in E', size=13, color=MUTE, ha='right')


# ================================================================ standard post sheet (F1-F5, M1-M8, ER1-ER11)
def kinds(notes, changed):
    m = {}
    for i, n in enumerate(notes):
        m[PC[n]] = ('root' if i == 0 else 'chg' if n in changed else 'tone', disp(n))
    return m


def fretboard(c, x0, y0, notes, changed):
    nut = x0 + 44; fw = (c.W - 60 - nut) / 12; sp = 24; km = kinds(notes, changed)
    rows = [4, 11, 7, 2, 9, 4]; names = ['e', 'B', 'G', 'D', 'A', 'E']
    c.rect(nut, y0, fw * 12, sp * 5, fc='#fbfaf7', z=1)
    for f in range(13):
        c.line(nut + f * fw, y0, nut + f * fw, y0 + sp * 5, c=INK if f == 0 else LINE, lw=4 if f == 0 else 1.2)
    for i in range(6):
        c.line(nut, y0 + i * sp, nut + 12 * fw, y0 + i * sp, c='#7c8494', lw=0.9 + i * 0.22)
        c.text(x0 - 22, y0 + i * sp, names[i], size=11, color=MUTE, ha='center')
    for f in (3, 5, 7, 9, 12):
        c.text(nut + (f - 0.5) * fw, y0 + sp * 5 + 24, str(f), size=11, color=MUTE, ha='center')
    for i, op in enumerate(rows):
        for f in range(13):
            p = (op + f) % 12
            if p in km:
                x = x0 + 16 if f == 0 else nut + (f - 0.5) * fw
                c.dot(x, y0 + i * sp, 10.5, km[p][0], km[p][1], size=8.6 if len(km[p][1]) > 1 else 9.6)
    return y0 + sp * 5 + 40


def keyboard(c, x0, y0, notes, changed, mode):
    ww, wh, bw, bh = 38, 104, 23, 64
    whites = [0, 2, 4, 5, 7, 9, 11]; km = kinds(notes, changed)
    start = PC[notes[0]]; marks = [start]
    for s in STEPS[mode]:
        marks.append(marks[-1] + s)
    for o in range(2):
        for i, p in enumerate(whites):
            x = x0 + (o * 7 + i) * ww
            c.rect(x, y0, ww, wh, fc='#ffffff', ec='#4b5563', lw=1, z=2)
            if o * 12 + p in marks:
                k = km[p % 12]; c.dot(x + ww / 2, y0 + wh - 20, 12, k[0], k[1], size=8.8 if len(k[1]) > 1 else 10)
    for o in range(2):
        for i, p in zip([0, 1, 3, 4, 5], [1, 3, 6, 8, 10]):
            x = x0 + (o * 7 + i + 1) * ww - bw / 2
            c.rect(x, y0, bw, bh, fc='#262b36', ec='#262b36', z=3)
            if o * 12 + p in marks:
                k = km[p % 12]; c.dot(x + bw / 2, y0 + bh - 17, 11.5, k[0], k[1], size=8.2)
    return x0 + 14 * ww, y0 + wh


def chord_box(c, cx, y0, name, roman):
    sp, fh, rows = 16, 22, 5
    frets = [None if ch == 'x' else int(ch) for ch in SHAPES[name]]
    fretted = [f for f in frets if f]
    base = 1 if max(fretted) <= 5 else min(fretted)
    assert max(fretted) - base + 1 <= rows, name
    left = cx - sp * 2.5; top = y0 + 58
    c.text(cx, y0 + 10, disp_name(name), size=19, weight='bold', ha='center')
    c.rect(left, top, sp * 5, fh * rows, fc='#ffffff', z=1)
    for i in range(6):
        c.line(left + i * sp, top, left + i * sp, top + fh * rows, c='#4b5563', lw=1.1)
    for r in range(rows + 1):
        nut = r == 0 and base == 1
        c.line(left, top + r * fh, left + sp * 5, top + r * fh, c=INK if nut else '#4b5563', lw=4 if nut else 1.1)
    if base > 1:
        c.text(left - 9, top + fh / 2, f'{base}fr', size=10.5, color=MUTE, ha='right')
    rpc = PC[parse(name)[0]]
    for i, f in enumerate(frets):
        x = left + i * sp
        if f is None:
            c.text(x, top - 13, '×', size=13, color=MUTE, ha='center')
        elif f == 0:
            is_root = OPEN[i] % 12 == rpc
            c.ax.add_patch(Circle((x, top - 13), 4.6, fc='#ffffff', ec=INK if is_root else '#4b5563', lw=1.6 if is_root else 1.1, zorder=4))
        else:
            c.dot(x, top + (f - base + 0.5) * fh, 6.6, 'root' if (OPEN[i] + f) % 12 == rpc else 'plain')
    yb = top + fh * rows
    c.text(cx, yb + 20, roman, size=14, weight='bold', ha='center', color=INK)
    c.text(cx, yb + 41, ' '.join(disp(t) if len(t) == 2 and t[1] == 'b' else t for t in tone_text(name).split()),
           size=10.5, color=MUTE, ha='center')
    return yb + 56


def legend(c, y, has_changed, chg_label):
    x = 60
    for kind, lab in [('root', 'Root'), ('tone', 'Scale note')] + ([('chg', chg_label)] if has_changed else []):
        c.dot(x + 10, y, 9, kind); c.text(x + 28, y, lab, size=11.5, color=MUTE); x += 46 + len(lab) * 7.6
    c.dot(c.W - 470, y, 6, 'root'); c.text(c.W - 458, y, 'Chord root', size=11.5, color=MUTE)
    c.dot(c.W - 350, y, 6, 'plain'); c.text(c.W - 338, y, 'Other chord note', size=11.5, color=MUTE)
    c.text(c.W - 60, y, '× = do not play', size=11.5, color=MUTE, ha='right')


def panel(c, y, key, mode, heading, chords, changed, note, chg_text):
    notes = SCALES[key][mode].split()
    h = 392 + (260 if chords else 0)
    c.rect(30, y, c.W - 60, h, fc=PANEL, r=10, z=0)
    c.text(60, y + 34, heading, size=20, weight='bold')
    c.text(c.W - 60, y + 34, '  '.join(disp(n) for n in notes), size=17, weight='bold', color=TONE_E, ha='right')
    yb = fretboard(c, 60, y + 74, notes, changed)
    kx, ky = keyboard(c, 60, yb + 12, notes, changed, mode)
    tx = kx + 50; ty = yb + 30
    c.text(tx, ty, 'Scale degrees', size=11.5, color=MUTE); c.text(tx, ty + 24, DEG[mode].replace(' ', '   '), size=16, weight='bold')
    if chg_text:
        c.text(tx, ty + 56, chg_text[0], size=11.5, color=MUTE); c.text(tx, ty + 80, chg_text[1], size=15, weight='bold', color=ACC_E)
    if note:
        c.text(tx, ty + 56 if not chg_text else ty + 106, note, size=12, color=MUTE)
    if chords:
        cy = ky + 40; n = len(chords); cell = min(150, (c.W - 120) / n); x = 60 + cell / 2
        c.text(60, cy - 8, 'Chords', size=11.5, color=MUTE)
        for nm, ro in chords:
            chord_box(c, x, cy + 10, nm, ro); x += cell
    return y + h + 24


def post_sheet(code, title, sub, mode, headE, headB, chE, chB, slug, noteE=None, noteB=None, chgE=None, chgB=None,
               chg_label='Changed from the major scale', hl=None):
    H = 118 + 2 * (392 + (260 if chE else 0) + 24) + 44
    c = Canvas(1200, H)
    c.rect(30, 26, 92, 54, fc=INK, r=8); c.text(76, 53, code, size=22, weight='bold', color='#ffffff', ha='center')
    c.text(140, 42, title, size=25, weight='bold'); c.text(140, 72, sub, size=13, color=MUTE)
    c.text(c.W - 34, 53, 'Theory in E', size=13, color=MUTE, ha='right')

    def changed(key):
        if hl is not None:
            return set(hl.get(key, []))
        ion = SCALES[key]['Ionian'].split(); cur = SCALES[key][mode].split()
        return {b for a, b in zip(ion, cur) if a != b}

    def ctext(key, given):
        if given:
            return given
        ion = SCALES[key]['Ionian'].split(); cur = SCALES[key][mode].split()
        d = [f'{disp(a)} → {disp(b)}' for a, b in zip(ion, cur) if a != b]
        return ('Changed from the major scale', '    '.join(d)) if d else None

    y = panel(c, 104, 'E', mode, headE, chE, changed('E'), noteE, ctext('E', chgE))
    y = panel(c, y, 'B', mode, headB, chB, changed('B'), noteB, ctext('B', chgB))
    legend(c, y + 6, bool(changed('E') or changed('B')), chg_label)
    return [c.save(f'{code}-{slug}.png')]


# ================================================================ F6: chords in each mode
def mode_chords_grid(c, y, key):
    c.text(34, y, f'In {key}' if key == 'E' else 'A fifth higher: in B', size=19, weight='bold')
    x0, lw, cw, rh = 34, 196, 133, 66; y0 = y + 24
    for d in range(7):
        c.text(x0 + lw + d * cw + cw / 2, y0 + 12, f'chord {d + 1}', size=11, color=MUTE, ha='center')
    for r, m in enumerate(ORDER):
        yy = y0 + 28 + r * rh
        c.rect(x0, yy, 52, rh - 10, fc=INK, r=6); c.text(x0 + 26, yy + (rh - 10) / 2, POST[m], size=12, weight='bold', color='#fff', ha='center')
        c.text(x0 + 64, yy + (rh - 10) / 2, f'{key} {m}', size=15, weight='bold')
        for d, (name, rom, q, _) in enumerate(triads(key, m)):
            fc = {'maj': TONE, 'min': PANEL, 'dim': ACC}[q]; ec = {'maj': TONE_E, 'min': LINE, 'dim': ACC_E}[q]
            x = x0 + lw + d * cw
            c.rect(x + 4, yy, cw - 8, rh - 10, fc=fc, ec=ec, lw=1.6 if d == 0 else 0.8, r=7)
            c.text(x + cw / 2, yy + 19, name, size=17, weight='bold', ha='center')
            c.text(x + cw / 2, yy + 41, rom, size=12, color=INK if q == 'dim' else MUTE, ha='center')
    return y0 + 28 + 7 * rh


def mode_chords_sheet(code='F6', slug='chords-in-each-mode'):
    c = Canvas(1200, 1290)
    header(c, f'{code}  Chords in each mode', 'A triad on every note of each mode, from brightest to darkest. The first column is each mode\'s home chord.')
    y = mode_chords_grid(c, 132, 'E')
    y = mode_chords_grid(c, y + 44, 'B')
    ly = y + 30
    for i, (fc, ec, lab) in enumerate([(TONE, TONE_E, 'Major'), (PANEL, LINE, 'Minor'), (ACC, ACC_E, 'Diminished')]):
        x = 40 + i * 170; c.rect(x, ly - 12, 30, 24, fc=fc, ec=ec, lw=1, r=5); c.text(x + 42, ly, lab, size=12, color=MUTE)
    c.text(1166, ly, 'Roman numerals are measured against the major scale of E (or B).', size=12, color=MUTE, ha='right')
    return [c.save(f'{code}-{slug}.png')]


# ================================================================ E1: two-octave arpeggios
def arpeggio_cell(c, x, y, w, name, rom, q, notes):
    pos, f = arpeggio(notes[0], q)
    c.rect(x, y, w, 262, fc=PANEL, r=8, z=0)
    c.text(x + 18, y + 26, name, size=20, weight='bold')
    c.text(x + 18 + len(name) * 13 + 14, y + 27, rom, size=14, color=MUTE)
    degs = ARP_DEG[q]
    c.text(x + w - 18, y + 27, '   '.join(f'{d} {disp(n)}' for d, n in zip(degs, notes)), size=12.5, color=INK, ha='right')
    frets = [fr for _, fr, _ in pos]
    lo = min(frets) if min(frets) > 0 else 0
    nf = 5
    left, top, fw, sp = x + 46, y + 58, (w - 80) / nf, 17
    is_open = lo == 0
    first = 1 if is_open else lo
    c.rect(left, top, fw * nf, sp * 5, fc='#fbfaf7', z=1)
    for k in range(nf + 1):
        thick = is_open and k == 0
        c.line(left + k * fw, top, left + k * fw, top + sp * 5, c=INK if thick else LINE, lw=3.5 if thick else 1.1)
    for i in range(6):
        c.line(left, top + i * sp, left + nf * fw, top + i * sp, c='#7c8494', lw=0.8 + i * 0.18)
        c.text(left - 30, top + i * sp, STRING_NAMES[5 - i], size=10, color=MUTE, ha='center')
    for k in range(nf):
        c.text(left + (k + 0.5) * fw, top + sp * 5 + 15, str(first + k), size=10, color=MUTE, ha='center')
    for s, fr, d in pos:
        cx = left - 12 if fr == 0 else left + (fr - first + 0.5) * fw
        cy = top + (5 - s) * sp
        fc, ec, tc = {0: (INK, INK, '#fff'), 1: (TONE_E, TONE_E, '#fff'), 2: (TONE, TONE_E, INK)}[d]
        c.ax.add_patch(Circle((cx, cy), 8.2, fc=fc, ec=ec, lw=1.1, zorder=5))
        c.text(cx, cy + 0.5, degs[d], size=7.6, weight='bold', color=tc, ha='center', zorder=6)
    # keyboard: two octaves of the arpeggio from the root
    kx, ky, ww, wh, bw, bh = x + 46, y + 172, 21, 74, 13, 46
    rpc = PC[notes[0]]
    whites = [0, 2, 4, 5, 7, 9, 11]
    start_white = rpc
    while start_white % 12 not in whites:
        start_white -= 1
    marks = {rpc + o * 12 + iv: i for o in range(2) for i, iv in enumerate(ARP_IV[q])}
    marks[rpc + 24] = 0
    a, wpos = start_white, []
    while len(wpos) < 16:
        if a % 12 in whites:
            wpos.append(a)
        a += 1
    for i, a in enumerate(wpos):
        c.rect(kx + i * ww, ky, ww, wh, fc='#ffffff', ec='#4b5563', lw=0.9, z=2)
        if a in marks:
            d = marks[a]; fc, ec = {0: (INK, INK), 1: (TONE_E, TONE_E), 2: (TONE, TONE_E)}[d]
            c.ax.add_patch(Circle((kx + i * ww + ww / 2, ky + wh - 12), 6.5, fc=fc, ec=ec, lw=1, zorder=5))
    for i, a in enumerate(wpos[:-1]):
        if (a + 1) % 12 not in whites:
            bx = kx + (i + 1) * ww - bw / 2
            c.rect(bx, ky, bw, bh, fc='#262b36', ec='#262b36', z=3)
            if a + 1 in marks:
                fc = {0: INK, 1: TONE_E, 2: TONE}[marks[a + 1]]
                c.ax.add_patch(Circle((bx + bw / 2, ky + bh - 11), 6.6, fc=fc, ec='#ffffff', lw=1.0, zorder=5))
    assert len(marks) == 7 and all(m in wpos or m in [w + 1 for w in wpos] for m in marks), name
    c.text(kx + 16 * ww + 14, ky + 20, 'Keys: two octaves', size=10.5, color=MUTE)
    c.text(kx + 16 * ww + 14, ky + 38, 'from the root', size=10.5, color=MUTE)


def arpeggio_sheet(key, mode, code='E1'):
    W, H = 1200, 104 + 4 * 278 + 6
    c = Canvas(W, H)
    c.rect(30, 26, 92, 54, fc=INK, r=8); c.text(76, 53, code, size=22, weight='bold', color='#fff', ha='center')
    c.text(140, 42, f'Arpeggios in {key} {mode}', size=25, weight='bold')
    sub = 'Two octaves from the root on the low E string to the same fret on the high e string.'
    if key == 'B':
        sub = 'A fifth higher. ' + sub
    c.text(140, 72, sub, size=13, color=MUTE)
    c.text(W - 34, 53, f'Theory in E · chords from F6 and {POST[mode]}', size=13, color=MUTE, ha='right')
    for i, (name, rom, q, notes) in enumerate(triads(key, mode)):
        arpeggio_cell(c, 30 + (i % 2) * 575, 104 + (i // 2) * 278, 565, name, rom, q, notes)
    x, y = 30 + 575, 104 + 3 * 278
    c.rect(x, y, 565, 262, fc='#ffffff', ec=LINE, lw=1, r=8, z=0)
    c.text(x + 20, y + 30, 'How to read it', size=16, weight='bold')
    for j, (fc, ec, tc, lab, txt) in enumerate([(INK, INK, '#fff', '1', 'Root'),
                                               (TONE_E, TONE_E, '#fff', '3', 'Third (♭3 in minor and diminished)'),
                                               (TONE, TONE_E, INK, '5', 'Fifth (♭5 in diminished)')]):
        yy = y + 68 + j * 34
        c.ax.add_patch(Circle((x + 34, yy), 10, fc=fc, ec=ec, lw=1.1, zorder=5))
        c.text(x + 34, yy + 0.5, lab, size=9, weight='bold', color=tc, ha='center', zorder=6)
        c.text(x + 56, yy, txt, size=12.5, color=INK)
    c.text(x + 20, y + 182, 'Play one note per beat, up and back down.', size=12.5, color=MUTE)
    c.text(x + 20, y + 206, 'Fret numbers sit under each box; a dot left of', size=12.5, color=MUTE)
    c.text(x + 20, y + 228, 'the nut is an open string.', size=12.5, color=MUTE)
    return c.save(f'{code}-arpeggios-{key}-{mode.lower()}.png')


def arpeggio_sheets(code='E1'):
    return [arpeggio_sheet(k, m, code) for k in 'EB' for m in ORDER]


# ================================================================ E2: arpeggio up, scale down
def _role_style(n, chord):
    """The chord's root, third and fifth keep the arpeggio colours; other scale notes are plain."""
    if n == chord[0]:
        return INK, INK, '#fff'
    if n == chord[1]:
        return TONE_E, TONE_E, '#fff'
    if n == chord[2]:
        return TONE, TONE_E, INK
    return '#ffffff', '#4b5563', INK


def _order_board(c, left, top, width, notes, first_step, chord, lo, title):
    nf, sp = 5, 22
    fw = width / nf
    c.text(left - 34, top - 30, title, size=14, weight='bold')
    is_open = lo == 0
    first = 1 if is_open else lo
    c.rect(left, top, fw * nf, sp * 5, fc='#fbfaf7', z=1)
    for k in range(nf + 1):
        thick = is_open and k == 0
        c.line(left + k * fw, top, left + k * fw, top + sp * 5, c=INK if thick else LINE, lw=3.5 if thick else 1.1)
    for i in range(6):
        c.line(left, top + i * sp, left + nf * fw, top + i * sp, c='#7c8494', lw=0.8 + i * 0.18)
        c.text(left - 32, top + i * sp, STRING_NAMES[5 - i], size=10.5, color=MUTE, ha='center')
    for k in range(nf):
        c.text(left + (k + 0.5) * fw, top + sp * 5 + 17, str(first + k), size=10.5, color=MUTE, ha='center')
    for j, (s, fr, _, n) in enumerate(notes):
        cx = left - 14 if fr == 0 else left + (fr - first + 0.5) * fw
        cy = top + (5 - s) * sp
        fc, ec, tc = _role_style(n, chord)
        c.ax.add_patch(Circle((cx, cy), 10, fc=fc, ec=ec, lw=1.2, zorder=5))
        c.text(cx, cy + 0.5, str(first_step + j), size=8.4, weight='bold', color=tc, ha='center', zorder=6)


def _bars(c, x0, y0, w, ex, chord):
    """Six bars of 4/4, one note per beat; the last note is held for the whole bar."""
    bw = w / 6
    beats = [n for *_, n in ex]
    for b in range(6):
        x = x0 + b * bw
        c.rect(x + 3, y0, bw - 6, 58, fc='#ffffff', ec=LINE, lw=1, r=6, z=1)
        c.text(x + 12, y0 + 12, f'bar {b + 1}', size=9.5, color=MUTE)
        notes = beats[b * 4:(b + 1) * 4] if b < 5 else beats[20:21]
        for k, n in enumerate(notes):
            idx = b * 4 + k
            fc, ec, tc = _role_style(n, chord)
            if idx >= 7 and fc == '#ffffff':
                fc, ec, tc = PANEL, LINE, INK
            cx = x + 20 + k * (bw - 30) / 4 + (bw - 30) / 8
            if b == 5:
                cx = x + 30
            c.rect(cx - 14, y0 + 24, 28, 24, fc=fc, ec=ec, lw=1, r=5, z=2)
            c.text(cx, y0 + 36, disp(n), size=11.5, weight='bold', color=tc, ha='center', zorder=3)
        if b == 5:
            c.text(x + 52, y0 + 36, 'hold 4 beats', size=10.5, color=MUTE)
        if b == 1:
            c.text(x + 3 + (bw - 6) * 0.72, y0 - 8, '↑ up │ down ↓', size=10, color=MUTE, ha='center')


QUALITY_WORD = {'maj': 'major', 'min': 'minor', 'dim': 'diminished'}


def arp_scale_sheet(code='E2', slug='e-ionian-arpeggio-and-scale', degree=0):
    W, H = 1200, 104 + 2 * 470 + 70
    c = Canvas(W, H)
    c.rect(30, 26, 92, 54, fc=INK, r=8); c.text(76, 53, code, size=22, weight='bold', color='#fff', ha='center')
    e = arp_scale_info('E', degree)
    if degree == 0:
        title, sub, corner = ('Arpeggio up, scale down',
                              'The major chord up two octaves from the root, then the major (Ionian) scale back down. One note per beat.',
                              'Theory in E \u00b7 builds on E1 and M2')
    else:
        title = f'Arpeggio up, scale down: the {e["roman"]} chord'
        sub = (f'The {e["roman"]} chord of the major key up two octaves from its root, then the key\'s notes back down '
               f'from that root: the {e["mode"]} mode. One note per beat.')
        corner = f'Theory in E \u00b7 builds on E2, F6 and {POST[e["mode"]]}'
    c.text(140, 42, title, size=25, weight='bold')
    c.text(140, 72, sub, size=13, color=MUTE)
    c.text(W - 34, 53, corner, size=13, color=MUTE, ha='right')
    y = 104
    for key in 'EB':
        info = arp_scale_info(key, degree)
        ex = arp_scale_exercise(key, degree)
        names = info['names']
        chord = info['chord_notes']
        lo = min(fr for s, fr, r, n in ex if r == 'arp')
        c.rect(30, y, W - 60, 452, fc=PANEL, r=10, z=0)
        label = f'{disp(info["root"])} {QUALITY_WORD[info["quality"]]} arpeggio, then {disp(info["root"])} {info["mode"]}'
        head = f'In E: {label}' if key == 'E' else f'A fifth higher: {label}'
        c.text(60, y + 32, head, size=19, weight='bold')
        c.text(W - 60, y + 32, '  '.join(disp(n) for n in names), size=16, weight='bold', color=TONE_E, ha='right')
        _order_board(c, 110, y + 104, 440, ex[:7], 1, chord, lo, 'Up: the arpeggio, notes 1 to 7')
        _order_board(c, 680, y + 104, 440, ex[7:], 8, chord, lo, 'Down: the scale, notes 8 to 21')
        _bars(c, 60, y + 270, W - 120, ex, chord)
        c.text(60, y + 368, f'Keys: right hand, from the {disp(names[0])} below middle C', size=11.5, color=MUTE)
        # keyboard strip: two octaves of the scale, chord tones coloured
        kx, ky, ww, wh, bw, bh = 60, y + 384, 26, 58, 16, 36
        whites = [0, 2, 4, 5, 7, 9, 11]
        rpc = PC[names[0]]
        sw = rpc
        while sw % 12 not in whites:
            sw -= 1
        scale = {}
        p = rpc
        for o in range(2):
            for i, n in enumerate(names):
                scale[p] = n
                p += STEPS[info['mode']][i]
        scale[p] = names[0]
        a, wpos = sw, []
        while len(wpos) < 16:
            if a % 12 in whites:
                wpos.append(a)
            a += 1
        for i, a in enumerate(wpos):
            c.rect(kx + i * ww, ky, ww, wh, fc='#ffffff', ec='#4b5563', lw=0.9, z=2)
            if a in scale:
                fc, ec, _ = _role_style(scale[a], chord)
                c.ax.add_patch(Circle((kx + i * ww + ww / 2, ky + wh - 11), 6.5, fc=fc, ec=ec, lw=1.1, zorder=5))
        for i, a in enumerate(wpos[:-1]):
            if (a + 1) % 12 not in whites:
                bx = kx + (i + 1) * ww - bw / 2
                c.rect(bx, ky, bw, bh, fc='#262b36', ec='#262b36', z=3)
                if a + 1 in scale:
                    fc, _, _ = _role_style(scale[a + 1], chord)
                    c.ax.add_patch(Circle((bx + bw / 2, ky + bh - 9), 6.5, fc=fc, ec='#ffffff', lw=1.0, zorder=5))
        assert len(scale) == 15 and all(m in wpos or m - 1 in wpos for m in scale), key
        c.text(kx + 16 * ww + 20, ky + 20, 'Two octaves of the scale.', size=11, color=MUTE)
        c.text(kx + 16 * ww + 20, ky + 40, 'Play the coloured keys going up, every key coming down.', size=11, color=MUTE)
        y += 470
    ly = y + 22
    items = [((INK, INK), 'Root'), ((TONE_E, TONE_E), 'Third'), ((TONE, TONE_E), 'Fifth'), (('#ffffff', '#4b5563'), 'Other scale note')]
    x = 60
    for (fc, ec), lab in items:
        c.ax.add_patch(Circle((x + 10, ly), 9, fc=fc, ec=ec, lw=1.2, zorder=5)); c.text(x + 26, ly, lab, size=11.5, color=MUTE)
        x += 50 + len(lab) * 8
    c.text(W - 60, ly, 'Numbers in the dots give the order to play the notes. A dot left of the nut is an open string.', size=11.5, color=MUTE, ha='right')
    return [c.save(f'{code}-{slug}.png')]


# ================================================================ summary charts
def mode_ladder():
    c = Canvas(1200, 640); header(c, 'The seven modes of E, brightest to darkest', 'Each row changes one note from the row above. Highlighted notes differ from E major (Ionian).')
    x0, y0, cw, rh = 330, 132, 96, 58
    for i in range(7):
        c.text(x0 + i * cw + cw / 2, y0 - 14, str(i + 1), size=12, color=MUTE, ha='center')
    ion = SCALES['E']['Ionian'].split()
    for r, mode in enumerate(ORDER):
        y = y0 + r * rh + 8
        c.rect(30, y, c.W - 60, rh - 8, fc=PANEL if mode != 'Ionian' else '#e9eef8', r=8, z=0)
        c.rect(46, y + 10, 50, 30, fc=INK, r=6); c.text(71, y + 25, POST[mode], size=12, weight='bold', color='#fff', ha='center')
        c.text(112, y + 25, 'E ' + mode, size=17, weight='bold')
        for i, n in enumerate(SCALES['E'][mode].split()):
            c.dot(x0 + i * cw + cw / 2, y + 25, 17, 'root' if i == 0 else ('chg' if n != ion[i] else 'tone'), disp(n), size=11.5)
        c.text(x0 + 7 * cw + 24, y + 25, DEG[mode].replace(' ', '  '), size=12.5, color=MUTE)
    yl = y0 + 7 * rh + 34
    c.text(34, yl, '▲ brighter', size=12.5, color=MUTE); c.text(140, yl, '▼ darker', size=12.5, color=MUTE)
    c.dot(300, yl, 9, 'root'); c.text(316, yl, 'Root', size=11.5, color=MUTE)
    c.dot(390, yl, 9, 'tone'); c.text(406, yl, 'Same as E major', size=11.5, color=MUTE)
    c.dot(560, yl, 9, 'chg'); c.text(576, yl, 'Changed from E major', size=11.5, color=MUTE)
    return [c.save('extra-mode-ladder.png')]


def circle_of_fifths():
    keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'D♭', 'A♭', 'E♭', 'B♭', 'F']
    sig = ['0', '1 sharp', '2 sharps', '3 sharps', '4 sharps', '5 sharps', '6 sharps', '5 flats', '4 flats', '3 flats', '2 flats', '1 flat']
    c = Canvas(1200, 860); header(c, 'The circle of fifths', 'Each step clockwise is a fifth higher. Neighbouring keys share six of their seven notes.')
    cx, cy, R1, R0 = 600, 450, 330, 190
    for i, k in enumerate(keys):
        a0 = 90 - (i * 30) - 15   # the y axis is inverted, so the angles are mirrored
        c.ax.add_patch(Wedge((cx, cy), R1, -a0 - 30, -a0, width=R1 - R0, fc=(INK if k == 'E' else ACC if k == 'B' else PANEL), ec='#ffffff', lw=3, zorder=2))
        am = math.radians(i * 30 - 90); rm = (R1 + R0) / 2
        x, y = cx + rm * math.cos(am), cy + rm * math.sin(am)
        c.text(x, y - 10, k, size=27, weight='bold', ha='center', color='#ffffff' if k == 'E' else INK)
        c.text(x, y + 20, sig[i], size=11, ha='center', color='#e5e7eb' if k == 'E' else (INK if k == 'B' else MUTE))
    c.text(cx, cy - 34, 'E → B', size=30, weight='bold', ha='center')
    c.text(cx, cy + 6, 'one step clockwise', size=14, color=MUTE, ha='center')
    c.text(cx, cy + 32, 'one more sharp: A becomes A#', size=14, color=MUTE, ha='center')
    c.rect(40, 812, 22, 22, fc=INK, r=4); c.text(72, 823, 'E: the home key of the series', size=12.5, color=MUTE)
    c.rect(360, 812, 22, 22, fc=ACC, r=4); c.text(392, 823, 'B: the key at the end of every post', size=12.5, color=MUTE)
    return [c.save('extra-circle-of-fifths.png')]


def twelve_bar():
    c = Canvas(1200, 800); header(c, 'The 12-bar blues', 'Twelve bars, three chords. Read left to right, four beats per bar.')

    def grid(y, title, I, IV, V):
        c.text(34, y, title, size=19, weight='bold')
        rows = [[I, I, I, I], [IV, IV, I, I], [V, IV, I, V]]; rom = [['I7'] * 4, ['IV7', 'IV7', 'I7', 'I7'], ['V7', 'IV7', 'I7', 'V7']]
        bw, bh = 270, 82
        for r in range(3):
            for k in range(4):
                x, yy = 60 + k * (bw + 8), y + 26 + r * (bh + 8); ch = rows[r][k]
                c.rect(x, yy, bw, bh, fc={I: PANEL, IV: TONE, V: ACC}[ch], r=8, z=1)
                c.text(x + 14, yy + 18, f'bar {r * 4 + k + 1}', size=10.5, color=MUTE if ch != V else INK)
                c.text(x + bw / 2, yy + 44, ch, size=27, weight='bold', ha='center')
                c.text(x + bw - 14, yy + 64, rom[r][k], size=12, color=MUTE if ch != V else INK, ha='right')
        return y + 26 + 3 * (bh + 8)
    y = grid(130, 'In E', 'E7', 'A7', 'B7'); grid(y + 50, 'A fifth higher: in B', 'B7', 'E7', 'F#7')
    return [c.save('extra-12-bar-blues.png')]


def practice_routine():
    c = Canvas(1200, 560); header(c, 'The 10-minute practice routine', 'Use it with any post in the series. Set a timer and stop when it ends.')
    segs = [(1, 'Listen', 'Hear the\naudio once.\nJust listen.', PANEL), (2, 'Scale', 'Play the scale in E,\nup and down, slowly.\nSay the note names.', TONE),
            (3, 'Chords', 'Play each chord.\nThen change between\nthem, four beats each.', TONE), (2, 'Play along in E', 'Play the sequence\nwith the audio.', ACC),
            (2, 'Play along in B', 'Same idea, a fifth\nhigher.', ACC)]
    x, unit, t = 40, 112, 0
    for mins, name, desc, fc in segs:
        w = mins * unit
        c.rect(x, 140, w - 8, 250, fc=fc, r=10, z=1)
        c.text(x + 16, 172, f'{mins} min', size=22, weight='bold'); c.text(x + 16, 208, name, size=15, weight='bold')
        c.text(x + 16, 232, desc, size=11.5, color='#374151', va='top', linespacing=1.45)
        c.line(x, 410, x, 424, c=INK, lw=1.4); c.text(x, 442, f'{t}:00', size=11.5, color=MUTE, ha='center')
        x += w; t += mins
    c.line(40, 410, x - 8, 410, c=INK, lw=1.4); c.line(x - 8, 410, x - 8, 424, c=INK, lw=1.4); c.text(x - 8, 442, '10:00', size=11.5, color=MUTE, ha='center')
    c.text(40, 500, 'Short on time? Do the first six minutes. The play-along steps use the tier-exclusive audio; without it, play the sequence on your own and count aloud.', size=12, color=MUTE)
    return [c.save('extra-practice-10-minutes.png')]


def practice_week():
    c = Canvas(1200, 470); header(c, 'One post, one week', 'A new post arrives each week. This plan fits one post into seven days.')
    days = [('Day 1', 'Read and listen', 'Read the post.\nListen to the audio\ntwice.', PANEL), ('Day 2', 'Routine', '10-minute routine.\nFocus on the scale.', TONE),
            ('Day 3', 'Routine', '10-minute routine.\nFocus on the chord\nchanges.', TONE), ('Day 4', 'Rest', 'No practice.\nLet it settle.', '#ffffff'),
            ('Day 5', 'Routine', '10-minute routine.\nFocus on playing\nalong in E.', TONE), ('Day 6', 'The key of B', 'Play the scale and\nthe sequence a fifth\nhigher.', ACC),
            ('Day 7', 'Look back', 'Replay last week\'s\nsequence, then this\nweek\'s. Hear the\ndifference.', PANEL)]
    w = 158
    for i, (d, n, t, fc) in enumerate(days):
        x = 40 + i * (w + 4)
        c.rect(x, 130, w, 280, fc=fc, ec=LINE if fc == '#ffffff' else 'none', lw=1.2, r=10, z=1)
        c.text(x + 14, 160, d, size=12, color=MUTE); c.text(x + 14, 190, n, size=15.5, weight='bold')
        c.text(x + 14, 216, t, size=11.5, color='#374151', va='top', linespacing=1.45)
    return [c.save('extra-practice-week.png')]


EXTRAS = {'mode-ladder': mode_ladder, 'circle-of-fifths': circle_of_fifths, '12-bar-blues': twelve_bar,
          'practice-10-minutes': practice_routine, 'practice-week': practice_week}
