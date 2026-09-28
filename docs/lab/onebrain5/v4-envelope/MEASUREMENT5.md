# MEASUREMENT5 — V4 help/harm envelope (2026-09-27)

**Question:** When does V4 (the 2a/2b denial deliberations) help, harm, or do nothing?  
**Method:** Frozen 20-item mini-prereg (v8), per-item predictions from mechanism rules before running, 5 modes × 3 byte-identical reruns, margin sweep M∈{8,10,12,14,16}, 7-item red team. Machinery: pinned binary SHA 630586da... (byte-identical to R4).

## Scores (correct/20)

| mode | score |
|---|---|
| single | 20/20 |
| onebrain | 10/20 |
| nov4 | 12/20 |
| nG | 10/20 |
| nov4nG | 16/20 |

## Predictions vs outcomes

- **Winner predictions: 100/100 correct.** Every per-item per-mode winner predicted correctly.
- **V4-effect direction: 20/20 correct.** (V3 transfer bar: 14/20 → PASS.)
- This transfers the §2 mechanism rules to fresh items — vs the R4 red team's 27/56 from blind surface text.

## The envelope

| condition | items | V4 effect | mechanism |
|---|---|---|---|
| **HELP** | E01–E04 (4) | +1 each (onebrain 16, nov4 19) | correction+challenge, inter(challenge)>inter(correction), rel tie → V4 denies challenge fact (dep 1<2); repairs reint's wrong 19 |
| **HARM** | E05–E08, E17–E18 (6) | −1 each (onebrain 19, nov4 15) | forget+challenge, rel tie → V4 denies forget fact (dep 1<2); removes correct 15 |
| **INERT (duel)** | E09–E12 (4) | 0 (both 19, wrong) | duel kills rd6 in round 1 (corr=0 by spacing) → V4 2a suppressed |
| **INERT (margin)** | E13–E16 (4) | 0 (both = single) | margin 18–21 > 12 → fork=0 → V4 cannot fire |
| **INERT (gate)** | E19–E20 (2) | 0 (both 15, right) | margin 13–14 > 12 → fork=0 |

**Net on v8:** onebrain 10/20 vs nov4 12/20 (−2). The net is composition-dependent, not a property of V4.

## The precise rule

V4 helps when its least-disruptive denial removes the fact supporting the **human-wrong** bid.  
V4 harms when it removes the fact supporting the **human-correct** bid.  
V4 is inert when (a) margin > threshold (no fork), (b) the duel already removed the contested bid, (c) the denial hits only non-contending facts, or (d) both arms converge anyway.

V4 does not help/harm by reading type — R1c shows V4 HELPING in a forget+correction item (denied the wrong forget fact).

## Margin sweep (H5e)

- V4-affected item count is monotonic in M: 0→4→10→12→12 (v8).
- Each item's V4 effect turns on at M ≥ its margin, precisely (E01–E04 at M=10; E05–E08/E17–E18 at M=12; E19/E20 at M=14).
- NET delta is NOT monotonic (0→+4→−2→−4): help-items (margin 9) turn on before harm-items (margins 10–14), so the sign flips. Composition sets the net.
- At M=8, V4 effects → 0 on both v8 and v7. The gate is necessary and precise.
- v7: only q01–q05 ever flip (at M=12). No hidden V4 effects elsewhere.

## Red team

- **R1:** V4-help confirmed in forget+correction (R1c). **NEW HARM MODE:** 2a+2b cross-step annihilation → NO_VERDICT (R1a, R1b). The per-step `skipped_annihilate` guard is insufficient when both steps fire.
- **R2:** V4 firing ≠ V4 mattering (2/2). Trace activity does not imply causal effect.
- **R3:** Duel pre-emption unbroken (0/2). Even with 3 readings, the duel decides.

## Void bars
- V1 (determinism): PASS — all reruns byte-identical (5 modes × 3, sweep 2×20, red team 2×2).
- V2 (no RNG): PASS — no rand/time/entropy; syscalls are read/write/open/close only.
- V3 (transfer): PASS — 20/20 ≥ 14/20.
- V4 (sweep sanity): PASS — M=12 binary byte-identical to pinned.

## Plain-English envelope

**V4 helps** when the wrong answer is propped up by a fact that V4's least-disruptive rule targets — typically the challenge fact in a correction+challenge where the challenge was repeated (4/4 here), and the forget fact in a forget+correction where the forget was the mistake (1/1 here).

**V4 harms** when the right answer depends on the fact V4 removes — typically the forget target in forget+challenge (6/6 here). In the extreme (both V4 steps fire), it can delete every answer → no verdict at all (2/3 red-team items).

**V4 does nothing** when the fork never opens (wide margin, 6/6), when the duel already settled the fight (4/4), or when its denial hits facts that weren't going to win anyway (2/2).

**The margin knob** turns V4 up smoothly: at 8 it's off, at 10 the helps appear, at 12 the harms join and can outvote the helps, at 14+ everything's on. The net score at any setting is set by the mix of items, not by V4 itself.
