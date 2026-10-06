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

| id | item | falsifier | status |
|---|---|---|---|
| `P5-meta` | prior experience changes **how future learning occurs** (not a strategy menu) | related prior must reduce acquisition cost on a NEW task; ablate meta-structure → speedup vanishes | RUNNING |
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

---

## SUCCESSOR-GENERATION RULE

On every failure record, before queueing anything else:
1. exact mechanism falsified;
2. broader family NOT falsified;
3. assumption that caused the failure;
4. smallest structurally different successor;
5. whether architecture can be **deleted** because of the result.

A negative must create the next question automatically.