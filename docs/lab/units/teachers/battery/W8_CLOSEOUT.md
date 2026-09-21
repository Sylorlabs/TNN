# W8 CLOSEOUT — §M cost model (Track B)

Closeout worker: C1 (task `units/trackb_coordinator/tasks/TASK_C1.md`,
generated from PREREG_FREEZE.md lines 565-729,
sha256 `c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879`).
Groundwork inventoried: `units/teachers/battery/COST_VERDICT.md`,
`units/teachers/battery/verify_cost/`. No live harness edits were made;
read-only access to crew-owned files (`learner/pcodec.zag`) throughout.

**Binding spec:** frozen PREREG_FREEZE.md §4 (verbatim in TASK_C1.md §5).
No §13 amendment was needed or made.

## Verification outcome — PASS

**1. Branch-blob comparison (11/11 byte-identical).** Every local file
under `units/teachers/battery/verify_cost/` and
`units/teachers/battery/COST_VERDICT.md` was fetched as a git blob from the
`tnn-native-lab` branch (repo path `docs/lab/<rel>`) via `gh-api` and
SHA-256-compared against the local bytes. Result: 11 ok, 0 missing,
0 mismatched. Files: `COST_VERDICT.md`, `verify_cost/w8_cost.zag`,
`verify_cost/w8_session.zag`, `verify_cost/probe_xlate.zag`,
`verify_cost/cost_arm1.tape`, `verify_cost/cost_arm3.tape`,
`verify_cost/evidence/r1.tape`, `verify_cost/evidence/hashes.txt`,
`verify_cost/evidence/adv_hashes.txt`,
`verify_cost/evidence/adv_flip_1.tape`,
`verify_cost/evidence/adv_trunc_1.tape`.
Branch head at verification: `13eb05949cf7`.

**2. Determinism spot-verification — recomputed tape hashes match
evidence.** Local `sha256sum` of every evidence tape equals the claimed
values in `evidence/hashes.txt` / `evidence/adv_hashes.txt`:
- `cost_arm1.tape` = `405762605f0e57bedfdf5c01242e9710a2b04ecf7674a91451309d6b42e8562a`
  (matches `hashes.txt` r1–r5 lines and the hash printed in COST_VERDICT.md).
- `cost_arm3.tape` = `663b0ed85bae2409e49c2cc30a8badd4da085021ed7eeb27681159b246e49211`
  (matches COST_VERDICT.md).
- `evidence/r1.tape` = `405762605f0e57…8562a` (same as cost_arm1 — the
  N=5 determinism artifact).
- `evidence/adv_flip_1.tape` = `d957b424526755218991e1be009b23f1b202a3b9ced1245525e057e5d64edfff`
  and `evidence/adv_trunc_1.tape` =
  `33dc50153ed3b6240720f8c7a04b0d3f5914d4efeacf54a7f34acb701dd7705f`
  (both match `adv_hashes.txt`).

**3. Extractor re-run reproduces the COST_VERDICT.md table exactly.**
`w8_cost.zag` was rebuilt from the committed source with the frozen
toolchain flags (`--no-zagd --no-analyze --no-foreground-cache`) and run
over `cost_arm1.tape` (×3) and `cost_arm3.tape` (×2). Outputs
byte-identical across reruns, and every number matches the table:

| arm | A/R/J | weight2 | teacher_msgs | delib_steps | ledger | appeals | defers | per-word ×1000 |
|-----|-------|---------|--------------|-------------|--------|---------|--------|----------------|
| 1 (rerun) | 34/3/7 | 81 | 44 | 166 | 88 | 0 | 0 | 2172 / 1086 / 4098 / 0 / 0 — matches COST_VERDICT.md exactly |
| 3 (rerun) | 1/0/11 | 13 | 12 | 36 | 23 | 0 | 0 | 3538 / 1846 / 5538 / 0 / 0 — matches COST_VERDICT.md exactly |

`wall_ms_per_word=NA` everywhere (no wallclock in any tape; B.9
informational only — never scored). Build artifacts went to
`~/workspace/scratch_c1/` (not `/tmp`); no binaries committed.

## Kept vs rebuilt

- **KEPT everything.** All W8 artifacts — the frozen-§B.9 extractor
  (`w8_cost.zag`), the session driver (`w8_session.zag`), the debug probe
  (`probe_xlate.zag`), both evidence tapes, and the full `evidence/`
  directory — match their branch blobs byte-for-byte. Nothing was
  discarded, nothing was re-generated, and no source line was edited.
- **REBUILT nothing.** The only build was a scratch recompile of the
  committed `w8_cost.zag` to produce the verification numbers above.

## F1 — RESOLVED: the translation shim is no longer needed

W8's finding F1 was an interface mismatch: the learner crew's
`pcodec.zag` laid §P fields out in a draft wire layout
(kind u16@6 / teacher_id u64@8 / session_id u64@16 / seq u64@24), while
frozen §B.3 requires teacher_id u32@6 / session_id u64@10 / seq u64@18 /
kind u8@26. `w8_session.zag` worked around it with `w8_xlate`
(frozen-§B.3 → learner-layout, field-exact), and the PARKED item asked
which side changes.

**Which side moved: the learner.** W5's commit
`4a6d898c1e66` ("pcodec repaired to frozen §B.3", on the branch, verified
present) rebuilt `learner/pcodec.zag` to the frozen layout. Verified
directly from the branch copy (local file is byte-identical to the
branch blob, sha256
`3ac2e0869cb47b8051ba783c20d72bbc1247c211ad20c02e96eba133d335ff65`):
`p_encode` writes magic u32@0, version u16@4, teacher_id u32@6,
session_id u64@10, seq u64@18, kind u8@26, span_start u64@27,
span_end u64@35, aux_count u8@43, aux spans@44, ground_count u8@44+ac*16,
grounding, confidence u8, checksum u64 — the exact frozen §B.3 layout —
and `p_decode` reads and validates the same. (This independently
corroborates AGENTS.md ZNC-2026-09-21-011, which characterized the
draft-vs-frozen gap: it was an integration gap, not a compiler bug, and
it is now closed on the learner side.)

**Explicit answer on the shim: it is NOT needed for any new learner
session.** The learner now ingests frozen-§B.3 wires natively via
`p_decode`; the translation step `w8_xlate` is obsolete and should be
dropped (not merely kept) in any future session generator — there is no
longer a second layout to translate into. **The already-generated
evidence tapes are unaffected:** `w8_session` wrote the teacher's frozen
§B.3 bytes verbatim into the TEACHER_MSG records (B.4 replay rule) and
used the translated wire only for the in-memory deliberation call at
generation time. The §M accounting reads the tape, so W8's cost numbers
stand unchanged.

## Four-arm verdict — UNCHANGED: still BLOCKED for the same-slice comparison

Per the closeout task: the verdict on the four-arm same-slice cost
comparison **STAYS as W8 left it unless new evidence exists — no new
evidence exists.** The blocker was missing crew outputs (no arm-3/4/5
teacher implementations; no harness mastery), not the accounting, and
W8 deliberately built no stand-in teacher (that would be fabrication).
The independently-written W9 head-to-head verdict sheet
(`units/teachers/TRACKB_VERDICT.md`, committed by closeout worker C4)
corroborates this: "No same-slice arm pair exists." The §B.9 cost
*accounting* remains IMPLEMENTED AND VERIFIED; the §M comparison remains
BLOCKED. Not softened.

## PARKED FOR MICAH

1. **§M same-slice comparison blocked.** Cannot run until arm-3/4/5
   teacher implementations exist (or the requirement is amended via
   §13). W8's raw numbers (S0 vs demo slices, no mastery) must not be
   read as a ranking — mastery comes from the harness crew.
2. **F1 is resolved, no action needed.** Noted only: learner `pcodec.zag`
   now speaks frozen §B.3 (commit `4a6d898c1e66`); the `w8_xlate` shim is
   obsolete for future sessions and must not be reintroduced.
3. **Semantic reading of §4 "zero malformed/malicious adoption" is
   yours.** Wire level: PASS (bitflip/truncation halt at INTEGRITY 1007,
   byte-identical ×2 each). Semantic level: the real learner adopted 5/12
   of arm 1's flaw-injection proposals (wrong-span ×3, false-confidence
   ×2) and rejected 7/12. Kill-bar verdict on the semantic reading belongs
   to you (flawscore worker owns the correctness taxonomy).
4. **`STUDENT_DELIB` event type 13 is a W8 local extension** — frozen B.4
   requires deliberation records but no crew defined a type. Needs a
   frozen §13 amendment or a crew-owned type number before tapes
   interoperate.

## Commits

- Evidence pre-existed on `tnn-native-lab` (11/11 byte-verified).
- This closeout file: committed to `tnn-native-lab` via
  `~/workspace/commit_to_branch.py` (docs/lab/units/teachers/battery/W8_CLOSEOUT.md).
