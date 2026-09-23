#!/usr/bin/env python3
"""Generate loop/battery.json from the frozen curriculum + new probe items.
Run from the loop/ directory. No hand transcription: T3 seeds and T1/T2/T4
specs/demos/tests are copied programmatically from coding/curriculum/curriculum.json.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
CUR = os.path.join(HERE, '..', '..', 'curriculum', 'curriculum.json')
ALL_PATTERNS = "p_math,p_search,p_slice,p_strrev,p_func,p_loop,p_struct,p_sort,p_argv,p_strcnt,p_slicefill"

c = json.load(open(CUR))
tasks = {t['id']: t for t in c['tasks']}

items = []
# R1..R10: repair-from-broken seeds (proven T3 items)
for n, t in enumerate(c['t3'], 1):
    items.append({
        'id': 'R%02d-%s' % (n, t['id']),
        'mode': 'seed',
        'spec': 'Repair the broken program so it compiles and passes its tests.',
        'seed': t['broken'],
        'tests': t['tests'],
        'patterns': ALL_PATTERNS, 'demo': '', 'card': '',
    })

# G1..G4: generation tasks that pass first-try (proven T1/T2/T4 items)
for gid, tid in [('G1', 't4_01'), ('G2', 't4_04'), ('G3', 't1_01'), ('G4', 't2_05')]:
    t = tasks[tid]
    items.append({
        'id': '%s-%s' % (gid, tid),
        'mode': 'gen',
        'spec': t['spec'],
        'demo': t.get('demo', ''),
        'card': t.get('card', ''),
        'tests': t['tests'],
        'patterns': ALL_PATTERNS,
    })

# F1: compiles, wrong only in trailing whitespace -> OUTPUT_FORMAT repair
items.append({
    'id': 'F1-newline',
    'mode': 'seed',
    'spec': 'Print the number 42 followed by a newline.',
    'seed': 'fn main()void {\n  _zag_print("42");\n}\n',
    'tests': [{'args': [], 'stdout': '42\n', 'rc': 0}],
    'patterns': ALL_PATTERNS, 'demo': '', 'card': '',
})

# H1: compiles, wrong VALUE, spec is gen-able -> regen-from-spec recovery
t410 = tasks['t4_10']
items.append({
    'id': 'H1-fibsum',
    'mode': 'seed',
    'spec': t410['spec'],
    'demo': t410.get('demo', ''),
    'card': t410.get('card', ''),
    'seed': ('fn main()void {\n'
             '  let a:i64=0;\n'
             '  let b:i64=1;\n'
             '  let i:i64=0;\n'
             '  while(i<10){let t:i64=a+b;a=b;b=t;i=i+1;}\n'
             '  _zag_print(_zag_i64_to_str(a));\n'
             '  _zag_print("\\n");\n'
             '}\n'),
    'tests': t410['tests'],
    'patterns': ALL_PATTERNS,
})

# X1: spec beyond the learner's concepts -> gen failure -> halt-genfail
items.append({
    'id': 'X1-ackermann',
    'mode': 'gen',
    'spec': 'T4|GOAL|compute the ackermann function A(2,3)',
    'demo': '', 'card': '',
    'tests': [{'args': [], 'stdout': '9\n', 'rc': 0}],
    'patterns': ALL_PATTERNS,
})

# X2: unfixable compile error (undefined variable; no patch applies) -> halt-no-patch
items.append({
    'id': 'X2-undefvar',
    'mode': 'seed',
    'spec': 'Repair the broken program so it compiles and passes its tests.',
    'seed': ('fn main()void {\n'
             '  let x:i64=1;\n'
             '  _zag_print(_zag_i64_to_str(y));\n'
             '  _zag_print("\\n");\n'
             '}\n'),
    'tests': [{'args': [], 'stdout': '1\n', 'rc': 0}],
    'patterns': ALL_PATTERNS, 'demo': '', 'card': '',
})

battery = {'name': 'fast-loop-harness battery v1', 'items': items}
out = os.path.join(HERE, 'battery.json')
json.dump(battery, open(out, 'w'), indent=1, sort_keys=True)
print('wrote', out, '%d items' % len(items))
for i in items:
    print(' ', i['id'], i['mode'])
