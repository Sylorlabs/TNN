# PREREG_MEM8.md -- H-MEM8: top-aligned recency weights + inversion reconciliation (preregistration)

Status: FROZEN. Written and committed BEFORE any H-MEM8 implementation
exists in the repo. This document alone governs the H-MEM8 verdict.
No em dashes are used in this file (loop documentation rule).

## 1. The downgrades being addressed

H-MEM7 DOWNGRADED by independent red team (MEM7_ADV_RESULT.md, prereg
a3203c3d0, 23/23 checks, pure Zag). Two downgrade findings narrow
frozen builder claims; the mechanism implements its spec.

(a) X-M7-2 (merit/harm inversion): R6 protects by recency-mass
(decmerit) but replay harm stays count-based (winuses). A protected
age-open slot can have strictly LOWER count-harm than an evictable
age-open slot. Measured: slot7 (decmerit 25, winuses 2, protected)
vs slot0 (decmerit 21, winuses 6, evictable), both age-open;
protection flips the LFU victim slot7 -> slot0 and the measured
count-harm 2 -> 6 (protection-induced harm 4). Under R5
(merit = harm = count) this shape was impossible.

(b) X-M7-3 (decay calibration): the frozen age-window lemma ("any 2
queries since learning protect, weights >= 12 each") is FALSE for
nq < 20. R6 weights are bottom-aligned (weight = position - lo + 1,
oldest in window weighs 1), so for nq < 20 the newest weights are
below 20. Measured: nq=9, 2 fresh queries at positions 7,8 weigh
8+9=17 < 25, evictable. The "every R5 fresh-merit shape preserved by
construction" claim was narrowed to full windows (nq >= 20). The red
team also noted an arithmetic slip in its own report (it wrote
"for nq <= 19, 2nq-1 < 25", but 2nq-1 < 25 iff nq <= 12); the
downgrade stands regardless, and the corrected fresh-pair boundary
under R6 is nq >= 13, not nq >= 20.

## 2. Hypothesis H-MEM8

H-MEM8 has two parts, one mechanism change and one reconciliation.

**Part 1 (mechanism, R7b): top-aligned recency weights.** Change
decmerit() so each query's weight is measured from the PRESENT
(newest query), not from the window start. Weight(i) =
win - (nq-1-i): the newest query always weighs win (20), the
second-newest 19, and so on, regardless of nq. For nq >= win this is
arithmetically identical to R6; for nq < win, recency becomes
history-length-invariant (a query's weight no longer depends on how
long the history is, only on how recent it is).

Consequence, stated before execution: the age-window lemma becomes
UNIFORM. Any 2 queries since learning protect, for ALL nq, with no
regime condition. This is the red team's "recalibrate for short
windows" alternative, implemented via the weighting rather than the
threshold, and it is stronger than re-deriving the claim with an
explicit nq >= 20 condition: the condition is eliminated, not
narrowed.

**Part 2 (reconciliation, no mechanism change): bound and reconcile
the merit/harm split.** Keep winuses() and replay_cost() count-based
(frozen R6 scope decision). Instead of unifying the weighting:
- Prove the inversion bound as a THEOREM (section 5): for age-open
  slots, protection-induced count-harm is at most 4.
- Reconcile the split as principled: merit (decmerit) is
  forward-looking (recency-weighted activity predicts future
  queries; protection shields active procedures); harm (winuses) is
  backward-looking (literal count of past queries that would need
  re-learning). They differ because they measure different things.
  On the forward-looking (mass) scale there is NO inversion:
  protection shields the higher-mass slot. The X-M7-2 "inversion"
  measures a forward-looking decision with a backward-looking
  yardstick.
- Document the rejected full unification (R7a) as negative evidence
  (section 6).

## 3. Mechanism (exact, frozen)

**R7b: the only code change.** In decmerit(), replace the weight
term (i-lo+1) with (win-(nq-1-i)).

Frozen arithmetic fact: for nq >= win, lo = nq-win, and
win-(nq-1-i) = i-nq+win+1 = i-lo+1. The two weightings coincide
exactly. For nq < win, lo = 0; bottom-aligned weighs the newest as
nq, top-aligned weighs it as win.

**Everything else is unchanged:** elig(), winuses(),
replay_cost(), victim(), pressure(), argmin_pol(), all fixtures,
all call sites. MTHRESH()=25, win=20, MERITK retained for lineage.
No threshold change, no harm change.

**Scope:** R7b changes decmerit() output ONLY for nq < 20. Every
fixture in the inherited suite has nq >= 20 (streams: 50..86;
hand-built: 20..26; ramp: 26..34). Therefore the entire inherited
suite output is provably byte-identical under R7b; the regression
bar K-M8-3 checks this by diff.

## 4. Uniform age-window lemma (frozen proof)

Lemma (R7b). For any nq: any 2 queries since learning protect
(decmerit >= MTHRESH = 25). A single query never protects (max
weight win = 20 < 25).

Proof. Age-open means st_seq(ST) < st_prot(s). st_prot(s) is set at
learning to seq_learn + PROB() = seq_learn + 10, so age-open implies
seq - seq_learn <= 9. The slot's queries since learning are therefore
among the last <= 9 queries of Q (positions nq-k..nq-1 for some
k <= 9, or all of Q if nq < 9). Under top-aligned weights the j-th
newest query (j = 1,2,...) weighs win-(j-1) = 21-j, so the last 9
queries weigh 20,19,...,12. If nq < 9, the nq queries are the nq
newest, weighing (21-nq)..20, each >= 12 because nq <= 9 implies
21-nq >= 12. Any 2 of these weigh at least 12+13 = 25 = MTHRESH.
A single query weighs at most 20 < 25. QED.

Corollary. The H-MEM6/H-MEM7 "every R5 fresh-merit shape is
preserved" claim holds UNIFORMLY (no nq >= 20 condition, no
nq >= 13 boundary). The X-M7-3 downgrade is repaired at the
mechanism level, not merely narrowed.

## 5. Inversion bound theorem and reconciliation (frozen)

Theorem (inversion bound). For age-open slots, let A be protected
(decmerit >= 25) and B be evictable (decmerit < 25). Then
winuses(B) - winuses(A) <= 4.

Proof. A protected implies decmerit(A) >= 25. One query weighs at
most win = 20 < 25, so winuses(A) >= 2. B evictable and age-open
implies decmerit(B) < 25. In-window weights are >= 1, so 7 queries
have mass at least 1+2+...+7 = 28 >= 25; hence winuses(B) <= 6.
Therefore winuses(B) - winuses(A) <= 6 - 2 = 4. QED.

Reconciliation (frozen position). Merit and harm answer different
questions. Merit (decmerit, recency-weighted): "is this procedure
currently active enough to deserve protection?" It is
forward-looking: recent queries predict near-future queries, so
fresh activity is the right shield criterion. Harm (winuses,
count-based): "if evicted, how many window queries must be
re-learned?" It is backward-looking: the literal replay count.
A procedure with 2 fresh queries (mass 25, count 2) IS active
(protect it) and IS cheap to re-learn (count 2); there is no
contradiction. The X-M7-2 "inversion" (protected count-harm 2 <
evictable count-harm 6) measures a forward-looking protection
decision with a backward-looking harm yardstick. On the
forward-looking (mass) scale the ordering is NOT inverted:
protection shields mass 25 and exposes mass 21. The downgrade's
narrowing stands (the "strict improvement over the count cliff"
reading is bounded), but the split is principled and the inversion
is bounded by theorem (<= 4), not merely observed (== 4).

## 6. Rejected alternative: R7a (harm = decmerit), negative evidence

Considered: unify the weighting by setting replay_cost() to return
decmerit() (recency-weighted harm), so merit and harm are the same
quantity and the X-M7-2 inversion class closes by construction
(protected age-open implies harm >= 25 > evictable age-open harm).

Tested: in /tmp scratch only (Zag compiler + shell; no Python; not
committed; not part of H-MEM8).

Rejected, for two frozen-bar reasons:
(i) It reorders the menu's argmin globally. On the inherited suite,
C2-ev0 flips from the frozen FIFO winner to LRU at W=20, failing
frozen K-M2-5 (band check expects FIFO). Changing K-M2-5's expected
winner would weaken a frozen bar, which is forbidden.
(ii) It dissolves F-M6-3b's :1 path: under mass-harm the unprotected
menu already avoids the fresh slot (its mass-harm 39 exceeds the
alternatives), so protection no longer flips the winner (1 -> 0).
The fresh-merit discrimination survives (K-M7-1a still :1), but the
flagship counterfactual is gone.

Position: R7a is coherent and closes the inversion, but it is
incompatible with frozen bars. It remains a future hypothesis that
requires newly frozen bars, not a revision of H-MEM8. The bounded
split (R7b + theorem) is the honest H-MEM8 position.

## 7. Frozen kill bars

### K-M8-1a: short-window fresh pair protects (X-M7-3 repair)

Fixture, frozen: store_init(W,ST); learn_stream(W,ST,0,7) (pids 0..6
-> slots 0..6, prot=10, sseq 0..6, seq=0, nq=0); st_learn(W,ST,7)
-> slot7 (sseq=7, prot=10); 7 filler st_query for pids 0,1,2,3,4,5,6;
2 st_query for pid7. End state: seq=9, nq=9, Q[7]=Q[8]=7.

Hand-derived expectation (frozen): nq=9 < 20 so lo=0.
Top-aligned weights: Q[7] weighs 20-(9-1-7)=19, Q[8] weighs
20-(9-1-8)=20. decmerit(slot7) = 39 >= 25. elig: st_seq(9) <
st_prot(10) and 39 >= 25, so elig = 0 (protected). Under R6
(bottom-aligned) this exact state read 8+9=17 (evictable): this bar
is the X-M7-3 instance, repaired.

PASS iff: st_nq(ST)=9, st_seq(ST)=9, decmerit(slot7)=39,
elig(slot7,20,1)=0. Any other outcome is a FAIL of H-MEM8.

### K-M8-1b: short-window single newest query does NOT protect

Fixture, frozen: store_init(W,ST); learn_stream(W,ST,0,7);
st_learn(W,ST,7) -> slot7; 8 filler st_query for pids
0,1,2,3,4,5,6,0; 1 st_query for pid7. End state: seq=9, nq=9,
Q[8]=7 (single newest query for pid7).

Hand-derived expectation (frozen): decmerit(slot7) = weight(8) =
20-(9-1-8) = 20 < 25. elig: 9 < 10, 20 < 25, so elig = 1
(evictable). The "single query is never merit" principle holds
uniformly in short windows.

PASS iff: decmerit(slot7)=20, elig(slot7,20,1)=1. Any other outcome
is a FAIL of H-MEM8.

### K-M8-2: inversion bound (X-M7-2 fixture, reconciled)

Fixture, frozen (Q layout and slots from PREREG_MEM7_ADV.md X-M7-2):
store_init(W,ST); st_set_seq(ST,105); st_set_nq(ST,26);
Q[0..26) = 1,2,3,4,5,6, 0,0,0,0,0,0, 1,2,3,4,5, 7,7,
6,1,2,3,4,5,6;
st_set(W,0,1,0,3,91,0,109); st_set(W,1,1,1,110,92,1,50);
st_set(W,2,1,2,120,93,2,50); st_set(W,3,1,3,130,94,3,50);
st_set(W,4,1,4,140,95,4,50); st_set(W,5,1,5,150,96,5,50);
st_set(W,6,1,6,160,97,6,50); st_set(W,7,1,7,2,101,7,109).

Hand-derived expectation (frozen; nq=26 >= 20 so R7b = R6,
identical to the red-team derivation):
- decmerit(slot7): Q[17],Q[18], weights (17-5)=12,(18-5)=13,
  sum 25. elig: 105 < 109, 25 >= 25 -> 0. Age-open: yes.
- decmerit(slot0): Q[6..11], weights 1,2,3,4,5,6, sum 21. elig:
  105 < 109, 21 < 25 -> 1. Age-open: yes.
- winuses(slot7)=2, winuses(slot0)=6: the count-scale inversion
  (2 < 6) materializes as the red team measured.
- LFU (pol 0) protected: eligible slots 0..6 (slot7 excluded),
  uses 3,110,120,130,140,150,160 -> victim slot0.
- LFU unprotected: all eligible, min uses slot7 (2) -> victim
  slot7.
- replay_cost(slot0)=6, replay_cost(slot7)=2.
- Bound check: 6-2 = 4 <= 4 (theorem).
- Mass-scale check: decmerit(slot7)=25 > decmerit(slot0)=21
  (no inversion on the forward-looking scale).

PASS iff all of: decmerit(slot7)=25, elig(slot7,20,1)=0,
decmerit(slot0)=21, elig(slot0,20,1)=1, winuses(slot7)=2,
winuses(slot0)=6, victim(LFU,protected)=slot0,
victim(LFU,unprotected)=slot7, replay_cost(slot0)=6,
replay_cost(slot7)=2, (6-2)<=4, decmerit(slot7)>decmerit(slot0).
Any other outcome is a FAIL of H-MEM8.

### K-M8-3: regression

Baseline: the frozen MEM7_RAW_OUTPUT.txt
(md5 79fdc6eea90c8ed9c019e6893e693bba).

PASS iff the diff of MEM8_RAW_OUTPUT.txt against that baseline
shows EXACTLY: the MEM7 trailing "ALL BARS PASS" line replaced by
the K-M8-1a section, the K-M8-1b section, the K-M8-2 section, and
"ALL BARS PASS". No other differences.

Rationale (frozen, derived before execution): R7b coincides with R6
for every nq >= 20 (section 3), and every inherited fixture
(streams, flat, fallback, flip family, xm51, m7pair, ramp) has
nq >= 20, so no inherited emit line can change. The only new output
is the appended K-M8 sections.

### K-M8-4: determinism

PASS iff three consecutive runs are byte-identical, exit 0, and
contain zero FAIL lines.

## 8. Explicit non-goals

- R7a (harm unification) is NOT part of H-MEM8 (section 6).
- No threshold change (MTHRESH stays 25).
- No new fixtures beyond K-M8-1a/K-M8-1b/K-M8-2.
- Classification remains bounded L2. No mechanism here establishes
  L3. The menu, the operating window, MTHRESH, and the linear decay
  weights are authored.

## 9. Execution and governance rules

- Pure Zag only: no Python anywhere (editing, generators,
  verifiers, analysis, harnesses, scratch). Disclosure does not cure
  a violation. Pre-freeze scratch work used only the Zag compiler
  and shell diff/cmp/md5sum in /tmp.
- This prereg is committed alone BEFORE any H-MEM8 implementation
  exists in the repo. The prereg commit must be a strict ancestor of
  the implementation commit.
- Verdict names the exact frozen bars above. No bar may be weakened
  or redefined after results.
- Commits are local (tnn-native-lab branch); nothing is pushed
  without Micah's explicit approval. Commit only explicitly owned
  paths; never broad-stage concurrent workers' files. On
  .git/index.lock, wait for the live lock; never remove it.
- Never commit binaries, caches, or unnecessary generated artifacts.
- Negative evidence and lineage are preserved; invalid claims are
  marked RETRACTED, SUPERSEDED, INVALID, or VOID.
- No em dashes in the prereg, the source, or the result doc
  (verified by byte grep).

## 10. Hand-derivation record (pre-freeze)

All expectations in section 7 were hand-derived from the frozen
mechanism in section 3 before any implementation existed in the
repo. The uniform lemma (section 4) and the inversion bound
(section 5) are proven, not observed. Pre-freeze scratch work in
/tmp (Zag compiler + shell only) confirmed: (a) R7b alone yields
byte-identical output to MEM7 on the inherited suite
(md5 79fdc6eea90c8ed9c019e6893e693bba); (b) the K-M8-1a/K-M8-1b
derivations above reproduce in scratch. The committed implementation
will be built from the prereg text, not from scratch artifacts.
