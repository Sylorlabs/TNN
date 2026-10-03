# One-System Rule Audit

Date: 2026-09-30. Auditor: One-System Rule Auditor.
Status: ONESYSTEM-AUDIT-COMPLETE.
Scope: active cognitive substrates in the TNN repository.
Method: systematic grep over all .zag sources; no sampling.

## Step 0 name-check

The applicable standing rules are (1) PURE ZAG ONLY, the literal no-Python
red line; this is documentation-audit work, so I used shell and git commands
exclusively and invoked no Python for any purpose; (2) shell-only byte checks
via the shell-only check_no_dash.sh snippet, never python3, since disclosure
does not cure use; (3) fork testing and the image-judge rule are not
applicable to a static codebase audit. I honored them by searching with
grep/awk/sed, writing pure markdown, leaving the contaminated paper untouched,
and committing with explicit pathspecs confined to my owned directory only.

## Inventory summary

| Category | Count | Verdict |
|---|---|---|
| Architectural modes (CAUSAL_MODE etc.) | 0 | CLEAN |
| Ablation flags named _MODE | 2 (SEL_MODE, CARRY_MODE) | NOTED, not architectural |
| Bridge mechanisms | 1 (bridge_apply/bridge_learn) | SINGLE, not three |
| Task-specific handlers (distinct) | 7 | FLAGGED |
| Hardcoded semantic cases | 0 switch/match; if-chain dispatch present | NOTED |
| Router mechanisms | 1 (route_line, 5 codes) | FLAGGED |

## Modes

Search: all .zag files for _MODE (case-sensitive).

Result: zero occurrences of CAUSAL_MODE, REVISION_MODE, LANGUAGE_MODE,
MEMORY_MODE, or PROCEDURE_MODE anywhere in the codebase.

The only _MODE identifiers are SEL_MODE (20 occurrences) and CARRY_MODE
(12 occurrences), both confined to hypd_v3/hyp_d_v3.zag. These are ablation
condition flags (v2 round-robin vs v3 schedule; v2 silent insert vs v3 seed
pool), not cognitive architecture modes. They exist to support the frozen
ablation comparison, not to route cognition through different subsystems.

Assessment: the architectural mode smell is absent. The ablation flags are
a mild process smell (behavior switches in source) but they are confined to
one experiment file and serve the preregistered ablation, not production
cognition.

## Bridges

Search: all .zag files for bridge function definitions.

Result: exactly two functions, forming ONE bridge mechanism:
- bridge_apply (conditional rule dispatch)
- bridge_learn (conditional rule induction via (pos,val) search)

Location: unified_learn.zag (canonical), inherited from bridge_learn.zag
(which is marked SUPERSEDED; the canonical implementation lives in the
unified learner).

The bridge serves one capability: when direct procedure discovery fails,
induce a conditional rule (IF input[pos]==val THEN proc_A ELSE proc_B).
The (pos, val) condition is learned via search, not hardcoded.

The One-System Rule triggers ARCHITECTURE REVIEW at three custom bridges
around one boundary. Count here is ONE bridge mechanism, not three.
No review trigger.

Assessment: the bridge is a dedicated mechanism, not learner-created state.
It is the single largest architectural smell in the active substrates.
However, it is ONE mechanism serving a general function (conditional
dispatch), and the condition itself is learned. It does not multiply.

Could the capability be achieved through learner-created state instead?
The bridge rule (pos, val, two procedure slots) is stored in a dedicated
4-slot table with a fixed 20-byte format. A more general design would store
conditional rules as ordinary learned structures in the same workspace as
procedures, with the condition expressed as a learned predicate rather than
a (pos,val) pair in a dedicated table. The current design hardcodes the
condition form.

## Task-specific handlers

Search: all .zag files for ^fn handle_ definitions. Deduplicated across
copies (the unified learner is replicated across many experiment dirs).

Distinct handlers:
1. handle_proc_learn_unified / handle_proc_learn: procedure learning
2. handle_proc_query_unified / handle_proc_query / handle_proc_query_intent:
   procedure query with intent disambiguation
3. handle_caus_learn: causal rule learning
4. handle_caus_query: causal query
5. handle_caus_hist: causal history inspection
6. handle_caus_revise: causal revision
7. handle_concept_learn: concept learning

The primary division is proc vs caus. Procedures and causal rules are:
- stored in separate bases (PBASE for procedures, BBASE for bridges,
  CBASE for causal rules)
- learned by separate functions
- queried by separate functions
- routed by separate codes (1/3 for proc, 2/4 for caus)

This is the clearest task-specific handler pattern in the codebase.
The router (route_line) classifies input lines by surface syntax
(str>str pairs vs iii>ii episodes) into proc vs caus tracks, and each
track has its own learn/query pipeline.

Assessment: this is a genuine architectural division. Procedures (string
transformations) and causal rules (integer triples) are treated as
different kinds of cognitive objects with different storage, learning,
and query machinery. The One-System Rule asks: why can the existing
general architecture not learn this behavior? Here the question becomes:
why can procedures and causal rules not share one learning substrate?

A partial answer exists in the representations: procedures operate on
strings, causal rules on integer tuples. But the learning operations
(discover a mapping from examples, store it, retrieve on query, revise
on contradiction) are structurally similar. The division is driven by
surface representation, not by a deep architectural necessity.

## Router

The structure-inferred router (route_line in unified_learn.zag) emits five
codes: 0=WITHHOLD, 1=PROC_LEARN, 2=CAUS_LEARN, 3=PROC_QUERY, 4=CAUS_QUERY.

Routing is by surface syntax, not learned. A line with 2+ str>str segments
routes to PROC_LEARN; 2+ iii>ii episodes route to CAUS_LEARN; a single bare
string routes to PROC_QUERY; a single 3-int tuple routes to CAUS_QUERY.

Assessment: the router is a hardcoded admission gate. It does not learn
routing; it classifies by syntax. This is the mechanism that enforces the
proc/caus division at the input boundary. If procedures and causal rules
shared one substrate, the router could be replaced by a single learned
dispatch (or eliminated entirely if the substrate handled mixed content).

Note: the frozen core (world_learn.zag) does NOT have this router. It has
a minimal command interface (OBSERVE, QUERY, ACT) with no task-specific
routing. The router lives in the unified learner, not the frozen core.

## Hardcoded semantic cases

Search: switch/match statements in .zag sources.

Result: zero switch/match statements found. Zag sources in this repo use
if-chain dispatch, not switch statements.

The if-chain dispatch in route_line (proc vs caus classification) and in
the intent mechanism (qscore computation) serve the same role as semantic
cases: they branch on the kind of cognitive object. But they are not
enumerated semantic type switches in the sense of the rule.

Assessment: no hardcoded semantic case blocks of the kind the rule targets.
The dispatch logic exists but is structured as conditionals, not as a
semantic type switch.

## Frozen core cleanliness

The frozen core (core_freeze/stage0/world_learn.zag, 1424 lines, 75
functions) contains:
- zero _MODE references
- zero bridge functions
- zero task-specific handlers (only OBSERVE/QUERY/ACT commands)
- zero router codes

Its mechanisms: fact store with importance/eviction, causal rule learning
(compute_arrivals, predict_gen), DDES ledger, two-hop reasoning, state
persistence. The ACT command is a documented placeholder (emits CHOICE 0).

Assessment: the frozen core is the cleanest substrate in the repo. It has
no modes, no bridges, no task-specific handlers, no router. The 1/9 freeze
result reflects capability gaps in this clean core, not architectural
sprawl. This is exactly what the One-System Rule wants: a small generic
core whose failures point to missing general mechanisms, not to missing
special subsystems.

## Continuing learner lineage

Files: continuing_learner/contlearn2.zag (27 fns),
learner_transfer/contlearn3.zag (39 fns), learner_substrate/lsub.zag
(39 fns), learner_compress/compress_learn.zag, learner_dev/dev_learn.zag.

All have zero _MODE, zero bridge functions. They use a single
consequence-policy store (capacity 36) with no task-specific handlers.
The compression work (C74) eliminated the independent 8,400-byte OpScope
slice, moving episodes to DDES ledger entries.

Assessment: the continuing learner lineage is architecturally cleaner than
the unified learner. It has one store, no router, no proc/caus split.
The C75 eviction pathology lives here (the 36-slot store with
lowest-index tie-break). Per the new direction, this must NOT become a
cache-policy treadmill; the fix must be a general learner-owned memory
representation, not another eviction variant.

## Top 3 consolidation opportunities

### 1. Unify proc/caus into one learned mapping substrate

What would be removed: the route_line 5-code router, the separate PBASE /
CBASE stores, handle_proc_learn_unified vs handle_caus_learn,
handle_proc_query_unified vs handle_caus_query. Approximately 4 handlers
and the router dispatch collapse into one learn function and one query
function.

What capability is preserved: procedure learning (string mappings),
causal learning (integer triple rules), and query for both. The surface
syntax distinction (str>str vs iii>ii) becomes a property of the learned
content, not a routing decision.

Falsifiable claim: a single mapping store with (key, value, kind-tag)
entries, one learn path, and one query path reproduces the K-U1 through
K-U5 unified learner battery scores with zero router codes and zero
proc/caus handler split.

Why it matters: this is the largest task-specific division in the active
codebase. It is also the division most likely to be unnecessary: both
tracks learn mappings from examples and retrieve on query.

### 2. Generalize the bridge into learner-created conditional structure

What would be removed: the dedicated bridge rule store (BR_MAX=4,
20-byte fixed format), bridge_apply, bridge_learn as separate functions.

What capability is preserved: conditional dispatch (IF condition THEN
proc_A ELSE proc_B) with learned conditions.

Falsifiable claim: conditional rules stored as ordinary entries in the
unified mapping substrate (condition as a learned predicate structure,
not a (pos,val) pair in a dedicated table) reproduce the K-U2a/b/c
bridge battery scores with zero dedicated bridge functions.

Why it matters: the bridge is the only dedicated cross-mechanism in the
unified learner. If conditions become learner-created structures rather
than (pos,val) pairs in a fixed table, the bridge dissolves into the
general substrate. This also answers the standing question directly:
the existing architecture cannot learn conditional dispatch because the
condition form is hardcoded, not learned.

### 3. Replace the intent retrieval layer with substrate-native
disambiguation

What would be removed: intent_record_proc, intent_record_br,
intent_exact_match, intent_qscore, intent_winner, and the IBASE store
(approximately 10 functions and one storage region).

What capability is preserved: withholding on ambiguity, selecting the
intended procedure/bridge on query.

Falsifiable claim: ambiguity detection via substrate-native signals
(multiple matching entries with divergent outputs) reproduces the
K-U4a/a2 intent battery scores with zero dedicated intent functions.

Why it matters: the intent layer is a retrieval-time disambiguation
mechanism bolted onto the procedure/bridge stores. If the substrate
natively tracks which entries match a query and whether they agree,
the intent layer is redundant. This is the smallest of the three but
the cleanest removal.

## Overall assessment

The codebase is cleaner than the One-System Rule fears suggest, but the
proc/caus division in the unified learner is a genuine architectural
split that should be consolidated. The frozen core is exemplary: no
modes, no bridges, no handlers, no router. The continuing learner lineage
is cleaner than the unified learner. The bridge is singular, not triple.
No architecture review trigger is hit.

The main risk is not current sprawl but future sprawl: each freeze-challenge
failure tempts a new handler, a new bridge, or a new mode. The audit
confirms the discipline has held so far (recent claims record zero new
modes/bridges/handlers). The consolidation opportunities above are the
places where the next failures should drive generalization, not addition.

## Kill bars

- K1 PASS: inventory via systematic grep over all .zag files, not
  sampling. Every _MODE, bridge function, and handle_ definition found.
- K2 PASS: each consolidation recommendation states what would be removed
  and what capability is preserved, with a falsifiable battery-score claim.
- K3 PASS: pure markdown, dash-clean via shell-only check_no_dash.sh,
  contaminated paper untouched (zero diff), zero Python.
