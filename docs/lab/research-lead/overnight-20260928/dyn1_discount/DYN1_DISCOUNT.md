# DYN-1 on Discount Pilot: Cost Impact Measurement

## Verdict

**DYN1-DISCOUNT-COMPLETE: FLAT.** The discount mechanism (D1+D2+W3+R1)
does not change the DYN-1 cost curve. Output is byte-identical to the
frozen TNN-2 baseline (SHA-256 `4f1367778a6b99f0b59021dc2f658ec4cd436dd1ec2a5098e66305c4c358d753`,
matching `003767553` exactly). The mechanism was completely inert in
the 250-event sequence: its write path never fired.

## Question

The discount pilot (`0daaa2ed4`) adds D1 (per-FACT field-12 discount),
W3 (minority discount increments on non-unanimous bootstrap), and R1
(scan skips facts with discount > 2). DYN-1 (`003767553`) established
frozen TNN-2 is flat; DYN-1 on Node 1 (`67b700d3f`) showed learning
can fire without bending the curve. Does the discount mechanism bend
DYN-1, leave it flat, or worsen it via extra writes?

## Method

Unfrozen measurement variant `dyn1d_full.zag`: the discount pilot
cognition (`discount_impl/di_variant.zag` from `0daaa2ed4`, verbatim,
no test main) plus the verbatim DYN-1 driver (`dyn1/dyn1_driver.zag`
from `003767553`) appended. Same 250-event lifetime-like sequence,
production handlers only:

- Phase A (events 0-79): 80 `ev_teach` (r=1, subjects 1..20)
- Phase B (events 80-129): 50 `ev_query` hits on taught (s,1)
- Phase C (events 130-179): 50 `ev_query` misses (r=99 never taught,
  subjects 101..110; all returned -2, true miss path)
- Phase D (events 180-229): 50 `ev_observe` (s=1..10 confirm, s=11..20
  contradict with 7777)
- Phase E (events 230-249): 20 repeat misses on Phase C keys

Per event: live nodes `hg(W,20)` and live edges `hg(W,24)` sampled
before and after. 3/3 byte-identical runs.

## Results

### Node deltas: identical to frozen (FLAT)

| Phase | Events | dn/event | min | max | Frozen baseline |
|-------|--------|----------|-----|-----|-----------------|
| A teach | 80 | +1 | 1 | 1 | identical |
| B qhit | 50 | +0 | 0 | 0 | identical |
| C miss | 50 | +2 | 2 | 3 | identical |
| D observe | 50 | +2 | 2 | 2 | identical |
| E miss2 | 20 | +2 | 2 | 2 | identical |

Per-event constancy verified: Phase A 80/80 at dn=1; Phase C 49 at
dn=2 plus the single dn=3 first-miss (policy anchor creation);
Phase E 20/20 at dn=2. Zero dedup: 70 UNCERTAINTY nodes, exactly 7
per miss key.

### Final state: identical to frozen

321 live nodes, 489 live edges, clock=250. The transcript hash
matches the frozen baseline hash exactly, confirming the discount
cognition produced no observable behavioral difference in this
sequence.

## Why the mechanism was inert

The discount write path (W3) fires only on non-unanimous bootstrap
evidence with a strict majority. In the DYN-1 sequence:

1. Phases C and E query r=99, which was never taught. The bootstrap
   evidence scan for r=99 finds zero FACTs (cnt=0 < 2), returns -2
   before reaching the unanimity check. W3 never fires.
2. Phase D uses `ev_observe`, which does not call `bootstrap_miss`
   (the only modified function in the pilot). Contradictions on the
   observe path cannot trigger W3 in this implementation.
3. The R1 scan filter (`discount <= 2`) passes for every FACT because
   all discounts remain 0. Scan behavior is unchanged.

The mechanism is dormant by design in the absence of disagreement:
no non-unanimous bootstrap evidence existed in the sequence, so no
discount was ever written.

## Cost analysis: why discount cannot bend DYN-1

Even when W3 fires (as in the contradiction-break replay), it
performs in-place field writes (`ns(W,mn,12,...)`), allocating zero
nodes. D1 reuses the allocator-zeroed field 12, adding no per-FACT
cost. R1 is a read-path filter that changes which facts are
considered, not how many structures are allocated.

DYN-1 measures node allocation per event. The dominant costs are
structural: one UNCERTAINTY node plus one guide per miss, one FACT
node per teach. The discount mechanism operates strictly below these
allocation sites: it annotates existing FACTs and filters scans. It
cannot reduce structures written per event because it never
prevents, dedupes, or reuses an allocation.

This is the same structural lesson as DYN-1 on Node 1: mechanisms
that change decisions (trial order, evidence filtering) without
touching allocation sites leave the cost curve flat. To bend DYN-1,
a mechanism must reduce structures written per event with
experience (uncertainty dedup, guide reuse, or miss-level decline
that withholds reification).

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (measurement only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0 (variant cognition from `0daaa2ed4`; driver is
  harness-side)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

## Constraints honored

Measurement only; unfrozen variant only; frozen source read-only;
pure Zag via pinned znc; safebin active, `which python3 python`
empty; zero em dashes byte-verified; paper untouched; no sealed
worlds; nothing pushed; explicit pathspecs on git add and commit.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/dyn1_discount/`:
- `NAMECHECK.md` (Step 0 toolchain guard, scope, input provenance)
- `DYN1_DISCOUNT.md` (this report)
- `dyn1d_cog.zag` (verbatim discount pilot cognition, no main)
- `dyn1_driver.zag` (verbatim DYN-1 driver)
- `dyn1d_full.zag` (measurement variant)
- `dyn1d_bin` (compiled binary)
- `run1.txt`, `run2.txt`, `run3.txt` (3/3 byte-identical,
  SHA-256 `4f1367778a6b99f0b59021dc2f658ec4cd436dd1ec2a5098e66305c4c358d753`)

**Verdict: DYN1-DISCOUNT-COMPLETE: FLAT.**
