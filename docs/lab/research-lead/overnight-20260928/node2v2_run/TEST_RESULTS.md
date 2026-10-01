# Node2-v2 Test Results

## Test Design (per frozen prereg Section 5)

Three-phase sealed discrimination test:

**Phase 1 (baseline):** 3 miss/resolve cycles on relation R1.
- Observations reveal `a_w` = 30 (confirming default) or `a_w` = -1 (neutral).
- Prediction: default remains 30. Tests no spurious shift without differential evidence.

**Phase 2 (shift):** 3 miss/resolve cycles on relation R2.
- Observations consistently reveal `a_w` = 45.
- Prediction: after third revelation, default shifts 30 -> 45.

**Phase 3 (confirmation):** 1 miss on relation R3.
- Prediction: new guide created with action 45.

## Results (3/3 byte-identical)

SHA-256: `74c48d5a85087eab5d9c86aebf6075ce69f89be5736422e6bf63e897f527aae9`

### Phase 1: PASS (no shift)

Default action after 3 cycles: 30.
- Cycle 1: a_w=30, history=(30,-1,-1), no shift (not all equal).
- Cycle 2: a_w=-1, history unchanged, no shift.
- Cycle 3: a_w=30, history=(30,30,-1), no shift (not all equal).
- Final default: 30. Correct.

### Phase 2: PASS (shift after 3 consistent revelations)

Default action progression:
- After cycle 1 (a_w=45): history=(45,-1,-1), default=30 (no shift).
- After cycle 2 (a_w=45): history=(45,45,-1), default=30 (no shift).
- After cycle 3 (a_w=45): history=(45,45,45), all equal, A=45 != 30.
  WRITE FIRES: field 20 := 45. History reset to (-1,-1,-1).
- Final default: 45. Correct.

### Phase 3: PASS (new guide carries 45)

Miss on R3 creates guide. Guide action: 45.
`miss_inquire` read field 20 (=45). Correct.

## Kill Bar Evaluation

| Kill Bar | Result |
|----------|--------|
| Default does not shift after 3 consistent a_w=45 | PASS (shifted to 45) |
| Default shifts during Phase 1 | PASS (stayed 30) |
| Default shifts on fewer than 3 revelations | PASS (shifted exactly on 3rd) |
| Write fires but Phase 3 guide still carries 30 | PASS (guide carries 45) |
| 3/3 byte-identical runs | PASS (SHA-256 match) |

## K-H3 Verdict: PASS

All six K-H3 audit elements satisfied:

1. **Structural decision:** which action new inquiry guides suggest (default action).
2. **Learner-state node/fields:** tag 40, subtype 2, field 20.
3. **Production read path:** `miss_inquire` reads field 20 (transcript: Phase 3 guide carries 45).
4. **Production write path:** `resolve_uncertainty_v2` writes field 20 (transcript: shift 30->45 on 3rd revelation).
5. **Triggering experience:** `ev_observe_aw` events with `a_w` >= 0 resolving open uncertainties.
6. **Sealed demonstration:** this test (builder-sealed; independent adversary preferred for replication).

Failure-condition pre-check:
- (a) Source-literal: NOT FAILED (decision read from field 20).
- (b) Read-only policy: NOT FAILED (write fired on transcript).
- (c) Unreachable write path: NOT FAILED (reachability proven by construction; write fired).
- (d) Researcher-encoded histories: NOT FAILED (world revealed actions; learner applied 3-revelation rule).

## Standing Metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 6
  (policy node field layout; 3-revelation threshold; history bound of 3;
   copy-then-revise bootstrap; ev_observe action-channel extension;
   reset-on-update)
- LEARNER-OWNED STRUCTURAL DECISIONS: 1
  (the default action value = 45 during Phase 2/3; set by experience)
- SOURCE-ENUMERABLE FORMS: action values are i32; the specific values
  (30, 45) come from world/sealed test, not enumerated in source.
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: the default action (field 20), and the
  revealed-action evidence (history slots) that set it.
- REUSE EVENTS: 4 (policy node read by miss_inquire for 4 guide creations
  in Phases 2-3 after initialization)
- REVISION EVENTS: 1 (field 20 write: 30->45, triggered by three a_w=45
  revelations on transcript)
- COGNITION LINES: ~100 (new/modified vs frozen)
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## Non-Claims (per prereg Section 6)

This result does NOT establish: inquiry discrimination, learner-authored
procedures, SUF, L3, H1, capability improvement on frozen batteries,
or a general solution to exploration. The 3-revelation threshold, history
bound, and bootstrap remain researcher-chosen.

## Limitations

- Builder-sealed worlds (not independent adversary). Hash transparency
  provided; independent replication preferred.
- Action values (30, 45) are small integers; the mechanism is value-agnostic
  but only tested on these.
- Single policy node; multiple concurrent policies not tested.
