# VERDICT_G1.md - G1 SUNSHAFTS, wave-20260924-1121pdt

Verdict: DISCARD

Frozen verdict mapping applied: ADOPT-QUEUED-FOR-JUDGE requires every
frozen kill bar KB1..KB8 to pass as specified; any bar failed or
unevaluable maps to DISCARD. No bar was weakened, narrowed, or
re-interpreted to force a pass. No sealed A/B pair and no JUDGE_BRIEF.md
were prepared (those exist only on a clean pass).

## What was built (implementation order per prereg)

1. Vendored substrate: candidates/g1/sub/R33_NATIVE_IO_V1.zag, recovered
   byte-identical from committed branch
   tnn-native-lab-wave-archive-20260923-2321pdt, sha256
   e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8.
   Arrangement matches wave-20260924-0521pdt (sub/ beside the sources,
   imported as ./sub/R33_NATIVE_IO_V1.zag).
2. Baseline FIRST: candidates/g1/r8c_baseline.zag is a byte copy of
   docs/lab/imagination_discovery/img/r8c_alien.zag with only the @import
   line repointed. Rendered BMP sha256
   e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d,
   the frozen S14-record baseline hash. Gate PASSED. No substitution.
3. G1 mechanism: candidates/g1/g1_sunshafts.zag (frozen default N=12),
   plus g1_n6.zag and g1_n24.zag which differ from it ONLY in the
   `fn g1_n()` return line (diff-verified). New pass g1_pass_sunshafts
   runs after r8c_pass3, before r8c_pass4. Frozen constants used
   verbatim: sun S=(82,532), D(x,y)=r8c_fbm(x*256/520, y*256/180, 9131, 3),
   jitter r8c_h01(px,py,9132+k)/64-8 and r8c_h01(py,px,9133+k)/64-8,
   T=mean(1024-D), L=max(0,T-400)*90/624, sun color (255,172,112),
   clamp 255, sky-only (tier_at==0). The density field is memoized in a
   full-resolution table (exact values, no formula change). The binary
   prints `G1 shafts: N=<n> sky_px=325786` and writes G1.1..G1.7 decision
   lines to the elaboration trace. Verifier: candidates/g1/g1_verify.zag
   (pure Zag). Runner: candidates/g1/run_g1.sh (bash only).
   Toolchain pinned: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
   sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.

## Killing evidence

The frozen verifier point-set asserts fail on exact geometry (computed
with the r8c world-model functions copied verbatim; cross-checked by an
independent probe before the verifier was written):

- WEDGE: kept 11 of 48, assert requires >= 36. FAIL. Root cause: the sun
  sits below the horizon (y=532 vs ridge ~315-450), so the rays' first
  1-2 steps land in the far-rim tier (tier 1, not sky), and the steep
  rays exit the frame within a few steps.
- OFFWEDGE: kept 28 of 48, assert requires >= 36. FAIL. Root cause: 20
  of the 48 points fall inside the gas-giant disc (tier 4).
- RADCUT: 10 readable kept of 24, assert requires >= 16. FAIL.
  Root cause: t=1..6 sit below the ridge line, t=17..24 have y<0
  (the ray exits the top of the frame).
- TERRAIN: kept 64 of 64, assert requires >= 56. PASS.

Because three of the four frozen asserts fail, KB2, KB3, KB5, and KB7
are UNEVALUATED as frozen: their point sets are invalid, so the bars
cannot be measured the way the prereg froze them. This is a prereg-spec
defect (point sets specified without validating against the world
model), not a candidate-mechanism failure. The mechanism was implemented
exactly as frozen. Per the mapping, unevaluable bars mean DISCARD.

## Per-bar results

| Bar | N=6 | N=12 (frozen default) | N=24 | Frozen bar | Result |
|-----|-----|----------------------|------|------------|--------|
| KB1 determinism (3 reruns) | n/a | 9f23b64c74d5c12df5ac2cd675a199132dc665e1350496108682e2d937fcbbd0 x3 identical | n/a | identical | PASS |
| KB2 shaft ratio | (info 1.3173) | (info 1.2644) | (info 1.2460) | >= 1.12 | UNEVALUATED (WEDGE assert failed) |
| KB3 var(dL) | (info 232.06) | (info 197.15) | (info 199.60) | >= 60.0 | UNEVALUATED (WEDGE assert failed) |
| KB4 terrain mean\|dL\| | 0.32 | 0.12 | 0.25 | <= 1.0 | PASS |
| KB5 off-wedge mean\|dL\| | (info 61.00) | (info 56.28) | (info 54.46) | <= 6.0 | UNEVALUATED (OFFWEDGE assert failed) |
| KB6 acutance ratio | 0.9978 | 0.9809 | 1.0190 | <= 1.10 | PASS |
| KB7 max\|2nd diff dL\| | (info 11) | (info 5) | (info 6) | <= 25 | UNEVALUATED (RADCUT assert failed) |
| KB8 cost (variant vs 3x baseline) | 1460ms | 1613ms avg | 1870ms | <= 3x957=2871ms | PASS (1.69x) |

INFO values are measurement-only over the kept points, not bar
evaluations. Baseline wall: 957ms. sky_px marched: 325786 (all N;
matches the binary's own count). N=12 ops: 1048576 density fbm evals,
3909432 march steps. Variant BMP hashes: N=6
61371fe4f5d2b688cbd333c34a3085676c55b5a5ee2b7d3f23ead6750c682dfb,
N=24 87e1c43730e78c9a929c906ca3cb5c03c3827b68369dbd6a513d9a82c0a256fb.

## Red-team findings (knowledge vs architecture)

1. The frozen lift gate does not produce confined shafts. Full-sky
   measurement (N=12, pure-Zag analysis): 97.14% of sky pixels lifted,
   mean dL +33.07 luma steps, max dL 69. The field's mean transmittance
   (~511) sits well above the frozen gate (400), so "above-average"
   includes nearly the whole sky. Visually the variant is a broad sky
   brightening/wash, not distinct crepuscular shafts. Had KB5 been
   evaluable it would have failed decisively (56.28 vs 6.0). Knowledge
   gap: the frozen threshold is miscalibrated relative to the field mean;
   the march/transmittance machinery itself works as specified.
2. No dropouts, black regions, crashes, or banding: max second
   difference on the readable RADCUT cut is 5 (N=12), and the renders
   are byte-identical across reruns.
3. Giant and moon discs correctly excluded from the lift; terrain mean
   |dL| is 0.12 (KB4). Pass-4 fixations diverge downstream of G1 by
   frozen design (fixations read the canvas, so they respond to the
   shafts); the terrain impact stays inside the KB4 bar.
4. Acutance unchanged (KB6 PASS): no grain added, E3 rejection honored.

## Recommended follow-up (for parent, not decided here)

File a prereg addendum with geometrically validated point sets (wedge
rays starting above the ridge line, off-wedge set avoiding the giant
disc, RADCUT confined to the in-frame sky segment) and, if localized
shafts are desired, recalibrate the T-gate against the field's measured
mean transmittance. G1 is not adopted and not queued for judge this wave.

## Purity

Python contact: none. Static checks in run_g1.sh all pass: no .py files
in candidates/g1/, no python token in any authored .zag source, no
python invocation in the runner, no rand/time/clock calls in sources.
Generator, verifier, analysis, and /tmp scratch are pure Zag compiled
with the pinned toolchain. ffmpeg was used only to render viewable PNG
copies (base.png, var_n12.png) for the visual red-team check; all
recorded numbers come from the Zag binaries.

## Files

- candidates/g1/r8c_baseline.zag (baseline source)
- candidates/g1/g1_sunshafts.zag (N=12), g1_n6.zag, g1_n24.zag
- candidates/g1/g1_verify.zag, candidates/g1/run_g1.sh
- candidates/g1/sub/R33_NATIVE_IO_V1.zag
- candidates/g1/bin/ (built binaries), candidates/g1/evidence/ (BMPs,
  traces, compile/run logs, verifier outputs, wall-time record)

Nothing committed, nothing pushed, per task orders.
