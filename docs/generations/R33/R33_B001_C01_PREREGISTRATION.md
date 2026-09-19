# R33-B001-C01 — native component regression

Prospective protocol, before any C01 fixture execution. BUILD_01 retains the
initial compile-only draft; review-driven changes compiled as BUILD_02. Neither
binary has run. R27 remains canonical at step60,423, zero restarts. B000 is consumed.

## Question and scope

Do native PCM16LE, RGB8, ordered-event, protected-selection, reconstruction and
in-memory trace components obey their frozen contracts? This does not complete
B001. No learner, historical generator, training, canonical checkpoint, natural
sensor/device or permission grant is admitted. PCM/RGB byte carriers are i32
arrays validated as 0..255. Generic copying intentionally admits all i32 values.

R33_B001_C01_FREEZE.json binds source, configuration, build, evaluator, review and
protocol identities before primary admission. One registry entry and one exclusive
primary directory own execution; no automatic retries or outcome-driven edits.

## Source, changed variables, trainer and hardcoding ledgers

R33_B001_COMPONENTS.zag and R33_B001_C01_DRIVER.zag are new candidate sources;
R32 and B000 code remain untouched. APIs prevalidate lengths/capacities, stage
source values, preserve signed literals and refuse protected victims. The bound
reconstruction entrypoint compares a separate codebook snapshot rather than only
the nominal version. The lower-level version-only helper is not content-bound.
An adversarial caller rewriting both reference and current book is not prevented.
Log checks now inspect IDs, parents and inter-record links, but the initial old
value is not authenticated against an external anchor. Logging is in-memory only.

Human input is authorization to develop/test R33. Architecture-agent choices are
generic envelopes, statuses, literal cases, sentinels and expected outputs. These
are evaluator machinery, not learned knowledge or teacher assistance credited to
TNN. No parameter learning occurs. Each metric names its changed input: value,
format, rate/channels, capacity/shape, order, mask, codebook content/version/alias,
or log field. Separate component checks are not a combined causal learner study.

Namespace: r33-b001-c01-authored-component-v1. No scientific partition or legacy
stage is allocated. B000-shaped cases are intentional regression controls, not
fresh generalization evidence. Build revisions are recorded compilation only.

## Frozen evaluation and falsifiers

77 scalar observations and40 vectors totalling77,986 vector elements. The PCM
oracle checks every one of65,536 codewords against independent signed arithmetic,
not merely inverse-codec self-consistency. The RGB maximum-frame oracle checks
12,288 channel values against `(index*29+11) mod256`. Other cases exercise invalid
carriers, huge shapes rejected before multiplication, alignment, empty and oversized
payloads, extrema, capacity-minus-one/exact/untouched-tail controls, aliases,
same-version mutation/reorder, and log ancestry corruption.

The external parser rejects missing/duplicate/unknown/malformed records and checks
every expected value. Exit0 or audit.completed alone prove no correctness. Empty
PCM is explicitly a successful zero-sample codec call, not a meaningful observation.
Partial-overlap slices, allocator failure, concurrent mutation, protected snapshot
ownership, physical ingestion, provenance and durable reload remain unqualified.
12 external oracle/parser tests passed; those are not native evidence.

## Reviews and dispositions

The completed independent sensory review is R33_B001_SENSORY_REVIEW.md. Its report
of missing oracle/configuration refers to the then-inspected files: both now exist
and are tested. Its criticisms motivated exact content binding, capacity-tail
controls, wider log checks and explicit codec-versus-RawRecord distinctions.
The full independent review remains retained, including unresolved limitations.

The additional safety reviewer did not return a verdict: concurrency failed, then
the resumed task lacked its trusted workspace context. No successful review is
inferred. The main agent reviewed the bounded runner and candidate against the
already-completed R33 safety requirements. Acceptance is for allowlisted non-learning
component tests only, not independent learner-runtime or M2/authority qualification.
The three completed initial independent R33 reviews remain unchanged.

## Authority, resources and attempt conservation

No learner authority level applies. Runtime wall30s, CPU20s, measured RSS256MiB,
per-stream8MiB; compile wall60s. This explicit output envelope accommodates full
independent oracle inputs rather than inheriting B000's64KiB cap. The unchanged
preflighted bounded runner restricts writes/network/fork and clears inherited
environment credentials. File reads are not kernel-isolated; reviewed native
code has no file-read facility. Hard RSS enforcement is unavailable: measured
peak violations invalidate the run. This is not hostile-module containment.

Reserve exclusively before native admission. Interrupted/partial exposure remains
consumed; retain all output and resource charges. No scientific source, expected
value, compiler or consumed primary attempt may be silently replaced. Termination
does not reset a learner because no learner is running.

## Result artifacts, reproduction and next step

Before execution no observed result exists. The primary directory will preserve
reservation/admission, binary, native stdout/stderr, RESULT.json and MANIFEST.json.
The build directory retains exact source and compile logs. Results include measured
resources, all scalar observations, checked-vector counts and mismatch keys; full
native vectors stay in stdout. The registry, consumed ledger, journal, current state
and handoff must agree with those records. Architecture diff: separate components
only, no canonical mutation or adopted learner architecture.

Read-only verification: `python3 -B Research/r33_c01.py --verify`, plus
`python3 -B Research/r33_execution_validate.py` for the unchanged B000 history.
The original authoring validator remains bound to its pre-execution snapshot.
After analysis, continue an actual encoded-byte/metadata path with immutable record
identity and fresh-process reload. Component success is not perception, learning,
full parent migration, durable rollback, B001 completion or R33 promotion.
