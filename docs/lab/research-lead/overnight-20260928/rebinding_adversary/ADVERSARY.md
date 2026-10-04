# Rebinding Adversary Report

## Verdict: REBIND-ADV-COMPLETE

All seven adversarial worlds: GRACEFUL. Zero crashes, zero hangs, zero
false accepts on unmasked queries. Three limitations documented
(masked-query arbitrariness, scale cost, order-dependent binding).

## Target

Structural rebinding mechanism from `91585087c` (REBINDING-COMPLETE
PASS). Unfrozen variant only. The mechanism: on a miss, scan promoted
MAPs in node-id order; for each chain-shaped MAP (via `rb_chain_plen`),
re-instantiate the chain on B's paths of matching length using B's own
literals; verify by execution (`t2_try_verify`); first verified rebound
wins and is promoted; fallback to trial if none verify.

Key design property under attack: the rebound NEVER executes the MAP's
own graph in B. It extracts only the shape parameter (plen) and rebuilds
a fresh chain from B's literals. The MAP's internal wiring, literals, and
stored answer do not propagate to B.

## Worlds and Measurements (3/3 byte-identical per world)

Worlds W1-W4b built in wave 1; W5-W7 added in wave 2 (retry). All seven
ran in one binary, 3/3 byte-identical outputs.

### W1: Non-chain topology -- GRACEFUL

A: COUNT MAP + SUM MAP (directly constructed and promoted) + chain MAPs
(decoy plen-3, main plen-5 via trial).

- `rb_chain_plen(count)=-1`, `rb_chain_plen(sum)=-1`. Both correctly
  rejected. No crash. The 103 (INC) cells break the 102/101 alternation;
  the step limit and tag checks hold.
- B1 (chain query, expects 114): ans=114, ok=1, tried=4 rejected=3.
  Count/sum MAPs skipped; chain MAPs used normally.
- B2 (count query, expects 3): ans=3, ok=1, rebound tried=1 rejected=1,
  trial tried=3 rejected=2. Chain rebounds built on B2's paths yielded
  endpoints != 3, correctly rejected by execution verification.
  Fallback to trial found the count graph.

The mechanism correctly falls back to trial on non-chain structure. No
false verification of a wrong shape.

### W2: Deceptive MAP -- GRACEFUL (robust)

A: chain graph with corrupted guard literal (901 -> 99999), promoted as
MAP. `rb_chain_plen` does not inspect literals; returned plen=5, no
crash.

B (chain query, expects 934): ans=934, ok=1, tried=1 rejected=0.

The corruption did not propagate. The rebound is rebuilt from B's own
literals via `t2_asm_chain`; the MAP's wrong literal is never copied.
Execution verification on B's data is the arbiter, not the MAP's
internals. The plen-only extraction is inherently robust to MAP-internal
deception.

### W3: Scale attack -- GRACEFUL (correct but expensive)

A: 19 wrong plen-3 MAPs (promoted first, lower node ids) + 1 correct
plen-5 MAP (promoted last, highest node id).

B (plen-5 query, expects 1114, with length-3 distractors):
ans=1114, ok=1, tried=91 rejected=90.

The mechanism scanned all 19 wrong MAPs (each tried on B's length-3
paths, all correctly rejected by execution verification) before reaching
the correct plen-5 MAP. Cost is O(MAPs x paths): 91 verifications for 20
MAPs, linear not exponential. Answer correct.

Performance note: the B-CHAIN query took ~5 minutes wall-clock. The
91 verifications each allocate chain scratch via `t2_asm_chain`; under a
populated workspace each allocation pressures the evictor. Correctness
is unaffected; latency scales with MAP count x path count x eviction
cost. This is a performance limitation, not a correctness failure.

### W4: Poisoned MAP (wrong stored answer) -- GRACEFUL (robust)

A: chain MAP manually promoted with ans=99999 (wrong; true=1214).
`rb_chain_plen`=5.

B (unmasked chain query, expects 1314): ans=1314, ok=1, tried=1
rejected=0. The stored wrong answer (99999) was ignored. The rebound
uses plen only; the answer comes from executing the freshly built chain
on B's data and verifying v==expected. The MAP's answer field is not
trusted.

### W4b: Masked query -- GRACEFUL but ARBITRARY (limitation)

A: plen-4 chain MAP. B: masked query (flags=1, no expected) with two
length-5 paths (P1 taught first).

Result: ans=413 (a length-4 PREFIX endpoint), not 414 or 424.

On masked queries `t2_try_verify` accepts any successful execution
(v != -2, v != -999999). The rebound matched plen=4 against B's length-4
prefix paths and accepted the first-executing one (BFS gather order).
The mechanism cannot prefer "complete" paths over prefixes, nor P1 over
P2, when there is no expected to verify against. This is inherent to
first-verified-wins on masked queries, not a crash or false accept
(there is no expected to be false against). Documented as a limitation:
masked-query rebinding is order-dependent and prefix-accepting.

### W5: Negative transfer -- GRACEFUL (correct, measurable tax)

A: 10 chain MAPs (plen 2x3, 3x3, 4x3, 5x1). B: count query (expects 3).
Fresh control: same count query, no A phase.

- Treatment: rebound tried=9 rejected=9, then trial tried=3 rejected=2.
  Total 12 verifications. ans=3, ok=1.
- Control: rebound tried=0 rejected=0, trial tried=3 rejected=2.
  Total 3 verifications. ans=3, ok=1.

The misleading old structure costs +9 wasted verifications (4x the
control cost) but correctness is fully preserved: every wrong-shape
rebound was rejected by execution verification and the trial fallback
found the count graph. Negative transfer is a latency tax, not a
correctness failure, and it scales linearly in MAPs x matching paths.

### W6: Ambiguous selection -- GRACEFUL but ORDER-DEPENDENT (limitation)

A: one plen-5 chain MAP. B: two plen-5 paths to the same endpoint 114
(decoy via 211, true via 111). Teach order swapped across variants.
Promoted MAP's DEP edges dumped to identify the bound path.

- W6A (decoy taught first): ans=114, tried=1 rejected=0. Bound facts:
  (101,1,211) (211,1,212) (212,1,213) (213,1,114). The DECOY path.
- W6B (true taught first): ans=114, tried=1 rejected=0. Bound facts:
  (101,1,111) (111,1,112) (112,1,113) (113,1,114). The TRUE path.

First-verified-wins is order-dependent: the mechanism binds whichever
length-matching path verifies first (BFS gather order follows teach
order) and cannot distinguish two hypotheses that both verify. The
answer is right in both variants (shared endpoint), but the learned
provenance commits to an arbitrary one. On unmasked queries with
distinct endpoints this is harmless (only the expected-matching path
verifies); on ambiguous worlds the choice is arbitrary. Documented as a
limitation: no hypothesis comparison, only first success.

### W7: Depth mismatch / partial applicability -- GRACEFUL

A: three plen-5 chain MAPs. B: true plen-4 chain (expects 113) plus a
length-5 decoy path (endpoint 214). Fresh control: same B, no A phase.

- Treatment: rebound tried=3 rejected=3 (the three plen-5 MAPs matched
  only the decoy path; endpoint 214 != 113, all rejected), then trial
  tried=3 rejected=2. Total 6 verifications. ans=113, ok=1.
- Control: rebound tried=0 rejected=0, trial tried=3 rejected=2.
  Total 3 verifications. ans=113, ok=1.

plen matching is all-or-nothing: a plen-5 shape is never partially
applied to a plen-4 problem, and a wrong-endpoint match is rejected by
verification rather than accepted. Tax +3 verifications (2x control).

## Summary Table

| world | ans correct | verifications | behavior |
|---|---|---|---|
| W1 B1 (chain) | 114=114 yes | 4 | non-chain MAPs skipped |
| W1 B2 (count) | 3=3 yes | 1+3=4 | chain rebounds rejected, trial fallback |
| W2 (deceptive) | 934=934 yes | 1 | corruption not propagated |
| W3 (scale 20) | 1114=1114 yes | 91 | linear scan, all wrong rejected |
| W4 (poison ans) | 1314=1314 yes | 1 | stored ans ignored |
| W4b (masked) | 413 (arbitrary) | 1 | first-executing prefix accepted |
| W5 (neg transfer) | 3=3 yes | 9+3=12 vs 3 | 4x tax, correct fallback |
| W6A (decoy first) | 114=114 yes | 1 | bound decoy path |
| W6B (true first) | 114=114 yes | 1 | bound true path |
| W7 (depth) | 113=113 yes | 3+3=6 vs 3 | 2x tax, all-or-nothing plen |

## Catastrophic vs Graceful

- Crash: none in any world (3/3 runs).
- Hang: none (W3 slow but completed).
- False accept on unmasked query: none. Every accepted rebound
  satisfied v==expected by execution.
- Wrong answer on unmasked query: none.
- Fallback to trial when rebinding inapplicable: correct (W1 B2, W5, W7).
- Later learning never poisoned: W5/W7 controls and treatments both
  answer correctly; the MAP store is append-only and MAP contents are
  never executed, only shape-extracted.

## Limitations (not failures)

1. Masked queries: first-executing path wins; order-dependent and
   prefix-accepting. No expected means no correctness arbiter.
2. Scale: verification count is O(MAPs x paths); wall-clock latency
   grows with allocation/eviction pressure. 20 MAPs -> 91 verifications
   -> ~5 min on this workload. Linear, not exponential, but expensive.
3. Ambiguous selection: with two verifying hypotheses the mechanism
   binds the first (teach/BFS order) with no comparison. Provenance is
   arbitrary even when the answer is right.

## Constraints honored

Unfrozen variant only; frozen source read-only (adv_base.zag is a
verbatim copy of rb_base.zag from 91585087c, SHA-256
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
adv_patch.zag is a verbatim copy of rb_patch.zag from 91585087c, verified
by diff). Pure Zag via pinned znc. Safebin PATH; `which python3 python`
returned nothing. Zero em/en dashes (byte-verified). Paper untouched.
No sealed worlds. Nothing pushed.

## Files

- NAMECHECK.md (Step 0 toolchain guard, scope, provenance)
- adv_base.zag (verbatim frozen copy from 91585087c)
- adv_patch.zag (verbatim rebinding mechanism from 91585087c)
- adv_driver.zag (seven adversarial worlds + MAP-dump helpers)
- adv_full.zag (assembled variant; base main excluded, driver main kept)
- adv_bin (compiled binary)
- adv_run1.txt, adv_run2.txt, adv_run3.txt (3/3 byte-identical)
- compile_err.txt (znc warnings only)
- ADVERSARY.md (this report)
