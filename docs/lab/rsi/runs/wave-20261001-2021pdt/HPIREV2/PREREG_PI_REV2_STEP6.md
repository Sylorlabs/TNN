# PREREG: H-PI-REV2 step 6 alternative-explanation attack plus ablation (FROZEN)

Status: FROZEN (drafted wave-20261001-2021pdt, HPIREV2-S6 lane;
coordinator commits this document alone before any implementation;
commit-order self-check applies; UNVERIFIABLE ORDERING voids this
prereg). No implementation, no baseline build, no execution follows
this freeze in this wave; execution happens in a later wave under
this text. Any further amendment must be committed transparently and
re-frozen before implementation; no bar may be altered after seeing
results. Builders report BUILD-PASS/BUILD-FAIL only.

This prereg defines step 6 of the 11-step promotion pipeline for the
H-PI-REV2 mechanism (pi_revise2/proc_revise2.zag, committed 847a8f10f,
wave-20260929-2321pdt; unchanged), which holds step-5 PASS under the
amended prereg (wave-20261001-2021pdt, 8/8 bars, independent red team:
EVIDENCE HOLDS; original BASELINE-FAIL unchanged; bounded-L2 ceiling,
not L3).

## The step-6 choice and its information-gain ranking

Step 6 is the alternative-explanation attack plus the ablation,
combined into one step, not the OOD test. Step 5's PASS rests on two
load-bearing claims: (a) the revision is genuinely cheaper than
re-search (K-SB2, 5 vs 1055), and (b) the revision reuses beyond mere
storage (K-SB3). Before spending fresh sealed adversary worlds on an
OOD test, the highest-information move is to attack those exact
claims with structurally different alternative explanations and to
ablate the mechanism's load-bearing component. If an alternative
explains the PASS, an OOD test would measure the wrong hypothesis
(mechanism versus new worlds, when the mechanism claim itself is
unproven); if the ablation shows the researcher-authored template
carries the repair, that pins what an OOD test should vary and what
it cannot claim. The attack runs on frozen fixtures, so it is fully
sealed already (adversary byte disjointness inherited), cheaper than
a new sealed battery, and its outcome directly decides whether step 7
OOD is worth running at all. OOD on fresh sealed adversary-designed
worlds remains the next step after this one.

## The question (one mechanism, one question)

Do the two step-5 claims survive their strongest alternative
explanations, and does the SPECIALIZE template carry the repair? Or
is the step-5 PASS explained by (A1) a patch-memory baseline with
class generalization, (A2) template-aware re-search, or does the
ablation (D1) show the template is not load-bearing?

## Provenance

- Mechanism under test: the frozen proc_revise2.zag at 847a8f10f.
- Fixtures T/F1r/F1r-reuse inherited verbatim from the amended
  step-5 prereg (wave-20261001-1721pdt HPIREV2 lane):
  T = ("abc"->"ccc"), ("xy"->"yy"), ("defg"->"gggg");
  F1r = ("rab"->"rrr"), adversary byte 'r' per the frozen
  ADVERSARY_BYTE_SET4.md declaration, disjoint from all frozen
  fixture inputs by that audit;
  F1r-reuse = ("rqw"->"rrr"), held from the revision machinery until
  after the revision completes.
- Frozen K-SB4a expectations (conflict rule updated): the revised
  procedure must satisfy the 5 checks ("abc"->"ccc", "xy"->"xx",
  "defg"->"gggg", "rab"->"rrr", "rqw"->"rrr"), fails=0.
- The step-5 measured facts used as fixed reference points, not
  re-decided here: revision_evals=5; B1 first_fit=-1 with 1055
  evaluated on T+F1r; B1 first_fit=38 with fails-on-T=0 on T alone;
  revised procedure predicts "xy"->"xx" (conflict-rule update).

## The alternatives and the ablation (frozen definitions)

- A1/B3 (class-patch memory, structurally different from B2's exact
  storage): the frozen v1 procedure (index 38 [N C1 SUB]) plus one
  patch learned from the single counterexample F1r, with NO
  diagnosis operator, NO primitive-construction kit, NO SPECIALIZE
  operator, NO conflict rule, NO rollback. The patch is:
  IF(input[0]==114, output = byte 114 repeated to input length,
  v_old(input)). Competence check (negative control): B3 must
  predict F1r ("rab"->"rrr") and F1r-reuse ("rqw"->"rrr") correctly;
  a B3 failing either is a strawman and the run is void, not a kill.
- A2/B4 (template-aware re-search, structurally different from B1's
  plain re-enumeration): re-search over the frozen 1055-program
  benum space in frozen dsearch order, EXTENDED with SPECIALIZE
  template completions: for pos in {0,1,2}, for byte in 0..255
  ascending, candidate = IF(byte-equality(pos,byte), alt_prog,
  v_old) where alt_prog is the first program in frozen dsearch
  order fitting F1r alone, and v_old is the frozen v1 procedure.
  The two streams are concatenated with the 1055 benum programs
  first, then the template completions in the stated order. B4 must
  use no diagnosis, no ranking, no conflict rule. Competence check
  (negative control): B4 must return first_fit >= 0 on T+F1r
  (evaluated against the frozen K-SB4a expectations); a B4 failing
  to solve the set is a broken baseline and the run is void.
  Metric: b4_enumerated = candidates evaluated until the first full
  fit (fails=0 on all 5 checks), or -1 with the full stream count
  if none fits.
- D1 (degraded-mechanism ablation: template excised): the frozen
  revision machinery with the SPECIALIZE template REMOVED and
  nothing else changed. Diagnosis and build_test run normally; the
  final construction may only select among the frozen 1055 programs
  (no IF-template wrapping): D1 selects the first program in frozen
  dsearch order fitting F1r alone, and reports its predictions on
  the 5 frozen checks. Precondition check: D1 must emit the same
  DIAGNOSIS line as the full run ("DIAGNOSIS pos=0 byte=114
  conflicts=0"); a D1 with altered diagnosis is a different ablation
  and the run is void.

## Frozen kill bars (all must pass for step-6 PASS)

Preserved step-5 bars (the full mechanism M must re-satisfy all of
them on the frozen fixtures; thresholds unchanged):

- K-SB1 (problem real): B0-equivalent check inherited: the frozen
  v1 procedure mispredicts F1r ("bbb", not "rrr"). Kill: "rrr".
- K-SB2 (revision cheaper than re-search): revision_evals=5 <
  b1_enumerated=1055, strict. Kill: revision_evals >= 1055.
- K-SB3 (revision beats storage on reuse): revised procedure
  predicts "rqw"->"rrr" with zero new revisions. Kill: any new
  DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION line after the reuse check.
- K-SB4a (revised procedure correctness): fails=0 across the 5
  frozen checks. Kill: any misprediction.
- K-SB4b (baseline competence): B1 over T alone first_fit >= 0,
  fails-on-T=0. Kill: first_fit < 0 or any misprediction on T.
- K-SB4c (verified-impossibility recheck): B1 over T+F1r
  first_fit=-1, programs-enumerated=1055. Kill: any deviation.
- K-SB5 (determinism): every run 3/3 byte-identical (sha256 match),
  exit 0, zero stderr bytes. Amended run matrix: 12 runs total
  (M revision x3, B3 x3, B4 x3, D1 x3). Kill: any divergence,
  nonzero exit, or any stderr byte.
- K-SB6 (purity and docs): pure Zag only; zero Python at any stage;
  zero em-dash and zero en-dash bytes in all lane files
  (byte-checked). Kill: any Python use or any forbidden byte.

New alternative-explanation kill bars (step-6 PASS requires the
alternatives to be KILLED here):

- K-AX1 (conflict rule is not a patch): B3 predicts "xy"->"yy"
  (v1 untouched outside the patch), while the revised procedure
  predicts "xy"->"xx" per frozen K-SB4a. Bar: B3's prediction on
  "xy" != "xx". Kill (step-6 FAIL): B3 predicts "xx", meaning the
  class-patch baseline reproduces the full mechanism's behavior on
  every frozen probe and the alternative explanation stands.
- K-AX2 (diagnosis beats template-aware search): B4 achieves
  first_fit >= 0 on T+F1r (competence, else void per the definition
  above), and b4_enumerated > revision_evals (5). Kill (step-6
  FAIL): b4_enumerated <= 5, meaning template-aware re-search
  matches or beats diagnosis-driven construction and the K-SB2
  efficiency claim is explained away by search-space completeness;
  the honest outcome is a downgrade of the efficiency claim, not a
  salvage.

New ablation bar (step-6 PASS requires the degradation to appear):

- K-ABL1 (template is load-bearing): D1 fails >= 1 of the 5 frozen
  checks (fails_total >= 1). Kill (step-6 FAIL): D1 achieves
  fails_total=0, meaning the SPECIALIZE template is not load-bearing
  and the bounded-L2 ceiling statement (the authored template
  carries the repair) is falsified as stated; the ceiling must be
  revised, not patched.

Architecture bars:

- K-ARCH1 (zero cognition source delta): the frozen mechanism
  source (proc_revise2.zag at 847a8f10f) is byte-identical before
  and after; cognition source delta = 0 exactly. Baseline and
  ablation sources are throwaway test harness code, recorded
  separately. Kill: any nonzero cognition source delta.
- K-ARCH2 (no architecture growth): new_semantic_cases=0,
  new_modes=0, new_bridges=0, new_routers=0, new_handlers=0; no
  protected-core changes. Kill: any nonzero value.

## Sealed evaluation design and adversary protocol

- No new post-freeze adversary worlds are required for step 6: the
  attack targets claims about frozen fixtures, and the seal is the
  frozen fixture set plus the inherited adversary-byte disjointness
  audit. Step 7 (OOD) is where post-freeze adversary-designed
  worlds enter.
- The alternative and ablation implementations are written
  post-freeze from this prereg text only. Code-sharing disclosure
  is mandatory in the result doc: B3 may reuse only the frozen v1
  procedure code; B4 may reuse only the frozen benum algorithm and
  the template shape stated here; D1 is the frozen machinery with
  the template excised (disclose the exact excised line ranges).
  No Section B revision-machinery code (diagnose, build_test,
  specialize, conflict rule, rollback) may appear in B3 or B4; the
  red team audits for leakage.
- The F1r-reuse input "rqw" remains held from every constructor
  until after its revision or patch is complete; the phase that
  presents it must not run before the revision/patch ACTIVE marker.
- Competence checks (B3 on F1r/F1r-reuse, B4 first_fit >= 0, D1
  DIAGNOSIS line) are void-on-failure, not kills: they validate the
  alternatives as strong, not strawman, before the kill bars judge.

## Cost accounting (required in the result doc)

Machine-greppable fields: revision_evals, b1_enumerated,
b3_correct_f1r, b3_correct_reuse, b3_predict_xy,
b4_first_fit_index, b4_enumerated, b4_wall_ms, b3_wall_ms,
d1_fails_total, d1_predict_xy, revision_wall_ms, binary_bytes (each
binary), source_delta_lines (test harness only),
cognition_source_delta (must be 0), new_semantic_cases, new_modes,
new_bridges, new_routers, new_handlers. Kill: any missing field;
any nonzero architecture-growth field; any nonzero
cognition_source_delta.

## Honest boundaries: bounded L2 ceiling, NOT L3

Step 6 does not test representational invention. A step-6 PASS means
the efficiency and reuse claims survive their strongest frozen-fixture
alternatives and the authored template is confirmed load-bearing; it
is not evidence toward L3 and must not be claimed as such. If K-AX2
kills, the honest verdict is a downgraded efficiency claim, recorded
as information gained, never salvaged by redefining the comparator.
If K-ABL1 kills, the ceiling statement is revised, not patched.

## Pipeline position statement

Steps 1-5 established: (1) committed preregistration across frozen
preregs; (2) implementation (F3a3 BUILD-PASS on corrected bars);
(3) sealed evaluation on frozen fixtures with the adversary byte;
(4) independent reproduction (byte-identical transcript match,
independent red-team re-runs); (5) simple-baseline comparison
(step-5 PASS, 8/8 amended bars, EVIDENCE HOLDS, original
BASELINE-FAIL unchanged). Step 6 establishes (6) the
alternative-explanation attack and (8) the ablation, combined:
whether the PASS survives structurally different alternatives and
which component carries the effect. Remaining for SURVIVES: (7) OOD
test on fresh sealed adversary-designed worlds, (9) transfer/reuse
test beyond the single reuse probe, (10) a second independent red
team over the full chain, (11) governance audit. A step-6 verdict is
PASS or FAIL on the attack; it is never SURVIVES.

## Verdict semantics

step-6 PASS: all preserved bars hold for M, K-AX1 and K-AX2 kill
their alternatives, K-ABL1 shows the expected degradation, K-ARCH1
and K-ARCH2 hold. Any kill bar tripped: step-6 FAIL with the tripped
bar named; the step-5 PASS record is not retroactively altered. This
prereg governs only the step-6 execution; no bar may be moved after
results are seen.

No em-dashes in this documentation.
