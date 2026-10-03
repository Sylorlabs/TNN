# Full Theater Ablation: Empirical Test of T1, T2, T3, T4, T6

**Verdict: THEATER-ABLATION-COMPLETE.** All 5 classifications CONFIRMED.
Zero refutations.

## 1. Question

The theater audit (`e0423538a`) classified 6 learner-state elements as
theater (no exercised production read path, or no exercised production
write path, or neither). T5 (UNCERTAINTY nodes) was empirically confirmed
by `408bcfaa5` (62/62 return-value lines identical after zeroing all T30
nodes). This experiment extends the empirical test to the remaining 5:
T1, T2, T3, T4, T6.

## 2. Method

Six learners in one deterministic binary, one run:

- WA (control): full battery, no ablation.
- WB (T1): MISS_POLICY node 1 zeroed in place at midpoint (tag and
  field 20 cleared, slot kept occupied).
- WC (T2): no destructive ablation; tag-903 field 20 read before and
  after bootstrap events. The theater is the absent write path, so the
  test is "does the value change?" not "does zeroing change behavior?"
- WD (T3): header field 16 (trial stats) zeroed at midpoint.
- WE (T4): event log count (header 28) reset to 0 at midpoint.
- WF (T6): eviction history chain head (header 12) reset to -1 and any
  tag-3 nodes zeroed at midpoint.

Battery (identical call sequence, all learners):

- Phase 1: 10 teaches, 4 masked misses, chain teach + masked query (MAP
  promotion), 3 action selections, 10 exact hits, bootstrap scenario 1
  (3 unanimous facts r=91/o=555, masked query on new subject).
- Midpoint: ablations applied.
- Phase 2: 4 masked misses, 10 teaches, 10 exact hits, 3 action
  selections, contradiction + revision, bootstrap scenario 2 (4 unanimous
  facts r=92/o=777), observation + confirm.

Every return value emitted with learner prefix (A/B/C/D/E/F).
Behavioral comparison strips the prefix and the ablation-diagnostic
lines (`T1-ABLATED`, `k_pre`, etc.), then diffs the streams.

Unfrozen variant only. Frozen source verified SHA-256 identical before
and after. 3/3 byte-identical runs (`a8d44ec4...`).

## 3. Results

### T1 (MISS_POLICY, DEAD): CONFIRMED

- Ablation: `T1-ABLATED n=1` (node 1 zeroed).
- `diff A_behav.txt B_behav.txt`: NO DIFFERENCES (63/63 lines).
- Zeroing the MISS_POLICY node changed zero production behavior.
- Consistent with audit: `mp_get`/`mp_set` have no production callers;
  `mp_run` calls `t2_trial` directly.

### T2 (P-INV threshold, READ-ONLY): CONFIRMED

- No destructive ablation (the claim is about the absent write, not an
  inert read).
- Bootstrap scenario 1: `boot=555` (bootstrap MAP created from 3
  unanimous facts). Bootstrap scenario 2: `boot2=777` (4 unanimous
  facts). Both bootstraps ran, proving the read path (`k_get` at
  `bootstrap_miss` line 775) is real and exercised.
- `k=3` in all 6 learners, before midpoint (`k_pre=3`), after phase 1,
  and after phase 2. The threshold was consulted twice and never
  rewritten.
- `diff A_behav.txt C_behav.txt`: NO DIFFERENCES (63/63 lines).
- Classification holds: READ-ONLY (researcher default in disguise), not
  DEAD. The read works; the write never happens.

### T3 (trial stats, WRITE-ONLY): CONFIRMED

- Ablation: `T3-ABLATED` (header 16 zeroed).
- `diff A_behav.txt D_behav.txt`: NO DIFFERENCES (63/63 lines).
- Zeroing recorded trial statistics changed zero production behavior.
- Consistent with audit: line 1232 is the only read, in test code.

### T4 (event log, WRITE-ONLY): CONFIRMED

- Ablation: `T4-ABLATED` (log count reset to 0).
- `diff A_behav.txt E_behav.txt`: NO DIFFERENCES (63/63 lines).
- Resetting the event log changed zero production behavior.
- Consistent with audit: 9 production write sites, zero production
  reads of log contents.

### T6 (eviction history, WRITE-ONLY): CONFIRMED

- Ablation: `T6-ABLATED was=-1` (chain head was already -1, the init
  value; no tag-3 nodes existed).
- `diff A_behav.txt F_behav.txt`: NO DIFFERENCES (63/63 lines).
- The eviction history chain was empty before ablation. `rec_evict`
  calls `alloc_raw`, which returns -1 when the budget is full (the only
  time `evict_node` runs), so the history is effectively write-never in
  practice, not just write-only in principle.
- Resetting the (empty) chain changed zero production behavior.

## 4. Overall verdict

| Instance | Classification | Ablation | Result |
|----------|---------------|----------|--------|
| T1 | DEAD | Zero node 1 | CONFIRMED (63/63) |
| T2 | READ-ONLY | Verify k=3 unchanged | CONFIRMED (63/63, k=3) |
| T3 | WRITE-ONLY | Zero header 16 | CONFIRMED (63/63) |
| T4 | WRITE-ONLY | Reset log count | CONFIRMED (63/63) |
| T6 | WRITE-ONLY | Reset chain (was empty) | CONFIRMED (63/63) |
| T5 | WRITE-ONLY | (prior work `408bcfaa5`) | CONFIRMED (62/62) |

All 6 theater classifications from `e0423538a` are now empirically
confirmed. Zero refutations.

## 5. Implications

- The genuine learner state is exactly what the audit listed: facts,
  guides, MAPs (for revision targeting), edges (bid magnitudes),
  clock/counters, context stack, POLICY_ROOT (bootstrap pointer).
- Any mechanism report citing T1-T6 as "learner-owned" parameters,
  "policy nodes," "uncertainty representations," or "experience memory"
  is citing theater.
- T2 is the most dangerous because it looks the most like a parameter:
  it IS read in production, so a naive "is it used?" check passes. The
  theater is specifically the absent write path. Reports must check
  both paths.
- T6 is write-never in practice (not just write-only in principle)
  due to the `alloc_raw` failure mode under budget pressure. The code
  exists but cannot fire when eviction actually happens.

## 6. Honest scope and non-claims

- This confirms the 6 nodes/fields are causally inert; it does not build
  the missing read/write paths.
- The ablations preserved slot occupancy and allocation order; a
  slot-freeing ablation was not tested (would introduce index artifacts).
- T2 was not destructively ablated; the test was value-stability, which
  is the correct test for a READ-ONLY classification.
- No SUF, L3, or capability claim. This is a negative result that
  sharpens the diagnosis: TNN-2's apparent learner-state richness
  overstates its actual cognitive substrate by 6 elements.

## 7. Standing architectural metric (this experiment)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (experiment, not architecture)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: all (no new forms)
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0 (revision path exercised but not counted as new)
- COGNITION LINES: 0 (driver only, unfrozen variant)
- MODES/BRIDGES/HANDLERS/SEMANTIC CASES: 0/0/0/0
