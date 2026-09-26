# ANOMALIES — Phase B2b (PREREG_LH §2b/§2c)

Format per prereg: ANOM-ID, DATE, HORIZON, OBSERVED, EXPECTED, CANDIDATES
(knowledge-first order), DISPOSITION.

---

**ANOM-ID:** ANOM-001
**DATE:** 2026-09-26
**HORIZON:** §2b prosody axis (scorer definition)
**OBSERVED:** Raw frame-level F0 CV on real speech is dominated by estimator
octave-jumps, not prosody: neutral EmoV speech reads cv≈1.09 raw / 1.00 with
f0>0 exclusion / 0.91 median-3 robust. Across pros40 targets raw cv spans
0.13–0.50 while robust spans 0.09–0.49; several clips drop 0.42→0.12 under
median-3 (isolated jump frames). scorer_p.py defines no prosody CV.
**EXPECTED:** "Scorer prosody CV" measures pitch variation of the reference.
**CANDIDATES:** (1) The prereg's "CV" is underdetermined — scorer_p has no
prosody definition; any choice is a freeze decision. (2) Estimator pathology
(octave errors, f0=0 "no estimate" flags) is a property of the measurement,
not the signal. (3) TNN cannot be at fault — the anomaly is in the judge.
**DISPOSITION:** Froze robust CV (median-3 over scorer-voiced f0>0 frames) in
scorer_ctrl.py BEFORE scored runs; TNN hears the same robust quantity
natively (median-3 over guard-voiced f0>0). Documented as prereg-noted
deviation. Raw-CV numbers retained in evidence for audit.

**ANOM-ID:** ANOM-002
**DATE:** 2026-09-26
**HORIZON:** §2b envelope axis
**OBSERVED:** The organ's env_class and the scorer's ans_env are the same
computation (thirds mean-rms ±4 dB; verified: organ
10·log10(ms/2^30) ≡ scorer 20·log10(rms/32768), integer-vs-float thirds agree
to <1 mdb vs the 4000 mdb gate). Render env therefore always scores what the
organ heard, by construction.
**EXPECTED:** An independent judge of TNN's envelope matching.
**CANDIDATES:** (1) The prereg named the organ's own quantity as the target
("scorer 3-class") with no independent manifest labels available. (2) Not a
TNN defect — the render path is faithful (calibration: rise/flat/decay all
correct).
**DISPOSITION:** Axis kept; reported honestly as a RENDER-FIDELITY test, not
a hearing test. Borderline clips (thirds diff within ~1 mdb of the gate) can
still disagree by truncation and are the only discriminating cases. Related:
the prereg's RC1 ≤25% bar vs ~33% chance agreement on a balanced 3-class
axis — addressed by choosing a maximally-mismatched frozen derangement
(env shift-by-1 on interleaved R/F/D: zero same-class pairs), the strongest
valid leniency test.

**ANOM-ID:** ANOM-003
**DATE:** 2026-09-26
**HORIZON:** §2b/§2c renderer (pre-run design)
**OBSERVED:** The wired 5-action renderer (QUERY/CONTINUE/NOTE_NEW/RECALL/
ATTEND) cannot emit continuous F0, shaped envelopes, or prosody — the control
battery is un-runnable with it.
**EXPECTED:** A renderer able to attempt the match.
**CANDIDATES:** (1) Vocabulary gap, not a TNN failure — the actions were
built for deliberation turns, not audio matching. (2) Extending the renderer
changes the system under test.
**DISPOSITION:** Minimal pure-Zag MATCH extension added (continuous F0,
flat/rise/decay, 5 Hz vibrato), zero RNG, documented as prereg-noted
deviation. The 5-action core is untouched.

**ANOM-ID:** ANOM-004
**DATE:** 2026-09-26
**HORIZON:** §2b prosody axis (vocabulary)
**OBSERVED:** Vibrato depth clamps at 0.5 (beyond is not vibrato); render CV
caps at ≈0.35. Refs with robust cv up to 0.49 exceed the vocabulary. (Hit
window is asymmetric: |0.35−cv|/cv ≤ 0.25 still hits up to cv≈0.46.)
**EXPECTED:** Full-range prosody expression.
**CANDIDATES:** (1) Genuine vocabulary ceiling of the MATCH extension.
(2) Could be raised with non-vibrato FM, but that leaves the "prosody"
construct.
**DISPOSITION:** Clamp kept and documented. Saturation misses are reported
as vocabulary limits, not hearing failures.

**ANOM-ID:** ANOM-005
**DATE:** 2026-09-26
**HORIZON:** §2c closed loop (dry run)
**OBSERVED:** Depth-0.5 vibrato on a 150 Hz tone biases the ORGAN's F0 reading
up ~19% (render at 150.1 Hz heard as 178.4 Hz; scorer reads 152.8 Hz —
the render is fine, the organ's hearing is biased). Low estimates trigger
the low-F0 guard path which re-estimates upward.
**EXPECTED:** The organ hears its own render veridically.
**CANDIDATES:** (1) Guard interaction with extreme FM — knowledge-first:
the guard was built for the sub-125 Hz blind spot, not FM tones.
(2) Not a render defect (scorer confirms the tone).
**DISPOSITION:** Kept as a real closed-loop phenomenon: the loop compensates
by rendering flat F0 lower (converged: heard 149.7/148.3 vs target 150.1).
Reported as a finding about the wired organ, not corrected (frozen organ).

**ANOM-ID:** ANOM-006
**DATE:** 2026-09-26
**HORIZON:** §2c target selection
**OBSERVED:** loop20 contains 5 low-F0-class cases, not the intended 4 —
one general candidate is also class lowf0.
**EXPECTED:** 16 general + 4 low-F0.
**CANDIDATES:** (1) Selection script detail (class overlap not excluded).
**DISPOSITION:** Reported honestly; the set stands (pre-run, deterministic).
If the prereg interpretation demands exactly 4, the 5th case is identified
in SELECTION.json (`loop_lowf0` list).

**ANOM-ID:** ANOM-007
**DATE:** 2026-09-26
**HORIZON:** RC0 design
**OBSERVED:** Severed renders are flat-envelope by construction, so RC0 env
hits ≈ P(ref is flat) ≈ 14/40 = 35% — the null is not 0%.
**EXPECTED:** (none — null behavior documented)
**CANDIDATES:** (1) Flat is the natural default render.
**DISPOSITION:** Reported; the permutation test (wired vs severed) accounts
for the non-zero null.

**ANOM-ID:** ANOM-008
**DATE:** 2026-09-26
**HORIZON:** RC0 execution
**OBSERVED:** First rc0 launch passed `1` as the sever argument; the binary
expects the literal token `sever` (streq(_zag_arg(5),"sever")). The run
proceeded wired (journal: `sever=0`).
**EXPECTED:** Severed null run.
**CANDIDATES:** (1) Operator error — harness arg convention not checked.
**DISPOSITION:** Run killed, partial outputs deleted, relaunched with the
correct token (journal confirms `sever=1`). No contamination: the killed
run's outputs never entered analysis.

**ANOM-ID:** ANOM-009
**DATE:** 2026-09-26
**HORIZON:** §2b prosody axis (RC1 scorer validation)
**OBSERVED:** RC1 frozen derangement (cyclic shift-20) yields 11/40 = 27.5%
hits on prosody, exceeding the 25% bar. The scorer is VOID for prosody
(per prereg: voids the scorer, not the trial).
**EXPECTED:** Deranged hit rate ≤25% (scorer discriminates true matches).
**CANDIDATES:** (1) The ±25% CV hit criterion is too lenient for the
prosody40 CV range (0.094–0.487) — deranged pairs fall within tolerance by
chance. (2) The shift-20 derangement, while maximally mismatched by minimum
distance (0.26), does not guarantee all pairs exceed 25%. (3) Robust CV
measurement noise contributes.
**DISPOSITION:** Scorer void for prosody. The 29/40 = 72.5% control hit rate
is reported but cannot be certified. Pitch (0%) and envelope (0%) RC1 pass;
their scorers remain valid.

**ANOM-ID:** ANOM-010
**DATE:** 2026-09-26
**HORIZON:** Run infrastructure
**OBSERVED:** VM rebooted at ~07:44 UTC (uptime 5 min on check). r2 (159/160)
and rc0 (154/160) processes killed mid-target; no done.txt. r1/r3 had
completed and flushed. Journals intact to last RENDERED.
**EXPECTED:** All runs complete.
**CANDIDATES:** (1) Infrastructure failure (host reboot), not a code defect —
r1/r3 completed deterministically. (2) No evidence of OOM (no dmesg access).
**DISPOSITION:** r1/r3 byte-identical proven (2×). r2 matches r1 on 159/160.
rc0 has all 120 control targets (1–120); missing 155–160 are repeats,
irrelevant for RC0. Reported honestly; determinism established.
