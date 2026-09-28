# BAR_RESULTS.md — Kill bar verdicts (implementer-reported; K4/K5 pending auditor)

## Calibration gates
| Gate | Condition | Result | Verdict |
|------|-----------|--------|---------|
| C1 | P median ≥480 | P=600 | **MET** |
| C2 | Z median <150 | Z=143.5 | **MET** |
| C3 | ≥3 distinct strategies ≥360 | Only ward-turtle (P) demonstrated at 600. No 2nd/3rd distinct strategy reaching 360 was found via scripted search. | **NOT MET** — world is effectively one-trick (ward-turtle). See note. |

**C3 note:** The energy math (6×30 + 2×40 = 260 max from motes; 100+260=360 total
vs 600 basal) makes 360 unreachable without a WARD (0 basal). The prereg's
example strategies (pure foraging, lamp-farming, surge-gambling) cannot reach 360
in this parameterization. The implementer did not retune the prereg's fixed
numbers (+30, +40, SURGE +40/-2×10) to force C3, as those are requirements, not
examples. The world therefore tests "can I invent the ONE working strategy"
rather than "which of several strategies does I invent". This limitation is
reported honestly.

## Kill bars
| Bar | Condition | Result | Verdict |
|-----|-----------|--------|---------|
| K1 — no invention effect | median(I-survive) ≤ median(R) | 220 > 160 | **NOT FIRED** |
| K2 — trivial/broken | median(I-survive) ≤ median(Z) | 220 > 143.5 | **NOT FIRED** |
| K3 — unsolvable | median(P) < 480 | P=600 | **NOT FIRED** (not VOID) |
| K4 — not novel | auditor finds key steps in training mass, or trivial recombination | Independent blind auditor: A1 reports NO coherent novel strategy in I's traces — nothing to audit. kb.txt verified clean (zero item/recipe/plan hits; the single grep hit is "toward"). | **NOT FIRED (vacuous)** — but H1's positive burden is unmet per A1 |
| K5 — cuing | blind auditor derives I's strategy from materials | Blind auditor derived only a *template* (forage → combine → test → shelter before storms); the winning instantiation (which recipe, effects, build order) is not derivable without experimentation. kb.txt clean; coordinator verified agent_i.zag/agent_r.zag contain zero §3 strategy terms (only agent_p.zag, the positive control, by design). | **NOT FIRED** on agent-facing materials |
| K6 — novelty not causal | ablation shows removing novelty does not reduce survival | A2: removing novelty drops median 250→232 (18 ticks, 7%); 3/9 variants improve. | **SUPPORTED** — the "novelty" was not doing the work |

## Summary
- The run is VALID (not VOID): C1 and C2 met, K3 not fired.
- K1 and K2 do not fire: I beats R and Z on median survival.
- K4 does not fire (vacuous — no invented strategy exists to audit); K5 does
  not fire (no cuing of agents; verified no §3 content in agent_i/agent_r
  sources or kb.txt).
- **K6 SUPPORTED: the invention claim is KILLED.** A1 finds no invented
  strategy; A2 finds the novelty is not causal. H1's mechanism
  (compositional deliberation → novel strategies → survival gain) is not
  demonstrated. I's 220-vs-160 edge over R comes from safety-constrained
  exploration and avoiding R's harmful reflexive COMBINE — not invention.
- H2: no survive-vs-invent framing difference (both 220).
- Methodological caveats: (1) C3 not met — one-trick world (ward-turtle),
  so this run tests "invent the ONE working strategy," not strategy choice
  among several. (2) The prereg §3 named example recipes matching the
  implemented table — agents never saw §3 (verified), but future runs should
  keep prereg examples disjoint from implemented parameters. (3) The taught
  storm rule's word "shelter" orients search toward shelter-seeking (yellow
  flag, not a violation).
- Task-1 comparison: the "composition is the broken link" finding replicates
  — implicit survival pressure did not fix it (see A3_task1_comparison.md).
