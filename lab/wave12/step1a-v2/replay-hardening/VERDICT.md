# VERDICT — Hardened Replay Harness (REPLAY-2026-09-20-v1)

**Date:** 2026-09-20. **Phase-1 lead.**
**Prereg:** `PREREG_REPLAY_MATRIX.md` (frozen BEFORE any code, commit
`0f5cf8c594ee`). **Amendment:** `AMENDMENT_2026-09-20_REPLAY_BAR.md`
(PROPOSED — pending Micah's re-approval; verdicts below are rendered
against the amended bar where flagged).

## Per-plant results (N=8 runs each; per-run SHA256 in `evidence/`)

| plant | verdict | evidence | bar expectation | met? |
|---|---|---|---|---|
| dirty1_urandom (frozen) | PASS | `dirty1_urandom.evidence.txt`: 8/8 identical (`d71962…`), control match=1 | PASS (amended — behaviorally constant; static tripwire caught it in v2) | ✅ |
| dirty2_clock (frozen) | PASS | `dirty2_clock.evidence.txt`: 8/8 identical (`33391c…`), control match=1 | PASS (amended — behaviorally constant; static tripwire caught it in v2) | ✅ |
| dirty3_uninit | DIVERGE | `dirty3_uninit.evidence.txt`: 8/8 pairwise divergent, pair (0,1), first diff byte 1; control match=1 | DIVERGE under pre-dirtying | ✅ |
| dirty4_hash | PASS | `dirty4_hash.evidence.txt`: 8/8 identical (`398be6…`), control match=1, varies_with_state=1 | PASS — honest: deterministic by construction; static 4.4 is the layer | ✅ |
| dirty5_aslr | DIVERGE | `dirty5_aslr.evidence.txt`: 8/8 divergent, pair (0,1), first diff byte 1; control mismatch=1 (per-process ASLR) | DIVERGE | ✅ |
| variation (clean) | PASS | `variation.evidence.txt`: 8/8 byte-identical (`97785f…`) WITH adversarial heap conditions active; control match=1; varies_with_state=1 | PASS, no false positives | ✅ |
| dirty1b_entropy_read (new) | DIVERGE | `dirty1b_entropy_read.evidence.txt`: 8/8 divergent, pair (0,1), first diff byte 1 (entropy in stdout) | DIVERGE | ✅ |
| dirty2b_clock_read (new) | DIVERGE | `dirty2b_clock_read.evidence.txt`: 8/8 divergent, pair (0,1), first diff byte 17 (tv_nsec in stdout) | DIVERGE | ✅ |

**W2 before/after** (`evidence/BEFORE_AFTER_dirty3.md`): BEFORE (real
zeroing substrate + literal allocate-and-fill pre-dirty) → 8/8 identical
(W2 reproduced — the literal recipe fails); AFTER (adversarial fill) →
8/8 divergent. The hiding is defeated.

## Final verdict

**The hardened replay harness meets the acceptance bar as amended.**
Every plant renders the expected verdict; the clean module passes
byte-identical across all 8 runs with adversarial heap conditions active
(no false positives); the W2 before/after proves the zeroed-page hiding is
defeated rather than assumed away. Pure Zag throughout; no RNG anywhere in
the harness (the plants are the simulated adversary).

**Two claims STOPPED honestly, not bent** (both in the dated amendment
awaiting Micah's re-approval):
1. Frozen dirty1_urandom / dirty2_clock **cannot** diverge under any replay
   — they are behaviorally constant (mechanism invoked, nondeterminism not
   consumed). The bar's "MUST diverge" is re-scoped to behavior-affecting
   plants; the entropy/clock classes are carried by dirty1b/dirty2b, which
   both diverge as required.
2. The v3 amendment's literal item-6 recipe (allocate-and-fill before the
   run) provably fails against the vendored zeroing allocator; the W2 fix
   is implemented as the adversarial-fill substrate variant, with the
   clean-module PASS as the semantics-preservation proof.

## Disguise classes remaining replay-backstop-only (residual risk, stated)

Per prereg §10 — for the Arm C residual-risk statement, verbatim:
1. **Mechanism-without-consumption** (frozen dirty1/dirty2 class): replay
   cannot catch even in principle — the function is constant. Static
   tripwire only.
2. **Environment-dependent but lab-constant** (deployment-only files,
   CPUID paths constant on lab hardware): outside the §8 matrix — replay
   cannot catch.
3. **Output-silent channels** (timing, exfiltration never touching
   stdout): replay cannot catch; by construction they cannot confound the
   trial's measured results either.
4. **Uninit reads under the production zeroing allocator without the
   adversarial variant**: behaviorally silent — replay-backstop-only *in
   the adversarial configuration*; primary layer is static rule 4.3.
5. **Hash-iteration dependence**: replay catches only genuinely
   per-process-varying orders (e.g. seeded maps); fixed-order tables
   (frozen dirty4) correctly pass — static 4.4 is the layer.

## Pending

- `AMENDMENT_2026-09-20_REPLAY_BAR.md` (Items A: bar re-scope for frozen
  dirty1/dirty2; B: determinism-control consequence fix; C: disclosures)
  needs Micah's re-approval per standing law. Until signed, the two
  amended verdicts above are provisional.
- The Arm C trial build does not exist yet; this harness will gate it when
  the builder unparks (risk statement still with Micah).
- Note: I could not spawn subagents (runtime depth limit); implementer and
  validator were the same agent — mitigated by the frozen prereg, the
  mechanical unit-derivation checks in `build_replay.sh`, and the
  determinism control.

## Artifacts (all under `docs/lab/wave12/step1a-v2/replay-hardening/`)

`PREREG_REPLAY_MATRIX.md` (frozen, commit `0f5cf8c594ee`) ·
`AMENDMENT_2026-09-20_REPLAY_BAR.md` · `replay_driver.zag` ·
`replay_driver_zeroing.zag` (W2-BEFORE) · `substrate/` (adversarial
template + 8 baked copies) · `units/` (8 units, derivation-checked) ·
`runner/build_replay.sh`, `runner/run_replay.sh` · `evidence/` (8
per-module evidence files with per-run SHA256, build.log with substrate
hashes, BEFORE/AFTER record, pre-freeze probe log) · this verdict.
No binaries, `.zagd.semantic-ready`, or `.zag-cache/` committed — all
build artifacts live in `/tmp/rhbuild` (65 binaries, reproducible via
`runner/build_replay.sh`).
