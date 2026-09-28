# R32 E45 ARM64 7cac aggregate ABI diagnostic

Classification: **non-qualification deployment evidence**.

This record isolates one compiler-transport question raised by the frozen R32
E45 evaluator-clean source SHA-256
`4de5785de37b02ad6e948e06381f310246a7738cb0c1a3f3887e3bf42cec1636`
and core SHA-256
`6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0`.
It is not a qualification run and does not change either source.

## Result

The official preserved ARM compiler
`znc_macos_arm64_7cacbfc0` (SHA-256
`3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`)
compiled the exact probe twice with deterministic flags. The two Mach-O ARM64
binaries were byte-identical, SHA-256
`197b6d7c72b3b623ccc7bc5401fa9c6f71bf05417adee30a7b45190942785256`.
The preserved binary printed the expected checksum `4065` and exited 0.

The probe places a 21-compiler-word context at the supported call boundary:
nine slices, two scalar pointers, and one scalar. It calls one function with the
context by value plus seven scalar arguments and another with a context pointer
plus seven scalar arguments. Both calls therefore have exactly eight source
arguments. Far context fields are read and writes through slice/pointer fields
are checked after return.

This supports a bounded repair strategy: replace each executed call above eight
source arguments with at most five parameters composed from small immutable
contexts and pointers to mutable contexts. Prefer context pointers on hot paths
to avoid aggregate copies.

## Frozen wide-call map

The frozen 4de5785d graph has 12 reachable declarations above eight parameters
and 32 executed call sites:

| Callee | Parameters | Executed sites | Proposed grouping |
| --- | ---: | ---: | --- |
| `r32e45_temporal_observe` | 19 | 3 | observation + state-reference context + policy context |
| `r32e45_option_begin` | 17 | 1 | begin input + option-state references |
| `r32e45_option_record` | 10 | 1 | observation + progress references |
| `r32e45_option_value_generic` | 9 | 5 | features + weights |
| `r32e45_option_value_logical` | 9 | 4 | features + weights |
| `r32e45_option_value_full` | 15 | 3 | features + weights |
| `e45_state_initialize` | 10 | 1 | state work + history + source model |
| `e45_state_observe` | 11 | 2 | state work + evidence step + source/hazard model |
| `e45_fill_full_features` | 10 | 8 | feature view + step scalars + output |
| `e45_build_state_tape` | 18 | 2 | evidence bundle + source/hazard model + state-tape work |
| `e45_train_episode` | 17 | 1 | train spec + learner state + mutable scalar refs + policy model |
| `e45_evaluate_arm_episode` | 17 | 1 | evaluation spec + learner state + scalar bias + policy model + metrics |

`e45_make_world` has 14 parameters but is not reachable from `main`; it has no
executed call site in the frozen source.

The largest proposed by-value context is the 18-word evidence bundle containing
nine slices. The diagnostic deliberately uses a larger 21-word aggregate. This
does not prove arbitrary aggregate sizes or nested aggregate behavior.

## Reproduction

Compiler version: `znc 2026.07.0-dev (edition 2026)`.

Build flags:

```text
--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache
```

Expected probe result:

```text
4065
exit 0
```

The build logs preserve the exact commands and emitted compiler messages. The
run log records stdout, exit status, and one timing observation.

## Limitations

This evidence establishes only that the exact isolated probe compiles and runs
with the preserved official ARM compiler, and that two builds are byte-identical.
It does **not** establish any of the following:

- support or correctness for calls with more than eight source arguments;
- successful compilation or execution of the R32 E45 qualification harness;
- ARM/x86 numerical parity;
- model, evaluator, training, causal, warrant, or qualification correctness;
- general aggregate ABI correctness beyond the exercised shapes and operations;
- memory-safety, bounds-safety, leak-freedom, optimization, or performance;
- reproducibility under another compiler binary, target, edition, or flag set.

The preserved binary is diagnostic evidence only and must not be cited as a
qualification artifact.
