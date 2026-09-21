# COST VERDICT — Track B, worker W8 (§M cost model)

**Verdict: BLOCKED** for the four-arm same-slice cost comparison.
The frozen §B.9 cost *accounting* itself is **IMPLEMENTED AND VERIFIED**
(pure-Zag extractor, cross-checked, deterministic). What blocks §M is
missing crew outputs, not the accounting.

Task authority: `units/trackb_coordinator/tasks/TASK_W8.md`
(SHA-256 `c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879`),
plus the coordinator's 2026-09-21 correction (§B.3: only `aux_count` is
zero for WORD_SPAN/BOUNDARY/RETRACT; `ground_count` is unrestricted
usage-example evidence spans).

## What was built (all pure Zag, no RNG, no wallclock)

- `verify_cost/w8_cost.zag` — the frozen §B.9 extractor. Reads a session
  tape and computes, per effective word (ADOPT + REVISE + 0.5×REJECT):
  `ledger_entries_per_word`, `teacher_msgs_per_word`
  (TEACHER_MSG+HINT+ORACLE_ANSWER), `student_deliberation_steps`,
  `appeals_per_word`, `deferrals_per_word`, `wall_ms_per_word`
  (informational, always NA — tapes carry no wallclock, and B.9 never
  scores it). Words use the LAST verdict per proposal seq; every
  verdict=DEFER record counts as one deferral. Ledger entries =
  max decision ledger index + 1 (append-only learner audit ledger).
- `verify_cost/w8_session.zag` — integrated session driver: runs the real
  naive learner (`learner/delib.zag`) over concatenated frozen-§B.3 §P
  wires and emits a fixture-framed TST-1 tape with genuine STUDENT_DELIB
  (local event type 13 — fixtures345 omitted the type despite frozen B.4
  requiring it; documented extension) and STUDENT_DECISION records,
  SHA-256 event chaining, DEFER re-presentation up to the §L bound.
- `verify_cost/probe_xlate.zag` — debug probe from the interface-mismatch
  investigation (kept as evidence).

## Measured costs (raw, from tape — NOT same-slice, see Blockers)

| arm | slice | session | words A/R/J | weight2 | teacher_msgs | delib_steps | ledger | appeals | defers | per-word ×1000 (ledger/teacher/delib/appeals/defers) | mastery |
|-----|-------|---------|-------------|---------|--------------|-------------|--------|---------|--------|------------------------------------------------------|---------|
| 1 (real teacher+learner) | S0 65536 B | OK, no integrity events | 34/3/7 | 81 | 44 | 166 | 88 | 0 | 0 | 2172 / 1086 / 4098 / 0 / 0 | UNAVAILABLE (harness crew) |
| 3 (fixture wires, real learner) | demo 123 B | OK, no integrity events | 1/0/11 | 13 | 12 | 36 | 23 | 0 | 0 | 3538 / 1846 / 5538 / 0 / 0 | UNAVAILABLE |
| 4 (fixture HINTs only) | demo | teacher_msgs=16 | 0/0/0 | 0 | 16 | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | NA (no decided words) | UNAVAILABLE |
| 5 (fixture ORACLE only) | demo | teacher_msgs=32 | 0/0/0 | 0 | 32 | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | UNAVAILABLE | NA (no decided words) | UNAVAILABLE |

wall_ms_per_word: NA everywhere (no wallclock in any tape; B.9 informational only).

**Do not read this as a ranking.** The slices differ (S0 vs demo) and
arms 4/5 have no student-side mechanism at all. A cheap arm teaching
nothing wins nothing — mastery (harness crew) must sit beside these
numbers before any comparison is drawn, and the same-slice comparison
is BLOCKED (below).

Evidence tapes: `verify_cost/cost_arm1.tape`
(`405762605f0e57bedfdf5c01242e9710a2b04ecf7674a91451309d6b42e8562a`),
`verify_cost/cost_arm3.tape`
(`663b0ed85bae2409e49c2cc30a8badd4da085021ed7eeb27681159b246e49211`).

## Determinism

- N=5 arm-1/S0 sessions: byte-identical,
  `405762605f0e57…8562a` (`verify_cost/evidence/hashes.txt`, `r1.tape`).
- Adversarial bitflip in a proposal → INTEGRITY 1007 halt, byte-identical
  ×2 (`d957b424…d64edfff`, `evidence/adv_flip_1.tape`).
- Adversarial truncation → INTEGRITY 1007 halt, byte-identical ×2
  (`33dc5015…01dd7705f`, `evidence/adv_trunc_1.tape`).
- Extractor: byte-identical output on repeat runs; every number
  cross-checked against an independent Python tape parse — all match.

## §4 kill-bar status (applied honestly)

1. **Taught acceleration claim** — UNAVAILABLE. Needs a timed
   taught-vs-untaught A/B; no such data exists in W8 scope. Not bent.
2. **Disconnect post-scaffold M1 ≥ 99.5%** — UNAVAILABLE. Mastery is the
   harness crew's measurement; no disconnect eval has been run on these
   sessions.
3. **Zero malformed/malicious adoption** — wire level: PASS. Bitflip and
   truncation attacks halt deterministically (INTEGRITY 1007); no malformed
   wire was ever deliberated, let alone adopted. Semantic level (arm-1
   teacher's own flaw-injection schedule, 12 flaws): the real learner
   adopted 5/12 (wrong-span ×3, false-confidence ×2) and rejected 7/12
   (incl. both plausible-false). Whether flaw adoption counts as
   "malicious adoption" under §4 is not W8's call — reported as fact for
   the flawscore worker / Micah.
4. **BPE-smuggling must trip** — PASS, with real-learner evidence. The
   200× conf-255 smuggle fixture was run through the real learner: the
   learner's §C tripwire fired on proposal seq 0 (conf=255 covering >5%
   of the 24-byte stimulus → immediate trip), the session halted, and
   nothing was adopted.

## Kept vs rebuilt

- **KEPT**: `battery/tb_scorer.zag` as downstream scorecard infrastructure.
  It consumes already-normalized component ratios; it does not extract
  frozen §B.9 raw counts from tapes, so it cannot serve as the §M source
  of truth — kept as-is, untouched.
- **REBUILT**: raw tape-derived cost accounting (`w8_cost.zag`) — did not
  exist.
- **NEW**: integrated session driver (`w8_session.zag`) — no crew had run
  the real learner over §P wires end-to-end into a TST-1 tape.

## Findings (for the coordinator)

- **F1 — interface mismatch**: the learner crew's `pcodec.zag` lays §P
  fields out differently from frozen §B.3 (kind u16@6 / teacher_id u64@8
  vs kind u8@26 / teacher_id u32@6). The fields are identical, so
  `w8_session` translates field-exact and keeps the teacher's frozen bytes
  verbatim on tape (B.4 replay rule). The learner cannot ingest any
  frozen-§B.3 wire without translation — learner crew / harness repair
  should resolve which side moves.
- **F2 — fixture decisions are synthetic**: `fixtures345` STUDENT_DECISION
  records are fixture-supplied, not learner outputs. Real learner verdicts
  differ sharply (demo tape: fixture claimed ADOPT×6/REVISE×2/REJECT×3;
  real learner: REJECT×11, ADOPT×1 for the RETRACT). Fixture tapes are
  parser calibration only — never headline evidence.
- **F3 — missing STUDENT_DELIB type**: frozen B.4 requires deliberation
  records; `fixtures345` defines no such event type. W8 uses local type 13.
- **F4 — no arm-3/4/5 teachers exist**: arm 3's only proposals are 12
  hand-made fixture wires on the 123-byte demo slice (`sp345.zag` is a
  codec, not a teacher); arms 4/5 are 16 HINT / 32 ORACLE_ANSWER fixture
  events with no teacher implementation and no learner-side HINT/ORACLE
  mechanism. Arm 1's teacher is wired to 64 KiB slices S0–S7 and cannot run
  the demo slice without re-wiring its flaw schedule. **There is no
  curriculum slice on which all four arms have teacher output — the
  same-slice comparison in §M is BLOCKED until crews deliver.**
- **F5 — self-caught framing bug**: my first `w8_wire_len`/`w8_xlate`
  read `ground_count` at fixed offset 44; frozen §B.3 places it after the
  aux spans (variable offset). The probe caught it (seq-8 demo proposal,
  aux=2); fixed, both sessions re-run clean, arm-1 output byte-identical
  to the pre-fix runs (all its proposals have aux=0, unaffected).

## PARKED FOR MICAH

1. §M's four-arm same-slice comparison cannot run until arm-3/4/5 teacher
   implementations exist (or the requirement is amended). No
   W8-invented stand-in teacher was built — that would be fabrication.
2. Learner `pcodec.zag` vs frozen §B.3 wire-layout mismatch (F1): which
   side changes? Until resolved, every learner session needs the
   documented translation shim.
3. Semantic reading of §4 "zero malformed/malicious adoption": the real
   learner adopted 5/12 of arm 1's flaw-injection proposals. Kill-bar
   verdict on the semantic reading is yours (flawscore worker owns the
   correctness taxonomy).
4. `STUDENT_DELIB` event type 13 is a W8 local extension — needs a frozen
   amendment or a crew-owned type number if tapes are to interoperate.
