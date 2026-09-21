# Q1 VERDICT: Does a planted knowledge model teach an unplanted knowledge model?

**Date:** 2026-09-21 · **Branch:** `tnn-native-lab` · **Experiment:** `q1-planted-teaches/`
**Question (Micah):** *"does a planted knowledge model teach an unplanted knowledge model?"*
**Instruction:** run the experiment, don't discuss it. This sheet reports what ran.

## Plain-language verdict

**YES.** A planted model taught an unplanted model — completely, and the
unplanted model proved it wasn't just parroting.

The teacher was Track 5's arm-A machinery: 240 trainer-planted Zharovia
facts, learn-gate set, unable to learn or revise. The learner was a fresh
arm-B-style learned-only TNN: empty store at t0, an 8-example scaffold it
verified itself, a learner-initiated disconnect, then deliberate learning
from the teacher's proposals.

Results:

- **Flaw battery: 12/12 raw exact hits on all 8 slices** (96/96 total) —
  expected verdict + expected reason on every flaw, scored by the sealed
  Track-B flaw scorer. Bar was ≥10/12 per slice. Every slice cleared it.
- **Track B arm-1 (the naive learner) scored [0,0,0,0,0,1,0,0], best 1/12.**
  The Q1 learner beats it 12-to-1 on every slice.
- **Knowledge transferred: 192/192 facts**, every one recalled with its true
  value at the end; 24/24 mastery in every slice; 20 clean adoptions per
  slice (the other 4 facts per slice entered via REVISE — corrected out of
  *flawed* teaching, which is teaching working, not failing).
- **No leakage, no tripwire:** the sealed flaw manifest was never visible to
  the learner (leak check 0/8 slices); the §C tokenizer-smuggling tripwire
  never fired (0/8).
- **Deterministic:** N=5 reruns byte-identical
  (`bfaf536c1a2d3792d39c9fce5a24bd0005f6865e702c66f2695e9c54ca2fe3ca` × 5).
  Zero RNG in any decision path (static scan clean).

The bottleneck is learner judgment, not the plantedness of the teacher.
Track B's arm-1 showed a naive learner absorbs flaws (1/12). Q1 shows a
learner with eliminative judgment absorbs the knowledge and rejects the
flaws (12/12) — from the *same planted teacher machinery*.

## What actually ran

**Teacher (planted model).** `q1_world.zag:q1_teacher_build()` — a T5Store
with all 240 facts planted by the trainer (`t5_plant`), learn-gate set
(constitution-side). It holds 12 deliberately false plants (verified:
`t5_plant_claim(29) != t5_truth(29)`); the curriculum never teaches them.
It emits frozen §B.3 §P proposal bytes (`teacher_id=6`, new registry value
— it is none of B.1's arms 1–5, and labeling it arm 1 would be dishonest).
Per slice: 24 clean teaching proposals (true span, 2 true grounding
occurrences, honest confidence 200 — selective proposals with expressed
uncertainty, §B.2.3) + the frozen §B.7 flaw schedule, flaw-first.

**World.** Deterministic Zharovia-record stimulus tapes: 2048 bytes,
16-aligned 8-byte records `[u32 fact_id][u32 value=t5_truth]`, 3 occurrences
per fact, placement a lawful function of (slice, ids). The learner's world
checks (alignment, bounds, decode) are its own observations.

**Learner (unplanted model).** `q1_learner.zag` — fresh T5Store (empty at t0,
fresh-audited: n==0 and no fact id present), 8-example scaffold verified by
its own observation (directives never enter evidence), deliberate adds via
`t5_verify` + `t5_add`, learner-initiated `SIGNAL_DISCONNECT` (audited),
then §L deliberation per proposal: world-validity test, teacher-evidence
test (grounding validity/consistency, confidence honesty), eliminate, weigh,
decide — ADOPT / REVISE/SPAN_SHIFT / REJECT/R1 / REJECT/R5. The learner never
sees the flaw manifest (driver-side only, instantiated after each session).

**Instrument.** The proven Track-B battery, copied verbatim: §P codec +
ingress gate (`q1_proposal.zag`), TST-1 tape + 16-word audit ledger
(`q1_tape.zag`), §C tripwire (`q1_tripwire.zag`), sealed flaw scorer
(`q1_flawscore.zag`). One documented delta: the ingress gate accepts
teacher_id 6 with its own seq counter; wire format unchanged.

## Per-slice numbers (raw exact hits — the bar is judged on these)

| slice | raw hits /12 | near | miss | score | pass | clean adopts | mastery /24 | tripwire | leak |
|-------|--------------|------|------|-------|------|--------------|--------------|----------|------|
| 0 | **12** | 0 | 0 | 120 | 1 | 20 | 24 | 0 | 0 |
| 1 | **12** | 0 | 0 | 120 | 1 | 20 | 24 | 0 | 0 |
| 2 | **12** | 0 | 0 | 120 | 1 | 20 | 24 | 0 | 0 |
| 3 | **12** | 0 | 0 | 120 | 1 | 20 | 24 | 0 | 0 |
| 4 | **12** | 0 | 0 | 120 | 1 | 20 | 24 | 0 | 0 |
| 5 | **12** | 0 | 0 | 120 | 1 | 20 | 24 | 0 | 0 |
| 6 | **12** | 0 | 0 | 120 | 1 | 20 | 24 | 0 | 0 |
| 7 | **12** | 0 | 0 | 120 | 1 | 20 | 24 | 0 | 0 |

Totals: **96/96 raw hits**, 8/8 slices ≥10/12, 160 clean adoptions,
192/192 final mastery, 200 units in the learner's store (8 scaffold + 192
taught), 0 check failures (76/76 CL_CHECKs green across the run).

Per-flaw behavior (all 8 slices identical): 4 wrong-span → REVISE/SPAN_SHIFT
(the learner found the true span via the teacher's honest grounds and
entered the corrected unit — knowledge extracted from flawed teaching);
4 false-confidence → REJECT/R1 (confidence 255 with missing/contradictory
grounding distrusted); 2 missing-grounding → REJECT/R1 (zero teacher
evidence shown); 2 plausible-false → REJECT/R1 (the world holds no such
record — checked, not assumed).

## Direct comparison with Track B arm 1

| | Track B arm-1 learner | Q1 learner (this experiment) |
|---|---|---|
| teacher | arm 1 (peer) | planted model (Track 5 arm-A machinery) |
| slices | 8 | 8 |
| flaw hits per slice | 0,0,0,0,0,1,0,0 | 12,12,12,12,12,12,12,12 |
| best slice | 1/12 | 12/12 |
| bar ≥10/12 | 0/8 slices | **8/8 slices** |
| failure mode | adopted wrong spans; confidence 255 overrode checks | none observed |

Source for Track B: `units/teachers/TRACKB_VERDICT.md` (2026-09-21).

## Honest caveats (read before citing the headline)

1. **Synthetic slices, real instrument.** The 8 slices are synthetic
   Zharovia-record corpora, not Track B's 8 text slices. This is deliberate:
   the planted teacher holds Zharovia facts, and a teacher can only teach
   what it holds. The §B.7 instrument is unchanged — same 4/4/2/2 flaw
   classes, same constructions (shifted spans, confidence-255,
   zero-grounding, absent units), same expected verdicts/reasons, same
   ≥10/12 bar, same sealed scorer code.
2. **Flaw-first ordering.** Within each slice the 12 flaws come before the
   clean teaching of the same facts, so the flaw battery is zero-shot. Side
   effect: the 4 wrong-span facts enter via REVISE, so clean ADOPTs read
   20/slice rather than 24 — all 24 facts are still learned per slice.
3. **The learner was built to judge.** The §L deliberation was designed with
   knowledge of the flaw taxonomy (the task required §L
   adopt/revise/reject/defer). So 12/12 is the *ceiling* for a
   judgment-capable learned-only TNN, not the floor — Track B's 1/12 is the
   naive floor. The mechanisms are general (world-validity, evidence
   validity, confidence honesty — no flaw-label lookup; the learner never
   sees flaw types), but the taxonomy shaped the tests. What the experiment
   proves: planted knowledge transfers completely to an unplanted substrate
   *when the learner judges*; it does not prove a naive learner would pass.
4. **Trust mapping.** The teacher is treated as a known tier-2 evidence
   source in `t5_verify` (recorded tier by confidence); the learner's own
   world observation is the independent tier-2 leg, and disagreement kills
   (proven live: disagreeing legs → 0). The teacher's word alone never
   suffices — every adoption/revision required the learner's own
   world-check to agree.

## Reproducibility

- Source: `q1-planted-teaches/src/` (pure Zag; toolchain
  `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
- Canonical output: `q1-planted-teaches/evidence/run1_stdout.txt`.
- Per-slice numbers: `q1-planted-teaches/evidence/per_slice.csv`.
- N=5 hashes: `q1-planted-teaches/evidence/n5_sha256.txt` (all identical).
- Run dirs `~/workspace/q1_run{1..5}` hold the binaries + outputs (binaries
  NOT committed).
- Static scan: no RNG / wallclock / raw-syscall in any Q1 decision path;
  substrate checked too.
- State digests in-run: learner
  `6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467`,
  teacher `6aee9aa2a962f8ef7d3259c5c145847fed4aec646a90a61c182bf1eb8f952816`.

## Answer to Micah's question

**Does a planted knowledge model teach an unplanted knowledge model?**
Yes — 192/192 facts transferred, 96/96 flaw judgments exact, 8/8 slices
over the bar, zero leakage, byte-identical ×5. The planted teacher's
knowledge is fully teachable; whether the student learns well depends on
the student's judgment, not on the teacher being planted.
