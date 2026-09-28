# HTD-1 DEBATE — Compositional / Hierarchical / Memory-First Generation
## Slice: "structure-first family" (neither pure-autoregressive nor pure-diffusion)

**Status:** DEBATE phase only. Nothing here is built. These hypotheses are proposed for preregistration and head-to-head testing against the autoregressive slice, the parallel/refinement slice (G-PAx), and each other.

**Standing constraints carried in:** pure Zag; zero randomness in any decision path (byte-identical reruns: same input + same logged state → byte-identical output); preregister with kill bars before building; test head-to-head, never minimize; evidence committed to `docs/lab/htd-1/` on the tnn-native-lab branch. All tie-breaking is deterministic (lowest candidate/chunk/region id); never wall-clock time, never memory addresses, never hash-map iteration order.

**Shared proxy corpora (read in place, never copied):** `~/workspace/tnn-lab/corpora/pg100.txt` (5.6MB Shakespeare), `~/workspace/tnn-lab/corpora/sqlite3.c` (9.5MB C).

---

## Why this slice matters

TNN has cognition but no decoder, and everything it *does* have is deliberative, discrete, and committed: every memory store is an explicit commit/refuse/rollback, every phase transition is petitioned and gated, every belief change cites evidence. The structure-first family asks whether generation can work the same way — decide the *shape* of the output as a deliberate, ledgered act, then produce the content under that shape's constraints — instead of bolting on a token pump that is awake for every byte. This is also the most direct attack on Micah's 20W question: a system that commits to a skeleton, a plan, or a template and then executes it mechanically wakes deliberation for the decisions and lets the rest run cold. The parallel slice (G-PAx) drafts whole and repairs; this slice decides structure *before* content exists. Those are different bets about where the intelligence lives, and the head-to-heads are written to settle it.

**Nearest-neighbor warning:** G-PA4 ("frozen checkpoints") is the closest existing hypothesis. The difference is load-bearing: PA4's levels are *fixed expansion machinery* (L1/L2/L3 always run, in that order); G-CO1's skeleton is *deliberated per task* (the hierarchy itself is the decision); G-CO4's templates are *long-term reusable knowledge* (the hierarchy is remembered, not designed). If the build phase shows these collapsing into each other, that is evidence, not a bug — the head-to-head G-CO1 vs G-PA4 is designed to detect exactly that.

**Measurable meaning of "generation working" (shared across this slice's hypotheses):** a generation mechanism works if, on the proxy tasks below, its output (a) reconstructs the checkable ground truth at or above bar (exact byte-match, constraint satisfaction — never vibes; no decoder exists so quality is always anchored to what can be verified), (b) is produced deterministically (byte-identical across reruns from the same logged state), and (c) honors its own committed structure — a skeleton, plan, or template that the output violates is a failure of the mechanism, not a near-miss. Structure-honoring is itself a metric here, because it is the slice's central claim.

---

## Hypothesis G-CO1 — "Deliberate skeleton, constrained fill"

**Mechanism sketch.**
1. *Task parse (mechanical):* the prompt is converted to a task record `{goal_kind, hard_constraints[], soft_preferences[], byte_budget B}` by a fixed rule-based extractor (extractor version pinned in prereg). No judgment here — parsing is deterministic table lookup over the prompt template.
2. *Skeleton deliberation:* candidate skeletons are proposed from a fixed generator set (boundary heuristics: sentence/clause boundaries for prose, brace/paren/string balance for code — the generators are dumb, the *choice* is deliberate). Each candidate = ordered region list; each region carries `{id, kind_tag, byte_budget, constraint_subset[], dependency_links[]}`. Elimination is checkable: budget sums must be ≤ B, every hard constraint must be assigned to ≥1 region, dependency graph must be acyclic. Survivors are scored by a fixed deterministic scorer (constraint coverage, then budget slack); ties break by lowest candidate index. The winner is COMMITTED to the ledger as `skeleton_commit` — append-only, replayable, auditable.
3. *Region fill (deliberation, parallelizable):* each region is filled by deliberate recall-and-assembly under its committed constraint subset. Fills proceed in deterministic dependency order (topological sort, ties by region id) and each fill is committed with a pointer to its skeleton region id. Regions are independent by construction — one region's fill may read the skeleton and its dependencies' committed fills, nothing else (one-brain shared ledger, but disciplined reads).
4. *Weave + verification (mechanical):* regions are concatenated in skeleton order; a verifier checks the full output against the task record's hard constraints and each region's committed budget. Mismatch → the offending region is rolled back (ledgered rollback with the violated-constraint code) and re-filled, max 2 retries; then the item FAILs with evidence.
5. *Ledger records:* task record, skeleton commit, per-region fill commits and rollbacks, weave verification verdict, termination reason. Replay re-derives the skeleton choice and replays fills in dependency order to the exact final bytes.

Deliberation is spent on skeleton choice and region fills; task parse, weave, and verification are mechanical.

**Falsifiable predictions.**
- P1: Skeleton survival predicts quality — items with zero region rollbacks beat items with ≥1 rollback by ≥15 points of exact-match. (If the skeleton doesn't predict the outcome, it isn't doing work.)
- P2: Region independence holds — a build-time ablation that fills regions in reverse dependency order (still deterministic) changes zero output bytes. Any change is evidence of hidden cross-region coupling and invalidates the parallelism claim.
- P3: Total ops scale with region count, sublinearly with output length at fixed region count — the hierarchy, not the tape length, sets the cost.

**KILL BARS (preregistrable; any one firing kills the hypothesis).**
- KB1 (quality floor): exact-match on PROSE-REC < 80% → KILL.
- KB2 (cost distribution — where the cost goes): planning-phase ops (parse + skeleton deliberation + weave verification) must be ≤ 50% of total generation ops on the median item; if > 60% while quality sits below the autoregressive baseline → KILL. The claim is that deliberation is *cheap relative to what it organizes*; if planning eats the budget, the skeleton is overhead, not leverage.
- KB3 (expected failure mode — skeleton/output mismatch): committed-constraint violation rate in final output, after the 2-retry budget, must be < 10%; if ≥ 20% of items ship with ≥1 violated *committed* constraint → KILL. A skeleton the output ignores is decoration.
- KB4 (hierarchy value): skeletons surviving to output unchanged must be ≥ 60% of items; if < 40% (the skeleton is rewritten more often than kept) → KILL.
- KB5 (determinism): any byte divergence across reruns from the same logged state → disqualification (program law, not a kill bar — no appeal).

**Proxy task + metric:** PROSE-REC + CODE-REC (shared spec below). Metrics: exact-match rate, hard-constraint satisfaction rate, skeleton-survival rate, region-rollback histogram, ops broken down by phase (parse / skeleton / fill / weave-verify), memory slots touched ÷ total slots (the 20W sparsity read).

**Must face head-to-head:** the autoregressive slice's best hypothesis (does planned hierarchy beat sequential care?); G-CO4 (per-task skeleton vs reusable template — the design-cost shootout); G-CO2 (deliberated fill vs retrieved fill — is designing regions better than citing memory?); G-PA4 (deliberated per-task skeleton vs fixed-level expansion — which hierarchy localizes work better?).

---

## Hypothesis G-CO2 — "Retrieve, then compose" (memory-first assembly)

**Mechanism sketch.** Generation is not writing — it is deliberate assembly of retrieved memory. The output's bytes are *cited*, not invented.
1. *Recall (deterministic ranking):* the prompt queries the memory substrate; chunks are scored by a fixed scoring function over chunk metadata (tag overlap with prompt tags, commit recency rank, chunk kind match). Top-K by score, ties broken by lowest chunk id. K is fixed in prereg. The ranked list is ledgered.
2. *Composition plan (deliberation):* choose an ordered subset of the recalled chunks and the glue between them. Glue comes from a FROZEN glue table — mechanical bridging bytes/transitions, versioned, pinned in prereg, never invented at runtime. The plan = sequence of `(chunk_id, span_range, glue_id)` entries, committed to the ledger.
3. *Assemble + cite (mechanical):* output = concatenation of cited chunk spans interleaved with glue bytes. Every output span carries a citation `{chunk_id, byte_range}`. A verifier byte-compares every non-glue emitted byte against its cited span — any divergence is ledgered as `CITATION_FAULT` and the item FAILs. There is no "close enough": citation is byte-exact or it is a fault.
4. *Coverage gate (deliberative refusal):* if recalled chunks cover < C% of the prompt's required elements (C fixed in prereg), the run ABSTAINs rather than composing a thin answer — the same refusal machinery that held 100% over 2,595 temptations, now pointed at generation. Abstention is a verdict, ledgered with the coverage computation, not a silent skip.
5. *Ledger records:* recall query + ranked chunk list, composition plan commit, per-span citations, coverage computation, emit/abstain verdict with reason.

Deliberation is spent on chunk selection and ordering; scoring tie-breaks, glue insertion, assembly, and citation verification are mechanical.

**Falsifiable predictions.**
- P1: The verifier catches 100% of injected citation divergences (white-box cheat probe: deliberately corrupt an assembled span pre-verification; the verifier must flag every one). Fidelity isn't luck — it's architecture.
- P2: Quality degrades via abstention, not hallucination — as chunk coverage drops across probe bands, abstain rate rises monotonically while emitted-item exact-match stays flat. (If emitted quality sags instead, the gate is leaking.)
- P3: Recall dominates cost — ≥ 60% of total ops land in the recall phase. Memory search is the work; composition is cheap. If assembly dominates, the hypothesis has collapsed into generation-by-another-name.

**KILL BARS.**
- KB1 (quality): emitted-item exact-match on PROSE-REC < 75% → KILL. (Memory-first must reconstruct what it can cite; the bar is lower than G-CO1's because abstention legitimately shrinks the scored set — but what it emits must be right.)
- KB2 (cost distribution — where the cost goes): recall + selection must be ≥ 50% of total ops AND mechanical assembly ≤ 20%; if assembly ops exceed 30% of total (spans being regenerated rather than cited) → KILL.
- KB3 (expected failure mode — hallucination): ANY emitted item containing a non-glue byte that fails byte-compare against its cited span → KILL, zero tolerance — provenance is the hypothesis's one job. Separately: on low-coverage probe items, uncited-fill rate > 5% → KILL (it must abstain, not invent).
- KB4 (coverage honesty): on the out-of-corpus probe set (200 prompts with zero relevant chunks), abstain rate must be ≥ 90%; if the system emits on > 20% of zero-coverage probes → KILL (the refusal machinery failed its transfer test).

**Proxy task + metric:** PROSE-REC with the corpus loaded as fixed memory chunks (256-byte chunks, ids assigned in corpus order — chunking pinned in prereg), plus the out-of-corpus abstention probe set (200 prompts). Metrics: exact-match on emitted items, citation-fidelity pass rate (byte-compare), abstain rate by coverage band, recall-vs-assembly op split, cheat-probe catch rate (must be 100%).

**Must face head-to-head:** G-CO1 (retrieved fill vs deliberated fill — is memory enough, or must regions be designed?); G-CO3 (composition plan over chunks vs generation plan over ops — which plan vocabulary wins?); the autoregressive slice (does citing memory beat sequential invention on reconstruction?).

---

## Hypothesis G-CO3 — "Plan-verify-emit" (eliminative planning, mechanical executor)

**Mechanism sketch.** All judgment happens before a single output byte exists; emission is a dumb executor running a committed program. This mirrors the RC1 reasoning-control result: the system inspects its own verification bar, and every prediction must hold.
1. *Plan generation (deliberation):* produce M candidate generation plans (M fixed in prereg, e.g., 4). A plan = ordered op list over a fixed op vocabulary: `RECALL(chunk_query)`, `FILL(region_spec)`, `WEAVE(order)`, `CHECK(constraint_id)`. Plans are programs, not text — the thing being deliberated is a *procedure*.
2. *Eliminative verification:* each candidate plan is dry-run against a deterministic simulator embodying the task's checkable constraints — the system's own bar, inspected the way RC1's learner inspected its bar. A plan is eliminated when it fails a challenge with cited evidence (which op, which constraint, which simulated state). Survivors ranked by fewest ops, ties by lowest plan index. The winner is COMMITTED to the ledger as `plan_commit`.
3. *Emission (mechanical executor):* the executor interprets the winning plan's op list exactly — no deliberation, no deviation permitted, no self-repair. The executor's only legal acts are the plan's ops in the plan's order.
4. *Post-emission verification (mechanical):* output checked against the task record. Mismatch → plan rollback ledgered, item FAILs. The executor may not fix its own output; a fix is a new plan, deliberated and committed separately.
5. *Plan cache (portable knowledge):* committed plans are stored as portable knowledge chunks (Micah's portable-chunks direction). On a new prompt, a deterministic precondition check tests cached plans first; a cache hit skips planning entirely. Cache hits/misses are ledgered.
6. *Ledger records:* all M candidate plans, per-plan challenge verdicts with cited evidence, elimination events, winning plan commit, executor op trace, post-emission verification verdict, cache hit/miss records. Replay re-runs elimination and re-executes the winning plan.

Deliberation is spent on plan generation and elimination; precondition checks, execution, and verification are mechanical.

**Falsifiable predictions.**
- P1: Executor deviation is zero by construction; the measurable claim is that post-emission verification catches 100% of injected executor faults (cheat probe: corrupt an executor op's output pre-verification — every injection must be caught and the item failed, never silently shipped).
- P2: Plan reuse amortizes — on a curriculum of similar tasks, amortized ops/item drops ≥ 30% from the first quartile to the fourth quartile as cache hits replace planning. Plans are assets, not overhead.
- P3: First-run planning dominates (≥ 70% of ops) yet total cost over 10 similar tasks beats the autoregressive slice — the thinking/doing split pays off at curriculum scale, not item scale.

**KILL BARS.**
- KB1 (quality): exact-match on CODE-REC < 80% → KILL.
- KB2 (cost distribution — where the cost goes): on first-run items, planning (generation + elimination) must be ≥ 60% of total ops; if executor ops exceed 40% → KILL (the executor is doing the real work — the thinking/doing split failed). On repeat-task curricula, amortized planning share must fall below 35% by item 10; if not → KILL (plans aren't reusable assets, they're per-item theater).
- KB3 (expected failure mode — executor deviation): ANY executor output byte differing from the plan-specified op output → KILL, zero tolerance. This is the architecture's hard line — the exact analog of RC1's self-change gate, and it fires the same way.
- KB4 (plan survival): if > 25% of committed plans fail post-emission verification → KILL (planning isn't predictive — the simulator is a fantasy).

**Proxy task + metric:** CODE-REC (plans-over-ops suit code's checkable structure) plus a repeat-task curriculum — 50 sqlite3.c functions from one family (fixed list in prereg) to measure amortization. Metrics: exact-match, executor-deviation count (must be 0), cache-hit rate by curriculum quartile, amortized ops/item curve, cheat-probe catch rate (must be 100%).

**Must face head-to-head:** G-CO2 (plan over ops vs plan over chunks — which plan vocabulary?); G-CO4 (generated plans vs pre-committed templates — do plans converge to templates under reuse pressure?); the autoregressive slice (does thinking-then-doing beat doing-while-thinking?); the RC1 evidence standard as internal control (the plan-verifier must meet the bar the reasoning-control pilot set: inspect own bar, predictions hold, rollback on violation).

---

## Hypothesis G-CO4 — "Deliberative templates" (schema-first slot filling)

**Mechanism sketch.** The structure is not designed per task (G-CO1) or generated per run (G-CO3) — it is *remembered*: a small library of pre-committed structural templates, each a piece of long-term knowledge with contractual slots.
1. *Template library (long-term memory):* each template = named slot list + per-slot schema `{byte_budget, allowed constructs/lexicon, required cross-references}` + cross-slot constraints (e.g., "slot RETURN must reference the identifier introduced in slot LOCALS"). Templates are committed once, versioned, and count as knowledge — the library is small by prereg cap (≤ 12 templates for the two proxy genres; more than that is a lookup table wearing a costume).
2. *Template selection (deliberation, eliminative):* the prompt is checked against each template's preconditions (deterministic checklist, pinned in prereg). Candidates scored by precondition-match count; ties by lowest template id. If no template's preconditions pass → explicit `TEMPLATE_MISFIT` signal, ledgered. Force-fitting a failing template is a fault, not a fallback.
3. *Slot filling (deliberation per slot, dependency order):* each slot is filled via recall + constrained assembly; every fill must pass its schema check (mechanical). Schema failure → slot re-fill, max 2 retries, then `TEMPLATE_MISFIT`. Slots fill in dependency order so cross-references resolve against committed fills.
4. *Cross-slot verification (mechanical):* the assembled output is checked against the template's cross-slot constraints; violation → item FAIL with the violated constraint cited.
5. *Ledger records:* template commits (once each), per-run selection with precondition scores, per-slot fill commits + schema verdicts, cross-slot verification verdict, misfit signals.

Deliberation is spent on template selection and slot content; schema checks, cross-slot verification, and assembly are mechanical.

**Falsifiable predictions.**
- P1: Within-genre template reuse ≥ 80% — the same template is selected for ≥ 80% of items in a genre family. (If every item needs a different template, the library isn't knowledge, it's inventory.)
- P2: Failures concentrate at the compositional joints — ≥ 60% of item FAILs are cross-slot constraint violations, not intra-slot schema failures. The slots are easy; the composition is the hypothesis.
- P3: Per-run ops beat per-task design — median per-run ops ≤ 70% of G-CO1's median on identical items. Reuse must be cheaper than redesign, or the library is dead weight.

**KILL BARS.**
- KB1 (quality): exact-match on CODE-REC < 80% → KILL.
- KB2 (cost distribution — the reuse claim): median per-run ops must be ≤ 65% of G-CO1's median per-run ops on identical items; if templates cost as much as designing a skeleton from scratch → KILL.
- KB3 (expected failure mode — schema violation): final outputs violating their committed slot schema must be < 5% of items; ≥ 15% → KILL. A template the output can't honor is a lie the system tells itself.
- KB4 (fit honesty): on the misfit probe set (100 prompts from a held-out genre with no covering template), force-fit rate — emitting under a template whose preconditions failed — must be 0%; > 10% → KILL. Companion cap: if the build needs > 12 templates to cover the two proxy genres → KILL (prereg cap; a bigger library is a different hypothesis).

**Proxy task + metric:** CODE-REC (code has natural template families: init/teardown/accessor/parse-loop) + the PROSE-REC verse subset (sonnet/quatrain templates), plus the misfit probe set (100 prompts from a held-out genre, e.g., stage directions against dialogue templates). Metrics: exact-match, slot-schema violation rate, cross-slot violation rate, template-reuse rate per genre, force-fit rate, per-run ops vs G-CO1.

**Must face head-to-head:** G-CO1 (the design-cost shootout: per-task skeleton vs reusable template); G-CO3 (generated plans vs pre-committed templates — do cached plans converge to templates?); the autoregressive slice (schema-first vs sequential on code, where schemas are checkable).

---

## Cross-cutting preregistration notes (for the build phase)

- **Shared proxy spec** (frozen before building): PROSE-REC — 1,000 pg100 passages; prompt = preceding 64 bytes (fixed anchor) + target span 64–256 bytes to reconstruct + 3 named constraints per item from a fixed constraint vocabulary (pinned list); CODE-REC — 300 sqlite3.c functions; prompt = function signature + docstring comment + required identifier list; target = function body. Item lists identical for all four hypotheses + the autoregressive slice (+ G-PA4 for the hierarchy comparison). G-CO2 additionally uses the fixed 256-byte chunking of the corpus as its memory load and the 200-item out-of-corpus abstention probe set; G-CO4 additionally uses the 100-item misfit probe set.
- **Determinism gate (program law, applies to all):** byte-identical reruns (same input + same logged state) on 100/100 sampled items before quality numbers count. Divergence is disqualification, not a kill bar.
- **Common instrumentation:** total deterministic ops by phase, planning-phase op share, memory slots touched ÷ total slots (the 20W sparsity metric — Micah's first question is scored here), ledger bytes per output byte, termination reason per item, abstain/misfit rates where applicable.
- **Anti-shopping rule:** all budgets fixed in prereg (K recall depth, M candidate plans, retry counts, template cap of 12, coverage threshold C). Halts, abstentions, and misfits are item verdicts, not invitations to try harder.
- **Deterministic ordering everywhere:** candidate indices, chunk ids, region ids, slot order — never wall-clock, never addresses.

## Head-to-head matrix (this slice)

| Matchup | Decides |
|---|---|
| Each G-COx vs autoregressive best | Does any structure-first family beat sequential at all? |
| G-CO1 vs G-CO4 | Per-task skeleton vs reusable template (the design-cost shootout) |
| G-CO1 vs G-CO2 | Deliberated fill vs retrieved fill (is designing regions better than citing memory?) |
| G-CO1 vs G-PA4 | Deliberated per-task skeleton vs fixed-level expansion (which hierarchy localizes work?) |
| G-CO2 vs G-CO3 | Plan over chunks vs plan over ops (which plan vocabulary?) |
| G-CO2 vs AR | Citing memory vs sequential invention on reconstruction |
| G-CO3 vs G-CO4 | Generated plans vs pre-committed templates (do cached plans converge to templates?) |
| G-CO3 vs RC1 standard | Does the plan-verifier meet TNN's own reasoning-control evidence bar? |
| G-CO4 vs AR | Schema-first vs sequential on code |

---

## Steelman: the strongest objection to compositional/hierarchical generation for TNN

Structure-first generation front-loads commitment: the skeleton, plan, or template is decided before any output exists, so an early misjudgment compounds through every downstream act instead of washing out the way local sequential decisions can self-correct — and the append-only ledger that makes TNN trustworthy makes plan mistakes expensive, with rollback cascades burning exactly the deliberation budget the scheme claimed to save. For genuinely novel outputs there is no evidence a good plan is findable before the output exists; planning may be strictly harder than generating, which would make the "efficiency" an accounting trick that moves the hard part off the books while the executor coasts. And the history of hierarchical generation is stilted, boundary-visible output — seams where regions meet, slots filled to schema but dead on the page, beautiful plans with hollow content. If TNN's deliberation is as good as claimed, the honest test is whether the plan survives contact with the content — and the kill bars above are written to let the plan die loudly when it doesn't.
