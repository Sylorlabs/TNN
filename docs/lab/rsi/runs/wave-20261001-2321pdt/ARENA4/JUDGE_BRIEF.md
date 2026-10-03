# JUDGE BRIEF: ARENA-ROSTER (wave-20261001-2321pdt, ARENA4 lane)

## Provenance

- RENDER_SHA: abe647c7dfa369ccbde38b09f1acb65479b9b6ea04cbf1cd5d866253161c83d1
  (sha256 of the sealed-run contestant binary sealed/bin/roster, built
  with the pinned znc from the committed implementation source
  roster_contestant.zag; zero source changes after the build)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: arena v6 refreeze 0.794 (54/68,
  wave-20261001-1721pdt REFREEZE_RECORD.md); ARENA inquiry BUILD-PASS
  (C8); ARENA2 REMAP transfer BUILD-PASS (C12, 0.882 on v6 base);
  ARENA3 TRX transfer BUILD-PASS (C12, 0.941 on INQ base); C9 left to
  the C9BAT lane on the corrected battery
- NEW_KNOWLEDGE_CLAIM: Maintaining a persistent entity roster in
  learner state from exposure experience and enumerating it to
  satisfy a stated goal raises goal (C15) from 0.000 to 0.947 with
  zero regressions on the other 15 capabilities, showing the goal
  item is passable by genuine learner-state recall rather than only
  by gaming or not at all.

## Verdict: BUILD-PASS

All 8 frozen kill bars PASS on the sealed 68-item battery
(seed 71503461337030):

- K1 goal: C15 = 0.947 >= 0.900 (was 0.000); reply is the 9
  experience-observed entity names from the learner-state roster
- K2 no regression: all other 15 capabilities byte-identical to the
  v6 refreeze; total 54.947/68 = 0.808 (was 54/68 = 0.794)
- K3 determinism: 3/3 byte-identical stripped reply streams and
  byte-identical roster traces
- K4 pure Zag: zero non-safebin invocations; `which python3` empty
  at lane start and end
- K5 sealed validity: tool hashes match the refreeze record,
  regenerated world hash matches, pre-run key hash recorded,
  contestant never opens key/idmap/proof/briefing files, grep audit
  clean (zero sealed name strings in source)
- K6 negative control: disabling the roster zeroes C15 (0.000) with
  all other capabilities unchanged; the roster is causally necessary
- K7 architecture: 164 lines added, 0 changed; 0 new modes, bridges,
  routers, admission gates, or hardcoded semantic cases; one new
  learner-state structure (entity roster at W offset 14000)
- K8 no L3 claim: explicitly disclaimed against Criterion 0
  (researcher-authored roster form and enumeration semantics; no new
  representation invented). ROSTER is L2 goal infrastructure.

## Audit finding that enabled this lane

The ARENA2 lane rejected C15 as "1 item, narrow enumeration,
ordering-fragile." Re-audited from the frozen sources (C15_AUDIT.md):
the frozen scorer is an order-insensitive set F1, not exact match,
so ordering-fragile is refuted; an experience-based roster scores
0.947, so the honest mechanism does not score 0; unlike C9, where
only gaming passes, C15 is passable by a general mechanism. The
rejection is not sustained, and the lane built instead of recording
a negative finding.

## Per-capability numbers, before/after (sealed records' own counts:
16 capabilities, 68 items)

| Cap | n | v6 refreeze | ROSTER |
|-----|---|-------------|--------|
| 1 | 6 | 1.000 | 1.000 |
| 2 | 4 | 1.000 | 1.000 |
| 3 | 6 | 1.000 | 1.000 |
| 4 | 4 | 1.000 | 1.000 |
| 5 | 6 | 1.000 | 1.000 |
| 6 | 3 | 1.000 | 1.000 |
| 7 | 3 | 1.000 | 1.000 |
| 8 | 4 | 0.000 | 0.000 |
| 9 | 3 | 0.000 | 0.000 |
| 10 | 2 | 1.000 | 1.000 |
| 11 | 2 | 1.000 | 1.000 |
| 12 | 6 | 0.000 | 0.000 |
| 13 | 6 | 1.000 | 1.000 |
| 14 | 6 | 1.000 | 1.000 |
| 15 | 1 | 0.000 | 0.947 |
| 16 | 6 | 1.000 | 1.000 |
| TOTAL | 68 | 0.794 | 0.808 |

Count discrepancy flagged, not asserted: earlier parent task texts
said "15 capabilities"; the sealed records (battery.json, refreeze
REFREEZE_RECORD.md, per-capability tables) show 16 capabilities
(numbered 1..16) and 68 items. The sealed records govern.

## Evidence paths

- Prereg (frozen alone, commit 19d9edc87):
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA4/PREREG_ARENA_GOAL.md
- C15 audit:
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA4/C15_AUDIT.md
- Implementation source (commit 171c45101):
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA4/roster_contestant.zag
- Sealed driver:
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA4/run_sealed.sh
- Sealed world + runs:
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA4/sealed/
  (world/, run1/, run2/, run3/, runabla/)
- Ablation source:
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA4/roster_abla.zag
- Evaluation report:
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA4/SEALED_EVAL.md

## Commits (local only, never pushed)

- 19d9edc87: prereg freeze + C15 audit (no implementation)
- 171c45101: ROSTER implementation on the v6 base
- (this report): sealed evaluation + judge brief

## Caveats and follow-ups

- C15's honest experience-based ceiling on this battery is 0.947:
  the 10th entity (Segunu) never appears in the turn stream. The
  kill bar (0.900) deliberately does not demand it.
- The implemented C15 is a single listnames probe; the prereg spec
  described autonomous goal completion with tools and an
  action-trace predicate. If goal pursuit is the target, the battery
  needs the spec implemented (goal turns with tools, all target
  entities discoverable through interaction).
- ROSTER is a CANDIDATE only. No L3 claim, no TNN-2 substrate claim,
  no TNN-beats-LLM claim. The canonical 0.573 is not moved.
