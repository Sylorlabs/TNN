# VERDICT_G1_V3.md - G1 SUNSHAFTS v3, wave-20260924-1721pdt

Verdict: DISCARD

Frozen verdict mapping applied: READY-FOR-JUDGE requires the baseline
byte-identity gate AND the geometric validator AND every frozen kill bar
KB1..KB8 to pass as specified; any gate, validator check, or bar failed
maps to DISCARD. No bar was weakened, narrowed, or re-interpreted to
force a pass. No sealed A/B pair and no JUDGE_BRIEF.md were prepared
(those exist only on a clean pass). Nothing enters the judge queue.

## What was built (implementation order per prereg plus addendum)

1. Prereg frozen and committed alone first: commit acf7cedce
   ("wave-20260924-1721pdt: freeze G1 sunshafts v3 prereg
   (directional-contrast fan selection)"),
   docs/lab/rsi/runs/wave-20260924-1721pdt/preregs/PREREG_G1_SHAFTS_1721.md.
2. Sign-correction addendum committed alone second: commit 1da140387
   ("wave-20260924-1721pdt: G1 v3 prereg addendum, clarity-gate sign
   correction (S10)"). The addendum quotes the coordinator decision
   verbatim: the prereg's clarity-gate formula and prose described
   opposite gates, and the PROSE-INTENDED reading was adopted, freezing
   s'(P) = (T(P) - BMEAN_T[b])*1024/BSTD_T[b] with SGATE = 1152 (the
   measured quantile, about 10 percent by construction). Runner-verified:
   the addendum is a descendant of the prereg commit (commit-order
   discipline held).
3. Vendored substrate: g1/sub/R33_NATIVE_IO_V1.zag, byte copy of the
   committed file, sha256
   e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8.
4. Baseline FIRST: g1/r8c_baseline.zag is a byte copy of the 1421pdt
   baseline source (sha256 99fc62b9... identical). Rendered BMP sha256
   e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d,
   the frozen S14-record baseline hash. Gate PASSED. No substitution.
5. G1 v3 mechanism: g1/g1_sunshafts_v3.zag. New pass
   g1v3_pass_sunshafts runs after r8c_pass3, before r8c_pass4. Frozen
   constants used verbatim: sun S=(110,300); D(x,y) fbm seed 9131;
   N=12; R_MIN=24; K=7 fan with plus or minus 144 px lateral spread;
   sunward ray uses the exact g1_transmittance march and jitter seeds;
   flank rays use seeds offset by 64*m; band means/stds and SGATE=1152
   from the phase-1 measurement; delta(P) > 0 strict angular minimum;
   L = 90*delta/(delta+1024) in sun color (255,172,112), clamp 255,
   sky-only. Frozen evaluation order with short-circuiting: sky/r check,
   sunward march plus clarity gate, fan marches only for gate passers,
   delta predicate, then lift. The binary prints
   "G1v3 shafts: N=12 K=7 gated_px=323997 clarity_pass=28476
   delta_pass=2805 lifted_px=2805" identically on all three runs.
6. Geometric validator: g1/g1_validate.zag, byte copy of the 1421pdt
   validator (sha256 ef418915... identical), carried over verbatim per
   the prereg. Verifier: g1/g1_verify_v3.zag, the v2 verifier with only
   cosmetic label updates (bars and point sets unchanged,
   mechanism-independent). Runner: g1/run_g1v3.sh (bash only), with the
   clarity tripwire (pass fraction within 50..150 per mille).
   Toolchain pinned: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
   sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
   verified before use.

## Per-bar results

| Bar | v3 measured | Frozen bar | Result |
|-----|-------------|------------|--------|
| Baseline gate | e4f65557... | byte-identical to S14 | PASS |
| Validator V1-V6 | all PASS, kept 39/48/64/24 | V1-V6 pass | PASS |
| Tripwire (clarity fraction) | 87 per mille (28476/323997) | 50..150 per mille | PASS |
| KB1 determinism (3 reruns) | 96f3a899ee45155b5272536a25f71614a43ef6bca213a2ab6a4b7fc212ec3cd4 x3 identical | identical | PASS |
| KB2 shaft ratio (WEDGE) | 1.0000 | >= 1.12 | FAIL |
| KB3 var(dL) (WEDGE) | 0.00 | >= 60.0 | FAIL |
| KB4 terrain mean\|dL\| | 0.00 | <= 1.0 | PASS |
| KB5 off-wedge mean\|dL\| | 0.00 | <= 6.0 | PASS |
| KB6 acutance ratio | 1.0000 (base 472, var 472) | <= 1.10 | PASS |
| KB7 max\|2nd diff dL\| (RADCUT) | 0 | <= 25 | PASS |
| KB8 cost (variant vs baseline) | 1964ms avg vs 934ms (2.10x) | <= 3x | PASS |

## Killing evidence

KB2 and KB3 fail: not a single one of the 39 validated wedge points
receives any lift (dL = 0 at all of them), so the shaft ratio is exactly
1.0000 and the dL variance is exactly 0. Post-run pure-Zag
characterization of the variant BMP (probe_lift_v3.zag, evidence only,
no tuning): 2609 sky pixels carry nonzero dL (of 2805 delta passers; 196
quantize to L=0 under integer math since L = 90*delta/(delta+1024) < 1
for delta < 12), max |dL| is 35 luma steps, and the lifted pixels form a
band with bbox x 125..1023, y 308..458, centroid (301,349): just below
and right of the sun. 2003 of the 2609 lifted pixels (77 percent) lie
within 200 px of the sun.

Mechanism reading: v3 fixed v2's specific failure mode. The lift is now
sun-anchored (77 percent within 200 px of the sun, versus v2's blob
870 px away) and higher-contrast (max dL 35 versus 9), and the
sign-corrected clarity gate passed 8.7 percent, confirming the measured
quantile behaves as designed on the byte-identical baseline. But the
delta > 0 predicate selected a band BELOW the sun (y 308..458), disjoint
from the frozen upward wedge fan (every wedge point has y < 300). The
prereg's fan-direction decision explicitly left the fan sector-agnostic
("no fixed global opening direction"), so nothing in the frozen
mechanism preferred the upward sector the WEDGE set measures. Ruled a
mechanism miss, not a freeze defect: geometry valid, gate behaved as
designed, predicate worked as specified, but the directional-contrast
predicate as frozen selects angular local minima wherever the D field
puts them, with no reason to produce the upward fan the detector and
the visual concept require. The novelty argument's core claim held (v2's
far-field corridor blob is gone; its selector was deleted), but a new
failure mode appeared in its place: sector-agnostic selection.

## Red-team notes (for the coordinator)

1. No dropouts, black regions, crashes, or banding. Determinism holds
   across 3 reruns. Terrain, off-wedge sky, and acutance are untouched
   (KB4/KB5/KB6 pass with 0.00/0.00/1.0000). E3 rejection honored.
2. Watch-item answers: (a) cost 2.10x, well under the 3.0x bar; the
   short-circuiting worked (about 1.5 marches per sky pixel effective,
   versus 2.0 for v2; the naive 7x never materialized); (b) evaluation
   order is frozen and recorded in trace G1.5 and in the evidence;
   (c) the WEDGE point set is geometrically valid (V1-V6 pass, 39 kept
   points all tier 0, validator/verifier kept counts identical) but it
   measures the upward fan while v3 lifted a below-sun band: the set
   does not capture v3's output sector, and the bars correctly report no
   shaft signal on the measured fan.
3. Structural observation for any future shaft work: the angular-minimum
   predicate needs a sector prior (crepuscular shafts fan upward from a
   low sun) or the D field needs correspondence with the visible cloud;
   as frozen, the predicate is sector-agnostic and the deck's clearest
   angular minima near the sun lie below it. The lifted band is also
   broad and horizontal rather than narrow shafts, suggesting the frozen
   plus or minus 144 px flank scale samples band-scale rather than
   shaft-scale structure. Any redesign is a new prereg, not a patch.
4. Staffing note: three waves have now been spent on G1 internals. The
   v3 wave produced a genuinely new mechanism and a clean negative
   result (sun-anchored selection confirmed, sector problem identified),
   which is the honest terminal state for this line until a new design
   idea exists. The frontier remains PAMs v2 and b_alpha v9.

## Purity

Python contact: none. Static checks in run_g1v3.sh all pass: no .py
files in g1/, no python token in any authored .zag source (comments
stripped before grep), no python invocation in the runner, no
rand/time/clock calls in sources. Generator, validator, verifier,
analysis probe, and scratch are pure Zag compiled with the pinned
toolchain. The /tmp build scratch is ephemeral; all durable evidence is
committed under g1/.

## Files

- g1/r8c_baseline.zag (baseline source, byte copy of 1421pdt source)
- g1/g1_sunshafts_v3.zag (variant source)
- g1/g1_validate.zag (byte copy of 1421pdt validator),
  g1/g1_verify_v3.zag (v2 verifier, cosmetic labels only)
- g1/run_g1v3.sh, g1/probe_lift_v3.zag
- g1/sub/R33_NATIVE_IO_V1.zag
- g1/measure/ (phase-1 diagnostic: g1_measure_t.zag, measure_out.txt,
  T_DISTRIBUTION_1721.md read-only)
- g1/bin/ (built binaries), g1/evidence/ (BMPs, traces, compile/run
  logs, validator/verifier outputs, tripwire record, wall-time record,
  probe output)

Commits: acf7cedce (prereg), 1da140387 (sign-correction addendum),
39707e077 (implementation and evidence). Nothing pushed to GitHub.
Nothing written to LOOP_STATE.md. Nothing surfaced to Micah; the
coordinator owns the judge queue, which is untouched.

## Addendum: judge-ordered classification change (debate wave-20260924-1721pdt, 2026-09-25)

Ordered by the debate judge (debate/JUDGE_RULING_1721.md, M2). The DISCARD
outcome is unchanged; no bar was weakened. The recorded classification changes
from "mechanism miss" to "detector mismatch / unfrozen correspondence;
upward-fan hypothesis refuted for this D field; mechanism performed as
frozen."

Reason (frozen text, quoted literally): the prereg's fan-direction decision
states "The fan has no fixed global opening direction; it is anchored
per-pixel to the sunward ray." A mechanism-miss ruling requires aim; the
frozen text disclaims fixed aim. The mechanism performed exactly as frozen:
sun-anchored lift confirmed (2805 delta passers, 2609 pixels with nonzero dL,
max |dL| 35 vs v2's 9, 2003 of 2609 = 76.8 percent within 200 px of the sun,
clarity gate 28476/323997 = 87.9 per mille inside the frozen 50..150 band),
while the frozen WEDGE detector measured the upward fan (all wedge points y <
300) and the minima lay below the sun (lift band bbox x 125..1023, y
308..458). The prereg froze a sector-agnostic mechanism, a sector-specific
detector, and an unfalsified-at-freeze correspondence claim between them; the
D-field belief that the minima would be sunward/upward was the author's
prediction, refuted by the D field. The red-team's three locks were rejected
on the frozen text: the no-re-interpretation clause bars re-interpretation to
force a PASS (a classification change cannot force a pass under a
DISCARD-only mapping); the novelty caveat pre-registered the outcome mapping,
not the failure-mode classification; and binding the authorial "measures
exactly the fan" claim while discounting the equally frozen "no fixed global
opening direction" is selective.

Terminal state downgraded: the directional-contrast idea is PAUSED pending a
re-aimed prereg with a sector prior (the specified next step already present
in the red-team note 3), not dead for lack of ideas. The staffing call (pause
G1 internals; the frontier is PAMs v2 and b_alpha v9) stands as a staffing
judgment, separated from the technical claim. The sign-correction addendum
stands as a legitimate pre-implementation S10 internal-consistency repair.
