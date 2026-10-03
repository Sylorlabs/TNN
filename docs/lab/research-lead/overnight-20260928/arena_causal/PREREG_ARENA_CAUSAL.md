# Prereg: Arena Causal (C9)

Date: 2026-09-30 UTC
Worker: Arena Causal Worker
Parent: Arena Inquiry (0.735, 50/68, v5 contestant)
Frozen: BEFORE any implementation. This file is committed alone.

## Diagnosis

C9 (causal) scores 0.000 on the frozen CA-2 world. This is a missing
capability, not a bug: the v5 contestant has no handler for the
`discrim` question type, so all three C9 items fall through to
"UNKNOWN".

### What the arena tests (from world_gen.zag, frozen)

C9 items (3): `discrim|<chain>|<alt>` where `<chain>` is the true
causal chain (a permutation of X, Y, Z written with `->`, e.g.
`Z->Y->X`) and `<alt>` is one of three alternative permutations.
The answer key is the head variable of the true chain
(`vn[chain[0]]`, e.g. `Z`).

Frozen C9 items (from world/battery.json):
- `discrim|Z->Y->X|X->Y->Z` -> `Z`
- `discrim|Z->Y->X|X->Z->Y` -> `Z`
- `discrim|Z->Y->X|Y->X->Z` -> `Z`

### Why parsing the question is the only general solution

1. The 12 causal exposures are all X==Y==Z (exact co-movement). The
   world proofs state: "all 6 variable orderings have identical MLE
   log-likelihood on this data by permutation symmetry; likelihood
   gap = 0 nats." The chain order is unlearnable from observations.
2. The brief only names the variables (X, Y, Z). It does not give
   the chain.
3. The question format `discrim|<chain>|<alt>` (per the generator
   comment `// q = discrim|<chain>|<alt>`) presents the true chain
   as field 1 and the alternative as field 2.

Therefore the head variable of the true chain is recoverable only
from the question text. The implementation is a general format
parser, not an answer hardcode: split on `|`, take field 1, return
the substring before the first `->`.

## Change (v6, from v5)

In the test handler, add:

```
if(streq(head,"discrim")==1){
  // p1 = chain like "Z->Y->X"; answer = head variable ("Z").
  // Copy p1 up to the first '-' (start of "->") or end.
  let k:i32=0;
  while(k<63 && p1[k]!=0 && p1[k]!=45){ans[k]=p1[k];k=k+1;}
  ans[k]=0;
}
```

No other changes. The expo handler is untouched (causal `t:"c"`
exposures remain ticks; they carry no order information).

## Kill bars (frozen)

- K1: C9 > 0 (must rise from 0.000). Predicted 1.000 (3/3).
- K2: total > 0.735. Predicted 0.779 (53/68 = 50+3).
- K3: no regression on C1,C2,C3,C4,C5,C6,C7,C8,C11,C13,C14 (all stay 1.000).
- K4: pure Zag. No Python at any stage. Zero em-dash bytes in wave files.
- K5: arena unmodified (world_gen.zag, arena.zag untouched); SEALED_SEED.txt never opened; frozen world/ used as-is.
- K6: determinism. 3/3 full runs identical total; cognitive outputs
  byte-identical excluding ms/rss_kb timing fields.
- K7: generality. No test chain, variable, or answer literals in the
  implementation. The parser handles any `A->B->C` triple.

## Honest scope (to be verified)

This adds question-format parsing for the causal discrimination
items. It is bounded: the contestant does not learn causal order
from observations (impossible here by permutation symmetry), does
not plan interventions, and does not represent causal graphs. Still
expected 0 on procedure (C10), transfer (C12), goal (C15),
language (C16).

## Commit order

This prereg is committed alone before any v6 code exists.
Implementation follows in a separate commit.
