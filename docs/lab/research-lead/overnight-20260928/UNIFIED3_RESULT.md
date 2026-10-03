# UNIFIED3 RESULT: H-UNIFIED3 SURVIVES (14/14)

**Date:** 2026-09-29
**Prereg:** PREREG_UNIFIED3.md (commit 4bf96904b, frozen before implementation)
**Implementation:** unified3_learn.zag (this directory)
**Raw evidence:** UNIFIED3_RAW_OUTPUT.txt (md5 4edce60da23687fb4556b5b2448c9dcf, 3/3 byte-identical)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere.

## Verdict: H-UNIFIED3 SURVIVES (14/14)

Both H-UNIFIED2 red-team downgrades are repaired at the composition
layer. All 12 original frozen tests pass unchanged; the 2 new frozen
tests pass.

## What was built

`unified3_learn.zag` = `unified2_learn.zag` copied verbatim, then:

**Repair A (X-U2-2a poison-first): explicit authoritative revision channel.**
- `route_line` strips a leading `!` (byte 33) and maps a would-be
  CAUS_LEARN (2) to new code 6 = CAUS_REVISE. `!` on any other shape
  routes WITHHOLD with an explicit reason. `route_name(6)` =
  "CAUS_REVISE".
- `handle_caus_revise` strips the marker, bypasses the coherence gate,
  and commits via `clearn` directly: contradicting episode marks the old
  ACTIVE rule CONFLICTED (rc=2); a repeated episode learns the corrected
  rule (rc=1). Same honest accounting as the stream handler, minus
  quarantine.
- Trust distinction (frozen): the unlabeled stream is UNTRUSTED
  (gated, append/corroborate-only, first-writer-wins by design); the
  explicit channel is the operator/researcher asserting authority.
  Veracity has a path; it is not the unlabeled path.

**Repair B (X-U2-2b capacity): honest accounting + explicit policy.**
- `clearn` now returns i32: 1 = new rule stored, 0 = corroborated,
  2 = conflict marked, -1 = dropped (store full). Matching and storage
  logic are byte-identical in behavior to H-UNIFIED2.
- `handle_caus_learn` returns the STORED count (not episodes handed to
  `clearn`), reports stored / corroborated / quarantined / dropped
  separately, emits an explicit `USTOREFULL` warning per dropped
  episode, and keeps a cumulative dropped counter at W[DCOUNT()]
  (address 65008).
- Capacity policy (frozen): REFUSE-WITH-WARNING. Verified knowledge is
  never evicted; queries on dropped states withhold. Eviction policy is
  future work (H-MEM lane).

## Frozen bar results

- **K-U3-1 PASS:** Route check `!1,0,0>1,0;1,0,0>1,0` -> 6. Stream
  poison first: stored=1, cpredict(1,0,0) yields s1=9 (poison ACTIVE).
  Late stream truth: stored=0, quarantined=2 (gate unchanged; the
  stream's order-dependence is documented, not hidden). Explicit
  revise: stored=2 (poison R0 CONFLICTED, corrected rule learned),
  active count 1, cpredict(1,0,0) yields s1=0. Stream truth then
  corroborates: stored=0, quarantined=0.
- **K-U3-2 PASS:** 16 distinct coherent states fill the store
  (active=16). Legitimate novel `99,0,0>0,1` x2: handler returns 0
  stored, dropped delta=2 (DCOUNT), explicit USTOREFULL warnings
  emitted, active stays 16, cpredict(99,0,0) withholds (returns 0).
- **K-U3-3 PASS:** All 12 original H-UNIFIED2 checks pass unchanged
  (K-U1, K-U2a, K-U2b, K-U2c, K-U3, K-U4a, K-U4b, K-U5, K-A, K-U2-1,
  K-U2-3a, K-U2-3b). Note: K-U2-1 expects ncommitted==0; the handler
  now returns the STORED count and quarantined episodes never reach
  `clearn`, so stored=0 still holds.
- **K-U3-4 PASS:** 3/3 runs byte-identical (cmp),
  md5 4edce60da23687fb4556b5b2448c9dcf.

## Source audit (self)

- `handle_caus_revise` contains no test-answer literals.
- The `!` marker check (`line[0]==33`) is structural.
- `clearn` return-code addition changes no matching/storage logic.
- Query path untouched from H-UNIFIED2.

## Honest limitations (carried from prereg)

1. The unlabeled stream remains first-writer-wins; the explicit channel
   is the only correction path. No autonomous veracity judgment.
2. Capacity policy is refuse-with-warning, not eviction. A continuing
   learner will eventually refuse all novel causal learning at 16
   slots.
3. The `!` marker is a researcher/operator affordance, not a learned
   trust signal.
4. Procedure/bridge stores have no analogous explicit revision channel
   (causal only).

## Classification

Bounded L2 integration repair, not L3. Closes both H-UNIFIED2
downgrades with explicit, tested mechanisms. Recommended follow-up:
independent red team on unified3 (attack the revise channel for
authority spoofing, and the refuse-with-warning policy for liveness).
