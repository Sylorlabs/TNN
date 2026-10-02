# H5R2-DECOY Lane Checklist

Lane: H5R2-DECOY, wave-20261001-2321pdt. Replacement worker for the
H5R2-BASELINE lane, which completed BASELINE-MATCHES via the recency
heuristic and named the missing discriminating world: one where the
NEWEST fact is NOT the LIVE one.

## Step 0: Toolchain guard (mandatory, first)

Setup output from `sh
docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
run at lane startup 2026-10-01 23:56 PDT:

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```

Verification command: `which python3; echo "which-python3-exit=$?"`

Exact output: nothing printed by which, exit code 1
(`which-python3-exit=1`). python3 does NOT resolve in PATH.

Pure Zag only. Shell only: invoke znc, run binaries, git ops,
move/copy files. Forbidden-interpreter invocation = PROCESS-FAIL.

## Step 1: Prereg freeze

Freeze PREREG_DECOY.md alone (with this NAMECHECK.md) before any
implementation work. Kill bars never move after freezing.

## Step 2: Read-only extraction

Extract sources from recorded commits only (git show, read-only):
- H5R2 implementation: 9db334bd4a01d21cce52da3bb2a1c45a10c4c172
  (SHA-256 04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a)
- baselines implementation: 1203b865d
- sealed worlds: e20ba54020dde7e38050dda9e54727d826fc7b45
Do NOT rebuild from working files. Verify hashes before use.

## Step 3: Fresh sealed decoy worlds

Generate FRESH sealed decoy worlds (new seeds; hashes in prereg before
runs). Decoy family: after a revert sequence on key K, a decoy OBSERVE
teaches a NEW fact on an UNRELATED key K2 (newer timestamp, live, but
irrelevant to K's revert); a probe on K requires the revert MAP to
anchor to K's live (older) fact, not the decoy.

## Step 4: Head-to-head run

H5R2 vs REVERT-TO-LATEST vs NO-GATE vs RANDOM-ANCHOR on the decoy
worlds. 3/3 byte-identical reruns per world. Verdict
DECOY-DISCRIMINATES or DECOY-NOT-DISCRIMINATING, reported honestly.

## Step 5: Docs

No em-dashes in any lane doc. Check every doc with
sh docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
before commit. Commit under
docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-DECOY/ only.
