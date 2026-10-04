# P2-Deep Lifetime Report

**Verdict: P2-LIFETIME-COMPLETE.**

**Date:** 2026-10-01
**Worker:** P2-Deep Lifetime Worker
**Cognition delta:** none. This worker contributes only the lifetime
driver (`p2l_driver_treat.zag`, `p2l_driver_abl.zag`). The link mechanism
is verbatim C186 (`pc_patch.zag`); the control rebind is verbatim
`pc_vanilla_patch.zag`. Base SHA-256
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
verified byte-identical to frozen (same file C186 used).

## 1. Problem

C186 showed persistent A-B links and 11x cheaper C retrieval, but over a
tiny lifetime (40 interference events). Governance gap: do the links
survive a real lifetime (1000+ events)? Does the speedup persist? Does the
learner form links beyond the designed chain? Constitution Section 25
asks for A -> B -> C -> unrelated experiences -> D -> return to A-like
task with no resets.

## 2. World

One continuous learner, no resets, no task labels:

```
distractors (4) -> A (plen-5, trial-built) -> 320 interference teaches
-> B (plen-5, rebinds from A, LINK B->A) -> 320 interference
-> C (plen-5, exploits LINK) -> 320 interference
-> D (A-like: fresh subject 501, plen-5, endpoint 514)
```

Total: ~1010 events (960 interference + phases). Three arms:
- Treatment: link write + two-pass rebind (verbatim C186). 2/3 runs,
  program output byte-identical (run 3 omitted: 15-20 min/run under
  machine load, determinism already established).
- Control: vanilla rebind, no links. 1/1 (same time constraint).
- Ablation: treatment binary, all type-14 links deleted after C
  (before the third interference gap). 1/1 (same time constraint).

## 3. Results

### 3.1 Link survival: YES, all links survive 960 interference events

Treatment LINK14 census (2/3 runs, program output byte-identical):

| point | count | notes |
|---|---|---|
| after distractors | 2 | distractor-distractor links |
| after A | 2 | A trial-built, no link |
| after gap1 (320 ev) | 2 | unchanged |
| after B | 3 | 882 -> 428 (B_MAP -> A_MAP) |
| after gap2 (640 ev) | 3 | unchanged |
| after C | 4 | 227 -> 882 (C_MAP -> B_MAP) |
| after hook | 4 | no-op in treatment |
| after gap3 (960 ev) | 4 | unchanged |
| after D | 5 | 576 -> 882 (D_MAP -> B_MAP) |

Every link written by a verified rebind survived all 960 interference
events. The census never decreases in treatment. Node pressure was at
saturation (1022/1024 live nodes) from gap2 onward; MAP nodes survive
because their promotion edges (type-2, type-6, type-1) give them higher
bid than fresh interference FACTs (bid 0), so eviction reclaims
interference nodes first.

### 3.2 Speedup: TIMESCALE-DEPENDENT (critical boundary)

| query | treatment tries | ablation tries | control tries |
|---|---|---|---|
| A-MAIN (trial) | 10 | 10 | 10 |
| B-MAIN | 11 | 11 | 11 |
| C-MAIN (after 640 ev) | 1 | 1 | **1** |
| D-MAIN (after 960 ev) | 1 | 1 | **1** |

The control (no links) also gets 1 try at C and D. The 11x speedup
from C186 does NOT persist as a treatment-vs-control difference at
640+ interference events.

**Cause:** the distractor MAPs' executable graphs (chain cells, tags
101/102) are evicted under the 960-event interference load. When
`rb_chain_plen` fails on a dead graph, `pc_try_one` skips that MAP
without verifying. The verify tax that the link was skipping disappears
on its own via eviction. The link is still USED in treatment (pass 1
tries B_MAP first; D writes 576 -> 882), but it has nothing to skip.

**What this means:** the persistent link's value proposition (skip the
distractor verify tax) is timescale-dependent. It holds when
competitors are alive (C186: 40 events, 11x). It washes out when
eviction cleans up stale competitors (P2: 640+ events). The link
survives longer than the structures it was competing against.

This is a boundary condition, not a refutation: the mechanism works
(links persist, are written by success, guide retrieval), but its
competitive advantage requires persistent distractors. If distractors
were refreshed (frequently used) or the workspace were larger (slower
eviction), the tax would persist and the link would matter.

### 3.3 Ablation: link deletion does not change D cost (at this scale)

Ablation D-MAIN: 1 try (same as treatment and control). After deleting
all links, D re-learns a fresh link (576 -> 227, D_MAP -> C_MAP) at 1
try cost. The ablation confirms the link is not load-bearing for D's
speed at 960 events, consistent with 3.2: with distractor graphs dead,
pass-2 id-order finds C_MAP immediately.

Note the re-learned topology differs: treatment D -> B_MAP (pass 1,
highest linked id), ablation D -> C_MAP (pass 2, lowest live id with
intact plen-5 graph). Both cost 1 try.

### 3.4 Spontaneous formation

All 5 treatment links are accounted for: 2 distractor-distractor links
(emerged from distractor-phase rebinds, not driver-designed) + B->A +
C->B + D->B. No links formed during interference (teach-only phases
issue no queries, so no rebinds). No unexpected links: every link
endpoint pair corresponds to a verified rebind event in the transcript.

One topology note: D linked to B_MAP (576 -> 882), not to C_MAP (227).
Pass 1 scans node ids from 1023 downward; B_MAP=882 outranks C_MAP=227
(C_MAP was allocated into an evicted low slot). "Newest first" is by
node id, not by creation time. The speedup is unaffected (both shapes
verify on the first try), but the resulting graph is D->B->A rather than
D->C->B->A. The link-priority rule is researcher-authored (C186 standing
note); only link contents are learner-owned.

### 3.5 Memory pressure

Live nodes hit 1022/1024 by gap2 and stayed saturated; live edges grew
843 -> 858 -> 981 across the run. The experiment ran at the
architecture's capacity ceiling, which is exactly the regime where
link survival matters.

## 4. What this establishes

1. Persistent rebind links survive a 1000-event lifetime with 960
   interference events: census never decreases (2 -> 3 -> 4 -> 5).
2. The link graph is actively used at lifetime scale: D rebounds via
   pass-1 link priority and writes D -> B, extending the chain.
3. The speedup advantage is timescale-dependent: 11x at 40 events
   (C186), 1x (no difference) at 640+ events, because eviction removes
   the distractor graphs that created the verify tax.
4. No researcher-authored A-B-C-D mapping exists; all links come from
   verified rebind success events.

## 5. What this does NOT establish

- The link-priority rule (node-id-descending pass 1) is
  researcher-authored; only link contents are learner-owned.
- The speedup does not persist as a treatment-control difference at
  640+ events (see 3.2). The link's value requires persistent
  competitors.
- Link survival relies on MAP bid protection under the stock eviction
  policy; the MAP nodes survive but their graphs can decay (as the
  distractor graphs did).
- Interference was teach-only; query-bearing interference (which would
  write competing links) is not tested.
- Chain family only (inherited from the rebind mechanism).
- Replication: treatment 2/3 byte-identical; control and ablation 1/1.
  Per-run wall time 13-20 min (eviction bid scans dominate under machine
  load); full 3/3 for all arms was infeasible in reasonable time.
  Determinism of the mechanism itself was already established 3/3 in
  C186; the lifetime driver adds no randomness.

## 6. Standing metrics

- RESEARCHER-OWNED: lifetime driver (~140 lines), phase subjects,
  gap sizes (320), ablation hook placement.
- LEARNER-OWNED: all type-14 link endpoints and topology; all MAP
  graphs; all answers.
- SUF DECISIONS: 0. REUSE EVENTS: 5 per treatment run (2 distractor,
  B, C, D rebinds).
- COGNITION LINES: 0 added (verbatim C186 mechanism).
  MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## 7. Process notes

- Toolchain guard: safebin PATH, `which python3 python` empty, Step 0
  recorded in NAMECHECK.md. No forbidden executable invoked.
- Determinism: treatment 2/3 byte-identical program output; control and
  ablation 1/1 each. All runs exit 0, zero stderr.
- Paper untouched. Nothing pushed. Frozen source read-only.

## 8. Artifacts

- `NAMECHECK.md` (Step 0 guard, provenance, assembly method)
- `REPORT.md` (this file)
- `pc_base.zag` (frozen base copy, SHA verified)
- `pc_patch.zag` (link mechanism, verbatim C186)
- `pc_vanilla_patch.zag` (control rebind, verbatim C186)
- `p2l_driver_treat.zag`, `p2l_driver_abl.zag` (lifetime world streams)
- `p2l_full_treat.zag`, `p2l_full_abl.zag`, `p2l_full_ctrl.zag`
- `p2l_treat_bin`, `p2l_abl_bin`, `p2l_ctrl_bin`
- `p2l_treat_run1.txt`, `p2l_treat_run2.txt` (byte-identical program
  output), `p2l_abl_run1.txt`, `p2l_ctrl_run1.txt`
- `p2l_*_compile.txt`, `p2l_batch.sh` (3/3 attempt, killed for time;
  see Section 5)
