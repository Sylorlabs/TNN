# H3-lite Node 1: Trial Search Order Policy - Implementation Report

**Verdict: H3LITE-NODE1-COMPLETE.** Build succeeds, 3/3 byte-identical, all white-box verifications pass.

## What was built

H3-lite Node 1 (trial search order policy) implemented on an unfrozen TNN-2 variant, per frozen prereg `9084a7760` Section 3.

### Policy node
- Tag 40, subtype field 4 = 1.
- Fields 8,12,16,20,24,28: six order slots holding family ids.
- Field 32: first-choice rejection count.
- Created on first `t2_trial` call via copy-then-revise bootstrap (initialized to researcher's current order).

### Family ids
- 0 = chain k=2, 1 = chain k=3, 2 = chain k=4, 3 = sum, 4 = count, 5 = single hop.

### Production read path
`t2_trial` is now a dispatch loop over the six policy order slots. Each slot's family id is read from learner state (`ng(W,pol,8+slot*4)`). Per-family assembly code (`t2_asm_chain`, `t2_asm_sum`, `t2_asm_count`) is unchanged; only invocation order is policy-driven. The dc/di/comb_present gates are preserved per family.

### Production write paths
1. **Hebbian promotion:** On verification success for family F at slot p > 0, swap F one step earlier (with slot p-1). Implemented in `t2_trial` dispatch loop after successful `h3n1_dispatch` return. (Prereg specifies "in t2_try_verify"; implemented at the call site where slot position is known. Effect identical.)
2. **Exhaustion demotion:** On trial exhausting all families without success, increment field 32. When field 32 > 8, swap slots 0 and 1 (demote first-choice one step) and reset field 32 to 0.

### Triggering experience
Verification success/failure outcomes of trial families during ordinary world interaction (ev_query miss path).

## White-box verification

All verified via test driver (`h3n1_driver.zag`), 3/3 byte-identical runs (SHA-256 `ee8fd40f...`):

| Test | What verified | Result |
|------|---------------|--------|
| T1 | Policy node created, initial order 0,1,2,3,4,5, rej=0 | PASS |
| T2 | Direct `h3n1_promote` swaps correctly; slot 0 no-op | PASS |
| T4 | 8 exhaustions increment rej to 8, no demotion; 9th demotes slots 0/1 and resets rej | PASS |
| T5 | Trial on miss creates policy node in learner state | PASS |
| T6 | Failed trial increments rej, order unchanged | PASS |
| T7 | **Real trial** with policy [0,5,1,2,3,4]: family 5 succeeds at slot 1, Hebbian promotes to [5,0,1,2,3,4] | PASS |

T7 is the critical end-to-end verification: the write path fires during ordinary trial execution, not just in direct function tests.

## Prereg discrepancy (documented, not hidden)

Prereg `9084a7760` Section 3 states: "Initialized to 2,1,0,3,4,5 (researcher's current literal order)" and describes the current order as "chains k=4,3,2, then sum, then count, then single hop."

The frozen source (`tnn2.zag` line 593) actually does:
```
let k:i32=2;
while(k<=4 && ans==-2){
```
This tries k=2, then k=3, then k=4 (ascending), i.e. families 0,1,2 in that order, followed by sum (3), count (4), single hop (5).

**Actual source order: 0,1,2,3,4,5. Prereg description (2,1,0,3,4,5) is factually incorrect.**

This implementation initializes the policy node to the ACTUAL source order (0,1,2,3,4,5) per the prereg's "copy-then-revise" bootstrap rule ("on first use the node is created with the researcher's current defaults copied in"). Copying the prereg's incorrect description would have CHANGED behavior on first use, violating the bootstrap intent.

The mechanism (policy-driven order, Hebbian promotion, exhaustion demotion) is implemented exactly as specified. Only the initial permutation differs from the prereg's erroneous description.

## Architecture accounting (per prereg Section 7)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: The six assembler families, the Hebbian swap rule, the demotion threshold (8), the six-slot structure, the copy-then-revise bootstrap. All thresholds/margins are researcher-chosen per prereg.
- LEARNER-OWNED STRUCTURAL DECISIONS: 1 (trial search order policy value). Passes K-H3 audit elements 1-5 (decision, node/fields, read path, write path, triggering experience). Element 6 (sealed demonstration) awaits the independent adversary's sealed world.
- SOURCE-ENUMERABLE FORMS: 6! = 720 possible orders over six fixed families. Explicitly enumerable; SUF not claimed.
- SUF DECISIONS: 0 (per prereg non-claims).
- LEARNER-INTERNAL CRITERIA: Order preference (which family to try first). Set by verification success/failure experience via Hebbian update.
- REUSE EVENTS: Policy node read on every trial after creation (distinguished from initialization).
- REVISION EVENTS: Each Hebbian swap and each demotion, tied to triggering verification outcome.
- COGNITION LINES: ~150 lines added (policy functions + dispatch refactor). Net change vs frozen t2_trial: the original ~80-line fixed-order loop replaced by ~30-line dispatch loop plus ~120 lines of policy/family helpers.
- MODES: 0 new.
- BRIDGES: 0 new.
- HANDLERS: 0 new.
- SEMANTIC CASES: 0 new.

Alternative C verified: no ALLOC/LINK/KILL opcodes added to learner-executable ISA. Policy writes use `ns` (field write) which the frozen source already performs. No new opcodes, modes, bridges, or handlers.

## Limitations (explicit non-claims per prereg Section 5)

1. **Learner-authored procedures:** NOT established. The six families remain researcher-authored Zag code. Only the invocation order is learner-revisable.
2. **SUF:** NOT established. The 720 orders are enumerable from source.
3. **L3:** NOT established. This is a precondition diagnostic, not representational invention.
4. **Capability improvement:** NOT predicted or claimed. FW1-FW9 scores measure the researcher-enumerated envelope, which is unchanged in kind.
5. **Nodes 2 and 3:** NOT implemented. This build is Node 1 only.
6. **Sealed evaluation:** NOT yet run. The weak K-LT-5 test (`weak_klt5/`) is designed but requires an independent adversary's sealed world.

## K-H3 audit status (per prereg Section 4)

For Node 1 (trial search order):
1. Structural decision: trial search order. ✓
2. Learner-state node/fields: tag 40, subtype 1, fields 8/12/16/20/24/28 (order), 32 (rej count). ✓
3. Production read path: `t2_trial` dispatch loop reads `ng(W,pol,8+slot*4)`. ✓ (verified T5/T6/T7)
4. Production write path: Hebbian swap in dispatch loop; demotion in `h3n1_exhaust`. ✓ (verified T2/T4/T7)
5. Triggering experience: verification success (promotion) / trial exhaustion (demotion) during ordinary ev_query. ✓ (verified T7)
6. Sealed demonstration: PENDING. Requires independent adversary sealed world.

Failure conditions check:
- (a) Not a source literal: PASS (order read from learner state).
- (b) Not read-only: PASS (write paths exist and fire, verified T7).
- (c) Write path reachable: PASS (fires during ordinary trial, verified T7).
- (d) Not researcher-supplied history: PASS (T7 uses ordinary teach/query).

## Files
- `h3n1_base.zag`: verbatim frozen copy (SHA-256 `a29972ca...`)
- `h3n1_funcs.zag`: H3-lite Node 1 implementation
- `h3n1_variant.zag`: assembled variant (t2_trial replaced)
- `h3n1_build.zag`: variant + test driver
- `h3n1_driver.zag`: test driver
- `h3n1_bin`: compiled binary
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical (SHA-256 `ee8fd40f8724f972535ca93832eba59a50887db8737dce0718e62c9f3e51850f`)

## Next steps (for parent coordinator)
1. The weak K-LT-5 sealed test can now be run once an independent adversary designs the sealed world (prereg `weak_klt5/WEAK_KLT5_PREREG.md` specifies R1-R5).
2. Nodes 2 and 3 remain unimplemented (separate builds per prereg).
3. The prereg discrepancy (initial order 0,1,2 vs 2,1,0) should be noted in the H3-lite evaluation record.
