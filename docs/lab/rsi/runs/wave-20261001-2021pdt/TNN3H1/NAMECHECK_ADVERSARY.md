# NAMECHECK_ADVERSARY: wave-20261001-2021pdt, lane TNN3H1-ADVERSARY

Independent adversary for the sealed evaluation of the H1 implementation.
This worker is independent of the TNN3H1 prereg worker and the TNN3H1-IMPL
builder worker. It has not read their implementation files beyond the
committed prereg (PREREG_H1.md, commit 1942eb51b), the transparent
amendment (AMENDMENT_H1_DELTA.md, commit 6e31a6c3c), the published
white-box signature (handle cell tag 904 + NAME edge type 11 to a sequence
root), and the lane NAMECHECK.md governance/Step-0 record (for toolchain
context only).

## Step 0: toolchain guard (safebin activation, adversary worker)

- Date: 2026-10-01 20:45 PDT (Thu)
- Ran: `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
- Result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python); znc OK
  (pinned /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
- Exported PATH="$HOME/safebin" (safebin only) in every shell.
- `which python3` prints NOTHING (exit 1, verified empty output).
- `which python` prints NOTHING (exit 1, verified empty output).
- No Python, C/C++, JavaScript, or Rust will be used for research logic in
  this lane. Shell only invokes the pinned znc, runs binaries (the frozen
  tnn3_bin plus pure-Zag adversary-built binaries), performs git ops, and
  moves/copies files. Any forbidden executable invocation is automatic
  PROCESS-FAIL and will be reported honestly.

## Step 0b: binary identity gate (before any sealed run)

- Expected frozen binary SHA-256 (from IMPLEMENTATION.md Step 2 record):
  ac715d080a7e67bbab4694feee66ad5973140d3e58095dcb88b687e55613d2db
- This worker re-verifies the hash of
  docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H1/tnn3_bin itself before
  running anything. If the hash does not match, the worker stops and
  reports BLOCKED. Recorded in SEALED_EVAL.md.

## Step 1: working copy

- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab
  (verified via `git branch --show-current` at worker start).
- Lane directory: docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H1/
- This worker writes ONLY new files inside the lane directory:
  NAMECHECK_ADVERSARY.md (this file), SEALED_C1.md, SEALED_C2.md,
  SEALED_C3.md, SEALED_EVAL.md. It does not modify any existing lane file.
- No git push, no git reset --hard, no rebase, no git commit by this
  worker; the coordinator commits at wave end.

## Step 2: independence declaration

- The sealed worlds (Families C1, C2, C3) are designed post-freeze from the
  frozen prereg's family descriptions only. This worker has not seen the
  builder's dev worlds (h1_dev.zag and its logs were not opened).
- Sealed world files are new files authored by this worker; their SHA-256
  hashes are recorded in SEALED_C1.md / SEALED_C2.md / SEALED_C3.md BEFORE
  the sealed run. The coordinator holds the worlds; the builder lane
  receives only execution transcripts and white-box dumps.
- Anti-smuggling: after the run, grep the white-box dumps and the frozen
  binary's transcript for adversary-recorded id tokens to confirm no
  world-specific ids were smuggled into the implementation (per prereg
  section 4.4 the grep is over the implementation diff; as an adversary
  without diff-write access, this worker greps transcripts and dumps for
  token misuse instead).
