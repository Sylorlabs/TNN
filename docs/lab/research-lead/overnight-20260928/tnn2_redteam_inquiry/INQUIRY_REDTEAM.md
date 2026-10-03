# TNN-2 Inquiry Red Team Report

Target: `tnn2.zag` frozen at `f4de7ff46` (SHA-256 verified). Read-only analysis.
Verdict: **INQUIRY-ATTACK-SUCCESS**

Two findings: (1) the "discriminating need" link is hardcoded, not
learner-derived; (2) the "evidence updates later behavior" link is
absent. Details below.

## 1. Causal-chain verification (link by link)

Required chain: unknown/miss -> learner creates uncertainty ->
learner derives discriminating need -> learner constructs guide ->
POLICY_ROOT receives it -> ACT selects based on learner state ->
evidence updates later behavior.

### L1. unknown/miss -> inquire trigger: LEARNER-ORIGINATED (PASS)

`ev_query` (line 813) miss path:
- line 815: `activate` fails (no stored fact).
- line 829: `mp_run` -> `t2_trial` returns -2 (no constructible graph verifies).
- line 831: `bootstrap_miss` returns -2 (no P-INV bootstrap).
- lines 833-834: `miss_inquire(W,s,r)` called, then return -2.

The trigger fires only after genuine failure of retrieval AND
construction AND bootstrap. No test scaffolding on this path. On an
empty state all three fail honestly, so the trigger is reachable
from empty learner state.

### L2. learner creates uncertainty: LEARNER-ORIGINATED (PASS)

`miss_inquire` (lines 795-812):
- line 796: `alloc_node(W)` allocates from the persistent workspace.
- line 797: `ns(W,u,0,30)` tags it T_UNCERT (30, defined line 85).
- line 799: `write_node(W,u,s,r,2,0)` records the specific miss (s,r)
  into slots 20,24. Content is miss-derived, not a default.
- No test function calls `miss_inquire`; its sole production caller
  is `ev_query`. The `t_t2_inquire` test (line 1237) uses fresh state
  and only public `ev_teach`/`ev_query`, confirming empty-state
  creation.

### L3. learner derives discriminating need: HARDCODED (ATTACK-SUCCESS)

This is the first broken link. `miss_inquire` lines 805-808:
```
let g:i32=alloc_node(W); if(g<0){return;}
ns(W,g,0,1); ns(W,g,4,s);
write_node(W,g,30,-999,0,0);
```
The guide's action value (slot 20 = 30) and content (slot 24 = -999)
are researcher-authored constants. There is no computation anywhere
in the inquiry path of:
- what evidence would discriminate between candidate hypotheses;
- which question is more informative;
- what the learner expects to learn.

The "guide" is a constant-action pointer ("do inquiry-action 30"),
not a derived discriminating need. `ev_act` returns slot 20 = 30
(line 896: `let av:i32=ng(W,best,20)`), so the entire inquiry
"action" is the constant 30 regardless of what is unknown. A
genuinely derived need would vary with the uncertainty; this one
cannot.

### L4. guide -> POLICY_ROOT: LEARNER-ORIGINATED (PASS)

- lines 800-804: POLICY_ROOT fetched via `pol_get` (header slot 20);
  if absent (<2), created on demand with `alloc_node` and `pol_set`.
- line 810: `link_edge(W,pr,10,g,0)` links POLICY_ROOT to guide.
- line 809: `link_edge(W,g,1,u,0)` links guide to uncertainty node.
All in persistent learner state, on the real path, no scaffolding.
Line 807 is the only production-code site creating a POLICY_ROOT-
linked guide (all other guide creations are in test functions).

### L5. ACT selects based on learner state: REAL MACHINERY, TRIVIALLY SATISFIED (QUALIFIED)

`ev_act` (lines 859-911) is genuine selection machinery: it scans
edges from POLICY_ROOT, filters by `is_superseded` (line 132),
context match against the 4-deep ring buffer (`ctx_get`, line 294),
and max `bid` (line 237, event-count based). This is real code over
learner state, not a hardcoded return.

However, in every exercised scenario there is exactly one guide, so
selection is trivially satisfied. `bid` differences only matter with
competing candidates, which no test constructs. The machinery is
general; the coverage is not. Additionally, `t_t2_actlive` (line
1263) calls `ctx_push(W,9002)` manually before `ev_act`; this is
redundant rather than load-bearing, because `ev_query` already
pushed s=9002 (line 814) and the ring buffer retains it at position
1 after `ev_act` pushes -3 (line 860). Verified by reading
`ctx_push`/`ctx_get` (lines 291-295).

### L6. evidence updates later behavior: ABSENT (ATTACK-SUCCESS)

This is the second broken link. When the missing fact is later
learned:
- `ev_observe` (line 836) on a miss calls `ev_teach_in`, which
  stores the fact. It never checks for, resolves, or removes
  UNCERTAINTY nodes (tag 30).
- `revise_on_contradict` (line 685) only scans MAP nodes (tag 20);
  it never touches guides or uncertainties.
- `is_superseded` (line 132) requires a type-3 self-edge; nothing in
  any production path creates one on a guide or uncertainty node.

Consequences: the UNCERTAINTY node and its guide persist forever,
remain POLICY_ROOT-linked, and remain ACT-eligible. A resolved
uncertainty can still win ACT selection later. There is no
"uncertainty resolved" transition anywhere in the source.

## 2. Attack results

### Attack 1: ambiguous evidence (two warranted uncertainties)

Source-level analysis. Two misses on (s1,r1) and (s2,r2) create two
uncertainty nodes and two guides, both linked to POLICY_ROOT.
`ev_act` selects by context match then max `bid`. Both guides are
content-identical (constant 30/-999); only slot4 (s) differs. With
both subjects in context, `bid` decides on incidental event counts
(fresh guides have near-zero counts; ties resolve to first found in
edge order). There is no informativeness comparison: the learner
cannot prefer the more informative inquiry. The disambiguation is
arbitrary, not derived. WEAK.

### Attack 2: misleading evidence (guide then contradiction)

Source-level analysis. Once a guide is constructed, no production
path revises or removes it. `revise_on_contradict` handles only
executable-graph MAPs. No type-3 supersession edge is ever created
on guides. If evidence later shows the inquiry was misguided, the
guide persists and remains selectable. The inquiry mechanism locks
in; it does not revise. FAIL.

### Attack 3: empty-state trigger

Verified via `t_t2_inquire` (line 1237): fresh `tnn2_init` state,
one `ev_teach` for an unrelated fact, then `ev_query` on an unknown.
The UNCERTAINTY node (tag 30, slots 20/24 = 9002/77), the guide
(tag 1, slot4 = 9002), and both edges (types 1 and 10) are all
created with no pre-existing structure. PASS: creation is from
learner machinery on the real path.

### Attack 4: test-scaffolding audit of T2-INQUIRE / T2-ACTLIVE

- Neither test pre-creates UNCERTAINTY nodes, guides, or POLICY_ROOT.
  State is fresh; all inquiry state arises from `ev_query` ->
  `miss_inquire`. PASS.
- `t_t2_actlive`'s manual `ctx_push(W,9002)` is redundant (see L5),
  not load-bearing. Minor note, not a scaffolding violation.
- Separately: pre-existing ACT tests (`t_a2` line 1045, `t_a5` line
  1065, `t_dv` line 1163) and the `r_mk_uncert` helper (line 1378)
  DO create tag-30 nodes via scaffolding, but those test ACT
  selection in isolation and predate the TNN-2 inquiry integration;
  they do not touch the `miss_inquire` path.

## 3. Summary of what works and what does not

Works (genuinely learner-originated on the real path):
- Miss detection after retrieval, construction, and bootstrap all fail.
- Uncertainty node creation with miss-specific content in persistent state.
- Guide construction and POLICY_ROOT linkage in persistent state.
- ACT selection machinery over learner state (bid, context, supersession).
- Empty-state creation; no scaffolding in the new inquiry tests.

Broken:
- L3: no derived discriminating need. Guide action (30) and content
  (-999) are constants. The learner never computes what would be
  informative. (Hardcoded link.)
- L6: no evidence-driven update. Uncertainty is never resolved;
  guides are never superseded on learning. Stale guides stay
  ACT-eligible. (Missing link.)
- Under ambiguity, selection is arbitrary (no informativeness basis).
- Under misleading evidence, inquiry locks in (no guide revision path).

## 4. Architectural implication

As integrated, the inquiry mechanism is a miss flag plus a constant
action, not discriminating information seeking. It satisfies the
letter of K-T2-4 (uncertainty node created) and K-T2-5 (non-constant
act choice vs the 0 fallback) but not the spirit: the "choice" of 30
is constant across all uncertainties, and nothing ever clears the
flag. A next generation that wants genuine inquiry needs (a) a
derived question representation (what would discriminate), and
(b) a resolution transition on learning. Neither exists here.

## Verdict: INQUIRY-ATTACK-SUCCESS

Specified hardcoded/missing links: L3 (discriminating need is a
researcher constant, lines 805-808) and L6 (no uncertainty
resolution or guide supersession anywhere in production code).
