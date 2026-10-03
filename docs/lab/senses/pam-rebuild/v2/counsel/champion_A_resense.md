# Champion A — the DELIBERATE RE-SENSE corner (G2 / G1 / F2 / F5)

## The thesis

The correlated-corroborator hole has a precise anatomy. The deployment blocker is not low confidence: the six timbredisc wrongs arrived at conf 701–718, mrgF 353–382, all PASSing RICH against truth BRIGHT (seq 10983–11192), absorbed as CORROBORATED instead of triggering revision. The V2-D red team added the second half: on 288 UNRESOLVED trials, independent-evidence acceptance fired ACCEPT_INSTALL 43 times, 9 false — a 20.9% false rate against a 0.6% calibration claim. Two organs agreed, and agreement added zero new evidence, because both looks consumed the same bytes through the same judgment-side machinery.

Every dead position died deciding something from the judgment pair. Ceiling 1 (judgment-side channels carry 0.0000 bits, mini Zag proof) and ceiling 2 (trial 1145: WRONG, conf 874, mrgF 10410, strong=1, agree=1 — no pointwise domination of logged axes can install) together forbid every judgment-side fix. The only surviving move is this corner's: **a fresh read of raw bytes, on a schedule that is not a function of the candidate judgment, performed by a separate organ, whose verdict gates install.** This is the program-law answer verbatim — the brain *choosing what to re-inspect*, refusing to install an untested percept.

## Why the corner respects each proven ceiling

**Ceiling 1.** G2 treats the logged judgment as radioactive: conf, mrgF, strong, agree are *discarded* before the second look. The attention map is a pure function of raw bytes; the second organ never sees the first organ's output. G1 partitions at the byte level — the predicate is over two disjoint raw views, never over a judgment plus a transform of it. F2's four transforms are functions of raw bytes, not of the first judgment, though the mini-Zag-proof probe must be re-run on each transform (the honest application of grok's H7 scope constraint to fable's transforms). F5 never derives install evidence from judgment distance: exemplar distance *blocks*; installation requires three deliberate 3-crop re-inspections.

**Ceiling 2.** Nothing here installs by outscoring an incumbent. G2 refuses the fight: trial 1145 cannot become installable on dominance because nothing compares the trial's axes — the demand is a second organ's independent same-label emission on different bytes. F5's partial challenge is legitimate and exactly stated: single-trial comparison suffices to *block* — a delayed correct percept is recoverable, an installed wrong is not — never to install.

**Ceiling 3 (824/1102 = 74.8%).** This corner is a false-install killer, not a recall booster; no hypothesis claims to rescue the 278 by gate arithmetic. RK-3 88.48% is the floor to defend, hence the "falls >3.0 points" bar in every kill battery.

**Ceiling 4 (zero RNG, byte-identical reruns, pure Zag).** All four are frozen, deterministic, historical: fixed map/partition/transforms, append-only bank. Nothing breaks replay.

## Program-law embodiment

Corroboration-as-autopilot — two full-frame PASSes from the same byte diet — is the stingy-LLM behavior the law forbids. G2 is the law rendered as mechanism: the second look is *deliberate* (attention map, bounded ≤64-offset budget, a separate organ trained and weighted apart), and "no install from two full-frame PASSes" kills the autopilot by statute. G1's fixed partition makes shared-bias corroboration impossible *by construction*: no organ may see the other's evidence. F5's negative-exemplar bank is the brain's memory doing its job — past reversed installs become active gates. F2 is weakest here: four fixed transforms are a rote ritual, not deliberate attention, and "rotate the modality" risks becoming exactly the interventional sensitivity V2-B proved attacker-controllable.

## Steelman: the best attack on this corner

The honest objection is that **the error lives in the bytes, and the re-sense re-reads the same bytes.** The six timbredisc wrongs were a *sustained front-end error* — one wrong reading repeated. V2-B's lesson cuts deeper than its verdict: it proved an attacker can control sensitivity, i.e., set the reading of a byte region across sense pipelines that consume it. If the spoof is written into the raw bytes, a second organ with the same front-end architecture is not a second witness — it is the same witness asked twice, and determinism guarantees the byte-identical misreading every time. G2's "separate organ, trained and weighted apart" is only as good as the architectural distance between the organs. G1 dies outright if the spoof is written into both stripes, and the frozen partition is knowable to the attacker. F2 dies on transform-invariant families, which fable itself concedes are constructible. F5 never catches the *first* instance of a novel correlated cluster: the bank is empty until the error is discovered and reversed, so a fresh spoof family installs unopposed — and with 53% novelty accuracy on 12 sealed families, the first instance is the one most likely to be wrong. The deepest form of the attack: **this corner relocates the hole from judgment-side correlation to byte-side correlation, and the committed evidence does not yet rule out byte-side correlation.** If the front-end's byte-reading is the shared organ, no organ-level diversity helps; that is a senses-rebuild question, not a PAMs question.

## Ranking (by expected value)

1. **G2 judgment-blind deliberate re-sense.** Highest EV: closes the hole with the exact property corroboration lacked (zero judgment-side evidence), cleanest program-law instantiation, cheapest battery (43 replay trials, no new data). Its residual risk — byte-side correlation — is directly testable (probe 4 below).
2. **G1 fixed disjoint stripes.** Purest structural guarantee, but the most expensive to build and the most likely to dent RK-3 88.48% (each organ loses half the bytes), with the both-stripes-spoof attack live.
3. **F5 counter-corroboration trap.** Cheapest to implement, graceful degradation (over-blocking delays, never corrupts), and the only hypothesis that *weaponizes* discovered errors. Ranked third because it is reactive: it cannot stop a novel correlated cluster's first install.
4. **F2 ADRS.** V2-B is a direct precedent against it: fixed, attacker-known transforms are interventional sensitivity by another name, and fable's own kill battery concedes the adversary can build transform-invariant families.

## Cheapest decisive first experiment (G2)

Reuse committed evidence only — the 43 ACCEPT_INSTALL trials from the V2-D red team (9 false including the 6 timbredisc wrongs at seq 10983–11192; 34 correct). Freeze the attention map (pure function of raw bytes, ≤64 offsets). Run:

1. **Wrong-kill test.** G2 re-sense on the 6 timbredisc wrong PASSes. **Kill bar: ≥2 of 6 still install as joint PASS → falsified.**
2. **Span-edit test.** On the 9 false ACCEPT_INSTALLs, replace unattended bytes with noise preserving the attended span, and the reverse. **Kill bar: false-install rate on those 9 under span-preserving outside edits stays above 2/9 → falsified.**
3. **Correct-retention test.** On the 34 correct ACCEPT_INSTALLs. **Kill bar: more than 8 lost (retention <26/34) → falsified.**
4. **Judgment-blindness probe.** For each of the 43, perturb raw bytes inside the attended span while holding the first organ's judgment constant; verify the re-sense outcome *moves with the bytes*. **Kill bar: a single trial where the re-sense output is invariant across byte changes with judgment fixed → falsified** — that proves a judgment-side channel smuggled into the map.
5. **No-regression gate.** Full RK-3 after G2 wiring. **Kill bar: RK-3 drops more than 3.0 points below 88.48% → falsified.**

Total cost: one separately-trained organ plus a replay-only battery over 43 trials. If all five bars pass, the corner's thesis stands: the hole closes when the second look is judgment-blind — and the remaining question, byte-side correlation, is a senses-rebuild problem the PAMs layer can now name honestly.
