# WS1-B PREREG — forced-conscious vs mixed vs autopilot head-to-head

**Status:** FROZEN 2026-09-24 ~08:20 PDT (before any WS1-B run). Written by WS1-B, committed before running.
**Question (Micah):** "allow BOTH (conscious + autopilot) or FORCE EVERYTHING conscious?"
**Method:** pure Zag, zero randomness in any decision path, byte-identical reruns ×3 (SHA256).

## §1. Regime definitions (frozen)

| Regime | Definition | Deliberation leg | Refusal leg | Perception leg |
|---|---|---|---|---|
| **AUTOPILOT** | every decision through the fast path | cost_harness `mode=autopilot` (single batch pass, all evidence at once, no freezing/elimination/TEST) | `fastref` (S2b fast-path refusal rule) | F1 autopilot decoder (bill) |
| **FORCED-CONSCIOUS** | every decision through the deliberate path | cost_harness `mode=tocap` (always deliberate to cap 16) | cost_harness `mode=tocap` | F2 deliberative-trained mechanism (bill) |
| **MIXED** | conscious deliberation decisions, autopilot for perception/routine | `mode=tocap` (deliberation decisions go conscious) | `mode=tocap` (refusal is a judgment) | F1 (perception → autopilot) |

Routing is a frozen deterministic class→mode table (perception fixtures → F1; items_v2 + rt_d1 + refusal → tocap). Measured routing cost: 0 ops (table lookup). Production-router cost is out of scope and noted as a caveat.

Consequence to note explicitly: on the deliberation and refusal legs MIXED ≡ FORCED-CONSCIOUS numerically by routing definition; MIXED vs FORCED-CONSCIOUS differ only on the perception leg. MIXED vs AUTOPILOT differ on deliberation + refusal legs.

## §2. Batteries (frozen inputs)

| Leg | Battery | n | Source |
|---|---|---|---|
| D | items_v2 admit / revoke / logic / trap / cost | 248 / 113 / 264 / 127 / 125 (877 total) | tnn-lab/deliberation_depth/items_v2/ |
| RT | rt_d1 red-team (weakly-ambiguous adversarial admit judgments: POISON/BAIT/DOUBLE/CLEAN/STRONG) | 14 | tnn-lab/deliberation_depth/depth1_discipline/batteries/rt_d1.jsonl |
| RF | refusal (7 families) | 60 | tnn-lab/consciousness_cost/refusal.jsonl |
| S | stress: trap.jsonl × 10 passes, item ids suffixed `_p1.._p10` by deterministic generator | 1270 | generated from trap.jsonl |
| P | perception (ambiguous: omission/inattentional/ambiguity/illusion/redteam fixtures) | 14 | bill-committed results, reused as frozen evidence (no new runs) |

Binaries: cost_harness sha256 `01c562be2c194da93008110421bd5988499c196ee42434bc3a854a12cf556137`; fastref `5398177a68175011722c5b8b3475bd735a119df69c60e464ee9addbbcd3c2098`. Verified before running; any mismatch aborts.

## §3. Gates (frozen)

- **G1:** res.jsonl + led.jsonl byte-identical across 3 reruns per (leg, config) cell (SHA256).
- **G2:** per-item (id, ops, rounds, ev, correct) identical across 3 reruns.
- **G3 (sanity vs bill anchors):** Leg-D accuracy matches committed bill values within 0.001 (autopilot and tocap: 1.000 on all 5 batteries). Any miss → halt, do not interpret.

## §4. Bars (frozen)

Per battery B, regime pair (X,Y):

- **ACC(X,Y,B):** Δ = acc(X) − acc(Y). Tie-band = 1 item: admit 0.40pp, revoke 0.88pp, logic 0.38pp, trap 0.79pp, cost 0.80pp, rtd1 7.14pp, refusal 1.67pp, perception 7.14pp. Δ > band → X WINS; Δ < −band → X LOSES; else TIE.
- **OPS(X,Y,B):** mean ops/item. Cheaper WINS; <2% apart → TIE. Report ratio.
- **LED(X,Y,B):** mean ledger bytes/item. Cheaper WINS; <2% apart → TIE.
- **MEM(X,Y):** memory pressure per 1000 decisions = 1000 × (18,040 B per-item arenas + mean ledger bytes/item) + 20 MiB fixed. Report totals; cheaper WINS (<2% TIE).
- **CPA(X,Y,B):** ops-per-correct = Σops / Σcorrect pooled over 3 reruns. Lower WINS. (If both regimes score 0 correct → n/a, reported.)
- **NW (H5 never-worse law):** if acc(FORCED) − acc(AUTOPILOT) < −tie-band on ANY battery → **NEVER-WORSE VIOLATION**, flagged in the verdict regardless of other bars.
- **ST-FLAT (stress leg):** per-pass mean ops/item and mean ledger bytes/item over 10 passes; least-squares slope. |slope| ≤ 2%/pass → FLAT; slope > +2%/pass → COMPOUNDING; slope < −2%/pass → DECAYING. Reported per regime.

## §5. Decision rule (frozen)

Recommendation ∈ {FORCED, MIXED, AUTOPILOT, CONDITIONAL(rule)}:

1. If FORCED wins ACC on ≥1 battery and triggers no NW violation → conscious is accuracy-dominant; recommendation is FORCED or CONDITIONAL depending on bill ratios (OPS/LED/CPA) and where the wins sit.
2. If AUTOPILOT wins any ACC bar → autopilot is accuracy-competitive there; recommendation must be MIXED or CONDITIONAL, never FORCED.
3. If no regime dominates ACC → CONDITIONAL with the routing variable the data supports (modality vs ambiguity-class), or MIXED if the data supports the class router.
4. CPA is the tiebreaker when ACC is tied: the regime with the lower cost-per-correct-decision wins the battery.
5. KB-control numbers (WS1-A's leg) enter the final recommendation only as cited context, not as WS1-B evidence.

## §6. Determinism (frozen protocol)

Zero RNG in harness decision paths (harness_cost/DETERMINISM.md). All batteries frozen before runs. 3 reruns per cell; G1/G2 must hold before interpretation. Wall-clock is reported for context only and is never a bar. Stress generator is deterministic (id suffixing only, no content change); verification: stripping `_pK` restores the original 127 lines byte-identically.

## §7. Never-worse watch list (from prior lineage, to check explicitly)

- depth1_discipline: fork E (more machinery) scored 0.429 vs fork B 0.571 on rt_d1 — more mechanism, less accuracy. WS1-B re-tests whether forced-conscious (tocap) loses accuracy to autopilot on rt_d1.
- KB-control: untrained deliberate (A3) committed 28 collateral true-kills — more consciousness made outcomes worse when untrained. WS1-A re-verifies; WS1-B does not rerun this leg.

## §8. Cells to run (69 total)

- D: 5 batteries × {autopilot, tocap} × 3 = 30
- RT: rt_d1 × {autopilot, tocap} × 3 = 6
- RF: refusal × {fastref, tocap} × 3 = 6
- S: trap×10 × {autopilot, tocap} × 3 = 6
- P: 0 new runs (frozen bill evidence)
- Reference context (cited, not rerun): bill adaptive-mode rows; bill perception wall/ops; BILL.md KB-control numbers.
