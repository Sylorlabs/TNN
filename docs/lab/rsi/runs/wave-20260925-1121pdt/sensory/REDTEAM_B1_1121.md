# REDTEAM B1-BOUNCE-1121: second opinion on DISCARD

Wave: wave-20260925-1121pdt. Lane: sensory. Candidate: B1 BOUNCE
(two-bounce indirect illumination on the r8c land tiers, frozen k=384).
Prereg: PREREG_B1_1121.md, commit b2b2a3349. Implementation + evidence:
commit c91c88ff4. Verifier: b1/b1_verify.zag (pure Zag), committed binary
bin/b1_verify.

## Verdict: AGREE with DISCARD

I independently reproduced every number in the worker's table by
re-running the committed verifier binary against the committed BMPs.
The failures are genuine, wide-margin, and the bars were applied
honestly with no gaming. Three frozen bars fail:

- KB4a: measured mean per-channel |delta| 2.03 vs frozen floor 3.5
  (58% of floor, n=141,684 shadowed land pixels).
- KB4b: 17% of those pixels reach mean |delta| >= 3.5 vs frozen 25%.
- KB6: max 4-neighbor delta-field gradient 14 vs frozen cap 8
  (1.75x the cap).

My rerun output matched the committed evidence files exactly:
kb4_mean_x100=203, kb4_hit_frac_x100=17, kb4_max=17, kb6_maxgrad=14 for
k384; kb4_mean_x100=86, hit 2%, max 15, grad 7 for k192. Rerun hashes
also match EVIDENCE: var_r1 == var_r2 == ef32cd97..., k192 ==
fbb69aa2... . The visual reads check out: I inspected cmp_arch.png and
cmp_rim.png myself and the two halves of each side-by-side are
indistinguishable, consistent with a ~2/255 mean move and with the
worker's "no visible difference" note.

## 1. Knowledge vs architecture: the worker's story is correct, with one correction

I verified the root cause directly in the r8c source (b1_baseline.zag,
pass 3 land branch, lines ~965-982). For land pixels, pass 3 first
scales pigment by effective light, then adds a cool fill of
(120,140,190) scaled by shadow depth (dk*110/1024/1024), then applies
the aerial wash: lerp toward (198,168,148) with wash 210 in the upper
tier, 120 mid tier, 50 near tier. The wash runs AFTER the shadow
scaling, exactly as the worker's post-mortem says. So the failure is
both: a calibration error in the prereg (the 3.1 to 14.4 per-terrain
prediction was computed from pure dab constants and never accounted
for the wash or for blended pre-light albedos) and an architectural
fact (pass 3 spends the shadow-color budget inside the light pass, so
a post-pass recolor fights the wash and loses).

Correction to the worker's framing: the EVIDENCE post-mortem calls
this "architecture, not a data gap." The calibration error part IS a
data gap, just not a missing-data gap: the prereg calibrated against
the wrong data (dab constants) instead of the actual base render's
pixel statistics. The lesson the worker recorded, "calibrate
effect-size bars against the actual base render's pixel statistics
with a probe program, never hand arithmetic on dab constants," is the
right lesson and I endorse it as banked knowledge. The worker's
further claim, that a bounce with real headroom would have to live
INSIDE the light pass replacing the flat fill and wash, is plausible
but untested speculation; it is recorded as a hypothesis, not a
finding, and pursuing it needs its own prereg.

## 2. Metric gaming and bar weakness: bars were weak in principle, honest in fact

Attack: were the frozen bars the right bars, and could they be gamed?

The verifier (b1_verify.zag) implements the frozen bars faithfully. I
read the full source. KB4a checks kb4_sum*100 >= 350*3*kb4_n, which is
exactly mean per-channel |delta| >= 3.5. KB4b's hit condition
sum3 >= 11 is integer-correct for per-pixel mean >= 3.5 (11/3 = 3.67,
the smallest integer threshold at or above 3.5; if anything stricter
than the frozen text). KB5 checks variance-numerator ratio >= 81/100,
which is exactly std ratio >= 0.90 squared. KB6 computes the max
forward-difference gradient of the per-channel |delta| field over all
pixels, matching the frozen definition. The KB4 population (land mask
from the copied world model, arch opening excluded, blurred sh > 512)
matches the prereg spec, n=141,684 in both reruns. The runner's static
checks (no Python, no RNG, k-constant-only diff between variants,
toolchain and substrate pins) all pass and I confirmed them
independently. No gaming detected anywhere: the passing bars (KB1,
KB2, KB3, KB5, KB7) pass structurally and honestly.

But the KB4 bars are weaker than they look. They measure magnitude,
not direction. A dishonest worker could have passed every bar with a
flat +4 tint over the KB4 population: KB4a mean would be 4.0 >= 3.5,
KB4b 100%, KB4c 4 <= 80, KB6 edge gradient 4 <= 8 (the delta field of
a constant tint has zero interior gradient and a 4-unit step at the
land-mask edge), KB3/KB5 unchanged, KB1/KB2/KB7 trivial. A flat tint
carries zero indirect-illumination content, so the frozen KB4 bars do
not encode the candidate's actual goal (spatially varying color from
the scene's own albedo). The worker did not exploit this. Future
preregs for recolor mechanisms should add a direction bar, for
example correlation of the delta field with the bounce field, so a
magnitude-only cheat cannot pass.

Is KB4's floor reachable by ANY post-pass recolor on this substrate?
Yes, as the flat-tint counterexample shows. So this is NOT a DF-1
joint-unsatisfiability of the bar set. What IS jointly unsatisfiable
is KB4a + KB6 within this mechanism's one-parameter family. From the
two measured points, (k=192: mean 0.86, grad 7) and (k=384: mean
2.03, grad 14), linear interpolation gives mean(k) approx
0.86 + (k-192)*0.00609 and grad(k) approx 7 + (k-192)*0.03646. KB4a
needs mean >= 3.5, which requires k >= ~625, at which grad ~= 22.8 >
8. KB6 needs grad <= 8, which requires k <= ~219, at which mean ~=
1.02 < 3.5. The gap is wide (roughly 3x on both axes), so no k in this
mechanism class can satisfy both bars even under generous
interpolation error. The deeper kill reason, which the worker's
recommendation reaches for but does not state this precisely: the
frozen mechanism cannot be tuned into a pass; its effect is too weak
to see and its hard gate edges too sharp to legalize, and the tuning
knob couples the two. A softened-gate, higher-k redesign might break
the coupling, but that is a different mechanism and needs its own
prereg. DISCARD stands on this deeper reason as well.

One more bar note: KB6 as frozen is single-worst-pixel
hypersensitive (max over ~1M pixels). The measured 14 comes from hard
on/off switches (luma gate >= 24, sky/land mask), and the worker's
crops plus my own inspection show nothing visible there. The failure
is legitimate under the frozen definition, and frozen is frozen, but
future preregs may want a percentile-based or boundary-aware edge bar
rather than a global max, so that a single mask pixel cannot kill an
otherwise clean candidate.

## 3. Provenance: B1 is genuinely new

Spot-check greps over docs/lab/rsi/runs (*.md, all waves) for bounce,
ambient light, color bleed / colour bleed, indirect illumination,
global illumination, and albedo return zero hits outside this wave's
b1 directory. The prereg's prior-art claim holds. The mechanism code
matches the frozen spec: the only differences between b1_bounce.zag
and b1_k192.zag are the k constant (384 vs 192) and its trace string,
exactly 4 diff lines. The mix formula is 384*sh/1024/1024 with
below/above albedo samples at y +/- 192, the luma gate at 24, the
PASS 3B trace block is present, and the decision count reads 270
(variant) vs 269 (baseline). Nothing in the sealed queue was touched;
no prior candidate's code, renders, or constants are reused.

## 4. Verdict check: AGREE with DISCARD, with a refined kill reason

The worker's DISCARD is correct and I do not change it. The frozen
verdict mapping makes PARTIAL unavailable and no bar may be moved
this wave. My refinement of the kill reason:

1. Primary: KB4a/KB4b fail with margin (2.03 vs 3.5; 17% vs 25%) and
   the effect is sub-visible, confirmed by independent rerun and by
   my own inspection of the committed comparison crops.
2. Structural: KB6 fails (14 vs 8) at hard gate/mask discontinuities,
   and the k-knob couples effect size to edge gradient, so no
   setting of the frozen mechanism can jointly satisfy KB4a and KB6
   (k >= ~625 needed for KB4a gives grad ~= 23; k <= ~219 needed for
   KB6 gives mean ~= 1.0).
3. Knowledge: the prereg calibrated effect size against dab constants
   instead of base-render pixel statistics; the aerial wash (up to
   210/1024 toward (198,168,148)) and the flat cool fill spend the
   shadow-color budget inside pass 3, leaving a post-pass recolor
   almost no headroom. Banked: probe the actual render statistics
   before freezing effect bars; consider inside-the-light-pass
   designs for future indirect-illumination work (new prereg only).

Not a DF-1: the bar set itself is jointly satisfiable (the flat-tint
counterexample), so the failure is the mechanism's, not the bars'.
The bars' weakness (magnitude without direction) should be repaired
in future recolor preregs, but it did not cause this verdict.

## 5. Commit order and Python checks

- Commit order: PASS. Prereg commit b2b2a3349 (2026-09-25 18:47:05
  UTC) contains ONLY PREREG_B1_1121.md. Implementation commit
  c91c88ff4 (2026-09-25 19:10:21 UTC) is the first commit touching
  sensory/b1/. Between the two, the only sensory-lane commit is
  c91c88ff4 itself; the sibling COMP-2 prereg (5bf152b35) is a
  different lane and does not affect the order check. Strict
  precedence holds.
- Python: PASS. No .py files anywhere in the lane dir. No 'python'
  token in any .zag source. run_b1.sh contains no python invocation
  (only its own static-check greps for the token). Nothing pushed;
  no reset, rebase, or merge performed.

## Anomalies (do not affect the verdict)

1. evidence/diffmap_k384.png and evidence/diffmap_k384_x20.png are
   byte-identical (confirmed with cmp). The "x20 amplified" diffmap
   is a duplicate of the unamplified one; the 20x amplification never
   happened or failed silently. EVIDENCE does not cite the diffmaps,
   so the verdict is unaffected, but a broken evidence artifact is
   committed and future waves should either produce the amplified
   version or drop the file.
2. The PNG crops (cmp_arch.png, cmp_rim.png, diffmaps) were produced
   outside run_b1.sh; no ffmpeg command is recorded anywhere in the
   lane dir. The visual reads are reproducible in principle because
   the BMPs are committed, but the exact crop commands are
   undocumented.
3. The .zag-cache directory and .zagd.semantic-ready file are
   committed inside b1/ (build byproducts). Harmless but noisy; the
   runner could exclude them next wave.

## Scope confirmations

Micah's frontier files untouched. None of the six governance rulings
touched. Sealed judge queue untouched (R9, C1, C2v3, S11-IMG, C12,
S11-AUD, S13, S14, whirlpool-planform all undisturbed). No judge pair
prepared, as the prereg requires. No push, no reset, no rebase, no
merge; single local commit of this file only.

## Recommendation to the parent

Accept DISCARD for B1. Bank two pieces of knowledge: (a) on the r8c
substrate, pass 3's aerial wash plus flat cool fill spend the
shadow-color budget, so post-pass recolor mechanisms get ~2/255 mean
effect at honest mixes; (b) calibrate effect-size kill bars against
the actual base render's pixel statistics with a probe program, never
hand arithmetic on dab constants. Flag the diffmap duplicate as a
harness hygiene issue, and consider a direction bar (e.g. delta-field
vs bounce-field correlation) for future recolor preregs so that
magnitude-only cheats cannot pass KB4.
