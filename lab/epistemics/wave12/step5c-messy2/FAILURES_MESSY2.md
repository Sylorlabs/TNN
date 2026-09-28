# STEP 5c-M2 — Failures Log

Date: 2026-09-20. Workstream-2. Prereg frozen 2026-09-20 (amendments A1, A3;
A2 withdrawn).

## Graded battery: NONE FOUND

No kill bars fired. No M-bar fired. The independent checker reports
`CHECK_RESULT: PASS` on the CUR transcript. `clean_corrupt=0/128`,
`xcheck_fail=0`, all in-Zag self-checks green.

The CTL arm fails M-bars as designed (it is contrast-only, ungraded);
its failures are the expected demonstration that weak defaults collapse
under messy conditions, not battery failures.

## Development defects fixed before the graded run

These were caught during harness development, fixed, and are NOT present
in the graded evidence. Recorded here per the prereg's honest-failure rule.

### D1. Slot-id aliasing: arm confused reused scratch slot for registry claim

**Symptom**: during CUR phase-B, later episodes showed `f3=1`
(kill-evidenced) where the frozen demand was `f3=0`. Diagnostic:
`DBG21,KE,63,0,0` — a kill-evidenced audit entry on slot 63 that was
episode scratch, not a registry claim.

**Root cause**: `st_add` reuses dead slot ids for new allocations. The R2
registry retains slot ids after claims are killed. The allocator reused
those ids for episode scratch. `arm_cur_r2b` checked only
`sl>=0 && live[sl]==1`, so after the first correct regime-break revision,
later phase-B episodes mistook live scratch slots for old registry claims
and killed one scratch slot per episode.

**Fix**: value-check the slot — verify `value[sl]==V` (the registry's
expected claim id) in addition to liveness. Slot ids are not stable
identities after free.

**Repro** (pre-fix binary, since recompiled): run the harness at the
commit before the fix; episodes in runs r≥1 phase-B show `f3=1` on the
checker where `dmask`-derived demand is 0. The checker (`check_messy2.awk`
v1) correctly flagged 68 such episodes.

### D2. znc "indexing unsupported" on three simultaneous slice aliases

**Symptom**: `znc: error in arm_cur_r2b: native: indexing unsupported
(only "literal"[i], slice[i], or *T[i])` after adding the value check via
a helper function with its own aliases.

**Root cause** (empirical): three simultaneous `[]u8` aliases from the same
large struct (`s.*.live`, `s.*.value`, `s.*.forcepin`) in nested scopes
trips a znc native-codegen limitation. Two aliases are fine.

**Fix**: call `st_i32_get(s.*.value,sl*4)` directly in the condition
instead of aliasing `value` to a local. No helper function.

**Repro**: any function with three `let x:[]u8=s.*.FIELD;` aliases from a
large struct used in nested scopes fails to compile; removing any one
alias fixes it.

### D3. Amendment A2 (prereg process, withdrawn)

**Symptom**: none in code. During pre-results review I drafted amendment A2
misreading `pin_esc==2 (one per st2=3 run)` as one escalation per
st2∈{0,3} run, which would have contradicted the frozen defeated sets.

**Fix**: A3 supersedes/withdraws A2 before any results were graded; the
original sets stand. No evidence was re-graded.
