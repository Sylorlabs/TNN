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
- CORRECTION (2026-10-02, post-freeze): the field-44 census above
  was wrong. Node slots are 40 bytes (noff(n)=64+n*40), so field 44
  aliases the next node's field 4; the first guard binary showed
  inverted behavior and the bit was moved to field 12, which is
  verified free on tag-1 FACT nodes (no f12 read on any tag-1 node
  in the six frozen sources). See Step 5 and REPORT.md. The frozen
  prereg text is left unamended; this note records the correction.

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

Frozen copies sha256 (all match preregistered C295 values exactly;
verified at copy time, before any edit):
cc_base dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6;
un_patch 3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2;
adapt_patch 867bd6d96d9d4026c39d9bc5a9c6944f9ac0427722a3f6451c325c49f60c2ff0;
revise_patch 5113000b1360bf3e978cb106f91f15a1e5956db113eb4b3c26a1ebde1fa7f6e3;
ts_patch 07b7b3952db65b04d8bccf288d28ff0a2aaa899fefd75a1da0250baa7d22b451;
lvcomp_patch ea833de28d21657b6cb6dcf2ad8c378b6cf604ccbe81680b6acfdcc68e24c302.

Build commands (both exit 0):
- Attack: cat cc_base.zag un_patch.zag adapt_patch.zag revise_patch.zag
  ts_patch.zag lvcomp_patch.zag integ_patch.zag rt_attack.zag >
  rt_full.zag && znc rt_full.zag -o rt_bin
- Guard: cat cc_base_g.zag un_patch.zag adapt_patch.zag revise_patch.zag
  ts_patch_g.zag lvcomp_patch_g.zag integ_patch.zag rt_guardtest.zag >
  rt_guard_full.zag && znc rt_guard_full.zag -o rt_guard_bin

Run digests (3/3 byte-identical each, cmp-clean):
- rt_bin: c48fe8f07b9fbf09a3b2642e14b0420d5d29034bc3cda37cc83b065f262f8e61
- rt_guard_bin: 5ca49343a0a3296e71b701a885dcbe050e844608becfc36bdddc986293b243c5

Verdicts: T1-ATTACK=PASS T2-ATTACK=PASS T3-ATTACK=PASS;
T1-GUARD=PASS T2-GUARD=PASS T3-GUARD=PASS (rt_run1/2/3.txt, rtg_run1/2/3.txt).

## Step 4: Constraints

- Pure Zag. Zero em/en dashes in lane docs (check_no_dash.sh).
- No `expected` token in new sources (grep audit).
- Guarded copies: 0 new edge/MAP types, 0 new opcodes, 0 modes,
  0 bridges, 0 handlers, 0 new semantic cases. Disclosed additions:
  fact field 12 (learner-origin bit; corrected from 44, see Step 0
  correction), header slot 40 (prediction source id). Guarded copies
  never leave this lane.
- Paper untouched (TNN_RESEARCH_PAPER_20260929.md).
- Explicit pathspecs. Shared history never amended. Nothing
  pushed.

## Step 5: Verification session

- Determinism: rt_bin 3/3 byte-identical (sha256
  c48fe8f07b9fbf09a3b2642e14b0420d5d29034bc3cda37cc83b065f262f8e61);
  rt_guard_bin 3/3 byte-identical (sha256
  5ca49343a0a3296e71b701a885dcbe050e844608becfc36bdddc986293b243c5).
  cmp-clean across all six run files.
- Dash audit: check_no_dash.sh over PREREG.md NAMECHECK.md
  REPORT.md rt_attack.zag rt_guardtest.zag cc_base_g.zag
  ts_patch_g.zag lvcomp_patch_g.zag -- exit 0, no dashes.
- Grep audits: no `expected` token in new driver sources
  (rt_attack.zag, rt_guardtest.zag); occurrences in guarded copies
  are inherited from the frozen base (t2_try_verify/ev_query_revise2
  parameters, comments), not new supervision. No `while.*!(` pattern
  in new Zag (FOURTH-defect check).
- Guard diff review: cc_base_g.zag +50/-0, ts_patch_g.zag +8/-0,
  lvcomp_patch_g.zag +34/-1. No new edge/MAP types, opcodes, modes,
  bridges, handlers, semantic cases.
- Field correction (2026-10-02): the learner-origin bit was moved
  from fact field 44 to fact field 12 after the first guard binary
  showed inverted behavior; root cause is node slots being 40 bytes
  (noff(n)=64+n*40), so field 44 aliases the next node's field 4.
  Field 12 is verified free on tag-1 FACT nodes (no f12 read on any
  tag-1 node in the six sources). Recorded in REPORT.md; the frozen
  PREREG text still says f44 and is left unamended.
- Originals untouched: the six frozen sources were never edited;
  all guard work happened in the _g copies.
