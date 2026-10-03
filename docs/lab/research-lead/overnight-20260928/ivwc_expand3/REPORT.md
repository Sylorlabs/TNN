# REPORT.md -- IVWC-EXPAND3: corrected K6/K8 re-run

## Verdict: BUILD-PASS (K1..K9 all PASS)

The corrected re-run passes all nine frozen kill bars. The learner
commits to compositions plus a pre-execution PASS/FAIL self-verdict
from a consequence-trained verifier before any outcome signal; the
verdict discriminates sealed outcomes (K3) and beats the trivial
baseline (K4, 9/12 vs 7/12); the consequence-content ablation is now
genuine (K6: shuffled 3/12 < true 9/12); the revision protocol
replicates bit-exactly (K7: 223 -> 235); and the law-change dial
shows carried verification degrading monotonically into
worse-than-trivial (K8: edge +2 -> -1; K9: 10/12 <= 11/12 at
wp=45). Deterministic 3/3.

## What was built

`src/ivwc_expand3.zag` (pure Zag, single file, ~800 lines, pinned
znc), `bin/ivwc_expand3` (frozen binary). The expand2 source with
exactly two corrections: (C1) the shuffled-consequence arm rotates
ONLY the eff array (sbkt[t]=tbkt[t], seff[t]=teff[(t+7)%24]),
genuinely breaking the bucket->eff mapping while preserving
marginals; (C2) K8 bars the edge degradation (acc-maj) rather than
absolute accuracy. One print-only addition: the shuffled verifier
table (VBSH lines). No other logic changes; all worlds, seeds,
verifier, shifts, and phases identical to expand2.

Build: `src/tools/toolchain/znc_linux_x86_64_abed8aa1
src/ivwc_expand3.zag -o bin/ivwc_expand3`. Analyzer: one
informational zagd-unavailable notice only.

## Kill-bar results

- K1 (commit before signal): PASS. 7/7 in-program STRUCT-PASS
  (K1T train commit; K1S/K1R at sh=0/1/2), zero STRUCT-FAIL.
  Audit A1: phase-pair ordering holds (446<459; 551<580;
  645<661; 673<675; 676<677). Audit A2: zero world_buf/world_off
  in the LEARNER section.
- K2 (no disguised oracle): PASS. Audit A3: zero
  expected|answer|key|target tokens. Audit A4: zero
  correct|reference_plan|gold tokens; == comparisons are
  physics/action/local only; verifier inputs are (bucket, eff)
  consequence pairs; T learner-computed.
- K3 (self-check discriminates, wp=15): PASS. np=6 sp=157 nf=6
  sf=66; 157*6=942 > 66*6=396 (mean PASS 26.2 > mean FAIL 11.0).
- K4 (beats trivial baseline, wp=15): PASS. acc=9/12 > maj=7/12.
- K5 (determinism): PASS. 3/3 byte-identical, sha256
  1a4fb4fcc356a8e91cf7089b0a9c987834f1db022ec55edeca87c1d5b6a07f7c.
- K6 (ablation, corrected): PASS. acc_shuf=3/12 < acc=9/12
  (strict). The shuffled table now genuinely differs: VBSH means
  35/15/16/5 (cnt 7/7/7/3, T=20) vs true VB means 0/47/16/10 --
  the shuffle inverted the rule (PASS iff bucket==0, the empty-plan
  bucket), and accuracy collapsed to 3/12. Consequence CONTENT
  drives the verifier.
- K7 (revision replicates, wp=15): PASS. Sealed sum_eff1=223,
  sum_eff2=235, sum_abl=223, n_abldiff=0 -- bit-exact IVWC-EXPAND
  replication for the second time (expand2 and expand3 agree).
- K8 (edge degrades, corrected): PASS. (acc-maj): +2 at wp=15
  (9-7), -1 at wp=45 (10-11); -1 < +2 strict. The verifier's value
  over the trivial rule erodes under law change.
- K9 (break found): PASS. At wp=45 acc=10/12 <= maj=11/12.

## Mechanism detail (white box)

Unchanged core numbers from expand2 (same deterministic
machinery): train verifier T=20, rule "PASS iff exactly one
planned gather"; per-shift selfcheck sums (sh=0: acc 9 maj 7;
sh=1: acc 8 maj 8; sh=2: acc 10 maj 11); revision gains +12 / +56
/ 0 across wp 15/30/45. The limits picture stands: carried
calibration degrades monotonically into worse-than-trivial (edge
+2 -> 0 -> -1), while fresh-consequence revision peaks under
moderate change (+56 at wp=30, where denser walls yield more bump
evidence) and floor-kills at wp=45 (100->100; eleven of twelve
sealed cases collect nothing under any plan). The two modes break
differently -- stale knowledge vs absent signal -- with no oracle
at any step.

The K6 correction is confirmed working as designed: with buckets
fixed and effs rotated, the shuffled table's bucket means moved
(35/15/16/5), the PASS rule flipped to the empty-plan bucket,
and sealed accuracy fell to 3/12. The expand2 vacuity
(bit-identical tables) is gone.

## Honest caveats

1. This wave is a correction, not a new experiment: only K6 and
   K8 were re-tested with fixed constructions; K1-K5/K7/K9
   re-confirm the expand2 numbers on identical machinery (the
   implementation is expand2's source plus the two corrections,
   so identical outcomes were expected everywhere else).
2. The wp dial covers one law-change axis (wall density); item
   law, belief noise, and energy budget are fixed. Other axes may
   break the mechanisms at different points.
3. Mechanism test, not a composition-novelty or L3 claim (per
   PREREG section 3). The verifier is a fixed bucket table; the
   claims concern the self-verdict loop, the content ablation,
   and the limits curves.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_expand3
~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1 src/ivwc_expand3.zag -o bin/ivwc_expand3
./bin/ivwc_expand3 | sha256sum   # expect 1a4fb4fcc356a8e91cf7089b0a9c987834f1db022ec55edeca87c1d5b6a07f7c
```

Frozen audits (PREREG section 4): A1 ordering 446<459, 551<580,
645<661, 673<675, 676<677; A2 count 0; A3 count 0; A4 zero tokens;
A5 sha256 equality across runs/ivwc_expand3-run{1,2,3}.txt.

## Branch note

Work committed on `tnn-native-lab` (the shared checkout this worker
was spawned on). All commits use explicit pathspecs confined to
`ivwc_expand3/`. Local only, never pushed. Git writes via
/usr/bin/git directly.
