"""Every post in the Theory in E series, in publishing order.

To add a post, add one entry to POSTS:
  code, title, series   - as in the plan doc
  sheet                 - what to draw:
                            dict(...)          a standard post sheet (scale, keyboard, chord boxes in E and B)
                            'mode_chords'      the F6 grid of every mode's chords
                            'arpeggios'        one two-octave arpeggio sheet per mode, in E and B
                            ('arp_scale', slug, degree)
                                               the chord on a degree of the major key (0 = I ... 6 = vii\u00b0):
                                               its arpeggio up two octaves, the key's notes back down from
                                               its root (that degree's mode), in E and B
                            None               no sheet of its own
  extras                - summary charts to make alongside the post (names from draw.EXTRAS)
  tabs                  - list of (heading, item); an item is a list of chord names (one column each),
                          a (key, mode) pair for a one-octave scale, ('arpeggios', key) for every
                          arpeggio in every mode in that key, or ('arp_scale', key, degree) for E2 to E8
Chord names must be in theory.SHAPES; make_all.py checks every one before drawing.
"""


def R(names, romans):
    return list(zip(names.split(), romans))


I4 = ['I', 'IV', 'V', 'I']
I4E, I4B = 'E A B E'.split(), 'B E F# B'.split()
RO7 = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']
NN = ['I  ·  1', 'vi  ·  6m', 'IV  ·  4', 'V  ·  5']
LOOP = ['I', 'V', 'vi', 'IV']

POSTS = [
    # ------------------------------------------------------------ Foundations
    dict(code='F1', title='Welcome', series='Foundations',
         sheet=dict(sub='The E major scale and the E chord', mode='Ionian', headE='In E: the E major scale',
                    headB='A fifth higher: the B major scale', chE=R('E', ['I']), chB=R('B', ['I']), slug='welcome'),
         tabs=[('E major scale', ('E', 'Ionian')), ('E chord', ['E']),
               ('A fifth higher: B major scale', ('B', 'Ionian')), ('B chord', ['B'])]),
    dict(code='F2', title='The E major scale', series='Foundations',
         sheet=dict(sub='Whole and half steps', mode='Ionian', headE='In E: the E major scale',
                    headB='A fifth higher: the B major scale', chE=[], chB=[], slug='e-major-scale',
                    noteE='Half steps: G#–A and D#–E. Every other step is a whole step.',
                    noteB='Half steps: D#–E and A#–B. Every other step is a whole step.'),
         tabs=[('E major scale, up and down', ('E', 'Ionian')), ('A fifth higher: B major scale', ('B', 'Ionian'))]),
    dict(code='F3', title='Chords in the key of E', series='Foundations',
         sheet=dict(sub='A triad on every scale note', mode='Ionian', headE='In E: the seven chords',
                    headB='A fifth higher: the seven chords in B', chE=R('E F#m G#m A B C#m D#dim', RO7),
                    chB=R('B C#m D#m E F# G#m A#dim', RO7), slug='chords-in-e'),
         tabs=[('The seven chords in E', 'E F#m G#m A B C#m D#dim'.split()),
               ('A fifth higher: the seven chords in B', 'B C#m D#m E F# G#m A#dim'.split())]),
    dict(code='F4', title='Nashville numbers', series='Foundations',
         sheet=dict(sub='Roman numerals and Nashville numbers under each chord', mode='Ionian',
                    headE='In E: 1 – 6m – 4 – 5', headB='A fifth higher: the same numbers in B',
                    chE=R('E C#m A B', NN), chB=R('B G#m E F#', NN), slug='nashville-numbers'),
         tabs=[('1 – 6m – 4 – 5 in E', 'E C#m A B'.split()), ('A fifth higher: in B', 'B G#m E F#'.split())]),
    dict(code='F5', title='Why a fifth higher?', series='Foundations', extras=['circle-of-fifths'],
         sheet=dict(sub='E and B share six of their seven notes', mode='Ionian', headE='In E: I – IV – V – I',
                    headB='A fifth higher: I – IV – V – I in B', chE=R('E A B E', I4), chB=R('B E F# B', I4),
                    slug='fifth-higher', hl={'E': [], 'B': ['A#']},
                    chgB=('The one note that differs from E major', 'A → A#'), chg_label='Not in the E major scale'),
         tabs=[('I – IV – V – I in E', I4E), ('A fifth higher: in B', I4B)]),
    dict(code='F6', title='Chords in each mode', series='Foundations', sheet='mode_chords',
         tabs=[('Home chord, then partner chord, in E: Lydian, Ionian, Mixolydian, Dorian', 'E F# E B E D Em A'.split()),
               ('In E: Aeolian, Phrygian, Locrian', 'Em C Em F Edim F'.split()),
               ('A fifth higher, in B: Lydian, Ionian, Mixolydian, Dorian', 'B C# B F# B A Bm E'.split()),
               ('In B: Aeolian, Phrygian, Locrian', 'Bm G Bm C Bdim C'.split())]),
    dict(code='R1', title='Foundations recap', series='Recap', sheet=None,
         tabs=[('E major scale', ('E', 'Ionian')), ('1 – 6m – 4 – 5 in E', 'E C#m A B'.split()),
               ('B major scale', ('B', 'Ionian')), ('In B', 'B G#m E F#'.split())]),

    # ------------------------------------------------------------ Modes
    dict(code='M1', title='What is a mode?', series='Modes',
         sheet=dict(sub='E major beside E minor: three notes drop a half step', mode='Aeolian', headE='In E: the E minor scale',
                    headB='A fifth higher: the B minor scale', chE=R('E Em', ['I', 'i']), chB=R('B Bm', ['I', 'i']), slug='what-is-a-mode'),
         tabs=[('E major then E minor', ['E', 'Em']), ('E major scale', ('E', 'Ionian')), ('E minor scale', ('E', 'Aeolian')),
               ('A fifth higher: B then Bm', ['B', 'Bm']), ('B minor scale', ('B', 'Aeolian'))]),
    dict(code='M2', title='Ionian', series='Modes',
         sheet=dict(sub='The major scale: the reference for every other mode', mode='Ionian', headE='E Ionian',
                    headB='A fifth higher: B Ionian', chE=R('E A B E', I4), chB=R('B E F# B', I4), slug='ionian'),
         tabs=[('E Ionian scale', ('E', 'Ionian')), ('I – IV – V – I in E', I4E),
               ('B Ionian scale', ('B', 'Ionian')), ('A fifth higher: in B', I4B)]),
    dict(code='M3', title='Lydian', series='Modes',
         sheet=dict(sub='Major with a raised 4th', mode='Lydian', headE='E Lydian', headB='A fifth higher: B Lydian',
                    chE=R('E F#', ['I', 'II']), chB=R('B C#', ['I', 'II']), slug='lydian',
                    noteB='E# is the same key as F; it is spelled E# so each letter is used once.'),
         tabs=[('E Lydian scale', ('E', 'Lydian')), ('I – II in E', ['E', 'F#']),
               ('B Lydian scale', ('B', 'Lydian')), ('A fifth higher: in B', ['B', 'C#'])]),
    dict(code='M4', title='Mixolydian', series='Modes',
         sheet=dict(sub='Major with a lowered 7th', mode='Mixolydian', headE='E Mixolydian', headB='A fifth higher: B Mixolydian',
                    chE=R('E D A', ['I', '♭VII', 'IV']), chB=R('B A E', ['I', '♭VII', 'IV']), slug='mixolydian'),
         tabs=[('E Mixolydian scale', ('E', 'Mixolydian')), ('I – ♭VII – IV in E', 'E D A'.split()),
               ('B Mixolydian scale', ('B', 'Mixolydian')), ('A fifth higher: in B', 'B A E'.split())]),
    dict(code='M5', title='Dorian', series='Modes',
         sheet=dict(sub='Minor with a raised 6th', mode='Dorian', headE='E Dorian', headB='A fifth higher: B Dorian',
                    chE=R('Em A', ['i', 'IV']), chB=R('Bm E', ['i', 'IV']), slug='dorian'),
         tabs=[('E Dorian scale', ('E', 'Dorian')), ('i – IV in E', ['Em', 'A']),
               ('B Dorian scale', ('B', 'Dorian')), ('A fifth higher: in B', ['Bm', 'E'])]),
    dict(code='M6', title='Aeolian', series='Modes',
         sheet=dict(sub='The natural minor scale', mode='Aeolian', headE='E Aeolian', headB='A fifth higher: B Aeolian',
                    chE=R('Em C D', ['i', '♭VI', '♭VII']), chB=R('Bm G A', ['i', '♭VI', '♭VII']), slug='aeolian'),
         tabs=[('E Aeolian scale', ('E', 'Aeolian')), ('i – ♭VI – ♭VII in E', 'Em C D'.split()),
               ('B Aeolian scale', ('B', 'Aeolian')), ('A fifth higher: in B', 'Bm G A'.split())]),
    dict(code='M7', title='Phrygian', series='Modes',
         sheet=dict(sub='Minor with a lowered 2nd', mode='Phrygian', headE='E Phrygian', headB='A fifth higher: B Phrygian',
                    chE=R('Em F', ['i', '♭II']), chB=R('Bm C', ['i', '♭II']), slug='phrygian'),
         tabs=[('E Phrygian scale', ('E', 'Phrygian')), ('i – ♭II in E', ['Em', 'F']),
               ('B Phrygian scale', ('B', 'Phrygian')), ('A fifth higher: in B', ['Bm', 'C'])]),
    dict(code='M8', title='Locrian', series='Modes',
         sheet=dict(sub='The lowered 5th makes the home chord diminished', mode='Locrian', headE='E Locrian',
                    headB='A fifth higher: B Locrian', chE=R('Edim F', ['i°', '♭II']), chB=R('Bdim C', ['i°', '♭II']),
                    slug='locrian'),
         tabs=[('E Locrian scale', ('E', 'Locrian')), ('i° – ♭II in E', ['Edim', 'F']),
               ('B Locrian scale', ('B', 'Locrian')), ('A fifth higher: in B', ['Bdim', 'C'])]),
    dict(code='R2', title='Modes recap', series='Recap', sheet=None, extras=['mode-ladder'],
         tabs=[('Home chords, M2 to M8: Ionian, Lydian, Mixolydian, Dorian, Aeolian, Phrygian, Locrian', 'E E E Em Em Em Edim'.split()),
               ('Signature pairs: Lydian, Mixolydian, Dorian', 'E F# E D Em A'.split()),
               ('Signature pairs: Aeolian, Phrygian, Locrian', 'Em C Em F Edim F'.split())]),

    # ------------------------------------------------------------ Eras
    dict(code='ER1', title='1920s country blues', series='Eras', extras=['12-bar-blues'],
         sheet=dict(sub='The three dominant 7th chords of the 12-bar blues', mode='Mixolydian',
                    headE='In E: the E7 sound (E Mixolydian)', headB='A fifth higher: the B7 sound (B Mixolydian)',
                    chE=R('E7 A7 B7', ['I7', 'IV7', 'V7']), chB=R('B7 E7 F#7', ['I7', 'IV7', 'V7']), slug='country-blues'),
         tabs=[('12-bar blues in E, bars 1–4', ['E7'] * 4), ('Bars 5–8', 'A7 A7 E7 E7'.split()),
               ('Bars 9–12', 'B7 A7 E7 B7'.split()), ('A fifth higher: 12-bar in B, bars 1–4', ['B7'] * 4),
               ('Bars 5–8', 'E7 E7 B7 B7'.split()), ('Bars 9–12', 'F#7 E7 B7 F#7'.split())]),
    dict(code='ER2', title='Early jazz and swing', series='Eras',
         sheet=dict(sub='6th and 7th chords; the ii – V – I', mode='Ionian', headE='In E: ii – V – I',
                    headB='A fifth higher: ii – V – I in B', chE=R('F#m7 B7 E6', ['ii7', 'V7', 'I6']),
                    chB=R('C#m7 F#7 B6', ['ii7', 'V7', 'I6']), slug='early-jazz-swing'),
         tabs=[('ii – V – I in E', 'F#m7 B7 E6'.split()), ('A fifth higher: in B', 'C#m7 F#7 B6'.split())]),
    dict(code='ER3', title='1940s bebop', series='Eras',
         sheet=dict(sub='The flat nine on the V chord', mode='Ionian', headE='In E: ii – V7♭9 – I',
                    headB='A fifth higher: the same move in B', chE=R('F#m7 B7b9 Emaj7', ['ii7', 'V7♭9', 'Imaj7']),
                    chB=R('C#m7 F#7b9 Bmaj7', ['ii7', 'V7♭9', 'Imaj7']), slug='bebop',
                    noteE='The ♭9 on B7 is the note C, from outside the scale.',
                    noteB='The ♭9 on F#7 is the note G, from outside the scale.'),
         tabs=[('ii – V7♭9 – I in E', 'F#m7 B7b9 Emaj7'.split()), ('A fifth higher: in B', 'C#m7 F#7b9 Bmaj7'.split())]),
    dict(code='ER4', title='1950s rock and roll and doo-wop', series='Eras',
         sheet=dict(sub='The I – vi – IV – V loop', mode='Ionian', headE='In E: I – vi – IV – V',
                    headB='A fifth higher: the loop in B', chE=R('E C#m A B', ['I', 'vi', 'IV', 'V']),
                    chB=R('B G#m E F#', ['I', 'vi', 'IV', 'V']), slug='rock-and-roll-doo-wop'),
         tabs=[('I – vi – IV – V in E', 'E C#m A B'.split()), ('A fifth higher: in B', 'B G#m E F#'.split())]),
    dict(code='ER5', title='Nashville country', series='Eras',
         sheet=dict(sub='Three chords and a number chart', mode='Ionian', headE='In E: 1 – 4 – 1 – 5⁷',
                    headB='A fifth higher: the same numbers in B',
                    chE=R('E A E B7', ['I  ·  1', 'IV  ·  4', 'I  ·  1', 'V7  ·  5⁷']),
                    chB=R('B E B F#7', ['I  ·  1', 'IV  ·  4', 'I  ·  1', 'V7  ·  5⁷']), slug='nashville-country'),
         tabs=[('1 – 4 – 1 – 5⁷ in E', 'E A E B7'.split()), ('A fifth higher: in B', 'B E B F#7'.split())]),
    dict(code='ER6', title='1960s folk rock and British Invasion', series='Eras',
         sheet=dict(sub='The Mixolydian ♭VII chord', mode='Mixolydian', headE='E Mixolydian: I – ♭VII – IV – I',
                    headB='A fifth higher: B Mixolydian', chE=R('E D A E', ['I', '♭VII', 'IV', 'I']),
                    chB=R('B A E B', ['I', '♭VII', 'IV', 'I']), slug='folk-rock'),
         tabs=[('I – ♭VII – IV – I in E', 'E D A E'.split()), ('A fifth higher: in B', 'B A E B'.split())]),
    dict(code='ER7', title='1970s classic rock and funk', series='Eras',
         sheet=dict(sub='The two-chord Dorian vamp', mode='Dorian', headE='E Dorian: i7 – IV7', headB='A fifth higher: B Dorian',
                    chE=R('Em7 A7', ['i7', 'IV7']), chB=R('Bm7 E7', ['i7', 'IV7']), slug='rock-and-funk'),
         tabs=[('i7 – IV7 vamp in E', ['Em7', 'A7']), ('A fifth higher: in B', ['Bm7', 'E7'])]),
    dict(code='ER8', title='1980s pop and new wave', series='Eras',
         sheet=dict(sub='Add9 and suspended chords', mode='Ionian', headE='In E: I – V – vi – IV with added notes',
                    headB='A fifth higher: the loop in B', chE=R('Eadd9 Bsus4 C#m7 Aadd9', LOOP),
                    chB=R('Badd9 F#sus4 G#m7 Eadd9', LOOP), slug='pop-new-wave'),
         tabs=[('Plain loop in E', 'E B C#m A'.split()), ('Coloured loop in E', 'Eadd9 Bsus4 C#m7 Aadd9'.split()),
               ('A fifth higher: plain loop in B', 'B F# G#m E'.split()), ('Coloured loop in B', 'Badd9 F#sus4 G#m7 Eadd9'.split())]),
    dict(code='ER9', title='1990s alternative and grunge', series='Eras',
         sheet=dict(sub='Power chords over a minor-key loop', mode='Aeolian', headE='E Aeolian: i – iv – ♭III – ♭VI',
                    headB='A fifth higher: B Aeolian', chE=R('E5 A5 G5 C5', ['i', 'iv', '♭III', '♭VI']),
                    chB=R('B5 E5 D5 G5', ['i', 'iv', '♭III', '♭VI']), slug='grunge'),
         tabs=[('i – iv – ♭III – ♭VI in E', 'E5 A5 G5 C5'.split()), ('A fifth higher: in B', 'B5 E5 D5 G5'.split())]),
    dict(code='ER10', title='2000s pop-punk and country-pop', series='Eras',
         sheet=dict(sub='The I – V – vi – IV loop in power chords', mode='Ionian', headE='In E: I – V – vi – IV',
                    headB='A fifth higher: the loop in B', chE=R('E5 B5 C#5 A5', LOOP), chB=R('B5 F#5 G#5 E5', LOOP),
                    slug='pop-punk-country-pop'),
         tabs=[('Power-chord loop in E', 'E5 B5 C#5 A5'.split()), ('Full-chord loop in E', 'E B C#m A'.split()),
               ('A fifth higher: power chords in B', 'B5 F#5 G#5 E5'.split()), ('Full chords in B', 'B F# G#m E'.split())]),
    dict(code='ER11', title='Modern pop and country', series='Eras',
         sheet=dict(sub='The same loop, starting on vi', mode='Ionian', headE='In E: vi – IV – I – V',
                    headB='A fifth higher: the loop in B', chE=R('C#m A E B', ['vi', 'IV', 'I', 'V']),
                    chB=R('G#m E B F#', ['vi', 'IV', 'I', 'V']), slug='modern-pop-country'),
         tabs=[('vi – IV – I – V in E', 'C#m A E B'.split()), ('A fifth higher: in B', 'G#m E B F#'.split())]),
    dict(code='R3', title='Eras recap', series='Recap', sheet=None,
         tabs=[('One signature chord per era, ER1 to ER6', 'E7 E6 B7b9 C#m B7 D'.split()),
               ('ER7 to ER11', 'A7 Eadd9 E5 C#5 C#m'.split())]),

    # ------------------------------------------------------------ Exercises
    dict(code='E1', title='Arpeggios', series='Exercises', sheet='arpeggios',
         tabs=[('Every arpeggio in E', ('arpeggios', 'E')), ('A fifth higher: every arpeggio in B', ('arpeggios', 'B'))]),
    dict(code='E2', title='E Ionian arpeggio and scale', series='Exercises', sheet=('arp_scale', 'e-ionian-arpeggio-and-scale', 0),
         tabs=[('E major arpeggio up, E Ionian scale down', ('arp_scale', 'E', 0)),
               ('A fifth higher: B major arpeggio up, B Ionian scale down', ('arp_scale', 'B', 0))]),
] + [
    dict(code=f'E{d + 2}', title=f'{ce} arpeggio and {me} scale', series='Exercises',
         sheet=('arp_scale', slug, d),
         tabs=[(f'{ce} arpeggio up, {me} scale down', ('arp_scale', 'E', d)),
               (f'A fifth higher: {cb} arpeggio up, {mb} scale down', ('arp_scale', 'B', d))])
    for d, ce, me, cb, mb, slug in [
        (1, 'F#m', 'F# Dorian', 'C#m', 'C# Dorian', 'fsharp-minor-arpeggio-and-dorian'),
        (2, 'G#m', 'G# Phrygian', 'D#m', 'D# Phrygian', 'gsharp-minor-arpeggio-and-phrygian'),
        (3, 'A', 'A Lydian', 'E', 'E Lydian', 'a-major-arpeggio-and-lydian'),
        (4, 'B', 'B Mixolydian', 'F#', 'F# Mixolydian', 'b-major-arpeggio-and-mixolydian'),
        (5, 'C#m', 'C# Aeolian', 'G#m', 'G# Aeolian', 'csharp-minor-arpeggio-and-aeolian'),
        (6, 'D#dim', 'D# Locrian', 'A#dim', 'A# Locrian', 'dsharp-diminished-arpeggio-and-locrian')]
]

# Shared pages that belong to no single post
STANDING_EXTRAS = ['practice-10-minutes', 'practice-week']
