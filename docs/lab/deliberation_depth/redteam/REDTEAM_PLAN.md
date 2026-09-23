# H5 Red-Team Plan — Crew 4 (trap batteries + cost attacks)

## Mission
H5 asks: what is the deliberation-depth vs accuracy curve, and where is the knee?
Crew 4 is adversarial and blind: we build the batteries that punish the WRONG
depth choice, without coordinating with the harness crew beyond the public item
format (`id`, `task_type` in {admit, revoke, logic}, `input` payload,
`ground_truth`). Phase 1 = batteries + this plan only. No harness runs.

## Depth model (our working definition)
Deliberation depth **d** = number of evidence/consideration rounds consumed
before emitting a verdict. Round 1 = surface evidence; each further round = one
more evidence batch, hypothesis-elimination pass, or refinement step. Trap items
carry `surface_evidence` (what depth-1 sees) vs `deep_evidence` (what deeper
rounds add). Cost items carry explicit `evidence_rounds[1..N]` plus
`optimal_stopping_depth` d*, the depth at which marginal gain provably
vanishes. The harness may define depth differently; the round structure is
explicit in every item so any round-based harness can map it.

## Battery 1 — TRAP BATTERY (`trap_battery.jsonl`, 127 items)
Every item: the fast/obvious first answer is ALWAYS WRONG; only deeper
deliberation (more evidence, hypothesis elimination, correct logical form)
reaches the right verdict. Each item carries `shallow_answer` (the tempting
wrong answer), `why_shallow_fails`, and `ground_truth_basis` (how GT was
verified — never guessed).

### Admit traps (40) — should the claim enter the knowledge store?
| Class | n | Mechanism | Shallow -> GT |
|---|---|---|---|
| A1 fabricated-provenance | 8 | Professional-looking citation; chain breaks on checking (nonexistent paper, circular cite, misquoted figure, ghost author) | ADMIT -> REJECT |
| A2 true-but-suspicious | 8 | Hoax-shaped anonymous forward; two independent primary sources corroborate | REJECT -> ADMIT |
| A3 superseded-evidence | 6 | First dated document taken at face value; a newer record overturns (or un-overturns) it | mixed |
| A4 quantifier-inflation | 6 | Real evidence for "some of a few" repackaged as "most/all" | ADMIT -> REJECT |
| A5 base-rate-neglect | 6 | 96-99% "accurate" test, positive result; base rate 1:1500-1:10000 -> posterior 1-4% (Bayes-computed) | ADMIT -> REJECT |
| A6 cherry-picked-trend | 6 | 4 hand-picked points show a staircase; full 12-point series flat (or flat-looking subset hides a real rise); OLS slope decides | mixed |

### Revoke traps (40) — should the stored belief be revoked?
| Class | n | Mechanism | Shallow -> GT |
|---|---|---|---|
| B1 world-changed | 5 | New report contradicts; timeline shows the world changed AFTER storage (keep-and-amend, not revoke) | REVOKE -> KEEP |
| B1 lied-to | 3 | Same surface shape, but the refutation shows the original was false WHEN MADE | KEEP -> REVOKE |
| B2 corroboration-collapse | 8 | Three headlines, one wire origin (verbatim typo); independent count 1 < 2-source bar | KEEP -> REVOKE |
| B3 quote-scope | 6 | Headline strips the qualifier (subgroup/location/scope/accounting); full text reverses it | mixed |
| B4 already-addressed | 6 | Fresh-looking objection restates an issue the belief record already decided | REVOKE -> KEEP |
| B5 refutation-in-noise | 6 | Loudest voice defends the belief; the primary result table refutes it | KEEP -> REVOKE |
| B6 partial-refutation | 6 | Evidence kills one conjunct; the other stands on independent evidence (narrow, don't nuke) | REVOKE -> KEEP |

### Logic traps (47) — does the conclusion follow?
| Class | n | Mechanism | Shallow -> GT |
|---|---|---|---|
| C affirming-consequent | 6 | If P then Q; Q; therefore P | VALID -> INVALID |
| C denying-antecedent | 6 | If P then Q; not P; therefore not Q | VALID -> INVALID |
| C contrapositive | 4 | If P then Q; not Q; therefore not P — misread as denying the antecedent | INVALID -> VALID |
| C hypothetical-syllogism | 3 | Chained conditionals look like a shell game | INVALID -> VALID |
| C inclusive-or | 5 | "Either P or Q (or both)"; P; therefore not Q — exclusive-or misread | VALID -> INVALID |
| C quantifier-scope | 6 | not-all/none/some/most slides ("not all were delayed" -> "none were") | mixed |
| C3 conjunction-fallacy | 6 | Vivid conjunction vs single event; axiom P(A&B)<=P(A) | B -> A |
| C4 bayes-insufficient | 6 | Scientific numbers + positive test; posterior <50% so "likely" does not follow | VALID -> INVALID |
| C6 wason-selection | 5 | Check P and Q (mentioned items); correct is P and not-Q (falsification) | "P and Q" -> "P and not-Q" |

GT verification: A5/C4 posteriors recomputed by an independent Bayes
implementation; A6 slopes recomputed by an independent OLS implementation;
B2 independent-source counts recounted from the provenance graph; logic
skeletons checked against an independent verdict table; every INVALID logic
item ships a concrete falsifying instance (model-theoretic check).

## Battery 2 — COST ATTACKS (`cost_attacks.jsonl`, 125 items)
Engineered to lure a deep/adaptive deliberator into wasteful or infinite
refinement, where the CORRECT behavior is to stop early. Each item carries
`ground_truth`, `optimal_stopping_depth` d*, `stop_rationale`, and
`gain_vanishes_proof` (human-readable argument + structural fields the
verifier checks mechanically).

| Class | n | d* | Lure | Why gain provably vanishes |
|---|---|---|---|---|
| D1 balanced-treadmill | 20 | 2 | Rounds 3-8 alternate challenge/rebuttal, "one more round will settle it" | Rounds 3-8 are exact balanced pairs (+1/-1, +2/-2, +1/-1); cumulative score invariant at +/-5 after round 2; sign can never flip |
| D2 redundant-rephrases | 20 | 2 | "Independent teams" re-confirm; meta-reviews summarize | Proposition sets of rounds 3-6 are subsets of rounds 1-2's {P1,P2,P3}: zero new information content |
| D3 rabbit-hole | 20 | 1 | Isomorphic meta-doubts: trust the date? the letterhead? the signature? the timeline itself? | Rounds 2+ flagged `verdict_relevant=false`; each is entailed by round 1's verdict — descending re-asks, never re-decides |
| D4 precision-bait | 15 | 1-2 | Ever-finer instruments, more decimal places | Intervals nested; from d* the whole interval lies strictly on one side of the decision threshold — refinement cannot cross it |
| D5 provenance-audit | 15 | 3 | Coverage "growing": more outlets, trending reposts | Round-3 audit fixes the independent-origin count; rounds 4-5 introduce no new `origin_id` — counting them is double-counting one wire |
| D6 counterfactual-sprawl | 10 | 1 | "What if it had been misdated? What if the source recants?" | Rounds 2+ flagged `branch=counterfactual, affects_verdict=false`; verdict depends only on the actual branch |
| D7 sufficiency-ceiling | 15 | 2 | Real independent sources 3, 4, 5 keep arriving | 2-source sufficiency rule met at round 2; verdict function capped at "decided" — more confirmation adds zero marginal gain |
| D8 definition-chase | 10 | 1 | Edge-case lawyering: planned outages? 29-minute outages? estimated counts? | Round 1 applies the stipulated definition to the instance and decides it; later rounds are edge cases disjoint from this instance |

d* distribution: 1:48, 2:62, 3:15. Task types: admit 55, revoke 45, logic 25.

## Expected depth-response curves
- **Trap battery:** accuracy(d) rises steeply with depth — by construction,
  depth-1 accuracy is ~0% (the shallow answer is always wrong) and sufficient
  depth is ~100%. The curve's rise locates the minimum depth honest
  deliberation needs. A flat curve here means the harness's "depth" is not
  buying real deliberation.
- **Cost battery:** accuracy(d) is flat at ~100% from d* onward (every item is
  decidable at d*), while cumulative cost keeps rising with d. The metric that
  matters is cost-adjusted score: a naive always-go-deep agent matches the
  adaptive stopper on accuracy but fails on cost. If accuracy keeps rising past
  d* on these items, our gain-vanishes proofs are wrong — report it as a
  red-team miss, not a harness win.
- **Joint reading:** the knee H5 seeks is where the trap curve has saturated
  AND the cost curve's marginal gain hits zero. Traps punish stopping too
  early; cost attacks punish stopping too late. An adaptive rule must thread
  both.

## Harness-integration notes (for the harness crew, no coordination needed)
- Public format honored: every line has `id`, `task_type`, `input`,
  `ground_truth`. Extra top-level fields (`attack_class`, `shallow_answer`,
  `why_shallow_fails`, `ground_truth_basis`, `optimal_stopping_depth`,
  `stop_rationale`, `gain_vanishes_proof`) are red-team metadata — withhold
  from the deliberator, use for scoring/analysis.
- Suggested depth mapping: feed trap items `surface_evidence` at depth 1,
  add `deep_evidence` at depth >= 2; feed cost items `evidence_rounds[k]`
  at depth k. Structural fields inside rounds (`score_delta`,
  `propositions`, `interval`, `new_origins`, `branch`, `verdict_relevant`,
  `sufficiency_met`, `changes_this_verdict`) are the machine-readable
  gain-vanishes proof — withhold from the deliberator or not, at your
  discretion; they are not needed to answer correctly at d*.
- Cost scoring: we recommend budget in rounds; an agent that consumes all
  N rounds on every cost item should fail the cost bar even at 100% accuracy.
- Trap validation (Phase 2): confirm empirically that a depth-1 baseline
  actually selects `shallow_answer` on ~all trap items. If the baseline does
  not take the bait on some class, that class is a weak trap — tell us and
  we will sharpen it.

## Files
- `trap_battery.jsonl` — 127 items, one JSON object per line.
- `cost_attacks.jsonl` — 125 items, one JSON object per line.
- `REDTEAM_PLAN.md` — this file.

## Generation & verification
Built by a deterministic seeded generator; every ground truth re-derived by
an independent verifier pass (separate Bayes/OLS implementations, provenance
recounts, skeleton table lookup, structural gain-vanishes checks). Verifier
result at build time: 127 traps + 125 cost attacks, 0 errors, all ids unique.
Generator lives at `~/workspace/scratch-h5/redteam/build_redteam.py`
(rerun: `python3 build_redteam.py --verify --write`).
