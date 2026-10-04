# Substrate-Driven Operation Selection: Report

## Verdict: SUBSTRATE-SELECTION-COMPLETE

Operation selection learned from consequence history in the shared
substrate. No task labels. No mode switch. Treatment 7/7, fixed-order
control 3/7. 3/3 deterministic byte-identical runs (sha256
2951d8b8faa2d08c99b98741092be40d93e76e5209c9208c4097fa3ca8fc7378).

## What was built

A fork of the prediction-optional compact world (po_full.zag, 510 lines)
with the tag-61 consequence substrate grafted on (record machinery from
build 02a338dbf). New key type kt=4 (OPSEL): ka = condition signature,
kb = operation id. One new file of machinery (ss_patch.zag, ~200 lines);
the world, operations, and executor are untouched.

Condition signature (6 bits, computed from learner state only):
- bit0 (1): a FACT matching (s,r) exists
- bit1 (2): that FACT is reliable (prov==1)
- bit2 (4): a derive basis exists in state
- bit3 (8): a trusted MAP (score>=6) exists for r
- bit4 (16): any MAP exists for r
- bit5 (32): a proven-but-untrusted predictor (score 3..5) exists

The selection function receives (W,s,r) only. It never receives a task
type label. The signature is a state description, not a category.

Selection rule: for the current signature, score each recorded operation
as (2*successes - attempts - avg_cost/20) and take the argmax. Ties go
to the lower operation id. If no operation has a record, or all recorded
scores are negative, fall back to a fixed default order
(retrieve, derive, verify, predict, construct, inquire).

Recording: after each query the world outcome is compared to the answer
and sub_note writes (signature, op, success, cost). Cost is nodes
allocated plus trial tries. The consequence, not a label, trains selection.

## Training (Phase A): guided consequence experience

Ten problems; each applicable operation is tried and its outcome recorded.
This is curated experience (scaffolding, documented below); the selection
mapping tested in Phase B uses only the recorded consequences.

Census after training (kt=4 records):

| sig | op | succ/att | learned |
|-----|----|----------|---------|
| 3 (fact, reliable) | 1 retrieve | 2/2 | retrieve works |
| 5 (fact, stale, basis) | 1 retrieve | 0/2 | retrieve fails |
| 5 (fact, stale, basis) | 2 derive | 2/2 | derive works |
| 24 (trusted map) | 3 verify | 2/2 | verify works |
| 24 (trusted map) | 5 predict | 2/2 | predict works, costs more |
| 48 (proven predictor) | 5 predict | 2/2 | predict works |
| 16 (untrusted map) | 5 predict | 0/1 | predict fails |
| 16 (untrusted map) | 7 construct | 1/1 | construct works |
| 0 (nothing) | 6 inquire | 1/1 | withhold works |

The substrate holds both positive and negative consequences, including
the critical negative record: retrieve under stale-fact conditions fails.

## Test (Phase B): novel problems, substrate selection only

Seven novel queries (fresh subjects; r=57 is a fresh relation).

| Q | situation | sig | op chosen | ans | exp | ok |
|---|-----------|-----|-----------|-----|-----|----|
| Q1 | fresh fact | 3 | 1 retrieve | 300 | 300 | 1 |
| Q2 | stale fact + basis (TRAP) | 5 | 2 derive | 600 | 600 | 1 |
| Q3 | trusted map | 24 | 3 verify | 13 | 13 | 1 |
| Q4 | proven predictor | 48 | 5 predict | 7 | 7 | 1 |
| Q5 | bad predictor, new relation | 16 | 7 construct | 6 | 6 | 1 |
| Q6 | repeat after construct | 24 | 3 verify | 6 | 6 | 1 |
| Q7 | unanswerable | 0 | 6 inquire | -3 | -3 | 1 |

Treatment: 7/7.

Q2 is the trap: a fixed retrieve-first order returns the stale fact (999).
The substrate selected derive because (sig=5, retrieve) has 0/2 and
(sig=5, derive) has 2/2. No task label was consulted.

Q5/Q6 is the sequence: under sig=16 the substrate chose construct (the
(sig=16, predict) record is 0/1 from training on r=58; this is
cross-relation transfer via the shared signature, r=58 to r=57).
Construction built a trusted MAP for r=57, changing the state; the repeat
query then had sig=24 and selected verify. The two-step
construct-then-verify sequence emerged from state-conditioned selection,
not from a plan or a mode.

Q7: under sig=0 the substrate chose inquire (withhold, -3), the correct
response to an unanswerable query.

## Control: fixed order, substrate never read (ablation)

Same setups, no training, no substrate reads. Fixed order
1,2,3,5,7,6.

| Q | op tried | ans | exp | ok |
|---|----------|-----|-----|----|
| C-Q1 | 1 | 300 | 300 | 1 |
| C-Q2 | 1 | 999 | 600 | 0 (stale-fact trap) |
| C-Q3 | 3 | 13 | 13 | 1 |
| C-Q4 | 5 | 7 | 7 | 1 |
| C-Q5 | 5 | 3 | 6 | 0 (bad predictor) |
| C-Q6 | 5 | 3 | 6 | 0 (never constructed) |
| C-Q7 | 7 | 0 | -3 | 0 (constructed nonsense) |

Control: 3/7.

The control is the ablation: identical operations available, identical
world setups, but selection without consequence history. It falls into
the stale-fact trap, trusts the bad predictor twice, and constructs a
bogus MAP for an unanswerable query instead of withholding. The 4-point
gap is causally attributable to the substrate reads, because writes are
the only other substrate interaction and the control performs none.

## Honest boundaries

1. Training experience is curated (guided exploration tries each
   applicable operation). The learner does not choose its own training
   curriculum. What is learned (the signature to operation mapping) comes
   only from recorded consequences, but the exploration policy is
   scaffolding. Self-directed exploration is future work.

2. The signature is coarse. Predictor quality is captured only via the
   proven-predictor bit and the success/failure records, not as a graded
   reliability in the signature itself. A good predictor under sig=16 on a
   new relation would be misjudged by the r=58 failure record. Finer
   condition features are future work.

3. The Q5 to Q6 sequence is state-conditioned selection across two
   queries, not de novo multi-step plan invention. The learner did not
   compose a novel plan; it selected the right operation at each step as
   the state changed. True sequence invention remains open.

4. Single-example trial overfits (the r=57 MAP computes 3*s+3, correct
   only at s=1). This is a limitation of try_construct_val, not of
   selection, but it bounds the sequence test to the trained subject.

5. Causal (op 4) was excluded from the battery. The experiment tests
   consequence-driven selection over six operations; the principle does
   not depend on the count, but a seventh operation was not exercised.

6. Cost tie-breaking (avg_cost/20) is a researcher-set scale. The
   ordinal claim (cheaper preferred on ties) is principled; the cardinal
   weight is scaffolding.

7. Researcher-owned: signature bit definitions, score formula, default
   order, training curriculum, cost scale. Learner-owned: all success,
   failure, and cost values; every selection decision; the Q2 trap
   avoidance; the Q5/Q6 sequence; the Q7 withhold.

## Architecture accounting (One-System Rule)

- Base: po_full.zag sections 1-9 (429 lines), two small patches
  (world_law r=57; tries stash).
- New: ss_patch.zag (~200 lines: substrate records, signature,
  selection, query/observe). ss_driver.zag (~120 lines).
- The OPSEL records (kt=4) live in the SAME tag-61 substrate as
  PURSUIT/STRATEGY. No new store, no new mechanism family.
- New modes: 0. New bridges: 0. New handlers: 0. New semantic cases: 0.
- This is a sixth consumer of the shared consequence substrate
  (after policy, withholding, abandonment, retention, search-order),
  and the first consumer that selects among cognitive operations.

## Reproduction

- Source: ss_core.zag + ss_patch.zag + ss_driver.zag = ss_full.zag
  (765 lines). Build: build.sh.
- Compiler: pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- Binary: ss_bin. Runs: ss_run1/2/3.txt, byte-identical (sha256
  2951d8b8...).
- Base: prediction_optional/po_full.zag (frozen TNN-2 untouched).
- Pure Zag via safebin; `which python3 python` empty; Step 0 in NAMECHECK.md.
