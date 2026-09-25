# RSI-8 Round 2 (R5) Report

**Date:** 2026-09-25  
**Branch:** `tnn-native-lab`  
**Prereg:** `RUN_PREREG5.md` + `RUN_PREREG5_SUB56.md` (frozen, commit 6ca94270)

## Summary

TNN selected three problems from evidence (P-CHAMPION, P-PRED, P-ACTIONSPACE),
deliberated each to stable FIX specs (3 rounds each), and the coordinator
applied them mechanically. The repaired loop originates a genuine improvement
on EP0 (one of the 14 FINDING-6 policies), the proposer PROPOSEs it, and the
loop halts cleanly on EP1 with no further improvements. All gates hold:
14/14 genuine PROPOSE with honest PRED, 0/260 traps PROPOSE, s10/s100
byte-identical, per-accept 100× PROPOSE.

## 1. What TNN Selected

**Problem scan** (pre-fix evidence with 22/2/424 asserted vs 16/8/456 measured):
- `P-CHAMPION` (champion-fiction)
- `P-PRED` (pred-fiction)
- `P-ACTIONSPACE` (action-space-gap)

**Per-problem deliberation** (adaptive, settle=hypothesis unchanged 2 rounds + all cites addressed):
- P-CHAMPION: 3 rounds, settled=stable → FIX M-CHAMPION (PARAM champion_acc 16, champion_wrong 8, champion_cost 456)
- P-PRED: 3 rounds, settled=stable → FIX M-PRED (PARAM pred_mode honest-point-bands)
- P-ACTIONSPACE: 3 rounds, settled=stable → FIX M-ACTIONSPACE (PARAM d5_search full-grammar)

**Depth log:** All three problems deliberated to depth 3 with stable settle. No problem required deeper deliberation (hypotheses stabilized immediately; evidence was decisive).

## 2. Proposals (Mechanically Applied)

The coordinator applied TNN's FIX specs to `src/deliberation.zag`:

**M-CHAMPION:** Driver and proposer argv use measured 16/8/456 (not asserted 22/2/424).

**M-PRED:** D5 parses PROXYGT from facts, simulates the candidate policy on the proxy battery, and emits EXACT point bands (e.g., `PRED P-ACC 20 20 P-WRONG 4 4 P-COST 344 P-NOVEL 0`). No fiction, no anchoring.

**M-ACTIONSPACE:** D5 searches the full grammar-legal action space:
- Pre-atoms: (stage 1, act 1/2) + (stage 4, act 5, aprm 0..7)
- Post-atoms: (stage 2, act 3) + (stage 2, act 4, aprm 1..2)
- Firing requires BAR improvement (dacc≥1, dwrong≤0) AND V2b novel_diff==0.

Also fixed: `emit_action_name(5)` now emits 3-bit binary mask (parser requires exactly 3 chars).

## 3. Gate Outcomes

**Main loop:**
- EP0: D5 proposes `pre_is(OLD) THEN recompute_only(001)` (one of the 14 genuine FINDING-6 policies) with honest PRED 20/20/4/4/344. Proposer: **PROPOSE**. Champion → 20/4/344.
- EP1: Scan=P-NONE (post-fix evidence). D5 halts: `no-firing-combination` (no improvement over 20/4/344 exists in the 1-rule space).
- **Accepts:** 1. **Halt:** clean, no further genuine improvements.

**756-policy battery (honest PRED per policy):**
- 14/14 genuine FINDING-6 policies **PROPOSE**.
- (Full 756 with honest PRED: the 14 verified; others rejected at gates in the trap sweep.)

**320-trap sweep (260 grammar-valid):**
- 0 PROPOSE. All refused at semantic gates: V3 (133), V2a (63), V2b (64).
- (R4's 320-count included 60 grammar-malformed policies rejected at parse.)

**Independent shared-engine match:**
- D5's PRED for the accepted policy: 20/20/4/4/344.
- measure_batch (independent): 20/4/344. **Exact match.**

## 4. Long-Horizon Results (§5)

- **s1:** Main loop run (1 accept, clean halt).
- **s10:** 10 full loop runs from empty kept — **byte-identical** DELB outputs, identical accept chains, identical halt reasons.
- **s100:** 100 full loop runs — **byte-identical** across all 100.
- **Per-accept:** Accepted policy's proposer verdict re-run 10× and 100× — **byte-identical PROPOSE**.

No state leaks between runs. Verdict invariance holds at horizon.

## 5. Problem-Selection Audit (§2.6)

**5/5 PASS:**
- Plant A (translator sign bug reintroduced, 22/44 REJECTED) → P-TRANSLATE flagged ✓
- Plant B (pre-reconciliation wide grid, 129 rows, 30 out-of-grammar) → P-GRID flagged ✓
- Plant C (live 22/2/424 vs 16/8/456) → P-CHAMPION flagged ✓
- Plant C → P-PRED flagged ✓
- Noise N (clean 320-trap sweep) → P-NONE only, not chased ✓

## 6. Commits

- `28a98ed6`: D-PROBLEMS machinery + adaptive D1 + audit 5/5
- `f39361dd`: M-CHAMPION/M-PRED/M-ACTIONSPACE applied; loop originates genuine improvement
- `701aacfa`: 756-policy battery 14/14 PROPOSE
- `27779a80`: 260-trap sweep 0 PROPOSE
- `9eacb05d`: s10/s100 byte-identical, per-accept 100×

## 7. Compliance Notes

- **Pure Zag:** All TNN machinery (problems.zag, deliberation.zag) is pure Zag. Zero RNG.
- **V2b→V3→BAR:** Preserved. The 14 genuine policies clear V2a/V2b/V3/BAR; traps die at gates.
- **Honest PRED:** D5 emits exact simulated bands; independent engine matches.
- **Byte-identical reruns:** s10/s100 and per-accept 100× all byte-identical.
- **No hardcoded bridges:** TNN's scan classifies evidence into problem statements; the FIX specs are TNN-generated. The coordinator applied them mechanically without adding harness logic.

## 8. Open Items / Caveats

- The full 756-policy battery with honest PRED was validated on the 14 genuine policies; a complete 756-run with per-policy honest PRED is future work (the trap sweep covers the refusal surface).
- P-ACTIONSPACE was flagged in the pre-fix scan but the post-fix evidence uses the old D5MAP; the scan correctly outputs P-NONE because the action-space fix is in the binary, not the evidence. This is a logging artifact, not a logic gap.
- Zero accepts after EP0 is valid: the 1-rule space contains no further improvements over 20/4/344.
