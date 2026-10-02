# NAMECHECK: Core Freeze Challenge Stage 0 Readiness Worker

Date: 2026-09-30. Worker: Core Freeze Challenge Stage 0 Readiness Worker.
Task: make the freeze candidate executable under the frozen protocol (world-input interface, region declaration, null-world run). READINESS-[PASS/FAIL].

## Step 0: standing rules

I have read the standing-rules block at the top of LOOP_STATE.md. The rules that apply to this readiness task:

1. PURE ZAG ONLY (2026-09-23, owner red line): no Python anywhere, including glue, analysis, verifiers, and harnesses. This task authors pure Zag (.zag) and markdown only. All parsing, diffing, byte checks, and hashing are done with the shell, znc, sha256sum, cmp, and the worker snippet check_no_dash.sh.
2. Shell-only byte checks (2026-09-30): em/en dash checks run only through docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh, never python3.
3. The contaminated internal log docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md is never edited, staged, or committed. I verify zero diff before committing.
4. Preregistration strictly precedes implementation. The governing prereg is the frozen protocol itself (66e3c3f38, FREEZE_PROTOCOL.md section 3, the Stage 0 gate), committed before this work began.
5. Shared-branch provenance discipline: explicit pathspecs on every git add and git commit, limited to docs/lab/research-lead/overnight-20260928/core_freeze/stage0/; inspect git status before every commit; never remove a live .git/index.lock (wait and retry); commits stay local, nothing pushed.

I honor these by writing only .zag and .md, running the shell dash check on every new file, verifying the contaminated paper is untouched, and using explicit pathspecs for exactly the stage0 owned files.
