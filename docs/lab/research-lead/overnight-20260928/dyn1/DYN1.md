# DYN-1 Measurement Report

## Verdict

**DYN1-COMPLETE: "write-mostly, not living" CONFIRMED.**

Per-experience node cost is exactly constant within each event type across
250 events. There is no learning curve, no amortization, no dedup. The cost
curve does not bend with experience.

## Method

Unfrozen variant `dyn1_full.zag`: verbatim frozen TNN-2 (`dyn1_base.zag`,
SHA-256 `a29972ca...` verified) with the original test `main` removed and a
measurement driver appended. Cognition code diff-verified byte-identical to
frozen (only the driver differs; driver is harness-side, not cognition).

250-event lifetime-like sequence, production event handlers only:
- Phase A (events 0-79): 80 `ev_teach` (r=1, subjects 1..20)
- Phase B (events 80-129): 50 `ev_query` hits on taught (s,1)
- Phase C (events 130-179): 50 `ev_query` misses (r=99 never taught, fresh
  subjects 101..110; all returned -2, confirming true miss path: trial and
  bootstrap both failed)
- Phase D (events 180-229): 50 `ev_observe` (s=1..10 confirm taught value,
  s=11..20 contradict with 7777)
- Phase E (events 230-249): 20 more misses on Phase C keys (7 misses per key)

Per event: live nodes `hg(W,20)` and live edges `hg(W,24)` sampled before and
after. 3/3 byte-identical runs (SHA-256 `4f1367778a6b99f0b59021dc2f658ec4cd436dd1ec2a5098e66305c4c358d753`).

## Results

### Node deltas (the DYN-1 measure): exactly constant

| Phase | Events | dn per event | min | max | Verdict |
|-------|--------|--------------|-----|-----|---------|
| A teach | 80 | +1 | 1 | 1 | constant (80/80) |
| B qhit | 50 | +0 | 0 | 0 | constant (50/50) |
| C miss | 50 | +2 | 2 | 3 | constant after init |
| D observe | 50 | +2 | 2 | 2 | constant (50/50) |
| E miss2 | 20 | +2 | 2 | 2 | constant (20/20) |

The single dn=3 in Phase C is the very first miss (event 130), which creates
the policy anchor node in `miss_inquire` in addition to the UNCERTAINTY node
and guide. Every subsequent miss, including the 70th, costs exactly +2 nodes.

### Duplication: zero dedup

70 UNCERTAINTY nodes total. Each of the 10 miss keys (101..110, r=99) was
missed 7 times and has exactly 7 UNCERTAINTY nodes. The 7th identical miss
creates the same structures as the 1st. There is no uncertainty dedup.

### Edge deltas: mechanical, not adaptive

Edge deltas vary by +-1 within phases (e.g. teach: 69x +1, 11x +2). Root
cause identified in source: `decay` expires ET_MEM edges on a fixed 12-event
TTL (`hg(W,4)` initialized to 12; each event decrements; at zero the edge is
removed and the edge count decremented). The variation is TTL expiry
coinciding with events, not any decision. Edge creation per event type is
constant; edge destruction is clockwork.

### Final state

321 live nodes, 489 live edges, clock=250 after 250 events. No saturation
reached in this envelope (well under the 1024-node wall).

## Interpretation

DYN-1 asks whether the cost of experience changes with experience. Answer:
no. The per-experience node cost is a fixed constant determined solely by
event type. A miss at event 249 costs exactly what a miss at event 131 cost.
There is no cheaper repeated ignorance, no amortization, no bending of the
curve.

This is the quantitative signature of "write-mostly, not living": state
changes continuously (321 nodes over 250 events) but the process that
changes it does not itself change.

For TNN-3, the acceptance gate from the scaling analysis stands: a candidate
must bend DYN-1 (per-experience cost decreasing with experience for repeated
or similar events) before any capability claim is interpretable as learning
rather than recording.

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (measurement only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0 (Phase D contradictions did not trigger graph revision;
  observations were confirms or simple contradicts on facts without MAPs)
- COGNITION LINES: 0 (driver is harness-side)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

## Constraints honored

UNFROZEN variant only. Frozen source read-only, hash re-verified before and
after. Pure Zag via pinned znc. Safebin active, `which python3 python` empty.
Zero em dashes (byte-verified). Paper untouched. No sealed worlds. Nothing
pushed. Explicit pathspecs on git add and git commit.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/dyn1/`:
- `NAMECHECK.md` (Step 0 toolchain guard, scope, constraints)
- `DYN1.md` (this report)
- `dyn1_base.zag` (verbatim frozen copy, SHA-256 verified)
- `dyn1_driver.zag` (measurement driver)
- `dyn1_full.zag` (variant: base minus test main plus driver)
- `dyn1_bin` (compiled binary)
- `run1.txt`, `run2.txt`, `run3.txt` (3/3 byte-identical)
