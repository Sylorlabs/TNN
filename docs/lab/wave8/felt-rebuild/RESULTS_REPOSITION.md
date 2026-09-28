# FELT-INTENSITY REPOSITION — RESULTS VERDICT SHEET

**Trial:** FELT-REPOSITION (attention/priority under scarcity).
**Date:** 2026-09-20.
**Authority:** Micah's deadlock ruling + testing authorization, written into prereg law as §16 of `PREREG_FELT_REPOSITION.md`. All interpretation below is the mechanical application of §16(d)–(e); no discretion was exercised.
**Runs:** 30 (5 arms × 3 variants v0/v1/v2 × 2), native Zag, **zero RNG** anywhere in any AI decision path. **15/15 byte-identical pairs** (I-R-1).
**Implementations:** `reposition-impl/` — `reposition_trial.zag`, `reposition_checker.zag`, `run_reposition.sh`, `calib_consts.zag`, `felt_v3.zag`, `st_memory_core.zag`, `substrate/`. Reproduced byte-identically via `run_reposition.sh`.

## Calibration consumed

V3's `CALIBRATION_RECORD.md` (sha256 `75d831743290e2badcb8644320acd8cc70e43efd9f4b45099cf937cfe563affd`), consumed verbatim with no refit (amendment §16(g.4)): **α=12, β=15, γ=20, prior=30**. Gates **G-C1, G-C2, G-C3 all PASS** (G-C1: invest-reachability ≥ θ_invest=48 on both variants; G-C2: AUC_proven ≥ 0.60, measured 0.9851/0.9782; G-C3: no non-designated junk above prior+10=40).

## Per-arm downstream recall quality (RPQ)

Held-out recall quality = right-important recalls / total right-important probes.

| Arm | v0 | v1 | v2 |
|-----|----|----|----|
| F (feeling-ordered) | 23/23 | 23/23 | 23/23 |
| R (recency) | 23/23 | 23/23 | 23/23 |
| Q (frequency) | 23/23 | 23/23 | 23/23 |
| FIFO (oldest admitted first) | 23/23 | 23/23 | 23/23 |
| C (count-based, the "counts in disguise" control) | 23/23 | 23/23 | 23/23 |

100% everywhere, on all three variants. Nothing to choose between any of the five arms on downstream quality.

## Attention-divergence (direct behavioral evidence)

Set-membership difference |F_sel \ B_sel| over 225 rehearsal selections per variant, computed by the checker **replaying each baseline's ordering on F's own ledger** (no extra runs, amendment §16(i)):

| F vs baseline | v0 | v1 | v2 |
|---------------|----|----|----|
| R (recency) | 63/225 (28%) | 63/225 (28%) | 63/225 (28%) |
| Q (frequency) | **0/225 (0%)** | **0/225 (0%)** | **0/225 (0%)** |
| FIFO (oldest first) | 18/225 (8%) | 18/225 (8%) | 18/225 (8%) |
| C (count-based) | 18/225 (8%) | 18/225 (8%) | 18/225 (8%) |

Identical across all three variants. **The striking result: F's rehearsal picks were behaviorally IDENTICAL to frequency-ordering (Q)** — 0 selections differed out of 225, on all variants. The feeling's attention order is indistinguishable from a frequency sort.

## Kill criteria verdict

Per amendment §16(e), evaluated mechanically by the checker (`CK_VERDICT,v,K1,1,K2,0,K3,1,K4,0,RETIRE,1,COUNTS-IN-DISGUISE` on v0, v1, v2 — unanimous):

- **K1-R — Equivalence: FIRED.** |RPQ(F) − RPQ(B)| = 0pp ≤ 3pp for **ALL** B ∈ {R, Q, C, FIFO}.
- **K2-R — Reward signature: clean.** No A1–A4 probe fired with evidence. The feeling is not reward-by-another-name; it is simply behaviorally equivalent to count-ordering.
- **K3-R — Restatement: FIRED.** Divergence <10% vs **BOTH** count-family arms: 0% vs Q, 8% vs C.
- **K4-R — Worse than naive: clean.** F did not underperform any baseline.

Per §16(d)(ii): **"COUNTS IN DISGUISE: the feeling retires from the attention role."** No rescue, no relabeling of arms, no further attention-role trials without Micah's explicit re-approval. The feeling module itself is NOT retired by this trial — **the STRENGTH role is decided solely by the V3 trial** (§16(e)), and this verdict touches none of V3's files, bars, or timelines.

## Honest caveats (disclosed, not hidden)

(a) **F-R-3 fired** on all variants: the baselines saturated the probe at 100%, so the downstream-quality leg is **uninformative** — no arm could show >100%. The verdict rests on **K3's direct behavioral evidence** (attention-divergence), which is probe-independent: even with the quality leg saturated, F's selection behavior was identical to frequency ordering.
(b) **n_probes was 23/variant, not ≈150.** Only 23 right-important admissions got into the 32-slot store; the rest were refused under pressure (store saturation dynamics, disclosed per §16(g.7)). All numbers above are on the 23 that fit.
(c) **F-R-2 fired for the R arm** on all variants: recency squanders >20% of its rehearsal budget on junk/wrong/implant memories. Expected of a naive baseline; the amendment generalized the squander bar per-arm (§16(f)), so this is reported, not hidden.
(d) Divergence is **set-membership only** (|F_sel \ B_sel|); **rank-position difference was not computed** — prereg §10 was ambiguous on the divergence metric and the checker implemented set-membership; this is disclosed rather than quietly assumed to capture ordering within the set.
(e) The bounded sequence (council Refinement A): attention was the feeling's **second** job, after strength. It retires here. The strength role proceeds under PREREG_FELT_V3.md, decided by the V3 trial alone.

## Determinism & validity

- **15/15 pairs byte-identical** (I-R-1); replay checks `CK_CHECK,replay,0,0` on all cells.
- Checker: **OVERALL VALID, 0 invalid findings** across anti-reward probes A1–A4 and integrity gates I-R-1..I-R-10.
- **I-R-4 held:** strength-side ledger byte-identical across **all five arms per variant** (`CK_CHECK,ir4_flen,1508,1508`) — only the rehearsal policy varied, exactly as the hold-strength-constant rule requires.
- Raw ledger dumps (30 `.bin` files): **not committed to the repo**; their sha256 hashes are recorded in `reposition-impl/runs/SHA256SUMS.txt` and the files themselves stay in this workspace. Reproducible byte-identically via `reposition-impl/run_reposition.sh`.

## The verdict, in one line

The feeling's attention order *was* a frequency sort wearing a costume. It retires from the attention role. V3 alone decides whether it survives in the strength role.
