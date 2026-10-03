# C1-REPRO Prereg: Independent Reproduction of C1-CLEAN (pipeline step 4)

Reproducer: C1-CLEAN Independent Reproducer (subagent)
Date: 2026-09-30 UTC
Frozen alone before any rebuild or rerun.

## Claim under reproduction

C1-CLEAN-PASS (b2b1ec415): canonical W0-W2 63/63 on every world, 3/3
byte-identical repetitions each, stages A-L perfect; exploratory H0 66/67,
H1 67/67. Chain: prereg 13e4b1ce3 -> freeze b8d38d9c8 -> worlds e0a30377f ->
results b2b1ec415.

## What will be rebuilt

1. Contestant binary: compiled from the committed contestant.zag source
   blob taken from freeze commit b8d38d9c8, using the repo-shipped znc
   compiler. No binary will be copied from the original worker: only
   source blobs from the frozen commit are used.
2. Sequencer: committed run_race.sh from freeze commit b8d38d9c8
   (shell only), used as-is after byte-identity verification.
3. World generator is NOT rebuilt: world fixtures are fixed inputs. The
   committed world files (worlds/w0..w2, worlds/h0,h1; turns.jsonl and
   key.json) from worlds commit e0a30377f will be verified byte-identical
   against committed blobs before any run.

## Exact verification criteria

- K1 (independent rebuild): the rebuilt contestant binary comes from
  committed source only; source commits used are documented; the
  original worker's binaries are never touched or copied.
- K2 (results reproduce): canonical worlds W0, W1, W2 each score 63/63
  on all 3 repetitions, and the per-rep output files (scores.jsonl,
  replies.jsonl, stage_scores.txt, state files) are byte-identical across
  the 3 reps within each world, matching the committed C1-CLEAN results.
  Hard worlds H0, H1 are rerun as exploratory checks against the
  committed H0 66/67 and H1 67/67 expectations.
- K3 (purity): zero Python at every step (compile, run, compare, write);
  em/en-dash byte checks via the shell-only check_no_dash.sh snippet only.

## Discrepancy protocol

Any mismatch in score, byte-identity, or hash is reported honestly in
the reproduction report with its exact magnitude. Source is never
"fixed" to match results; a mismatch is a failure to be recorded, not
an artifact to be patched. Verdict is C1-REPRO-PASS only if all three
kill bars pass; otherwise C1-REPRO-FAIL with documented discrepancies.

## Standing rules honored

Pure Zag everywhere (no Python for glue, analysis, verifiers, or
harnesses); fixtures come only from committed blobs (pure-Zag red line
scope); shell-only byte checks; owned pathspec commits only on the
shared branch; the contaminated paper file is never touched; a live
.git/index.lock is waited on, never removed.

Step 0 name-check recorded: the four sections are (1) Standing owner
rules (pure Zag; Micah judges images; not in scope here), (2) Standing
owner rule: fork testing (frozen battery per fork; not applicable to
this single-chain reproduction), (3) Standing ruling: pure-Zag red line
scope (fixtures are loop work, so only committed world bytes are used),
(4) Standing rule: shell-only byte checks (check_no_dash.sh only).
