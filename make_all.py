"""Build every diagram and tab for the Theory in E series.

    python3 make_all.py                 everything, into the folder "output"
    python3 make_all.py --only F6 E1    just those posts (plus nothing else)
    python3 make_all.py --check         run the music checks and stop
    python3 make_all.py --out mydir     use another output folder
    python3 make_all.py --tables        just the table images
    python3 make_all.py --about         just the Patreon About text (output/about.txt)

Table images come from the doc's tabs exported as Markdown into doc_export/ (see tables.py).

Nothing is drawn unless every scale, chord shape, triad and arpeggio passes its check.
"""
import argparse, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import theory
from posts import POSTS, STANDING_EXTRAS


def check_catalogue():
    bad = []
    codes = [p['code'] for p in POSTS]
    if len(codes) != len(set(codes)):
        bad.append(('duplicate post codes', [c for c in codes if codes.count(c) > 1]))
    for p in POSTS:
        sheet = p.get('sheet')
        names = []
        if isinstance(sheet, dict):
            names += [n for n, _ in sheet.get('chE', []) + sheet.get('chB', [])]
            if sheet['mode'] not in theory.SCALES['E']:
                bad.append((p['code'], 'unknown mode', sheet['mode']))
        for _, item in p.get('tabs', []):
            if isinstance(item, list):
                names += item
        for n in names:
            if n not in theory.SHAPES:
                bad.append((p['code'], 'no chord shape for', n, '- add it to SHAPES in theory.py'))
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default='output', help='output folder (default: output)')
    ap.add_argument('--only', nargs='*', help='post codes to build, e.g. F6 E1')
    ap.add_argument('--check', action='store_true', help='run the checks only')
    ap.add_argument('--tables', action='store_true', help='build only the table images')
    ap.add_argument('--about', action='store_true', help='write only the Patreon About text')
    ap.add_argument('--doc', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'doc_export'),
                    help='folder of the doc tabs exported as Markdown (default: doc_export)')
    a = ap.parse_args()

    import about
    problems = theory.check_all() + check_catalogue() + about.problems(POSTS)
    if problems:
        print('Stopped: these need fixing before anything is drawn:')
        for p in problems:
            print('  -', p)
        sys.exit(1)
    print(f'Checks passed: {len(theory.SHAPES)} chord shapes, 14 scales, 98 triads, 98 arpeggios, 14 arpeggio-and-scale runs, {len(POSTS)} posts.')
    if a.check:
        return

    if a.about:
        build_about(a); return
    if a.tables:
        build_tables(a); return

    import draw
    from tabs import all_tabs
    diagrams = os.path.join(a.out, 'diagrams')
    os.makedirs(diagrams, exist_ok=True)
    draw.OUT = diagrams

    wanted = [p for p in POSTS if not a.only or p['code'] in a.only]
    if a.only and len(wanted) != len(a.only):
        unknown = set(a.only) - {p['code'] for p in POSTS}
        print('Unknown post codes:', ', '.join(sorted(unknown))); sys.exit(1)

    t0 = time.time(); made = []
    for p in wanted:
        sheet = p.get('sheet')
        if isinstance(sheet, dict):
            made += draw.post_sheet(p['code'], p['title'], **sheet)
        elif sheet == 'mode_chords':
            made += draw.mode_chords_sheet(p['code'])
        elif sheet == 'arpeggios':
            made += draw.arpeggio_sheets(p['code'])
        elif isinstance(sheet, tuple) and sheet[0] == 'arp_scale':
            made += draw.arp_scale_sheet(p['code'], slug=sheet[1], degree=sheet[2])
        for x in p.get('extras', []):
            made += draw.EXTRAS[x]()
        print(f'  {p["code"]:5} {p["title"]}')
    if not a.only:
        for x in STANDING_EXTRAS:
            made += draw.EXTRAS[x]()

    tabs_file = os.path.join(a.out, 'tabs.md' if not a.only else f'tabs-{"-".join(a.only)}.md')
    with open(tabs_file, 'w', encoding='utf-8') as f:
        f.write(all_tabs(wanted))
    print(f'Made {len(made)} images in {diagrams} and the tabs in {tabs_file} ({time.time() - t0:.0f} s).')
    if not a.only:
        build_tables(a)
        build_about(a)


def build_about(a):
    import about
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, 'about.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(about.about_text(POSTS))
    print(f'Wrote the Patreon About text to {path}.')


def build_tables(a):
    import tables
    if not os.path.isdir(a.doc):
        print(f'No table images: export the doc tabs as Markdown into {a.doc} first.'); return
    out = os.path.join(a.out, 'tables')
    made = tables.build(a.doc, out)
    print(f'Made {len(made)} table images in {out}, all {tables.WIDTH} px wide.')


if __name__ == '__main__':
    main()
