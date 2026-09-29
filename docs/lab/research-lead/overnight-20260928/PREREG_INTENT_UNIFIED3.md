# PREREG H-INTENT-UNIFIED3: Repair of the IU2-ADV Red-Team Downgrade

## Hypothesis

The two IU2-ADV findings (X-IU2-1 verbatim-vs-verbatim heuristic
resolution, X-IU2-3 silent 16-cap truncation) and the X-IU2-3b latent
bridge_learn crash can be repaired by (a) extending the ambiguity
guard to verbatim conflicts: withhold AMBIGUOUS when the top two
candidates both carry verbatim training evidence (em=1) for the exact
query but produce different answers, so no heuristic term (cf/lm)
silently resolves a genuine training contradiction; (b) emitting an
explicit warning when the 16-input record cap truncates training
inputs, making the boundary explicit instead of silent; (c) sizing the
bridge_learn split index buffers by npairs instead of a fixed 16
entries, closing the out-of-bounds crash. All frozen H-INTENT-UNIFIED2
behaviors are preserved.

## Background

- H-INTENT-UNIFIED2 DOWNGRADED by IU2-ADV (report IU2_ADV_RESULT.md,
  commit d9d1d9cca; prereg 130109b6b):
  X-IU2-1 SUCCESS (verbatim-vs-verbatim conflict resolved silently by
  the cond_fire heuristic: proc em=1 score 50000 vs bridge em=1 cf=1
  score 60000, bridge wins with no withhold);
  X-IU2-2 CONTROL-PASS (pure em tie withholds; guard works);
  X-IU2-3 BOUNDARY confirmed (17th training input silently dropped
  from the record, in_count=16, em=0; heuristic wins over genuine
  unrecorded evidence);
  X-IU2-3b LATENT CRASH, pre-existing from H-UNIFIED (f5dd7cdc7):
  bridge_learn s1idx/s2idx are z_alloc(64) = 16 fixed i32 entries but
  n1/n2 can reach npairs; 18-pair fixture panics with slice index out
  of bounds;
  X-IU2-4 source audit PASS.
- The 5/5 frozen H-INTENT-UNIFIED2 repair bars still pass; the
  downgrade narrows the "X-IU2 CLOSED" and 16-cap claims.
- The flaw is inherited from H-INTENT, so the repair is applied
  identically to intent_learn.zag (standalone) and unified_learn.zag
  (port), preserving the X-IU4 faithfulness invariant.

## Root causes (from the red team)

1. X-IU2-1: the em specificity term protects verbatim evidence against
   a heuristic ONLY when the heuristic side has no verbatim evidence
   of its own. When both sides have em=1, the cf (20000) or lm (10000)
   terms break the tie silently. The qscore-tie ambiguity guard never
   fires because the scores differ. The training data genuinely
   contradicts itself ("xab>bax" vs "xab>xxx"), and the mechanism picks
   a winner without reporting the contradiction.
2. X-IU2-3: intent_record_inputs caps at 16 with no diagnostic. The
   17th input vanishes from the record; queries for it lose em
   coverage and can lose to heuristics. Silent degradation.
3. X-IU2-3b: s1idx/s2idx fixed at 16 entries. Beyond 16 pairs on one
   split side, the 17th index write goes out of bounds and the learner
   hard-crashes instead of learning.

## Mechanism (frozen)

### R1. Verbatim-conflict guard (X-IU2-1)

In intent_winner (both files, identical):

- Track em per candidate in a new ce[] array alongside ck[] (kind),
  ci[] (index), cs[] (score).
- After top/second selection and gap computation, before returning
  the winner: if second>=0 AND ce[top]==1 AND ce[second]==1, the two
  best-supported candidates both carry verbatim training evidence
  for this exact query. Compute both answers (re-apply proc_apply or
  bridge_apply per kind) and compare byte-wise over qlen bytes.
- If the answers differ: the training data contradicts itself on
  this input. WITHHOLD AMBIGUOUS (kind -2, slot -1). No heuristic
  term may silently resolve a verbatim-vs-verbatim conflict.
- If the answers agree: fall through to the existing rules (the
  contradiction is moot; the top scorer wins as before).
- The existing qscore-tie rule (gap==0 -> withhold) is unchanged and
  evaluated as before; the new guard is an additional withhold
  condition, checked after gap is stored in res+8.

Rationale for the agree/disagree refinement: two records can both
contain the query verbatim yet prescribe the same output (e.g.
duplicated training across slots). Withholding there would be
over-broad. The guard fires exactly when the evidence conflicts.

Safety for frozen checks: em never fires on any frozen-battery query
(no query is verbatim in its workspace's training inputs; verified
before freezing H-INTENT-UNIFIED2 and unchanged here). K-IU2-2 has
exactly one em=1 candidate, so the guard cannot trigger there.

### R2. Explicit cap warning (X-IU2-3)

In intent_record_inputs (both files, identical):

- When npairs > 16, emit:
  "INTENT WARN: record cap 16 reached; N training inputs, only first
  16 recorded; em coverage incomplete"
  where N is npairs. The truncation behavior is unchanged (first 16
  recorded); the boundary is now explicit in the trace, not silent.
- The 16-cap remains a documented boundary. No frozen battery uses
  more than 5 inputs per record.

### R3. Split buffer sizing (X-IU2-3b)

In bridge_learn (both files):

- Replace the fixed `z_alloc(64)` for s1idx/s2idx with
  `z_alloc(npairs*4)` (npairs i32 entries). n1/n2 are bounded by
  npairs by construction (one increment per pair index i < npairs),
  so the buffers cannot overflow.
- No other logic changes. The 18-pair crash fixture must now learn
  or fail gracefully (rc -1), never panic.

### Faithful port

Identical repair in intent_learn.zag and unified_learn.zag.
stress_learn.zag, genbias_test.zag, and unified_adversary/ulib.zag
are separate frozen experiments and are not modified.

## Frozen Kill Bars

- K-IU3-1 (X-IU2-1 closed): the red-team verbatim-collision fixture
  (D2 trained "xab>bax;xcd>dcx" as reverse proc; bridge trained
  "xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee" with condition
  input[0]==120 confirmed; em_D2("xab")==1 asserted) queried with
  "xab" returns kind -2 (WITHHOLD AMBIGUOUS), not a silent bridge
  win. Trace shows the verbatim-conflict guard firing.
- K-IU3-2 (X-IU2-3 warned): the 17-pair fixture (17 reverse pairs,
  "tuv>vut" 17th) emits the explicit INTENT WARN cap line during
  learning. in_count is still 16 and em_D("tuv") is still 0
  (documented boundary, behavior unchanged); the truncation is now
  explicit, not silent.
- K-IU3-3 (X-IU2-3b fixed): the 18-pair bridge_learn crash fixture
  (17 extractable pairs on one split side, direct discovery failing)
  completes without panic. It may learn (rc>=0) or fail gracefully
  (rc -1); it must not crash.
- K-IU3-4 (no regressions): all H-INTENT-UNIFIED2 frozen scenarios
  keep their verdicts: the 5/5 repair checks (K-IU2-1 interleaved
  withhold, K-IU2-2 verbatim beats condition, K-IU2-2b legitimate
  condition routing, K-IU2-3 10/10 + 20/20 batteries, K-IU2-5
  len_match boundary) plus the X-IU2-2 pure-em-tie control
  (withhold). Concretely: repaired intent_learn.zag main() 10/10
  PASS, repaired unified_learn.zag main() 20/20 PASS, and the
  iu2_fix.zag F1/F2/F2b/F3 scenarios replicate their K-IU2 verdicts.
- K-IU3-5 (determinism): three consecutive runs of each test binary
  produce byte-identical output (md5).

## Test Design (frozen)

Pure Zag. Pinned znc 2026.07.0-dev (edition 2026). No Python anywhere:
no generators, no verifiers, no analysis scripts, no scratch tooling.

- iu3_fix.zag: byte-copy of the repaired unified_learn.zag with
  main() replaced by the kill-bar scenarios: G1 (X-IU2-1 fixture,
  asserts kind -2), G2 (X-IU2-3 fixture, asserts WARN emitted),
  G3 (X-IU2-3b fixture, asserts no panic), G4 (K-IU2-1/K-IU2-2/
  K-IU2-2b/K-IU2-5 replication, asserts unchanged verdicts),
  G5 (X-IU2-2 pure em tie, asserts kind -2).
- Regression: the repaired intent_learn.zag and unified_learn.zag
  mains run unmodified (10/10 and 20/20).
- Raw outputs committed: IU3_FIX_RAW.txt (authoritative), plus
  regression raws. md5 over three runs per binary (K-IU3-5).
- Only repair-owned files staged and committed. No other agent's
  files touched.

## What does NOT count

- A verbatim-conflict rule that withholds when the two em=1
  candidates agree on the answer (over-broad; must compare answers).
- Silencing the cap by raising it without a principled sizing
  argument and regression proof; the cap stays 16 with an explicit
  warning.
- Changing any frozen 20/20 or 10/10 scenario to dodge a verdict.
- Recording intent for bridge sub-procedures.
- An em implementation that consults anything beyond the slot/rule's
  own recorded training inputs.
- Python in any form.

## Commit order

This prereg commit strictly precedes the implementation commit.
