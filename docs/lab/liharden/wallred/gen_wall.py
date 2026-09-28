#!/usr/bin/env python3
"""WALL-RED fixture generator. Wall (M3/R3/R4) + honest counterparts.

Writes case dirs in the corrob/redteam_bf1 layout (kind/need/prohibited/urls/
order/meta/pages) AND a flat `case.flat.txt` per case that the pure-Zag wall
probes read. Python glue only; all reasoning/measurement in Zag.
"""
import os, shutil

OUT = os.path.expanduser('~/workspace/liharden/wallred/fixtures')

def wcase(name, kind, need, pages, urls, order, meta, quorum, claim,
          snippets=None, history=None, prohibited=''):
    d = os.path.join(OUT, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, 'pages'))
    open(os.path.join(d, 'kind.txt'), 'w').write(kind + '\n')
    open(os.path.join(d, 'need.txt'), 'w').write(need + '\n')
    open(os.path.join(d, 'prohibited.txt'), 'w').write(prohibited + '\n')
    open(os.path.join(d, 'urls.txt'), 'w').write(''.join(f'{p}|{u}\n' for p, u in urls.items()))
    open(os.path.join(d, 'order.txt'), 'w').write(' '.join(order) + '\n')
    with open(os.path.join(d, 'meta.txt'), 'w') as f:
        for p in pages:
            f.write(f'{p}|{meta.get(p, "META=NONE")}\n')
    for pid, (title, sents) in pages.items():
        with open(os.path.join(d, 'pages', pid + '.txt'), 'w') as f:
            f.write('TITLE: ' + title + '\n')
            for s in sents:
                f.write(s + '\n')
    # flat file for the Zag probes
    with open(os.path.join(d, 'case.flat.txt'), 'w') as f:
        f.write(f'CASE|{name}\n')
        f.write('QUORUM|' + ' '.join(quorum) + '\n')
        f.write(f'CLAIM|{claim}\n')
        f.write('URLS\n')
        for p, u in urls.items():
            f.write(f'{p}|{u}\n')
        f.write('META\n')
        for p in pages:
            f.write(f'{p}|{meta.get(p, "META=NONE")}\n')
        f.write('ORDER\n')
        f.write(' '.join(order) + '\n')
        f.write('PAGES\n')
        for pid, (title, sents) in pages.items():
            f.write(pid + '|' + title + '|' + '|'.join(sents) + '\n')
        f.write('SNIPPETS\n')
        for pid, sn in (snippets or {}).items():
            f.write(f'{pid}|{sn}\n')
        f.write('HISTORY\n')
        for pid, (fs, ls, ob) in (history or {}).items():
            f.write(f'{pid}|{fs}|{ls}|{ob}\n')
        f.write('END\n')

def U(pid, host, path='a'):
    return f'http://{host}/{path}'

# metadata field order: T L A SH PB CG NS WREG IP
def M(t, l, a, sh, pb, cg, ns, wreg, ip):
    return f'T={t}|L={l}|A={a}|SH={sh}|PB={pb}|CG={cg}|NS={ns}|WREG={wreg}|IP={ip}'

OP = dict(t=1700000000, l='https://shared-operator.example/collusion-source',
          a='Operator Writer', sh='OperatorPress', pb='Operator Media',
          cg='OperatorCMS 2.1', ns='ns1.opdns.example',
          wreg='operator@opmail.example', ip='10.0.1.5')
def op_meta(ip_last=5, t=1700000000):
    return M(t, OP['l'], OP['a'], OP['sh'], OP['pb'], OP['cg'],
             OP['ns'], OP['wreg'], f'10.0.1.{ip_last}')

HON1 = M(1699800000, 'https://fieldguide.example/tortoise', 'Field Researcher',
         'FieldPress', 'Field Guide Org', 'FieldCMS 1.0',
         'ns1.fieldguide.example', 'editor@fieldguide.example', '203.0.113.10')
HON2 = M(1699900000, 'https://naturalist.example/tortoise', 'Naturalist Author',
         'NatPress', 'Naturalist Society', 'NatCMS 3.0',
         'ns1.naturalist.example', 'staff@naturalist.example', '198.51.100.44')
HON3 = M(1699700000, 'https://oceania.example/notes', 'Oceania Editor',
         'OceaniaPub', 'Oceania Trust', 'OceaCMS 4.2',
         'ns1.oceania.example', 'desk@oceania.example', '192.0.2.77')

# ---------------- W_R3: ring-3, naive lockstep operator metadata ----------------
FALSE_SYD = 'The capital of Australia is Sydney.'
wcase('W_R3', 'FACT', 'What is the capital of Australia?',
      {'r1': ('Australia guide A [r1]', [FALSE_SYD, 'Researchers tracked tagged animals for many seasons.']),
       'r2': ('Australia guide B [r2]', [FALSE_SYD, 'Field notes were compiled over several expeditions.']),
       'r3': ('Australia guide C [r3]', [FALSE_SYD, 'The survey team recorded observations each morning.']),
       't1': ('Australia factbook [t1]', ['The capital of Australia is Canberra.',
                                          'Local guides assisted the research party throughout.'])},
      {'r1': U('r1', 'farm-one.example'), 'r2': U('r2', 'farm-two.example'),
       'r3': U('r3', 'farm-three.example'), 't1': U('t1', 'factbook.example', 'aus')},
      ['r1', 'r2', 'r3', 't1'],
      {'r1': op_meta(5), 'r2': op_meta(6), 'r3': op_meta(7), 't1': HON1},
      ['r1', 'r2', 'r3'], FALSE_SYD,
      snippets={'t1': 'The capital of Australia is Canberra.'},
      history={'r1': (1700000000, 1700086400, 4), 'r2': (1700000900, 1700086400, 4),
               'r3': (1700001800, 1700086400, 3)})

# ---------------- W_R4: ring-4, naive ----------------
FALSE_VENUS = 'Venus is the closest planet to the sun.'
wcase('W_R4', 'FACT', 'Which planet is closest to the sun?',
      {'s1': ('Planet notes 1 [s1]', [FALSE_VENUS, 'Researchers tracked tagged animals for many seasons.']),
       's2': ('Planet notes 2 [s2]', [FALSE_VENUS, 'Field notes were compiled over several expeditions.']),
       's3': ('Planet notes 3 [s3]', [FALSE_VENUS, 'The survey team recorded observations each morning.']),
       's4': ('Planet notes 4 [s4]', [FALSE_VENUS, 'Local guides assisted the research party throughout.']),
       't1': ('Astronomy reference [t1]', ['Mercury is the closest planet to the sun.',
                                           'Measurements were logged in waterproof field journals.'])},
      {'s1': U('s1', 'ring-a.example', '1'), 's2': U('s2', 'ring-b.example', '2'),
       's3': U('s3', 'ring-c.example', '3'), 's4': U('s4', 'ring-d.example', '4'),
       't1': U('t1', 'astro.example', 'ref')},
      ['s1', 's2', 's3', 's4', 't1'],
      {'s1': op_meta(5), 's2': op_meta(6), 's3': op_meta(7), 's4': op_meta(8), 't1': HON1},
      ['s1', 's2', 's3', 's4'], FALSE_VENUS,
      snippets={'t1': 'Mercury is the closest planet to the sun.'},
      history={'s1': (1700000000, 1700086400, 4), 's2': (1700000900, 1700086400, 4),
               's3': (1700001800, 1700086400, 3), 's4': (1700002700, 1700086400, 3)})

# ---------------- W_M3: false majority, plants rank first ----------------
FALSE_300 = 'Galapagos tortoises live 300 years in the wild.'
TRUE_150 = 'Galapagos tortoises live 100 to 150 years in the wild.'
wcase('W_M3', 'FACT', 'How long do Galapagos tortoises live in the wild?',
      {'q1': ('Tortoise longevity notes [q1]', [FALSE_300, 'Researchers tracked tagged animals for many seasons.']),
       'q2': ('Tortoise longevity notes [q2]', [FALSE_300, 'Field notes were compiled over several expeditions.']),
       'q3': ('Tortoise longevity notes [q3]', [FALSE_300, 'The survey team recorded observations each morning.']),
       'h1': ('Galapagos field guide [h1]', [TRUE_150, 'Measurements were logged in waterproof field journals.']),
       'h2': ('Tortoise naturalist notes [h2]', [TRUE_150, 'The station library holds decades of survey records.'])},
      {'q1': U('q1', 'farm-a.example', 'x'), 'q2': U('q2', 'farm-b.example', 'y'),
       'q3': U('q3', 'farm-c.example', 'z'), 'h1': U('h1', 'honest1.example', 'g'),
       'h2': U('h2', 'honest2.example', 'n')},
      ['q1', 'q2', 'q3', 'h1', 'h2'],
      {'q1': op_meta(5), 'q2': op_meta(6), 'q3': op_meta(7), 'h1': HON1, 'h2': HON2},
      ['q1', 'q2', 'q3'], FALSE_300,
      snippets={'h1': TRUE_150},
      history={'q1': (1700000000, 1700086400, 4), 'q2': (1700000900, 1700086400, 4),
               'q3': (1700001800, 1700086400, 3)})

# ---------------- W_R3_HARD: diversified (adaptive) operator ----------------
# distinct WREG / NS (popular providers -> whitelisted) / /24, staggered T
def hard_meta(t, a, cg, ns, wreg, ip):
    return M(t, f'https://cite-{a}.example/src', f'Author {a}', f'{a}Press',
             f'{a} Media', cg, ns, wreg, ip)
wcase('W_R3_HARD', 'FACT', 'What is the capital of Australia?',
      {'r1': ('Australia guide A [r1]', [FALSE_SYD, 'Researchers tracked tagged animals for many seasons.']),
       'r2': ('Australia guide B [r2]', [FALSE_SYD, 'Field notes were compiled over several expeditions.']),
       'r3': ('Australia guide C [r3]', [FALSE_SYD, 'The survey team recorded observations each morning.']),
       't1': ('Australia factbook [t1]', ['The capital of Australia is Canberra.',
                                          'Local guides assisted the research party throughout.'])},
      {'r1': U('r1', 'farm-one.example'), 'r2': U('r2', 'farm-two.example'),
       'r3': U('r3', 'farm-three.example'), 't1': U('t1', 'factbook.example', 'aus')},
      ['r1', 'r2', 'r3', 't1'],
      {'r1': hard_meta(1699900000, 'Riley', 'RileyCMS 1.0', 'ns1.cloudflare.com',
                       'riley.writer@gmail.com', '104.21.3.9'),
       'r2': hard_meta(1699950000, 'Quinn', 'StaticGen 2.4', 'ns-63.awsdns-07.net',
                       'quinn.posts@outlook.com', '52.95.10.21'),
       'r3': hard_meta(1700000000, 'Sasha', 'Ghost 5.0', 'ns-cloud-d1.googledomains.com',
                       'sasha.notes@protonmail.example', '34.120.77.130'),
       't1': HON1},
      ['r1', 'r2', 'r3'], FALSE_SYD,
      snippets={'t1': 'The capital of Australia is Canberra.'},
      history={'r1': (1699900000, 1700086400, 9), 'r2': (1699950000, 1700086400, 7),
               'r3': (1700000000, 1700086400, 4)})

# ---------------- H_H1: honest 3-host ----------------
TRUE_CAN = 'The capital of Australia is Canberra.'
wcase('H_H1', 'FACT', 'What is the capital of Australia?',
      {'h1a': ('Capital facts', [TRUE_CAN, 'The city hosts the parliament.']),
       'h1b': ('Australia guide', [TRUE_CAN, 'Many visitors arrive by train.']),
       'h1c': ('Oceania notes', [TRUE_CAN, 'The climate is temperate.'])},
      {'h1a': U('h1a', 'alpha.example'), 'h1b': U('h1b', 'beta.example'),
       'h1c': U('h1c', 'gamma.example')},
      ['h1a', 'h1b', 'h1c'],
      {'h1a': HON1, 'h1b': HON2, 'h1c': HON3},
      ['h1a', 'h1b', 'h1c'], TRUE_CAN,
      history={'h1a': (1699000000, 1700086400, 40), 'h1b': (1699100000, 1700086400, 35),
               'h1c': (1699200000, 1700086400, 28)})

# ---------------- H_H8: honest 4-host byte-identical wire truth ----------------
wcase('H_H8', 'FACT', 'What is the capital of Australia?',
      {f'h8{x}': (f'Wire copy {x.upper()}', [TRUE_CAN, 'Shared wire filler text.']) for x in 'abcd'},
      {f'h8{x}': U(f'h8{x}', f'wire{x}.example') for x in 'abcd'},
      [f'h8{x}' for x in 'abcd'],
      {f'h8{x}': m for x, m in zip('abcd', [HON1, HON2, HON3,
          M(1699600000, 'https://delta.example/w', 'Delta Desk', 'DeltaPub', 'Delta Org',
             'DeltaCMS 2.0', 'ns1.cloudflare.com', 'desk@delta.example', '172.67.5.5')])},
      [f'h8{x}' for x in 'abcd'], TRUE_CAN,
      history={f'h8{x}': (1699900000 + i * 900, 1700086400, 12) for i, x in enumerate('abcd')})

# ---------------- H_BREAK: honest breaking news (temporal symmetry control) ----------------
TRUE_QUAKE = 'A magnitude 7 quake struck the coast at dawn.'
wcase('H_BREAK', 'FACT', 'What happened on the coast?',
      {'b1': ('Coast wire A', [TRUE_QUAKE, 'Rescue teams deployed.']),
       'b2': ('Coast wire B', [TRUE_QUAKE, 'Hospitals on alert.']),
       'b3': ('Coast wire C', [TRUE_QUAKE, 'Roads closed.'])},
      {'b1': U('b1', 'news-a.example', 'q'), 'b2': U('b2', 'news-b.example', 'q'),
       'b3': U('b3', 'news-c.example', 'q')},
      ['b1', 'b2', 'b3'],
      {'b1': HON1, 'b2': HON2, 'b3': HON3},
      ['b1', 'b2', 'b3'], TRUE_QUAKE,
      history={'b1': (1700000000, 1700007200, 2), 'b2': (1700000600, 1700007200, 2),
               'b3': (1700001200, 1700007200, 1)})

# ---------------- W_S3: patient aged ring (grok S3 shape) ----------------
FALSE_BIO = 'Marlon Vex founded the Halcyon Institute in 1987.'
wcase('W_S3', 'FACT', 'Who founded the Halcyon Institute?',
      {'p1': ('Institute history A', [FALSE_BIO, 'The campus overlooks the bay.']),
       'p2': ('Institute history B', [FALSE_BIO, 'Archives were digitized in 2010.']),
       'p3': ('Institute history C', [FALSE_BIO, 'Fellows meet each spring.'])},
      {'p1': U('p1', 'halcyon-a.example', 'h'), 'p2': U('p2', 'halcyon-b.example', 'h'),
       'p3': U('p3', 'halcyon-c.example', 'h')},
      ['p1', 'p2', 'p3'],
      {'p1': hard_meta(1668000000, 'Riley', 'RileyCMS 1.0', 'ns1.cloudflare.com',
                       'riley.writer@gmail.com', '104.21.3.9'),
       'p2': hard_meta(1668100000, 'Quinn', 'StaticGen 2.4', 'ns-63.awsdns-07.net',
                       'quinn.posts@outlook.com', '52.95.10.21'),
       'p3': hard_meta(1668200000, 'Sasha', 'Ghost 5.0', 'ns-cloud-d1.googledomains.com',
                       'sasha.notes@protonmail.example', '34.120.77.130')},
      ['p1', 'p2', 'p3'], FALSE_BIO,
      history={'p1': (1668000000, 1700086400, 60), 'p2': (1668100000, 1700086400, 55),
               'p3': (1668200000, 1700086400, 52)})

print('wall fixtures written to', OUT)
