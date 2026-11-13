"""Every table in the series doc as an image, all the same width.

The doc is the source for its tables. Export each tab as Markdown (the doc's Export menu,
or Claude does it) into the folder doc_export/, then run make_all.py; this module finds every
table in those files and draws it.

Each table is drawn at its natural size, in the house colours, then centred on a white canvas
WIDTH pixels wide, so every image has the same width whatever the table. Wide tables wrap their
text to fit; height grows with the rows.
"""
import html, os, re
from PIL import Image, ImageDraw, ImageFont

WIDTH = 2400                 # same width as the diagram sheets
MARGIN = 80                  # white space left, right, top and bottom
SIZE = 38                    # text size in pixels
PAD_X, PAD_Y = 28, 20        # space inside each cell
MIN_COL = 150                # narrowest a wrapped column may get
INK = '#1f2430'; MUTE = '#6b7280'; LINE = '#d5dae3'; HEAD = '#dbe6f7'; BAND = '#f7f8fb'

# Doc tab name -> short name used in file names
TAB_NAMES = {'Tab 1': 'main', 'Glossary': 'glossary', 'Practice routines': 'practice',
             'Recording guide': 'recording-guide', 'Calendar': 'calendar', 'Series reference': 'series-reference'}
SKIP_TABS = {'Tabs'}         # the guitar tabs tab holds code blocks, not tables


def _font_path(names):
    import matplotlib.font_manager as fm
    for n in names:
        for d in ('/usr/share/fonts/opentype/inter', '/usr/share/fonts/truetype/inter', os.path.expanduser('~/.fonts')):
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    return None


def _fonts():
    import matplotlib.font_manager as fm
    dejavu = fm.findfont('DejaVu Sans')
    dejavu_b = fm.findfont(fm.FontProperties(family='DejaVu Sans', weight='bold'))
    reg = _font_path(['Inter-Regular.otf', 'Inter-Regular.ttf']) or dejavu
    bold = _font_path(['Inter-SemiBold.otf', 'Inter-SemiBold.ttf', 'Inter-Bold.otf']) or dejavu_b
    from fontTools.ttLib import TTFont
    cover = set(TTFont(reg).getBestCmap())
    return {'reg': ImageFont.truetype(reg, SIZE), 'bold': ImageFont.truetype(bold, SIZE),
            'fb': ImageFont.truetype(dejavu, SIZE), 'fbb': ImageFont.truetype(dejavu_b, SIZE), 'cover': cover}


F = None


def _runs(s, bold):
    """Split text into runs of the main font and the fallback (for characters Inter lacks, such as ♭)."""
    main, fb = (F['bold'], F['fbb']) if bold else (F['reg'], F['fb'])
    out = []
    for ch in s:
        f = main if ord(ch) in F['cover'] or ch == ' ' else fb
        if out and out[-1][0] is f:
            out[-1][1] += ch
        else:
            out.append([f, ch])
    return out


def _w(s, bold=False):
    return sum(f.getlength(t) for f, t in _runs(s, bold))


def _draw(d, x, y, s, bold=False, fill=INK):
    for f, t in _runs(s, bold):
        d.text((x, y), t, font=f, fill=fill)
        x += f.getlength(t)


def clean(cell):
    """Markdown cell -> plain text."""
    s = cell.strip()
    s = re.sub(r'\[([^\]]*)\]\((?:<[^>]*>|[^)]*)\)', r'\1', s)       # links keep their text
    s = re.sub(r'(\*\*|__)(.+?)\1', r'\2', s)               # bold
    s = re.sub(r'(?<!\w)[*_](.+?)[*_](?!\w)', r'\1', s)     # italics
    s = s.replace('`', '').replace('<br>', ' ')
    s = re.sub(r'\\(.)', r'\1', s)                          # escapes such as \_ and \#
    return html.unescape(s)


def _split_row(line):
    line = line.strip()
    if line.startswith('|'): line = line[1:]
    if line.endswith('|') and not line.endswith('\\|'): line = line[:-1]
    return [c.replace('\\|', '|') for c in re.split(r'(?<!\\)\|', line)]


def find_tables(md, tab):
    """Every table in one exported tab, with the heading it sits under."""
    lines = md.split('\n'); out = []; h2 = h3 = ''; i = 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r'(#+)\s+(.*)', l)
        if m:
            text = clean(m.group(2))
            if len(m.group(1)) <= 2: h2, h3 = text, ''
            else: h3 = text
        if l.startswith('|') and i + 1 < len(lines) and re.match(r'\|\s*:?-{3,}', lines[i + 1]):
            header = [clean(c) for c in _split_row(l)]
            rows = []; i += 2
            while i < len(lines) and lines[i].startswith('|'):
                r = [clean(c) for c in _split_row(lines[i])]
                rows.append((r + [''] * len(header))[:len(header)]); i += 1
            out.append(dict(tab=tab, heading=h2, section=h3, header=header, rows=rows))
            continue
        i += 1
    return out


def _slug(s):
    s = s.replace('#', ' sharp ').replace('♭', ' flat ')
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:60].strip('-')


def post_slugs():
    """Post code -> the name its diagram sheet uses, so a post's tables sit beside its diagrams."""
    from posts import POSTS
    out = {}
    for p in POSTS:
        sheet = p.get('sheet')
        if isinstance(sheet, dict): out[p['code']] = sheet['slug']
        elif isinstance(sheet, tuple): out[p['code']] = sheet[1]
        elif sheet == 'mode_chords': out[p['code']] = 'chords-in-each-mode'
        elif sheet == 'arpeggios': out[p['code']] = 'arpeggios'
        else: out[p['code']] = _slug(p['title'])
    return out


def _name(t, slugs):
    """F3-chords-in-e-table for a post's table; calendar-exercises-table and so on for the rest."""
    m = re.match(r'([A-Z]{1,2}\d+):', t['section'] or '')
    if t['heading'].lower().startswith('post draft') and m:
        code = m.group(1)
        return f"{code}-{slugs.get(code) or _slug(t['section'][len(code) + 1:])}"
    short = TAB_NAMES.get(t['tab'], _slug(t['tab']))
    label = t['section'] if t['section'] and short != 'main' else ' '.join(x for x in (t['heading'], t['section']) if x)
    label = _slug(re.sub(r'\([^)]*\)', '', label))          # drop "(6 posts)" and the like
    if short == 'main':
        return label
    return short if label in ('', short) else f'{short}-{label}'


def _wrap(s, width, bold):
    words = s.split(' '); lines = []; cur = ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if _w(trial, bold) <= width or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    out = []                                  # break any single word still too long
    for l in lines:
        while _w(l, bold) > width and len(l) > 1:
            k = len(l)
            while k > 1 and _w(l[:k], bold) > width: k -= 1
            out.append(l[:k]); l = l[k:]
        out.append(l)
    return out


def _col_widths(t):
    cols = len(t['header']); avail = WIDTH - 2 * MARGIN
    need = []
    for c in range(cols):
        cells = [(t['header'][c], True)] + [(r[c], c == 0) for r in t['rows']]
        need.append(max(_w(s, b) for s, b in cells) + 2 * PAD_X)
    if sum(need) <= avail:
        return need
    # share the width: narrow columns keep their size, the rest split what is left
    widths = [None] * cols; left = avail; open_ = list(range(cols))
    while open_:
        share = left / len(open_)
        fixed = [c for c in open_ if need[c] <= share]
        if not fixed:                         # wide columns share the rest by how much they hold
            total = sum(need[c] for c in open_)
            for c in open_:
                widths[c] = max(MIN_COL, left * need[c] / total)
            break
        for c in fixed:
            widths[c] = need[c]; left -= need[c]; open_.remove(c)
    return widths


def render(t, path):
    global F
    if F is None: F = _fonts()
    widths = _col_widths(t)
    line_h = int(SIZE * 1.35)
    grid = []
    for ri, row in enumerate([t['header']] + t['rows']):
        cells = [_wrap(s, widths[c] - 2 * PAD_X, ri == 0 or c == 0) for c, s in enumerate(row)]
        grid.append((cells, max(len(x) for x in cells) * line_h + 2 * PAD_Y))
    tw = int(sum(widths)); th = int(sum(h for _, h in grid))
    img = Image.new('RGB', (WIDTH, th + 2 * MARGIN), 'white')
    d = ImageDraw.Draw(img)
    x0 = (WIDTH - tw) // 2; y = MARGIN
    for ri, (cells, h) in enumerate(grid):
        if ri == 0:
            d.rectangle([x0, y, x0 + tw, y + h], fill=HEAD)
        elif ri % 2 == 0:
            d.rectangle([x0, y, x0 + tw, y + h], fill=BAND)
        x = x0
        for c, lines in enumerate(cells):
            for k, l in enumerate(lines):
                _draw(d, x + PAD_X, y + PAD_Y + k * line_h + (line_h - SIZE) // 2 - 2, l, bold=(ri == 0 or c == 0))
            x += widths[c]
        y += h
        d.line([x0, y, x0 + tw, y], fill=LINE, width=2)
    d.rectangle([x0, MARGIN, x0 + tw, MARGIN + th], outline=LINE, width=2)
    x = x0
    for w in widths[:-1]:
        x += w; d.line([x, MARGIN, x, MARGIN + th], fill=LINE, width=2)
    img.save(path, optimize=True)
    return path


def all_tables(export_dir):
    """Tables from every exported tab, in the doc's tab order."""
    order = list(TAB_NAMES)
    files = [f for f in os.listdir(export_dir) if f.endswith('.md') and f[:-3] not in SKIP_TABS]
    files.sort(key=lambda f: (order.index(f[:-3]) if f[:-3] in order else 99, f))
    out = []
    for f in files:
        with open(os.path.join(export_dir, f), encoding='utf-8') as fh:
            out += find_tables(fh.read(), f[:-3])
    return out


def build(export_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    slugs = post_slugs()
    tables = all_tables(export_dir)
    names = [_name(t, slugs) for t in tables]
    made = []; k = {}
    for t, base in zip(tables, names):
        if names.count(base) > 1:                              # M1 has two tables: -table-1, -table-2
            k[base] = k.get(base, 0) + 1
            base = f'{base}-table-{k[base]}'
        else:
            base = f'{base}-table'
        made.append(render(t, os.path.join(out_dir, base + '.png')))
    return made
