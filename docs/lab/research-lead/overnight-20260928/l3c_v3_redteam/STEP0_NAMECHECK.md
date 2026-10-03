# Step 0 Name-Check: L3C v3 Independent Red Team

Date: 2026-09-30. Task: attack the L3C-V3-PASS claim (commit 3bfa0947c)
as an independent red team, pipeline step 10. Assume the claim is false
and try to break it.

Standing rules from the top of the repo-root LOOP_STATE.md that apply:

1. PURE ZAG ONLY. This is a literal red line. My red-team work uses pure
Zag for the attack harness, pure shell for builds and byte checks, and
markdown for plans and results. No Python anywhere: not in the harness,
not in analysis, not in verification. I will use the shell-only
check_no_dash.sh snippet for dash checks, never python3.
2. Shell-only byte checks. Same as above: the worker_snippets
check_no_dash.sh script is the only byte checker.
3. Fork testing. Not applicable: this is a red-team attack on one
committed mechanism, not a wave battery.
4. Image judge. Not applicable: no image work.

How I honor them: all attack artifacts are .zag, .sh, or .md files under
my owned path docs/lab/research-lead/overnight-20260928/l3c_v3_redteam/
only. Commits use explicit pathspecs and only after inspecting
git status. The contaminated paper
docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
is never edited, staged, or cited as evidence. If a live .git/index.lock
appears, I wait and retry; I never remove it.

Name-check written before any attack plan or implementation. Proceeding.
