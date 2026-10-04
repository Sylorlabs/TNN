# NAMECHECK: L3-NIV2 CALR red team (K10 adjudication worker)

Worker: L3-NIV2 CALR red-team worker (subagent, 2026-10-02). Replacement
for a completed worker (D3 policy redesign). Task: adversarial red-team
of CALR, the L3-NIV2 wave-3 search mechanism (BUILD-PASS, ledger C334).

## Step 0: Worker toolchain guard (MANDATORY, recorded)

Safebin activated before any execution in this task:

- Ran the mandatory setup: mkdir -p $HOME/safebin; symlinks created for
  git, znc (pinned src/tools/toolchain/znc_linux_x86_64_abed8aa1), sh,
  bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum,
  git-receive-pack, git-upload-pack. export PATH="$HOME/safebin".
- Verified under the safebin PATH: `which python3` returns nothing,
  `which python` returns nothing.
- Pinned compiler verified: $HOME/safebin/znc resolves to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- All scientific computation is pure Zag compiled with the pinned znc.
  Shell is used only for: invoking znc, running compiled binaries, git
  operations, file moves, sha256sum digests, FIFO plumbing in the battery
  supervisor, and the no-dash documentation check. No python3, python, or
  any other forbidden interpreter is invoked at any point.

Per Micah's 2026-09-30 governance ruling: any forbidden executable
invocation would make this wave PROCESS-FAIL.

Toolchain notes specific to this task (Zag pitfalls observed while
reading the frozen sources; applied in all new Zag code):
- No `as *i32` plus slice construction inside functions.
- No `_zag_print` for dynamic output; single-buffer emit plus one
  `_zag_raw_syscall` per line (e1str/e1i64/e1hex/wraw pattern).
- `as []f64` / `as []i64` do not rescale `.len`; avoided.
- `if` nesting kept at 3 or fewer.
- No `!(A && B)` in `while` conditions; De Morgan form used.

## Step 1: Scope check

- Adversarially red-team CALR as frozen at commit e61c9c50c
  (L3-NIV2 wave 3, REPORT_WAVE3.md BUILD-PASS, ledger C334). Break it:
  find problems where it DEFERS or commits wrong although a solution
  exists within the TEST budget.
- Do NOT modify the l3_novel_intermediate_v2 lane. All red-team work
  lives in l3_niv2_calr_redteam/. The artifact under test is a read-only
  copy of the frozen e61c9c50c sources (extracted via `git show`, never
  edited) plus binaries built from them.
- Do NOT weaken K1 through K12 or KC0A through KC0D. Do NOT widen the
  5-op ISA. Do NOT redesign the task. Do NOT inspect sealed-world
  contents. All attack fixtures are newly authored unsealed dev-style
  keys, clearly labeled REDTEAM, never confused with sealed content.
- Freeze PREREG.md plus this Step 0 update in a commit containing those
  two files ALONE, before any red-team .zag source, key file, binary, or
  run log exists. (The impl/ directory currently holds only the
  read-only frozen-source copies and their build outputs; no red-team
  attack code exists at freeze time.)
- Commits stay LOCAL, explicit pathspecs, never pushed, never amend
  shared history, never git reset. Do not touch other workers' files.
- No em/en dashes in loop documentation (checked before commit).
- 3/3 determinism required per attack (K1). VOID is terminal.
