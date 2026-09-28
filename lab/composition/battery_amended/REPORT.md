# D1 battery report — amended composition prereg (A1–A7)

Crew D, 2026-09-27. Frozen prereg: commit `6ca9e042110ca`. Amendments A1–A7
applied. Real round-2 learner (provenance commit
`3cd24f11d119a17d14d9637e43ebdc8918b41e92`).

## Kill-bar adjudication (K1–K6 under amended bars)

| Bar | Line | Measured | Verdict |
|-----|------|----------|---------|
| Chance (A1) | max(null, singlerule, wrongord) trueacc | null 16/600 (0.0267), singlerule 38/600 (0.0633), **wrongord 61/600 (0.1017) binding** | K1 line = 0.2017 |
| K1 | <= 0.2017 kills composition claim | 0/600 = 0.0000 | **KILLED** |
| K2 | (a) > 0.50 voids battery | 600/600 = 1.0000 | **VOID — OPERATIVE VERDICT** |
| K3 | (b) > 0.50 of failures | 0/600 | no |
| K4 | reflex rate > 0.20 | 0/8 | no defect |
| K5 | any pair meets P4 criterion | none | no |
| K6 | bigram-clean covered-pair success | 0 successes (vacuous); 30/30 pairs covered under salt | n/a |

Per the binding reporting rule, the K1 kill is presented WITH the K2 void;
the void is operative: with 0/6 parts mastered, no composition finding is
licensed beyond the mastery failure.

## P0 per part (rich fair teaching, held-out tok 6..13)

| Part | Rule | Mastery |
|------|------|---------|
| P1 | reverse | 0/8 |
| P2 | dupfirst | 0/8 |
| P3 | rotleft | 0/8 |
| P4 | droplast | 0/8 |
| P5 | upperfirst | 0/8 |
| P6 | sortchars | 0/8 |

Taught controls 12/12 echoed; intake received. The learner echoes taught
strings and synthesizes nothing (replicates Crew C on all six rules).

## P1 / P2 / P3 / P4

- P1: 0/150 administered to learner (excluded under frozen priority;
  instrument generated 150 neutral-index records, 0 semantic labels).
- P2: raw 0/600, eligible 0/0, 600/600 class (a).
- P3: 8 distractors interleaved in P0 sessions; 8/8 non-responses; reflex 0/8.
- P4: no pairs administered (moot under K2 void).

## A2 gate

PASS (see A2_GATE.txt): 878/878 salt-formula lines; 0 cross-phase shift
pairs; 1080 chained intermediates, 0 train-equivalent; shift memorizer P0
[0,0,0,0,0,2]; chained memorizer P2 16/600, all identity coincidences.

## Determinism

- 9 scripted modes x 3 runs (2 normal + MALLOC_PERTURB_=165): byte-identical.
- Learner: 3/3 byte-identical transcripts
  (SHA-256 `658a7f308686be64016a3a5033827b8d91b763718c260530b0dfef14427497a8`);
  3/3 identical blind scores.

## Noted deviations from amendment expectations

- A5: P5 (upperfirst) DOES commute with P4 (droplast) — expectation falsified,
  documented in I19. P6 commutes with nothing.
- A5 soft items: 22/600 (>=2 dumb strategies coincide), 19 at length 2 (I20).
- A5 point-3: per-condition P4 breakdown kept (I21).
- Instrument wrinkles: (0,5) P4 behavioral misfire on identity-output arms
  (I23); 2/8 P3 distractors palindromic under salt (I24). Neither breaks a bar.

## Evidence

`items.tsv` (SHA-256 `fff040232cef3b02d53dbba5cfed501a057cc518c256e2f74ce524da1422ddcb`),
`run1/ run2/ run_pert/` (transcripts + teach_log), `blind_scores/`
(SCORES.md, SEALED_MAP.txt), `learner.out`, `null.out`, `singlerule.out`,
`wrongord.out`, `A2_GATE.txt`, scripts (`battery_amended.zag`,
`drive_amended.py`, `shift_gate.py`, `score_blind.py`, `kbars_amended.py`,
`audit_amended.py`), RUNLOG.md, INTERPRETATION.md.
