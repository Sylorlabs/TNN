# PREREG: H-PI-REV2 step 5 simple-baseline comparison (FROZEN)

Status: FROZEN this wave (wave-20261001-1121pdt), writing-only lane.
No implementation, no baseline build, no execution follows this freeze
in this wave; execution happens in a later wave under this text. Any
amendment must be committed transparently and re-frozen before
implementation; no bar may be altered after seeing results. Builders
report BUILD-PASS/BUILD-FAIL only.

This prereg supplies the frozen baseline bar text the 02:21 wave found
missing (LOOP_STATE.md wave-20261001-0221pdt: "No frozen baseline bar
text exists in any prereg or the M5 debate record; inventing bars
post-hoc is forbidden"). It is step 5 of the 11-step promotion
pipeline for the H-PI-REV2 BUILD-PASS mechanism (F3a3, BUILD-PASS on
corrected bars K-F3-1..4, independently reproduced in step 4). On all
bars passing, the verdict is step-5 PASS (the baseline comparison is
survived), never SURVIVES; the pipeline continues to step 6.

## Provenance

NEW prereg, written by the inline worker for wave-20261001-1121pdt.
Mechanism under test: pi_rev2/proc_revise2.zag (committed 847a8f10f,
wave-20260929-2321pdt; unchanged). Fixtures T/F1/R inherited from
PREREG_PI_REV2.md (wave-20260929-1721pdt design lane). Adversary byte
'r' per the frozen declaration in
docs/lab/rsi/runs/wave-20261001-0221pdt/pi_rev2/ADVERSARY_BYTE_SET4.md
(set {k,m,r}; standing selection rule: last letter in sorted byte
order, per F3a2/F3a3 convention). Byte 'r' is disjoint from every
frozen fixture input string by that audit.

## The question (one mechanism, one question)

Does the revision machinery (diagnosis operator, primitive-construction
kit, SPECIALIZE revision operator, conflict rule, rollback) beat
simpler alternatives on the counterexample-driven revision task, or is
the F3a3 BUILD-PASS explained by machinery any baseline would match?

## Frozen fixtures

- T (Family X training, inherited): ("abc"->"ccc"), ("xy"->"yy"),
  ("defg"->"gggg"). v1 discovery finds index 38 [N C1 SUB].
- F1r (this prereg's counterexample, adversary byte 'r'):
  ("rab"->"rrr"). The v1 procedure predicts "bbb" (broadcast-last of
  the input's last byte class); the correct output is "rrr".
- F1r-reuse (held from the revision machinery until after revision):
  ("rqw"->"rrr"). Tests within-class reuse of the revised procedure
  with no further revision. Disjoint input string from F1r, same byte
  class.

## The three baselines (frozen here)

- B0 (no-revision control): the frozen v1 procedure (index 38
  [N C1 SUB]) applied to F1r unchanged. Sanity control: establishes
  the revision problem is real.
- B1 (full re-enumeration): the discovery enumeration benum (1055
  programs, byte-identical algorithm to the frozen v1 discovery) run
  over the augmented set T+F1r, taking the first program fitting all
  examples. This is the simpler alternative the revision operator must
  beat: brute-force re-search instead of structural revision. Metric:
  programs enumerated until the first full fit, plus wall time.
- B2 (memorization control): an explicit exception table storing
  ("rab"->"rrr") as a lookup, with the v1 procedure handling all other
  inputs, and no structural revision. This is the L0-storage control:
  the revision machinery must do better than mere storage, measured on
  F1r-reuse.

All baselines are pure Zag, deterministic, and run under the pinned
znc. The revision run is the frozen proc_revise2.zag binary with
argv[1]="r" (the F2-style phase, per the frozen interface), executed
exactly as in the F3a3 evidence.

## Frozen kill bars (all must pass for step-5 PASS)

- K-SB1 (problem real): B0 mispredicts F1r (predicts "bbb", not
  "rrr"). Kill: B0 predicts "rrr" (the revision problem is vacuous).
- K-SB2 (revision cheaper than re-search): the revision operator's
  total candidate evaluations (diagnosis (p, byte) candidates ranked
  plus primitive-construction byte-equality tests plus the single
  SPECIALIZE application) is strictly less than B1's programs
  enumerated until its first full fit on T+F1r. Kill: revision
  evaluations >= B1 enumerations (revision adds no efficiency over
  re-search).
- K-SB3 (revision beats storage on reuse): the revised procedure
  predicts F1r-reuse ("rqw"->"rrr") correctly with zero new revisions
  (no new DIAGNOSIS, no new primitive construction, no new version);
  B2 mispredicts "rqw" (it has no stored entry for it) or requires a
  new stored entry to get it right. Kill: the revision machinery
  needs a new revision for "rqw", or B2 predicts "rrr" for "rqw"
  without storing it.
- K-SB4 (correctness parity): the revised procedure is correct on all
  of T (with updated expectations per the frozen conflict rule),
  F1r, and F1r-reuse. B1's fitted program is correct on T+F1r.
  Kill: any misprediction by the revised procedure on T/F1r/F1r-reuse,
  or any misprediction by B1's fit on T+F1r.
- K-SB5 (determinism): the revision run and each baseline run execute
  3/3 byte-identical (sha256 match), exit 0, zero stderr bytes on
  every run. Kill: any divergence, nonzero exit, or any stderr byte.
- K-SB6 (purity and docs): pure Zag only; zero Python at any stage
  (implementation, build, run, analysis); zero em-dash and zero
  en-dash bytes in all lane files (byte-checked). Kill: any Python
  use or any forbidden byte.

## Honest boundaries: bounded L2 ceiling, NOT L3

The revision machinery repairs a supplied procedure after a
counterexample; it does not invent a representation, and the
reconstruction template (SPECIALIZE as IF(P_test, alt, v_old)) is
researcher-authored. A step-5 PASS means the revision is genuinely
cheaper than re-search and genuinely reuses beyond storage; it is not
evidence toward L3 and must not be claimed as such. No protected-core
changes. No new dedicated semantic cases.

## Sealing protocol

- The adversary byte 'r' is frozen here and is disjoint from all
  frozen fixture inputs by the ADVERSARY_BYTE_SET4.md audit.
- The F1r-reuse input "rqw" is held from the revision machinery until
  after the revision completes; the phase that presents it must not
  run before the revision's CONVERGE-equivalent marker.
- The baseline implementations must not share code with the revision
  machinery beyond the frozen benum algorithm (B1) and the frozen v1
  procedure (B0, B2); the executor discloses any shared code in the
  result doc and the red team audits for leakage.

## Cost accounting (required in the result doc)

The result doc must contain machine-greppable fields: revision_evals
(total candidate evaluations), b1_enumerated (programs to first fit),
b1_wall_ms, revision_wall_ms, binary_bytes (each binary), plus
source_delta_lines, new_semantic_cases, new_modes, new_bridges for any
new code written. Kill: any missing field; any nonzero
new_semantic_cases, new_modes, or new_bridges.
