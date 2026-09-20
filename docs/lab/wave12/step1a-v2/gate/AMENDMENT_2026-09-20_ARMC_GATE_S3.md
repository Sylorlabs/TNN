# DATED AMENDMENT — Arm C trial §3 gate: auditor-PASS → replay + certifier gate

**Date:** 2026-09-20
**Status:** DRAFT — pending Micah's explicit re-approval. NOT IN FORCE.
**Amends:** `PREREG_ARMC_TRIAL.md` (frozen `97882fc`), §3 gate item 2.
**Author:** RNGSCAN implementation coordinator, per Micah's 2026-09-20
decision adopting the debate's converged middle path.
**Standing law:** frozen bars/gates change only via dated amendments with the
owner's approval. Until signed, the old §3 gate item 2 stands in full, and
the Step 1e (Arm C trial) builder stays parked.

---

## 1. The old gate (quoted verbatim from frozen §3.2)

> **Auditor PASS:** the integrated Arm C variation path and the NULL path
> each hold a PASS attestation from the step-1a auditor, under a version NOT
> killed under `PREREG_NO_RNG_AUDIT.md` §6. A killed auditor version
> invalidates every Arm C trial run under it; those runs do not count and are
> not reported as evidence.

## 2. Why it must change

The gate requires a PASS from a step-1a auditor version that has not been
killed. Three auditor versions have now been built (v1, v2, v3) and all three
were killed by their own blind red teams — v3 died to the same structural
class as v2 (hand-rolled table with innocent names, invisible to
token-based detection; evidence commit `7b64c89271d5353aaa995b587207442ca18183e2`).
No unkilled general-auditor version exists or is on a credible path to
existing: each version dies to a NEW shape inside already-listed categories,
which is the empirical signature of an inexhaustible idiom space, not a
closing checklist. Under the old gate, the Arm C trial — the program's
central state-variation question — is parked indefinitely behind a gate that
may never converge. A parked experiment produces zero evidence.

The replacement gate keeps the no-RNG law mechanically enforced per build,
but on the layers the evidence shows actually catch: hardened replay
divergence (which caught the real smuggled randomness in every blind round
to date) and prescriptive per-build certification (which converts open-ended
detection into bounded verification of a known artifact).

## 3. The new §3 gate item 2 (replaces the old text in full)

> **No-RNG gate (replay + certifier + statement):** the integrated Arm C
> variation path and the NULL path each hold, at the time the runs executed,
> ALL of the following on the EXACT frozen build (source and binary hashes
> recorded; any rebuild restarts this gate):
>
> a. **Hardened-replay PASS attestation** — N=8 runs, byte-identical stdout
>    and audit log, adversarial heap pre-dirtying, allocation-pattern
>    variation, deployment-like conditions per the preregistered matrix
>    (`REPLAY-2026-09-20-v1`, prereg frozen `0f5cf8c594ee`).
> b. **Thin-certifier PASS attestation** — rules R1–R8 hold on the frozen
>    build (as amended; see §4 dependencies).
> c. **v2 static scan executed as tripwire** — result recorded alongside the
>    attestation; informational only, carries no kill bar.
> d. **The signed residual-risk statement** (`RESIDUAL_RISK_STATEMENT_ARMC.md`)
>    covering the exact frozen build, published next to the results.
>
> A killed general-auditor version (v1/v2/v3) does NOT by itself invalidate
> runs — the kills are recorded in the risk statement (§"What is NOT
> certified" item 1). Invalidation now requires a failed item (a)–(d) above:
> a replay divergence, a certifier FAIL, or a revoked/unsigned statement
> invalidates every bar result collected under it; those runs do not count
> and are not reported as evidence.

## 4. Dependencies, stated openly

This gate is FINAL only when both underlying draft amendments are signed:

- `AMENDMENT_2026-09-20_REPLAY_BAR.md` (phase-1 replay acceptance-bar
  re-scoping) — `docs/lab/wave12/step1a-v2/replay-hardening/`
- `AMENDMENT_2026-09-20_THINCERT_R3.md` (R3→R3′, R1b, R4b) —
  `docs/lab/wave12/step1a-v2/thin-certifier/`

Until both are signed, every attestation under items (a)–(b) is marked
AMENDMENT-PENDING and no bar result (K1–K9, repetition probe, K7 scorecard)
counts. These two amendments, this §3 amendment, and the residual-risk
statement are presented as one signature package.

Note on §3 gate item 3 (K1 harness baselining): the hardened replay harness
acceptance evidence (commit `e3b4091b3819` — adversarial-heap no-false-positive
proof, dirty-plant divergence table) supersedes the interim K1 baseline once
the replay-bar amendment is signed. No separate K1 re-baselining run is
required beyond what phase 1 already committed.

## 5. What does NOT change

- All other §3 gate items (1, 3, 4, 5, 6) are unchanged.
- Kill bars K1–K9, the repetition probe, and the K7 scorecard are unchanged.
- The no-RNG law itself is not amended — only the certification gate.
- The v3 line stays dead; no v4 starts without a separate explicit decision.
- Pure-Zag and freeze-before-build discipline continue to bind all
  implementation work under the new gate.

## 6. Approval

- [ ] Micah APPROVES: old §3.2 replaced by §3 above; the Step 1e builder
  unblocks on the new gate once the two dependency amendments and the
  residual-risk statement are also signed.
- [ ] Micah REJECTS: old §3.2 stands; the Step 1e builder stays parked;
  the replay harness, thin certifier, and v3 evidence remain committed as
  research records.

**Signed:** Micah ________________________  **Date:** ________

*Unsigned draft. This amendment has no force until signed.*
