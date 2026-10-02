# RESULT: Learner-Substrate Integration Test

Worker: I1 Learner-Substrate Integration Worker.
Date: 2026-09-30 UTC.
Verdict: **INTEGRATION-TESTED** (all frozen kill bars pass).

Prereg: `ff7558bff` (committed alone before any implementation;
verified strict ancestor of the implementation commit via
`git merge-base --is-ancestor`).
Implementation: `lsub.zag` (this directory, pure Zag, self-contained).
Raw: `LSUB_RAW_1.txt` (md5 `a5f56602660cda7f1bd8a333203530d6`).
Determinism: 3/3 byte-identical, exit 0, zero stderr on all runs.
Governance: pure Zag at every stage (znc, bash, grep, git only; no
Python in source, build, execution, or analysis); zero non-ASCII bytes
in wave files (byte-checked); prereg strictly precedes implementation;
commits local on `tnn-native-lab`, owned paths only
(`docs/lab/research-lead/overnight-20260928/learner_substrate/`).

## 1. What was built

The P7 continuing-learner policy from `contlearn3.zag`
(TRANSFER-TESTED, `08d7c9fd5`) was ported onto the shared substrate
from `substrate.zag` (SUBSTRATE-PROTOTYPED, `2835e5641`):

- The 64 x 20-byte integer slot array is deleted. All experience
  lives in the substrate's string-interned fact triple store.
- Subjects map to entity keys ("s" + decimal subject id; subjects
  are unique per domain so no domain field is needed), relation 1
  maps to "r1", objects map to decimal strings. Each distinct key
  is interned exactly once via a small key cache.
- `flearn` / `fquery` implement the exact record semantics of the
  substrate's `sub_fact_learn` / `sub_fact_query` (append record,
  latest-wins lookup, conflict counting) on the substrate's fact
  record format, using only its primitives.
- Schema state (kind, default, exception subject/object) and the
  seventeen counters live in a policy region at POL=30000, above the
  substrate string pool ceiling. Schema state is policy state, not
  domain experience; the substrate keeps analogous policy-adjacent
  state (ep_processed, conflicts) in its header.
- The policy logic (gates, apply/refit, fallback, both retirement
  triggers, kind-1/kind-2 discovery) is a behavioral port of
  contlearn3. The frozen 15-domain workload (`true_obj`) is
  identical.
- Episodes and the causal entry machinery are present in the
  workspace (via verbatim `sub_init`) but unused by this workload;
  nvar=1. Disclosed, not hidden.

## 2. Kill bar evaluation

- K1 (policy ported): PASS. Source audit: zero occurrences of slot
  machinery (`sbase`, `free_slot`, slot scans). Every experience
  read/write goes through `flearn`/`fquery` on substrate records.
  All policy functions present (gate1_pass, gate2 inline, apply,
  fallback, retire_ledger, retire_consec, discover, discover2) and
  drive the run. No parallel experience store exists.
- K2 (15-domain sequence): PASS. Every frozen marker matches:
  TRANSFER_OK=1, SEL_CORRECT=7/7, CONSEC_RET_D11=1,
  REDISCOVER_D12=1, APPLY_D13=1, LEDGER2_D14=1, S2DISC_D15=1,
  OPS_P7=53, OPS_FRESH=60. The D1-D8 event sequence matches the
  frozen expectations exactly (SCHEMA_DISC obj=4; applies at D2, D3;
  ledger retirement at D4; rediscovery at D5; kind-2 supersession at
  D6 with excabs=62 excobj=9; APPLY2 at D7; fallback at D8).
- K3 (purity and determinism): PASS. Pure Zag; zero Python; zero
  non-ASCII bytes; 3/3 byte-identical runs, exit 0, zero stderr.
- K3a: PASS (kind-1 discovered at D1).
- K3b: PASS (53 < 60).
- K3c: PASS (FACT_RECORDS=53 equals OPS_P7: exactly one substrate
  fact record per learn, no hidden storage).

No substrate extension was required: no record-format change, no
header change, no new API. The port used only existing substrate
primitives.

## 3. Interpretation

1. The P7 policy does not depend on its bespoke slot array. The
   substrate's generic fact store hosts the full 15-domain
   continuing-learner run with identical policy behavior: same
   discoveries, same applies, same fallbacks, same retirements,
   same transfer and interference outcomes, same op count (53).
2. FACT_CONFLICTS=0 is correct, not a bug: subjects are unique per
   domain and each is learned once, so no (entity, attr) pair is
   ever re-taught with a different value. The conflict counter
   works (it is the substrate's own); this workload simply never
   triggers it.
3. The key cache is an implementation convenience with identical
   semantics to naive interning; without it, repeated query-key
   interning would consume roughly 3.5KB of the 4KB string budget.
   With it, the whole run uses a fraction of the budget.

## 4. What breaks / extensions needed

Nothing broke. Required extensions for the substrate: none for this
workload. Honest gaps for future work:

- The episode/causal half of the substrate is unexercised here.
  A workload that interleaves fact learning with causal episodes
  (e.g., the merged curriculum test in `substrate_integ/`) is the
  next integration step, not this wave.
- Transfer remains form-to-novel-values within one relational
  template (same bound as TRANSFER-TESTED). The substrate does not
  change that bound; it only changes where experience lives.
- Schema state as integers in a side region is a porting choice.
  A deeper integration could represent schemas as substrate facts
  too; that would test whether the policy itself can be
  substrate-native. Not attempted here.

## 5. Honest scope and limits

- Bounded L1/L2, not L3. Two researcher-supplied schema forms; the
  policy decides persistence and kind selection; the learner fills
  values. The substrate changes the storage substrate, not the
  learning class.
- No SURVIVES claim: promotion needs the full 11-step pipeline.

## 6. Files

- `PREREG_LSUB.md` (ff7558bff, frozen before implementation)
- `lsub.zag` (implementation, pure Zag)
- `LSUB_RAW_1.txt` (md5 a5f56602660cda7f1bd8a333203530d6; runs 2, 3 identical)
- `LSUB_RAW_2.txt`, `LSUB_RAW_3.txt` (determinism evidence)
- `LSUB_ERR_1.txt`, `LSUB_ERR_2.txt`, `LSUB_ERR_3.txt` (zero bytes each)
- `LSUB_RESULT.md` (this file)
