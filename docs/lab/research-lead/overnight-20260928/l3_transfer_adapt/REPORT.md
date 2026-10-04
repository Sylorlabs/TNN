# REPORT: L3 Transfer-Adapt

Verdict: **L3-TRANSFER-ADAPT-COMPLETE**. All kill bars T1-T8 PASS, no
falsifier fired, 3/3 deterministic runs byte identical with ALL PASS.

## What was tested

Whether a stored invented intermediate M can be ADAPTED (not exactly
reused, not reinvented) for a partially matching domain, via generic
L2 operators. Domain A (FORAGE) invents M_A = [ADD R0,R2] computing
e0+e2. Domain B (AEGIS, hidden rule alert iff e0+e2+e3 >= 16) partially
matches: e0+e2 is necessary but not sufficient. The learner's generic
lib_adapt policy rejects exact reuse (M_A probes 7/8, decoy M_C 5/8),
scans the L2 adaptation neighborhoods, and adopts EXTEND(M_A,
(ADD,0,3)) = [ADD R0,R2, ADD R0,R3] with recorded provenance
(parent=entry 0, op=EXTEND), at 80 evals vs 240 for fresh construction,
with zero construction evals in phase B.

## Kill bar results

- T1 determinism: PASS. run1/2/3.txt sha256 identical:
  9a67cbc29515331935276b7d46f0d190d6e3a489b7866f00bd1378636e66b0d6.
  Stdout byte verified (od -c spot check), single buffer single
  raw syscall write, no RNG.
- T2 invention in A: PASS. code=1, rounds=2, evals=160, base0=5,
  win=(1,0,2), gain=3, score=8, t=10. Entry 0 = [1,0,2], n=1,
  origin=FORAGE, parent=255. A test 4/4.
- T3 RELAY adaptation: PASS. Exact probe of M_A on RELAY = 5/8
  t=12, rejected. code=2, entry=0, op=SPECIALIZE, pos=0,
  instr=(2,0,1), t=3, score=8, adapt_evals=161 (80 EXTEND + 1
  TRUNCATE + 80 SPECIALIZE). Entry 1 = [2,0,1], origin=RELAY,
  parent=0, pop=SPECIALIZE. Uniqueness audit: exactly one perfect
  (0, SPECIALIZE, pos 0, (2,0,1)). C test 4/4.
- T4 AEGIS adaptation: PASS. Exact probes 7/8 t=16 and 5/8,
  n_perfect=0. code=2, entry=0, op=EXTEND, instr=(1,0,3), t=16,
  score=8, adapt_evals=80. construct_evals delta = 0. M slot =
  [1,0,2,1,0,3], n=2, threshold 16. Entry 2 = [1,0,2,1,0,3], n=2,
  origin=AEGIS, parent=0, pop=EXTEND. Chain: entry 2 -> entry 0
  (FORAGE, invented). Uniqueness audit: exactly one perfect
  (0, EXTEND, (1,0,3)) across all entries, operators, candidates.
  B test 4/4.
- T5 fresh baseline: PASS. ARM-FRESH code=1, rounds=3, evals=240,
  rwin[0]=(1,0,2,gain 2,score 7,t 16),
  rwin[1]=(1,0,3,gain 1,score 8,t 16). Invented entry
  [1,0,2,1,0,3], origin=AEGIS, parent=255. Y prior fit 6/6 t=16.
  B test 4/4.
- T6 cheaper: PASS. 80 < 240.
- T7 library causal: PASS. ARM-NO-LIB wipes the library (LIBN=0),
  phase B constructs from scratch: code=1, evals delta=240,
  origin=AEGIS, B test 4/4.
- T8 hygiene: PASS. 0 modes, 0 bridges, 0 handlers, 0 new semantic
  cases (frozen grep audit: all 7 patterns 0 matches). Pure Zag for
  all research logic. Safebin PATH, no python/python3 resolvable or
  invoked. Unfrozen scope only; frozen source untouched; paper
  untouched; nothing pushed; explicit pathspecs on all git
  operations; no em/en dashes in docs (byte verified).

## Falsifiers

None fired. F-NO-INVENT-A, F-C-NOT-SPECIALIZE, F-C-EXACT-REUSE,
F-WRONG-ADAPT, F-REINVENT-B, F-ORIGIN, F-NO-SPEEDUP, F-NONUNIQUE,
F-OP-EXPAND, F-AUDIT, F-NONDET, F-PYTHON: all silent.

## What this establishes (and does not)

Establishes: a learner-owned intermediate invented in one domain can
be adapted, not reinvented, for a partially matching domain through a
domain-blind generic policy, with (a) evidence-driven selection (exact
probe rejection, neighborhood scan), (b) lower cost than fresh
invention (80 vs 240 evals, 3x), (c) white-box provenance (parent
entry + operator recorded in learner state), and (d) causal
attribution to the library (wipe restores full cost). Two L2
operators fired on real partial-match structure: EXTEND (AEGIS) and
SPECIALIZE (RELAY, where no EXTEND/TRUNCATE of M_A fit and the
1-edit neighborhood contained the RELAY solution).

Does not establish: broad generality (two adaptation instances, both
builder-designed tables, no independent adversary; Micah C0-C open);
TRUNCATE as a learning operator (implemented, unit tested on fixed
programs, no frozen learning domain exercises it); Micah's full
12-criterion L3 bar. The adapted program is byte identical to the
fresh-construction optimum; the claim rests on path, cost, and
provenance, stated in PREREG 10.

## Architecture accounting

- learner.zag 743 lines, driver.zag 466 lines. New learner state:
  library entry parent/pop provenance fields, adapt_calls,
  adapt_evals counters. New generic machinery: three L2 operators
  (EXTEND/TRUNCATE/SPECIALIZE), adapt_eval_one candidate
  evaluation, lib_adapt transfer policy.
- Modes/bridges/handlers added: 0. New hardcoded semantic cases: 0.
  Op basis unchanged {CPY,ADD,SUB,MAX,MIN}.

## Files

`docs/lab/research-lead/overnight-20260928/l3_transfer_adapt/`:
NAMECHECK.md, PREREG.md (frozen, committed alone as 5b8f3ce8c),
REPORT.md, learner.zag, driver.zag, full.zag, build.sh,
compile.log, l3a_bin, run1.txt, run2.txt, run3.txt.
