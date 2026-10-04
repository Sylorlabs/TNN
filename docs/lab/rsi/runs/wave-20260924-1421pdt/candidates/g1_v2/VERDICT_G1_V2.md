# VERDICT_G1_V2.md - G1 SUNSHAFTS re-freeze, wave-20260924-1421pdt

Verdict: DISCARD

Frozen verdict mapping applied: READY-FOR-JUDGE requires the geometric
validator to pass AND every frozen kill bar KB1..KB8 to pass as specified;
any bar failed maps to DISCARD. No bar was weakened, narrowed, or
re-interpreted to force a pass. No sealed A/B pair and no JUDGE_BRIEF.md
were prepared (those exist only on a clean pass). Nothing enters the judge
queue.

## What was built (implementation order per prereg)

1. Prereg frozen and committed alone first: commit 1d8d40013
   ("wave-20260924-1421pdt: freeze G1 sunshafts re-freeze prereg"),
   docs/lab/rsi/runs/wave-20260924-1421pdt/preregs/PREREG_G1_SHAFTS_1421.md.
2. Vendored substrate: candidates/g1_v2/sub/R33_NATIVE_IO_V1.zag, byte copy
   of the committed file, sha256
   e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8.
3. Baseline FIRST: candidates/g1_v2/r8c_baseline.zag is a byte copy of
   docs/lab/imagination_discovery/img/r8c_alien.zag with only the @import
   line repointed. Rendered BMP sha256
   e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d,
   the frozen S14-record baseline hash. Gate PASSED. No substitution.
4. G1 v2 mechanism: candidates/g1_v2/g1_sunshafts_v2.zag. New pass
   g1_pass_sunshafts runs after r8c_pass3, before r8c_pass4. Frozen
   constants used verbatim: sun S=(110,300), validated 76px above the
   ridge line; D(x,y)=r8c_fbm(x*256/520, y*256/180, 9131, 3); jitter
   r8c_h01(x,y,9132+k)/64-8 and r8c_h01(y,x,9133+k)/64-8; N=12;
   T=mean(1024-D) over the march (march factored into g1_transmittance,
   same math as 1121pdt); sun color (255,172,112), clamp 255, sky-only.
   Recalibrated gate per the frozen procedure: pass A marches every sky
   pixel on the rebuilt baseline and measures mean_T and std_T, then
   G = mean_T + std_T + std_T/2 (1.5 sigma, frozen margin); pass B
   applies L=max(0,T-G)*90/(1024-G). The binary prints
   "G1 shafts: N=12 sky_px=325786 gate=707" and writes G1.1..G1.8
   decision lines to the elaboration trace.
5. Geometric validator: candidates/g1_v2/g1_validate.zag (pure Zag).
   Verifier: candidates/g1_v2/g1_verify_v2.zag (pure Zag). Runner:
   candidates/g1_v2/run_g1v2.sh (bash only). Pre-freeze geometry probes
   kept as candidates/g1_v2/probe/probe_geo.zag and probe_sets.zag;
   post-run lift characterization as probe/probe_lift.zag.
   Toolchain pinned: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
   sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
   verified before use.

## Both 1121pdt defects were repaired

- Defect 1 (geometrically defective point set): the runtime geometric
  validator passes every frozen check: V1 sun 76px above the horizon
  (margin >= 40 required), V2 sun tier_at == 0, V3/V4/V5 every kept
  WEDGE/OFFWEDGE/RADCUT point tier_at == 0, V6 keep counts 39/48/64/24
  against asserts 36/36/56/16. The runner diffs the validator and
  verifier *_KEPT lines: all four identical. KB2/KB3/KB5/KB7 were fully
  evaluable this wave.
- Defect 2 (miscalibrated T-gate): the recalibration ran as frozen.
  Measured on the rebuilt baseline: mean_T=569, std_T=92, gate=707.
  Lifted sky pixels: 3651 of 325786 (11 per mille, about 1.1 percent),
  versus 97.14 percent washed at the hardcoded gate 400 in 1121pdt.
  The broad sky wash is gone: full-frame off-wedge mean|dL| is 0.00.

## Per-bar results

| Bar | N=12 measured | Frozen bar | Result |
|-----|---------------|------------|--------|
| KB1 determinism (3 reruns) | 8076028d9031618544c6986dc6c4ddd12408add53afdf82dac7801c14b8c3bea x3 identical | identical | PASS |
| KB2 shaft ratio (WEDGE) | 1.0000 | >= 1.12 | FAIL |
| KB3 var(dL) (WEDGE) | 0.00 | >= 60.0 | FAIL |
| KB4 terrain mean\|dL\| | 0.00 | <= 1.0 | PASS |
| KB5 off-wedge mean\|dL\| | 0.00 | <= 6.0 | PASS |
| KB6 acutance ratio | 1.0000 (base 472, var 472) | <= 1.10 | PASS |
| KB7 max\|2nd diff dL\| (RADCUT) | 0 | <= 25 | PASS |
| KB8 cost (variant vs baseline) | 1948ms avg vs 957ms (2.04x) | <= 3x (2871ms) | PASS |

## Killing evidence

KB2 and KB3 fail: not a single one of the 39 validated wedge points
receives any lift (dL = 0 at all of them; dL = 0 at the sun point too),
so the shaft ratio is exactly 1.0000 and the dL variance is exactly 0.
Post-run pure-Zag characterization of the variant BMP (probe_lift.zag,
evidence only, no tuning): 2238 sky pixels carry nonzero dL (the
remaining 1413 of the 3651 above-gate pixels quantize to L=0 under
integer math), max dL is 9 luma steps, and the lifted pixels form one
small blob with bbox x 888..1023, y 254..305, centroid (984,278): the
far right edge just above the ridge line, 870px from the sun.

Mechanism reading: the recalibrated gate confines the lift as designed,
but the march-mean transmittance rewards long line-of-sight alignments
through low-density corridors far from the sun, not fan-shaped shafts
radiating from it. The pixels whose march to (110,300) runs lengthwise
through a low-D corridor at y~280 lift faintly (max +9); the wedge fan
radiating from the sun intersects no such corridor. The result is a
faint bright patch at the frame edge, not crepuscular shafts, and the
frozen shaft detector correctly reports nothing. This is a mechanism
miss, not a freeze defect: both 1121pdt defects were repaired and the
bars were genuinely at risk.

## Red-team notes (for the coordinator)

1. No dropouts, black regions, crashes, or banding. Determinism holds
   across 3 reruns. Terrain, off-wedge sky, and acutance are untouched
   (KB4/KB5/KB6 pass with 0.00/0.00/1.0000). E3 rejection honored.
2. The gate formula mean + 1.5 sigma overshoots on this field: the T
   distribution's upper tail is thin (march-means regress hard), so the
   gate catches only 1.1 percent and even the max lift is +9 luma. A
   lower multiple would lift more, but nothing in the frozen evidence
   suggests the lift would then fall on the sun fan rather than on
   far-field line-of-sight alignments.
3. Structural observation for any future shaft work: T = mean(1024-D)
   over the full pixel-to-sun segment makes far pixels' T an average
   over long paths, so high-T pixels sit far from the sun where paths
   align with corridors. A line-of-sight clearance formulation (e.g.
   minimum D along the march) would concentrate the signal near the
   sun instead. That is a mechanism redesign, not a re-freeze, and is
   not decided here.

## Purity

Python contact: none. Static checks in run_g1v2.sh all pass: no .py
files in candidates/g1_v2/ or probe/, no python token in any authored
.zag source, no python invocation in the runner, no rand/time/clock
calls in sources. Generator, validator, verifier, analysis probes, and
/tmp scratch are pure Zag compiled with the pinned toolchain. The /tmp
build and probe binaries are ephemeral scratch; all durable evidence is
committed under candidates/g1_v2/.

## Files

- candidates/g1_v2/r8c_baseline.zag (baseline source)
- candidates/g1_v2/g1_sunshafts_v2.zag (variant source)
- candidates/g1_v2/g1_validate.zag, candidates/g1_v2/g1_verify_v2.zag
- candidates/g1_v2/run_g1v2.sh
- candidates/g1_v2/sub/R33_NATIVE_IO_V1.zag
- candidates/g1_v2/probe/probe_geo.zag, probe_sets.zag, probe_lift.zag
- candidates/g1_v2/bin/ (built binaries), candidates/g1_v2/evidence/
  (BMPs, traces, compile/run logs, validator/verifier outputs,
  wall-time record)

Nothing pushed to GitHub. Nothing written to LOOP_STATE.md. Nothing
surfaced to Micah; the coordinator owns the judge queue.
