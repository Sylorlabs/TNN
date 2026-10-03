# SEALED_EVAL_C9.md: C9 Causal Contestant Sealed Evaluation

Wave: wave-20261002-0521pdt | Lane: ARENA | Date: 2026-10-02
Prereg: PREREG_CAUSAL.md (frozen alone as fdaa5c0a4, wave-20261002-0221pdt)
Mechanism: causal_contestant.zag (two-stage interventional protocol,
HI=0.75, integer arithmetic, zero chain-string literals in logic)

## Verdict: CAUSAL-PASS (K1 through K7 all PASS)

## Transparent protocol deviation (disclosed, kill bars unchanged)

The frozen prereg named fixrun1 as the eval substrate and the frozen
arena scorer as the instrument. Both are unusable, for reasons
discovered during this wave's execution:

1. fixrun1 is unscorable by the frozen scorer: `arena score`
   aborts with `DIVERGENCE: q mismatch` on C9 item27. This is an
   independent confirmation of defect D5 (fixed this wave in
   world_gen_c9d5fix.zag; see C9D5FIX_EVAL.md): fixrun1's
   turns.jsonl and battery.json disagree on item27's candidate
   order, and the scorer's cross-check rejects the world.
2. The frozen scorer cannot score ANY 291-turn world: its
   turn-indexed arrays are fixed at 256 entries (arena.zag lines
   207-210, 260-265) and it panics with `slice index out of
   bounds` on the 291-turn fixed-generator worlds. The frozen
   scorer was built for 131-turn worlds.

The eval therefore ran on fixrun2 (this wave's GEN-PASS D5-fixed
world, same frozen seed, battery path byte-identical to fixrun1)
scored by arena_512.zag: a copy of the frozen arena.zag differing
ONLY in the ten turn-indexed allocation sizes (256 -> 512; strides
unchanged; verified by diff). arena_512 was cross-validated against
the frozen scorer on the 131-turn 2321pdt sealed world with the
INQ run1 replies: results.json BYTE-IDENTICAL, report output
identical. All kill bars K1-K7 are applied exactly as frozen; only
the substrate and the (provably equivalent) scoring capacity
changed, both forced by post-freeze discoveries, both disclosed
here.

## Builds (pure Zag, safebin, pinned znc)

- causal_contestant.zag -> bin/causal_contestant: BUILD-PASS.
  Source sha256:
  d5ded24a53bfeb363899a77e8294d24fe43f591a3237c4c0789d758112ad0ad1
  (provenance: 0221pdt lane working tree, written under the frozen
  PREREG_CAUSAL; copied byte-identical into this lane).
  Binary sha256:
  f485de4b7f7f11c8894edc5b106fdbc14acdf847438201e8b2666fbd5c9b4738
- v6_base.zag (refreeze devint1_contestant_v6.zag) -> bin/v6_base:
  BUILD-PASS. Source sha256
  c6dbc20cf447dce7ab506576b42557a0542065e170bee6516558ecfb435d1e89
  (matches the prereg's recorded hash). Binary sha256
  5d2be6acf4d98ef2118e2e1f2e52d87d38a9f848cb83e04d8b252199ce966f15
  (byte-identical to the ARENA5/ARENA-GEN v6 binary: independent
  confirmation of a correct build).
- arena.zag (frozen) -> bin/arena: BUILD-PASS. Binary sha256
  3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076
  (matches the refreeze record).
- arena_512.zag -> bin/arena_512: BUILD-PASS. Binary sha256
  ea9adbfc4f9e1b0b2e650016acd4ffb466d14e7c5b8951912f32501de0ac896a.

## Results

### v6 baseline on fixrun2 (K2 reference)
TOTAL 68, 0.794 (54/68). Per capability: C1-C7 1.000, C8 0.000,
C9 0.000, C10 1.000, C11 1.000, C12 0.000, C13 1.000, C14 1.000,
C15 0.000, C16 1.000. The v6 profile on the fixed world matches
its frozen-world profile exactly (0.794, zeros on C8/C9/C12/C15).

### Causal candidate on fixrun2 (3 runs)
TOTAL 68, 0.838 (57/68) on all three runs. Per capability:
identical to the v6 baseline on every capability except C9, which
moves 0.000 -> 1.000 (3/3 items, replies "X->Z->Y" x3, the true
chain, on every run).

### K1 (C9 capability): PASS
3/3 C9 items correct via sealed eval (arena_512). Replies are the
full true-chain string matching a listed candidate; the mechanism
never uses candidate position.

### K2 (no regression): PASS
Per-capability diff causal vs v6 on fixrun2: the single changed
line is `9 3 0.000` -> `9 3 1.000`. All other 15 capabilities are
identical (C8/C12/C15 remain 0.000 for both; every passing
capability still passes).

### K3 (determinism): PASS
3/3 sealed runs produce byte-identical stripped reply streams
(ms, rss_kb excluded):
eeee5acd2961960740c6f78688072e497374ecc05031599c4114a3aefb2934fc
(x3). Raw streams differ only in the volatile ms/rss_kb fields.

### K4 (ablation): PASS
causal_contestant_abl.zag (the two do/do_out stat-accumulation
blocks neutralized: `if(0==1)` guards; discrim protocol
untouched): C9 = 0/3 (replies "UNKNOWN" x3), TOTAL 68, 0.794,
identical to the v6 baseline. With no accumulated statistics the
protocol's nX>0 && nZ>0 guard leaves the chain unidentified and
the reply stays UNKNOWN. The C9 gain is caused by the causal
section, not the base.

### K5 (no order exploit): PASS
Swap world (c1/c2 exchanged in all 3 discrim questions, battery
and turns kept consistent): the candidate replies "X->Z->Y" x3
(unchanged), C9 = 3/3, TOTAL 68, 0.838. The mechanism infers the
chain from the intervention statistics only; candidate position
is never consulted (the reply is built from variable indices and
matched against the listed candidates).

### K6 (architecture): PASS
Diff vs the v6 base: 82 lines added (66 non-comment non-blank),
1 line replaced (the expo fallthrough condition now also excludes
"do"/"do_out" so intervention turns are not double-ticked).
Zero new modes, bridges, handlers, or hardcoded semantic cases.
The mechanism is generic accumulation (six counters in W cells
15000..15020 plus pending do state) and integer cross-multiplied
comparison against the frozen HI=0.75 threshold. Zero
chain-string literals in executable logic (the 3 grep hits are
code comments; the reply string is built from variable indices
88/89/90). Cognition lines added: 66.

### K7 (no L3 claim): PASS (by construction)
This is L1/L2 mechanism work: parameter filling (intervention
statistics) and structural inference from a fixed,
researcher-specified two-stage protocol. No representational
invention is claimed; the protocol, threshold, and candidate
matching were specified in the frozen prereg.

## Toolchain note (new AGENTS.md lesson, 2026-10-02)

A second znc miscompile was reported today (name/layout-dependent
_zag_print misbehavior; workaround: prebuilt single output buffer
plus stdout byte verification). Mitigation applied here: all
lane binaries emit replies through a single prebuilt output
buffer, and every binary's stdout bytes were verified (3/3
byte-identical stripped streams for the candidate; byte-identical
results.json for the scorer cross-validation; byte-identical
world files across 3 generation runs). No dynamic-content
_zag_print pattern is present in the new code.

## Scope

C9 moves 0.000 -> 1.000 on the D5-fixed world family via genuine
intervention-driven inference (not candidate-order parsing: K5).
The frozen arena C9 battery remains a sealed zero (ARENA2 negative
finding stands for the original battery). No TNN-beats-LLM claim;
no generality or L3 claim. The contestant is a per-capability
candidate on the v6 base, not the integrated continuing learner.

## Queued next

- Bare-prompt abstention test (frozen PREREG_ABSTENTION).
- C8/C12 surface-transfer prereg on fixrun2.
