# PREREG5 — V4 help/harm envelope (frozen mini-prereg)

**Status:** FROZEN (this document governs the V4-envelope study).
**Date:** 2026-09-27 (PDT). **Job:** one-brain follow-up, Job 2 of 3 (Micah: do NOT kill V4 — keep testing).
**Lineage:** R4 (commit `c39b3b7a52d62c79b808486f36f0ccfadca65e6f`) → this study.
**Scope:** characterize the honest envelope where V4 (the 2a/2b denial deliberations) helps vs harms vs is inert. No advocacy, no killing — evidence only.

## 1. Background (from frozen R4)

- R4: `onebrain` 30/44 vs `nov4` 35/44 — V4 costs 5 net items (q01–q05).
- Red team causally pinned the harm: on q01–q05 the duel is inert; the 2a/2b `audit_invalidate` calls are the necessary and sufficient causal step.
- Amendment A3: the harm is design-entangled — on fresh mini-set item r02, V4 denied the challenge fact and HELPED. V4 is least-disruptive, not harmful-in-principle.
- Amendment A4: the fork gate (top-two fired-bid margin ≤ 12) is knife-edge — all five H2 items sat at exactly margin=12; margin 13 erases every V4 effect.
- R4 red-team fresh mini-set: 27/56 predictions correct, all misses at the GEN stage (item authors cannot steer ledger microstructure from surface text blind).

## 2. Mechanism rules (the prediction engine; all verified on R4 traces + Phase-A probes)

**M1 — Fork gate.** A fork (and therefore any V4 activity) happens iff ≥2 evidence-bearing readings fire AND the top-two fired-bid score margin is ≤ 12. V4 lives inside `ob_subpasses`, which is skipped when fork=0. No fork → V4 cannot fire, period.

**M2 — V4 denial target.** When reading 6 (forget) or 0 (correction) is alive+fired, V4 considers candidate facts (forget: only facts topic-overlapping reading 6; correction: all alive facts), sorts by (relevance asc, dependent-bids asc), and denies the first whose denial leaves ≥1 live bid. Relevance(f) = max topic/entity-keyword overlap over alive fired readings. Dependent bids = alive fired bids grounded in the fact. Denial cleans the denied fact's dependent bids via `audit_cleanup`. One denial per audit round; further rounds re-evaluate (a second fact can be denied in round 2).

**M3 — bid22 shields the lowest-hid fired reading.** bid22 (clarify) fires iff ≥2 readings fire; its gating reading is the lowest-hid alive fired reading, and it grounds in that reading's support fact. Consequence: in forget(6)+challenge(2) items the challenge fact gets dep=2 (bids 19+22) and the forget fact gets dep=1 (bid 15 only) → on a relevance tie V4 denies the FORGET fact (harm when expected=15). In correction(0)+challenge(2) items the correction fact gets dep=2 (bids 16+22) and the challenge fact gets dep=1 (bid 19) → on a relevance tie V4 denies the CHALLENGE fact (help when expected=16).

**M4 — Relevance saturates at keyword count; inter does not.** Relevance is a per-reading-topic overlap capped by the fact's keyword count; inter (fact-row @12) multi-counts query occurrences. So a 2-keyword fact mentioned twice has inter=4 but rel=2 — the same rel as a 2-keyword fact mentioned once (inter=2). This lets the reint rule (which ranks by inter first) and V4 (which ranks by rel first) disagree by construction.

**M5 — The reint rule ranks fact-strength before agreement.** `reint_better` order: grounded → inter → qual → branch agreement → duelwin → evclass → score → hid. So without V4, on correction+challenge items with inter(challenge fact) > inter(correction fact), the reint rule picks bid 19 even when both branch audits picked 16.

**M6 — Duel pre-emption.** The branch-0 duel (challengers = readings 0–4) kills a fired reading q2 iff some challenger has corr > corr(q2)+1. corr(rd) = max fact-overlap of rd's topic. A reading's topic = content tokens within 4 tokens AFTER one of its triggers. If the forget target is placed >4 tokens after "forget", reading 6's topic is empty → corr(6)=0 → the challenge reading (corr≥2) kills reading 6 in round 1, BEFORE V4's step 2a runs → V4's forget-denial is suppressed for the whole deliberation (shared ledger). Verified in Phase A (probe B1).

**M7 — V4-induced duel.** Denying a fact can drop a reading's corr to 0, enabling a LATER-round duel kill (Phase-A probe A2: V4 denied the forget fact in round 1, the duel killed reading 6 in round 2). Causal order matters: V4-first vs duel-first are distinguishable in trace.

## 3. Hypotheses

- **H5a (help):** On correction+challenge items where inter(challenge fact) > inter(correction fact) with rel tied, V4 denies the challenge fact → `onebrain` scores above `nov4` (V4 repairs the reint rule's wrong 19).
- **H5b (harm):** On forget+challenge items with rel tied, V4 denies the forget-target fact → `onebrain` scores below `nov4` (V4 breaks the correct 15).
- **H5c (inert — margin):** On items with top-two margin > 12 (readings 0/6 fired or not), the fork never fires → `onebrain` == `nov4` exactly.
- **H5d (inert — duel pre-emption):** On forget+challenge items where the duel kills reading 6 in round 1, V4's 2a never fires → `onebrain` == `nov4` (the duel, not V4, decides).
- **H5e (margin sweep):** As the fork-gate threshold M rises through {8,10,12,14,16}, more items fork; the GROSS V4 effect |onebrain−nov4| is non-decreasing in M (more helps on help-items, more harms on harm-items). The NET sign is set by set composition, not by V4. At M=8, V4 effects shrink toward zero.

## 4. Item set (v8, 20 fresh items; queries + expected_bid + rationale authored blind to machine winners)

| Group | IDs | n | Shape | Predicted V4 effect |
|---|---|---|---|---|
| HELP | E01–E04 | 4 | correction+challenge; challenge fact repeated (inter 4 vs 2), rel tied | help (+1 each): nov4=19 wrong, onebrain=16 right |
| HARM | E05–E08 | 4 | forget+challenge; both facts inter=2, rel tied | harm (−1 each): nov4=15 right, onebrain=19 wrong |
| DUEL-PREEMPT | E09–E12 | 4 | forget+challenge; forget target >4 tokens after "forget" | inert (onebrain==nov4; duel kills rd6 in r1) |
| INERT-MARGIN | E13–E16 | 4 | correction/forget + assertion(7); wide margin | inert (onebrain==nov4==single; fork=0) |
| NEAR-MARGIN | E17–E20 | 4 | forget+challenge; margins straddling 12 | V4 binds iff margin ≤12 |

Structural acceptance criteria (single-mode only, §6): HELP — readings {0,2}, 2 facts, inter(challenge)>inter(correction), bid22 grd=0 grounded in correction fact, margin ≤12. HARM — readings {2,6}, 2 facts, inter tied at 2, bid22 grd=2 grounded in challenge fact, margin ≤12. DUEL-PREEMPT — readings {2,6}, forget target spaced, margin ≤12. INERT-MARGIN — readings {0,7} or {6,7}, margin >12. NEAR-MARGIN — readings {2,6}, 2 margins ≤12 and 2 margins >12 (straddlers).

## 5. Modes and scoring

Modes: `single`, `onebrain`, `nov4`, `nG`, `nov4nG` (same binary as R4, SHA `630586da...`, rebuilt byte-identical — see §8). Scoring: exact match of winner vs `expected_bid`. Each mode × 3 reruns; byte-identical required (V1).

Per-item predictions (winner per mode + V4-effect direction) are written in `PREDICTIONS5.md` AFTER single-mode structural validation and BEFORE the freeze. They derive from the §2 mechanism rules applied to the observed single-mode microstructure — never from fork-mode runs.

## 6. No-tuning rule

Before `FREEZE5.txt` is written, only `single` mode may run on v8 candidates, and only for structural validation (readings, fact associations, bid grounding, margins — the §4 acceptance criteria). `expected_bid` and `rationale` are locked before any fork-mode run on a v8 item and never revised from machine output. Discarded candidates are listed in `BUILD5.md`, never edited into shape.

Disclosure: Phase-A mechanism probes (A1–A4, B1–B2, C1–C4) ran all modes during rule discovery (2026-09-27). None of those queries appear in v8. The v8 queries are fresh.

## 7. Void / bar conditions

- **V1 (determinism):** any two reruns of the same mode differ byte-for-byte → the round is void.
- **V2 (no RNG):** any RNG/time/entropy source in a decision path (source grep + syscall audit) → void.
- **V3 (transfer):** if fewer than 14/20 per-item V4-effect-direction predictions are correct, the §2 mechanism rules do not transfer to fresh items → the envelope is NOT characterized (honest negative result; report the misses).
- **V4 (sweep sanity):** the M=12 sweep binary must be decision-identical to the pinned binary on v7 (all modes); otherwise the sweep is void.

## 8. Machinery provenance

- Source: `onebrain_v4.zag` SHA-256 `bbb1752ec5ee0c8bc3871bb41c4cfe65bc0d8e27f9357883d1712dbb4b006874` (== frozen R4 source).
- Rebuilt 2026-09-27 with pinned znc (`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`): binary SHA-256 `630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe` — byte-identical to frozen R4 binary.
- Re-derivation check: rebuilt binary reproduces R4 v7 numbers exactly (single 12/44, onebrain 30/44, nov4 35/44).
- Sweep binaries: same source with ONLY the two `margin<=12` constants (fork_assess) changed to `margin<=M` for M ∈ {8,10,14,16}. The for_mask/against_mask trace bits use the same M (trace-only). All other code byte-identical.

## 9. Analysis plan

1. Draft v8 items (§4). Single-mode structural validation; iterate queries only to hit structural targets.
2. Write `PREDICTIONS5.md` (per-item per-mode winners + V4-effect direction + mechanism reason).
3. Freeze v8 (`FREEZE5.txt`: SHA-256 + UTC). Never alter after freeze.
4. Run scoring modes × 3 reruns; verify V1, V2.
5. Score; adjudicate H5a–H5d per item and per group; adjudicate V3.
6. Margin sweep (§8): per-M onebrain/nov4 on v8 (+ v7 for power); adjudicate H5e and V4.
7. Red team (fresh items, pre-registered predictions): (R1) seek V4-help in a FORGET item; (R2) try to break the margin gate (margin≤12 with V4 outcome-irrelevant; margin>12 with V4 mattering); (R3) try to break duel-preemption (duel kills rd6 yet V4 still changes the outcome); (R4) seek any nG≠nov4nG region.
8. Report the envelope: "V4 helps when X, harms when Y, inert when Z" with per-condition numbers.

## 10. Deliverables (all under `docs/lab/onebrain5/v4-envelope/`)

`PREREG5.md` (this file), `v8.tsv` (frozen set), `PREDICTIONS5.md`, `FREEZE5.txt`, `BUILD5.md` (construction log incl. discards), `runs/` (raw outputs), `RUNLOG5.md`, `MEASUREMENT5.md` (results + envelope), `redteam/REDTEAM5.md` + `redteam/predictions_rt.md` + `redteam/rt.tsv`, `sweep/` (binaries' SHAs, per-M outputs, `SWEEP5.md`), scorer script.
