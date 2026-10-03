# NAMECHECK: ddes-refreeze worker, wave 20261001-0821pdt

Worker role: ddes-refreeze (DDES follow-up V2 re-freeze).
Phase 1: fresh prereg only. No implementation, no execution.
Working directory: docs/lab/rsi/runs/wave-20261001-0821pdt/ddes/
Branch: tnn-native-lab. Commits stay local, never push.
This lane does NOT commit; the coordinator commits the prereg freeze.

## Step 0: toolchain guard activation (per AGENTS.md worker toolchain guard)

Exact commands run, in order, and their outputs:

1. `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   Output:
   ```
   safebin: /home/hatch/safebin
   linked: 36 tools
   znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
   verify: python3 absent from safebin PATH (OK)
   verify: python absent from safebin PATH (OK)
   SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
   ```
2. `export PATH="$HOME/safebin"` in every shell session this wave.
3. `which python3` -> NOT FOUND (no output, nonzero status; verified absent).
4. `command -v python` -> NOT FOUND (no output; verified absent).

PURE ZAG ONLY for this lane: no Python anywhere (not glue, not analysis,
not verifiers, not harnesses). Shell only: invoke znc, run binaries,
git ops, move/copy files. Phase 1 writes documentation only; no
implementation file was written and no binary was executed.

Zag idiom acknowledged: never use `as *i32` + `q[0..n]` slice
construction inside functions (pinned znc miscompiles it); use
u8-backed cells with little-endian get32/set32 helpers. This will
govern the phase 2 implementation.

## Step 1: forbidden-executable audit (updated at wave end)

- Phase 1 tool use: shell tools only (bash for safebin setup; grep,
  sed, cat, head, tail, ls, find for reading prior preregs, evidence,
  and the broken ddesp.zag). No znc invocation, no binary execution,
  no git mutation by this lane.
- Zero Python invocations in phase 1. Zero forbidden executables
  invoked in phase 1.
- (Wave-end update goes here after phase 2: full audit of every
  executable invoked across both phases.)

## Scope

- PREREG_DDES_FOLLOWUP_V2.md: fresh prereg, written this phase, to be
  committed ALONE by the coordinator (prereg commit strictly precedes
  any implementation commit).
- Phase 2 (implementation ddesp2.zag + sealed execution) starts only on
  the follow-up authorization message.
- Supersedes the retired 2021pdt prereg
  (docs/lab/rsi/runs/wave-20260930-2021pdt/ddes_followup/PREREG_DDES_FOLLOWUP.md),
  judged BUILD-FAIL + UNVERIFIABLE ORDERING in LOOP_STATE.md
  (wave wave-20261001-0221pdt): its ddesp.zag does not compile under
  the pinned znc (ddes_world takes 15 params, 6 call sites pass 14;
  phase B never wired) and prereg plus implementation shared commit
  904e9b6f6.
