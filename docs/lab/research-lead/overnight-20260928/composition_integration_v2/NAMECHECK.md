# NAMECHECK.md -- H-COMPINTEG-2 Worker

## Step 0: Toolchain Guard

- Date: 2026-10-02
- Safebin setup: ran
  `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`;
  linked 36 tools; `export PATH="$HOME/safebin"`.
- `which python3` under worker PATH: no output (exit 1) -- GUARD PASS
- `which python` under worker PATH: no output (exit 1) -- GUARD PASS
- Pinned znc: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (same binary the C295 and C305 lanes used).
- Pure Zag for all computation. Shell only for znc, binaries, git,
  file moves. No forbidden executable invoked at any point.
- Compiler lessons honored: no `as *i32` + slice construction in
  functions (u8 cells + get32/set32 helpers); no _zag_print for
  dynamic output (emit/e64 only); no reliance on `.len` of cast
  slices; if-nesting kept shallow with hoisted flags; no `!(A && B)`
  in while conditions (grep audit planned); capacity plan under the
  1024-node workspace.

## Step 1: Provenance

- Worker: Composition Integration v2 (subagent, 2026-10-02).
- Parent mandate: H-COMPINTEG-2, integration retry of H-COMPINTEG-1
  (ledger C295, verdict COMPOSITION-INTEGRATION-INCOMPLETE) WITH the
  three INTEG-BREAK red-team guards (ledger C305), plus routing of
  the INTEG-EXEC-STALE sentinel into the adapt/revise path (the red
  team's flagged open item).
- Branch: tnn-native-lab. Commits stay LOCAL, never pushed
  ("Local only, never pushed." appended to messages).
- Reports read: integ_break_redteam/REPORT.md (C305),
  composition_integration/PREREG.md + PREREG_AMENDMENT1/2/3.md +
  REPORT.md (C295).

## Step 2: Commit order self-check

- PREREG.md + this NAMECHECK.md (Step 0 only at freeze time)
  committed ALONE first. No implementation (.zag sources, guarded
  copies, build script, binaries, runs) written before that commit.
  Freeze ordering: PASS/FAIL recorded at commit time below.
- Prereg freeze is terminal for bars: no weakening, no salvage.

(Freeze commit hash: filled at commit time.)

## Step 3: Build records (filled after implementation)

- Guarded copies (byte-identical to red-team commits, verified):
  cc_base_g 7ef2e6a9d8731969afea53e977026320bfe28c19469e3bb99e12196242699b0d
  ts_patch_g fe6878b980bb9911f6dbec2c39acb8388aa6106122f566a535b46462973de6c6
  lvcomp_patch_g e4e2a9464be72a508279f3d7822136854ad3248c4669c22f884bd72745782f01
- Pristine copies (sha256 must match C295 values from C305 NAMECHECK):
  un_patch 3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2
  adapt_patch 867bd6d96d9d4026c39d9bc5a9c6944f9ac0427722a3f6451c325c49f60c2ff0
  revise_patch 5113000b1360bf3e978cb106f91f15a1e5956db113eb4b3c26a1ebde1fa7f6e3
  ts_patch (unused; superseded by ts_patch_g in this build)
  lvcomp_patch (unused; superseded by lvcomp_patch_g in this build)
  integ_patch 1077c89c0a0c3eb9134f056d02f3678763b10bec4ef81a7c2ec95d1544bccff9
- New: integ2_patch.zag (stale routing + compose_integ2), integ2_driver.zag.

## Step 4: Constraints

- Pure Zag. Zero em/en dashes in lane docs (check_no_dash.sh).
- The token `expected` appears in no new source (grep audit).
- No new edge/MAP types, opcodes, modes, bridges, handlers,
  semantic cases, fact fields, or header slots beyond the three
  already-characterized guards. integ2_patch.zag <= 150 lines.
- The three guards are EXPERIMENTAL copies in this lane only; they
  are NOT promoted to the frozen base (that needs Micah's ruling).
- Paper untouched (TNN_RESEARCH_PAPER_20260929.md). Red-team
  originals never edited. Explicit pathspecs. Shared history never
  amended. Nothing pushed.

## Step 5: Verification session (filled after runs)

- Determinism: integ2_bin 3/3 byte-identical, sha256 recorded.
- Dash audit, grep audits, frozen sha256 audits: recorded here.
