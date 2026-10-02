# REPORT: Composition L3 Novel Intermediate (FORAGE)

Verdict: **COMPOSITION-L3-COMPLETE** (all seven frozen kill bars pass,
no falsifier fires).

Date: 2026-10-02. Worker: Composition L3 Novel Intermediate Worker.
Prereg: `PREREG.md` (frozen 4339bbe9e; transparent amendment 53bab7771,
re-frozen before the implementation commit). Determinism: 3/3
byte-identical runs (sha256
014e175b96992a3f085f839a8ce9086094e8f85b8e54a6a378b1e5259d967b8a).

## What was built

Three Zag files, concatenated to `l3_full.zag`, compiled with the pinned
znc to `l3_bin`:

- `learner.zag`: generic machinery + learned state only. X (episode
  recall: id -> 4 readings), Y (threshold decide: scalar -> stay/leave,
  threshold learned from scalar experience), a register-machine program
  executor (R0..R3 preloaded; ops 0=CPY 1=ADD 2=SUB 3=MAX 4=MIN; output
  R0), greedy program construction from labeled episodes (80 candidates
  per round, strictly positive gain, first-max ties, 8-instruction cap),
  threshold refit, and a generic `adapt()` policy: keep if perfect,
  else refit threshold, else extend the program via construction, else
  HONESTFAIL. No episode data, no world rules, no aggregation solution.
- `world.zag`: experiment side only (the learner never calls it).
  Episode tables, the three hidden labeling rules (phase 1: rich iff
  e0+e2 >= 10; phase 2: rich iff e0+e2 >= 14; phase 3: rich iff
  e0+e2+e3 >= 16), and five menu aggregations as controls (SUM, MAX,
  MIN, FIRST, LAST).
- `driver.zag`: teaches X/Y, runs construction/adaptation, evaluates
  the five arms and three phases, prints the kill-bar summary. Output
  goes through one preallocated buffer and a single raw-syscall write.

## The creation trace (K-L3-3)

Phase 1, construction from the empty program on 8 labeled episodes:

```
C-ROUND 1 base=5 eval=80 win=1,0,2 gain=3 score=8 t=10
C-ROUND 2 base=8 eval=80 stop
M-BUILT n=1 t=10 score=8/8
M-STATE n=1 gen=1 sup=0 t=10 prog=1,0,2,...
```

The learner evaluated 80 single-instruction candidates; `ADD R0,R2`
(op=1,d=0,s=2) was the unique 8/8 candidate (gain 3 over the 5/8
baseline). Rejected alternatives probed by the driver: CPY-R0-R2 7/8,
ADD-R0-R1 5/8, ADD-R0-R3 6/8, MAX-R0-R2 6/8, MIN-R0-R2 6/8,
SUB-R0-R2 4/8. The final form (add readings 0 and 2) appears nowhere in
the learner source (K-L3-2 grep audit: 0 hits on all 8 frozen patterns,
including the solution expression, episode data, and any mode/bridge
token). It is source-underdetermined and history-determined: the same
machinery builds a different intermediate from phase-3 history (below).

## Kill bars

- K-L3-1 (insufficiency): ARM-X-ONLY 0/4 (sequences, no decision
  procedure; every decision NO_DECISION), ARM-Y-ONLY 0/4 (decision
  procedure, no perceptual input), ARM-FULL 4/4. PASS=1.
- K-L3-2 (no enumerated solution): frozen grep audit on `learner.zag`,
  0 hits on all 8 patterns. PASS.
- K-L3-3 (creation): trace above; non-empty program, 8/8 on train.
  PASS=1.
- K-L3-4 (causal necessity): ARM-FULL 4/4, ARM-NO-M (M slot wiped) 0/4.
  Removing M restores the X/Y type gap: no scalar reaches Y, every
  decision is NO_DECISION. PASS=1. Additionally, all five menu
  aggregations fail on test (SUM 2/4, MAX 3/4, MIN 2/4, FIRST 2/4,
  LAST 2/4), so the specifically learned M, not just any aggregation,
  is necessary. F-MENU-WIN silent.
- K-L3-5 (persistence): the 28 structural bytes of the M slot
  (n, gen, sup, pad, program) are byte-identical after phase 1 and
  phase 2 (M-PERSIST=1; see ERRATUM-1 in PREREG.md for the scope).
  PASS=1.
- K-L3-6 (reuse): phase 2 (new episodes, stricter stay criterion)
  adapt returns code 1 (threshold-only: t 10 -> 14, M program
  untouched) and held-out decisions are 2/2. PASS=1.
- K-L3-7 (determinism): 3/3 byte-identical. PASS.

## Revision (beyond the bars)

Phase 3 changes the world (rich iff e0+e2+e3 >= 16). The learner's
`adapt()` first re-evaluates M (4/8), then refits the threshold (best
7/8, fails), then extends M via construction:

```
C-ROUND 1 base=7 eval=80 win=1,0,3 gain=1 score=8 t=16
C-ROUND 2 base=8 eval=80 stop
ADAPT code=2
M-STATE  n=2 gen=2 sup=0 t=16 prog=1,0,2,1,0,3,...
MPREV-STATE n=1 gen=1 sup=1 t=14 prog=1,0,2,...
```

The revised intermediate M' = [ADD R0,R2, ADD R0,R3] extends the old
program (prefix preserved); the old M is retired to Mprev with
superseded=1, not deleted. Z on 4 new test episodes: 4/4.

## Disclosed footprint and non-claims

- The op basis {CPY,ADD,SUB,MAX,MIN} and the register machine are
  researcher-supplied generic machinery, frozen in the prereg and never
  expanded. The L3 claim is about the intermediate's form, not the
  basis. This is the same class of residual footprint as the operator
  vocabulary in the L3 bridge work.
- The hidden world rules were designed by the builder, not an
  independent adversary. Sealed-adversary generality (Micah C0-C) and
  transfer beyond this world family remain open.
- This build targets the seven composition-L3 bars; it does not claim
  Micah's full 12-criterion L3 bar.
- Two transparent prereg errata (committed before implementation):
  ERRATUM-1 clarifies K-L3-5's scope (structural bytes; the threshold
  field is Y's parameter and changes 10 -> 14 in phase 2); ERRATUM-2
  corrects the SUM train-fit threshold to t=18 (builder arithmetic
  slip; frozen tables unchanged).

## Files

- `PREREG.md`: frozen prereg + transparent amendments.
- `NAMECHECK.md`: toolchain guard, constraints, development notes.
- `REPORT.md`: this file.
- `learner.zag`, `world.zag`, `driver.zag`: sources (pure Zag).
- `l3_full.zag`: concatenated build source.
- `l3_bin`: compiled binary (build artifact).
- `l3_compile.txt`: compiler log (exit 0, 2 benign A0102 warnings).
- `l3_run1.txt`, `l3_run2.txt`, `l3_run3.txt`: byte-identical outputs.

## Verdict

COMPOSITION-L3-COMPLETE. The learner created a novel intermediate
reduction program through experience, the program is causally necessary
for Z, it persists in learner state, it is reused on a new problem with
only parametric adaptation, and it is structurally revised (not rebuilt)
when the world changes. All seven frozen kill bars pass with no
falsifier firing.
