# REPORT: Cross-Domain Causal to Intervention L3 Novel Intermediate (INTERVENE)

Worker: Causal L3 Worker (subagent, 2026-10-02).
Prereg: `xdomain_causal_l3/PREREG.md`, frozen alone at commit e53775073
before any implementation file existed. No amendments were needed:
the first full run reproduced every hand-derived expectation, so the
frozen prereg stands unamended.

## Verdict: XDOMAIN-CAUSAL-L3-COMPLETE

All seven kill bars PASS with no falsifier firing. 3/3 runs
byte-identical.

## 1. What was tested

Whether the SAME generic learner machinery that constructed a novel
intermediate for sequence to scalar (FORAGE, M = [ADD R0,R2]) and for
grammar to program (COMPILE, M = [ADD R0,R3]) constructs a DIFFERENT
novel intermediate for causal observation to intervention, where a
causal model X (scenario recall, outputs a sequence) and an
intervention gate Y (scalar strength to ACT/SKIP) are jointly
insufficient for the goal Z (decide ACT/SKIP on new scenarios).
`learner.zag` is a byte-identical copy of
`composition_l3/learner.zag` (sha256
9317f63c0a72263a533ef9a54b12eed7535dc71a0b202e0c9b14b247fce08e7b),
copied with cp, never edited.

## 2. Kill bar results

| Bar | Requirement | Observed | Result |
|-----|-------------|----------|--------|
| K-XC-1 insufficiency | X-ONLY 0/4, Y-ONLY 0/4, FULL 4/4 | 0/4, 0/4, 4/4 | PASS |
| K-XC-2 novelty | 8 frozen grep patterns, 0 hits on learner.zag | all 0 | PASS |
| K-XC-3 creation trace | positive-gain round, non-empty program, 8/8 train, bytes (1,0,1) | C-ROUND 1 base=7 eval=80 win=1,0,1 gain=1 score=8 t=11; M-BUILT n=1 t=11 8/8; prog=1,0,1 | PASS |
| K-XC-4 necessity | FULL 4/4, NO-M 0/4 | 4/4, 0/4 | PASS |
| K-XC-5 persistence | 28 structural M bytes identical phase 1 to phase 2 | M-PERSIST 1 | PASS |
| K-XC-6 reuse | phase-2 adapt code 1, held-out 2/2 | code=1, Z-HELD 2/2 | PASS |
| K-XC-7 determinism | 3 runs byte-identical | sha256 1a7c9915...f7cf7d0 x3, cmp clean | PASS |

Revision (reported, not a bar): phase-3 adapt code=2,
M' = [ADD R0,R1, ADD R0,R2] (prog bytes 1,0,1,1,0,2), t=18, Z-REV
4/4, old M retired to Mprev with superseded=1.

## 3. Key evidence (from xc_run1.txt)

- Construction: `C-ROUND 1 base=7 eval=80 win=1,0,1 gain=1 score=8
  t=11`, then `C-ROUND 2 base=8 eval=80 stop`. The invented
  intermediate is M = [ADD R0,R1], program bytes (1,0,1): the sum of
  the two causal-antecedent readings. Rejected single-instruction
  alternatives probed by the driver: CPY-R0-R1 5/8, ADD-R0-R0 7/8,
  MAX-R0-R1 6/8, MIN-R0-R1 6/8, SUB-R0-R1 6/8, ADD-R0-R2 6/8.
- Insufficiency arms: Z-FULL 4/4, Z-XONLY 0/4 (all NO_DECISION),
  Z-YONLY 0/4 (all NO_DECISION).
- Menu controls (train-fit thresholds, first-max ascending): SUM
  t=16 7/8 train, 3/4 test (miss on 11); MAX t=6 5/8 train, 2/4 test;
  MIN t=0 4/8 train, 2/4 test; FIRST t=6 7/8 train, 2/4 test; LAST
  t=0 4/8 train, 2/4 test. No menu control reaches 4/4 (F-MENU-WIN
  silent).
- Necessity: Z-NOM 0/4 with the M slot wiped; the X/Y type gap
  returns and Z fails.
- Reuse: phase-2 ADAPT code=1 (threshold-only refit 11 -> 16, M
  program untouched), M-PERSIST 1, Z-HELD 2/2.
- Revision: phase-3 `C-ROUND 1 base=6 eval=80 win=1,0,2 gain=2
  score=8 t=18` (nearest rivals CPY R0,R2 and MIN R0,R2 at 7/8,
  gain 1), ADAPT code=2, M' n=2 gen=2 t=18, MPREV n=1 gen=1 sup=1,
  Z-REV 4/4.
- Determinism: xc_run1/2/3.txt sha256 identical
  (1a7c99158a8a347b439cd0a268acfeba8eb80cbbfdf5031f730e9c3f1c7cf7d0),
  cmp clean on both pairs. No RNG anywhere; fixed candidate order,
  first-max tie-breaking, ascending threshold sweeps; output via one
  preallocated 64KB buffer and a single raw-syscall write loop.

## 4. Cross-domain evidence

Three distinct invented intermediates from the same frozen learner
source (sha256 identical across all three builds):
- FORAGE (sequence to scalar): [ADD R0,R2], bytes (1,0,2)
- COMPILE (grammar to program): [ADD R0,R3], bytes (1,0,3)
- INTERVENE (causal to intervention): [ADD R0,R1], bytes (1,0,1)

The intermediate's form is history-determined (it tracks each
world's hidden rule: e0+e2, e0+e3, e0+e1 respectively), not
source-determined. Phase-3 revisions likewise differ:
[1,0,2,1,0,3], [1,0,3,1,0,2], [1,0,1,1,0,2].

## 5. Falsifiers

None fired. F-NO-CREATE, F-MENU-WIN, F-ABLATE-FAIL,
F-NOT-NECESSARY, F-NO-PERSIST, F-NO-REUSE, F-NO-REVISE, F-OP-EXPAND,
F-AUDIT, F-NONDET, F-PYTHON all silent. The op basis was never
expanded (learner.zag byte-identical to the frozen source). Zero
python invocations in the worker process tree.

## 6. Residual footprint and non-claims

- The op basis {CPY,ADD,SUB,MAX,MIN}, the register machine, the
  greedy search, and the adapt() policy are researcher-supplied
  generic machinery, frozen and shared with the FORAGE and COMPILE
  builds. The L3 claim is about the intermediate's form being
  source-underdetermined and history-determined for a third domain
  pair, not about the basis.
- The hidden world rules were designed by the builder, not an
  independent adversary. Sealed-adversary generality (Micah C0-C) is
  open future work.
- One world family (causal observation to intervention strength).
  No generality claim beyond the demonstrated phases.
- This build targets the seven xdomain-causal-L3 bars. It does not
  claim Micah's full 12-criterion L3 bar.

## 7. Reproduction

```
cd docs/lab/research-lead/overnight-20260928/xdomain_causal_l3
cat learner.zag world.zag driver.zag > xc_full.zag
<repo>/src/tools/toolchain/znc_linux_x86_64_abed8aa1 xc_full.zag -o xc_bin
./xc_bin > xc_run1.txt
```

Pure Zag throughout. 0 modes, 0 bridges, 0 handlers, 0 new semantic
cases. Paper untouched. Nothing pushed; commits local on
tnn-native-lab.

## 8. Files

- NAMECHECK.md (toolchain guard, constraints, notes)
- PREREG.md (frozen kill bars, commit e53775073)
- learner.zag (byte-identical copy of composition_l3/learner.zag)
- world.zag (INTERVENE environment, experiment side only)
- driver.zag (arms, phases, kill-bar evaluation)
- xc_full.zag (concatenated build input)
- xc_compile.txt (znc build log, exit 0, 2 benign A0102 warnings)
- xc_bin (native binary)
- xc_run1.txt, xc_run2.txt, xc_run3.txt (3/3 byte-identical outputs)
