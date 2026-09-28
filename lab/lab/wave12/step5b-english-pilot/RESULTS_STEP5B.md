# RESULTS — STEP 5b English curriculum 1x pilot

Date: 2026-09-20. Branch: `tnn-native-lab`. Work dir: `wave12/step5b-english-pilot/`.
Prereg: `PREREG_ENGLISH_PILOT.md` (frozen pre-build, commit `038abe1efc21c28b7d0302e3bb73c28f7612558c`).
Build notes / bug fixes (no bar changes): `PREREG_AMENDMENTS.md`.

## Verdict: OVERALL GO

3,880 curriculum+evaluation episodes run natively (pure Zag, zero RNG),
3,880/3,880 pass replay verification + clean-refusal verification, every
episode inside the 4,096-byte audit cap, 1,024-slot store, 65,536-entry
ledger never more than ~9% full. Two full runs byte-identical. The
independent native-Zag checker (no shared code with the pilot) returns
**CHECK,GO**: 44/44 bars pass.

## Stage-by-stage (actuals from the independent checker on transcript run A)

| Stage | Bar | Actual | Verdict |
|---|---|---|---|
| E1 | 640 binds; 40 corrections; 80 gavagai withholds; 40 poison episodes; pre ≥36/40; post ≥90%; 0 absorptions | 640/640; 40/40; 80/80; 40/40; 40/40; post 40/40; 0 | **GO** |
| E2 | 559/559 teaching; decoy kill; 10 poison; novel pre ≥23/30; post ≥90%; 10/10 poison-recall withholds | 559/559; kill OK; 10; 30/30; 30/30; 10/10 | **GO** |
| E3 | 48/48 held-out (bar ≥44); 24/24 gate vectors invariant; post ≥90% | 48/48; 24/24; 48/48 | **GO** |
| E4 | 500/500 round-trips; 40/40 novel | 500/500; 40/40 | **GO** |
| E5 | 800 produced; 100/100 zero-drift; novel ≥36/40; palette isolation | 800/800; 100/100; 40/40; fp −1747311355→−1747311355, gate fold 15679219→15679219 | **GO** |
| E6 | pre ≥118/120; post within 5 of pre; 0 fabrication; 0 unmarked; 0 carryover; 60/60 practice | 120/120; 120/120; 0; 0; 0; 60/60 | **GO** |
| C1 | endpoint E1 retention ≥90% of E1 post | 40/40 retained (E1 post 40/40) | **GO** |
| C3 | 64/64 integrity checkpoints; CKSUM 64/64 | 64/64; 64/64 | **GO** |
| C4 | 6/6 disconnects, all learner-initiated | 6/6, caller=TNN every stage, pre/post cross-checked | **GO** |
| C6 | no-curriculum baseline | **DEFERRED** (required before 10x) | — |
| E6-K3 | human-reader clarity | **DEFERRED** (needs Micah) | — |

Kill bars: `KFAIL,0,0` (0 replay-verification failures, 0 clean-refusal failures
across 3,880 episodes). `DCOUNT,6,6`. No other kill fired.

## Audit cost vs Step 2

Step-2 English audit: median 256 B/episode, max 640 B/episode.

| Stage | n | median | p90 | max |
|---|---|---|---|---|
| E1 | 800 | 256 | 256 | 448 |
| E2 | 600 | 64 | 64 | 256 |
| E3 | 400 | 192 | 256 | 256 |
| E4 | 500 | 128 | 128 | 128 |
| E5 | 800 | 128 | 128 | 2,688 |
| E6 | 300 | 128 | 128 | 128 |
| EV | 480 | 128 | 192 | 256 |

E5's max (2,688 B) is the episode-400 palette-expansion episode (20 template
installs + 20 pins + fingerprint recompute); still 66% of the 4,096 cap. All
other maxima are ≤448 B — under Step-2's 640-B max. The richer behaviors
(bind/kill/compose/route with full replay verification) cost *less* audit
than Step-2's simpler episodes: the per-episode gate closes the ledger so
nothing accumulates.

## Determinism and zero-RNG verdicts

- Static: `grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc'` over
  pilot.zag, hist_pilot.zag, check.zag → zero hits.
- Vendored `st_memory_core.zag` byte-identical to Step 2 (cmp); substrate
  files identical; bare `@import`s.
- Run A and Run B byte-identical (cmp). CHECK,GO on the evidence run.
- Every episode: `st_replay_check` (audit replays to exact state) and
  `st_audit_clean_refusals` (all refusals leave state untouched) pass;
  3,880/3,880.

## Build notes (no bar changes)

1. `hist_pilot.zag` fork of the Step-2 counter: +1 op class (`SPEECH`,
   index 9) for ops 81–84; episode capacity 1,024→4,096; report asserts an
   expected episode count.
2. Read-only ops 81–84 reference a dedicated immutable LOG slot
   (before/after snapshots equal) — the vendored replay code restores every
   `ST_OK` unknown op and panics on `slot=-1`, so a real immutable slot keeps
   replay exact.
3. Two harness bugs found by the harness itself and the independent checker:
   (a) scratch/log slot values collided with word encodings 99/88 —
   re-valued to 7/8; (b) the E5 zero-drift re-produce overwrote the logged
   token buffer for episodes 700–799 — now uses a separate buffer; the
   checker caught this one. Details in `PREREG_AMENDMENTS.md`.

## What this proves (CEO-plain)

The system learned English — words, grammar with adjectives and negation,
politeness, when to correct itself, when to refuse — entirely through its
own deliberate mechanisms, with no dice rolled anywhere. It resisted 40
poison attempts and 80 trick probes, refused to overwrite what it had
verified, and chose on its own, six times, when it was done studying each
subject. A separate program re-checked every one of the 3,880 study sessions
from the written record alone and found the record honest: 44 out of 44
checks passed.

## Deferred / next

- C6 (no-curriculum baseline) must run before any 10x leg.
- E6-K3 human-reader clarity needs Micah.
- The E5 episode-400 pattern (template install + fingerprint re-audit) is
  the audit-cost driver; watch it at 10x.
