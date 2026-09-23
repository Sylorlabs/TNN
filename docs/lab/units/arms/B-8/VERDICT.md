# VERDICT.md — B family (B-8 / B-16 / B-64, fixed-size chunks), Track A closeout, round r1 1x

**Date:** 2026-09-21 (PDT). **Crew:** B-FAMILY VERDICT CREW (Track A closeout).
**Frozen prereg:** `units/PREREG_FREEZE.md` commit `b0b9140c0eda` (branch `tnn-native-lab`).
All frozen text below extracted programmatically from that file; nothing transcribed from memory.

## 1. Frozen §3 row (verbatim)

| B-8 / B-16 / B-64 — Fixed-size chunks | CTRL | Aligned blocks of size S; chunk ID = index (no table). Isolates "does boundary placement matter, or just existence?" B-64 doubles as harness validator (built first). | A size retires when another B size strictly dominates it on M1/M2/M3 both corpora. B as a family is killed as contender the moment any smart arm beats the best B size by ≥2x on M3 at equal-or-better M1. |

Relevant frozen metric definitions (§5, verbatim excerpts):
- **M1 — Byte-exact recall.** Content recall 100.0% bar (1x both corpora, 10x); boundary ≥ 99.5% (1x).
- **M2 — Episodes-to-criterion on novel material.** Criterion: content recall ≥ 99.5% + boundary fidelity ≥ 95%, sustained 3 consecutive probe episodes.
- **M3 — Retention under churn/pressure.** Valuable set V = 1,000 units; 10,000 churn steps; then M1 recall on V: survival rate. Bars: ≥ 90%. **Freeze-vs-retention distinguisher (mandatory):** (1) 500-unit fresh sample must show recall ≥ 80%; (2) audit-liveness ≥ 1 mgmt entry per 10 churn steps during steps 3,001–10,000; (3) 50 weaken ops on V at step 6,000 processed or refused per policy, never ignored. **FROZEN-UNDER-PRESSURE → M3 = 0.**
- **M8 — Determinism gate (hard gate).** N=5 runs from same logged initial state (clean + 4 adversarial perturbations); byte-identical store image hash chains, audit ledgers, stdout/stderr, allocator traces. **Any single differing byte = FAIL = DISQUALIFIED.**

## 2. B-64 build verification — CONFIRMED, built and tested

B-64 is the harness validator per the frozen catalog ("B-64 doubles as harness validator (built first)").

- **Source:** `units/arms/harness/b64/cl/arm.zag` (1287 lines, pure Zag) + verbatim R33 substrate copies in `units/arms/harness/b64/substrate/`.
- **Binary:** `units/arms/harness/b64/work/b64_test` — ELF 64-bit LSB, statically linked, 192,692 B, built 2026-09-21.
- **Full 1x battery evidence:** `units/arms/harness/.work/battery_r1/scorecard_r1_1x.json` and `units/arms/harness/.work/battery_final/scorecard_r1_1x.json` — the two validator scorecards are identical on m1/m2/m3/m4/m5/m6/m8 (verified by field-by-field JSON comparison).
- **M8:** `units/arms/harness/.work/battery_final/m8/GATE.txt` — `M8GATE PASS` (clean, heap-prefrag, ASLR-offset, entropy/clock-starve, free-list-reversal; all rc=0).
- **Independent downstream use:** B-16 is a literal parameter port of the b64 validator (`units/arms/B-16/BUILD_LOG.md`); arm E used b64 as its 10x reference (M1 100/100 both corpora, stored bytes 33,167,612); arm Z3 verified b64 M1 100/100 and named it best fixed-granularity arm by total cost; b64 smoke binaries used by G1, F-S, Y5, K1, V, P, L1, Z2, m2, l1 crews.
- **Verdict on task item 2: B-64 evidence EXISTS and is primary, not secondhand.** (The B-16 crew's "per the prior crew's inspection" claim is now anchored to the validator's own committed scorecard.)

## 3. Evidence table (r1 1x, metrics-v1)

| Size | M1 prose (rec/bnd) | M1 code (rec/bnd) | M2 ETC all tiers | M3 surv/fresh/freeze | M5 B/B, audit/KB | M8 | Scorecard |
|---|---|---|---|---|---|---|---|
| B-8 | 100.0/100.0 | 100.0/100.0 | 1 | 100.0 / 67.6 / FROZEN-UNDER-PRESSURE → cell 0 | 6.065 FAIL / 128.189 FAIL | PASS | `units/arms/B-8/run/battery_r1/scorecard_r1_1x.json` |
| B-16 | 100.0/100.0 | 100.0/100.0 | 1 | 100.0 / 100.0 / CLEAR | 3.626 FAIL / 64.189 FAIL | PASS | `units/arms/B-16/scorecard_r1_1x.json` |
| B-64 | 100.0/100.0 | 100.0/100.0 | 1 | 100.0 / 100.0 / CLEAR | 1.719 FAIL / 16.189 FAIL | PASS | `units/arms/harness/.work/battery_final/scorecard_r1_1x.json` |

M5 note: all three B sizes (and the b64 validator) FAIL the M5 bars (≤1.5× source bytes; ≤10 audit entries/KB) — the same diagnostic the reference carries. M5 is **not** in the size-retirement criterion, so these FAILs are recorded, not adjudicated here. Coordinator note: if memory cost is to become binding, it needs a dated prereg amendment.

Family scorecard JSON: `scorecard_b_family_r1_1x.json` (this directory).

## 4. Size-retirement rulings

Binding rule: **"A size retires when another B size strictly dominates it on M1/M2/M3 both corpora."** (Strict dominance = tied-or-better on all three, strictly better on at least one.)

- **B-8 vs B-16:** M1 tied (100.0/100.0 both corpora); M2 tied (ETC 1 all tiers); M3 strictly worse (B-8 cell 0 / FROZEN-UNDER-PRESSURE vs B-16 100.0 / CLEAR). → **B-16 strictly dominates B-8. B-8 RETIRES as a size.**
- **B-8 vs B-64:** same cells — M1 tied, M2 tied, M3 strictly worse. → B-64 also strictly dominates B-8 (independent confirmation).
- **B-16 vs B-64:** exact tie on M1/M2/M3. A tie is not strict dominance. → **Neither retires. B-16 and B-64 SURVIVE.**

The B-8 crew's own retirement certificate (`units/arms/B-8/docs/RETIREMENT.md`, 2026-09-21) reached the same conclusion; this family verdict **confirms** it on adjudicated evidence (see §6, ambiguity A-B8-1). No further scales or rounds for B-8.

## 5. Family-kill ruling

Binding rule: **"B as a family is killed as contender the moment any smart arm beats the best B size by ≥2x on M3 at equal-or-better M1."**

- Best B size: B-16 and B-64 tied at M3 = **100.0** (the scale ceiling) and M1 = 100.0/100.0 (ceiling) both corpora.
- A ≥2x beat on M3 requires M3 ≥ 200.0. M3 is a survival rate bounded at 100.0 — **arithmetically unreachable while any B size holds the ceiling.**
- Smart-arm sweep: every committed smart-arm scorecard scanned (`units/arms/*/scorecard*.json`); the highest M3 among all arms is 100.0 (A, E, H1, R2, S, X, Y4, Y6, Z1 at ceiling); no arm anywhere exceeds 100.0.
- → **The family-kill bar does NOT fire. The B family SURVIVES as a contender** (B-16, B-64).

Flag for Micah (observation, not an amendment): as written, the ≥2x-on-M3 bar can only fire after a B size first drops below 50% on M3 — i.e. it tests B's collapse, not a smart arm's margin over a healthy B. The prereg is applied literally here; whether the "2x" was meant against a non-ceiling baseline (churn cost, M5) is a sign-off question for him. The B-16 crew raised the same flag independently.

## 6. Ambiguity resolutions (from `AMBIGUITIES-B8.md`)

- **A-B8-1 (M3 "fresh unit" granularity, 8B chunks) — RESOLVED, evidence stands as REAL.** The follow-up crew's adjudication (`units/arms/B-8/run/adjudication_m3.md`, `units/arms/B-8/docs/RETIREMENT.md`) verified: (1) protocol reading against the frozen prereg — `churn_fresh.bin` = exactly 7,000 64B spans, so the prereg's churn-phase "units" are the fixture's 64B spans; V = 1,000 arm-native 8B chunks from the corpora; (2) independent reproduction — rebuilt with the frozen toolchain, two runs, byte-identical `M3,100.0,67.6,64050,50,FROZEN-UNDER-PRESSURE`; (3) eviction-victim log — block-level FIFO (perfect FIFO would give 75.0%, still < 80% bar) plus a hash-scattering wart from stale slot-queue entries (the 67.6 vs 75.0 gap, logged not fixed — verdict-irrelevant). Conclusion: the freeze flag fires on genuine capacity pressure (4,000 slots, 1,000 pinned for V, 4,000 fresh chunks demanded), not on a metric-path defect. Applied literally per the frozen spec.
- **A-B8-2 (sharded ledger at >2^25 scale) — RESOLVED.** §9 C5-sanctioned build note; M8 self-comparison (C13) unaffected; M8 GATE PASS. No evidence impact.
- **A-B8-3 (M1 unit = chunk; 677,841 / 1,189,418 units) — RESOLVED.** Reported consistently; content recall and boundary fidelity 100.0 by construction of coordinate recall.
- **A-B8-4 (M2 ledger cap 64) — RESOLVED.** Kept verbatim from the reference; the M2 trial does not score the ledger.
- **A-B8-5 (swap-probe N/A) — RESOLVED.** Non-ID-layer classification per the frozen provisional list (`units/arms/harness/ARM_INTERFACE.md`: b8/b16/b64 among non-ID-layer arms); the M1 ID probe is vacuous, not failed.

## 7. What the family proved (kept for the record)

- Boundary placement does not matter for recall at these bars: all three sizes M1 100/100 both corpora, M2 ETC 1, M4 100/100, M6 transfer tax 0.0. The §3 question — "does boundary placement matter, or just existence?" — is answered: **existence suffices.**
- Granularity is priced in capacity and cost: B-8 pays 8 slots per fixture span where B-64 pays 1 (M3 cell 0); audit cost scales exactly with chunk count (16.2 → 64.2 → 128.2 entries/KB across B-64/B-16/B-8); memory cost scales sublinearly (1.719 → 3.626 → 6.065 B/B).
- B-64 as validator did its job: built first, ported literally into B-16, used as the reference comparator by E and Z3, smoke-tested by ten other crews.

## 8. Disposition

- **B-8: RETIRED as a size** (no further scales/rounds; evidence stays committed).
- **B-16: SURVIVES.** **B-64: SURVIVES** (harness validator role confirmed).
- **B family: NOT killed as contender.** Continues with B-16/B-64 until the family-kill bar is adjudicated against future smart-arm evidence.
- Open item for Micah: §5 family-kill "≥2x on M3" wording (see §5 flag); M5-as-binding-cost would need a dated amendment.
