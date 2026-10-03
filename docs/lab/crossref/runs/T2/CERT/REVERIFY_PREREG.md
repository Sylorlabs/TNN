# REVERIFY_PREREG — T2-CERT (deeper adversarial re-verification)

**Coordinator:** re-verification coordinator (Wave-2 crossref Tier-2 re-verification track)
**Date frozen:** 2026-09-23 (PDT)
**Frozen prereg:** `docs/lab/crossref/PREREG_TIER2.md` @ `7b2100d09911c5c10252c5756c7def288e70bd1f` (blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`, SHA-verified via API)
**Tier-2 verdict under re-verification:** see extract below (from `docs/lab/crossref/runs/T2/CERT/VERDICT.md`)

## 1. Frozen prereg section — byte-verbatim from PREREG_TIER2.md @ 7b2100d09911c5c10252c5756c7def288e70bd1f

> The section below was sliced programmatically from the frozen document. It was NOT transcribed.

```
## T2-CERT — certifier red-team: 0 flips (Type C)

**Claims:** 2026-09-22 day verdict: 0 flips — the no-RNG law stands, no historical certification voided. Honest gap: the dirty1_urandom binary is unreproducible.
**Method:** Type C — re-derive from the committed red-team evidence (crew freezes the pin); verify the 0-flip count and the dirty1_urandom gap as described.
**Rule:** REPRODUCED if 0 flips re-derives; UNREPLICABLE-AS-IS if the evidence pin can't be located (name it).
```

## 2. Tier-2 verdict being re-verified (extracted programmatically from the crew VERDICT.md)

```
# VERDICT.md — T2-CERT (replacement crew): certifier red-team, 0 flips (Type C)
> **Rule:** REPRODUCED if 0 flips re-derives; UNREPLICABLE-AS-IS if the evidence pin can't be located (name it).
per PREREG KB-FLIP: INCONCLUSIVE = input-missing, never a flip) / CONFIRMED / VOID / ARTIFACT-FAIL /
| ARTIFACT-FAIL | 0 | 0 |
**Verdict on claim 1: REPRODUCED.** Zero flips re-derives exactly; zero voided certifications.
`R7=FAIL` (binary hash mismatch) — the binary already failed to match its manifest pin at
**Verdict on claim 2: VERIFIED AS DESCRIBED** — and the mechanism is now identified: the
**REPRODUCED.** Per the frozen decision rule: 0 flips re-derives (pure Zag, 3/3 byte-identical),
```

Full verdict: `docs/lab/crossref/runs/T2/CERT/VERDICT.md`; run log: `docs/lab/crossref/runs/T2/CERT/RUNLOG.md`.

## 3. Re-verification scope for this family

This track does NOT redo Tier-2. It performs INDEPENDENT re-derivations (different code/method than the Tier-2 crew where possible) and FRESH adversarial red teams designed to BREAK the Tier-2 claim. A break is the most valuable outcome and is reported plainly, never buried.

## Re-verification plan (fresh work)

- **RV1 — independent 0-flip re-derivation.** Fetch the committed red-team evidence chain (verdict commit `cadacc199684381833dbed4b27bb171b1d6f739f`, prereg `26b86329b53b9aa24589dcf11d5ff09b125c1fe8`; evidence tree `docs/lab/redteam/certifier-rebuild/`). Build a FRESH pure-Zag verifier (new code, not the T2 crew's `thincert_rb.zag`/`rngscan_v3_rb.zag`) that recomputes row-by-row: rows, flips, confirmed, void, artifact_fail, inconclusive. 3x byte-identical. Expected: rows=35, flips=0, confirmed=34, void=0, artifact_fail=0, inconclusive=1.
- **RV2 — artifact-boundary characterization.** Extract the `dirty1_urandom` plant source; document the EXACT symbol gap: prove `nio_open_readonly` and `_zag_rand` are unknown to the pinned toolchain (build attempt, record the exact error text). Attempt alternative reproduction paths and document each: (a) deterministic shim feasibility — a constant-returning `_zag_rand` stub is deterministic but changes the plant's semantics; document why this is NOT a reproduction of the original binary; (b) scan the rest of the plant battery for the same symbol gap. Deliverable: exact toolchain-gap documentation (symbol-level).
- **RV3 — fresh red team: 5 NEW deterministic adversarial plants** aimed at flipping the 0-flips claim: P1 empty-input plant; P2 max-size/oversize plant; P3 malformed/truncated-evidence plant; P4 plant targeting each "inconclusive"-row's reasoning; P5 boundary-value plant (off-by-one on every threshold the certifier checks). Each pure-Zag, deterministic, byte-identical across runs. Any plant that changes the count (flips>0, or confirmed/void/inconclusive moves) BREAKS the claim.

## Kill bars (frozen)

- **RV-CONFIRM** iff RV1 yields exactly (rows=35, flips=0, confirmed=34, void=0, artifact_fail=0, inconclusive=1) AND RV3 yields 0 flips across all 5 plants AND RV2 documents the gap at symbol level with the failed-build evidence.
- **RV-BROKE** iff RV1 deviates on any count, or any RV3 plant flips the count, or the gap documentation is wrong (a symbol claimed unknown builds fine).

## Protocol (binding for this track)

- Pure Zag for all mechanisms / learners / verification code. Python glue/analysis only (statistics, parsing, plotting) — never in a decision path.
- ZERO randomness in any decision path. Every run byte-identical; prove with SHA-256 digests, >=3 reps unless the plan says otherwise.
- Slices and indexable structures under 2^25 bytes each.
- No full git clones on this VM (SIGKILL/OOM under load). Use blob-filtered single-commit fetches, sparse checkouts, or per-file SHA-verified API fetches.
- Commits to `sylorlabs/TNN`, branch `tnn-native-lab`, ONLY via `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`; lab-relative paths NOT starting with `docs/lab/` (never double-prefix). Never commit binaries or `.zagd`.
- This prereg is frozen at its commit: no implementation work before the prereg commit lands. Any deviation is recorded in RUNLOG.md and flagged.
- If a Tier-2 claim BREAKS under this probing, that is the most valuable outcome: report it plainly with evidence. Verdicts that survive get stronger; verdicts that break get reported, not buried.

## Deliverables

- `docs/lab/crossref/runs/T2/CERT/reverify/VERIFY.md` — per-leg results, digests, red-team outcomes
- `docs/lab/crossref/runs/T2/CERT/reverify/RUNLOG.md` — timestamped run log
- `docs/lab/crossref/runs/T2/CERT/reverify/evidence/` — digests, tables, boundary maps (text only)
