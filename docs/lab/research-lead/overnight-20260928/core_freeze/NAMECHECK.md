# NAMECHECK: Core Freeze Challenge Designer

Date: 2026-09-30. Worker: Core Freeze Challenge Designer (top-priority research program).
Task: design the CORE FREEZE CHALLENGE protocol. Design only; no implementation, no builds, no runs.

## Step 0: standing rules

I have read the standing-rules block at the top of LOOP_STATE.md. The rules that apply to this design task:

1. PURE ZAG ONLY (2026-09-23, owner red line): no Python anywhere in loop work, including verifiers and harnesses. This task authors pure markdown only, no code of any kind. The protocol specifies shell/sha256sum-only verification procedures for the freeze hashes, so the future freeze worker has a Python-free path.
2. Shell-only byte checks (2026-09-30): loop documents are checked for em/en dash bytes with docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh, never python3. I will run that script on both protocol files before committing.
3. The contaminated internal log docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md is never edited, staged, or committed. I will verify zero diff before committing.
4. Preregistration strictly precedes implementation. This protocol document IS the preregistration for the freeze challenge: no freeze worker, world designer, or adversary may implement, build, or run anything under this protocol before this protocol is committed.
5. Shared-branch provenance discipline: explicit pathspecs on every git add and git commit, limited to docs/lab/research-lead/overnight-20260928/core_freeze/; inspect git status before every commit; never remove a live .git/index.lock (wait and retry); commits stay local, nothing pushed.

I will honor these by authoring only markdown, running the shell dash check, verifying the contaminated paper is untouched, and using explicit pathspecs for exactly the two protocol files.
