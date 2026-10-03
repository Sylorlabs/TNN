# REPORT: L2-INVERT-VALUE (value-mapping inversion completes op 4 INVERT)

Worker: L2-INVERT-VALUE subagent (depth 2/2), 2026-10-03.
Prereg: `l2_invert_value/PREREG.md`, frozen alone at
commit ee8dca0ca before any implementation existed. One
transparent pre-verdict amendment: PREREG_AMENDMENT1.md
(QV-AS 1186->1237: prereg used the pre-amendment parent
base 1142 instead of the amended 1193; the implementation
output 1237 confirms the corrected derivation; plus
removal of a stale duplicate F-ABLATET-T16 falsifier
line, and corrections to two informational
ablation-arm counts whose parent bases contained errors;
no counting-rule or learner-code change).

## Verdict

**L2-INVERT-VALUE-PASS.** All eight kill bars PASS, no
falsifier fired, 3/3 byte-identical.

## What was built

The parent L2-METAREUSE-EXTEND harness extended with
value-mapping inversion, completing the INVERT operator.
Assembled as `cat learner.zag world.zag driver.zag >
iv_full.zag` (2797 lines) and compiled with the pinned
znc to `iv_bin` (build exit 0; only A0102
ignored-return-value warnings, same class as the parent
lane). No forbidden executables. 0 modes, 0 bridges,
0 handlers, 0 new edge types, 0 new opcodes, 0 semantic
cases, 0 domain-pair templates. World facts unchanged
(44); the new query grounds entirely in mA's own facts.

Answer to the parent task's question "Can the learner do
it? (or is it just structural?)": the learner does it.
Op 4 INVERT now has two forms. Form B (value-mapping
inversion, tried first): reverse value lookup (scan all
44 facts for rel==dvr AND obj==v; the terminal carrying
the value is DISCOVERED, never given; it must equal the
source's own terminal, else the value does not belong
to this source's mapping) followed by a backward chain
walk (one obj-match hop per source rel, in reverse
order, each verified against a live world fact) from
that terminal to the key. Form A (the parent lane's
structural relation-sequence reversal + strict forward
walk) is now the fallback. The two forms are mutually
discriminating: Q_INVVAL (11,100,11) is solvable ONLY by
Form B (Form A fails: no rel-6 hop from 11), and Q_INV
(120,127,60) is solvable ONLY by Form A (Form B fails:
value 60's terminal 127 is not mA's terminal 43).

New machinery (all generic, relation-agnostic):
- ex_find_objrel: counted obj-match fact scan
  (mirrors ex_find_subrel).
- mr_invert_val: reverse value lookup + backward walk
  + strict terminal check; builds via mr_buildwin_inv.
- mr_buildwin_inv: backward execution-verify
  (chain_exec_bwd), creates the MAP with dir=1,
  single-source t16 provenance, deliver.
- MAP dir flag at row byte +39 (was pad): 0=forward,
  1=inverse/backward. m_exec walks backward
  (obj==cur -> cur=sub) when dir==1; the pipeline
  reads an inverse MAP's value from its stored
  value-fact's obj (learner state + world, never the
  query).
- mr_invert tries Form B first, Form A on failure;
  mr_adapt's op-4 mask bit 8 gates both forms as one
  operator.

The new query and structure (FULL arm):
- Q_INVVAL (11,100,11,AGG,A): op 4 Form B. Ops 1-3
  fail (no fact with sub==11). Form B: lookup finds
  fact 6 = (43,2,11), t*=43 == mA end 43; backward
  walk 43->32->42->31->41->30->40->100; cur==t.
  Z_invval id 10: walk-order rels [2,6,5,6,5,6,5,18],
  facts [6,5,4,3,2,1,0,7], start 11, end 100, dir=1,
  descriptor (2,6,5,3,2). t16: 10->1.
- Re-ask Q_INVVAL-B goes through the pipeline via Z
  id 10 with no meta phase (MR_ENTERED=0): the
  inverse structure persists and is reused by
  backward execution, ANS term=100 val=11 via=10.

## Kill-bar results (in-Zag BARS + shell checks on iv_run1.txt)

- K1: qa_via=1, qb_via=2, disj=1. `Q QA` < `Q QB` <
  `Q QCOMB`. PASS.
- K2: all seven phit=0 in FULL; NOREUSE arm all seven
  vals=-2, t16=0. 7 `MR-PIPELINE-FAIL` lines in FULL,
  7 in NOREUSE. PASS.
- K3: qc_op=1, qs_op=2, qt_op=3, qv_op=4, qe_op=5,
  qn_op=6, qvv_op=4; tries 1/2/3/4/5/6/4;
  decided=1 each; qc_asrc=1, qvv_asrc=1. Shell
  verbatim per query; QINVVAL shows `MR-OP-TRY 4`,
  `MR-INVVAL-OK`, `MR-OP-OK 4` with no `MR-INV-REV`
  after (Form A never attempted); QINV shows
  `MR-INVVAL-FAIL` before `MR-INV-REV`/`MR-INV-OK`
  (Form B tried first and failed). `grep -c` of all
  operator/form trace tags in driver.zag = 0. PASS.
- K4: vias 4/5/6/7/8/9/10, vals 42/11/32/60/77/91/11,
  zc=zs=zt=zi=za=zn=zv=1 (exact match, incl. Z_invval
  dir=1). Seven `MR-ZBUILD` lines and seven `ANS`
  lines verbatim. PASS.
- K5: six ablation arms. ABLATE-COMBINE (62): QCOMB
  -2, others pass incl. QINVVAL=11, t16=6.
  ABLATE-SUBST (61): QSUB -2, others pass, t16=7.
  ABLATE-TRUNC (59): QTRUNC -2, others pass, t16=7.
  ABLATE-INV (55): QINV -2 AND QINVVAL -2 (op 4 is
  one operator covering both forms), others
  42/11/32/77/91, t16=6. ABLATE-ABS (47): QABS -2,
  others pass, t16=7. ABLATE-CONC (31): QCONC -2,
  others pass, t16=7. PASS.
- K6: 3/3 byte-identical, sha256
  649609a2e92041a8ffb299a48bec6294b417a685b7ce04b3d64aea9f221b8e9c
  x3. PASS.
- K7: frozen token-allowlist audit: comment/string-
  stripped learner.zag yields exactly the 55-token
  allowlist (no world/answer id outside structural
  offsets); new-id spot check (11/43/100) clean.
  PASS.
- K8: t16F=8; e_has(4,1,16), (4,2,16), (5,1,16),
  (6,1,16), (7,1,16), (8,1,16), (9,3,16),
  (10,1,16) all 1. PASS.

Falsifiers: 0 fired. F-COUNT silent (FULL as/ae:
333/2, 335/2, 324/2, 1237/2, 1286/2, 1146/2, 393/2,
exactly the amended hand derivation). Ablate-arm
informational counts: 460/533/497/1183(QINV)+411
(QINVVAL)/1185/849, each reconciled against the
frozen algorithm (the 497 and 1183 incorporate the
two amendment corrections to buggy parent bases).

## Numbers

- FULL: QCOMB op=1 tries=1 as=333 ae=2 via=4 val=42;
  QSUB op=2 tries=2 as=335 ae=2 via=5 val=11;
  QTRUNC op=3 tries=3 as=324 ae=2 via=6 val=32;
  QINV op=4 tries=4 as=1237 ae=2 via=7 val=60
  (Form B 44: t*=127!=43 FAIL; Form A 196);
  QABS op=5 tries=5 as=1286 ae=2 via=8 val=77;
  QCONC op=6 tries=6 as=1146 ae=2 via=9 val=91;
  QINVVAL op=4 tries=4 as=393 ae=2 via=10 val=11
  (Form B 73: lookup 44 + walk 29; Form A never
  attempted); re-asks via 4/5/6/7/8/9/10,
  MR_ENTERED=0; t16=8
  {4->1,4->2,5->1,6->1,7->1,8->1,9->3,10->1};
  LINK14 to 4..10; NM=11; distractor mD live=1; no
  edge type outside {14,16} in any arm.
- NOREUSE: all seven -2, t16=0, NM=4. FRESH: all
  seven -2, t16=0, NM=0.

## Disclosures and non-claims

- The two INVERT forms, reverse value lookup with the
  source-terminal check, backward chain walk,
  inverse-MAP dir flag, backward execution in m_exec
  / chain_exec_bwd, and the pipeline value read for
  inverse MAPs are researcher-supplied generic
  machinery, frozen in the prereg. None names a
  relation, MAP, domain, query, form-to-query
  assignment, value, terminal, or key. The fixed
  operator order [1..6] and Form-B-first policy are
  generic; which form verifies is decided at runtime
  by execution, as the traces demonstrate (Q_INV
  fails Form B then passes Form A; Q_INVVAL passes
  Form B without attempting Form A).
- The strict source-terminal check (t* must equal
  the source's stored end) is a deliberate
  principled restriction: Form B inverts THIS
  source's value mapping, not any value chain in
  the world. A looser "any terminal carrying v"
  variant was considered and rejected as less
  faithful to "the MAP maps A->B, the inverse maps
  B->A".
- This is L2 (learner-driven structural adaptation
  with operator/form choice), not L3: the operator
  menu and the two INVERT forms are
  researcher-supplied. Meta-selection does not
  invent operators or forms.
- OP_MASK is a driver-set causal-control flag (the
  COMBINE_ON precedent), never written by the
  learner; it enables the lesion comparison and is
  set per ARM, never per query.
- One world family. No generality claim beyond the
  nine arms; the world is builder-designed, not
  adversary-designed. Sealed-adversary generality is
  open future work.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types,
  0 new opcodes, 0 new semantic cases. Pure Zag,
  safebin toolchain, zero forbidden executables.
- No em/en dashes in loop documentation. Paper
  untouched. Commits local with explicit pathspecs.
  Nothing pushed.
- Unfrozen only: no frozen source touched. The
  frozen TNN core is not used here; this is a
  standalone learner-mechanism experiment.
- This wave does not integrate anything into the
  protected core or any continuing learner.

## Files

- `learner.zag`, `world.zag`, `driver.zag`,
  `iv_full.zag` (concatenated build input),
  `iv_bin` (pinned-znc binary), `iv_compile.txt`,
  `iv_run1.txt`, `iv_run2.txt`, `iv_run3.txt`
- `NAMECHECK.md` (Step 0 toolchain guard),
  `PREREG.md` (frozen, committed alone at ee8dca0ca
  before implementation), `PREREG_AMENDMENT1.md`
  (pre-verdict arithmetic corrections)
