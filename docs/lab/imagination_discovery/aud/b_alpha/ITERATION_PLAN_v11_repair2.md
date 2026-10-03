# ITERATION PLAN — V11 Repair Round 2 (Fork R2)

**Date:** 2026-09-24
**Fork:** R (repair), second iteration → `render_v11_repair2.zag`
**Authority:** JUDGE_VERDICT_V11.md §5 (Fork R — ITERATE); frozen bars VOICE_SIG_FROZEN.md; discriminators REDTEAM_DISCRIMINATORS.md (`~/workspace/aud_v11/judge2/`).
**Instruments verified:** rebuilt `rtfeat`/`rtanal`/`voice_sig` from judge sources with the pinned znc reproduce round-1 numbers exactly (perframe byte-identical; rtanal report identical; D6 classify 0.89). Voice_sig rebuild in progress; no render until it reproduces the round-1 9-bar signature.

## Round-1 diagnosis (white-box, from `render_v11_repair.zag`)

D3 kill-shot root causes, in the formant path (control tick, every 64 samples):

1. **Syllable-coupled F2 morphing.** `vXf2=(2350-500*mouth)*(1+0.30*vv)` with
   `vv=sin(2π·sylPh·0.5)` at sylR≈5 Hz → **F2 swings ±30% at ~2.5 Hz,
   continuously, on every voice.** Every syllable is a new vowel position.
   This is the hyper-articulation: real children repeat syllables on a
   HELD vowel ("ma-ma-ma") with STATIC formants.
2. **F3/F4 random walk.** `F3=3600+1000·hw(t,2.2s)`, `F4=5600+1400·hw(t,2.6s)`
   — up to 1000 Hz of F3 wander. Nothing in a held child vowel does this.
3. **4-voice overlap.** voiced_frac 0.51 (anchor 0.06): 4 dense voices whose
   LPC-24 peaks hop between speakers frame-to-frame, multiplying per-frame
   f1/f2 jitter on top of the per-voice morphing.

D6 (0.89) separability is driven by the same features: med_var_f1/f2
(66×/11× anchor), voiced_frac (0.51 vs 0.06), n_clusters (9 vs 4, from the
continuous F2 scatter), burst_rate (0.37 vs 0.00).

What round-1 got RIGHT and must be preserved: glottal source + sharpening
(F0/TILT/HNR bars), aspiration level (HNR 3.6), syllabic AM at 4–6 Hz
(MOD4 0.520), footsteps (D2 1.13/s), utterance-gate turn-taking,
deterministic hash modulation (D5 exact-match 0.17/2.15).

## Mechanisms to change (and why)

**M1 — Discrete vowel targets with long dwells (attacks D3 directly).**
Replace the continuous `mouth`/`vv` formant law with per-voice vowel
TARGETS from a 4-vowel child table (/a/ 1050/1500/3300, /i/ 420/3100/3800,
/u/ 480/1250/3300, /o/ 950/2100/3400 — child-scaled, Iseli corners tempered
toward the anchor centroids). Each voice holds one vowel for a 1.8–3.4 s
dwell (hash-scheduled), glides to the next over τ≈0.25 s exponential
approach, then holds again. Formants are bit-static inside dwells.
Expected: 1-s D3 windows fully inside dwells → var(f1)+var(f2)≈0 →
frac_static → ~0.6–0.8 (target ≥0.25); med_var collapses toward anchor
(target ≤4×). Bonus: 4 discrete vowels → D1 ≈ 4 cells = anchor (was 9).

**M2 — Syllable AM decoupled from articulation (protects MOD4, fixes the
coupling bug).** Keep `sylPh`/`sylg` 4–6 Hz syllabic AM untouched — it is
the MOD4 engine and mimics "ma-ma-ma" repetition on a held vowel. The bug
was coupling: one oscillator drove both rhythm AND vowel position. Now
rhythm runs at 5 Hz, vowels change only between bouts.

**M3 — F3 wander killed, F4 calmed.** F3 comes from the vowel table
(±glide only); F4 wander 5600+1400·hw → 6000+400·hw (slow drift). Protects
V-F3B bar (anchor 2814±200) while removing a pure-variance source.

**M4 — Sparser vocal duty (attacks D6 voiced_frac + D3 cross-voice
confusion).** Deepen the utterance gate
`ug=0.05+0.95·smoother(hw·1.9−0.45)` → longer, deeper pauses
(`smoother(hw·2.4−1.1)` at 0.9 s knots), and add a bout-level pause
(0.5–1.4 s) between vowel dwells. Target voiced_frac ~0.20–0.25 (anchor
0.06; round-1 0.51) — sparse enough that LPC usually sees one dominant
voice, dense enough to keep VS_NVOICED ≫ 25 (round-1 had 342; budget
~80–120). Also damps D4 burst count (0.37/s → lower) and D6 feature #1.

**M5 — Everything else frozen.** Glottal pulse, aspiration 0.10, jitter,
vibrato, footsteps, air, chaos master, vboost: untouched (they earned the
9/9 and D5).

## Risks / tradeoffs (declared up front)

- **V-F2B_IQR (bar 429–1001, R1 525):** discrete vowels SPREAD F2
  (/u/1250 → /i/3100). IQR may rise toward ~700 — inside the bar, but will
  verify; if it overshoots, temper vowel F2s.
- **V-F3B (2614–3014, R1 2734):** vowel F3s 3300–3800 could pull the
  1500–4600-band centroid up; the strong F2 energy (~2000) in-band pulls it
  down. Measure; temper if needed.
- **M-MOD (0.010–0.814, R1 0.520):** sparser voices + bout pauses deepen
  envelope contrast; could push MOD4 up. Bar is wide; measure.
- **D2 (1.13/s):** footsteps untouched; sparser voices may slightly raise
  detected transient rate (quieter beds) — acceptable either way.
- If stabilizing trajectories breaks any of the 9/9 bars, that tradeoff is
  itself the finding — documented, not hidden.

## Targets (judge's instruments, no new metrics)

1. frac_static ≥ 0.25 (anchor 0.40; R1 0.00)
2. med_var_f1 ≤ 19,772 and med_var_f2 ≤ 330,224 (≤4× anchor; R1 66×/11×)
3. D6 classify ≤ 0.65 (R1 0.89)
4. 9/9 frozen voice_sig bars (full §3 rule incl. nearer-than-V10 half)
5. Keep D2 ≈ 1/s, D5 ≈ 0.17/0.00/2.15 (no regressions on strengths)

## Process

Render → rtfeat perframe → rtanal report+classify → voice_sig 9-bar.
Iterate constants only (vowel table, dwell/pause ranges, gate depth).
Final: `src/render_v11_repair2.zag`, `clips/b_alpha_kids_1e_l_v11_repair2.wav`
(≥2 byte-identical renders), `FINDINGS_v11_repair2.md` with full tables,
byte-identical proof, and the mandatory honest steelman. Ears are NOT
claimed — Micah's ears remain the oracle.
