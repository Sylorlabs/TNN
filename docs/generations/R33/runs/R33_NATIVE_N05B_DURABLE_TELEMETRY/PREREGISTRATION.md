# R33-N05B — native allocation corrective durable-telemetry regression

Identity: r33-native-n05b-durable-telemetry-native-allocation-v2.
One primary, 41 supervised children. Native Zag only. No learner or scientific
data, canonical mutation, authority grant, or promotion. N05A remains a frozen
failed experiment; the 40 known N05A engineering shapes are explicitly reused
as corrective controls, not unseen scientific evidence.

## Hypothesis, permitted changes, and pre-exposure evidence

Correct native allocation and alias extents, while preserving four-byte signed
wire encoding, will remove N05A's configuration corruption and allow the same
bounded durable-integration controls to run. The pinned compiler source at
7cacbfc04f6cffec02ea9b1d5ff6702fe2e93f3c, file
selfhost/native/arch/aarch64/acodegen.zag, lines 411–413 and 2161–2187,
defines eight-byte numeric element strides and zalloc_i allocations. Its zfree
is arena-style, not an incremental release; measured process bounds still apply.
This is static source evidence; the prospective runtime stride check is separate.

Allowed: replace n*4 allocation with native zalloc_i and matching zfree;
correct native alias extents to eight bytes; add signed wire-range validation
before mutation; change experiment paths/markers; add the ABI guard and a
tail-of-buffer alias control. All prior fixtures and expected outcomes remain
unchanged. Disk format and N04 accumulator semantics remain unchanged.
Forbidden: N05A/N04 changes; compiler replacement; learner reset/training;
sensor, optimizer, teacher, representation, parent-state or permission changes.

## Exact schedule and pass/fail contract

Inherit the complete 40-case schedule, byte sizes, status codes, failure modes,
resource ceilings and claim boundaries from the frozen
../R33_NATIVE_N05A_DURABLE_TELEMETRY/PREREGISTRATION.md.
Add one `abi` child immediately after invalid mode, before any store creation.
It must observe stride 8, six intact configuration words, intact adjacent 88-
and 168-word buffers after another allocation, exact encoded root configuration,
explicit rejection of out-of-range signed-32 values without output mutation,
and exact minimum/maximum signed-32 roundtrip. Add a refusal for an 88-word slice
at the far end of the accumulator, which the previous four-byte alias extent
could miss. All 41 children and complete terminal counters must pass. Any
unexpected outcome stops subsequent cases, preserves the failure and consumes
this identity. No post-exposure source/oracle editing or same-primary retry.

Success qualifies only trusted, bounded, single-writer process-death telemetry
engineering: at most 16 events, 32 retained attempts, six 64-byte causal slots.
Missing causal evidence remains missing. No actual learner reasoning, full
schema, physical power-cut durability, hostile containment, global freshness,
human authentication, or full continuing-brain qualification is inferred.

## Resource, review, identity, and artifact obligations

Parent guard 60s, ordinary child deadline 15s, intentional kill deadline 1s,
1MiB parent file limit and 256KiB child file limit, no cores, 64 descriptors,
observed child RSS <=256MiB. Actual CPU/wall/RSS are recorded separately from
fixture resource fields. No historical learner, Python, generator, or old
primary is invoked. Shell is limited to compilation, inspection and artifacts.

Main-agent bounded engineering review; no independent scientific/authority
approval is asserted. Freeze compiler, imports, all new sources/protocol/config,
reservation/review, exact build copies and binaries before sole admission.
Preserve native logs/result, failures, checksums, architecture diff, resources,
consumed-registry update, current state, journal and handoff. Continue subsequent
R33 work subject to actual parent/sensor/authority gates, not favorable prose.

Source directory: Research/R33_NATIVE_N05B_DURABLE_TELEMETRY.
Sole run directory: Research/R33_NATIVE_N05B_RUN_PRIMARY_V1.
Launch siblings: Research/R33_NATIVE_N05B_LAUNCH.stdout and .host.stderr.
