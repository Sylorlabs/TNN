# Tooling Contamination Register

Date: 2026-09-30. Worker: Tooling Contamination Auditor.
Verdict label: TOOLING-AUDIT-COMPLETE.

## Audit standard

Micah's tooling ruling (2026-09-30): ONLY Zag may implement research
logic. No Python, C/C++, JavaScript, Rust, or other language for
scratch experiments, generators, analyzers, verifiers, mirrors,
fixture construction, scientific calculations, or editing helpers.
Shell/git exist only as unavoidable orchestration: invoke znc,
execute Zag binaries, git operations, move/copy files. Shell/awk/sed/
grep scripts must not serve as substitute research programs. If
scientific evidence depends on computation, parsing, generation,
scoring, verification, hashing logic, etc., that logic belongs in
Zag. Important prior results whose scientific logic depended on a
prohibited-language implementation remain contaminated until
independently reproduced in pure Zag. Python-mirror-developed logic
may NOT be adopted.

## Disposition key

- CLEAN: scientific logic in pure Zag; no prohibited-language
  dependence. May carry a process note.
- NEEDS-RERUN: scientific logic depended on a prohibited language.
  The claim is contaminated until independently reproduced in pure
  Zag. Underlying data is intact; a Zag reimplementation of the
  driver/scorer can re-derive the result.
- NON-CANONICAL-OK: contaminated, but the result's standing already
  reflects it (PROCESS-FAIL, superseded, or a negative finding whose
  evidential weight does not depend on the contamination). No rerun
  required unless the result is promoted.

## Part 1: Python incidents in this cycle

Four recorded Python process incidents. Disclosure does not cure use.

1. C55 (OpScope displacement): one inadvertent python3 heredoc during
   setup, placeholder only, no artifact. Disclosed in the ledger;
   purity not asserted as fully clean for this lane. The scientific
   finding (position-contingent negation) rests on Zag binary outputs.
   Disposition: NON-CANONICAL-OK (disclosed caveat travels with the
   entry; the lane is closed per the gate-lineage ruling).

2. L3A trace original build (a6fbee865): python3 heredoc patched a
   /tmp scratch file during diagnostic debugging. K3 process FAIL;
   technical findings preserved as exploratory only. Superseded by
   the C70 clean rebuild. Disposition: NON-CANONICAL-OK (superseded;
   do not cite).

3. C67 (learner-dev P12): python3 invocation for the F3 literal
   audit. Status PROCESS-FAIL; the previously reported
   LEARNER-DEV-PASS is governance-invalidated. The C74 compression
   successor resolved the architectural debt but explicitly did not
   cure the process failure. Disposition: NON-CANONICAL-OK (standing
   already reflects the failure; no clean rebuild warranted under
   the one-system rule).

4. C77 (L3A-trace red team): one python3 invocation during Attack 5
   setup (text insertion into a probe file); the file was deleted,
   recreated from pristine source, and redone with awk. No
   Python-derived content remains in committed files. Note: the
   redo used awk for fixture construction, which the new ruling
   also prohibits (no awk for fixture construction). The verdict is
   ADVERSARY-BREAKS, a negative finding: the tie-break fragility
   and reify capacity bug were demonstrated by running the Zag
   binary, not by the Python/awk step. Disposition: NON-CANONICAL-OK
   (the break stands as a negative finding; the process blemish is
   recorded; no rerun needed unless C70 is re-promoted).

An earlier audit (docs/lab/research-lead/overnight-20260928/
python_audit/PYTHON_AUDIT.md) catalogued 11 additional violations
from earlier waves; those are outside this audit's scope except
where they touch the claims below. None of C64-C77 depend on them.

## Part 2: Shell/awk as substitute research programs

The new ruling explicitly prohibits shell/awk/sed/grep scripts as
substitute research programs. The following were found doing
scientific work:

A. score_probes.sh (core_freeze/run_phase/): parses QUERY lines from
   world files and ANSWER lines from binary stdout with grep/awk,
   joins them, and computes per-world scores (OK/MISS, SCORE n/m).
   The Core Freeze Challenge's 1/9 WORLD-PASS verdict and every
   per-world score (W1 10/12, W2 0/8, W3 0/10, W4 1/6, W5 1/2,
   W6 1/5, W7 0/4, W8 0/5, W9 0/28) were derived by this script.
   Scoring logic in shell/awk is exactly what the ruling prohibits.
   The underlying data (sealed world files, frozen binary outputs
   in battery/) is intact. Disposition: NEEDS-RERUN. A pure-Zag
   scorer must re-derive all nine world scores from the frozen
   artifacts before the 1/9 result can be canonically cited under
   the new ruling. This is the highest-priority rerun: the freeze
   challenge is the central architectural benchmark.

B. run_race.sh (c1_fe_family/, 147 lines; identical copy in
   c1_baseline/runs/): implements JSON parsing (jget/jgeti via
   grep/sed), the causal simulation of the experimental world
   (causal_sim: the true-graph semantics for P/Q/R updates), query
   scoring against key.json (expected_for, N_CORRECT), and stage
   score aggregation. The scientific model of the experiment and
   the scoring both live in shell. Every C1-family numeric claim
   depends on it: C1 clean 63/63, the F-E family 24/24 misses,
   C76 small-k 24/24 hits, the C1 reproduction 63/63 and 30/30
   byte-identical files, and the in-progress C1 baseline. The Zag
   contestant binary is clean; the contamination is in the driver/
   scorer. Disposition: NEEDS-RERUN. The race driver (world
   simulation + scoring) must be reimplemented in pure Zag and the
   C1 results re-derived. Affects C76 directly as a ledger claim.

C. drive_smallk.sh (c1_smallk/): sequences the small-k runs and
   derives the summary counts (R1 HIT-OK etc.) via grep -c over the
   diag output. Scoring aggregation in shell. Depends on the
   run_race.sh outputs. Disposition: NEEDS-RERUN (with B).

D. run_l3b_v2.sh (l3b_v2/): compiles and runs the Zag binary 3x
   (orchestration, allowed), byte-compares with cmp (verification),
   then derives the L3B-V2 verdict by grepping the binary's own
   V2-BAR PASS lines, and runs source audits (V2-AUD-A/B/C) via
   sed/grep. The scientific evaluation (all bars) is performed by
   the Zag binary and printed as verdict lines; the shell only
   aggregates them. The source audits are shell verifiers, which
   the ruling prohibits as a category, but they are governance
   defense-in-depth: the L3B claims do not depend on them.
   Disposition: CLEAN with process note. The claims stand; the
   source audits should be reimplemented in Zag for full
   compliance, but no scientific result depends on them.

E. audit_edit.sh (causal_editinvent/): source audit via grep
   verifying the invented edit type is absent from source. A shell
   verifier (prohibited as a category), but the C65 scientific
   claim (the learner constructed EXTEND-DELAY) is evidenced by
   the Zag binary's behavior, not by this audit. Disposition:
   CLEAN with process note. Same remedy as D.

F. run.sh (l3c_v3/): builds, runs the Zag binary 4x, checks
   determinism with cmp, records sha256sums. Pure orchestration
   and byte-identity verification. The scientific logic is in the
   Zag binary. Disposition: CLEAN.

G. Governance audit hash verification (core_freeze/
   governance_audit/): sha256sum and grep used to verify the
   binary/source/world seals. The ruling lists hashing logic as
   belonging in Zag when scientific evidence depends on it. These
   are governance controls on frozen artifacts, not cognitive
   performance evidence. Disposition: CLEAN with process note.
   A Zag seal-verifier would remove all doubt for future freezes.

H. check_no_dash.sh (worker_snippets/): documentation hygiene
   (em-dash detection in markdown). Not scientific logic.
   Disposition: CLEAN. Explicitly within the audit brief's
   allowance.

## Part 3: Claim-by-claim register (C64-C77)

- C64 L3B-V2-ADV-BOUNDED: ledger records "Pure Zag"; adversary
  harness made no source changes. Disposition: CLEAN (see D).
- C65 CAUSAL-EDITINVENT-PASS: ledger records "Pure Zag".
  Disposition: CLEAN (see E).
- C66 L3C-V2-ADV2-SURVIVES-THIS-ROUND: ledger records "Pure Zag".
  Disposition: CLEAN.
- C67 LEARNER-DEV-P12: PROCESS-FAIL (Python incident 3).
  Disposition: NON-CANONICAL-OK.
- C68 L3B-V2-ROBUST-PASS: ledger records "Pure Zag".
  Disposition: CLEAN.
- C69 OPSCOPE-BEHAV-PASS: ledger records "Pure Zag".
  Disposition: CLEAN.
- C70 L3A-TRACE-CLEAN-BUILD-PASS: ledger records zero Python for
  any purpose including diagnostics and /tmp scratch. Qualified
  by C77 (verdict measures byte-reproduction, not learning).
  Disposition: CLEAN (build fidelity; evidential weight qualified
  by C77, not by tooling).
- C71 EDITINVENT-ADV-BREAKS: ledger records "Pure Zag".
  Disposition: CLEAN.
- C72 HYPD-V3-PASS: ledger records "Pure Zag"; no shell scripts
  in the lane; the Zag binary produces all scores. The em-dash
  blemish is in the prereg document text, not a tooling
  contamination of scientific logic. Disposition: CLEAN.
- C73 L3C-V3-PASS: ledger records "Pure Zag". Disposition: CLEAN
  (see F).
- C74 COMPRESSION-PASS: ledger records "Pure Zag". Disposition:
  CLEAN.
- C75 EVICTION-TIE-BREAKER-PATHOLOGY: the mechanism finding (the
  OBSERVED/EVICT signature, the tie-breaker analysis) is a direct
  observation of frozen binary stdout and white-box source
  reading; it does not depend on score_probes.sh. The revised
  W4/W5 score numbers do depend on the contaminated scorer (see
  A). Disposition: CLEAN for the mechanism finding; the score
  revisions inherit the NEEDS-RERUN of A.
- C76 SMALLK-REVISION-CONFIRMED: the 24/24 claims depend on
  run_race.sh scoring and drive_smallk.sh aggregation (see B, C).
  Disposition: NEEDS-RERUN.
- C77 L3A-TRACE-REDTEAM-BREAKS: Python incident 4 plus awk fixture
  construction. Disposition: NON-CANONICAL-OK (see incident 4).

## Part 4: Major results register

- Core Freeze Challenge run phase (97b28e6a6): NEEDS-RERUN (see A).
  The worlds, the frozen binary, and the outputs are intact; only
  the scoring step needs a pure-Zag reimplementation. Priority:
  highest.
- C1 reproduction (140f49eb4): NEEDS-RERUN (see B). The 63/63
  scores and byte-identity claims depend on run_race.sh.
- F-E family baseline (6e03b2fa5): NEEDS-RERUN (see B).
- C1 simple baseline (in progress): uses the identical
  run_race.sh; its results will be contaminated on arrival unless
  the driver is rewritten in Zag first. Flagged for the parent.
- L3B v2 / robust (C64, C68): CLEAN (see D).
- L3C v3 (C73): CLEAN (see F).
- HypD v3 (C72): CLEAN.
- Causal edit invention (C65) and its adversary break (C71):
  CLEAN.
- OpScope behavioral (C69) and compression (C74): CLEAN.

## Part 5: Recommended remediation order

1. Write a pure-Zag scorer for the frozen Core Freeze Challenge
   artifacts (world files + battery outputs) and re-derive the
   9 world scores. Unblocks the central benchmark.
2. Reimplement the C1 race driver (world simulation + key.json
   scoring) in pure Zag; re-derive the C1 clean, F-E family,
   small-k (C76), and reproduction results from the sealed worlds.
   Unblocks C76 and the baseline program.
3. Reimplement the shell source-audit verifiers (D, E) and the
   seal-verifier (G) in Zag for full ruling compliance. Lower
   priority: no scientific claim depends on them.

## Audit method note

This audit was conducted by reading committed reports, ledger
entries, and scripts via git show and file reads. No
prohibited-language tools were executed to perform the audit.
The contaminated paper was not read, cited, or modified.
