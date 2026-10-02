# NAMECHECK.md -- INTEG-BREAK Red Team Worker

## Step 0: Toolchain Guard

- Date: 2026-10-02
- Safebin setup: ran
  `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`;
  linked 36 tools; `export PATH="$HOME/safebin"`.
- `which python3` under worker PATH: no output (exit 1) -- GUARD PASS
- `which python` under worker PATH: no output (exit 1) -- GUARD PASS
- Pinned znc: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (same binary the C295 lane used).
- Pure Zag for all computation. Shell only for znc, binaries, git,
  file moves. No forbidden executable invoked at any point.
- Header slot census (grep over the six frozen sources for
  hg/hs(W,N)): used slots are 0, 4, 8, 12, 16, 20, 24, 28, 32, 36,
  48, 56. Slots 40 and 44 are free. GUARD-T2 uses hg(W,40) for the
  prediction source struct id (guarded copies only).
- Fact field census (tag-1 nodes): fields 0, 4, 8, 12, 16, 20, 24,
  28, 32, 36 observed in use. Field 44 is free. GUARD-T1 uses
  field 44 as the learner-origin bit (guarded copies only).

## Step 1: Provenance

- Worker: INTEG-BREAK red team (subagent, 2026-10-02).
- Parent mandate: attack the three integration breaks from
  H-COMPINTEG-1 (ledger C295, verdict
  COMPOSITION-INTEGRATION-INCOMPLETE): (1) self-referential FACT
  substitution in ts_specialize_src (K3), (2) circular
  self-verification defeating stale revision (K5), (3) value-replay
  vs live-fact execution gap in t2_exec (I5 diagnostic).
- Branch: tnn-native-lab. Commits stay LOCAL, never pushed
  ("Local only, never pushed." appended to messages).
- Report read: composition_integration/REPORT.md (C295).

## Step 2: Commit order self-check

- PREREG.md + this NAMECHECK.md (Step 0 only at freeze time)
  committed ALONE first. No attack implementation (.zag drivers,
  guarded copies, build script, binaries, runs) written before
  that commit. Freeze ordering: PASS (commit hash recorded at
  commit time).
- Prereg freeze is terminal for bars: no weakening, no salvage;
  a blocked arm reports ATTACK-FAILED with its trace.

## Step 3: Build records

(To be filled after the prereg commit: frozen copy sha256 values,
build commands, run digests. Preregistered values the copies must
match, from the C295 report: cc_base
dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6;
un_patch
3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2;
adapt_patch
867bd6d96d9d4026c39d9bc5a9c6944f9ac0427722a3f6451c325c49f60c2ff0;
revise_patch
5113000b1360bf3e978cb106f91f15a1e5956db113eb4b3c26a1ebde1fa7f6e3;
ts_patch
07b7b3952db65b04d8bccf288d28ff0a2aaa899fefd75a1da0250baa7d22b451;
lvcomp_patch
ea833de28d21657b6cb6dcf2ad8c378b6cf604ccbe81680b6acfdcc68e24c302.)

## Step 4: Constraints

- Pure Zag. Zero em/en dashes in lane docs (check_no_dash.sh).
- No `expected` token in new sources (grep audit).
- Guarded copies: 0 new edge/MAP types, 0 new opcodes, 0 modes,
  0 bridges, 0 handlers, 0 new semantic cases. Disclosed additions:
  fact field 44 (learner-origin bit), header slot 40 (prediction
  source id). Guarded copies never leave this lane.
- Paper untouched (TNN_RESEARCH_PAPER_20260929.md).
- Explicit pathspecs. Shared history never amended. Nothing
  pushed.

## Step 5: Verification session

(To be filled after runs: determinism digests, dash audit, grep
audits, guard diff review.)
