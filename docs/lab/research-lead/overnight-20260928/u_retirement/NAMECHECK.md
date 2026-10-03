# NAMECHECK: U-RETIREMENT

Date: 2026-10-03. Worker: U-RETIREMENT. Lane:
`docs/lab/research-lead/overnight-20260928/u_retirement/`.

## Step 0: Toolchain guard (Micah's governance ruling, 2026-09-30)

- Safebin activated at session start: `export PATH="$HOME/safebin"`.
- `which znc` -> `/home/hatch/safebin/znc` (pinned znc).
- `which python3` -> nothing. `which python` -> nothing.
- All research computation in pure Zag via the pinned znc. Shell used only
  for: znc invocation, running compiled binaries, git operations,
  file assembly (cat), output comparison (cmp/sha256sum).
- Zero forbidden-executable invocations. Any accidental invocation would
  make this wave PROCESS-FAIL per the ruling.

## Scope

Documentation + verification only. No new mechanism. This lane:
1. Re-verifies the frozen U, GEN, and diamond batteries (fresh builds,
   3 runs each, byte-identical against frozen outputs).
2. Runs the restriction experiment: frozen GEN composer with the
   predicted-handshake admission restriction, on U's battery driver.
3. Writes RETIREMENT.md formally retiring U as a separate mechanism.

Commits: local only, never push, explicit pathspecs on every commit.
Use `/usr/bin/git` directly if the safebin symlink EPERMs (AGENTS.md lesson).
