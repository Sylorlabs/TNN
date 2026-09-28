# R33 native competency telemetry V1

Status: **COMPILED, NOT EXECUTED**. Native source and synthetic assertion driver; compilation-only delivery. No test execution, learner training, preregistration, promotion, canonical mutation or authority grant is performed by this work. R27 remains canonical at step60423 with zero newborn restarts. The sidecar does not claim to represent or migrate its state.

## Scope and evidence

This is an evaluator/supervisor-owned, bounded event-sourced competency accumulator. It maintains one experiment/brain/branch/competency/clock namespace. The retained event log is authoritative for this component; all counters are derived from it. It does not import any changing SHA, I/O, process-supervision, journal, C03 or historical learner implementation.

Only the following source files are added:

- `Research/R33_NATIVE_TELEMETRY_V1.zag`: accumulator, validation, snapshots and record lookup.
- `Research/R33_NATIVE_TELEMETRY_TEST_V1.zag`: native synthetic expected/actual assertions.
- This design document; compiler outputs are confined to `Research/R33_NATIVE_TELEMETRY_BUILD_01/`.

The requested source contracts were read completely. Their SHA-256 values at inspection were:

| Contract | SHA-256 | Relevant scope |
| --- | --- | --- |
| `Research/R33_TRAINER_INTERFACE_AND_TELEMETRY.md` | `a54cee9c1bfe0942fa71dbc76a42316e7cf58422bb1b2c036974cfa0fa52a0bf` | Lines 22–56: metrics, assistance, payload identity, evaluator separation; 69–81: attribution and charged rejected work |
| `Research/R33_TELEMETRY_SCHEMA.json` | `083216426b2ea258eeb0bc03930ccf7728d237ed32526c0840c2458a9c162fcc` | Lines 14–43: explicit missing measurements; 99–154: identity/assistance; 158–199: competency snapshots |
| `Research/R33_WHITE_BOX_OBSERVABILITY_CONTRACT.md` | `e814dbc1da911da0741c27795f5b7106e575998e450b8f45684b4ef1fff08e2b` | Lines 16–50: complete state, non-rewindable accounting and validate-before-commit |
| `Research/R33_B001_COMPONENTS.zag` | `4f567a9392d65e298cd93a1c90fb8a2849aeda485ca5ad64c7caed7028981a32` | Native slice, status, ordering and no-partial-write syntax reference only; not imported |

Additional syntax references were `Research/R33_B001_C01_DRIVER.zag`, `Research/R33_NATIVE_N02_DRIVER.zag`, and `/Users/Shared/micah/Documents/zag/zag-poc/tests/generic_pointer_slice.zag`. These were read as source, not executed or edited. No Python was executed or edited, and no new Python code was authored.

## API and ownership

All public inputs are valid caller-owned contiguous `[]i32` buffers. No compiler-level protection against forged pointers or hostile native callers is claimed. The admitted public API is:

| Function | Contract |
| --- | --- |
| `tm_init(state, capacity, experiment, brain, branch, competency, clock)` | Initialize an exactly sized, all-zero buffer. Reject nonzero buffers; there is no reset/rollback API. |
| `tm_validate(state)` | Validate committed records, identity, order and event semantics without mutation. |
| `tm_append(state, event)` | Validate all history and the incoming record before writing. On success copy the complete record and advance the committed count last. |
| `tm_snapshot(state, output)` | Produce exactly 56 metric rows in a separate 168-word output. Refuse invalid state or overlapping output before any output write. |
| `tm_rate(snapshot, numerator_key, denominator_key, output)` | Expose integer numerator/denominator, not a guessed percentage or calibrated probability. Requires a successful snapshot; output has four words. |
| `tm_event_at(state, index, output)` | Copy an exact 88-word retained record, including causal indices. Reject invalid/missing indices without changing output. |

Other `tm_*` functions are internal helpers, not independently validated ingress APIs. Calls must be serialized by the parent supervisor; the code is not a concurrent transaction implementation. The accumulator has no allocation or syscall in its mutation path. Snapshot calculation also uses caller-provided storage, not dynamic scratch allocation. The synthetic driver allocates its fixture buffers using the compiler's native runtime.

## Bounded state and record ABI

Capacity is 0–128 events. State length is exactly `16 + 88 * capacity` i32 words, at most 11,280 words / 45,120 payload bytes, excluding runtime allocation overhead. The header is:

| Offsets | Meaning |
| --- | --- |
| 0, 1 | Magic `330101`, format version `1` |
| 2, 3 | Declared capacity, committed event count |
| 4–8 | Positive experiment, brain, branch, competency and clock IDs |
| 9–15 | Reserved zero |
| 16 onward | Fixed-width events; uncommitted tail is not included in snapshots |

All event identity fields are positive scoped registry IDs, not cryptographic credentials or pointers into a learner. Ordinals start at zero and are contiguous. Event IDs must be unique in this log but need not numerically match ordinals. Immediate parent is exactly ordinal minus one (`-1` at the root). The additional causal index is `-1` or an earlier event index. Equal nonnegative ticks are allowed; backwards time or a clock/namespace change is rejected. Ticks are bounded i32 units defined by the caller; they are not a full nanosecond timestamp implementation.

| Event offsets | Meaning |
| --- | --- |
| 0–11 | Version, event ID, ordinal, immediate parent index, additional causal index, experiment, brain, branch, competency, clock, tick, kind |
| 12–19 | Episode ID, experience ID, actor kind, actor ID, delegating human ID, assistance, outcome, mode |
| 20–24 | New request indicator, help result, human interventions, software interventions, intervention-dose units |
| 25–30 | Retrieval found/useful; finalized update proposals/accepted/rejected/rolled-back counts |
| 31–36 | Operations, I/O bytes, CPU microseconds, summed wall microseconds, logical-memory bytes, peak RSS bytes |
| 37–39 | Original assessment index for anchor enrollment, interfering competency ID, retention-panel/checkpoint registry ID |
| 40–71 | 32 externally supplied payload-digest bytes, each carried as an i32 in 0–255 |
| 72–87 | Up to 16 anchor outcomes in enrollment order; unused positions must be `-1` |

Actor kinds: 1 learner, 2 human, 3 human group, 4 software teaching aid, 5 evaluator, 6 protected supervisor. Software aid requires a positive delegating-human reference. This is reference validation, not authentication. A software aid is never interpreted as the human trainer.

The record is a deliberately narrower native aggregation ABI, **not** a serialized instance of the complete JSON schema. Missing full-schema fields, including authenticated policy/grant/checkpoint hashes, multiple causal-reference categories, mutation before/after hashes, group overlap certificates, clock timebase and resource measurement methods, require a future native adapter. Do not label these records JSON-schema-conformant full causal events.

### Event kinds and canonical unused fields

1. `TM_EXPOSURE`: one learner presentation, positive episode/experience, nonzero digest. Mode1 is first-seen payload; mode2 is replay. Assistance is `-1`, `0` or `1`.
2. `TM_HELP`: episode-level request/delivery/refusal. Result0 is a learner request; result1 is human/group/appropriately delegated software delivery; result2 is refusal. Refusal carries no intervention/dose. The request indicator denotes a **new request occurrence**, not repetition of an earlier request on its response. Separate response records use zero for that flag. Producers own truthful request occurrence attribution.
3. `TM_ASSESS`: evaluator-recorded learner outcome `-1` unmeasured, `0` failed, `1` succeeded. Mode1 requests a locally fresh payload; mode2 is a repeated assessment. Teaching aids cannot author assessment records through this API.
4. `TM_ANCHOR`: enroll an existing successful, unassisted assessment using its exact event index, episode, experience and digest. Duplicate anchors are refused; the set freezes at the first retention panel.
5. `TM_RETENTION`: one entire unassisted panel for the fixed anchor set, in enrollment order. Panel ID strictly increases. Every enrolled anchor must have outcome0/1; incomplete panels are rejected rather than imputed. No panel means retention remains unmeasured. At most16 anchors are admitted.
6. `TM_RETRIEVAL`: one supervisor-reported attempt; found/useful independently support unknown where meaningful. A miss requires useful0; unknown found requires unknown useful; useful1 requires found1.
7. `TM_UPDATE`: a supervisor-reported **finalized batch**; accepted + rejected must equal proposed, and same-batch rolled-back cannot exceed accepted. Accepted and spent work are not subtracted upon rollback. Pending proposals, separate later rollback transactions and rollback-of-old-batch accounting are outside V1.
8. `TM_RESOURCE`: one final charge record for exactly one earlier non-resource event. The causal index identifies that event. Duplicate charges and charges for resource records are refused. All resource fields may explicitly be unknown.

Unused identity/payload/counter fields must be zero or the documented `-1` sentinel. The validator refuses inconsistent inactive fields so an exposure cannot carry hidden update counts, for example. The native test builder is a source-level example of canonical record construction.

## Identity, freshness and assistance semantics

Payload comparison uses all32 supplied digest bytes, not experience ID alone. Reusing an experience ID with a different digest is rejected. Giving the same digest a new experience ID cannot make it unique/fresh. Zero digest is reserved as missing and not admitted for payload-bearing events. The implementation does not compute SHA-256 or prove correspondence between the supplied digest and real bytes.

First-seen/fresh are **local to the complete retained log and its declared namespace**. All preceding exposure and assessment payloads participate in duplicate detection. Enrollment duplicates are not new presentations. Evidence previously seen by the historical parent, another process/competency, or outside this log cannot be certified fresh here. A trusted native upstream adapter must authenticate payload bindings and independent source-group overlap evidence before scientific freshness/generalization claims.

Any delivered help before assessment makes that episode assisted even when a subsequent record claims unassisted. Unknown assistance on an earlier exposure propagates unless assistance is positively established. Known assistance dominates unknown. Later help/exposure/another assessment on an already assessed episode is rejected; there is no retroactive rewrite of finalized outcomes. Exposure assistance counters describe assistance known **at presentation time**; fresh-assessment assistance describes the complete recorded episode prefix.

Fresh scored denominators exclude unmeasured outcomes but report the excluded count explicitly. Scored outcomes with unknown assistance are included in overall fresh counts but excluded from both unassisted and assisted strata; unknown assistance has its own count. Repeat assessments do not increment fresh success counts. A success is an externally reported operational outcome, not inferred understanding or teacher competence.

## Derived metrics and missingness

There are56 rows, each `[status, value, reason]`. Status2 means `DERIVED` from admitted records; status0 means `NOT_MEASURED` and always has value`-1`. Reason0 means present,1 no relevant records,2 an unknown required observation,3 zero denominator (rate view),4 not implemented,5 incomplete event resource coverage. Code reserves reason6 for unknown-assistance views; V1 reports such records in explicit counters. Measured zero and missing are therefore distinct.

Metric constants are the authoritative key map. The main groups are exposure1–5, help6–11, fresh assessment12–20, retention23–31, retrieval32–36, update37–40, resource41–49, and resource-complete totals54–55. Key0 is the exact retained-event count, including zero for an empty log. Explicit unsupported metrics are understanding50, teacher competence51, transfer52 and calibration53. Correct/failed learner action `UNKNOWN` distinction21–22 is also not implemented; an **unmeasured outcome** is not treated as an `UNKNOWN` action.

`tm_rate` emits `[status, numerator, denominator, reason]`. A zero denominator produces `NOT_MEASURED` with reason3 and retains the known zero numerator/denominator for inspection. Unknown inputs produce `[-1,-1]` numerator/denominator, never0%. The caller must choose semantically corresponding rows, such as fresh successes/scored outcomes or unassisted successes/unassisted scored outcomes; this helper is not a statistical estimator.

### Retention and interference

The fixed anchors start with known original success. Each complete panel records all pointwise outcomes. `FINAL_LOST` is loss at the last panel, `EVER_LOST` counts anchors lost at least once, and `WORST_LOST` is the largest simultaneous complete-panel loss. `NEW_LOSSES` and `RESCUES` count adjacent-panel 1→0 and 0→1 transitions; first-panel comparisons use original success. Full recovery never clears ever-lost history. Equal totals with swapped cases remain distinguishable.

An interference-tagged panel names a different competency and must causally reference an earlier update batch bearing that same competency tag. Its loss/rescue transitions enter separate interference counters. This proves **record association**, not controlled causal attribution. There is no full pairwise interference matrix or experimental effect estimate in V1; records retain the information needed for a future scoped reducer.

### Resource and update accounting

Each additive resource or intervention/update field is limited to10,000,000 per event. With at most128 records, sums are at most1,280,000,000, within signed i32. Nonnegative logical bytes/peak RSS may reach2,147,483,647 because they use maxima rather than sums. There is no silent saturation. Larger charges require a separately versioned envelope, not relabeling the same charge twice.

Resource41–47 covers the set of recorded charges. Any unknown value makes that field's aggregate unmeasured, not a misleading partial total. Peak memory uses maximum, not addition. CPU may exceed summed wall time for concurrent work. Summed wall durations are not overall elapsed time, and logical-memory peak is the largest reported sample, not a guarantee that all instantaneous peaks were observed.

`CHARGED_EVENTS` is the number of uniquely charged non-resource events; `UNCHARGED_EVENTS = all_events - 2 * resource_records`. Resource records themselves are not recursively charged. Complete CPU/operations totals54–55 are measured only when every non-resource event has a final charge and every contributing field is known. Full cost outside this log (process startup, compiler, omitted supervisor work, shared/multi-competency work) is not thereby measured. One accumulator cannot prevent another accumulator from duplicating the same physical charge; allocation remains the parent's responsibility.

## Mutation and reconstruction boundaries

`tm_append` checks input shape, state/event non-overlap, complete committed history, capacity, incoming identity/order, payload/assistance semantics, anchor completeness, and charge consistency **before the first store**. On any returned failure, state, including its unused capacity, and input are unchanged. Snapshot and record-lookup refusal likewise preserve outputs. Partial overlapping slices are checked by start-address membership in either contiguous slice; no pointer-to-integer casts are used.

After validation, append copies the event, then increments the committed count. This is return-time atomicity for a serialized in-memory call—not crash atomicity, fsync, authenticated durability, concurrent readers or protection against a hostile caller editing memory. There is no allocation or recoverable branch inside the commit copy. Complete history is revalidated on each public state operation, but a self-consistent malicious rewrite has no cryptographic protection here. Uncommitted tail bytes are not authenticated.

Reconstruction reinitializes a **separate empty buffer** and appends the exact previously retained records in order. It is telemetry reduction, not learner replay or new experience. The driver designs same-process state/snapshot parity controls for this operation; no fresh-process/disk-reload claim is made. Parent-owned durable journaling and supervision must surround this component before integrated qualification. Rejecting an incoming record requires the parent to retain the failure status externally; this component cannot append a rejection to an already full log.

## Designed native assertions, not executed evidence

The driver requires an explicit `check` argument; another invocation returns2. Every assertion prints its label, expected value, actual value and equality indicator. Failures accumulate across test groups; main returns1 when any assertion differs and emits the pass marker only when the failure total is zero. Fixture allocation/I/O/runtime failures can still abort before a final marker and must be treated as failure/incomplete by the supervising parent.

The designed groups cover:

| Group | Engineering controls |
| --- | --- |
| Empty/initialization | Missing versus measured zero, no inferred understanding/teacher competence, nonempty reset refusal, zero capacity, invalid initialization without mutation |
| Identity/exposure | All five namespace fields, duplicate ID, ordinal gap, wrong parent/future cause, backwards/equal time, ID→digest rebinding, renamed duplicate payload, honest replay, invalid digest byte/inactive field/truncated record |
| Help/assessment | Human-group/software aid separation, required human delegation reference, sticky assistance, refused/accepted aid, assisted anchor refusal, teacher-authored assessment refusal, unknown outcomes/help and exact numerators/denominators |
| Retention | Fixed successful anchors, equal-total pointwise swaps, loss/rescue trajectories, final recovery retaining ever/worst history, source-tag validation, missing/extra/duplicate/assisted panels, frozen-anchor refusal and original causal indices |
| Retrieval/resources | Misses in denominator, unknown found/usefulness, invalid useful miss, peaks versus sums, CPU>wall, duplicate charges, bounded totals, measured zero versus unknown and charging rejected updates |
| Anchor capacity | All16 anchors,17th enrollment refusal without mutation, complete all-lost panel |
| Atomicity/reconstruction | Partial alias refusal, invalid output shape, corrupt history, unchanged buffers, absent record, duplicate delivery, full record/state/snapshot reconstruction,128 accepted events and capacity+1 refusal |

These tests are engineering controls, not learner training or evidence that an actual learner passed. The full assertions are not scientifically preregistered or executed here. They intentionally avoid the changing native SHA constant-table and process-supervision work owned by the main agent.

## Compilation record

The pinned compiler is `/Users/Shared/micah/Documents/TNN/TNN/Research/toolchain/znc_macos_arm64_7cacbfc0`, measured SHA-256 `3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`.

The initial source/driver compiled with exit0 using:

```sh
Research/toolchain/znc_macos_arm64_7cacbfc0 Research/R33_NATIVE_TELEMETRY_TEST_V1.zag --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o Research/R33_NATIVE_TELEMETRY_BUILD_01/telemetry_test
```

Initial logs are `compile_01.stdout` and `compile_01.stderr` in the build directory. After adding explicit anchor-capacity and full-history reconstruction controls, the final sources compiled again with **exit0**, using the same flags and output path `Research/R33_NATIVE_TELEMETRY_BUILD_01/telemetry_test_02`. Its compiler stdout is164 bytes and stderr is0 bytes. File inspection identifies a **297,344-byte Mach-O 64-bit arm64 executable**. The initial `telemetry_test` binary is superseded; `telemetry_test_02` is the handoff candidate.

Final compilation command (already compiled; not a test-run authorization):

```sh
Research/toolchain/znc_macos_arm64_7cacbfc0 Research/R33_NATIVE_TELEMETRY_TEST_V1.zag --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o Research/R33_NATIVE_TELEMETRY_BUILD_01/telemetry_test_02
```

Measured final identities, relative to `/Users/Shared/micah/Documents/TNN/TNN/`:

| Artifact | SHA-256 |
| --- | --- |
| `Research/R33_NATIVE_TELEMETRY_V1.zag` | `0754366ee76714c8610b74d0b8ae9c86a554034d2ca5a5fc9e2233c4d21ae16f` |
| `Research/R33_NATIVE_TELEMETRY_TEST_V1.zag` | `b9572286757b784848267f5d15bbcab4155462922f226e1eeef8956258b81fb9` |
| `Research/R33_NATIVE_TELEMETRY_BUILD_01/telemetry_test_02` | `bd1782d9ff4d5cc3e7c458de3266e96e496961ae3db4ed5f064e4dea5019a4ec` |
| `Research/R33_NATIVE_TELEMETRY_BUILD_01/compile_02.stdout` | `a2b52d8f5c8829f60ff622518ca90069028bf336584c36c150feea045b117dbf` |
| `Research/R33_NATIVE_TELEMETRY_BUILD_01/compile_02.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Neither produced binary was executed, including its argument guard. No native assertion result, pass marker, runtime measurement, primary run or new scientific exposure exists from this task. Hashes identify these compiled artifacts, not validated execution semantics.

## Qualification limits

Compilation does not establish correct execution, runtime isolation, allocation behavior, performance, complete JSON-schema conformance, native journal durability, scientific freshness, causal improvement, perception, understanding, teacher competence, state migration, milestone enforcement or promotion. All unsupported fields remain explicitly unmeasured. This work does not authorize changing any registry, current state, handoff, historical source, accepted parent or primary-run allocation.
