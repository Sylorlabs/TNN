# PREREG.md -- IVWC-CASEBIAS: case-level bias signals for phantom-type errors

Frozen: 2026-10-03. This prereg is committed alone before any
implementation. The implementation commit must strictly follow it
(K1 commit-order self-check). Non-ledger task (claim minting paused).

## 1. Question

IVWC-SCOREBIAS closed the score side: V-UCB is the first strict
in-distribution gain (11/12 @15) but strict dominance is blocked
by two structural ceilings. Ceiling 1 (@15): s=3 (phantom items,
P=50) shares bucket 1 with four genuine positives (P=33); no
per-bucket bias fixes s=3 without breaking four correct verdicts
first. Recommended follow-up #1: "Case-level (not bucket-level)
bias signals for phantom-type errors like s=3 -- the bias must
see what the bucket cannot."

This wave tests whether a bias signal operating at the CASE
level (individual problem, learner-visible features) fixes s=3
without breaking the four genuine bucket-1 positives, i.e.
whether case-level bias reaches 12/12 @15, and whether it helps
@45.

## 2. Load-bearing facts (from the scorebias REPORT.md per-case
## details and the learner-visible train T-lines; no sealed
## truth used)

- Train bucket-1 overconfidence d = preff - eff:
  {0,0,0,0,0,0,33} (t=3,5,6,9,10,13,17).
- Train cases with (bkt=1, preff=50): t=3, t=9, t=10, t=13 --
  4/4 GENUINE (eff=50, d=0). The single train bucket-1 miss is
  t=17 (bkt=1, preff=33, eff=0, d=33).
- Sealed @15: s=3 is (bkt=1, preff=50, eff=0) -- a PHANTOM whose
  (bucket, preff) signature is, in the train diet, perfectly
  associated with genuine outcomes. The four genuine positives
  s=2,4,7,9 are (bkt=1, preff=33, eff=33).
- UCB baseline (frozen, recomputed in-program): 11/12 @15
  (error {s=3}), 10/12 @45 (errors {s=0, s=4}).

## 3. Frozen case-level variants (all trained on the 24 train
## cases only; no sealed data; no researcher-set constants)

Let UCB[b] = (0,16,27,20) be the frozen scorebias UCB biases,
recomputed in-program. Let d_t = preff_tr[t] - eff_tr[t] and
resid_t = d_t - UCB[bkt[t]]. All three variants refine UCB with
a case-level residual table (mean resid, integer floor; empty
cell -> 0):

- V-CONDC (vv=1, conditional): R1[b][p] = mean resid_t over
  train cases with bkt=b AND preff=p (4x101 table).
  bias[s] = UCB[bkt[s]] + R1[bkt[s]][preff[s]].
  Tests: finer-than-bucket score conditioning -- "what the
  bucket cannot see" at its most direct (P=50 vs P=33).
- V-AGREE (vv=2, internal-prediction confidence): run the three
  independent composer paths (fwd, rev, nn) on each case;
  agree = 1 + (g_rev==g_fwd) + (g_nn==g_fwd) in {1,2,3}.
  R2[a] = mean resid_t over train cases with agree=a.
  bias[s] = UCB[bkt[s]] + R2[agree[s]].
  Tests: multi-path agreement as a learner-computable
  confidence proxy for the committed plan.
- V-STRUCT (vv=3, structural): bumpbin from the internal
  simulation's believed bumps: 0 / 1-2 / 3+.
  R3[b][bb] = mean resid_t over train cases with bkt=b and
  bumpbin=bb (4x3 table).
  bias[s] = UCB[bkt[s]] + R3[bkt[s]][bumpbin[s]].
  Tests: structural features of the learner's own internal
  simulation trace.

Shuffled ablations (vv=4,5,6): same three tables built from the
rotate-by-7 shuffled d (ds_t = preff_tr[t] - seff[t]).
vv=0 is the UCB anchor. Anchors OF, X3, HYB(>=), MG(>) are
re-scored in-program for K3/K4.

Each variant: adjV[s] = preff[s] - biasV[s]; TV = mean adjV
over the sealed batch; verdict = adjV > TV (strict margin,
same family as scorebias). World/belief/composer/stepper/
verifier/seeds are verbatim copies of IVWC-SCOREBIAS, so K3/K4
anchors verify bit-identical sealed pairs.

## 4. Frozen kill bars

- K1 (diet / commit-order): in-program K1T/K1P/K1S
  STRUCT-PASS; shell audits A1-A8 with frozen counts:
  A1 phase ordering (train COMMIT/PREFF before train CONSEQ
  world_execute; sealed VERDICT COMMIT before SCORING
  world_execute); A2 zero world_buf/world_off tokens in the
  LEARNER section; A3 zero expected/answer/key/target tokens;
  A4 zero correct/reference_plan/gold tokens; A5 sha256
  equality across runs/ivwc_casebias-run{1,2,3}.txt; A6
  world_execute( count = 3 (def + 2 call sites),
  WC-FINAL=60 (24 train + 36 sealed); A7 zero learner_*
  calls after the sealed COMMIT phase; A8 zero oracle
  tokens in the LEARNER section (the oracle diagnostic is
  fenced inside the harness SCORING section only).
- K2 (determinism): 3/3 byte-identical stdout (shell sha256).
- K3 (@15 replication anchor): acc_of=10 AND acc_x3=9.
- K4 (@45 replication anchor): acc_of=8 AND acc_x3=10.
- K5 (HEADLINE, case-level fixes s=3): exists V in
  {CONDC,AGREE,STRUCT} with accV@15 = 12.
- K6 (no harm @15): every V in {CONDC,AGREE,STRUCT} has
  accV@15 >= 11.
- K7 (@45 gain): exists V in {CONDC,AGREE,STRUCT} with
  accV@45 > 10.
- K8 (no harm @45): every V in {CONDC,AGREE,STRUCT} has
  accV@45 >= 10.
- K9 (mechanism: the train diet forbids fixing s=3):
  in-program check that all four train cases with bkt=1 AND
  preff=50 have d=0 (count=4, all d==0). STRUCT-PASS required.
- K10 (even the oracle cannot win with (bucket,P)
  conditioning): harness-side diagnostic (SCORING section,
  clearly fenced, NOT a learner variant): fit per-(bucket,
  preff)-cell mean bias on the SEALED labels, apply with the
  transductive bar, report accuracy @15. Bar: oracle @15
  accuracy <= 11.

## 5. Frozen mechanism predictions (derived pre-implementation
## from the train diet; sealed V-lines of scorebias not re-read
## beyond the published REPORT.md per-case details)

- V-CONDC @15: 11/12, error {s=3}. Train cell (1,50) has
  resid -16 x4, so R1[1][50] = -16 and bias(s=3) = 0 (down
  from UCB's 16): adjV[3] rises 34 -> 50. Train cell (1,33)
  resids (-16,+17) average to 0, so the four genuine
  positives keep bias 16, adjV 17. All other sealed
  (bkt,preff) cells are empty in train (R=0). New sealed sum
  = 172, TV = 14; s=3 (50 > 14) stays PASS/wrong, everything
  else holds. The honest train-fit case-level correction
  moves the WRONG way for s=3: the diet says (1,50) is safe.
- V-AGREE @15: 11/12. Bucket-1 cases gather a single believed
  item under all three policies (agree=3/3 in train and
  sealed); agreement does not separate the train phantom
  t=17 from train genuine cases, so R2[3] is near zero and
  s=3 keeps ~UCB bias.
- V-STRUCT @15: 11/12. Phantom-ness is an independent
  belief-noise coin flip; believed bumps do not separate
  train phantoms from genuine cases.
- @45: all three variants 10/12 (errors {s=0, s=4}, same as
  UCB). Train cell (1,50) resid -16 -> bias(s=0)=bias(s=4)=0,
  adjV=50, still above the bar; the genuine s=11 (1,100)
  keeps bias 0, adjV=100, stays correct.
- K5: FAIL. K6: PASS. K7: FAIL. K8: PASS. K9: PASS.
  K10: PASS -- hand computation: oracle (bucket,preff)-cell
  mean bias @15 gives adjV = {0,0,33,0,33,33,20,33,0,33,25,
  13}, sum 223, TV=18; s=6 (20>18) and s=10 (25>18) flip to
  wrong PASS while s=3 is fixed: 10/12. Even the oracle
  (bucket,P) bias cannot beat UCB's 11/12 under the
  transductive bar.

Predicted verdict: BUILD-FAIL (K5 and K7 fail). The finding
is the point: s=3 is unfixable by case-level bias learned
from the consequence diet, because (a) the train diet
associates s=3's exact (bucket, preff) signature with genuine
outcomes (K9), and (b) the phantom-generating corruption is
independent noise, so no learner-visible feature separates
phantoms from genuine positives in train.

## 6. Verdict rule

BUILD-PASS requires K5 (a case-level variant reaches 12/12
@15). If the run contradicts the predictions, the verdict
follows the frozen bars, not the predictions.

## 7. Feature audit (preregistered, reported not barred)

Per train case the program prints (learner-visible only):
t, bkt, preff, eff, d, L, bumps_bel, wallcount_bel,
itemcount_bel, agree. Per sealed case (learner-visible only):
s, bkt, preff, L, bumps_bel, wallcount_bel, itemcount_bel,
agree. The REPORT will state, for the bucket-1 group, which
features separate the train phantom (t=17) from the train
genuine cases, and what s=3's feature values are -- the
empirical answer to "what distinguishes a phantom from a
genuine positive, and can the learner compute it."

## 8. Scope limits (inherited)

One wall-density law-change axis; item law, belief noise,
energy budget fixed. Bars computed over the sealed batch
(transductive) from predictions + learned biases only; no
world data enters any bar or any learner variant. 12 sealed
cases per regime. Consequence-training diet: 24 true train
outcomes at wp=15, declared here not hidden. Mechanism test,
not a composition-novelty or L3 claim; the composer is fixed.

## 9. Frozen audits

A1: train COMMIT/PREFF call sites precede train CONSEQ
world_execute; sealed VERDICT COMMIT precedes SCORING
world_execute (grep -n phase markers).
A2: zero world_buf/world_off tokens in the LEARNER section.
A3: zero expected/answer/key/target tokens (case-insensitive).
A4: zero correct/reference_plan/gold tokens.
A5: sha256 equality across runs/ivwc_casebias-run{1,2,3}.txt.
A6: world_execute( count = 3 (def + 2 call sites);
WC-FINAL=60 (24 train + 36 sealed).
A7: zero learner_* calls after the sealed COMMIT phase.
A8: zero oracle tokens in the LEARNER section.
No post-prereg probe of any kind; the scorebias committed
per-case sealed run outputs were not read pre-prereg beyond
the published REPORT.md per-case details (task context) and
the train T-lines (learner-visible).
