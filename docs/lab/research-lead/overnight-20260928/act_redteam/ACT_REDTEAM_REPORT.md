# ACT Red Team Audit Report

**Verdict: ACT-REDTEAM-COMPLETE.** Adversarial audit of the ACT
implementation (commit `f7d87938f`) against the prereg (commit
`51a818141`). All 24 builder tests re-run and confirmed PASS.
Five attack vectors investigated. One ATTACK-SUCCESS (spec
divergence), two caveats (hardcoded protections), remainder
ATTACK-PASS.

## Method

- Step 0 toolchain guard recorded in NAMECHECK.md. Zero Python
  invocations. Shell/git/read-only analysis.
- Full source read of `act.zag` (615 lines).
- Full prereg read of `PREREG_ACT.md` (337 lines).
- Integration spec cross-check for signed-bid definition.
- CLA-2 `bid()`/`evcount()` cross-check for aggregation consistency.
- Branch enumeration in `act_event`, `activate`, `nbr`, `bid`.
- Binary re-run: `./act_bin all` -> 24/24 PASS, ALL-PASS.

## Vector 1: Genericity -- ATTACK-PASS (with caveat)

`act_event(nd, ed, st, cx)` takes only stores plus context. No
world, task, or relation parameters exist in the signature.

All 8 branches in `act_event` classified:
- `if(pr<=0)` : null POLICY_ROOT check. Structural.
- `if(nget(nd,pr,0)==0)` : tombstoned root check. Structural.
- `if(nget(nd,a,0)!=0)` : node liveness check. Structural.
- `if(r0==ctxget(cx,k) && r0!=0)` : address equality on refs.
  Structural. This is the entire "match" semantics.
- `if(m==1)` : match flag. Structural.
- `if(b>bestbid || (b==bestbid && (best<0 || a<best)))` :
  numeric bid comparison with deterministic lowest-address
  tie-break. Content-free ordering, not semantic preference.
- `if(best<0)` : no-match check. Structural.

Type tags T_GOAL (101), T_GUIDE (102), T_UNCERT (103),
T_CONSEQ (104), T_FACT (105), T_SESSION (106) are defined but
NEVER checked in `act_event` or in `activate`. Verified by grep:
zero tag references in either function. The core does not
interpret tags, exactly as the prereg requires.

**Caveat:** `nbr()`, called by `activate()`, called by
`act_event()`, contains two hardcoded exclusions:
- Line 150: `if(f==a && t!=REG_NODE())`
- Line 153: `if(t==a && f!=REG_NODE())`
Node 0 is excluded from graph traversal by address. This is not
a branch on world/task/relation identity, so it does not violate
the letter of K-ACT2. It is a hardcoded structural special case
in the traversal path. See Vector 2 for the full protection
analysis.

## Vector 2: POLICY_ROOT -- ATTACK-PASS (with caveat)

`polset` uses `nset(nd,REG_NODE(),5,a)`. `polget` uses
`nget(nd,REG_NODE(),5)`. These are the ordinary node-store
WRITE/READ operations. No special register opcodes, no separate
storage. The mechanism matches A12.

**Caveat:** Node 0 (and node 1) are protected by THREE
scattered hardcoded address checks, not by a unified mechanism:
1. `nalloc` line 97: `if(a<1){ a=1; }` -- node 0 never allocated.
2. `evict_to_cap` line 331: `let a:i32=2;` -- nodes 0-1 never
   evicted (loop starts at 2).
3. `nbr` lines 150, 153: node 0 excluded from traversal.

If node 0 is "just a node written via ordinary WRITE," the three
hardcoded protections are ad-hoc. A principled design would use
one mechanism (for example, the defined-but-unused E_PROTECT
edge type, or a register-file abstraction). The protections are
defensible as "registers are protected by definition," but the
implementation does not have a register abstraction -- it has
three address comparisons in three different functions.

This does not affect test outcomes. It is an architectural
smell: the kind of scattered special-casing the One-System Rule
asks us to notice.

## Vector 3: Evidence bid -- ATTACK-SUCCESS (spec divergence)

The ACT `bid()` counts edges touching the node in EITHER
direction:
```
if(f==a){ hit=1; }
if(t==a){ hit=1; }
```

The CLA-2 `evcount()`, which the integration spec cites as the
reference aggregation, counts only INCOMING edges:
```
if(eg(W,e,8)==n){   // field 8 is the target
```

Integration spec A3 (line 358-364): "select the match with the
highest CLA-2 evidence bid (count over USE / CONFIRMS / SUPPORTS
edges per the eviction aggregation). ... The core already
computes bid(node) for eviction; ACT reuses the same function."

ACT does NOT reuse the same function. It implements its own
`bid()` with bidirectional counting.

**Impact analysis:** In the current test suite, all evidence
edges are incoming (`learn_confirm` creates ses -> guide via
USE/CONFIRMS; `mk_guide` creates guide -> goal via DEPENDS which
is not counted). The divergence is not exercised by the tests.

**Divergent case:** A guide with an outgoing SUPPORTS edge to an
outcome node (guide -> outcome, SUPPORTS), as described in
prereg section 2(d) "CONSEQUENCE structures," would score:
- CLA-2 directional: 0 (guide is source, not target)
- ACT bidirectional: +1

The prereg section 2(d) explicitly describes ACTION-GUIDE nodes
linking SUPPORTS to outcome nodes. Under the ACT implementation,
those consequence edges inflate the guide's own bid. Under the
CLA-2 aggregation they would not.

**Severity:** Medium. The tests pass, but the implementation
diverges from the frozen integration spec on the definition of
the bid. If CLA-2 and ACT are to share "the same bid" for
architectural compression (the spec's stated goal), one of them
must change. Recommend: align ACT `bid()` with CLA-2
`evcount()` directionality, or amend the spec to authorize
bidirectional counting with rationale.

## Vector 4: Uncertainty -- ATTACK-PASS

`act_event` contains zero references to T_UNCERT (103) or any
tag. The P-ACT2 uncertainty behavior is emergent from wiring:
- Guide g1 has ref0 = uncertainty node u.
- Context contains u (pushed via `ctxpush(cx,u)`).
- Address equality `r0==ctxget(cx,k)` matches.
- No tag interpretation occurs.

The decoy test (decoy context -> action 21, not 20) confirms no
positional bleed. The `act_event` signature takes no positional
input, so the P-ACT2 swap-test requirement is satisfied
structurally.

The "uncertainty" is purely a learner-side convention. This is
CORRECT per the design: the prereg section 2(c) says uncertainty
is "ordinary workspace content that can serve as a context
anchor." The implementation honors this. No curiosity module,
no uncertainty bonus, no drive term found in source.

## Vector 5: K1/K2/K3 -- VERIFIED

**K1 (prereg ordering):** PASS. `git merge-base --is-ancestor
51a818141 f7d87938f` returns true. The prereg strictly precedes
the implementation.

**K2 (no task branches/modes/bridges):** PASS on letter.
- Zero `if` branches on world/task/relation identity in the
  ACT handler. Verified by grep: the only "world|task|relation"
  match near an `if` is a code comment.
- Zero modes, zero bridges, zero task-specific handlers.
- Zero regularity detectors, zero planners, zero search.
- **Caveat:** Three hardcoded address-based register
  protections (Vector 2) and the `nbr()` traversal exclusion
  (Vector 1) are hardcoded special cases, though not
  world/task/relation branches.

**K3 (pure Zag):** PASS.
- `grep -i python act.zag` returns one match: line 19, a comment
  reading "Pure Zag. No Python." No Python code, no Python
  invocation.
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md`:
  zero diff from 323f2afaa to HEAD. Untouched.
- Shell-only byte checks used for dash verification.

## Summary of findings

| Vector | Result | Detail |
|--------|--------|--------|
| 1. Genericity | ATTACK-PASS* | Zero task branches; tags never checked; *`nbr()` hardcodes node-0 exclusion |
| 2. POLICY_ROOT | ATTACK-PASS* | Ordinary WRITE/READ; *three scattered address protections, no register abstraction |
| 3. Evidence bid | ATTACK-SUCCESS | Bidirectional count diverges from CLA-2 directional `evcount()`; spec says "reuses the same function" |
| 4. Uncertainty | ATTACK-PASS | Emergent from wiring; zero tag checks; no curiosity module |
| 5. K1/K2/K3 | PASS | Ordering, purity, and paper verified |

## Recommendations for parent

1. **Bid alignment (medium):** Decide whether ACT `bid()`
   should match CLA-2 `evcount()` directionality. The
   integration spec's "reuses the same function" is currently
   false. Either change ACT to directional counting or amend
   the spec with rationale for bidirectional. The consequence
   edges in prereg 2(d) make this more than cosmetic.

2. **Register protection (low):** The three hardcoded address
   checks work but are ad-hoc. If the architecture grows more
   registers, consider a unified protection mechanism. Not
   blocking.

3. **No test invalidation:** All 24 tests pass under both the
   current and the recommended (directional) bid semantics,
   because the test suite uses only incoming evidence edges.
   The BUILD-COMPLETE verdict stands; the divergence is a
   spec-compliance issue, not a correctness issue.

## Governance

- Read-only audit. Implementation not modified.
- Zero Python invocations by this worker.
- No sealed FW1-FW9 files accessed.
- Contaminated paper zero-diff verified.
- Dash-clean via shell byte check.
