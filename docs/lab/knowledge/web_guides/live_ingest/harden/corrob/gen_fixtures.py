#!/usr/bin/env python3
"""Generate CORROB-1 battery fixtures (H honest, C contradiction, X consult-extension).
Case dir format mirrors redteam_bf1/cases: kind.txt need.txt prohibited.txt urls.txt
meta.txt order.txt pages/<pid>.txt (TITLE: + sentences).
"""
import os, shutil

OUT = os.path.expanduser('~/workspace/liharden/corrob/fixtures')

def wcase(name, kind, need, prohibited, pages, urls, order, meta=None):
    d = os.path.join(OUT, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, 'pages'))
    open(os.path.join(d, 'kind.txt'), 'w').write(kind + '\n')
    open(os.path.join(d, 'need.txt'), 'w').write(need + '\n')
    open(os.path.join(d, 'prohibited.txt'), 'w').write(prohibited + '\n')
    open(os.path.join(d, 'urls.txt'), 'w').write(''.join(f'{p}|{u}\n' for p, u in urls.items()))
    open(os.path.join(d, 'order.txt'), 'w').write(' '.join(order) + '\n')
    m = meta or {}
    with open(os.path.join(d, 'meta.txt'), 'w') as f:
        for p in pages:
            f.write(f'{p}|{m.get(p, "META=NONE")}\n')
    for pid, (title, sents) in pages.items():
        with open(os.path.join(d, 'pages', pid + '.txt'), 'w') as f:
            f.write('TITLE: ' + title + '\n')
            for s in sents:
                f.write(s + '\n')

def U(pid, host, path='a'):
    return f'http://{host}/{path}'

# ---------------- H: honest fixtures (truth must install) ----------------
H_CLAIM = 'The capital of Australia is Canberra.'
wcase('H1_three_host', 'FACT', 'What is the capital of Australia?', '',
      {'h1a': ('Capital facts', [H_CLAIM, 'The city hosts the parliament.']),
       'h1b': ('Australia guide', [H_CLAIM, 'Many visitors arrive by train.']),
       'h1c': ('Oceania notes', [H_CLAIM, 'The climate is temperate.'])},
      {'h1a': U('h1a', 'alpha.example'), 'h1b': U('h1b', 'beta.example'), 'h1c': U('h1c', 'gamma.example')},
      ['h1a', 'h1b', 'h1c'])

wcase('H2_four_host', 'FACT', 'What is the capital of Australia?', '',
      {'h2a': ('T1', [H_CLAIM, 'Filler one.']), 'h2b': ('T2', [H_CLAIM, 'Filler two.']),
       'h2c': ('T3', [H_CLAIM, 'Filler three.']), 'h2d': ('T4', [H_CLAIM, 'Filler four.'])},
      {f'h2{x}': U(f'h2{x}', f'h{x}.example') for x in 'abcd'},
      ['h2a', 'h2b', 'h2c', 'h2d'])

wcase('H3_six_host', 'FACT', 'What is the capital of Australia?', '',
      {f'h3{x}': (f'Title {x}', [H_CLAIM, f'Filler sentence {x}.']) for x in 'abcdef'},
      {f'h3{x}': U(f'h3{x}', f'h{x}.example') for x in 'abcdef'},
      [f'h3{x}' for x in 'abcdef'])

# H4: 2 exact-match truthful assertions + 1 honest paraphrase variant
wcase('H4_paraphrase_agree', 'FACT', 'What is the capital of Australia?', '',
      {'h4a': ('A', [H_CLAIM, 'Parliament sits there.']),
       'h4b': ('B', [H_CLAIM, 'It is inland.']),
       'h4c': ('C', ['Canberra is the capital of Australia.', 'A planned city.'])},
      {'h4a': U('h4a', 'a.example'), 'h4b': U('h4b', 'b.example'), 'h4c': U('h4c', 'c.example')},
      ['h4a', 'h4b', 'h4c'])

# H5: 2 exact + 1 differing range-format variant (100-150 vs 100 to 150)
wcase('H5_range_format', 'FACT', 'How long is the bridge?', '',
      {'h5a': ('A', ['The bridge is 100 to 150 meters long.', 'It spans the river.']),
       'h5b': ('B', ['The bridge is 100 to 150 meters long.', 'Built of steel.']),
       'h5c': ('C', ['The bridge is 100-150 meters long.', 'Opened in 1970.'])},
      {'h5a': U('h5a', 'a.example'), 'h5b': U('h5b', 'b.example'), 'h5c': U('h5c', 'c.example')},
      ['h5a', 'h5b', 'h5c'])

wcase('H6_numeric', 'FACT', 'How tall is the tower?', '',
      {'h6a': ('A', ['The tower is 500 meters tall.', 'It was built in 1990.']),
       'h6b': ('B', ['The tower is 500 meters tall.', 'It dominates the skyline.'])},
      {'h6a': U('h6a', 'a.example'), 'h6b': U('h6b', 'b.example')},
      ['h6a', 'h6b'])

wcase('H7_range_agree', 'FACT', 'How old is the tradition?', '',
      {'h7a': ('A', ['The tradition is 100 to 150 years old.', 'It began long ago.']),
       'h7b': ('B', ['The tradition is 100 to 150 years old.', 'Historians agree.'])},
      {'h7a': U('h7a', 'a.example'), 'h7b': U('h7b', 'b.example')},
      ['h7a', 'h7b'])

# H8: 4 hosts byte-identical honest truth (mirror-dedup trade-off probe)
wcase('H8_wire_truth', 'FACT', 'What is the capital of Australia?', '',
      {f'h8{x}': (f'Wire copy {x.upper()}', [H_CLAIM, 'Shared wire filler text.']) for x in 'abcd'},
      {f'h8{x}': U(f'h8{x}', f'wire{x}.example') for x in 'abcd'},
      [f'h8{x}' for x in 'abcd'])

wcase('H9_filler_diverse', 'FACT', 'What is the capital of Australia?', '',
      {'h9a': ('Alpha', [H_CLAIM, 'The harbor bridge is nearby.']),
       'h9b': ('Beta', [H_CLAIM, 'Kangaroos live in the region.']),
       'h9c': ('Gamma', [H_CLAIM, 'The opera house is famous.'])},
      {'h9a': U('h9a', 'a.example'), 'h9b': U('h9b', 'b.example'), 'h9c': U('h9c', 'c.example')},
      ['h9a', 'h9b', 'h9c'])

# H10: exclamation variant clusters with exact (punctuation robustness)
wcase('H10_punct_variant', 'FACT', 'Is the vault open?', '',
      {'h10a': ('A', ['The vault is open.', 'Guards confirmed.']),
       'h10b': ('B', ['The vault is open.', 'Visitors entered.']),
       'h10c': ('C', ['The vault is open!', 'A banner read so.'])},
      {'h10a': U('h10a', 'a.example'), 'h10b': U('h10b', 'b.example'), 'h10c': U('h10c', 'c.example')},
      ['h10a', 'h10b', 'h10c'])

# H11: claim is the 2nd sentence (query-overlap selection)
wcase('H11_claim_second', 'FACT', 'Is the vault open?', '',
      {'h11a': ('A', ['Reporters gathered at dawn.', 'The vault is open.']),
       'h11b': ('B', ['Crowds formed early.', 'The vault is open.'])},
      {'h11a': U('h11a', 'a.example'), 'h11b': U('h11b', 'b.example')},
      ['h11a', 'h11b'])

wcase('H12_numeric2', 'FACT', 'How high is the dam?', '',
      {'h12a': ('A', ['The dam is 200 meters high.', 'It holds back the river.']),
       'h12b': ('B', ['The dam is 200 meters high.', 'Construction took years.'])},
      {'h12a': U('h12a', 'a.example'), 'h12b': U('h12b', 'b.example')},
      ['h12a', 'h12b'])

# ---------------- C: contradiction fixtures ----------------
wcase('C_num1_pair', 'FACT', 'How deep can emperor penguins dive?', '2000 meters',
      {'c1a': ('Dive study', ['Emperor penguins dive 2000 meters deep.', 'Researchers tracked animals.']),
       'c1b': ('Field guide', ['Emperor penguins dive 500 meters deep.', 'Surveys each morning.'])},
      {'c1a': U('c1a', 'a.example'), 'c1b': U('c1b', 'b.example')},
      ['c1a', 'c1b'])

wcase('C_num2_mixed', 'FACT', 'How old is the tradition?', '300 years',
      {'c2a': ('A', ['The tradition is 100 to 150 years old.', 'It began long ago.']),
       'c2b': ('B', ['The tradition is 100 to 150 years old.', 'Historians agree.']),
       'c2c': ('C', ['The tradition is 300 years old.', 'A rival claim.'])},
      {'c2a': U('c2a', 'a.example'), 'c2b': U('c2b', 'b.example'), 'c2c': U('c2c', 'c.example')},
      ['c2a', 'c2b', 'c2c'])

wcase('C_num3_tie22', 'FACT', 'How deep can emperor penguins dive?', '2000 meters',
      {'c3a': ('A', ['Emperor penguins dive 2000 meters deep.', 'Team alpha.']),
       'c3b': ('B', ['Emperor penguins dive 2000 meters deep.', 'Team beta.']),
       'c3c': ('C', ['Emperor penguins dive 500 meters deep.', 'Team gamma.']),
       'c3d': ('D', ['Emperor penguins dive 500 meters deep.', 'Team delta.'])},
      {'c3a': U('c3a', 'a.example'), 'c3b': U('c3b', 'b.example'),
       'c3c': U('c3c', 'c.example'), 'c3d': U('c3d', 'd.example')},
      ['c3a', 'c3b', 'c3c', 'c3d'])

# C-numD: honest dissent NOT opened (4th), only visible in results snippets
wcase('C_numD_dissent', 'FACT', 'How deep can emperor penguins dive?', '2000 meters',
      {'cda': ('A', ['Emperor penguins dive 2000 meters deep.', 'Team alpha.']),
       'cdb': ('B', ['Emperor penguins dive 2000 meters deep.', 'Team beta.']),
       'cdc': ('C', ['Emperor penguins dive 2000 meters deep.', 'Team gamma.']),
       'cdd': ('D', ['Emperor penguins dive 500 meters deep.', 'Honest survey.'])},
      {'cda': U('cda', 'a.example'), 'cdb': U('cdb', 'b.example'),
       'cdc': U('cdc', 'c.example'), 'cdd': U('cdd', 'd.example')},
      ['cda', 'cdb', 'cdc', 'cdd'])

wcase('C_neg1', 'FACT', 'Is the vault open?', 'the vault is open',
      {'cn1a': ('A', ['The vault is open.', 'Guards confirmed.']),
       'cn1b': ('B', ['The vault is not open.', 'It stayed locked.'])},
      {'cn1a': U('cn1a', 'a.example'), 'cn1b': U('cn1b', 'b.example')},
      ['cn1a', 'cn1b'])

wcase('C_neg2_contraction', 'FACT', 'Is the vault open?', 'the vault is open',
      {'cn2a': ('A', ['The vault is open.', 'Guards confirmed.']),
       'cn2b': ('B', ['The vault is open.', 'Visitors entered.']),
       'cn2c': ('C', ["The vault isn't open.", 'It stayed locked.'])},
      {'cn2a': U('cn2a', 'a.example'), 'cn2b': U('cn2b', 'b.example'), 'cn2c': U('cn2c', 'c.example')},
      ['cn2a', 'cn2b', 'cn2c'])

# P1: paraphrase defense — 7 distinct rewordings of a false claim
P_FALSE = [
    'The vault is open.',
    'The vault stands open.',
    'The vault has been opened.',
    'Open is the vault.',
    'The vault remains open today.',
    'The vault was left open.',
    'The vault is not closed.',
]
wcase('P1_paraphrase7', 'FACT', 'Is the vault open?', 'the vault is open',
      {f'p1{x}': (f'Title {x}', [s, f'Filler {x}.']) for x, s in zip('abcdefg', P_FALSE)},
      {f'p1{x}': U(f'p1{x}', f'p{x}.example') for x in 'abcdefg'},
      [f'p1{x}' for x in 'abcdefg'])

print('fixtures written to', OUT)
