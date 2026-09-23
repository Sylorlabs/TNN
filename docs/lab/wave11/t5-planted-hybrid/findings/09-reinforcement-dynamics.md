# Track 5, Slice 09 — Hybrid Reinforcement Dynamics

## 1. Slice
Track 5 (planted-only vs learned-only vs hybrid), slice 09: hybrid reinforcement dynamics — how
planted and learned knowledge reinforce each other over time, in both directions.

## 2. Falsifiable claim
On the 10x developmental curriculum with a 20% planted-seed mix (half true, half false seeds),
the hybrid arm reaches mastery (≥90% of the prereg mastery criteria) in **≥30% fewer episodes**
than the learned-only arm, **and** vicious-cycle incidence — false seeds that acquire ≥2 learned
corroborations before being revised — stays **below 5%** of planted false seeds. If either half
fails, the hybrid is not worth its oversight cost.

## 3. Design
Every memory slot carries provenance: `PLANTED` (scaffold-gifted, with trainer id + episode) or
`LEARNED` (built by the learner through eliminative verification). Scaffolding is
scaffold-and-release: planted slots are NOT pinned; they are hypotheses the learner must
corroborate or kill. Two lawful cycles can form:

- **Virtuous:** a true planted seed acts as eliminative scaffold → the learner derives
  corroborating evidence in later episodes → each learned corroboration adds an independent
  citation edge to the seed and a deliberate `strengthen` op (judgment-set, never passive) →
  the strengthened seed accelerates subsequent learning (fewer episodes to adjacent claims).
- **Vicious:** a false planted seed lowers the eliminative bar locally → ambiguous evidence is
  "confirmed" against it → learned errors cite the seed as corroboration → mutual citation
  inflation with no independent root. The seed never faces a disconfirmation probe because the
  bar is tuned to itself.

**Oversight machinery (all deterministic, no RNG):** the learner maintains a citation DAG
(slot → supporting slots, tagged per episode). Per claim it computes, on a fixed schedule
(every N episodes, lowest-diversity claims first, ties broken by slot id):

```
// Zag-flavored pseudocode
roots(s)      := distinct provenance-roots of all citation ancestors of s
indep_ratio(s) := count(roots(s) where root is LEARNED or world-record) / count(citations(s))
if indep_ratio(s) < 0.25 and age(s) > probe_threshold:
    schedule_disconfirmation_probe(s)   // deliberate: seek evidence that kills s
```

A claim whose entire support ancestry collapses to one planted root is *provenance-concentrated*:
its signature is low `indep_ratio` + zero disconfirmation probes survived. **Intervention
protocol:** (1) quarantine — freeze all strength-ops citing that root; (2) mandatory probe
episode seeking world evidence against the claim (debate/revision machinery applies —
`docs/lab/wave6/` showed false claims revised 18/18 against world records); (3) deliberate
`kill` or `demote` of the false seed and propagation of revision to dependents; (4) full audit
entries for each step. Planted slots are never force-pinned — force-pin is a human-only op —
so nothing in this loop is irreversible by TNN itself.

## 4. Kill bar
The hybrid design is killed if ANY of these fire at 10x scale: (a) hybrid reaches mastery in
<15% fewer episodes than learned-only; (b) vicious-cycle incidence ≥5% of planted false seeds;
(c) any vicious cycle persists undetected >20 episodes after its second learned corroboration;
(d) the oversight machinery itself revises a true seed (false-positive kill rate >0 over 10x);
(e) oversight probe episodes consume >20% of total episodes (the cure costs more than the
disease). Numeric, prereg-style; no re-running cells, no rule changes.

## 5. Honesty notes
Weakest point: the whole scheme leans on the debate experiment's limit — disconfirmation
probes need authoritative world records, and where records don't exist (the accepted
sensor-deceivable hole) the monitor detects concentration but cannot settle truth. The 0.25
threshold is a guess, not derived; it must be swept, not defended. Probes are deliberate
episodes, so they *cost* the episode savings the hybrid claims — this is exactly what bar (e)
polices. I am NOT claiming planted knowledge is ever safe to pin, that concentration implies
falsity (true seeds concentrate early too — probes are disconfirmation attempts, not verdicts),
or that this works without the eliminative-logic and deliberate-ops substrate already proven
(MA1 58/58; debate 22/22; integrity 137/137). Felt intensity is dead and plays no role here.

## 6. Next build step
Build the citation DAG + `indep_ratio` monitor on the existing memory substrate at 1x with a
5% seed mix, and inject exactly two false seeds with seeded ambiguous evidence. The single
most informative question: does the monitor flag both false seeds before they reach their
second learned corroboration, with zero true-seed flags — or does ambiguity defeat the probe
scheduler? That result decides whether the 10x trial is worth running.
