# REPORT: COGOPS-LEADERSHIP-TRANSITION

Date: 2026-10-03. Worker: COGOPS-LEADERSHIP-TRANSITION.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_leadership_transition/`
Prereg: frozen commit 98db87132 (PREREG.md + NAMECHECK.md +
c20_stages_predicted.txt, committed alone before any
implementation file existed).
Implementation commit follows this report.

## Verdict: BUILD-FAIL (K3b, K3c-transition, K3e fail; all other bars pass)

The battery forced leadership dynamics through two
regime-change blocks and measured the outcome honestly.
The preregistered crossing prediction for Block B was
wrong (the hand-sim used a 6-comparison NEED failure
cost; the true cost is 3, see Section 3), so K3b/K3e
fail. But Block D2 produced exactly one genuine
leadership transition (NEED->WHOLE at D2-7), and the
failure analysis yields a PRECISE quantitative
characterization of when transitions occur (Section 3).
Across 38 eligible selections with one forced
transition, exact ties occurred 0 times and the hedge
fired 0 times: the transition jumped over exact
equality (D2-6 near-miss: cross-products differed by
25). Per the preregistered decision rules, this is the
"transitions occur under failure-cost-asymmetric regime
change, but exact ties remain knife-edge even at
transitions" outcome.

## Headline results

1. **One genuine leadership transition in 38 eligible
   selections.** Block D2 (context (4,613), unwinnable
   kind 9): NEED led D2-1..D2-6, WHOLE took over at
   D2-7 and held D2-8..D2-10 (DET-STRAT 3->2,
   DET-TIE tm 8->4). The only other selection changes
   were the two cold-start id-defaults (A1: PW->NEED,
   D1a1: PW->NEED), excluded by the preregistered
   definition.

2. **Block B did NOT transition (prereg prediction
   killed).** 10 all-fail stages in (3,613) left NEED
   leading throughout (tm=8 on all 10). The score race
   analysis (Section 3) shows why: the dethroning
   condition was not met within 10 stages; it projects
   a crossing around B15-16. The prereg's B6 crossing
   prediction rested on a wrong turn-cost model.

3. **Tie frequency 0/38, hedge firings 0/38.** Every
   eligible stage's DET-TIE mask had popcount 1 (the
   argmin alone: tm=8 for NEED-led, tm=4 for
   WHOLE-led, tm=0 on the two fresh contexts). The
   D2-6->D2-7 crossing passed within 0.3 raw score
   units (NEED 331.09 vs WHOLE 331.38) without exact
   equality. 95% rule-of-three upper bound ~7.9% (with
   the c19 caveat that selections share learner
   state).

4. **The transition condition, quantitatively.** With
   score_s = [(c+8)*rb + (f+1)*ra]/(u+2), write mean
   failure cost m_s = c/u and failure rate
   phi_s = f/u. Asymptotically score_s -> m_s*rb +
   phi_s*ra: a ledger-weighted sum of failure COST
   and failure RATE. A challenger W dethrones
   incumbent N iff
     ra/rb < (m_N - m_W)/(phi_W - phi_N).
   Measured: Block B: m_N-m_W = 1 (NEED 3 NCMP vs
   WHOLE 2 CMP per failure), phi_W-phi_N ~ 0.29 ->
   threshold ra/rb < 3.45; actual ledger ra/rb ->
   4.67 (mean rescue cost). Condition never met:
   no transition. Block D2: m_N-m_W = 2 (4 needs:
   NEED 4 NCMP vs WHOLE 2), phi_N = 0.6 at crossing
   -> threshold < 5.0; actual 4.61 -> crossing at
   D2-7. The incumbent is protected twice: (a) past
   wins dilute phi_N, amplified by expensive rescues
   (high ra/rb); (b) the leader is always selected
   first, and at pass 2 one lag is unavailable, so
   its failure turn is capped at one lag's
   comparisons -- selection order itself cheapens
   the leader's failures (second-order anti-tie).

5. **Anti-tie baseline reproduced.** Block A: NEED
   selected A2-A4, extending its lead (0 transitions
   after A1). Block C: NEED led throughout (the B
   dethroning never happened, so there was nothing
   to retake). Block D1: NEED throughout after the
   cold start.

## Kill bar assessment

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | 40 HGATE == 40 STRAT == 40 TIE; eligible == 38 | 40/40/40; eligible=38 (all but A1, D1a1) | PASS |
| K2 | every HEDGE: dt1==0, dt3==0, ev>=1001; firing stages have tm bits 1&3 | 0 HEDGE lines (vacuous) | PASS |
| K3a | A2,A3,A4 chosen=3; 0 transitions in A after A1 | 3,3,3; 0 | PASS |
| K3b | >=1 transition in B; B10 chosen=2 | 0 transitions; B10 chosen=3 | FAIL |
| K3c | >=1 transition in C; C12 chosen=3 | 0 transitions; C12 chosen=3 | FAIL (transition part) |
| K3d | D1a2,a3,a4 chosen=3; >=1 transition in D2; D2-10 chosen=2 | 3,3,3; 1 transition (D2-6->D2-7); D2-10 chosen=2 | PASS |
| K3e | total transitions across B,C,D2 >= 3 | 1 | FAIL |
| K4 | tie stages (popcount(tm)>=2) <= 3 of 38 | 0 | PASS |
| K5 | setup blocks byte-identical to c19h_run1.txt's | lines 1-53 sha256 identical | PASS |
| K6 | 3/3 byte-identical; stderr empty | sha256 11bc371b... x3; .err 0 bytes x3 | PASS |
| K7 | 40/40 Q lines match predictions (id, tag, how) | 40/40 | PASS |
| K8 | safebin, no python, pinned znc, neg-conj clean, provenance diffs exact | all verified (below) | PASS |
| K9 | A1, D1a1 DET-TIE: best=1 tm=0 | both best=1 tm=0 | PASS |

## Why Block B did not transition (killed prediction, analyzed)

The prereg hand-sim charged NEED 6 NCMP per Block-B
failure. In fact the leader is always selected FIRST,
at pass 2, where lag 3 has b=-1 and is skipped: NEED
pays only 3 NCMP (one lag's comparisons) per failure,
vs WHOLE's 2 CMP. The per-failure cost gap is 1/use,
not 4. With the incumbent's 4-win lead and the
ledger's ra/rb converging to ~4.67 (mean rescue cost
14/3 per stage), the dethroning threshold
ra/rb < (m_N-m_W)/(phi_W-phi_N) = 1/0.29 = 3.45 is
never reached. At B10 NEED still led 185.8 vs 194.2;
the race converges at ~B15-16, beyond the block.
In Block D2 the 4-need context doubles the gap
(4 NCMP vs 2 CMP) and the threshold
ra/rb < 2/(1-0.6) = 5.0 was satisfied at the actual
4.61: crossing at D2-7, exactly as the inequality
predicts. The mechanism is confirmed; the B
parameterization was wrong, not the theory.

## The D2-7 transition in detail

D2-6 selection (rt=231, rc=49; ra=233, rb=51):
NEED(9,4,36): 3642/11 = 331.09; WHOLE(6,0,12):
2651/8 = 331.38; PW: 363.25. Cross-products
3642*8=29136 vs 2651*11=29161 differ by 25: near-tie,
not exact; NEED selected, no hedge fire (tm=8). D2-7 selection (rt=247, rc=52;
ra=249, rb=54): NEED(10,4,40): 4335/12 = 361.25;
WHOLE(7,0,14): 3180/9 = 353.33. WHOLE selected
(tm=4), holds through D2-10. Rescue order within
each D2 stage follows the score order
(NEED->WHOLE->PW->ALT after the crossing).

## Pre-prereg probe discovery (c19 (3,615) staleness)

Documented in PREREG Section 2; restated here as it
is material to "builds on c19". A pure-Zag probe
(/tmp/probe, throwaway) showed c19's F17-F22 did not
run on the world the comments describe: S4's
episodes (ids 12-15) log rel 615 into ret coverage,
S6B specializes on world F (no 615 facts) leaving an
empty 615 bucket, and setup_worldF_plus adds the
facts without re-specializing. Rel 615 is therefore
invisible to the specialized RETRIEVE, so kind-5
need1 was [] (PW won degenerately at lag 2 via the
prior) and kind-6 need1 was [] (all-fail). The
rebuild-from-source check (byte-identical output)
confirms this is the committed c19 behavior. c19's
0/22 firing count is unaffected (it counts
selections, not kinds), but its kind-5/kind-6
characterizations describe the intended, not the
as-run, world. This worker's kinds 8/9 were designed
with the coverage mechanics explicitly accounted
for (613/605 not in ret coverage -> generic
retrieve; 604 in coverage AND indexed at S6B ->
working drifter) and their unwinnability was
validated by DET evidence (B1: NEED mask {0,1}
trivial -> fail; whole never repeats).

## What this establishes (and does not)

Establishes: (1) leadership transitions occur under
failure-cost-asymmetric regime change, governed by
the quantitative condition
ra/rb < (m_N-m_W)/(phi_W-phi_N); (2) the incumbent
has two structural protections -- failure-rate
dilution from past wins (amplified by expensive
rescues) and the first-turn failure-cost cap from
selection order; (3) even at a forced transition,
exact ties are knife-edge: 0/38 ties, 0/38 hedge
firings, with the crossing jumping over equality
(D2-6 off by 25 in cross-products). Does not
establish: that ties can never coincide with a
transition (0/38 bounds, does not prove); the
keep/delete decision (Micah's call, governance
#11); generality beyond the two contexts tested.

## Governance input for Micah (item #11)

The transition study adds one row to the hedge
ledger: the hedge's precondition (exact PW/NEED tie
for the argmin) did not arise even when leadership
was forced to turn over (0/38 ties, 0/38 firings,
one measured transition). Combined with c19's 0/22,
the lifetime natural record is 0/60 selections with
1 forced transition. The mechanism analysis shows
ties require an exact integer equality in a race
whose dynamics push scores apart (cost-gap and
failure-rate dilution separate them); the D2-6
near-miss (25/29161 relative gap) illustrates the
knife-edge. Whether that option value justifies
keeping the hedge remains the design call.

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin;
`which python3` / `which python` return nothing
before and after; verified this session). Pinned znc
`$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
for the build and the /tmp/probe build. All
computation pure Zag; shell only for znc/binary/git/
assembly/byte-verification/counting. Zero
forbidden-executable invocations. New Zag (world-add
kinds 8/9, driver battery, 1 strat instrumentation
block, probe) scanned for the `while.*!(` pattern:
clean; no deep nesting (max 3). Git writes via
/usr/bin/git absolute path, explicit pathspecs,
current branch (tnn-native-lab) only, nothing
pushed. Provenance verified: c20_base.zag
cmp-identical to c19_base.zag; c20h_strat_additive
diff vs c19h = exactly the 17-line DET-TIE block;
c20_world_add diff vs c19 = exactly mk_goal8/9
(35 added lines, 0 removed); c20_main diff vs c19 =
kind-12 dump branch + lesion-helper deletion +
battery swap only.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_leadership_transition/`:
PREREG.md, NAMECHECK.md, c20_stages_predicted.txt
(frozen, commit 98db87132), c20_base.zag,
c20_world_add.zag (mk_goal8/9), c20h_strat_additive.zag
(+DET-TIE kind-12 block), c20h_learn.zag,
c20_main.zag (40-stage battery + kind-12 dump),
battery_new.zag (battery section source),
c20_build.sh, c20h_full.zag, c20h_bin,
c20h_compile.txt, c20h_run1/2/3.txt (sha256
11bc371bf38ee8198156989fec671ae61ed29eeaad27226b84a334bc5cc345cc
x3) + .err (empty), REPORT.md (this file).
