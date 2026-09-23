# RED TEAM VERDICT — "Too good to be true" (Micah, 2026-09-21)

Four legs: three native skeptic crews (methodology / toolchain-artifact /
battery-design) + Sol's hostile peer review (UnoRouter) + the TNN's own
self-critique leg (`critic.zag`). Grok timed out 3× and is excluded from the
critical path — external scrutiny below means Sol alone, a limitation stated
openly.

**Bottom line up front:** not fabrication — **overclaimed inferential reach**.
The perfect scores are real outputs of real deterministic code, but they are
the expected outcome of deterministic code + wide bars + generator-coupled
batteries, and several load-bearing claims do not survive contact with their
own instruments. Three findings are *proven* (not hypothetical), two attacks
were *measured empirically*, and the single most urgent item is a live
miscompile inside the no-RNG law-gate certifier itself.

## Ranked attacks

| Rank | Attack | Severity | Status | Source legs |
|---|---|---|---|---|
| 1 | The no-RNG certifier reads through a proven-live miscompile | Serious (gate-threatening) | **PROVEN by reproduction** | toolchain |
| 2 | Test-generation coupling: mechanisms dispatch on battery kind labels; disjoint vocabulary costs 25 points | Serious | **PROVEN in code + MEASURED** | methodology, battery-design, Sol #1 |
| 3 | RSI "+10000→+10000 EXACTLY" entailed by construction | Serious | **PROVEN from source** | toolchain, methodology, Sol #5 |
| 4 | No truth instrument exists anywhere in the program | Serious | Untested gap (partly self-documented) | methodology, battery-design, Sol #2, self-critique |
| 5 | Kill bars are tripwires; perfect scores are the expected outcome | Serious (methodological) | **MEASURED** (157× slack sampled) | methodology |
| 6 | Frozen world: "live web" result is frozen-envelope replay | Serious | Untested assertion | battery-design, self-critique |
| 7 | Silent thresholds + dirty recycled heaps | Serious (robustness) | **PROVEN by probe** | toolchain |
| 8 | Cost accounting "4.000 ops / 92 B per fact" is by construction | Minor–serious (headline) | **CONFIRMED from source** | methodology, Sol #3 |

### #1 — The law-gate certifier miscompiles (PROVEN, test next first)

ZNC-2026-09-21-007 (consecutive `as []i32` casts alias: 2nd+ table reads return
the *previous* table's data) was reproduced on the pinned toolchain with a
faithful replica of the no-RNG gate's own code. The pattern is live in
`thincert.zag` (9 casts) and `rngscan_v3.zag` (30 casts). Byte-identical reruns
are blind to it *by construction* — identically wrong 5/5. Blast radius on
historical verdicts: untested. **Next test:** rebuild the certifier with the
documented `[]u8`+accessor workaround and diff every historical certification.
Could-be vs is: the miscompile IS live in the gate's code; whether any verdict
was corrupted IS NOT yet known.

### #2 — The perfect scores are scored on the generator's own inventory (PROVEN in code + MEASURED)

- Code: the 156/156 "contradiction mechanism" opens with `let k:i32=bat_kind(f)`
  and routes on the battery's kind labels — generator and learner share one
  binary. It measures kind-dispatched handlers satisfying their kinds, not a
  general contradiction resolver.
- Measured: 48 facts × 3 probe tiers, battery predating scoring (Sol's
  "unknown until frozen" satisfied). Novel syntax: Δ=0.000. **Disjoint concept
  vocabulary: sol 0.9375→0.6875, grok 0.7917→0.5625; misc-count family
  collapses to 0.167/0.250.** "Generalization across wordings" reduces to
  "generalization across the generator's template inventory."
- Sol's "existential" downgraded to serious-and-bounded: the prereg froze the
  taxonomy before mechanism code, and leaf rules are generic. **Next test:**
  a battery from a fully independent party, disjoint schema, undisclosed
  corruption rate — never done anywhere in the program.

### #3 — RSI exact reproduction is entailed, not calibrated (PROVEN from source)

T-PRIN's prediction is a hardcoded constant (`m_s32(reff,…,10000)`);
T-DENSE/T-DOMAIN3 predict `10000−baseline` (tautological full-gap closure);
the variants flip the battery's own flag (`if(prin==1){installed_truth=1;}`);
the oracle's KB2 bar (≥50%) is looser than the "EXACTLY" headline; the
constitution screen is a compile-time constant. The loop genuinely runs; the
calibration claim is "a unit test in a lab coat." **Next test:** held-out
weakness prediction + genuine quantitative risk + independent implementation +
published failures (zero failed interventions on record = total selection
effect). Could-be vs is: the entailment IS proven; the loop's *usefulness* as
an engineering loop is not thereby disproven.

### #4 — No "does it believe true things" instrument exists (untested gap)

The program's own q1n verdict: "A 'does it believe true things' instrument
does not exist in this battery." No independent-party battery, no provenance
scoring in most batteries, no deletion/revision battery, trust values
stipulated by batteries. Abstention is first-class in 3 batteries (better than
Sol implies); trust calibration is untested everywhere (worse). Sol #2's
devastating part (50% corruption → 100% mirroring) is our own documented
finding — weaker per the ranking rule. The untested part is the sharp edge.
**Next test:** truth-grounded evaluation with corruption rates unknown to the
learner, provenance-sensitive scoring, abstention options.

### #5 — Kill bars are tripwires (MEASURED)

157× slack sampled (self-test overhead bar 2.0 vs measured 0.0127); the
devastating q1n result (19/19 absorbed) had *no bar at all*. Perfect scores
are the expected outcome of deterministic code + wide bars, not a miracle.
**Next test:** bar-sensitivity audit — tighten bars until something trips and
report the margin. This deflates all headlines at once, methodologically.

### #6 — Frozen world (untested assertion)

17 SearXNG envelopes replayed; "live re-fetch wouldn't change the mechanism
verdict" is untested; the 12 falsehoods are hand-picked web-consensus facts;
spoofs are constructed fictions, not real adversarial web. **Next test:**
live re-fetch delta + genuinely adversarial queries.

### #7 — Silent thresholds + dirty heaps (PROVEN by probe)

`ln_teach` silently drops facts 129+ (128-cap, no error); `au_append` writes
unbounded into a 64-record buffer; free→realloc→read returns `0xAB` fill, so
allocator-level adversarial testing is vacuous. History-dependent but
per-history deterministic — invisible to rerun hashing. Comparative bars
(variant−baseline) are blind to *shared* degeneracy: the dangerous class is
degenerate legs that pass.

### #8 — Cost accounting is by construction (CONFIRMED from source)

"Exactly 4.000 ops/fact" = one find+add+verify+audit per taught fact, eval
probes uncounted; "92 B/fact" hardcodes slot=24/index=4 as literals, only
audit bytes measured. What survives: 4.2µs wall-clock and constancy — the
real finding. Headline needs revision, not a fatal blow.

## What the TNN said about itself (self-critique leg, `critic.zag`)

8 suspicion probes computed from its own record, ranked, oracle-verified,
5/5 byte-identical (commit `849ab67c`). Its top two — (9) form-content gap,
(8) RSI circularity — are the same two load-bearing doubts Sol raised
independently. Honest boundary, same as RSI: suspicion templates authored;
triggering/ranking computed.

## Retractions and clearances (intellectual honesty)

- **B-vs-C "irreconcilable": RETRACTED.** Battery-design reproduced the figures
  under frozen ABS-3 and found Worker C's parser bug. The system working.
- **Sol #4 (frozen pipeline/cache): CLEARED for RSI** — clean-room rebuild
  byte-identical; determinism practice is sound. (Residual: rebuilds aren't
  routine; fail-open/fail-closed audit untested lab-wide.)
- **Metric shopping / caveats-as-pressure-valve / selection bias: NOT
  SUSTAINED.** Downward revisions happen: v2 killed as pinned path, quality
  hypothesis abandoned twice, SWE banned, hy3/GLM dropped, KB-M-COST
  trip→repair→repass. The program publishes its devastations.
- **Sol #2's devastating half and the form-content gap are our own
  documented findings** — they rank weaker as *attacks* precisely because we
  found them first.

## Recommended test queue (ordered)

1. Rebuild the no-RNG certifier with the `[]u8`+accessor workaround; diff all
   historical certifications. (attack #1)
2. Independent-party battery, disjoint schema, undisclosed corruption rate —
   run against the contradiction mechanism and the v1 prose path. (#2, #4)
3. RSI-2 with held-out weakness prediction, quantitative risk, independent
   implementation; publish failures. (#3)
4. Live re-fetch delta on the info-source envelopes + adversarial queries. (#6)
5. Bar-sensitivity audit across headline trials; report margins. (#5)
6. Lab-wide init-hygiene + silent-threshold audit (bounds-check every
   capped structure; fail loud, never silent). (#7)
7. Truth-grounded evaluation battery: provenance scoring, abstention,
   deletion/revision. (#4)

## Leg verdicts

- Methodology: `docs/lab/redteam/methodology/` — commit `cdff084c8f27`
- Toolchain/artifact: `docs/lab/redteam/toolchain/` — commit `d553a857f143`
- Battery-design: `docs/lab/redteam/battery-design/` — commit `196d677882c3`
- TNN self-critique: `docs/lab/redteam/self-critique/` — commit `849ab67ca9`
- Sol's hostile review: integrated into all three worker verdicts (attacks
  merged, never double-counted). Grok: 3× timeout, excluded; supplement if
  it recovers.
