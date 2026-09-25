# FAM-NOM evidence log (D4-RESID, prereg PREREG_D4_RESID.md @ 235152e8247c542480560b0c5317616e4083e2ca)

## Step 1 — unmodified rebuild (method §5.1)
- Sources: d4fix.zag, d4fix_triple.zag, R33_NATIVE_IO_V1.zag copied from
  /home/hatch/workspace/d4resid/build0/ (byte-identical to repo commit 5aef8c16,
  verified via raw.githubusercontent.com SHA-256 match).
- Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
- Rebuild output d4fix_bin SHA-256 == build0/d4fix_bin SHA-256
  (aaeb363c35a2a02a114e0106c80da9296c2e3c0e93a6ddf97fa66db456b596f2).
  Deterministic rebuild confirmed.

## Step 1 — smoke battery B4+B5 (unmodified), runs/smoke*
- wb: w1 INSTALLS (hole), w2 WITHHOLD + U|ROLE-SWAP, w3 WITHHOLD + U|MODAL.
- blind: bl-h1..h6 INSTALL 6/6; bl-a1 ROLE-SWAP, bl-a2 MODAL, bl-a6 REFERENCE,
  neither side installed from those clusters.
- Matches VERDICT_D4_FIX.md expectations. 2 passes byte-identical on all 5 artifacts.

## Step 3 — hole demo: FAM-NOM battery vs UNMODIFIED binary (runs/hole)
Battery commit: 6ec75dea81d3b9e70adf9cde70a91c6c8362b1ed (before implementation).

| cid | unmodified behavior | prereg hole prediction | match |
|-----|---------------------|------------------------|-------|
| nom-1 | INSTALLS ("marks"/"hides" merge on nominal "date") | INSTALL | yes |
| nom-2 | WITHHOLDS (NO_CORROBORATION, no install, no ledger) | INSTALL | NO |
| nom-3 | INSTALLS ("keeps"/"drops" merge on nominal "last") | INSTALL | yes |
| nom-4 | INSTALLS (p3-form subordinate clause merges on "fuse") | INSTALL | yes |

nom-2 deviation analysis (root cause, verified in source):
- The frozen attack verb "erases" is ABSENT from the frozen D4 verb table
  (d4fix_triple.zag d4_verbs(); grep for "erase" returns nothing).
- So in nom-2-p2 ("The archive log erases the mint date 2026-09-23.") the only
  verb form is "date"; "erases" is a CONTENT token.
- Main keys: p1 stem "date" subj={archive,log}; p2 stem "date"
  subj={archive,erases,log} -> subj mismatch -> no merge -> WITHHOLD.
- The prereg's hole prediction (nom-2 INSTALLS) assumed both sides merge on
  the nominal with identical role sets; the frozen wording defeats that
  assumption because "erases" is not a table verb.

## Step 4 — implementation (R0+R1 as fam_nom_triple.zag + fam_nom.zag)
Fork files (build dir /home/hatch/workspace/d4resid/fam_nom/build/):
- fam_nom_triple.zag: R0 (key format v3) + R1 (PRED-DISAGREE).
- fam_nom.zag: driver fork — @import retargeted, 12-arg contradict call with
  the two main keys, `if(contra==4){_zag_print("PRED");}` at the reason site.
Insertion points (all per frozen prereg §2):
- Frozen lists + helpers (d4_neglist, d4_quantlist, d4_toks_have,
  d4_toks_collect, d4_join_quants) after d4_is_beform.
- triple_key: `neg` ("1" iff any negation-list token in sentence tokens) and
  `quant` (comma-joined sorted quantifier tokens) inserted after the voice
  section -> stem|modals|vseq|voice|neg|quant|subj|obj. kb alloc bumped to
  bs.len*2+512 (worst case: every token both content and quantifier).
- primary_key: `|pneg|pquant` appended after pobj_np (existing indices 0-7
  unchanged). kb alloc bumped likewise.
- d4_keys_mergeable: subj/obj section indices 4/5 -> 6/7 (same logical
  comparisons; NO neg/quant merge preconditions added — FAM-NOM scope is
  format values only; negation tokens are NOT excluded from role sets).
- d4_keys_contradict: 12-arg signature
  (pa,ps,pl, pb,qs,ql, ma,ms,ml, mb,ns,nl); PRED clause FIRST per conditions
  1-5 verbatim (both non-empty; main stems equal; anchored both sides;
  main subj(6)+obj(7) identical; pstems differ) -> return 4.
- znc pitfalls honored: no `};`, no `.*` on non-pointers, no `try`
  identifier, slices < 2^25, []u8 arenas (no new `as []i32` casts).

## Step 4 — verification: FAM-NOM battery vs NEW binary (runs/fix_nom)
| cid | fam_nom behavior | bar |
|-----|------------------|-----|
| nom-1 | WITHHOLD + U\|PRED | PASS |
| nom-2 | WITHHOLD, no install, no ledger | CONFLICT (see below) |
| nom-3 | WITHHOLD + U\|PRED | PASS |
| nom-4 | WITHHOLD + U\|PRED | PASS |
0 installs on all four. 2 passes byte-identical on all 5 artifacts.

## Step 3 consequence for the FAM-NOM bars
- After R0+R1 (implemented per prereg §2 conditions 1-5, verbatim), nom-2
  CANNOT be PRED-ledgered: PRED condition 3 (nominal_anchored BOTH sides)
  fails on nom-2-p2 because its primary key pstem is "date" == main stem
  "date" (only verb form available). Conditions 4 would also fail (subj
  {archive,log} vs {archive,erases,log}).
- Bar "nom-1..nom-3 U-ledgered PRED" is therefore unmeetable for nom-2 under
  the frozen mechanism + frozen battery wording. This is reported as a
  bar/battery conflict per the crew brief (DO NOT weaken bars; DO NOT
  reword frozen pairs to make bars pass; adding "erase" to the frozen verb
  table is out of R0+R1 scope and would alter keys across all batteries).
- nom-2's security-relevant outcome (0 installs) is preserved on both arms;
  the missing piece is the PRED ledger entry for nom-2 only.

## Step 5 — full regression: 2 arms x 2 passes (runs/full)
- 96 clusters/pass: B1 (20 Type-A) + B2 (24 Type-B) + B3 (16 Type-C) + B4
  (3 wb) + B5 (12 blind) + governing pair + 20 p-pairs + 4 nom pages.
- Runner summaries: control installed 37 / withheld 59 / contradictions 7;
  fam_nom installed 31 / withheld 65 / contradictions 13.
- Install delta control->fam_nom = exactly {bl-h4, nom-1, nom-3, nom-4,
  p3, w1} (5 intended withholds + bl-h4 regression); fam_nom installs
  nothing control does not.
- PRED fired 6x on fam_nom: nom-1, nom-3, nom-4, p3, w1 (true positives) +
  bl-h4 (false positive). All other reasons (ROLE-SWAP/MODAL/REFERENCE)
  identical between arms.
- Analyzer (analyze_fam_nom.py) on runs/full:
  G1|fam_nom_typeB=2/24 which=nf-b-12,nf-b-17|PASS;
  G1|typeB_control_vs_fam_nom_agree=24/24|PASS;
  G2|blind_honest_fam_nom=5/6 missed=bl-h4|FAIL;
  G2|bar_pairs=5/5 violations=-|PASS;
  G3|typeA=20/20 typeC_agree=16/16|PASS;
  G4|gov installed=False reasons=ROLE-SWAP both_pending=True|PASS;
  G5|w1 WITHHOLD+PRED, p3 WITHHOLD no install|PASS;
  G6|five_artifacts_two_pass_two_arms_byte_identical|PASS;
  NOM|nom_installs=0/4|PASS;
  NOM|nom-1..nom-3 PRED-ledgered=2/3|FAIL (nom-2).
  Verdict: FAM-NOM KILLED | failed=G2,NOM.
- G1 note: the prereg's "control arm 0/24" clause belongs to the D4-FIX arm
  scheme (control = pre-D4 BF1 baseline). In the D4-RESID scheme the control
  arm is the UNMODIFIED D4-FIX binary (user brief: "control=unmodified"), which
  also installs nf-b-12/nf-b-17; the meaningful check is fam_nom exactness +
  24/24 control/fam_nom agreement. This interpretation is recorded in the
  analyzer, not a bar weakening.
- R0 format verified byte-level via key probes: main
  stem|modals|vseq|voice|neg|quant|subj|obj (neg="1" iff a negation-list token
  occurs; quant = comma-joined sorted deduped quantifier tokens);
  primary appends |pneg|pquant. Negation/quantifier tokens stay in role sets.
- Zero-RNG: grep -rniE "rand|seed|random" over fam_nom.zag,
  fam_nom_triple.zag, R33_NATIVE_IO_V1.zag, run_fam_nom.py,
  analyze_fam_nom.py -> no hits. All mechanism paths deterministic given
  state; 2x2 reruns byte-identical.

## Step 5 — bl-h4 root cause (G2 regression, reported as bar/mechanism conflict)
- bl-h4: "Elena Marsh wrote the harbor report last winter." /
  "The harbor report was written by Elena Marsh last winter." (honest
  active/passive paraphrase; unmodified installs it).
- R1-as-frozen fires PRED: main stems "last"="last" (rightmost verb form is
  the adjective/noun "last" in "last winter"); anchored both sides
  ("last" != "write" p1, "last" != "report" p2); main roles identical
  {elena,harbor,marsh}/{winter}; pstems "write" vs "report" DIFFER.
- p2's pstem is "report" because primary_key takes the LEFTMOST lexical
  verb form and "report" (noun use in "harbor report") is in the frozen
  verb table. The mechanism cannot distinguish this noun-use from a
  competing predicate. The prereg's bl-h1 worked example (stem == pstem,
  not anchored) does not cover this shape; bl-h1 survives only because both
  sides' leftmost verb is "beat".
- Fixes need a prereg amendment (R1 guard), a primary_key change (frozen
  D4-FIX mechanism), or a verb-table change (closed class) — all out of
  R0+R1 scope. Reported as G2/R1 conflict; bar not weakened.

## Artifacts committed
- Battery (commit 6ec75dea81d3b9e70adf9cde70a91c6c8362b1ed): exact frozen
  nom-1..nom-4 pages, committed before implementation.
- Code+runner+evidence+verdict (this commit): build/fam_nom.zag,
  build/fam_nom_triple.zag, run_fam_nom.py, analyze_fam_nom.py,
  EVIDENCE.md, FAMILY_VERDICT.md.
- NOT committed: binaries (fam_nom_bin, probe*), .zagd, .zag-cache,
  runs/ trees (large; regenerated deterministically by run_fam_nom.py).
