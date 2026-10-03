# NAMECHECK: BATTERY-M2W2RERUN (wave-20261001-2021pdt, lane BATTERY)

Worker role: research worker for wave wave-20261001-2021pdt, lane
BATTERY-M2W2RERUN (M2-W2 fresh-state re-run under the frozen amendment).
Independence note: I am independent of the BATTERY-M2W2FIX amendment
author. I implement from the frozen amendment text only
(AMENDMENT_M2W2.md, frozen at c3a753abe). I did not author, edit, or
preview the amendment design before its commit.

## Step 0 (toolchain guard)

1. Ran `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   (the task's relative path resolved to this absolute path; the first
   attempt from `~` failed with no such file, and the file was located
   inside the working copy with find).
2. Safebin activated: `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
   Pinned znc resolves from safebin:
   `/home/hatch/safebin/znc` -> pinned
   `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
3. `which python3` prints NOTHING (exit 1). `which python` prints NOTHING
   (exit 1). Guard check: PASS, not blocked.
4. PURE ZAG ONLY commitment: shell invokes only the pinned znc (via
   safebin), runs prebuilt pure-Zag binaries, git read-only ops, and file
   moves/copies. No new Zag code is compiled for this re-run (all tools
   are prebuilt frozen artifacts; no new source is authored). Any
   forbidden executable invocation is automatic PROCESS-FAIL and will be
   reported honestly.

## Order and scope commitments

- Commit-order self-check: amendment c3a753abe ("FREEZE M2-W2 amendment")
  was committed before any M2W2R_ artifact. Verified: `git log` shows
  c3a753abe precedes HEAD effcce4d; prereg freeze d43fe32c5 precedes the
  amendment. All M2W2R_ files first appear in the working tree AFTER
  c3a753abe (new files only; no such files exist at or before that
  commit). Filesystem mtimes recorded in M2W2R_RUN_LOG.md.
- Scope: write ONLY inside
  `docs/lab/rsi/runs/wave-20261001-2021pdt/BATTERY/`, new files only,
  prefix `M2W2R_` (this NAMECHECK file is the lane-required namecheck
  document, excepted by task instruction). No modification of existing
  lane files. No commits, no pushes, no `git reset --hard`, no rebase.
- World file `m2w2v2_world.txt` content UNCHANGED (hash verified against
  WORLD_MANIFEST_V2.sha256 before the re-run).
- Frozen binaries verified before runs (shim hash; tnn2.zag hash; git
  status on frozen cognition paths).
- Documentation rule: no em-dashes in any written file.

## Declaration of planned protocol (frozen amendment section 3, verbatim)

1. Fresh state A: run M2-W1 per the prereg (template plus envelope_r,
   driver log saved), exactly as in the v2 validation. State A persists.
2. Fresh state B (separate state file, never chained from state A):
   remove any prior state-B file; run the M2-W2 world
   (`m2w2v2_world.txt`, UNCHANGED) on fresh state B with the frozen
   `freeze_shim2_bin`; save stdout as the M2-W2 transcript. Executed 3
   times from fresh state; 3 transcripts byte-identical (sha256 equality).
3. Continue state A: run M2-W3 on the post-W1 state (W1 -> W3 chain).
4. N recorded as the measured parameter from step 2's baseline ACT
   (expected 0); carried to the M2-W3 scorer as a parameter
   (`BAR=M2W3:M=<M>:N=<N>`), replacing the contaminated in-chain N=30.
5. Calibration controls for M2-W2 (D1 constant-action, D2 stale-action,
   C miss/hit responder) re-run on the fresh-state configuration BEFORE
   any mechanism verdict. Gates: D1 must not pass (WORLD-INVALID by
   validity or FAIL), D2 must FAIL, C must PASS. Any gate failure voids
   the amended M2-W2 as a battery defect.
6. Amended K-S9v2 scored: PASS iff post-resolution ACT == N (fresh-state
   baseline); validity: pre-resolution ACT != N, else WORLD-INVALID.
   Predicted for frozen mechanisms: N=0, pre=30, post=30 (stale), FAIL.
7. Collateral-probe restatements applied exactly as specified (M2-W2 two
   probes and M2-W3 44111 probe expect the miss response M as engagement
   probes; retention claims withdrawn; K-S14v2 denominator stays 12).
8. Unexpected-PASS rule: a frozen-mechanism PASS of amended K-S9v2 voids
   the world as a battery defect (not a vindication).
