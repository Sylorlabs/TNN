# PYTHON SWEEP REPORT — scaffold-and-release program

**Date:** 2026-09-22
**Ordered by:** Micah ("some groups might be running python — redirect if needed and document results")
**Auditor:** python-sweep subagent (this report)
**Scope:** `training_paradigms/rl_necessity/`, `training_paradigms/scaffold_release/` (+ `forks/`), `wave4/scaffold-release/` (shared substrate)

## Verdict (plain language)

**The program is CLEAN.** There is no Python anywhere in the scaffold-and-release program — no `.py` files, no `python`/`python3` invocations, no Python one-liners hiding in shell scripts. All decision-path logic (action selection, learner state updates, reward/score accumulation, disconnect firing) lives in four pure-Zag files compiled with the pinned znc. The two shell runners are glue: they compile, check determinism, and verify emitted check-lines — they make no trial decisions. **Nothing had to be redirected.** If you find nothing in decision paths, that is itself the report — this is that report, with the evidence below.

## Inventory (every file in scope, classified)

| # | File | Kind | Role | Classification |
|---|------|------|------|----------------|
| 1 | `rl_necessity/tn.zag` (305 lines) | Zag | Trial system: learner/world/harness | Pure Zag — decision path, no Python |
| 2 | `rl_necessity/tn_trial.zag` (550 lines) | Zag | Trial binary: arms A/B/C, disconnect logic, TN_CHECK emission | Pure Zag — decision path, no Python |
| 3 | `rl_necessity/run_trial.sh` | Bash | Runner: static checks → compile → 2-run determinism → verify checks | **GLUE** — no Python, no decision logic (see §Glue check) |
| 4 | `wave4/scaffold-release/sr.zag` | Zag | Scaffold-release system (shared substrate) | Pure Zag — decision path, no Python |
| 5 | `wave4/scaffold-release/sr_trial.zag` | Zag | SR trial binary | Pure Zag — decision path, no Python |
| 6 | `wave4/scaffold-release/run_trial.sh` | Bash | Runner (same shape as #3) | **GLUE** — no Python, no decision logic |
| 7–10 | `scaffold_release/forks/g1_rematch/r1`–`r5` | dirs | G1 fork workdirs | Empty — no code landed yet |
| 11 | `scaffold_release/forks/g3_lying_teacher/l1_mistaught_teaching/FORK_PREREG.md` | Markdown | Frozen fork prereg (prose) | No code at all |
| 12 | `scaffold_release/forks/g3_lying_teacher/l2_scalar_scaffold/FORK_PREREG.md` | Markdown | Frozen fork prereg (prose) | No code at all |
| 13 | `scaffold_release/forks/g3_lying_teacher/l3_hint_scaffold/` | dir | G3 fork workdir | Empty — no code landed yet |

**Census of the whole scope:** 4 `.zag`, 2 `.sh`, 18 `.md`, 6 `.txt`, 2 compiled binaries, zag cache files — and **0 `.py`**. Case-insensitive grep for `python` across every file in scope returned hits only in prose sentences saying the trial contains no Python (e.g. `R33_NATIVE_IO_V1.zag` line 17: *"No Python, shell execution, libc implementation or hidden language runtime"*; `wave4/PLAN.md`: *"No Python except documented one-time…"*). No shebangs other than `#!/bin/bash` on the two runners. No `system()`, `popen`, `exec`, or `_zag_raw_syscall` in any of the four Zag files — the only imports are `@import("tn.zag")` / `@import("sr.zag")`, sibling Zag sources.

## Glue check (the two runners)

`run_trial.sh` (both copies) embeds `awk` and `sed`, so each was read line-by-line for decision logic:

- `awk 'BEGIN{drop=0} /^fn arm_c\(\)/{drop=1} …'` — a static source-text filter that deletes the `arm_c()` function before grepping for `csum`/`ccnt`. It inspects source code, never trial state. It does not choose actions, update the learner, score rewards, or judge outcomes — it enforces the preregistered "accumulation confinement" bar on the code itself.
- The `while read … done < <(grep '^TN_CHECK,')` loop — compares the binary's emitted `actual` field against its emitted `expected` field. This is evidence verification after the fact; the decisions were already made inside the Zag binary. The runner judges nothing about what the learner should have done.
- Everything else is `sha256sum` comparisons and exit-code checks.

Classification for both runners: **GLUE** (verification harness, fine as-is). No Python, no embedded decision logic, nothing to redirect.

## Redirects

None. Zero DECISION-PATH hits, so zero rewrites, zero before/after diffs, and no determinism re-runs were required (no code was touched — the audit was read-only).

## Open watch (re-sweep trigger)

The fork groups have not landed implementation code yet: G1's five workdirs are empty, G3 has only frozen prereg prose in L1/L2 and an empty L3, and G2/G4/G5/G6 have no dirs at all. **This sweep covers what exists today.** Re-run this sweep when fork binaries land — the natural moment is when each fork crew commits its `.zag` sources, before its verdict is accepted.

## Method (for reproducibility)

1. Enumerated every file in scope (`find`, including dotfiles and dirs).
2. Grepped all files case-insensitively for `python`; grepped all `.sh`/`.zag` for `system(`/`popen`/`shell`/raw syscalls; checked shebangs.
3. Read both `run_trial.sh` files fully and classified every `awk`/`sed` usage as GLUE vs DECISION-PATH.
4. Confirmed the four `.zag` files are pure Zag with no external-process capability (only sibling `@import`s).

**Bottom line:** as of 2026-09-22, the scaffold-and-release program's evidence is clean of Python decision-making. The only Python-adjacent words in the entire scope are sentences saying there is no Python.
