# NAMECHECK.md - Documentation Auditor

## Step 0: Toolchain Guard

- Safebin setup: executed `setup` loop linking allowed tools into `$HOME/safebin`
- `export PATH="$HOME/safebin"` applied
- `which python3 python` returned: nothing (both absent)
- Guard check output: `guard-check-done`
- Zero forbidden executables invoked
- Verdict: TOOLCHAIN-GUARD-PASS

## Scope

- Audit only. No files edited by this worker.
- Task: search all docs for "seven floor" and "7 floor", verify each is correct
  (capabilities = 6, tests = 7), report any errors.
- Owned path: `docs/lab/research-lead/overnight-20260928/doc_audit/`
- Branch: `tnn-native-lab`, HEAD at start: `9e6c457cc9ee7bbb6ac8e2916bd0f93ad6451d02`

## Input provenance

- Floor spec commit `f383dd11c`: defines 6 floor capabilities (F1/F2/F3/G1/G2/G3)
  and a 7-test floor battery (verification tests, distinct from capabilities).
- Issue-fixer commit `877d8491a038e5cce6e3209d35c09c482d9d62a0`: fixed
  "seven floor capabilities" to "six floor capabilities" in
  `guard_integration/GUARD_INTEGRATION.md` (insertion B).
- Follow-up commit `9e6c457cc`: fixed same count error in
  `guard_integration/NAMECHECK.md` (7 -> 6).

## Constraints

- No em dashes in any output.
- Paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- Audit only: no edits to any document, including the one under audit.
- Nothing pushed.
