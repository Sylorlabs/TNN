# VERDICT-SG-FOLLOWUP — Sol-vs-Grok follow-ups (2026-09-22)

Follow-up package to the Sol-vs-Grok duel (VERDICT.md: SCENARIO-FIT, no
champion). All three future bars from the duel verdict were built in pure
Zag, frozen per PREREG-SG-FOLLOWUP.md, and tested on a fresh sealed battery
(celestial vocabulary, disjoint from calib and scored; 384 teach / 432
probes; check_sg.py 0 failures). Frozen Sol/Grok binaries were re-run on
the same sealed battery as the reference.

## Sealed-battery results

| build | SG-PARA | SG-SAFE | SG-PREC | SG-COMP | SG-WRONG |
|---|---|---|---|---|---|
| sol | 0.5000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| grok | 1.0000 | 0.9167 | 0.8672 | 0.1250 | 0.2153 |
| **verify (a)** | **1.0000** | **1.0000** | **1.0000** | 0.1250 | **0.0000** |
| coref1 (b1) | 1.0000 | 0.9167 | 0.9219 | **1.0000** | 0.1667 |
| coref2 (b2) | 1.0000 | 0.9167 | 0.9062 | 0.7500 | 0.1806 |
| gated (c) | 1.0000 | 1.0000 | 0.9808 | 0.7500 | 0.0139 |

Per-slice (correct/total), sealed: grok's 93 wrong-values were neg 3,
hedge 3, distr 24, multi 21 (non-correct incl. unknowns: neg 3, hedge 3,
distr 24, multi 21). verify: neg/hedge/distr all 24-48/48 correct via
vetoes (attestation=48, subject=39, tie=6 in proofs), multi 3/24 unchanged.
gated: neg/hedge 24/24, distr 48/48, multi 18/24 — its 6 residual
wrong-values are all same-entity wrong-relation BoW picks in multi, which
neither the subject gate nor the attestation gate can see.

## Bar decisions (preregistered)

- **(a) verify-direction hybrid — HYBRID CHAMPION.** Bars: SG-PARA ≥
  1.00 − 0.01 = 0.99 ✓ (1.0000 — kept ALL of Grok's paraphrase, typo 48/48)
  and SG-WRONG ≤ 0.05 ✓ (0.0000 — all 93 wrong-values eliminated).
  The verifier buys safety at zero paraphrase cost on the sealed battery.
  (On the visible calib battery the tie veto cost 12 typo-correct; the
  veto's price is battery-dependent — sealed it was free.)
- **(b1) coref-in-lex — PASS (diagnostic).** SG-COMP 24/24 ≥ 20/24 ✓,
  SG-WRONG 0.1667 ≤ grok's 0.2153 ✓, SG-PARA 1.0 ✓. The "neither does
  coref" cell is repaired: appending the resolved entity's stems to the
  teach row's lex generalizes to unseen vocabulary.
- **(b2) separate entity-similarity term — FAIL (capability bar).**
  SG-COMP 18/24 < 20/24. It scored 24/24 on the visible calib battery, so
  the re-ranking design is battery-sensitive: when the correct row's
  unbonused score falls below the 1/4 threshold, no bonus can save it.
  The in-lex design (b1) is strictly more powerful and it generalizes.
- **(c) gated Grok — champion-ELIGIBLE, runner-up.** Eligibility:
  PARA 1.0 ≥ 0.97 ✓, WRONG 0.0139 ≤ 0.05 ✓, SAFE 1.0 ≥ 0.90 ✓;
  margin vs Sol 0.50 ≥ 0.03 ✓. Not named champion: verify (a) dominates it
  on every frozen metric (WRONG 0.0000 vs 0.0139, PREC 1.0 vs 0.9808;
  PARA/SAFE tied). Unexpected finding: the subject gate repaired most of
  multi too (18/24) — the multi wrong-values were cross-entity ties.

## Package verdict

**The original SCENARIO-FIT, no-champion verdict is OVERTURNED.**
**CHAMPION = sg_verify, the verify-direction hybrid** (Grok proposes →
verifier gates): SG-PARA 1.0000 with SG-WRONG 0.0000 — Grok's full
paraphrase reach with Sol-grade safety. The duel's dilemma (paraphrase vs
safety) was real for the two pure contenders, but the verify-direction
hybrid dissolves it: propose generously, verify strictly.

Untested composition (verify gates on top of gated retrieval) is future
work — it was not preregistered and was not built.

## Kill bars

- KB-F-DET: 5/5 runs byte-identical (stdout + proof SHA256) for all six
  binaries — PASS (see evidence/followup/RUNS.md).
- KB-F-PROOF: 432 proof lines per build — PASS.
- KB-F-TOOL: only the known-benign A0101 analyzer note; no new warnings
  — PASS.
- KB-F-CACHE: no binaries or .zagd committed — PASS.

## Evidence

- `evidence/followup/<build>/verdicts_run{1..5}.txt` — all five sealed runs
- `evidence/followup/<build>/proof_*.txt` — proof traces (veto/gate fields)
- `evidence/followup/RUNS.md` — SHA256 manifest
- `evidence/followup/sealed_scores.txt` — scorer output
- `gen/followup/` — sealed battery (teach/probe/expected/frames)

Note: `gen/score_fup.py` had a JSON-serialization bug in its summary print
(the metrics table was always correct); fixed formatting-only after the
sealed runs, metrics unchanged, table re-verified identical.
