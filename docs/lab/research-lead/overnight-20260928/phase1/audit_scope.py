#!/usr/bin/env python3
"""PHASE 1 -- scope-accurate structural audit.

audit_structure.py v1 flagged 94 files as "learner state reaches a structural
sink". That was a LINE-COINCIDENCE false positive: it matched any line
containing both a state name and a sink name, with no scope check. hc_full.zag
was one such false positive: its two structural writers (mat_inputs,
apply_kind1) take (G, W) and (G, W, OUTS, ni) -- no learner state at all.

This version does the audit per-FUNCTION with parameter-scope resolution:
a structural write only counts if the function that performs it takes a
learner-state parameter, or reads a module-level learner-state buffer that
it also writes.

Run outside the PURE-ZAG session env: static analysis, not simulation.
"""
import re
import subprocess
import sys
from collections import defaultdict

# Structural sinks: writes that change what can exist or be executed.
STRUCTURAL = [
    (re.compile(r'\bnewnode\s*\('), 'newnode'),
    (re.compile(r'\breset_graph\s*\('), 'reset_graph'),
    (re.compile(r'\bset32\s*\(\s*(W|store|gr|graph|G)\b'), 'set32(struct)'),
    (re.compile(r'\bnset\s*\(\s*(W|store)\b'), 'nset(struct)'),
]

# learner-state parameter names, by convention in this corpus
STATE_HINT = re.compile(r'^(L|S|sup|acc|acc_|sup_|mem|hist|h_|state|st)[0-9_]*$', re.I)


def self_accumulating(text):
    """Buffers/scalars written from themselves = carry experience across steps."""
    found = set()
    for m in re.finditer(r'set32\(\s*([A-Za-z_]\w*)\s*,([^,]+),\s*get32\(\s*\1\s*,', text):
        found.add(m.group(1))
    for m in re.finditer(r'\b([A-Za-z_]\w*)\s*\[[^\]]+\]\s*=\s*\1\s*\[', text):
        found.add(m.group(1))
    for m in re.finditer(r'\b([A-Za-z_]\w*)\s*=\s*\1\s*[+\-]=?\s*', text):
        if m.group(1) not in ('i', 'j', 'k', 'm', 't', 'n', 'a', 'b', 'c', 'p', 'q',
                              'x', 'y', 'z', 'f', 'g', 'h', 's', 'r', 'v', 'w'):
            found.add(m.group(1))
    return found


def parse_functions(text):
    out = []
    for m in re.finditer(r'^fn\s+(\w+)\s*\(([^)]*)\)[^{]*\{', text, re.M):
        name, params = m.group(1), m.group(2)
        start = m.start()
        end = text.find('\nfn ', start + 1)
        if end < 0:
            end = len(text)
        out.append((name, params, start, end))
    return out


def audit(path):
    try:
        text = open(path, encoding='utf-8', errors='replace').read()
    except Exception:
        return None
    if 'fn main' not in text:
        return None

    state_buffers = self_accumulating(text)
    fns = parse_functions(text)

    state_params, struct_writers = set(), []
    for name, params, s, e in fns:
        body = text[s:e]
        pnames = [p.strip() for p in params.split(',') if p.strip()]
        for p in pnames:
            pn = p.split(':')[0].strip()
            if STATE_HINT.match(pn):
                state_params.add(pn)
        for rx, tag in STRUCTURAL:
            if rx.search(body):
                struct_writers.append((name, pnames, tag, body))
                break

    # structural write depends on learner state only if the writing function
    # takes a state parameter, or reads a self-accumulating buffer
    real = []
    for name, pnames, tag, body in struct_writers:
        dep = [p.split(':')[0].strip() for p in pnames
               if STATE_HINT.match(p.split(':')[0].strip())]
        if not dep:
            for sb in state_buffers:
                if re.search(r'\b' + re.escape(sb) + r'\b', body):
                    dep.append(sb + '(buffer)')
        if dep:
            real.append((name, tag, dep))

    return {
        'path': path,
        'n_fns': len(fns),
        'state_params': sorted(state_params),
        'state_buffers': sorted(state_buffers - state_params),
        'struct_writers': [(n, t) for n, p, t, b in struct_writers],
        'real_struct': real,
    }


def main(roots):
    files = []
    for r in roots:
        files += subprocess.check_output(['git', 'ls-files', r], text=True).split()
    files = [f for f in files if f.endswith('.zag')]
    print(f"auditing {len(files)} .zag sources, per-function with scope resolution\n")

    res = [r for r in (audit(f) for f in files) if r]
    with_struct = [r for r in res if r['struct_writers']]
    real_struct = [r for r in res if r['real_struct']]
    rank_only = [r for r in res
                 if r['struct_writers'] and not r['real_struct']]

    print(f"  sources with any structural writer          : {len(with_struct)}")
    print(f"  ... whose writer depends on learner state    : {len(real_struct)}")
    print(f"  ... whose writer does NOT depend on it       : {len(rank_only)}")

    if real_struct:
        print("\n--- GENUINE structural levers (must isolate and test) ---")
        for r in real_struct:
            for name, tag, dep in r['real_struct']:
                print(f"  {r['path']}")
                print(f"      fn={name} sink={tag} via={dep}")

    print("\n--- structural writers with NO learner-state dependence "
          "(the majority pattern) ---")
    for r in rank_only[:12]:
        print(f"  {r['path']}")
        print(f"      writers={','.join(n for n, t in r['struct_writers'][:5])}")
    if len(rank_only) > 12:
        print(f"  ... and {len(rank_only)-12} more")
    return real_struct, rank_only


if __name__ == '__main__':
    main(sys.argv[1:] or ['docs'])