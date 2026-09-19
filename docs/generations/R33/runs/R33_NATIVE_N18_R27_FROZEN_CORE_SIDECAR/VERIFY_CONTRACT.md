# R33-N18 verification contract

This is a design-time verification inventory. It authorizes no execution.

## Classification vocabulary

- `DIRECT_NATIVE_RECOMPUTATION`: the final native candidate must calculate and
  assert the value itself.
- `NATIVE_EQUIVALENT_REQUIRES_REVIEW`: a native implementation may be used only
  after the exact mapping and boundary are reviewed and pinned.
- `HISTORICAL_WITNESS_ONLY`: retained historical material may corroborate a
  claim but cannot act as a new gate.
- `DEFERRED_BLOCKER`: an unresolved prerequisite prevents registration or
  exposure.

## Required checks

| Check | Classification | Required outcome |
|---|---|---|
| canonical R27 raw bytes | DIRECT_NATIVE_RECOMPUTATION | exact SHA256 equals the custody pin before and after every stage |
| canonical format/step/restarts | DIRECT_NATIVE_RECOMPUTATION | `TNN_PRE_V1_R27_GENERAL_LEARNING`, 60423, 0 |
| N10 map identity | DIRECT_NATIVE_RECOMPUTATION | exact pinned map manifest and page checks |
| R27 semantic continuity | DEFERRED_BLOCKER | N17 full continuity or approved methodology amendment before exposure |
| parent runtime behavior | DEFERRED_BLOCKER | no surrogate may be silently treated as canonical R27 |
| R27-to-sidecar feature/output mapping | DEFERRED_BLOCKER | exact dimension, encoding, residual composition and arm19 mapped-space semantics must be pinned |
| N16 arm19 mechanism identity | DIRECT_NATIVE_RECOMPUTATION | exact algorithm/build/input pins; no retuning |
| stage seed namespaces | DIRECT_NATIVE_RECOMPUTATION | 1210000/1310000/1410000, mutually disjoint from N16 |
| C0/C1/C2/C3 condition identity | DIRECT_NATIVE_RECOMPUTATION | exact condition mapping and fixed output-delta semantics |
| training/evaluator separation | NATIVE_EQUIVALENT_REQUIRES_REVIEW | no probe/holdout data reaches sidecar fitting or gates |
| parent write isolation | DIRECT_NATIVE_RECOMPUTATION | write attempts refuse; canonical hash unchanged |
| paired population accounting | DIRECT_NATIVE_RECOMPUTATION | 40/64/64 condition-population rows as applicable |
| primary win rule | DIRECT_NATIVE_RECOMPUTATION | native confirmation gate only; no external rescoring |
| stage gates and multiplicity | DIRECT_NATIVE_RECOMPUTATION | fixed 10/16/16 paired gates; one confirmatory C2-vs-C0 claim; controls cannot rescue a failed gate |
| C1 wrapper control | DIRECT_NATIVE_RECOMPUTATION | every C0/C1 row, decision and counter must match exactly |
| C3 randomized/untrained control | DIRECT_NATIVE_RECOMPUTATION | cannot satisfy C2 rule or the fixed nonspecific-benefit sentinel |
| historical N16 result | HISTORICAL_WITNESS_ONLY | supports mechanism identity only; not R27 evidence |
| historical 33/33 R27 receipt | HISTORICAL_WITNESS_ONLY | never a new native continuity gate |
| canonical mutation/authority/promotion | DIRECT_NATIVE_RECOMPUTATION | all remain false for N18 |
| resource/capacity refusal | NATIVE_EQUIVALENT_REQUIRES_REVIEW | explicit bounded native behavior and receipts |
| literal result substitution | DIRECT_NATIVE_RECOMPUTATION | expected values cannot replace recomputation |
| complete pre-freeze custody manifest | DEFERRED_BLOCKER | every map/substrate/source/fixture/compiler/input hash must be bound before admission |
| exact sidecar ABI and dataflow | DEFERRED_BLOCKER | no synthetic N16 interface may be laundered into R27 behavior |
| C3 randomization manifest | DEFERRED_BLOCKER | exact PRNG, range, norm, seed derivation and no-update behavior must be frozen before admission |
| response/refusal encoding | DIRECT_NATIVE_RECOMPUTATION | status values and zero residual/choice refusal semantics are fixed |
| stage-relative C3 sentinel | DIRECT_NATIVE_RECOMPUTATION | development old-loss limit10; validation/confirmation limit16, even without full C2 win |
| native parent runtime/evaluator | DEFERRED_BLOCKER | exact ABI, state, evaluator, refusal and resource identity required |

## Terminal dispositions

Allowed design-stage dispositions are:

- `REQUEST_CHANGES`;
- `APPROVE_FOR_PREREGISTRATION_ONLY_NO_EXECUTION_AUTHORIZATION`.

Any later postrun disposition must preserve the narrower claim class selected
by the prerequisite path. No reviewer may authorize canonical mutation or
promotion through N18.
