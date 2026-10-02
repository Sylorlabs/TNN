# Step 0 Name-Check: Pure-Zag Freeze Scorer

Date: 2026-09-30. Worker: Pure-Zag Freeze Scorer.

## Standing rules identified before any work

1. Pure Zag only for research logic. No Python. No C/C++/JavaScript/Rust.
   Shell/git exist only to: invoke znc; execute Zag binaries; perform git
   operations; move/copy files. No shell/awk/sed/grep scripts as
   substitute research programs. The scorer itself is Zag.
2. Contaminated paper
   `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
   is never edited, staged, committed, or cited. Verified zero-diff at
   each commit.
3. No em dashes in this directory. Verified with shell-only byte check.
4. Frozen artifacts (commit 97b28e6a6, FREEZE-RUN-COMPLETE) are read-only.
   This worker never modifies them.
5. Commit only the owned path
   `docs/lab/research-lead/overnight-20260928/freeze_rescore/` with
   explicit pathspecs.
6. Pinned compiler: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
7. AGENTS.md compiler lesson: never construct function-local slices with
   `as *i32`; use u8-backed cells with little-endian helpers.

## Task

Reimplement the Core Freeze Challenge scoring logic (currently
`score_probes.sh` in shell/awk, flagged NEEDS-RERUN in the tooling audit)
in pure Zag. Run the Zag scorer against the frozen battery outputs and
re-derive all nine world scores. Scores must match the reported 1/9
verdict, or any discrepancy is documented.

Verdict label on completion: FREEZE-RESCORE-COMPLETE.
