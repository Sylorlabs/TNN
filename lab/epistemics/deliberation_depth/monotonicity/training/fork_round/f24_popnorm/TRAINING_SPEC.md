# F24 POPNORM — Pre-Training Spec Record

**Written BEFORE any training run or build. Date: 2026-09-24.**
**Amended 2026-09-25 for PREREG FROZEN v2 (commit `3a2eef44`); see §13.**
**Fork:** F24 POPNORM (Population-Normalized Confidence), mech 24.
**Frozen authority:** PREREG_FORKROUND.md FROZEN v1 §3(F24) +
  `ideas/native2_forks.md` FORK 1 (authoritative on discrepancy; read in full).

## 1. Frozen pins

- Training cells: `training/features/features.tsv`, 5240 rows, 15 cols
  (id, family, heldout, depth, t, rel4, correct4∈{1,0,A}, f1..f8).
- SHA-256 of the frozen file (verified byte-identical to sylorlabs/TNN @
  `0566cc81`, blob `89fa14ca265f6cdca2494cedb17faafe33bf38d7`):
  `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`.
  **NOTE:** the prereg/task statement prints `...e65e897d` (hex pos 60 = `e`);
  the actual frozen file has `...e65a897d` (`a`). Single-character transcription
  typo in the prereg string; the FILE is canonical and verified against the
  frozen commit. This record uses the true file SHA.
- Heldout flags honored: only heldout=0 rows are training cells.
- Toolchain ONLY: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Harness: `training/src/*.zag` copied byte-identical (SHAs in
  `logs/SRC_SHA256SUM.txt`); verified after copy.
- Eval: 37 legs via `training/run_eval.sh full <bin> 24 0` (gate=0 per
  precedent `run_eval.sh loss10x polbuild/policy_loss_a 17 0`).
- CTL yardstick deltas vs NEC m9 (`ncal/results_nec2/`, B2 pass, B3=6, B13=6).

## 2. f9 definition

- Training: per (family, heldout, depth) group over the TSV,
  f9 = 1000·(N−R_d)/N (integer division, truncation). N = distinct items in
  group; R_d = rows with rel4=1. f9=0 at depth 1 by construction (R_1=N).
  Measured training f9 range: 0..1000 (see §7).
- Eval: per leg, N = item lines in the leg's items file, R_d = released count
  at depth d from the M4 skeleton (release ⟺ L_t==L_1). Same formula.
- f9 is a within-run population statistic (legal per prereg §2 / ideas file).

## 3. Head form

C(s,d) = clamp((Σ_{i=1..8} w_i·f_i)/1000 + b − (w_9·f_9)/1000, 0, 1000),
all integer arithmetic (i64), truncation toward zero via explicit tr_tdiv
(codegen div semantics not trusted for negatives).

## 4. Stage 1 — TRAIN-COORD (frozen spec)

- Params p = (w1..w8, b), init 0. Fixed sweep order w1..w8, b.
- Per sweep, per param: try +50 then −50; first strict objective improvement
  accepted (objective: Σ(C−1000·y)² over depth-1, heldout=0, rel4=1 cells;
  y∈{0,1}); boxes w_i∈[−1000,1000], b∈[−100000,100000]; 8 sweeps max.
- Hard vetoes on every candidate (integer-exact forms):
  - V1 (theater): V1+V2 = 0 over ALL training cells (heldout=0, rel4=1),
    per-(family,id) adjacent-depth pairs in file order. V1: 1→0 with conf
    non-decreasing; V2: 0→0 with conf strictly rising. (Training n10 = 0, so
    the V1 half is vacuous; the V2 half binds.)
  - V2: Σconf ≥ 550·n over depth-1 training correct cells (≡ meanConfCorrect
    ≥ 0.55 exactly, no float).
  - V3: per training (family,depth) with n_rel ≥ 8:
    1000·(S−1000·K) + 80·n ≥ 0 (≡ G ≥ −0.080 exactly), S=Σconf, K=#correct.
- Scoping decision (recorded): objective + veto-V2 on the stage-1 set
  (depth-1 training legs, the cells being fit); veto-V1/V3 on all training
  cells (they are inherently multi-depth). Rationale: vetoes guard the
  shipped head; multi-depth vetoes need multi-depth data.

## 5. SPEC DEFECT — stage 1 infeasible as written (PROVEN, pre-training)

**Theorem.** Under §4 as written, TRAIN-COORD cannot leave the zero init.
*Proof.* Init C≡0. Any single probe moves one param ±50: max achievable conf
on any cell is 50 (w_i=+50: 50·f_i/1000 ≤ 50; b=+50: 50; negative moves give
C≡0 after clamp). Hence meanConfCorrect ≤ 0.05 < 0.55 on depth-1 correct
cells → veto-V2 rejects every probe of sweep 1. Incumbent stays 0; induction
over 8 sweeps → final params = init. ∎
Independent blocks: veto-V1 rejects the natural first moves too (C∝f1 has
125 V2-theater events on training cells), and veto-V3 rejects them
(G(1) ≈ −0.23..−0.50 on admit/revoke/logic/cost for small-conf heads).

**Feasibility of the veto SET (not just the search):** the only heads passing
all three vetoes are near-constant (theater=0 forces w1,w2,w4,w5≈≤0 and
reliance on never-rising f3,f6,f7,f8; those collapse under selection so V3
then forces conf back up to a constant; verified: constant C=920 passes all
vetoes, C∈{920,950,1000} are the feasible constants). Near-constant heads are
degenerate (B5 separation ≈ 0). TRAIN-COORD from 0 cannot reach them anyway
(needs b=920 > 8·50=400 reachable). So the frozen stage-1 is doubly
infeasible: the search can't move, and the feasible set is degenerate.

**Disposition:** two tracks (Micah: "when in doubt, test both").
- **Track L (LITERAL, official):** implement §4 exactly (per-probe vetoes).
  Expected: params = init (empirical check of the proof). §5 go/no-go then
  gives **VOID** (weights = init at checkpoint). This is the frozen-spec
  verdict.
- **Track R (REPAIRED, informative, deviation flagged):** test the POPNORM
  *mechanism* (stage-2 debias) with a working stage-1. Deviation R1: stage-1
  vetoes dropped (proven jointly infeasible for non-degenerate heads; proof
  above); stage-1' = unconstrained TRAIN-COORD argmin on depth-1 cells
  (0 init, ±50, fixed order, 8 sweeps, objective-only). Everything else per
  spec. Track R results are INFORMATIVE (mechanism test), not
  frozen-binding; they cannot earn SUPPORTED under §10.

## 6. Stage 2 — w9 grid (both tracks; runs only if base head is non-init)

- Freeze base (w1..w8, b). Grid w9 ∈ {0,50,…,1000} ascending.
- conf on training cells uses f9 per (family,heldout=0,depth).
- Primary: # strict B3 violations on training legs (families admit, revoke,
  logic, cost, trap, redteam, P, D, O; adjacent depths; violation ⟺
  G(d+1)>G(d), integer-exact via cross-multiplication
  (S2−1000K2)·n1 > (S1−1000K1)·n2; ties not violations).
- Tie-break: Σ over families, d>1 with G defined of |G(d)−G(1)|, f64, fixed
  summation order (family order admit,revoke,logic,cost,trap,redteam,P,D,O;
  depths ascending). Deterministic.
- Extra veto: reject w9 with any training (family,depth), n_rel ≥ 8,
  G < −0.080 (integer-exact as §4 V3). Scoping decision (recorded): n_rel≥8
  applied, matching V3/B13; the ideas text omits the qualifier but its own V3
  and B13 both scope to n_rel≥8 and tiny-n G is noise (FM7). Both scoped and
  unscoped veto counts are reported.
- Selection: min violations → min tie-break → smallest w9. w9=0 always
  eligible (extra veto cannot reject it: base trained under Track R has no
  V3 guarantee — if w9=0 violates the extra veto, the veto is vacuous and
  w9=0 still ships; recorded).

## 7. Measured training-set facts (pre-training; Python probes, not training)

- (family,heldout,depth) f9 values: admit/revoke/logic/cost all 0 (R_d=N at
  every depth — no selection); trap: 0,330,960,1000,1000; redteam:
  0,0,333,666,666; D: 0,250,500,750,750,750,750; O/P:
  0,0,0,250,500,750,1000. R_d nonincreasing in d everywhere ✓.
- Training theater pairs: 179 wrong→wrong adjacent pairs (trap 90, P 70,
  D 15, redteam 4); n10 = 0. f1 rises on 125/179, f2 on 177/179, f4 on
  116/179, f5 on 177/179; f3,f6,f7,f8 never rise.
- Naive head C=f1: V2-theater=125, depth-1 mcc=0.587, G(1) =
  admit −0.229, revoke −0.500, logic −0.500, cost −0.460, trap +0.100,
  redteam −0.133, P +0.310, D −0.050, O −0.690.

## 8. Policy binary (both tracks)

- `src/policy_f24.zag` modeled on frozen `policy.zag`: same M4 release
  skeleton (release ⟺ L_t==L_1), same f1..f8, same TSV columns
  (id depth t rounds consumed ne release correct conf leader_idx cert),
  cert="f24-popnorm".
- f9 computed per leg (N items, R_d released), single pass with per-item
  arena storage ([]u8 + LE accessors; no `as []i32` casts; no zalloc-named
  fns; no slice > 2^25).
- conf = clamp((Σ_{1..8} w_i·f_i)/1000 + b − (w9·f9)/1000, 0, 1000).
- Params baked via generated `f24_params.zag` (Track R) — never hand-edited.
  Base-head binary (mech 124) built from same source with w9=0 params for
  kill conditions (a)–(c).
- A/B byte-identical builds; run_eval.sh A/B byte-identical runs.

## 9. Kill conditions (frozen, operationalized)

Base head = Track R stage-1' (w9=0). F24 = base + fitted w9.
- (a) KILL if eval strict-B3 violations(F24) ≥ violations(base).
- (b) Per eval family, BASE head: OLS slope of G_base(d) on f9(d) over depths
  with defined G (need ≥3 points); "G still rises" = base has ≥1 strict
  violation in the family. KILL if on >1/3 of the 9 eval families
  (i.e. ≥4) the slope is wrong-sign-or-~0 (slope < 1e-4 per f9-thousandth)
  while G still rises. (Slope>0 = premise holds: drift is first-order in
  selection intensity.)
- (c) KILL if eval B13 failures(F24) > B13 failures(base), where a B13
  failure = (family,depth) with n_rel ≥ 8 and G < −0.100.

## 10. Bars (frozen analyze.py + killbars_f24.py)

B1: n10=0. B2: V1=0,V2=0. B3: Gviol=0 per family (strict). B4: aggregate
meanConfCorrect ≥0.50. B4b: per-family mean C on released correct
(n_rel_correct≥10) ≥0.50; honest families = {admit,revoke,logic,cost}
(trap/redteam adversarial; ceiling = stress battery) — all 9 reported.
B5: meanConfCorrect−meanConfWrong ≥0.20 (aggregate). B6: released-correct /
M4 released-correct ≥0.95 per family. B7: abstained/total ≤0.30. B8 amended
(§4b): M4-feasible slots (M4 releases ≥10); ≥4/5 defined slots; nonvacuity
(not all equal within 1e-3 unless all |G|≤1e-6). B9: 100% release+correct
identity vs M4. B12: G>0 crossings recorded. B13: count (F,d) n_rel≥8 with
G<−0.100. B3pi: per-item (conf_{d+1}−acc_{d+1})>(conf_d−acc_d) violations,
recorded.

## 11. Honest expectations (pre-training)

- Track L: params = init → VOID (§5). No eval.
- Track R: stage-1' is a real calibrated head (unconstrained argmin); stage-2
  grid minimizes TRAINING B3 violations. Honest expectation per the ideas
  file: eval violations collapse toward zero, not literal zero (linear
  correction of a nonlinear residue). Kill (a) is the mechanism's clean
  A/B: it fires iff the f9 term buys nothing over the base head.
- B5 risk: the base head is fit for calibration; the f9 term is a leg-level
  intercept shift (preserves within-leg ranking) → B5 should track the base.
- B4/B4b risk (flagged in ideas): debias shifts deep means down; watch
  sparse legs with large f9.
- B13: extra veto guards training; eval risk on sparse legs.

## 12. Deliverables & gates

- Pure Zag, zero RNG (fixed file order, 0 init, integer arithmetic).
- Training ×2 → byte-identical params (.zag cmp). A/B byte-identical builds
  (binary cmp). 37-leg A/B byte-identical runs (run_eval.sh).
- []u8 arenas + LE accessors; no fn named zalloc; slice fields via pointer
  indirection; no slice > 2^25; no bare {...} blocks.
- No binaries / .zagd committed. Incremental commits via
  ~/workspace/commit_racefree.py with TMPDIR=~/workspace/tmp_commit.
- REPORT BACK: kill-bar table, §10 verdict, failure-mode number, commit SHAs.

## 13. v2 AMENDMENT (2026-09-25; PREREG_FORKROUND.md FROZEN v2, commit `3a2eef44`)

v2 §5b repairs the shared TRAIN-COORD (coordinator-issued). v1's trainer
("vetoes on every candidate AND the final answer", init 0) is UNSATISFIABLE:
F25's analytical lock proof (committed `f25_dismin/VERDICT_F25.md`, v1 VOID
stands) shows that from zero init any single ±50 step gives |C|≤50, so the
V2 veto (meanConfCorrect<0.55) rejects EVERY first-step candidate —
data-independent. The proof applies identically to F24's 9 params (same
trainer, same init, same |features|≤1000 bound). F24 completed NO v1
training run (the mode-0 binary panicked on a TSV parser bug before any
training; no v1 params or logs exist), so F24 goes straight to v2; the
v1-lock observation is the analytical proof, cited in the v2 log header.

**Repaired TRAIN-COORD v2** (frozen §5b, implemented literally):
- candidates accepted on strict L-reduction alone (no per-candidate vetoes);
- probe order per param: +50, −50, +8, −8, +1, −1 (first strict improvement
  accepted); fixed param order w1..w8, b; 8 sweeps max (early stop on a
  no-move sweep); init 0; boxes w_i∈[−1000,1000], b∈[−100000,100000].
- Scoping decision (recorded): the "±50, then ±8, then ±1 refine" schedule is
  implemented as the per-param probe order within each of the 8 sweeps (the
  only reading that keeps exactly "8 sweeps" with no invented per-phase
  budget).
- vetoes V1–V3 apply to the FINAL answer only: a final fitted head violating
  any veto → VOID (reported with evidence, no stage 2, no eval).
- F24's stage-2 w9 grid keeps its per-candidate V3 veto (unchanged).
- No kill bar changed; no fork mechanism changed.
- v2 §11(b) also fixes the §2 features.tsv hash typo (`…e65e897d` →
  `…e65a897d`); the file itself was verified correct (confirms §1 note).

The Track L / Track R two-track plan of §5 is superseded: v2 IS the
repair; there is one v2 training pipeline (stage-1' + final veto gate +
stage-2 grid iff vetoes pass).
