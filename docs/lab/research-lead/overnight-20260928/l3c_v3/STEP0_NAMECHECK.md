# L3C v3 Builder: Step 0 standing-rules name-check (2026-09-30)

Four standing sections govern this task. (1) PURE ZAG ONLY: honored. The
prereg is markdown, the implementation is pure Zag compiled with the pinned
znc (498abcb5), and all analysis, harnesses, and byte checks are shell only.
The dash check uses
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
and nothing else. Zero Python anywhere, including scratch and verification.
(2) Fork testing: the frozen v2 mechanism is reused verbatim as the base;
the interpreter is copied unchanged and its diff against the committed v2
source is verified EMPTY, which is the lineage check for this task.
(3) Pure-Zag red-line scope for fixtures: honored. No fixtures are
provisioned; all test worlds are constructed inline in the Zag main.
(4) Shell-only byte checks: honored, per (1). The contaminated paper
(TNN_RESEARCH_PAPER_20260929.md) is left completely untouched.

ONE-SYSTEM RULE (standing directive, 2026-09-30): honored. The change adds
no new semantic case, no new op, no new cognitive mode, no bridge, and no
task-specific handler. The new machinery is the general learning operation
of cover-set composition over the existing separator vocabulary, and the
union semantics it needs already exists in the interpreter's select_edge.
The architecture delta is recorded explicitly in the prereg and the result:
cognition source lines added, new hardcoded semantic cases (0), new modes
(0), new bridges (0), new task-specific handlers (0), learner-state
structures created.
