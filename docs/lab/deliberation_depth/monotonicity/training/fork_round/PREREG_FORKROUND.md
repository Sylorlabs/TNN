# PREREG — H5 New-Fork Round: What Fixes Overconfidence with Depth?

- **Status:** FROZEN v2 — coordinator sign-off 2026-09-25. v1 remains in
  git history (`0566cc81`). v1→v2 changelog in §11. No building or
  measurement under this prereg until frozen. Any change after freezing
  requires version bump + note.
- **Date:** 2026-09-25
- **Authority:** Micah (2026-09-24): "For H5 test more thoroughly try more
  forks." B3 (strict) is the DEFAULT bar for this round.

## §1 The question

The SR round killed all six arms: scaffold-and-release is *unrefuted as
required* (necessity survives) but *refuted as sufficient* (both scaffold
variants died: crutch collapse, mask-invisible depth schedule). NEC's
per-item ceiling is the only zero-theater mechanism (V1=V2=0) but fails
strict B3 (6: M4 selection effects + tiny-n noise) and B13 (6: ceiling/O
pooling). NEC continued development runs in parallel — this round tests
NEW mechanisms only.

**This round's question:** WHAT mechanism — new, not a NEC iteration —
achieves non-degenerate non-overconfident depth under STRICT B3?
18 forks from four independent idea sources (2 native muse brainstorms,
grok-4.7, fable). Full 37-leg battery per fork, long-horizon legs for
survivors.

## §2 Frozen machinery — reused

- Eval matrix = **37 legs** exactly as `training/run_eval.sh`: admit,
  revoke, logic, trap, cost, redteam × depths {1,2,4,8,16} (30 legs) +
  ceiling × depths {1,2,4,8,16,32,64} (7 legs). A/B byte-identical per leg.
- Policy binary interface: `<polbin> <items> <depth> <gate> <out.tsv>`.
  TSV cols: id depth t rounds consumed ne release correct conf leader_idx
  cert. Forks needing per-item cross-depth state at inference use a
  NEC-style BATCH driver (one binary, frozen ordered cell list, all 37
  TSVs in one run, per-item state in memory) OR per-leg driver with
  deterministic on-disk per-item state (deleted at run start, legs in
  fixed depth order). Either way: A/B byte-identical.
- Metrics from frozen `training/analyze.py`: G(d) = mean_conf − accuracy
  over released cells per (family, depth); Gviol = count of
  adjacent-depth rises G(d+1) > G(d) (tolerance 1e-12); V1 =
  correct→wrong with conf non-decreasing; V2 = wrong→wrong with conf
  rising; n10 = 1→0 correctness transitions.
- M4 release skeleton FIXED (release L_t iff L_t == L_1). B9 requires
  100% release+correct identity vs M4 per fork — any disagreement =
  implementation bug: stop, fix, re-run. Forks may NOT change the release
  rule; the battleground is the confidence head.
- Training cells: `training/features/features.tsv` (5240 cells, SHA256
  `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`),
  heldout flags honored (odd P/O/D replicates never trained).
- Harness modules in `training/src/` may be copied byte-identical
  (SHA-verified) into fork trees.
- CTL yardstick: NEC m9 (B2 pass, B3=6, B13=6). Every fork's numbers
  reported as deltas vs NEC.

## §3 The forks (FROZEN)

Full frozen specs in `fork_round/ideas/`: `native1_forks.md`,
`native2_forks.md`, `fable_forks.md`, `grok_forks.md` (+ raw transcripts).
Each fork's falsification conditions are in its source file and are part
of this freeze. Mechanism IDs 20–37.

### Native brainstorm 1 (`ideas/native1_forks.md`)

- **F20 USD — Unearned-Stability Discount.** New feature
  f9 = max(0, (f6+f7)/2 − f5) (stability−evidence gap, the trap
  signature). Head: C = clamp((Σ_{1..8} w_i·f_i − w9·f9)/1000 + b, 0, 1000),
  w9 ≥ 0 by projection. Targets FM6 (selection concentrates traps) via
  FM2. Kill: trap/redteam B3 violation at n_rel≥16, or B4<0.50 honest,
  or w9→0.
- **F21 GRAF — Per-Depth G-Anchored Fitter.** Head form UNCHANGED;
  training objective becomes
  L = Σ_d n_d·G(d)² + λΣ(c−y)² + μΣ max(0, c_{d+1}−c_d),
  deterministic integer coordinate descent. Fits calibration on the
  population each rung is scored on. Targets FM6 directly, B2 via μ.
  Kill: any full-n leg still violates B3 (capacity problem), or B3
  passes while B2 fails (bar-gaming).
- **F22 FORESHADOW — Foreshadow Head.** New feature
  f9 = predicted P(release at d+1 | state at d)
  = clamp(1000 − [α(1000−f1) + β·f3 + γ(1000−f6) + δ·f8]/1000, 0, 1000),
  α,β,γ,δ ≥ 0 fitted. Head subtracts w9·(1000−f9)/1000, w9 ≥ 0.
  Discounts conf BEFORE doomed releases. Targets B2 theater at root,
  FM5, FM1. Kill: V1+V2>0 at n_rel≥16, or α..δ→0, or B4<0.50 honest.
- **F23 SELFNORM — Self-Normalized Margin Head.** f1' =
  1000·f1/max(64, trailing-max f1); f4' likewise on |f4|. Each item its
  own yardstick; rewards growing decisiveness (f4'>0) traps can't fake.
  Targets FM1, FM8, FM3. Kill: clamps persist (>50% cells at 0/1000),
  or theater rises vs baseline, or w1(f1')→0.

### Native brainstorm 2 (`ideas/native2_forks.md`)

Shared deterministic trainer TRAIN-COORD (coordinate descent, ±50 steps,
8 sweeps; vetoes: theater>0 reject, train meanConfCorrect<0.55 reject,
train G<−0.080 at n_rel≥8 reject).
- **F24 POPNORM — Population-Normalized Confidence.** Leg-level feature
  f9 = 1000·(N−R_d)/N (selection intensity). Two-stage: fit base on
  depth-1 legs, freeze, fit w9 to minimize training B3 violations.
  Subtracts first-order compositional drift. Targets FM6, FM7. Kill:
  eval B3 ≥ base, or drift-vs-f9 wrong-sign on >1/3 families, or B13
  worse than base.
- **F25 DISMIN — Disjoint-Feature Min Ensemble.** A on f1..f4, B on
  f5..f8, C = min(A,B) + Δ bias-shift (Δ∈{0,50,…,500} grid). No new
  features. Targets FM2 (crutch), FM1, FM3. Kill: veto rate <2% with no
  B3/B8 gain, or B4 fails after full Δ, or correlated crutches.
- **F26 EFFIC — Deliberation-Efficiency Head.** f9 =
  f1·1000/(1000+q), q = cumE·1000/E_ref (evidence spent vs leg median).
  Margin discounted by what it cost. Targets FM8, FM5. Stillborn gate:
  within-leg std(q)<100 on >50% training legs → report, don't eval.
  Kill: high-depth B3/B8 no better than base despite live q, or w9→0.
- **F27 DIVETAX — Divergence-History Honesty Tax.** f9 = 1000·D/d,
  D = depths k<d with L_k≠L_1. Head subtracts w9·f9/1000, w9≥0. Taxes
  returnees M4's endpoint-blindness misses. Targets FM6 (returnees),
  traps. Stillborn gate: fire rate <5% on training → report, don't eval.
  Requires harness leader-history observable — verify first; missing =
  STILLBORN. Kill: w9=0, or taxed cells MORE accurate (wrong sign), or
  B3 ≥ base.

### Fable (`ideas/fable_forks.md`)

- **F28 DEB — Differential Evidence Budget.**
  budget_0=1000;
  budget_t = clamp(budget_{t−1} + margin_t·(1000/nh) − t·1000/64, 0, 1000);
  C = clamp(min(budget_t, clamp(margin_t·1000/nh,0,1000)), 0, 1000).
  Depth-charge coefficients never increase during learning. Targets
  FM1 structurally; Q2 predicts beats NEC on logic/admit deep, loses on
  redteam/trap. Kill: B3 no better than NEC (structurally blind to FM6).
- **F29 DG — Disagreement-Geometry Head.** D_t = pairwise survivor
  disagreement fraction (thousandths); S_t = 1000−D_t; ΔD_t velocity;
  depth_suppress(t) = 1000−t·1000/64.
  C = clamp((S_t·w_s + margin_t·w_m + (1000−clamp(ΔD_t,0,1000))·w_v
  + depth_suppress·w_d)/1000, 0, 1000), weights ≥0 sum ≤1000.
  G-rise-reversing weight ratchet in training. Requires survivor
  hypothesis values — verify observable; missing = STILLBORN. Targets
  FM6 via population structure; dies to adversarial convergence (FM4).
  Kill: V2>0 on converged-wrong survivors, or B3 ≥ base.
- **F30 THAC — Two-Head Adversarial Cap.** P(s) optimistic predictor;
  C_n(s) = clamp(min(margin_t, 1000−t·1000/64,
  1000 if nalive≤2 else nalive·1000/nh) + b_c, 0, 1000), b_c∈[−500,0];
  C = min(P, C_n). Censor trained adversarially on predictor's
  overconfident items. Asymmetric suppress-only guarantee; structural
  B2 on censor-bound items. Targets FM6 via monotone suppression.
  Kill: B4/B5 damage on honest ceiling (global schedule over-suppresses),
  or B13 from blanket depression.
- **F31 DDCL — Depth-Discounted Calibration Ledger.** Base B(s) linear;
  per-depth FIFO ledger (cap 2048) of (conf, correct);
  offset(d) = clamp(G_empirical(d)·damp, −200, 200), damp∈[200,800]
  meta-adapted; C = clamp(B(s) − offset(d), 0, 1000). Directly measures
  and corrects G(d); offset cap structurally blocks clamp death.
  Targets FM6 empirically, B13. Kill: feedback oscillation (offset
  hits cap and G still rises), or redteam tiny-n B3 ≥ base.

### Grok-4.7 (`ideas/grok_forks.md`)

Shared: interior-ratio invariant ρ(k,n)=(k+1)·1000/(n+2) ∈ [1,998]
(clamps unreachable); d_idx=log2(d); updates after label observed;
release rule untouched. The selection identity
G(d)−G(d−1) = E_d + δ_d − ΔA_d is the design substrate.
- **F32 RSW — Regime-Switch Calibrator.** Ledgers over key (m=min(4,f1/200),
  yld=min(2,my/400)), 15 keys × 7 depths; one-bit regime LATCH/TRACK per
  key switching on measured deep-vs-shallow accuracy gain γ≥100 (with
  hysteresis); LATCH: C=clamp(C*+min(S_d,0),1,999); TRACK follows ρ(d).
  Closed-form δ_d = ΔA_d − E_d − β. Flip/trauma: C←min(C,C_prev−1).
  Targets FM6 (subtracts selection), FM1 (ρ codomain), FM2 (no f7).
  Kill: LATCH key with accuracy gain >100, or TRACK key with G<−0.10
  at n_rel≥8 (bin bias).
- **F33 SRS — Selection-Residual Subtraction.** RSW's shift, no regime
  bit: depth-1 base C* from margin×survivor ledger; per-key global δ_d =
  ΔA_d − E_d − 3, |δ_d|≤40; C = clamp(C* + Σδ_j − π, 1, 999),
  π = min(400, 1_{f3>0}·50 + max(0,f8−f8^(1))/8) on flip/trauma.
  Solved identity, no controller lag. Targets FM6 via accounting.
  Kill: applied δ vs recomputed δ diverge (non-stationarity), or
  cross-family pooling false (E_d sign flips across families ≥3 depths).
- **F34 LSTWBA — Latched State Tax, Worst-Boundary Adversary.**
  Depth-1 latch C*=ρ; tax table T[d][r]≥0 monotone in depth; worst
  boundary d*=argmax(g[d]−g[d−1]) gets +1 tax per released item;
  decrement path on g<−80; region-level B4 freeze at correct-mean 520.
  Per-family ceiling without family labels (the family is discovered as
  the region whose G misbehaves). Targets FM6, structural B2 (monotone
  tax + flip −1). Kill: taxes never settle after 10^4 items, or region
  with g[d]−g[d−1]>0 at n≥30 after taxes freeze.
- **F35 CDC — Cluster-Discovered Ceilings.** Online L1 prototypes over
  x=(f1,f5,f6,min(f8,1000),my), K≤8, data-determined τ; per-cluster SRS
  residuals; yield gate on cluster transitions. Targets FM8 (split
  pooled populations before residual estimation), FM6 per cluster.
  Kill: I(cluster;battery)≈0 (discovery failed), or partition never
  stabilizes in 2000 items.
- **F36 MEY — Marginal-Yield Ledger.** Key q=(m,y) with y=min(3,my/250);
  depth is a STRATUM not an input; C=ρ(k_{q,d},n_{q,d}); path rule:
  yield drop blocks confidence rise (min(C,C_prev)); f2 deleted from
  the function class. Targets elapsed-depth inflation, FM6 partially.
  Kill: nondecreasing-f5 items still show C-slope > accuracy-slope at
  n≥30 (causal claim wrong); predicted B13/B4b risk on saturated
  ceilings.
- **F37 IFP — Interior Fixed-Point Head (control).** Contracting emit
  C=(A_d+max(s,0))·1000/(B_d+|s|+max(−s,0)+1) ∈ [1,998] via permanent
  pseudocounts; mandatory weight decay; outward-gradient freeze;
  monotone depth coupling of base rate (μ_d ≤ μ_{d−1}+20). Isolates
  "fix the dynamics" (FM1/FM3) from "fix selection". Expected: B2 fail
  via margin. Kill (fixed-point, not bars): max|w_i| grows linearly
  with t after 10^4 updates, or >5% emits in [1,20]∪[980,999].

## §4 Kill-bar table (preregistered; B3 strict is DEFAULT)

"Achieves non-degenerate non-overconfident depth" = clears ALL of B1–B9
(+B4b, +B13). SUPPORT withheld on any failure.

| # | Bar | Measurement (frozen analyzer, 37-leg matrix) | Threshold | Applies to |
|---|---|---|---|---|
| B1 | §1 accuracy | 1→0 transitions (n10) | = 0 | all |
| B2 | Theater | V1 = 0 and V2 = 0 | = 0 | all |
| B3 | Law (strict, DEFAULT) | G-violations per family | = 0 every family | all |
| B4 | Non-degenerate | meanConfCorrect (aggregate) | ≥ 0.50 | all |
| B4b | Honest-family floor | mean C on released correct, per honest family (n_rel_correct ≥ 10) | ≥ 0.50 | all |
| B5 | Separation | meanConfCorrect − meanConfWrong | ≥ 0.20 | all |
| B6 | Recall | released-correct / M4 released-correct, per family | ≥ 0.95 | all |
| B7 | Abstention volume | abstained / total cells (aggregate) | ≤ 0.30 | all |
| B8 | G-definedness (AMENDED §4b) | per §4b | pass | all |
| B9 | Answer channel frozen | release+correct identity vs M4 | 100% | all |
| B12 | Refined reading | G>0 crossings | recorded (does not kill) | all |
| B13 | Underconfidence floor | per (F,d), n_rel ≥ 8: G(F,d) | ≥ −0.100 | all |
| B3pi | Per-item B3 (RECORDED) | per-item conf_i(d+1)−acc_i(d+1) ≤ conf_i(d)−acc_i(d) violations | recorded (does not kill) | all |

### §4b B8 amendment (coordinator-signed; defect documented in SR round)

The frozen B8 was defective: (a) the flatness clause killed *genuine*
perfect calibration (revoke/logic/cost G≡0.000000); (b) the defined-count
clause was unsatisfiable under B9+M4's skeleton (trap d8/d16: 0 released
cells). Amended B8:
- **B8-definedness:** denominator = depth slots where M4 itself releases
  ≥10 cells ("M4-feasible slots"). Pass iff G defined on ≥4 such slots
  (5-depth families) / ≥5 (ceiling). Fewer M4-feasible slots than asked
  → B8 VOID for that family (recorded, kills nothing).
- **B8-nonvacuity:** defined G values must not be all equal within 1e-3,
  EXCEPT all-equal with |G| ≤ 1e-6 passes (genuine perfect calibration).

### §4c Per-item B3 (recorded, not killing)

Fable's Q5 argues strict family-mean B3 is unsatisfiable under M4
(fixed-point circularity: the released population is a function of the
head's own output). This is RECORDED as an open adjudication question,
not adopted: Micah set strict B3 as the default bar. B3pi is measured so
the data can speak — if every fork fails B3 but passes B3pi, the
unsatisfiability thesis gains evidence and goes to Micah as a
prereg-amendment question.

## §5 Per-fork go/no-go (training checkpoint)

Training-based forks: weights ≠ init at checkpoint; plus the fork's
liveness signal from its ideas-file spec (spread correlation, variance
floor, fire rate, veto rate, stillborn gates for F26/F27). An arm whose
intervention is provably dead at checkpoint is VOID (reported with
evidence, not "killed"). Non-training forks skip this section.
Observable-verification FIRST: F27 (leader history) and F29 (survivor
hypothesis values) must verify their observables exist in the frozen
inputs before building — missing = STILLBORN (reported, not killed).

### §5b TRAIN-COORD defect repair (v2; coordinator-issued, see §11)

TRAIN-COORD as specified in `ideas/native2_forks.md` ("vetoes applied to
every candidate AND the final answer", all params init 0) is
UNSATISFIABLE as written. Proof (F25 v1 run, committed evidence in
`f25_dismin/VERDICT_F25.md`): from the zero init, any single ±50
coordinate step yields |C(s)| ≤ 50 on every cell (|features| ≤ 1000),
so training meanConfCorrect ≤ 0.05 < 0.55 and the V2 veto rejects EVERY
first-step candidate — the trainer is analytically locked at init,
data-independently. Applies identically to F24, F26, F27 (same trainer,
same init). F25's v1 VOID stands as committed evidence of the defect;
the fork mechanisms themselves were never tested.

**Repaired TRAIN-COORD v2** (F24, F25, F26, F27 only): coordinate descent
accepts candidates on strict L-reduction alone (±50, then ±8, then ±1
refine; fixed order; 8 sweeps; init 0 — unchanged). Vetoes V1–V3 apply to
the FINAL answer only: a final fitted head violating any veto is VOID
(reported with evidence). This preserves the vetoes' evident intent —
reject degenerate *solutions* (theater, clamp attractors, blanket
underconfidence) — while making the stated objective (minimize squared
calibration error) reachable. No kill bar is changed; no fork mechanism
is changed. F24's stage-2 w9 grid keeps its per-candidate V3 veto (it
starts from nonzero fitted base weights, so it is not locked).

## §6 Long-horizon legs (survivors only)

Any fork clearing B1–B9+B13 on the 37-leg short battery advances to
long-horizon: the same 37-leg matrix at the 100× training/stream scale
(training forks: 100× curriculum epochs; online-state forks: 100× stream
length via repeated battery passes in fixed order). The depth law must
hold at 100× (zero confident disagreements); red-team at horizon; all 6
vectors contained. A fork dying at horizon is KILLED AT HORIZON (a
short-battery pass is not a survive).

## §7 Failure-mode taxonomy (carried + open for update)

Carried: (1) clamp attractors; (2) crutch collapse; (3) uniform-manifold
escape; (4) spread anti-learning; (5) mask-invisible depth schedule;
(6) M4 selection effects; (7) tiny-n noise; (8) ceiling/O pooling. Any
fork death by a NEW mechanism gets a numbered entry + name in VERDICT.md.

## §8 Build & determinism gates

Pure Zag, zero RNG (fixed file order, fixed inits, integer arithmetic).
Pinned toolchain ONLY:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
A/B byte-identical builds AND runs. All large tables on []u8 arenas with
explicit LE accessors (ZNC-2026-09-21-007). No function named `zalloc`;
slice fields via pointer indirection; no slice > 2^25 bytes; no bare
`{...}` blocks in function bodies. Per AGENTS.md throughout. Training run
twice → byte-identical params. No binaries or .zagd committed.

## §9 Deliverables

`deliberation_depth/monotonicity/training/fork_round/`: this prereg
(frozen; v1 in git history, current v2), `ideas/` (four source files +
raw transcripts),
per-fork dirs `f20_usd/` … `f37_ifp/` (src, params, logs, results,
analysis), `VERDICT.md` (final adjudication + updated taxonomy).
Branch: `tnn-native-lab`. The frozen prereg is committed BEFORE any
fork's first build.

## §10 Adjudication

Per fork: SUPPORTED (clears B1–B9+B13 short + survives §6 horizon) /
PARTIAL (honest families clear, adversarial residual characterized) /
KILLED (failing bar named + failure-mode number) / DEGENERATE (passes
law bars only by degenerate compliance — named, does not count) /
VOID (§5) / STILLBORN (§5). The round succeeds iff it names what, if
anything, makes depth non-overconfident under strict B3 — or kills every
fork honestly. Fable's Q5 unsatisfiability thesis is adjudicated on the
B3-vs-B3pi evidence and goes to Micah only as a question, never as a
silent bar change.

## §11 Changelog

- **v1** (2026-09-25, commit `0566cc81`): initial freeze. 18 forks,
  strict B3 default, amended B8, recorded B3pi.
- **v2** (2026-09-25): (a) §5b TRAIN-COORD defect repair — v1's shared
  trainer ("vetoes on every candidate", init 0) is provably unsatisfiable
  (analytical lock proof + byte-identical empirical logs in
  `f25_dismin/`, committed `8461c659`); vetoes now gate the final answer
  only. No bar changed, no fork mechanism changed. F25's v1 VOID stands
  as evidence; F24/F25/F26/F27 train under v2. (b) §2 features.tsv hash
  typo fixed (`…e65e897d` → `…e65a897d`; file itself verified correct).

---
*End of PREREG_FORKROUND.md FROZEN v2 — coordinator sign-off 2026-09-25.*
