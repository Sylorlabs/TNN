# DP-1 DOSSIER: orphaned candidate verification - wave-20260926-1121pdt

Candidate: DP-1 DOPPLER FLYBY [NEW], from wave-20260925-1721pdt.
Worker role: DP-1 DOSSIER worker, depth-2. Read-only verification of the
1721pdt run dir; nothing in that dir was modified. This worker adopts
nothing and integrates nothing. This dossier is for the mandatory debate
group of wave-20260926-1121pdt.

RECOMMENDATION: CERTIFY READY-FOR-JUDGE, with two flagged caveats for the
debate (see sections 5 and 6). All 8 frozen bars pass, provenance is clean,
commit order passes, red team agrees, and independent hash spot checks
confirm the evidence.

## 1. Provenance header (quoted verbatim from EVIDENCE_DP1_1721.md)

RENDER_SHA: 994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771
FIRST_RENDERED_WAVE: wave-20260925-1721pdt
COMPONENT_LINEAGE: D-AUD-3-substrate(synth.zag f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055, vendored byte-identical as sub/synth_base.zag); R9:QUEUED-UNJUDGED; C1:QUEUED-UNJUDGED; C2v3:QUEUED-UNJUDGED; S11-IMG:QUEUED-UNJUDGED; S11-AUD:QUEUED-UNJUDGED; S12:DEAD; S12b:DEAD; S13:QUEUED-UNJUDGED; S14:QUEUED-UNJUDGED; whirlpool-planform:QUEUED-UNJUDGED; B1:DEAD; DF-1:DEAD; C-D19:DEAD; G1:STOOD-DOWN; ST-1:DEAD; D-VID-1:STOOD-DOWN
NEW_KNOWLEDGE_CLAIM: A frozen constant-velocity flyby rendered through a time-varying propagation delay adds motion-based realism to the D-AUD-3 bed via doppler pitch fall, inverse-distance loudness swell, and lateral pan at linear resampling cost.
Tag: [NEW].

Provenance verdict: COMPLETE AND CLEAN.
- RENDER_SHA: in the prereg it was a stated placeholder ("filled at render
  time in EVIDENCE"), and the evidence fills it with
  994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771.
  Independent sha256 of dp1_variant_r1.wav, dp1_variant_r2.wav, and
  dp1_variant_r3.wav all match this SHA exactly. Not recycled: git history
  grep for "doppler"/"flyby" across all commits finds zero hits outside
  wave-20260925-1721pdt, and the WAV first appears as an added file in
  commit 02d1dcb31. FIRST_RENDERED_WAVE claim confirmed.
- COMPONENT_LINEAGE: every prior candidate ID present with a judge-queue
  status (QUEUED-UNJUDGED / DEAD / STOOD-DOWN). No JUDGED items listed.
  R9, C1, C2v3, S11-IMG, S11-AUD, S13, S14, whirlpool-planform correctly
  listed as QUEUED-UNJUDGED.
- NEW_KNOWLEDGE_CLAIM: one sentence, present.
- No recycled render. Tagged [NEW], not a re-certification.

## 2. Prereg commit-order self-check: PASS

- Prereg: 18ad30fe3 "DP-1 doppler flyby: frozen prereg (pre-implementation)",
  2026-09-26 00:58:46 UTC. Single file: PREREG_DP1_1721.md (147 lines).
  Committed alone.
- Implementation: 02d1dcb31 "DP-1 doppler flyby: implementation plus evidence
  (READY-FOR-JUDGE)", 2026-09-26 01:26:51 UTC. 18 files, all inside
  docs/lab/rsi/runs/wave-20260925-1721pdt/sensory/dp1/ (EVIDENCE, LISTENING,
  REDTEAM docs, .zag sources, .wav artifacts, traces, sub/synth_base.zag,
  verifier output). No other repo files touched.
- Order: prereg strictly precedes implementation (28 minutes earlier).
  Both commits are ancestors of tnn-native-lab HEAD.

## 3. Frozen kill bars (from EVIDENCE_DP1_1721.md), measured numbers

| Bar | Measured | Result |
|-----|----------|--------|
| KB1 determinism 3/3 | variant WAV sha256 994f9402... x3; trace sha256 eb375fd6... x3 | PASS |
| KB2 no clipping | base_peak=21713, var_peak=21739, both < 32767, 0 clips | PASS |
| KB3 doppler ratio +/-3% | f_approach=52.500, f_recession=43.500, ratio_meas=1.207, ratio_exp=1.207 | PASS |
| KB4 crest +/-1.5 dB | crest_ratio=0.994 (bounds 0.84140..1.18850) | PASS |
| KB5 energy +/-2 dB | rms_ratio=1.007 (bounds 0.79433..1.25893) | PASS |
| KB6 pure Zag, pinned compiler | token grep zero hits in DP-1-authored code; znc 498abcb5 | PASS |
| KB7 cost <=2.0x baseline | variant 6.726 s / baseline 3.603 s = 1.867x | PASS |
| KB8 trace audit 210/210 | 0 mismatches at 1e-9 scale | PASS |

Verdict mapping (READY-FOR-JUDGE iff all pass): SATISFIED. All 8 bars pass.

Independent spot checks (read-only, this worker):
- sha256 of dp1_variant_r1.wav, r2, r3: identical, all match RENDER_SHA.
- sha256 of dp1_baseline.wav matches evidence: a32ff18e8a359963152a090aa96ee16a32461dbf9632b9510e6bba4bdd224f7c.
- sha256 of dp1_probe.wav matches evidence: e20dbae75e266db301e4936415352c289b9f9e266611219f8db2d689e83b6f94.
- sha256 of dp1_trace.txt/r2/r3: identical, match eb375fd64aa9325d1f7cb8957ad38335c2e6ee0362231bc5c3aaaf37244e6712.
- sha256 of sub/synth_base.zag matches the vendored substrate claim: f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055.
- Raw verifier output (dp1_verifier_out.txt): header_ok=1, KB2=1, KB3=1,
  KB4=1, KB5=1, KB8=1, fails=0.

## 4. Red-team report: EXISTS, AGREES with READY-FOR-JUDGE

REDTEAM_DP1_1721.md (adversarial self-review) confirms novelty (repo-wide
grep: doppler 0 hits), rebuts the S11-AUD mechanism-class objection
(static time-invariant room filtering vs time-varying source-motion delay;
no shared code, parameter, or measurement), clears the ST-1 replay check,
clears the substrate-vibrato collision, and confirms bar integrity
(no gaming on KB3 tolerance, KB4/KB5 ratios 0.994/1.007 are honest
minimal-perturbation results, KB7 1.867x under the 2.0x bar).

Bottom line, quoted verbatim:
"No padding, no re-freeze, no bar movement, no frontier contact. DP-1
stands as [NEW] with all bars passing. READY-FOR-JUDGE."

Honesty flags the red team itself discloses (belong to the judge):
the flyby is a new world event (a lifter), not a transformation of an
existing voice, so it is content-adjacent; the S11-AUD thematic overlap is
a real judgment call for the owner; audibility was not ear-checked by the
worker (levels set analytically).

## 5. Python finding: DISCLOSED NO-CONTACT CONTACT, one instance

EVIDENCE_DP1_1721.md disclosure 2: the worker used `python3 -c` once to
count dash characters in its own draft fragment (read-only, no
modification, no analysis, no wave artifact written). All subsequent
checks used grep.

Independent grep of the whole dp1 run dir: the only "python" mentions are
the KB6 token-grep bar text in the prereg and the disclosure itself. No
.py files, no scripts invoke Python, no Python content in the .zag
sources. Classification per P13/P15: disclosed no-contact contact, NOT a
breach of the worker's own KB6 bar (that bar covers DP-1-authored .zag
code plus token grep). CAVEAT for the debate: under the tightened loop
governance (pure-Zag literal, restored 2026-09-24), this is the kind of
contact the debate should explicitly note and rule acceptable or not.

This dossier worker's own attestation: zero Python touched wave artifacts.
No Python was invoked by this worker in this verification; all checks
used git, sha256sum, grep, and cat only.

## 6. Sealed blind A/B pair / human listening status

There is NO sealed blind A/B pair for DP-1 (no coded pair like S11-AUD in
the judge queue). DP-1 is not queued; its status per the evidence is
READY-FOR-JUDGE awaiting his verdict.

LISTENING_DP1.md exists and is a listening instruction for his ears:
- Baseline: dp1_baseline.wav (D-AUD-3 bed, stereo, 21 s).
- Variant: dp1_variant_r1.wav (bed plus flyby, stereo, 21 s).
- Both at the same fixed level, no normalization tricks.
- Listen for: motion (enters far left, through center at t=10.5 s, exits
  far right), pitch fall (measured 52.5 Hz to 43.5 Hz on the stem, about
  a 1.2x drop), loudness swell peaking at closest approach.
- The question for his ears: "Does the flyby make the planetvoice scene
  feel like a real place with something moving through it, or does it
  read as a synth effect pasted on?"
- His ears are the kill bar; there is no metric behind this. The worker
  could not listen.

Per the sensory headspace rule, human ears outrank audio metrics. All 8
bars pass on the metric side; the listening verdict is outstanding and
belongs to him.

## 7. Orphan status: CONFIRMED ORPHANED

- No section for wave-20260925-1721pdt exists in docs/lab/rsi/LOOP_STATE.md.
- No "DP-1" mention anywhere in LOOP_STATE.md.
- Debate dir docs/lab/rsi/runs/wave-20260925-1721pdt/debate/ is empty
  (no transcript, no ruling).
- No debate transcript in any wave run dir mentions DP-1.
- DP-1 has never reached Micah. Evidence commit message claimed
  READY-FOR-JUDGE; the wave died before any debate or judge ruling.

## 8. Debate recommendation

CERTIFY READY-FOR-JUDGE. The candidate satisfies every mechanical
requirement: complete honest provenance, prereg before implementation in
separate single-purpose commits, all 8 frozen bars passing with
independently confirmed artifact hashes, a red-team report that agrees
with the verdict while disclosing its own weaknesses.

Two items for the debate to note on the record:
1. The single disclosed `python3 -c` contact (read-only dash count on the
   worker's own draft, no artifact touched): rule it acceptable contact or
   flag it under the tightened pure-Zag governance.
2. The red team's honesty flags (content-adjacent lifter carrier;
   S11-AUD thematic overlap; no worker ear-check): these belong to his
   listening verdict, not to the metrics. If the debate wants a sealed
   blind A/B pair before he listens, that sealing work is outstanding;
   the pair does not exist yet.

Wave artifacts referenced:
- Run dir: docs/lab/rsi/runs/wave-20260925-1721pdt/sensory/dp1/
- Prereg commit: 18ad30fe3
- Evidence commit: 02d1dcb31 (READY-FOR-JUDGE message)
- This dossier: docs/lab/rsi/runs/wave-20260926-1121pdt/dp1/DP1_DOSSIER_1121.md
