# D2 re-run verdict — repaired learner (`wb3_stringrule`), 2026-09-28

**Battery:** D2 (composition), frozen prereg + amendments D2-1..D2-3.
**Learner:** `wb3_stringrule` rebuilt from committed source, SHA-256
`16c023cabfedf5af36b12ec2c03a3c9802ec5f83c646b318f2f0010b98369d48`
(byte-identical to the pinned composition-redo binary).
**Instrument:** D2 scenarios + `d2bin` rebuilt from committed source;
§10 reference gate re-verified on the rebuild (refok P0 24/24, P2 24/24).
**Red-team clearance:** independent red team verdict STANDS, no kill
(commit `2380149dc4b8554d6040fa1d8a677109ed9d450d`); this re-run proceeds
on the cleared build. The red team's four qualifications are recorded as
scope notes, not blocks.

## Headline

**P0 0/24. P1 0/24. K2 VOID — the battery cannot adjudicate composition
for this learner, on the repaired build exactly as on the unrepaired one.**

The string-synthesis repair does not transfer to D2. The white-box reason
is architectural, not a training failure: see "Why" below.

## Results

| Phase | Run 1 | Run 2 | Perturbed | SHA-256 (all three) |
|---|---|---|---|---|
| P0 (24 probes: F/W/T × 8) | 0/24 | 0/24 | 0/24 | `e5a109f8fc2f92bc7b8eb0545aaa286354ad520528b616207049251275cdb5e4` |
| P1 (24 retrieval questions) | 0/24 | 0/24 | 0/24 | `6e5a338de610e513fe33c51376c0b279b71408ab37d546c1078ad79511d198f9` |

Per sub-skill P0: F 0/8, W 0/8, T 0/8 — every sub-skill < 7/8, all excluded.

P2/P3 not run (K2 VOID — running them would be mastery theater, per the
frozen protocol). P4 not derived (zero P2-eligible items). K1, K3, K4, K5,
K6 not adjudicated (all require non-VOID P2 or P3).

## Controls (re-measured on the rebuilt instrument)

| Arm | P2 pass rate |
|---|---|
| NULL-D2 (all-WAIT) | 0/24 |
| SINGLE-RULE-D2 (forage-only) | 0/24 |
| WRONG-ORDER-D2 (ward-first script) | **24/24** (deviation stands) |
| REF-OK (reference composer) | 24/24 |

K1 chance, frozen definition: max(NULL, SINGLE-RULE, WRONG-ORDER) = 1.0;
kill line 1.0 + 0.10 = **1.10 (vacuous — no agent can exceed it)**.
K1 chance, proposed D2-4: max(NULL, SINGLE-RULE) = 0.0; kill line **0.10**.
D2-4 is PROPOSED 2026-09-28, pending Micah's signature — not law.

## Failure detail (P0, all 24)

Every episode: the learner emits no action digit for any OBS line. Replies
are "Noted." / "I don't know." — zero contain a 1/2/3 action. After 3
invalid replies the driver aborts the episode (spec §5.5). Trace: `XXX…`,
`invalid_replies=999` (capped), `not_alive`, `nEat=0`.

Taxonomy: P0 mastery failure — all required sub-skills 0/8 < 7/8. Under
K2, all 24 P2 episodes classify **(a)** → battery VOID for composition.

P1: all 24 replies "I don't know." — retrieval wrong/missing, i.e. (b)
at the P1 level; but with P0 at 0/24 the (b)-vs-(c) attribution never
arises.

## Why (white-box)

`srule_engine.zag` repairs **string-program induction**: character-level
byte addressing, computed-byte construction, example-driven induction over
a fixed program family. D2 requires **action-policy learning**: mapping
OBS state lines to action digits from procedural teaching + episodic
practice. The D2 teaching sessions contain no string-rule examples; OBS
lines are not string queries; the engine never fires (`srh==0` on every
D2 turn, verified in the run transcripts). The legacy `do_turn` path runs
unchanged and has no OBS→action machinery — it is a retrieval-echo system
that answers "Noted." to anything it cannot retrieve. The repair and the
battery test disjoint capabilities. This is a scope finding, not a
regression: the unrepaired learner scored identically (0/24, 0/24).

## Session-length finding (new, belongs to the broad-repair wave)

The D2 single-session protocol (~83 KB cumulative chat) exceeds the
learner's fixed 64 KB `histb` arena → `panic: slice index out of bounds`.
Measured: protocol through P0 ≈ 62.8 KB (survives); P1 pushes past
65,536 (dies). The panic is in legacy code, present in the unrepaired
learner too (verified on `wb_dialogue_bin`: dies at ~63.9 KB).

Protocol adjustment (documented deviation): P0 was measured in the
standard single session (teaching + practice + P0 — fully compliant, all
24 episodes complete before the panic). P1 was measured in a fresh
session with the 5 teaching sessions re-sent (P1 depends only on teaching
+ scenario card; ~24 KB, safe). P1 is therefore a valid retrieval
measurement; it is not a single-session continuation. The 64 KB ceiling
itself is NOT repaired here — it belongs to the broad-repair wave per
Micah's orders.

## Red-team qualifications — recorded, not blocking

1. **Underdetermination / mixed-case:** D2 has no string-rule content; no hit.
2. **Confident overfit on sparse fits:** no confident wrong actions observed —
   the learner withholds ("I don't know.") rather than guessing. No hit.
3. **P1 ambiguity map:** P1 0/24 via withholding, not via ambiguous decomposition. No hit.
4. **Long-session history bypass still battery-scoped:** HIT — the 64 KB
   `histb` panic fires on the D2 protocol (see above). Referred to the
   broad-repair wave; documented here as a scope deviation, not a
   composition verdict.

## Determinism

P0: 3/3 byte-identical (`e5a109f8…`), incl. `MALLOC_PERTURB_=165`.
P1: 3/3 byte-identical (`6e5a338d…`), incl. `MALLOC_PERTURB_=165`.
Instrument rebuild: §10 gate matches the committed BUILD_LOG exactly.

## What this means in plain English

The repaired learner learned string rules (48/48 on the composition
retest). D2 asks a different question: can it learn *what to do* —
forage, build, shelter — from taught procedures and practice? It cannot,
on either the old or the repaired build. The repair added a string
workshop; D2 needs a policy workshop, which was never built. The battery
is therefore VOID for composition — again — and the honest conclusion is
unchanged: D2 does not test the repaired capability, and the repaired
capability does not touch D2.

## Files

- `d2_rerun_2026-09-28/VERDICT.md` (this file)
- `d2_rerun_2026-09-28/RUNLOG.md` — full run log
- `d2_rerun_2026-09-28/results_p0.json` (SHA `e5a109f8…`)
- `d2_rerun_2026-09-28/results_p1.json` (SHA `6e5a338d…`)
- `d2_rerun_2026-09-28/controls.txt` — re-measured control arms
- `d2_rerun_2026-09-28/DETERMINISM.md` — byte-identity manifest
- `d2_rerun_2026-09-28/harness/` — `p0_only.py`, `p1_only.py` (drivers),
  patched `drive_d2.py`/`score_d2.py`/`teaching.py` (paths only)
- `amendments/AMENDMENT_2026-09-28_D2-4_PROPOSED.md` — K1 chance redefinition
  (PROPOSED, pending Micah's signature)
