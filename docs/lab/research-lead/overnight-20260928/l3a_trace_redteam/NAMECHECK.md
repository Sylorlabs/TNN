# Step 0 Name-Check: L3A-TRACE Independent Red Team

## Standing rules that apply

From the standing-rules block at the top of `LOOP_STATE.md` (repo root):

1. **PURE ZAG ONLY (2026-09-23, owner red line).** This is an attack/analysis
   task. All probes will be written in Zag or POSIX shell. No Python will be
   invoked for any purpose: not for implementation, not for diagnostics, not
   for /tmp scratch, not for log comparison, not for byte checks.

2. **Shell-only byte checks (2026-09-30).** All dash checks will use the
   shell-only snippet
   `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`.
   I will not reach for python3 for byte checks.

3. **Contaminated paper (standing).** The file
   `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
   will not be read, edited, staged, or committed in this wave.

4. **Commit discipline.** Commits stay local on branch `tnn-native-lab`.
   Owned paths only
   (`docs/lab/research-lead/overnight-20260928/l3a_trace_redteam/`),
   explicit pathspecs on every git add/commit. I will inspect `git status`
   before every commit and never stage another worker's files. If I encounter
   a live `.git/index.lock`, I will wait and retry; I will never remove it.

5. **Kill-bar honesty.** My attack plan is committed alone BEFORE any probe
   runs (K1). Probes execute against the committed source/binary (K2).
   Results are recorded honestly whether they break or confirm the claim.

## How I will honor them

- Attack plan committed first, alone, before any probe code exists.
- All probe harnesses in POSIX shell + pinned znc + pure-Zag variants.
- `cmp`, `sha256sum`, `grep` for comparisons; never python3.
- `check_no_dash.sh` for every doc I write.
- Explicit pathspecs; `git status` before each commit.
- The contaminated paper is never touched.
