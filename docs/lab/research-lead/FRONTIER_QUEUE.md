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
> refuted. Ten defects (was nine; the tenth is the dead generator `m5g.zag`
> itself). Re-derivation: the closing conclusion SURVIVES because it never
> rested on `m5g` numbers. Reopening requires `substrate-spec`.


| id | item | falsifier | status |
|---|---|---|---|
| `P6-rich` | Attacked. Rename survived; uniqueness KILLED (6/6 NT-role tables cover the 22 strings); depth KILLED (train L1+L2 installs no A2, held-out 0/16). Live residue: menu-select a table that generalizes a first-symbol cut at the trained depth. L2, weaker than induced=truth | — | ATTACKED |
| `P6-uniq` | uniqueness+depth cannot be jointly satisfied in this encoding (NT=3, NRULE=2, any-NT-as-start, greedy-strict). Unique 1-rule family has n_pos<=1 so n_test>=8 is impossible. VOID, not a construction failure | — | VOID |
| `P7-inq` | VOID on this encoding. All 16 menu plans max at greedy-info 128; adaptive ceiling also 128; oracle 320 strictly best. LEARNER_EMPTY. Researcher menu contains the optimum, so any policy over it is researcher-owned | reopen only with a query language the world answers outside ASK_0..ASK_N | VOID |
| `gate-possibility` | FRESH and EXPERIENCED generate the same set {aa, bb}. SEEN_AB wrote the table; membership ignored it. No ENABLE bit. Possibility did not change | S1 must contain an element not in S0 that is not a source-authored unlock | NULL — ranking only, no expansion |
| `count-rule-own` | PAIR never (g67nb holds). CTAB=1 ORA=1. LEARNER_EMPTY. Count-table is live and researcher-owned | learner must cheapen a count rule without source-allocated count[sym] slots | VOID-OWN — gen-bias exhausted for non-pair structure |
| `join-underdet` | F1-add and F2-mul both 2/2 train, 0/2 hold, DISAGREE_HOLD=2. D is underdetermined (unlike lifejoin). LEARN empty | LEARN must not equal a named formula on held-out; F1 must disagree with F2 on hold | VOID LEARN — world clean, nobody owns the join |
| `joinown` | 4-form menu winner is always a named form. ADD/MUL fit train miss hold. ADD1 solves hold misses train. M empty | M must not be a two-item F1/F2 selector; complete object must not be a source menu | VOID L3 — ceiling L2-menu |
| `joinanon` | Train IDs pair-index AREV_B (i=3-k,j=k). Winner is a named map. FACTS/SCAN hold 0/2. LEARN empty | winning object must not be a named map in source | VOID L3 — ceiling L2-map. Successor: write (i,j) from unique-sum matches without a pairing-id menu |
| `depth-gen` | Depth-3 /16: induced=mem=facts=shallow=random=ablate-rec=0, oracle 16. No recursive concat induced | induce a recursively reusable rule, not a depth-specific table | VOID — obstruction is p6uniq Fact D plus first-rule-wins |
| `combin` | source-concat 2/2 on {345,453}, foils 0/2. facts/mem/ablate 0/2. LEARNER ties CONCAT=REV=2 and abstains. Compose is reusable at unused depth | LEARNER must not be source-concat via a source opcode; only one combinator in source => VOID ownership | VOID LEARN — compose is live; researcher owns box |
| `joinij` | WRITE stored unique train pairs (3,0),(2,1). LOOKUP 2/2 train, 0/2 hold. FACTS hold 0/2. GEN empty — i=3-k,j=k would be a pairing-id menu | stored (i,j) lookup must miss hold; regularity must not be a named map | VOID LEARN-GENERALIZE — pair-write is memory; regularity owner is researcher |
| `gmethod` | GRAPH tied LIST on transfer 100/100, inapp, revision 4/4, and fuel. FACTS 0. Wrong order 0. Topology did not cause method reuse | graph must beat a flat step list on transfer/revision; facts-only must miss | VOID LEARN — method graphs are not special |
| `gfail` | Localization works; owner is researcher. H-GFAIL killed (K2+K6). GRAPH-local does not beat a non-graph local revise that gets the same failure signal | GRAPH-local must beat FLAT-all on recovery cost without source saying revise-node-2 | KILLED — topology-as-index is researcher-owned |
| `lineage` | 1 clone/gen, pop=6, mutation live. FRESH d1=5/4/5 (lineages survive). STRUCT 3/2/3 vs FRESH 18/9/24 vs NOISE 9/19/24. FACTS miss the new band. Not meta-learning | structured==noise==fresh => prior unused; structured must not contain test answers | SURVIVING as clone-dominance lift only. lineageatk: WRONG beats NOISE; SHUF still separates; D1 and D2 both separate; MIN_HAM=1 plant=0. Advantage is compactness, not add-prefix structure. P5 stays closed |
| `gcomp` | GCOMP = LCOMP = COUNT on XFER 100. FACTS 0. Unit expanded (not bookkeeping). Graph spent 1 extra slot and won nothing | GRAPH-compress must beat LIST-compress on memory and reuse; compressed form must be used at test | KILLED H-GCOMP — graph compression is decorative |
| `gnary` | NARY = TABLE on acc+fuel. PAIR = NARY at LOOSE (extra node is bookkeeping). TIGHT NARY>PAIR is starvation, not capability | n-ary must beat a flat triple table; pairwise with enough intermediates must not merely starve | KILLED H-NARY — a triple table is enough |
| `glife` | GRAPH A-after-B = TABLE A-after-B = A-alone (100). Size 2->4, accuracy flat (append, not learning). Conflict flips both. TIGHT GRAPH>TABLE is starvation | GRAPH A-after-B must differ from TABLE A-after-B for a reason other than capacity | KILLED H-GLIFE — accumulated topology is unchanged vs a table |
| `rep-dual` | SEQ-REP wins SEQ loses PAIR; PAIR-REP opposite; SWITCH wins both (kill); SOURCE-OR wins both at 2x fuel. LEARN empty | body must not branch on family-id; BOTH_WIN only via source-OR is not ownership | VOID LEARN — dual-win without a switch is not available in this encoding |
| `holdout-uncacheable` | FACTS_HO=0 ORA_HO=8 FRE=0 LEARNER_EMPTY. Increment-all is researcher-owned. Cache cannot hit held-out | LEARN>FACTS on held-out FACTS cannot store; LEARNER must not be a source-coded transform | VOID LEARN — first honest FACTS-miss world, no owner of the transform |
| `query-construct` | World answers any 4-bit mask. Menu of 8 does not name {1,2,4,8}. Learner emitted exactly those four singletons (size 4) and scored 20 vs greedy-L 256. Still a menu | emitted strings must not be a subset of a size-8 researcher list | VOID LEARN — constructed queries collapsed to a smaller menu |
| `pred-gate` | no-gate damages (apply 2, dmg 1). researcher-P is pos==0 (4/4). LEARN empty | ablate-P must hurt; P must not be pos==p in source | VOID LEARN — applicability is a gate; researcher owns P |
| `rule-no-store` | FACTS_HO=0 ORA_HO=4 FRE=0. xor-5 is researcher-owned. LEARN empty | FACTS must miss never-stored x; LEARNER must not be a source-coded f | VOID LEARN — only a fact table; researcher owns the rule |
| `do-choose` | Informed is source f(x)=1 always-do-B. N_SPLIT=1. LEARN empty. Any learner that converges to do(B) imitates a researcher policy | more than one distinguishing intervention; world must answer interventions the researcher did not index | VOID ownership — single named splitter |
| `space-writer` | FRESH-LONG=PARSE=closure(M). S0=S1={aa,bb}. WRITE=0. SEEN_AB=2 ignored. No ENABLE. Live generator confirms 0/576: nothing is written that is not already in the source menu | S1 must contain a string outside closure(M) that is not a source literal | VOID-EXPANSION — researcher owns M |
| `trust-transfer` | Recency 22, oracle 24, ignore=fixed=16. C delayed A: recency on C works (7>0) without C≈A because C has its own window (T15_C=4 != T15_A=0). LEARN empty | a hidden if-source-id-then-trust is not transfer; C labelled like A is not transfer | VOID — trust is per-id recency, not a transferable type |
| `alias-write` | Auditor missed the alias (1 writer, 0 levers). S0=S1={aa,bb}. Scramble unlocks source literal abab (ENABLE, not a hole). 0/576 holds dynamically | S1!=S0 AND auditor misses it => first live hole | BOUND-HOLDS — caveat is real (missed alias) but possibility did not change |
| `open-prod-reject` | TABLE S1=S0={aa,ab,ba,bb}. Only drop of ab is source if-seen-neg-skip, which equals FACTS. CAND stays 4 | S1 missing ab only via source skip => researcher gate; EXPERIENCED=FACTS => filter not space change | NULL-EXCLUDE — filter, not a production-space change |
| `program-lossy` | Compact (form, k) 4/4 vs FACTS 0/4. Unique xor-5. menudel: WITH 4/4, DEL xor-k 0/4, EMPTY 0/4 | FACTS must miss held-out; compact menu containing f by construction is L2 not L3 | CONFIRMED researcher menu — deletion kills the win |
| `menudel` | program-lossy win dies when xor-k is deleted. combin: DEL CONCAT leaves REV 2/2; EMPTY 0/2. Family owned reuse, not unique CONCAT | win survives menu deletion => something else owned it | CONFIRMED — both L2 residues are researcher cognition |
| `gate-acquire` | LEARN is pos==k after search over {0..n}; k=0. LEARN=RESP=FACTS on TRAIN/HOLD; both lose on SHIFT | LEARNER-P must not be pos==k with k source-searched | VOID L3 — compact P from damage is a stored position, not a predicate |
| `combinown` | EMPTY 0/2. ANY surviving singleton {CONCAT} or {REV} 2/2. Unique constructor abstains. N_OUTSIDE=0 | family must not own reuse; EMPTY must not collapse if an unnamed combinator exists | VOID L3 — family {CONCAT, REV} owns reuse. Successor: apply-function emitter, not another named-op family |
| `inc-own` | FACTS_HO=0 ORA_HO=8. LEARN is x+k over {0..7}; K_PICK=1 hold 8/8. DEL k=1 -> 0/8. EMPTY -> 0/8. WIPE leaves k, kills facts | M must not be search over deltas containing 1 | VOID L3 — L2-delta-menu. Menu owned the win |
| `applyfn` | EMPTY 0/2. EXACT 0/2. Live tapes 01=CAT, 10=REV. N_OTHER=0. LIFT 2/2. Apply-function collapsed to {CONCAT, REV} | body must not decode to CONCAT or REV; tape must not be a source constant | VOID L3 — need a fixture that splits CONCAT from REV and a body language whose winners are not all-X-then-all-Y / all-Y-then-all-X |
| `partial-obs-prior` | REL=IRR=MIS=NONE 0/8 on never-stored queries. FACTS misses. Only ORACLE knows K. P5 collapse avoided; related prior still cannot help. LEARN empty | FACTS must miss test; REL must not store test answers; REL>NONE | VOID LEARN — PRIOR_HELP=0 |
| `alpha-extend` | Σ size 4 unchanged. S0=S1={0,1,2,3}. PAIR={1,3}. All Σ arms miss H. ORACLE hits H with researcher-owned 4. No ENABLE | new symbol must appear in a held-out win and must not be a source literal | VOID-MINT — fixed-alphabet holds |
| `rebuild-remain` | REB=DEC=4 FRE=0 ORA=8. Remaining cheapens the unflipped half vs fresh; decrement already had those pairs. Replenish unused. Researcher owns the keep-set re-count | rebuild must beat decrement-only; flipped half must not stay oracle-only | VOID LEARN — complement of bigram-revision is still researcher-owned |
| `hidden-signal` | ignore POST 2/4 vs acc POST 4/4. H never stored. Leak does not identify H alone. Researcher owns the XOR accumulator. LEARN empty | ignore must not match accumulator; leak must not equal H | VOID LEARN — A1 of the counting dilemma is now tested: a non-identifying signal can change guesses; the owner is the researcher |
| `compose-nc` | noncommutative join works (rev=4/8, rmerge=4/8, join=8/8). XY=fresh=chance 1/8. No learner composition | X+Y must beat fresh and must not equal reverse-join | RUNNING — world ok, learner empty |
| `method` | BASE 8/8, SUBTRACT 0/8 test, FACTS 0/8 test, ANSWERS_DISJOINT=1. LEARN VOID (no fake learner). Researcher owns finder/method. L0 | LEARN must beat FACTS on held-out and die under ablation | VOID LEARN — world clean |
| `causal2` | chain vs fork observationally identical; only do(B) splits. Oracle 80 > informed 72 > random 42 > obs 40. Learner slot empty. No CAUSAL_MODE | observational-only must not solve it; learner must beat random intervention | VOID learner-causal-ownership — world clean |
| `lifetime` | persist = fresh on D (0/4, cost 4). Store grew 4->8 and JOIN_D=4 (parts existed) but lookup never used them. All three kills fired. AGE does not improve future learning | persist must beat fresh on D; A-shifted must not be pure interference | KILLED — persistence without retrieval is not lifetime learning |
| `lifejoin` | persist+join 4/4 cost 0 vs persist-no-join/fresh/facts-only 0/4 cost 4. Researcher wrote ST[x-8]+ST[x-4] | persist+join must beat fresh and facts-only on held-out D; join must not leak D answers | KILLED as lifetime learning. Lookup is live (wrong-join/shuffle/empty-A/B all 0/4) but formula+train derives every D answer 4/4. Scoring the join against D is scoring a definition against itself. Ceiling L1 |
| `repown` | SEQ-REP wins SEQ 8/8 loses PAIR; PAIR-REP wins PAIR loses SEQ; AGREE=7 BOTH_WIN=0. No REPRESENTATION_MODE. Dual-win body would be a source switch (a kill), so LEARNER_EMPTY | a hidden if-task-class-then-rep is not ownership; both fixed reps solving both families means the world is too easy | VOID LEARN — researcher owns representation |
| `prov` | recency 14, oracle 16, ignore=fixed=8. Flip detected. Copies != two sources. Deletion removes the gain. Learner slot empty | ignore-source must not match the best arm; flip must be detected | VOID-LEARNER-PROVENANCE — world clean, researcher owns trust |
| `P6-struct` | 3-string fixture too small: n_test=1 and held-out was a prefix-extension. Inducer recovered A0->[3 3] A1->[A0 4] not truth. Precondition still holds as L1 representational viability (and enum-audit: numeric bars satisfied by ~256 grammars) | — | SUPERSEDED by P6-rich |
| `P5-meta5f` | **SHORT ACQUISITION.** 5e showed acquisition is INSENSITIVE to its starting population over 300 trials. Cut trials to ~15 so the initial condition still matters. If the prior is inert at 300 and active at 15, the blocker is search horizon, not meta-learning | prior must be inert at 300 AND active at short horizon | QUEUED |
| `substrate-spec` | not an experiment: a SPEC for a substrate where (a) a harness assertion proves solutions are reachable BEFORE any result is read, and (b) the prior's carrier provably survives acquisition. Both are preconditions, not tuning. This is what would reopen P5-meta. **Condition (a) now has a working, pure-Zag implementation** (`p6struct/precond.zag`); condition (b) still unmet | — | PARTIAL |
| `noop-detector-rollout` | **DONE.** swept every run.txt on this lane. Self-comparisons all NO-OP (detector correct). `bounded_pin` run{1,2,3}v2 byte-identical to originals -- INVESTIGATED AND CORRECT: PREREG_V2 re-executes the same frozen binary against corrected bars, so identical output is the expected result, not a no-op regression. No genuine regressions found. | — | CLOSED |
| `P5-meta5b` | (competing fork, parallel branch) require the learner to apply a learned RULE to never-stored inputs; the rule is the acquired object | rule must beat fresh on unseen inputs without any fact store | QUEUED → separate branch |
| `P6-formal` | resolve `ZD2-PASS-DEGENERATE-POLICY`; does learned formal structure constrain generation? | learned grammar must reject invalid unseen structures AND accept valid unseen ones; survive symbol renaming | QUEUED (next) |
| `P7-inquiry` | baselines exist on lane/p7inq. Learner-Q lost to greedy-info. Next: a learner that owns the inquiry *choice* without a researcher slot menu | inquiry must beat greedy-info because evidence changes beliefs | QUEUED — needs different mechanism |
| `phase10-context` | generic rewrite applicability from **learner-owned** context, NOT `if pos==p` | position-blind rewrites were destructive; successor must acquire context itself | QUEUED |

**Standing hazard for every CURRENT item:** an arm that does not execute the
state its label claims. Happened 4+ times. `tools/lab/arm_audit.zag` exists to
catch it; generators MUST emit `FP` fingerprint rows.

**Standing rule on evidence (adopted after four instrument failures):** a verdict is
not admissible until it has been reproduced against something INDEPENDENT of the code
that produced it — a hand derivation, a self-comparison, or an analytic ceiling. Four
instruments in this lane shipped with bugs that made them pass on mis-indexed data
(`score17`, `noop_detect`, `arm_audit`, `p6struct/precond`). All four were caught only by
such an external check. **An instrument validated only against itself is worse than no
instrument, because it manufactures confidence.** Corollary: never run a binary whose
compile failed; a stale build once had me analysing a program that did not exist.

---

## QUEUED

| id | item |
|---|---|
| `compose-noncommutative` | composition where the join does NOT commute, so random-merge cannot tie the upper bound |
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

### NEXT-WAVE (ranked, 2026-10-06) — do not rank by expected positivity

Rank = info gain × ownership relevance × falsifiability ÷ cost. One line each. Existing rows above are unchanged.

| rank | id | tests | cheap falsifier | why not a killed mechanism in new clothes |
|---|---|---|---|---|
| 1 | `gate-possibility` | whether any learner-updated cell appears in a predicate that *excludes* candidates (changes the reachable set, not cost) | candidate-set(gated)==candidate-set(ungated) on a world with ≥1 illegal continuation | `corpus-no-gating` is open debt. Pair-cache only cheapens SEEN bigrams; H-GRAPH/H-LEARNED-TOPO changed layout not possibility; lifejoin scored a definition |
| 2 | `count-rule-own` | whether any learner-updated state that is *not* a pair table can cheapen a count/parity continuation (g67nb successor) | EXP=FRE never at 200 on the g67nb world for every non-pair carrier | pair-cache-nonlocal killed *n-gram* cheapening of a count rule, not every carrier. Not Cond 3 (not claiming facts==distilled). Not method-menu (no finder slot) |
| 3 | `join-underdet` | join of stored A,B where ≥2 source formulas fit train and disagree on held-out D (D not algebraically fixed) | LEARN equals any named formula on held-out, or LEARN≤fresh | lifejoin-definition scored ST[x-8]+ST[x-4] against itself. H-COMPOSE-HINTLESS was hintless XOR (commutes). Here a combine step exists; who owns *which* combine |
| 4 | `holdout-uncacheable` | LEARN>FACTS on held-out items FACTS cannot store by construction | LEARN≤FACTS or wipe-store leaves LEARN intact | Cond 3 asked distilled==facts on the *same* queries. fact-cache-metalearn measured speedup with the answers already stored. This world forbids the cache hit |
| 5 | `query-construct` | learner emits a bit-string the world answers; no ASK_0..ASK_N menu | emitted strings ⊆ a researcher list of size ≤8 AND policy ≤ greedy-info on that list | P7-inq VOID'd a slot menu that contained the optimum. This requires a constructed query the world interprets |
| 6 | `rule-no-store` | acquired mapping applied to x' never stored, store wiped at test | wiped==fresh or wiped==facts-restored | fact-cache-metalearn and assoc-substrate kept a lookup. P5-meta5b is a competing fork; this is the wipe-at-test cut, not a new prior carrier |
| 7 | `alpha-extend` | learner mints a symbol absent from the source op set and uses it in a held-out win | \|Σ\| unchanged after training, or new symbol never appears in a win | pair-cache reweights existing symbols. H-LEARNED-TOPO grew edges that duplicated stored facts, not new symbols. fixed-alphabet is open debt |
| 8 | `space-writer` | whether any structural writer can read learner state (attack the 0/576 bound) without becoming a mode switch | re-audit still 0/N, or the read is a compile-time constant | audit-bound is a static fact, not a killed cognitive mechanism. Not PLAN/CAUSAL/REPRESENTATION_MODE — the probe is a data dependence, not a labeled arm |
| 9 | `open-prod-reject` | induced constraint rejects illegal unseen *and* accepts legal unseen when the production space is *not* source-enumerated | illegal-accept ≥ legal-accept, or rename collapses the split | P6-uniq killed uniqueness+depth in a 3-NT/2-rule encoding. P6-rich residue is menu-select over NPROD=294. This bans the enumerated menu |
| 10 | `depth-gen` | same productions, train max-depth 2, test depth 3; no uniqueness demand | depth3=0/N and a depth2-memorizer matches LEARN | P6-uniq said uniqueness+depth cannot hold *jointly*. This tests depth generalization of the surviving first-symbol-cut residue only |
| 11 | `program-lossy` | acquired object P is runnable; delete P kills held-out; delete facts does not | del-P==full or del-facts < del-P | assoc-no-mapping: MACH was deletable with no loss because the world was a fact store. This world must be inexpressible as lookup |
| 12 | `pred-gate` | executable predicate P(context) must hold to apply a rewrite (gate, not rank) | ablate-P==full, or P ≡ (pos==p) | pos-blind-rewrite keyed on op-pair only. Queued `learned-predicate` is a ranking context source. This is exclusion, same cut as `gate-possibility` on rewrites |
| 13 | `do-choose` | learner picks which variable to intervene; must beat random-do and observational-only | chosen var ~ uniform, or LEARN==obs | causal2 world is clean, slot empty. H-GRAPH killed topology-as-substrate not intervention choice. No CAUSAL_MODE label |
| 14 | `trust-transfer` | contradiction revises a source weight that then applies to a *third* unseen source | third-source weight == recency or == ignore | prov VOID'd researcher-owned trust arms. Not H-IDENT (not node IDs). Transfer to an unseen source is the ownership cut |
| 15 | `rep-dual` | learner-built R wins both SEQ and PAIR; body has no family-id branch | BOTH_WIN=0 or body branches on family-id | repown VOID'd *source-chosen* fixed reps (SEQ-REP vs PAIR-REP). Dual-win by a hidden switch was already named a kill; this forbids the switch |
| 16 | `rebuild-remain` | after 50% pair invalidation, remaining evidence restores the cheap path | post == decrement-only baseline | bigram-revision killed decrement-with-no-replenish. The unfalsified complement is an active rebuild, not a bigger n-gram |
| 17 | `partial-obs-prior` | meta-prior under OBS ⊊ answer-set so relevant ≠ irrelevant ≠ misleading | three priors tie on examples-to-criterion | all-prior-carriers closed P5 in a full-info substrate (OBS copied the answers). full-info-acquisition is the named debt. Not a new population carrier |
| 18 | `hidden-signal` | target hidden; learner gets a parity-of-misses bit, not the answer | LEARN==chance | proposal-ranking killed scaling-N when the target was observable (→search) or fully hidden (→no signal). Partial non-answer signal is the untested middle |
| 19 | `lineage-prior` | cap clones/gen to 1 so independent lineages survive; structured prior vs noise prior | still prior==fresh | clone-dominance made "prior changes acquisition" unfalsifiable (12/24 cloned). Changing the dynamics is not rerunning 5e. Not all-prior-carriers without that change |
| 20 | `alias-write` | aliasing/global path lets a structural writer depend on learner memory (audit's declared blind spot) | runtime answers invariant to scrambling the aliased cell | audit-bound cannot see aliasing. Not H-IDENT, not a topology carrier — it is a dependence probe on the 0/576 claim |

### NEXT-WAVE-2 (2026-10-06) — change the owner, do not rebuild VOID worlds

VOID/KILL/L2-menu worlds stay as-is. Successors change *who authors* the live object. Rank = info × ownership × falsifiability ÷ cost. Not positivity. Existing rows above are unchanged.

| rank | id | tests | cheap falsifier | why not a killed mechanism in new clothes |
|---|---|---|---|---|
| 1 | `menu-delete` | delete the researcher menu/opcode/form list from program-lossy, joinown, combin; residual win must survive | after deletion LEARN=0 while oracle still solves, or LEARN wins via a leftover named form | deletion of researcher cognition, not a new menu. program-lossy residue is unique-index in a source menu; this removes the menu |
| 2 | `join-owner` | on the already-clean join-underdet world, learner authors a combine that is not F1/F2/ADD/MUL/ADD1 and wins where those disagree | LEARN equals any named formula, or LEARN is a k-way selector over named forms | world already underdetermined (not lifejoin-definition). joinown VOID'd the menu. Owner of the combiner, not a rebuilt D |
| 3 | `combin-own` | combin compose is live; learner constructs the combinator from parts rather than selecting CONCAT/REV | winner is source-concat or source-rev, or source contains only one combinator | H-COMPOSE-HINTLESS was hintless commuting XOR. combin VOID'd ownership of a live box. Same world; different author of the box |
| 4 | `inc-own` | holdout-uncacheable already forbids the cache hit; learner induces the transform from (x,y) pairs with no source +1 opcode | LEARN is source-coded increment, or LEARN≤FACTS on held-out | Cond 3 / fact-cache measured stored answers. World is the first honest FACTS-miss. Owner of the transform, not a new holdout |
| 5 | `gate-acquire` | pred-gate is live; P is induced from damage, not written as pos==0 | P ≡ pos==p in source, or ablate-P==full | pred-gate VOID'd researcher-P. Queued learned-predicate ranks. This is exclusion owned by the learner (possibility, not cost) |
| 6 | `sum-pair` | write (i,j) from unique-sum matches with no pairing-id menu and no named map i=3-k | stored train pairs hit hold, or pairing is a named map / menu of maps | joinij pair-write is memory; joinanon VOID'd L2-map. Named successor: compute the pairing, do not select it |
| 7 | `rule-induce` | rule-no-store world; induce f from (x,f(x)), wipe store; f is not a source opcode and not a menu index | LEARN is xor-k / named opcode, or wiped==fresh, or unique index in a form menu | program-lossy survived as L2-menu xor-5. rule-no-store researcher owns f. Same world; f has no source name |
| 8 | `poss-no-enable` | S1 contains a string outside closure(M) with no ENABLE bit and no source-literal unlock | S1=S0, or the new string is a source literal, or an ENABLE flag appears | space-writer / gate-possibility VOID'd S0=S1 with ENABLE as the only unlock. Possibility expansion without ENABLE is the debt |
| 9 | `topo-eval` | two topologies, identical stored facts, different eval order ⇒ different answers; learner must build the topology that computes the right value | GRAPH==FLAT on answers (not fuel), or topology unused at eval, or FACTS matches | H-GRAPH/H-LEARNED-TOPO/H-GCOMP/H-GFAIL/gmethod killed topology-as-storage/index/compress. Here topology changes the computed value |
| 10 | `method-trace` | method world is clean; learner recovers an operation-trace from I/O, not a finder slot, not a graph, not a step-list menu | LEARN==FACTS, or the object is a source finder / GRAPH / LIST menu | gmethod VOID'd graphs-not-special. method VOID'd researcher finder. A recovered trace is a method object that is not a menu |
| 11 | `finder-delete` | delete the researcher finder from the method world; if a correct method remains recoverable from I/O, learner must recover it | after deletion no correct method exists, or LEARN uses a leftover named finder | deletion of researcher cognition on an already-clean world. Not H-GFAIL (not topology-as-index) |
| 12 | `count-noslot` | cheapen a count/parity continuation with no source count[sym] slots and no pair table | EXP=FRE, or a count[sym] array exists in source, or the carrier is a pair table | pair-cache-nonlocal killed n-grams on count rules. count-rule-own VOID'd the researcher count table. Owner of a third carrier |
| 13 | `acc-own` | hidden-signal world; learner constructs the accumulator; source XOR-acc is deleted | LEARN==source XOR-acc, or ignore==acc, or leak==H | hidden-signal tested A1 and VOID'd researcher-owned acc. Same leak; different author of the acc |
| 14 | `do-multi` | ≥3 variables split the world differently; learner picks among them; world answers do(X) for X not in a researcher index | N_SPLIT=1, or chosen var is the single named splitter, or LEARN==obs | do-choose VOID'd always-do-B (N_SPLIT=1). causal2 world is clean. Owner of multi-way choice, not a rebuilt chain/fork |
| 15 | `query-open` | world answers any bit-string of length ≤N (not a size-16 mask space); emitted set must not sit inside any researcher list of size ≤16 | emitted strings ⊆ a list of size ≤16, or policy ≤ greedy-info on that list | P7-inq VOID'd a slot menu. query-construct collapsed to {1,2,4,8} inside 16 masks. Open length removes the implicit menu |
| 16 | `join-construct` | on joinown's world, complete object is built from A,B matches; not a named form and not a selector over named forms | winner ∈ {ADD,MUL,ADD1,F1,F2} or is a k-way selector over those | joinown VOID L3 ceiling L2-menu. join-underdet nobody owns. Construction from matches, not selection, not a new formula set |
| 17 | `trust-type` | a class weight (not per-id recency, not C≈A) transfers to an unseen same-class source that has no own window | third-source weight == recency or == ignore, or T_C≠0 own window, or hidden if-source-id | prov VOID'd researcher trust arms. trust-transfer VOID'd per-id recency (C had its own window). Type-level, no own window |
| 18 | `replenish-own` | after 50% invalidation, learner-authored replenish restores the *flipped* half; not a keep-set re-count of the unflipped half | post==decrement-only, or replenish is a source re-count of remaining pairs, or flipped half stays oracle-only | bigram-revision killed decrement-only. rebuild-remain VOID'd researcher keep-set. Owner of replenish, same invalidation |
| 19 | `mint-op` | a minted symbol is *used as an operator* in a held-out win; not a source literal; no ENABLE | \|Σ\| unchanged, or new symbol never used as an op in a win, or ENABLE unlocks it | alpha-extend VOID'd fixed-alphabet (Σ size 4, all arms miss H). pair-cache reweights existing ops. Use-as-op, not alphabet storage |
| 20 | `space-both` | S1 loses an illegal *and* gains a legal that was not in S0, without source if-seen-neg-skip | S1⊆S0 (pure filter), or the new legal is a source literal, or EXPERIENCED=FACTS | open-prod-reject was NULL-EXCLUDE (filter). H-LEARNED-TOPO grew edges that duplicated facts. Expansion+rejection together |
| 21 | `rep-construct` | encoding where a single constructed R (not SEQ-REP/PAIR-REP/OR/SWITCH) can win both families; learner builds R from data | BOTH_WIN only via source-OR or family-id branch, or encoding still has no switchless dual-win | rep-dual VOID'd switchless dual-win in *that* encoding. repown VOID'd source-chosen fixed reps. New encoding so ownership is possible |
| 22 | `depth-own` | combin/depth-gen: reuse compose at unused depth with no source opcode and no uniqueness+depth demand | depth3 matches a depth2 table, or winner is source-concat, or uniqueness is required | P6-uniq killed joint uniqueness+depth. depth-gen VOID'd first-rule-wins. combin researcher owns the box. Owner of reuse at new depth |
| 23 | `ham-equal` | 1-clone dynamics kept; structured prior vs compact-wrong at equal Hamming and equal length | STRUCT==COMPACT-WRONG, or advantage dies when Hamming equalized, or test answers planted | lineageatk: advantage is compactness not add-prefix. clone-dominance already lifted. Equalizing compactness tests leftover structure |
| 24 | `writer-live` | a structural writer reads a *runtime-updated* learner cell and S1≠S0; not compile-time const; not alias of a source literal | re-audit 0/N, or the read is a compile-time constant, or S1=S0 | 0/576 holds statically. space-writer/alias-write found ENABLE or no change. Live cell → writer → new string, no ENABLE |
| 25 | `do-policy` | causal2 world; learner owns *when* to intervene (not which named var); no CAUSAL_MODE; no always-do-B | LEARN==informed (always-do-B), or LEARN==obs, or policy is a source if-x-then-do | do-choose VOID'd a single named splitter. causal2 slot empty. Policy ownership, not a rebuilt chain/fork and not H-GRAPH |

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
| `all-prior-carriers` | **P5-meta CLOSED as NOT-ESTABLISHED.** fact store, population, retained population, and non-population weight table all failed to reduce acquisition cost; 37x horizon range neutral; population-borne prior actively harmful. Void where the harness could not reach provably-existing solutions | meta-learning in a substrate meeting the `substrate-spec` preconditions | prior experience never reached the mechanism: 10 defects, all the same shape. `m5g.zag` is dead (bare block); "fix did not fix" is NOT REPRODUCIBLE |
| `H-GRAPH` | graph topology as a causal cognitive substrate (graphq1) | graphs as a storage layout | GRAPH tied FLAT/SEQ/TABLE/BAG at LOOSE; beat RANDTOPO on content not topology |
| `H-LEARNED-TOPO` | learner-created/deleted/rewired edges as a causal carrier (graphq2) | facts-only reconstruction | CREATE grew 0->12 edges matching truth; FACTS stored the same 12 facts with 0 edges and the same answers. Topology changed; topology did not cause the gain |
| `H-IDENT` | node IDs as a hidden carrier (graphq3) | genuine structure | consistent perm held on GRAPH/FLAT/FACTS; broken two-map dropped 100->66. Q16 ablation UNSEEN/DEEP 0/0 confirms topology decorative |
| `H-COMPOSE-HINTLESS` | spontaneous X+Y composition without a combine command (compose) | source-authored join | XY=Xabl=Yabl=fresh=irrel=4/8 chance; join=rmerge=8/8. XOR commutes so random merge tied the upper bound. Researcher owns every policy |
| `generic-machine-scaffold` | first-observation machine bootstrap in `observe` | seeded machines that are not content-independent | any prior at all scaffolds a partial fit, so irrelevant prior "helped" 40% |
| `assoc-substrate-metalearn` | p5meta4: asking learning-to-learn of a lookup+scaffold substrate | meta-learning on any substrate that can REPRESENT a mapping | acquisition was measured on queries the fact store could answer; on never-seen queries the prior went 3.00 -> 60.00 (never) |
| `router-selection` | `count16` SIG_B bucket router | query-conditional mechanisms generally | feature WAS the answer; researcher-authored router |
| `stochastic-outcome-additive` | additive support over chain elements | non-additive support | self-composition `(s,s)` scores `2s` |
| `pair-cache-nonlocal` (g67nb) | n-gram / pair-count state cheapening a count or parity continuation | other carriers that are not pair tables; cheapening of *seen adjacent* bigrams (`gen-bias-L2` residue) | pair table cannot store a non-adjacent count; EXP=FAC=FRE never at 200, oracle cost 1 |
| `lifejoin-definition` (lifejoinatk) | scoring ST[x-8]+ST[x-4] against D as lifetime/join learning | a join whose D answers are not algebraically fixed by the stored parts + a source formula | formula+train derives every D answer 4/4; lookup is live but the score is a definition against itself. Ceiling L1 |

---

## SURVIVING

| id | claim | boundary |
|---|---|---|
| `gen-bias-L2` | experienced makes a *seen* sequence cheap vs fresh-uniform | **L2 pair-count cache, near-tautological.** Cond 3 dead. g67nb + countown: count-rule world EXP=FAC=FRE never, oracle 1, count-table researcher-owned cost 1, LEARNER_EMPTY. Pair cache cannot cheapen what it cannot store. No learner-owned non-pair carrier without source count[sym] slots |
| `gen-bias-perm` | that result survives identifier permutation | A=8 vs H=6; broken-perm control correctly detected |
| `audit-bound` | **0/576** structural writers read learner state (cold clone; was 574 on an older tree) | static analysis, type-aware; cannot see aliasing/global effects |
| `p6-rich-L2` | induced productions = truth grammar on 22-string language; held-out 8/8 vs mem 0/8; recursion necessary | **L2.** Production space enumerated in source (NPROD=294). Not method ownership. Not yet attacked by rename or depth-shift |
| `counting-ceiling` | query-blind arms are capped at `ceil(H/N)`; in affine-composition families the dilemma holds | bounded to that family; assumption A1 **untested** |
| `p1-p4-reweight` | local-plasticity / content-addressed / attractor arms make generation cheaper | **bounded L2 reweighting**; no structural expansion |
| `inherited-b5d-criterion` | `lifetime_metalearn` B5D compared errors across DIFFERENT families | within-family acquisition criteria (which p5meta3 adopted) | cross-family comparison measured task difficulty, not learning |

---

## NEEDS_REPLICATION

| id | why |
|---|---|
| `gen-bias-L2` | **REPRODUCED then NARROWED then BOUNDED.** A=8 vs B never stands for *seen bigram sequences*. Cond 3 killed. g67nb: count-rule world, EXP=FAC=FRE never, oracle 1. The residue is "counting (prev,next) makes regenerating that pair cheaper than uniform" | still single author; residue is near-tautological |
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
| `no-op-detector-coverage` | **CLOSED.** the Zag detector handles FP/T/R rows; the 5 legacy formats were variants it never parsed. All 5 transitions verified and pinned in `tools/lab/fixtures/noop_fixtures.txt`. | — |
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

### REPO HYGIENE — 332 committed binaries (FLAGGED, deliberately not fixed)

`git ls-files` shows 332 tracked files with **no extension** (`*_bin`, `bp_bin`, `c5_bin`,
...). Mach-O build artifacts committed alongside their `.zag` sources, an established
convention on this lane that predates the current work.

**Why it matters:** a committed binary cannot be rebuilt on another platform and silently
shadows the source beside it. That is not hypothetical — a failed compile followed by
running the stale binary had me analysing a program that did not exist
(`p6struct/REPORT.md` §7). Any verdict produced from a committed binary is not
reproducible from the tree alone.

**Why unfixed:** removing 332 files is a large mechanical change to committed history
nobody requested, and some may be load-bearing frozen executables for older reports. The
4 binaries this lane's recent work introduced are now untracked and `.gitignore`d.

**Decide explicitly:** purge-and-rebuild-all, or adopt a documented "frozen binary" rule
with a `FROZEN.md` per phase. Do not leave it undecided.

### TOOLCHAIN — resolved 2026-10-05: lane is pure-Zag

This lane ran 13 Python files whose verdicts gated ~1,260 raw tables, invoked via
`/usr/bin/python3` specifically to bypass the PURE-ZAG guard. Charter section 4 violation;
every established lane on this repo has zero python with a NAMECHECK asserting it.

**Now zero.** All 13 ported to Zag and validated against real data:

| tool | validates |
|---|---|
| `tools/lab/arm_audit.zag` | I1–I7 arm-execution invariants; clean PASS, 6/6 defect fixtures FAIL |
| `tools/lab/noop_detect.zag` | 5 transitions incl. self-test; caught 2 real bugs in its own port |
| `tools/lab/namecheck.zag` | mechanical charter-4 audit; `RESULT=PASS -- lane is pure-Zag` |
| `phase1/audit_struct.zag` | 0 levers across **574** structural writers (was 137 under a narrower grammar) |
| `phase6/score67.zag` | every phase6/7 bar incl. permutation closure |
| `phase4/score4.zag` | every phase4/5 bar incl. the disqualifying Condition 3 |
| `count17/score17.zag` | all count17 verdicts over 42,120 rows |
| `count17/dilemma17.zag` | 780/1170/1560/1950 pairs, zero ambiguous |
| `count17/rootcause17.zag` | arm metric identically zero at every N |
| `p5meta3/score53.zag`, `p5meta4/score54.zag` | all five P5-meta bars, both phases |
| `p6struct/precond.zag` | substrate precondition, checked against hand-derived arithmetic |

**Four instruments shipped with bugs that made them PASS on wrong data** — `score17`
(block indexing + a 20k row cap on a 42k table), `noop_detect` (key omitted `budget`;
episode rows carry no `rg`/`arm`), `arm_audit`, and `p6struct/precond` (six bugs, plus
one stale-binary run). All were caught only by a check that does **not** consult the
implementation's own output. Hence the standing evidence rule in CURRENT.

**Independence is unchanged and not improved by any of this.** Same author wrote the
experiments, wrote the ports and wrote the checks. The ports make every verdict
*re-derivable in pure Zag*; they do not make it *independently confirmed*.
`external-red-team` stays BLOCKED.

---

## SUCCESSOR-GENERATION RULE

On every failure record, before queueing anything else:
1. exact mechanism falsified;
2. broader family NOT falsified;
3. assumption that caused the failure;
4. smallest structurally different successor;
5. whether architecture can be **deleted** because of the result.

A negative must create the next question automatically.