# PREREG: Learner-Substrate Integration Test

Frozen before any implementation or test execution. This prereg commits
the integration design, the port plan, and the kill bars. Any amendment
must be committed transparently and re-frozen before implementation; no
bar may be altered after seeing results.

## Context

Two prior results are complete:

1. Continuing Learner Transfer (TRANSFER-TESTED, `08d7c9fd5`):
   `contlearn3.zag` runs 15 sequential domains in one persistent
   process. Two schema kinds (kind-1 uniform default, kind-2 default
   plus single exception), P7 persistence policy (gate, apply/refit,
   fallback, consecutive-rejection retirement, accuracy-ledger
   retirement). Results: TRANSFER_OK=1, SEL_CORRECT=7/7,
   OPS_P7=53 < OPS_FRESH=60. Experience store: 64 x 20-byte integer
   slot array at workspace base 0; schema state at offset 1280;
   counters at 1304.

2. Shared Substrate (SUBSTRATE-PROTOTYPED, `2835e5641`):
   `substrate.zag` hosts a string-interned fact triple store AND an
   episodic causal store on one 32768-byte workspace. Variable count
   is a runtime header field. Fact records: (e_off, a_off, v_off)
   into a string pool; latest-wins query; conflict counting.

Open question this wave answers: can the P7 policy and schema
machinery run on the substrate's generic fact store, with no parallel
experience store? If the policy logic ports cleanly and the frozen
15-domain sequence reproduces the TRANSFER-TESTED markers, the
substrate is a viable host for the continuing learner. If the port
requires substrate extensions (new APIs, layout changes), those are
architectural evidence about what the substrate lacks.

## Integration design

### Workspace

- W is 32768 bytes. `sub_init(W, 1)` (nvar=1; the episode/causal
  machinery is present but unused by this workload; disclosed).
- String pool: base computed by sub_init (8064 for nvar=1), 4096
  byte budget.
- Policy region: POL=30000, safely above the string pool ceiling
  (8064+4096=12160). Schema state at POL+0..20 (kind, rel,
  obj/default, live, exc_abs, exc_obj), mirroring contlearn3's
  layout. Seventeen counters at POL+24..88, same offsets as
  contlearn3's counter block.

### Experience representation

The 64-slot integer array is deleted. All experience lives in the
substrate fact store:

- Entity key: "s" concatenated with the decimal subject id
  (subjects are d*10+i, unique per domain, so no domain field is
  needed; contlearn3's dom slot field was redundant).
- Attribute key: "r1" (rel=1 in the frozen workload).
- Value key: decimal object id.
- Each distinct key string is interned exactly once via a small
  key cache (linear scan with sub_streq, else sub_str; at most 80
  distinct keys: 60 subjects, 1 relation, 19 values).
- `flearn(W, eo, ao, vo)`: fact insert with the exact semantics of
  the substrate's `sub_fact_learn` (append record, count a conflict
  when (e,a) matches with a different v). Operates on the
  substrate's fact record format through its primitives
  (h_factbase, h_factcount, sub_streq, h_conflicts_set).
- `fquery(W, eo, ao)`: latest-wins lookup with the exact semantics
  of `sub_fact_query`; returns the interned value offset or -1.
- Schema state (kind, default, exception) stays as integers in the
  policy region: it is policy state, not domain experience. The
  substrate itself keeps policy-adjacent state (ep_processed,
  conflicts) in its header; this placement is architecturally
  consistent.

### Policy logic

Byte-for-byte behavioral port of contlearn3's policy:

- `true_obj(d,i)`: identical frozen workload for D1-D15.
- Gates: gate1 (three probes equal), gate2 (exactly one differs).
- Apply: refit default/exception from probes, 3 learns, accuracy
  check over 4 queries, ledger update, ledger retirement when < 0.
- Fallback: 4th learn, consec++, retirement at consec>=2 or
  ledger<0, else kind-2 discovery attempt.
- Discovery: kind-1 (all four probed values agree), kind-2
  (exactly one differs at a probed slot).
- `iobj(dom,q)`: fquery on the subject key; -999 on miss.
- `query(subj)`: fquery; on miss apply live schema from policy
  region (kind-1 default, kind-2 exception check).
- OPS accounting: one op per flearn; OPS_FRESH = 60.

### Frozen expected event sequence

D1: 4 learns, SCHEMA_DISC kind-1 obj=4.
D2: APPLY (3 learns, acc 4/4).
D3: APPLY (3 learns, acc 4/4).
D4: (6,6,6,1) gate passes, APPLY 3 learns acc 3/4, ledger -1,
  SCHEMA_RETIRED_LEDGER consec=0.
D5: 4 learns, REDISCOVER kind-1 obj=5.
D6: (3,3,9,3) kind-1 live, gate fails, FALLBACK 4 learns,
  SCHEMA2_DISC (supersession).
D7: (7,7,4,7) APPLY2 3 learns acc 4/4.
D8: (2,8,4,6) FALLBACK 4 learns, consec=1, no retirement.
D9: (100,100,50,100) APPLY2 3 learns acc 4/4, TRANSFER_OK=1.
D10: (200,200,200,200) FALLBACK 4 learns, consec=1.
D11: (300,300,300,300) FALLBACK 4 learns, consec=2,
  SCHEMA_RETIRED_CONSEC.
D12: (300,300,300,300) 4 learns, REDISCOVER kind-1 obj=300.
D13: (400,400,400,400) APPLY 3 learns acc 4/4.
D14: (500,500,500,999) APPLY 3 learns acc 3/4, ledger -1,
  SCHEMA_RETIRED_LEDGER consec=0.
D15: (600,600,70,600) 4 learns, SCHEMA2_DISC default=600
  exc_obj=70.

Expected counters: OPS_P7=53, OPS_FRESH=60, TRANSFER_OK=1,
SEL_CORRECT=7/7, CONSEC_RET_D11=1, REDISCOVER_D12=1,
APPLY_D13=1, LEDGER2_D14=1, S2DISC_D15=1. Fact records used: 53
(one per learn). No domain applies the wrong schema kind.

## Kill bars (all must pass)

- K1 (policy ported): the implementation contains no slot array and
  no slot scan; every experience read/write goes through the
  substrate fact API (flearn/fquery on substrate records); the
  policy functions (gate, apply, fallback, retire, discover,
  discover2) are present and drive the run. Verified by source
  audit (grep). Kill: any parallel experience store, or any policy
  function missing/bypassed.
- K2 (15-domain sequence): all frozen markers and counters match:
  TRANSFER_OK==1, SEL_CORRECT==7/7, CONSEC_RET_D11==1,
  REDISCOVER_D12==1, APPLY_D13==1, LEDGER2_D14==1, S2DISC_D15==1,
  OPS_P7==53, OPS_P7 < OPS_FRESH. Kill: any marker or counter
  mismatch.
- K3 (purity and determinism): pure Zag at every stage (source, znc
  build, execution, analysis); zero Python invocations; zero
  em-dash bytes in all wave files (byte-checked); 3/3
  byte-identical runs, exit 0, zero stderr. Kill: any Python use,
  any em-dash byte, or non-identical runs.

Verdict INTEGRATION-TESTED iff K1, K2, K3 all pass. On any port
breakage that requires changing the substrate's record format,
header layout, or API semantics, the verdict is INTEGRATION-BLOCKED
with the required extension documented as architectural evidence
(the port must not silently fork the substrate).

## Notes on what this proves and does not prove

- Proves: the P7 policy does not depend on its bespoke slot array;
  the substrate's generic fact store can host a continuing learner's
  experience with identical policy behavior.
- Does not prove: cross-task transfer (same bounded workload as
  TRANSFER-TESTED), episode/causal integration (unused here), or
  that the substrate is the right long-term host (that needs the
  merged-curriculum test running in substrate_integ/).
- The key cache is an implementation convenience, not a semantic
  change: without it, repeated query-key interning would consume
  roughly 3.5KB of the 4KB string budget. Semantics are identical
  either way.

## Commit order

This prereg is committed alone. The implementation commit must be a
strict descendant. Verified via git merge-base --is-ancestor before
the result is reported.
