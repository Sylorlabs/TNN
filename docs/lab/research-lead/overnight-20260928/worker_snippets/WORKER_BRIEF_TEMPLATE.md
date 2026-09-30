# WORKER BRIEF TEMPLATE

Standard brief structure for all spawned workers in this loop. Every brief
uses the same sections, in the same order. The coordinator fills the
placeholders marked `[...]`.

---

## Template

**Role:** `You are the [NAME].` One line, exactly.

**Mission:** One sentence: what this worker must produce or decide.

**Context:** Relevant background, with exact commit hashes, verdict labels,
and prior findings the worker must know. No instruction is allowed to live
only in Context.

**Your task:** Numbered steps. Each step is concrete and checkable.
Separate design from implementation: a designer must not build, a builder
must not redesign.

**Kill bars:** Exactly three, named K1/K2/K3, each with a pass criterion.
Examples: K1 (prereg frozen before implementation), K2 (deliverable
complete), K3 (pure Zag, deterministic).

**Rules:** Always include all of these lines verbatim:
- No Python. No em dashes.
- Commits local, owned paths only ([path]).
- Use pathspec commits: never stage or commit files outside the owned path.
  Inspect `git status` before every commit; other workers stage their own
  files on this shared branch.
- Report [VERDICT-LABEL] in the final report.

---

## Step 0: mandatory standing-rules name-check (do this first)

Before any work, read the standing-rules block at the top of
`LOOP_STATE.md` in the repository root: the `## Standing owner rules`
section, the `## Standing owner rule: fork testing` section, the
`## Standing ruling: pure-Zag red line scope` section, and the
`## Standing rule: shell-only byte checks` section. State in one short
paragraph which standing rules apply to this task and how you will honor
them. Do not proceed to Step 1 until the name-check is written down in
your working notes or report.

Standing rules currently in force (name-checked at 2026-09-30):

1. PURE ZAG ONLY. No Python anywhere in loop work: not glue, not analysis,
   not verifiers, not harnesses. This is a literal rule: authoring Python
   scratch code anywhere in the wave is a K4 violation even if it is never
   executed. Disclosure does not cure use.
2. Image judge: sealed blind A/B pairs only when coded, tested, and ready.
3. Fork testing: every wave enumerates every branch and fork and runs the
   frozen battery against each.
4. Pure-Zag scope: fixture provisioning counts as loop work and must be
   Zag-only.
5. Shell-only byte checks: when checking loop documents for em or en dash
   bytes, use the shell-only snippet
   `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`
   (usage in `WORKER_BYTECHECK.md` in the same directory). Do not reach for
   python3 for byte checks.

---

## Brief-type variants

All variants keep the sections above. They differ only in scope:

- **Builder:** prereg commit must strictly precede implementation in
  ancestry; verify with `git merge-base --is-ancestor`.
- **Implementer:** copy frozen mechanisms byte-identical (sha256); only
  the driver may change.
- **Assessor / Monitor:** monitor only; no commits, no file changes.
- **Designer:** design only; no implementation, no build, no runs.
- **Attacker:** copies only; never modify sealed or frozen files.

---

## Final report contract

The final report must restate, in full, the deliverable the parent asked
for: verdict label, the commits made, the kill-bar results, and the key
findings or measurements. Reports are delivered automatically by the
runtime; the parent sees only the final message, so it must be complete
on its own. Never reply with "already delivered above".
