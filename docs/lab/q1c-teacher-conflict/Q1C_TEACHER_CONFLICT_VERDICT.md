# Q1C — Teacher Self-Contradiction Leg — VERDICT

**Date:** 2026-09-21
**Leg:** Q1C (CREW TQ-CONFLICT), `tnn-lab/q1c-teacher-conflict/`
**Question:** When the teacher contradicts itself across passes — asserting the
true value in pass 1 and a plausible-false value in pass 2 for the same fact —
does the learner withhold, commit to one side, or flip-flop?
**Answer (by test, not opinion): the learner commits to the true side on all
17 contradicted facts, withholds on 0, and its end state is byte-identical to
the un-contradicted Q1B learned leg. The contradiction is detected and killed
17/17 by the eliminative verification; it leaves no trace.**

## 1. Control (prerequisite, current tree)

Pristine Q1B `q1b_driver.zag` rebuilt from the current tree and run N=5:
- Learned teacher: **12/12 on all 8 §B.7 slices**, 162/162 checks matched.
- Stdout SHA-256 (all 5 runs): `407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151`
  — byte-identical to Q1B's canonical evidence hash. **No tree drift.**
- Verdict: control reproduced; the Q1C experiment ran against a clean baseline.

## 2. Experimental setup (frozen-spec discipline)

- The conflicted teacher is built by the **unmodified** `q1b_learned_teacher_build`
  (scaffold-and-release; `q1b_teacher.zag` byte-identical to Q1B). Audit:
  228 units, 228 adds, 0 plants, 1 disconnect, **0 false stored claims**.
  Teacher digest `6f387ee3e6fddc7692d5138fd4c1106bd745f2ec0a837956196b07c3dee756b5`
  — identical to Q1B's learned-teacher digest.
- Conflict set (deterministic): `fid % 12 == 0` over the 228 held facts →
  **exactly 20 facts**: 0,12,24,36,48,60,72,84,96,108,120,132,144,156,168,180,192,204,216,228.
  (Independently verified: none of the 20 is a false-plant id.)
- False value: `base + ((truth − base + 1) % category_range)` — the same
  modular-successor construction as `t5_plant_claim`, so the false assertion is
  plausible (in-category) rather than absurd.
- Pass 1: Q1-pattern teaching, all-true assertions (frozen §B.7 flaw battery,
  sealed scorer). Pass 2: re-teach all 200 taught facts; the 17 taught
  conflicted facts are asserted FALSE, the other 183 asserted true.
- Of the 20 conflicted facts: 16 in the curriculum, 1 in the scaffold
  (fid 72), 3 never taught to the learner (fids 0, 36, 204 — probe indices
  200–227, the teacher's extra tape). The 17 taught ones all faced the
  contradiction in pass 2.

### Deltas vs Q1B (all in-file documented; full diffs in `evidence/delta_*.diff`)
1. `q1_types.zag`: `TB_TID_CONFLICTED=8`.
2. `q1_proposal.zag`: `TbSess.last8` + ingress accept for tid 8 (per-teacher
   seq tracking preserved).
3. `q1_world.zag`: aux[0] of the clean span carries the teacher's asserted
   claim as `(u64 fid, u64 value)` — a frozen §B.3 field previously unused.
   The Q1 wire format, span layout, and offsets are unchanged; flaw emissions
   now assert `(fid, t5_truth(fid))` (behavior-neutral: flaw paths don't ADOPT).
4. `q1_learner.zag`: the §L ADOPT branch reads the asserted claim; R5
   (redundant) applies only when the assertion matches the held claim.
   Otherwise the asserted claim and the independent world observation are
   treated as two evidence legs fed to `t5_verify` — a false assertion
   disagrees with the observation and is killed (REJECT/R1).
5. New: `q1c_teacher.zag` (conflict predicate, false-value constructor,
   `q1c_assert(fid,pass)`, `q1c_was_taught`), `q1c_driver.zag`.

The flaw battery, sealed scorer, tripwire, bar, and §P codec are byte-identical
to Q1B (verified by `cmp`).

## 3. Results

### 3a. Pass 1 — §B.7 flaw judgment on true teaching (unconflicted facts)

| slice | hits | nears | misses | FPs | score | pass | clean adopts | mastery |
|---|---|---|---|---|---|---|---|---|
| 0 | 12 | 0 | 0 | 0 | 120 | 1 | 20 | 24/24 |
| 1 | 12 | 0 | 0 | 0 | 120 | 1 | 20 | 24/24 |
| 2 | 12 | 0 | 0 | 0 | 120 | 1 | 20 | 24/24 |
| 3 | 12 | 0 | 0 | 0 | 120 | 1 | 20 | 24/24 |
| 4 | 12 | 0 | 0 | 0 | 120 | 1 | 20 | 24/24 |
| 5 | 12 | 0 | 0 | 0 | 120 | 1 | 20 | 24/24 |
| 6 | 12 | 0 | 0 | 0 | 120 | 1 | 20 | 24/24 |
| 7 | 12 | 0 | 0 | 0 | 120 | 1 | 20 | 24/24 |

Aggregate: **96/96 hits, 8/8 slices pass, 0 false positives, 160 clean
adoptions, tripwire silent on all tapes.** Flaw judgment on the conflicted
teacher's true pass is uncontaminated — the machinery self-tests
(`q1c_verify_kills_disagreement/accepts_agreement/kills_assertion_mismatch`)
prove the gates were live.

### 3b. Pass 2 — the contradiction (per-fact verdicts in `evidence/conflict_outcomes.csv`)

- **17/17** false assertions → **REJECT / R1_INSUFFICIENT**. The eliminative
  verification (teacher-asserted leg vs independent world-observation leg)
  detected every self-contradiction; none survived. 0 verdicts of any other
  kind.
- **183/183** unconflicted re-assertions → **REJECT / R5_REDUNDANT** (already
  known, assertion matches held claim). No state change, no contamination.

### 3c. Final disposition of the 20 conflicted facts

| group | n | withheld | commit true | commit false | flip-flop/other |
|---|---|---|---|---|---|
| taught + contradicted (16 curriculum + 1 scaffold) | 17 | **0** | **17** | 0 | 0 |
| never taught (fids 0, 36, 204) | 3 | 3 (trivially absent) | 0 | 0 | 0 |

The learner did **not** withhold on any contradicted fact. It kept the true
value it had adopted in pass 1 on all 17 — the false assertion was killed at
the gate (R1) and never entered the store. No false commitment, no flip-flop.

### 3d. Unconflicted mastery

**183/183** unconflicted taught facts held true after both passes. The
contradiction contaminated nothing.

### 3e. The headline digest

Learner end-state digest: `6317c2dcf17e850c6e1419f547a8723efdeeda3a9747baf5f8af019ba3092467`
— **byte-identical to Q1B's learned-leg learner digest.** The teacher's
self-contradiction left literally zero trace on the learner's knowledge state.

## 4. Determinism

- N=5 reruns, pure Zag, zero RNG (static token scan clean): stdout
  SHA-256 `5f81826a65a73aed7579f8d7dc4d663aa28b92ebca97c6310b70ff72b592532e`
  × 5 — byte-identical.
- `Q1C_COMPLETE`; **102/102 CL_CHECKs** matched (0 mismatches).

## 5. Verdict

**Q1C: PASS (by preregistered mechanics).** The arm-B-style learner handles a
self-contradicting teacher the way its eliminative design predicts: the first
(true) assertion is verified and adopted; the second (false) assertion
disagrees with the learner's independent world observation and is killed by
`t5_verify` (R1) before it can touch the store. There is no withholding
mechanism in this learner — and the test shows none is needed for this threat:
commit-to-true is the correct outcome, achieved 17/17, with the end state
provably identical to the never-contradicted baseline.

Caveats (documented, not hidden):
- This is the immediate (arm-B-style) learner. A learner that deferred judgment
  pending corroboration might withhold instead; that is a different architecture
  and was deliberately NOT built for this leg (no mechanism was added to force
  an expected result).
- The 3 never-taught conflicted facts are trivially "withheld" (absent); they
  never faced the teacher and carry no information about contradiction handling.
- 8 of the 96 flaw targets were conflicted facts; the flaw battery ran on them
  in pass 1 with true assertions and scored 12/12 on every slice regardless.

## 6. Evidence index (`evidence/`)

- `run1_stdout.txt` — canonical run (148 lines)
- `n5_sha256.txt` — N=5 byte-identical hashes
- `per_slice.csv` — §B.7 per-slice scores
- `conflict_outcomes.csv` — per-fact pass-2 verdicts (17 rows)
- `summary.txt` — machine-readable aggregates + 102/102 check count
- `delta_q1_{types,proposal,world,learner}.zag.diff` — the only 4 modified
  files vs Q1B (5 files byte-identical by `cmp`; `q1b_teacher.zag` unmodified)

**Commit:** (to be filled on commit to `tnn-native-lab`)
