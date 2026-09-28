# R33-N04: native competency telemetry V2 engineering qualification

Identity r33-native-n04-telemetry-v2-local-abi-v1. No existing N04 allocation or
primary was found. One primary with two supervised child invocations: invalid
mode must exit2 silently; check mode must finish all eight named assertion groups
with exit0, no mismatching ASSERT and the complete V2 zero-failure marker.
Parent emits27 CHECK rows and N04_TELEMETRY_V2_ENGINEERING_PASS,8 on success.

## Exact changes and scope

The inherited V1 telemetry and original test remain preserved and unexecuted.
V2 retains the88-word event/16-word header/56-row snapshot ABI. Its only semantic
change removes the requirement that every refusal record claim a new request:
a separately logged refusal may set request-occurrence0 just like a delivery
response. Learner request records still require occurrence1. Producers remain
responsible for honest occurrence attribution; this is not a pending-request
matching/authentication engine.

TEST_V2 copies the seven existing groups without changing their expectations,
mechanically renames their schema identifiers, and defines the renamed ABI
constants locally from literal numbers. A static text comparison verified that
all local declarations exactly match the specification's numeric mapping.
Imported numeric constants are absent from test sizes, offsets and oracles;
N01P remains the failed interface evidence, not a repaired compiler. Local
state-capacity preflight precedes allocation/writes. The eighth group records
request then refusal-response and requires requests1/refusals1/interventions0/
dose0; malformed request and intervention-bearing refusal stay rejected, and
exact reconstruction is checked.

The seven inherited groups cover initialization/missingness; identity/exposure;
assessment/help; pointwise retention; retrieval/resources;16-anchor capacity;
alias, full128-event capacity and reconstruction. All groups retain byte/word
state checks after refusals. Exact assertions and loop coverage are frozen in
the source; observed row count is reported, not estimated from source call sites.

## Reviewed boundaries and potential confounds

Main-agent code review uses complete V1/V2 code, original design/tests, trainer
and white-box contracts, and N01P/N03A results. Reuse of the prior telemetry agent
returned not-found; a new independent reviewer spawn failed the agent limit.
Neither counts as an independent verdict. This is bounded engineering admission,
not discharge of a scientific/authority independent-review gate.

Local fixture digests are supplied byte tags, not SHA bindings to raw sensory
data. Freshness is only within this accumulator's log, not the historical parent
or source-group held-out population. Help/refusal counts follow declared records,
not verified human intent. Interference is recorded association, not a causal
effect estimate. Resource measurements in synthetic records are fixture values;
actual process CPU/RSS/wall are separately captured by the supervisor. Unsupported
understanding, teacher competence, transfer and calibration remain unmeasured.
This component is not durable, authenticated, a full schema adapter, or a brain.

## Build, resource and authority contract

Pin all five source/import files and their BUILD01 copies, both binaries,
compile outputs, this protocol and the same macos-arm64 compiler/flags before
execution. Parent uses tested PROCESS_V3/IO_V1. Native test has no filesystem,
network, learner, teacher, historical generator or authority calls.
Parent guard60s/file1MiB/core0/fd64; child deadline15s (invalid1s), child file128KiB,
observed positiveRSS<=256MiB. RSS remains measurement, not hard containment.
Any runtime abort/missing group or terminal marker fails qualification.

Whole native-admitted root is Research/R33_NATIVE_N04_RUN_PRIMARY_V1. Specifically
named siblings R33_NATIVE_N04_RESERVATION.json, R33_NATIVE_N04_LAUNCH.stdout and
R33_NATIVE_N04_LAUNCH.host.stderr retain reservation/launch evidence and are
copied into the admitted root. No prior primary is a write target.

No Python or alternate runtime implements evaluation. Shell copying, bounded
mechanical source renaming, native compiler invocation and independent host
checksums are operational tooling only. Literal oracles are disclosed fixture
logic, never domain knowledge inserted into a learner.

Preserve every outcome, all raw logs, source/build identities, resource report,
artifact list/verification, consumed status, architectural diff, next rationale
and current/handoff/journal updates. A failure needs a new corrective identity,
not an altered frozen oracle. R27 stays60423/restarts0; no R33 training or grant.
