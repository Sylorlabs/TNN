# REPORT: L2-COMPOSE-CHAIN3 (3-operator chain probe)

Worker: L2-COMPOSE-CHAIN3 subagent (depth 2/2), 2026-10-03.
Prereg: `l2_compose_chain3/PREREG.md`, frozen alone at
commit 36a8d1345 before any implementation existed. Two
transparent pre-verdict amendments: PREREG_AMENDMENT1.md
(44-fact cap discovery; world redesigned to 44 facts,
mB'/QB dropped, mP' id 3->2, QD1 90->97, QD4 shortened
to 5 facts) and PREREG_AMENDMENT2.md (Z MAP ids are
3,4,5 not 4,5,6 with 3 taught MAPs; plus two off-by-one
fact-list corrections in Z5/Z6 predictions).

Non-ledger task (claim minting paused): this is a wave
verdict, not a ledger claim.

## Verdict

**L2-COMPOSE-CHAIN3-PASS.** All frozen bars hold with
zero falsifiers, 3/3 byte-identical per binary:

- Build E: E-K1 through E-K8 all PASS, including the
  QD3 3-chain signature (op=4, tries=16, dec=1, via=5,
  val=65, Z6-exact=1: INVERT Form A fired on the
  phase-2-built Z5 after 6 failed phase-1 tries and 6
  failed phase-2 tries on Z4) and the QD4
  bounded-termination signature (tries=24, val=-2, no
  new Z, run terminates with three live Z sources).
- Control E-K7: the frozen learner on the identical
  world solves QD1 (op=6, tries=6, via=3, val=59) but
  fails QD2/QD3/QD4 (-2, tries=6, op=-1), proving the
  3-chain is what solves QD3.
- Ablations discriminate: ABLATE-INV (mask 55, op4
  masked) fails QD3 (tries=15, -2): op4 is necessary
  for the third link. ABLATE-ABS (mask 47) reroutes:
  QD2 composes via phase-2 CONCRETIZE on Z4 (op=6,
  tries=10), and QD3 still completes via op4 on the
  rerouted Z5 (op=4, tries=14, val=65).

## What was built (and what was deliberately NOT built)

The learner is BYTE-IDENTICAL to compose2's extended
learner.zag (sha256
6e8ed1e047e9dee8311a264aaec9a995ddbb723f5b284e21c18baa0e68038ddd,
verified at copy time). Zero source changes: not one
line, not one comment. This is the strongest test
form for the task's question: the frozen phase-2
mechanism was asked to compose 3-deep with no help.

New files: world_E.zag (44 facts: the frozen f_teach
cap discovered the hard way, see amendments),
driver_E.zag, driver_Ectl.zag. `learner_frozen.zag`
is byte-identical to the adversary's frozen learner
(sha256 698be75b19e3d9a85b3b308aa4d1e645cbb4e386169bcb47d8b20dfb93877731).
Builds: `cat learner.zag world_E.zag driver_E.zag >
comp_E_full.zag`, `cat learner_frozen.zag world_E.zag
driver_Ectl.zag > ctl_E_full.zag`, pinned znc, exit 0,
warnings only (same classes as the compose2 builds).

The drivers never name an operator, source pair,
binding, pattern, or form (F-SEAL-E shell tag audit
0 hits on all three files); queries are
(start,terminal,value,cap,dom) with one arm-level
OP_MASK. Fresh rel id 31 only.

## Answers to the task's questions

**Q1: 3-operator chains? YES.** The [6,5,4] chain:
QD1 fires CONCRETIZE (phase 1) and banks Z4 id 3
(dnf=3, de=29); QD2, unsolvable by any single
operator on the taught source, fires ABSTRACT (op5)
on Z4 in phase 2 and banks Z5 id 4; QD3, unsolvable
by 1 operator (phase 1: all 6 fail) AND unsolvable by
2 operators (phase 2 on Z4: all 6 fail - Z4 is the
only Z a 2-chain could use), fires INVERT (op4)
Form A on Z5 in phase 2 and banks Z6 id 5, answering
65. The trace signature: MR-COMP-SRC id=4,
MR-COP-TRY 1/2/3 FAIL, MR-COP-TRY 4,
MR-INVVAL-LOOKUP t*=167 srcend=148 MR-INVVAL-FAIL
(Form B correctly rejects), MR-INV-OK,
MR-ZBUILD rels=23,22,23,22,23,22,29
facts=31,32,33,34,35,36,37, MR-VERIFY term=167 OK,
MR-PROMOTE z=5 t16=5->4, ANS term=167 val=65 via=5.
tries=16 is itself the discriminator: 6 phase-1 + 6
Z4 + 3 Z5 failures precede the single success, so a
<=2-chain solution would have shown tries<=12
(F-CHAIN2).

**Q2: fixed enumeration suffices; within-query
chaining NOT needed.** The unchanged phase-2 (fixed
[1..6] enumeration retried over ZSRC_IDS) composes
3-deep with zero learner changes. The 3-chain emerges
across three queries, each step independently gated
by full execution verification. F-NO-INTRA shell
audit: `MR-COMP-SRC id=5` (Z6) occurs exactly twice
in the FULL run, both inside QD4's phase-2 block
(after QD3's ANS), never inside QD3: per T2, the Z
built during QD3's phase 2 is recorded for future
queries but never tried within QD3. T2 holds
empirically, not just by construction.

**Q3: termination holds (T1-T6).** QD4 is unsolvable
by design and exhausts the full product: 6 phase-1
tries + 6 on each of three live Z sources = 24
tries, val=-2, op=-1, dec=0, no new Z, no hang. T1-T6
hold by construction (unchanged code) and the QD4
signature demonstrates them with three live Z
sources.

## Kill-bar results (build E)

### FULL arm (mask 63)

- QA via=1 val=51 (E-K1).
- QD1 (90,97,59): phase 1, op=6, tries=6, dec=1,
  via=3, val=59, phit=0. Z4=3(1,7,90,97,1,1,29,26,
  27,3,4,0) rels[29,26,27,26,27,26,27]
  facts[15,16,17,18,19,20,21], Z4-exact=1.
  e_add(3,2,16) (src1=pattern id 2).
- QD2 (140,148,63): phase 1 all 6 fail; phase 2 on
  Z4: op=5, tries=11, dec=1, via=4, val=63, phit=0.
  Z5=4(1,7,140,148,1,1,29,22,23,3,4,0)
  rels[29,22,23,22,23,22,23]
  facts[23,24,25,26,27,28,29], Z5-exact=1.
  e_add(4,3,16).
- QD3 (160,167,65): phase 1 all 6 fail; phase 2 on
  Z4 all 6 fail; phase 2 on Z5: ops 1-3 fail, op4
  Form B fails (167 != 148) then Form A verifies:
  op=4, tries=16, dec=1, via=5, val=65, phit=0.
  Z6=5(1,7,160,167,1,1,23,22,23,3,4,0)
  rels[23,22,23,22,23,22,29]
  facts[31,32,33,34,35,36,37], Z6-exact=1.
  e_add(5,4,16).
- QD4 (170,174,66): phase 1 6 fail; phase 2 on Z4/Z5/
  Z6 6 fail each: op=-1, tries=24, dec=0, val=-2,
  phit=0. No new Z. Terminates.
- Re-asks: QD1-B via=3 val=59 entered=0; QD2-B
  via=4 val=63 entered=0; QD3-B via=5 val=65
  entered=0 (pipeline walks Z6 forward 160->167).
- FULL t16=3; e_has(3,2,16)=1; e_has(4,3,16)=1;
  e_has(5,4,16)=1; e_has(5,2,16)=0;
  e_has(3,1,16)=0; e_has(4,2,16)=0; LINK14 to 3, 4,
  5; mD' live=1; oth=0.
- as=671/1651/3468/4017 ae=2/2/2/0 (informational).

### NOREUSE arm (mask 0)

QD1=QD2=QD3=QD4 val=-2, t16=0, oth=0.

### ABLATE-INV arm (mask 55: ops 1,2,3,5,6)

- QD1: op=6, tries=5, via=3, val=59.
- QD2: op=5, tries=9, via=4, val=63.
- QD3: val=-2, tries=15, op=-1 (op4 necessary for
  the third link). QD4: val=-2, tries=15, op=-1.
- t16=2; e_has(3,2,16)=1; e_has(4,3,16)=1;
  e_has(5,4,16)=0; oth=0.

### ABLATE-ABS arm (mask 47: ops 1,2,3,4,6)

- QD1: op=6, tries=5, via=3, val=59.
- QD2: op=6, tries=10, via=4, val=63 (preregistered
  reroute through phase-2 CONCRETIZE on Z4).
- QD3: op=4, tries=14, via=5, val=65 (3-chain
  completes through the rerouted Z5). QD4: val=-2,
  tries=20, op=-1.
- t16=3; e_has(3,2,16)=1; e_has(4,2,16)=1;
  e_has(4,3,16)=0; e_has(5,4,16)=1; oth=0.

### FRESH arm (facts only, mask 63)

QD1=QD2=QD3=QD4 val=-2 (MR-NO-SRC), t16=0, oth=0.

### CONTROL arm (frozen learner, E-K7)

FULL: QA via=1; QD1: op=6, tries=6, via=3, val=59,
Z4-exact=1; QD2/QD3/QD4: val=-2, tries=6, op=-1,
dec=0; QD1-B via=3 val=59 entered=0; t16=1;
e_has(3,2,16)=1; e_has(3,1,16)=0; LINK14 to 3;
mD' live=1; oth=0. NOREUSE: all QD val=-2, t16=0.
The frozen 6-operator harness cannot solve QD3: the
3-chain is necessary.

### Determinism and seal

3/3 byte-identical per binary:
comp_E a25e4a58f55b875d768fabbad80a4cab75407eaf36a849e73d7149c69836f53c,
ctl_E 3e98a8903e65aba1258d78a57ab1f224e0a769abf023b1ca75a0c6992ed68598.
FALSIFIERS 0 on every run of every binary.

## Findings

1. Composability scales beyond pairs with NO
   mechanism change: the frozen phase-2 (fixed
   enumeration over operator-built Z sources,
   snapshot-once-per-query) composes 3 operators in
   sequence. The [6,5,4] chain is the discriminating
   triple: CONCRETIZE mints dnf=3 (only op6 can),
   ABSTRACT re-skins it onto new folds (only op5
   verifies on Z4), INVERT Form A reverses Z5's
   rels into a walk no single operator and no
   2-chain can produce (verified: all 6 ops fail on
   taught mA' and all 6 fail on Z4 for QD3).
2. Within-query chaining is not the missing piece
   for depth 3: cross-query composition with T2's
   snapshot discipline suffices, demonstrated not
   asserted (F-NO-INTRA: Z6 tried only in QD4,
   never in QD3).
3. Termination scales with the source count: QD4's
   24-try exhaustion over three live Z sources shows
   the bound is (6 phase-1 + 6 per live Z source),
   linear in registry size, no hang, no new Z.
4. The chain is robust to operator ablation: with
   ABSTRACT masked, the 3-chain reroutes through
   phase-2 CONCRETIZE (QD2 op=6 tries=10) and still
   completes via INVERT (QD3 op=4 tries=14) with
   correct provenance (5,4,16).
5. Honest note on the third link: it is INVERT
   Form A (structural reversal), not Form B (value
   inversion): Form B correctly rejects first
   (t*=167 != 148) on every arm. The chain's third
   step is a reversed-rel walk, preregistered as
   such.

## Disclosures and non-claims

- L2 evidence only (operator output reused as
  operator input across queries by a fixed,
  researcher-supplied two-phase enumeration), not
  L3: the operator menu, the phase-2 rule, and T1-T6
  are researcher-supplied.
- One [6,5,4] triple on one fresh family does not
  establish general 3-operator composability;
  within-query chaining was deliberately NOT built
  (T2 forbids it) and remains out of scope, as do
  4+ chains, the protected core, the continuing
  learner, scaling, and transfer.
- Build E's world is worker-designed; its
  discriminating power comes from the frozen-learner
  control arm (E-K7), not from designer blindness.
- The 44-fact cap (f_teach n>=44) and the Z-id shift
  (3,4,5) were discovered during the wave and
  corrected via two transparent pre-verdict
  amendments; no bar was weakened to force a pass.
- as/ae tick counts were informational only, never
  bars; determinism rests on 3/3 byte-identical runs.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types,
  0 new opcodes, 0 semantic cases, 0 learner source
  changes. Pure Zag, safebin toolchain, zero
  forbidden executables (Step 0 verified at startup;
  `which python3` empty under safebin PATH).
- No em/en dashes in loop documentation. Commits
  local with explicit pathspecs; nothing pushed.
  Compose2, adversary, and builder lane directories
  were never modified.

## Files

- `NAMECHECK.md` (Step 0 toolchain guard),
  `PREREG.md` (frozen alone at 36a8d1345),
  `PREREG_AMENDMENT1.md` (44-fact cap redesign),
  `PREREG_AMENDMENT2.md` (Z-id shift 3,4,5),
  `REPORT.md` (this file)
- `learner.zag` (sha256-identical to compose2's
  extended learner), `learner_frozen.zag`
  (sha256-identical to the adversary's frozen
  learner), `world_E.zag`, `driver_E.zag`,
  `driver_Ectl.zag`, `comp_E_full.zag`, `comp_E_bin`,
  `comp_E_compile.txt`, `comp_E_run{1,2,3}.txt`,
  `ctl_E_full.zag`, `ctl_E_bin`, `ctl_E_compile.txt`,
  `ctl_E_run{1,2,3}.txt`
