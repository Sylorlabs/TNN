# NAMECHECK.md - lane HPI, wave-20261002-1121pdt

Lane: HPI. Branch: lane-hpi-20261002-1121pdt.
Worktree: ~/workspace/tnn-rsi-work/wave-20261002-1121pdt/hpi.
Task: queue item 3 / H5R3 implementation (H5R2 revision-chain-through-revert gap).
Frozen prereg: docs/lab/rsi/runs/wave-20261002-0521pdt/HPI/PREREG_H5R3.md
commits bfb01b47e (NAMECHECK Step 0) and b675b1d5a (prereg alone).

## Step 0 - toolchain guard (recorded at lane startup, 2026-10-02 12:08 PDT)

Command: bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
Literal output tail:
  linked: 36 tools
  znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
  verify: python3 absent from safebin PATH (OK)
  verify: python absent from safebin PATH (OK)
  SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)

With PATH="$HOME/safebin":
  `which python3` -> (resolves to NOTHING, exit 1)
  `which znc` -> /home/hatch/safebin/znc

Guard status: PASS. All research logic in pure Zag; shell only invokes
znc, runs binaries, does git ops, moves/copies files.

## Step 1 - provenance and prereg commit-order self-check

Prior lane branch lane-hpi-20261002-0821pdt read for provenance: its
wave went INCOMPLETE after daemon restarts; queue item 1 (F1 re-freeze)
completed; H5R3 carried to this wave per BACKLOG item 2.

Prereg-order check (run before any implementation commit):
  git log --all --oneline --grep H5R3 -> only b675b1d5a
  (FROZEN PREREG_H5R3.md alone, 2026-10-02 12:30:24 UTC).
  bfb01b47e precedes b675b1d5a on the prereg lane.
  No commit containing a tnn3_h5r3 implementation file exists anywhere
  in the repo (git grep over all objects: zero hits).
  Conclusion: PREREG-ORDER-OK. The frozen prereg strictly precedes all
  H5R3 implementation artifacts.

## Step 2 - substrate provenance record (frozen numbers, KB-S1)

Frozen substrate: docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/tnn3_h5r2.zag
at commit 9db334bd4a01d21cce52da3bb2a1c45a10c4c172.
Expected source SHA-256: 04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a.
Expected binary SHA-256: 19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287.
Verified at: 2026-10-02 12:08 PDT lane run.
KB-S1 RESULT: PASS.
- Extracted source SHA-256: 04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a (match).
- Diff vs verified H5R base (tnn3_h5r.zag at 830f95ab7, SHA-256
  d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384):
  exactly the t2_prov_ok gate addition (1 definition at new lines
  508-521) plus the gate at all four t2_trial promote sites
  (5 occurrences of t2_prov_ok: 1 definition + 4 call sites).
  Activate tag-20 admission hunk present (line 156); promote_graph
  carries zero ev_teach_in calls (deletion hunk intact).
- Zero added/removed cognition lines vs frozen H5R2 source: extracted
  file is byte-identical to the committed file at 9db334bd4a.
- Rebuild with pinned znc (src/tools/toolchain/znc_linux_x86_64_abed8aa1):
  3/3 byte-identical builds, each SHA-256
  19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287,
  equal to the committed frozen binary at 9db334bd4a.
- PREREG DEFECT NOTED (not a bar move): the prereg prints the binary
  reference as 19dcf2e4436079a4ab6f9cf48b2b6a556f743d3d9d16102249cd5ac970287
  (61 hex chars, malformed transcription). The operative KB-S1 gate
  (source hash + diff hunks + zero cognition delta) is unaffected; the
  rebuild reproduces the true frozen binary byte-for-byte. Recorded here
  and in SEALED_EVAL.md for the governance audit.

## Step 3 - pinned defect discipline

All Zag work follows the pinned-znc mandatory workarounds:
(1) no _zag_print for dynamic content, one preallocated buffer plus
cursor-returning emit helpers and a single _zag_raw_syscall write,
byte-verify stdout; (2) no as *i32 plus q[0..n] in functions, u8 cells
plus ig/is; (3) no .len trust on cast slices; (4) 2-byte getter for
PCM16; (5) nesting at most 3 deep, hoist call results and conditions
into flag lets; (6) capacity plan nodes under 1024; (7) minimal
ev_query supplied per harness.
