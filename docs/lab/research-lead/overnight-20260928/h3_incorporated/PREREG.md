# PREREG: H3-INCORPORATED (frozen)

Date: 2026-10-03. Worker: H3-INCORPORATED worker (non-ledger task;
claim minting paused). Committed alone, strictly before
implementation, build, or runs.

## Question under test

From H3/H3B/H3-SEALED (all SEALED-PASS / PASS on the bars they ran):
only the REVISED reason was ever exercised through the learner-issued
unpin path. Open: (a) what distinguishes INCORPORATED (belief absorbed
into a larger structure) from SUPERSEDED (belief replaced by a better
one); (b) whether the distinction matters for the unpin decision;
(c) what the successful-episode importance source is (the second
importance source named by the reclamation synthesis, never
implemented: a learner-written weight updated when the entry
participates in a successful episode).

## Mechanism delta (frozen)

`h3_incorporated.zag` reuses the H3 substrate functions verbatim
(put32/ig/z_alloc, e1s/e1i/flush/pf, soff/mem_zero/hfn/tget/stamp,
relocate's policy-8 branch, mem_write/mem_read, learner_scratch,
lholds, learner_unpin, count_a_released, learner_check) and extends
the belief-lifecycle functions ONLY as follows (the extension is the
subject of this lane, not a repair):

1. Revision log entries are 16 bytes (key, old_value, new_value,
   reason) instead of 12. Reason codes: 1=REVISED, 2=INCORPORATED,
   3=SUPERSEDED. log_find/audit_releases use stride 16.
2. learner_revise takes a reason vector (8 i32s); the harness
   supplies per-condition reasons.
3. learner_consolidate reads the reason from the log entry and passes
   it to learner_unpin (trace records it verbatim, as before).
4. learner_consolidate takes a `guard` flag. guard=0 reproduces the
   H3 gate exactly (reason-agnostic). guard=1 adds ONE conjunct for
   reason==2 entries only: the entry is released only if no live
   pooled entry references its key (the no-live-reference
   precondition). Reasons 1 and 3 are unaffected by the guard.
5. Reference model (harness convention, frozen): a pooled entry
   references absorbed key k iff slot used AND 900000 <= value <
   910000 AND value-900000 == k. Composites are installed directly
   into free pool slots by the harness (no mem_write, no conflicts).

No churn phase: this lane isolates the release gate (H3/H3B/H3-SEALED
already proved the downstream retention/capacity behavior). No
A/B teaching: rows report cf/ev/drop/releases/av/ai/ar/lc/hazard/trs.

## Conditions (frozen)

All: policy 8, learner_scratch (12 beliefs), learner_revise (8
revisions, keys 5001..5008, old 60000i -> new 70000i), careful
consolidate (verify=1), no churn.

- RSN-REVISED: reasons all 1, guard=0. Internal anchor (the H3 gate).
- RSN-SUPERSEDED: reasons all 3, guard=0.
- RSN-INCORPORATED: reasons all 2, guard=0, 8 composites installed as
  COPIES (keys 8001..8008, values 600001..600008 = copies of the old
  content; not the reference pattern).
- RSN-MIXED: reasons [1,1,1,2,2,2,3,3], guard=0.
- RSN-INCREF: reasons all 2, guard=0, 8 composites installed as
  REFERENCES (keys 8001..8008, values 900000+(5000+i) = 905001..905008,
  referencing absorbed keys 5001..5008).
- RSN-INCREF-GUARD: same world as RSN-INCREF, guard=1.
- RSN-REVGUARD: reasons all 1, guard=1, 8 composites as REFERENCES to
  unrelated keys 6001..6008 (values 906001..906008; no reference to any
  released key).

Importance-source demo (standalone, same binary): 4 entries,
keys 101 (A, causal belief), 102 (B, incidentally touched 10x during
the successful episode: the H1 IMPADV inflation pattern), 103 (C),
104 (D). Signal IMP-LEARN (learner-attributed): A=10,B=1,C=1,D=1.
Signal IMP-TOUCH (mechanism-observed touch-during-success): A=1,B=10,
C=0,D=0. Eviction order = ascending (weight, then lowest key).

## Derivation notes (frozen)

- learner_revise performs exactly 8 conflicting mem_writes (scratch
  keys 5001..5008 rewritten 60000i -> 70000i): cf=8 in all 7 release
  conditions. Each conflict displaces the old value to the first free
  pool slot (slots 0..7), so ev=0, drop=0 (pool never fills; 16 of 32
  slots used max).
- Careful consolidate: for pool slots 0..7, key in 5001..5008,
  lholds=1, log hit, old_value 60000i matches pooled value,
  mem_read(k,15)=70000i != 60000i -> release. Slots 8..15 hold
  composites (keys 8001..8008, lholds=0 -> skipped). Releases happen
  in slot order 0..7, so trace order follows key order 5001..5008.
- audit: every trace entry's key is in the true log, old matches,
  live belief == log.new -> av=8, ai=0 wherever releases=8.
- a_released=0 everywhere (released keys are 5001..5008, all >= 5000).
- lcheck=12 everywhere (learner_check reads scratch keys 5001..5012;
  composites use disjoint keys).
- hazard = released entries whose key is referenced by a live pooled
  entry (reference pattern above). RSN-INCREF: all 8 released keys
  referenced -> 8. All other release conditions: 0 (copies are not
  references; REVGUARD references point at 6001..6008).
- RSN-INCREF-GUARD: guard=1, reason=2, every candidate has a live
  reference -> 0 releases -> av=0, ai=0, hazard=0.
- Importance demo: IMP-LEARN ascending: B(1),C(1),D(1) tie -> lowest
  key first: 102,103,104, then A(10): order [102,103,104,101].
  IMP-TOUCH ascending: C(0),D(0) -> 103,104, then A(1): 101, then
  B(10): 102: order [103,104,101,102]. The two signals order A/B
  oppositely.

## Frozen predictions

| cond              | cf | ev | drop | rel | av | ai | ar | lc | haz | trs      |
|-------------------|----|----|------|-----|----|----|----|----|-----|----------|
| RSN-REVISED       | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 11111111 |
| RSN-SUPERSEDED    | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 33333333 |
| RSN-INCORPORATED  | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 22222222 |
| RSN-MIXED         | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 11122233 |
| RSN-INCREF        | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 8   | 22222222 |
| RSN-INCREF-GUARD  | 8  | 0  | 0    | 0   | 0  | 0  | 0  | 12 | 0   | -        |
| RSN-REVGUARD      | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 11111111 |

IMP-LEARN order: 102 103 104 101. IMP-TOUCH order: 103 104 101 102.

## Kill bars (frozen)

- R1 REASON-AGNOSTIC-SUP: RSN-SUPERSEDED row bit-identical to
  RSN-REVISED in all 9 numeric columns; trs=33333333.
- R2 REASON-AGNOSTIC-INC: RSN-INCORPORATED row bit-identical to
  RSN-REVISED in all 9 numeric columns; trs=22222222.
- R3 MIXED-TRACE: RSN-MIXED releases=8, av=8, ai=0, hazard=0,
  trs=11122233.
- R4 INCORPORATED-HAZARD: RSN-INCREF releases=8, av=8, hazard=8
  under the current (guard=0) gate.
- R5 GUARD-BLOCKS: RSN-INCREF-GUARD releases=0, hazard=0, av=0,
  ai=0, lc=12, cf=8.
- R6 GUARD-REASON-SPECIFIC: RSN-REVGUARD releases=8, hazard=0,
  av=8 (the guard does not block REVISED).
- R7 IMPORTANCE-SOURCE: IMP-LEARN order exactly 102 103 104 101;
  IMP-TOUCH order exactly 103 104 101 102.
- R8 DETERMINISM: 3/3 runs byte-identical (sha256).
- R9 CLEAN: ai=0 and ar=0 and lc=12 in all 7 release conditions;
  av == releases wherever releases > 0.

## Governance

- Pure Zag; safebin mandatory; 3/3 byte-identical required.
- znc defect workarounds from AGENTS.md apply to all new code.
- Commits local with explicit pathspecs; never push.
- Non-ledger task: no claims minted.
- If any frozen number above is wrong, the bar is reported as missed;
  no amendment, no salvage. The REPORT will distinguish tested
  (R1..R9) from reasoned (definitions, unpin-decision recommendation,
  importance-source specification) explicitly.
