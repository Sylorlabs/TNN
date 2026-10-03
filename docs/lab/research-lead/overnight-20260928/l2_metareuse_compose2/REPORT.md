# REPORT: L2-METAREUSE-COMPOSE-2 (operator composition probe)

Worker: L2-METAREUSE-COMPOSE-2 subagent (depth 2/2), 2026-10-03.
Prereg: `l2_metareuse_compose2/PREREG.md`, frozen alone at
commit c3613c685 before any implementation existed. One
transparent pre-verdict amendment: PREREG_AMENDMENT1.md
(ABLATE-ABS QD1 tries 6 -> 5: MR_OP_TRIES counts only
actually-tried operators, never masked skips; frozen
mask-gated counting behavior, no code change).

Non-ledger task (claim minting paused): this is a wave
verdict, not a ledger claim.

## Verdict

**L2-METAREUSE-COMPOSE-2-PASS.** The extended learner
passes all frozen bars with zero falsifiers, 3/3
byte-identical per binary:

- Build D: D-K1 through D-K8 all PASS, including the
  QD2 composition signature (op=5, tries=11, via=5,
  val=63: ABSTRACT fired on the CONCRETIZE-built Z4
  after 6 failed phase-1 tries) and the QD3
  bounded-termination signature (tries=18, val=-2, no
  new Z, run terminates).
- Control D-K7: the frozen learner on the identical
  world solves QD1 (op=6, tries=6, via=4, val=59) but
  fails QD2/QD3 (-2, tries=6, op=-1), proving the
  composition step is what solves QD2.
- Regression R-REG: all seven sealed adversary builds
  reproduce their exact barred outcomes on the extended
  learner (in-Zag falsifiers 0 on every build; output
  diffs vs the sealed runs are trace-lines-only, zero
  removed lines).

## What was built

Build D: `cat learner.zag world_D.zag driver_D.zag >
comp_D_full.zag` and the control `cat
learner_frozen.zag world_D.zag driver_Dctl.zag >
ctl_D_full.zag`, compiled with the pinned znc (build
exit 0; only A0102 ignored-return-value and E0102
constant-product warnings, same classes as the sealed
lanes). `learner_frozen.zag` is byte-identical to
`l2_metareuse_adversary/learner.zag` (sha256
698be75b19e3d9a85b3b308aa4d1e645cbb4e386169bcb47d8b20dfb93877731).
The extended `learner.zag` differs from the frozen
file ONLY in the four sanctioned categories (R-K7'
change audit): (a) header comment describing phase 2,
(b) state-layout comments for 1392/1396, (c) ZSRC
append in mr_buildwin and mr_buildwin_inv, (d) the
phase-2 block in mr_adapt. No checked field changes;
phase 1 is textually identical. The drivers never name
an operator, source pair, binding, pattern, or form
(F-SEAL-D shell tag audit 0 hits on all three files);
queries are (start,terminal,value,cap,dom) with one
arm-level OP_MASK. Fresh rel/node ids throughout
(28,29,34,35 for the composition family).

The composition mechanism: phase 2 runs only when
phase 1 fails; it retries the fixed [1..6] enumeration
over operator-built Z MAPs (ZSRC_IDS registry, live,
cap==qcap, id != agg_src, build order) with distinct
MR-COP-TRY/OK/FAIL/SKIP tags and identical mask
discipline and tries counting. Termination: T1 phase 2
only on phase-1 failure; T2 source list snapshotted
once per query (no intra-query chaining); T3 one
composition step per query; T4 all operator calls stay
fold/rel bounded; T5 op_mask gates phase 2 (skipped
when 0); T6 sources are operator-built, live,
cap==qcap, id != agg_src.

## Kill-bar results (build D, extended learner)

### FULL arm (mask 63)

- QA via=1 val=51; QB via=2 val=-1 (D-K1).
- QD1 (90,98,59): phase 1, op=6, tries=6, dec=1,
  via=4, val=59, phit=0. Z4=4(1,7,90,98,1,1,29,26,
  27,3,4,0) rels[29,26,27,26,27,26,27]
  facts[18,19,20,21,22,23,24], Z4-exact=1.
- QD2 (140,148,63): phase 1 all 6 fail; phase 2 on
  Z4: MR-COMP-SRC id=4, ops 1-4 fail, op=5
  tries=11, dec=1, via=5, val=63, phit=0 (D-K3
  composition signature). Z5=5(1,7,140,148,1,1,29,
  22,23,3,4,0) rels[29,22,23,22,23,22,23]
  facts[27,28,29,30,31,32,33], Z5-exact=1.
- QD3 (150,157,64): phase 1 all 6 fail; phase 2 on
  Z4 (6 fails) and on Z5 (6 fails): op=-1,
  tries=18, dec=0, val=-2, no new Z (D-K3 bounded
  termination).
- Re-asks: QD1-B via=4 val=59 entered=0; QD2-B
  via=5 val=63 entered=0 (D-K4 persistence).
- t16=2; e_has(4,3,16)=1 (Z4 built by CONCRETIZE
  from pattern mP' id 3); e_has(5,4,16)=1 (Z5 built
  by ABSTRACT from Z4); e_has(4,1,16)=0;
  e_has(5,3,16)=0; LINK14 to 4 and 5; mD' live=1;
  oth=0 (D-K8).
- as=815/1706/4816 ae=2/2/0 (informational).

### NOREUSE arm (mask 0)

QD1=QD2=QD3 val=-2, t16=0, oth=0 (D-K2).

### ABLATE-ABS arm (mask 47: ops 1,2,3,4,6)

- QD1: op=6, tries=5, via=4, val=59 (prereg
  amended: masked op5 is never tried, never
  counted).
- QD2: phase 1 (5 tries, op5 SKIP, op6 OLD-FOLDS
  fail); phase 2 on Z4: op=6, tries=10, via=5,
  val=63 (preregistered reroute: CONCRETIZE on
  Z_conc, folds (22,23) novel vs Z4's (26,27)).
  Z5 row identical to FULL; e_add(5,3,16).
- QD3: val=-2, tries=15, op=-1.
- t16=2; e_has(4,3,16)=1; e_has(5,3,16)=1;
  e_has(5,4,16)=0; e_has(4,1,16)=0; oth=0 (D-K5).

### ABLATE-CONC arm (mask 31: ops 1-5)

QD1=QD2=QD3 val=-2, tries=5 each, t16=0, oth=0
(D-K5: op6 necessary for the whole chain; with no
Z_conc banked, QD2 cannot compose).

### FRESH arm (facts only, mask 63)

QD1=QD2=QD3 val=-2 (MR-NO-SRC), t16=0, oth=0.

### CONTROL arm (frozen learner, D-K7)

FULL: QA via=1, QB via=2; QD1: op=6, tries=6,
via=4, val=59, Z4-exact=1; QD2: val=-2, tries=6,
op=-1, dec=0; QD3: val=-2, tries=6, op=-1, dec=0;
QD1-B via=4 val=59 entered=0; t16=1;
e_has(4,3,16)=1; e_has(4,1,16)=0; LINK14 to 4;
mD' live=1; oth=0. NOREUSE: QD1=QD2=QD3 val=-2,
t16=0, oth=0. The frozen 6-operator harness cannot
solve QD2: composition is necessary.

### Determinism and seal

3/3 byte-identical per binary:
comp_D fe65ce839977d95bd63fd97581d792f39bdb1cec3ad5b1546742ef7e83066112,
ctl_D 9ba4c635fc12eb83e52c205648ed66ca3129577e9847c04ca06fbfc5da9a2e34,
reg_A 1b8d5907ce39475308c8b57930eba2b9b9d1f2cccc7d9f9a794eb7342205047f,
reg_B 8c52fba26c5901876abe2535274e97a261469c5278546d1115a80e239416b90b,
reg_C 1e6a911e0afc4a38736a07b068008590c883cff7b93af634d2cf997fc76a21c0,
reg_X1 8fac62cc5b276513a668aa649a5dbb6735f4c2493a445e5e1914feca43eec0aa,
reg_X2 f97a284a6c6d5db05feb01f9b8d619299b50fdce216563f9ff764f39bd92f2eb,
reg_X3 70117de19dc96d860ce05e38c6da2b81f37ab4c6348fa1dc8de317496ec89969,
reg_X4 302479ce2798ac13e0616b02a737e29033ce8a9a9bf6075330ad1c8afe617ab3.
FALSIFIERS 0 on every run of every binary.

## Regression: the seven sealed adversary builds (R-REG)

Extended learner + byte-identical copies of the
adversary's world/driver files (sha256-verified).
All seven builds: in-Zag FALSIFIERS 0, 3/3
byte-identical. Output diffs vs the sealed runs are
trace-lines-only (zero removed lines on every
build): A +128, B +2, C +40 (phase-2 traces in
ablation arms where a query fails phase 1 with a
non-empty ZSRC registry; every phase-2 try fails,
no answer/bar line changes), X1-X4 +1 each (the
single MR-COMP-NONE line). Barred values reproduce
exactly: A t16=4 oth=0; B t16=2; C t16=2;
X1-X4 XK1-BOUNDARY 1, XK1-SOLVED 0, QX val=-2.
The four documented boundary limitations still fail
gracefully and deterministically; X4 terminates.

## Findings

1. Operators ARE composable in the cross-query
   sense: CONCRETIZE's Z output (dnf=3, de=29, a
   structure no single operator can mint from the
   taught source) served as ABSTRACT's source on the
   next query, solving QD2 which no single operator
   solves on the taught source. The [6,5] pair is the
   discriminating composition: only CONCRETIZE can
   mint dnf=3 from the taught mA' (verified against
   the frozen operator source), so ABSTRACT-on-Z
   succeeds exactly where SUBSTITUTE-on-taught-source
   cannot.
2. The fixed [1..6] enumeration did NOT need to
   become a general operator-sequence search for this
   result: retrying the same fixed enumeration over
   operator-built Z sources (a bounded
   operator x Z-source product, at most 6 tries per
   source) suffices, with termination conditions
   T1-T6. Within-query chaining was not needed and
   was not built.
3. Composition has a preregistered reroute: with
   ABSTRACT masked, QD2 still composes through
   phase-2 CONCRETIZE on Z_conc (op=6, tries=10),
   with provenance correctly pointing at the
   pattern (e_has(5,3,16)=1, e_has(5,4,16)=0).
4. Bounded termination is demonstrated, not
   asserted: QD3 exhausts 12 phase-2 tries across
   two live Z sources and returns -2 with no new Z
   and no hang.
5. The existing 6-operator behavior is unbroken:
   all seven sealed builds reproduce their exact
   barred outcomes; the only output changes are
   added phase-2 trace lines.

## Disclosures and non-claims

- This is L2 evidence (operator output reused as
  operator input across queries by a fixed,
  researcher-supplied two-phase enumeration), not
  L3: the operator menu, the phase-2 rule, and the
  termination conditions are researcher-supplied.
- One composition pair [6,5] on one fresh family
  does not establish general operator
  composability; within-query operator chaining,
  longer chains, the protected core, the continuing
  learner, scaling, and transfer are out of scope.
- Build D's world is worker-designed; its
  discriminating power comes from the frozen-learner
  control arm (D-K7), not from designer blindness.
  The [4,5] pair was preregistered as
  non-discriminating by mechanism analysis
  (INVERT-A mints dnf=2 on the taught source, so
  SUBSTITUTE covers anything ABSTRACT covers
  there), not tested with a build.
- as/ae tick counts were informational only, never
  bars; determinism rests on 3/3 byte-identical runs.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types,
  0 new opcodes, 0 semantic cases. Pure Zag, safebin
  toolchain, zero forbidden executables (Step 0
  verified at startup; `which python3` empty under
  safebin PATH).
- No em/en dashes in loop documentation. Commits
  local with explicit pathspecs; nothing pushed.
  Adversary and builder lane directories were never
  modified.

## Files

- `NAMECHECK.md` (Step 0 toolchain guard),
  `PREREG.md` (frozen alone at c3613c685),
  `PREREG_AMENDMENT1.md` (pre-verdict tries-count
  correction, committed at 6e3a2a3aa),
  `REPORT.md` (this file)
- `learner.zag` (extended), `learner_frozen.zag`
  (byte-identical to the adversary's frozen learner),
  `world_D.zag`, `driver_D.zag`, `driver_Dctl.zag`,
  `comp_D_full.zag`, `comp_D_bin`,
  `comp_D_compile.txt`, `comp_D_run{1,2,3}.txt`,
  `ctl_D_full.zag`, `ctl_D_bin`, `ctl_D_compile.txt`,
  `ctl_D_run{1,2,3}.txt`
- `reg_world_{A,B,C,X1,X2,X3,X4}.zag`,
  `reg_driver_{A,B,C,X1,X2,X3,X4}.zag`
  (sha256-verified copies of the sealed files),
  `reg_{A,B,C,X1,X2,X3,X4}_full.zag`,
  `reg_{A,B,C,X1,X2,X3,X4}_bin`,
  `reg_{A,B,C,X1,X2,X3,X4}_compile.txt`,
  `reg_{A,B,C,X1,X2,X3,X4}_run{1,2,3}.txt`
