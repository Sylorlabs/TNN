# PREREG: Continuing Learner Extension (Noise + Second Schema Kind)

Frozen before any implementation or test execution. This prereg commits
the workload, the two extensions, and the kill bars. Any amendment must
be committed transparently and re-frozen before implementation; no bar
may be altered after seeing results.

## Context

P7 Integration (INTEGRATION-PROTOTYPED, `9844fb753`) left two gaps:
1. The accuracy-ledger retirement trigger was implemented but never
   exercised (exact-match retrieval gave 4/4 on both paths, ledger 0).
2. Only one schema kind (single-relation default rules).

This wave closes both gaps in one continuing learner, single main(),
no resets, no task labels, pure Zag.

## Extension 1: noise so the ledger trigger fires

Domains carry exceptions to the default. When a domain's default holds
for the 3 gate probes but an exception sits in the unprobed slot, the
gate passes, the schema applies, and the schema path scores 3/4 while
the fresh path is assumed 4/4 (same convention as v1: acc_f = 4).
Ledger goes -1 and the schema retires via the LEDGER trigger with
consec = 0, proving the ledger trigger (not the consecutive-rejection
trigger) did the work. Retirement emits the distinct marker
SCHEMA_RETIRED_LEDGER (vs SCHEMA_RETIRED_CONSEC).

## Extension 2: second schema kind (default + single exception)

Schema kind 2 form: (rel R, default D, exc_abs E, exc_obj O).
Semantics: queries for (subj, R) with no instance return O if
subj == E, else D. The exception position is refit per domain from the
3 probes: the gate passes iff exactly two probes agree and one differs;
the minority value becomes exc_obj, its probe position becomes the
exception position, the majority becomes default. The unprobed slot is
assumed to follow the default (disclosed inductive bias; if it does
not, the ledger will show it on a later noisy domain).

Discovery: after a fallback (all 4 instances present), if kind-1
uniform discovery fails, kind-2 discovery installs the schema when
exactly one of the four instances differs from the other three.
Kind-2 discovery supersedes a live kind-1 schema (new incarnation:
consec and ledger reset; the supersession is counted and disclosed).

Query order: instance first, then live schema (kind-1 or kind-2).

## Frozen workload (8 domains, 4 slots each, rel = 1, subj = d*10+i)

- D1: (4,4,4,4) uniform. Discover kind-1 (obj 4). learns 4.
- D2: (2,2,2,2) uniform. Kind-1 gate passes. Apply, refit obj 2.
  acc 4/4, ledger +0. learns 3.
- D3: (0,0,0,0) uniform. Apply, refit obj 0. acc 4/4. learns 3.
- D4: (6,6,6,1) noisy, exception in slot 3 (unprobed). Kind-1 gate
  passes (probes 6,6,6). Apply, refit default 6. Slot-3 query via
  schema returns 6, truth 1: acc 3/4. Ledger -1. Retire via LEDGER
  trigger with consec 0. Marker SCHEMA_RETIRED_LEDGER. learns 3.
- D5: (5,5,5,5) uniform, no live schema. Learn 4, rediscover kind-1
  (obj 5). Marker REDISCOVER.
- D6: (3,3,9,3) kind-2 pattern, exception in probed slot 2. Kind-1
  gate fails (probes 3,3,9). Fallback (learn slot 3, consec 1).
  Kind-1 discover fails; kind-2 discover succeeds (default 3,
  exc_abs 62, exc_obj 9). Supersedes kind-1. Marker SCHEMA2_DISC.
  learns 4.
- D7: (7,7,4,7) kind-2 pattern, exception in probed slot 2. Kind-2
  gate passes (probes 7,7,4: two agree, one differs at pos 2).
  Apply: refit default 7, exc_abs 72, exc_obj 4. Slot-3 query via
  schema2 returns default 7, truth 7: acc 4/4. Marker APPLY2.
  learns 3.
- D8: (2,8,4,6) mixed. Kind-2 gate fails (probes 2,8,4: no pair
  agrees). Fallback (learn slot 3, consec 1). Kind-2 discover fails
  (no single exception). Marker DOM 8 GATE2=0 FALLBACK. learns 4.

Frozen expectations:
- OPS_P7 = 4+3+3+3+4+4+3+4 = 28. OPS_FRESH = 32. 28 < 32.
- LEDGER ends 0 (reset at D4 retirement and D6 supersession; D7 +0).
- RETIRED_LEDGER = 1, S2DISC = 1, S2APP = 1, SUPERSEDED = 1,
  APPLIES = 4 (D2, D3, D4, D7).
- Retired-consec count = 0 (no domain pair reaches consec 2).

## Kill bars (all must pass)

- K1 (ledger trigger exercised): RETIRED_LEDGER == 1 and the D4
  retirement marker shows consec 0. Kill: retirement only via
  consecutive rejections, or no ledger retirement at all.
- K2 (second schema kind works): S2DISC == 1 (kind-2 discovered at
  D6) and S2APP == 1 (kind-2 applied at D7 with 4/4 acc). Kill:
  kind-2 never discovered or never applied.
- K3 (purity and determinism): pure Zag at every stage (source, znc
  build, execution, analysis); zero Python invocations; zero em-dash
  bytes in all wave files (byte-checked); 3/3 byte-identical runs,
  exit 0, zero stderr. Kill: any Python use, any em-dash byte, or
  non-identical runs.

Supporting checks (reported, must hold for the verdict):
- K3a: kind-1 schema discovered at D1 (DISCOVERED >= 1).
- K3b: OPS_P7 < OPS_FRESH (28 < 32).

Verdict LEARNER-EXTENDED iff K1, K2, K3, K3a, K3b all pass.

## Commit order

This prereg is committed alone. The implementation commit must be a
strict descendant. Verified via git merge-base --is-ancestor before
the result is reported.
