# Arm 3 Variation A — Verdict

**Date:** 2026-09-21. **Artifact:** `teacher.zag` + `sp345.zag` + `tape345.zag`
(teacher_id=3), native binary built with
`znc_linux_x86_64_abed8aa1`. **Verdict: PASS.**

## What was built

A pure-Zag deliberative adaptive teacher. The full
(spec, stimulus cursor, session history) → proposal mapping lives in the
teacher binary: the script language has no proposal directives, so no proposal
content can originate outside it. Per-session fixed-size state only; no RNG,
no wallclock, logical ticks only.

Deliberative behaviors (all in-teacher, all covered by policy unit tests):
R1 appeals (same span, new grounding, ≤2 appeals, confidence −20/appeal);
R2/R5 mark the span dead and advance (+RETRACT on R2 when `seq+1 ≤ stim_len`);
REVISE takes the student's span as canonical and emits SAME_AS (+GROUP);
3 WORD_SPAN adoptions in a 64-byte region emit BOUNDARY+GROUP; DEFER retries
once with extra grounding then moves on; two consecutive session-final
rejections of a normalized span mark it dead; R3/R4/R6 mark dead immediately.

§P iron rules: every emitted proposal is encoded then re-decoded through the
hostile path (`sp_decode` + `sp_validate`) before touching the tape; any
self-violation halts with INTEGRITY (1000+V), exit V, zero TEACHER_MSG.

§C: the conservative **cumulative** monitor (coverage/accept/maxconf legs over
the whole session; immediate fire on confidence=255 covering >5% of stimulus).
Never weakened toward rolling-200, per explicit instruction.

## Evidence (all in `evidence/`; `evidence/verify_varA.log` is the full run)

`verify_varA.py` — 35 checks, 0 failures (`VERIFY,DONE,failures=0`):

- **V0** — 109 `test`-mode self-checks, 0 failures (ported §P battery:
  roundtrip/tamper/2× iron-rule suites; ported §C battery; policy unit tests
  against the real policy functions).
- **V1** — N=5 byte-identical runs on fixed stimulus + fixed history
  (tape bytes + stdout identical, sha `ca72d94fbb8d6e89…`).
- **V2** — 5 adversarial heap-fill patterns → 5/5 byte-identical tapes.
- **V3** — different decision histories ⇒ different proposal sequences
  (4 distinct digests; anti-canned-script proof).
- **V4** — 12 malformed-script cases: exact exits (12/13), INTEGRITY logged,
  zero TEACHER_MSG for the bad input; all tapes independently audited.
- **V4b** — 12 malformed-§P probe cases through the real hostile ingress
  gate (`probe <case> <tape>`): exact exit = violation code (1..10),
  INTEGRITY (1000+V) logged, zero TEACHER_MSG, `HALTED:VIOLATION` footer;
  all 12 probe tapes pass the independent auditor.
- **V5** — §C through the real TW: cumulative smuggle fires code 1 (halt at
  950/1000 covered bytes), vocab-dump fires code 2, 94%-coverage and
  half-revise controls stay quiet; honest large-span sessions never fire.
- **V6** — clean adopt/mixed/R1/R3 teaching sessions: exit 0, no INTEGRITY,
  auditor PASS.

`audit_varA.py` (independent, Python): TST-1 framing, sha256 chain, §P field
validation, seq monotonicity, decision↔proposal seq agreement, cumulative
tripwire replay — PASS on every session tape and every probe tape.

## Design notes / deviations

- **Struct-safety refactor (post-evidence):** the 11-field `Prop` (with two
  slice fields = 40 bytes of the 88-byte layout) was replaced by a 7-field
  `PropH` (scalars, 56 B) + 4-field `PropT` (counts + 2 slices, 48 B), both
  `_zag_malloc`'d with headroom and explicitly initialized, per ZNC-003/005/
  006/009/010. The codec signature is now
  `sp_encode(h,t)` / `sp_decode(buf,h,t)` / `sp_validate(h,t,…)`; the wire
  layout is byte-identical. All 109 self-tests and the full 35-check battery
  were re-run after the refactor — green.
- **`tw_decide` has no duplicate protection by design:** the session loop
  consumes the decision FIFO strictly once per emitted proposal (one D line
  per proposal; DECISIONS_EXHAUSTED halts; trailing D at END is malformed),
  so the one-decision-per-proposal invariant is structural, not bookkeeping.
  Cumulative accept-rate semantics hold without a 4096-entry decided table.
- **Bad-confidence is wire-unrepresentable** (confidence is u8 on the wire);
  it is covered at the Prop level (`vt.iron2.conf_300` ⇒ V_SPAN).
- **Documented deviation:** the §C monitor is the stricter cumulative
  variant, not the frozen spec's windowed reading. Kept cumulative per
  explicit instruction.

## Residual / future work

- The decision stream is scripted student behavior, not a live learner.
  Closing the loop with a live student is future work and does not change
  this spec.
- Commit hygiene: only text files are committed (`teacher_bin`, `*.tape`,
  `*.out`, `.zagd`/caches excluded). Files ≥96 KB go through
  `~/workspace/commit_big_files.py`.
