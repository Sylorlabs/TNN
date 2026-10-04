# NAMECHECK.md: H-PI-REV2 step 4 independent reproduction (wave-20260930-2321pdt)

Lane: H-PI-REV2 step 4 (independent reproduction of F3a3 BUILD-PASS from committed source).
Worker role: independent reproducer only. No source edits, no bar changes, no new claims.

## Step 0: worker toolchain guard (mandatory)

Date: 2026-09-30, wave wave-20260930-2321pdt.

1. Safebin activated at startup: ran
   docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
   from the repo root, then export PATH="$HOME/safebin".
   Result: SAFEBIN-READY (36 tools, no python). znc resolves to the
   pinned repo binary
   src/tools/toolchain/znc_linux_x86_64_abed8aa1.
2. `command -v python3` returns nothing (exit 1); `command -v python`
   returns nothing (exit 1); direct invocation of python3 fails with
   "command not found". The safebin directory listing contains none
   of: python3, python. (Note: safebin has no `which` command, so
   verification used the shell builtin `command -v` and a direct
   invocation probe instead.)
3. All computational research operations in this lane use Zag (build
   via znc, runs via the compiled binary). Shell only: git operations
   and file moves. Zero Python, zero C/C++/JS/Rust anywhere in this
   lane's pipeline.
4. No forbidden executable was invoked this wave; no PROCESS-FAIL
   condition triggered.
5. No prereg or standing rule was altered or debated this lane; no
   Python pre-authorization exists in the frozen prereg 53256838f
   (void-on-sight rule acknowledged).

No em-dashes in this documentation.
