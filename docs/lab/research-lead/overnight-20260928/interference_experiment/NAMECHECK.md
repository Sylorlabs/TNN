# NAMECHECK: Memory Interference Experiment

## Step 0: Toolchain guard (mandatory, recorded)

Activation (2026-10-01):
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned nothing. Zero forbidden executables
invoked. All research logic in pure Zag, compiled with the pinned toolchain
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`. Shell used only for znc
invocation, git operations, and file moves. Any forbidden executable
invocation would have been PROCESS-FAIL; none occurred.

## Scope

UNFROZEN VARIANT ONLY. Diagnostic experiment, not a fix.

Task: measure retention of a learned executable structure under graded
interference volume (Micah's lifetime measure: "memory under long
interference"). Confirm/refine the transfer analysis (475c57e23) P4 finding
with a controlled retention curve.

## Input provenance

- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  (verified identical at copy time). NOT MODIFIED.
- Frozen binary: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2_bin`.
  NOT MODIFIED, NOT REBUILT.
- Variant: `interference_experiment/tnn2_interference_variant.zag`.
  Cognition functions byte-identical to frozen; test battery and test main
  removed; interference probes appended. This is the same variant pattern as
  the transfer probes (475c57e23): frozen source with probe main.
- NO cognition changes. NO eviction policy changes. The fixed 3-step
  eviction / directional-bid policy is the object under measurement, not
  the thing being modified.

## Constraints honored

- UNFROZEN ONLY: frozen `tnn2.zag` and `tnn2_bin` untouched (verified).
- Diagnostic, not a fix: no new eviction policy implemented.
- Zero em dashes in all deliverables (byte-verified before commit).
- Paper untouched: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
  not read, not modified.
- No sealed FW/H2 contents inspected.
- Nothing pushed; commits local only.
- Determinism: 3 runs, stdout byte-identical (cmp clean) required.

## Deliverables

- `NAMECHECK.md` (this file)
- `INTERFERENCE_EXPERIMENT.md` (retention curves, white-box eviction analysis)
- `tnn2_interference_variant.zag` (variant source)
- `interference_probes.zag` (probe driver, also appended to variant)
- `tnn2_interference_variant_bin` (compiled probe binary)
- `interf_run1.txt`, `interf_run2.txt`, `interf_run3.txt` (3 byte-identical runs)
