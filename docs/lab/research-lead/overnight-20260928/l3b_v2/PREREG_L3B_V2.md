# PREREG: L3B constructor v2 (FROZEN)

Status: FROZEN. Committed alone before any implementation file exists.
Verdict labels: L3B-V2-PASS, L3B-V2-PARTIAL, L3B-V2-FAIL.

## 1. What v1 proved and where the adversary drew the boundary

L3B-GROWTH-PASS (c5be6dfb5 to 2fb110ce7): the learner grows base-language
programs via generic constructors; C0-A answered mechanically (semantics
live in the pre-existing interpreter). Clean bounded-L2 grower of single
stationary arithmetic residuals inside the fixed vocabulary envelope.

L3B-C0C-BOUNDARY-EXPOSED (14a92a69d to a40aac558): the C0-C claim broke at
exactly the predicted boundary:
- Family A2 (n-squared residual): analyzer abstained honestly (NO-GROWTH),
  TRACE-CREATE 0, HIDDEN-A2 0/3. Crux: hand-built MUL(VAR,VAR) evaluates
  to 25 at f0=5, so the execution substrate is open while the
  construction substrate (rel_of plus build_expr) is closed.
- Family B2 (alternating law): revision churn v1 to v2 to v3 with v3
  content-identical to v1 but rebuilt from scratch; no version memory;
  FINAL-B2 0/2. The static single-program form cannot represent
  per-regime structure.

## 2. Redesign (constructor level, not a vocabulary patch)

Two changes, both in the constructor machinery. No new semantic case is
added to the interpreter (the INTERP-BEGIN/END region is copied
byte-identical from v1). The fixed-vocabulary analyzer rel_of is DELETED,
not extended. Adding MUL(VAR,VAR) or any per-family case to an analyzer
would repeat the downgraded template-widening pattern and is prohibited
by this prereg.

### 2a. Program-space search replaces vocabulary fitting

A generic enumerative search over small programs in the base language B.

Grammar (fixed, generic, family-blind):
- Atoms: VAR (feature F0), CONST k for k in 0..8.
- Binary ops: ADD, MUL, SUB (op codes 3, 4, 5, the existing B ops).

Generation (canonical order, deterministic, no family branches):
- Depth 0: VAR, C0..C8 (10 programs).
- Depth 1: for op in (ADD, MUL, SUB), for atoms a, b: skip if a and b are
  both const; for ADD/MUL skip if b < a (canonical: smaller child first).
  Yields 10 plus 10 plus 19 = 39 programs.
- Depth 2: for op in (ADD, MUL, SUB), for each depth-1 program d:
  ADD/MUL emit only (VAR, d) (canonical atom-first); SUB emits (VAR, d)
  and (d, VAR). Yields 39 plus 39 plus 78 = 156 programs.
- Total: 205 programs. The implementation asserts this count at startup.

Every program is a node DAG in the shared store and is evaluated by the
UNCHANGED binterp_eval. The n-squared program MUL(VAR,VAR) is in the
space because it is a small program produced by the generic rule
(op = MUL, children = (VAR, VAR)), under the same rule that produces the
other 204 programs. There is no squaring operator, no n-squared-shaped
proposal rule, and no per-family branch anywhere in the search.

Selection (on a growth trigger): for each residual (r1: n to tl1,
r2: n to tl2), score every program by exact matches on the 3-observation
failure window, in canonical order; best = first program with maximal
score. Growth fires only if best1 is exact (3/3) AND best2 is exact (3/3)
AND the symbol channel is intact on the window (ts1 == h0 and ts2 == h1
on all 3 observations; the learnable residual is in the lengths, as in
v1). The current predictor just failed 3 consecutive times on this
window, so an exact pair strictly improves on it.

On fire, the winning programs are ASSEMBLED by the generic constructors:
their structural keys are parsed and CREATE/CONNECT calls build the
nodes, all logged. The CALL log is the evidence that the form was
constructed, not retrieved.

### 2b. Version archive plus per-regime dispatch replaces static form

The grown structure is no longer one static (r1, r2) pair. It is a
version archive plus an active pointer.

- Archive: up to 8 versions. Each version = (p1 root, p2 root, p1 key,
  p2 key). Every constructed version is appended at construction;
  insertion dedupes by key pair.
- Active pointer: exactly one version predicts at a time.
- Single-failure dispatch: on a failed episode with an active version,
  BEFORE the failure is buffered, each archived version other than the
  active one is tested against the current observation (n, tl1, tl2):
  if p1(n) == tl1 and p2(n) == tl2 (and ts1 == h0, ts2 == h1), the
  version becomes active immediately with TRACE-DISPATCH. Zero
  construction calls occur. The failure is explained, so it is not
  buffered toward a construction trigger. The episode still counts as a
  wrong prediction (honest tally). Dispatch is allowed in every phase:
  recognizing a previously learned regime is memory retrieval, not new
  construction.
- Construction trigger (unchanged policy): 3 consecutive unexplained
  failures with allow_create == 1. The search runs; on an exact pair the
  new version is constructed, archived, and activated with TRACE-CREATE
  and the CALLS log; otherwise TRACE-NO-GROWTH.
- Recall evidence: TRACE-DISPATCH logs the dispatched-to version's root
  node ids; the harness asserts they equal the ids logged at that
  version's TRACE-CREATE (same nodes reused, nothing rebuilt) and that
  the constructor call log is empty across the dispatch.

## 3. Frozen falsifiers

Families A2 and B2 are taken VERBATIM from the adversary's FAMILIES.md
(commit a40aac558), which was itself frozen after prereg 14a92a69d:

Family A2: law content a^n b^(n^2), head "ab" (97,98).
LEARN-A2 n = [2,3,5,7,4,6], (tl1,tl2) = (n,n^2).
HIDDEN-A2 n = [1,4,8], (tl1,tl2) = [(1,1),(4,16),(8,64)].
KX-A2: E_m for m = 1..12 with l1 = m, l2 = m^2.
N2-INTERP: hand-built MUL(VAR(F0),VAR(F0)) with CREATE/CONNECT,
eval at f0 = 5. Expected 25.

Family B2: R1: a^n b^(2n). R2: a^n b^(n+4). Head "ab" (97,98).
LEARN-B2 n = [2,3,5,7,4,6], law R1.
HIDDEN-B2 n = [1,4,8], law R1.
SWITCH1 (CONTRADICTION) n = [3,6,5], law R2.
SWITCH2 (CONTRADICTION) n = [2,3,5], law R1 (n = 4 excluded per the
adversary's frozen spec: there v2's n+4 law is accidentally correct).
FINAL-B2 (FOLLOWUP) n = [5,7], law R2.

Plus v1 regression families (behavioral bars only; the grown programs
may differ representationally from v1's (rel,k) pairs, e.g. ADD(VAR,VAR)
instead of MUL(VAR,CONST(2)) for 2n, which is an expected honest
consequence of generic search):
- inst1 (family A): LEARN (tl1 = n, tl2 = 2n), HIDDEN, CONTRADICTION
  (tl2 = n+4), FOLLOWUP (tl2 = n+4).
- inst2 (family B): LEARN (tl1 = n+2, tl2 = n), HIDDEN.
- Ablations: growth disabled.

## 4. Frozen predictions

### A2 group
- P-A2a: KX-A2 max = 1 (base language L unchanged; same as adversary).
- P-A2b: at least one TRACE-CREATE whose p2 key is exactly "(M,V,V)",
  with the CALLS log showing the CREATE/CONNECT assembly of
  MUL(VAR,VAR). The n-squared form is assembled by the search.
- P-A2c: HIDDEN-A2 = 3/3.
- P-A2d: N2-INTERP = 25 (interpreter unchanged).
- P-A2e: anti-widening audit PASS: INTERP-BEGIN/END region
  byte-identical to v1 (shell sha256 compare of the extracted regions);
  no vocabulary/analyzer function in the source; no family-specific
  branch or literal anywhere in the .zag.

### B2 group
- P-B2a: TRACE-CREATE count = 2, TRACE-DISPATCH count = 2.
- P-B2b: archive keys exactly v1 = ("V", "(A,V,V)"),
  v2 = ("V", "(A,V,C4)").
- P-B2c: HIDDEN-B2 = 3/3, SWITCH = 3/6 (SWITCH1 0/3, SWITCH2 2/3),
  FINAL-B2 = 1/2.
- P-B2d: both dispatches are recalls: dispatched-to root ids equal the
  ids logged at the version's TRACE-CREATE, and zero constructor calls
  occur across each dispatch.

### Honest deviation note (P-B2c FINAL-B2)
The task brief suggested FINAL-B2 = 2/2. Analysis shows 2/2 requires an
oracle: the regime flips from R1 (SWITCH2) to R2 (FINAL-B2) with no
observable pre-prediction cue, so the first post-flip episode is
unpredictable without task labels (prohibited). The frozen bar is the
honest ceiling 1/2: fail on the flip, dispatch on the observed
contradiction, correct thereafter. v1 scored 0/2 here with no recall at
all, so 1/2 plus demonstrated recall is progress, not a weakened bar:
the bar was never frozen for v2 before this prereg.

### Regression group
- P-R1: inst1 hiddenA = 3/3, follow = 2/2.
- P-R2: inst2 hiddenB = 3/3.
- P-R3: ablation total = 0/6.

### Harness bars
- K1: this prereg strictly precedes implementation
  (git merge-base --is-ancestor verified at commit time).
- K2: all P-A2a..e, P-B2a..d, P-R1..R3 hold against the frozen
  predictions above, 3/3 byte-identical runs.
- K3: pure Zag, zero Python at every step; shell-only dash check clean
  on all lane files; u8-backed cells only.

## 5. Verdict rules

- L3B-V2-PASS: every prediction in sections 4 (A2, B2, regression) and
  every harness bar holds.
- L3B-V2-PARTIAL: exactly one of {A2 group, B2 group} fully holds, the
  other does not, and the regression group fully holds.
- L3B-V2-FAIL: any other outcome, including any regression failure.

## 6. Scope

Bounded L2 at most. No L3 claim is made or implied. If v2 passes, the
mechanism is a bounded-L2 grower of small programs with per-regime
recall; C0-C beyond the frozen families remains untested.
