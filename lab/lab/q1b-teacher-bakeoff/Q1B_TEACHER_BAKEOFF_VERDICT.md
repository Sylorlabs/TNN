# Q1B VERDICT: Teacher bake-off — planted-teacher vs learned-teacher, head-to-head

**Date:** 2026-09-21 · **Branch:** `tnn-native-lab` · **Experiment:** `q1b-teacher-bakeoff/`
**Question (Micah):** Q1 proved a *planted* model teaches an unplanted model — but a *learned*
teacher was never tested. Is planted the best teacher, or does learned teach as well or better?
**Instruction:** run the experiment, don't discuss it. This sheet reports what ran.

## Plain-language verdict

**The learned teacher teaches exactly as well as the planted teacher — identical
scores on every slice, identical final learner state.** Planted is not the best
teacher; it is merely *a* teacher. What matters is that the teacher genuinely
holds the knowledge and the learner judges — not how the teacher acquired it.

- **Planted leg (control): 12/12 raw exact hits on all 8 slices** (96/96) —
  Q1 replicated byte-for-byte: the planted leg's learner and teacher state
  digests are identical to Q1's canonical run digests.
- **Learned leg: 12/12 raw exact hits on all 8 slices** (96/96) — every number
  identical to the planted leg, including the learner's final state digest
  (same bytes as Q1's learner digest: the learner ended in *exactly* the same
  knowledge state under both teachers).
- **The learned teacher is real:** a Track 5 arm-B learned-only TNN that acquired
  all 228 non-false Zharovia facts itself — 8-example scaffold verified by its
  own observation, learner-initiated SIGNAL_DISCONNECT, then self-directed
  deliberate learning from the world tapes (slot-scan discovery, 3-occurrence
  cross-verification, `t5_verify` + `t5_add`). Zero `t5_plant` calls in its
  construction (source-verified); the audit ledger proves it: 0 plants,
  228 deliberate adds, 1 disconnect.
- **The learned teacher's knowledge is strictly cleaner:** all 228 held claims
  are true (0 false claims). The planted teacher carries 12 deliberately false
  plants. On the flaw battery this changes nothing (the curriculum never
  teaches the false plants); on knowledge quality, learned wins.
- **Deterministic:** N=5 reruns byte-identical
  (`407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151` × 5).
  Zero RNG in any decision path (static scan clean).

## What actually ran

**Leg 0 — planted teacher (Q1 replication, tid=6).** `q1_teacher_build()`:
T5Store with 240 trainer-planted facts, learn-gate set. Same emissions as Q1
(frozen §B.3 §P wire, 24 clean proposals + frozen §B.7 flaw schedule per slice,
flaw-first). Control requirement: reproduce Q1's 12/12 — met, with
byte-identical end-state digests to Q1's canonical evidence.

**Leg 1 — learned teacher (tid=7, new registry value).**
`q1b_teacher.zag:q1b_learned_teacher_build()`: fresh T5Store (learn-gate
*open* — arm-B learns), fresh-audited by construction; the same 8-example
scaffold as the Q1 learner (directives verified by its own world observation,
never evidence); learner-initiated SIGNAL_DISCONNECT; then self-directed
learning over 9 world tapes (8 curriculum tapes of 24 facts + 1 extra tape of
28 — disjoint probe-id ranges covering all 228 non-false facts). Per tape the
teacher *discovers* records by slot-scan (given no fact list), hypothesizes
(fid,val) from the first occurrence, tests it against the other two
occurrences (disagreement kills — the eliminative gate is live code),
verifies via `t5_verify` over 3 independent tier-2 OBS legs, and deliberately
adds via `t5_add`. Build log: scaffold 8/8, then 24/24 × 8 tapes, 28/28 on the
extra tape. The teacher never touches `t5_truth` in its learning path (its
evidence is the world records); the truth-comparisons in the driver are
harness-side honesty checks, not teacher inputs.

**The learner (both legs, identical construction).** Fresh arm-B-style
learned-only TNN per leg: empty store at t0 (fresh-audited), 8-example
scaffold verified by its own observation, deliberate adds, learner-initiated
SIGNAL_DISCONNECT, then `q1_learn_one` §L deliberation per proposal —
unchanged from Q1. The learner is tid-agnostic (trust tier comes from
confidence, not teacher id); only the ledger's d1 field records 6 vs 7.

**Instrument (both legs, frozen).** The proven Track-B battery, copied from Q1
with three documented Q1B deltas: `TB_TID_LEARNED=7` registry value, `last7`
seq counter + ingress acceptance of tid 7, and a tid parameter threaded
through the emission functions. The flaw emissions are byte-identical across
legs except the teacher_id field — the instrument is frozen; the variable
under test is the teacher's acquisition history.

## Per-slice numbers (raw exact hits — the bar is judged on these)

Both legs, all 8 slices:

| slice | raw hits /12 | near | miss | score | pass | clean adopts | mastery /24 | tripwire | leak |
|-------|--------------|------|------|-------|------|--------------|--------------|----------|------|
| 0–7 (planted) | **12** | 0 | 0 | 120 | 1 | 20 | 24 | 0 | 0 |
| 0–7 (learned) | **12** | 0 | 0 | 120 | 1 | 20 | 24 | 0 | 0 |

(Full table in `evidence/per_slice.csv` — all 16 rows identical.)

Totals per leg: **96/96 raw hits**, 8/8 slices ≥10/12, 160 clean adoptions,
192/192 final mastery, 200 units in the learner's store, 0 check failures
(162/162 CL_CHECKs green across the whole binary, both legs), 0 tripwire
fires, 0 leaks.

Per-flaw behavior (both legs, all slices identical — 12/12 hits with 0
near-misses means expected verdict + expected reason on every flaw):
4 wrong-span → REVISE/SPAN_SHIFT; 4 false-confidence → REJECT/R1;
2 missing-grounding → REJECT/R1; 2 plausible-false → REJECT/R1.

## Knowledge-transfer numbers

| | planted teacher | learned teacher |
|---|---|---|
| facts held | 240 (228 true claims + 12 false plants) | 228 (228 true claims, 0 false) |
| acquisition | trainer `t5_plant` × 240, learn-gate set | scaffold + self-directed deliberate learning, 0 plants (audited) |
| holds curriculum (192 facts, true claims) | yes (checked) | yes (checked) |
| learned spans world-true (per-slice check) | n/a (planted spans) | 0 failures across 8 slices |
| learner facts recalled (final) | 192/192 | 192/192 |
| learner mastery per slice | 24/24 × 8 | 24/24 × 8 |
| learner clean adoptions | 160 | 160 |
| learner end-state digest | `6317c2dc…a3092467` | `6317c2dc…a3092467` (identical) |

## Answer to Micah's question

**Is planted the best teacher, or does learned teach as well or better?**
Learned teaches *as well as* planted — not better on the battery (the scores
are identical down to the learner's final bytes), but as well, and with
strictly cleaner knowledge (no false plants). Plantedness of the teacher is
not the bottleneck and not an advantage: Q1 showed the bottleneck is learner
judgment; Q1B shows the teacher's acquisition history doesn't move the needle
either, given a teacher that genuinely holds the knowledge and a learner that
judges. A TNN that learned everything itself is a fully capable teacher.

## Honest caveats (read before citing the headline)

1. **The flaw schedule is the instrument, not teacher behavior.** Both legs
   present the identical frozen §B.7 schedule (byte-identical except tid).
   The bake-off varies the teacher's knowledge-acquisition history, not its
   pedagogy — a learned teacher in the wild would not naturally emit flaw
   proposals. What the experiment proves: given the same curriculum, a
   learned teacher's knowledge transfers exactly as completely as a planted
   teacher's.
2. **The learner was built to judge** (same caveat as Q1): 12/12 is the
   ceiling for a judgment-capable learned-only TNN; Track B's 1/12 is the
   naive floor. The bake-off compares teachers holding the learner fixed.
3. **The learned teacher learned from the same world the learner later sees.**
   That is what "learned" means here — no answer key: the teacher's learning
   path never consults `t5_truth`; it reads world records and verifies across
   occurrences. The truth-comparisons are driver-side honesty checks.
4. **Teacher registry:** tid=7 (`TB_TID_LEARNED`) is a Q1B-local registry
   value, like Q1's tid=6 — not part of frozen §B.3. The wire format itself
   is unchanged.

## Reproducibility

- Source: `q1b-teacher-bakeoff/src/` (pure Zag; toolchain
  `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`). Q1B deltas vs Q1 are
  documented in-file: `TB_TID_LEARNED` (q1_types.zag), `last7` + ingress
  (q1_proposal.zag), tid-parameterized emissions (q1_world.zag); new files
  `q1b_teacher.zag` (learned-teacher construction) and `q1b_driver.zag`
  (both-leg driver). All other files are byte-copies of Q1's.
- Canonical output: `q1b-teacher-bakeoff/evidence/run1_stdout.txt`.
- Per-slice numbers: `q1b-teacher-bakeoff/evidence/per_slice.csv`.
- N=5 hashes: `q1b-teacher-bakeoff/evidence/n5_sha256.txt` (all identical).
- Run dirs `~/workspace/q1b_run{1..5}` hold the binaries + outputs (binaries
  NOT committed).
- Static scan: no RNG / wallclock / raw-syscall in any Q1B decision path.
- State digests in-run: planted leg matches Q1 exactly (learner
  `6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467`,
  teacher `6aee9aa2a962f8ef7d3259c5c145847fed4aec646a90a61c182bf1eb8f952816`);
  learned teacher `6f387ee3e6fddc7692d5138fd4c1106bd745f2ec0a837956196b07c3dee756b5`
  (228 all-true facts).
