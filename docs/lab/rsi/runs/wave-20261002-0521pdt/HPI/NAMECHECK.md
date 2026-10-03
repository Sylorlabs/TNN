# NAMECHECK: wave-20261002-0521pdt HPI lane (H5R3 fresh prereg, Option A)

Lane dir: docs/lab/rsi/runs/wave-20261002-0521pdt/HPI/
Task: TNN RSI wave-20261002-0521pdt, lane HPI, H5R fresh prereg Option A
(backlog item 24). Deliverable this wave: fresh prereg PREREG_H5R3.md
frozen alone; implementation plan included; implementation queues next
wave.

## Step 0: worker toolchain guard (mandatory first, recorded before any work)

- Ran docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh.
  Output: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).
- PATH exported as $HOME/safebin for all subsequent commands.
- `which python3` returns nothing (exit 1). `which python` returns nothing.
- Pinned znc present: src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (verified by setup script: znc OK).
- Pure Zag only. Shell only for znc invocation, binaries, git ops, file
  moves. Pinned znc constraints honored: no `as *i32` plus q[0..n] slice
  construction in any new Zag code; u8 cell loop idiom only.
- Any forbidden executable invocation is automatic PROCESS-FAIL.

## Step 1: lane history read (before writing the prereg)

Read in full: the H5R2-SYNTH prereg
(docs/lab/rsi/runs/wave-20261002-0221pdt/HPI/PREREG_H5R2_SYNTH.md), the
H-PI-REV2 step-5 re-execution (REEXEC_STEP5.md), the H5R prereg and
sealed eval (wave-20261001-2021pdt/TNN3H5R/PREREG_H5R.md,
SEALED_EVAL_H5R.md), and the H5R2 prereg and sealed eval
(wave-20261001-2321pdt/TNN3H5R/PREREG_H5R2.md, SEALED_EVAL_H5R2.md).

Key facts carried into the fresh prereg:
- H5 KILLED: shadow fact on the MAP key made MAP supersession
  behaviorally inert.
- H5R KILLED on KB-W2R 8/12: revert MAPs anchored DEP edges to
  superseded facts, breaking the DEP based revision chain. Root cause:
  t2_trial accepted the first verifying candidate in BFS/node-id order
  with no liveness check on licensing facts.
- H5R2 ADVANCED (BUILD-PASS): the t2_prov_ok provenance gate (a
  superseded fact licenses nothing) corrected the flaw. KB-W2R 12/12,
  KB-W3 8/8, KB-B2R 24/24, KB-B3 24/24. The honest scope note: H5R2's
  worlds never contradicted the reverted fact after a revert, so the
  full cycle through the revert step is untested. That gap is exactly
  what this wave's fresh prereg targets.
- H5R2-SYNTH BUILD-FAIL: the newest-live-among-all-live gate showed the
  pre-registered newest-bias failure signature; no tie-breaking rule is
  crowned. Not repeated here.

## Step 2: seeds (chosen pre-freeze)

- y1: "TNN3H5R3|wave-20261002-0521pdt|world-y1",
  sha256 b303b30cbc6109141d3560b4797517fa63b83f8b91e9dc5e5874a740fa4de0b6,
  first byte 0xb3 = 179, vo = 179 mod 7 = 4.
- y2: "TNN3H5R3|wave-20261002-0521pdt|world-y2",
  sha256 bf14edcd3f5707352e1b400ed80d1bec5472e3b5b7a06cc2e7769e17aa786813,
  first byte 0xbf = 191, vo = 191 mod 7 = 2.
Computed with safebin sha256sum; no python involved.

## Commit order record

- This NAMECHECK.md is committed first, alone (process record, not
  implementation).
- PREREG_H5R3.md is committed second, alone (the prereg freeze).
- Both strictly precede any H5R3 implementation artifact. Any
  implementation whose mtime predates the prereg freeze commit is
  UNVERIFIABLE ORDERING and the evaluation is VOID.

No em-dashes or en-dashes in this file (checked with check_no_dash.sh
before commit).
