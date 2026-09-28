# FREEZE RECORD — RNGSCAN-2026-09-20-v2

Frozen: 2026-09-20, after the scored dirty round (5/5) and clean round (PASS)
both completed on this exact source. Attestation rerun determinism verified
(byte-identical).

## Frozen artifacts

- `checker/rngscan_v2.zag`
  sha256: `ee962e53817c81721996a8086c5e42530da07316250b1a4906ab74a56a3d9e5d`
- checker binary (build artifact, NOT committed)
  sha256: `9bbaf5390f140a88516d6f1912bc060610bd773af32406f7fd935c5281c41943`
  built with `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- `runner/run_audit.sh` — RUNAUDIT-2026-09-20-v1 (deterministic shell glue)
- scored-round evidence: `results/` (5 dirty + 1 clean attestations)

## Binding rule

No edits to `checker/rngscan_v2.zag` after this point. Any edit — however
small — invalidates the freeze and restarts the dirty round (5/5) and the
clean round from scratch. The blind red-team round (20 plants, separate
agent) must run against this frozen source and binary, unmodified.

## Kill criteria (prereg §8, binding)

- K1: any replay divergence on an audit-PASS build kills v2.
- K2: any blind-plant miss among the 20 kills v2.
- K3: any banned construct found post hoc on a PASS path kills v2.
