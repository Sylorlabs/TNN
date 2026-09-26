# Adoption Evidence — Deliberative Pricing

**Date:** 2026-09-26
**Branch:** `tnn-native-lab`
**Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
**Pre-adoption source:** `c442e892fa0a` (`docs/lab/wave8/strength-retrial/port-fix-2026-09-26/implementation/`)

All runs: pure Zag, zero RNG, deterministic.

---

## 1. Pre/post regression table (byte-identical)

| Suite | Cells | Passes | Pre source | Post result |
|---|---|---|---|---|
| S1 matrix (B/C/C-P3/B2 × VUP/WBS/JI × 0/1/2) | 36 | 2 | `pre_evidence/s1_p{1,2}/` | 72/72 byte-identical |
| Gates B/C/C-P3/B2 | 4 | 2 | `pre_evidence/gates/` | 8/8 byte-identical |
| Wedge battery (W1..W8) | 1 | 2 | — (port-fixed) | `WB_VERDICT fail=0`, byte-identical |
| Adoption battery | 51 checks | 2 | — (new) | 51/51 pass, byte-identical |

**Total: 80 regression outputs compared, 0 byte-differences.**

The high-water default (`ST_PRICE_HIGHWATER`) is unchanged; frozen pre-adoption
drivers produce byte-identical output. Deliberative pricing is opt-in per store
via `st_set_price_mode(s, ST_PRICE_DELIB)`.

Manifest: `evidence/regression_manifest.txt` (SHA256 per output).

## 2. Personality-mismatch → 122 (explicit)

From `evidence/adopt_test.out`:

| Check | Result |
|---|---|
| `M_delib_price` (HIST deliberation, price) | 2 — PASS |
| `M_cost_before` (COST under HIST) | 2 — PASS |
| `M_cost_mismatch` (COST after switch to FRESH) | -1 — PASS |
| `M_kill_122` (destroy after switch) | 122 — PASS |
| `M_122_numeric` (exact code) | 122 — PASS |
| `M_still_live` (slot survives the refusal) | 1 — PASS |
| `M_fresh_price` (fresh FRESH deliberation) | 2 — PASS |
| `M_rekill_ok` (destroy after fresh deliberation) | 0 (ST_OK) — PASS |
| `M_ck` (checker agrees) | 0 — PASS |

The old-personality deliberation does not bind after the switch. Destruction
returns 122 (never a discount). A fresh deliberation under the new personality
restores lawful destruction.

## 3. Weight preservation (hand-authored, unchanged)

| Check | Ledger | Price | Expected | Result |
|---|---|---|---|---|
| W1_base | ADD50 | 1 | 2+0−1+0+0=1 | PASS |
| W2_strong | ADD90 | 2 | 2+1−1+0+0=2 | PASS |
| W3_weak | ADD10 | 0 | 2+0−1+0+0−1=0 | PASS |
| W4_contested | ADD50+3 cites | 3 | 2+0+1+0+0=3 | PASS |
| W5_salient | ADD50+JUSTIFY6 | 2 | 2+0−1+1+0=2 | PASS |
| W6_directive | ADD50+JUSTIFY7 | 4 | override | PASS |
| W7_retract | ADD50+JUSTIFY3 | 0 | 2+0−1+0−1=0 | PASS |

## 4. Personality contrast (HIST vs FRESH)

| Check | Price | Result |
|---|---|---|
| P_hist (sees pre-overwrite trail) | 4 | PASS |
| P_fresh (epoch-scoped) | 2 | PASS |

## 5. Fail-closed edges

| Check | Result |
|---|---|
| N_kill_122 (no deliberation) | 122 — PASS |
| S_kill_122 (stale after STRENGTHEN) | 122 — PASS |
| O_third_cite_122 (over-cite at CITE) | 122 — PASS |
| O_kill_ok (slot not bricked) | ST_OK — PASS |
| U_kill_109 (under-cite) | 109 — PASS |
| E64_price (2³² vs 0 distinct) | 3 — PASS |
| K_tnn_113 (trainer-only kill) | 113 — PASS |
| K_trainer_ok | ST_OK — PASS |
| D_delete_strong_ok (DELIB via DELETE_STRONG) | ST_OK — PASS |
| G_double_spend_121 (store-wide) | 121 — PASS |

All 51 checks pass; the independent checker (`ck_verify`) agrees on every
ledger (0 failures).

## 6. Source SHAs

- `src/strength_core.zag`: `876715093d5fd9b876b2aae99d909913017386fd3c83cafb3b6d67d3bc2b2c60`
- `src/strength_checker.zag`: `aa7b76ac737f36399a9e8f2b3765bf59a09a8ff58a0ef2cf46f46bdff6e3680e`

Verify: `python3 scripts/verify_adoption.py`
