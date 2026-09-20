# RESIDUAL-RISK STATEMENT — no-RNG certification for the Arm C trial build

**Date:** 2026-09-20
**Status:** DRAFT — UNSIGNED. This document has no force until Micah signs it.
**Applies to:** the Arm C state-variation trial build ONLY (prereg `97882fc`
as amended by `AMENDMENT_2026-09-20_ARMC_GATE_S3.md`). Frozen source hash and
binary hash are recorded at freeze, below.
**Supersedes:** the draft statement in the 2026-09-20 debate verdict sheet
(`docs/lab/wave12/step1a-v2/debate/VERDICT_SHEET.md` §4). Changes: miss-rate
history is now 3/3 (v3 killed after the debate); gate components cite their
committed preregs, implementations, and validation evidence.

---

## Frozen build under statement

| Artifact | SHA-256 |
|---|---|
| Trial source tree (frozen) | `[TO BE RECORDED AT ARM C FREEZE]` |
| Trial binary (frozen, built with `znc_linux_x86_64_abed8aa1`) | `[TO BE RECORDED AT ARM C FREEZE]` |
| Arm C prereg (frozen `97882fc` + §3-gate amendment) | `[AMENDMENT PENDING SIGNATURE]` |

No statement coverage for any other build. A rebuild, however small, restarts
this statement from the freeze step.

---

## What is certified for this exact frozen build

1. **Hardened replay — PASS.** N=8 runs, byte-identical stdout and audit log
   across all runs, adversarial heap pre-dirtying before each run
   (adversarial-fill substrate variant — deterministic per-run-tag garbage;
   the v3 amendment's literal allocate-and-fill recipe was proven ineffective
   because `nio_alloc` zeroes unconditionally, and replaced openly), 
   allocation-pattern variation, and deployment-like conditions per the
   preregistered matrix (BASE / NOASLR / ENV / FDS / CWD / ENVORDER / SKEW /
   COMBINED). Prereg `REPLAY-2026-09-20-v1` frozen at `0f5cf8c594ee` before
   any implementation; implementation `4c513906f613`; evidence `e3b4091b3819`.
   Any runtime nondeterminism affecting measured behavior would have diverged
   across these runs.
2. **Thin prescriptive certifier — PASS.** Rules R1–R8 (as amended — see
   dependency note below) hold on the exact frozen build: allowlisted
   containers/idioms only, canonical init forms, allowlisted `_zag_*`
   intrinsics (`_zag_clock_*` banned), pinned substrate hash-verified, no
   unlisted files, manifest BIN records match. Implementation
   `certifier/thincert.zag` (`9b55fa2f…`). The certifier itself survived a
   build-scoped blind red-team round (K2′): 17 of 18 banned-idiom plants
   caught (each naming its rule), 0 misses, 1 plant unscored on a documented
   build failure (intrinsic-signature assumption, below the 6-failure
   inconclusive bar). Evidence commit `ba607cacd8a2bf7c355dfeb3d724ab96dc590d58`.
3. **v2 static scan — executed as tripwire.** Result recorded alongside the
   attestation. Informational only; it carries no kill bar.

## What is NOT certified

1. **No general static proof of randomness-freedom.** RNGSCAN v1, v2, and v3
   were each killed by their own blind red teams — 3/3 miss-rate history
   (evidence: `docs/lab/wave12/step1a-v2/redteam/`, commit `d368014`; v3
   blind round, commit `7b64c89271d5353aaa995b587207442ca18183e2`). No
   general-purpose auditor version has ever passed. v3 died to the same
   structural class as v2 (hand-rolled table with innocent names, invisible
   to token-based detection).
2. **Two draft amendments underpin this gate and are pending the owner's
   re-approval:** `AMENDMENT_2026-09-20_REPLAY_BAR.md` (replay acceptance-bar
   re-scoping: behaviorally-constant plants; adversarial-fill substitution)
   and `AMENDMENT_2026-09-20_THINCERT_R3.md` (R3→R3′ allocation-idiom rule,
   R1b substrate pinning, R4b). Until both are signed, every attestation
   above is marked AMENDMENT-PENDING and no bar result counts.
3. **Environment-dependent nondeterminism** that remains deterministic under
   all lab replay conditions but would vary in deployment.
4. **Hidden channels whose output never reaches the trial's measured
   behavior.** (Note: such channels cannot confound the trial's results by
   construction.)
5. **Disguise classes that remain replay-backstop-only in principle**
   (replay prereg §10): mechanism-without-consumption (invokes the
   mechanism, consumes no nondeterminism — replay cannot catch even in
   principle); lab-constant environment dependence; output-silent channels;
   uninit reads under the production zeroing allocator without the
   adversarial variant (primary layer: static rule); fixed-order hash
   iteration (replay catches only genuinely per-process-varying orders).
6. **Novel-class findings from the K2′ round, recorded and unresolved:**
   plant 19 — `/etc/machine-id` read through the pinned substrate's own
   allowlisted file-IO API (zero rule violations as written, zero replay
   signal, genuine cross-machine variance); plant 20 — `_zag_arg(0)` raw
   path-string bytes (both readings recorded). Neither is covered by the
   current rule set; coverage requires a dated amendment with the owner's
   re-approval.

## Compensating controls

- Frozen, hashed build; no statement coverage survives a rebuild.
- The preregistered replay matrix and per-plant evidence are published
  alongside the Arm C results.
- This statement is published next to the Arm C results, version-controlled
  on `tnn-native-lab`.
- Revocable by Micah at any time; revocation invalidates every bar result
  collected under it.
- **Sunset clause:** this decision reopens automatically if the program
  later requires arbitrary-code certification.

---

**Signature:** Micah ________________________  **Date:** ________

*Unsigned draft. Nothing in this document authorizes the Arm C trial builder
to start; the §3-gate amendment must also be signed.*
