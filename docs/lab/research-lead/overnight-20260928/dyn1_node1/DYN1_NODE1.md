# DYN-1 on H3-lite Node 1: Measurement Report

## Verdict

**DYN1-NODE1-COMPLETE: FLAT.** The H3-lite Node 1 learning mechanism does
not bend the DYN-1 cost curve. Per-experience node cost remains exactly
constant within each event type across the same 250-event sequence, even
though the learning machinery fired 7 times during the run.

## Question

DYN-1 (`003767553`) established that frozen TNN-2 is flat: the 70th miss
costs exactly what the 2nd miss cost. The TNN-3 acceptance gate requires a
candidate to bend DYN-1 (per-experience cost decreasing with experience)
before any capability claim counts as learning rather than recording.
H3-lite Node 1 is the first genuine learning mechanism built on TNN-2
(learner-owned trial-order policy with Hebbian promotion and exhaustion
demotion). Does it bend the curve?

## Method

Unfrozen measurement variant `dyn1n1_full.zag`: the Node 1 cognition
(`h3n1_variant.zag` from `45c55ed83`, minus its test `main`) plus the
verbatim DYN-1 driver from `003767553` appended. Same 250-event
lifetime-like sequence, production handlers only:

- Phase A (events 0-79): 80 `ev_teach` (r=1, subjects 1..20)
- Phase B (events 80-129): 50 `ev_query` hits on taught (s,1)
- Phase C (events 130-179): 50 `ev_query` misses (r=99 never taught,
  subjects 101..110; all returned -2, true miss path)
- Phase D (events 180-229): 50 `ev_observe` (s=1..10 confirm, s=11..20
  contradict with 7777)
- Phase E (events 230-249): 20 repeat misses on Phase C keys

Per event: live nodes `hg(W,20)` and live edges `hg(W,24)` sampled before
and after. 3/3 byte-identical runs (SHA-256
`84304b2a5a7c22900d1f608a1669bba5e7eb3b947aa36deefae7c7eea60cf189`).

A probe binary (`probe_bin`, same cognition, driver augmented to emit the
tag-40 policy node state) verified the learning machinery was active.

## Results

### Node deltas: exactly constant (FLAT)

| Phase | Events | dn/event | min | max | Frozen baseline |
|-------|--------|----------|-----|-----|-----------------|
| A teach | 80 | +1 | 1 | 1 | identical |
| B qhit | 50 | +0 | 0 | 0 | identical |
| C miss | 50 | +2 | 2 | 4 | min 2, max 3 |
| D observe | 50 | +2 | 2 | 2 | identical |
| E miss2 | 20 | +2 | 2 | 2 | identical |

The single dn=4 in Phase C is event 130 (the first miss), which creates the
tag-40 policy node in addition to the policy anchor, the UNCERTAINTY node,
and the guide. Every subsequent miss costs exactly +2 nodes, including the
70th. Zero dedup: 70 UNCERTAINTY nodes total, exactly 7 per miss key.

### The learning machinery was active

Probe result after the full sequence:

```
PROBE-POLICY node=82 order=1,0,2,3,4,5 rej=7
```

The policy node was created (node 82) and the exhaustion demotion fired
exactly 7 times: 70 misses each exhausted (all trials returned -2), and
every 9th exhaustion swapped slots 0/1 (7 swaps at 9,18,27,36,45,54,63;
alternation leaves 1,0; remainder rej=7). Hebbian promotion never fired
because no trial succeeded in this sequence. The learner's policy state
changed 7 times. Per-event cost did not change once.

### Final state

322 live nodes, 489 live edges, clock=250 (frozen baseline: 321 nodes;
the +1 is the policy node).

## Interpretation

The Node 1 mechanism changes which trial families are attempted and in what
order. It does not change what structures are reified per event. A miss
always costs one UNCERTAINTY node plus one guide, regardless of the trial
order that preceded it; demotion costs zero nodes (field swaps in place).
DYN-1 measures state-write cost, not scan work: policy reorder can reduce
`t2_try_verify` invocations (the weak K-LT-5 measure E(X)), but it cannot
reduce nodes allocated per event, because the allocation sites are
structural, not policy-gated.

This is the stronger FLAT result: not "no learning happened," but
"learning happened and the curve still did not bend." The 7 demotions are
proof the read/write paths fired; the constant +2 is proof they do not
touch per-experience cost.

## TNN-3 gate implication

To bend DYN-1, a mechanism must reduce structures written per event with
experience. Candidates that could: uncertainty dedup (recognize a repeated
miss instead of reifying a fresh node), guide reuse (match an existing
guide to a new miss), or miss-level decline (withhold the reification when
the substrate predicts failure). Policy reorder over trial families is
provably insufficient: it operates one level below the allocation sites.

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (measurement only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0 (variant cognition from `45c55ed83`; driver is
  harness-side)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

## Constraints honored

Unfrozen variant only. Frozen source read-only, hash verified before and
after. Pure Zag via pinned znc. Safebin active, `which python3 python`
empty. Zero em dashes (byte-verified). Paper untouched. No sealed worlds.
Nothing pushed. Explicit pathspecs on git add and git commit.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/dyn1_node1/`:
- `NAMECHECK.md` (Step 0 toolchain guard, scope, input provenance)
- `DYN1_NODE1.md` (this report)
- `dyn1n1_cog.zag` (verbatim Node 1 cognition)
- `dyn1_driver.zag` (verbatim DYN-1 driver)
- `dyn1n1_full.zag` (measurement variant)
- `dyn1n1_bin` (compiled binary)
- `run1.txt`, `run2.txt`, `run3.txt` (3/3 byte-identical)
- `probe_driver.zag`, `probe_nomain.zag`, `probe_bin`, `probe_run.txt`
  (policy-state probe evidence)
