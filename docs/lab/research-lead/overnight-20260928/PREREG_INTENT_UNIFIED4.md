# PREREG H-INTENT-UNIFIED4: Repair of H-INTENT-UNIFIED3 Red-Team Downgrades

**Date:** 2026-09-29
**Status:** FROZEN (before implementation)
**Parent:** H-INTENT-UNIFIED3 (SURVIVES 8/8, DOWNGRADED by red team)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python.

## Background

H-INTENT-UNIFIED3 red team (IU3-ADV) DOWNGRADED (not killed). Two attacks succeeded:

1. **X-IU3-1a' (cap-times-verbatim composition):** The verbatim-conflict guard is blind to out-of-cap collisions. Guard precondition (both top-two em=1) is a property of the intent RECORD, not the training data. Fixture: proc trained on 17 reverse pairs with colliding input "xab>bax" as the 17th (unrecorded); bridge trained on 5 pairs with "xab>xxx" (recorded). Query "xab" yields kind=1, answer "xxx", zero VERBATIM-CONFLICT lines. Control proves proc genuinely learned "xab>bax". The training data genuinely contradicts itself, but em=0 on proc side (truncation artifact), guard never fires.

2. **X-IU3-2 (distinct-value table overflow):** R3 sized s1idx/s2idx by npairs but left adjacent distinct-value table `dvals=z_alloc(128)` fixed. Fixture: 129 pairs with 129 distinct first-byte values, direct discovery failing. Result: panic "slice index out of bounds", exit 1. The repair covered the reported vector, not the buffer class.

X-IU3-1b (agreement), X-IU3-3 (reproduction), X-IU3-4 (audit) all passed.

## Repairs (frozen)

### R4: Cap-robust conflict detection (X-IU3-1a' repair)

**Mechanism change 1:** The intent record field at o+8 currently stores `cap = min(npairs, 16)`. Change it to store the TRUE npairs (uncapped). In `intent_exact_match`, use `min(n, 16)` as the loop bound over the recorded list. This gives a persistent truncated-evidence flag: `truncated = (get32(W, rec+8) > 16)`. No layout change required; the 16-byte record format is preserved.

Files: `intent_record_proc`, `intent_record_br`, `intent_exact_match` in both `intent_learn.zag` and `unified_learn.zag`.

**Mechanism change 2:** In `intent_winner`, after the existing verbatim-conflict guard, add a truncated-conflict guard. Condition: top candidate has em=1 AND second candidate has em=0 AND second's record is truncated (true npairs > 16); OR the symmetric case (second has em=1, top has em=0 and top's record truncated). Action: compute both answers via proc_apply/bridge_apply dispatch by kind; if answers differ, emit "INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer; WITHHOLD AMBIGUOUS" and return kind=-2. If answers agree, fall through to existing rules (no over-broad withholding).

This directly implements the red team's recommended R4: "record a truncated-evidence flag per record and withhold (or emit an explicit conflict-possible diagnostic) when a verbatim candidate on one side meets a truncated record on the other whose learned procedure answers differently."

### R5: Distinct-value buffer sizing + WORK/PAIRBASE audit (X-IU3-2 repair)

**Mechanism change 3:** In `bridge_learn`, change `dvals:[]u8=z_alloc(128)` to `z_alloc(256)`. Principled sizing: a byte holds 256 distinct values; ndv counts distinct byte values at a position, so 256 is the exact upper bound. No new constant; derived from the type.

Files: `unified_learn.zag:503`, `intent_learn.zag:468`.

**Mechanism change 4:** Audit found a further latent capacity boundary: `bridge_learn` lays out `seqbase=work`, `statbase=work+npairs*64`, `lenbase=statbase+npairs*4`, requiring `work+npairs*72` bytes. With WORK=2048 and PAIRBASE=8192, npairs >= 86 causes the WORK area to overlap PAIRBASE (silent corruption, not a panic). Add an honest guard at the start of `bridge_learn`: if `work + npairs*72 > pairbase`, emit "bridge: WORK area too small for npairs=N; honest failure" and return -1. This converts silent corruption into an explicit failure. The 129-pair X-IU3-2 fixture will then fail honestly (not panic, not corrupt) unless the caller provides a larger WORK area.

## Frozen kill bars

- **K-IU4-1 (truncated-conflict guard):** X-IU3-1a' fixture. Train proc D on 17 reverse pairs with "xab>bax" as 17th; train bridge B on "xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee". Query "xab". PASS iff kind=-2 (WITHHOLD) AND output contains "TRUNCATED-CONFLICT-POSSIBLE". (H-IU3 behavior: kind=1, answer "xxx", zero diagnostics.)

- **K-IU4-2 (no panic on 129 pairs):** X-IU3-2 fixture. 129 pairs with 129 distinct first-byte values at position 0, direct discovery failing. PASS iff exit code 0 (no panic). Note: the WORK/PAIRBASE guard may cause an honest bridge_learn failure (return -1) for npairs=129 with the default WORK area; this is PASS (honest failure, not panic, not silent corruption). The bar is "no panic", not "bridge learns successfully".

- **K-IU4-3 (regression):** All K-IU3-1 through K-IU3-5 still PASS:
  - K-IU3-1: X-IU2-1 in-cap fixture → kind -2 WITHHOLD with VERBATIM-CONFLICT.
  - K-IU3-2: 17-pair fixture → WARN emitted; record stores true npairs=17 (o+8=17, loop bound 16).
  - K-IU3-3: 18-pair split → no panic, rc=1000.
  - K-IU3-4: 10/10 standalone intent battery; 20/20 unified scenarios; zero FAILs.
  - K-IU3-5: 3/3 byte-identical runs.

- **K-IU4-4 (determinism):** 3/3 runs byte-identical (cmp-verified) for the full test binary.

## Classification

Bounded L2 integration infrastructure. Not L3. The repairs make conflict detection robust to the record cap and make buffer sizing principled; they do not invent new representations.

## Governance

- Prereg frozen BEFORE any implementation. Commit order verified via merge-base.
- Pure Zag. No Python at any stage.
- Both `intent_learn.zag` and `unified_learn.zag` receive identical repairs (X-IU4 faithfulness invariant preserved).
- No em dashes in loop documentation.
