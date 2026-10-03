# JUDGE VERDICT — AUDIO V11 Phase 2 (fork adjudication)

**Judge:** independent Phase-2 judge (subagent of coordinator 7b003e12)
**Date:** 2026-09-24
**Protocol:** `JUDGE_PROTOCOL_V11.md` (frozen), voice signature `VOICE_SIG_FROZEN.md`
**Scope:** forks R (repair), P (paradd_tract), W (waveguide), G (gesture)

## 0. What this judge did independently

1. **Verified the frozen instruments.** `voice_sig_frozen.zag` SHA-256
   `7117ac57b2ad98a2849e4c86ef659164911835f03b50a63c5f6b7b64996e9a65`
   matches the live `consistency_gate/src/voice_sig.zag`; dependency
   `src/common_v5.zag` SHA-256
   `f98c04dc0e68536035faccaac32a1fb0e700f26ffec6d6be54224100deac4dc5`.
   Rebuilt with the pinned `znc` toolchain; the rebuilt binary reproduces the
   anchor metrics exactly (VS_NVOICED 36, MOD4 0.412, F0 651.3, F0DYN 174.3,
   F1B 794, F2B 2104, F2B_IQR 715, F3B 2814, HNR 3.7, TILT 0.9) and reruns
   byte-identically.
2. **Re-ran every clip twice** through the frozen `voice_sig` (3 V10 + 4 V11
   clips, byte-identical reruns) and applied the frozen §3 mechanical rule
   myself — including the tie-epsilon half of the rule that several fork
   reports misapplied (see §3).
3. **Built unseen pure-Zag discriminators D1–D6** (`REDTEAM_DISCRIMINATORS.md`,
   frozen before measuring any fork), measured anchor + all V10 + all forks
   twice each (byte-identical), and **attacked the discriminators** with three
   trivial deterministic game synths to map what they can and cannot catch.
4. **No audio playback exists in this environment.** Every statement below
   about "how it sounds" is instrument-based or quoted from the forks' own
   reports. Micah's ears remain the final oracle; nothing here overrules them.

## 1. Clip inventory (all 44.1 kHz / mono / 16-bit / 30.0 s, SHAs match fork claims)

| clip | SHA-256 (prefix) | voice_sig reruns |
|---|---|---|
| k_v11_repair (R) | `e9d716a4…` | byte-identical ×2 |
| k_v11_paradd_tract (P) | `0d4ffe0c…` | byte-identical ×2 |
| k_v11_waveguide (W) | `13cc7ecf…` | byte-identical ×2 |
| k_v11_gesture (G) | `4c7c62df…` | byte-identical ×2 |
| j_v10_artic / paradd / specstat | — | byte-identical ×2 |

## 2. Frozen 9-bar adjudication (independent, mechanical §3 rule)

Rule per bar: PASS iff (a) |F−A| ≤ tol **and** (b) |F−A| < |V10best−A| + tol/20
(V10best = PARADD, the only V10 render with voice metrics).

| bar | anchor±tol | V10 PARADD | **R** | **P** | **W** | **G** |
|---|---|---|---|---|---|---|
| V-F0 | 651.3±60 | 766.6 | 632.7 ✅ | 690.9 ✅ | 636.1 ✅ | 657.8 ✅ |
| V-F0DYN | 174.3±69.7 | 384.3 | 161.6 ✅ | 135.7 ✅ | ~70 ❌ | 410.8 ❌ |
| V-F1 | 794±120 | 740 | 777 ✅ | 750 ✅ | 787 ✅ | 743 ✅ |
| V-F2 | 2104±180 | 2329 | 2282 ✅ | 2168 ✅ | 1807 ❌ | 2107 ✅ |
| V-F3 | 2814±200 | 2968 | 2734 ✅ | 2634 ❌(b) | 2435 ❌ | 3074 ❌ |
| V-HNR | 3.7±4.0 | 4.0 | 3.6 ✅ | 3.6 ✅ | 3.2 ❌(b) | 3.1 ❌(b) |
| V-TILT | 0.9±3.0 | 0.0 | 0.9 ✅ | 0.0 ✅ | −0.6 ❌(b) | 0.5 ✅ |
| V-F2DYN | 715±286 | 1247 | 525 ✅ | 942 ✅ | 182 ❌ | 860 ✅ |
| M-MOD | 0.412±0.402 | 0.551 | 0.520 ✅ | 0.723 ❌(b) | 0.861 ❌ | 0.474 ✅ |
| **total** | | | **9/9** | **7/9** | **2/9** | **6/9** |

❌(b) = passes anchor tolerance but fails the strictly-nearer-than-V10 half.

### 2.1 Adjudication corrections (the forks misapplied their own bars)

- **R is 9/9, not 8/9.** The R crew read the HNR bar as a "4.0–4.2 dB" window;
  the frozen bar is anchor ± 4.0 dB (window −0.3…7.7), and the nearer-V10 half
  also passes (0.1 < 0.3 + 0.2). Their raw numbers reproduce exactly; only the
  adjudication was wrong.
- **W is 2/9, not 3/9.** Its HNR (3.2) sits exactly on the nearer-V10 boundary
  (|F−A| = 0.5, bound = 0.3 + 0.2 = 0.5, strict `<` fails) and its TILT (−0.6)
  passes anchor tolerance but is not nearer than V10 (1.5 < 1.05 false).
- **P's "strict lower bound" language is non-protocol**, but its 7/9 stands:
  F3B and MOD4 fail half (b).
- **G's 7/9 table used anchor tolerance alone**, ignoring half (b); under the
  full rule it is 6/9 — moot, since geometry kills it (§4).

## 3. Kill geometry (frozen rule a, z-distance over the 9 bars)

| fork | D(anchor) | D(V10-PARADD) | verdict |
|---|---|---|---|
| R | 1.342 | 4.817 | survives |
| P | 1.770 | 4.386 | survives |
| W | 3.686 | 7.431 | survives (worst of the four) |
| G | 3.704 | 2.680 | **KILLED** |

## 4. Unseen discriminators (independent red team, advisory — not frozen gates)

Definitions frozen in `REDTEAM_DISCRIMINATORS.md` before any fork was measured.
Pure Zag, zero RNG, byte-identical reruns. Anchor baselines (30 s field
recording, 2,997 frames, 171 voiced):

| disc | anchor | R | P | W | G |
|---|---|---|---|---|---|
| D1 vowel clusters | 4 | 9 | 5 | 4 | 3 |
| D2 transient rate /s | 1.50 (45) | 1.13 (34) | 0.43 (13) | 0.87 (26) | 0.83 (25) |
| D3 traj windows / med var F1 / med var F2 / frac static | 5 / 4,943 / 82,556 / 0.40 | 39 / 328,107 / 885,141 / 0.00 | 10 / 214,083 / 729,985 / 0.00 | 6 / 92,025 / 2,396,445 / 0.00 | 8 / 94,659 / 1,027,305 / 0.00 |
| D4 burst rate /s | 0.00 | 0.37 (11, 2 eps) | 0.00 | 0.23 (7, 1 ep) | 0.03 (1) |
| D5 F0-static frac / drone frac / HNR std | 0.17 / 0.00 / 2.16 | 0.17 / 0.00 / 2.15 | 0.22 / 0.00 / 2.03 | 0.22 / 0.00 / 3.16 | 0.33 / 0.00 / 2.61 |
| D6 blind 3-s-seg LOO accuracy (anchor vs fork) | — | 0.89 | 0.72 | 0.61 | 0.72 |
| voiced fraction | 0.06 | 0.51 | 0.25 | 0.25 | 0.10 |

Reading:
- **D5 is the forks' strong suit**: R matches the anchor *exactly* on pitch
  staticity (0.17) and HNR variability (2.15 vs 2.16); P and W are close.
- **D3 is the universal failure**: every fork's formant trajectories are
  18–66× more variable than the anchor's and *never* hold still
  (frac_static 0.00 vs 0.40). Real children hold vowels; all four forks glide,
  wobble, or jitter constantly. This is the single most consistent
  non-child fingerprint in the batch.
- **D6 (blind classifier)** separates R (0.89) and P (0.72) from the anchor but
  barely separates W (0.61) — W's static-tract jitter scatters features into
  anchor-like regions without being child-like (cf. its 2/9 objective score).
  Calibration: anchor-vs-V10 = 0.83–0.94; anchor-vs-trivial-game-synths = 1.00.
- **D1 is partially gameable**: V10-PARADD (no vocal tract at all) scores 3/4
  via F0-sweep harmonic scatter, and R overshoots to 9. Treat D1 as supporting,
  not decisive.
- **D2 weakness (documented)**: the transient gate misses bursts riding on
  loud harmonic beds (game synth G1's 10 noise bursts → 0 detected). A low
  transient rate on a dense synth is suspicious; a high one is evidence of
  real onsets. R's 1.13/s is its best child-like feature after D5.
- **D4**: no fork shows *mechanical* burst regularity; R's and W's bursts are
  irregular episodes, not the 8 Hz gating pattern D4 was built to catch. W's
  reported 8 Hz wobble is sub-burst modulation, below D4's resolution — noted
  as a gap, not a pass.

### 4.1 Gameability attacks (did the discriminators earn their keep?)

Three trivial deterministic synths, built to cheat:
- **G1** (6 static vowel stacks + noise bursts, games D1/D2): caught by D5
  (F0-static 0.96 vs 0.17) and D6 (1.00). D2 missed its bursts (weakness, §4).
- **G2** (fixed-F0 harmonic drone, games "voiced"): D5 destroys it
  (F0-static 1.00, HNR-std 0.06 vs 2.16), D6 1.00. Note: the drone gate
  itself missed G2 — an octave error in the F0 detector pushed measured HNR
  below the 15.1 dB gate; **F0-static fraction is the robust submetric**,
  the drone gate is fragile. Documented, not hidden.
- **G3** (4 Hz AM noise + harmonic bed, games "rhythm"): caught by D5
  (HNR-std 0.43) and D6 (1.00).
- A `nf0==1` panic in the classifier's segment IQR (negative index) was found
  by the attack corpus, root-caused, and fixed; all classifier numbers above
  are post-fix.

## 5. Per-fork verdicts

### Fork R (repair) — ITERATE (objective leader, not yet ears)
- Objective 9/9 (corrected §2.1); geometry survives (1.342 vs 4.817).
- D5 exact-match, D2 near-anchor: genuine progress on voice naturalness.
- But: D3 hyper-articulation (formants never static, 66× anchor variance),
  D1 overshoot (9 vs 4 clusters), D6 blind-separable (0.89), voiced 51% vs 6%,
  and its own steelman answers "probably not" children (no phonemes/words/
  coarticulation).
- **Next-round targets (measurable):** frac_static ≥ 0.25 with steady vowels;
  median F1/F2 trajectory variance within 4× of anchor; D6 accuracy ≤ 0.65;
  keep 9/9 and D5. Then ears.

### Fork P (paradd_tract) — ITERATE
- Objective 7/9 (F3B, MOD4 fail the nearer-V10 half); geometry survives.
- D1 5≈4, D5 close, D6 0.72 — nearer the anchor blind than R is.
- Gaps: no consonants by design (D2 0.43/s), buzzer source, random prosody
  (crew's own steelman), D3 never-static, MOD4 0.723 (overshoot).
- **Targets:** F3B > 2650 (nearer-V10 half), MOD4 < 0.571, add consonant
  onsets (D2 ≥ 0.8/s), D3 static vowels.

### Fork W (waveguide) — ITERATE (last place, fundamental rework needed)
- Objective 2/9; worst geometry (3.686 — 2.7× R's distance).
- D6 0.61 looks kind but is fool's gold: monovowel static tract + jitter
  scatters features without being child-like (F2 297 Hz off, F3 379 Hz off,
  F0DYN collapsed, MOD4 overshoot).
- Crew's own steelman concedes single-vowel /a/ and dark static tract.
- **Targets:** multi-vowel tract (D1 ≥ 3 *via distinct vowels*, not jitter),
  brighter spectrum (F2/F3 within tolerance), real F0 dynamics. Effectively a
  redesign of the tract, not a tune.

### Fork G (gesture) — KILL (frozen geometric kill)
- Independent re-run: 6/9 under the full §3 rule; D(anchor)=3.704,
  D(V10)=2.680 → nearer the V10 failure mode than the anchor. **Killed** per
  frozen rule (a), exactly as its own crew self-reported. Retained in the
  clips directory as the negative control only.
- Unseen profile for the record: D1 3, D2 0.83/s, D3 19×/12× anchor variance
  with frac_static 0.00, D5 0.33/2.61, D6 0.72 — mid-pack, irrelevant post-kill.

## 6. Ears

**No clip has earned Micah's ears.** R is the only 9/9 and the D5/D2 leader,
but the protocol requires both prongs, the unseen red team finds it
measurably non-child on D3/D6, and its own crew's steelman is negative.
Sending it to ears now repeats the V10 mistake (metrics pass, ears reject).
R iterates against the §5 targets; the first fork to hold 9/9 *and* close the
D3/D6 gaps goes to the ear panel.

## 7. Instrument notes for the record

- Fork crews' adjudication tables cannot be trusted at face value: R
  under-claimed (8/9 → true 9/9), W over-claimed (3/9 → true 2/9), G used
  half the rule. Always re-adjudicate from raw `voice_sig` output.
- `rtfeat perframe` schema documents a `pk` column that is not emitted; D5's
  pk ≥ 0.97 gate is implemented via the mathematically equivalent
  HNR ≥ 15.1 dB. Non-semantic; noted here, frozen method untouched.
- Per-clip `voice_sig` and perframe runs: twice each, byte-identical.
  `rtanal` report/classify: twice each, byte-identical.

## 8. Provenance

- voice_sig_frozen.zag: `7117ac57…64996e9a65`; common_v5.zag:
  `f98c04dc…700f26ffec6d6be54224100deac4dc5`; pinned znc rebuild clean.
- Judge code: `~/workspace/aud_v11/judge2/` (rtfeat.zag, rtanal.zag,
  gamesynth.zag, judge_table.py, REDTEAM_DISCRIMINATORS.md) — scratch, not
  committed (binaries excluded from the commit per protocol).
- This verdict commits to `sylorlabs/TNN`, branch `tnn-native-lab`, as
  `imagination_discovery/aud/b_alpha/JUDGE_VERDICT_V11.md` (report only).
