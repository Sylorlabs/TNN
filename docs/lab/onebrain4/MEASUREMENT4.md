# MEASUREMENT4 — One-Brain Round 4 results

**Date:** 2026-09-27 (PDT). **Round:** R4, component disentanglement.
**Lineage:** R1 (H1 killed), R2 (H1′ killed), R3 (H1″ first pass, K1″ 23/44 > 20/44;
red-team amended the mechanism story: reintegration pre-empted-not-decorative,
V4 denial-determinative only where it hurts).

## Hypothesis H1‴ (from frozen PREREG4)

On a fresh frozen set containing V4-binding items and reintegration-room items
built so V4 does not pre-kill the challengers (repairing v6's redundancy flaw):

1. Deliberative reintegration alone (V4 off) beats the honest null — reintegration carries real accuracy.
2. V4's marginal given reintegration is ≤ 0 — V4 is net-neutral-or-negative.
3. Full onebrain > single deliberation replicates on the fresh set (lineage check).

## Frozen inputs (all SHA-verified)

| Input | SHA-256 |
|---|---|
| PREREG4.md | frozen alongside v7 (see FREEZE4.txt) |
| v7.tsv (44 items) | `3f3b3d6c34364460fdd54303729033e02c2da2f5c9960ea1586a72efd95bda3a`, frozen 2026-09-27 22:32:05 UTC |
| impl/onebrain_v4 (binary) | `630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe` |
| impl/onebrain_v4.zag (source) | `bbb1752ec5ee0c8bc3871bb41c4cfe65bc0d8e27f9357883d1712dbb4b006874` |
| toolchain znc | `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` |

Freeze compliance: only `single` ran on v7 candidates before freeze (structural
validation, permitted by PREREG4 §6; disclosed in FREEZE4.txt). Implementation
crew never saw v7 before freeze; set-builder never opened any .zag source.

## Scores (/44, frozen v7)

| Mode | Score | What it is |
|---|---|---|
| nov4 (reint on, V4 off) | **35** | reintegration alone |
| onebrain (reint on, V4 on) | **30** | full machinery |
| min (bare driver) | 30 | TNN's-own-decision scaffold check |
| ablate (shared ledger off) | 26 | channel ablation |
| nov4nG (honest null, V4 off) | 24 | reint-off, V4-off |
| poison | 17 | causal sanity (23 NO_VERDICT) |
| nG (honest null, V4 on) | 16 | reint-off, V4-on |
| single | 12 | single deliberation |

Determinism: 8 modes × 3 reruns, all byte-identical (24/24). Independent
re-derivation: rebuilt binary byte-identical to pinned SHA; all 8 mode outputs
reproduced byte-identically. No RNG in decision paths (source grep + rerun
identity + read/write/open/close-only syscalls).

## Kill-bar adjudication

| Bar | Rule | Numbers | Verdict |
|---|---|---|---|
| K1‴ | nov4 ≤ nov4nG kills Claim 1 | 35 vs 24, margin **+11** | NOT TRIGGERED — Claim 1 survives |
| K2‴ | onebrain − nov4 ≥ +2 kills Claim 2 | 30 − 35 = **−5** | NOT TRIGGERED — Claim 2 survives (V4 costs 5 net items) |
| K3‴ | onebrain ≤ single kills Claim 3 | 30 vs 12, **+18** | NOT TRIGGERED — Claim 3 survives |
| K4‴ | any rerun pair differs | 24/24 identical | PASS |
| K5‴ | RNG in decision paths | zero markers | PASS |
| K6‴ | min does not fan out | min forked 41/44 | NOT TRIGGERED |

**Verdict: H1‴ SURVIVES — all three claims hold numerically and mechanistically.
No kill bar triggered; the round is not void.**

## Mechanism decomposition (white-box, trace-verified)

- **Claim 1 (+11):** the nov4−nov4nG margin decomposes to +14 reintegration-rule
  fixes − 3 reintegration-rule harms (q06–q08, where the rule's fact-strength
  ranking picks 19). The honest null is uncontaminated: CLOSE is provably
  read-only (352/352 trace blocks, never overrides). The nov4nG−single +12 gap
  (24 vs 12) is fully explained by the branch duel killing the joke bid —
  not leakage.
- **Claim 2 (−5):** on q01–q05 the duel is inert in every branch of every mode;
  the 2a/2b `audit_invalidate` calls (denial → `AUDIT_CLEAN` of the expected
  bid's fact) are the necessary and sufficient causal step. The −5 decomposes
  to exactly those 5 items.
- **Claim 3 (+18):** onebrain 30 vs single 12; min (bare driver) matches
  onebrain at 30, so the gain is TNN's own decision, not scaffold.

## Red team (7 attacks — no kill; 4 amendments required)

Independent red team: re-derivation (byte-identical binary + outputs), hardcode
audit (no v7 literals; exactly the 3 documented deltas vs v3), attribution
probes, fresh 8-item mini-set with pre-registered predictions, determinism.
Full report: `redteam/REDTEAM4.md`. **No attack killed any claim.** Four
amendments to the round's story are required and are incorporated here:

- **A1:** PREREG4 §3 mislabels `ablate` as "fork disabled" — ablate forks 41/44;
  what it disables is the *shared ledger* (shared=0). Diagnostic only; no
  kill-bar impact. Read all "ablate" comparisons as shared-ledger-off.
- **A2:** DESIGN_NOTES.md's H1 prediction is falsified by trace: on q06–q08,
  nov4 (V4 off) answers 19, not the predicted 16 — the reintegration rule's
  own fact-strength ranking picks bid 19 with no V4 involvement. Claim 2's
  mechanism evidence is the 5 H2 items (q01–q05), not 8.
- **A3:** "V4 is harmful" is restated: V4's least-disruptive denial bound the
  intended fact on the 5 H2 items, but the harm is design-entangled — the items
  were built so the denied fact carries the right answer. It does not
  generalize: on fresh mini-set item r02, V4 denied the challenge fact and
  *helped*. V4 is least-disruptive, not harmful-in-principle.
- **A4:** The fork gate (top-two fired-bid margin ≤ 12) is knife-edge: all five
  H2 items sit at exactly margin=12; one bonus point the other way (mini-set
  r01: margin 13) erases every V4 effect. Legitimate (pre-freeze verified per
  PREREG4 §6) but fragile — future sets should not pile mechanism evidence on
  margin-12 items.

## Honest scope

- Withhold-by-absence (q41–q44, expected 23): **0/4 on every mode** — the
  generator's known limitation (machinery answers 19/20 on KB-absent claims),
  unchanged since R2. Not a regression; not yet fixed.
- Support-quality items (q29–q36): mixed — reintegration fixes some, V4
  re-breaks others. Cat-D-like room is partially, not fully, closed.
- single scores 12/44 on v7 vs 20/44 on v6: by design — v7 was built with
  reintegration-room items where score order is wrong. Not a degradation of
  the single baseline.

## Bottom line

R4 disentangled R3's components: the deliberative reintegration carries +11
items of real accuracy on its own; V4's fact-invalidation costs 5 net items
once reintegration does the discriminating; the one-brain gain over single
replicates on a fresh set (+18). The red team could not kill any of it, but
narrowed the story honestly: V4's harm is design-entangled, not a general
property, and the fork gate it depends on is knife-edge.
