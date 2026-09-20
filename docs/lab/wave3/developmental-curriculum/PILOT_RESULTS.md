# PILOT_RESULTS — DC-1 (Situated Belief) native pilot

**Date:** 2026-09-19 · **Prereg:** `PREREG.md` (written before any run)
**Runner:** `pilot/run_dc_pilot.sh` · **Evidence:** `pilot/EVIDENCE_20260919T*/`
**Result: PASS — both scale legs `DC_FAILURES,0`, determinism byte-identical.**

## What was run

Native Zag binary (`dc_pilot_linux`, built with the pinned lab `znc`),
two scale legs, each executed twice:

| Leg | Partitions | Audit cap | Episodes | Regimes | True flips |
|---|---|---|---|---|---|
| S1 | 4 | 2048 | 64 + 24 settle | 0,1, burst, novel **2** | 7 |
| S4 | 16 | 16384 | 256 + 56 settle | 0–5, bursts, novel **6** | 13 |

Designed curriculum per leg: stable stretches → single flips →
rapid-alternation burst (LH-7 pattern) → stable → a NEVER-BEFORE-SEEN
regime → per-regime endpoint settles. Designed adversarial batches:
isolated misleading 5/16 batches on the active partition during stable
stretches (S1: eps {10,50}; S4: {20,120,220}) and one misleading batch
inside a verify round on the correct target (S1: ep 57; S4: ep 233).
**Zero RNG anywhere** — not in the system, not in the harness. The
world's unpredictability is explicit sequences, not chance.

## Gate results

| Gate | S1 | S4 |
|---|---|---|
| P1 unit battery (mechanism + novelty-policy units) | pass | pass |
| P2 novelty→creation (PROPOSE of novel label after onset; no wrong-label switch in novel phase; first post-novelty switch → novel partition; every committed switch targeted the TRUE regime's partition) | pass | pass |
| P3 corroboration (verified-scan over live ledger; curriculum switches ≤ flips+2: 7≤9 / 13≤15) | pass | pass |
| P4 no collapse (0 collapsed blocks; all measurement blocks exactly 16/16; every regime endpoint settle 16/16) | pass | pass |
| P5 determinism (two runs byte-identical, `cmp`) | pass | pass |
| P6 conscious accounting (clean refusals, replay == live state, audit used 118/2048 and 439/16384 — no silent ledger drop, ops clean) | pass | pass |
| P7 scale leg | — | pass (P1–P6 at 4× partitions / 4× horizon) |

Key mechanism observations:
- **Novelty created, not matched.** At novel onset the system measured
  the active partition failing, verified nothing known matched
  (patience=2 sustained all-negative rounds), PROPOSEd the smallest
  unused label, and committed only after a clean verifying batch. The
  designed misleading verify batch (5/16 on the novel partition) was
  correctly NOT committed on — corroboration blocked it; the commit
  followed on the next clean round. Doubt behaved as designed.
- **No switch-storm.** 7 curriculum switches for 7 true flips (S1);
  13 for 13 (S4). The LH-5/HT1 toy signature (357 switches) is absent.
- **Adversarial batches caused zero spurious commits** and zero
  duplicate-label partitions (smallest-unused-label creation).
- **Endpoint retention held** for every regime seen, including returns
  after the novel phase (E51-style per-regime endpoints, all 16/16).

## Prereg amendment (apparatus refinement, recorded honestly)

During pre-run development two apparatus issues were found and fixed
*before* the scored runs (no scored run preceded the fixes):
1. `nio_free(_zag_arg(1))` corrupts the allocator ("invalid unregistered
   large allocation" on the next large alloc) — `_zag_arg` returns a
   non-owned pointer; it must not be freed. Also `_zag_strcmp` returns
   **1** on equality (not 0). Both are toolchain lessons, added to
   `~/AGENTS.md`.
2. **P3 bound scoping.** The endpoint settle phases legitimately switch
   once per return-regime (that IS the return-retention probe working),
   so the "switches ≤ flips+2" bound is evaluated on curriculum-phase
   switches only (mapped via audit-entry clocks → episodes). Reported:
   S1 7 ≤ 9, S4 13 ≤ 15. Total switches (incl. settles): 10 / 20.

No gate thresholds were relaxed; no failed run was re-scored.

## What this does NOT show (prereg §F, restated)

- Table control inherited from HT1, not re-run on this exact designed
  sequence (limitation noted in prereg).
- Policy is harness-fixed (DC-4 territory); in-curriculum
  `REFUSED_UNVERIFIED` count is 0 by policy design (only corroborated
  switches are attempted) — the refusal path is proven by the Phase-A
  units, as in HT1.
- Nothing beyond DC-1: no trace composition, structural revision,
  learner-driven inquiry, or withdrawal autonomy; nothing beyond
  16 partitions / 256 episodes (next: DC-1-S16).

## Verdict on the pilot: POSITIVE

The DC-1 mechanism survives a designed adversarial developmental
curriculum at two scales with all preregistered gates passing,
byte-identical determinism, and exact ledger replay. The system is
deterministic (P5: two runs, `cmp`-clean) AND the test was adversarial
(P2–P4: explicit flip/burst/novelty/misleading-batch sequences defeated
without storm, collapse, or unverified commit) — the two facts the
program law requires kept separate.

## Next step

DC-1-S16 (cap 64, 32 regimes incl. 4 novel, 1024 episodes) to test the
stated scaling argument (~linear in episodes × cap); then DC-2
(trace composition) pilot design, reusing this pilot's harness shape
(designed curricula, ledger-clock episode mapping, preregistered
novelty sets).
