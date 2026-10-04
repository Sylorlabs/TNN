# RESULT L3C-FORM: emergent conditional dispatch from generic construction ops

Date: 2026-09-30. Lane: L3-C revision-form builder.
Prereg: PREREG_L3C_FORM.md, commit dc9a91501 (frozen; committed alone).
Implementation: l3c_form.zag (this directory).
Compiler: znc 2026.07.0-dev (edition 2026).
Verdict: **L3C-FORM-PASS** (all frozen kill bars pass).

## What was built

A learner whose starting vocabulary contains NO conditional form:
rule table sig -> node, TERM nodes holding constants, and five generic
construction ops (op_new_node, op_mark_term, op_mark_disp, op_new_edge,
op_label_edge). Fixed generic machinery: a contradiction monitor (same
sig, different required output), a fixed generic discriminator disc()
(first single-feature separator found by data scan over f0..f3), and a
generic edge-following interpreter. On a clash event, construct() runs a
fixed six-op protocol parameterized only by disc()'s discovered (feat,
val) pair. The dispatch structure emerges in persistent state W; no
source routine names a feature, a value, or a sig-specific conditional.

## Frozen kill-bar results (mode 1, from run1.txt; run2/run3 byte-identical)

- K1: prereg dc9a91501 committed alone before any implementation file
  existed. Precedence verified: git merge-base --is-ancestor dc9a91501
  <this-result-commit> (see commit message trailer).
- K2a: events_pre_clash=0, events_fam1=2 (exactly the two motivating
  sigs, both after the clash phase). PASS.
- K2b: check_disp PASS for sig 67, sig 131, and sig 327. Graph dump
  shows per sig: exactly 1 DISP node, 2 TERM nodes, 2 edges; one
  unlabeled default edge to the old value, one labeled edge to the new
  value. PASS.
- K2c: eval_fam1=6/6 (4 training -> 2, 2 clash -> 0). PASS.
- K2d: zero source change for family 2. disc() discovered (f3 == 9), a
  different feature index than family 1's (f2 == 1). eval_fam2=4/4 and
  family-1 evals still 6/6. PASS.
- K2e: audit.sh exit 0, AUDIT=PASS (output verbatim in
  audit_output.txt). A1: zero forbidden constructor identifiers. A2:
  exactly one op_label_edge call site, args are variables (W,e1,fi,fv).
  A3: label writers sit only inside op_label_edge; feat/val are
  parameters. A4: interpreter has one uniform edge path; label contents
  flow through variables lf/lv; no domain feature or value literal.
  A5: every set32 sits inside an op_* fn, rule_link (seeding /
  protocol step 6 re-point), stash (observation memory), construct
  (op_* calls + bookkeeping), observe (event counters), or main init
  writing -1 to fresh state.
- K2abl: mode 0 run (identical source and binary, construction
  disabled by argv flag): monitor still fires (events_total=4), built=0,
  no dispatch nodes in dump; training evals pass (fam1 4/6, fam2 2/4),
  clash evals fail. The construction ops carry the revision. PASS.
- K3: pure Zag, zero Python at every step (implementation, harness,
  audit, byte checks all Zag or POSIX shell). 3/3 byte-identical runs:
  sha256 821d207a9c58a70debecf8fbcc8927f8066c7101f8883355da24ef1c8476b400
  for run1/run2/run3. No em or en dashes (shell-only
  check_no_dash.sh: DASH-CLEAN).

## Key finding

The separating predicates were discovered, not supplied: (f2 == 1)
for the motivating broadcast-last clash and (f3 == 9) for the
investigator-designed law-shift family, found by the same fixed scan
with no per-family source change. The resulting dispatch semantics
(which feature, which value, which outputs, for which sig) live
entirely in learner-constructed graph state in W. This is bounded
evidence toward C0-A (semantics in learner-created persistent state)
and C0-B (incrementally grown structure). It is NOT L3, NOT
Criterion 0 satisfied, NOT SURVIVES: the discriminator and the
construction protocol are fixed researcher machinery, and the
11-stage pipeline (independent reproduction, baselines,
alternative-explanation attack, OOD, transfer, red team, governance
audit) has not been run.

## Disclosure

Prereg section 7 K2d contains an arithmetic slip: the parenthetical
"(12/12 total)" is inconsistent with the operative frozen
denominators (6 family-1 evals + 4 family-2 evals = 10). The
per-family bars are unambiguous and both pass; the true total is
10/10. The slip is recorded here, not silently reinterpreted.

## Raw outputs

- run1.txt / run2.txt / run3.txt (mode 1, byte-identical)
- run_abl.txt (mode 0 ablation)
- sha256sums.txt
- audit_output.txt (verbatim audit)
