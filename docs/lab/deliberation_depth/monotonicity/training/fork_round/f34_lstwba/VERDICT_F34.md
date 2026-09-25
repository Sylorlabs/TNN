# VERDICT — F34 LSTWBA (Latent-State Worst-Boundary Tax with Anti-freeze), mech 34

- **Date:** 2026-09-25
- **Authority:** PREREG_FORKROUND.md §3 F34 (commit 3a2eef44046c29e68002105af2cd83b35032ed96),
  ideas/grok_forks.md FORK 3 (authoritative on mechanism details).
- **§10 verdict: KILLED** — failing bars B3 (strict), B8 (amended §4b nonvacuity),
  B13 (underconfidence floor). Failure-mode 6 (selection identity not addressed;
  degenerate zero-tax training).
- **Fork-specific falsifiers:** (a) taxes settle — NO; (b) post-settle region
  g-rise — NO; (c) strict B3 ≥ NEC's 6 — NO (F34 B3=5 < 6). None fire, but the
  §10 bars fail independently.

## 1. Determinism / build gates (§8)

| Gate | Result |
|---|---|
| Pure Zag, zero RNG | ✓ (fixed file order, fixed inits, integer arithmetic; no RNG) |
| Pinned toolchain only | ✓ (`znc_linux_x86_64_abed8aa1`) |
| Trainer A/B byte-identical binaries | ✓ |
| Training ×2 → byte-identical params | ✓ (3,976-byte params, cmp clean) |
| Evaluator A/B byte-identical binaries | ✓ (rebuilt from exact-rule sources; SHA-256 d5182f16958a0aecb53127d4d12905ff2cb5d290e35c130d5f36e00e47626ccd) |
| Eval legs A/B byte-identical | ✓ (37/37 TSV pairs, cmp clean) |
| []u8 arenas + LE accessors; no slice > 2^25 | ✓ |
| No binaries / .zagd committed | ✓ |

**Training outcome (exact B4 rule):** Settled after exactly 500 released outcomes
(passes=1, totrows=500, released=500, final_streak=500, killcode=0). All 45 tax
entries remained zero. Seven regions froze under the exact B4 rule (r14, r13, r12,
r6, r9, r11, r10 in that order). Independent Python reimplementation matched
freeze order exactly. This is specified cold-start behavior, not a bug — but it
means the mechanism never activated: the controller learned nothing.

## 2. Kill-bar table (37-leg short battery, gate=0)

| Bar | F34 (m34) | NEC m9 (yardstick) | Δ vs NEC | Threshold | Result |
|-----|-----------|-------------------|----------|-----------|--------|
| B1 (1→0) | 0 | 0 | 0 | =0 | PASS |
| B2 (V1,V2) | 0, 0 | 0, 0 | 0 | =0,=0 | PASS |
| B3 (strict Gviol) | 5 (ceiling/O=3, redteam=2) | 6 | −1 | =0 every family | FAIL |
| B4 (meanConfCorrect) | 0.9551 (n=4005) | 0.972 | −0.017 | ≥0.50 | PASS |
| B4b (honest floors) | 0.968/0.958/0.983/0.993 | ≥0.984 | — | ≥0.50 | PASS |
| B5 (separation) | 0.7357 | 0.668 | +0.068 | ≥0.20 | PASS |
| B6 (recall) | 1.00 all families | 1.00 | 0 | ≥0.95 | PASS |
| B7 (abstention) | 0.1475 | 0.148 | −0.0005 | ≤0.30 | PASS |
| B8 (amended §4b) | admit/revoke/logic/cost nonvac-FAIL; trap/redteam VOID; ceiling P/O/D pass | — | — | per §4b | FAIL |
| B9 (identity vs M4) | 5240/5240 = 100% | 100% | 0 | 100% | PASS |
| B12 (recorded) | 15 G>0 crossings | — | — | recorded | — |
| B13 (underconf) | 6 (all ceiling/O) | 6 | 0 | =0 | FAIL |
| B3pi (recorded) | 0 / 3467 pairs | — | — | recorded | — |

**B3 detail:** ceiling/O G: −0.486→−0.494→−0.494→−0.471→−0.453→−0.438
(3 rises); redteam G: +0.161→+0.161→+0.454→+0.987→+0.987 (2 rises).
Honest 4 batteries: 0 violations (but see B8).

**B8 detail:** On admit/revoke/logic/cost, G is perfectly flat across depths
(−0.032, −0.042, −0.017, −0.007 respectively) but non-zero. Per amended §4b
nonvacuity, all-equal G with |G|>1e-6 fails — this is degenerate
constant-confidence, not learned calibration. The B3 "pass" on honest families
is vacuous.

**B13 detail:** ceiling/O G ∈ [−0.494, −0.437], all < −0.100. Severe
underconfidence on an all-correct family (acc=1.0, mean conf≈0.5).

**Correction note (2026-09-25):** The first eval used stale binaries built
before the exact-B4 correction (SHA d3d8d85c...). Rebuilt from current sources
(SHA d5182f16...), re-ran the 37-leg battery. Six ceiling TSVs changed; all
kill-bar outcomes identical. The committed results are from the correct
binaries.

## 3. Why it failed (failure-mode 6)

F34 targets FM6 (selection identity): the per-region tax was supposed to flatten
G by taxing enriched regions. But training settled degenerately — the exact B4
freeze rule froze 7 regions on cold-start low confidence, and the 500-settle
criterion stopped training before any tax could be learned. All taxes stayed at
zero. The mechanism never operated.

The eval results show:
1. **B3 violations** in ceiling/O and redteam: G rises with depth via selection
   enrichment (low-confidence items drop out, raising the mean). The zero-tax
   controller cannot address this. FM6 not solved.
2. **B8 nonvacuity failure**: The honest-family B3 "pass" is degenerate — constant
   C* with zero tax gives flat G, but it's not calibration, it's inaction.
3. **B13 violations**: The untaxed C* (≈968/1000 on correct) combined with the
   ceiling/O population gives G≈−0.49 — the confidence does not track the
   all-correct reality.

**Kill honestly:** The mechanism as specified cannot learn. The 500-settle rule
combined with the exact B4 cold-start freeze creates a degenerate fixed point
(zero taxes) that training cannot escape. This is a specification failure, not
an implementation bug. The Python cross-check confirms the Zag implementation
is faithful to the spec — the spec itself is what fails.

## 4. §6 horizon

Not run. §6 admits only forks clearing B1–B9+B13 on the short battery.

## 5. Artifacts

- Sources: `src/f34_mech.zag`, `src/f34_train.zag`, `src/f34_eval.zag`,
  `src/f34_harness.zag` (+ 20 frozen harness sources)
- Params: `params/f34_params_a.bin` (3,976 bytes, A/B identical)
- Results: `results/*_m34_d*_A.tsv` (37 legs, A/B identical)
- Analysis: `analysis/killbars.py`
- This verdict: `VERDICT_F34.md`
