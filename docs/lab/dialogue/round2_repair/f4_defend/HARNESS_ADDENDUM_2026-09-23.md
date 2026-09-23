# Harness addendum — 2026-09-23 (harness-only, post-prereg)

The frozen prereg (commit b936d0f4b9a4a5b9ceb55351c2dfb803cec1f1c1) froze the
seven held-out probes' **inputs and acceptance criteria** in `HELDOUT.md`.
That freeze stands and is unchanged.

What changed, and why: the `heldout_battery.txt` committed in the prereg used
section labels `CHALLENGE` and `PROVENANCE`. The dialogue binary's section
accounting maps labels via `stype_idx`, which returns -1 for unknown labels,
and a -1 index causes an out-of-bounds panic during accounting after the
first turn. The labels `CHALLENGE`/`PROVENANCE` are therefore unusable in a
batch run.

Locally (before any held-out was examined or scored), the section labels in
`heldout_battery.txt` were changed to the supported label `FOLLOWUP`. No probe
input text, no expected-criteria text in `HELDOUT.md`, and no scoring rule
changed — only the batch-runner section label. The held-outs were run and
scored against the frozen `HELDOUT.md` criteria, manually verified below.

This addendum is dated after the prereg commit because the label failure was
discovered after it. History is not rewritten: the prereg commit keeps the
original file, this addendum documents the harness-only correction.
