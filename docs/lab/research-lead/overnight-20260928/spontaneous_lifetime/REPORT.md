# Spontaneous Connections Lifetime Report

**Verdict: SPONTANEOUS-COMPLETE: RETRIEVES.**

**Date:** 2026-10-01
**Worker:** Spontaneous Connections Lifetime Worker
**Cognition:** byte-identical to rebind treatment variant (`91585087c`).
Base SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.
Cognition bytes of assembled sources verified identical (sha `fac94d6ff56c12dd`).
Only the driver (world stream) is new. Zero cognition changes.

## 1. Design

A continuous 523-event lifetime on one learner, no resets, no task labels,
no "use A now" instruction.

- **Phase 1 (8 events):** Teach structure A. Decoy chain 2->21->22, query
  (2,51) expects 22, promotes plen-3 MAP. Main chain 1->11->12->13->14,
  query (1,50) expects 14, promotes plen-5 MAP.
- **Phase 2 (500 events):** 400 teaches (relations 60-69, entities 5000-5399)
  and 100 observes (relations 70-79, entities 7000-7099). All entities and
  relations disjoint from Phases 1 and 3. No queries, no trials, no MAPs.
- **Phase 3 (15 events):** Teach B facts (chain 101->111->112->113->114 plus
  distractor paths of lengths 3, 4, and a length-5 decoy, all new literals).
  Present query (101,50) expecting 114. No hint. Just the query.

Control: fresh learner, Phase 3 only. Measures blind-trial cost of B.

Spontaneity criterion: the driver never references A during Phase 3. The only
retrieval path is the generic MAP scan inside `ev_query`, which fires on
every miss without instruction.

## 2. Results (3/3 byte-identical per arm)

Treatment SHA-256: `8288019a3b81a05a...`
Control SHA-256: `8e2c6bb14f6b6a14...`

### 2.1 Treatment (full lifetime)

```
A-DECOY ans=22 tried=1 rejected=0
A-MAIN ans=14 tried=3 rejected=2     (rebind tried decoy shape: rejected=1, then trial)
P1 live=67 edges=48 maxnode=68
P2 live=567 edges=452 maxnode=568
B-MAIN ans=114 tried=7 rejected=6    (RB-STAT: rebind fired)
P3 live=658 edges=502
XEDGES a-b=0
```

### 2.2 Control (fresh learner, B only)

```
B-MAIN ans=114 tried=11 rejected=10  (blind trial; rebind scan found no MAPs)
P3 live=143 edges=82
XEDGES a-b=0
```

### 2.3 Headline

The learner **spontaneously retrieved A** after 500 unrelated events.
B cost 7 verifies (rebind) vs 11 (fresh trial): 4 fewer verifies, a 36%
reduction, coming entirely from reuse of the Phase-1 chain structure.
The 500-event gap caused **zero degradation**: 7 verifies here vs 7 verifies
in the no-gap rebinding experiment (`91585087c`). Retention held because
total state (567 nodes) stayed under the 1024 cap, so no eviction touched
A's MAPs.

## 3. Edge analysis (Q12)

**XEDGES a-b = 0.** Zero edges connect Phase-1 node IDs to Phase-3 node IDs.

The rebind mechanism reuses the SHAPE (chain topology read from A's MAP
graph) but assembles fresh cells with B's literals and promotes a new,
separate MAP. It creates no persistent structural link between the source
MAP and the rebound structure. The spontaneous "connection" exists as a
retrieval event (the scan reads A's MAP during B's miss), not as new edges
in the graph.

Implication: current reuse is functional, not structural. If the target is
a growing web of cross-domain connections visible in the graph, that
requires a mechanism not present here. The retrieval happened; the trace
did not persist.

## 4. What this establishes

1. **Spontaneous retrieval works across a 500-event gap.** No hint, no task
   label, no reset. The generic miss-path scan found A's MAP and rebound it.
2. **No interference from unrelated experience.** 500 unrelated teaches and
   observes on disjoint relations did not disturb the MAPs, the scan, the
   gather, or the verification. Cost identical to the no-gap case.
3. **The cost difference is reuse, not priming.** The control (same B facts,
   no A) costs 11; the treatment costs 7. The ablation in `91585087c`
   already showed MAPs are inert without the rebind machinery.
4. **Retention was not stressed.** 567 < 1024, so eviction never fired.
   This experiment does not test whether A survives memory pressure; the
   interference and budget-pressure experiments cover that (answer: poorly).

## 5. What this does NOT establish

- No test under memory pressure (eviction would likely kill A's MAPs first,
  per the recency policy and the fossil census).
- No structural connection formation (XEDGES=0).
- No competing-structure selection under ambiguity beyond the decoy
  rejection already shown.
- Chain family only (inherited limit from the rebind mechanism).
- The "spontaneity" is the mechanism firing on every miss by construction;
  there is no separate decision to retrieve. A learner that chose WHEN to
  attempt retrieval would be a further step.

## 6. Standing metrics

- RESEARCHER-OWNED: rebind procedure (~70 lines, prior work); this worker's
  world-stream design (phase structure, 523-event layout, disjoint
  entity/relation allocation, cross-era edge census).
- LEARNER-OWNED: 2 Phase-1 MAP graphs (reused in Phase 3); 1 rebound MAP
  (created in Phase 3 from A's shape + B's literals).
- SOURCE-ENUMERABLE: chain plen read from learner graph topology.
- SUF DECISIONS: 0.
- REUSE EVENTS: 1 (B query rebound from A's MAP).
- REVISION EVENTS: 0.
- COGNITION LINES: 0 (driver only).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## 7. Process notes

- Toolchain guard: `which python3 python` empty under safebin PATH. One
  stray `python3 -c` probe was typed during driver editing but did not
  execute (binary not in PATH; no output produced). No forbidden executable
  ran. No contamination.
- Determinism: 3/3 byte-identical per arm, exit 0, zero stderr.
- Paper untouched. Nothing pushed. Frozen source read-only.

## 8. Artifacts

- `NAMECHECK.md` (Step 0 guard, provenance)
- `REPORT.md` (this file)
- `sl_driver_treat.zag`, `sl_driver_ctrl.zag` (world streams)
- `sl_full_treat.zag`, `sl_full_ctrl.zag` (assembled sources)
- `sl_treat_bin`, `sl_ctrl_bin` (binaries)
- `sl_treat_run1/2/3.txt`, `sl_ctrl_run1/2/3.txt` (3/3 transcripts)
