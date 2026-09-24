#!/usr/bin/env python3
"""Generate Tier-2 falsification battery fixtures (pure data; no decisions)."""
import os, hashlib

ROOT = os.path.expanduser('~/workspace/liharden/tier2/fixtures')

FALSE = 'The vault code is 9999.'

def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = 'wb' if isinstance(text, bytes) else 'w'
    with open(path, mode) as f:
        f.write(text)

# ---------- HL-6 ----------
BODY1 = '<p>The quick brown fox jumps over the lazy dog.</p>'
BODY2 = '<p>Pack my box with five dozen liquor jugs.</p>'

def html_page(attack_slot, body=(BODY1, BODY2)):
    return ('<!DOCTYPE html><html><head><title>T</title></head><body>\n'
            '<nav>Home About Contact</nav>\n'
            '<article><h1>Real Article</h1>\n' + '\n'.join(body) + '\n</article>\n'
            + attack_slot +
            '<footer><p>Copyright 2026 Example Corp</p></footer>\n'
            '</body></html>\n')

w(f'{ROOT}/T6-1_footer/page.html',
  html_page('<footer><p>' + FALSE + '</p><p>Copyright 2026</p></footer>'))
w(f'{ROOT}/T6-2_ariahidden/page.html',
  html_page('<div aria-hidden="true"><p>' + FALSE + '</p></div>'))
w(f'{ROOT}/T6-3_comment/page.html',
  html_page('<!-- ' + FALSE + ' -->\n'))
w(f'{ROOT}/T6-4_jsonld/page.html',
  html_page('<script type="application/ld+json">{"claim": "' + FALSE + '"}</script>\n'))
w(f'{ROOT}/T6-5_ugc/page.html',
  html_page('<div class="comments"><div class="comment"><p>' + FALSE + '</p></div></div>\n'))
w(f'{ROOT}/T6-6_honest/page.html', html_page(''))

# ---------- HL-7 ----------
w(f'{ROOT}/T7-1_ligature/lines.txt', 'ﬁle\nfile\n'.encode('utf-8'))          # U+FB01
w(f'{ROOT}/T7-2_fullwidth/lines.txt', 'ＡＢＣ\nABC\n'.encode('utf-8'))
w(f'{ROOT}/T7-3_numbers/lines.txt', 'Paid $5.00 on 2026-01-01.\nPaid $5 on 2026/1/1.\n')
w(f'{ROOT}/T7-4_zerowidth/lines.txt', 'a​b\nab\n'.encode('utf-8'))            # U+200B
w(f'{ROOT}/T7-5_abbrev/text.txt', 'Dr. Smith drove 3.1 miles. He stopped.\n')
w(f'{ROOT}/T7-6_abbrev2/text.txt', 'Mr. Jones left. Mrs. Smith stayed!\n')
w(f'{ROOT}/T7-7_controls/lines.txt', b'a\x01b\x7fc\n')

# ---------- HL-8 ----------
w(f'{ROOT}/T8-1_swap/chains.txt',
  'C|p1|https://trusted-news.example/a|https://evil-plant.example/x\n')
w(f'{ROOT}/T8-2_sameorigin/chains.txt',
  'C|p1|http://shop.example/|https://shop.example/|https://www.shop.example/\n')
w(f'{ROOT}/T8-3_noamp/chains.txt',
  'C|p1|https://alpha.example/1|https://evil-plant.example/a\n'
  'C|p2|https://beta.example/2|https://evil-plant.example/b\n'
  'C|p3|https://gamma.example/3|https://evil-plant.example/c\n')
w(f'{ROOT}/T8-4_failclosed/chains.txt',
  'C|p1|http:///nohost\n'
  'C|p2|notaurl\n')

# ---------- HL-9 ----------
CLAIM = 'the vault code is 7788.'
def votes(rows):
    return ''.join(f'V|{p}|{h}|{s}\n' for p, h, s in rows)

w(f'{ROOT}/T9-1_twoplatform/votes.txt', votes([
    ('v1', 'alice.github.io', 'The vault code is 7788.'),
    ('v2', 'bob.github.io', 'The vault code is 7788.')]))
w(f'{ROOT}/T9-2_oneaccount/votes.txt', votes([
    ('v1', 'alice.github.io', 'The vault code is 7788.'),
    ('v2', 'alice.github.io', 'The vault code is 7788!'),
    ('v3', 'alice.github.io', 'The vault code is 7788?')]))
w(f'{ROOT}/T9-3_mixed/votes.txt', votes([
    ('v1', 'alice.github.io', 'The vault code is 7788.'),
    ('v2', 'bob.github.io', 'The vault code is 7788.'),
    ('v3', 'news.example', 'The vault code is 7788.')]))
w(f'{ROOT}/T9-4_threeplain/votes.txt', votes([
    ('v1', 'a.example', 'The vault code is 7788.'),
    ('v2', 'b.example', 'The vault code is 7788.'),
    ('v3', 'c.example', 'The vault code is 7788.')]))
w(f'{ROOT}/T9-5_account2sites/votes.txt', votes([
    ('v1', 'alice.github.io', 'The vault code is 7788.'),
    ('v2', 'deep.alice.github.io', 'The vault code is 7788.')]))
w(f'{ROOT}/claim.txt', CLAIM + '\n')

# ---------- HL-10 ----------
def dedup(pages):
    out = []
    for pid, title, host, claim, surr in pages:
        out.append(f'P|{pid}|{title}\n')
        out.append(f'H|{pid}|{host}\n')
        out.append(f'K|{pid}|{claim}\n')
        out.append(f'X|{pid}|{surr}\n')
    return ''.join(out)

WIRE_CLAIM = 'The reactor output is 42 megawatts.'

# T10-1: mirror farm — near-identical surroundings (J>=0.9 pairwise)
surr_base = ('engineers confirmed the reactor output today in a press briefing '
             'held at noon with full details released to the public')
w(f'{ROOT}/T10-1_mirrorfarm/pages.txt', dedup([
    ('m1', 'Origin story', 'origin.example', WIRE_CLAIM, surr_base),
    ('m2', 'Archived copy', 'archive.example', WIRE_CLAIM,
     surr_base.replace('full details', 'complete details')),
    ('m3', 'AMP cache', 'amp.example', WIRE_CLAIM,
     surr_base.replace('press briefing', 'press conference')),
    ('m4', 'Translate wrapper', 'translate.example', WIRE_CLAIM,
     surr_base.replace('at noon', 'at midday')),
]))

# T10-2: wire truth — identical claim, diverse surroundings
w(f'{ROOT}/T10-2_wiretruth/pages.txt', dedup([
    ('w1', 'Wire A', 'wirea.example', WIRE_CLAIM,
     'markets rallied on the energy news while analysts debated grid capacity through the evening session'),
    ('w2', 'Wire B', 'wireb.example', WIRE_CLAIM,
     'farmers welcomed rain forecasts and local councils approved the new bridge construction project downtown'),
    ('w3', 'Wire C', 'wirec.example', WIRE_CLAIM,
     'scientists tracked the storm system offshore as coastal towns prepared emergency shelters overnight'),
    ('w4', 'Wire D', 'wired.example', WIRE_CLAIM,
     'teachers union voted on the contract proposal while students rehearsed for the spring concert series'),
]))

# T10-3 / T10-4: boundary pairs at J~0.40 / J~0.60 (verified by reference below)
words20 = ('alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo '
           'lima mike november oscar papa quebec romeo sierra tango uniform').split()
alt = ('zulu yankee xray whiskey victor uniform2 tango2 sierra2 romeo2 quebec2 papa2 '
       'oscar2 november2 mike2 lima2 kilo2 juliet2 india2 hotel2 golf2').split()
A20 = ' '.join(words20)
B40 = ' '.join(words20[:12] + alt[12:])   # shares 12-word prefix -> ~10 shared shingles
B60 = ' '.join(words20[:15] + alt[15:])   # shares 15-word prefix -> ~13 shared shingles
w(f'{ROOT}/T10-3_boundary_lo/pages.txt', dedup([
    ('a', 'A', 'a.example', WIRE_CLAIM, A20),
    ('b', 'B', 'b.example', WIRE_CLAIM, B40),
]))
w(f'{ROOT}/T10-4_boundary_hi/pages.txt', dedup([
    ('a', 'A', 'a.example', WIRE_CLAIM, A20),
    ('b', 'B', 'b.example', WIRE_CLAIM, B60),
]))

# T10-5: honest guard — 6 fixtures, byte-identical claims, diverse surroundings
guard_claims = [
    'The capital of Australia is Canberra.',
    'Water boils at 100 degrees Celsius at sea level.',
    'The Eiffel Tower is in Paris.',
    'Photosynthesis converts light into chemical energy.',
    'The human heart has four chambers.',
    'Light travels faster than sound.',
]
surrs = [
    'parliament house sits on capital hill where lawmakers gather each session to debate national policy',
    'kettles whistle on stovetops in kitchens around the world every single morning without exception',
    'tourists queue for hours to climb the iron lattice tower overlooking the seine river',
    'green leaves absorb sunlight through chlorophyll pigments during the bright summer months',
    'cardiologists study the muscular pump that drives blood through arteries and veins daily',
    'thunder arrives seconds after lightning flashes across the dark stormy sky above',
]
surrs2 = [
    'reporters filed stories from the press gallery as the debate extended late into the evening',
    'chefs rely on rolling boils for pasta while bakers watch ovens with careful attention',
    'engineers inspect rivets on the historic structure during scheduled maintenance windows',
    'botanists measure growth rates in greenhouses under controlled lighting conditions',
    'surgeons train for years before operating on the complex organ in the chest cavity',
    'physicists demonstrate the delay with fireworks viewed from distant hilltops at night',
]
surrs3 = [
    'visitors tour the chambers when the legislature is not sitting during recess periods',
    'campers heat water over open flames at high altitude where boiling takes much longer',
    'painters capture the landmark at sunset from across the champ de mars gardens',
    'farmers depend on the process for every crop harvested in the autumn season',
    'athletes monitor heart rates with wearable sensors during intense training sessions',
    'sailors see the flash before hearing the boom during offshore electrical storms',
]
for gi, (cl, s1, s2, s3) in enumerate(zip(guard_claims, surrs, surrs2, surrs3), start=1):
    w(f'{ROOT}/T10-5_guard{gi}/pages.txt', dedup([
        (f'g{gi}a', 'GA', f'ga{gi}.example', cl, s1),
        (f'g{gi}b', 'GB', f'gb{gi}.example', cl, s2),
        (f'g{gi}c', 'GC', f'gc{gi}.example', cl, s3),
    ]))

print('fixtures written under', ROOT)
