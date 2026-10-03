# REPORT.md -- IVWC-LEARNERK: learner-owned K via revealed stakes

## Verdict: BUILD-PASS (K1 through K10 all pass)

The learner can own K -- but owning it does not beat being given it.
Two revealed-stakes verdicts were built in which the world's cost
parameter never enters the learner's computation (audited K1-A10b):
the learner sets its GO/NO-GO threshold to the bar that maximized its
experienced train net outcomes. The preregistered verdict:

1. **Can the learner own K effectively? YES, globally (K10/K6).**
   UCB x V_LOK totals 258 = UCB x V_WK's 258, with per-case identical
   GO sets on all three batches. The learner recovers
   decision-equivalent stakes from experienced net outcomes alone --
   the revealed global bar (14) is behaviorally indistinguishable
   from the given stakes (15) because no sealed score equals 15.
   Ownership without loss.
2. **Does learner-owned K beat fixed-K? NO (K4, preregistered NULL).**
   258 ties; it does not exceed. The per-bucket (context-adaptive)
   version V_LOKB totals 228 < 258 (K7/K9): revealed per-bucket
   stakes overfit train, reprising PBOPT's lesson with K removed from
   the computation entirely.
3. **Is this the right direction for Priority #4? Partially.** It
   closes "can the learner determine stakes from experience" (yes --
   globally, without loss), but it opens no new winning direction.
   The worth-K verdict is *robust* to removing K as a given rather
   than improved by owning it. The remaining frontier is the
   K-sensitivity curve (for which K do the rankings change?),
   explicitly not tested this wave.

## Headline numbers (profit at K=15; GO/NO-GO, no labels)

| arm | @15 | @30 | @45 | total |
|---|---|---|---|---|
| UCB x V_WK (control) | 75 (6) | 128 (8) | 55 (3) | 258 |
| UCB x V_LOK (MAIN-1) | 75 (6) | 128 (8) | 55 (3) | 258 |
| UCB x V_LOKB (MAIN-2) | 60 (7) | 128 (8) | 40 (4) | 228 |
| execute-all (ref) | 43 | 113 | -80 | 76 |

(Parentheses: GO counts.) Every number was preregistered exactly from
the committed tables; all confirm. Owned stakes: lokbar = 14 (global
revealed bar; train net plateau 265 tied at {5} U {9..14},
preregistered conservative tie-break toward the larger bar);
lokbbar = (0,16,5,9) (per-bucket revealed bars).

## What was built

`src/ivwc_learnerk.zag` (pure Zag, single file, pinned znc),
`bin/ivwc_learnerk` (build artifact; excluded from the commit per
Micah's 2026-10-03 guidance). World/belief/composer/stepper/seeds/
biases/UCB tables/mcalib/pbkbar/pboptbar verbatim from the IVWC
lineage (24/24 train TAUDIT lines byte-identical to the committed
table; K3 re-verifies bars). New:

- **Train TNET (harness):** `tnet[t] = teff[t] - EXCOST`, the
  experienced train net outcome per case (reward minus charge, one
  number -- the faithful consequence interface), plus `tadj[t]`,
  the learner's own train score. Pure arithmetic on the
  CONSEQ-filled buffers; zero world calls.
- **`lok_global` / `lok_bucket` (learner):** revealed-preference
  bar computation. Global: argmax over integer bars b in
  [min tadj - 1, max tadj] of P(b) = sum over train cases with
  tadj > b of tnet; ties toward the larger bar. Per-bucket: the
  same argmax restricted to the bucket, same data-driven range
  rule, same tie-break. Both functions read only tnet, tadj,
  tbkt -- zero `EXCOST` and zero `teff` tokens in their bodies
  (K1-A10b). The learner could recover K=15 from (teff, tnet);
  it does not: the restriction is the operational definition of
  ownership.
- **V_LOK:** GO iff adjucb_s > lokbar (= 14). Reads no bucket;
  the direct learner-owned analog of the V_WK control.
- **V_LOKB:** GO iff adjucb_s > lokbbar[sbkt_s] (= (0,16,5,9)).
  Context-adaptive owned stakes. (PBOPT's objective with the
  K-referencing candidate range and K-pulled tie-break removed;
  b0/b3 bars differ from PBOPT's (15,16,5,15) only through that
  removal.)
- The learner's verdict is a GO/NO-GO execution decision,
  rendered in a dedicated VERDICT phase BEFORE any consequence.
  The learner never sees `eff`.
- Scoring is pure consequence: the world charges EXCOST=15 per
  GO; profit = sum over GO cases of (eff - 15). No `ge`, no
  threshold on truth -- K1-A9 audits zero `Tpred` tokens.
- `world_execute(` appears exactly 4 times (1 def + 3 call sites:
  train CONSEQ, the shared `conseq_arm` helper, REFERENCE).
  WC-FINAL = 113 (24 train + 53 GO + 36 reference; no fenced
  diagnostics this wave -- V_WK *is* the exact-stakes reference).
- In-program kill flags K3-K10 all 1; K1STRUCT=1.

Build: pinned znc `$HOME/safebin/znc`
`src/ivwc_learnerk.zag -o bin/ivwc_learnerk` under the safebin
PATH (`which python3` and `which python` return nothing).
Analyzer: the standard zagd-unavailable informational notice
only.

## Kill-bar results

- K1 (diet / commit order / no-exact-signal / probe-proofness /
  ownership): PASS. A1: phase order
  520<527<535<547<553<712<725<736<823<827<835<853<889<916<925
  (train SETUP < COMMIT < PREFF < CONSEQ < LEARN < TNET <
  LOKBARS < BAR < sealed SHIFT < SETUP < COMMIT < BARS <
  VERDICT < CONSEQUENCE < REFERENCE). A2: 0 `world_buf`/
  `world_off` in learner fns (lc_blocked, lc_leg,
  learner_compose, gather_cells, lok_global, lok_bucket). A3: 0
  `expected|answer|key|target`. A4: 0
  `correct|reference_plan|gold`. A5: `world_execute(` x4. A6:
  WC-FINAL=113. A7: 0 `learner_`/`belief_` after the
  CONSEQUENCE marker (line 916). A8: 0 `oracle`. A9: 0 `Tpred`.
  A10: the V_LOK/V_LOKB bars are computed from train
  (tnet, tadj, tbkt) only and never read a sealed bias-adjusted
  score; the fenced lineage probes touch adjusted scores only,
  never bkt, so they cannot move either LOK bar. A10b
  (ownership): 0 `EXCOST` and 0 `teff` tokens inside the
  `lok_global` / `lok_bucket` bodies -- the stakes computation
  never sees the world cost parameter or the decomposed effect
  table.
- K2 (determinism): PASS. 3/3 byte-identical, sha256
  `115f09a1ee0ffebff41662c0b12cd46511c9659ce17aa7934f8489f0e5a2a8e5`.
- K3 (verbatim machinery + new): PASS. BARS ThyA=13/20/6,
  ThyB=13/20/13; TFIXED=12; CVAL=15; ThyHKC=15/20/15;
  bucb=(0,16,27,20); mcalib=(0,-11,-12,-3);
  pbkbar=(15,4,3,12); pboptbar=(15,16,5,15);
  UCB x V_WK=(75,128,55)=258; execute-all=(43,113,-80). New:
  lokbar=14; lokbbar=(0,16,5,9) (in-program K3=1, via shallow
  sub-flags k3a-k3d).
- K4 (PRIMARY, preregistered NULL): PASS. UCB x V_LOK total
  258, NOT > 258, AND UCB x V_LOKB total 228 < 258
  (in-program K4=1). Learner-owned K does not beat fixed-K.
- K5: PASS. Execute-all = (43, 113, -80) (in-program K5=1).
- K6: PASS. eq_lok_wk=1 (per-case GO equality across all 36
  sealed cases) AND tot_ulok=258 (in-program K6=1). Mechanism:
  lokbar 14 vs fixed 15; no sealed adj equals 15, so the bars
  are decision-equivalent on these batches.
- K7: PASS. UCB x V_LOKB total 228 < 258 = UCB x V_LOK total
  (in-program K7=1). Per-bucket revealed stakes overfit vs the
  global revealed bar.
- K8: PASS. WC-FINAL=113 (in-program K8=1).
- K9 (divergence): PASS. UCB x V_LOKB total 228 < UCB x V_WK
  total 258 (in-program K9=1).
- K10: PASS. UCB x V_LOK total 258 = UCB x V_WK total 258
  (in-program K10=1). Ownership without loss.

## Mechanism detail (white box)

### Why V_LOK ties V_WK exactly (K6/K10)

The global revealed bar is 14, not 15: on train, P(b) plateaus
at 265 for b in {5} U {9..14} (the (6,+-15),(7,+1),(9,-4) nets
cancel exactly), and the preregistered conservative tie-break
picks the largest, 14. On sealed batches, GO iff adj > 14 vs
adj > 15: with integer scores these differ only at adj = 15,
and no sealed case in any batch has adjucb = 15 (committed
tables: adjs are 13/0/17/34/24/6/9/2, 30/20/23/5, -2/84...).
So the owned bar and the given bar make identical commitments
everywhere: 75/128/55, GO (6,8,3). The learner earns the
fixed stakes from experience alone -- it never sees K=15 --
and loses nothing for it. This is the sense in which the
worth-K verdict is *robust* to removing K as a given.

The tie-break is load-bearing and was disclosed pre-hoc: the
aggressive tie-break (b=5) gives sealed (75,138,-40) = 173 by
arithmetic on the committed tables (not run). The conservative
rule ("when train-indifferent, demand higher stakes") is the
preregistered structural choice; the sensitivity is reported,
not hidden.

### Why V_LOKB loses (K7/K9)

The per-bucket revealed bars (0,16,5,9) inherit train's
bucket structure the same way PBOPT's (15,16,5,15) did -- now
with K absent from the computation entirely. The losses vs the
global bar: @15, the b2 bar 5 takes s0's -15 (adj 13, eff 0);
@45, the b3 bar 9 takes s5's -15 (adj 13, eff 0). The b3
difference from PBOPT (9 vs 15) is the K-free range/tie-break
at work: with the candidate range capped at the data (max adj
9) instead of reaching up to K, the argmax {9} stands alone
and the bar sits at 9, taking s5's -15 at @45 that PBOPT's
K-pulled bar 15 avoided. Removing K from the computation
cost exactly that -15 (228 vs PBOPT's 243) -- the one place
the K-given tie-break had been protective. Below-batch
resolution overfits whether or not K is given: the transfer
defect is in the signals, not in who supplies the stakes.

### Ownership is structural (K1-A10b)

The `lok_global` / `lok_bucket` bodies contain zero `EXCOST`
and zero `teff` tokens (audited pre-build). They read tnet
(experienced nets, harness-reported), tadj (the learner's own
train scores), tbkt. The tnet buffer is filled harness-side
from (teff, EXCOST) -- the world still charges K; the learner's
stakes module simply never sees it. The learner *could*
recover K=15 per case from (teff, tnet) since teff is
learner-visible on train; the audit enforces that it does
not. This is the operational content of "the learner owns K":
the threshold is a learner-determined argmax over experienced
outcomes, not a read of a world constant.

### Correction-independence is preserved (K1-A10)

Structural, not claimed. The LOK bars are train-fixed
(tnet/tadj/tbkt only); the verdict compares the sealed score
to the bar, as every verdict does. No sealed bias-adjusted
score enters any bar computation, so the fenced lineage
probes (which touch adjusted scores only) cannot move the
LOK bars. The D1b/D2b probe arms were not re-run this wave,
as in PERBUCKET/MARGINAL.

## Answers to the task's key questions

1. **What does "learner-owned K" mean operationally?** The
   decision threshold is set to the argmax over the learner's
   experienced train net outcomes (revealed stakes), with the
   world cost parameter and the decomposed effect table absent
   from the computation by audited structure. Not cost
   inference (trivial on this world), not a researcher-set
   risk attitude.
2. **Can the learner determine stakes from experience?** Yes,
   globally: V_LOK recovers decision-equivalent stakes
   (258 = 258, identical GO sets, K6/K10) from train nets
   alone. Per-bucket, it determines stakes that overfit
   (228, K7/K9) -- the same below-batch lesson as PBOPT, now
   K-free.
3. **Does learner-owned K beat fixed-K (15)?** No --
   preregistered NULL K4 (258 ties, 228 loses). Owning the
   stakes matches being given them at best.
4. **Is this the right direction for Priority #4?** It closes
   the "determine stakes from experience" question but opens
   no new winning direction. The finding strengthens worth-K:
   the verdict does not depend on K being handed to the
   learner. Next: the K-sensitivity curve.
5. **Is this L2 or L3?** L1 (parameter learning) with an L2
   flavor, not L3. The bar *form* (global / per-bucket
   threshold) is researcher-given; the learner fills the
   *value* by optimization over its experience (L1). The L2
   flavor is the ownership itself: a decision variable that
   was a world-supplied constant becomes learner-determined
   via revealed preference. Not L3 by a wide margin: no new
   representation, abstraction, or procedure is invented; the
   threshold family is researcher-enumerated; Criterion 0
   fails (the source holds the complete threshold machinery).

## Honest caveats

1. One wall-density law-change axis; item law, belief noise, and
   energy budget fixed (inherited from the IVWC lineage).
2. K=15 is the world's execution cost (unchanged); the profit
   ranking remains K-sensitive. The K-sensitivity curve is the
   named follow-up, not tested here.
3. The execute-all reference is counterfactual (fenced); the
   primary metric uses only real GO commitments.
4. The conservative tie-break (larger bar) is load-bearing for
   the V_LOK tie: b=5 would give 173 (arithmetic on committed
   tables, disclosed in PREREG, not run). The rule was frozen
   pre-build with its sensitivity stated.
5. The tnet interface (harness-reported experienced nets) is a
   small world-interface change vs the lineage's
   eff-visible-plus-K-given train interface; it is the more
   faithful "experience" interface (net outcomes are what an
   agent lives through), and the ownership audit is defined
   against it.
6. The D1b/D2b probe arms were not re-run; probe-proofness for
   the LOK bars is established structurally (K1-A10), not
   behaviorally, this wave.
7. Mechanism application, not a composition-novelty or L3 claim.
   The composer is fixed.

## Process notes and disclosures

- **No toolchain incident.** This lane is clean: zero
  python3/python invocations at any step. Safebin PATH
  throughout (`which python3` and `which python` return
  nothing). Pure Zag, pinned znc. See NAMECHECK.md Step 0.
- **Pre-build audits all green before the first build:** A1
  phase order strictly increasing; A2/A3/A4/A7/A8/A9 all 0;
  A5 `world_execute(` x4; A10b 0 `EXCOST` / 0 `teff` in the
  LOK function bodies.
- No post-prereg probe of any kind. All predictions were
  arithmetic on the committed tables. Every frozen prediction --
  lokbar=14, lokbbar=(0,16,5,9), all arm profits, all GO counts,
  WC-FINAL=113, all verbatim lineage bars -- confirmed exactly.
- One design note: the first draft of the TNET phase filled
  tadj inside the harness phase; it was kept there as a
  convenience copy of the learner's own score (the LOK phase
  that reads it is separately labeled learner). No behavioral
  consequence.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_learnerk
$HOME/safebin/znc src/ivwc_learnerk.zag -o bin/ivwc_learnerk  # safebin PATH, pinned znc
./bin/ivwc_learnerk | sha256sum  # expect 115f09a1ee0ffebff41662c0b12cd46511c9659ce17aa7934f8489f0e5a2a8e5
```

Frozen audits (PREREG K1): A1 phase order
520<527<535<547<553<712<725<736<823<827<835<853<889<916<925;
A2 0; A3 0; A4 0; A5 `world_execute(` x4 (1 def + 3 call sites);
A6 WC-FINAL=113; A7 0 `learner_`/`belief_` after line 916;
A8 0; A9 0 `Tpred`; A10 LOK bars read no sealed adjusted score
(train tnet/tadj/tbkt only); A10b 0 `EXCOST`/0 `teff` in
lok_global/lok_bucket. K2: sha256 equality across
runs/ivwc_learnerk-run{1,2,3}.txt. Train TAUDIT 24/24
byte-identical to the committed lineage table.

## Branch note

Work committed on `tnn-native-lab` in the `~/workspace/tnn-rsi`
worktree (prereg commit `668677abe` strictly precedes the
implementation). All commits use explicit pathspecs (via separate
GIT_INDEX_FILE plumbing, leaving the shared index untouched)
confined to `ivwc_learnerk/`. `bin/` (reproducible via the pinned
znc) is deliberately excluded from the commit per Micah's
2026-10-03 guidance. This is a non-ledger task. Pushing to origin
is AUTHORIZED per Micah's 2026-10-03 authorization; this lane is
clean (zero python3/python invocations).
