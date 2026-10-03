# PREREG: S1 vs S2 empty-mask semantics (frozen)

Date: 2026-10-02. Status: FROZEN. Committed before any implementation or
execution in this lane. This prereg changes no prior frozen bar; it pins the
underspecification recorded as item 3 in the reproduction REPORT.md
("Empty-mask pair semantics (S1 vs S2)") and in PREREG_AMEND3.md.

## 1. Background and the underspecified point

The unified behavior-contract operation U (compose-collapse PREREG Section 3)
admits candidates with one rule:

- Single A admitted iff kin compatible with A.inmask and kout with A.outmask.
- Pair (A,B), A!=B, admitted iff kin compatible with A.inmask, A.outmask
  INTERSECTS B.inmask (nonempty), and kout compatible with B.outmask.
- Compatibility: an EMPTY kind-set (no observations) is compatible with every
  kind; otherwise the kind bit must be present.

The middle pair condition is stated as raw set intersection ("INTERSECTS ...
(nonempty)"), while the outer positions invoke "compatible", which the
Compatibility sentence defines for empty sets. The reproduction pinned S2 in
AMEND3 on textual grounds; S1 was recorded as the competing hypothesis. This
prereg freezes both readings and four problems on which they disagree.

## 2. Frozen definitions

Kinds: 1=NODE (value appears as a fact subject), 2=NUM (otherwise). Masks are
bitsets over {1,2}: bit0=NODE, bit1=NUM; mask value 3 = {1,2}.

- S1 (pure bitmask intersection, empty rejects): all three admission positions
  use RAW masks. Single A admitted iff (A.inmask has the kin bit) and
  (A.outmask has the kout bit). Pair (A,B) admitted iff (A.inmask has the kin
  bit), (A.outmask & B.inmask) != 0, and (B.outmask has the kout bit). An
  empty mask has no bits, so an empty mask in ANY of the three positions
  rejects.
- S2 (empty reads as universal): in all three admission positions, an empty
  kind-set is first replaced by the universal set {1,2} (mask 3); the same
  three checks then run on the effective masks. An empty mask therefore never
  rejects in any position.

Everything else (execution rule, trial order, widening, success recording) is
identical between the two readings and follows the frozen U specification:
admitted singles in MAP-id order, then admitted pairs in (a,b) id order, each
trial executed and verified end-to-end; if every admitted candidate fails, the
filter-rejected ordered pairs are retried once in (a,b) id order with WIDEN=1
logged.

## 3. Prior (stated before the run)

Textual grounding favors S2. The Compatibility sentence is unconditional: "an
EMPTY kind-set (no observations) is compatible with every kind". It is the
governing definition of "compatible", which the outer admission positions
invoke directly, and nothing in the prereg restricts its scope to the outer
positions. AMEND3's rationale is adopted: a kind filter that treated absence
of evidence as evidence of absence would contradict the Compatibility
sentence; the filter restricts on observed evidence, not on missing
observations. The "INTERSECTS (nonempty)" wording for the middle condition is
the source of the ambiguity, but intersection must be evaluated on the
effective sets once the Compatibility sentence redefines what empty means in
this calculus.

Empirical prior: the sealed K9 observation (reproduction REPORT.md) already
discriminates. K9 froze UNI on P6 as ANS=2 TRIES=3 INTER=44 with no widening,
and it passed. Under S1, hand derivation gives UNI P6 = ANS=2 TRIES=4
INTER=44 WIDEN=1: the untaught Y is rejected as a single on its empty masks,
the pair (X,Y) is rejected on the raw empty middle, and (X,Y) succeeds only in
the widening retry. The observed (2,3) no-widen profile is inconsistent with
S1. Prior: S2 strongly favored. This battery is a preregistered decisive
replication across four fresh problems; the verdict follows the frozen kill
bars below, not the prior.

## 4. Discriminating problems (frozen worlds)

Shared mechanics: facts are (subject, rel, object) triples; kinds derived per
value (NODE iff the value appears as any fact subject). Behaviors: WALK(rel)
chains (s,rel,o) facts; COUNT(rel) counts (s,rel,*) facts, failing (-2) on
zero; IDENT returns its input. Teaching records kind observations only from
successful teaching executions; untaught MAPs have n=0 and masks (0,0).
Candidate trials: one single-MAP execution or one ordered-pair pipeline;
success iff the end-to-end result equals the expected value. Each problem
below is run once per arm binary (the binary emits all four problems);
predictions are hand-derived here before any execution.

Notation: MAP ids 0..3; masks shown as (inmask,outmask) with 1={NODE},
2={NUM}, 3={1,2}, 0=empty.

### Q1: EMPTY-SINGLE (empty masks in single-admission positions)

Facts (teach): (31,81,32),(32,81,33),(33,81,34),(34,82,301).
Facts (query): (41,81,42),(42,81,43).
MAPs: M0=WALK(81), taught 31->34: masks (1,1). M1=IDENT, UNTAUGHT: masks
(0,0). M2=COUNT(82), taught 34->1: masks (1,2).
nmaps=3. Query: s=41, kin=1, kout=1, exp=41.
Behavior notes: M0(41)=43 (walk 41->42->43, stops). M1(41)=41. M2(41)=1
(count of (41,81,*)).

Hand derivation, S2 arm:
- Singles in id order: M0 admitted (1 has kin bit; 1 has kout bit); M0(41)=43
  fails, try 1. M1 admitted by empty-set fallback; M1(41)=41 succeeds, try 2.
- Result: ANS=41 TRIES=2, no INTER, no WIDEN.

Hand derivation, S1 arm:
- Singles: M0 admitted, fails (try 1). M1 rejected (empty inmask has no kin
  bit). M2 rejected (outmask 2 lacks kout bit 1).
- Pairs (kin=1,kout=1): (0,1): middle 1&0=0 reject. (0,2): middle 1&1=1 but
  kout 1 not in outmask 2 reject. (1,0): kin bit absent from empty inmask
  reject. (1,2): kin reject. (2,0): middle 2&1=0 reject. (2,1): middle 2&0=0
  reject. Zero admitted pairs.
- Widening over all 6 rejected pairs in (a,b) order: (0,1): 43, M1(43)=43
  fail. (0,2): 43, M2(43)=0 facts -> -2 fail. (1,0): M1(41)=41, M0(41)=43
  fail. (1,2): 41, M2(41)=1 fail. (2,0): M2(41)=1, M0(1)=-2 fail. (2,1): 1,
  M1(1)=1 fail.
- Result: ANS=-2 TRIES=7 WIDEN=1.

### Q2: EMPTY-MIDDLE (empty B.inmask in the pair middle condition)

Facts (teach): (31,81,32),(32,81,33),(33,81,34),(34,82,301),(34,82,302),
(11,81,12).
Facts (query): (41,81,42),(42,81,43),(43,81,44),(44,82,45),(44,82,46).
MAPs: M0=WALK(81), taught 31->34: (1,1). M1=COUNT(82), UNTAUGHT: (0,0).
M2=IDENT, taught 11->11: (1,1). M3=COUNT(81), taught 31->1: (1,2).
nmaps=4. Query: s=41, kin=1, kout=2, exp=2.
Behavior notes: M0(41)=44. M1(41)=-2 (no (41,82,*) facts); M1(44)=2.
M3(41)=1.

Hand derivation, S2 arm:
- Singles: M0 rejected (outmask 1 lacks kout bit 2). M1 admitted by fallback;
  M1(41)=-2 fails, try 1. M2 rejected (outmask 1 lacks 2). M3 admitted;
  M3(41)=1 fails, try 2.
- Pairs: (0,1) first in (a,b) order: kin ok; effective middle {1} & {1,2} =
  {1} nonempty; kout 2 in effective outmask {1,2}. Admitted. M0(41)=44,
  M1(44)=2 succeeds, try 3.
- Result: ANS=2 TRIES=3 INTER=44, no WIDEN.

Hand derivation, S1 arm:
- Singles: M0 rejected, M1 rejected (empty), M2 rejected, M3 admitted;
  M3(41)=1 fails, try 1.
- Pairs admitted: (0,3): middle 1&1=1, kout 2 in 2; exec M0(41)=44,
  M3(44)=0 facts -> -2 fails, try 2. (2,3): middle 1&1=1, kout ok; exec
  M2(41)=41, M3(41)=1 fails, try 3. All other pairs rejected (any empty
  position rejects; (0,2)/(2,0)/(3,2) fail middle or kout on raw masks).
- Widening over the 10 rejected pairs in order; first is (0,1): M0(41)=44,
  M1(44)=2 succeeds, try 4.
- Result: ANS=2 TRIES=4 INTER=44 WIDEN=1.

### Q3: EMPTY-OUTER-IN (empty A.inmask in the pair outer position)

Facts: same as Q2.
MAPs: M0=WALK(81), UNTAUGHT: (0,0). M1=COUNT(82), taught 34->2: (1,2).
M2=IDENT, taught 11->11: (1,1). M3=COUNT(81), taught 31->1: (1,2).
nmaps=4. Query: s=41, kin=1, kout=2, exp=2.
Behavior notes: M0(41)=44. M1(41)=-2; M1(44)=2. M2(41)=41. M3(41)=1.

Hand derivation, S2 arm:
- Singles: M0 admitted by fallback; M0(41)=44 fails, try 1. M1 admitted;
  M1(41)=-2 fails, try 2. M2 rejected (outmask 1 lacks 2). M3 admitted;
  M3(41)=1 fails, try 3.
- Pairs: (0,1) first: kin in effective inmask {1,2}; middle {1,2} & {1} = {1};
  kout 2 in outmask 2. Admitted. M0(41)=44, M1(44)=2 succeeds, try 4.
- Result: ANS=2 TRIES=4 INTER=44, no WIDEN.

Hand derivation, S1 arm:
- Singles: M0 rejected (empty inmask). M1 admitted, fails (try 1). M2
  rejected. M3 admitted, fails (try 2).
- Pairs admitted: (2,1): middle 1&1=1, kout ok; exec M2(41)=41, M1(41)=-2
  fails, try 3. (2,3): middle 1&1=1, kout ok; exec 41, M3(41)=1 fails, try 4.
  Every pair touching M0 is rejected on its empty masks; (1,0),(1,2),(1,3),
  (3,1),(3,2),(2,0),(0,*) fail on raw middle/kin/kout.
- Widening over the 10 rejected pairs in order; first is (0,1): M0(41)=44,
  M1(44)=2 succeeds, try 5.
- Result: ANS=2 TRIES=5 INTER=44 WIDEN=1.

### Q4: BOTH-EMPTY-MIDDLE (empty masks on both sides of the middle)

Facts: same as Q2.
MAPs: M0=WALK(81), UNTAUGHT: (0,0). M1=COUNT(82), UNTAUGHT: (0,0).
M2=IDENT, taught 11->11: (1,1). M3=COUNT(81), taught 31->1: (1,2).
nmaps=4. Query: s=41, kin=1, kout=2, exp=2.
Behavior notes: M0(41)=44. M1(41)=-2; M1(44)=2. M3(41)=1.

Hand derivation, S2 arm:
- Singles: M0 admitted by fallback, fails (try 1). M1 admitted by fallback,
  fails (try 2). M2 rejected. M3 admitted, fails (try 3).
- Pairs: (0,1) first: effective middle {1,2} & {1,2} = {1,2} nonempty; outer
  positions pass on effective masks. Admitted. M0(41)=44, M1(44)=2 succeeds,
  try 4.
- Result: ANS=2 TRIES=4 INTER=44, no WIDEN.

Hand derivation, S1 arm:
- Singles: M0 rejected, M1 rejected, M2 rejected (outmask 1 lacks 2), M3
  admitted; M3(41)=1 fails, try 1.
- Pairs admitted: (2,3) only (middle 1&1=1, kout 2 in 2); exec M2(41)=41,
  M3(41)=1 fails, try 2. Every pair touching M0 or M1 is rejected on an empty
  position; (3,2) fails the raw middle (2&1=0).
- Widening over the 11 rejected pairs in order; first is (0,1): M0(41)=44,
  M1(44)=2 succeeds, try 3.
- Result: ANS=2 TRIES=3 INTER=44 WIDEN=1.

### Prediction summary (frozen)

| Problem | Position tested | S2 prediction | S1 prediction |
|---|---|---|---|
| Q1 | single, empty in/outmask | ANS=41 TRIES=2 (no WIDEN) | ANS=-2 TRIES=7 WIDEN=1 |
| Q2 | pair middle, empty B.inmask | ANS=2 TRIES=3 INTER=44 (no WIDEN) | ANS=2 TRIES=4 INTER=44 WIDEN=1 |
| Q3 | pair outer, empty A.inmask | ANS=2 TRIES=4 INTER=44 (no WIDEN) | ANS=2 TRIES=5 INTER=44 WIDEN=1 |
| Q4 | pair middle, both masks empty | ANS=2 TRIES=4 INTER=44 (no WIDEN) | ANS=2 TRIES=3 INTER=44 WIDEN=1 |

Every problem separates the readings: Q1 on ANS, Q2-Q4 on (TRIES, WIDEN).

## 5. Implementation plan (frozen)

Two arm binaries from one source: `em_arm.zag` implements the U admission
rule with S2 semantics via `u_eff` (empty mask -> 3). `em_arm_s1.zag` is
generated from `em_arm.zag` by a one-line sed replacing the S2 effectiveness
line with the raw-mask S1 reading; the diff is verified to be exactly that
line. Shared base `em_base.zag` holds facts, kinds, behaviors, observations,
teaching, output helpers, and the four world setups. Assembled sources
`em_full_s2.zag` / `em_full_s1.zag` are compiled with the pinned znc. Each
binary runs Q1-Q4 and emits one line per problem:
`ARM PROB ANS=<n> TRIES=<n> [INTER=<n>] [WIDEN=1]`.

## 6. Frozen kill bars

- K1 Q1: S2 arm emits `s2 Q1 ANS=41 TRIES=2` with no WIDEN; S1 arm emits
  `s1 Q1 ANS=-2 TRIES=7 WIDEN=1`.
- K2 Q2: S2 arm emits `s2 Q2 ANS=2 TRIES=3 INTER=44` with no WIDEN; S1 arm
  emits `s1 Q2 ANS=2 TRIES=4 INTER=44 WIDEN=1`.
- K3 Q3: S2 arm emits `s2 Q3 ANS=2 TRIES=4 INTER=44` with no WIDEN; S1 arm
  emits `s1 Q3 ANS=2 TRIES=5 INTER=44 WIDEN=1`.
- K4 Q4: S2 arm emits `s2 Q4 ANS=2 TRIES=4 INTER=44` with no WIDEN; S1 arm
  emits `s1 Q4 ANS=2 TRIES=3 INTER=44 WIDEN=1`.
- K5 DETERMINISM: 3/3 runs byte-identical per arm (sha256 digests recorded).
- K6 HYGIENE: pure Zag for all scientific computation; safebin guard attested
  in NAMECHECK.md Step 0; zero em/en dash bytes in lane docs (byte-verified).
- K7 SINGLE-VARIABLE AUDIT: `em_arm_s1.zag` differs from `em_arm.zag` by
  exactly the effectiveness line (diff-verified); the arm source contains one
  admission rule and no flag, mode, or branch selecting between readings
  beyond that line.

## 7. Verdict mapping (frozen)

- All four problems match the S2 column and mismatch the S1 column:
  S2 CONFIRMED as the correct pinning of the prereg underspecification.
- All four problems match the S1 column and mismatch the S2 column:
  S1 CONFIRMED (overturns the AMEND3 pinning and the K9-consistent reading).
- Any other pattern (mixed columns, or a problem matching neither column):
  UNDECIDED. The decisive follow-up is then a fresh Q1-style empty-single
  problem with a different behavior and query on which the observed arm
  profile is compared against corrected hand derivations after a source audit
  of the admission implementation; the audit must first rule out an
  implementation bug before any semantic conclusion is drawn.
- Build failure or nondeterminism: UNDECIDED with the defect named.

Kill bars are never weakened. VOID is terminal.
