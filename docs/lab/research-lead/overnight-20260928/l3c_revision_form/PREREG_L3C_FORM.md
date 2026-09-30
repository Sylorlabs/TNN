# PREREG L3C-FORM: emergent conditional dispatch from generic construction ops

Status: FROZEN. Committed alone before any implementation.
Date: 2026-09-30. Lane: L3-C revision-form builder.
Compiler: znc 2026.07.0-dev (edition 2026), pinned at
  ~/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc

## 1. Question

Can a learner that starts with NO conditional form in its construction
vocabulary construct conditional-dispatch structure itself, from generic
graph-construction ops, when it hits the H-REVISE revision impossibility
(same input signature, different required outputs)?

## 2. Lineage (why this is structurally different)

- H-REVISE: KILLED with mathematical proof. No function P(k,n)->index can
  satisfy both training P(k,3)=2 and counterexample P(k,3)=0 for identical
  (k,n).
- REVISE2..11 chain: sidestepped the proof with RESEARCHER-DESIGNED
  versioned conditional dispatch. Downgraded; generic claim dead.
- bridge_learn.zag (SUPERSEDED): researcher-designed IF(input[pos]==val)
  form; the conditional constructor is in source.
- THIS attempt: the learner begins with no conditional form. It owns only
  generic graph ops (new node, new edge, label an edge with a predicate
  discovered from data) plus a generic interpreter that follows labeled
  edges. The conditional-dispatch structure must EMERGE via construction;
  it is not supplied. Source audit must confirm no conditional-dispatch
  constructor exists in source, only generic ops.

## 3. Starting vocabulary (frozen; contains no conditional form)

State W (byte array, fixed layout):
- Rule table: sig (i32, packed k*64+n) -> node id. At start every known
  sig maps to a TERM node holding a constant output.
- Graph store: nodes and edges.
  - Node kinds: TERM (holds a constant output value) and DISP
    (holds no value; routes through outgoing edges).
  - Edge: (from, to, label_kind, label_feat, label_val).
    label_kind 0 = unlabeled default edge; 1 = predicate edge
    meaning feats[label_feat] == label_val.
- The vocabulary has no "if", no "condition", no "dispatch builder":
  only nodes, edges, labels-as-data.

## 4. Generic construction ops (the ONLY mutators of graph/rule state)

- op_new_node() -> id          (creates empty node)
- op_mark_term(id, value)      (marks node TERM holding value)
- op_mark_disp(id)             (marks node DISP; holds no value)
- op_new_edge(from, to) -> eid (creates unlabeled edge)
- op_label_edge(eid, feat, val)(attaches predicate label; label is data)

No other routine may write nodes, edges, labels, or the rule table.

## 5. Fixed generic machinery (not construction vocabulary)

- Contradiction monitor: on observe(sig, out, feats): let node =
  rule(sig). If node is TERM and node.value != out, record a
  contradiction event (sig, old=node.value, new=out) and stash feature
  vectors. If node is DISP, predict via the interpreter; a mismatch
  records a second-order event (unexpected in frozen tests).
- Edge-label discriminator D (fixed, generic, data-driven): given
  multiset A of training feature vectors and multiset B of contradicting
  vectors, scan features i = 0..NF-1 (NF=4, frozen) and return the first
  pair (i, v) such that every vector in A has feats[i] != v and every
  vector in B has feats[i] == v. Pure search; no domain knowledge; the
  separating feature is never named in source.
- Generic interpreter: eval(sig, feats): node = rule(sig); if TERM
  return value; if DISP: scan outgoing edges in edge-id order; remember
  the first unlabeled edge as default; for each labeled edge, if
  feats[label_feat] == label_val, return the target TERM value; if no
  labeled edge matches, follow the default edge. One uniform code path
  for all labels: the interpreter never names a feature.
- Construction protocol (frozen sequence of generic ops, parameterized
  ONLY by discovered data): on contradiction (sig, old, new) with
  separator (i, v) from D:
  1. t_old = op_new_node(); op_mark_term(t_old, old)
  2. t_new = op_new_node(); op_mark_term(t_new, new)
  3. d = op_new_node(); op_mark_disp(d)
  4. e0 = op_new_edge(d, t_old)            (unlabeled: default)
  5. e1 = op_new_edge(d, t_new); op_label_edge(e1, i, v)
  6. rule(sig) = d
  The conditional form (dispatch on feats[i]==v) emerges from this
  protocol plus the discovered label. No source routine builds "a
  conditional for feature X"; X arrives only via D's data scan.

## 6. Frozen test cases

NF = 4 features, fixed order f0..f3.

Family 1 (motivating case; H-REVISE analog: broadcast-last, then the
impossibility made operational):
- sigs: (k=1,n=3) and (k=2,n=3).
- Training: 2 observations per sig: out=2, feats=[k%2, n%2, 0, 7].
- Counterexample: 1 observation per sig: out=0, feats=[k%2, n%2, 1, 7].
- Expected: monitor fires exactly 2 contradiction events, zero before
  the counterexample phase; D discovers (f2 == 1) for both sigs.

Family 2 (investigator-designed second contradiction family; frozen here
as the post-freeze novelty stand-in; full independent adversary comes
later in the pipeline):
- "law-shift": sig (k=5,n=7).
- Training: 2 observations: out=4, feats=[jitter, 3, 0, 7] where jitter
  is 0 then 1 (an irrelevant varying feature that must NOT separate).
- Counterexample: 2 observations: out=1, feats=[jitter, 3, 0, 9].
- Note f2 = 0 in both phases (the family-1 phase feature is
  uninformative here); the separator is (f3 == 9), a different feature
  index than family 1. The learner must handle this with zero source
  change.

## 7. Frozen kill bars

- K1: this prereg is committed ALONE before any implementation file
  exists; precedence verified with git merge-base --is-ancestor.
- K2a: family 1: exactly 2 contradiction events, both after the
  counterexample phase; D returns (2,1) for both.
- K2b: constructed graph dump shows, per family-1 sig: exactly 1 DISP
  node, 2 TERM nodes, 2 edges; one unlabeled default edge targeting the
  old value 2; one edge labeled (feat=2,val=1) targeting the new value 0.
- K2c: revised behavior: all 6 family-1 evals correct (4 training -> 2,
  2 counterexamples -> 0).
- K2d: family 2 with zero source change: D returns (3,9); dispatch
  built with default edge -> 4 and labeled edge (feat=3,val=9) -> 1;
  4/4 family-2 evals correct and family-1 evals still 6/6 (12/12 total,
  no interference).
- K2e: source audit passes per the frozen audit procedure in section 8.
- K2abl (ablation): mode 0 run (construction disabled by runtime argv
  flag; identical source and binary): monitor still fires its events,
  zero constructions occur, counterexample evals fail while training
  evals pass. Proves the construction ops carry the revision.
- K3: pure Zag, zero Python at every step; 3/3 byte-identical runs
  (sha256 of stdout equal); no em or en dashes in any committed file
  (shell-only check_no_dash.sh).

Verdict labels: L3C-FORM-PASS only if K1, all of K2a..K2e, K2abl, and K3
pass. Otherwise L3C-FORM-FAIL. No SURVIVES claim: this is a builder-stage
result; the 11-stage pipeline (independent reproduction, baselines,
alternative-explanation attack, OOD, transfer, red team, governance
audit) comes later. No L3 claim either: at most bounded evidence toward
C0-A/C0-B.

## 8. Frozen audit procedure (shell only; proves no conditional
constructor in source)

Run against the single implementation file l3c_form.zag:
- A1: grep -nE for forbidden constructor identifiers:
  mk_cond|make_cond|cond_new|build_cond|cond_dispatch|versioned|mk_if|
  if_pos|cond_pos . Expect zero matches. (Zag language keyword `if`
  is allowed: it is the host language, not a learner-vocabulary
  constructor. The audit distinguishes them: A1 targets identifiers,
  never the keyword.)
- A2: op_label_edge has exactly ONE call site in the file, and its
  feat/val arguments are variables (never integer literals). Verified
  by grep -n "op_label_edge" plus reading the call site.
- A3: no integer literal appears as a feature index in predicate
  position: grep for label_feat/label assignment lines; the only
  feature-index source reaching a label is D's loop variable.
- A4: the interpreter contains exactly one edge-following code path;
  it names no feature index and no output value (grep the interpreter
  fn for integer literals used as features: expect none).
- A5: the only writers of node/edge/label/rule state are the five
  op_* routines (grep set32/write sites confined to op_ fns plus the
  initial rule-table seeding, which writes TERM mappings only).
Audit script audit.sh (shell + grep) is committed with the
implementation; its output is recorded verbatim in the result log.

## 9. Determinism and purity

- No randomness, no clock, no hash iteration order, no input beyond
  frozen scripted observations and the argv mode flag.
- Pure Zag: implementation, harness, audit, byte checks are Zag or
  POSIX shell. Authoring Python anywhere is a violation; disclosure
  does not cure it.
- stdout is the only output channel; 3/3 runs compared by sha256sum.

## 10. What this does NOT claim

- Not L3, not Criterion 0 satisfied, not SURVIVES. The discriminator D
  is fixed researcher machinery (generic search, but researcher-fixed);
  the construction protocol is a fixed op sequence. What is
  learner-created: the graph topology, the predicate labels, and the
  resulting dispatch semantics, all in persistent state W, all derived
  from data. This is bounded evidence toward C0-A (semantics in
  learner state) and C0-B (growing structure), nothing more.
