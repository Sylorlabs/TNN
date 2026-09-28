# E51M assembly integrity note

The authoritative native E51M implementation is:

- `01_calibration_curve.zagfrag`
- `02_main_injection.zagfrag`
- `.github/workflows/r32-e51m-native.yml`

The workflow preserves the assembled Zag source, double-built binaries, raw ledger, source hashes, runtime, and the exact workflow used.

## Sealed-confirmation namespace

The historical effective-state allocator has a finite 1,000,003-state namespace. At E51M's maximum 12,960-episode development dose plus 5,400-episode validation partition, attempting to reserve all 10,800 unexecuted confirmation episodes through that allocator can exhaust the remaining collision-free tuples and perform billions of futile probes.

E51M therefore keeps development and validation in the existing effective-state namespace, while the unexecuted confirmation partition receives deterministic nominal IDs during assembly. The workflow records:

- `e51m_sealed_confirmation_nominal_namespace = 1`
- `e51m_sealed_confirmation_effective_streams_reserved = 0`
- `e51m_sealed_confirmation_executed = 0`

Nominal confirmation IDs are never executed. If an E51M arm reaches the exact validation gate, confirmation remains blocked until a separately preregistered expanded executable evaluator namespace is implemented. This infrastructure change does not alter learner-visible features, development data, validation data, targets, fitting, or validation gates.

## Claim boundary

A successful workflow establishes execution integrity only. It does not promote R32, establish dominance over R27, or provide evidence of consciousness or AGI.
