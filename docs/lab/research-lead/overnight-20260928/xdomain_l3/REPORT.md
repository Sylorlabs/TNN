# REPORT: Cross-Domain Grammar to Program L3 Novel Intermediate (COMPILE)

Verdict: **XDOMAIN-L3-COMPLETE** (all seven frozen kill bars pass,
no falsifier fires).

Date: 2026-10-02. Worker: Cross-Domain L3 Worker.
Prereg: `PREREG.md` (frozen f54a1214a; transparent amendment a6b02f69b,
re-frozen before the implementation commit). Determinism: 3/3
byte-identical runs (sha256
4b58e7e5acc8352d827d3c33589a7e3564e12a0af198be7716c48520cdaf01ac).

## What was built

Four Zag files, concatenated to `xg_full.zag`, compiled with the pinned
znc to `xg_bin`:

- `learner.zag`: byte-identical copy of
  `composition_l3/learner.zag` (sha256
  9317f63c0a72263a533ef9a54b12eed7535dc71a0b202e0c9b14b247fce08e7b
  for both; never modified). Generic machinery + learned state only:
  X (grammar production recall: rule id -> 4 opcode-weight symbols),
  Y (program fuel gate: scalar -> RUN-OK/FAIL, threshold learned from
  scalar fuel experience), a register-machine program executor
  (R0..R3 preloaded, R0 output; ops 0=CPY 1=ADD 2=SUB 3=MAX 4=MIN),
  greedy program construction from labeled rule experience (80
  candidates per round, strictly positive gain, first-max ties,
  8-instruction cap), threshold refit, and a generic `adapt()` policy:
  keep if perfect, else refit threshold, else extend the program via
  construction, else HONESTFAIL. No production data, no world rules,
  no reduction solution.
- `world.zag`: experiment side only (the learner never calls it).
  Grammar production tables, the three hidden program-run rules
  (phase 1: RUN-OK iff e0+e3 >= 10; phase 2: e0+e3 >= 14; phase 3:
  e0+e2+e3 >= 16), and five menu reductions as controls (SUM, MAX,
  MIN, FIRST, LAST).
- `driver.zag`: teaches X/Y, runs construction/adaptation, evaluates
  the five arms and three phases, prints the kill-bar summary. Output
  goes through one preallocated buffer and a single raw-syscall write.

## The creation trace (K-XD-3)

Phase 1, construction from the empty program on 8 labeled rules:

```
C-ROUND 1 base=5 eval=80 win=1,0,3 gain=3 score=8 t=10
C-ROUND 2 base=8 eval=80 stop
M-BUILT n=1 t=10 score=8/8
M-STATE n=1 gen=1 sup=0 t=10 prog=1,0,3,...
```

The learner evaluated 80 single-instruction candidates; `ADD R0,R3`
(op=1,d=0,s=3) was the unique 8/8 candidate (gain 3 over the 5/8
baseline; CPY R0,R3 reached 7/8, gain 2). Rejected alternatives probed
by the driver: CPY-R0-R3 7/8, ADD-R0-R1 5/8, ADD-R0-R2 6/8,
MAX-R0-R3 6/8, MIN-R0-R2 6/8, SUB-R0-R3 4/8. The final form (add
symbols 0 and 3) appears nowhere in the learner source (K-XD-2 grep
audit: 0 hits on all 7 frozen patterns, including the solution
expression, production data, and any mode/bridge token). It is
source-underdetermined and history-determined: the same frozen source
builds [ADD R0,R2] on FORAGE's world and [ADD R0,R3] here.

## Kill bars

- K-XD-1 (insufficiency): ARM-X-ONLY 0/4 (productions, no program
  procedure; every decision NO_DECISION), ARM-Y-ONLY 0/4 (fuel gate,
  no grammar input), ARM-FULL 4/4. PASS=1.
- K-XD-2 (no enumerated solution): frozen grep audit on `learner.zag`,
  0 hits on all 7 patterns. PASS.
- K-XD-3 (creation): trace above; non-empty program (bytes 1,0,3),
  8/8 on train. PASS=1.
- K-XD-4 (causal necessity): ARM-FULL 4/4, ARM-NO-M (M slot wiped)
  0/4. Removing M restores the X/Y type gap: no scalar reaches Y,
  every decision is NO_DECISION. PASS=1. Additionally, all five menu
  reductions fail on test (SUM 2/4, MAX 3/4, MIN 2/4, FIRST 2/4,
  LAST 3/4), so the specifically learned M, not just any reduction,
  is necessary. F-MENU-WIN silent.
- K-XD-5 (persistence): the 28 structural bytes of the M slot
  (n, gen, sup, pad, program) are byte-identical after phase 1 and
  phase 2 (M-PERSIST=1; the threshold field is Y's parameter and
  changes 10 -> 14, excluded per the prereg). PASS=1.
- K-XD-6 (reuse): phase 2 (new rules, stricter fuel criterion)
  adapt returns code 1 (threshold-only: t 10 -> 14, M program
  untouched) and held-out decisions are 2/2. PASS=1.
- K-XD-7 (determinism): 3/3 byte-identical. PASS.

## Revision (beyond the bars)

Phase 3 changes the world (RUN-OK iff e0+e2+e3 >= 16). The learner's
`adapt()` first re-evaluates M (4/8), then refits the threshold (best
7/8 at t=10, fails), then extends M via construction:

```
C-ROUND 1 base=7 eval=80 win=1,0,2 gain=1 score=8 t=16
C-ROUND 2 base=8 eval=80 stop
ADAPT code=2
M-STATE  n=2 gen=2 sup=0 t=16 prog=1,0,3,1,0,2,...
MPREV-STATE n=1 gen=1 sup=1 t=14 prog=1,0,3,...
```

The revised intermediate M' = [ADD R0,R3, ADD R0,R2] extends the old
program (prefix preserved); the old M is retired to Mprev with
superseded=1, not deleted. Z on 4 new test rules: 4/4.

## The amendment, honestly

The original freeze expected M = [ADD R1,R3] for a rule on e1+e3.
The first full run, before any implementation commit, showed this
expectation is unimplementable in the frozen register machine: the
executor always outputs R0, so a d != 0 instruction cannot affect the
output. The learner itself was sound (it found a 3-instruction 8/8
program); the builder's hand-derivation was wrong. Rather than rescue
the result, the prereg was transparently amended (AMENDMENT-1): the
production tables swap the e2/e3 columns, TRUE1 is RUN-OK iff
e0+e3 >= 10, and the expected intermediate is M = [ADD R0,R3].
The amendment was committed as a PREREG.md-only commit (a6b02f69b)
before the implementation commit. All expectations were re-derived
for the swapped tables; the implementation reproduces every one
exactly (construction winner and gains, menu fits, adapt codes,
thresholds, revision winner).

## Cross-domain reading

The same frozen `learner.zag` that invented [ADD R0,R2] for FORAGE's
foraging world invented [ADD R0,R3] for COMPILE's grammar-to-program
world, and revised it to [ADD R0,R3, ADD R0,R2] when this world's rule
changed (versus FORAGE's [ADD R0,R2, ADD R0,R3]). No source byte
differs between the two learners. The intermediate's form is
world-determined, not machinery-determined: this is the L3 evidence
for the cross-domain question.

## Disclosed footprint and non-claims

- The op basis {CPY,ADD,SUB,MAX,MIN}, the register machine, the greedy
  search, and the adapt() policy are researcher-supplied generic
  machinery, frozen in the prereg and never expanded. The L3 claim is
  about the intermediate's form, not the basis. Reusing learner.zag
  verbatim is the experimental design, not a shortcut.
- The hidden world rules were designed by the builder, not an
  independent adversary. Sealed-adversary generality (Micah C0-C) and
  transfer beyond this world family remain open.
- This build targets the seven xdomain-L3 bars; it does not claim
  Micah's full 12-criterion L3 bar.
- One transparent prereg amendment (AMENDMENT-1), re-frozen before
  implementation. No bar was weakened to force a pass.

## Files

- `PREREG.md`: frozen prereg + transparent amendment.
- `NAMECHECK.md`: toolchain guard, constraints, development notes.
- `REPORT.md`: this file.
- `learner.zag`: verbatim copy of composition_l3/learner.zag (never
  modified; sha256-identical).
- `world.zag`, `driver.zag`: sources (pure Zag).
- `xg_full.zag`: concatenated build source.
- `xg_bin`: compiled binary (build artifact).
- `xg_compile.txt`: compiler log (exit 0, 2 benign A0102 warnings,
  same class as FORAGE).
- `xg_run1.txt`, `xg_run2.txt`, `xg_run3.txt`: byte-identical outputs.

## Digests

- xg_bin:
  d24c5e9109990005b34e8eac56695cdf54bac50a58bbc8381881a111aaf85d69
- xg_run1/2/3.txt:
  4b58e7e5acc8352d827d3c33589a7e3564e12a0af198be7716c48520cdaf01ac
  (identical all three; cmp clean both pairs)

## Verdict

XDOMAIN-L3-COMPLETE. The learner created a novel intermediate
reduction program bridging grammar productions and program fuel
through experience, the program is causally necessary for Z, it
persists in learner state, it is reused on a new problem with only
parametric adaptation, and it is structurally revised (not rebuilt)
when the world changes. The same frozen learner invents a different
intermediate for this domain pair than for FORAGE. All seven frozen
kill bars pass with no falsifier firing.

Constraints honored: pure Zag; zero Python; safebin mandatory (36
tools, no python3/python); no em/en dashes in loop documentation;
paper untouched; nothing pushed (commits local on tnn-native-lab);
0 modes/bridges/handlers.
