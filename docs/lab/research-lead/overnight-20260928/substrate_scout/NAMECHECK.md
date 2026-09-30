# Step 0 Name-check (Substrate Scout)

The standing rules from the top of LOOP_STATE.md that apply to this task:

1. **PURE ZAG ONLY (owner red line).** This is documentation-only scouting work,
so it produces pure markdown written by hand. No Python is invoked for any
purpose: no scripts, no analysis, no verification harnesses. Dash checks use
the shell-only `check_no_dash.sh` snippet. Documentation work does not compile
Zag, so no toolchain interactions are needed.

2. **Image-judge rule: not applicable.** This task produces no image candidates
and surfaces nothing to Micah for judgment.

3. **Fork testing: not applicable.** This task modifies no TNN source or
binaries, so there is nothing to fork-test.

4. **One-System Rule accounting.** This is scouting, not implementation: 0
cognition source lines added, 0 new semantic cases, 0 new modes, 0 new
bridges, 0 new task-specific handlers, 0 new learner-state structures. The
document itself is learner-agnostic survey material; it proposes no subsystem.

5. **Contaminated paper untouched.** `TNN_RESEARCH_PAPER_20260929.md` is never
edited, staged, or cited as evidence.

6. **Commit hygiene.** Commits are local only, owned paths
(`docs/lab/research-lead/overnight-20260928/substrate_scout/`) only, explicit
pathspecs on add and commit, `git status` inspected before each commit. On a
live `.git/index.lock`, wait and retry; never remove it.
