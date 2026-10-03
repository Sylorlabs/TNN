# PREREG: Coverage-Directed vs Failure-Triggered Widening in Behavior-Contract Composition

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Step 0) strictly precedes all implementation.

## 1. Question

C319 established SUBSUMPTION (H1+H2 = behavior-contract composition); C325
independently reproduced it; C329 pinned S2 (empty kind-set reads as universal
{1,2} in all three admission positions; FROZEN, used here, not re-litigated).
The unified operation U widens its kind filter when the contract is too narrow.
Currently widening is FAILURE-TRIGGERED: after every admitted candidate fails,
retry all filter-rejected pairs blindly, once per query (WIDEN=1). The open
question from the C325 reproduction: should widening be COVERAGE-DIRECTED,
driven by analysis of what the filter has and has not covered, before
exhaustive failure? This battery freezes both mechanisms and discriminates them.

## 2. Frozen background (not under test)

- One admission rule (S2-pinned): single A admitted iff kin in u_eff(A.inmask)
  and kout in u_eff(A.outmask); pair (A,B), A!=B, admitted iff kin in
  u_eff(A.inmask), u_eff(A.outmask) INTERSECTS u_eff(B.inmask), kout in
  u_eff(B.outmask). u_eff: empty mask reads as universal {1,2}.
- One execution rule: admitted singles in MAP-id order, then admitted pairs in
  (a,b) id order; end-to-end verification; intermediates logged.
- Success-recording (Amendment 2, shared by both arms): successful trials record
  kind observations into the contract masks.
- Arm F = this frozen U exactly, including failure-triggered blind widening.
- Kinds: 1=NODE (value appears as a fact subject) else 2=NUM. Behaviors
  (WALK/COUNT/MAYBE/IDENT) installed as previously-learned MAPs. One TRIAL = one
  single-MAP or one ordered-pair execution. 3/3 byte-identical runs per arm.

## 3. Coverage-directed design (frozen)

### 3a. Coverage statistic (learner-owned, no researcher oracle)

missbits[m][p]: per MAP m, per position p in {in, out}, the set of kind bits
OBSERVED at runtime during the learner's own trial executions that are NOT
covered by m's contract mask at p. Coverage test uses the S2 reading, so a miss
is recordable only against a nonempty mask. missbits is per-query (cleared at
query start) and populated from FAILED trials only (a successful trial ends the
query and records into the contract masks instead). Observed positions:

- single trial of m, s -> v, v >= 0: in-position kind pkind(s),
  out-position kind pkind(v). (x.in cannot miss: admission guarantees kin is
  covered and pkind(s) = kin in these worlds.)
- pair trial (x,y), s -> v1 -> v2: x.out-position kind pkind(v1) if v1 >= 0;
  y.in-position kind pkind(v1) if v1 >= 0; y.out-position kind pkind(v2) if
  v2 >= 0.

Every input to missbits is something the learner executed and observed itself
via probe_kind. No researcher oracle.

### 3b. Widening decision (frozen)

Arm C REPLACES the blind failure-triggered retry with this rule (no
exhaustive-failure backstop in arm C; this is the strongest test of the
hypothesis):

On a failed trial that adds at least one NEW bit to missbits, immediately admit
every ordered pair (x,y), x != y, that is ALL of: (i) currently
filter-REJECTED, (ii) not yet tried, (iii) kin in u_eff(x.inmask) and kout in
u_eff(y.outmask), (iv) junction-justified by the accumulated ledger:
(missbits[x][out] INTERSECTS u_eff(y.inmask) nonempty) OR
(missbits[y][in] INTERSECTS u_eff(x.outmask) nonempty).

The newly admitted pairs are tried immediately in (x,y) id order, before the
composer resumes the admitted sequence. Log WIDEN=1 once per query, WTRIG=2
(coverage trigger; failure trigger is WTRIG=1), and WADD=x,y per admitted pair.
Pairs already admitted need no widening; pairs justified by no ledger content
are never admitted.

Rationale: the miss is direct learner-observed evidence that the filter's
junction model is wrong at a specific MAP and kind; the widening is selective
to pairs whose junction that evidence covers, instead of blind.

## 4. Discriminating problems (frozen worlds)

Shared teaching rule: teaching executions record kind observations on success
only. MAP ids are installation order.

D0 CANONICAL SANITY (no widening expected; guards against regression).
World = P3 facts/MAPs/teaching from the frozen C319 prereg (X=WALK(81) id0,
Y=COUNT(82) id1, D1=IDENT id2, D2=COUNT(81) id3; teaching n=2 each; sealed
(31,81,32),(32,81,33),(33,81,34),(34,82,35),(35,82,36); query s=31, kin=1, kout=2, exp=2, nm=4).

D1 EARLY SELECTIVE WIDEN (P2b replay; coverage evidence observable early).
World = P2b facts/MAPs/teaching (X=WALK(81) id0 taught 11->14 NUM so
X.outmask={2}; Y=COUNT(82) id1; D1=IDENT id2; D2=COUNT(81) id3; sealed
(41,81,42),(42,81,43),(43,81,44),(44,82,45),(45,82,46); query s=41, kin=1,
kout=2, exp=2, nm=4). Working pair (X,Y) is filter-rejected; X is admitted as a
single, so its misleading output kind is observable on try 1.

D2 SPURIOUS WIDEN (coverage evidence genuine but non-diagnostic).
Facts teach: (11,81,12),(12,81,13),(13,81,14); (70,82,71),(70,82,72);
(60,83,61),(60,83,62),(61,83,63).
MAPs: D=WALK(81) id0 taught 11->14 (14 not a subject: NUM; D.inmask={1},
D.outmask={2}); Q=COUNT(82) id1 taught 70->2 (in{1},out{2}); W=COUNT(83) id2
taught 60->2 (in{1},out{2}).
Facts sealed: (41,81,42),(42,81,43),(43,81,44); (44,83,441); (41,83,411),
(41,83,412). Query s=41, kin=1, kout=2, exp=2, nm=3.
Correct: W alone (W(41)=2). D(41)=44 is NODE, a genuine miss against
D.outmask={2}; it justifies rejected pairs (D,Q) and (D,W), which both fail.

D3 UNOBSERVABLE COVERAGE (the misleading MAP is never admitted, so no miss is
ever observable).
Facts teach: (11,81,12),(12,81,13),(13,81,14); (70,82,71),(70,82,72);
(31,81,32).
MAPs: X=WALK(81) id0 taught 11->14 NUM (in{1},out{2}); Y=IDENT id1 taught
31->31 (in{1},out{1}); Q=COUNT(82) id2 taught 70->2 (in{1},out{2}).
Facts sealed: (41,81,42),(42,81,43),(43,81,44). Query s=41, kin=1, kout=1,
exp=44, nm=3.
Correct: pair (X,Y): X(41)=44, Y(44)=44. X is rejected everywhere (its
outmask={2} contradicts kout=1), so X is never executed and no coverage miss
can be observed.

## 5. Frozen predictions

Format: ANS / TRIES / WIDEN / WTRIG / INTER, where INTER is the successful
pair's intermediate (-1 if the success was a single or there was none),
WTRIG 0=none 1=failure 2=coverage.

| Prob | Arm F (failure-triggered) | Arm C (coverage-directed) |
|------|---------------------------|---------------------------|
| D0 | 2 / 3 / 0 / 0 / 34 | 2 / 3 / 0 / 0 / 34 |
| D1 | 2 / 7 / 1 / 1 / 44 | 2 / 2 / 1 / 2 / 44 |
| D2 | 2 / 3 / 0 / 0 / -1 | 2 / 5 / 1 / 2 / -1 |
| D3 | 44 / 2 / 1 / 1 / 44 | -2 / 1 / 0 / 0 / -1 |

Tried-set / widening predictions:
- D1: F tries {X,Y,D2,(D1,X),(D1,Y),(D1,D2),(X,Y)} (blind: 6 admitted fail,
  WIDEN=1, rejected (X,Y) succeeds at try 7). C tries {X,(X,Y)}: try-1 miss
  (X,out,1) selectively admits WADD=(0,1),(0,3); (X,Y) succeeds at try 2.
- D2: F tries {D,Q,W}, no widening (W succeeds at try 3 before any exhaustion).
  C tries {D,(D,Q),(D,W),Q,W}: try-1 miss (D,out,1) fires SPURIOUS widening
  WADD=(0,1),(0,2); both fail; W succeeds at try 5.
- D3: F tries {Y,(X,Y)}: Y fails, exhaustive admitted failure, WIDEN=1
  (WTRIG=1), blind retry finds (X,Y) at try 2. C tries {Y} only: no miss is
  observable (Y's kinds are covered), no widening exists in arm C, query fails.
- D0: both arms identical, no misses, no widening.

Ledger predictions: C records missbits[0][out]={1} on D1 and D2 (LEDGER m=0
in=0 out=1); all F ledgers are empty (F never records misses); C ledgers on D0
and D3 are empty.

## 6. Frozen kill bars

- K1 D0: F (2,3,0,0,34); C (2,3,0,0,34). 3/3 each.
- K2 D1: F (2,7,1,1,44) with tried-set of 7; C (2,2,1,2,44) with
  WADD=(0,1),(0,3) and tried-set {X,(X,Y)}. 3/3 each.
- K3 D2: F (2,3,0,0,-1); C (2,5,1,2,-1) with WADD=(0,1),(0,2). 3/3 each.
- K4 D3: F (44,2,1,1,44); C (-2,1,0,0,-1). 3/3 each.
- K5 LEDGER: C D1 and C D2 show `LEDGER m=0 in=0 out=1`; every F ledger line
  shows in=0 out=0; C D0/D3 ledgers empty. 3/3.
- K6 DETERMINISM: each arm 3/3 byte-identical whole-output; sha256 recorded.
- K7 NO-MODE AUDIT: each arm binary implements exactly one widening rule,
  always on, with no flag/mode/branch selecting widening policies at runtime.
  The F vs C difference is the experimental manipulation (two separately
  assembled binaries sharing one base file), never a learner-selected mode.
- K8 HYGIENE: zero em/en dash bytes in all docs; safebin guard attested;
  pure Zag for all scientific computation.

## 7. Frozen verdict mapping (faster vs different)

- K1-K5 all PASS exactly as predicted: MIXED. Coverage-directed widening is
  not a pure speedup: it changes WHAT is tried and WHEN. Boundary statement
  (frozen): coverage-directed selective widening wins (D1: 7 tries to 2, same
  answer, narrower tried-set) exactly when the coverage evidence is observable
  inside the admitted trial sequence, i.e. the misleading MAP gets executed;
  it pays a spurious cost when genuine misses are non-diagnostic (D2: WIDEN=1
  where F has none, 3 tries to 5); and it fails where the misleading MAP is
  never admitted (D3: F succeeds via blind retry, C fails -2). The blind
  failure-triggered retry is the exploration backstop for unobservable
  coverage. Recommended follow-up (not claimed): hybrid arm, coverage-selective
  first with failure-triggered blind retry as backstop.
- COVERAGE-DIRECTED WINS requires C to match or beat F on every problem
  (tries <=, same answers, no spurious widening, no new failures): NOT the
  frozen prediction; would require K2-K4 to come out differently than Section 5.
- FAILURE-TRIGGERED SUFFICES requires C's column identical to F's on all four
  problems: NOT the frozen prediction.
- Any K1-K5 failure: UNDECIDED; REPORT diagnoses which prediction broke and
  names the decisive follow-up experiment. VOID is terminal.

## 8. Honest boundaries (pre-declared)

- Behaviors are installed as previously-learned MAPs; behavior induction not
  under test (canonical standing).
- Expected answers verify final acceptance (canonical boundary).
- missbits is per-query; cross-query contract growth happens only via the
  shared Amendment-2 success-recording. The battery tests within-query widening
  policy, not lifetime learning.
- Arm C has no blind backstop by design (strongest test); a hybrid is
  follow-up work, not part of this verdict.
- Four problems discriminate the widening policy; they do not establish
  generality of either policy.

## 9. Implementation plan (frozen order)

1. w_base.zag: output buffer + cursor helpers + single raw-syscall flush;
   arena (base layout plus missbits ledger, tried masks, succ_inter,
   widen flags); fact store; probe_kind; walk/count/ident; MAP table;
   observe/teach; S2-pinned admission (k_has, k_inter); world setups D0-D3;
   report/census/ledger printers.
2. w_fail.zag: arm F composer (admitted singles, admitted pairs, blind
   failure-triggered retry of all rejected pairs once, WTRIG=1) + main.
3. w_cov.zag: arm C composer (miss recording, junction-justified selective
   widening on first new miss, WTRIG=2, WADD lines; NO blind retry) + main.
4. Assemble with cat, compile with the pinned znc, run 3x each, record sha256.
5. REPORT.md with verdict per Section 7 mapping.

Zag pitfalls observed: u8-backed z_alloc; no _zag_print for dynamic content
(single buffer, cursor helpers, one raw syscall; verify stdout bytes);
if-nesting at most 3 (widening scan hoisted into helpers); no !(A && B) in
while conditions; no WAV I/O.
