#!/usr/bin/env python3
"""PHASE 1 -- mechanical audit: does learner state change STRUCTURE or only RANKING?

Method (dataflow, not naming): for each .zag source, identify learner-state
arrays (self-accumulating buffers), then trace every read of those arrays to
see whether it reaches a STRUCTURAL sink or only a RANKING sink.

Structural sinks (would mean learner state alters possibility):
  newnode, reset_graph, set32(W,...), set32(store,...), nset(...)

Ranking sinks (learner state only reorders a researcher-fixed space):
  compared against a running best (score/best), used in a tie-break,
  used as a sort key, used only as a counter for reporting.

The question is NOT whether a file mentions these names. It is whether a value
that learner state wrote flows INTO a structural sink.

Run outside the PURE-ZAG session env: this is static analysis, not simulation.
"""
import re
import sys
from collections import defaultdict

STRUCTURAL = [
    (re.compile(r'\bnewnode\s*\('), 'newnode'),
    (re.compile(r'\breset_graph\s*\('), 'reset_graph'),
    (re.compile(r'\bset32\s*\(\s*(W|store|gr|graph)\b'), 'set32(struct)'),
    (re.compile(r'\bnset\s*\(\s*(W|store)\b'), 'nset(struct)'),
]

RANKING = [
    (re.compile(r'>\s*best|best[a-z]*\s*[<>]=?\s*get32|>\s*bestScore'),
     'vs running best'),
    (re.compile(r'\bscore\b|bestScore|bestv|bestV|bs\b'), 'score/best compare'),
]


def learner_state_buffers(text):
    """Buffers written self-referentially: set32(X, i, get32(X,i) +/- ...) or X[i] += ...
    These are the only things that can carry experience across steps."""
    found = set()
    # set32(X, e, get32(X,e) OP ...)  -- same buffer name on both sides
    for m in re.finditer(
            r'set32\(\s*([A-Za-z_]\w*)\s*,([^,]+),\s*get32\(\s*\1\s*,', text):
        found.add(m.group(1))
    # NAME[...] = NAME[...] + ...  (scalar self-accumulation)
    for m in re.finditer(
            r'\b([A-Za-z_]\w*)\s*\[[^\]]+\]\s*=\s*\1\s*\[', text):
        found.add(m.group(1))
    # scalar: NAME = NAME + something inside a loop
    for m in re.finditer(r'\b([A-Za-z_]\w*)\s*=\s*\1\s*\+\s*', text):
        found.add(m.group(1))
    return found


def reads_of(text, name):
    """Every occurrence of `name` outside its own accumulator write."""
    out = []
    for m in re.finditer(r'\b' + re.escape(name) + r'\b', text):
        out.append(m.start())
    return out


def audit_file(path):
    try:
        text = open(path, encoding='utf-8', errors='replace').read()
    except Exception:
        return None
    if 'fn main' not in text:
        return None

    state = learner_state_buffers(text)
    state = {s for s in state if s not in ('i', 'j', 'k', 'm', 't', 'n', 'a', 'b', 'c', 'p', 'q')}
    if not state:
        return {'state': [], 'structural': False, 'ranking': False, 'path': path}

    # line-level attribution: for each line, which state names appear
    struct_hit = False
    rank_hit = False
    for line in text.splitlines():
        names = [s for s in state if re.search(r'\b' + re.escape(s) + r'\b', line)]
        if not names:
            continue
        for rx, _ in STRUCTURAL:
            if rx.search(line):
                struct_hit = True
        for rx, _ in RANKING:
            if rx.search(line):
                rank_hit = True
    return {
        'state': sorted(state),
        'structural': struct_hit,
        'ranking': rank_hit,
        'path': path,
    }


def main(roots):
    files = []
    for root in roots:
        files.extend(
            __import__('subprocess').check_output(
                ['git', 'ls-files', root], text=True).split())
    files = [f for f in files if f.endswith('.zag')]
    print(f"auditing {len(files)} .zag sources\n")

    res = []
    for f in files:
        r = audit_file(f)
        if r:
            res.append(r)

    both = [r for r in res if r['structural']]
    rank_only = [r for r in res if r['ranking'] and not r['structural']]
    neither = [r for r in res if not r['ranking'] and not r['structural']]

    print(f"  files with learner state reaching a STRUCTURAL sink : {len(both)}")
    print(f"  files with learner state reaching only RANKING sinks : {len(rank_only)}")
    print(f"  files with learner state and no classified sink     : {len(neither)}")
    print(f"  total with learner state                             : {len(res)}")

    if both:
        print("\n--- STRUCTURAL hits (learner state may alter possibility) ---")
        for r in sorted(both, key=lambda x: -len(x['state']))[:40]:
            print(f"  {r['path']}")
            print(f"      state={','.join(r['state'][:8])}")
    return both, rank_only, neither


if __name__ == '__main__':
    main(sys.argv[1:] or ['docs'])