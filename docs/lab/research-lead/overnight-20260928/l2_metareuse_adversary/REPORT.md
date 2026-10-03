# REPORT: L2-METAREUSE-ADVERSARY (sealed-world generality probe)

Worker: L2-METAREUSE-ADVERSARY subagent (depth 2/2), 2026-10-03.
Prereg: `l2_metareuse_adversary/PREREG.md`, frozen alone at
commit a62b04c67 before any implementation existed. One
transparent pre-verdict amendment: PREREG_AMENDMENT1.md
(build A Z ids 4,5,6 -> 3,4,5 and build B Z ids 4,5 ->
3,4: both builds teach three MAPs, so `map_create`
assigns from id 3; row contents, ops, tries, answers,
and t16 counts unchanged; no counting-rule or
learner-code change).

Non-ledger task (claim minting paused): this is a wave
verdict, not a ledger claim.

## Verdict

**L2-METAREUSE-ADVERSARY-PASS.** All seven sealed builds
pass their frozen bars with zero falsifiers, 3/3
byte-identical each:

- Core builds A, B, C: K1', K2', K3', K4', K5', K8'
  all PASS. All six operators (COMBINE, SUBSTITUTE,
  TRUNCATE, INVERT-A, INVERT-B, ABSTRACT, CONCRETIZE)
  fire on fresh adversary-designed families with the
  intended operator selected by verification, exact
  predicted Z rows, pipeline persistence on re-ask,
  and per-operator ablation necessity.
- Falsification builds X1-X4: XK1' boundary confirmed
  on all four (predicted graceful failure, ANS -2,
  tries=6, op=-1, t16=0, oth=0); XK2'-XK5' PASS. No
  HARNESS-SOLVED positive case occurred. All four
  mechanism decision points behave exactly as the
  adversary modeled, and every run terminates.

## What was built

Seven sealed builds, each `cat learner.zag world_*.zag
driver_*.zag > adv_*_full.zag` compiled with the pinned
znc (build exit 0; only A0102 ignored-return-value
warnings, same class as the builder lanes).
`learner.zag` is byte-identical to the builder's frozen
`l2_invert_value/learner.zag` (sha256
698be75b19e3d9a85b3b308aa4d1e645cbb4e386169bcb47d8b20dfb93877731
both files); the builder lanes were never modified
(git status clean). The drivers never name an
operator, source pair, binding, pattern, or form
(shell tag audit 0 hits on all drivers and worlds);
queries are (start,terminal,value,cap,dom) with one
arm-level OP_MASK.

Fresh ids throughout (rels 4,21-29,31-37, never the
builder's 2,5,6,7,8,9,11,12,15,16,17,18,19,38).

## Kill-bar results

### Build A (ops 1-3, fresh family; 3 taught MAPs)

FULL: QA via=1 val=51; QB via=2 val=-1;
Q1 (40,47,53): op=1 tries=1 via=3 val=53;
Q2 (50,55,54): op=2 tries=2 via=4 val=54;
Q3 (20,23,55): op=3 tries=3 via=5 val=55.
Z rows exact: Z1=3(1,7,40,47,2,1,0,0,0,0,4,0)
rels[24,24,21,22,23,22,23] facts[9,10,11,12,13,14,15];
Z2=4(1,5,50,55,1,1,25,26,27,2,4,0)
rels[25,26,27,26,27] facts[17,18,19,20,21];
Z3=5(1,3,20,23,1,1,21,22,23,1,4,0)
rels[21,22,23] facts[1,2,3].
Re-asks via 3/4/5, entered=0. t16=4:
(3,1),(3,2),(4,1),(5,1); LINK14 to 3,4,5; mD' live.
Ablations: COMBINE-out: Q1=-2, Q2=54, Q3=55, t16=2;
SUBST-out: 53,-2,55, t16=3; TRUNC-out: 53,54,-2,
t16=3. NOREUSE/FRESH: all -2, t16=0.
K1'-K5',K8' PASS, 0 falsifiers. as=297/431/200
ae=2/2/2 (informational).

### Build B (op 4 both forms; 3 taught MAPs)

FULL: Q4A (60,65,56): op=4 tries=4 via=3 val=56.
Form B tried first: MR-INVVAL-LOOKUP t*=65
srcend=25 -> MR-INVVAL-FAIL (strict terminal
check); Form A strict walk of reversed
[23,22,23,22,21] 60->65, MR-INV-OK.
Z4a=3(1,5,60,65,1,1,23,22,23,2,4,0)
rels[23,22,23,22,21] facts[9,10,11,12,13].
Q4B (57,20,57): op=4 tries=4 via=4 val=57.
Form B: lookup finds (25,4,57), tstar=25 ==
source end, backward walk 25->20, MR-INVVAL-OK;
Form A never attempted. Z4b=4(1,6,57,20,1,1,
4,23,22,2,4,1) rels[4,23,22,23,22,21]
facts[15,5,4,3,2,1] (dir=1; re-ask executes
backward through the pipeline, val read from
stored fact 15's obj).
Re-asks via 3/4, entered=0. t16=2: (3,1),(4,1).
ABLATE-INV: Q4A=-2, Q4B=-2, t16=0.
K1'-K5',K8' PASS, 0 falsifiers. as=353/138
ae=2/2.

### Build C (ops 5-6; pattern mP' nf=3)

FULL: Q5 (80,86,58): op=5 tries=5 via=4 val=58.
ABSTRACT backtracks entry candidates: (80,21,81)
FAIL-SHAPE, then (80,21,82) SHAPE-OK term=86
VERIFY-OK with runtime folds (26,27).
Z5=4(1,5,80,86,1,1,21,26,27,2,4,0)
rels[21,26,27,26,27] facts[18,19,20,21,22].
Q6 (90,98,59): op=6 tries=6 via=5 val=59.
CONCRETIZE picks pattern id 3 (nf=3, read from
the pattern, not hardcoded); dead entry
(90,28,91) FAIL-SHAPE, live entry (90,29,92)
verifies with novel 3-fold (26,27) vs source
(22,23). Z6=5(1,7,90,98,1,1,29,26,27,3,4,0)
rels[29,26,27,26,27,26,27]
facts[25,26,27,28,29,30,31].
Re-asks via 4/5, entered=0. t16=2: (4,1),(5,3).
ABLATE-ABS: Q5=-2, Q6=59, t16=1; ABLATE-CONC:
Q5=58, Q6=-2, t16=1.
K1'-K5',K8' PASS, 0 falsifiers. as=500/806
ae=2/2.

### Build X1 (greedy fold discovery)

QX1 (100,106,61): val=-2, tries=6, op=-1,
t16=0, oth=0. Trace: MR-SUB-CAND r=25 u=101
then FAIL-SHAPE (first-fid decoy (101,31,102)
committed, no backtracking); all 6 ops fail,
ANS -2. XK1' boundary=1, XK2'=1, 0 falsifiers.
as=407 (informational).

### Build X2 (first-match reverse value lookup)

QX2 (57,20,57): val=-2, tries=6, op=-1, t16=0,
oth=0. Trace: MR-INVVAL-LOOKUP t*=110 srcend=25
-> MR-INVVAL-FAIL -> MR-INV-FAIL (no rel-23 hop
from 57); op6 MR-NO-PATTERN. XK1' boundary=1,
XK2'=1, 0 falsifiers. as=107.

### Build X3 (first-match pattern selection)

QX3 (90,96,59): val=-2, tries=6, op=-1, t16=0,
oth=0. Trace: MR-PATTERN-SRC id=3 (mP1', nf=3,
cannot span the 2-fold region); the fitting
mP2' (id 4, nf=2) is never considered.
XK1' boundary=1, XK2'=1, 0 falsifiers. as=831.

### Build X4 (cycle-trapped discovery)

QX4 (120,126,62): val=-2, tries=6, op=-1,
t16=0, oth=0. Trace: MR-SUB-CAND r=25 u=121
SHAPE-OK term=121 VERIFY-FAIL (2-cycle walked
twice, bounded, lands on 121 not 126). Run
terminates; no hang. XK1' boundary=1, XK2'=1,
0 falsifiers. as=580.

### Determinism and seal

3/3 byte-identical per build:
A a443ccdc2b4edc5d10207c1bce424b68024c3d89f8187d5880ec3e7b8467e151,
B f8e880474b9e69485fa741ef8f59d0a3f85720a9e7707c813a3428502dba6127,
C c5430014ead6bfad625baad4b3ffc9af36c7ab624ec5ea305fcb4a5cdf486770,
X1 3e67988207022f297917f81939fb2f452d6dc398f553e7f486c1e18601d1b35d,
X2 7c2f5741af40f234797407deb675d8fecec9ab74162bbe3366efa1df8ac954c0,
X3 e8f44e1a9564534ec587be9982558fd50c062930c9d7afe6bf326ef35ac67c74,
X4 feb422b71399602fe0f450e46dce67b217bc1781d3afd4245593e945d8f2409d.
K7'/XK5' seal: learner.zag sha256-identical to the
builder's frozen file; 0 operator/form trace tags
in any driver or world file; builder lanes
untouched.

## Findings (adversarial)

1. The six operators generalize beyond the
   builder's family: three fresh sealed families
   (different rel ids, nf=2 source, nf=3 pattern,
   prefix-reuse TRUNCATE, dual-entry ABSTRACT,
   dead/live-entry CONCRETIZE) reproduce the full
   K-bar profile, including per-operator ablation
   necessity and pipeline persistence.
2. INVERT's two forms remain mutually
   discriminating on a fresh family (Form B
   strict-terminal failure -> Form A on Q4A;
   Form B success without attempting Form A on
   Q4B).
3. Four precise boundary limitations are now
   documented with sealed evidence (all fail
   gracefully, ANS -2, no crash/hang/wrong
   answer, deterministic):
   - fold-relation discovery is greedy
     first-match with no backtracking (X1);
     a lower-fid decoy or cycle defeats it
     (X4, and it terminates);
   - reverse value lookup keeps the first
     (rel==dvr,obj==v) match, so value aliasing
     defeats the strict terminal check (X2);
   - pattern selection is first-match by MAP
     id, not best-fit: two patterns interfere
     (X3);
   - entry selection in mr_agg_seg is
     first-match (dead first entry defeats
     COMBINE/TRUNCATE b=1 on Q5/Q6, while
     ABSTRACT/CONCRETIZE backtrack their own
     candidate loops).
4. No HARNESS-SOLVED positive case: the
   adversary's mechanism model predicted all
   four X outcomes exactly.

## Disclosures and non-claims

- This is L2 evidence (operator choice by
  verification on sealed worlds), not L3: the
  operator menu and INVERT forms remain
  researcher-supplied.
- Three fresh core families plus four probes do
  not certify the operators against all
  worlds; scaling, transfer, the protected
  core, and the continuing learner are out of
  scope.
- as/ae tick counts were informational only,
  never bars; determinism rests on 3/3
  byte-identical runs.
- One implementation bug was caught by the
  xk2 bar pre-verdict and fixed: driver_X3's QA
  used terminal 25 while X3's mA' ends at 27
  (PREREG world spec authoritative); corrected
  to (20,27,51) before the final runs. No
  prereg prediction changed.
- 0 modes, 0 bridges, 0 handlers, 0 new edge
  types, 0 new opcodes, 0 semantic cases. Pure
  Zag, safebin toolchain, zero forbidden
  executables (Step 0 verified at startup).
- No em/en dashes in loop documentation.
  Commits local with explicit pathspecs;
  nothing pushed.

## Files

- `NAMECHECK.md` (Step 0 toolchain guard),
  `PREREG.md` (frozen alone at a62b04c67),
  `PREREG_AMENDMENT1.md` (pre-verdict Z-id
  correction, committed at d0f04fe02),
  `REPORT.md` (this file)
- `learner.zag` (byte-identical copy of the
  builder's frozen learner)
- `world_A/B/C/X1/X2/X3/X4.zag`,
  `driver_A/B/C/X1/X2/X3/X4.zag`,
  `adv_A/B/C/X1/X2/X3/X4_full.zag`,
  `adv_A/B/C/X1/X2/X3/X4_bin`,
  `adv_A/B/C/X1/X2/X3/X4_compile.txt`,
  `adv_A/B/C/X1/X2/X3/X4_run{1,2,3}.txt`
