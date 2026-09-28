# R33-B000 analysis and reproduction

Status: analysis procedure only. The
[execution record](R33_B000_EXECUTION_STATUS.json) records a successful native
compile but **zero native fixture executions**. There are no observed audit
values to interpret yet. Expected values in the configuration and parser unit
tests are authored fixtures, never native evidence.

## Read-only preflight

From the repository root:

```sh
python3 -B -m unittest discover -s Research -p 'test_r33_contracts.py' -v
python3 -B Research/r33_validate.py
git diff --check
```

The validator checks the hierarchy, scoped schema, reviews, guarded evidence,
frozen source hashes, exact copied functions, allowed calls and preregistration.
It does not launch the audit, test end-to-end perception, authenticate grants,
or validate a continuing-brain checkpoint. Narrow `.gitignore` exceptions keep
these two external authoring/evaluation scripts visible without allowing Python
cognition. No third-party package or installation is required.

## Compilation and primary execution requirements

The recorded compile used the pinned `znc_macos_arm64_7cacbfc0`, explicit
`--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache`, and the
standalone source. It completed with exit0 and produced binary SHA-256
`31c964cea11f59d4795ad5405985acd3d2954105405d14b90356fc8b9daa6470`.
Compilation wall time was 0.29000366700347513 seconds, measured by an external
monotonic clock. This is not training/inference timing. The temporary binary is
not a retained scientific artifact or a complete compiler qualification.

Do not execute a bare shell command without the protocol's bounded launcher.
Before the primary run, implement/verify the external resource/environment
wrapper, reserve a unique result directory, mark the batch active through the
main-agent registry, and recheck pins. Save exact source/config/compiler/binary
identities, command, environment metadata, raw stdout/stderr, actual exit status,
runtime/CPU/RSS with measurement methods, and interrupted/partial output.
Evolve execution-state validation with rejection tests; do not disable it simply
because the batch has moved beyond `PREREGISTERED_NOT_EXECUTED`.

## Parsing retained native stdout

After a properly admitted native run, the external read-only parser can inspect
the retained CSV:

```sh
python3 -B Research/r33_validate.py --audit-output /absolute/path/to/retained-native-stdout.csv
```

This checks output, not run provenance by itself: bind the CSV hash to the
recorded binary/command/environment first. Parser tests synthesize records in
memory solely to validate rejection behavior. Never copy their output into an
execution artifact. A structurally valid CSV with differing observations is
reported as a mismatch; the top-level repository `PASS` is not witness success.

Analyze each prefix (`visual`, `audio`, `trace`, `lru`, `chunk`) separately.
Confirm raw inputs and positive/full-capacity controls before attributing a
difference to the tested helper. Inspect every trace tuple field, not only its
retained count. Explain a mismatch before any new attempt and retain the negative.
Compiler/backend anomalies and source-level predictions are distinct hypotheses.

## Closeout after actual execution

Preserve immutable output identities and full negative/partial results; update
the fixture-exposure record, experiment registry, resource report, architecture
diff, current state, journal and handoff. Mark subsequent identical executions
as explicit reproduction rather than new evidence. No E51 stage is released or
reused. A confirmed defect motivates a separately registered correction and
qualification; it does not pass S0/S1/S2 or M0–M7 and does not promote R33.
