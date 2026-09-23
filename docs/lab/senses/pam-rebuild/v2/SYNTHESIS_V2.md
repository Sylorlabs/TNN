# PAMs v2 Deep Dive — Final Synthesis

**Date:** 2026-09-23 | **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Program order:** Micah — "we need pams v2 to accept truths"; Sol + Muse subagents dig deep into the white-box architecture; find why PAMs are failing; knowledge vs machinery; TNN deep-diver by default for behavior.
**Scope:** 10 teams, all completed, all commits independently verified via GitHub API.

---

## 1. Executive verdict

**PAMs fail mostly from missing knowledge, not machinery ceilings — but three genuine ceilings and one spec tension bound what knowledge alone can fix.**

- R2-4's 9.4%-vs-85% liveness collapse is **KNOWLEDGE**: the gate had the inputs (parsed confidence, unused; disjoint-span evidence, unparsed) and lacked the rule. A corroborated-revision rule replays to 621/621 conflict-withheld truths recovered at exactly 0 false installs.
- 9 of the 12 death-board kills are **KNOWLEDGE**: the signal existed and was unused (perfect separator 400/400 on R2-2 PTC-2; texture correlation rescuing 86% of R2-10 CCN-1). The old synthesis "front end fooled with NO DETECTABLE SIGNAL" is refuted.
- The genuine ceilings: (a) **C2/C3 judgment-side channels are a MACHINERY ceiling** — when the perturbed judgment is a deterministic function of the original, no predicate over the pair carries information (0.0000 bits even with perfect knowledge of transforms and law, proven in miniature in pure Zag); (b) **pointwise adjudication is machinery-impossible** — trial 1145 was WRONG yet dominated its incumbent on every axis (conf 874, margin 10,410, strong=1, agree=1): no per-trial evidence comparison can ever be safe; (c) **R2-3 is withhold-only by design** — symmetric disagreement only ever produces withholding; it is an admission harness, not an install mechanism.
- The **RK-3 85% bar is a SPEC-TENSION**: gate-side ceiling is arithmetically 74.8% (824/1,102). No gate change can reach 85% — the rest must come from sense/program (278 never-PASS cases) and the prereg's denominator definition.

---

## 2. Knowledge-vs-machinery verdicts per failure mode

| Failure mode | Verdict | Evidence |
|---|---|---|
| R2-4 CONFLICT_WITHHELD (621 missing installs) | **KNOWLEDGE** — gate lacked the rule; inputs existed | Corroborated-revision replay: 621/621 recovered, false installs 0; gate replay 0/11,840 mismatches (AUTOPSY_R2-4.md) |
| R2-4 per-trial adjudication | **MACHINERY ceiling** (cf2) — no single-trial rule can be safe | Trial 1145: wrong percept strictly dominates incumbent on every axis; naive single-shot revision installed it |
| R2-4 suppressed by negative evidence (99; 81 poisoned by own false-negative FAILs) | **KNOWLEDGE** — program emits false negatives against correct percepts | Decomposition; corroborated-negative-evidence rule proposed |
| R2-4 never-reached-PASS (278) | **KNOWLEDGE** — sense/program gap | Gate never saw the judgments |
| R2-4 knowledge-delivery gap (25% of correct-highconf never reached gate input) | **KNOWLEDGE** — delivery path missing | Diagnostics harness K1 96.4% knowledge present vs 74.8% reaching gate input |
| RK-3 85% bar unreachable | **SPEC-TENSION** — bar vs arithmetic | Gate ceiling 824/1,102 = 74.8%; "a spec tension, not a code problem" |
| Death-board 9 of 12 kills | **KNOWLEDGE** — signal existed, unused | gl_b>0 perfect 400/400; texcorr_gate 82/95; pure-Zag verifiers, byte-identical (AUTOPSY_DEATHBOARD.md) |
| R2-10 CCN-2 "32 false installs" | **BENCHMARK BUG** — 338/340 fixtures mislabeled | Front end was correct; labels were wrong |
| R2-10 MOT-1 | **UNRECOVERABLE** — benchmark premise flawed | Generator reverses frames, labels pre-reversal direction; truth unobservable from pixels |
| R2-10 flat-patch COL-2 | **MACHINERY** (narrow) | Death-board autopsy |
| C2 deterministic transforms / C3 noisy re-observation | **MACHINERY ceiling** (frozen-threat-model scoped) | 0.0000 / 0.0049 bits even with law + new transforms handed over; mini proof in Zag (AUTOPSY_KB4_CHANNELS.md) |
| R2-3 (survivor) | **MACHINERY-BY-DESIGN** — withhold-only | 1,200/1,200 withholds; cannot admit truths by construction |
| R2-8 interventional leg | Load-bearing (Leg-II ablation +13.70pp false installs) but dead on purity | Gate+ledger were Python — "best numbers" inadmissible as native evidence; prereg/implementation mapping discrepancy open |
| V2-D independent-evidence acceptance | **KILLED** — violates withhold-everything | Red-team: 43 ACCEPT_INSTALL on 288 UNRESOLVED, 9 false; 20.9% false vs 0.6% claimed calibration (REDTEAM_V2.md) |
| V2-A adjudicator | **WEAKENED** — passes withhold (0/288) but decoy revises permanents wrong | 13 REVISE_INSTALL, 15 false installs on decoy stream |
| V2-B interventional port | **UNTESTABLE as gate** (no gate landed); sense = R2-4 byte-identical | Ablation passes but fork dead on RK-3 regardless |
| V2-C knowledge-first | **UNTESTABLE as gate** (unbuildable as landed); detectors 0 fires (stubs) | — |

**Sol's qualification (accepted):** "Nine cases had replay-recoverable or externally demonstrated signal, but frozen-gate installation was not established." Prescription: three labels per case — **recoverable signal / admissible under frozen gate / safe to install**.

---

## 3. PAMs v2 architecture (post-Sol-Round-4 ranking)

1. **Revisable admission/install gate** (resurrected #1, redefined): "revisable" means **historical corroboration only** — pointwise revision is BANNED (trial-1145 rule). The gate is redesigned as an admission/coverage system attacking the **delivery gap** (the largest quantified deficit: 96.4% knowledge present, 74.8% reaching gate input).
2. **Native interventional adjudication** (#2, unchanged): R2-8's load-bearing mechanism in pure Zag, with preregistered channel semantics and explicit contradiction handling. The R2-8 prereg/implementation mapping discrepancy (perturb independent source vs perturbed X) must be frozen one way and re-run.
3. **C1-class independent corroboration** (per family): INSTALL iff a frozen pure-Zag analytic probe — diverse from and uncontrolled by the proposer — agrees with the proposed judgment. Judgment-side channels are banned unless registered (frozen threat model); registered channels carry their own false-installation budget.
4. **Claim-local evidence escrow** (demoted to #3): "evidence that is never admitted, surfaced, or adjudicated remains operationally unavailable" — escrow preserves but does not deliver.
5. Hard mechanisms from survivor extraction (M1–M9): disjoint evidence declarations, overlap audit, interventional withholding, cross-source agreement, intervention-responsiveness, trinary dispositions, executable warrants, claim-discriminative challenges, provenance/ledger, paired recall bar.

**Explicitly ruled out:** judgment-side acceptance channels (MACHINERY ceiling); pointwise revision rules; withhold-everything as a safety strategy (safety by never installing is not the target — accepting truths is).

---

## 4. Sol/Muse disagreements (all five preserved as live, reframed)

1. Knowledge/machinery framing → **both sides now partly right** (Sol conceded universal machinery claim overgeneralized).
2. Revisable-claim safety → reopened in new form by the new #1 (temporal/contradiction rules doing revision-authority's work). Settling experiment: preregistered sequential protocol.
3. Intervention = enumeration + actuation → **STANDS**, reframed "one useful scout ≠ an enumerated channel space." Settling experiment: finite intervention registry.
4. FS-G bars don't provably specify contradiction behavior → **STANDS**; trial 1145 "a concrete demonstration of the gap." Settling experiment: **contradiction matrix — run first (cheapest)**.
5. Death-board weight (12 kills vs one invalid dependency pattern) → reframed by the 9/1/1/1 split.

Sol's tooling constraint recorded: Sol via UnoRouter returns empty completions above ~5KB — briefs must stay inside ~1,200 tokens.

---

## 5. Red-team results (Team 8 + 8b)

- **12 novel adversarial families** sealed and validated (PTC-4/5, TMB-4/5, COL-4/5, CCN-3/4, SHP-4/5, MOT-4/5; 288 fixtures + 288 truth sidecars, manifest digest `c140013e…f56b9d`, byte-identical regeneration). Generator bugs caught and fixed (LCG low-bit collapse; MOT-4 ambiguous truth).
- **V2-D KILLED**: withhold-everything violation confirmed with byte-identical evidence. The correlated cross-span failure attack surface (fool F and G identically at high confidence) is the mechanism.
- **V2-A WEAKENED**: withhold holds, revision path doesn't.
- **Sense itself is weak on novelty**: 53% on the 12 families; reaches its own install bar on only 44/288 trials (zero in 8 of 12 families).
- **Autopsy audits**: R2-4 RK-3 104/1,102 recomputed exactly (STRONG); **R2-10's "58/76 constitutional-veto firings" is NOT recomputable — prose-only, no evidence file** (source existence ≠ evidence the firings occurred); KB4 mech demo byte-identical (adequate).
- Bar-gaming temptations: install-nothing and withhold-everything batteries run; ledgers observed.

---

## 6. What changed in TNN's default diagnostic behavior

Deep-diver-by-default is now machinery, not just a directive:

- **`v2/diagnostics/DEEP_DIVE_METHOD.md`**: mandatory 5-step protocol for ANY behavioral failure — (a) reproduce + freeze, (b) instrument white-box internals, (c) knowledge-vs-machinery probe split, (d) verdict with evidence, (e) no surface patches without (a)–(d). Frozen verdict taxonomy: MACHINERY-BUG / KNOWLEDGE / MACHINERY-BY-DESIGN / SPEC-TENSION / INCONCLUSIVE. Red-team rule: every conclusion gets adversarial review, recorded.
- **`v2/diagnostics/diagnose.zag`**: pure-Zag harness automating the probe split — reproduces+freezes the metric, replays the gate rule over the frozen record, runs K1–K4 knowledge probes and M1/M2 synthetic machinery probes, computes the gate-side ceiling, emits a structured verdict with its own SHA256-chained 16-word audit ledger. Zero RNG; byte-identical reruns.
- **Machine-readable `surface_patch=BLOCKED`**: patch classes enumerated; verdict-first reasoning and hand-analysis-as-evidence explicitly overridden.
- **Self-application to R2-4/RK-3**: verdict KNOWLEDGE + SPEC-TENSION, all 6 kill bars PASS — and the instrument caught what hand analysis missed (deliberation-downgraded trials the gate never saw).
- Genuine machinery ceilings stay explicit: the harness emits MACHINERY-BUG and MACHINERY-BY-DESIGN verdicts, and Team 4's fixed-point result stands as the model of an honest ceiling.

---

## 7. Prereg-level decisions flagged for Micah

1. **RK-3 85% needs SPEC-CHANGE, not sub-bars** — "Sub-bars may diagnose where the loss occurs, but they cannot make an unreachable aggregate target valid." Prereg must fix the denominator/admission population/treatment of never-reached cases. (Sol's prescription.)
2. **Ban pointwise revision rules** in every v2 gate that changes a live claim (trial-1145 rule).
3. **Ban unregistered judgment-side acceptance channels** for the frozen threat model; registered C1-class channels allowed with their own false-installation budget.
4. **Correlated cross-span failure**: hardening V2-A/V2-D's frozen decision rule (`jG==jF, conf≥700`) = prereg amendment — needs Micah's word. V2-D's ALIVE verdict is qualified as "within the frozen threat model" until resolved.
5. **R2-8 mapping discrepancy**: freeze one perturbation mapping (prereg's vs implementation's) and re-run before any interventional leg is frozen.
6. **Settling experiments, cheapest first**: contradiction matrix (formal) → preregistered sequential protocol → finite intervention registry → end-to-end frozen-gate test on preregistered inputs (keep the factorial with the K1→K2 delivery path as an explicit factor).
7. **Knowledge-injection experiment** (Sol's cheapest unrun decider on CONFLICT_WITHHELD): explicit revision rule via the knowledge channel, no code change.
8. V2-B (`vgate_b.zag`) and V2-C (`vsense_c.zag`) are explicitly deferred with reasons — revive or retire by prereg call.

---

## 8. Commit index (all independently verified via GitHub API)

| Commit | Content |
|---|---|
| `b43a1d60` | Team 3 survivor mechanisms (SURVIVOR_MECHANISMS.md) |
| `adac4f7d` | Team 1 R2-4 autopsy (AUTOPSY_R2-4.md) |
| `9c839099` | Team 4 KB4 channels autopsy (AUTOPSY_KB4_CHANNELS.md + mech demo) |
| `325337d6` | Team 5 Sol debates rounds 1–3 (DEBATES_V2.md + briefs) |
| `b1f2858c` | Team 7 diagnostic prereg (PREREG_DIAG.md) |
| `edb27457` | Team 7 diagnose.zag + method + self-application |
| `70f0c555` | Team 2 death-board autopsy (AUTOPSY_DEATHBOARD.md + verifiers) |
| `4c47fad5` | Team 5b Sol Round 4 (DEBATES_V2_R2.md + briefs) |
| `f9bc9992` / `e915358b` | Team 6 V2-A/V2-D build fixes + exposure docs |
| `cc4689f6` / `f74f4d8f` (+`471e8e76`, `9b10843f`) | Team 6 V2-B/V2-C source landing + manifests |
| `0e38440f` | Team 8b sealed red-team fixtures + generator |
| `ed8b43a7` | Team 8b attack harnesses + REDTEAM_V2.md |

All under `docs/lab/senses/pam-rebuild/v2/` on `tnn-native-lab`. Pure Zag for mechanisms; Python glue/analysis only; zero RNG everywhere; byte-identical reruns with digests.
