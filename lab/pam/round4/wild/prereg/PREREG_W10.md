# PREREG — W10 FORGE-PAM: DETERMINISTIC SPOOF-DUEL (wild track, WILD-B)

**Date:** 2026-09-24. **Crew:** WILD-B. **Status:** FROZEN — committed before
any W10 fixture, build, or run. Parent: debate record
`pam/round4/hypotheses/debate_pam_r4.md` (§W10). Shared tape:
`wild/tape/TAPE.md` (frozen).

## 1. Falsifiable claim

Every admission candidate must survive a duel against the best spoof a frozen
deterministic forger builds from it. Admit iff E(genuine) − max E(spoofs) ≥ μ
(μ frozen); ties/losses reject by rule. Claims:

- **F1:** the duel REJECTS forged candidates (relabel + authority-forgery
  attacks) that single-score gates would pass — the forger "repairs" the
  forgery into a stronger spoof, so the forged candidate loses its own duel.
- **F2:** genuine candidates (1102 C bundles) beat their spoofs by ≥ μ —
  D1 paranoia does not fire.
- **F3:** the margin μ does real work but is not the whole mechanism (D2);
  the forger is O(1) per candidate (D3); the library cannot mint known
  wrong-set attacks at duel-winning strength (D4).

Not W2 (adversary = fixed transform library, not an opposed agent). Not W7
(proactive per-admission duel, not post-hoc detection).

## 2. Frozen candidate bundles (`gen_w10.py`, committed after this prereg)

Deterministic (zero RNG). One bundle per tape row + 50 forged-attack bundles:
`id|kind|conf|mrgF|strong|agree|origin|prov_label|content_sig`
- kind ∈ {C, W, P, B} from the tape; F = forged-attack (every 22nd C row,
  then attacked — see below).
- origin ∈ {0=GEN,1=EXT}: frozen rule `origin = (conf + mrgF) mod 2`.
- prov_label ∈ {0=GEN,1=EXT}: C/B/F… : C and B: prov_label = origin
  (consistent). W and P: prov_label = 1−origin (GEN→EXT relabeled — the
  laundering attack on confident wrongs). F: prov_label = 1−origin AND
  conf := min(1000, conf+150) (relabel + authority forgery combined).
- content_sig (u64): `base = conf*1000003 XOR mrgF*9176 XOR idx*31`;
  `content_sig = base*1000 + (base mod 500)` → `(sig mod 1000) < 500`
  always (intact marker). F bundles keep intact sig (the forgery is in
  label+conf, not content).

## 3. Frozen evidence score E (design constants, NOT calibrated)

E(bundle) = conf*100 + min(mrgF,20000)/100 + strong*5000 + agree*2000
           + prov_term + content_term
- prov_term = +8000 if prov_label==origin else −8000.
- content_term = +4000 if (content_sig mod 1000) < 500 else −4000.

Hands-off note (§5(a)): E uses the frozen axes (conf, mrgF, strong, agree)
as-is. It does NOT recalibrate the M1 strong/agree thresholds or the C3
gates — it is W10's own frozen scoring function, fixed here before any
fixture exists. "Reused from the C3-repair machinery, unmodified" is honored
in the only honest concrete sense available: the axes and their semantics
are the frozen ones; no threshold is moved.

## 4. Frozen forger: transform library (K=6, pure functions)

1. **T_relabel**: prov_label := 1−prov_label. (Δprov = ∓16000)
2. **T_eps_up**: conf := min(1000,conf+25); content_sig := content_sig+500
   (deterministically breaks intactness: x<500 → x+500 ∈ [500,999]).
3. **T_eps_down**: conf := max(0,conf−25); content_sig := content_sig+500.
4. **T_splice**: mrgF := max(mrgF,9000);
   content_sig := (content_sig & ~1023) | 700 (broken marker).
5. **T_authforge**: conf := min(1000,conf+150); prov_label := 1−prov_label;
   content_sig := content_sig+500.
6. **T_declfork**: strong := 1; agree := 1; prov_label := 1−prov_label;
   content_sig := content_sig+500.

Duel (in-instrument, pure Zag): for candidate P compute E(P) and E(T_i(P))
for i=1..6; margin = E(P) − max_i E(T_i(P)); verdict = ADMIT iff margin ≥ μ,
else REJECT (ties reject by rule — no coin flip). Frozen μ = 1000.

Predicted margins (from frozen arithmetic): genuine C bundle — worst
transform is T_eps_up (ΔE = +2500−8000 = −5500) → margin +5500 ≥ μ ✓ ADMIT.
Relabeled W bundle — T_relabel repairs it (ΔE=+16000) → margin −16000 →
REJECT ✓. F bundle — same → REJECT ✓.

## 5. Kill bars (program §4 K1–K5 verbatim + debate D1–D4, add-only)

- **K1:** any false-admit on the frozen wrong set → KILL. Here: any W or P
  bundle (or F attack bundle) with verdict ADMIT → KILL.
- **D1 (added):** ≥10% of the 1102 frozen true bundles duel-rejected →
  KILL (paranoia). Predicted 0%.
- **D2 (added):** halve μ to 500 and re-run; if verdicts change on >20% of
  candidates → HOLD/redesign (margin doing all the work, forger decorative).
  Predicted 0% (no predicted margin in [500,1000)).
- **D3 (added):** forger runtime superlinear in candidate size → KILL
  (6 transforms × O(1) by construction).
- **D4 (added):** for each wrong-set bundle W (30 items), if any library
  transform applied to any C bundle reproduces W EXACTLY (all fields) with
  E(spoof) ≥ E(genuine) − μ → count it; count > 1 → KILL (library arms the
  attacker). Predicted 0 (T_relabel is the only exact-relabel path and its
  ΔE = −16000 ≪ −μ).
- **K2:** either battery run's stdout differs by one byte → KILL. (Three
  runs: μ=1000 twice + μ=500 once; the two μ=1000 runs must be byte-identical.)
- **K3:** correct-admit = 1102/1102 = 100% predicted ≥ 66.78% → SURVIVE
  expected. (B-row duel dispositions are diagnostic-only, reported.)
- **K4/K5:** per §4 (O(1) per candidate; terminates).

## 6. Battery

Instrument: pure-Zag `w10_duel.zag`. CLI: `w10_duel <bundles> <mu>`.
Emits `id|kind|verdict|margin|bestT|e0|e1|e2|e3|e4|e5` per candidate + summary.
Scorer `score_w10.py`: mirrors the 6 frozen transforms (from §4 above),
asserts mirrored E(spoof) == instrument-emitted E for every spoof
(mismatch → KILL as implementation defect), computes K1/D1/D2/D4/K3, and the
B-row diagnostic.

## 7. Debate open question — recorded

W10's forger and W7's laundering fixtures share NOTHING (see PREREG_W7 §7):
independently defined, independently implemented. Deliberate non-sharing.

## 8. Hands-off / laws compliance

- No M1/C3 threshold touched; E is W10's own frozen function.
- Fable's 4 kill-bar repairs: not applied. 3 HELD items: not run.
- Zero RNG; no wall-clock; deterministic given (bundle, μ).
- []u8 arenas + LE accessors; no `as []i32/u32/u16` indexed casts.

## 9. Standing-law cap note (for verdict-time classification)

Frozen numeric caps: μ=1000, K=6, weights in E, ε=25, +150, splice 9000.
Classified at verdict time per the 2026-09-24 standing law.
