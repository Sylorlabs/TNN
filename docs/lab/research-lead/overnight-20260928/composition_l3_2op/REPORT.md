# REPORT: Composition L3 Two-Op First Creation (LEDGER)

Verdict: **COMPOSITION-L3-2OP-COMPLETE** (all five frozen kill bars
pass, no falsifier fires).

Date: 2026-10-02. Worker: Composition L3 2-Op First-Creation Worker.
Prereg: `PREREG.md` (frozen 8ca044a80; committed alone before any
implementation existed; zero amendments). Determinism: 3/3
byte-identical runs (sha256
00744eb20a24a7a822068b46972cb4ce40389dc489f4dac00eff5068074bd348).

## What was built

Three Zag files, concatenated to `ledger_full.zag`, compiled with the
pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`) to
`ledger_bin`:

- `learner.zag`: byte-identical copy of the FORAGE/RELAY mechanism
  (sha256 9317f63c0a72263a533ef9a54b12eed7535dc71a0b202e0c9b14b247fce08e7b,
  verified before and after the build). Generic machinery + learned
  state only: X episode recall, Y threshold decide, register-machine
  program executor (ops 0=CPY 1=ADD 2=SUB 3=MAX 4=MIN), greedy program
  construction, threshold refit, generic adapt() policy (codes 0/1/2/3),
  decide() with -1 NO_DECISION. UNMODIFIED.
- `world.zag`: new LEDGER environment (experiment side only; the
  learner never calls it). Credit-minus-debit hidden rules: phase 1
  clear iff e0+e1-e2 >= 6; phase 2 clear iff e0+e1-e2 >= 9; phase 3
  clear iff e0+e1-e2+e3 >= 9. New episode tables (PREREG.md section 3)
  and the same five menu aggregations as controls.
- `driver.zag`: new experiment-side driver for LEDGER. Teaches X/Y,
  runs the learner's construct/adapt, evaluates the five arms and three
  phases, prints the kill-bar summary. It never invents the
  intermediate: all construction goes through the unmodified
  learner.zag. Output goes through one preallocated buffer and a single
  raw-syscall write.

## The creation trace (K-2OP-1, K-2OP-3)

Phase 1, construction from the empty program on 8 labeled episodes:

```
C-ROUND 1 base=5 eval=80 win=1,0,1 gain=2 score=7 t=9
C-ROUND 2 base=7 eval=80 win=2,0,2 gain=1 score=8 t=6
C-ROUND 3 base=8 eval=80 stop
M-BUILT n=2 t=6 score=8/8
M-STATE n=2 gen=1 sup=0 t=6 prog=1,0,1,2,0,2,...
```

Round 1: the learner evaluated 80 single-instruction candidates;
`ADD R0,R1` (bytes 1,0,1) was the UNIQUE 7/8 candidate (gain 2 over the
5/8 empty-program baseline at t=2). No single instruction reached 8/8:
the driver-side MAX1OP check over all 20 distinct d=0 candidates
returns 7/8. Round 2: from [ADD R0,R1], `SUB R0,R2` (bytes 2,0,2) was
the UNIQUE 8/8 candidate (gain 1, t=6). Round 3 stopped. The final
intermediate is the 2-op program [ADD R0,R1, SUB R0,R2] (R0 =
e0+e1-e2), invented in FIRST creation, with zero revision steps taken.

Rejected 1-op alternatives probed by the driver on phase-1 train:
ADD-R0-R1 7/8 t=9 (round-1 winner, imperfect), SUB-R0-R2 5/8 t=3,
SUB-R0-R3 6/8 t=0, MIN-R0-R2 6/8 t=2, ADD-R0-R3 5/8 t=14,
CPY-R0-R0 5/8 t=2. Prior-world solutions do not transfer:
FORAGE-ADD-R0-R2 5/8 t=5, RELAY-SUB-R0-R1 4/8 t=0. The final 2-op form
appears nowhere in the learner source (K-2OP-2 grep audit: 0 hits on
all 8 frozen patterns, including the solution expression, both
solution instructions, episode data, hardcoded thresholds, and any
mode/bridge token; sha256 matches the frozen FORAGE learner hash).

## Kill bars

- K-2OP-1 (insufficiency): PASS. Z-XONLY 0/4, Z-YONLY 0/4, Z-FULL 4/4,
  and MAX1OP 7/8 < 8/8. X and Y each alone fail Z; no 1-op suffices.
- K-2OP-2 (novelty): PASS. 8/8 frozen grep patterns return 0 hits on
  the copied learner.zag; sha256
  9317f63c0a72263a533ef9a54b12eed7535dc71a0b202e0c9b14b247fce08e7b
  matches the frozen FORAGE learner hash.
- K-2OP-3 (creation + necessity): PASS. Final program has exactly 2
  instructions (n=2), byte sequence 1,0,1,2,0,2 (M-FORM-2OP 1), 8/8 on
  phase-1 train, built by exactly two positive-gain rounds from empty
  (no revision involved); Z-FULL 4/4 and Z-NOM 0/4.
- K-2OP-4 (persistence): PASS. Phase-2 adapt code 1 (threshold-only,
  t 6 -> 7), 28 structural M bytes byte-identical (M-PERSIST 1),
  held-out 2/2.
- K-2OP-5 (determinism): PASS. ledger_run1/2/3.txt sha256-identical
  (00744eb2...), cmp clean.

Revision lifecycle (falsifier-armed, not a kill bar): phase-3 adapt
code 2; extension round 1 found ADD R0,R3 as the unique 8/8 append
(gain 1, t=9) from the 2-op base; M' = [ADD R0,R1, SUB R0,R2, ADD R0,R3]
(n=3, gen=2, t=9); old 2-op M retired to Mprev with superseded=1;
Z-REV 4/4.

## Falsifier sweep

F-ONEOP: silent (round-1 winner 7/8, final n=2 at 8/8).
F-MENU-WIN: silent (menu test scores 3/4, 1/4, 1/4, 3/4, 1/4).
F-ABLATE-FAIL: silent (0/4, 0/4). F-NOT-NECESSARY: silent (0/4).
F-NO-PERSIST: silent (M-PERSIST 1). F-NO-REUSE: silent (code 1, 2/2).
F-NO-REVISE: silent (code 2, 4/4). F-OP-EXPAND, F-LEARNER-MODIFIED,
F-AUDIT, F-NONDET, F-PYTHON: all silent.

## Design notes (pre-freeze, from NAMECHECK.md)

Two design iterations were caught by the awk verifier before the
prereg froze: (a) the first phase-1 draft let SUB R0,R2 reach 8/8 in
round 1 (1-op sufficiency, would have voided the build); fixed with
rich episodes with low e0-e2 and poor episodes with high e0-e2.
(b) the first phase-3 draft let CPY R0,R3 reach 8/8 in the extension
round (e3 was label-correlated); fixed with poor episodes with high e3
and very negative v, and rich episodes with low e3. Both fixes are
world-design corrections documented before implementation, not
post-hoc tuning: the frozen expectations were verified against the
corrected verifier before the prereg commit.

## Non-claims

- Targets the five composition-L3-2OP bars only; does not claim
  Micah's full 12-criterion L3 bar. One world family (ledger
  settlement); no generality claim beyond the demonstrated phases.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  Paper untouched. Nothing pushed. Local commits on tnn-native-lab.
