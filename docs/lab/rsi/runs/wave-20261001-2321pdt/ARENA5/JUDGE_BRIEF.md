# JUDGE BRIEF: ARENA5-DEFRECALL (wave-20261001-2321pdt, ARENA5 lane)

## Provenance

- RENDER_SHA: 3d629deda888c18d19ff95ce9819829f2c268cf8e459330b7c573c3892cd57d7
  (sha256 of the sealed-run contestant binary sealed/bin/defrecall,
  built with the pinned znc from the committed implementation
  source defrecall_contestant.zag, commit 2320c3454; source verified
  byte-identical to the commit before building; zero source changes
  after the build)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: arena v6 refreeze 0.794 (54/68,
  wave-20261001-1721pdt REFREEZE_RECORD.md); ARENA4 ROSTER
  BUILD-PASS (C15 0.000 -> 0.947 on the original seed via a
  dedicated listnames handler; commits 19d9edc87, 171c45101,
  f8d7b9b2e) as the direct predecessor. DEFRECALL keeps ARENA4's
  entity-roster state and population logic verbatim, removes the
  dedicated listnames handler, and satisfies the goal through the
  generic default action instead.
- NEW_KNOWLEDGE_CLAIM: A stated goal (the C15 bare prompt) can be
  satisfied with no dedicated goal handler when the learner's
  test-turn dispatch carries a general default action (report the
  persistent knowledge state for bare prompts with no applicable
  procedure): C15 rises from 0.000 to 0.947 with zero regressions,
  zero goal-string branches in the mechanism, and the abstention
  behavior rewarded by the frozen scorers preserved.

## Verdict: BUILD-PASS

All 8 frozen kill bars PASS on the fresh 68-item sealed battery
(seed 71503461337032, selected per the frozen Amendment 1):

- K1 goal: C15 = 0.947 >= 0.900 (was 0.000); reply is the 9
  experience-observed entity names from the learner-state roster,
  produced by the generic default action (trace line "defrecall",
  not a goal-named handler)
- K2 no regression: all other 15 capabilities byte-identical to
  the v6 baseline run on the same fresh battery; total 54.947/68
  = 0.808 (was 54/68 = 0.794); C11 (invent) preserved at 1.000
  because the default fires only for bare prompts
- K3 determinism: 3/3 byte-identical stripped reply streams and
  byte-identical defrecall traces
- K4 pure Zag: zero non-safebin invocations; `which python3` empty
  at lane start and end
- K5 sealed validity: arena hash matches the refreeze record;
  world_gen is a 1-line seed variant (diff verified); fresh
  turns/key hashes recorded pre-run; contestant never opens
  key/idmap/proof/briefing files; grep audit clean (zero fresh
  entity-name strings in source)
- K6 negative control: disabling the roster zeroes C15 (0.000)
  with all other capabilities unchanged; the roster is causally
  necessary; the default action alone hallucinates nothing
- K7 architecture: 174 lines added, 0 removed, 0 changed; 0 new
  modes, bridges, routers, admission gates, or hardcoded semantic
  cases; ZERO dedicated goal handlers (zero "listnames" hits in
  the mechanism source; the enumeration trigger is structural);
  one new learner-state structure (entity roster at W offset
  14000)
- K8 no L3 claim: explicitly disclaimed against Criterion 0
  (researcher-authored roster form and default-action semantics;
  no new representation invented). DEFRECALL is L2 goal
  infrastructure.

## What this lane changed relative to ARENA4

ARENA4's flag #2: the implemented C15 was a single probe served by
a dedicated listnames question handler, while the prereg spec
described autonomous goal completion. This lane closes that gap
under the load-bearing constraint (no dedicated goal-completion
handler):

- The `if(streq(head,"listnames"))` block is gone, replaced by the
  generic default action at the existing fallback position.
- The default action fires for ANY bare prompt with no specific
  handler (demonstrated on novel dev prompts "recall" and "who",
  never in any battery), and abstains (UNKNOWN) for parameterized
  prompts with no handler (preserving C7/C11).
- A supplementary run (default action disabled, roster enabled)
  scores C15 = 0.000, proving the default action is the
  goal-completion path and no hidden handler carries the goal.

Honest limitation, stated plainly: on this battery the default
action is extensionally equivalent to a listnames handler (the
C15 probe is the only bare prompt among the test items). Its
claim to generality rests on intension, not extension: zero
goal-string references in the mechanism (audited), a structural
trigger, and demonstrated firing on novel bare prompts. The judge
should weigh whether that clears the "dedicated handler" bar.

## Per-capability numbers (fresh battery, seed 71503461337032)

| Cap | n | v6 fresh baseline | DEFRECALL |
|-----|---|-------------------|-----------|
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

Count note: the sealed records show 16 capabilities (numbered
1..16) and 68 items. The sealed records govern.

## Evidence paths

- Prereg (frozen, commit b63f80289):
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA5/PREREG_DEFRECALL.md
- Amendment 1 (frozen alone, commit f3320caf8):
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA5/PREREG_DEFRECALL_AMEND1.md
- Implementation source (commit 2320c3454):
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA5/defrecall_contestant.zag
- Sealed driver:
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA5/run_sealed.sh
- Fresh world + runs:
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA5/sealed/
  (world/, bin/, v6base/, run1/, run2/, run3/, runabla/,
  runnodef/)
- Ablation source:
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA5/defrecall_abla.zag
- Supplementary source (default action disabled):
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA5/defrecall_nodef.zag
- Evaluation report:
  docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA5/SEALED_EVAL.md

## Commits (local only, never pushed)

- b63f80289: prereg freeze + NAMECHECK Step 0 (no implementation;
  note: this commit swept in two BATTERY-E4 files staged by a
  concurrent worker in the shared index; later commits use
  pathspec isolation)
- f3320caf8: Amendment 1 (seed-selection rule; alone, 1 file)
- 2320c3454: DEFRECALL implementation (alone, 1 file)
- (this report): sealed evaluation + judge brief

Commit-order self-check: prereg commit b63f80289 strictly precedes
the implementation commit 2320c3454. Satisfied.

## Caveats and follow-ups

- C15's honest experience-based ceiling is 0.947 on every seed:
  entity index 9 never appears in expo turn events (structural).
  The kill bar (0.900) deliberately does not demand it.
- The frozen battery still expresses the goal as a test-turn bare
  prompt; the original spec's tool protocol (goal turns with
  tools, action-trace predicate) remains unimplemented. The
  autonomy shown here is handler-free goal completion, not
  multi-step tool use.
- DEFRECALL is a CANDIDATE only. No L3 claim, no TNN-2 substrate
  claim, no TNN-beats-LLM claim. The canonical 0.573 is not moved.
