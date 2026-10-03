# RECLAMATION SYNTHESIS: the memory-reclamation policy comparison arc

Date: 2026-10-03. Worker: RECLAMATION-SYNTHESIS (non-ledger task; claim
minting paused).

This document synthesizes five preregistered lanes:

| Lane | Verdict | Question answered |
|------|---------|-------------------|
| EVICTION-POLICY-COMPARE | PASS 8/8 | FIFO vs owner-partitioned vs pinning under churn |
| PINNING-RECLAMATION | PASS 7/7 | No-reclaim vs LRU vs owner-consent reclamation |
| MULTI-OWNER-CHURN | PASS 8/8 | Do the policies survive churn that crosses the class boundary? |
| CONSENT-MULTIOWNER | PASS 10/10 | Does owner-consent reclamation survive multi-owner churn? |
| LIVENESS-SIGNAL | PASS 11/11 | Does an owner-blind liveness signal avoid the boundary problem? |

Every lane reproduced its parents' frozen tables bit-for-bit on the
modified substrate (all 72 cells of the EVICTION-POLICY table; the
full 9-row consent table; the frozen PIN rows under new adversaries),
so the numbers compose across lanes: this arc is one calibrated
measurement chain, not five separate experiments.

## The policy space

Five policies, parameterized identically (pool 32, 20 benign victims,
doses r=0/20/32 plus multi-owner M2/M3/X2), measured on retention
(ret), evictions (ev), drops to destroy-in-place (drop), and raw
primary-resident reads (rawA). The full measured surface:

| Policy | Signal (what counts as evictable) | ret under benign | ret under churn | Capacity price |
|--------|----------------------------------|------------------|-----------------|----------------|
| FIFO | oldest arrival | 100 | 0 (flushable) | none |
| PART (16/16) | other-class arrival | 77 (fragmentation) | 77 single-owner / 0 multi-owner | fragmentation up front |
| PIN | nothing | 100 | 100 | leak: drop grows 8/20/28/48 |
| PIN-LRU | least-recently-touched pinned | 100 | bit-for-bit FIFO (100/54/0) | full restore, zero robustness |
| PIN-CONSENT (mask 16) | pinned entries owned by consenting owner | 100 | 100 | graceful: drop 0 single-owner / 17 / 43 / 28 under mask-miss |
| PIN-LIVENESS (recency) | coldest touch-stamp | 100 | 0 catastrophic (single and multi) | full restore (drop 0) of the wrong entries |

## The deep structure: every policy encodes a hypothesis about death

Each policy answers one question: "which entries are dead?" Every
policy's answer is a hypothesis, and every hypothesis has a boundary
where the adversary lives.

1. **FIFO hypothesizes: oldest = deadest.** The churn adversary is
   always newest, so FIFO flushes the benign knowledge first and keeps
   the churn history. ret goes 100 -> 54 -> 0 exactly.
2. **PART hypothesizes: other-class = evictable.** As long as the
   churner stays in the other class, the protected partition holds
   (ret=77 flat). When the churner carries an A-family owner, the
   protected partition is flushed from the inside (ret 77 -> 0).
   The 16/16 split is a stated policy choice; moving it moves the
   retention/fragmentation tradeoff, it never removes it.
3. **PIN hypothesizes: nothing is dead.** Retention is perfect and
   boundary-free precisely because no death judgment is made. The
   price is the leak: drop reaches 48 of 32 slots at the M3 dose.
   Pinning is not a solution; it is the refusal to solve, quantified.
4. **PIN-LRU hypothesizes: coldest = deadest.** Under the tested
   protocol (no pool reads during churn), last-touch order equals
   placement order equals FIFO bump order, so recency degenerates to
   arrival and the LRU row is bit-for-bit the FIFO row. This was a
   preregistered sharp prediction, hit exactly. LRU reclamation here
   is not "worse than no reclamation"; it IS no-reclamation plus
   FIFO's failure, paying pinning's implementation cost for FIFO's
   outcome.
5. **PIN-CONSENT hypothesizes: dead = entries whose owner consented.**
   Retention is boundary-free (consent can only evict mask-matching
   entries; benign victims never match). Capacity restoration is
   boundary-bound: ev/drop splits of 11/17 (M2), 5/43 (M3), and
   0/28 under mask-miss (X2: bit-for-bit no-reclaim pinning). Its
   miss case is "reclaim nothing", never "evict the wrong entries".
6. **PIN-LIVENESS hypothesizes: cold = dead.** This is the
   catastrophic one. Pinned knowledge is installed once during
   teaching and never re-touched during churn; churn history is
   installed later. Least-recently-touched therefore evicts the
   pinned knowledge FIRST, in slot order: ret 100 -> 0, rawA 35 ->
   15, under every adversary including single-owner. The boundary did
   not disappear when identity was removed; it relocated from
   identity to time, and the relocated boundary points at exactly
   what the system was told to keep.

The unifying observation: **the adversary never attacks the policy;
it attacks the policy's epistemic assumption about what "dead"
means.** FIFO assumes age; PART assumes class; LRU assumes recency;
consent assumes owner-consent correlates with death; liveness assumes
coldness. Every assumption is a boundary, every boundary has a
miss case, and the miss case is the policy's true character.

## Failure modes, ordered by danger, not by retention

Retention numbers hide the important ordering. Order by what the miss
case does:

- **Fails safe (PART-class-miss):** retention collapses (77 -> 0) but
  capacity behavior is unchanged. Bad, visible.
- **Fails safe on retention (consent mask-miss):** retention never
  moves (ret=100 throughout); capacity restoration degrades
  gracefully (drop 0 -> 17/43, then degenerates to no-reclaim).
  The policy does less, never harms. This is strictly safer than
  PART's boundary, and it is the only policy whose miss case harms
  nothing.
- **Fails catastrophic (liveness cold-knowledge):** retention goes
  to zero while capacity metrics look healthy (drop=0 in every
  liveness row). A monitor watching only ev/drop would call this the
  best policy while the knowledge base is destroyed. This is the most
  dangerous failure in the arc: silent, total, and aimed at the
  protected class by construction.

The lesson: **a reclamation policy's quality is its miss case, not
its hit case.** All six regimes hit ret=100 under some adversary; the
miss cases separate them.

## The fundamental tradeoff

Three quantities, two axes:

- **Retention vs capacity** is the familiar axis: PIN buys retention
  with leak; LRU buys capacity with collapse. But the arc shows this
  axis is incomplete.
- **Retention vs boundary-dependence** is the real axis. The
  retention-capacity tradeoff can be escaped (consent gets both under
  the aligned adversary), but only by importing a boundary from the
  researcher: the class split, the consent mask. The boundary then
  carries its own miss case, and the miss case determines whether the
  policy is safe (consent), merely fragile (PART), or catastrophic
  (liveness, which tried to escape the boundary by relocating it to
  time and aimed it at the protected knowledge).

Stated as a trilemma: among **retention**, **capacity**, and
**boundary-freedom**, the arc found no policy achieving all three.
PIN achieves retention + boundary-freedom but no capacity.
Consent achieves retention + capacity but no boundary-freedom.
Liveness achieves capacity + boundary-freedom but no retention.

## What the arc did NOT test (honest accounting)

- Every liveness signal in the arc is researcher-authored: the class
  boundary, the consent mask, the touch stamps, the re-read schedule
  that rescues liveness (LIVR-M2). The learner never once decided an
  entry was dead. The continuing-learner form of the question
  ("who decides, and on what evidence?") is untouched.
- The LRU rescue condition (benign re-reads interleaved during churn)
  was identified but not run as its own lane; LIVENESS-SIGNAL's
  LIVR-M2 is the reuse-conditioned version and it works (ret=100,
  ev=28, drop=0, beating consent's capacity), but the re-read schedule
  is researcher-designed, not learner-issued.
- Frequency-based liveness was analyzed, not implemented
  (ordering-equivalence argument for the single-touch workload).
- All adversaries are mechanism stressors, fully specified in
  preregs, deliberately aimed at known weaknesses. No sealed world,
  no adversary-designed-post-freeze evaluation family, no
  cold-but-critical sealed test.
- Owner-scoped reads are retained throughout, so the label-free
  routing caveat carries over from L2-INTERFERENCE2 unchanged: this is
  a mechanism check on eviction policy in shared memory, not a claim
  about a full continuing learner.

## What remains unresolved: the hard problem

The arc leaves one question standing, and it is the only one that
matters for the continuing learner:

**Who decides an entry is dead, and on what evidence, when the
knowledge is cold-but-critical (never re-touched, must survive), no
researcher supplies the signal, and the adversary is shaped by the
workload rather than by a prereg?**

Every policy in the arc fails this question by construction:

- PIN refuses to answer (leak).
- PART and CONSENT answer with researcher-supplied identity boundaries
  (PART's boundary is unsafe; consent's is safe but capacity-bound).
- LRU and LIVENESS answer with time, which is aimed at pinned
  knowledge by construction: anything the learner was told to keep
  and not disturb is exactly what recency kills first.

The reuse-conditioned recovery (K8) sharpens the problem rather than
solving it: the owner-blind signal works when the workload supplies
liveness. But "the workload supplies liveness" is just another way of
saying the researcher arranged for the protected knowledge to be warm.
Rare-but-critical knowledge, the knowledge a continuing learner most
needs to protect (a corrected belief, a hard-won procedure, a
counterexample that must not be forgotten), is cold by definition.
No tested signal protects it. That is the hard problem.

A secondary unresolved point: **eviction = destruction** is assumed
by all five lanes. The drop counter measures destroy-in-place; no lane
tested a cold tier, compression, or recoverable exile. The trilemma
above is a trilemma of destruction policies; changing the consequence
of eviction may change the tradeoff space.

## Three structurally distinct next hypotheses

Each hypothesis belongs to a different family: a new signal type, a
new consequence structure, and a new decision authority. None is a
repair of an existing policy; per the no-patch-treadmill rule, the
measured prices stand as evidence.

### H1. Importance-weighted liveness (new signal type: learner-owned value, not identity, not time)

Entries carry an importance signal derived from the learner's own
cognition: e.g. downstream dependency count (how many live structures
reference the entry), or a learner-written importance weight updated
when the entry participates in a successful episode. Eviction targets
lowest importance, with recency only as a tiebreaker.

The discriminating test: a sealed world containing **cold-but-critical
knowledge** (zero re-touches during a long churn phase, but high
dependency count or learner-marked importance) alongside warm churn
history. The preregistered sharp prediction is that recency kills the
critical entries first while importance-weighting reclaims the churn
history, i.e. the two signals order oppositely and measurably.

Why it is structurally distinct: the decision input is neither who
owns the entry (identity boundary) nor when it was touched (time
boundary) but what the entry is worth to the learner's own
structures. It is the first policy in the arc whose signal could, in
principle, protect cold-but-critical knowledge. Honest risk: if
importance is researcher-scored rather than learner-derived, this
collapses to another researcher boundary (the consent-mask pattern);
the lane must preregister the importance source and run a control
where the researcher scores importance adversarially.

### H2. Exile, not destruction (new consequence structure: recoverable cold tier)

Eviction no longer destroys. Entries evicted by any ranking policy
(LRU, importance, even FIFO) move to a cheap cold tier: compressed,
deduplicated, or summarized, recoverable on demand at a measured
retrieval cost. Retention is then measured in two grades: hot
retention (immediately resident) and recoverable retention
(retrievable within the cold-tier budget).

The discriminating test: LRU reclamation, which this arc proved
destroys pinned knowledge (ret 100 -> 0), rerun against the exile
substrate. The preregistered sharp prediction: hot retention still
collapses bit-for-bit to the FIFO row, but recoverable retention
stays 100, and the retrieval-cost ledger shows which entries the
workload actually needed back. The policy question shifts from "which
entries are dead?" (unanswerable, per the arc) to "which entries are
worth keeping hot?" (a ranking question with a recoverable miss
case).

Why it is structurally distinct: all five lanes share the frame
"eviction = destruction", which makes every miss case permanent. Exile
makes the miss case recoverable, which changes the trilemma: a
catastrophic ranking (LRU under churn) becomes a capacity bill
(retrieval cost) rather than knowledge loss. Honest risk: the cold
tier is itself bounded memory, so the destruction question recurses
one level down; the lane must preregister the cold-tier eviction rule
and measure whether the recursion converges or just delays the same
collapse.

### H3. Learner-issued unpin (new decision authority: the learner, not the policy)

Reclamation may only ever touch entries the learner has released.
The learner emits unpin when it judges an entry dead: e.g. it has
incorporated the entry's content into a successor structure, revised
the belief the entry recorded, or superseded the procedure the entry
implemented. The policy's only job is choosing among released
entries (any ranking); it can never touch a pinned entry the learner
still holds.

The discriminating test: a sealed continuing-learner world where the
learner builds, revises, and supersedes structures across episodes
under memory pressure, with no researcher-supplied mask, boundary, or
re-read schedule. The preregistered predictions: (a) retention of
learner-held knowledge is 100 by construction (the policy cannot
violate it); (b) capacity is restored exactly to the extent the
learner actually releases entries, so drop measures learner
release behavior, not policy cleverness; (c) the adversarial case is
a learner that never releases (degenerates to no-reclaim pinning,
the measured leak) or releases wrongly (the first honest measurement
of learner judgment error under pressure).

Why it is structurally distinct: every policy in the arc locates the
death decision in the mechanism (the eviction rule) fed by a
researcher signal. H3 relocates the decision to cognition: death is a
learner judgment with a white-box trace (what superseded what, when,
and why), which is independently the kind of evidence the L3 bar
requires. It also reframes the hard problem honestly: instead of
asking the mechanism to infer death from signals, it asks whether the
learner can learn to manage its own memory, and measures the failure
when it cannot. Honest risk: this is the hardest lane to run without
smuggling the answer in through the task design; the sealed world
must be adversary-designed post-freeze, and "learner-issued" must be
audited to exclude researcher-issued releases wearing learner labels.

## Reading guide for the parent

- If the next work must stay in mechanism space: H1 is the cheapest
  to preregister (one new signal, same substrate, same adversaries).
- If the trilemma itself is suspect: H2 attacks its framing
  (destruction is assumed, not proven necessary).
- If the research program is serious about the continuing learner:
  H3 is the only hypothesis that moves the death decision into
  learner cognition, which is where the protected-core / learner-state
  boundary says it belongs. It is also the hardest to run honestly.

## Lane hygiene

- Documentation only; no implementation was produced or modified.
- All five REPORT.md files were read in full; numbers above are
  copied from the frozen tables, not recomputed.
- Per the no-patch-treadmill rule, no lane's verdict is amended here
  and no repair lineage is proposed: H1/H2/H3 are fresh hypotheses
  for fresh preregistration, not work orders against existing
  policies.
