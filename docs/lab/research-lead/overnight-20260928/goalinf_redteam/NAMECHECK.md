# NAMECHECK: GOALINF Red Team (goal-type inference adversarial battery)

## Step 0: Worker toolchain guard (mandatory, recorded before any work)

- Ran the safebin setup block at session start (2026-10-02 ~08:15 PDT):
  linked git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk,
  wc, cmp, sha256sum, git-receive-pack, git-upload-pack into
  $HOME/safebin.
- `export PATH="$HOME/safebin"` active for every command in this session.
- `which python3 python` under safebin PATH returned NOTHING (empty
  output before "guard-check-done"). No python3/python resolves.
- All computation in this task is pure Zag via the pinned znc binary
  (reached through $HOME/safebin/znc). Shell used only to invoke znc,
  run binaries, assemble with cat, and do file/git operations.
- Reproduction check: reassembled H-GOALINF-1's gi_full.zag from its
  committed sources and rebuilt with safebin znc; output SHA-256
  matched the committed runs byte for byte
  (abc1afdb0f796a1625edf7f121893e1b57f83c3ebf897abd92b46db215687291).
  Toolchain verified before attack work began.
- If any forbidden executable is invoked, this wave is PROCESS-FAIL.
  None was: zero Python invocations this session.

## Provenance

- gi_base.zag (2444 lines): cp copy of H-GOALINF-1's committed
  gi_base.zag, cmp-verified byte-identical. Never edited.
- gi_patch.zag (226 lines): cp copy of H-GOALINF-1's committed
  gi_patch.zag, cmp-verified byte-identical. Never edited. This is the
  frozen mechanism under attack: gi_factscan, gi_probe, gi_supersede,
  gi_compose, ev_iquery.
- gi_attack.zag (218 lines): new file, the only new code. Four attack
  worlds plus instrumentation helpers (gi_confirm copied verbatim from
  the H-GOALINF-1 driver; mk_chain world builder; map/FACT counters).
  The attack driver builds adversarial worlds and calls the frozen
  ev_iquery; it never reimplements or patches the routing.
- Build: cat gi_base.zag gi_patch.zag gi_attack.zag > gi_full.zag
  (2888 lines); compiled with pinned znc (exit 0, A0102 warnings only,
  same class as H-GOALINF-1); 3 runs, SHA-256
  70094d20f061535f123675445d3a37e4cf8dd8f911645dbccd19a810586a07a7,
  3/3 byte-identical.

## Constraints honored

- Frozen mechanism attacked, never modified (copies, cmp-verified).
- Pure Zag. Zero Python invocations (guard above).
- Zero em/en dashes in all documentation (byte-verified with grep).
- Research paper untouched. Nothing pushed to GitHub (local commits only).
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- No fixes applied to anything killed: attack A is reported as KILL
  with the mechanism left exactly as found.
- Git commits use EXPLICIT pathspecs only.
