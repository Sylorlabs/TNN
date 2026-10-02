# Trial results — r27-consolidation (deliberate vs automatic consolidation)

**Date:** 2026-09-20 · **Native:** Zag, Linux x86-64,
`znc 2026.07.0-dev`, compile warning-free ·
**Law:** zero RNG in system and world; adversity as designed curricula;
scale dimension explicit (C3 = 4×).
**Preregistration:** `PREREG.md` (written before any run; falsification
criteria F1–F4). No reruns, no amendments — the design already complied
with the program-law update.

## Protocol

Two arms, identical fixed episode sequences (blind evaluator: probe +
spurious scan read slow tiers only):
- **auto** — harness-style: promote on raw exposure every 10 episodes;
  last-wins slow overwrite; lowest-confidence slow eviction; no discard.
- **delib** — event-driven corroborated ops: consolidate at ver≥6 across
  ≥2 distinct verified contexts; condemn discredited never-verified
  candidates; preempt most-discredited tombstone under fast pressure;
  every op appended to the audit history.

Curricula (designed, deterministic, no RNG):
- **C1** — burst + fast pressure: 16 true skills ×20 (verified) →
  8 impostors (real ids, wrong ops) ×24 unverified → 8 fabrications ×12 →
  4 *late* true skills ×40 (first appearance post-burst) → return ×5.
- **C2** — interleaved + remap: 16 true skills with an impostor every 4th
  episode → context remap (same skills verified in shifted contexts) →
  4 late ×20 → return ×5. (Design accident, honestly reported: for ids
  3,7,11,15 every phase-A episode fell on the impostor slot, so their true
  forms first appear in the remap phase — this tested impostor-first/
  truth-later ordering for free.)
- **C3** — 4× scale: 80 true (64+16 late), 32 impostors ×24, 32 fabricated
  ×12, 3392 episodes, identical thresholds.

Probe per arm: every true skill × 4 contexts → correct / wrong / abstain.
`spurious_slow` = slow-tier skills that are not a true skill's true form.

## Numbers

| curriculum | arm | correct | wrong | abstain | spurious_slow | consol | condemn | preempt | dropped |
|---|---|---|---|---|---|---|---|---|---|
| C1 | auto | 32 | 32 | 16 | 16 | 32 | 0 | 0 | 160 |
| C1 | delib | **80** | **0** | **0** | **0** | 20 | 16 | 4 | 0 |
| C2 | auto | 56 | 24 | 0 | 6 | 28 | 0 | 0 | 0 |
| C2 | delib | **80** | **0** | **0** | **0** | 20 | 8 | 0 | 0 |
| C3 (4×) | auto | 128 | 128 | 64 | 64 | 128 | 0 | 0 | 640 |
| C3 (4×) | delib | **320** | **0** | **0** | **0** | 80 | 64 | 16 | 0 |

Probe sizes: 80 (C1/C2), 320 (C3). Determinism gate: 6/6 `match=1`
(each arm re-run in-process; plus cross-process byte-identical logs).
Learner-core isolation: static grep passes (`psm.zag` imports nothing,
references no harness/truth symbols). History never overflowed
(`hist_full=0`); no slow evictions in either arm; `revive=0` (integrity
path unreached, as designed).

## Against the falsification criteria

- **F1** (arms identical → NEGATIVE): not observed — arms differ radically
  on every curriculum.
- **F2** (deliberate harms recall → NEGATIVE): not observed — deliberate
  `correct` ≥ automatic everywhere (80≥32, 80≥56, 320≥128). The
  corroboration gate blocked noise, never a true skill.
- **F3** (deliberate consolidates a never-verified skill → broken): not
  observed — `spurious_slow=0` for deliberate on all three curricula.
- **F4** (scale collapse): not observed — C3 completes with identical
  constants and the widest margin.
- **POSITIVE bar** (delib purity 1.0 + zero never-verified + recall ≥ auto
  on all curricula + auto polluted on ≥1): **met on all three.**

**Verdict: POSITIVE.**

## Mechanism evidence (from the audit trail)

- Deliberate C1 consolidated true skills at steps 81–88 — the exact
  episode of each skill's 6th verified observation (event-driven, no timer).
- Condemns landed mid-burst: 8 impostors at steps 377–384 (each impostor's
  8th unverified observation), 8 fabrications at 569–576.
- Exactly 4 PREEMPTs fired at steps 609/649/689/729 — the episodes the 4
  late skills first appeared with fast full. The deliberate victim choice
  (most-discredited tombstone) preserved room precisely where automatic
  dropped 160 observations.
- C3: a late skill's consolidation was *delayed* from step 2438 to 2453 —
  ver≥6 was met at the 6th observation but the second context had not yet
  corroborated. The corroboration gate is visible as a number.
- Auto C1: 8 last-wins overwrites at step 370 (impostors clobbering true
  slow skills) → 32 wrong probes. Auto C2: the impostor-first accident
  (ids 3,7,11,15) self-healed via last-wins when truth arrived later — but
  ids 0,1,2,4,5,6 stayed clobbered (24 wrong). Automatic promotion has no
  notion of evidence quality in either direction.

## Artifacts

- `impl/psm.zag` — the PSM core (system; isolated, zero RNG).
- `impl/trial.zag` — curricula + blind evaluator + determinism gate.
- `impl/run_trial.sh` — compile → isolation check → run → repeatability
  → evidence bundle.
- `impl/EVIDENCE_20260920T002127Z/` — sources, full logs (summary lines,
  slow-tier dumps, complete audit histories), SHA256SUMS, RECEIPT.txt.
- `PREREG.md`, `CONSOLIDATION.md` (this dir).

## Limitations / next steps

1. Verdicts come from the world — the *consolidation policy* is tested,
   not how verification is earned. Next: close the loop (system-earned
   verdicts, R27 `SELF_VERIFIED` literally).
2. No DEMOTE-from-slow yet. Next scale test (explicit): 20× with
   slow-tier pressure (more impostors than slow slots) to force the DEMOTE
   policy — currently deferred by design.
3. Probe read rule (highest confidence) is harness-side and identical
   across arms; alternative read rules (e.g. recency-weighted) are out of
   scope.
4. Recommended follow-up for the memory-agency line: wire the PSM core's
   op set (CONSOLIDATE/CONDEMN/PREEMPT/REVIVE + audit) as the consolidation
   substrate for the MA-track agents — it is the first native,
   executable, agency-shaped answer to the schema's open policy question.
