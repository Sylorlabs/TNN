# W9 CONSTRUCTION AUDIT — sensory-buffer seal (PREREG_W9.md §3/§6)

**Date:** 2026-09-24. **Auditor:** WILD-A crew. **Status:** PASS — battery
unblocked.
**Sources audited:** `wild/w9/w9.zag`, plus `wild/r4lib.zag` plumbing.

## Method

Source inspection of the renderer functions plus an input-arity assertion:
the renderer must take exactly `(strong, agree)` — no `(conf, mrgF)`
parameter, no global/closure capture of the sensory buffer, and no
compressed-copy smuggling (prototypes must be small integer constants, not
encoded percept data).

## Findings

(a) **Input arity:** the renderer is two functions,
`render_conf(strong:i64, agree:i64)` and `render_mrg(strong:i64, agree:i64)`
— exactly two parameters each. The only call sites (lines 58–59) pass
`(strong, agree)` and nothing else.

(b) **No sensory-buffer capture:** the bodies of both renderer functions
contain zero references to the `aconf`/`amrg` arenas, zero references to
any `conf`/`mrg` variable (the single grep hit for "conf" inside the
function text is the function's own name `render_conf`). Zag has no
closures; the only data a function can see are its parameters and globals,
and the renderer reads neither global arenas nor anything derived from
`(conf, mrgF)`.

(c) **No compressed-copy smuggling:** the prototypes are six integer
constants total — `(850,15000)`, `(750,8000)`, `(720,2000)` — selected by
the four trace classes. Two integers per class cannot encode the
`(conf, mrgF)` percept; they are trace-conditional constants as the prereg
requires.

(d) **The fidelity comparison** (`20*|conf−conf′| + |mrgF−mrgF′| ≤ 11000`)
runs in `main`, outside the renderer — the gate may see the sensory
buffer; the renderer may not. This matches the prereg's seal definition.

**Verdict: PASS.** The W9 battery may run.
