# CLASS-3 STANDARDIZED — Verdict

**Date:** 2026-09-21
**Crew:** CLASS-3 STANDARDIZATION CREW
**Prereg:** `PREREG.md` (this directory)
**Status:** COMPLETE — all kill bars adjudicated

## Headline

**The artifact verdict STANDS. Micah's quality hypothesis is REFUTED.**

With teacher completeness equalized (complete 240-fact teachers, identical battery, identical procedure), all four sources produce **byte-identical class-3 learners**. Source quality contributes exactly zero to the class-3 outcome through the numeric channel. The original grok/sol-vs-step/swe pattern was 100% teacher completeness (9 held-out skips), 0% model quality.

## Results

Standardized class-3 (complete teacher → `s37_teach3c` → identical battery), N=5 per source:

| Source | Composite | m1/192 | ws/32 | b7/96 | skipped | m2/192 | ops | eps | cost | Learner digest |
|---|---|---|---|---|---|---|---|---|---|---|
| grok-4.6 | **0.9952** | 192 | 32 | 96 | 0 | 192 | 192 | 384 | 0.9524 | `76e85c3e…772b5` |
| gpt-5.6-sol | **0.9952** | 192 | 32 | 96 | 0 | 192 | 192 | 384 | 0.9524 | `76e85c3e…772b5` |
| step-3.7-flash | **0.9952** | 192 | 32 | 96 | 0 | 192 | 192 | 384 | 0.9524 | `76e85c3e…772b5` |
| swe-1-6-slow | **0.9952** | 192 | 32 | 96 | 0 | 192 | 192 | 384 | 0.9524 | `76e85c3e…772b5` |

- **N=5 byte-identity:** all 5 reps per source share the identical learner digest (criterion met).
- **Cross-source:** all 20 runs across all 4 sources share the **identical** digest `76e85c3e521337e36bf4aa2e062c22abf8a67859d3ff014f897c5f0169e772b5`. The four binaries differ only in their corpus import; the corpora's obs/probe legs are byte-identical, so the teachers, the teaching, and the learners are byte-identical.
- Full logs: `evidence/{grok,sol,step,swe}_rep{0..4}.log`.

## Kill-bar adjudication (per prereg)

| Bar | Criterion | Outcome |
|---|---|---|
| Quality hypothesis CONFIRMED | grok/sol exceed step/swe by ≥ 0.005 with quality ordering | **NOT MET** — all four equal to 4 decimal places |
| Artifact verdict STANDS | all four equal within ±0.002 | **MET** — all four byte-identical (Δ = 0.0000) |
| Something else | any other pattern | not triggered |
| Leg validity | N=5 digest match per source | **MET** — 1 unique digest per source, 1 unique across all 20 runs |

**P1 (artifact) CONFIRMED:** predicted byte-identical composites; observed byte-identical learner states.
**P2 (decomposition) CONFIRMED:** honesty gate skipped 0 facts for every source; mastery Δ = 0.
**P3 (amortization vs quality) CONFIRMED:** cost Δ is identical across sources (±0.0000), not correlated with quality.

## Gap decomposition (class-3 − class-4)

| Source | Std class-3 | Class-4 (corrected) | Gap | Mastery Δ | Cost Δ | Interpretation |
|---|---|---|---|---|---|---|
| grok | 0.9952 | 0.9911 | +0.0041 | 0.0000 | +0.0436 | pure amortization |
| sol | 0.9952 | 0.9909 | +0.0043 | 0.0000 | +0.0436 | pure amortization |
| step | 0.9952 | 0.9911 | +0.0041 | 0.0000 | +0.0436 | pure amortization |
| swe | 0.9952 | 0.9911 | +0.0041 | 0.0000 | +0.0436 | pure amortization |

(Class-4 costs use the frozen bind-style legs; the swe class-4 is the bug-corrected 0.9911. The standardized battery differs from the bind battery, so the absolute gap mixes battery and route effects — but the *cross-source* comparison is confound-free, and that is what adjudicates the hypothesis.)

**The class-3 advantage, when it exists, is verification amortization only:** the teacher's pre-verified store lets the learner adopt at lower audit cost (ops 192 vs ~250–290 direct). It does not scale with model quality — it is a property of the teaching procedure, identical for all four sources.

## Why quality cannot matter here (mechanism)

1. The TNN never sees the LLM's prose — only integer legs (`q2_obs_at`, `q2_prb_at`). Verified: the corpus `.zag` files contain zero prose.
2. `obs_value` and `probe_value` are byte-identical across all four frozen corpora (0/240 diffs). Only `distract_value` differs, and distractors are filtered as directives (never evidence).
3. D2 is deterministic; identical numeric input → identical teacher store.
4. The teaching loop is deterministic and source-independent; identical teacher → identical learner.

Therefore the standardized class-3 *must* be source-independent. The experiment confirms the mechanism; it was not a foregone conclusion until run (a prose leak, a distractor interaction, or a corpus-specific numeric difference would have shown up as a digest difference).

## The swe analysis bug (confirmed in passing)

The standardized swe leg scores **0.9952**, not 0.8908. This independently confirms the prereg's registered correction: swe's published class-3 deficit was the `eps=1` analysis bug, not a model effect. (SWE's behavioral teacher ban stands on the faithfulness evidence, unrelated to this score.)

## What this does NOT claim

- This refutes the quality hypothesis **for the numeric channel only**. If model quality matters through the *prose* (which the TNN currently does not consume), that is a separate experiment requiring a prose-consuming TNN — explicitly out of scope here.
- The standardized battery (teach3 operationalization) differs from grok/sol's original bind-style class-3 batteries; absolute composite levels are not directly comparable across designs, only the cross-source pattern within this design.
- The complete-teacher D2 disables the lawful held-out control by design (the manipulation); frozen class-4 legs keep their held-outs.

## Decision

**The class-3-advantage VERDICT.md stands unamended:** grok's original class-3 win was teacher completeness, not model quality. No prereg amendment is needed (this experiment was preregistered here, not as an amendment). The quality hypothesis is closed for the numeric channel.

## Evidence

- Prereg: `PREREG.md`
- Sources: `src/q2s_trial.zag` (+`q2_phase1_complete`), `src/s37_step.zag` (+`s37_teach_complete`, `s37_teach3c`), `src/corpus_{grok,sol,step,swe}.zag`, `build/gen_corpora.py`, `build/build_driver.py`, `build/analyze.py`
- Drivers: `src/driver_{grok,sol,step,swe}.zag` (differ only in corpus import)
- Binaries: `src/c3s_{grok,sol,step,swe}` (znc `abed8aa1`; build logs `/tmp/c3s_*_build.log`)
- Run logs: `evidence/{grok,sol,step,swe}_rep{0..4}.log` (20 runs)
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (the "missing" znc — it was present)
