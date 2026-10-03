# PAMs v2 Whole-Counsel Synthesis — judge's verdict

**Date:** 2026-09-24. **Judge:** native Muse subagent (parent: PAMs v2 whole-counsel task from Micah).
**Counsel:** grok-4.7 (7 hypotheses, delivered), claude-fable-5.1 (5 hypotheses, delivered), gpt-5.6-sol (3 attempts, all `choices:null` — provider backend generating nothing), claude-opus-5.5 (2 socket timeouts + 1 HTTP 524 — endpoint down this session). Raw attempts preserved in this directory.
**Debate:** three native champions argued the corners (deliberate re-sense / historical corridor audit / attack-the-ceiling-at-the-sense), each required to steelman the strongest attack on their own corner.

## Judge's finding: the hole and the ceiling are two different problems

The three corners agree on the anatomy and disagree only on priority:
- Corner A (re-sense) and Corner B (corridor) both target the **deployment blocker** (correlated wrong corroborators). They are complementary, not competing: A adds new evidence per install; B refuses historically. B caught a genuine structural dependency — the corridor mechanisms only work as a STACK, because F1's "running FPR" and G6's "joint-wrong rate" need a post-install truth signal that exists only in F5's reversal bank.
- Corner C proved arithmetically that **no gate-side hypothesis can reach 85%**: 0.85 × 1102 = 937 installs needed; gate-side ceiling is 824. The sense must convert ≥113 of the 278. Every defense-side hypothesis only rearranges installs inside the ceiling.
- The honest merge is therefore: **defense = F5 + G2 (block the hole), offense = G5 (move the ceiling)**. Rank them as one program, not one winner.

## Ranked hypotheses (cross-corner, evidence-judged)

### 1. F5 — Counter-corroboration trap (negative exemplar bank) — BUILD FIRST
Ranked #1 by Corner B, #3 by Corner A. Mechanism: percepts that were installed then reversed by deliberate re-inspection become negative exemplars; any candidate within distance (same family, conf ±150, mrgF ±2000) is BLOCKED regardless of evidence score until three deliberate re-inspections from three temporal crops confirm — then the exemplar is removed (explicit re-judgment). Blocking is the safe direction: a delayed correct percept is recoverable, an installed wrong corrupts the system. Supplies the post-install truth signal F1/G6 need. Graceful failure (over-blocking measured, not asserted).
Kill battery (cheapest of all corners — offline backtest, no new binary): replay the F5 block predicate over the 43 logged ACCEPT_INSTALL trials (9 false, 34 true), seeding the bank with the six timbredisc wrongs. KILL if <8/9 false accepts blocked, or >4/34 true accepts within exemplar distance. Red-team follow-up: 300 near-exemplar correct percepts; kill if >25% delayed >50 trials.

### 2. G2 — Judgment-blind deliberate re-sense — BUILD SECOND (or in parallel with F5)
Corner A's top pick; the program-law answer. Mechanism: on any candidate install, discard conf/mrgF/strong/agree; a fixed attention map (pure function of raw bytes only) selects ≤64 offsets; a separate organ — trained and weighted apart from the first — re-reads those offsets plus a frozen neighborhood and must emit the same label. No install from two full-frame PASSes. Respects ceiling 1 (second percept is not a function of the first judgment) and ceiling 2 (nothing installs by dominating old axes). This is conscious perception as machinery: the brain chooses what to re-inspect and verifies before installing.
Steelman's attack (the one to beat): the error may live in the bytes, and the re-sense re-reads the same bytes — the corner relocates the hole from judgment-side to byte-side correlation, which committed evidence does not rule out. The separate organ's architectural distance from the first is the load-bearing property and must be measured, not asserted.
Kill battery (replay-only, 5 parts, on the 43 V2-D ACCEPT_INSTALL trials): (a) wrong-kill: ≥2 of 6 timbredisc wrongs survive re-sense → kill; (b) span-edit: >2/9 false installs under span-preserving edits outside attended set → kill; (c) correct-retention: <26/34 true installs retained → kill; (d) judgment-blindness probe: any feature constant when attended bytes change but judgment stays → kill; (e) RK-3 no-regression: >3.0pt drop from 88.48% → kill.

### 3. G5 — New sense aimed at the 278 — RUN IN PARALLEL (offense)
Corner C's top pick; the only hypothesis that can move the 74.8% ceiling. Mechanism: do not retune the PASS threshold. Add a heavy second-pass sense that runs ONLY when the current sense is high-confidence but not PASS; it may use a wider window, different byte grouping, or prototype match against verified installs; it emits PASS under the existing numerical bar or abstains. It cannot raise confidence of an already-PASS item into install; corroborated-wrong handling stays with F5/G2.
Steelman's attack (the one to beat): the six corroborated-wrong RICH trials prove the current sense already mints confident wrongs; a heavier sense may learn the same spoof features. This becomes a kill bar, not a dismissal.
Kill battery (one binary, three frozen datasets): freeze RK-3, sense, and gate numbers; run the candidate sense only on the frozen 278. KILL if <100 convert to true PASS (true 85%-bar requirement is ≥113; 100–112 = real effect, insufficient). KILL if false-PASS on the 12 sealed families rises >2 points above today's rate. KILL if RK-3 drops below 88.48%. KILL regardless if the second sense re-emits PASS on ≥2 of the six timbredisc wrongs (it learned the spoof features).

### Honorable (do not build yet)
- **F1 TCAT (amended):** corridor-level FPR audit is the exact signature of the blocker, but as written it has no truth signal — it needs F5's bank. Revisit after F5's backtest.
- **F3 staleness gate:** the only mechanism that denies a sustained error its faked property (permanence). Higher variance — risks destabilizing correct installs. Revisit after F5/G2.
- **G1 disjoint stripes:** purest structural guarantee, but expensive and risks RK-3; G2's attention map is the cheaper version of the same idea.
- **G7 scope-challenge:** not a build — a standing constraint on all builds. The zero-bit proof covers judgment+deterministic-transform predicates, not a second raw read; the trial-1145 dominance proof covers logged axes, not future raw measurements. Any builder that smuggles the second look through the first judgment re-runs the miniature Zag proof and dies on the first 0.0000-bit predicate.
- **F4 novelty-first, F2 ADRS, G3 residual organ, G4 quarantine, G6 bins:** ranked below by the champions on evidence grounds (F4: 53% novelty makes it a wrong-install pipeline; F2: V2-B is a direct precedent against attacker-known transforms; G3: novelty-memorization risk; G4: dies cleanly to a resourced M-context attacker; G6: bin granularity is attacker-dodgeable, folded into F5's stack).

## Build order recommendation
1. **F5 first** — offline backtest this week, no new binary. If it blocks ≥8/9 false accepts at ≤4/34 true cost, freeze it as the refusal layer.
2. **G2 in parallel** — replay-only 5-part battery. If it passes, it becomes the install-time verification organ (the conscious-perception law, mechanized).
3. **G5 in parallel** — the offense leg. The 85% bar cannot fall without it.
All three are pure Zag, zero RNG, byte-identical reruns, frozen preregs before builds — standard laws apply.

## Model-availability log (for the record)
- grok-4.7: 1 call, success, 9,096 bytes.
- claude-fable-5.1: 2 calls (first returned identity-only preface), success on retry with no-preamble instruction, 10,751 bytes.
- gpt-5.6-sol: 3 calls, all `choices:null` with 0 completion tokens (provider backend generating nothing — the documented flaky mode). Unreachable this round.
- claude-opus-5.5: 3 calls — 2 socket timeouts at 120s, 1 HTTP 524. Endpoint down this session. Unreachable this round.
