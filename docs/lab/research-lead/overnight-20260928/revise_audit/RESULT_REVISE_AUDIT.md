# RESULT: REVISE Pipeline Governance Audit (Step 11)

Verdict: REVISE-AUDIT-FAIL.

Frozen prereg: 62f6a9c31 (committed alone before analysis; K1 holds for
this audit step).

## Method

Read the standing rules in LOOP_STATE.md (Step 0) before any work.
Shell, git, grep, sed, and the shell-only check_no_dash.sh only. Zero
Python at every stage of this audit. All findings below are from
committed documents and git ancestry, not from worker handoffs.

## Bar-by-bar findings

### A1. Commit ancestry: PASS

Every step with a prereg verified with git merge-base --is-ancestor
(prereg strictly precedes implementation/result):

- c197e7cd8 -> 7009d711c (S1/S2)
- 8cdf0992a -> 1df8addec (S3)
- 4786633c5 -> c810d5f55 (S5)
- db585360a -> c810d5f55 (S5 amendment)
- 12da75511 -> bbdb65c99 (S6)
- 7bf467d35 -> 1125be9bb (S7)
- 6dcb1f11b -> 96e22de82 (S8)
- 7e80e52e6 -> c3c3e3bc8 (S9)
- fc57bb738 -> 4a2b8ef43 (S10)

All 18 cited commits exist in the repo. S4 (reproduction, 7407dd4a7)
has no separate prereg; it reproduces frozen sealed artifacts, which is
the correct method for a reproduction step, and its doc records zero
Python invocations with 33/33 byte-identical runs.

### A2. Verdict integrity: PASS

Each committed result document states its verdict and kill-bar
outcomes. No frozen bar was altered in any result document:

- S1/S2 REVISE-PASS, S3 REVISE-SEALED-PASS, S4 REVISE-REPRO-PASS,
  S5 REVISE-BASELINE-PASS, S6 REVISE-ATTACK-SURVIVES,
  S7 REVISE-OOD-PASS, S8 REVISE-ABLATION-PASS,
  S9 REVISE-TRANSFER-PASS, S10 REVISE-REDTEAM-KILLS.

### A3. K4 purity: FAIL

One Python touch exists in the committed record, in step 9.

S1, S2, S3, S4, S5, S6, S7, S8, S10: committed documents declare zero
Python invocations, and a repo-wide search of those steps' directories
finds no python3 invocation, only "no Python" / "zero Python"
governance declarations. Clean.

S9 (transfer/reuse, result commit c3c3e3bc8): the committed result
document RESULT_REVISE_TRANSFER.md contains this disclosure in its K3
section, quoted verbatim:

"Disclosure: one stdout-only `python3 -c` invocation was used as a
hex-to-decimal calculator (0x54524645 -> 1414678085) with no artifact
contact; per the S7 artifact-touch framework this is disclosed, not
void."

The same K3 section also claims "Zero Python in authoring, world
files, build, runs, analysis, and byte checks," which is contradicted
by its own disclosure sentence.

Ruling under the frozen audit rules:

- R1 (literal owner red line): any Python use in loop work is a
  breach. A hex-to-decimal calculator invocation is Python use.
- R2: the S7 narrowed artifact-touch test was adopted by debate but
  was never approved by Micah; it is ruling (1) of the six governance
  rulings still awaiting his decision. Pending his ruling, the literal
  rule governs. The worker's appeal to S7 does not stand.
- R3 (2026-09-30 standing rule): disclosure does not cure use.

A3 therefore fails at step 9. The breach is disclosed and
stdout-only, which bounds its blast radius (no artifact was touched),
but under the literal rule it is still a K4 breach.

### A4. Step-9 disclosure verification: CONFIRMED

The disclosure quoted under A3 is present in the committed document at
docs/lab/research-lead/overnight-20260928/revise_transfer/
RESULT_REVISE_TRANSFER.md, committed as c3c3e3bc8. It was not hidden,
minimized, or added post-hoc. The S10 red-team result document also
flags it as a governance note. Credit for honest disclosure is
recorded; it does not cure the breach per R3.

### A5. Blemish disclosure chain: PASS

The sealed-evaluation REFUTE-DRILL artifact blemish (embedded
self-test with a world-calibrated poisoned set that can print
REVISE-FAIL on S-NEG2 while the mechanism produces the correct final
rule) was disclosed at S3 in RESULT_REVISE_SEALED.md section 4
("Central finding: the REFUTE-DRILL misfires on S-NEG2"). At S6,
attack E2 excised the drill from a copy of the frozen learner and
showed mechanism outputs byte-identical, confirming blemish, not
defect. No silent fix or reinterpretation occurred at any step; the
frozen learner was never modified.

### A6. Amendment discipline: PASS

The S5 amendment db585360a (corrected sha256 hashes in the baseline
prereg) strictly precedes the S5 implementation commit c810d5f55, was
committed alone, and altered no verdict rule. No other step amended
its prereg.

## Verdict

REVISE-AUDIT-FAIL.

Failed bar: A3 (K4 purity), at step 9 (transfer/reuse).

The pipeline cannot be certified governance-clean while step 9 stands
on a Python touch. The S9 result REVISE-TRANSFER-PASS cannot be cited
as K4-clean evidence. Remedy: re-run the transfer test pure-Zag under
a new frozen prereg; the disclosed calculator use is trivially
replaceable (the hex constant 0x54524645 is a fixed world tag).

## What the FAIL does and does not mean

- It does not overturn any scientific verdict. S10's
  REVISE-REDTEAM-KILLS stands on its own pure-Zag evidence and does
  not depend on S9. The surviving characterization (bounded L2; D1
  revision reliable only when no inert 0-in-passive/1-in-goal-setup
  variable precedes the true cause in var order) is unaffected.
- It does not void steps 1-8 or 10. Those steps are governance-clean
  and remain citable.
- It blocks pipeline certification only. No SURVIVES claim was
  possible anyway: S10 killed the generic reading at step 10.

## Audit step kill bars

- K1 (prereg frozen before audit): PASS. 62f6a9c31 committed alone
  before any analysis.
- K2 (all steps audited): PASS. S1 through S10 each checked against
  A1-A6 as applicable.
- K3 (pure Zag): PASS. This audit used shell, git, grep, sed, and
  check_no_dash.sh only. Zero Python. This document is dash-clean per
  the shell-only checker.
