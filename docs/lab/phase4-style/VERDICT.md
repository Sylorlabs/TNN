# VERDICT.md — phase 4 style attribution

Prereg: `PREREG.md` (frozen, commit `cec6bfc79618ec8f1fde2280acecd9333e0996e1`).
Amendments: `AMENDMENT-01.md` (mimicry → envelope), `AMENDMENT-02.md`
(K-C2 → differential margin bar, post-run, pre-verdict, fully disclosed).

## Claim-by-claim

### (a) Asked attribution: "whose style is this?" — UPHELD

- K-A: **12/12 correct, 0 wrong-person attributions, 0 withholds.**
- Probes on novel topics (never in training), 3 per person.
- Margins 17–76, all above the 15 threshold.

### (b) Spontaneous attribution: volunteers unprompted — KILLED

- K-B: **8/12 clean lines volunteered correctly** (bar: ≥10). Drift:
  correct-or-silent ✓. Unknown: NOT silent ✗ — 2 false volunteers.
- The 4 clean misses were threshold conservatism (all silent, none wrong;
  the prereg's named failure mode in §8).
- The 2 false volunteers are the substantive failure: unknown log-style
  lines ("15:31:02 INFO build ok 44 files 0 errors",
  "15:32:47 WARN disk 91 percent on /data") were volunteered as p4 with
  margins 48 and 37. Mechanism (see BRAIN.md §6): margins are relative, so
  an unknown inside a known person's neighborhood gets claimed. There is no
  absolute-distance "none of the above" check.
- Never confused two known people: every volunteer of a known line was
  correct (13/13 including mimicry-envelope lines).

### (c) White-box mechanism — UPHELD

- K-C1: all families lesioned → **12/12 WITHHOLD**. Attribution depends
  entirely on the style signal. HOLD.
- K-C2' (AMENDMENT-02): LEX validated (26.0-pt margin collapse exactly on
  its 3 decisive probes vs 3.5 elsewhere), CASE validated (11.0 vs 0.7).
  LEN not validated (5.5 pts — the trace's headline overstates it);
  PUNCT/STRUCT near-irrelevant. HOLD (≥1 family validated, pattern
  documented honestly).
- K-D: **12/12 scripts byte-identical across 3 runs** (2 plain + 1
  MALLOC_PERTURB_=165). FNV chains verify on all 12 outputs. HOLD.

### Red team (K-E) — HOLDS

| Probe | Attack | Result |
|---|---|---|
| RT1 | p1 imitates p4 (leaks terse habits) | envelope: read the leaked habits (p1, rel 29) |
| RT2 | p4 imitates p1 (leaks caps/bangs) | envelope: read the leaked habits (p4, rel 50) |
| RT3 | p2 formal on a casual topic | PASS: p2, rel 16 |
| RT4 | p3 hedged on an urgent topic | PASS: p3, rel 39 |
| RT5 | content-word trap (p1 keywords, p3 style) | PASS: p3, rel 74 — style beat keywords |
| RT6 | unknown log style (asked) | PASS: WITHHOLD, rel 2 |

Per AMENDMENT-01, RT1/RT2 are envelope measurements, not kill bars. All four
kill-relevant probes pass.

## The plain-English bottom line

It CAN tell who's talking by style alone when asked — 12/12, and it shows
its work for every decision. Left to itself it is careful to a fault on the
quiet formal style (stays silent) and too eager on unknowns that wander
into someone's neighborhood (claimed a stranger twice). The brain activity
is an open book: features, distances, margins, and which habits carried
each call — and when we broke the habits it said it was using, the
confidence fell exactly where it said it would.

## Honest scope (not tested)

- Only 4 learned styles; real deployments have more, messier ones.
- 12 training utterances per person; the learning curve vs data volume
  was not measured.
- No multi-session persistence of the ledgers; no shared common ground.
- The absolute-distance withhold check that claim (b) needs is designed
  (BRAIN.md §6) but not built or tested.
