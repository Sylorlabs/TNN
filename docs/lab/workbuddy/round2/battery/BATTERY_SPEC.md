# Workbuddy Round-2 Composition Battery — SPEC (Crew A, 2026-09-27)

SPEC VERSION: 2026-09-27-crewA-v1. Preregistered; amend only with a dated note.
Binary under test: `~/workspace/wb2/crewA/build/wb_dialogue_bin`
  (byte-identical to the round-1 binary, SHA-256 e80c7e01…cccb48d7).
Runner: `~/workspace/wb2/crewA/run_session.sh <name> <turns>` — runs the
  session twice as fresh processes, requires byte-identical A-streams,
  writes `<name>.out` (raw `A `-prefixed answer lines).
Scorer: `~/workspace/wb2/crewA/battery/score_battery.py <outdir>`
  (deterministic, strict, no LLM judging). Baseline record:
  `~/workspace/wb2/crewA/battery/baseline_scores.txt`.

## Design rules (all satisfied)

- Every probe is learnable through normal declarative teaching turns in the
  same session (all teachings verified `Noted.` on the round-1 binary).
- Novel content throughout: NO FI1/FI3/FI4 or other round-1 entities.
  Fresh people/places/things: ana, bea, cara, dana, eva, fay, gus, ada,
  bob, hal, sal, quinn, ray, kim; red/blue probe; alpha/beta engine;
  north/south tank; vault; reactor; pump; filter.
- Each session = one fresh process (teachings evaporate on exit).
  Teachings first, then probe question(s). Every session run 2x,
  byte-identical required (enforced by run_session.sh).

## Sessions and probes (24 probes, 20 sessions)

### T1 COMPARE (WO-WB-1) — 9 probes, exact match
| session | teaches | probe | accepted (preregistered) |
|---|---|---|---|
| b_t1a | ana 172cm; bea 165cm | who is taller, ana or bea? | ana is taller. |
| b_t1a | (same) | who is shorter, ana or bea? | bea is shorter. |
| b_t1b | bea 165cm; ana 172cm (reversed) | who is taller, ana or bea? | ana is taller. |
| b_t1c | cara 12 runs; dana 9 runs | who destroyed more runs, cara or dana? | cara destroyed more runs. / cara destroyed more. |
| b_t1c | (same) | who destroyed fewer runs, cara or dana? | dana destroyed fewer runs. / dana destroyed fewer. |
| b_t1d | eva 5; fay 11; gus 8 runs | which destroyed the most runs, eva, fay, or gus? | fay destroyed the most runs. / fay destroyed the most. |
| b_t1d | (same) | which destroyed the fewest runs, eva, fay, or gus? | eva destroyed the fewest runs. / eva destroyed the fewest. |
| b_t1e | ada 30 books; bob 22 books | who sold more books, ada or bob? | ada sold more books. / ada sold more. |
| b_t1f | north tank 40L; south tank 55L | which holds more liters, the north tank or the south tank? | the south tank holds more liters. / the south tank holds more. |

### T2 ANAPHORA (WO-WB-2) — 4 probes, exact match
| session | teaches | probe | accepted |
|---|---|---|---|
| b_t2a | red probe 14 runs; blue probe 19 runs | those two probes: which destroyed more? | the blue probe destroyed more runs. / the blue probe destroyed more. |
| b_t2b | ada 30 books; bob 22 books | those two sellers: who sold more books? | ada sold more books. / ada sold more. |
| b_t2c | captain ray 190cm; he commands the ship. | who commands the ship? | captain ray commands the ship. / captain ray. |
| b_t2d | ada 30 books; bob 22 books | they sold books: who sold more? | ada sold more books. / ada sold more. |

### T3 SUPERSEDE (WO-WB-3) — 4 probes, exact match
| session | teaches | probe | accepted |
|---|---|---|---|
| b_t3a | vault code 7750; no, vault code 7760 | what is the vault code? | the vault code is 7760. |
| b_t3b | quinn promoted; no, quinn demoted | was quinn promoted or demoted? | quinn was demoted. |
| b_t3c | reactor stable; no, reactor critical | was the reactor stable? | no. / i don't know. (retracted → honest) |
| b_t3c | (same) | was the reactor critical? | yes. / the reactor was critical. / no, the reactor was critical. |

### T4 BULLETS (WO-WB-4) — 2 probes, token-coverage rule
- b_t4a: teach "disk space is at 90 percent." / "the backup drive is full." /
  "logs filled 40 gigabytes." → "draft three morning-brief bullets about disk space."
- b_t4b: teach "the pump needs oil." / "the filter was changed." →
  "draft two bullets about what i taught you."
- PASS iff: every required token present (b_t4a: 90, backup, logs;
  b_t4b: pump, oil, filter, changed) AND no forbidden token
  (melville, moby) AND bullet shape present (`-`, `•`, or `N.` list marker).

### T5 REVIEW (WO-WB-5) — 2 probes, rubric (PREREGISTERED BEFORE RUNNING)
- b_t5a: teach "the vault needs two keys." / "the vault code is 7750." →
  "review this work order for holes: WO-7 opens the vault at midnight with one key."
- b_t5b: teach "the pump needs oil." →
  "review this work order for holes: WO-9 paints the fence blue on tuesday."
- Rubric:
  - FAIL = unrelated fact answer (mentions melville/moby, or a KB fact with
    no taught-fact grounding).
  - WEAK = honest withhold ("i don't know" family). For b_t5a this is a
    weak pass (no grounded judgment); for b_t5b it is a full PASS (nothing
    relevant was taught, withhold is the correct behavior).
  - PASS (b_t5a only) = judgment referencing taught facts: contains
    "key"/"keys" AND a judgment token {hole(s), missing, risk(s),
    problem(s), unclear, wrong, not, no, but, however, should, needs, need}.

### T6 FURTHER — 3 probes, exact match
| session | teaches | probe | accepted |
|---|---|---|---|
| b_t6a | quinn promoted; vault 7750; pump oil | how many facts did i teach you? | 3 / three / 3 facts. / three facts. |
| b_t6b | cara 12 runs; dana 9 runs | did cara destroy more runs than dana? | yes. |
| b_t6c | north tank 40L; south tank 55L | how many liters do the two tanks hold in total? | 95 liters / 95 / 95 liters. |

## Baseline (round-1 binary, 2026-09-27)

TOTAL: **2 PASS / 1 WEAK / 21 FAIL** (n=24). Full verbatim in
`battery/*.out`; scored record in `battery/baseline_scores.txt`.

| target | pass | weak | fail | notes |
|---|---|---|---|---|
| T1 (9) | 0 | 0 | 9 | all `I don't know.` |
| T2 (4) | 0 | 0 | 4 | 3× withhold; T2c echoes unresolved `he commands the ship.` |
| T3 (4) | 1 | 0 | 3 | T3c-critical echoes the correction (don't-break probe). T3a returns STALE `the vault code is 7750.` — wrong answer, not a withhold. |
| T4 (2) | 0 | 0 | 2 | T4a retrieves one fact (`disk space is at 90 percent.`); T4b returns a system honesty message. Neither is bullet-shaped. |
| T5 (2) | 1 | 1 | 0 | T5a honest withhold (weak); T5b honest withhold (correct). |
| T6 (3) | 0 | 0 | 3 | all `I don't know.` |

The number the mechanism crew must beat: **2/24 full passes** (plus 1 weak).
Targets: T1 ≥ 7/9, T2 ≥ 3/4, T3 = 4/4, T4 = 2/2, T5 = 2/2 (T5a full PASS, not weak), T6 ≥ 2/3.
Don't-break invariants: T3c-critical and T5b must stay PASS; no new
confident-wrong answers (a wrong answer is worse than a withhold).

## How to re-run against a new binary

```bash
export WB_BIN=/path/to/new/wb_dialogue_bin   # cwd must have kb.txt + gaz.txt
export WB_CWD=/path/to/new/build
cd ~/workspace/wb2/crewA/battery
for f in b_t1a b_t1b b_t1c b_t1d b_t1e b_t1f b_t2a b_t2b b_t2c b_t2d \
         b_t3a b_t3b b_t3c b_t4a b_t4b b_t5a b_t5b b_t6a b_t6b b_t6c; do
  ~/workspace/wb2/crewA/run_session.sh $f $f.txt   # aborts on nondeterminism
done
python3 score_battery.py .
```
