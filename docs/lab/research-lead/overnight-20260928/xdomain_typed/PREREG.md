# PREREG: xdomain_typed -- Cross-Domain Composition via Learned Typed I/O Contracts

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.

## Hypothesis H1
Cross-domain composition (chain navigation + count aggregation) becomes
possible when each learned structure carries a TYPE SIGNATURE learned from
its observed behavior (not researcher-assigned), and the composer admits a
pair (A,B) only when sig(A).out == sig(B).in with endpoints matching the
goal kinds. This replaces the "navigation concatenation" admission
(plen/relse q) that caused all three mechanisms A/B/C to fail cross-domain.

## World (fixed before implementation)
Facts: (31,81,32) (32,81,33) (33,81,34) -- chain 1, r=81.
       (41,81,42) (42,81,43) -- chain 2, r=81.
       (34,82,101) (34,82,102) -- count targets of node 34 (count=2).
       (43,82,103) (43,82,104) (43,82,105) -- count targets of node 43 (count=3).
Kinds: KIND 1=NODE iff value appears as a fact subject (probe_kind),
       else 2=NUM. Node ids and counts are disjoint by construction.

## Learned structures (behaviors installed as previously-learned;
## behavior induction was demonstrated in prior waves; under test here
## is signature learning + type-directed composition, not behavior induction)
- X id 0: chain-follow (walk r=81 to endpoint). Expected learned sig NODE->NODE.
- Y id 1: count r=82 outgoing. Expected learned sig NODE->NUM.
- D1 id 2: identity distractor. Expected learned sig NODE->NODE.
- D2 id 3: count r=81 outgoing distractor. Expected learned sig NODE->NUM.
Signature learning: record probe_kind(input)/probe_kind(output) per
successful teaching query; finalize when n>=2 by majority (avg>=1.5 -> NUM).
Source must contain ZERO per-MAP signature literals (K4 audit).

## Sealed goal Z
Query (31,93)->2. No paired X+Y examples. No hint. No label.
Composer: singles with sig.in==kin && sig.out==kout, then pairs (A,B) with
sig(A).in==kin, sig(A).out==sig(B).in, sig(B).out==kout. Execute, verify.
On success promote composite Z (behavior=composite, contract=in(A)->out(B))
with provenance to A,B. Expected: Z = X then Y, 3 verifies
(Y try, D2 try, (X,Y) success).

## Arms (fresh workspace each, one binary)
- TREAT: teach all, solve Z typed, then Z2=(41,93)->3 via Z directly.
- NOTYPE: teach all, solve Z with type filter disabled (all pairs admitted).
- ABL-X: teach all, delete X, solve Z typed.
- ABL-Y: teach all, delete Y, solve Z typed.
- FRESH: no teaching, solve Z typed.

## Frozen kill bars
- K1 SOLVE: TREAT solves Z via composite with comp_a=0, comp_b=1.
  ARM-RESULT PASS. 3/3 byte-identical runs.
- K2 CAUSAL: ABL-X, ABL-Y, FRESH all fail Z (expected-fail PASS). 3/3.
- K3 CONTRACT-CAUSAL: NOTYPE solves Z with STRICTLY MORE verifies than
  TREAT (predicted 6 vs 3). 3/3. Proves the contract prunes the search.
- K4 LEARNED-NOT-ASSIGNED: audit passes. grep shows no per-MAP signature
  literal assignment; every sig_in/sig_out value derives from probe_kind
  observations or contract composition in promote_comp (generic machinery).
- K5 DETERMINISM: 3 full runs byte-identical (sha256 recorded).
- K6 NO-TEMPLATE: audit passes. No CHAIN_COUNT literal; Z assembled at
  runtime from learned MAP ids with provenance links.
- K7 REUSE: Z2=(41,93)->3 solved by direct Z application, tries <= 4. 3/3.

## Predicted numbers (recorded before implementation)
TREAT Z tries=3. NOTYPE Z tries=6. Z2 tries=3. Signatures: X 1->1, Y 1->2,
D1 1->1, D2 1->2.
