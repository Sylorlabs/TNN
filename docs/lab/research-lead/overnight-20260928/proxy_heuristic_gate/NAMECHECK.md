# NAMECHECK: PROXY-HEURISTIC-GATE

## Step 0 -- Toolchain guard (recorded before any implementation)

- `export PATH="$HOME/safebin"` at session start (2026-10-03, this worker).
- `which python3` -> nothing. `which python` -> nothing.
  `which perl` -> nothing. `which ruby` -> nothing. `which node` -> nothing.
- `which znc` -> `/home/hatch/safebin/znc` (pinned compiler).
- Safebin contains 49 allowed tools; python3/python do not resolve.
- All research logic (implementation, builds, runs, verification of
  outputs) in pure Zag compiled by the pinned znc, or in POSIX shell
  for file movement, compilation invocation, hashing, and text
  extraction. No forbidden-interpreter invocation at any point.
- Lane: `docs/lab/research-lead/overnight-20260928/proxy_heuristic_gate/`
- Non-ledger task (claim minting paused).

## Identifier hygiene (new tokens introduced by this lane)

- File prefix `hg_` (heuristic-gate), banner tags `redun3-HG` /
  `redun2a-K3-HG`.
- New functions: `advpaird`, `advpair2d` (dormancy-conditioned MA4b
  detectors; mirror `advpair`/`advpair2` plus the (D) dormancy gate).
- New arena tallies: `advkilld` (3687364), `advkill2d` (3687368),
  carved from the documented-unused 64-byte region at 3687364.
- New output fields: `ADVKILLD=`, `ADVKILL2D=`.
- No changes to existing identifiers, functions, or tallies. The
  redun3 proxy is untouched (per task constraint); `advpair` and
  `advpair2` are untouched.
