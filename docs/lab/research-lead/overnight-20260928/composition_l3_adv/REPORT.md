# REPORT: Composition L3 Adversarial World (RELAY)

Verdict: **COMPOSITION-L3-ADV-COMPLETE** (all seven frozen kill bars
pass, no falsifier fires).

Date: 2026-10-02. Worker: Composition L3 Red-Team Worker (independent
adversary relative to the FORAGE builder).
Prereg: `PREREG.md` (frozen 10389d72e; committed alone before any
implementation existed; zero amendments). Determinism: 3/3
byte-identical runs (sha256
f9910fc7b05cfed128456a6fe906b045d7ff0715ae7c9ddb91a41208f849b182).

## What was built

Four Zag files, concatenated to `relay_full.zag`, compiled with the
pinned znc to `relay_bin`:

- `learner.zag`: byte-identical copy of the FORAGE mechanism
  (sha256 9317f63c0a72263a533ef9a54b12eed7535dc71a0b202e0c9b14b247fce08e7b,
  verified before and after the build). Generic machinery + learned
  state only: X episode recall, Y threshold decide, register-machine
  program executor (ops 0=CPY 1=ADD 2=SUB 3=MAX 4=MIN), greedy program
  construction, threshold refit, generic adapt() policy (codes 0/1/2/3),
  decide() with -1 NO_DECISION. UNMODIFIED.
- `world.zag`: new adversary-designed RELAY environment (experiment side
  only; the learner never calls it). Difference-based hidden rules:
  phase 1 open iff e0-e1 >= 4; phase 2 open iff e0-e1 >= 6; phase 3 open
  iff e0-e1+e3 >= 8. New episode tables (section 3 of PREREG.md) and the
  same five menu aggregations as controls (SUM, MAX, MIN, FIRST, LAST).
- `driver.zag`: new experiment-side driver for RELAY. Teaches X/Y, runs
  the learner's construct/adapt, evaluates the six arms and three
  phases, prints the kill-bar summary. It never invents the
  intermediate: all construction goes through the unmodified
  learner.zag. Output goes through one preallocated buffer and a single
  raw-syscall write.

## The creation trace (K-ADV-3)

Phase 1, construction from the empty program on 8 labeled episodes:

```
C-ROUND 1 base=6 eval=80 win=2,0,1 gain=2 score=8 t=3
C-ROUND 2 base=8 eval=80 stop
M-BUILT n=1 t=3 score=8/8
M-STATE n=1 gen=1 sup=0 t=3 prog=2,0,1,...
```

The learner evaluated 80 single-instruction candidates; `SUB R0,R1`
(op=2,d=0,s=2 -> bytes 2,0,1) was the unique 8/8 candidate (gain 2 over
the 6/8 empty-program baseline at t=4). Rejected alternatives probed by
the driver on phase-1 train: FORAGE-ADD-R0-R2 5/8 t=12, SUB-R0-R3 5/8
t=0, MAX-R0-R3 4/8 t=0, MIN-R0-R2 5/8 t=1, ADD-R0-R3 4/8 t=0,
CPY-R0-R1 4/8 t=0. The final form (subtract reading 1 from reading 0)
appears nowhere in the learner source (K-ADV-2 grep audit: 0 hits on
all 8 frozen patterns, including the solution expression, both solution
instructions, episode data, and any mode/bridge token). It is
source-underdetermined and history-determined: the same byte-identical
machinery built `ADD R0,R2` from FORAGE history and `SUB R0,R1` from
RELAY history.

## Anti-transfer result (adversarial question 4)

The FORAGE intermediate [ADD R0,R2] evaluated on RELAY phase-1 train
scores 5/8 (t=12); on RELAY phase-1 test it scores 3/4. The RELAY
intermediate [SUB R0,R1] is a different op on a different register, and
the FORAGE solution does not solve this world. F-FORAGE-REUSE silent.
The learner avoided the FORAGE-specific solution because experience,
not source, selected the program.

## Kill bars

- K-ADV-1 (insufficiency): ARM-X-ONLY 0/4 (sequences, no decision
  procedure; every decision NO_DECISION), ARM-Y-ONLY 0/4 (decision
  procedure, no perceptual input), ARM-FULL 4/4. PASS=1.
- K-ADV-2 (no enumerated solution): frozen grep audit on the copied
  `learner.zag`, 0 hits on all 8 patterns; sha256 equals the frozen
  FORAGE learner hash. PASS.
- K-ADV-3 (creation): trace above; non-empty program, not the FORAGE
  bytes (1,0,2), 8/8 on train. PASS=1.
- K-ADV-4 (causal necessity): ARM-FULL 4/4, ARM-NO-M (M slot wiped)
  0/4. Removing M restores the X/Y type gap: no scalar reaches Y, every
  decision is NO_DECISION. PASS=1. Additionally, all five menu
  aggregations fail on test (SUM 2/4, MAX 2/4, MIN 2/4, FIRST 2/4,
  LAST 1/4), so the specifically learned M, not just any aggregation,
  is necessary. F-MENU-WIN silent.
- K-ADV-5 (persistence): the 28 structural bytes of the M slot
  (n, gen, sup, pad, program; threshold field excluded per the carried
  ERRATUM-1 rationale) are byte-identical after phase 1 and phase 2
  (M-PERSIST=1). PASS=1.
- K-ADV-6 (reuse): phase 2 (new episodes, stricter margin) adapt returns
  code 1 (threshold-only: t 3 -> 5, M program untouched) and held-out
  decisions are 2/2. PASS=1.
- K-ADV-7 (determinism): 3/3 byte-identical. PASS.

## Revision (beyond the bars)

Phase 3 changes the world (open iff e0-e1+e3 >= 8). The learner's
`adapt()` first re-evaluates M (5/8 at t=5), then refits the threshold
(best 5/8 at t=2, fails), then extends M via construction:

```
C-ROUND 1 base=5 eval=80 win=1,0,3 gain=3 score=8 t=8
C-ROUND 2 base=8 eval=80 stop
ADAPT code=2
M-STATE  n=2 gen=2 sup=0 t=8 prog=2,0,1,1,0,3,...
MPREV-STATE n=1 gen=1 sup=1 t=5 prog=2,0,1,...
```

The revised intermediate M' = [SUB R0,R1, ADD R0,R3] extends the old
program (prefix preserved); the old M is retired to Mprev with
superseded=1, not deleted. Z on 4 new test episodes: 4/4. The revision
instruction (ADD R0,R3) was also absent from the learner source
(K-ADV-2 pattern 3, 0 hits).

## Disclosed footprint and non-claims

- The op basis {CPY,ADD,SUB,MAX,MIN} and the register machine are
  researcher-supplied generic machinery, byte-identical to the FORAGE
  build, never expanded. The L3 claim is about the intermediate's form,
  not the basis.
- The hidden RELAY rules were designed by the red-team worker as an
  independent adversary (no input from the FORAGE builder), sealed in
  the prereg before implementation. This closes the FORAGE honest
  boundary for one additional world family; it does not establish broad
  generality, and transfer beyond RELAY remains open.
- This build targets the seven composition-L3 bars; it does not claim
  Micah's full 12-criterion L3 bar.
- Zero prereg amendments were needed: every frozen hand-derived
  expectation reproduced exactly on the first build.

## Files

- `PREREG.md`: frozen prereg (commit 10389d72e, alone).
- `NAMECHECK.md`: toolchain guard, constraints, development notes.
- `REPORT.md`: this file.
- `learner.zag`: byte-identical FORAGE mechanism (frozen, unmodified).
- `world.zag`, `driver.zag`: new RELAY experiment-side sources (pure Zag).
- `relay_full.zag`: concatenated build source.
- `relay_bin`: compiled binary (build artifact).
- `relay_compile.txt`: compiler log (exit 0, 2 benign A0102 warnings,
  same class as the FORAGE build).
- `relay_run1.txt`, `relay_run2.txt`, `relay_run3.txt`: byte-identical
  outputs (144 lines, 0 NUL bytes, ends with L3-RELAY-END).

## Verdict

COMPOSITION-L3-ADV-COMPLETE. On a sealed adversary-designed world whose
hidden rule demands a different structure, the unmodified L3 mechanism
constructed a novel intermediate (`SUB R0,R1`, not the FORAGE
`ADD R0,R2`), the FORAGE solution demonstrably fails on this world, the
program is causally necessary for Z, it persists in learner state, it is
reused on a new problem with only parametric adaptation, and it is
structurally revised (not rebuilt) when the world changes. All seven
frozen kill bars pass with no falsifier firing.
