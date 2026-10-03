# NAMECHECK: PROXY-WINDOW-PRINCIPLED

## Step 0 -- Toolchain guard (recorded before any implementation)

- `export PATH="$HOME/safebin"` at session start (2026-10-03, this worker).
- `which python3` -> nothing. `which python` -> nothing.
  `which perl` -> nothing. `which ruby` -> nothing. `which node` -> nothing.
- `which znc` -> `/home/hatch/safebin/znc` (pinned compiler, 2026.07.0-dev).
- Safebin-only PATH throughout; zero forbidden-executable invocations.
- All research logic (implementation, builds, runs, verification of
  outputs) in pure Zag compiled by the pinned znc, or in POSIX shell
  for file movement, compilation invocation, hashing, and text
  extraction. No forbidden-interpreter invocation at any point.
- Lane: `docs/lab/research-lead/overnight-20260928/proxy_window_principled/`
- Non-ledger task (claim minting paused).
- Parent caveat under test: PROXY-HEURISTIC-GATE closed as
  HEURISTIC-GATE-ALIGNED with the caveat "The 60-episode window
  itself remains unprincipled (inherited, not tested)."

## Base and lineage

- Base files: `pr_w6.zag`, `pr_t1.zag`, `pr_t2.zag`, `pr_t3.zag`,
  `pr_t4.zag` from PROXY-REDESIGN (the 5-stream K=3-driven shadow
  setup where the B8 dormancy table was measured). Rationale: the
  window's discrimination is fully specified by the B8 table; the
  shadow setup (K=3 drives, redun3 write-only) is the only
  configuration where a window sweep is provably non-interfering
  (all shadows write-only, loop trajectory invariant to W). The
  redun3 code is byte-identical (frozen) across PROXY-REDESIGN,
  PROXY-CLOSEDLOOP, and PROXY-HEURISTIC-GATE, so this continues the
  HEURISTIC-GATE-ALIGNED investigation line without redesigning.
- This lane does NOT modify the redun3 proxy (per task constraint).
  Window-parameterized shadows (`redun3w`) run alongside untouched
  `redun3`, following the PROXY-HEURISTIC-GATE twin pattern.

## Identifier hygiene (new tokens introduced by this lane)

- File prefix `pw_` (proxy-window), banner tag `-PW`.
- New function: `redun3w` (window-parameterized twin of `redun3`;
  byte-identical body, window W as parameter instead of literal 60).
- New function: `pw_learn` (max-margin window from win-recency
  distribution at a PX audit point; harness-side, write-only).
- New arena: `pwn` (3689000), `pwlog[32]` at 3689004 (window-sweep
  audit log; carved after the documented arena end at 3688988,
  inside the 4MB G allocation).
- New output section: `PW` lines (per-record sweep results).
- No changes to existing identifiers, functions, or tallies.
