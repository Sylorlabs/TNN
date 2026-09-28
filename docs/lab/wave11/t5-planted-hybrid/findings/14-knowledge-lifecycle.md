# 14 — Unplanting and Knowledge Lifecycle (Track 5, wave11)

## Slice
Design the lifecycle state machine for a unit of knowledge (planted ↔ learned ↔ killed), the deliberate op effecting each transition, per-transition ledger entries, and the lifecycle metrics that diagnose planting quality.

## Falsifiable claim
Every knowledge unit in TNN carries a lifecycle record with a provenance-tagged state (PLANTED / LEARNED / CORROBORATED / TRUSTED / REFUTED / KILLED / FORCEPINNED), every state transition is effected by exactly one deliberate op (kill/pin/promote/demote/revise/unplant) with a ledger entry, and lifecycle metrics (survival-to-corroboration rate, kill rate, unplant rate) computed natively in Zag are invariant under byte-identical replay. Claim: unplanted units (planted content demoted to learned status, provenance kept) show equal-or-better subsequent truth-tracking than units left PLANTED-forever, because planted status grants no evidential weight.

## Design

### State machine (states are provenance-tagged; content ≠ status)
```
PLANTED --corroborate--> CORROBORATED --promote--> TRUSTED
PLANTED --refuted--> REFUTED --kill--> KILLED
PLANTED --unplant--> LEARNED            (status shed; content retained; provenance retained)
LEARNED --corroborate--> CORROBORATED
LEARNED --superseded--> REVISED (→ LEARNED with replaced content; old content archived, not deleted)
TRUSTED --refuted--> REFUTED            (trust does not immunize; evidential bar to refute is higher)
FORCEPINNED — terminal for kill only; human/trainer only (standing law 8); TRUSTED→FORCEPINNED by force-pin op.
```

### Deliberate op per transition (native Zag, MA1 ops extended)
- `kb_corrob(s,slot,evidence_ep)` → PLANTED/LEARNED → CORROBORATED. Op: promote + provenance stamp.
- `kb_promote(s,slot,threshold_met)` → CORROBORATED → TRUSTED. Higher bar: ≥N independent corroborations (N fixed at trial start, no per-unit tuning).
- `kb_demote(s,slot,reason)` → CORROBORATED/TRUSTED → PLANTED/LEARNED (reverse transitions stay inside same provenance branch).
- `kb_revise(s,slot,new_content,sup_ev)` → content replaced; old content archived with REV_BY pointer; state REVISED, then judged as LEARNED.
- `kb_unplant(s,slot)` → PLANTED → LEARNED. The novel op. See below.
- `kb_kill(s,slot,ref_ev)` → REFUTED → KILLED. CORE unkillable (MA1, 58/58).
- `kb_forcepin(s,slot,human_auth)` → terminal. Audited, visible (law 8).

No op may change provenance (planted/learned) except `kb_unplant` and `kb_forcepin`; no op may change content except `kb_revise`.

### Unplanting — precise spec
`kb_unplant(s, slot)`:
1. Precondition: `slot.state == PLANTED`, `slot` not FORCEPINNED, not REFUTED.
2. Effect: `slot.state := LEARNED`; `slot.provenance := PROV_UNPLANTED_FROM_PLANTED` (provenance is write-once-append-only, never erased).
3. Content untouched. Truth-tracking weight of the unit drops to the learned-unit baseline: planted units may be granted no evidential privilege over learned units from this point on.
4. Ledger entry (append-only audit, MA1 replay semantics): `OP_UNPLANT slot=<n> from=PLANTED to=LEARNED ep=<e> caller=<deliberative ctx> reason_code=<rc>` with `reason_code` ∈ {EVIDENTIALLY_INERT (survived but never consulted), PROMOTED_PREMATURELY, PLANTING_SOURCE_DEPRECATED, PLANTING_CONTESTED (another source planted contradictory)}.
5. Correctness condition: unplanting is correct when the unit's planted status is no longer load-bearing for any decision — i.e., no live decision trace in the ledger references `slot.state == PLANTED` as the deciding factor, and the unit's corroboration count meets the ordinary learned-unit bar. If a decision trace cites the planted status as decisive, `kb_unplant` is REFUSED and the ledger records `OP_UNPLANT_REFUSED`.
6. Reversal: re-planting is forbidden. A unit can move LEARNED→CORROBORATED→TRUSTED on its own merits; provenance keeps `PROV_UNPLANTED_FROM_PLANTED` forever so later analysis can detect whether ex-planted units behave differently.

### Lifecycle metrics (computed natively per batch of W episodes)
- survival rate = |PLANTED→CORROBORATED within window| / |PLANTED at window start| — diagnoses planting relevance (high = planting tracks world).
- kill rate = |PLANTED→REFUTED→KILLED| / |PLANTED| — diagnoses planting accuracy (high = bad planting source).
- unplant rate = |OP_UNPLANT| / |PLANTED| — diagnoses planting necessity (high = planted status doing no work).
- refute-resistance of TRUSTED = |TRUSTED→REFUTED| / |TRUSTED| — must stay low; a spike is a K-flag.
- ex-planted truth-tracking = subsequent corroboration rate of PROV_UNPLANTED_FROM_PLANTED units vs units that stayed PLANTED — the unplanting efficacy metric.
All metrics must be byte-identical under replay from logged state (law 2). Evidence basis: MA1 audit/replay, wave5/6 ledger-proves machinery (docs/lab/wave5, wave6 on branch tnn-native-lab).

## Kill bar
The design is killed if ANY of: (1) a full logged-state replay of a 500-episode knowledge lifecycle run fails to reproduce all state transitions and all five metrics byte-identically; (2) ex-planted units truth-track WORSE (lower subsequent corroboration rate) than units that stayed PLANTED, difference >10pp — unplanting must not degrade epistemics; (3) any `kb_unplant` succeeds on a unit whose planted status is cited as decisive in a live decision trace — the refusal guard fires on a probe and must hold 50/50 planted-vs-ex-planted planted-status-decisiveness probes; (4) provenance is erasable — a builder demonstrates a unit reaching TRUSTED with no recoverable provenance tag. A K-flag (not kill) fires if TRUSTED→REFUTED rate exceeds 15% in any 500-episode window.

## Honesty notes
- Weakest point: the unplant-refusal guard ("no live decision trace cites planted status as decisive") requires decision-trace indexing over the audit ledger; the znc 2^25-byte slice-indexing limit (see brief) constrains how much trace history can be searched in one pass — chunked search needs an equivalence proof via byte-identical reruns before this can ship at scale.
- The refusal guard is a mechanism, but the *definition* of "decisive" in a trace is a judgment call by the deliberative context — honest failure mode: the guard could become a rubber stamp. Probe it adversarially (red-team deliberately cites planted status to smuggle content through).
- Not claiming unplanting is *better* than killing: unplant keeps content as learned; if the content is refuted, kill it (REFUTED→KILLED). Unplant is for content that is fine but whose planted privilege is inert.
- Not claiming these metrics *cause* good planting; they diagnose it (cf. wave5/6 integrity attribution: ledger proves, doesn't cause). The planting source itself is out of scope for this slice.
- Felt-intensity retirement (law 9) respected: no importance-feeling anywhere in this design; strength is judgment-set per law 8, not lifecycle-derived.

## Next build step
Build the lifecycle substrate in native Zag at 100 episodes: seed N=50 planted units + 50 learned units with deterministic scripted evidence, implement all seven ops plus the unplant-refusal guard, log every transition, then replay from full logged state and require byte-identical metrics. The single most informative probe: 50 trials where a deliberative context cites `PLANTED` status as decisive in a decision trace, then calls `kb_unplant` — the guard must refuse 50/50, and the refute/kill path must still work on the same units afterward.
