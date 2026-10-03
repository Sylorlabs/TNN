# REPORT: L2-COMPOSE-CHAIN4 (4-operator chain probe)

Worker: L2-COMPOSE-CHAIN4 subagent (depth 2/2), 2026-10-03.
Prereg: `l2_compose_chain4/PREREG.md`, frozen alone at
commit 3fcc63b68 before any implementation existed. No
amendments: all frozen predictions held on first build.

Non-ledger task (claim minting paused): this is a wave
verdict, not a ledger claim.

## Verdict

**L2-COMPOSE-CHAIN4-PASS.** All frozen bars hold with
zero falsifiers, 3/3 byte-identical per binary:

- Build F: F-K1 through F-K8 all PASS, including the
  QD4 4-chain signature (op=4, tries=22, dec=1, via=6,
  val=65, Z7-exact=1: INVERT Form B fired on the
  phase-2-built Z6 after 6 failed phase-1 tries, 6
  failed phase-2 tries on Z4, and 6 failed phase-2
  tries on Z5) and the QD5 bounded-termination
  signature (tries=30, val=-2, no new Z, run
  terminates with four live Z sources).
- Control F-K7: the frozen learner on the identical
  world solves QD1 (op=6, tries=6, via=3, val=59) but
  fails QD2/QD3/QD4/QD5 (-2, tries=6, op=-1), proving
  the 4-chain is what solves QD4.
- Ablations discriminate: ABLATE-INV (mask 55, op4
  masked) fails QD3 (tries=15, -2) AND QD4 (tries=15,
  -2): op4 is necessary for the third and fourth
  links. ABLATE-ABS (mask 47) reroutes: QD2 composes
  via phase-2 CONCRETIZE on Z4 (op=6, tries=10), QD3
  still completes via op4 Form A on the rerouted Z5
  (op=4, tries=14, val=65), and QD4 completes via
  op4 Form B on Z6 (op=4, tries=19, val=65, Z7
  built): the 4-chain survives the reroute with
  correct provenance (6,5,16).

## What was built (and what was deliberately NOT built)

The learner is BYTE-IDENTICAL to chain3's learner.zag
(sha256
6e8ed1e047e9dee8311a264aaec9a995ddbb723f5b284e21c18baa0e68038ddd,
verified at copy time). The WORLD is BYTE-IDENTICAL
to chain3's world_E.zag (44 facts, sha256
9197c57320515f2a186a9bb752cc74ff7a46b27b4240ac1c4be3b7e5b6be58a2,
verified at copy time). Zero source changes to
either: not one line, not one comment, not one fact.
This is the strongest test form for the task's
question: the frozen phase-2 mechanism was asked to
compose 4-deep with no help, on the exact world where
it composed 3-deep.

New files: driver_F.zag, driver_Fctl.zag.
`learner_frozen.zag` is byte-identical to chain3's
frozen learner (sha256
698be75b19e3d9a85b3b308aa4d1e645cbb4e386169bcb47d8b20dfb93877731).
Builds: `cat learner.zag world_F.zag driver_F.zag >
comp_F_full.zag`, `cat learner_frozen.zag world_F.zag
driver_Fctl.zag > ctl_F_full.zag`, pinned znc, exit 0,
warnings only (same classes as the chain3 builds).

The drivers never name an operator, source pair,
binding, pattern, or form (F-SEAL-F shell tag audit
0 hits on all three files); queries are
(start,terminal,value,cap,dom) with one arm-level
OP_MASK. No new rel ids.

## Answers to the task's questions

**Q1: 4-operator chains? YES.** The [6,5,4,4] chain:
QD1 fires CONCRETIZE (phase 1) and banks Z4 id 3;
QD2, unsolvable by any single operator on the taught
source, fires ABSTRACT (op5) on Z4 in phase 2 and
banks Z5 id 4; QD3, unsolvable by 1 operator (phase 1:
all 6 fail) AND unsolvable by 2 operators (phase 2 on
Z4: all 6 fail), fires INVERT (op4) Form A on Z5 in
phase 2 and banks Z6 id 5; QD4=(65,160,65),
unsolvable by 1 operator (phase 1: all 6 fail, no
sub-65 facts), unsolvable by 2 (phase 2 on Z4: all 6
fail, tstar=167 != 97), unsolvable by 3 (phase 2 on
Z5: all 6 fail, tstar=167 != 148), fires INVERT
(op4) Form B on Z6 in phase 2 and banks Z7 id 6
(dir=1), answering 65. The trace signature:
MR-COP-TRY 1/2/3 FAIL on Z6, MR-SRC-INV id=5,
MR-INVVAL-LOOKUP t*=167 srcend=167,
MR-INVVAL-WALK key=160, MR-INVVAL-OK, MR-ZBUILD
rels=4,29,22,23,22,23,22,23
facts=38,37,36,35,34,33,32,31, MR-VERIFY term=160 OK,
MR-PROMOTE z=6 t16=6->5, ANS term=160 val=65 via=6.
tries=22 is itself the discriminator: 6 phase-1 + 6
Z4 + 6 Z5 failures precede the single success, so a
<=3-chain solution would have shown tries<=18
(F-CHAIN3).

**Q2: fixed enumeration suffices; within-query
chaining NOT needed.** The unchanged phase-2 (fixed
[1..6] enumeration retried over ZSRC_IDS) composes
4-deep with zero learner changes and zero world
changes. The 4-chain emerges across four queries,
each step independently gated by full execution
verification. F-NO-INTRA shell audit: `MR-COMP-SRC
id=6` (Z7) occurs exactly once in the FULL arm, at
line 578, after QD4's ANS (line 398), inside QD5's
phase-2 block, never inside QD4: per T2, the Z built
during QD4's phase 2 is recorded for future queries
but never tried within QD4. T2 holds empirically,
not just by construction.

**Q3: termination holds (T1-T6) with 4 live Z
sources.** QD5 is unsolvable by design and exhausts
the full product: 6 phase-1 tries + 6 on each of
four live Z sources = 30 tries, val=-2, op=-1,
dec=0, no new Z, no hang. T1-T6 hold by construction
(unchanged code) and the QD5 signature demonstrates
them with four live Z sources, including the dir=1
Z7 as a tried-and-failed source. The bound is (6 +
6 per live Z source), linear in registry size.

## Kill-bar results (build F)

### FULL arm (mask 63)

- QA via=1 val=51 (F-K1).
- QD1 (90,97,59): phase 1, op=6, tries=6, dec=1,
  via=3, val=59, phit=0. Z4-exact=1.
- QD2 (140,148,63): phase 1 all 6 fail; phase 2 on
  Z4: op=5, tries=11, dec=1, via=4, val=63, phit=0.
  Z5-exact=1.
- QD3 (160,167,65): phase 1 all 6 fail; phase 2 on
  Z4 all 6 fail; phase 2 on Z5: ops 1-3 fail, op4
  Form B fails then Form A verifies: op=4, tries=16,
  dec=1, via=5, val=65, phit=0. Z6-exact=1.
- QD4 (65,160,65): phase 1 all 6 fail; phase 2 on
  Z4 all 6 fail; phase 2 on Z5 all 6 fail; phase 2
  on Z6: ops 1-3 fail, op4 Form B verifies
  (tstar=167==aend, backward walk 167->160): op=4,
  tries=22, dec=1, via=6, val=65, phit=0.
  Z7=6(1,8,65,160,1,1,4,29,22,3,4,1)
  rels[4,29,22,23,22,23,22,23]
  facts[38,37,36,35,34,33,32,31], Z7-exact=1.
  e_add(6,5,16).
- QD5 (170,174,66): phase 1 6 fail; phase 2 on
  Z4/Z5/Z6/Z7 6 fail each: op=-1, tries=30, dec=0,
  val=-2, phit=0. No new Z. Terminates.
- Re-asks: QD1-B via=3 val=59 entered=0; QD2-B
  via=4 val=63 entered=0; QD3-B via=5 val=65
  entered=0; QD4-B via=6 val=65 entered=0 (pipeline
  walks Z7 backward 65->160; value read from stored
  fact[0]'s obj).
- FULL t16=4; e_has(3,2,16)=1; e_has(4,3,16)=1;
  e_has(5,4,16)=1; e_has(6,5,16)=1;
  e_has(6,3,16)=0; e_has(4,1,16)=0;
  e_has(5,3,16)=0; e_has(6,4,16)=0; LINK14 to 3, 4,
  5, 6; mD' live=1; oth=0.
- as=671/1651/3468/1688/5129 ae=2/2/2/2/0
  (informational).

### NOREUSE arm (mask 0)

QD1=QD2=QD3=QD4=QD5 val=-2, t16=0, oth=0.

### ABLATE-INV arm (mask 55: ops 1,2,3,5,6)

- QD1: op=6, tries=5, via=3, val=59.
- QD2: op=5, tries=9, via=4, val=63.
- QD3: val=-2, tries=15, op=-1 (op4 necessary for
  the third link). QD4: val=-2, tries=15, op=-1
  (op4 necessary for the fourth link too). QD5:
  val=-2, tries=15, op=-1.
- t16=2; e_has(3,2,16)=1; e_has(4,3,16)=1;
  e_has(5,4,16)=0; e_has(6,5,16)=0; oth=0.

### ABLATE-ABS arm (mask 47: ops 1,2,3,4,6)

- QD1: op=6, tries=5, via=3, val=59.
- QD2: op=6, tries=10, via=4, val=63 (preregistered
  reroute through phase-2 CONCRETIZE on Z4).
- QD3: op=4, tries=14, via=5, val=65 (3-chain
  completes through the rerouted Z5). QD4: op=4,
  tries=19, via=6, val=65 (4th link completes
  through the rerouted chain; Z7 built,
  e_add(6,5,16)). QD5: val=-2, tries=25, op=-1.
- t16=4; e_has(3,2,16)=1; e_has(4,2,16)=1;
  e_has(4,3,16)=0; e_has(5,4,16)=1;
  e_has(6,5,16)=1; oth=0.

### FRESH arm (facts only, mask 63)

QD1=QD2=QD3=QD4=QD5 val=-2 (MR-NO-SRC), t16=0, oth=0.

### CONTROL arm (frozen learner, F-K7)

FULL: QA via=1; QD1: op=6, tries=6, via=3, val=59,
Z4-exact=1; QD2/QD3/QD4/QD5: val=-2, tries=6,
op=-1, dec=0; QD1-B via=3 val=59 entered=0; t16=1;
e_has(3,2,16)=1; e_has(3,1,16)=0; LINK14 to 3;
mD' live=1; oth=0. NOREUSE: all QD val=-2, t16=0.
The frozen 6-operator harness cannot solve QD4: the
4-chain is necessary.

### Determinism and seal

3/3 byte-identical per binary:
comp_F e4cd4ce4ccb08870630c8b5055ae51bb36f84d33287fca2b169e7a3dfadbf51e,
ctl_F 2111a18040d13cf50355e902ef36b4a535f09b0c81d8bc0420efe0459dce688d.
FALSIFIERS 0 on every run of every binary.

## Findings

1. Composability scales to 4-deep with NO mechanism
   change and NO world change: the frozen phase-2
   (fixed enumeration over operator-built Z sources,
   snapshot-once-per-query) composes 4 operators in
   sequence on the exact world where it composed 3.
   The [6,5,4,4] chain is the discriminating
   4-tuple: CONCRETIZE mints dnf=3 (only op6 can),
   ABSTRACT re-skins it onto new folds (only op5
   verifies on Z4), INVERT Form A reverses Z5's rels
   into a walk no single operator and no 2-chain can
   produce, INVERT Form B inverts Z6's value mapping
   (tstar=167==aend, backward walk to key 160) in a
   way no 1-, 2-, or 3-chain can produce (verified:
   all 6 ops fail on taught mA', all 6 fail on Z4,
   all 6 fail on Z5 for QD4).
2. Within-query chaining is not the missing piece
   for depth 4 either: cross-query composition with
   T2's snapshot discipline suffices, demonstrated
   not asserted (F-NO-INTRA: Z7 tried only in QD5,
   never in QD4).
3. Termination scales linearly with the source
   count: QD5's 30-try exhaustion over four live Z
   sources (including the dir=1 Z7) shows the bound
   is (6 phase-1 + 6 per live Z source), no hang, no
   new Z.
4. The chain is robust to operator ablation: with
   ABSTRACT masked, the 4-chain reroutes through
   phase-2 CONCRETIZE (QD2 op=6 tries=10) and still
   completes via INVERT Form A (QD3 op=4 tries=14)
   and INVERT Form B (QD4 op=4 tries=19) with
   correct provenance (6,5,16).
5. Honest note on the fourth link: QD4=(65,160,65)
   has s==v. This is a structural requirement of the
   frozen INVERT Form B, preregistered in PREREG
   section 3, not discovered post hoc: the inverse
   walk's first hop is the value fact (tstar,dvr,v)
   whose obj is v, and chain_exec_bwd starts at
   cur=s, so verification requires s==v. The query
   poses the value as the inverse-walk start
   (value->key inversion). The chain inverts, then
   inverts the inversion: Form A reversed Z5's
   structure to build Z6; Form B inverts Z6's value
   mapping to build Z7.

## Disclosures and non-claims

- L2 evidence only (operator output reused as
  operator input across queries by a fixed,
  researcher-supplied two-phase enumeration), not
  L3: the operator menu, the phase-2 rule, and T1-T6
  are researcher-supplied.
- One [6,5,4,4] chain on one shared family does not
  establish general 4-operator composability;
  within-query chaining was deliberately NOT built
  (T2 forbids it) and remains out of scope, as do
  5+ chains, the protected core, the continuing
  learner, scaling, and transfer.
- The world is byte-identical to chain3's world_E;
  its discriminating power comes from the
  frozen-learner control arm (F-K7), not from
  designer blindness.
- as/ae tick counts were informational only, never
  bars; determinism rests on 3/3 byte-identical runs.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types,
  0 new opcodes, 0 semantic cases, 0 learner source
  changes, 0 world changes. Pure Zag, safebin
  toolchain, zero forbidden executables (Step 0
  verified at startup; `which python3` and `which
  python` empty under safebin PATH).
- No em/en dashes in loop documentation. Commits
  local with explicit pathspecs; nothing pushed.
  Compose2, adversary, builder, and chain3 lane
  directories were never modified.

## Files

- `NAMECHECK.md` (Step 0 toolchain guard),
  `PREREG.md` (frozen alone at 3fcc63b68),
  `REPORT.md` (this file)
- `learner.zag` (sha256-identical to chain3's
  extended learner), `learner_frozen.zag`
  (sha256-identical to chain3's frozen learner),
  `world_F.zag` (sha256-identical to chain3's
  world_E), `driver_F.zag`, `driver_Fctl.zag`,
  `comp_F_full.zag`, `comp_F_bin`,
  `comp_F_compile.txt`, `comp_F_run{1,2,3}.txt`,
  `ctl_F_full.zag`, `ctl_F_bin`,
  `ctl_F_compile.txt`, `ctl_F_run{1,2,3}.txt`
