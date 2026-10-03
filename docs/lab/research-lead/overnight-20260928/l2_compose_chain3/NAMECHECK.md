# NAMECHECK: L2-COMPOSE-CHAIN3 (3-operator chain probe)

Worker: L2-COMPOSE-CHAIN3 subagent (depth 2/2), 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/l2_compose_chain3/`
Non-ledger task (claim minting paused): wave verdict only.

## Step 0: Toolchain guard (worker startup)

- Safebin activated: `export PATH="$HOME/safebin"` at startup.
- `~/safebin` contains 51 tools; grep for
  python|perl|ruby|node returns nothing.
- `which python3` under the safebin PATH returns
  nothing (exit 1). No python3/python available.
- Pinned compiler: `~/safebin/znc`, version
  `znc 2026.07.0-dev (edition 2026)`.
- All computational research operations in this wave
  use Zag compiled with the pinned znc. Shell is used
  only to invoke znc, run binaries, do git ops, and
  move/copy files. No forbidden executable will be
  invoked; if one ever is, this wave is automatically
  PROCESS-FAIL per the worker toolchain guard.

## Scope

Build on the phase-2 design from L2-METAREUSE-COMPOSE-2
(the extended learner.zag, sha256
6e8ed1e047e9dee8311a264aaec9a995ddbb723f5b284e21c18baa0e68038ddd).
The compose2, adversary, and builder lane directories
are never modified. Commits local with explicit
pathspecs; nothing pushed.

## Key design decision (frozen before implementation)

The learner is used BYTE-IDENTICAL to compose2's
extended learner (sha256-verified copy; zero source
changes, not even comments). Phase 2 already retries
the fixed [1..6] enumeration over ALL Z sources in
ZSRC_IDS, including Z MAPs built by an earlier
query's phase 2. The 3-chain question is therefore
answered by world/driver design alone: no learner
change is the strongest possible test that the frozen
phase-2 mechanism composes 3-deep with termination
T1-T6 intact.
