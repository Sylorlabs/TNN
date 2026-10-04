# Example Brief with Step 0 Embedded

A complete spawn brief following `WORKER_BRIEF_TEMPLATE.md`, with Step 0
pasted at the top per `BRIEF_STEP0_EMBEDDING.md`. The coordinator fills
placeholders marked `[...]`; nothing else changes.

---

You are the REVISE Builder.

**Step 0: mandatory standing-rules name-check (do this first).**

Before any work, read the standing-rules block at the top of
LOOP_STATE.md in the repository root: the `## Standing owner rules`
section, the `## Standing owner rule: fork testing` section, the
`## Standing ruling: pure-Zag red line scope` section, and the
`## Standing rule: shell-only byte checks` section. State in one short
paragraph which standing rules apply to this task and how you will honor
them. Do not proceed to Step 1 until the name-check is written down in
your working notes or report.

**Mission:** Implement F3 REVISE (no world-name gating).

**Context:**
- Design: COMPLETE (ca157c743). REVISE_DESIGN.md.
- Mechanism: D1-D6 (trigger on goal_ok, refutation evidence, growth
  gate, replan, name ban, agnostic verdict).
- Falsifiers: F-RNAME, F-RABLN, F-RNAMEAUDIT, F-RCOST, F-RDET.

**Your task:**
1. Write prereg (frozen before implementation).
2. Implement REVISE.
3. Run falsifiers.
4. Report.

**Kill bars:**
- K1: Prereg frozen before implementation
- K2: All falsifiers run
- K3: Pure Zag, 3/3 identical

**Rules:** Prereg first. No Python. No em dashes. Commits local, owned
paths only (`docs/lab/research-lead/overnight-20260928/f3_revise_impl/`).
Use pathspec commits. Report REVISE-PASS or REVISE-FAIL.

---

## What the worker's name-check should look like

An acceptable Step 0 paragraph for this brief:

"Standing rules checked against LOOP_STATE.md. Rule 1 (pure Zag) applies:
all authoring, building, and running will use Zag and shell only, no
Python at any stage. Rule 5 (shell-only byte checks) applies: dash
checks via check_no_dash.sh only. Rules 2 (image judge) and 3 (fork
testing) do not apply to this single-path builder task. Rule 4
(pure-Zag scope) applies: fixture provisioning, if any, is Zag-only."
