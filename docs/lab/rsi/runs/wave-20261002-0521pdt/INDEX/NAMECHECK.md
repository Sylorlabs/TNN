# NAMECHECK.md - INDEX-EVICT lane, wave-20261002-0521pdt

## Step 0 - Worker Toolchain Guard (owner red line, 2026-10-02)

1. Ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   at 2026-10-02 05:26 PDT from `~/workspace/tnn-rsi`.
   Output: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).
   Neither `python` nor `python3` resolves in safebin PATH.
2. Verified `which python3` under `export PATH="$HOME/safebin"` returns NOTHING
   (exit code 1). Every shell command in this lane is prefixed with
   `export PATH="$HOME/safebin";`.
3. All research logic in this lane is pure Zag compiled with the pinned znc
   `src/tools/toolchain/znc_linux_x86_64_abed8aa1` (sha256 prefix 498abcb5,
   re-verified before use). No Python, C/C++, JavaScript, or Rust in verifiers,
   scorers, harnesses, analysis, or scratch. Forbidden-executable invocation =
   automatic PROCESS-FAIL and immediate self-disclosure.
4. Pinned znc rule (AGENTS.md): no `as *i32` + `q[0..n]` slice construction
   inside functions; u8-cell loop idiom with little-endian pack/unpack
   helpers. Observed in all new Zag code in this lane.
5. Dash scan policy: only via
   `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`.
   No em or en dashes anywhere in loop documentation in this lane.

Step 0 status: PASS, 2026-10-02 05:26 PDT, worker session INDEX-EVICT.

## Commit-order self-check (prereg discipline)

- PREREG_EVICT.md frozen in its own commit before any implementation file.
  Freeze commit: `0f2a862f2` (2026-10-02, 1 file, 199 insertions, pathspec-only).
  No implementation, sealed input, or eval file existed in that commit.
- Implementation and sealed-eval commits strictly follow the prereg commit.
- No frozen kill bar weakened after seeing results.
