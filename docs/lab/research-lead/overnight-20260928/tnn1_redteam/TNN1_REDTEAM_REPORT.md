# TNN-1 Red Team Report

## Verdict: TNN1-REDTEAM-COMPLETE

**Target:** `docs/lab/research-lead/overnight-20260928/tnn1_build/tnn1.zag`
(commit `0323b97d5`, 1088 lines, 153 functions)

**Overall:** 5 of 6 vectors ATTACK-PASS. 1 qualified ATTACK-SUCCESS.

---

## Vector 1: Integration genuineness : ATTACK-SUCCESS (qualified)

**What holds:** The workspace is genuinely shared. `ev_query`, `ev_teach`,
`ev_observe`, `ev_act`, plan construction (`plan_c2`, `plan_g`, `plan_it`),
`promote_map`, `contradict_map`, and `map_standing` all operate on the same
`W:[]u8` workspace. There is no separate state per subsystem. Nodes created
by the query path are visible to the ACT path via the shared edge store.
This is not three systems in a trench coat at the state level.

**What fails:** The XCAP test (`t_xcap`, F-INT4) does not prove the prereg's
strongest claim. The prereg F-INT4 requires "a query-miss plan must become
an action guide through shared edges." The test does not do this. It:

1. Runs `ev_query` and verifies the plan/MAP path returns the right answer.
2. Creates a SYNTHETIC guide node via `alloc_node` (not the query's MAP).
3. Gives it bid via a self-loop, then calls `contradict_map`.
4. Verifies both `map_standing` and `bid` decrease.

The test never calls `ev_act`. It never shows the query's MAP being picked
up as an action guide. What it actually verifies is that `contradict_map`
(a CAM-1 port) demotes both the query-path standing metric and the ACT-path
bid metric on the same node. That is real shared structure, but it is a
weaker property than plan-to-guide conversion.

The builder's own report acknowledges this: "The XCAP test uses a synthetic
guide node rather than reusing the query's MAP node directly, to avoid
fragile node-search logic."

**Impact:** The integration is structurally real, but F-INT4 as frozen does
not discriminate between genuine plan-to-guide flow and metric co-location.
A stronger test would run `ev_query` (miss, plan, promote), then `ev_act`
in the same workspace, and verify the promoted MAP is selected as the
action guide.

---

## Vector 2: Line-count honesty : ATTACK-PASS (with note)

1088 lines, 153 functions. One dead function found: `verify_plan`
(lines 554-564, 11 lines) is defined but never called. The verification
logic it contains is inlined in `mp_run` (lines 594-606). This is 11 lines
of dead code, not hidden complexity. The line count is fundamentally honest.

`lg` (log getter) and `main` were flagged by a naive unused-function scan
but `lg` is used and `main` is the entry point. No other dead code found.
No duplicated logic blocks. No comment inflation.

---

## Vector 3: Template smuggling : ATTACK-PASS

Exactly three base plan templates exist:
- `plan_c2` (line 331, TM_C2=1, CHAIN-2)
- `plan_g` (line 338, TM_G=2, GATHER)
- `plan_it` (line 352, TM_IT=3, ITERATE-UNTIL)

`TM_COMP=4` is used by `plan_ext` and `plan_c2c`, but these are composition
functions that clone and extend existing plans, not a fourth base template.
TM_COMP is the prereg-authorized TM_COMPOSED marker for composition results
(prereg: "template markers TM_CHAIN2/TM_GATHER/TM_ITER/TM_COMPOSED").
No additional templates, no semantic cases, no domain-specific branches.

---

## Vector 4: Menu resurrection : ATTACK-PASS

No `eval_body`. No LITERAL, COPY_A, DBL_A, ADD_AB. The CAM-1 menu is dead.

The dispatch in `exec_plan` (lines 427-456) branches on step-kind codes
1/2/3/4/5/6, which are the ISA opcodes SK_READ/SK_MOVE/SK_BEQ/SK_INC/
SK_EMIT/SK_APPLY. This is generic execution machinery over the closed
4-op ISA plus READ/EMIT, explicitly authorized by the prereg and the
protected-core ISA ruling. It is not a domain-template menu.

No `switch` statements. No chained type-dispatch resembling a menu.

---

## Vector 5: Determinism : ATTACK-PASS

Three consecutive runs of `tnn1_bin` produce byte-identical output.
SHA-256 `78847448a6afa384b6c9387d11d80ea849135f4c402196a3e03034b254cd8164`
on all three runs. `diff` confirms zero differences.

---

## Vector 6: Cross-suite interference : ATTACK-PASS

35 test functions, 38 `z_alloc(110656)` calls. Each test allocates a fresh
workspace via `z_alloc` + `tnn1_init`. No shared mutable state between
tests. Order-dependence is structurally impossible.

---

## Kill-bar assessment

- **K2** (zero new ops/cases/modes/bridges/handlers, 1200-line ceiling):
  PASS. No modes, bridges, or handlers in code (only in comments).
  1088 lines < 1200 ceiling. 11 lines of dead code noted but not a bar breach.
- **F-INT3** (template smuggling / semantic cases): PASS. Exactly 3 base
  templates; composition marker is prereg-authorized.
- **F-INT4** (coexistence-without-integration): QUALIFIED. The workspace is
  shared and the XCAP test verifies metric co-location on one node, but it
  does not verify plan-to-guide conversion. The trench-coat test as frozen
  is weaker than its description.

---

## Recommendations

1. Strengthen F-INT4 or narrow its claim: either implement a test where
   `ev_query` (miss, plan, promote) is followed by `ev_act` in the same
   workspace with the promoted MAP selected as guide, or reword F-INT4 to
   claim only shared-metric demotion.
2. Remove the dead `verify_plan` function (11 lines).
3. No other changes required. The build is sound.

---

## Governance

- Step 0 guard: `/usr/bin/python3` present as unremovable system binary,
  documented non-use, zero invocations. Shell/git only.
- Target not modified. Read-only attack.
- Sealed FW1-FW9 files not accessed.
- Contaminated paper zero-diff (not touched).
- No em dashes (byte-verified).
