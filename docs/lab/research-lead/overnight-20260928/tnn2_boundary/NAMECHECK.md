# NAMECHECK: TNN-2 Capability Boundary Map

Date: 2026-10-01. Worker: TNN-2 Capability Boundary Mapper.
Target: frozen TNN-2 binary/source, commit `f4de7ff46`
(`docs/lab/research-lead/overnight-20260928/tnn2_build/`).
Owned path: `docs/lab/research-lead/overnight-20260928/tnn2_boundary/`
(probes, NAMECHECK.md, BOUNDARY_MAP.md only).

## Step 0: Toolchain guard (mandatory)

- Ran the repo's `safebin_setup/setup_safebin.sh` (first attempt ran under
  the restricted PATH and missed `ln`; re-ran with `ln` resolvable, then
  re-locked `PATH="$HOME/safebin"`).
- safebin: 36 tools + pinned znc
  (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`); setup script prints
  SAFEBIN-READY.
- Verified under the restricted PATH: `command -v python3 python` prints
  nothing. `which python3 python` likewise resolves nothing.
- All probe computation in Zag via pinned znc. Shell used only to invoke
  znc, run probe binaries, do git operations, and move/copy files.
- Zero Python/C/C++/JS/Rust invocations in this wave. No forbidden
  executable was invoked: no PROCESS-FAIL condition arose.

## Method: probe harness (read-only on frozen source)

- The frozen binary runs a fixed self-test suite and ignores CLI args, so
  behavioral probes are compiled as separate Zag programs:
  `probes/base.zag` is a byte-identical copy of the frozen `tnn2.zag`
  (SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  verified equal to the frozen source hash).
- Each probe `pN.zag` = `base.zag` with ONLY the single line
  `fn main()i32 { return run_all(); }` mechanically replaced by a probe
  `main`. No other line of the frozen source is touched. The frozen
  `tnn2_build/` directory is never written to.
- Fidelity check: probe `p0` runs the unmodified `run_all()` suite and must
  reproduce 46/46 before any boundary claim is trusted.
- Probes drive the public event paths (`ev_teach`, `ev_query`,
  `ev_observe`, `ev_act`, `ctx_push`) plus white-box readers
  (`t2_exec`, `t2_sig`, `map_standing`, `hg`) to observe learner state.
- Each probe binary is run 3 times; outputs must be byte-identical
  (determinism check) before results are recorded.
- No sealed FW1-FW9 assets are inspected or referenced. Probes use fresh
  synthetic scenarios only.

## Probe index

- p0: harness fidelity (run_all 46/46, 3x byte-identical)
- pA: construction depth ceiling (2..6 hop chains)
- pB: sum path with/without comb node; sum cap 800 vs 950
- pC: masked first-guess on diamond
- pD: inquiry accumulation, selection, no-resolution
- pE: revision (terminal patch, second patch, revert, interior contradiction)
- pF: composition (no CALL; fresh flat re-assembly; tag census)
- pG: novelty (diamond-sum, subtraction, count isolation)
- pH: memory pressure + determinism
- pI: guide bid selection and interference
- pJ: no-feedback inertness (expected=-2)

## Verdict

BOUNDARY-MAP-COMPLETE (recorded in BOUNDARY_MAP.md and commit message).
