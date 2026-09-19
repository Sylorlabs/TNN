# V91 native historical-generator qualification sidecar

This directory contains the pure-Zag reconstruction and frozen qualification
for the historical R23 semantic generator retained inside the R27 continuity
work.

## Closed milestones

- exact historical R23 source/state/summary recovered
- dataset/order reconstruction: 16/16 intended rows
- naive n=1 generation: 16/16 exact historical strings
- semantic roundtrip n=128 generation/reranking: 16/16 exact historical strings
- deterministic repeat of the full roundtrip generated frame
- inference/oracle structural isolation
- canonical R27 unchanged

Latest frozen evidence:

`evidence/RECOVERY_EXACT_ROUNDTRIP_20260918T051756Z`

Latest generated roundtrip frame SHA-256:

`3a2f4075ad758f9481bdc6f6f5cff75dc044b0a69e3ee14e6280c3f309d253f5`

## Requalification

Run from this directory with a fresh evidence destination:

```sh
zsh qualify_native_roundtrip_recovery.zsh evidence/RECOVERY_EXACT_ROUNDTRIP_<UTC_TIMESTAMP>
```

The evidence directory must not already exist. Qualification freezes author
sources and historical source custody, projects native import closure, builds
with the pinned compiler, reconstructs conditions, performs isolated native
inference twice, checks byte-identical determinism, opens historical oracle
custody only after inference artifacts exist, compares all 16 rows, verifies
canonical R27 before/after identity and seals SHA256SUMS.

Pinned compiler:

`/Users/Shared/micah/Documents/zag/znc`

SHA-256:

`3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`

Historical Python source is inert specification only. No Python, PyTorch,
TensorFlow, JAX, NumPy, Hugging Face, pickle execution or foreign ML runtime is
used in the qualification path.

## Claim boundary

The historical V91 evaluation generator paths are reconstructed. This does not
open `learn`, promote a successor, mutate canonical R27, or establish broader
architecture-versus-LLM claims. Full N17 continuity remains fail-closed while
R25/R26 source/member dependencies remain unresolved and until the ordered
independent review is complete.

See `V91_STATUS.md` for the evidence identities and exact boundary.
