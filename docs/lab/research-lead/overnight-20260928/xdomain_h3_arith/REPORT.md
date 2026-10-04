# REPORT.md -- H3 Dataflow Generality on Arithmetic to Planning

## Verdict: XDOMAIN-H3-ARITH-FAIL (clean negative, white-box diagnosed)

H3's dataflow mechanism does NOT generalize to arithmetic to planning.
The failure is clean, deterministic (3/3 byte-identical), and diagnosed
to the exact line where the mechanism's structure-derived execution
assumption breaks. This bounds H3's generality: it is chain to count
specific in its execution semantics, not a general cross-domain
mechanism.

## Kill bars (frozen in PREREG.md, commit 4760d5c9e)

| Bar | Result | Detail |
|-----|--------|--------|
| K1 SOLVE | **FAIL** | TREAT Z ans=-2 (expected 203) |
| K2 CAUSAL | PASS | ABL-X, ABL-Y, FRESH all ans=-2, no ZMAP |
| K3 MECHANISM-CAUSAL | PASS | NO-DF TREAT ans=-2 |
| K4 LEARNED-NOT-ASSIGNED | PASS | Zero 93/91/92/71/82 literals in df_patch.zag |
| K5 DETERMINISM | PASS | 3/3 byte-identical, sha256 d035b25407960265a8cd3e05d815439efcdd408ebfc3147bdfec04aa92c1ea53 |
| K6 NO-TEMPLATE | PASS | No ARITH_TO_PLAN or SUM_TO_PLAN in any source |
| K7 REUSE | **FAIL** | Z2 ans=-2 (expected 213) |

NO-DF run sha256: a9db85560718ec1cc21b652173ad29199ac364970901ce9136b1a664cb01b53a.

## Competence (all arms): HOLDS

| Query | TREAT ans | via |
|-------|-----------|-----|
| X1 (101,91) | 15 | trial sum (1 tried, 0 rejected) |
| X2 (102,91) | 10 | trial sum (1 tried, 0 rejected) |
| Y1 (15,92) | 203 | trial chain (2 tried, 1 rejected) |
| Y2 (10,92) | 213 | rebind (1 tried, 0 rejected) |

MAP census (TREAT, identical across runs):
- 2 arith MAPs: r=91, plen=-1, factrel=71, class=arith (pure INC chains)
- 2 plan MAPs: r=92, plen=4, factrel=82, class=chain

Both domains are solidly learned. The negative is mechanism-specific,
not a broken world. Trial alone cannot solve Z in FRESH (tried=6,
rejected=6), confirming Z requires composition.

## White-box diagnosis: the exact breaking line

Trace (TREAT Z, identical in all 3 runs):
```
DF-DISCOVER s=103 r=93
DF-STAGE1 proc=0 rel=91 factrel=71
DF-STAGE1 out=1
DF-STAGE1 proc=1 rel=91 factrel=71
DF-STAGE1 out=1
DF-NOWIRE
Z ans=-2
```

The failure is in `df_exec_sub` (df_patch.zag, verbatim from canonical
H3):

```zag
fn df_exec_sub(W:[]u8,map_id:i32,s:i32,fact_rel:i32)i32 {
  let root:i32=ng(W,map_id,20);
  if(root<0){return -2;}
  if(df_has_inc(W,root)==1){
    return df_count_links(W,s,fact_rel);   // <-- TAKEN for SUM MAP
  } else {
    return df_walk_end(W,s,fact_rel);
  }
}
```

The SUM MAPs are pure unrolled INC chains (t2_asm_sum). `df_has_inc`
returns 1. So `df_exec_sub` calls `df_count_links(W,103,71)`.

But sum facts are STAR-shaped, not chains: (103,71,6), (103,71,9).
`df_count_links` walks transitively:
1. Find (103,71,6). nxt=6, cnt=1.
2. Find (6,71,*). None. Return 1.

Result: out=1, not sum=15. The correct answer requires summing OBJECT
values (6+9=15), which neither `df_count_links` nor `df_walk_end` can
express.

Discovery then searches for Q with `df_has_fact(W,1,82)`. No (1,82,*)
facts exist. Both X MAPs tried, both give out=1. pi stays -1.
DF-NOWIRE. Z fails.

## The architectural boundary

H3's execution is **structure-derived** with exactly two modes:
1. INC cells present implies count links (`df_count_links`).
2. Otherwise walk to endpoint (`df_walk_end`).

This works when MAP structure faithfully encodes the computation:
- Chain MAP (no INC) to walk to endpoint: correct.
- Count MAP (INC cells, chain-shaped facts) to count links: correct.

It fails when the computation is **value-aggregation over star-shaped
facts**: the INC cells are present (so mode 1 is selected), but the
facts do not form a walkable chain, and the answer is not a link
count. SUM is the minimal case; MAX, AVG, or any object-value
reduction would fail identically.

H3 does not re-execute the MAP's own graph. It re-derives execution
from a structural heuristic. That heuristic is chain/count specific.

## Three-way comparison (same domain pair)

| Mechanism | Z | Z2 | Principle | Verdict |
|-----------|---|----|-----------|---------|
| H1 typed contracts | 3 tries, PASS | 3 tries, PASS | Learned signatures prune pair search; procedures are black boxes | PASS (0c6cfa780) |
| H2 value composition | 6 tries, PASS | 5 tries, PASS | Ordered pair search over black-box executions | PASS (0c6cfa780) |
| H3 dataflow | NOWIRE, FAIL | NOWIRE, FAIL | Structure-derived execution (INC to count, else walk) | **FAIL (this worker)** |

The key difference: H1 and H2 treat learned procedures as **black
boxes** whose behavior is observed (signatures from probe outputs, or
direct execution). They do not inspect HOW the procedure computes.
H3 inspects MAP structure to decide HOW to execute, and its two-mode
heuristic cannot express value-aggregation.

## What this means for the generality claim

H1 and H2 generalize to arithmetic to planning because their
composition principles (type-directed search, value-level function
application) are agnostic to internal representation. H3's dataflow
wiring (discover P, execute to mid, discover Q) is sound, but its
**execution** step is not general. The wiring discovery would work if
`df_exec_sub` could actually execute a SUM procedure; it cannot.

A repair would require `df_exec_sub` to re-execute the MAP's own
arithmetic graph (or dispatch on a richer learned execution
signature), not just INC-presence. That is a mechanism change, not a
driver change, and is out of scope for this generality test (which
required verbatim mechanism logic).

## Honest boundaries

1. One domain pair (sum to plan). The "H3 is chain to count specific"
   claim rests on the white-box mechanism analysis (two-mode
   structure-derived execution), not on sweeping the pair space.
2. Mechanism logic verbatim from `xdomain_dataflow_clean/df_patch.zag`
   (sha256 b6f38ece...). Only the driver is new.
3. `df_set_factrel` simulates the learner's procedure registry (same
   as H3 original).
4. The base sum trial branch required the tag-8 combination-context
   scaffold (precedent: xio_general, C269). It teaches no facts.
5. Level 1 (exact reuse) only. Expected-answer verification.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/xdomain_h3_arith/`:
- `PREREG.md` (frozen 4760d5c9e, before implementation)
- `NAMECHECK.md` (Step 0 guard, assembly record)
- `REPORT.md` (this file)
- `h3a_driver.zag` (behavior implementations only)
- `h3a_full.zag`, `h3a_full_nodf.zag` (assembled inputs)
- `h3a_bin`, `h3a_nodf_bin` (pinned znc, exit 0)
- `h3a_run1.txt`, `h3a_run2.txt`, `h3a_run3.txt` (3/3 byte-identical)
- `h3a_nodf_run1.txt` (NO-DF control)
- `h3a_compile.txt`, `h3a_compile_nodf.txt`

Pure Zag. Safebin PATH. `which python3 python` empty throughout.
Zero em/en dashes (byte-verified). Paper untouched. Frozen source
read-only. 0 modes, 0 bridges, 0 handlers. Local commit only, nothing
pushed.
