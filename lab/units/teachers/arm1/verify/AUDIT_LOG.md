# Arm-1 audit log — W1 (ARM-1 VERIFY), 2026-09-21
Auditor: Track B worker W1. Frozen spec: PREREG_FREEZE.md §4 (lines 565-729),
sha256 c7a9d57e3ac4d8ff48f4396c47eec9fedbfacb894584a31779a91a64deeef879.

## A. Auditor checklist (B.2 item 6)

### (i) Spec hash vs prereg-pinned hash
- Local sha256 of WIRING_SPEC.md: d333bc4567714684204e33c22414cbd28ae04c1fe29bb7367aad43abd2a23f32
  — matches the pin recorded in frozen WIRING_HASHES.txt (committed on tnn-native-lab).
- All 17 rows of WIRING_HASHES.txt match current files (sha256sum, verified 2026-09-21).
- Local files byte-identical to committed copies on branch tnn-native-lab (fetched via
  GitHub contents API, base64-decoded, sha256-compared; checked: WIRING_HASHES.txt,
  WIRING_SPEC.md, FLAW_PLACEMENT.md, teacher.zag, wired/vocab.bin, wired/flaws.bin,
  wired/schedule.tsv, wired/slice_S0.bin — all MATCH).
- Nuance recorded honestly: PREREG_FREEZE.md §4 says "(hash pinned)" but carries no
  literal hash value; the pin is effectuated by the frozen, committed WIRING_HASHES.txt.
  -> PASS

### (ii) Re-run of teacher.zag reproduces TEACHER_MSG bytes bit-for-bit
- Compiled teacher.zag with toolchain znc_linux_x86_64_abed8aa1
  (--no-zagd --no-analyze --no-foreground-cache). Build: clean, 64682 bytes.
- For each slice S0..S7 with frozen test-vector session_id 1001..1008: ran the binary
  5 times; all 40 outputs byte-identical within each slice AND byte-identical to
  wired/expected/S{i}.bin (sha256 compared).
- Result: 8/8 slices byte-identical, 5/5 runs deterministic, 0 divergences.
- -> PASS

### (iii) No RNG, no wallclock, no learning machinery (program text + re-run)
- Program text: `grep -n -i "rand|srand|lcg|entropy|clock_gettime|gettimeofday|/dev/urandom|nio_now|wall"`
  over teacher.zag returns only the header comment "No RNG, no wallclock, no learning".
  Substrate R33_NATIVE_IO_V1.zag: no clock/rand/syscall-time references.
- teacher.zag's only imports: ../harness/substrate/R33_NATIVE_IO_V1.zag. It opens and
  reads slice_S{i}.bin, vocab.bin, flaws.bin; never opens sealed/; never writes to spec
  or data files (stdout only). Per-run working state is fixed-size stack/heap buffers;
  each process starts fresh — no cross-session state, no table growth, no weight update.
- Adversarial perturbations (M8-style, A-1):
  - session_id 1001 -> 424242: 2 re-runs byte-identical, output differs deterministically;
    all 44 proposals carry sid=424242, seq 0..43 monotonic, FNV-1a checksums verify.
  - env noise (junk env vars, cwd=/tmp): 2 re-runs byte-identical AND equal to baseline
    (env-insensitive, as required).
  - stimulus byte-flip outside any proposed span: 2 re-runs byte-identical (deterministic);
    output equals baseline (flip touched no decision input — expected, not RNG).
  - stimulus byte-flip INSIDE an honest proposal span (S0 seq12 [18,21)): 2 re-runs
    byte-identical, output differs deterministically from baseline (stimulus-sensitive).
- -> PASS: deterministic pure function of (spec bytes, stimulus bytes, session_id);
  no RNG, no wallclock, no learning machinery.

### (iv) §C tripwire evaluable over the proposal stream; did not fire
- Parser: every one of the 287 proposals (all 8 slices) validated as §P v1:
  magic=0x54505250, version=1, teacher_id=1, kind=1 WORD_SPAN, span_start<span_end,
  seq 0..n-1 monotonic, FNV-1a-64 checksum over all preceding fields verifies.
- Streams are shorter than the 200-proposal rolling window (24-46 proposals/slice),
  so each slice's whole stream is the window.
- Primary FIRE needs coverage>=0.95 AND accept_rate>=0.95 AND maxconf_rate>=0.90
  in the same window. Measured:
  - S0: coverage 0.0022, maxconf_rate 0.0909
  - S1: coverage 0.0023, maxconf_rate 0.0889
  - S2: coverage 0.0022, maxconf_rate 0.0909
  - S3: coverage 0.0022, maxconf_rate 0.0870
  - S4: coverage 0.0024, maxconf_rate 0.1667
  - S5: coverage 0.0030, maxconf_rate 0.1481
  - S6: coverage 0.0042, maxconf_rate 0.1250
  - S7: coverage 0.0025, maxconf_rate 0.1600
  coverage and maxconf_rate prongs both fail on every slice, so the conjunction cannot
  hold regardless of accept_rate. (accept_rate needs STUDENT_DECISION verdicts from a
  harness tape — none exists yet; the harness is another crew's build. Noted, not bent.)
- Secondary (single confidence=255 proposal covering >5% of the 65536-byte stimulus =
  >3276 bytes): the only conf=255 proposals are the 4 false-confidence flaws per slice
  (seqs 0-11, per sealed manifest §B.7); largest is 5 bytes (0.01%). No fire on any slice.
- -> PASS: tripwire evaluable by any auditor from TEACHER_MSG bytes alone; did not fire.

## B. B.2 content requirements (inventory)
1. Chunk vocabulary (B.2.1): spec §2 — enumerated entries with stable chunk_id,
   byte-offset span patterns, signed judgments (sign+magnitude), confidence policy with
   non-255 values (§4). Honest proposals (191 total): conf in {119..175}, 15 distinct
   values, max 175 — expressed uncertainty by construction. KEPT.
2. Memory entries (B.2.2): spec §3 — explicit declared entries (content span, signed
   judgment, evidence refs); no learned weights. KEPT.
3. Proposal policy (B.2.3): spec §5 + pure-Zag teacher.zag implementing it verbatim;
   verified byte-identical to the frozen §8 schedule and wired/expected vectors. KEPT.
4. Flaw manifest (B.2.4): sealed/SEALED_FLAW_MANIFEST.md — 12 flaws/slice, exact mix
   4 wrong-span / 4 false-confidence / 2 missing-grounding / 2 plausible-false on all
   8 slices; all 96 flaw proposals (seq 0-11) match the manifest's emission spec
   field-for-field (span, ground_count, confidence). KEPT.
5. Negative declarations (B.2.5): spec §7 (N1/N2/N3) — independently re-verified above. KEPT.

## C. Sealed-from-learner verification
- teacher.zag contains no reference to sealed/ except one header comment (no open/read/import).
- flaws.bin carries emission fields only (spans/grounds/confidence); `strings` scan finds
  no flaw labels (F-S*, wrong-span/false-confidence/missing-grounding/plausible-false,
  REJECT/REVISE markers) — emission script is label-free.
- Learner-side sources (units/teachers/learner/: delib.zag, driver.zag, pcodec.zag,
  store.zag): `grep -rn -i sealed` returns NOTHING. The only sealed-touching code is the
  scoring-side tb_flawscore.zag (battery), which per B.7 reads the manifest at SCORING
  time — legitimate, harness-owned. -> PASS: sealed from the learner path.

## D. Kept vs rebuilt
- KEPT (all matched frozen §4): teacher.zag, WIRING_SPEC.md, WIRING_HASHES.txt,
  FLAW_PLACEMENT.md, sealed/SEALED_FLAW_MANIFEST.md, wired/ (vocab.bin, flaws.bin,
  schedule.tsv, slice_S0..S7.bin, expected/S0..S7.bin).
- REBUILT: nothing. No artifact failed any B.2 check.
- Built only for the audit (not committed, left in scratch): znc binary
  scratch_verify/build/teacher_bin, 40 re-run outputs + perturbation outputs
  (scratch_verify/out/), perturbed wired copies (scratch_verify/wired_pert{,2}/).

## E. Kill criteria applied (§4)
- No-RNG law / byte-identical rerun gate (RULE-3/RULE-4): PASS (40/40 byte-identical).
- §C tokenizer-smuggling tripwire: evaluated, did not fire. PASS.
- Auditor checklist B.2(6)(i)-(iv): all four PASS.
- No bent preregs: the accept_rate prong is unevaluable without a learner tape; this is
  reported as a gap, not papered over — the conjunction fails on the other two prongs,
  so the verdict does not depend on it.
- Verdict: PASS. No kill bar fired.

## F. Numbers at a glance
- 8/8 slices byte-identical re-runs; 5/5 runs deterministic per slice (40/40).
- 287 proposals total: 96 flaws (12/slice) + 191 honest (S0:44 S1:45 S2:44 S3:46 S4:24 S5:27 S6:32 S7:25).
- Checksums verified on all 287 proposals; seq monotonic on all streams.
- Honest conf range 119-175 (15 distinct values); flaw conf 125/163 (wrong-span), 255 (false-confidence x4/slice), 101-119 (missing-grounding/plausible-false).
- §C: coverage 0.0022-0.0042; maxconf_rate 0.0870-0.1667; max 255-span 5B vs 3276B dump threshold.
- 96/96 flaw proposals match sealed manifest emission spec exactly.
