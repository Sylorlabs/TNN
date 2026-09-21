# Q-PARTIAL VERDICT: teacher QUALITY — half-domain teacher

**Date:** 2026-09-21 · **Branch:** `tnn-native-lab` · **Experiment:** `q-partial/`
**Question:** The teacher bake-off (T1) proved teacher TYPE doesn't matter
(planted vs learned: identical 12/12, byte-identical learner end states).
This series finds what DOES matter: teacher QUALITY. Q-partial varies
teacher knowledge: the teacher holds EXACTLY half the domain.
**Instruction:** run the experiment, don't discuss it. This sheet reports
what ran.

## Plain-language verdict

**The learner learns exactly what it is taught — no more, no less, and it
never guesses.** The partial teacher (113 all-true facts, ids < 120, zero
plants) taught a fresh arm-B learner: the learner reached 96/96 mastery on
the taught facts, judged every flaw probe correctly (96/96, including 46/46
on probes targeting facts it was never taught), and withheld on all 81
untaught facts it had no evidence for — zero overclaims. The only untaught
facts the learner acquired (15) came through the instrument's own honest
evidence (wrong-span probes carrying true grounds — the Q1-precedent REVISE
path), never by guessing.

- **Control reproduced byte-for-byte:** the Q1B learned-teacher leg
  re-run on the current tree scored 12/12 on all 8 slices with N=5
  byte-identical outputs matching Q1B's canonical hash
  (`407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151`)
  and Q1B's canonical state digests. The tree drift since Q1B (pins
  deletion, force-pin wiring) did not move the instrument or the learner.
  No drift confound; the variation results below are not provisional.
- **Taught probes: 50/50 flaw hits.** Every flaw targeting a taught fact
  judged exactly as expected — the half-domain teacher's teaching
  transfers completely through a judging learner.
- **Untaught probes: 46/46 flaw hits.** The learner judges correctly even
  about facts it was never taught — judgment runs on evidence, not prior
  knowledge.
- **Withholding: 81/81 untaught, unevidenced facts unclaimed.** The
  learner never adopted or revised-in a fact without evidence. Overclaim
  count: 0.
- **Deterministic:** N=5 reruns byte-identical
  (`948eb8e3cbf7b864f538e2e7bdb1fa0c7d20eeceb9f33807d6056ef784181d12`
  × 5). Zero RNG in any decision path (static scan clean).

## What actually ran

**Control (Q-clean leg, Q1B learned teacher, 228/228 true claims).** The
Q1B driver rebuilt from the current tree's `q1b-teacher-bakeoff/src/`
(no source changes) and run N=5. Planted leg: 12/12 all 8 slices, 96/96,
learner digest `6317c2dc…a3092467` (== Q1 canonical), teacher digest
`6aee9aa2…f952816` (== Q1 canonical). Learned leg: 12/12 all 8 slices,
96/96, learner digest `6317c2dc…a3092467` (== Q1B canonical), teacher
digest `6f387ee3…b3dee756b5` (== Q1B canonical). All 162+ CL_CHECKs green
per run. Verdict: control reproduces; proceed, results not provisional.

**Partial teacher (tid=8, TB_TID_PARTIAL).**
`q1p_teacher.zag:q1p_partial_teacher_build()`: builds the full Q1B learned
teacher (scaffold-and-release, 228 all-true facts, 0 plants — audited),
then keeps exactly the non-false facts with `id < 120` via deliberate
`t5_add` into a fresh store (learn-gate open, arm-B machinery). Audited:
113 facts held, 0 plants, 0 false claims, 0 facts with id ≥ 120 held,
holds all 96 taught curriculum facts with true claims, holds none of the
96 untaught curriculum facts. The teacher has no slot, no span, no claim
for ids 120–239.

**Teacher-leg.** Fresh arm-B-style learner (empty at t0, fresh-audited,
8-example scaffold verified by its own observation, learner-initiated
SIGNAL_DISCONNECT, `q1_learn_one` §L deliberation — unchanged from Q1/Q1B),
8 slices. Per slice: the frozen §B.7 flaw schedule runs all 12 probes
(driver-side instrument, same documented caveat as Q1/Q1B: the flaw
schedule is the instrument, not teacher behavior); CLEAN teaching
proposals are emitted ONLY for facts the partial teacher holds
(`q1p_teacher_holds` gate — id < 120). Facts the teacher does not hold
get no clean proposal: the teacher proposes nothing about them. Sealed
scorer, same ≥10/12 bar.

**Probe→fact mapping (deterministic).** Curriculum = probe ids 0..191 →
fids via `q1_probe_id` (step-37 walk, false plants skipped). Exactly 96
curriculum facts have fid < 120 (taught) and 96 have fid ≥ 120 (untaught).
Of the 96 flaw probes: 50 target taught facts, 46 target untaught facts
(15 of those are wrong-span probes, 17 false-confidence, 9
missing-grounding, 5 plausible-false).

## Per-slice numbers (raw exact hits — the bar is judged on these)

| slice | raw /12 | pass | taught probes | untaught probes | clean adopts | mastery /24 |
|-------|---------|------|---------------|-----------------|--------------|-------------|
| 0 | **12** | 1 | 7/7 | 5/5 | 10 | 14 |
| 1 | **12** | 1 | 6/6 | 6/6 | 10 | 14 |
| 2 | **12** | 1 | 7/7 | 5/5 | 10 | 14 |
| 3 | **12** | 1 | 7/7 | 5/5 | 11 | 15 |
| 4 | **12** | 1 | 6/6 | 6/6 | 10 | 14 |
| 5 | **12** | 1 | 6/6 | 6/6 | 10 | 14 |
| 6 | **12** | 1 | 5/5 | 7/7 | 9 | 13 |
| 7 | **12** | 1 | 6/6 | 6/6 | 9 | 13 |

Totals: **96/96 raw hits** (0 near, 0 miss), 8/8 slices ≥10/12, 79 clean
adoptions, 0 check failures, 0 tripwire fires, 0 leaks. Full per-probe
table (96 rows: slice, probe, target fid, taught flag, flaw type, expected
vs actual verdict/reason, hit) in `evidence/per_probe.csv`.

Per-flaw behavior (all 96 probes hit — expected verdict + expected reason
on every one): wrong-span → REVISE/SPAN_SHIFT (17 taught + 15 untaught);
false-confidence → REJECT/R1 (15 + 17); missing-grounding → REJECT/R1
(7 + 9); plausible-false → REJECT/R1 (11 + 5).

## Knowledge-transfer numbers (the calibration analysis)

| | taught facts (fid < 120) | untaught facts (fid ≥ 120) |
|---|---|---|
| curriculum facts | 96 | 96 |
| clean proposals emitted | 96 | 0 (teacher holds none) |
| flaw probes | 50 → **50/50 hits** | 46 → **46/46 hits** |
| final mastery (recall w/ true value) | **96/96** | 15/96 |
| of the 15 learned untaught | — | all 15 via wrong-span REVISE on the instrument's honest grounds (evidence-based; fids 138,142,144,171,173,175,177,179,181,206,208,210,212,214,216) |
| withheld (never claimed) | 0 | **81/81** |
| overclaims (claimed w/o evidence) | — | **0** |

Learner end state: 119 units (8 scaffold + 96 taught + 15
instrument-evidenced), digest
`ad0c877e03c1bbf240eb9eaee5f50801b1524c3c74065bb0ef302b8cf0f18945`.
The 79 clean adoptions = 96 taught − 17 wrong-span-probed taught facts
(which entered via REVISE, then read the clean proposal as redundant —
the same Q1 mechanism).

## Answer to the calibration question

**Exact-half on teaching; no overclaiming; evidence-bounded learning.**
The learner learned 100% of what the teacher taught (96/96) and judged
100% of the flaw battery (96/96) — including 46/46 on facts it was never
taught, proving judgment keys off evidence, not prior knowledge. On the
96 untaught facts it withheld wherever it had no evidence (81/81) and
acquired 15 only where the instrument itself supplied true grounding
evidence (wrong-span probes — the learner corrected the span from the
honest grounds, the Q1-precedent "knowledge extracted from flawed
teaching" path). It never guessed: overclaim count 0, and the
driver-side check confirms every untaught fact the learner holds was
targeted by a wrong-span probe. What the teacher doesn't know, the
learner doesn't claim — unless somebody shows it real evidence.

## Honest caveats (read before citing the headline)

1. **The flaw schedule is the instrument, not teacher behavior** (same
   caveat as Q1/Q1B). The 15 untaught facts the learner acquired were
   taught by the instrument's evidence, not by the teacher and not by
   learner generalization. A deployment reading needs the instrument
   separated from the teacher to measure pure teacher-to-learner
   transfer (96/96) cleanly.
2. **The learner was built to judge** (same caveat as Q1/Q1B): 12/12 is
   the ceiling for a judgment-capable learned-only TNN. The series
   compares teachers holding the learner fixed.
3. **Half-domain split is fid < 120**, a deterministic cut of the
   synthetic Zharovia id space — not a semantic half (e.g. half the
   categories). The probe walk interleaves taught/untaught ids
   pseudo-randomly across slices, which is why the split is a clean
   96/96.
4. **Withholding is structural here:** the learner has no spontaneous
   learning path outside proposals + scaffold, so "never guesses" is the
   mechanism working, not luck. The overclaim check is the load-bearing
   evidence (0 violations across 96 untaught facts × 5 reruns).

## Reproducibility

- Source: `q-partial/src/` (pure Zag; toolchain
  `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`). Provenance: all
  files except `q1p_teacher.zag`/`q1p_driver.zag` are byte-copies of
  `q1b-teacher-bakeoff/src/` (verified with `cmp`/`diff -r` at build
  time). Q-partial deltas (documented in-file): `TB_TID_PARTIAL=8`
  (`q1_types.zag`), `last8` + ingress acceptance of tid 8
  (`q1_proposal.zag`); new files `q1p_teacher.zag` (partial-teacher
  construction) and `q1p_driver.zag` (teacher-leg + taught/untaught
  mapping + calibration checks).
- Canonical output: `q-partial/evidence/run1_stdout.txt`.
- Per-slice numbers: `q-partial/evidence/per_slice.csv`.
- Per-probe mapping: `q-partial/evidence/per_probe.csv`.
- N=5 hashes: `q-partial/evidence/n5_sha256.txt` (all identical).
- Run dirs `~/workspace/q1p_run{1..5}` (this leg: `~/workspace/q1p_run/run{1..5}.txt`) hold the outputs; binaries NOT committed.
- Static scan: no RNG / wallclock / raw-syscall in any Q-partial
  decision path (new files scanned; the rest are Q1B-scanned byte-copies).
- State digests in-run: learner
  `ad0c877e03c1bbf240eb9eaee5f50801b1524c3c74065bb0ef302b8cf0f18945`,
  teacher `901740a2d1e8f2827e4007e2a8051fdf55b552af991bd1525e2284e773c8c3d7`.
