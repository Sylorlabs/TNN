# RE-VERIFICATION PLAN: ST-1 stereo field, pristine verifier (wave-20260925-0821pdt)

Wave: wave-20260925-0821pdt. Run dir: docs/lab/rsi/runs/wave-20260925-0821pdt/sensory_st1_reverify/.
Status: PLAN ONLY. This commit strictly precedes any re-verification implementation commit (commit-order self-check).

## Background

Wave-20260925-0521pdt implemented ST-1 (D-AUD-3 planetvoice stereo field, 42 stems, world-derived constant-power panning) but the verdict was UNVERIFIABLE [NEW]: the worker's own evidence disclosed a Python text edit on st1_verify.zag, reverted via backup with no pre-touch hash or revert diff. Under the 1121pdt standing rule (taint by contact, not intent), the verifier's evidence is void. The +1.61 dB KB7 reading stands as an untested hypothesis. The 0521pdt judge queued a pristine re-verification: zero Python contact, all Zag, before any verdict (including DEAD) can be rendered.

## Frozen bars (unchanged from PREREG_ST1_AUD.md, wave-20260925-0521pdt)

KB1 determinism: 3/3 stereo renders byte-identical (sha256 equal). KB2 energy preservation: |10*log10(E_st / E_dry)| <= 0.5 dB, E_st = sum(L^2+R^2) over both channels. KB3 geometry audit: the pure-Zag verifier asserts all 42 stem pan positions against the frozen pan table from the binary's trace; any mismatch kills. KB4 safety: zero samples with |s| >= 32767 in either channel. KB5 purity: pinned znc (sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef), zero Python contact with any wave artifact (shell and sha256sum only), token grep clean for rand/srand/random/time/clock. KB6 mono compatibility: downmix (L+R)/2 vs dry mono Pearson correlation >= 0.95 AND RMS within +/-2 dB. KB7 crest character: |crest_st - crest_dry| <= 1.5 dB (S11-AUD precedent bar; stays; no narrowing). KB8 cost: stereo render wall time <= 3x dry render wall time.

## Preserved artifacts (committed wave-20260925-0521pdt, never Python-touched)

- sensory/st1/st1_r1.wav, st1_r2.wav, st1_r3.wav (3,704,444 bytes each): the three preserved stereo renders.
- sensory/st1/trace_r1.txt (plus trace_r2/r3): binary decision lines (element, stem index, pan, gL, gR).
- sensory/st1/dry_ref.wav: dry rebuild reference (frozen gate sha256 7728fbee2d00ec0d1f791c379dd0430b37aae86fa86e00bba25f90fe42d0612c).
- sensory/st1/bin_st1: generator binary (untainted; only the verifier was touched).
- sensory/st1/st1_stereo.zag and sensory/st1/sub/synth_base.zag: generator and vendored sources (untainted).

## Tainted artifact (do not cite, do not reuse)

sensory/st1/st1_verify.zag: Python contact, evidence void. The pristine verifier is authored FRESH from the frozen prereg spec via shell heredoc. It must not copy the tainted file. Reading committed clean sources (prereg, synth_base.zag, PLANETVOICE.md) read-only is allowed.

## Re-verification procedure (frozen)

1. Re-verify the dry gate: sha256sum of dry_ref.wav equals the frozen gate hash; stop if not.
2. KB1: sha256sum of the three preserved renders; all equal means PASS.
3. Build the pristine verifier st1_verify_pristine.zag (pure Zag, shell-authored, pinned znc). It reads WAV bytes and computes: E_st, E_dry, peaks, crest ratios (KB2, KB4, KB7), downmix correlation and RMS vs dry (KB6). It parses trace_r1.txt and asserts all 42 pan positions against the frozen pan table (KB3), reimplementing the frozen h01 hash from the clean synth_base.zag bytes.
4. KB5: token grep on st1_stereo.zag for rand/srand/random/time/clock; worker attests zero Python contact (shell heredocs plus znc only, /tmp scratch shell-only).
5. KB8: fresh timed re-runs of bin_st1 vs bin_dry under shell `time`; stereo wall <= 3x dry wall. Fresh renders are labeled re-verification artifacts; if they reproduce the preserved WAVs byte-identically, that is recorded as a cross-time determinism cross-check.

## Verdict mapping (frozen; measurement only)

- All KB1..KB8 PASS on pristine evidence: PASS-ON-BARS [NEW]. The stereo WAVs plus pristine evidence are QUEUED for Micah's ears in a future wave (audio precedent: no sealed pair for audio; Micah's ears are the judge). No adoption this wave; no judging this wave.
- Any bar FAIL: DEAD [NEW] with the killing evidence (the pristine KB7 reading either confirms or refutes the +1.61 dB hypothesis).
- Any Python contact with a wave artifact: VOID on sight.

## Provenance header (for the evidence)

RENDER_SHA: sha256 of the preserved stereo WAVs (recomputed at re-verification time)
FIRST_RENDERED_WAVE: wave-20260925-0521pdt
COMPONENT_LINEAGE: st1_stereo.zag generator: committed wave-20260925-0521pdt, UNTAINTED (only the verifier was voided); synth.zag-score_aud3(committed,7728fbee); S11-AUD:QUEUED-UNJUDGED (not stacked); R9:QUEUED-UNJUDGED; C1:QUEUED-UNJUDGED; C2v3:QUEUED-UNJUDGED; S11-IMG:QUEUED-UNJUDGED; C12:QUEUED-UNJUDGED; S13:QUEUED-UNJUDGED; S14:QUEUED-UNJUDGED; whirlpool-planform:QUEUED-UNJUDGED; st1_verify.zag (0521pdt): VOID-BY-TAINT (superseded by the pristine verifier, this wave)
NEW_KNOWLEDGE_CLAIM: A pristine zero-Python-contact verifier re-measures the preserved ST-1 stereo renders against the frozen kill bars, settling the voided KB7 reading as a tested measurement.
Tag: [NEW]. This is not a re-certification and re-surfaces no queue item.
