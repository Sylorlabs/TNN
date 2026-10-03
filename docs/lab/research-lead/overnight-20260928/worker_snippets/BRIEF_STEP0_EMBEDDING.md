# Embedding Step 0 in Coordinator Spawn Messages

How to put the mandatory standing-rules name-check (Step 0) directly into
every `subagent.spawn` brief message, per `WORKER_BRIEF_TEMPLATE.md`.

## Placement

Step 0 is the FIRST item in the brief message body, before Role/Mission
or immediately after the one-line role. It is never a footnote and never
"see the template". The worker must complete Step 0 before any other
step.

## Verbatim Step 0 block to paste

Paste this block unchanged at the top of every spawn brief:

```
**Step 0: mandatory standing-rules name-check (do this first).**

Before any work, read the standing-rules block at the top of
LOOP_STATE.md in the repository root: the `## Standing owner rules`
section, the `## Standing owner rule: fork testing` section, the
`## Standing ruling: pure-Zag red line scope` section, and the
`## Standing rule: shell-only byte checks` section. State in one short
paragraph which standing rules apply to this task and how you will honor
them. Do not proceed to Step 1 until the name-check is written down in
your working notes or report.
```

## Rules always applicable (worker must name-check against these)

1. PURE ZAG ONLY. No Python anywhere in loop work: not glue, not
   analysis, not verifiers, not harnesses. Authoring Python scratch
   code anywhere in the wave is a K4 violation even if never executed.
   Disclosure does not cure use.
2. Image judge: sealed blind A/B pairs only when coded, tested, ready.
3. Fork testing: every wave enumerates every branch and fork and runs
   the frozen battery against each.
4. Pure-Zag scope: fixture provisioning counts as loop work, Zag-only.
5. Shell-only byte checks: use
   `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`
   for em/en dash checks. Never use python3 for byte checks.

## Coordinator compliance check

When the worker reports back, the coordinator verifies:

- The final report contains, or references, the written name-check
  paragraph (which rules apply, how honored). A report with no
  name-check evidence is a compliance gap; note it in the paper log.
- At least rule 1 (pure Zag) and rule 5 (shell-only byte checks) must
  be named by any worker that authors or checks files.
- K4 violations are still violations even when the worker discloses
  them or completes Step 0 correctly.

## Example

See `BRIEF_EXAMPLE_STEP0.md` in this directory: a full builder brief
with Step 0 embedded.
