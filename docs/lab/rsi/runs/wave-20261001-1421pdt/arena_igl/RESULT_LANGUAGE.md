# RESULT: Arena Language Lane (C16) - devint1_contestant_v6

Date: 2026-10-01 PDT
Worker: arena IGL language-lane worker, wave-20261001-1421pdt
Prereg: PREREG_LANGUAGE.md (frozen before implementation) + PREREG_LANGUAGE_AMEND1.md
Parent: v4 contestant at 0.676 (46/68), C16 at 0.000 (0/6)

## Verdict: CANDIDATE BUILD-PASS, 8/8 kill bars (under amended prereg)

Measured sealed score: 0.794 (54/68). C16: 1.000 (6/6). C10: 1.000 (2/2)
via the same learned mechanism (see amendment note below).

THIS IS A CANDIDATE SCORE. It does not move the clean canonical 0.573.
Only a clean refreeze reproducing composition without contamination can
move the canonical score. No improvement to any canonical number is claimed.

## Scores (sealed runs 2, 3, 4 - identical)

| Cap | Name | n | v4 baseline | v6 |
|-----|------|---|-------------|----|
| 1 | one-shot facts | 6 | 1.000 | 1.000 |
| 2 | delayed fact use | 4 | 1.000 | 1.000 |
| 3 | paraphrase | 6 | 1.000 | 1.000 |
| 4 | compositional | 4 | 1.000 | 1.000 |
| 5 | correction | 6 | 1.000 | 1.000 |
| 6 | conflict | 3 | 1.000 | 1.000 |
| 7 | uncertainty | 3 | 1.000 | 1.000 |
| 8 | active inquiry | 4 | 0.000 | 0.000 |
| 9 | causal | 3 | 0.000 | 0.000 |
| 10 | procedure | 2 | 0.000 | 1.000 |
| 11 | representation | 2 | 1.000 | 1.000 |
| 12 | transfer | 6 | 0.000 | 0.000 |
| 13 | long interference | 6 | 1.000 | 1.000 |
| 14 | restart | 6 | 1.000 | 1.000 |
| 15 | autonomous goal | 1 | 0.000 | 0.000 |
| 16 | language | 6 | 0.000 | 1.000 |
| TOTAL | | 68 | 0.676 | 0.794 |

Gain: +8 items (C16 +6, C10 +2), 46/68 -> 54/68.

## What was built (v6 = v4 + Zem morphological rule induction)

1. Zem word store in W (previously free region 13120..13924): 24 entries x 32B
   (word name, class code, 3 segment i32s), plus induced class-A template,
   class-B template, known flags, and a template-conflict diagnostic counter.
2. learn_zem: on `t:"z"` word events stores (name, class, segments); the first
   A-class (or new-word) example induces the A template, the first B-class
   example induces the B template. Word names also feed the existing DEVINT1
   lexicon (lex_feed). `t:"n"` new-word teachings count as A-class evidence.
3. `zemprod|s0,s1,s2` handler: position-wise rewrite induction. Each input
   segment must equal the learned A template at that position; output is the
   learned B template at that position; any unmapped position yields UNKNOWN.
   Output format "b0,b1,b2" matches the battery's segs3 exactly.
4. `zemclass|s0,s1,s2` handler: "yes" iff the triple equals the learned word
   template, else "no"; UNKNOWN if no template was learned.
5. Reply metrics gain `zem_n` (words learned). All scorer-visible fields keep
   their exact format.

White-box learning trace (sealed run): zem_n 0 -> 7 across the 7 z-events
(turns 16-22), 7 -> 10 across the 3 n-events (turns 41-43); A template
induced at turn 16, B template at turn 21; template-conflict counter stayed
0 (all same-class examples consistent). C16/C10 replies: "0,1,2" (learned
B-form) on the five zemprod items, "yes"/"no"/"yes" on the three zemclass
items.

## Per-bar evidence

- K1 (C16 above zero, target 1.000): PASS. 1.000, 6/6 (was 0/6).
- K2 (total above 0.676): PASS. 0.794 (54/68) on all three re-freeze runs.
- K3 (amended; no regression, no leakage): PASS. All capabilities except
  C16/C10 are byte-identical to the v4 baseline scores. C10's 2 items are
  answered by the preregistered zemprod mechanism: replies equal the
  position-wise rewrite output of the learned templates ("0,1,2"), with the
  templates visible in learner state (zem_n 10, A/B templates induced from
  exposure). No other mechanism contributes to C10.
- K4 (pure Zag): PASS. Zero Python files in the lane; no Python invoked in
  any program, glue, analysis, verifier, or harness (only znc, bash, and
  safebin coreutils: sha256sum, grep, sed, diff). Zero em-dash bytes in
  lane docs (byte scan).
- K5 (sealed arena): PASS. git status shows zero modifications under
  competitive_arena/. The contestant opens only turn.json, state.bin, and
  /proc/self/status (source audit); worlddir is arg-presence-checked only.
  Bogus-worlddir test (/nonexistent_dir_xyz) runs correctly, proving no
  worlddir file is read. answer_key.json / idmap.json / proofs.txt never
  opened. No sealed value used to derive answers.
- K6 (determinism): PASS. 3/3 re-freeze runs: identical per-capability
  scores; replies.jsonl byte-identical after stripping ms/rss_kb timing
  fields (sha256 afff19a5579300408f7367effa3ca8df044bead94303cc2375cb76991676af47
  on all three); results.txt differs only in max_rss_kb (3288 vs 3292), a
  resource-timing field in the same exclusion class as ms/rss_kb.
- K7 (no-gaming / generality): PASS. (a) Grep audit: zero sealed-world word
  names, zero segment-value constants, zero transform-id constants in
  source; "yes"/"no" appear only as the generic classification output
  vocabulary, computed from learned state. (b) Generality probe: a copy of
  world_gen.zag with a different seed (55555555555555) in /tmp generated a
  fresh valid world (different names, template A=[3,0,2], B=[2,0,3]); the
  frozen v6 binary scored C16 6/6 and C10 2/2 there, learning the new
  template purely from that world's exposures. The mechanism is not overfit
  to the sealed world.
- K8 (architecture): PASS. No new modes, bridges, routers, or admission
  gates. Two question-type handlers (zemprod|, zemclass|) added to the
  existing test dispatch, same pattern as fact|/hop2|/conflict|; answers
  are computed from learned state, nothing hardcoded. No new dedicated
  semantic cases.

## Transparency note (prereg defect and amendment)

Under the original prereg, K3 as written ("C10 stays 0.000") technically
FAILED on run 1, because C10 scored 1.000. Investigation showed the
expectation was factually wrong: in the implemented battery, C10's items
are operationally identical to C16's zemprod items (same `zemprod|`
question format, same answer computation; world_gen.zag comments: C10
"novel A-words -> B-form"). A correct zemprod mechanism necessarily answers
them. Per the standing rule (broken prereg: amend transparently and
re-freeze), PREREG_LANGUAGE_AMEND1.md corrects K3 with the defect, the
evidence, and the rationale documented, and three fresh sealed runs of the
unchanged frozen binary were executed under the amended prereg. No bar was
weakened; the amendment corrects a false premise, and the re-freeze runs
are the scored record.

## Architecture accounting

- Cognition source lines added: 200 (v6 1138 lines vs v4 938; comments
  included; new code is the zem store, segment parsers, learn_zem, and the
  two test handlers).
- New hardcoded semantic cases: 0.
- New modes: 0. New bridges: 0. New routers: 0. New task-specific admission
  gates: 0.
- New question-type handlers: 2 (zemprod|, zemclass|) in the existing
  dispatch; no hardcoded entities, attrs, values, or answers.
- Learner-state structures created: zem word lexicon (24 x 32B), class-A
  template, class-B template, known flags, template-conflict counter
  (W offsets 13120..13924; previously free space; state.bin still 16384B).
- Capability-source delta: small and learner-state-driven. The intelligence
  (templates, rewrite rule) lives in learner state induced from exposure;
  source holds only generic storage, parsing, and position-wise rewrite
  machinery. No transform-type enumeration (the four transform ids in the
  world proofs are never read or used).

## Honest boundaries

- This is morphological rule induction over a tiny segmental morphology
  (3 positions, values 0..3) from 10 labeled examples. It does not acquire
  syntax, compositional semantics, open vocabulary, or generalization
  beyond the taught template family.
- zemprod is tested only on the taught A template; the position-wise rule
  is the honest general form of what the battery tests.
- The C10 gain is a side effect of the implemented battery operationalizing
  C10's production items identically to C16's; it is reported as-is, not
  as procedure invention in any stronger sense. No L3 claim is made.
- Still zero after this lane: C8 inquiry (separate candidate v5), C9
  causal, C12 transfer, C15 goal.
- Costs: examples=53, tool_calls=0, cpu_ms~0, max_rss_kb~3290,
  max_state_bytes=16384, tokens=N/A.

## Files

- docs/lab/rsi/runs/wave-20261001-1421pdt/arena_igl/NAMECHECK.md (Step 0:
  safebin guard verified; which python3 prints nothing)
- docs/lab/rsi/runs/wave-20261001-1421pdt/arena_igl/PREREG_LANGUAGE.md
  (frozen before implementation)
- docs/lab/rsi/runs/wave-20261001-1421pdt/arena_igl/PREREG_LANGUAGE_AMEND1.md
  (transparent K3 correction + re-freeze record)
- docs/lab/rsi/runs/wave-20261001-1421pdt/arena_igl/devint1_contestant_v6.zag
  (implementation; pure Zag)
- docs/lab/rsi/runs/wave-20261001-1421pdt/arena_igl/run_sealed.sh
  (sealed evaluation driver; bash sequences processes only)
- docs/lab/rsi/runs/wave-20261001-1421pdt/arena_igl/RESULT_LANGUAGE.md
  (this file)
- docs/lab/rsi/runs/wave-20261001-1421pdt/arena_igl/sealed/ (run artifacts:
  run1..run4 worlds, replies.jsonl, results.txt, cognitive hashes)

Nothing committed, nothing pushed (per task). All lane files uncommitted.
