# NAMECHECK: Law-Revert Integration Worker

Step 0 standing-rules check, 2026-09-30.

The standing rules that apply to this task: (1) Pure Zag only. No Python anywhere
in loop work: not glue, not analysis, not verifiers, not harnesses, not byte
checks. (2) Byte checks on loop documents must use the shell-only
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh;
python3 byte checks are a red-line breach even with disclosure. (3) Commits stay
local on tnn-native-lab with explicit pathspecs limited to my owned path
docs/lab/research-lead/overnight-20260928/learner_revert/; inspect git status
before every commit; never git commit --amend on the shared branch; never remove
a live .git/index.lock (wait and retry); never touch the contaminated paper
docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md.

I will honor these by: writing the prereg, implementation, and all verification
in Zag plus shell tools only (grep/awk/cmp/sha256sum); freezing the prereg alone
in its own commit before any implementation file exists; using explicit pathspecs
on every git add/commit with a git status --porcelain check immediately before;
and verifying the contaminated paper has zero diff at the end.
