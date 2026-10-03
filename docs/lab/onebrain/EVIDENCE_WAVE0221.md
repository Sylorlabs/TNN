# EVIDENCE — Experiment 2 Follow-up (wave-20260927-0221pdt)

**Prereg:** `docs/lab/onebrain/PREREG_WAVE0221.md` @ `06e28f088` (frozen before implementation).
**Problem freeze:** `32eadf722` (S2, S3, 5 batteries; SHA-pinned before scoring).
**Machinery:** frozen `onebrain.zag` + `ob_*.zag` (2321pdt). No params tuned.
**Toolchain:** `znc_linux_x86_64_abed8aa1` (sha256 `498abcb5...58ef`). Pure Zag, zero Python.
**Status:** All kill bars pass. Regression sweep clean. Red-team review pending (worker cannot spawn subagents; parent to arrange).

## 1. Broader holdouts (new ambiguity structures)

Two new 10-problem holdouts, hand-authored to frozen design rules, SHA-pinned before scoring:

- **S2 "synergy"** (`problems_holdout_s2.tsv`, sha `40bb2be3...`): rescue-required. Strong early misleading (+730), weak attacks (-300), late correct supports. Max |attack| 300 < 650 (XEXAM/TEST never fire).
- **S3 "slow-burn"** (`problems_holdout_s3.tsv`, sha `feb4fce2...`): distributed. All |w| <= 350. Misleading strength spread across e3/e4; correct supports late (e5/e7/e8).

Both are synthetic mechanism probes (prereg syntheticity note). Correct reading balanced 5/5.

### Per-mode accuracy

| Holdout | one-brain | baseline | ablation (b0) | forked |
|---------|-----------|----------|---------------|--------|
| S2 (10) | 10/10     | 0/10     | 0/10          | 10/10  |
| S3 (10) | 10/10     | 0/10     | 0/10          | 10/10  |
| Original (10, continuity) | 10/10 | 0/10 | 0/10 | 10/10 |

K1 (conjunctive): one-brain > baseline AND ablation(b0) < one-brain. **PASS** on S2, S3, and original.

## 2. K4 hardening (verdict-level)

The hardened bar: attack-lens-alone (ablation bv1) <= 5/10 (chance) on each new holdout.

### Branch-alone accuracies (ablation bv0/bv1/bv2 vs expected)

**S2:** bv0 0/10, **bv1 0/10**, bv2 0/10.
- All three branches alone are WRONG; the shared ledger is RIGHT (10/10).
- Fully decisive verdict-level K4. Stronger than the prereg prediction (which expected b2 wrong by intent; confirmed).

**S3:** bv0 0/10, **bv1 0/10**, bv2 10/10.
- b0 and b1 alone are WRONG; b2 (rescuer) alone coincides with the shared verdict.
- The hardened bar targets the attack lens specifically: **PASS** (0/10 <= 5/10).
- The b2 coincidence is the prereg-predicted caveat, recorded here.

**Original (continuity):** bv1 10/10 (the known caveat from last wave; motivates the hardening).

K4-hardened: **PASS**. The attack lens alone is at 0/10 (below chance) on both new holdouts, so when the shared ledger is correct, the verdict-level evidence is decisive.

### K4 trace-level (supporting)

Delete/reorder on S2-01, S3-01, HO-01 (generalized driver `ob_delreord2.zag`):
- S2-01: delete PASS (changes fan-out), reorder PASS, not-decorative PASS (no branch reproduces the verdict).
- S3-01: delete PASS, reorder PASS, not-decorative FAIL (b2 reproduces; the caveat).
- HO-01: delete PASS, reorder PASS, not-decorative FAIL (b1 reproduces; known).

## 3. K2 poison (causal)

On S2-01 and S3-01 (`ob_poison2.zag`, generalized driver):
- S2-01: evidence-poison PASS, hypothesis-poison PASS, control (isolation) PASS.
- S3-01: evidence-poison PASS, hypothesis-poison PASS, control (isolation) PASS.

K2: **PASS**. Shared poison changes observables; private-ledger control leaves other branches byte-identical.

## 4. K3 scaffold

Minimal driver (`ob_scaffold.zag`, no fan_out, no fork threshold, no branch logic):
- S2: forks on 10/10, verdicts identical to full driver.
- S3: forks on 10/10, verdicts identical to full driver.

K3: **PASS**. The fork decision lives inside the machinery (ledger-driven).

## 5. Regression sweep (R1)

Frozen batteries translated by `ob_battery.zag` (pure Zag, weights verbatim). Runs: `ob_run` (one-brain), `ob_baseline` (delib-v1 deep), `ob_ablate`.

| Battery | items | one-brain | baseline | ablation (b0) | R1 (ob >= bl) |
|---------|-------|-----------|----------|---------------|---------------|
| admit   | 248   | 248/248   | 248/248  | 248/248       | PASS          |
| logic   | 264   | 264/264   | 264/264  | 264/264       | PASS          |
| revoke  | 113   | 113/113   | 113/113  | 113/113       | PASS          |
| trap    | 127   | 127/127   | 122/127  | 122/127       | PASS          |
| cost    | 125   | 125/125   | 125/125  | 125/125       | PASS          |

**No regressions.** On trap, one-brain (127/127) exceeds baseline (122/127). Zero baseline-correct to one-brain-wrong flips on any battery (R2 diagnostic).

Note: `ob_score` has a 64-item cap; batteries scored with `ob_score2.zag` (pure Zag, 2048-item cap). The 64-item partial scores were discarded.

## 6. K5 determinism

3x byte-identical runs (S2 one-brain):
- TSV: `ee886787...` (all three identical)
- JSONL: `08ad6e79...` (all three identical)

K5: **PASS**. Full SHA manifest in `results_wave0221/DETERMINISM_WAVE0221.txt`.

## 7. K6 RNG audit

Grep over all `docs/lab/onebrain/*.zag`: one match, a comment ("Zero RNG"). No RNG in any decision path.

K6: **PASS**.

## 8. Design predictions vs observed (from prereg)

| Prediction | Observed | Match |
|------------|----------|-------|
| S2: ob 10/10, bl 0/10, b0 0/10, b1 0/10 | 10/10, 0/10, 0/10, 0/10 | YES |
| S2: b2 0/10 (fully decisive) | 0/10 | YES |
| S3: ob 10/10, bl 0/10, b0 0/10, b1 0/10 | 10/10, 0/10, 0/10, 0/10 | YES |
| S3: b2 may coincide (caveat) | 10/10 (coincides) | YES |

All prereg predictions confirmed.

## 9. Limitations (for red-team)

1. **Syntheticity.** S2/S3 are hand-authored mechanism probes, not grounded in real deliberation failures. Ecological validity is untested.
2. **b2 caveat on S3.** The rescuer branch alone reaches the shared verdict on slow-burn. The hardened K4 targets the attack lens; a future wave should harden against b2 as well.
3. **Trap battery.** One-brain beats baseline on trap (127 vs 122). This is positive but unexplained; the 5-item gap deserves a mechanism note.
4. **No Python breach (prior).** This worker ran Python during exploratory inspection before the prereg commit. Disclosed to parent. The evidence above was produced after the freeze using only pinned znc and shell.

## 10. Verdict

All kill bars pass under the hardened K4. No regression on the sweep. The experimental record is strengthened (broader holdouts, decisive verdict-level K4 on S2, K4-hardened on S3 with b2 caveat).

**Recommended: ADOPT as strengthened experimental record (broader holdouts).** Wire-in remains not on the table (per prereg; regression sweep was the prerequisite, now satisfied, but wire-in is a separate wave decision).

Queued next work: (a) independent red-team review of this evidence; (b) ground broader structures in real deliberation failures; (c) harden K4 against the rescuer lens (b2); (d) explain the trap 5-item gap.
