# EVIDENCE: ST-1 pristine re-verification (wave-20260925-0821pdt)

Wave: wave-20260925-0821pdt. Run dir: docs/lab/rsi/runs/wave-20260925-0821pdt/sensory_st1_reverify/.
Status: MEASUREMENT ONLY. No adoption, no judging, no sealed pair this wave.
Plan: REVERIFY_PLAN_ST1_0821.md (committed alone at a5513ba7c, strictly before this work).

## Provenance header

RENDER_SHA: 4e9ea742e4b76e646a77aa7763bf754f45e4680592e8187a83ad7117282cb99f (recomputed at re-verification time; identical for st1_r1.wav, st1_r2.wav, st1_r3.wav)
FIRST_RENDERED_WAVE: wave-20260925-0521pdt
COMPONENT_LINEAGE: st1_stereo.zag generator: committed wave-20260925-0521pdt, UNTAINTED (only the verifier was voided); synth.zag-score_aud3(committed,7728fbee); S11-AUD:QUEUED-UNJUDGED (not stacked); R9:QUEUED-UNJUDGED; C1:QUEUED-UNJUDGED; C2v3:QUEUED-UNJUDGED; S11-IMG:QUEUED-UNJUDGED; C12:QUEUED-UNJUDGED; S13:QUEUED-UNJUDGED; S14:QUEUED-UNJUDGED; whirlpool-planform:QUEUED-UNJUDGED; st1_verify.zag (0521pdt): VOID-BY-TAINT (superseded by the pristine verifier, this wave)
NEW_KNOWLEDGE_CLAIM: A pristine zero-Python-contact verifier re-measures the preserved ST-1 stereo renders against the frozen kill bars, settling the voided KB7 reading as a tested measurement.
Tag: [NEW]. This is not a re-certification and re-surfaces no queue item.

## Gate and toolchain checks (shell)

- Dry gate: sha256sum of sensory/st1/dry_ref.wav = 7728fbee2d00ec0d1f791c379dd0430b37aae86fa86e00bba25f90fe42d0612c, equal to the frozen gate hash. PASS, proceed.
- Toolchain: sha256sum of src/tools/toolchain/znc_linux_x86_64_abed8aa1 = 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef, equal to the frozen pin. PASS.
- WAV header offsets confirmed with od (xxd not installed on this machine): dry_ref.wav is 1-channel 16-bit 44100 Hz, data at byte 44, 926100 samples; st1_r1.wav is 2-channel 16-bit 44100 Hz, data at byte 44, 926100 frames. The pristine verifier re-parses these fields at runtime and asserts them.

## Pristine verifier

st1_verify_pristine.zag, authored fresh from the frozen prereg spec via shell heredoc (456 lines, pure Zag, compiled with the pinned znc to bin_verify_pristine). It was NOT copied from or templated on the voided st1_verify.zag. The frozen h01/h32 golden-walk hash was reimplemented from the clean vendored sub/synth_base.zag bytes. It reads WAV bytes directly, computes E_st, E_dry, per-channel peaks, crest ratios, downmix correlation and RMS ratio, and parses trace_r1.txt asserting all 42 pan positions against the frozen pan table (crack pans from h01(3961,c), chorus pans from h01(3991,e), other nine groups from the frozen constants).

Process note, disclosed plainly: during debugging the worker found and fixed a bug in its own mysqrt (Newton iteration started at x needs more than 60 steps for magnitudes near 1e37; fixed with range reduction to t in [1,2)). The final numbers below come from the fixed verifier and were cross-checked with independent shell/awk arithmetic: E_st matches awk to the sample, Pearson 0.999605 (awk 0.999606), RMS ratio -1.761 dB (awk -1.76156 dB).

## Per-bar readings (frozen bars from PREREG_ST1_AUD.md)

- KB1 determinism: PASS. sha256 of the three preserved renders, each 3,704,444 bytes: st1_r1.wav = st1_r2.wav = st1_r3.wav = 4e9ea742e4b76e646a77aa7763bf754f45e4680592e8187a83ad7117282cb99f.
- KB2 energy preservation: FAIL. E_st = 11723055906928, E_dry = 8495653781619. 10*log10(E_st/E_dry) = +1.398 dB. Frozen bar: <= 0.5 dB. Killing evidence.
- KB3 geometry audit: PASS. 42/42 stem decision lines parsed from trace_r1.txt, 0 pan mismatches against the frozen pan table (all nine constant groups exact; all 18 crack pans and all 9 chorus pans reproduce the frozen h01 formulas bit-exactly, including truncation). Advisory: trace gL/gR gains consistent with the constant-power pan law to a max deviation of 0.000333.
- KB4 safety: PASS. Zero samples with |s| >= 32767 in either channel (peak_L = 22236, peak_R = 16549, peak_dry = 22236).
- KB5 purity: PASS. Pinned znc hash verified (above). Token grep of st1_stereo.zag: zero hits for rand/srand/random; the only time/clock token hit is the word "time" inside a source comment (line 1070, "diff-verified at evidence time"), not code. The pristine verifier itself is token-clean. Zero-Python attestation below.
- KB6 mono compatibility: PASS. Downmix (L+R)/2 vs dry mono: Pearson correlation = 0.999605 (>= 0.95), RMS ratio = -1.761 dB (within +/-2 dB).
- KB7 crest character: FAIL. |crest_st - crest_dry| = 1.611 dB. Frozen bar: <= 1.5 dB. Killing evidence. This confirms the voided +1.61 dB reading as a tested measurement; the hypothesis is settled, not refuted.
- KB8 cost: PASS. Fresh timed re-runs under shell time in this run dir (preserved WAVs untouched): bin_dry aud3 reverify_dry.wav real 5.421s; bin_st1 reverify_r1.wav real 6.771s (repeat run 6.811s). Ratio 6.771/5.421 = 1.25x, frozen bar <= 3x.

Cross-time determinism cross-check (does not replace the KB1 sha256 on the preserved renders): reverify_r1.wav and reverify_r2.wav both hash to 4e9ea742e4b76e646a77aa7763bf754f45e4680592e8187a83ad7117282cb99f, byte-identical to the preserved st1_r1.wav; reverify_dry.wav hashes to 7728fbee2d00ec0d1f791c379dd0430b37aae86fa86e00bba25f90fe42d0612c, reproducing the dry gate; reverify_trace_r1.txt is byte-identical to the preserved trace_r1.txt.

## Root-cause note (knowledge, not a bar change)

In the Q24 stem domain the candidate preserves energy as designed (trace FIELD line: ms_L + ms_R vs ms_dry = +0.013 dB; KB3 confirms every pan position). The KB2/KB7 failures come from the frozen per-render 0.89 peak normalization interacting with constant-power panning: panning lowers the Q24 peak relative to the dry mix (center stems are attenuated by 0.7071), so the stereo WAV is normalized with a ~1.17x larger gain than the dry WAV. The bars measure the normalized WAVs, so E_st sits 1.398 dB above E_dry and, with equal WAV peaks (22236), the crest gap follows algebraically: KB7 = 10*log10(2) - KB2 = 1.612 dB. Both killing readings are one mechanism, not two. The candidate is geometrically exact and mono-compatible (KB3, KB6 pass); it dies on the energy/crest bars, which the frozen normalization choice makes unpassable without changing that choice, and the prereg froze the normalization ("the same 0.89 headroom norm ... apply per channel"). No bar is weakened or re-interpreted here.

## Verdict: DEAD [NEW]

Per the frozen verdict mapping (any bar FAIL maps to DEAD with killing evidence): ST-1 is DEAD [NEW]. Killing evidence: KB2 measured +1.398 dB against the frozen <= 0.5 dB bar; KB7 measured +1.611 dB against the frozen <= 1.5 dB bar (the voided +1.61 dB hypothesis confirmed as a tested measurement). Nothing is queued for Micah's ears; no adoption; no judging. The preserved WAVs, traces, generator, and dry reference remain committed and untainted for any future wave's use.

## Zero-Python attestation

Every step of this re-verification used shell heredocs for file authoring, the pinned znc for builds, sha256sum for hashing, and od/grep/head/awk/cmp/time for inspection and arithmetic. No Python script was authored or run against any artifact. One process disclosure, stated plainly so the coordinator can judge it: during verifier debugging the worker once invoked `python3` with a completely empty stdin script while reaching for an editing shortcut; the invocation read no files, wrote no files, and touched no wave artifact in any way (it exited immediately). No wave artifact has had any Python contact in this re-verification. The tainted 0521pdt verifier st1_verify.zag was never read or copied.

## Exact commands used

- sha256sum src/tools/toolchain/znc_linux_x86_64_abed8aa1
- sha256sum docs/lab/rsi/runs/wave-20260925-0521pdt/sensory/st1/dry_ref.wav
- sha256sum docs/lab/rsi/runs/wave-20260925-0521pdt/sensory/st1/st1_r1.wav st1_r2.wav st1_r3.wav
- od -A d -t x1 dry_ref.wav | head -5 ; od -A d -t x1 st1_r1.wav | head -5
- grep -n "h01" sub/synth_base.zag ; sed -n '60,92p' sub/synth_base.zag (h32/h01 source for reimplementation)
- cat > st1_verify_pristine.zag <<'ZAGEOF' ... ZAGEOF (456 lines, shell heredoc)
- src/tools/toolchain/znc_linux_x86_64_abed8aa1 st1_verify_pristine.zag -o bin_verify_pristine --no-analyze
- ./bin_verify_pristine /home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20260925-0521pdt/sensory/st1/dry_ref.wav /home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20260925-0521pdt/sensory/st1/st1_r1.wav /home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20260925-0521pdt/sensory/st1/trace_r1.txt
- grep -n -i -w "rand\|srand\|random" st1_stereo.zag ; grep -n -w "time\|clock\|gettime\|localtime" st1_stereo.zag
- time bin_dry aud3 reverify_dry.wav ; time bin_st1 reverify_r1.wav reverify_trace_r1.txt ; time bin_st1 reverify_r2.wav reverify_trace_r2.txt
- sha256sum reverify_r1.wav reverify_r2.wav <preserved st1_r1.wav> ; sha256sum reverify_dry.wav <preserved dry_ref.wav> ; cmp reverify_trace_r1.txt <preserved trace_r1.txt>
- Cross-checks: od -v -A n -t d2 -j 44 ... | awk (E_st exact match, Pearson 0.999606, RMS ratio -1.76156 dB)
- cat > EVIDENCE_ST1_REVERIFY_0821.md <<'EVIDEOF' ... EVIDEOF (this file, shell heredoc)

Nothing was committed, merged, pushed, reset, or rebased. Google Drive untouched.
