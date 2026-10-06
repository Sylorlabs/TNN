# FRONTIER QUEUE — lane/ownership

Autonomous control loop. **This file, not the conversation, is the state.**

```
experiment -> commit -> update this file -> pop next CURRENT -> experiment
```

Decision rule (standing, no human router):
- Both reasonable + reversible → **test both**.
- Expensive → **cheap falsifier each**, then invest in the survivor.
- Architecture → **separate worktrees**, compare, merge only evidence-supported.
- BLOCKED items never block anything else. They sit here.

Ranking = ARCHITECTURAL INFORMATION GAIN × POSSIBILITY OF FALSIFICATION
× RELEVANCE TO LEARNER OWNERSHIP ÷ IMPLEMENTATION COST.
**Not** ranked by likelihood of a positive.

---

## CURRENT

> **NOTE ON P5-meta**: CLOSED as *not established in this substrate*, not
> refuted. Nine defects, all one shape -- the intended intervention never
> reached the mechanism under test. Two permanent instruments were built
> because of it (`arm_audit.py`, `noop_change_detector.py`), and both
> earned their place within one phase. Reopening requires the
> `substrate-spec` preconditions, not another experiment on this
> substrate.


| id | item | falsifier | status |
|---|---|---|---|
| `P5-meta5f` | **SHORT ACQUISITION.** 5e showed acquisition is INSENSITIVE to its starting population over 300 trials. Cut trials to ~15 so the initial condition still matters. If the prior is inert at 300 and active at 15, the blocker is search horizon, not meta-learning | prior must be inert at 300 AND active at short horizon | RUNNING |
| `P6-formal` | **PROMOTED (was queued).** Resolve `ZD2-PASS-DEGENERATE-POLICY`. Does learned formal structure constrain generation, reject invalid unseen structures, and support valid unseen generation? Survive symbol renaming; fail under structure ablation | learned grammar must reject invalid AND accept valid unseen structures | RUNNING |
| `substrate-spec` | not an experiment: a SPEC for a substrate where (a) a harness assertion proves solutions are reachable BEFORE any result is read, and (b) the prior's carrier provably survives acquisition. Both are preconditions, not tuning. This is what would reopen P5-meta | — | QUEUED |
| `noop-detector-rollout` | **DONE.** swept every run.txt on this lane. Self-comparisons all NO-OP (detector correct). `bounded_pin` run{1,2,3}v2 byte-identical to originals -- INVESTIGATED AND CORRECT: PREREG_V2 re-executes the same frozen binary against corrected bars, so identical output is the expected result, not a no-op regression. No genuine regressions found. | — | CLOSED |
| `P5-meta5b` | (competing fork, parallel branch) require the learner to apply a learned RULE to never-stored inputs; the rule is the acquired object | rule must beat fresh on unseen inputs without any fact store | QUEUED → separate branch |
| `P6-formal` | resolve `ZD2-PASS-DEGENERATE-POLICY`; does learned formal structure constrain generation? | learned grammar must reject invalid unseen structures AND accept valid unseen ones; survive symbol renaming | QUEUED (next) |
| `P7-inquiry` | learned inquiry vs strong baselines (fixed/greedy-info/uncertainty/random/oracle) | inquiry must beat greedy-info because evidence changes beliefs | QUEUED |
| `phase10-context` | generic rewrite applicability from **learner-owned** context, NOT `if pos==p` | position-blind rewrites were destructive; successor must acquire context itself | QUEUED |

**Standing hazard for every CURRENT item:** an arm that does not execute the
state its label claims. Happened 4+ times. `tools/lab/arm_audit.py` exists to
catch it; generators MUST emit `FP` fingerprint rows.

---

## QUEUED

| id | item |
|---|---|
| `causal-intervention` | intervention-capable vs observational-only learner; latent alternatives observation cannot separate |
| `trial-graph-leak` | do transient trial structures enter persistent state? clean / contaminated / reconstruction / persistence / permutation |
| `bridge-BR2` | conditional bridge at `unified_learn.zag:423,445` → generic replacement, rerun correctness+transfer+revision |
| `bridge-BR1` | syntactic five-route router at `:734` → contract-derived routing |
| `bridge-BR3` | candidate-origin taxonomy at `:1008` |
| `long-lifetime` | one persistent learner: A→B→C→changed A→A+B→misleading→memory pressure→new formal→inquiry→intervention→reuse |
| `scaling-100k` | does the generative-bias effect survive 100k structures (vs the ≤5-N artifact)? |
| `learned-predicate` | executable predicates as context source (distinct from learned pair stats) |
| `persistent-topology` | learned topology as context source |
| `dependency-expansion` | learned dependency expansion as context source |
| `rewrite-of-rewrite` | 2nd-order structural transforms (H10, never built) |
| `metagen` | generative state that changes the *generator's* own parameters |

---

## BLOCKED

| id | item | why |
|---|---|---|
| `external-red-team` | independent human reproduction + adversary | cannot be manufactured by the same agent. Internal adversarial replication (`tools/lab/`) is a mitigation, **not** a substitute. |
| `measure-tnn` | run any experiment against canonical TNN rather than a reproduction | out of scope for this lane; never executed the canonical learner |

BLOCKED items do **not** gate anything above.

---

## KILLED

| id | mechanism falsified | does NOT falsify | assumption that caused failure |
|---|---|---|---|
| `pos-blind-rewrite` | position-blind learned rewrites (P2/P5, phase10) | position-*aware* or context-acquired rewrite applicability | rewrite keyed on op-pair only; forced successor applied at any position |
| `bigram-transfer` | bigram/frequency state transferring to a related unseen target | structural or dependency-based generative state | state captures *what followed what*, not a structural relation |
| `bigram-revision` | bigram state recovering after invalidation | state with an active rebuild/replenishment path | decrements with no replenishment (reinforcement only on success) |
| `proposal-ranking` | scaling N to defeat counting (phase16/17) | anything about state changing *generation* | target either observable (→search) or hidden (→no signal) |
| `fact-cache-metalearn` | p5meta3: "learning-to-learn" as acquisition speedup with a retained-fact lookup available | learning-to-learn where facts CANNOT be retained | retention dominates when learning speed is measured on queries already stored |
| `all-prior-carriers` | **P5-meta CLOSED as NOT-ESTABLISHED.** fact store, population, retained population, and non-population weight table all failed to reduce acquisition cost; 37x horizon range neutral; population-borne prior actively harmful. Void where the harness could not reach provably-existing solutions | meta-learning in a substrate meeting the `substrate-spec` preconditions | prior experience never reached the mechanism: 9 defects on this line, all the same shape |
| `generic-machine-scaffold` | first-observation machine bootstrap in `observe` | seeded machines that are not content-independent | any prior at all scaffolds a partial fit, so irrelevant prior "helped" 40% |
| `assoc-substrate-metalearn` | p5meta4: asking learning-to-learn of a lookup+scaffold substrate | meta-learning on any substrate that can REPRESENT a mapping | acquisition was measured on queries the fact store could answer; on never-seen queries the prior went 3.00 -> 60.00 (never) |
| `router-selection` | `count16` SIG_B bucket router | query-conditional mechanisms generally | feature WAS the answer; researcher-authored router |
| `stochastic-outcome-additive` | additive support over chain elements | non-additive support | self-composition `(s,s)` scores `2s` |

---

## SURVIVING

| id | claim | boundary |
|---|---|---|
| `gen-bias-L2` | learner state changes **proposal generation**; experienced cost 8 vs fresh >4000; distilled state beats re-deriving from identical facts | **bounded L2.** Not transfer, not revision, not method ownership. State is n-gram statistics over a fixed alphabet. |
| `gen-bias-perm` | that result survives identifier permutation | A=8 vs H=6; broken-perm control correctly detected |
| `audit-bound` | across 1,025 audited sources, **0/137** structural writers read learner state | static analysis, type-aware; cannot see aliasing/global effects |
| `counting-ceiling` | query-blind arms are capped at `ceil(H/N)`; in affine-composition families the dilemma holds | bounded to that family; assumption A1 **untested** |
| `p1-p4-reweight` | local-plasticity / content-addressed / attractor arms make generation cheaper | **bounded L2 reweighting**; no structural expansion |
| `inherited-b5d-criterion` | `lifetime_metalearn` B5D compared errors across DIFFERENT families | within-family acquisition criteria (which p5meta3 adopted) | cross-family comparison measured task difficulty, not learning |

---

## NEEDS_REPLICATION

| id | why |
|---|---|
| `gen-bias-L2` | single author; 3 defects found in own code during the phase |
| `phase10-perm` | 8× ratio vs 1.5× tolerance — **not** a clean pass (draw hash not permuted) |
| `internal-adversary` | blind scorer / mutation adversary / cold-checkout reproduction — **not yet run** on phase 6 or 10 |

---

## ARCHITECTURAL DEBT

| debt | detail | blocks |
|---|---|---|
| `corpus-no-gating` | `sup[]` in `b24.zag` **ranks** (11 reads, all comparisons) and never **gates** (0 gated failures). Nothing in 88 borrowed experiments lets prior state change possibility. | any gating-state experiment |
| `fixed-alphabet` | generators sample a source-defined op set; learner reweights but never extends it | structural possibility |
| `no-position-context` | rewrites need context; handcoding `if pos==p` is forbidden | phase10-context |
| `mode-risk` | P1–P5 selected by arm index = mildest form of the forbidden mode pattern | phase10 |
| `arm-identity` | arm↔state mismatches are systemic, not isolated | trust in every result |
| `arm-divergence-check` | 4 of 5 p5meta5a defects were visible ONLY by comparing arms that should differ | (now permanent infra) |
| `intervention-persistence` | RESOLVED in 5d (clone minority restores it) | — |
| `no-op-detector-coverage` | detector reports INCOMPARABLE on 5 legacy table formats (bounded_pin, count16, lifetime15, noisy, selforg9) — formats it cannot parse are formats it cannot protect | QUEUED: extend parser |
| `age-never-read` | AGE buffer incremented and never read in the 5a-5e line — "retain the fittest" was decorative | — | fixed in 5e |
| `prior-mutation-dominates` | prior phase applied 75 mutations before acquisition started (vs 6 per acquisition trial), swamping any inheritance rule | priors that do not mutate | fixed in 5e; caught by no-op detector |
| `assoc-no-mapping` | the meta substrate has no representation of a rule independent of stored facts | any substrate with programs/structure | lookup+scaffold cannot express "learned rule"; `MACH` deletable with no loss |
| `clone-only-harness` | an evolutionary loop with cloning but no mutation operator | search procedures with any variation operator | fitness-improving search is impossible when the population can only converge to its current leader; distinct population collapsed 24 -> 4 |
| `full-info-acquisition` | a prior cannot accelerate a learner that already holds the full target answer set | meta-learning measured under PARTIAL observation | OBS was a complete copy of the answer set, so relevant==irrelevant==misleading exactly; substituting OBS for want() changed nothing |
| `clone-dominance` | a prior cannot help when cloning fills the majority of slots each generation | dynamics that preserve independent lineages | 24 slots, 12 cloned per trial, 1 mutated: the prior is overwritten on trial 1, so any "prior changes acquisition" hypothesis is unfalsifiable here |
| `converge-vs-retain` | p5meta5d: a prior that CONVERGES the population makes the NEXT learning phase worse (17.67 fresh vs 25.00 prior) | priors that RETAIN diversity and add structure alongside | SUPERSEDED by 5e: elitist retention removes the harm (17.67 = 17.67) and the benefit is still zero |
| `acq-insensitivity` | p5meta5e: acquisition ignores its starting population entirely over 300 trials | superseded by 5f (horizon also ruled out) | replacing the prior hurts, preserving it does nothing -- both mean the initial condition is irrelevant |
| `horizon-explanation` | p5meta5f: the inertness is not a search-horizon artifact (neutral at 8..300, a 37x range) | carriers other than population | measurement is SATURATED at both ends: long horizon washes out the start, short horizon makes the task too easy to distinguish starts |
| `noop-first-run-coverage` | no-op detector catches no-op EDITS, not wrong FIRST runs -- the 5f horizon bug masked the short end undetected because there was no prior table | pre-run assertion that sweep parameters reach the output | fallback used TRIALS() instead of the swept horizon; horizons 8 and 15 reported 300 |

---

## SUCCESSOR-GENERATION RULE

On every failure record, before queueing anything else:
1. exact mechanism falsified;
2. broader family NOT falsified;
3. assumption that caused the failure;
4. smallest structurally different successor;
5. whether architecture can be **deleted** because of the result.

A negative must create the next question automatically.