# T30 Ablation: Empirical Test of the Theater Classification

Verdict: T30-ABLATION-COMPLETE. Theater classification CONFIRMED.

## 1. Question

The ignorance-dedup analysis (`8510e327b`, Section 2d) predicted that
"ablating every T30 node from a live learner would change zero
production behavior," because UNCERTAINTY nodes have an exercised
production write path but no production read path (theater audit
`e0423538a`, T5: write-only). This experiment tests that prediction
empirically on an unfrozen variant.

## 2. Method

Two learners in one binary, one deterministic run:

- WA (control): full battery, no ablation.
- WB (ablation): identical battery; at the midpoint every live tag-30
  node is zeroed in place (tag and fields cleared, slot kept occupied
  so allocation order and node indices stay identical across learners).

Battery (both learners, same call sequence):

- Phase 1: 10 teaches, 4 masked misses (each creates a T30 + guide),
  chain teach + masked query (MAP promotion), 3 action selections,
  direct guide query (key 30,-999), 10 exact query hits.
- Ablation point (WB only): `t30_ablate`, 4 nodes zeroed.
- Phase 2: 4 more masked misses (fresh T30s in both learners),
  10 more teaches, 10 exact hits, 3 action selections, contradiction
  on a MAP-licensing fact (revision path) + query of the revised MAP,
  plain observation + confirm, guide query again, re-miss on a
  pre-ablation key (the dedup scenario).

Every return value is emitted with an A/B prefix. Behavioral comparison
strips the prefix and the t30-count lines (which differ by design) and
diffs the streams.

## 3. Results (3/3 byte-identical runs, `ac9576f78...`)

Ablation mechanics (from the transcript):

- Pre-ablation: A t30=4, B t30=4.
- `ABLATED n=4`. Post: B t30_post=0, A t30_post=4.
- Phase 2 misses: A t30=8, B t30=4 (new T30s created in both).
- Final re-miss: A t30=9, B t30=5.

Behavioral comparison: 62 return-value lines per learner covering
teaches, query hits, masked misses, MAP promotion, action selection,
guide queries, contradiction, revision, and observations. `diff` of the
A and B streams: NO DIFFERENCES.

Notable identicals:

- `teach2=42..51`: node indices identical, confirming the zero-in-place
  ablation preserved allocation order exactly.
- `promote=7003`, `contra_q=9999`: MAP promotion and revision behave
  identically without the T30 records.
- `act=0`, `guideq=0`: action selection and guide-as-fact queries
  unaffected, even though the pre-ablation guides in B point at zeroed
  T30 nodes.
- `miss=-2`, `remiss=-2`: miss handling identical, including the
  re-miss on a key whose uncertainty record was ablated.

## 4. Verdict: theater CONFIRMED

Deleting (zeroing) all 4 UNCERTAINTY nodes mid-lifetime changed zero
production behavior across 62 subsequent behavioral events spanning
every event type (teach, query hit, query miss, MAP promotion, act,
guide query, contradiction, revision, observation). The T30 nodes are
causally inert records: the learner writes its ignorance and never
reads it back.

Implications:

- The dedup report's structural prediction is empirically confirmed,
  not just argued from source inspection.
- K-H2-3 FAIL for frozen TNN-2 is now doubly supported: the uncertainty
  node sits in no decision's causal chain, so no accept/reject/withhold
  decision can depend on it, independent of sealed-world content.
- A dedup check alone (suppressing duplicate T30 allocation) would be
  behavior-preserving and therefore theater by Micah's rule. The honest
  unit of progress remains the 4-element mechanism in the dedup report
  (keyed lookup + production read path + retirement + learning guide
  content), of which the read path is the binding constraint.

## 5. Honest scope and non-claims

- This confirms the nodes are inert; it does not build the read path.
- The ablation zeroed T30 nodes only. Guide nodes (tag-1), POLICY_ROOT
  (tag-2), and all edges were left intact in both learners.
- Node-index return values from `ev_teach` matched exactly because the
  ablation preserved slot occupancy; a slot-freeing ablation was not
  tested (it would introduce index artifacts unrelated to behavior).
- No SUF, L3, or capability claim. This is a negative result that
  sharpens the diagnosis: the inquiry subsystem is a logging pipeline,
  not a learning loop.

## 6. Standing architectural metric (this experiment)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 1 (the ablation itself,
  experimenter-side).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SOURCE-ENUMERABLE FORMS: all.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0 exercised.
- REUSE EVENTS: 0. REVISION EVENTS: 2 (one per learner, identical).
- COGNITION LINES: 0 added to the variant (driver only).
- MODES/BRIDGES/HANDLERS/SEMANTIC CASES: 0/0/0/0.

## 7. Files

- `NAMECHECK.md`: Step 0 guard, variant declaration, provenance.
- `T30_ABLATION.md`: this document.
- `t30_base.zag`: verbatim copy of frozen source (SHA-256 identical).
- `t30_driver.zag`: driver source (ablation + battery).
- `t30_full.zag`: base with original main removed + driver appended.
- `t30_bin`: compiled binary (pinned znc).
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical transcripts.
