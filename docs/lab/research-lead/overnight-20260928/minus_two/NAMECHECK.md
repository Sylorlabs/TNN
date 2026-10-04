# NAMECHECK.md - Minus-Two Disambiguator

## Step 0: Toolchain Guard

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 18 allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` applied before all work.
- `which python3 python` returned nothing (empty output). Zero forbidden executables invoked.
- All computation in pure Zag via pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- Shell used only for: invoking znc, running binaries, git operations, moving/copying files.

**Result: GUARD-PASS. No violations. No near-misses.**

## Scope

Measurement and analysis ONLY. This worker:
- Reads frozen TNN-2 source (read-only).
- Builds drivers on VERBATIM copies (SHA-256 verified identical before modification of the copy).
- Instruments the COPY for white-box logging (header 52 bitmask). Frozen original untouched.
- Does NOT modify frozen `tnn2.zag`, `tnn2_bin`, or build `f4de7ff46`.
- Does NOT design implementations or propose architecture changes.

## Input Provenance

- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  - SHA-256: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  - Verbatim copy `m2_base.zag`: same hash, verified before and after copy.
  - Instrumented copy `m2_inst.zag`: derived from verbatim copy; frozen original never touched.
- Decline signal analysis: commit `9e0ae81d1` ("The -2 is pipeline exhaust, not a cognitive choice").
- No sealed worlds opened. No FW/H2 contents inspected.

## Behavior Preservation

- Same 12-query battery run on instrumented copy and uninstrumented verbatim copy.
- All 12 `v=` return values byte-identical between versions.
- Instrumentation (header-52 bitmask, `m2_mark` calls) is non-invasive: sets bits only, never alters control flow.
- 3/3 byte-identical runs of instrumented driver (SHA-256 `db97f21f9971fc234e8bc2a907947df76ed6110eb288c204d9130c660a20cb07`).

## Constraints

- Zero em dashes (byte-verified via grep for U+2014).
- Paper `TNN_RESEARCH_PAPER_20260929.md` untouched.
- Nothing pushed. All commits local to `tnn-native-lab`.
- Verdict: MINUS-TWO-COMPLETE with path frequencies.
