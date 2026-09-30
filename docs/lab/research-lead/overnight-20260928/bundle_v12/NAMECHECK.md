# NAMECHECK: Bundle v12 Archivist

Step 0, written before any work.

- Task: Create fresh verified git bundle backup of tnn-native-lab (v12).
- Worker role: Bundle v12 Archivist (shell/git orchestration only).
- No research logic will be written. Shell/git only: git bundle, git verify, sha256sum, file writes, git add/commit.
- Contaminated paper `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` must remain zero-diff.

## Toolchain guard (Step 0, mandatory)

Command run: `which python3 python 2>/dev/null; echo "guard-check-done"`
Result: `/usr/bin/python3` present. Guard check recorded. No Python will be invoked for any bundle operation.

## Commits owned

- bundle_v12/NAMECHECK.md (this file)
- bundle_v12/METADATA.md (bundle filename, HEAD, SHA-256, date, verification status)

Local only. No push.
