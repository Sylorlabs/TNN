# UNPHONY LOOP LOG

## 2026-09-24 ~06:30 UTC — loop opened
- Frozen bar committed: `docs/lab/audio/unphony_loop/UNPHONY_BAR_V1.md`
  (commit e972b34e9553b780cac2df1e395e1517cbfd0522, tnn-native-lab).
- Key constraint recorded: PAR recurrence 1.0 still horrible → phoniness ≠ drift.
- Grok wave 1 fired (4 parallel, highest reasoning): A1 clip diagnosis,
  A2 general theory, A3 synthesis architectures, A4 plan-vs-render red-team.
- Fable R1 fired (batched deep audit, 6 hard sub-questions).
- Clip measurement job running (numpy stats on 4 motif wavs).
- Debate context drafted: ~/workspace/unphony_loop_work/debate_context.md.

## Coordination with V11
- V11 line is ACTIVE (4 preregs frozen 2026-09-23/24: gesture, waveguide,
  repair, paradd_tract + amendment). Fork W = child-scale digital-waveguide
  vocal tract + two-mass vocal folds — the physical-modeling bet for voice.
- This loop does NOT duplicate fork W. Loop territory: (1) motif/instrumental
  phoniness (different physics), (2) general phoniness theory + frozen
  discriminator, (3) generalize or explain fork W's outcome.
- Real anchors available: aporee kids (voice), inspiration/ dir (mars wind,
  dust devil, ice crackling, thunderbolts) for non-voice classes.

## Next
1. Grok wave 1 + fable R1 land → spawn 3 native debaters
   (steelman / red-team / judge-synthesizer).
2. Debate → build shortlist (max 3) → pure-Zag test crews.
3. Red-team forks → loop.

## 2026-09-24 ~06:35 UTC — grok 524, recovered, natives spawned
- Grok wave 1 first attempt: all 4 calls HTTP 524 (provider down). Probe call
  succeeded minutes later (transient). Wave 1 re-fired in background.
- 2 native hypothesis subagents spawned (instrumental-phoniness mechanisms;
  plan-vs-render + discriminator design) — loop does not stall on providers.
- In flight: grok x4, fable R1, numpy clip stats, native hyp x2.
- Next: all land -> 3 debaters (steelman/red-team/judge) -> build shortlist.

## 2026-09-24 ~06:40 UTC — fable R1 timeout, wrapper built
- Fable R1 via unorouter.py failed: read timeout (unorouter.py hardcodes
  120 s; fable's deep reasoning needs far longer).
- Built ~/workspace/unphony_loop_work/fable51.py (mirrors grok47.py pattern,
  model claude-fable-5.1, 1800 s timeout). R1 re-fired with it.
- Lesson: never use unorouter.py chat for fable deep rounds; use fable51.py.

## 2026-09-24 ~06:55 UTC — grok flapping, backoff loop installed
- Grok wave-1 retry: all 4 HTTP 524 again (provider flapping: brief recovery
  then down). Per standing notes grok can be down a whole session.
- Installed grok_retry.sh: background loop, 10 attempts, 25-min backoff,
  writes grok_out/SENTINEL on completion/exhaustion. Loop proceeds WITHOUT
  waiting: native hyps + fable R1 carry round 1; grok folds in if/when it
  recovers (grok is cheap; the hypotheses stay useful whenever they land).
- KEY MEASUREMENT (clip_measurements.txt): all 4 clips HNR ~ -2..0 dB —
  nearly inharmonic. Debate must explain missing harmonicity, not drift.

## 2026-09-24 ~07:00 UTC — native hyp A landed
- 6 hypotheses (attack missing / dead partials / no room / identical repeats /
  frozen sustain / no sympathetic coupling), ranked by ear-impact.
- Key: H1+H2+H6 compose into one deterministic pipeline (exciter -> strike ->
  modal body -> vibrato -> sympathetic bus -> room FDN), zero RNG.
- Whole-set killer defined: if all six meters show render ~= anchor, the
  phoniness is in the PLAN, loop moves up to the planner.
- Still in flight: native hyp B, fable R1 retry, grok backoff loop.

## 2026-09-24 ~07:10 UTC — both providers 524, loop goes native-first
- Fable R1 retry ALSO hit HTTP 524 (rc=1, 27 bytes). Whole UnoRouter backend
  flapping for both grok-4.7 and claude-fable-5.1.
- Installed fable_retry.sh (same backoff pattern as grok: 10 attempts,
  25-min spacing, SENTINEL on done). Both model waves now retry unattended.
- LOOP PROCEEDS NATIVE-FIRST: measurement crew spawned to build the
  falsification meters from native_hyp_A (attack centroid drop, partial
  co-modulation, room T60, repeat CV, vibrato, better HNR) and run them on
  the 4 clips + hunt for a real music anchor. Measurement-first was the
  hypotheses' own falsification order — the debate gets calibrated numbers
  instead of predicted thresholds.
- Debate fires when native hyp B + meter results land; grok/fable fold in
  on recovery.

## 2026-09-24 ~07:15 UTC — native hyp B landed
- Plan-vs-render: clean seam defined; 2x2 factorial decisive experiment
  (P_TNN/P_HUMAN x R_CUR/R_PHYS) with committed decision rule incl.
  "both wrong" -> report exhaustion. Commits: RENDER dominates (single-note
  killer: timbre fails in 200 ms; plan needs a sequence).
- Discriminator: 8 features, pure-Zag deterministic, milli-unit bars;
  11 red-team traps (3 must-score-real, 5 must-score-phony, 3 adversarial).
- Note: subagent claimed clip_measurements.txt missing — file EXISTS
  (written before spawn); its caveat is stale, debaters get the real file.
- Next: spawn 3 debaters now; meter results arrive as follow-up -> final rank.

## 2026-09-24 ~07:20 UTC — debate round 1 spawned
- 3 debaters (steelman / red-team / judge-synthesizer) arguing native_hyp_A +
  native_hyp_B + clip measurements. Judge issues provisional ranking now,
  final when meter results land (will forward via subagent.send).
- In flight: 3 debaters, meter crew, grok backoff, fable backoff.
- After debate: build shortlist (max 3) -> pure-Zag test crews -> red-team.

## 2026-09-24 ~07:25 UTC — steelman + judge landed, red-team fed
- STEELMAN: render-dominates frame strongest (plan swept to extremes, HNR
  defect constant); H2 attack; H1 dead partials. Counter: plan-dominates
  (R_PHYS plan-driven; single-note killer = category error; uncanny valley;
  detuned pitch classes = live plan-side cause of inharmonicity).
- JUDGE (provisional): #1 missing physical source model (harmonic-sustain
  deficit), #2 H2 attack, #3 H1 modal body, #4 plan-schema impoverishment.
  Killed: drift/recurrence, timing-only, additive-sine, reverb-rescue, RNG.
  2x2 repaired (single-note pre-test first). Builds: meter battery, R_PHYS v1,
  repaired 2x2. Confidence ~70% render-side; most-likely-wrong: crude HNR
  proxy misleads -> calibrated meters decide (meter crew running).
- Red-team debater still running; forwarded steelman+judge for full-strength
  engagement. Judge gets meter results next for FINAL ranking.
