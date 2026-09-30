# Step-0 name check (LOOP_STATE.md standing rules)

The standing-rules sections at the top of LOOP_STATE.md that apply to this
attack work are:

1. Standing owner rules: PURE ZAG ONLY. No Python anywhere in loop work,
   including implementation, harnesses, analysis, verification, and byte
   checks. I honor this by writing the attack harness, build, runs, and all
   analysis in pure Zag plus shell tools only (grep, awk, sort, sha256sum,
   cmp, diff). Zero Python at every step.
2. Standing owner rule: fork testing. Not directly applicable; this is a
   single-branch mechanism attack, no forks created.
3. Standing ruling: pure-Zag red line scope. Fixture provisioning counts as
   loop work; I provision no fixtures.
4. Standing rule: shell-only byte checks. I use
   docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
   for every committed document, never python3.
5. Debate rules: missing evidence means CANNOT-CONFIRM, never a pass; any
   Python touch of a wave artifact voids that artifact's wave evidence;
   frozen design constants change only via a dated pre-change prereg
   addendum. I honor these by freezing this prereg alone before any attack
   file exists, never weakening a frozen bar after results, and attacking
   only a verbatim copy of the committed mechanism (the committed
   l3c_v2.zag is never modified).

Additional discipline for this attack: explicit pathspecs on every git
add and git commit; git status inspected before each commit; never remove
a live .git/index.lock (wait and retry); the prohibited contaminated paper
(docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md)
is never edited, staged, committed, or read for evidence.

No em dashes or en dashes in any committed document (shell check above).
