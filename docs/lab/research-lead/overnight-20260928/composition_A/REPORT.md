# REPORT: Composition Hypothesis A -- Goal-conditioned graph composition from MAP contracts

Verdict: **COMPOSITION-A-COMPLETE** (positive composition evidence with reuse and ablation).

Date: 2026-10-01. Worker: Composition Hypothesis A (subagent 78cc4cdb).
Determinism: 3/3 byte-identical runs (sha256 7081af84...).

## Background

The knowledge-composition study (C1-C3) returned a negative: TNN-2
knows X and knows Y but cannot construct Z; it rebuilds from raw facts
or fails outright. Approach A tests whether composition can be
recovered structurally: each MAP carries a CONTRACT derived from its
own structure (its chain plen via rb_chain_plen, never
researcher-labeled). A new general pipeline stage, compose_try, sits
between rebind and trial in ev_query. On a query where exact-shape
reuse fails, it searches MAP pairs (m1, m2) such that m1's contract
applies to a real gathered path from the query subject, m2's contract
applies to a real gathered path from m1's output value, and the chained
execution verifies against the goal. On success it concatenates the two
rebound chains (SEQ link), sanity-executes the composite, promotes it
as a new MAP, and writes persistent type-1 DEP edges from the
composite to the helper MAPs.

There is no COMPOSE_MODE, no task label, no paired X/Y examples, and
no "combine" hint. Pairing is discovered from contract applicability
to actual data and arbitrated by execution verification. The search is
deterministic (id order, first verifying pair wins).

## Experiment design

Two suites, four arms each, separate workspaces, 30-fact interference
gap between training and test.

Suite A (beyond trial): X is a plen-3 chain (rel 1, query rel 71),
Y is a plen-4 chain (rel 2, query rel 72). Z-alpha needs the plen-6
chain 301->302->303->304->305->306 (query rel 70). Trial's gather
depth is 5, so blind trial CANNOT build plen 6: composition is the
only possible path. This isolates necessity.

Suite B (reusable composite): X' is a plen-2 chain (rel 3, query
rel 73), Y' is a plen-4 chain (rel 4, query rel 74). Z-beta needs the
plen-5 chain 311->312->313->314->315 (query rel 75), then Z-beta-prime
probes reuse on fresh subject 321. This isolates first-class
persistence: the composite must rebind directly like any learned MAP.

Arms per suite: TREAT (train X and Y), ABL-X (train Y only), ABL-Y
(train X only), FRESH (train nothing).

## Results

### Suite A (necessity, beyond trial)

- A-TREAT: compose tried 3 pairs, rejected 2, verified X1+Y1.
  ZA ans=306. New Z MAP id=247, plen=6, with 5 fact DEPs and 2 MAP
  DEPs: DEP->MAP 13 (plen 3, the X MAP) and DEP->MAP 89 (plen 4,
  the Y MAP). The composite structurally references both helpers.
- A-ABL-X (Y only): ZA ans=-2. No Z MAP. Mechanism: m1=Y1 yields
  intermediate 304, but no len-4 path exists from 304 (only
  304->305->306 remains), so the second stage finds nothing.
- A-ABL-Y (X only): ZA ans=-2. No Z MAP. Mechanism: m1=X1 yields
  303, m2 finds 305 which verifies against 306 and is rejected.
- A-FRESH: ZA ans=-2. Trial cannot reach plen 6.

Both ablations break Z. Fresh rediscovery is impossible, not merely
expensive: composition enables the otherwise-impossible.

### Suite B (persistence and reuse)

- B-TREAT: compose tried 3 pairs, rejected 2, verified X'1+Y'1.
  ZB ans=315. New Z MAP id=219, plen=5, DEP->MAP 15 (plen 2, X')
  and DEP->MAP 90 (plen 4, Y'). Z-beta-prime on fresh subject 321:
  ans=325 via direct rebind of the Z-beta MAP (rebind tried 5,
  rejected 4; the composite was the 5th candidate and hit). The
  composite is a first-class reusable structure.
- B-ABL-X and B-ABL-Y: ZB ans=315 via TRIAL (3 tried, 2 rejected),
  producing plen-5 MAPs with zero MAP DEPs. Honest reading: within
  trial's reach, composition is an optimization, not a necessity;
  the ablations correctly fall back to blind construction. Necessity
  is established by Suite A, not Suite B.
- B-FRESH: ZB ans=315 via trial, dep_maps=0.

### Cost

Suite A: compose verifies after 3 pair tries; fresh trial fails
entirely (infinite cost ratio in the strict sense). Suite B: compose
(3 pairs) vs trial (3 tries) are comparable; composition reuses
learned structure at no extra verification cost. No claim is made
that composition is always cheaper; the claim is that it enables
construction beyond the blind builder's reach and that the product
persists as reusable learner state.

## White-box evidence

- The Z MAPs are genuine executable graphs: the composite chain is
  sanity-executed before promotion (vc==v2 required), and Z-beta's
  MAP later executes successfully through the standard rebind path
  on a fresh subject.
- DEP->MAP edges (type 1) point to the actual helper MAPs by id,
  confirmed tag-20 with the expected plens (3 and 4 for Z-alpha,
  2 and 4 for Z-beta).
- Ablation destroys the capability at the mechanism level (no
  len-matching second-stage path, or verification rejection), not
  by researcher deletion.

## Limits and non-claims

- Suite B ablations do NOT break Z (trial fallback). Necessity holds
  only beyond trial's reach (Suite A).
- "Cheaper than fresh" holds as enablement in Suite A; in Suite B
  costs are comparable. No general cost-superiority claim.
- Contracts are currently plen-only and only chain MAPs participate.
  Richer contracts (value patterns, guard structure) are future work.
- One pipeline stage was added (compose_try, ~200 lines unfrozen).
  It is general (fires on any query where contracted MAPs chain),
  not a Z-alpha/Z-beta template, but it is researcher-written
  machinery, not learner-invented. This is L2 structural reuse
  evidence, not L3 representational invention.

## Artifacts

- cx_core.zag (TNN-2 base, ev_query removed), cx_patch.zag
  (composition machinery + pipeline ev_query), cx_driver.zag
  (8-arm experiment), cx_full.zag (concatenated source),
  cx_bin (pinned znc build), cx_run1/2/3.txt (byte-identical),
  cx_compile.txt, NAMECHECK.md, REPORT.md.

## Verdict

COMPOSITION-A-COMPLETE. TNN discovers the X->Y chain from MAP
contracts with no compose instruction, builds a new executable Z
MAP, both ablatives break Z where trial cannot reach, the composite
persists with structural references to its helpers, and it rebinds
directly on a fresh subject. This is the composition capability the
knowledge-composition study found absent, recovered through
goal-conditioned contract chaining.
