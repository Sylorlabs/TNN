# ATTACK PREREG — V2-B interventional-leg red-team (Gap Crew C)

**Status: FROZEN 2026-09-23. Committed BEFORE any attack execution.**
**Scope:** red-team ONLY the interventional leg + admission law of V2-B
(PREREG_V2-B.md, frozen 2026-09-23). Not the sibling crew's build.
**Target mechanism (preregistered spec, §2):** program PASS iff (confG≥700)
AND (every Pi FAILs cleanly), FAIL_clean(Pi) = (j(Pi)≠jG) OR
(|measureG−measurePi| > 3σ_task); else UNRESOLVED. Install gate: WITHHOLD iff
jF≠jG; ADMIT iff jF==jG. INSTALL iff ADMIT AND program PASS. 3σ from the
committed `evidence/calibration_3sigma.json` (colordisc: 69 measure units).
**Front-end:** `src/vsense.zag` as committed (SHA256
cf4ffb43314650f1bba73b702c078475b8f32c755a99440f2f390c26d699a78e,
byte-identical to R2-4 `sense_r24.zag` — verified by Gap Crew C).
Perturbations are Gap Crew C's own byte-exact instances of the frozen
families (prereg §3): P1 channel-rotate (R,G,B)→(G,B,R); P2 rows
[h//3, 2h//3) zeroed; P3 XOR payload byte i with ((i*0x9E3779B9)>>16)&0xFF.
Deterministic; zero RNG anywhere.

## White-box facts used (from vsense.zag source)
- colordisc: 128×64 RGB; judgment from mean colors of left/right halves over
  sparse rows (rows%16∈{0,8}); DIFFERENT iff dE≥23.0 (milli-dE ≥2300);
  measure=(decm+50)/100; confidence=1000·|decm−2300|/(|decm−2300|+1500).
- conf≥700 requires DIFFERENT with dE≥58 (SAME maxes at 605).
- Dual-span .r24 = [magic,tcode] + F(8B wh+24576 RGB) + G(8B wh+24576 RGB).
  Single-span files (no magic) run as one span: used for F-only / G-only /
  P-only judgments.

## Truth convention for attack trials
`truth` = majority-pixel scene label of the crafted image (the R2A
convention: the fixture's scene label). The attacks paint the minority
sampled rows; a front-end judgment driven by those rows that contradicts
the scene label is WRONG (a spoof in the PAM sense: percept formed from
manipulated evidence).

## Attacks (all on colordisc; n per attack below)

### A. Sparse-row spoof + perturbation-reactive (iii × i — the kill shot)
Craft F and G (disjoint images): 56 of 64 rows uniform gray (scene SAME);
the 8 sampled rows (rows%16∈{0,8}): left half saturated red (255,0,0),
right half saturated green (0,255,0).
- Predicted: jF=jG=DIFFERENT, conf≥700, truth=SAME → WRONG high-conf.
- P1: left→blue, right→red; predicted residual |dE−dE'|≫0.69 → clean fail.
- P2: 3 of 8 sampled rows zeroed → large residual → clean fail.
- P3: structure destroyed → judgment flips to SAME → clean fail.
- **Predicted outcome: program PASS, admission ADMIT → INSTALL of a FALSE
  judgment.** Falsifies "intervention discriminates truth from spoof":
  the leg tests SENSITIVITY (reacts vs not), not TRUTH.
- n=12 trials (6 F/G background-gray pairs × 2 color orders).

### B. G-span gaming (ii — the "independent" holdout is gameable)
Same construction as A but F is a CLEAN truthful DIFFERENT scene (real
red/green halves, truth DIFFERENT, jF=DIFFERENT correct) while G is the
spoof from A (truth SAME, jG=DIFFERENT wrong).
- Predicted: jF==jG → admission ADMITs on a spoofed G; G judgments are
  attacker-chosen at will (white-box: the sparse-sampling hole exists in
  G exactly as in F — pixel-disjointness ≠ mechanism-independence).
- n=6 trials. Success = jG is the attacker-chosen WRONG judgment with
  conf≥700 (G fully driven).

### C. Liveness / weak-perturbation abuse (iv)
C1: uniform mid-gray images (truth SAME). Predicted: j=SAME conf≈605;
  P1/P2/P3 all leave judgment SAME with residual≈0 → program UNRESOLVED
  on every trial → install rate 0%.
C2: grayscale black/white halves (truth DIFFERENT, j=DIFFERENT conf≈985,
  CORRECT high-conf). P1 is the identity on R=G=B → never a clean fail →
  program UNRESOLVED despite a correct high-confidence percept.
- Predicted: C1 install rate 0/12; C2 program-PASS rate 0/12 (P1 blocks).
  An adversary (or a grayscale sensor) feeding perturbation-invariant
  inputs denies ALL installs — availability kill on RK-3.
- n=12+12.

### D. P1-evasive color class (i)
Grayscale images are EXACTLY invariant under channel rotation
((R,G,B)→(G,B,R) is the identity when R=G=B). For ANY grayscale input,
P1 can never clean-fail (judgment identical, residual exactly 0).
- Predicted: 12/12 grayscale trials → P1 not a clean fail (analytic +
  empirical). The P1 family is blind to a whole natural input class.

## Bars (deciding)
- **A-BAR:** ≥1 FALSE INSTALL through the full preregistered program
  (INSTALL of a judgment contradicting declared truth) → interventional
  leg FALSIFIED as a truth-discriminator (it is a sensitivity test).
- **B-BAR:** jG attacker-driven to a chosen wrong judgment with conf≥700
  on ≥5/6 trials → G-span "independence" provides no trust anchor vs a
  white-box attacker.
- **C-BAR:** install rate 0% on C1 and program-PASS rate 0% on C2 →
  liveness kill demonstrated (perturbation-invariant inputs deny service).
- **D-BAR:** P1 clean-fail rate 0% on grayscale → P1 family blind spot.
- Any attack trial that does NOT behave as predicted is reported as a
  miss with the observed vsense outputs (no hiding).

## Laws
Pure Zag for the gate/ledger/verification (`attack_gate.zag`: program,
admission law, memory-contract slot, sha256 hash-chain ledger).
Python only for span crafting (deterministic, no RNG), running the
compiled vsense binary, and analysis. Every attack binary run is
byte-identical across 3 reruns (B6-style check on the attack records).
The attack prereg is committed BEFORE execution; results in
`evidence/REDTEAM_V2-B.md`.

## Non-goals
Not testing the sibling crew's Python scorer or their exact P-bytes;
not testing other tasks/modalities; not building V2-B itself.
