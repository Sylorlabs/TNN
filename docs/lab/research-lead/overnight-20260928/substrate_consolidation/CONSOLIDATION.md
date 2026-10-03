# Substrate Consolidation: Decline Gate over the Shared Consequence Substrate

**Verdict: CONSOLIDATION-COMPLETE. EMERGES.**

The decline gate does not need its own tally machinery. It emerges as
one read over the shared substrate: generic PURSUIT records, a generic
write path, a generic read path. DYN-1 still bends with the same 40
declines and the same 2 to 0 per-event cost collapse.

## 1. What the decline gate does (pilot f3e6985d4)

- **What:** after 3 failed pursuits of the same (s,r), further queries
  return WITHHOLD (-3) instead of running trial, bootstrap, and
  miss_inquire.
- **State it used:** live UNCERTAINTY (tag 30) nodes keyed (s,r). Each
  failed miss reifies exactly one, so the live count was the failure
  tally. No new storage; a full 1024-node scan per query.
- **Decision:** WITHHOLD vs proceed, checked in ev_query after
  activate fails, before trial.
- **Result:** DYN-1 BENDS. 40 declines, 80 nodes saved, final 241 live
  nodes vs 321 frozen baseline.

## 2. Mapping to the shared substrate (spec 550fa268b)

| Decline-gate element | Substrate element |
|---|---|
| Tally of failures per (s,r) | PURSUIT record keyed (s,r), field consec_fail |
| WITHHOLD decision | Substrate read: sub_consec(W,PURSUIT,s,r) >= 3, in ev_query before trial |
| Consequence record | Action: query/inquiry attempt on (s,r). Outcome: fail, mode F6 (activation miss). Provenance: taught (driver-supplied query; spec 7.2). Cost: nodes allocated by the attempt. |
| Production write path | sub_note failure write at the ev_query miss tail (where miss_inquire runs); sub_note success writes on the activate-hit, trial-success, and bootstrap-success branches |
| Production read path | ev_query, after activate fails, before the trial loop |
| Changed decision | WITHHOLD (-3) vs trial/bootstrap/inquiry |

The WITHHOLD trace names the pursuit key, the value read, and the
threshold (log_ev p0=-3, p1=consec_fail read, p2=N), per spec 5.1.

Spec-faithful behaviors the pilot lacked:
- **Reset on success** (spec 4.2): consec_fail resets to 0 on any
  success write. The pilot's tally was total failures (identical in the
  battery, where miss keys never succeed); the substrate counts
  consecutive failures, which is strictly more correct in general.
- **Declines do not write** (spec 5.1): the gate's own caution cannot
  inflate the count it reads. Census confirms: attempts=3 per key
  despite 7 queries per key.
- **Source tagging** (spec 2.4/7.2): src_taught/src_observed/src_self
  counters are written on every attempt. The minimal gate reads
  consec_fail only; the tags are infrastructure for richer consumers.

## 3. Implementation (unfrozen variant sc_full.zag)

Base: verbatim frozen copy (SHA-256
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd,
verified). Cognition diff vs base is exactly sc_substrate.zag:
substrate machinery plus replacement ev_query; test main swapped for
the DYN-1 driver. Verified by diff.

Generic machinery (knows nothing about decline):
- sub_find / sub_get: keyed lookup and get-or-create over tag-61
  record nodes, keyed (key_type, key_a, key_b). Two namespaces:
  PURSUIT and STRATEGY.
- sub_note: one write path for all consumers. Parameters: namespace,
  key, success/fail, failure mode (F1-F7), source class, node cost,
  create flag. Implements spec 4.2 exactly.
- sub_consec: one read path. Returns consec_fail, 0 when no record.

Decline-specific code: the threshold (N=3, carried over unchanged),
the WITHHOLD constant (-3), and three lines in ev_query (read, compare,
return). The private UNCERTAINTY tally scan is deleted.

Record cost (spec 6.4): one 40-byte node per PURSUIT record. 10 records
in this battery. last_active omitted (documented): its only specified
consumer is record reclamation, which is not implemented in this pilot.

## 4. Results: DYN-1 still bends

3/3 byte-identical runs (SHA-256
9a15c80e3e2703fbbb36546d6c5bca558bc19489411a8baaecc6c79beaf63a55).

| Phase | Frozen baseline | Pilot (ad-hoc tally) | Substrate version |
|---|---|---|---|
| A teach (80) | 80 | 80 | 80 |
| B qhit (50) | 0 | 0 | 0 |
| C miss (50) | 101 | 61, 20 declines | 71, 20 declines |
| D observe (50) | 100 | 100 | 100 |
| E miss2 (20) | 40 | 0, 20 declines | 0, 20 declines |
| Final live nodes | 321 | 241 | 251 |
| Nodes saved vs baseline | - | 80 | 70 net (80 gross, 10 record nodes) |

Key 101 trace (representative of all 10 miss keys):

| Event | Miss # | ret | dn |
|---|---|---|---|
| E130 | 1 | -2 | 4 (pilot: 3; +1 is record creation) |
| E140 | 2 | -2 | 2 |
| E150 | 3 | -2 | 2 |
| E160 | 4 | -3 | 0 |
| E170 | 5 | -3 | 0 |
| E230 | 6 | -3 | 0 |
| E240 | 7 | -3 | 0 |

- 40 declines, all with dn=0, none outside the miss phases.
- UNCERTAINTY census identical to pilot: 30 total, 3 per key
  (miss_inquire behavior unchanged).
- Substrate census: 10 records, one per miss key; per key
  consec_fail=3, attempts=3, successes=0. No records for Phase B
  (s,1) keys: per spec 4.1, records are created on first miss or
  trial, not on answers from memory.

Counterfactual check (learning-machinery definition):
(a) same probe (101,99): full inquiry at E130, WITHHOLD at E160;
(b) mediated by learner-state difference (PURSUIT record consec_fail
0 to 3); (c) caused by a production write path (sub_note failure
writes from the ev_query miss tail). All three hold.

## 5. Source delta

- Pilot: ~40 cognition lines (private tally + gate check).
- Substrate version: ~110 cognition lines (generic store ~75,
  gate integration ~35).
- The extra ~70 lines are the shared store: keyed lookup,
  generic write, generic read, source tagging, lifecycle packing.
  Nothing in it is decline-specific. A second consumer (abandonment
  reads the same consec_fail and writes the same state field; trial
  reorder reads STRATEGY records through the same lookup) adds only
  its read rule, zero new storage machinery.

## 6. One-System Rule

Holds. MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.
One new node tag (61) used purely as keyed storage infrastructure;
no production function branches on tag 61 to alter cognition
(sub_find only locates records). No new edge types, no new fields
on existing node types, no task-specific handlers.

## 7. Honest limits

1. **One consumer only.** The substrate is demonstrated structurally
   (generic API, two namespaces, shared record format), but only the
   decline gate reads it. Spec 9.4 (S2 falsification) remains open:
   a second consumer must show the shared store earns its keep
   against narrow per-decision counters.
2. **N=3 still researcher-set**, carried over unchanged for
   comparison. No learner-owned threshold.
3. **Eviction-decoupled persistence.** The pilot's tally was coupled
   to T30 node liveness (forgetting re-opened inquiry); substrate
   records persist until a success resets them. No eviction fires in
   this battery, so it cannot discriminate; the difference is real
   and is the spec-mandated behavior.
4. **Source tags written but not consumed** by the minimal gate.
   The bootstrap-exclusion rule (spec 7.1) is specified, tagged,
   and ready; this gate does not need it.
5. **No reclamation implemented** (last_active omitted, documented).
   Record count is bounded by distinct pursuit keys in this pilot.
6. The decline criterion remains bounded L2, researcher-authored.
   Nothing here is L3 or a learner-internal criterion.

## 8. Standing metrics (this wave)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 3 (substrate record format,
  N=3 threshold carried over, tag-61 storage tag)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (consec_fail values are
  learner state; the decline criterion is researcher-authored)
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: ~110 added (generic substrate + gate integration)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

## 9. Why EMERGES and not SEPARATE

SEPARATE would have required decline-private machinery the substrate
could not express: a special counter, a special timing rule, or a
special storage path. None was needed. The tally became a field in a
generic record; the gate became a generic read; the failure/success
accounting became the generic write path that abandonment, retention
input, and trial reorder are specified to share. The DYN-1 bend
survived the migration with identical decline behavior and honestly
accounted record cost. Decline is a consumer of the consequence
substrate, not a separate engine.

Next discriminating test: migrate a second consumer (abandonment via
the state field, or H3-lite Node 1 trial reorder via STRATEGY
records) onto the same store with zero new storage machinery, and
run the spec 9.4 S2 comparison against narrow counters.

## Constraints honored

Unfrozen variant only; frozen source untouched (hash verified).
Pure Zag via pinned znc; safebin; `which python3 python` empty.
Zero em dashes byte-verified. Paper untouched. No sealed worlds.
Nothing pushed.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/substrate_consolidation/`:
- `NAMECHECK.md` (Step 0 toolchain guard, scope, constraints)
- `CONSOLIDATION.md` (this report)
- `sc_base.zag` (verbatim frozen base, SHA-256 verified)
- `sc_substrate.zag` (substrate machinery + replacement ev_query)
- `sc_driver.zag` (DYN-1 driver + decline counters + substrate census)
- `sc_full.zag` (assembled unfrozen variant)
- `sc_bin` (compiled binary)
- `sc_run1.txt`, `sc_run2.txt`, `sc_run3.txt` (3/3 byte-identical,
  SHA-256 9a15c80e3e2703fbbb36546d6c5bca558bc19489411a8baaecc6c79beaf63a55)
