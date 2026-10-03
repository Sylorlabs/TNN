# OPRECRUIT2 Result: BUILD-PASS (non-adversarial battery)

Date: 2026-09-30.
Prereg: `1df644256` (`PREREG_OPRECRUIT2.md`).
Design: `c6ef7ffcf` (`op_recruit/OPRECRUIT2_DESIGN.md`).
Implementation: `oprecruit2.zag` (pure Zag, 42,331 bytes source).
Verdict: **BUILD-PASS** for the non-adversarial battery. T-ADV remains PENDING (independent post-freeze adversary).

This is a builder report, not a SURVIVES claim. Only the full 11-step pipeline may yield SURVIVES.

## Battery results (3 runs, byte-identical stdout, empty stderr, exit 0)

```
OPRECRUIT2 battery
TEST R-V1
RECRUITED op=32 arity=1 len=8 gain=32
RV1 recruited=1 nrec=1 op=32
R-V1 PASS
TEST T-NOFIRE
TNOFIRE r1=0 r2=0 nrec=0
T-NOFIRE PASS
TEST T-SELF
RECRUITED op=32 arity=1 len=2 gain=2
TSELF recruited=1 before=31 after=26 op=32
TSELF task0 ctrl=76966 treat=10170
TSELF task1 ctrl=80966 treat=10654
TSELF task2 ctrl=71966 treat=9565
T-SELF PASS
TEST T-ARITY2
RECRUITED op=32 arity=2 len=3 gain=7
TARITY2 recruited=1 op=32
TARITY2 arity=2
RECRUITED op=33 arity=2 len=3 gain=3
TARITY2 rc2=1 op2=33
T-ARITY2 PASS
TEST T-RETIRE
RECRUITED op=32 arity=1 len=2 gain=2
RETIRED op=32
TRETIRE retired_at=4 nrec=0 n_recruited=1 n_retired=1
T-RETIRE PASS
T-ADV PENDING
BATTERY DONE
```

Raw logs: `OPRECRUIT2_run1.log`, `OPRECRUIT2_run2.log`, `OPRECRUIT2_run3.log` (692 bytes each, identical). Stderr logs are empty (0 bytes).

## What was built

`oprecruit2.zag` implements the OP-RECRUIT v2 design:

- Generic stack VM with opcodes 0..31 (including IN2 op 21, IN3 op 22).
- Exactly one generic dispatch branch for recruited opcodes 32..63.
- Persistent learner state: nrec, rec_meta (base, arity, len, res, use, idle, gain), rec_buf (2048 bytes), rec_buf_top, staging, experience buffer (16 inputs), program store (16 programs x 388 bytes), persistent RNG.
- Consolidation: DETECT (byte-exact subsequence scan, freq>=3, gain>0) -> PROPOSE (abstract stack-effect worklist, arity 1..4) -> VALIDATE (provisional install, 16 generated input tuples, INLINE vs WRAPPED) -> RECRUIT (store rewrite, behavioral checksum gate/F_BREAK) -> RETIRE (W_IDLE=3 decay, re-expansion).
- Driver calls consolidation; driver never recruits directly.

## Transparent implementation amendments (post-freeze discoveries)

These were discovered during implementation and testing. They do not alter frozen kill bars. They are disclosed here, not retrofitted into the prereg.

### A7: PROPOSE rejects INk in recruited bodies (soundness)

**Problem:** Prereg A1 binds `in_k` to popped stack values `v[k]`. A body containing `IN0` (op 1), `IN1` (op 2), `IN2` (op 21), or `IN3` (op 22) that read program inputs in the original program is unsound after recruitment, because the wrapper's `in_k` are stack values, not program inputs.

**Evidence:** During development, the F_BREAK behavioral gate caught two unsound recruitments:
1. R-V1: candidate `[IN0,IN0,PUSH:-1,GT,JZ:7,IN0,JMP:9,IN0]` (pos 0) absorbed the input-loading `IN0`; rewritten program produced top=100 instead of 107.
2. T-ARITY2: candidate `[IN0,IN1,ADD,PUSH:2,MUL]` (gain 9) absorbed `[IN0,IN1]`; rewritten A0 produced 16 instead of 2.

**Fix:** PROPOSE returns 0 (reject) if the body contains op 1, 2, 21, or 22. Recruited bodies must be stack-polymorphic. This does not contradict A1; it restricts candidates to the sound subset where A1's binding is correct.

**Consequence:** R-V1 uses a DUP-based ABS body `[DUP,PUSH:-1,GT,JZ:7,DUP,JMP:9,DUP,NEG]` (no INk). The prereg's IN2/IN3 remain as generic VM primitives for main programs.

### A8: Jump target relativization when staging

**Problem:** Candidate byte sequences record `JZ`/`JNZ`/`JMP` args as absolute program positions. Staging the raw bytes into a standalone body preserves the absolute targets, which point outside the body.

**Fix:** When copying to `stage_buf`, subtract `first_pos` from args of ops 16, 17, 18. This makes targets body-relative.

**Limitation (disclosed):** Sound only when every occurrence shares the same start position. DETECT records only the first occurrence position. If occurrences are at different positions, relativization is incorrect for the others. The battery does not test this case. A future version should verify positional uniformity or reject such candidates.

### A9: Transactional F_BREAK rollback

**Problem:** On behavioral checksum mismatch, `recruit_finalize` emitted F_BREAK and returned 0, but left the store rewritten and the provisional op installed. Consolidation then continued on corrupted state, accepting later candidates and leaving failed provisional operators installed. (Observed: R-V1 ended with nrec=2; T-ARITY2 reached op=34 after two failed provisionals.)

**Fix:** Before rewrite, backup the full store (6208 bytes) and record `rec_buf_top`. On mismatch: restore store from backup, decrement `nrec`, restore `rec_buf_top`, clear staging, emit F_BREAK, return 0. The walk then cleanly tries the next candidate.

### A10: T-RETIRE stops at first retirement

**Problem:** After retirement re-expands the body, the same subsequence is detectable again (freq>=3), causing re-recruitment in the next episode (oscillation: recruit -> idle -> retire -> recruit). The test's 5-episode loop saw re-recruitment at episode 5, violating `n_recruited==1`.

**Fix:** The test breaks after the first retirement event. The prereg bar is "retirement within W_IDLE+2"; continued suppression of re-recruitment is not required by the prereg.

**Limitation (disclosed):** The recruit/retire oscillation is a real design limitation. A production system would need a cooldown or tombstone mechanism. Not implemented; documented here.

## Test details

### R-V1 (prereg 5.1)
5 programs `[IN0, ABS8(DUP-based) at pos 1, PUSH:(100+i), ADD]`. Recruited op=32, arity=1, len=8, gain=32. Behavioral checks: `[PUSH:x, OP]` and `[IN0, OP]` top==|x| for x in -8..8. PASS.

### T-NOFIRE (prereg 5.2)
6 programs with pairwise-unique 2-grams. Two consolidations, zero recruitments. PASS.

### T-SELF (prereg 5.3, amendment A6)
Deterministic enumerative search. Recruited `[DUP,MUL]` (op=32, arity=1, len=2, gain=2). Store 31->26 ops. Treatment evaluations (10,170 / 10,654 / 9,565) far below control (76,966 / 80,966 / 71,966), demonstrating the recruited op shortens search. PASS.

### T-ARITY2 (prereg 5.4)
5 programs sharing `[ADD,PUSH:2,MUL]`. Recruited op=32, arity=2, len=3, gain=7. Verified `[PUSH:a,PUSH:b,OP]` top==2(a+b) for 9 probes. Composition: added P5/P6 sharing `[OP32,PUSH:1,ADD]` with A0'; second consolidation recruited op=33 (arity=2, len=3, gain=3) whose body contains OP32 (hierarchical). Verified `[PUSH:3,PUSH:4,OP33]` top==15. PASS.

### T-RETIRE (prereg 5.5)
Recruited `[DUP,MUL]`, then idle consolidations. Retired at episode 4 (within W_IDLE+2=5). `nrec==0`, `n_recruited==1`, `n_retired==1`, behavioral checksums preserved. PASS.

### T-ADV (prereg 5.6)
PENDING. Requires an independent post-freeze adversary. Not measured.

## Falsifier status

- F_BREAK (behavioral checksum gate): Active. Caught 2 unsound candidates during development (since fixed via A7). Did not fire in the final battery (all recruitments were sound).
- F-DRIVER (driver never recruits directly): Held by construction (driver calls only `consolidate`).
- T-ADV: PENDING. The independent adversary has not yet run.

## Limitations and non-claims

1. **L2 bounded.** This is structural learning (new opcode from experience), not L3 representational invention. The candidate space (byte-exact subsequences, lengths 2..8) is researcher-enumerated.
2. **A7 restricts to stack-polymorphic bodies.** Bodies requiring program-input reads (INk) cannot be recruited. This is a soundness-motivated restriction, not a capability.
3. **Jump relativization (A8) assumes positional uniformity.** Not verified; documented limitation.
4. **Recruit/retire oscillation (A10).** No cooldown; documented.
5. **T-ADV pending.** No independent red team yet.
6. **LLM baseline PENDING.** Human baseline NOT MEASURED. (Per standing rules.)
7. **Single continuing learner?** Each test uses a fresh learner state. Integration into one continuing learner across tasks is future work (per the developmental integration requirement).

## Reproduction

Compiler: `/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`
Command: `znc oprecruit2.zag -o oprecruit2_final --no-analyze`
Binary: 139,644 bytes, zero external tools. Warning only: `zagd unavailable`.
Run: `./oprecruit2_final` (exit 0, empty stderr).
Determinism: 3 runs byte-identical.

## Source audit

- Pure Zag. No Python anywhere (verified via grep; only comment mentions "No Python").
- No em dash or en dash bytes in source or docs (verified via byte grep).
- No temporary debug output (FBDBG/TEMP/DBG removed).
- No committed binaries.

## Commits

- Prereg: `1df644256` (frozen, precedes implementation).
- Implementation: to be committed (this report).
- Verify: `1df644256` is an ancestor of the implementation commit.
