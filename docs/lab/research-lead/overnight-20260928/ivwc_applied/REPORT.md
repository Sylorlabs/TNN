# REPORT.md -- IVWC-APPLIED: hybrid verdict on selective execution (no oracle)

## Verdict: BUILD-PASS (K1 through K10 all pass)

The hybrid verdict works as a real internal verification mechanism
with no expected-answer oracle anywhere -- not for the learner, not
even fenced for scoring. The learner verifies its own learned-bias
work (UCB x V_HA) and more than doubles profit vs executing
everything (210 vs 76, K4). But the preregistered mixed result
holds: the hybrid does NOT dominate on profit. Its @45 bias-mix
limit is a real 15-profit loss (K6), and -- the deepest finding --
accuracy-optimal DIVERGES from profit-optimal (K9): D1b x V_HA has
the better accuracy in the verdict wave's committed table (35/36 vs
34/36) but the worse profit here (262 vs 280). The hybrid bar
answers a relative-trust question ("above the batch's level?"),
not a consequence question ("worth K?"). That divergence is the
next frontier for Priority #4.

## Headline numbers (profit at K=15; GO/NO-GO, no labels)

| arm | @15 | @30 | @45 | total |
|---|---|---|---|---|
| A1 UCB x V_T | 75 (6) | 95 (6) | 55 (3) | 225 |
| A2 UCB x V_N | 60 (7) | 128 (8) | 40 (4) | 228 |
| A7a UCB x V_HA (KEY) | **75 (6)** | **95 (6)** | **40 (4)** | **210** |
| A7b UCB x V_HB | 75 (6) | 95 (6) | 55 (3) | 225 |
| A8a D1b x V_HA | 72 | 105 | 85 | 262 |
| A8b D1b x V_HB | 72 | 105 | 85 | 262 |
| A3 D1b x V_T | 52 | 133 | 85 | 270 |
| A4 D1b x V_N | 72 | 123 | 85 | 280 |
| A9a D2b x V_HA | 39 | 65 | 55 | 159 |
| A9b D2b x V_HB | 39 | 65 | 55 | 159 |
| execute-all (ref) | 43 | 113 | -80 | 76 |

(Parentheses: GO counts, learner arms.) Every number above was
preregistered exactly from the committed verdict-wave tables; all
confirm.

## What was built

`src/ivwc_applied.zag` (pure Zag, single file, pinned znc),
`bin/ivwc_applied` (build artifact; excluded from the commit per
Micah's 2026-10-03 guidance). World/belief/composer/stepper/seeds/
biases/bars verbatim from IVWC-HYBRID-VERDICT (all 24 TA lines
byte-identical to the committed run; K3 re-verifies bars). New:

- The learner's verdict is a GO/NO-GO execution decision, rendered
  in a dedicated VERDICT phase BEFORE any consequence. The learner
  never sees `eff`.
- Scoring is pure consequence: the world charges EXCOST=15 per GO;
  profit = sum over GO cases of (eff - 15). No `ge`, no threshold
  on truth -- K1-A9 audits zero `Tpred` tokens in the source.
- `world_execute(` appears exactly 4 times (1 def + 3 call sites:
  train CONSEQ, the shared `conseq_arm` helper, REFERENCE).
  WC-FINAL = 185 (24 train + 125 GO + 36 reference).
- In-program kill flags K3-K10 all 1; K1STRUCT=1.

Build: pinned znc `$HOME/safebin/znc`
`src/ivwc_applied.zag -o bin/ivwc_applied` under the safebin PATH
(`which python3` and `which python` return nothing). Analyzer: the
standard zagd-unavailable informational notice only.

## Kill-bar results

- K1 (diet / commit order / no-oracle): PASS. A1: phase order
  432<439<447<459<465<526<574<582<599<646<672<683<743 (train
  SETUP < COMMIT < PREFF < CONSEQ < LEARN < BAR < sealed SETUP <
  COMMIT < BARS < VERDICT < CONSEQUENCE < FENCED-DIAG <
  REFERENCE). A2: 0 `world_buf`/`world_off` in learner fns
  (lc_blocked, lc_leg, learner_compose, gather_cells). A3: 0
  `expected|answer|key|target`. A4: 0
  `correct|reference_plan|gold`. A5: `world_execute(` x4. A6:
  WC-FINAL=185. A7: 0 `learner_`/`belief_` calls after line 672
  (the CONSEQUENCE marker). A8: 0 `oracle`. A9: 0 `Tpred` --
  the no-oracle bar; no transductive threshold exists anywhere.
- K2 (determinism): PASS. 3/3 byte-identical, sha256
  `366ad663c1136e052f71aaa6dc1bf04a7be3bbc82dd44c292b0a76c1db67e9b8`.
- K3 (verbatim machinery): PASS. BARS ThyA=13/20/6,
  ThyB=13/20/13; TFIXED=12; CVAL=15 (in-program K3=1).
- K4 (PRIMARY): PASS. UCB x V_HA profit = (75, 95, 40), total
  210 > execute-all 76 (in-program K4=1). Self-verification
  without an oracle beats no-verification by 134.
- K5: PASS. Execute-all = (43, 113, -80) (in-program K5=1).
- K6: PASS. UCB x V_HA @45 = 40 < UCB x V_HB @45 = 55
  (in-program K6=1). The @45 bias-mix limit as profit: HA's s=5
  false GO (adjV=13 clears ThyA=6; eff=0) costs exactly 15.
- K7: PASS. D1b x V_HA @15 = 72 > D1b x V_T @15 = 52
  (in-program K7=1). The un-blocking pays in consequences:
  V_T's chase-down executes s=1, s=8 (eff=0; -15 each).
- K8: PASS. WC-FINAL=185 (in-program K8=1).
- K9: PASS. D1b totals: V_HA=262, V_T=270, V_N=280
  (in-program K9=1).
- K10: PASS. D2b x V_HA = 159, D2b x V_HB = 159
  (in-program K10=1).

## Mechanism detail (white box)

### Why self-verification works without an oracle (K4)

The learner's GO decision uses only its own quantities: preff
(bias-free belief prediction), bucb (train-learned bias), C
(train-fixed), and the sealed batch's preff/adjucb sums (bars).
No eff, no label, no threshold on truth exists in the experiment
(K1-A9). Yet the consequence (profit) strongly favors
verification: 210 vs 76. The mechanism is the same one the
verdict wave isolated -- the hybrid bar cannot be chased by the
learner's own corrections -- now with the score itself
oracle-free. The 134-profit gap is the measured value of
internal verification on this problem.

### Why the @45 limit is a profit loss (K6)

@45 the sealed batch is bucket-0 heavy; the train-fixed offset C
miscalibrates and ThyA=6 undershoots. s=5 (UCB adjV=13, eff=0)
clears the bar -> false GO -> -15 profit. V_HB (ThyB=13, reading
the sealed bucket mix through the frozen baseline) correctly
abstains -> 55 vs 40. The K10 accuracy limit of the verdict wave
is now a priced consequence. Correction-independence forces the
offset to be train-fixed; a train-fixed offset cannot track
bias-mix shifts; untracked shifts cost money. The chain is
exact, not analogical.

### Why the un-blocking pays @15 (K7) but not overall (K9)

@15, V_T's bar (mean of d1adj, dragged down by the -40s) executes
s=1 and s=8 (eff=0; -15 each) -- the chase-down, priced. HA's
unmoved bar (ThyA=13) holds -> 72 vs 52. But @30 the ranking
flips: V_N (bar 12) executes s=2 (d1adj=17, eff=33, +18 profit)
which HA's bar (20) skips. s=2's adjV sits BELOW the batch's
trust level but ABOVE the execution cost. The hybrid bar is
calibrated to the batch's relative level; profit is calibrated
to K=15. When relative and absolute disagree, the hybrid loses.
Totals: V_N 280 > V_T 270 > V_HA 262.

### The divergence (K9 vs the verdict wave's accuracy table)

Committed accuracy (verdict wave): A8a (D1b x V_HA) 11/12, 12/12,
12/12 = 35/36; A4 (D1b x V_N) 11/12, 11/12, 12/12 = 34/36.
Profit (this wave): A8a 262 < A4 280. The verdict that best
matches the (transductive) labels is NOT the verdict that makes
the most money. The labels ask "is eff above the batch mean?";
profit asks "is eff above K?". These are different specifications
of "verify correctly", and no threshold bar can serve both when
they diverge. This is the honest limit of the hybrid verdict as
an internal verification mechanism: it is cost-blind by
construction.

## Answers to the task's key questions

1. **Can internal verification work without an oracle?** Yes --
   K4: 210 vs 76, with K1-A9 proving no label or threshold
   exists anywhere in the experiment. The learner's
   commitment -> world consequence -> measured outcome loop
   needs no expected answer.
2. **Is the hybrid verdict the right mechanism?** It is the
   right mechanism for correction-independence (K7: the
   un-blocking has consequence value), but it is NOT sufficient
   as a complete verification mechanism: it is cost-blind (K9:
   the accuracy/profit divergence; K6: the @45 limit priced).
   The hybrid verdict is a necessary component (a verdict that
   can be chased by its own corrections is self-deception), not
   a complete solution.
3. **What are the limits?** (a) K6: bias-mix shifts that the
   train-fixed offset cannot track cost real profit. (b) K9:
   relative-trust bars diverge from consequence-optimality when
   the batch level and the cost K disagree; the verdict wave's
   accuracy crown does not transfer to profit. (c) The verdict
   is cost-blind by construction -- K never enters the bar --
   so the profit ranking is K-sensitive by design.
4. **What's the next frontier for Priority #4?** A
   consequence-aware hybrid verdict: a bar that keeps the
   correction-independence (the hybrid's structural
   contribution -- never read the learner's corrected scores)
   while incorporating the stakes K (a world parameter, not a
   label, so no oracle is introduced). Concrete next
   experiments: (i) ThyA_K = max(ThyA, K - margin) and
   variants, preregistered against these profit tables;
   (ii) learner-owned K (opportunity cost learned from train
   consequences); (iii) mapping the K-sensitivity curve to find
   where relative-trust and consequence-optimality align vs
   diverge. The deeper program: characterize when a
   verification specification (labels) and the consequence
   structure (profit) agree, and build verifiers that detect
   their own misalignment.

## Honest caveats

1. One wall-density law-change axis; item law, belief noise, and
   energy budget fixed (inherited from the IVWC lineage).
2. D1b/D2b remain fenced harness diagnostics with a
   researcher-set +40; they stress the verdict structure, not a
   learnable bias.
3. K=15 is a preregistered world cost, chosen near the bar
   center; the profit ranking is K-sensitive (reported as a
   finding, not a flaw).
4. The execute-all reference is counterfactual (fenced); the
   primary metric uses only real GO commitments.
5. Mechanism application, not a composition-novelty or L3 claim.
   The composer is fixed.

## Process notes and disclosures

- **Toolchain incident, disclosed:** during the pre-build source
  audit (after the source was written, before any build or run)
  I accidentally prefixed a shell audit command with
  `python3 -c "print('skip')"`. `python3` is not in the safebin
  PATH, so the invocation failed immediately (command not
  found); it computed nothing, read nothing, wrote nothing, and
  no artifact existed yet to be touched. All work remains pure
  Zag, byte-verifiable from the pinned-znc build. Reported per
  the invocation-based guard; if governance rules this
  PROCESS-FAIL, the clean re-freeze is: rebuild the committed
  source with the pinned znc under safebin and re-run 3x
  (deterministic from source). See NAMECHECK.md Step 0b.
- **Branch repair, same session:** before this lane, the
  `tnn-native-lab` tip tree was found broken (commit 169894404
  with the empty tree; 88e9108f4 built on it with 8 files).
  Repair commit `cef8c4095` restored the tree to `560dd16a3`
  (last good) + the 8 `ivwc_hybrid_clean` files (verified: diff
  shows exactly 8 additions, 0 deletions), via a separate
  GIT_INDEX_FILE; shared index and worktree files untouched. The
  COGOPS-PLEN-ADVANTAGE report artifacts (never committed
  anywhere, not in any worktree) are unrecoverable; the loss is
  documented in the repair commit message. Flagged to the
  parent orchestrator.
- No post-prereg probe of any kind. All predictions were
  arithmetic on the committed verdict-wave per-case tables.
  Every frozen prediction -- all 33 profit numbers, all 3 GO
  count vectors, WC-FINAL=185, all bar values -- confirmed
  exactly.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_applied
$HOME/safebin/znc src/ivwc_applied.zag -o bin/ivwc_applied  # safebin PATH, pinned znc
./bin/ivwc_applied | sha256sum  # expect 366ad663c1136e052f71aaa6dc1bf04a7be3bbc82dd44c292b0a76c1db67e9b8
```

Frozen audits (PREREG K1): A1 phase order
432<439<447<459<465<526<574<582<599<646<672<683<743; A2 0;
A3 0; A4 0; A5 `world_execute(` x4 (1 def + 3 call sites);
A6 WC-FINAL=185; A7 0 `learner_`/`belief_` after line 672;
A8 0; A9 0 `Tpred`. K2: sha256 equality across
runs/ivwc_applied-run{1,2,3}.txt.

## Branch note

Work committed on `tnn-native-lab` in the
`~/workspace/tnn-rsi-gpi3` worktree (prereg commit `bcfebba05`
strictly precedes the implementation commit). All commits use
explicit pathspecs (via separate GIT_INDEX_FILE plumbing, leaving
the shared index untouched) confined to `ivwc_applied/`.
`bin/` (reproducible via the pinned znc) is deliberately
excluded from the commit per Micah's 2026-10-03 guidance. This
is a non-ledger task. Pushing to origin is AUTHORIZED per
Micah's 2026-10-03 authorization; the parent orchestrator should
note the branch repair (`cef8c4095`) and the toolchain
disclosure above before pushing.
