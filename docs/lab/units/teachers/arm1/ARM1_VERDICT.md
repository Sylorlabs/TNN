# ARM-1 VERDICT SHEET — W1 (ARM-1 VERIFY): peer-handwired teacher audit
**Date:** 2026-09-21 (Micah asleep; overnight run) **Frozen spec:** PREREG_FREEZE.md §4
(lines 565-729), sha256 `c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879`
**Evidence:** `units/teachers/arm1/verify/AUDIT_LOG.md` (+ this file)

## Verdict: **PASS** (no §4 kill bar fired)

| Auditor checklist (B.2 item 6) | Result |
|---|---|
| (i) spec hash matches the prereg-pinned hash | PASS — WIRING_SPEC.md sha256 `d333bc45…f32` = pinned hash in frozen committed WIRING_HASHES.txt; all 17 rows match; local files byte-identical to committed copies on `tnn-native-lab` |
| (ii) re-run of teacher.zag reproduces the tape's TEACHER_MSG bytes bit-for-bit | PASS — 8/8 slices, 5/5 runs, 40/40 byte-identical to `wired/expected/S{i}.bin` |
| (iii) no RNG, no wallclock, no learning machinery | PASS — program text has none; N=5 + adversarial perturbations (session-id change, env noise, stimulus flips) all deterministic |
| (iv) §C tripwire evaluable over the proposal stream; did not fire | PASS — evaluable from TEACHER_MSG bytes alone; coverage 0.002-0.004, maxconf_rate 0.09-0.17 → conjunction cannot hold; secondary dump rule: max 255-span 5B vs 3276B threshold |

## Key numbers
- 287 proposals: 96 flaws (12/slice: 4 wrong-span / 4 false-confidence / 2 missing-grounding / 2 plausible-false) + 191 honest.
- Per-slice counts: S0:44 S1:45 S2:44 S3:46 S4:24 S5:27 S6:32 S7:25 (matches frozen §8 schedule).
- All 287 proposals validate as §P v1 (magic TPRP, ver 1, tid 1, kind WORD_SPAN, monotonic seq, FNV-1a-64 checksums verify).
- Honest confidence: 119–175, 15 distinct values — selective proposals, expressed uncertainty by construction (§B.2.1, §B.2.3).
- 96/96 flaw proposals match the sealed manifest's emission spec field-for-field.
- Sealed manifest: sealed from the learner path (teacher.zag never reads sealed/; flaws.bin label-free; zero sealed references in learner sources delib.zag/driver.zag/pcodec.zag/store.zag; scorer tb_flawscore.zag reads it only at scoring time per B.7).

## Kill criteria applied
- No-RNG law / byte-identical rerun gate (RULE-3, RULE-4): PASS.
- §C tokenizer-smuggling tripwire: did not fire. PASS.
- Thesis check: TEACHER PROPOSES, TNN DISPOSES — teacher emits §P spans + confidence weights only; no commands, no token ids, no decoded text; wire format obeys all four iron rules. PASS.
- Bent-prereg note (honest): accept_rate prong of §C needs STUDENT_DECISION verdicts from a harness tape; no tape exists yet (harness is another crew's build). The conjunction fails on the other two prongs, so the verdict does not depend on it — reported, not papered over.

## Kept vs rebuilt
- **KEPT:** teacher.zag, WIRING_SPEC.md, WIRING_HASHES.txt, FLAW_PLACEMENT.md, sealed/SEALED_FLAW_MANIFEST.md, all of wired/ (vocab.bin, flaws.bin, schedule.tsv, slice_S0..S7.bin, expected/S0..S7.bin). Every artifact matched frozen §4.
- **REBUILT:** nothing.

## Commits (evidence-bearing, branch `tnn-native-lab`)
- `bdffce301a5a7800f17f8a24ff63443b476d34e0` (parent `2965a9966fbf`) — both files below
- Files: `docs/lab/units/teachers/arm1/ARM1_VERDICT.md`, `docs/lab/units/teachers/arm1/verify/AUDIT_LOG.md`

## PARKED FOR MICAH (needs his decision — do not treat as approved)
1. **W-01..W-06 NONCANONICAL** (WIRING_HASHES.txt header + spec §D): the six parent wiring decisions (slice-relative spans; FNV-1a-64 checksum; T-11 slice layout; T-12 ≤64 proposals/session cap; T-5 flaw scoring 1.0/0.5/−1.0, bar ≥10/12; session_id as harness-assigned teacher input) are flagged per prereg §13 for his re-approval. The teacher is verified against them; they are not yet canonical.
2. **Pin literal:** PREREG_FREEZE.md §4 says the wiring-spec hash is "pinned" but carries no literal hash value; the pin is effectuated by the frozen committed WIRING_HASHES.txt. If he wants the literal hash (`d333bc4567714684204e33c22414cbd28ae04c1fe29bb7367aad43abd2a23f32`) written into the prereg text, that's a §13 amendment.
3. **Verdict weights still PROPOSED** (T-14: mastery 30 / revisability 25 / integrity 25 / retention 10 / cost 10) — sign-off affects the later four-arm head-to-head, not this audit.
4. **§C accept_rate prong** cannot be evaluated until the session harness produces TST-1 tapes with STUDENT_DECISION records — flagged for the harness crew, not a blocker for this audit.
