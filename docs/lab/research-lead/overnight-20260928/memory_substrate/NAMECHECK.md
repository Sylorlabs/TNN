# Step 0 Name-Check: Memory Substrate Designer

Date: 2026-09-30. Worker: General Memory Substrate Designer.

Applicable standing rules from LOOP_STATE.md:

1. PURE ZAG ONLY (2026-09-23): This task is design plus markdown prereg only.
No implementation is authorized. I will use shell and git commands exclusively
and invoke no Python for any purpose.

2. Shell-only byte checks (2026-09-30): Dash checking uses only
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
Never python3 for byte checks.

3. Fork testing and image-judge rules: not applicable to memory-substrate design.

4. Commits stay local. Owned paths only:
docs/lab/research-lead/overnight-20260928/memory_substrate/. Explicit pathspecs
on add and commit. Inspect git status before committing. The contaminated paper
TNN_RESEARCH_PAPER_20260929.md is outside my owned path and will be left
untouched (verified zero diff).

5. Micah 2026-09-30 directive: the Core Freeze Challenge is the central
architecture benchmark. The 1/9 result is evidence about what the frozen core
is missing, not nine requests for nine patches. The store/eviction failure
must NOT become another cache-policy version treadmill. Design must answer:
what general learner-owned memory representation/policy lets one frozen learner
preserve newly useful knowledge, dependencies, hypotheses and structures
without task-specific storage logic. One-System Rule applies: capability from
learner-created state, not new Zag subsystems. Fewer mechanisms, fewer
bridges/modes, lower source delta, more capability from the same frozen core.
Reject single-world fixes unless they reveal a general mechanism.

This paragraph was written before any design work began.
