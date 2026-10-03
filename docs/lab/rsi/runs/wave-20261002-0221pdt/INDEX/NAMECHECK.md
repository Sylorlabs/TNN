# NAMECHECK.md - INDEX lane, wave-20261002-0221pdt

## Step 0 - Worker Toolchain Guard (owner red line, 2026-10-02)

1. Ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh` at
   2026-10-02 02:26 PDT from `~/workspace/tnn-rsi`.
   Output: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).
   Linked 36 tools: awk, basename, bash, cat, chmod, cmp, cp, cut, date, diff, dirname,
   echo, find, git, git-receive-pack, git-upload-pack, grep, head, ln, ls, mkdir, mv, od,
   printf, rm, sed, sh, sha256sum, sleep, sort, stat, tail, tee, timeout, touch, tr, uname,
   uniq, wc, which, xargs, znc. Neither `python` nor `python3` resolves in safebin PATH.
2. Verified `which python3` under `export PATH="$HOME/safebin"` returns NOTHING
   (exit code 1). This check is repeated at the top of every shell invocation in this
   lane (`export PATH="$HOME/safebin";` prefix on every command).
3. All research logic in this lane is pure Zag compiled with the pinned znc below.
   No Python, C/C++, JavaScript, or Rust will be used in verifiers, scorers, harnesses,
   analysis, or scratch. Forbidden-executable invocation = automatic PROCESS-FAIL and
   immediate self-disclosure.
4. Pinned znc re-verified with sha256sum before use:
   `src/tools/toolchain/znc_linux_x86_64_abed8aa1` sha256 starts with `498abcb5`
   (matches the pinned prefix). Full hash recorded in PREREG_INDEX_REPRO.md.
5. Dash scan policy: only via
   `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`.
   No em or en dashes anywhere in loop documentation in this lane.

Step 0 status: PASS, 2026-10-02 02:26 PDT, worker session INDEX.
