# NAMECHECK: INTEGRATION-HOOK

## Step 0: Toolchain guard (executed at startup, before any other command)

- Ran `export PATH="$HOME/safebin"` as the FIRST command of this session.
- `which python3` returns nothing; `which python` returns nothing.
- All builds will use the pinned znc from safebin; all computation in
  pure Zag; text processing via shell tools only.
- Git writes via /usr/bin/git absolute path; explicit pathspecs on every
  commit; nothing pushed (local only).

## Steps 1-6 (to be completed)

1. Prereg written and committed ALONE before any implementation file.
2. Byte-copy base/world/module from C461 (cmp-verified identical).
3. Hook implementation in ih_learn.zag; driver in ih_main.zag.
4. Build with pinned znc; 3 runs byte-identical; stderr empty.
5. Kill-bar audit: frozen lines, identifier grep, dash-byte audit.
6. REPORT.md with verdict.
