# Motion4 (M4) build notes — 2026-09-24

## Source
`senses/youtube_ingest/motion4/motion4.zag` — pure Zag, integer (i64)
arithmetic only, zero RNG. Single import beyond the substrate: none
(`R33_NATIVE_IO_V1.zag` syscall/alloc substrate only, same as M3).

Implements PREREG_MOTION4.md §4 verbatim:
- §4.1: luminance planes L = r+g+b (u16 LE arenas), all frames — M3 verbatim.
- §4.2: deterministic pyramid — S0 full plane; S1 = 2×2 block floor-mean;
  S2 = 4×4 block floor-mean, **both taken directly over the S0 luminance
  plane** ("exact integer means"; remainder pixels ignored). Effective
  full-res search range S0 ±2px / S1 ±4px / S2 ±8px.
- §4.3: at each scale the M3 pipeline runs verbatim (8×8 blocks, stride 8,
  pairs (0,1)..(nf−2,nf−1), SAD over 25 offsets ±2 edge-clamped,
  e_b = SAD(0,0) − SAD(best) ≥ 0, vote iff e_b > 0, frozen octant binning,
  aggregates E_total/E_bin[9]/N_vote/G_num/N_tot, coh_pm/G_pm/Ebar,
  M3 §3.6 decision rules) with scale-local constants COH_DIR 667,
  COH_STILL_MAX 667, G_MIN_PM 500, VOTE_FRAC 1/4, E_FLOOR 64 — same
  numbers at every scale, interpreted in that scale's pixel units.
- §4.4: P5 cross-scale resolution exactly as frozen (blind scale never
  vetoes; DirCands∩StillCands → `still_dir_conflict`; ≥2 distinct dir
  bins → `scale_disagree`; single bin → CANDIDATE with
  confidence = min over DirCands, reason `coherent_multiscale`;
  still-only → STILL CANDIDATE with min StillCands confidence and the
  finest still reason; else WITHHOLD with S0's reason code).
- §4.5: ops = M3 lum-build px-adds at S0 verbatim + SAD inner-loop
  pixel comparisons at every scale; pyramid downsample passes count 0.
  This reproduces the frozen estimates exactly on the standard 8-frame
  64×64 clip: 749,568 (S0) + 179,200 (S1) + 44,800 (S2) = **973,568**
  < 1.5M ceiling (K7).
- stdout: `approach=M4, task=motiondir, judgment=…, decision=…,
  confidence=…, reason=…, debug_vec=s0:win=…;coh_pm=…;g_pm=…;ebar=…|
  s1:…|s2:…, ops=…` (M3 field order kept).

## Toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).
Build (from a scratch dir holding `motion4.zag` + `R33_NATIVE_IO_V1.zag`,
because `@import` resolves relative to cwd):
`znc_linux_x86_64_abed8aa1 motion4.zag -o motion4`
Binary: 72,397 bytes, sha256
`d0de7df75a3762deb512125af0a1fa0f4ef0c08cb1188ae8c4a6fef06ee67b3f`.
The compiled binary lives ONLY in scratch and is NEVER committed.

## Analyzer warnings (9, non-fatal, same class as M3's)
- 8× L0012 string-buffer leak: `_zag_i64_to_str` result passed unbound
  to `ob_add` (also present in M3's `ob_pair`; output-path only).
- 1× A0102 ignored `nio_write_all` return in `fail` (same as M3).
None affect decision logic. Documented; repairing would not change
frozen behavior.

## Cost
973,568 ops per standard 8-frame 64×64 clip (frozen target ≤1.5M).
All B1/B2/RM1 fixtures are 8-frame 64×64 → same count.

## Zero RNG / zero time
`grep -ciE "rand|random|time|clock|seed"` over `motion4.zag`: **0**.
All decisions are pure functions of the input bytes.

## K6 determinism evidence (smoke battery — 8 deterministic fixtures,
generator `mk_smoke.py`, scratch-only, NOT the frozen batteries)
- 3× single-fixture runs (`smoke/move6_e.vid`) → byte-identical stdout,
  sha256 `fb28b33e864f7bb4e6134e99446793d9d6036efa91129fbc543330bdb74b7b73`.
- Full smoke battery (8 fixtures) run twice from wiped caches →
  identical digest sha256
  `8d684be565458330c52e35eab34b873b4aed05a80cbca4a2fab0e417bb3eccac`.
- Pinned-toolchain rebuild from a wiped scratch dir → byte-identical
  binary, sha256 `d0de7df75a3762deb512125af0a1fa0f4ef0c08cb1188ae8c4a6fef06ee67b3f`.
- Full B1+B2+RM1 rerun per K6 is for the kill-battery crew on the frozen
  binary+source (fixtures were still being built by the sibling crew).

## S0 verbatim audit vs the frozen M3 binary
`motion3.zag` rebuilt with the pinned toolchain; per-fixture S0
`win/coh_pm/g_pm/ebar` compared against the M3 binary's debug_vec on
all 8 smoke fixtures + 3 real B1 fixtures (p000/p001/p059):
**bit-identical on all 11**. Per-scale (decision, bin, confidence,
reason) also matched M3's (judgment, decision, confidence, reason) on
all 8 smoke fixtures (via a scratch-only instrumented build; the
instrumentation was never committed).

## Smoke behavior (not scored — kill batteries run later, in order,
by a separate crew on the frozen binary+source)
- still (gray/texture): STILL CANDIDATE `exact_still`, conf 1000, all scales.
- 1px/frame E: S0+S1 coherent E, S2 `exact_still` → per frozen P5
  WITHHOLD `still_dir_conflict`, conf 0.
- 3px/frame E: S0 blind, S1+S2 coherent E → E CANDIDATE
  `coherent_multiscale`, conf 840 (min of scale confidences).
- 6px/frame E: S0+S1 blind, S2 coherent E → E CANDIDATE, conf 921.
- 8px/frame E: S2 coherent E → E CANDIDATE, conf 1000.
- cut: WITHHOLD `sparse` (S0's reason), conf 0.

## Implementation notes (not spec changes)
1. **S2 from S0 directly.** §4.2 "S2 = 4×4 block average (floor
   division)" is read as 4×4 blocks of the S0 plane (not cascaded
   2×2 of S1 — those differ in general). Documented here; both are
   deterministic, the frozen reading is the direct one.
2. **Degenerate scales.** The prereg does not name the case
   ws<8 or hs<8 (the 8×8-block pipeline cannot run). Treated as blind
   per P5: WITHHOLD with an internal-only reason code, never vetoing,
   never a candidate. Unreachable on all frozen batteries (frames are
   64×64). This is a P5-consistent completion, not a rule change.
3. **ops counting.** §4.5's formula ("SAD inner-loop pixel
   comparisons") is operationalized by its own frozen estimates:
   S0 counts the verbatim M3 lum-build adds (hence 749,568), S1/S2
   count SAD px-visits only (179,200 / 44,800), downsample passes 0.
4. **debug_vec `win`** is the argmax bin (M3 semantics), reported even
   on WITHHOLD/STILL outcomes — an early draft printed the judgment
   bin instead and was corrected before commit.

## Heads-up for the kill-battery crew (frozen-spec consequence, no deviation)
On the 1px/frame B2 clips, S2 (0.25 scale-px/frame) claims STILL while
S0/S1 claim coherent direction, so frozen P5 forces
`still_dir_conflict` → WITHHOLD. If B2's 26 moving clips are all
1px/frame, expect moving-catch ≈ 0/26 against K2's ≥ 25/26 bar —
a mechanism-vs-bar tension the repair-round rule (§7) anticipates.
Do NOT "fix" by reinterpreting P5; a frozen-bar failure goes through
the declared repair round with Micah's sign-off.

## Kill batteries
NOT run by this crew (per tasking: B1→B2→B3a→RM1→RM2→B4 run in order
by a later crew on the frozen binary+source). No victory declared.
