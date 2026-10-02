# NAMECHECK.md - wave-20261002-1121pdt, lane SENSORY

Wave: wave-20261002-1121pdt. Lane: SENSORY. Worker branch: lane-sensory-20261002-1121pdt.
Working copy: ~/workspace/tnn-rsi-work/wave-20261002-1121pdt/sensory/ (sparse, branched from tnn-native-lab tip).
Run dir: docs/lab/rsi/runs/wave-20261002-1121pdt/sensory/.

## Step 0 - toolchain guard (recorded first, before any other work)

Safebin setup run at startup:
```
bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
```
Setup output (verbatim tail):
```
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```
Literal outputs:
- `which python3` => (empty; resolves to NOTHING)
- `which python`  => (empty; resolves to NOTHING)
- `which znc`     => /home/hatch/safebin/znc

Guard: PASS. All subsequent build/run steps use PATH="$HOME/safebin" with
znc resolved from the safebin. No python3/python resolves anywhere on this
PATH. Any forbidden-interpreter invocation would be automatic PROCESS-FAIL
for this lane's wave; none has occurred.

## Step 0b - sparse checkout repair

The worktree's sparse-checkout info file contained a bogus literal
`/--no-checkout/` pattern line, which suppressed checkout of the sparse
dirs (wave-20261002-1121pdt, wave-20261002-0821pdt were missing on disk).
Fixed by removing the line and re-running `git sparse-checkout reapply`.
The 1121pdt run dir is untracked in tnn-native-lab (coordinator created);
it will be created fresh in this lane dir and committed pathspec-only to
this lane branch.

## Provenance inherited this wave

SA lineage: PREREG_SA1 frozen alone at 5305d9195 (wave-20261002-0221pdt);
SA1 implementation + sealed eval at 71c0f6952 (wave-20261002-0521pdt),
VERDICT BUILD-FAIL. Root cause (REDTEAM_SA1.md): speech non-stationarity;
the single global pitch period does not fit 5 s of drifting pitch, so the
harmonic prediction washed out, residual = signal, NEVT = 0 on both
atoms. The prereg's anti-leakage gates worked; the model did not. The
red team prescribed a short-time harmonic model (per-chunk T0, overlap
blend, or pitch-tracked phase lock) as a DIFFERENT mechanism with its own
prereg, not a parameter change. SA1b follows that prescription.

H lineage: PREREG_SENSORY_H4 frozen alone at 983e3073d; H4 implementation
+ sealed eval at 7ce4be8b3 (wave-20261002-0521pdt), VERDICT BUILD-FAIL.
Root cause (REDTEAM_ARTIFACTS_H4.md, SEALED_EVAL_H4.md): cirrus-field
sparsity; the mechanism fired correctly (21,032 bytes darker, all
darkening, terrain-confined, zero sky/moon change, no artifacts) but
covered only 0.67% of pixels, failing KB4/KB5/KB6. The red team noted a
denser field capture would be a NEW prereg (H5), not a patch. H5 follows
that with a genuinely new mechanism (penumbra-dilated shadow field).

Judgment standing: E3 film grain was REJECTED by human eyes
(wave-20261002-0221pdt/E3BLIND); no micro-grain tweaks. H1/H1v2/H2v1/H3
image history recorded in prior lane reports; no recycled renders.
