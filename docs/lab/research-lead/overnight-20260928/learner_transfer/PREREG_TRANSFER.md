# PREREG: Continuing Learner Transfer and Interference Test

Frozen before any implementation or test execution. This prereg commits
the workload, the transfer/interference designs, and the kill bars. Any
amendment must be committed transparently and re-frozen before
implementation; no bar may be altered after seeing results.

## Context

Continuing Learner Extended (LEARNER-EXTENDED, `179b4a950`) verified:
two schema kinds in one persistent run, both retirement triggers
(consecutive-rejection and accuracy-ledger), OPS_P7 = 28 < OPS_FRESH = 32.

Open questions this wave answers:
1. TRANSFER: does a schema FORM transfer to novel surface values, or
   does the learner only work on seen value ranges?
2. INTERFERENCE: when domains alternate between conflicting schema
   kinds, does the learner select correctly, retire cleanly, and
   recover without catastrophic interference?

## Design

The learner is `contlearn2.zag` extended to 15 domains (D1-D8 frozen
identical to the LEARNER-EXTENDED workload; D9-D15 new). Single main(),
no resets, no task labels, pure Zag. Schema state persists across all
15 domains.

After D8, the live schema is kind-2 (default=7, exc_abs=72, exc_obj=4
from D7; D8 mixed caused one fallback, consec=1, no retirement).

### Phase 1: Transfer (D9-D10)

- D9: (100,100,100,100) uniform, novel values (100 never seen).
  Kind-2 live. Gate2 probes (100,100,100): a==b and b==c, so g2=0.
  Expected: FALLBACK, 4 learns, consec=2? No: consec was reset to 0
  at D7 APPLY2... let me trace. D8: kind-2 live, gate fails,
  fallback, consec=1 (was 0 after D7 apply reset it). D9: gate fails,
  fallback, consec=2 -> RETIRE_CONSEC. Hmm, this retires the kind-2
  schema at D9, before D10 can test transfer.

  This is a problem. I need D9 to NOT trigger retirement, so D10 can
  test kind-2 transfer. Options: make D9 match kind-2 form so the
  gate passes, or accept the retirement and test transfer differently.

  Revised: D9 is (100,100,50,100): kind-2 pattern with novel values.
  Gate2 probes (100,100,50): a==b, b!=c -> g2=1. APPLY2 with refit
  default=100, exc at pos 2, exc_obj=50. 3 learns, acc 4/4.
  This is the TRANSFER test: kind-2 FORM applies to values (100, 50)
  never seen before. If the learner were memorizing values, the gate
  would fail. The gate checks structural pattern only.

- D10: (200,200,200,200) uniform, novel values. Kind-2 live.
  Gate2 probes (200,200,200): g2=0. FALLBACK, 4 learns, consec=1.
  No kind-2 discovery (uniform). Schema stays kind-2 live.
  This sets up the interference phase: a uniform domain the live
  kind-2 schema cannot handle.

### Phase 2: Interference (D11-D14)

- D11: (300,300,300,300) uniform, novel values. Kind-2 live.
  Gate2 fails. FALLBACK, 4 learns, consec=2 -> RETIRE_CONSEC.
  Schema dead. This is correct interference handling: the learner
  detects the persistent mismatch and retires rather than forcing
  the wrong schema kind.
- D12: (300,300,300,300) uniform. No live schema.
  discover (kind-1): all four are 300, uniform -> success.
  REDISCOVER kind-1, obj=300. 4 learns.
  Recovery: the learner re-acquires the appropriate schema kind
  for the current world structure.
- D13: (400,400,400,400) uniform, novel values. Kind-1 live.
  Gate1 passes (400,400,400). APPLY, refit obj=400. 3 learns,
  acc 4/4. Clean kind-1 operation after the interference episode.
- D14: (500,500,500,999) noisy uniform, novel values, exception in
  unprobed slot 3. Kind-1 live. Gate1 passes (probes 500,500,500).
  APPLY, refit obj=500. Slot-3 query via schema returns 500,
  truth 999: acc 3/4. Ledger -1 -> RETIRE_LEDGER with consec=0.
  Marker SCHEMA_RETIRED_LEDGER. This re-verifies the ledger trigger
  on novel values (transfer of the retirement machinery itself).

### Phase 3: Cross-kind interference stress (D15)

- D15: (600,600,70,600) kind-2 pattern, novel values, exception in
  probed slot 2. No live schema (retired at D14).
  discover (kind-1): values 600,600,70,600 not uniform -> fail.
  discover2 (kind-2): exactly one differs (70 at pos 2) -> success.
  SCHEMA2_DISC, default=600, exc_abs=subj(15,2), exc_obj=70.
  4 learns. Tests kind-2 discovery from scratch on novel values
  after a full interference cycle.

## Frozen expectations

Domain summary (learns per domain):
- D1-D8: identical to LEARNER-EXTENDED (4,3,3,3,4,4,3,4 = 28 ops)
- D9: kind-2 novel -> APPLY2, 3 learns, acc 4/4
- D10: uniform novel, kind-2 live -> FALLBACK, 4 learns, consec=1
- D11: uniform novel, kind-2 live -> FALLBACK, 4 learns, consec=2,
  RETIRE_CONSEC
- D12: uniform, no schema -> REDISCOVER kind-1, 4 learns
- D13: uniform novel, kind-1 live -> APPLY, 3 learns, acc 4/4
- D14: noisy uniform novel -> APPLY, 3 learns, acc 3/4,
  RETIRE_LEDGER consec=0
- D15: kind-2 novel, no schema -> SCHEMA2_DISC, 4 learns

New-domain ops: 3+4+4+4+3+3+4 = 25.
Total OPS_P7 = 28 + 25 = 53.
OPS_FRESH = 15 domains * 4 = 60.
53 < 60.

Counters (cumulative from D1):
- TRANSFER_OK = 1 iff D9 shows APPLY2 with learns=3 and acc=4.
  (Kind-2 form transferred to novel values 100/50.)
- INTERFERE_CLEAN = 1 iff D11 retires via consec (not ledger) and
  no domain applies the wrong schema kind. Wrong-kind application
  is defined as: kind-1 schema applied when the domain has a
  one-exception structure, or kind-2 schema applied when the domain
  is uniform. The gates prevent this; the counter verifies.
- RECOVER_OK = 1 iff D12 rediscovers kind-1 and D13 applies it
  with acc 4/4.
- LEDGER2 = 1 iff D14 retires via the ledger trigger with
  consec=0 (second ledger-trigger firing, on novel values).
- S2DISC2 = 1 iff D15 discovers kind-2 from scratch.

Schema selection accuracy: for each domain D9-D15, the applied or
discovered schema kind must match the domain structure
(uniform -> kind-1, one-exception -> kind-2, mixed -> none).
7/7 required.

## Kill bars (all must pass)

- K1 (transfer): TRANSFER_OK == 1 and schema selection 7/7.
  Kill: D9 falls back (form did not transfer) or any domain gets
  the wrong schema kind.
- K2 (interference): INTERFERE_CLEAN == 1 and RECOVER_OK == 1 and
  LEDGER2 == 1 and S2DISC2 == 1.
  Kill: retirement via wrong trigger, failed recovery, ledger
  trigger does not re-fire, or kind-2 not rediscovered.
- K3 (purity and determinism): pure Zag at every stage (source, znc
  build, execution, analysis); zero Python invocations; zero em-dash
  bytes in all wave files (byte-checked); 3/3 byte-identical runs,
  exit 0, zero stderr. Kill: any Python use, any em-dash byte, or
  non-identical runs.

Supporting checks (reported, must hold for the verdict):
- K3a: D1-D8 output byte-identical to LEARNER-EXTENDED CL2_RAW_1.txt
  for the first 8 domains (persistence did not alter history).
- K3b: OPS_P7 < OPS_FRESH (53 < 60).

Verdict TRANSFER-TESTED iff K1, K2, K3, K3a, K3b all pass.

## Notes on what transfer means here

The learner does not have a separate "transfer module." Transfer is
operationalized as: the gate (a structural pattern check) passes on
novel values, allowing the schema form to apply with refit parameters.
This is form transfer, not value memorization. The falsifier is D9:
if the implementation secretly keyed on seen values, the gate would
fail on (100,100,50) and we would see FALLBACK instead of APPLY2.

Interference is operationalized as: consecutive domains with
conflicting structures cause clean retirement (not corruption), and
the learner re-acquires the right kind afterward. The falsifier is
D11: if the kind-2 schema corrupted the uniform domains (e.g., wrong
answers on unprobed slots), we would see acc < 4 on D10/D11 applies.
But D10/D11 are fallbacks (gate correctly rejects), so interference
shows as extra learns, not wrong answers. This is disclosed: the gate
is the interference shield; the test verifies the shield holds.

## Commit order

This prereg is committed alone. The implementation commit must be a
strict descendant. Verified via git merge-base --is-ancestor before
the result is reported.
