# RED-TEAM REVIEW: wave-20260924-0521pdt (independent second opinion)

Reviewer: red-team subagent. Date: 2026-09-24. Working copy:
~/workspace/tnn-rsi, branch tnn-native-lab. This review used shell,
grep, and file reads only. No Python was used in this review.

Scope: three worker verdicts (second judgment path part C, D-VID-1 V2,
C-D19 focus-plane detail). Each candidate's prereg, implementation,
evidence, verdict, and red-team file were read in full and attacked
independently. Numbers below are recomputed from the committed
sources, not quoted on trust.

## Global: prereg commit-order self-check

| Candidate | Prereg | Implementation | Verdict | Order |
|---|---|---|---|---|
| Second path part C | 7a0f69b62 (12:37:13 UTC) | 6a61b8f4f (13:54:17 UTC) | same commit | PASS, prereg strictly precedes implementation |
| D-VID-1 V2 | 840d54e6c (12:34:02 UTC) | addendum 8767a005a (12:48:11 UTC), impl/verdict a7c695590 (13:21:14 UTC) | same commit | PASS, prereg < addendum < implementation |
| C-D19 | 35f81a256 (12:49:18 UTC) | f26e277da (13:04:29 UTC) | cc48ae52a (13:04:46 UTC) | PASS, strict order holds |

All three commit-order self-checks PASS.

---

## CANDIDATE 1: second judgment path part C

Worker verdict: DISCARD. Prereg
docs/lab/rsi/runs/wave-20260924-0521pdt/preregs/PREREG_SECONDPATH_PARTE_0521.md.

**RED-TEAM: AGREE with DISCARD. Tag: [NEW].**

### Attack (a): independence fraud

Attacked by static audit of the committed judge4.zag and driver4.zag.

- The path-B section of judge4.zag starts at the PB-IND banner
  (line 826). Every f0_fast / f0_robust / autocorr token in the file
  lies in the path-A KB4V2 section above it; the path-B section
  contains zero such tokens except in its own independence comments.
- T4 path B (j_pitchdisc2) computes f0 via b4_f0_goertzel, a
  Goertzel-bank harmonic peak picker built on b4_dft_energy and the
  independent Taylor sine b4_sin1024. No lag-domain computation, no
  shared autocorrelation buffer, no f0 estimate passed in.
- T5 path B (j_timbredisc2) takes no f0 input: it calls b4_balance,
  the spectral centroid on the fixed 100..8000 Hz grid, and maps to
  labels with the frozen 506 / 712 / 1463 Hz thresholds.
- Lineage audit: both path-B judgments take raw fixture bytes plus
  sample rate and offsets. No path-A feature crosses the boundary.
  driver4.zag runs path B on the candidate arm only, identically on
  all variants, and never lets it vote, rank, or touch the baseline
  arm.

PB-IND PASS is upheld. No independence fraud found.

### Attack (b): the disclosed Python deviation ([VOID] vs [NEW])

The worker disclosed that python3 edited /tmp/spc/probe_b.zag twice
(a development scratch for the Goertzel bank). The wave artifacts
(judge4.zag, driver4.zag, the committed evidence) were never
Python-touched. The prereg's own no-Python clause covers wave
artifacts; the owner's red line is stricter ("no Python anywhere in
loop work"), and the S7 precedent voided SHAPED-MEMBERS when Python
generated /tmp debug sources.

Decision: **DISCARD stands on the measured evidence. Tag [NEW], not
[VOID].** Reasons:

1. The killing evidence is the structural veto arithmetic plus the
   measured SP-B1 (1891 bp vs the frozen bar strictly below 1842 bp).
   The Python contact touched only the path-B development scratch.
2. The kill is provably immune to any contamination of path B:
   with 0 false T4/T5 adversarial installs (PA-B1 = 0, T5 cand
   adversarial accuracy 10000 bp), a veto can only remove installs.
   Even a perfect Goertzel bank (0 disagreements) yields 7/38, which
   is not strictly below the bar. Even a worthless one fails harder.
   No property of the Python-assisted component can change the
   verdict.
3. The SP-B1 measurements come from the pure-Zag driver4.zag and the
   committed summaries; the contamination path from the scratch probe
   to the veto ledger does not exist.

This is a narrow immunity exception, stated explicitly: the verdict
survives only because its killing evidence is structurally
independent of the contaminated work. The worker's "letter vs spirit"
framing must not become precedent. Recommendation below.

### Attack (c): PB-AGREE denominator

Measured: pb_agree_disagree_primary_t45 = 1, pb_agree_n_primary_t45 =
120, pb_agree_disagree_bp = 83. The denominator is the frozen fixture
set: 60 primary fixtures in t4_pitchdisc/primary plus 60 in
t5_timbredisc/primary (each dir holds 120 entries because every
.pcm has a .truth sidecar). 1/120 = 83 bp against the frozen 500 bp
budget. PASS with large margin; no denominator manipulation could
flip this bar.

### Attack (d): commit order

7a0f69b62 (12:37:13 UTC) strictly precedes 6a61b8f4f (13:54:17 UTC).
PASS.

### Attack (e): structural kill and hypothesis-class closure

Recomputed from the committed evidence/summary_run2.txt:
cand_adv_false = 7, cand_adv_installs = 37, cand_adv_fir_bp = 1891;
the pinned bar is 7/38 = 1842 bp, strictly below required.

The worker's arithmetic is confirmed: the single adversarial veto
withheld a true install (p006.pcm), moving FIR from 7/38 to 7/37.
With 0 false T4/T5 adversarial installs, no veto-only mechanism over
T4/T5 can remove a false install; it can only remove true installs
(FIR rises) or never fire (FIR = 7/38, equal, not strictly below).
The bar is unsatisfiable by construction for this mechanism class on
this substrate.

The kill generalizes to a class closure (the SHAPED S11 pattern): a
veto-only second path cannot improve adversarial FIR whenever the
residual falses lie outside the vetoed tasks. The evidence supports
closing the veto-only-on-T4/T5 slot for FIR improvement on the KB4V2
substrate. Reopening requires either residual falses inside the
vetoed tasks (for example a veto that targets T2 colorconst, where
the 7 falses live) or a changed residual distribution. Revisiting
the SP-B1 bar definition to permit equality would be weakening a
frozen kill bar and is rejected.

### Attack (f): SP-B2 at exactly 8486 bp

cand_primary_mean_bp = csum/6 where each task term is rate_bp =
floor(10000*k/n). Floors only, no rounding up anywhere: the measured
8486 is a lower bound on the true mean, and it is exact
(50916/6 = 8486). Bar >= 8486 bp. PASS confirmed, no rounding games.

### Other bars

PB-DET (3/3 identical sha256), PA-B1 (0), PA-B2 (baseline arm
untouched), SP-B3 (3/3 identical), SP-B4 (1017190050 <= 1034717556),
SP-B5 (3000 bp >= 1621 bp) all confirmed PASS from the committed
summaries. The sole miss is SP-B1, and the frozen verdict mapping
mandates DISCARD on any bar miss.

### Hygiene flags (non-verdict)

- VERDICT_SECONDPATH_PARTE_C.md still carries the placeholder
  "Implementation: [to be committed]"; the actual commit is
  6a61b8f4f. Cosmetic only.
- The verdict's claim that all 7 falses are in T2 colorconst is
  consistent with the frozen 2021pdt record (T4/T5 residual 0) and
  with 0 false T4/T5 adversarial installs here, but the exact
  task location is not load-bearing for the kill.

---

## CANDIDATE 2: D-VID-1 V2

Worker verdict: DEAD, self-voided. Prereg
docs/lab/rsi/runs/wave-20260924-0521pdt/preregs/PREREG_DVID1_V2_0521.md,
addendum committed at 8767a005a (frozen before coding).

**RED-TEAM: AGREE with DEAD. Tag: [VOID].**

### Attack (a): self-void completeness

The VKB5 frozen rule: "no Python anywhere in loop work. Any Python
touch of a new wave artifact voids its wave evidence." A python3
heredoc edited v2_verify.zag mid-wave; the file was later rebuilt
Python-free, but the touch stands. The worker voided the wave
evidence (SHA256SUMS_V2.txt, VERIFY_OUT.txt, all measurements) and
labeled them VOID in the verdict. The self-void is correctly and
completely applied: the verdict presents no measurement as
non-void, and VKB1 was correctly not performed on void evidence.

What survives the void: the generator ocean_dvid1_v2.zag was never
Python-touched (committed in a7c695590), and the technical kill can be
re-derived analytically from committed formulas alone (see (b)). The
DEAD verdict is therefore over-determined: the governance kill and
the technical kill are independent, either one sufficient.

### Attack (b): independent re-derivation of the bfade = 0 no-op

Re-derived from committed sources (analytic, no Python, no probes):

1. Baseline formula (inherited verbatim into the V2 generator,
   ocean_dvid1_v2.zag line 455):
   bfade = o_clamp01k((200 - wz) * 1000 / 140). For any pixel with
   wz >= 200, (200 - wz) <= 0, so bfade = 0.
2. Vortex geometry (o_scene): o_vwz = 720 + (o_vn3(...) - 500) *
   100 / 1000, so vwz lies in [670, 770]. The influence disc is
   r < 160, so disc wz lies in [510, 930], entirely above 200.
   Therefore bfade = 0 everywhere in the disc.
3. Every term the V2 co-rotating block retargets is gated by bfade:
   bupm = o_mix(1000, ..., bfade) = 1000 when bfade = 0;
   abupm likewise (computed but never applied, dead code in both
   arms); the sbup streak multiplier is 1000/1000 = 1. The
   co-rotating sampling coordinates (cx, cz) are multiplied out.
4. The bfade2 fine-shading block (nonzero in the disc) was not
   modified by V2 and contributes identically to both arms.

Conclusion: the V2 transform is a proven no-op in the vortex disc.
Disc pixels are identical baseline vs variant, so any disc-based
metric (including T1) must be exactly equal. The reported T1
A_pm = B_pm = 498 (bar <= 0.7*A = 348, i.e. 348) is exactly what the
analytic result predicts. The mechanism hypothesis (disc foam churn
comes from breakup sampled in translating coordinates) is wrong at
the source: there is no breakup modulation in the disc to fix.

Note: the empirical pixel-level proof (0/5024 differing cells) was
computed with voided or uncommitted machinery and cannot be cited as
wave evidence. It is immaterial: the analytic derivation above is a
theorem about the committed shader and suffices on its own.

### Attack (c): the addendum inverse defect

Confirmed. The addendum's forward transform applies the inward-drift
law (cx = qx * inw / 1000 + vwx), but its claimed inverse maps the
grid through inverse rotation only, omitting the * 1000 / inw
division. The worker disclosed this. It is immaterial to the verdict:
given the bfade = 0 no-op, the defective inverse cannot change any
measured outcome. A future wave must re-freeze the inverse correctly;
it must not silently repair it in implementation.

### Attack (d): "terminate this lane"

AGREE. This is a mechanism-level death, not a candidate-level miss.
Any V3 that retargets breakup sampling coordinates for disc foam
churn would hit the same bfade = 0 wall. The D-VID-1 foam-breakup
lane is closed. A future wave may target the actual disc churn
mechanism (geometry churn: arm and crest masks sweeping through the
rotating frame) only under a fresh prereg with a different mechanism
and metric.

### Attack (e): commit order

840d54e6c (12:34:02 UTC) < 8767a005a (12:48:11 UTC) < a7c695590
(13:21:14 UTC). PASS. The addendum was frozen before any V2
implementation file existed, satisfying the S8 addendum-first rule.

---

## CANDIDATE 3: C-D19 focus-plane detail

Worker verdict: DISCARD. Prereg
docs/lab/rsi/runs/wave-20260924-0521pdt/preregs/PREREG_C_D19_0521.md.

**RED-TEAM: AGREE with DISCARD. Tag: [NEW].**

### Attack (a): provenance honesty

- The D19 renders are new this wave: var1/var2/var3.bmp share
  sha256 30a9cd5c... (from the committed evidence/SHA256SUMS),
  all three byte-identical, first rendered in this wave.
- base.bmp reproduces the committed r8c baseline byte-identically
  (e4f65557...), declared as a rebuild, not presented as new.
- No recycled renders: S11-IMG, C1, C2v3, whirlpool, D15/R9,
  D17/S13, D18/S14 are not stacked into this variant; the prereg
  explicitly records them as QUEUED-UNJUDGED and untouched.
- The D14 fulfillment claim is legitimate: D14 is a frozen world
  decision ("detail will gather there" at (430,400)), and D19 is
  the first candidate to implement it. Fulfillment, not invention,
  and not a recycled judgment.

Provenance PASS. No render presented as new that is not new.

### Attack (b): metric gaming

Measured (from committed evidence/evidence_verify.txt):
KB2_FOCUS_BP = 11804 (bar >= 13000, FAIL), KB3_STONE_BP = 19027
(bar >= 12000, PASS), KB4_SKY_BP = 10000 (bar <= 11000, PASS),
KB5_MEANABS_X100 = 5 (bar <= 800, PASS). KB1-DET PASS (3/3
identical), KB6 PASS (208 dabs exact, 0.95x wall).

The frozen verdict mapping mandates DISCARD on any KB1..KB6 fail.
The PARTIAL clause requires KB2 and KB3 both to pass (with KB5
marginal or mild fringing); KB2 failed, so no PARTIAL escape
applies, and its narrowing direction (cutting alphas) would weaken
the already-weak focal effect anyway. The KB3 1.90x PASS does not
rescue a KB2 miss: one miss is DISCARD. The verdict mapping is
correctly applied.

### Attack (c): governance

- No Python contact: run_d19.sh carries its own static no-Python
  guards (no python files, no python token in comment-stripped
  sources, no python invocation in the runner); grep confirms the
  only "python" tokens are in those guards and a substrate comment.
  Pure Zag, zero RNG confirmed by the frozen static checks.
- Commit order: 35f81a256 < f26e277da < cc48ae52a, strict. PASS.

### Attack (d): is the kill numbers, not rhetoric?

Yes. The kill is KB2 = 1.18x vs the frozen bar >= 1.30x, a 0.12x
shortfall measured by the frozen verifier on the frozen 40-point
F3 set (points frozen in the prereg before any D19 code existed).
The "visually negligible at 1024px" language in the verdict and the
red-team crop review is corroboration, not the kill. The DISCARD is
mandated by the frozen mapping regardless of any visual reading, and
no sealed pair was prepared, correctly.

### Hygiene flag (non-verdict)

VERDICT_C_D19.md's KB1 row prints a mangled 59-character sha256
(30a9cd5c...093b0b146feb013a) that does not match the committed
evidence/SHA256SUMS (64 characters, ...093b0a9ab0b146feb013a).
The evidence file is authoritative; KB1-DET PASS (3/3 identical)
is unaffected. Fix the transcription in a follow-up doc commit.

---

## Standing-rule and lane recommendations

1. **Adopt: any Python contact anywhere in loop work, including
   /tmp scratch files, voids the wave evidence.** Candidate 1's
   DISCARD survives only under the narrow immunity argument (its
   killing evidence is structurally independent of the contaminated
   scratch work). The worker's "letter vs spirit" distinction must
   not become precedent. This aligns the standing rule with the
   owner's red line and the S7 void precedent.

2. **Close the veto-only second-path slot for FIR improvement on
   the KB4V2 substrate** (candidate 1 class closure). A veto-only
   mechanism over tasks with zero residual falses cannot improve
   adversarial FIR; the SP-B1 "strictly below" bar is unsatisfiable
   for that class. Reopen only if residual falses exist inside the
   vetoed tasks or the residual distribution changes. Do not weaken
   the bar to permit equality.

3. **Terminate the D-VID-1 foam-breakup lane** (candidate 2). The
   mechanism is dead at the source (bfade = 0 in the vortex disc);
   retargeting breakup sampling coordinates cannot affect disc foam.
   A future wave may address disc foam churn only via a different
   mechanism (geometry churn) under a fresh prereg.

## Summary

| Candidate | Worker verdict | Red-team | Tag | Commit order |
|---|---|---|---|---|
| Second path part C | DISCARD | AGREE | [NEW] | PASS |
| D-VID-1 V2 | DEAD (self-voided) | AGREE | [VOID] | PASS |
| C-D19 | DISCARD | AGREE | [NEW] | PASS |

No blockers. All three worker verdicts are upheld on their cited
numbers, verified against the committed sources.
