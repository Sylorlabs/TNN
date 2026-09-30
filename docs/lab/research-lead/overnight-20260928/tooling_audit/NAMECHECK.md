# Tooling Contamination Audit: Step 0 Name-Check

Date: 2026-09-30. Worker: Tooling Contamination Auditor.

## Standing rules identified before any audit work

1. Pure Zag/shell only. No Python, C, or other languages for research logic.
   Shell exists only as orchestration: invoke znc, execute Zag binaries,
   git operations, move/copy files.
2. Owned path only: docs/lab/research-lead/overnight-20260928/tooling_audit/.
   Commit with explicit pathspecs. No other paths staged or committed.
3. Contaminated paper docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
   is never edited, staged, committed, cited as canonical, or treated as evidence.
4. No em dashes in loop documentation. Shell-only dash check.
5. Other workers' untracked files are left untouched.

## Micah's tooling ruling (the audit standard)

ONLY Zag may implement research logic. No Python, C/C++, JavaScript, Rust,
or other language for scratch experiments, generators, analyzers, verifiers,
mirrors, fixture construction, scientific calculations, or editing helpers.

Shell/git may exist only as unavoidable orchestration: invoke znc, execute
Zag binaries, git operations, move/copy files where necessary.

Shell/awk/sed/grep scripts must not serve as substitute research programs.
If scientific evidence depends on computation, parsing, generation, scoring,
verification, hashing logic, etc., that logic belongs in Zag.

Any important prior result whose scientific logic depended on a
prohibited-language implementation remains contaminated until independently
reproduced in pure Zag.

Python-mirror-developed logic may NOT be adopted into TNN.
