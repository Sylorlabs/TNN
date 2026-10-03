# WIRE-IN PROPOSAL: mint_guard.sh

**Worker:** GUARD-WIREIN (maintenance; claim minting paused per `f40fbeb11`)
**Date:** 2026-10-03
**Lane:** `docs/lab/research-lead/overnight-20260928/guard_wirein/`
**Design basis:** `mint_guard/MINT_GUARD.md` (MINT-SCRIPT-FIX, 2026-10-03)
**Status:** PROPOSAL ONLY. Nothing installed, nothing modified. Parent approval required before any step below is executed.

---

## 1. What the guard is and what it is not

`mint_guard.sh` is a bash pre-commit gate for the WATCHDOG claim ledger
(`canonical_ledger/CLAIM_LEDGER.md`). It inspects the staged diff after
`git add` and before `git commit`, enforcing: TIP matches HEAD (mint built
on a known-good base), insertions > 0 with deletions == 0, HEAD:ledger is a
byte-prefix of the staged file (pure append, retires the tail rewrite),
exactly one well-formed 4-line entry with id = TIP max + 1, and no unstaged
ledger surprises. Retrospective testing in MINT_GUARD.md section 5 shows it
would have blocked all nine tail wipes and the empty commit.

It is a **worker-loop procedure backed by governance**, not a server-side
enforcement mechanism. The repo is local-only and unpushed; any worker can
bypass the script by committing without running it. Its force comes from the
rule "a ledger commit without a recorded guard pass is a violation", plus,
optionally, a git hook that makes bypass harder.

## 2. Environment facts that constrain the design

These were verified on 2026-10-03 in `~/workspace/tnn-rsi-gpi3`:

1. **This checkout is a linked worktree.** `.git` is a gitfile pointing at
   `/home/hatch/workspace/tnn-rsi/.git/worktrees/tnn-rsi-gpi3`. There are
   30+ sibling worktrees in `.git/worktrees/` (lane-*, tnn-rsi-*, etc.).
2. **Hooks are shared across all worktrees.** `git rev-parse --git-path
   hooks` from this worktree returns the COMMON hooks dir,
   `/home/hatch/workspace/tnn-rsi/.git/hooks`. A `pre-commit` hook placed
   there fires for commits made in EVERY worktree, on every branch, by
   every worker. There is no per-worktree hook directory consulted by git
   (the per-worktree gitdir has no `hooks/` and git does not look there).
3. **The incident mechanism is shared index/worktree contamination.**
   MINT_GUARD.md section 3.4: six of nine wipes were committed by experiment
   workers that never minted, because a botched watchdog rewrite left the
   shared worktree/index with the C377 tail deleted and the next committer
   swept the deletion in. Any wire-in must assume ledger damage can be
   sitting in any worker's index at any time.
4. **Minting is currently paused** (`f40fbeb11`), and the pending
   `f20dddf0b` restore (RESTORE_PLAN.md) is not yet executed. The guard's
   TIP is initialized to expect exactly the restored SHA
   (`31431585...6bcdf972`, max claim 410); it fails closed on the current
   damaged HEAD. Wire-in must therefore be sequenced AFTER the restore.
5. **The guard script hard-requires `/usr/bin/git`.** The `$HOME/safebin/git`
   symlink has known EPERM write failures (AGENTS.md). Any hook or wrapper
   that invokes the guard, or reimplements its git calls, must use the
   resolved binary, not the PATH-resolved `git`.

## 3. Placement options

### Option A: Procedural wire-in (tracked script + mandatory mint step)

Commit `mint_guard.sh`, `TIP`, and `MINT_GUARD.md` into the repo as tracked
files. Add one mandatory step to the watchdog mint instructions: after
`git add`, before `git commit`, run `./mint_guard/mint_guard.sh --claim N`
from the repo root; commit only on `MINT-GUARD PASS`; then
`--advance-tip`. This is exactly the placement MINT_GUARD.md section 4.1
specifies.

Strengths:

* The guard source is versioned, reviewable, and identical in every
  worktree once the commit is present on the branch. No per-machine install
  step to drift.
* Zero blast radius on experiment workers: nothing runs unless the mint
  procedure invokes it. The 30+ worktrees doing experiment commits are
  unaffected.
* Matches the existing governance model (AGENTS.md shared-worktree
  discipline is already procedural: explicit pathspecs, `/usr/bin/git`).

Weaknesses:

* Does not stop a worker from committing a ledger wipe without running the
  guard. It would not have stopped the six experiment-worker wipes, because
  those workers never ran a mint procedure at all. It relies on governance
  ("ledger commit without a guard pass is a violation") plus after-the-fact
  detection.
* The `--advance-tip` step writes the TIP working-tree file; if TIP is not
  committed, each worktree's TIP diverges (see section 5, refinement 1).

### Option B: `pre-commit` hook in the common hooks dir

Install an executable `pre-commit` at
`/home/hatch/workspace/tnn-rsi/.git/hooks/pre-commit`. It fires on every
commit in every worktree. It must be **ledger-conditional**: first check
whether the staged diff touches the ledger path
(`git diff --cached --name-only -- <ledger>`); if not, exit 0 immediately
(fast path, no worker impact). If the ledger IS staged, exec the tracked
guard script in mint or restore mode based on the commit subject, and block
(non-zero exit) on failure.

Strengths:

* Closes the bypass: the six experiment-worker wipes (commits that swept a
  staged ledger deletion alongside lane files) would have been BLOCKED at
  commit time, quarantining the damage instead of propagating it. This is the
  only option that addresses the propagation half of the incident, which the
  guard alone does not.
* The fast path is one `git diff --cached --name-only` on a single path:
  negligible overhead for the experiment commits that dominate traffic.

Weaknesses and risks (all specific to this environment):

* **Blast radius is repo-wide by construction.** One hook file governs 30+
  worktrees. A bug in the hook (wrong path, bad assumption, nonzero exit on
  the fast path) blocks ALL workers on ALL branches until fixed. The hook
  must be treated as shared infrastructure with a higher testing bar than
  the guard itself.
* **Blocks legitimate worker commits that swept damage.** When a worker's
  index contains a staged ledger deletion they did not author, the hook
  blocks their whole commit, including their lane files. This is the
  intended quarantine behavior, but the worker needs a documented unblock
  procedure or they stall mid-experiment (see section 6, step 4).
* **Not versioned, not cloned.** `.git/hooks/` is outside the worktree. New
  clones, repo re-creations, and fresh machines silently lose the hook. It
  needs an install checklist and a periodic "hook present and current?"
  verification, or it rots.
* **Old worktrees lack the guard script.** A worktree checked out at a
  commit before the guard lane exists has no `mint_guard.sh` to exec. The
  hook must degrade gracefully there (warn and pass, or fail closed only
  when it can actually evaluate). Fail-closed-everywhere would brick
  commits in stale worktrees.
* **Hook inherits the worker's PATH.** Safebin workers have a restricted
  PATH; the hook must use absolute paths (`/usr/bin/git`, `/usr/bin/sha256sum`,
  etc.) and must not assume `python3` or any interpreter beyond bash and
  coreutils.
* **Does not cover `--advance-tip`.** TIP advancement stays procedural
  (Option A) regardless; a pre-commit hook cannot do post-commit bookkeeping.

### Option C: Wrapper script for ledger commits

A tracked `mint_commit.sh` that runs the guard and then commits. Pure
convention; strictly weaker than A (a worker can still call `git commit`
directly) with no additional coverage. Not recommended as the primary
mechanism. It may still be useful as a convenience inside the mint
instructions, but it adds nothing the guard step does not already provide.

### Option D: `core.hooksPath` pointing at a tracked directory

Set `core.hooksPath` to a tracked directory (e.g. a `githooks/` dir in the
repo) so the hook SOURCE is versioned while the config is a one-line
install. Same blast radius and degradation issues as Option B; the only
gain is reviewable hook source. Worth considering as the implementation of
B rather than as a separate option: hook source lives in the repo, config
points at it. Note the config itself is still not versioned (repo config,
not cloned), and per-worktree config nuances apply, so the install
checklist from B remains.

## 4. Recommendation

**Adopt A now, add B (implemented via D) as the follow-up, in this order:**

1. **Option A (procedural)** is the mandatory base. The guard only works if
   the mint procedure runs it and `--advance-tip` stays a human/worker step.
   No hook can replace that.
2. **Option B via D (hook)** is justified specifically because six of nine
   wipes propagated through workers that never minted. The guard alone
   cannot stop propagation; only a commit-time check in the shared index can.
   The hook must be ledger-conditional with a microsecond-scale fast path,
   degrade gracefully on worktrees lacking the script, and ship with the
   worker unblock procedure in section 6.

Do NOT install the hook before: the pending `f20dddf0b` restore is executed
and verified (the guard fails closed on damaged HEAD, so a premature hook
would block every ledger-touching commit, including the restore itself
unless the restore path is handled); the guard script and TIP are committed
as tracked files; and the two refinements in section 5 are decided.

## 5. Refinements needed before wire-in (parent decisions)

1. **TIP must be a committed file, and the hook should read TIP from HEAD.**
   As designed, TIP is a working-tree file advanced by `--advance-tip`.
   Across 30+ worktrees, working-tree TIPs diverge immediately, and an
   uncommitted TIP is itself subject to the shared-worktree contamination
   the guard exists to prevent. Recommended: commit the TIP update with each
   guarded ledger commit (same commit, explicit pathspec for both files),
   and have the guard/hook read the TIP from `HEAD:mint_guard/TIP` rather
   than the working tree. The `--advance-tip` flow then becomes: advance
   working-tree TIP, stage it alongside the ledger, commit once. Parent to
   confirm; MINT-SCRIPT-FIX should amend the script accordingly before
   wire-in.
2. **Graceful degradation rule for the hook.** For worktrees whose HEAD
   predates the guard lane: if the ledger path is staged but the guard
   script is absent, the hook cannot evaluate. Options: (i) warn loudly and
   pass (keeps old worktrees working, leaves a bypass window), or
   (ii) block (fail closed, bricks stale worktrees until rebased). Recommend
   (i) with the warning text naming the exact remediation (`git rebase` onto
   a commit containing the lane), because bricking experiment worktrees over
   a maintenance gate is disproportionate, and the window closes as
   worktrees refresh. Parent to confirm.

## 6. Draft installation steps (NOT executed; awaiting approval)

**Prerequisites (must complete first):**

* P0. Execute the pending `f20dddf0b` restore per
  `ledger_restore/RESTORE_PLAN.md` and verify the working-tree ledger SHA
  equals `31431585aec8d01b971af959fe8cd48562f3d083dd0cf66b1c31974e6bcdf972`
  with max claim 410. The guard fails closed until this holds.
* P1. Resolve the section 5 refinements (committed TIP; hook degradation
  rule). If refinement 1 is adopted, MINT-SCRIPT-FIX amends `mint_guard.sh`
  to read TIP from `HEAD:` before wire-in.

**Step 1. Commit the guard as tracked files.**

* Step 1a. In a worktree on the mint branch, verify the three lane files
  are present and unmodified from the design:
  `docs/lab/research-lead/overnight-20260928/mint_guard/mint_guard.sh`,
  `mint_guard/TIP`, `mint_guard/MINT_GUARD.md`, plus this proposal
  (`guard_wirein/WIREIN_PROPOSAL.md`).
* Step 1b. `chmod +x` the script (record the mode bit; hooks and exec
  depend on it).
* Step 1c. Stage with explicit pathspecs using the resolved binary:
  `/usr/bin/git add -- docs/lab/research-lead/overnight-20260928/mint_guard/ docs/lab/research-lead/overnight-20260928/guard_wirein/`
* Step 1d. `/usr/bin/git commit -- <paths> -m "WATCHDOG: wire in mint_guard design (design only, not yet enforced)"`.
  Verify with `git show --stat HEAD`.

**Step 2. Procedural wire-in (Option A).**

* Step 2a. The parent designates where the watchdog mint instructions live
  (the spawn brief / watchdog procedure doc; no single canonical mint-procedure
  document was found in the overnight-20260928 tree during this task).
  Insert the mandatory 5-step sequence from MINT_GUARD.md section 4.5
  (pure append; stage with explicit pathspec via `/usr/bin/git`;
  run guard `--claim N`; commit only on PASS; `--advance-tip`),
  plus the two standing rules from section 4.6: the tail-rewrite mint is
  retired (repairs go through `--restore` only), and bare `git commit` /
  `git commit -a` remain forbidden in the shared worktree.
* Step 2b. Record in the same instructions that a ledger commit without a
  preceding `MINT-GUARD PASS` is a governance violation, and that the
  dash-hygiene trailer claim is under parent review (MINT_GUARD.md
  section 7 item 3), so workers do not "fix" it unilaterally.

**Step 3. Hook wire-in (Option B via D; only after Steps 0-2).**

* Step 3a. Add a tracked hook source, e.g.
  `docs/lab/research-lead/overnight-20260928/githooks/pre-commit`, with
  exactly this logic:
  1. Resolve repo root: `TOP=$(/usr/bin/git rev-parse --show-toplevel)`.
  2. Fast path: if `/usr/bin/git diff --cached --quiet -- <ledger-path>`
     (ledger path relative to TOP), exit 0.
  3. If `$TOP/<lane>/mint_guard.sh` is not executable, print
     `MINT-GUARD WARN: guard script absent at this HEAD; ...` and exit 0
     (degradation rule, section 5 item 2).
  4. Otherwise exec the guard: mint mode when the staged ledger diff is
     insertions-only and the pending commit subject starts with
     `WATCHDOG: ledger C`; restore mode when the subject starts with
     `WATCHDOG: restore` (pass `--expect-sha` from the staged TIP or the
     restore plan value). Any other subject touching the ledger: run mint
     mode with `--claim` derived from the staged entry, or block with
     "ledger changed outside mint/restore procedure".
  5. On guard failure, print the guard output plus the unblock procedure
     (Step 4 below) and exit 1.
  6. All git invocations via `/usr/bin/git`; no PATH dependence.
* Step 3b. Test the hook file with `bash -n` and with a dry run in a
  scratch worktree: stage a ledger deletion, confirm the hook blocks;
  stage a well-formed 4-line append on a verified-good base, confirm it
  passes; commit a lane-only change, confirm the fast path exits 0 and
  adds no perceptible delay.
* Step 3c. Install: `git config core.hooksPath <repo>/docs/lab/research-lead/overnight-20260928/githooks`
  (repo-level config in `~/workspace/tnn-rsi/.git/config`; applies to all
  worktrees). Verify with `git config --get core.hooksPath` from two
  different worktrees.
* Step 3d. Document the install in the lane README and in the parent's
  environment checklist: any fresh clone or repo re-creation must re-run
  Step 3c. Add a periodic verification (e.g. watchdog checks
  `git config --get core.hooksPath` and hook-file presence/executability
  on its cycle and mints a claim noting drift).

**Step 4. Worker unblock procedure (ship with the hook).**

* When the hook blocks a commit because the staged ledger diff fails the
  guard, the worker must: (1) NOT force the commit; (2) unstage the ledger
  path only: `/usr/bin/git restore --staged -- <ledger-path>`; (3) commit
  their lane files with an explicit pathspec; (4) immediately notify the
  watchdog that ledger damage is staged/present in worktree `<name>`.
  The working-tree ledger damage is then handled via the restore procedure,
  never by the blocked worker improvising a repair.

**Step 5. Post-install verification.**

* Confirm the hook fires in at least two worktrees (one ledger-touching
  blocked case in scratch, one lane-only fast-path case).
* Confirm the next real guarded mint passes end to end: guard PASS,
  commit, `--advance-tip`, TIP committed (if refinement 1 adopted).
* Record the wire-in completion as a ledger claim (ironic but appropriate:
  the guard's first production pass).

## 7. Risks accepted by this proposal

* **Procedural layer remains bypassable.** Option A plus governance stops
  honest mistakes, not deliberate bypass. The hook raises the bar but a
  worker can still `git -c core.hooksPath=/dev/null commit` or
  `--no-verify`. Full enforcement is impossible in a local-only repo; the
  residual control is audit (every ledger commit should have a matching
  guard pass in the record).
* **TOCTOU is narrowed, not eliminated.** Another worker can commit between
  the guard run and `git commit`. The hook shrinks the window to the
  hook-execution-to-commit interval but the shared-branch race remains;
  the TIP check guarantees the mint was built on a known-good base, which
  is the substantive protection.
* **Hook as single point of failure.** One file in one untracked directory
  governs 30+ worktrees. Mitigated by: ledger-conditional fast path,
  graceful degradation, absolute binary paths, dry-run testing before
  install, and the periodic presence check in Step 3d.
* **TIP concurrency.** Two simultaneous mints serialize through the TIP/HEAD
  check: the second minter's guard fails (their base moved) and they must
  rebuild on the new HEAD. Correct behavior, but the mint instructions
  should state the retry rule explicitly so the watchdog does not interpret
  a TIP failure as damage.

## 8. Explicitly out of scope for this wire-in

* Retiring the tail rewrite is a **procedural rule** (mint instructions),
  enforced mechanically by the guard's byte-prefix check (4.2 check 3).
  No code change beyond the guard itself.
* The dash-hygiene gap (MINT_GUARD.md section 7 item 3): every entry claims
  "No em dashes were used in this entry (verified)" while C402/C406/C407/C410
  contain em-dash bytes. The guard warns only. Enforcement, trailer fix, or
  claim removal is a parent content decision, not a wire-in step.
* The C411/C412/C415 backfill and the C455-C460 numbering collision
  (ledger_write/STAGED_LEDGER_ENTRIES.md): parent governance matters that
  must resolve before minting resumes, independent of how the guard is wired.
* Amending `~/AGENTS.md` shared-worktree discipline to reference the guard:
  home-file edit, parent decision, not done here.

---

**Decision needed from parent:** (1) approve Option A procedural wire-in;
(2) approve or defer Option B hook (with D implementation); (3) rule on the
two section 5 refinements (committed TIP read from HEAD; hook degradation
rule); (4) confirm the tail-rewrite retirement; (5) designate the canonical
location of the watchdog mint instructions for the Step 2a edit. No
installation performed by this worker.
