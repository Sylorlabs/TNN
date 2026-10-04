# L3-NIV2 Wave 2 Report

## Summary
Wave 2 debugger and clean rerun of L3-NIV2 implementation.

**Panic:** Root cause identified as worker bug (buffer sizing), fixed. Implementation
now builds clean and runs without panic. Wave-1 BUILD-FAIL (panic) is resolved.

**Search:** T1 DEFERs on DEV-S1. Four beam-search variants tried; none finds the
length-3 solution. This is a search-adequacy failure.

**Verdict:** BUILD-FAIL. Bar K1 (T1 must COMMIT) is not met.

## Step 0: Toolchain Guard
Safebin activated at $HOME/safebin per setup_safebin.sh. `which python3` returns
nothing; `which python` returns nothing. Pure Zag for all scientific computation.
Shell only for znc invocation, binary execution, git ops, file movement.

Near-miss disclosure: A command fragment `python3 -c "print('skip')"` was typed
during debugging. With safebin PATH, python3 does not resolve; the invocation
failed with "command not found". No forbidden computation occurred. The guard
worked as designed. Disclosed per the 2026-09-30 governance ruling.

## Debug Report: T1 select_beam Panic

### Root Cause: Worker Bug (not design flaw)
In `expand_level` (lm_cons2.zag), `pstart` and `pend` were `z_alloc(128)` = 32 u32
slots. The beam count `bn` reaches `max_n` = 40. The write `put32(pstart, bi*4, chn)`
at `bi` = 32 writes past the 128-byte buffer, causing `panic: slice index out of bounds`.

The panic surfaced in `select_beam` because `expand_level` calls it after the
overflow. Wave-1 misattributed the panic to `select_beam`; the bug was the
undersized buffers in the caller.

### Fixes Applied (lm_cons2.zag, lm_cons.zag, lm_arms.zag, lm_main.zag)
- `expand_level`: pstart/pend 128 -> 512; ret 32768 -> 262144; rescued_marks
  8192 -> 262144; tmp_idx 4096 -> 8192.
- `construct`: seeds 1024 -> 4096.
- `lm_main`: ch 32768 -> 262144; beam 256 -> 512; pool 4320000 -> 7077888
  (POOL_N 20000 -> 32768); stab 262144 -> 524288.
- `lm_cons`: POOL_N -> 32768; mk_cand cap 20000 -> 32768; stab 32768 -> 65536
  entries (masks 32767 -> 65535).
- `lm_arms` `revise`: eb 8192 -> 81920.
- `select_beam` call sites: max_n 40 -> 80.
- Restored real `select_beam` (wave-1 had TRIVIAL STUB).

Build: `sh battery.sh build` -> "build ok". No compiler errors.

## Search Adequacy Investigation

After the panic fix, T1 runs clean (rc=0, no panic) but DEFERs on DEV-S1
(y = x^2 + x; refprog `[CPY r1,r0][MUL r0,r0][ADD r0,r1]`, length 3).

### Diagnosis
Every length-3 solution must pass through the score-1 prefix
`[CPY r1,r0][MUL r0,r0]` (pool id 913). Analysis of the candidate pool:
- 2109 distinct (first,second)-instruction pairs at score 1.
- The crucial pair ranks 326/2109 by min-id.
- Beam quota 26 per level cuts it before extension.

The id-ordering is circular: beam order determines children ids, which
determines future beam ranking. Any id-based criterion risks pruning crucial
intermediates.

### Variants Tried
1. **Score-greedy** (original): DEFER. Crucial prefix is 3rd in its group by id.
2. **Score-stratified** (equal quota per score level): DEFER. Within score-1,
   still id-ranked.
3. **(first,second) syntactic grouping** (best-1 per pair, 6561 groups): No panic,
   but DEFER. Crucial pair rank 326 > quota 26.
4. **Behavioral-signature grouping** (group by 6-output signature via local
   isa_run, zero TEST cost; best-1 per signature):
   - Hash-table version: panicked (compiler pattern issue, not logic).
   - Direct-compare with ordering sort: panicked in sort (not fully isolated).
   - Encounter-order (no sort): Clean run, no panic, but DEFER. 12 distinct
     level-2 behaviors in beam; solution not found. Possible signature
     collisions or extension failure.

### Conclusion
The beam search, as implemented in four variants, cannot reliably discover the
length-3 solution for DEV-S1. The crucial intermediate is pruned before extension.
This is a search-adequacy gap.

## Battery Results

T1 (DEV-S1, y=x^2+x): DEFER. CONSTRUCT-DONE, ARM-END T1 FAIL.
  Beam: L2=12, L3=25, L4=36, L5=38, L6=40 candidates. No panic.

T2-T4: Not completed (battery killed after T1 confirmed DEFER; T1 is the
gate for the construction mechanism).

Determinism: Not verified (3x byte-identical) because T1 does not COMMIT.

## Verdict: BUILD-FAIL

**Failed bar:** K1 (T1 construction must COMMIT with the novel intermediate).

**Flaw:** The beam-search construction prunes the crucial score-1 intermediate
(`[CPY r1,r0][MUL r0,r0]`, the x^2 prefix) before it can be extended to the
length-3 solution. Four beam criteria tried (score-greedy, score-stratified,
syntactic grouping, behavioral grouping); all prune it. The 2109 candidates at
score 1 with beam 80 means any fixed ranking must cut 96 percent; the crucial
prefix (rank 326 by id) is cut.

**Design vs implementation:** The PREREG specifies "beam search" without pinning
the selection criterion, giving implementation latitude. The failure across four
reasonable variants suggests the bar requires a search strategy beyond the
tried beam formulations (e.g., explicit lookahead, best-first by potential, or
non-beam enumeration). This is reported as BUILD-FAIL, not silently patched.

**What was fixed:** The wave-1 panic (worker bug) is resolved. The implementation
is clean, builds, runs without panic, and honors the frozen ISA, budgets, and
protocol. The failure is in search adequacy, not in the panic bug.

## Files Changed
- l3_novel_intermediate_v2/impl/lm_cons2.zag (buffer sizes, beam_level rewrite)
- l3_novel_intermediate_v2/impl/lm_cons.zag (POOL_N, stab sizes)
- l3_novel_intermediate_v2/impl/lm_arms.zag (revise buffer, max_n)
- l3_novel_intermediate_v2/impl/lm_main.zag (pool, beam, ch, stab sizes)
- l3_novel_intermediate_v2/NAMECHECK.md (Step 0 wave-2)
- l3_novel_intermediate_v2/REPORT.md (this file)

## Recommended Follow-up
The construction search needs a fundamentally different strategy to retain
crucial intermediates. Options: (a) iterative deepening with backtracking,
(b) explicit two-step lookahead in beam scoring, (c) novelty search rewarding
behavioral diversity with higher quota. Any new strategy must stay within the
frozen PREREG (no new opcodes, no weakened bars) or trigger a fresh prereg.
