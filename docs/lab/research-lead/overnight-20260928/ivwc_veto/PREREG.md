# PREREG.md -- IVWC-VETO: verifier veto (selective execution)

Frozen: 2026-10-03. This document fixes the experimental design
and the kill bars K1..K8. It must be committed ALONE (with
NAMECHECK.md, no implementation) before any implementation work.
The prereg commit must strictly precede the implementation
commit. Amending a bar after results invalidates the verdict.

## 1. What this wave is

IVWC-EXPAND3 showed the learner CAN verify its own work
pre-execution (consequence-trained bucket verifier, 9/12 vs 7/12
baseline, interpretable "exactly one gather" rule), but the
verdict never ACTED on anything: every plan was executed anyway.
This wave closes the loop: the verifier VETOES low-verdict plans
(selective execution). The learner commits veto decisions BEFORE
any sealed consequence, then executes only non-vetoed plans.

Incorporated by reference (unchanged): the world generator, the
belief generator, the NAV+GATHER composer, the consequence
simulator, the bucket verifier (train + check), all frozen seeds,
the wp=15/30/45 law-change dial, and the 12 sealed case
identities -- all from ivwc_expand3/PREREG.md sections 2-4 and
ivwc_expand3/src/ivwc_expand3.zag. The revision protocol and the
shuffled-consequence ablation are REMOVED (separate mechanisms,
not part of this question). The sealed (bucket, eff) pairs are
therefore bit-identical to expand3's; expand3's run1 V-lines are
used below ONLY to calibrate bar directions (prior data, not a
substitute for the fresh run -- the verdict is computed from the
fresh run's own numbers).

## 2. Veto design

Per sealed shift (wp in {15, 30, 45}), per sealed case s:

- VETO COMMIT (batched, before any sealed world_execute):
  learner_compose on beliefs -> plan + bucket; verifier_check on
  the frozen train table -> verdict. Three veto policies decide:
  - P1 (learner): VETO iff verifier_check(vb, bucket)==0, i.e.
    the bucket has no train data or its train mean is below the
    LEARNER-COMPUTED threshold T (tot/n over train
    consequences). No researcher-set constant anywhere.
  - P2 (fixed strict control, researcher-written): VETO iff
    bucket != 1 (execute only the "exactly one gather" bucket --
    the interpretable rule expand3's table implemented).
  - P3 (fixed lax control, researcher-written): VETO iff
    bucket == 0 (veto only empty plans; the naive conservative
    fixed rule).
  - P0: no veto (execute all) -- baseline.
  P2/P3 are comparison controls only; the learner's policy is
  P1. Decisions are stored; a world-call counter check (wc
  unchanged) enforces commit-before-signal (K1).
- CONSEQUENCE (single harness pass): every committed plan is
  executed once through the deterministic world; per-case
  (collected c, energy u, eff = (100*c)/u, plan length L) is
  recorded. Selective execution is then realized as
  pre-committed SELECTION over these deterministic
  consequences: for policy p, vetoed cases contribute nothing
  (no energy, no collection); executed cases contribute their
  recorded (c, u). Because the world is deterministic and plans
  are frozen at commit, this yields bit-exactly the outcomes
  physical selective execution would produce; the veto decision
  precedes any sealed consequence (K1), and the learner never
  observes the harness pass.

Per shift, per policy p, the program accumulates (integer):
- ne[p], nv[p]: executed / vetoed counts
- W[p]: wasted executions = #{executed with eff < T}
- ns[p]: successes = #{executed with eff >= T}
- sumc[p], sumu[p]: collection / energy over executed
- esav[p]: energy saved = sum of L over vetoed
- cforf[p]: collection forfeited = sum of c over vetoed
  (counterfactual: what the veto gave up)
- se_sum[p], se_n[p]: eff sum/count over executed
- sv_sum[p], sv_n[p]: eff sum/count over vetoed

Findings (not bars): global efficiency U[p] = 100*sumc[p]/sumu[p]
(needs per-case c,u; reported, not barred), collection totals,
esav/cforf, and the P1-vs-P2 veto-set identity per shift.

## 3. Frozen kill bars

- K1 (commit before signal): PASS iff all in-program checks
  hold: world-call counter == 0 after train COMMIT, and unchanged
  across each shift's VETO COMMIT, AND the section-4 audits
  confirm code ordering and the learner section contains no
  world-truth tokens.
- K2 (no disguised oracle): PASS iff the section-4 audits hold
  (no expected|answer|key|target tokens; no
  correct|reference_plan|gold tokens; == only physics/action/local;
  no reference plan; verifier inputs are consequence-derived
  (bucket, eff) pairs; T learner-computed; veto decisions use
  only (verdict, bucket)).
- K3 (fewer wasted executions, wp=15): PASS iff
  W[1] < W[0] (strict). The learner veto must strictly reduce
  the count of executed plans with eff < T.
  Calibration (expand3 V-lines, wp=15): W[1]=1 < W[0]=5.
- K4 (higher success rate among executed, wp=15): PASS iff
  ne[1] > 0 and ns[1]*ne[0] > ns[0]*ne[1] (strict).
  Calibration: 5*12=60 > 7*6=42.
- K5 (determinism): PASS iff 3 runs byte-identical (equal
  sha256).
- K6 (learner threshold beats naive fixed rule, wp=15): PASS
  iff W[1] < W[3] (strict). The learner-computed threshold must
  waste strictly less than the fixed lax control.
  Calibration: W[1]=1 < W[3]=3.
- K7 (veto stays targeted under strong law change, wp=45):
  PASS iff sv_n[1] > 0 and se_n[1] > 0 and
  sv_sum[1]*se_n[1] < se_sum[1]*sv_n[1] (strict). The vetoed
  set's mean counterfactual eff must sit strictly below the
  executed set's mean eff even where the verifier's accuracy
  edge went negative (expand3: +2 -> -1).
  Calibration: 0*3 < 100*9.
- K8 (veto still avoids waste at wp=45): PASS iff
  W[1] < W[0] (strict).
  Calibration: W[1]=2 < W[0]=11.

Verdict: BUILD-PASS iff K1..K8 all PASS. Any FAIL yields
BUILD-FAIL naming the failed bar. VOID conditions: any
forbidden-interpreter invocation (PROCESS-FAIL), or any
amendment to this prereg after implementation begins.

## 4. Frozen audit commands (run at report time, shell only)

- A1 (phase ordering): in src/ivwc_veto.zag, within the sealed
  shift loop, the VETO COMMIT block (learner_compose /
  veto_p1 call sites, no world_execute) textually precedes the
  CONSEQUENCE block (world_execute call sites). Verified by
  reporting grep -n line numbers: every learner_compose and
  veto_p1 call line in the commit block is smaller than every
  world_execute call line in the consequence block.
- A2: the LEARNER section (between the `// ===== LEARNER =====`
  and `// ===== MAIN =====` markers) contains zero occurrences
  of `world_buf` or `world_off`.
- A3: zero occurrences of `expected|answer|key|target` in the
  .zag (grep -c -E).
- A4: zero occurrences of `correct|reference_plan|gold` in the
  .zag (grep -c -E); `==` occurrences are physics/action/local
  comparisons only (spot-checked in report).
- A5: sha256 equality across runs/ivwc_veto-run{1,2,3}.txt.

## 5. Why the bars discriminate

- K3/K4 are the direct operationalization of "does selective
  execution improve outcomes": they fail if the veto
  mis-targets (vetoes good plans while executing bad ones) or
  is no better than executing everything.
- K6 discriminates the threshold question: if the
  learner-computed T were no better than the naive fixed rule
  (veto only empties), W[1] would tie or exceed W[3] and the
  bar fails. P2 (the strict fixed rule) is kept as a finding:
  at wp=15 the learned table implements exactly the bucket-1
  rule, so P1 and P2 should select identical sets -- a
  checkable interpretability claim, not a bar.
- K7/K8 discriminate the law-change question: expand3 showed
  the verifier's accuracy edge goes negative at wp=45. K7/K8
  fail if vetoing under degradation stops being targeted
  (vetoed plans as good as executed ones) or stops saving
  waste. The calibration suggests veto can remain useful even
  when the verdict-accuracy edge is negative, because the
  environment's waste density changes too -- that is the
  empirical claim under test, and the bars would fail if the
  dial behaved otherwise.

## 6. What is NOT claimed

Mechanism test of the veto loop, not a composition-novelty or
L3 claim (per expand3 PREREG section 3, incorporated by
reference). The verifier is a fixed bucket table; the claims
concern whether acting on the verdict improves outcomes, which
threshold does it best, and how the benefit interacts with law
change. One wall-density law-change axis; item law, belief
noise, and energy budget fixed. The energy-saved and
collection-forfeited figures are exact under the deterministic
world, not measured physical savings; the decision to veto is
the learner behavior under test.
