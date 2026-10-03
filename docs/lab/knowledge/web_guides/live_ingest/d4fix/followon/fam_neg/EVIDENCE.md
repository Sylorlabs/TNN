# FAM-NEG evidence log

Crew: D4-RESID FAM-NEG (R0 key-format v3 + R2 NEGATION).
Prereg: PREREG_D4_RESID.md, frozen commit 235152e8247c542480560b0c5317616e4083e2ca.
Base code: d4fix @ 5aef8c16 (repo-fetched sources byte-identical to
/home/hatch/workspace/d4resid/build0/).
Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.

## Step 1 — unmodified rebuild + hole demonstration

Unmodified sources rebuilt -> `orig_bin` (warnings OK, same 17 analyzer
warnings as baseline). Smoke B4+B5 + blind battery reproduced D4-FIX
behavior: w2/w3/bl-a1/bl-a2/bl-a6 ledgered with correct reasons
(ROLE-SWAP/MODAL/REFERENCE).

Hole (run_hole2, orig_bin, `run_hole2/fam_neg/pass1/`):
- bl-a3: WITHHOLD (NO_CORROBORATION), NO undetermined-ledger entry.
  ("did not build"/"built" withholds only by accidental key mismatch.)
- neg-1..neg-4: WITHHOLD, no installs, no ledger entries.
- neg-h1/neg-h2: WITHHOLD, no installs (honest negatives fail to merge:
  "not"/"never" pollute the role sets -> key mismatch).
- w1: INSTALLS (R1 nominal-verb hole; out of FAM-NEG scope, unchanged).

## Step 2 — implementation (R0+R2 only)

Forks: `fam_neg_triple.zag`, `fam_neg.zag` (driver; only the
`@import` retarget + `if(contra==5){_zag_print("NEGATION");}` differ).

R0 (key format v3):
- `d4_negations()` = "not never no none nobody nothing neither"
- `d4_quants()` = "all every each some many few several most any
  one two three four five six seven eight nine ten"
- Main key: stem|modals|vseq|voice|neg|quant|subj|obj
  (neg="1" if any negation-list token anywhere in sentence tokens else "";
   quant=comma-joined sorted quantifier tokens else "").
- Primary key: pstem|pmodals|psubj|pobj|pvoice|pargbag|psubj_np|pobj_np|pneg|pquant.
- Quantifier tokens STAY in role sets (R3's rule strips them; not implemented here).

R2:
- (a) `d4_is_content` now returns 0 for negation-list tokens (negation lives
  only in neg/pneg, mirroring modal verb-forms).
- (b) `d4_keys_mergeable`: neg sections (4) unequal -> return 0; subj/obj
  indices shifted 4,5 -> 6,7 for the v3 layout.
- (c) `d4_keys_contradict`: NEGATION clause after codes 1-3 — inside the
  modals-equal branch, when psubj AND pobj are equal and pneg sections (8)
  differ -> return 5. (Restructured the branch so the check sits textually
  after the ROLE-SWAP/REFERENCE checks; behavior of codes 1-3 unchanged.)
- (d) Driver prints NEGATION for contra==5; runner treats it as an opaque
  reason string (no ledger format changes).

Keydump probe (`keydump` binary, temporary): verified v3 sections, e.g.
"The Harborlight crew did not build the new pier last winter." ->
T|last||did,build,last|A|1||arborlight,crew,he,new,pier|winter
P|do||arborlight,crew,he|new,pier,winter|A|arborlight,crew,he,new,pier,winter|arborlight,crew|new,pier,winter|1|
("he" for "the" is a pre-existing baseline tokenizer quirk, identical in
unmodified keydump.)

Bug caught during implementation: when the neg/pneg section was empty the
code advanced the key cursor without writing a byte, leaving uninitialized
heap garbage in the key. Fixed (`if(ng==1){kb[oo]=49; oo=oo+1;}`); keydump
verified clean keys afterwards.

## Frozen-battery vs frozen-mechanism findings (reported, not worked around)

The prereg's worked predictions assume facts that do not hold in the frozen
code/battery. The mechanism is implemented exactly as specified; the
following bars cannot pass on the frozen pairs for mechanical reasons:

1. neg-1 / bl-a3 ("did not build"/"built"): the frozen NEGATION clause is
   gated on primary-key pstem equality. The primary verb of "The
   Harborlight crew did not build ..." is "did" (stem "do"; leftmost lexical
   verb with non-empty content subject+object per frozen primary_key), while
   the other side's is "built" (stem "build"). pstem "do" != "build", so the
   clause can never fire. The prereg's "pstem 'build' both" does not hold.
   Outcome: WITHHOLD, 0 installs, no ledger (same as the hole, now via the
   explicit neg-merge precondition instead of accidental mismatch).
2. neg-2 ("approved") / neg-3 ("emitted"): these verb forms are ABSENT from
   the frozen d4_verbs table -> empty keys -> M4 byte-fallback refuses ->
   WITHHOLD, no ledger possible under the frozen mechanism.
3. neg-4 ("none"/"all"): "none" is excluded from p1's roles per R2a, but
   "all" STAYS in p2's roles per the frozen spec ("Quantifier tokens STAY in
   role sets"), so pobj differs -> NEGATION clause fails. QUANT rule is
   FAM-QUANT's (explicitly not implemented here). Outcome: WITHHOLD,
   0 installs, no ledger.
4. neg-h2 ("filed"): "filed" is absent from the frozen verb table, so p2
   ("The night crew never filed the log entry.") has an empty key and cannot
   merge -> WITHHOLD, no install. The INSTALL bar cannot pass as frozen.
5. neg-h1 ("did not build"/"never built"): INSTALLS (both sides negated,
   roles equal after R2a exclusion). PASS.

Crew-added extra pairs (prereg allows up to 4, documented in
battery/BATTERY_NOTES.md) use in-table verbs to exercise R2 end-to-end:
neg-5/neg-6 (attacks, expect NEGATION ledger), neg-h3/neg-h4 (honest, expect
INSTALL).

G5 note: w1 and p3 still INSTALL (R1 nominal-verb hole; no negation-list
tokens in either cluster, so R2 cannot change them). G5 as literally written
requires FAM-NOM's mechanism; reported as baseline-unchanged, not a
FAM-NEG regression.

## Regression guard

Grepped all honest battery sentences (B1 Type-A/B snapshots, B5 h1..h6,
neg-h1/neg-h2) for whole-word negation-list tokens:
- B1: 4 hits, all fixture distractor meta-sentences in nf-b-18 ("repeat"
  not a verb -> empty keys before and after) and nf-b-19 ("writes"/"uses"
  stems differ -> never merged). No honest merging pair affected.
- B5 h1..h6: 0 hits.
- neg-h1/neg-h2: only the intended claim sentences (both sides negated ->
  neg sections equal -> merge).
No honest merging pair is split by the neg rule.

## Full regression (run_full)

B1 (60) + B2 (p1..p4) + B3 (s1 h1..h6/a1..a6) + B4 (w1..w3) +
B5 (blind h1..h6/a1..a6) + gov-wolves + neg battery (10 clusters),
2 arms (control, fam_neg) x 2 passes.
Analyzer: analyze_fam_neg.py (G1-G6 + family bars). Results below.

## Addendum — prereg-level conflict: R2 worked prediction for bl-a3 is a mis-trace

Independently flagged by sibling FAM-DV crew (hex key-dump verified) and
confirmed in this build via the `contra` probe (primary keys + exact
d4_keys_contradict return code):

- Frozen `d4_stem_lexical` (fam_neg_triple.zag:153-161) excludes ONLY
  {will,can,shall,may,must,be}. It does NOT exclude "do".
- For bl-a3 p1 ("The Harborlight crew did not build the new pier last
  winter."), primary_key's leftmost lexical verb with non-empty content
  subject+object is "did" -> stem "do". Probe: PA=`P|do||...|1|`, PB=`P|build||...||`.
- Frozen R2 NEGATION clause requires pstem equality (gated with codes 1-3).
  "do" != "build" -> d4_keys_contradict returns 0. NEGATION can NEVER fire
  on bl-a3 as specified. Probe: CONTRA|0, MERGE|0 (neg sections "1" vs "").
- The prereg's worked prediction ("pstem 'build' both") is factually wrong
  about the frozen code's output on the frozen sentence. Per contract, the
  frozen code wins over the worked prediction; no fix invented here (in
  particular: "do" NOT silently excluded, clauses NOT reordered).
- Integration note (FAM-DV measurement, not re-verified here — PRED is not
  implemented in this R0+R2-only build): under R0+R1, PRED fires on bl-a3
  first and would preempt NEGATION in an integrated build. This is reported
  for the integration crew; the likely amendment (exclude dummy-auxiliary
  "do" from primary_key candidacy + a PRED/NEGATION clause-ordering rule)
  is pending parent approval.

Per-pair attack characterization (probe-verified, `contra` mode):
- neg-1 (same sentences as bl-a3): CONTRA=0 — pstem "do" vs "build".
- neg-2: CONTRA=0 — BOTH primary keys empty ("approved" absent from frozen
  d4_verbs table; keydump shows PA| / PB| empty).
- neg-3: CONTRA=0 — both empty ("emitted" absent from frozen verb table).
- neg-4: CONTRA=0 — pstem "hold" equal, psubj equal, but pobj differs
  ({charts,original} vs {all,charts,original}): "all" STAYS in p2's roles
  per the frozen R2 spec, so the pobj-equality gate fails. QUANT rule is
  FAM-QUANT's, explicitly out of scope.
- neg-5 / neg-6 (crew extras, in-table verbs): CONTRA=5 (NEGATION fires),
  MERGE=0 — the mechanism works exactly as specified where the frozen
  battery lets it engage.
Honest pairs: neg-h1 MERGE=1 (installs); neg-h2 MERGE=0 ("filed" absent ->
p2 empty key -> cannot install); neg-h3/neg-h4 MERGE=1 (install).

End-to-end (run_full, fam_neg arm, 2x byte-identical passes): neg-5/neg-6
ledgered NEGATION with 0 installs; neg-1..neg-4 and bl-a3 withhold with 0
installs and NO undetermined-ledger entry; neg-h1 installed; neg-h2
withheld. Failing bars are reported as FAIL, not worked around.

## Methodology correction (2026-09-25): control binary

The first full run mistakenly used
`/home/hatch/workspace/tnn-lab/knowledge/web_guides/live_ingest/d4/src/control_bin`
(a stale 244KB binary from the D4-FIX crew's tree, SHA 130afea0...) as the
control arm. The correct control is `orig_bin` — built in this workdir from
the repo-fetched D4-FIX @ 5aef8c16 sources (byte-identical to build0/).
run_fam_neg.py now points the control arm at `orig_bin`; the full run was
redone (run_full deleted and regenerated). Note the stale control_bin does
NOT merge bl-h1's honest sentences while true 5aef8c16 does (probe:
unmodified MERGE=1, CONTRA=0) — all shared-guard comparisons below are
against the true baseline.

## Full regression (run_full, corrected)

102 clusters x 2 arms (control=orig_bin unmodified 5aef8c16,
fam_neg) x 2 passes. All 5 artifacts byte-identical across passes in both
arms (DETERMINISM|PASS). Analyzer output (analyze_fam_neg.py):

G1|fam_neg_typeB=2/24 which=nf-b-12,nf-b-17|PASS
G1c|control_typeB=2/24 nf-b-12,nf-b-17; fam_neg matches|PASS
G2|blind_honest_fam_neg=6/6|PASS  (control also 6/6)
G2b|attack_pairs ledgered=5/5 ROLE-SWAP/MODAL/REFERENCE, none installed|PASS
G3|typeA 20/20 both arms; typeC 16/16 identical|PASS
G4|gov-wolves ROLE-SWAP ledgered, not installed|PASS
G5|w1=INSTALL, p3=INSTALL (R1 hole; out of FAM-NEG scope; baseline-unchanged)
G6|byte-identical + zero-RNG grep|PASS
NEG-neg-1..neg-4: 0 installs OK; NEGATION ledger MISSING (FAIL, see conflict)
NEG-neg-h1: INSTALL|PASS
NEG-neg-h2: INSTALL|FAIL ("filed" absent from frozen verb table)
NEG-bl-a3: WITHHOLD OK; NEGATION ledger MISSING (FAIL, see conflict)
NEGX-neg-5/neg-6: NEGATION ledgered, 0 installs|PASS
NEGX-neg-h3/neg-h4: INSTALL|PASS
LEDGER|fam_neg_pairs=9|reasons=MODAL=2,NEGATION=2,REFERENCE=1,ROLE-SWAP=4

Arm install diff (fam_neg minus control): +neg-h1, +neg-h3, +neg-h4
(exactly the honest negated pairs R2a un-breaks). Nothing that installed
under control withholds under fam_neg. Strictly additive, zero regressions.
