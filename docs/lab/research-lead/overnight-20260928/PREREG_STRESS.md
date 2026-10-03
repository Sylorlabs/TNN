# Preregistration: Stress Test of the Unified Learner (H-STRESS)

**Date:** 2026-09-29
**Status:** FROZEN (committed before implementation)
**Hypothesis H-STRESS:** The unified learner (`unified_learn.zag`, H-UNIFIED SURVIVES 9/9)
degrades gracefully under store pressure: it processes 10+ interleaved learning
events without crashing, returns honest failure (-1) when stores are full,
never silently corrupts or overwrites existing entries, retains old tasks, and
keeps procedure and causal paths non-interfering.

**Store capacities (from committed source):**
- Procedure store: 16 slots (`PROC_MAX`)
- Bridge rule store: 4 slots (`BR_MAX`)
- Causal rule store: 16 slots (`CR_MAX`)

## Planned event sequence (all unlabeled, one process, no reset)

| # | Event | Type | Predicted outcome |
|---|-------|------|-------------------|
| E1 | S1 reverse `abcd>dcba;efgh>hgfe` | PROC_LEARN simple | slot 0, reverse stored |
| E2 | C1 cond trigger `x` (5 pairs) | PROC_LEARN conditional | bridge rule 0, proc slots 1,2 |
| E3 | S2 bcast-last `abcd>dddd;efgh>hhhh` | PROC_LEARN simple | proc slot 3 |
| E4 | C2 cond trigger `y` (5 pairs) | PROC_LEARN conditional | bridge rule 1, proc slots 4,5 |
| E5 | S3 bcast-first `abcd>aaaa;efgh>eeee` | PROC_LEARN simple | proc slot 6 |
| E6 | C3 cond trigger `z` (5 pairs) | PROC_LEARN conditional | bridge rule 2, proc slots 7,8 |
| E7 | S4 identity `abcd>abcd;efgh>efgh` | PROC_LEARN simple | proc slot 9 |
| E8 | C4 cond trigger `w` (5 pairs) | PROC_LEARN conditional | bridge rule 3, proc slots 10,11; bridge now 4/4 FULL |
| E9 | C5 cond trigger `v` (5 pairs) | PROC_LEARN conditional | **-1 (bridge full). Predicted leak: proc slots 12,13 consumed and wasted** |
| E10+ | Fill loop: reverse on fresh alphabets until -1 | PROC_LEARN simple | succeeds until proc 16/16, then -1 |
| E_over | one more simple reverse | PROC_LEARN simple | **-1 (proc full)** |
| EK1 | 16 causal episodes, 16 distinct (s0,act) | CAUS_LEARN | 16 causal rules |
| EK2 | 2 causal episodes, 2 new (s0,act) | CAUS_LEARN | no new rules (causal full) |

Total learning events: 15+. Ambiguity probes (`ab>ba`, `hello;world`)
interleaved; all must WITHHOLD.

**Predicted leak (F-LEAK, from code reading):** In `bridge_learn`, when
`br_store` fails on a full bridge store, the already-stored `s1`/`s2`
procedure slots are NOT released (the `return -1` path skips cleanup).
E9 is predicted to return -1 while still consuming 2 proc slots. This is
wasteful but not corrupting; it is recorded as a finding, not a kill.

## Frozen kill bars

- **K-S1 (no crash, 10+ events):** PASS if the program processes all 15+
  learning events plus queries and exits 0 with no crash, hang, or
  out-of-bounds write. Any crash, hang, or sanitizer-style fault = FAIL.
- **K-S2 (graceful exhaustion):** PASS if (a) E_over returns -1, (b) proc
  used count is exactly 16 afterwards, (c) slot 0 still applies
  `hello`->`olleh`, (d) bridge rule 0 still dispatches `xqw`->`xxx`.
  Any overwrite, corruption, or crash = FAIL. The F-LEAK waste is
  documented separately and does not fail this bar.
- **K-S3 (retention):** PASS if after all pressure: (a) slot 0 procedure
  still maps `hello`->`olleh`, (b) bridge rule 0 still maps `xqw`->`xxx`
  and `zzz`->`zzz`, (c) causal predictions for taught combos still correct
  (`cpredict(2,0,3)` gives s1=1, `cpredict(0,0,0)` gives s1=0).
  Any wrong answer = FAIL. Honest WITHHOLD where nothing was learned = PASS.
- **K-S4 (no interference):** PASS if (a) causal learning succeeds while
  the proc store is full, (b) causal queries are correct after proc
  exhaustion, (c) proc queries are correct after causal fill, (d) all
  ambiguity probes WITHHOLD (zero misroutes). Any cross-type corruption
  or misroute = FAIL.

## Method

- Pure Zag, no Python. Mechanism code copied verbatim from committed
  `unified_learn.zag`; only `main()` is replaced with the stress sequence.
- Determinism: 3 runs, md5-identical outputs required.
- Raw output committed as authoritative evidence.

## What success / failure looks like

Success: all four bars PASS; the learner is robust under pressure with
honest failure modes. Failure: any crash, corruption, overwrite,
catastrophic forgetting presented as success, or cross-type interference.
The F-LEAK finding is reported regardless.
