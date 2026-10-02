# PREREG: REVISE Pipeline Governance Audit (Step 11)

Frozen: 2026-09-30. Auditor: REVISE Governance Auditor (subagent).
Scope: F3 REVISE 11-step promotion pipeline, steps 1 through 10.
This prereg is committed alone before any audit analysis begins.

## Standing rules applied

R1. Pure Zag only, literal owner red line (LOOP_STATE.md standing owner
rules 2026-09-23; Micah 2026-09-30: everything in pure zag, zero python,
C, or other languages allowed). No Python anywhere: not glue, not
analysis, not verifiers, not harnesses, not calculators.

R2. The debate-adopted S7 narrowed artifact-touch test (stdout-only with
no artifact contact disclosed but not voided) is NOT approved: it is
ruling (1) of the six governance rulings awaiting Micah's decision.
Pending his ruling, the literal rule governs.

R3. 2026-09-30 standing rule: disclosure does not cure use. A disclosed
Python touch is still a K4 breach.

R4. Prereg commit-order self-check: each step's prereg commit must
strictly precede its implementation/result commit, verified with
git merge-base --is-ancestor.

R5. Shell-only byte checks via
worker_snippets/check_no_dash.sh. No python3 for byte checks.

R6. No frozen bar may be moved or reinterpreted after results.

## Steps under audit

S1 prereg c197e7cd8, implementation/result 7009d711c (REVISE-PASS).
S2 is the implementation step itself (7009d711c).
S3 sealed eval prereg 8cdf0992a, result 1df8addec (REVISE-SEALED-PASS).
S4 independent reproduction result 7407dd4a7 (REVISE-REPRO-PASS).
S5 baseline prereg 4786633c5, amendment db585360a, result c810d5f55
(REVISE-BASELINE-PASS).
S6 alternative-explanation attack prereg 12da75511, result bbdb65c99
(REVISE-ATTACK-SURVIVES).
S7 OOD prereg 7bf467d35, result 1125be9bb (REVISE-OOD-PASS).
S8 ablation prereg 6dcb1f11b, result 96e22de82 (REVISE-ABLATION-PASS).
S9 transfer prereg 7e80e52e6, result c3c3e3bc8 (REVISE-TRANSFER-PASS,
with a disclosed python3 -c calculator invocation).
S10 red team prereg fc57bb738, result 4a2b8ef43 (REVISE-REDTEAM-KILLS).

## Audit bars

A1. Commit ancestry: for each step with a prereg, the prereg commit is
a strict ancestor of the step's implementation/result commit.
Method: git merge-base --is-ancestor for each pair. All pairs must hold.

A2. Verdict integrity: each step's committed result document states its
verdict and kill-bar outcomes without alteration of the frozen bar.

A3. K4 purity: no Python interpreter invocation in any step's work.
Method: read each step's committed result/prereg documents for Python
disclosures, and inspect build scripts for python references. Any
Python touch, disclosed or not, is a breach under R1/R3. Findings are
reported per step.

A4. Step-9 disclosure verification: confirm the python3 -c disclosure
is present in the committed S9 result document, quote it verbatim, and
record the consequence under R1/R3.

A5. Blemish disclosure chain: the sealed-evaluation REFUTE-DRILL
artifact blemish disclosed at S3 must remain disclosed through S6 E2
and S10, with no silent fix or reinterpretation.

A6. Amendment discipline: the S5 amendment db585360a must strictly
precede the S5 implementation commit c810d5f55, and must not alter any
verdict rule after results.

## Verdict rule (frozen)

REVISE-AUDIT-PASS iff A1 through A6 all hold with zero Python touches
in any step.

REVISE-AUDIT-FAIL if any bar fails. The verdict names the failed bar,
the affected step, and the exact evidence. A FAIL on A3 names the
step and quotes the disclosure; that step's result cannot be cited as
K4-clean evidence, and the pipeline cannot be certified governance
clean until the contaminated step is re-run pure-Zag under a new
frozen prereg.

## Out of scope

Scientific merit of REVISE is not re-litigated here. S10 killed the
generic causal-revision reading; the surviving bounded-L2
characterization stands as S10 reported it. This audit certifies the
record, not the claim.
