#!/usr/bin/env python3
"""PHASE 1 -- structural audit, v3: type-aware.

Two prior versions were wrong and both errors were mine:

  v1 (audit_structure.py): line-coincidence matching. Reported 94 structural
     hits; hc_full.zag was a false positive -- its structural writers take
     (G,W) and (G,W,OUTS,ni), no learner state.

  v2 (audit_scope.py): added per-function parameter scoping, but its
     self-accumulation regex also matched SCALAR self-assignment `x = x + ...`.
     That captured ordinary locals and i32 parameters -- `fn es(W,e:i32,f:i32,
     v:i32)` in bp2_full.zag reported "learner state via buffer e" when `e` is
     an edge index. 137/137 "genuine levers" were this artifact.

v3 requires, for a structural lever:
  1. the writing function has a learner-state ARRAY parameter
     (declared `X:[]u8`, not `X:i32`), AND
  2. that array is self-accumulating (set32(X,...,get32(X,...)) or X[i]=X[i]),
     AND
  3. the structural sink reads that parameter.

Run outside the PURE-ZAG session env: static analysis, not simulation.
"""
import re
import subprocess
import sys

# Sinks that change what can exist or be executed.
STRUCTURAL = [
    (re.compile(r'\bnewnode\s*\('), 'newnode'),
    (re.compile(r'\breset_graph\s*\('), 'reset_graph'),
    (re.compile(r'\bset32\s*\(\s*(W|store|gr|graph|G)\b'), 'set32(struct)'),
    (re.compile(r'\bnset\s*\(\s*(W|store)\b'), 'nset(struct)'),
]

# only these names count as learner state, and only when declared as []u8
STATE_NAMES = {'L', 'S', 'sup', 'acc', 'mem', 'hist', 'state', 'st', 'W_state'}

PARAM_RE = re.compile(r'([A-Za-z_]\w*)\s*:\s*\[\]u8')


def parse_functions(text):
    out = []
    for m in re.finditer(r'^fn\s+(\w+)\s*\(([^)]*)\)[^{]*\{', text, re.M):
        end = text.find('\nfn ', m.start() + 1)
        if end < 0:
            end = len(text)
        out.append((m.group(1), m.group(2), m.start(), end))
    return out


def is_accumulating(text, name):
    """Self-referential write on an array parameter named `name`."""
    a = re.search(r'set32\(\s*' + name + r'\s*,[^,]+,\s*get32\(\s*' + name + r'\s*,', text)
    b = re.search(re.escape(name) + r'\s*\[[^\]]+\]\s*=\s*' + re.escape(name) + r'\s*\[', text)
    return bool(a or b)


def audit(path):
    try:
        text = open(path, encoding='utf-8', errors='replace').read()
    except Exception:
        return None
    if 'fn main' not in text:
        return None
    fns = parse_functions(text)

    writers, levers = [], []
    for name, params, s, e in fns:
        body = text[s:e]
        tag = None
        for rx, t in STRUCTURAL:
            if rx.search(body):
                tag = t
                break
        if not tag:
            continue

        arrs = {p for p in PARAM_RE.findall(params)}
        # which of this fn's array params are learner state AND accumulating?
        st = [a for a in arrs
              if a in STATE_NAMES and is_accumulating(text, a)]
        writers.append((name, tag, sorted(arrs), sorted(st)))

        if st:
            # the sink must actually read that array on the same line-ish body
            if re.search(r'\b' + re.escape(st[0]) + r'\b', body):
                levers.append((name, tag, st[0]))

    return {
        'path': path,
        'n_fns': len(fns),
        'writers': writers,
        'levers': levers,
    }


def main(roots):
    files = []
    for r in roots:
        files += subprocess.check_output(['git', 'ls-files', r], text=True).split()
    files = [f for f in files if f.endswith('.zag')]
    print(f"auditing {len(files)} .zag sources (type-aware)\n")

    res = [r for r in (audit(f) for f in files) if r]
    w = [r for r in res if r['writers']]
    lv = [r for r in res if r['levers']]

    print(f"  sources with a structural writer                 : {len(w)}")
    print(f"  sources where that writer reads LEARNER STATE     : {len(lv)}")
    print(f"  sources where the writer is state-independent     : {len(w) - len(lv)}")

    if lv:
        print("\n--- GENUINE structural levers -- isolate and test ---")
        for r in lv:
            for name, tag, via in r['levers']:
                print(f"  {r['path']}")
                print(f"      fn={name} sink={tag} learner_state={via}")

    print("\n--- state-independent structural writers (sample) ---")
    for r in [x for x in w if not x['levers']][:15]:
        nm = ','.join(n for n, t, a, s in r['writers'][:4])
        print(f"  {r['path']}")
        print(f"      writers={nm}  arrays={[a for n,t,a,s in r['writers'][:2]]}")
    n = len([x for x in w if not x['levers']])
    if n > 15:
        print(f"  ... and {n-15} more")
    return lv, w


if __name__ == '__main__':
    main(sys.argv[1:] or ['docs'])