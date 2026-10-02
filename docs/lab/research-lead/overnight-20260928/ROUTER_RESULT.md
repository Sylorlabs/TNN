# Router Result: H-ROUTER SURVIVES

**Date:** 2026-09-29
**Prereg:** PREREG_ROUTER.md (commit d6e4eb485, frozen before implementation)
**Implementation:** route_learn.zag (new file, pure Zag, no Python)
**Raw output:** ROUTER_RAW_OUTPUT.txt (byte-identical across 3 runs,
md5 ee7f050c2975050a89afba0b4c07d6d2)
**Verdict:** H-ROUTER SURVIVES (9/9 sub-checks, 5/5 kill bars)

## What Was Built

`route_learn.zag`: the dual-store continuing learner with the explicit
P/C/Q router replaced by a **structure-inferred router**. Each input
line carries no type label. The router computes the route per item from
structural predicates over format markers (`>`, `;`, `,`) and field
content (comma-free string vs int-tuple), emits a white-box trace
`ROUTE [line] -> TARGET (reason)`, and withholds on ambiguity.

Route codes: PROC_LEARN (2+ `str>str` segments), CAUS_LEARN
(2+ `iii>ii` segments), PROC_QUERY (single bare string), CAUS_QUERY
(single 3-int tuple), WITHHOLD (everything else).

Mechanism code (procedure store + 1055-program discovery, causal
store + induction) is copied verbatim from the committed
`integ_learn.zag`; only the router, handlers, and `main()` are new.

## Kill Bar Verdicts

| Bar | Sub-checks | Result |
|-----|-----------|--------|
| K-R1 (procedure learning routes + works) | K-R1a reverse `hello`->`olleh`; K-R1b broadcast-last `hello`->`ooooo` at a distinct slot; K-R1c slot 0 intact after L3 | PASS |
| K-R2 (causal learning routes + works) | K-R2a `(hot,low,pressurize)`->low; K-R2b `(cold,low,pressurize)`->high | PASS |
| K-R3 (queries route + work) | K-R3a `hello`->PROC_QUERY, both slots reported (`olleh`, `ooooo`); K-R3b/c `1,0,0` and `0,0,0`->CAUS_QUERY with correct predictions | PASS |
| K-R4 (ambiguity withholds) | `ab>ba`, `0,0,0>0,1`, `hello;world`, empty line all WITHHOLD with reasons; zero misroutes | PASS |
| K-R5 (no regression) | Committed `integ_learn.zag` recompiled from source: 5/5, H-INTEG SURVIVES | PASS |

**Result: 5/5 kill bars PASS. H-ROUTER SURVIVES.**

## Key Traces (from raw output)

- `ROUTE [abc>cba;xy>yx] -> PROC_LEARN (2+ segs, str>str)`
- `ROUTE [0,0,0>0,1;...] -> CAUS_LEARN (2+ segs, iii>ii)`
- `ROUTE [hello] -> PROC_QUERY (single bare string)` then
  `QPROC slot 0 [hello] -> [olleh]` and `QPROC slot 1 [hello] -> [ooooo]`
- `ROUTE [1,0,0] -> CAUS_QUERY (single 3-int tuple)`
- `ROUTE [ab>ba] -> WITHHOLD (single pair/episode: learning needs 2+ segs)`
- `ROUTE [hello;world] -> WITHHOLD (mixed or malformed segments)`
- `ROUTE [] -> WITHHOLD (empty line)`

## Exploratory Probe E1 (non-kill, as predicted)

`ab>xy;cd>zw` routed PROC_LEARN on structure, then `pextract`
honestly failed (`LEARN FAIL: pextract failed on pair 0`). This
documents the intended separation: the router claims a *type*, the
mechanism owns *success*.

## Honest Limitations

1. **Predicates are authored.** The structural rules are written by the
   researcher; what is inferred is the per-item decision. This is
   structure-inferred routing, not meta-learned routing.
2. **Slot selection is out of scope.** A procedure query applies all
   stored procedures and reports each `(slot, output)`. Choosing the
   intended procedure is a separate retrieval problem (future work).
3. **The >= 2 threshold is an authored disambiguation rule.** A single
   pair is structurally identical to a malformed query; the router
   withholds. One-shot procedure learning from a single pair is
   therefore unreachable through this router.
4. **Format markers are assumed.** The input language uses `>`, `;`,
   `,` as structural markers. These are format, not type labels, but
   a fully marker-free stream would need a further inference step.
5. **Simplified stores inherited from v1.** Same simplifications as
   INTEGRATION_RESULT.md (single-condition causal rules, no bridge).

## What This Proves

Task-type routing can be computed from input structure with no label
supplied, every decision inspectable, ambiguity withheld, and the
original labeled capability fully preserved.

## What This Does NOT Prove

- That routing rules can be learned (they are authored here).
- That procedure intent can be inferred (slot selection is explicit
  reporting, not inference).
- Any L3 claim. Classification: **bounded L2 infrastructure**.
  No representational invention is involved.

## Classification

**Bounded L2 integration infrastructure.** Removes the explicit task
label while preserving all v1 capabilities. One step closer to the
continuing learner's "no task label supplied to cognition"
requirement; the remaining gap is learned (not authored) routing
rules and procedure-intent retrieval.
