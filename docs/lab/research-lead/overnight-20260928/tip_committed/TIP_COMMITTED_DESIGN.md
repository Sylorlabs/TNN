# TIP as Committed File: Design

**Worker:** TIP-COMMITTED (maintenance; design only; claim minting paused)
**Date:** 2026-10-03
**Lane:** `docs/lab/research-lead/overnight-20260928/tip_committed/`
**Design basis:** GUARD-WIREIN `WIREIN_PROPOSAL.md` section 5 refinement 1; MINT-SCRIPT-FIX `mint_guard/MINT_GUARD.md` section 4; `mint_guard/mint_guard.sh` (design artifact, uncommitted)
**Status:** PROPOSAL ONLY. Nothing implemented, nothing installed, nothing modified. Parent approval required before any implementation.

---

## 1. Problem statement

`mint_guard.sh` currently reads its TIP from the working-tree file
`mint_guard/TIP` and advances it with a post-commit `--advance-tip` step.
GUARD-WIREIN's proposal flags two consequences:

1. **Divergence.** Across 30+ worktrees the working-tree TIP is per-worktree
   floating state. Two minters on different worktrees hold different TIPs;
   one successful mint silently invalidates the other's TIP without any
   mechanism to notice.
2. **Contaminability.** The TIP is exactly the kind of shared, uncommitted
   file the guard exists to protect against: a botched operation in any
   worktree can rewrite the TIP, and the next guard run would then compare
   `HEAD:ledger` against a forged known-good base.
3. **Non-atomic advance.** The current flow is guard PASS, commit, then
   `--advance-tip`. A worker who forgets step 5, or whose session dies
   between commit and advance, leaves the TIP stale; the next mint is then
   built on a base newer than TIP and fails closed for no good reason.
   Worse, the guard PASS and the TIP advance are not the same transaction,
   so the TIP can describe a state that was never committed.

## 2. Decision: TIP is a tracked file, advanced inside the guarded commit

**Where TIP lives:** keep `docs/lab/research-lead/overnight-20260928/mint_guard/TIP`,
adjacent to the script that parses it. No relocation. Rationale: every
existing reference (MINT_GUARD.md, WIREIN_PROPOSAL.md, the script's
`TIP_FILE` constant) already names this path; moving it would churn
references for zero functional gain. Keeping it out of
`canonical_ledger/` is deliberate: the TIP describes the ledger, and
describing it from inside the same file would make the ledger's SHA depend
on the description (self-referential; unusable).

**Format:** unchanged. Last non-comment, non-blank line is
`<sha256-hex> <max-claim-int>`; comment header documents the rules.
The parser already ignores comment and blank lines; both the HEAD read
and the staged read use the identical parser.

**The core change:** the TIP update becomes part of the same atomic
commit as the ledger change. There is no post-commit `--advance-tip`
step and no floating per-worktree TIP that matters after the commit.

## 3. How `mint_guard.sh` reads the TIP

The script gains a single primitive and uses it everywhere a TIP value
is needed:

```
tip_at() { # $1 = git revspec, e.g. HEAD or :0
  /usr/bin/git show "$1:mint_guard/TIP" 2>/dev/null | tip_parse
}
```

`tip_parse` strips comment and blank lines, takes the last remaining
line, and validates: exactly two fields, field 1 is 64 lowercase hex
chars, field 2 is a non-negative integer with no leading junk. Anything
else is a hard FAIL with the exact defect quoted.

Two call sites, two distinct revspecs:

* **Base TIP** = `tip_at HEAD`. This is the known-good state the mint
  must be built on. It replaces the working-tree read in check 1:
  `sha256(HEAD:ledger)` must equal the base TIP's SHA. Reading from HEAD
  means the base cannot be contaminated by working-tree damage, and the
  value is identical for every worker standing on the same commit.
* **Staged TIP** = `tip_at :0` (the index). This is the proposed new
  known-good state. A NEW guard check verifies the staged TIP transition
  (section 4). The working-tree TIP file is ignored entirely by the
  guard; it exists only as a scratch pad for the `--stage-tip` helper.

**Bootstrap / absent TIP.** If `git show HEAD:mint_guard/TIP` fails
(worktree whose HEAD predates the guard lane), the guard FAILs closed
with an explicit message: the mint procedure may not run on a HEAD that
does not contain the lane; rebase or checkout onto a TIP-bearing commit
and rebuild the entry. This is deliberate: the procedure-side guard must
be strict, because a minter on an old HEAD cannot produce a trustworthy
TIP advance. (The hook-side degradation for such worktrees is different
on purpose; see section 7.)

**Resolved binary.** All reads use `/usr/bin/git`, never PATH-resolved
`git` (AGENTS.md safebin EPERM rule, already honored by the script).

## 4. The guarded commit flow (mint mode)

The old five-step procedure becomes:

```
# 1. append the 4-line entry to the ledger (PURE APPEND; tail rewrite retired)
# 2. stage the ledger with an explicit pathspec via the resolved binary
/usr/bin/git add -- docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md
# 3. compute the TIP advance from the STAGED state (helper, no commit)
/docs/lab/research-lead/overnight-20260928/mint_guard/mint_guard.sh --stage-tip
# 4. stage the TIP file (explicit pathspec, resolved binary)
/usr/bin/git add -- docs/lab/research-lead/overnight-20260928/mint_guard/TIP
# 5. run the guard BEFORE committing
./docs/lab/research-lead/overnight-20260928/mint_guard/mint_guard.sh --claim N
# 6. only if the guard prints MINT-GUARD PASS, commit BOTH paths explicitly
/usr/bin/git commit -- docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md \
                       docs/lab/research-lead/overnight-20260928/mint_guard/TIP \
  -m "WATCHDOG: ledger C464 (...)"
```

**What `--stage-tip` does** (replaces `--advance-tip`): reads the base
TIP from `HEAD:mint_guard/TIP`; reads the staged ledger from
`:canonical_ledger/CLAIM_LEDGER.md`; computes `new_sha =
sha256(staged ledger)`; verifies the new entry id in the staged ledger
equals `base_max + 1` (it cross-checks against `--claim` when given);
writes the working-tree TIP file as the old comments plus one new data
line `new_sha (base_max+1)`. It commits nothing and stages nothing; the
worker stages it explicitly. It is pure and idempotent: re-running it
recomputes the same line from the same staged state.

**New guard check (staged-TIP transition), run pre-commit:** the staged
TIP's data line must equal exactly `(sha256(:ledger), base_max + 1)`.
That is: field 1 == `sha256` of the staged ledger file, field 2 ==
base TIP max + 1. This check plus the existing checks compose the full
invariant:

1. Base TIP is the state the mint was built on (`HEAD:ledger` SHA ==
   `HEAD:TIP` SHA).
2. The staged ledger is a pure 4-line append on that base (existing
   checks 2 through 5, unchanged).
3. The staged TIP truthfully names the staged ledger's new SHA and the
   incremented max claim (new check).
4. No unstaged surprises: `git diff --quiet` must hold for BOTH the
   ledger and TIP paths (existing check 6, extended to the TIP path so a
   concurrent edit to either file between staging and commit is caught).

On PASS, the single commit atomically records ledger change and TIP
advance. The next worker's `HEAD:TIP` is then self-consistent by
construction.

**Why this is strictly better than post-commit `--advance-tip`:**
atomicity (no forget-to-advance state), verifiability (the guard
validates the TIP transition before the commit exists, not after),
and TOCTOU narrowing (the pre-commit hook re-evaluates the same checks
at commit time against the then-current HEAD; see section 6).

## 5. Restore mode

`--restore --expect-sha <sha>` follows the same shape:

1. `--stage-tip` equivalent for restore: the staged TIP's SHA field must
   equal `--expect-sha` (the restore acceptance criterion, same value
   RESTORE_PLAN.md uses), and its max field must equal the max claim id
   parsed from the staged restored ledger.
2. The guard's restore path skips the TIP-base match (HEAD is damaged by
   definition) but still runs the staged-TIP transition check, the
   insertions-only check, and the commit-subject rule
   (`WATCHDOG: restore` prefix).
3. TIP and ledger commit together with an explicit pathspec for both
   paths.

After the restore commit, `HEAD:TIP` names the restored state and normal
minting resumes on top of it. The pending `f20dddf0b` restore remains
the sequencing prerequisite: the guard fails closed until a HEAD exists
whose TIP and ledger agree.

## 6. Interaction with the pre-commit hook (WIREIN_PROPOSAL Option B via D)

The committed TIP makes the hook simpler and closes the main TOCTOU
window the proposal accepted as residual risk:

* At hook execution time the hook reads the base TIP from the CURRENT
  `HEAD:mint_guard/TIP` and the staged TIP from `:0:mint_guard/TIP`,
  then runs the same transition checks as the procedure-side guard.
  If another worker committed a mint between the procedure-side guard
  run and this commit, current HEAD's ledger SHA no longer equals the
  base TIP SHA the staged change was built on, and the hook blocks.
  The serialize-on-HEAD behavior the proposal wanted is now enforced at
  commit time, not merely at guard-run time.
* The hook never reads any working-tree TIP value. The only TIP inputs
  are HEAD (base) and the index (proposed advance).
* The hook still cannot do post-commit bookkeeping, and with this design
  it no longer needs to: there is nothing to advance after the commit.

The hook's ledger-conditional fast path is unchanged.

## 7. The 30+ worktree consistency problem

This is the section the design must carry, because the failure mode it
eliminates is the one that produced six of nine wipes.

**The invariant.** TIP is versioned state, not worktree state. For any
commit C that contains the lane, `C:mint_guard/TIP` names exactly the
ledger state `C:CLAIM_LEDGER.md` is in. Every worktree standing on C
sees the identical TIP. Divergence is impossible by construction: there
is no per-worktree value left to diverge.

**Staleness is explicit and safe, never silent.** Worktrees stand on
different commits; that is normal. A worktree on an older commit sees an
older TIP, and that older TIP is still self-consistent with that older
ledger. Two cases:

* An experiment worktree on an old commit never touches the ledger.
  The hook fast path exits 0. Zero impact, as in the proposal.
* A minter must be on a TIP-bearing HEAD whose TIP matches current
  branch tip state before minting. Concretely: the mint instructions
  require the minter to `git fetch`/sync and confirm
  `sha256(HEAD:ledger) == HEAD:TIP sha` (the guard's check 1 does this
  automatically). If their HEAD is behind, check 1 compares against the
  older TIP and the staged-TIP check still passes against that older
  base, but the commit would then fork the TIP lineage... no: this is
  the shared-branch race, and it resolves at commit time. The
  pre-commit hook reads CURRENT HEAD at commit time; if another mint
  landed first, check 1 fails and the second minter is told to rebuild
  on the new HEAD (`--claim` recomputed as new max + 1, `--stage-tip`
  re-run). If no competing mint landed, the commit is a normal
  fast-forward on the branch and the TIP lineage is linear. Branch
  topology is handled by ordinary git: two TIP-bearing commits on
  divergent branches merge like any other file, and a TIP conflict in
  a merge is resolved by taking the TIP of the branch whose ledger the
  merged ledger actually equals, then verifying with the guard.

**No resurrection of stale state.** Because the guard ignores the
working-tree TIP file, an old worktree with a months-old `TIP` file in
its working tree cannot inject that value anywhere. The file is scratch;
the committed blob is truth. A recommended cleanup (parent decision):
delete working-tree TIP drift by never committing from a worktree
whose working-tree TIP file disagrees with `:0:` TIP; the guard's
extended no-unstaged-surprises check already enforces the staged side.

**New clones and repo re-creation.** TIP arrives with the clone like
any tracked file. No install step, no bootstrap file to lose. This is
strictly more robust than the proposal's Option B concern about hook
rot: the TIP cannot rot because it is content.

## 8. Hook degradation rule (refinement 2, design input)

The hook must handle a ledger-touching commit in a worktree whose HEAD
predates the guard lane (no `HEAD:mint_guard/TIP`). Recommend
**warn-and-pass**, per GUARD-WIREIN's recommendation, for the reasons
given there, plus one this design adds: with TIP committed, the bypass
window is self-closing in a stronger sense. Any mint or restore that
wants the guard's protection must stand on a TIP-bearing HEAD anyway;
old worktrees can only make unguarded ledger commits, which the audit
rule ("a ledger commit without a recorded guard pass is a violation")
already treats as violations. Bricking stale experiment worktrees over
a maintenance gate remains disproportionate. The warning text must name
the remediation (`rebase` onto a commit containing the lane) and must
be loud: `MINT-GUARD WARN` to stderr, not a silent pass.

Fail-closed-everywhere is rejected: it would block legitimate
experiment commits in stale worktrees that happen to have swept ledger
damage into their index, with no path forward except a rebase the
worker may not be equipped to perform mid-experiment. The unblock
procedure from WIREIN_PROPOSAL section 6 step 4 covers the damage case
independently of the hook.

## 9. Failure modes of this design and their handling

1. **Corrupt TIP at HEAD** (unparseable data line). Fail closed with the
   defect quoted. Repair path: a `--restore`-style governance commit
   that stages a corrected TIP whose SHA field equals
   `sha256(HEAD:ledger)` and whose max field equals the parsed max claim
   id at HEAD; the hook's restore-mode subject rule covers it. Parent
   approval required for such a commit; it is not a routine mint.
2. **TIP/ledger mismatch at HEAD** (SHA fields disagree, file well
   formed). This is the "damage sitting in HEAD" state. The guard fails
   closed on every mint until a restore commit re-establishes agreement.
   This is the intended behavior, and it is now checkable by any worker
   in any worktree with one command, no scratch file needed.
3. **Two simultaneous minters.** Serialized through HEAD at commit
   time (section 6). The loser rebuilds: re-sync, recompute
   `--claim` as `new_max + 1`, re-run `--stage-tip`, re-run guard.
   The mint instructions must state this retry rule explicitly so the
   watchdog does not misread a TIP failure as damage (same note as
   WIREIN_PROPOSAL section 7 item 4).
4. **A minter stages TIP but edits the ledger afterwards.** The staged
   TIP check uses `:ledger` (index), and the extended
   no-unstaged-surprises check covers the TIP path; a post-stage
   working-tree edit to either file fails the guard. Re-stage and
   re-run.
5. **`--no-verify` / `core.hooksPath` override.** Unchanged from the
   proposal: bypass is possible in a local-only repo; the residual
   control is audit. Committed TIP strengthens the audit: every ledger
   commit's TIP transition is reviewable in `git log -p --
   mint_guard/TIP`.
6. **Merge conflicts on TIP.** TIP is a one-data-line file; conflicts
   are trivially resolvable by rule (take the TIP whose SHA matches the
   merged ledger; verify with the guard before committing the merge).
   Document the rule in the mint instructions.

## 10. What changes in `mint_guard.sh` (implementation checklist for MINT-SCRIPT-FIX)

For the parent's approval; no code written here:

1. Add `tip_parse` and `tip_at <revspec>`; all TIP reads go through
   them. Delete the working-tree `$TIP_FILE` read from the guard path
   (keep `$TIP_FILE` only as the `--stage-tip` output path).
2. Replace `--advance-tip` with `--stage-tip` (compute from `:ledger`
   and `HEAD:TIP`; write working-tree TIP file; stage nothing).
   Keep `--advance-tip` as a deprecated alias that errors with a
   pointer to `--stage-tip`, or remove it; parent decision. Removing
   avoids a silent no-op footgun; erroring avoids a confusing
   "command not found."
3. Add the staged-TIP transition check to mint mode and the
   EXPECT_SHA/max variant to restore mode.
4. Extend the no-unstaged-surprises check to the TIP path.
5. Resolve repo root via `git rev-parse --show-toplevel` and anchor
   `LEDGER`/`LANE` to it, so the script works when invoked from any
   cwd inside the worktree (current script assumes repo-root cwd).
6. Update the procedure block in MINT_GUARD.md section 4.5 to the
   six-step flow in section 4 above; retire the "after the commit,
   advance the TIP" sentence in section 4.2.
7. The hook source (`githooks/pre-commit` in the WIREIN_PROPOSAL plan)
   implements steps from section 6: fast path, degrade warn-and-pass
   when `HEAD:mint_guard/TIP` is absent, else exec the tracked guard
   with the same checks, reading TIP from HEAD and the index only.

## 11. Sequencing and prerequisites

1. Parent approves this design (and the two refinements it encodes).
2. MINT-SCRIPT-FIX amends `mint_guard.sh` and MINT_GUARD.md per section
   10. The amended script is tested in a scratch worktree: staged
   TIP mismatch blocked, stale working-tree TIP ignored, absent
   HEAD TIP fails closed with the bootstrap message.
3. The pending `f20dddf0b` restore executes per RESTORE_PLAN.md;
   working-tree ledger SHA verified as
   `31431585aec8d01b971af959fe8cd48562f3d083dd0cf66b1c31974e6bcdf972`,
   max claim 410.
4. Wire-in proceeds per WIREIN_PROPOSAL section 6 with the procedure
   text replaced by section 4 above: Step 1 commits the lane (TIP
   enters HEAD at its initialized value, which names the restored
   state); Step 2 installs the six-step mint instructions; Step 3
   installs the hook.

## 12. Open parent decisions

1. Approve TIP as committed file with same-commit advance (this design),
   or keep post-commit `--advance-tip` with a different
   divergence control.
2. Hook degradation: warn-and-pass (recommended, section 8) vs
   fail-closed.
3. `--advance-tip`: remove outright vs deprecated-alias error.
4. Whether the initial TIP-bearing commit should also be the wire-in
   commit (Step 1 above) or a separate governance commit preceding it.
   Recommendation: same commit; fewer moving parts, and the TIP's
   initialized value is already recorded in the lane's TIP file.
5. Designate the canonical location of the watchdog mint instructions
   for the Step 2a edit (still outstanding from WIREIN_PROPOSAL).

---

**Summary for the parent:** make `mint_guard/TIP` a tracked file whose
advance is staged and committed atomically with each guarded ledger
change; the guard and hook read the base TIP from `HEAD:` and the
proposed TIP from the index, never from the working tree; replace
`--advance-tip` with a pure `--stage-tip` helper; 30+ worktrees stay
consistent because TIP is versioned state identical at identical
commits, staleness is explicit and safe, and concurrent mints serialize
through the HEAD check at commit time. Design only; no implementation
performed.
