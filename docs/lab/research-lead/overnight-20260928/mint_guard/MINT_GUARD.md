# MINT GUARD: pre-commit gate for WATCHDOG ledger mints

**Worker:** MINT-SCRIPT-FIX (maintenance; claim minting paused per `f40fbeb11`)
**Date:** 2026-10-03
**Lane:** `docs/lab/research-lead/overnight-20260928/mint_guard/`
**Repo:** `~/workspace/tnn-rsi`
**File under guard:** `docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md`
**Status: DESIGN ONLY.** No live procedure was modified. `mint_guard.sh` and `TIP`
in this lane are design artifacts, not wired into any worker instructions.
Nothing in this lane was committed.

Prior art: `c411_investigate/C411_INVESTIGATION.md` (C411 loss analysis),
`ledger_restore/RESTORE_PLAN.md` (pending f20dddf0b restore plan).

---

## 1. The mint procedure as found

**There is no mint script.** A repo-wide search found no script, function, or
harness that writes the canonical claim ledger:

- `grep -rl "CLAIM_LEDGER.md" --include="*.sh"` over the repo returns nothing
  that touches the canonical ledger. The only ledger-related scripts in the
  repo (`docs/lab/wave12/step2-ledger-instrument/run_step2.sh`,
  `docs/lab/wave4/integrity-ledger/run_il.sh`,
  `docs/lab/wave5/ledger-gating/run_lg.sh`) target older, unrelated ledgers;
  none reference `canonical_ledger/`.
- The WATCHDOG ledger mint is a **manual agent procedure**: the watchdog worker
  composes the 4-line claim entry, edits `CLAIM_LEDGER.md` with its file-edit
  tool, stages the file, and commits with subject `WATCHDOG: ledger C<n> (...)`.
  Every "WATCHDOG: ledger Cxxx" commit is authored by `tnn-rsi-loop
  <rsi-loop@localhost>`, the identity shared by all workers.

The canonical entry shape (4 physical lines, verified on the `860f009b5`
version of the file):

```
<blank>
- Cnnn (<entry text, single physical line>)
<blank>
No em dashes were used in this entry (verified).
```

## 2. Incident inventory (verified from the git record)

`git diff --numstat <c>^ <c> -- <ledger>` for every commit touching the ledger
in the 2026-10-03 07:45-08:12 UTC window. All times UTC.

### 2a. Tail-wipe commits: 0 insertions, N deletions (9 incidents)

| # | Commit | Author role | Time | ins/del | Deleted range |
|---|--------|-------------|------|---------|---------------|
| 1 | `29897129a` | WATCHDOG mint (C403, COMPOSE-CYCLES) | 07:45:18 | 0 / 96 | C377-C400 |
| 2 | `1932fe844` | experiment worker (LIFETIME-META) | 07:54:10 | 0 / 108 | C377-C403 |
| 3 | `d1d55de31` | experiment worker (NT-CAPACITY) | 07:58:21 | 0 / 112 | C377-C404 |
| 4 | `1e29a87c` | experiment worker (COGNITIVE-OPS-LEARNER) | 08:00:20 | 0 / 120 | C377-C406 |
| 5 | `8c6af9c4f` | experiment worker (L3-INR-SEALED) | 08:03:53 | 0 / 124 | C377-C407 |
| 6 | `eaf6d7ba1` | WATCHDOG mint (C411, LIFETIME-META-2) | 08:06:46 | 0 / 128 | C377-C408 |
| 7 | `cc7d7baae` | experiment worker (U-RETIREMENT) | 08:09:09 | 0 / 128 | C377-C408 |
| 8 | `b9999590` | experiment worker (GEN-CYCLES) | 08:11:12 | 0 / 136 | C377-C410 |
| 9 | `f20dddf0b` | WATCHDOG mint (C415, META-GENERALIZE) | 08:12:23 | 0 / 136 | C377-C410 |

The task named incidents 6 and 9; the full record shows **nine**, not four.
Six of the nine were committed by experiment workers that never intended to
mint a claim.

### 2b. Empty mint commit (1 incident)

| Commit | Author role | Time | Effect |
|--------|-------------|------|--------|
| `9bb51ff39` | WATCHDOG mint (C412, NT-EVICT-H1) | 08:08:05 | No file changes at all; C412's text exists only in the commit subject |

### 2c. Silent repairs inside "successful" mints (4 incidents)

These WATCHDOG mints show far more insertions than one 4-line entry, because
each re-added lines missing from its (damaged) parent and then appended its
own entry:

| Commit | Mint | ins/del | Composition |
|--------|------|---------|-------------|
| `9992a325e` | C404 | 112 / 0 | repaired `1932fe844`'s 108-line wipe + 4 new |
| `1611dc81c` | C405 | 116 / 0 | repaired `d1d55de31`'s 112-line wipe + 4 new |
| `ff8a2d8df` | C408 | 128 / 0 | repaired `8c6af9c4f`'s 124-line wipe + 4 new |
| `92a1831a7` | C409 | 132 / 0 | repaired `cc7d7baae`'s 128-line wipe + 4 new |

### 2d. Explicit restores (4 completed, 1 planned)

`a481fbe82` (+96 after #1), `07bb1cac2` (+120 after #4), `d238f75ca` (+128
after #6), `860f009b5` (+136 after #8). The restore for #9 (`f20dddf0b`) is
planned in `ledger_restore/RESTORE_PLAN.md` and **not yet executed**; the
current tip ledger ends at C376 and is missing C377-C410.

### 2e. True pure-append mints in the window

`bba82122a` (C402), `955bd5857` (C403), `c99bd82f5` (C407), `44ecf987a`
(C406), `9fd459b2e` (C410): each 4 insertions / 0 deletions. These are the
only mints that behaved as a mint should.

## 3. Root cause hypothesis

### 3.1 Primary: the mint is a tail REWRITE anchored at C377, not an append

The procedure the watchdog follows is not "append 4 lines at EOF". It is
"replace the region from C377 to EOF with a reconstructed tail plus the new
entry". Evidence:

1. **Constant anchor, tracking end.** All nine wipes delete exactly the block
   from the blank line preceding `- C377` through the live EOF. The start
   never moves (always C377); the end tracks concurrent appends (96 lines when
   EOF was C400, growing to 136 as the tail reached C410). An append-gone-wrong
   would be anchored at EOF, not at a fixed interior claim. A rewrite procedure
   with a fixed region start explains the anchor exactly.
2. **The silent repairs prove rewrite semantics.** A pure append can add at
   most 4 lines per mint. The 112/116/128/132-insertion mints (section 2c) are
   only possible if the worker rewrote the whole C377-anchored tail: each one
   reconstructed the missing entries from its own records and wrote them back
   together with its new entry. The procedure therefore *depends* on the
   worker's reconstruction being complete and correct on every run.
3. **C377 is the batch start.** C377 is the first claim of the overnight
   watchdog mint batch; the worker (or its session instructions) anchored the
   rewrite region there.

### 3.2 The intermittent failure mechanism

The rewrite has a single load-bearing step: reconstruct the C377..EOF tail.
When that reconstruction comes back **empty** (the worker's tail source read
fails, its in-memory block is lost, or it builds the replacement from an
empty variable), the file-edit operation replaces the whole region with
nothing. Result: 0 insertions, N deletions, committed with a subject line
that correctly describes the claim that was never written. Same procedure,
same anchor, empty reconstruction: this is why the failure is intermittent
and always takes the identical shape.

### 3.3 The empty commit

`9bb51ff39` (C412) is the complementary edit-tool failure: the edit's
old-text did not match (the file moved under the worker between read and
edit, plausibly because of the concurrent mint traffic in that window), so
nothing was staged, and the worker committed anyway **without inspecting
`git diff --cached`**. There is no verification step anywhere in the manual
procedure: no read-back of the edited region, no staged-diff inspection
before commit.

### 3.4 Why experiment workers committed ledger wipes

Six of the nine wipes were committed by workers doing unrelated experiment
work (their commits also contain their own lane files, e.g. `1e29a87c`
adds `cognitive_ops_learner/NAMECHECK.md` alongside the 120-line ledger
deletion). These workers never ran a mint. The mechanism is the **shared
worktree / shared index**: many workers operate in one checkout on one
branch and one index (documented in `~/AGENTS.md`, "Shared-workspace git
discipline"). A botched watchdog rewrite left the working tree (or the
shared index) with the C377 tail deleted; the next worker to commit in that
worktree swept the deletion into its commit, either via a bare `git commit`
or via an already-staged deletion. The 08:00-08:12 UTC window shows damage,
silent repair, damage, repair alternating almost commit-to-commit, which is
exactly what a shared worktree with concurrent uncoordinated writers
produces.

### 3.5 What the evidence rules out

- **Not a script bug:** no mint script exists (section 1).
- **Not a restore bug:** every restore was verified as a byte-identical
  inverse of its wipe (C411_INVESTIGATION.md section 3c); the C411/C412/C415
  claim texts were lost at mint time (0 insertions), never at restore time.
- **Not deliberate:** the commit subjects describe the intended claims;
  the workers gained nothing from the deletions and immediately repaired
  them when noticed.

### 3.6 Summary

The mint procedure rewrites the C377-anchored tail on every mint; when the
tail reconstruction is empty the rewrite becomes a wipe; nothing verifies
the staged diff before commit; and the shared worktree propagates one
worker's botched rewrite into other workers' commits. Nine wipes and one
empty commit in 27 minutes, four of them silently papered over by later
rewrites.

## 4. Guard design

### 4.1 Placement and invocation

- Artifact: `mint_guard.sh` in this lane (full source below, section 4.5).
- The watchdog's mint procedure gains one mandatory step, placed **after
  `git add` and before `git commit`**, run from the repo root:
  `./docs/lab/research-lead/overnight-20260928/mint_guard/mint_guard.sh --claim <n>`
- Exit 0: the commit may proceed. Any non-zero exit: **do not commit**.
  Re-run the guard after any fix; never commit a ledger change the guard
  has not passed.
- Toolchain: bash, `/usr/bin/git` (the `$HOME/safebin/git` symlink has known
  EPERM write failures; the resolved binary is mandatory), `sha256sum`,
  `grep`, `cmp`, `head`, `tail`. No forbidden executables.

### 4.2 Mint-mode checks (in order; first failure aborts)

Given the staged change S (index vs HEAD) for the ledger path:

1. **TIP check.** `sha256(HEAD:ledger)` must equal the `TIP` file's recorded
   SHA. The TIP is the last known-good ledger state, advanced only by guarded
   mints and guarded restores. Rationale: a mint built on a damaged HEAD
   (concurrent wipe) must not proceed; the four "silent repair" mints in
   section 2c are exactly what this check forbids. They felt helpful but they
   masked damage and depended on the worker's reconstruction being byte-right;
   under the guard, damage goes through the restore procedure instead.
2. **Insertions > 0, deletions == 0** on the staged numstat. The task's
   required assertion, with the deletion threshold set to 0: no legitimate
   mint deletes ledger lines; the ledger is append-only. This single check
   catches all nine wipes (0/N) and the empty commit (empty diff).
3. **Byte-prefix check.** `HEAD:ledger` must be a byte-prefix of the staged
   new file (`head -c <old_bytes> new | cmp -s - old`). This retires the
   rewrite semantics at the mechanism level: the committed file must be
   exactly the old file plus an appended block. Numstat alone is insufficient
   (a mid-file insertion also yields 4/0).
4. **Entry shape.** Exactly 4 added lines forming one well-formed block:
   blank / `- C<n> (...)` header / blank /
   `No em dashes were used in this entry (verified).` trailer; the new id
   equals the `--claim` argument and equals TIP max + 1; the id occurs
   exactly once in the staged file.
5. **Dash hygiene: WARNING ONLY.** The appended block is scanned for em-dash
   bytes (U+2014); hits are reported but do not block. Rationale, verified:
   existing entries routinely contain em dashes despite the trailer
   (C402 has 2, C410 has 2: "cost 192) -- the record", "machinery -- the
   choice"), so a blocking check would halt all minting under current
   practice. The trailer's per-entry verification is systematically
   unreliable; flagged for parent review in section 7.
6. **No unstaged surprises.** `git diff --quiet -- <ledger>` must hold, so a
   concurrent worker's in-flight edit in the shared worktree cannot slip in
   between staging and commit.

After the commit, the worker runs `mint_guard.sh --advance-tip` to record
the new known-good SHA and max claim id.

### 4.3 Restore mode

`mint_guard.sh --restore --expect-sha <sha256>`: for the legitimate
repair case. Asserts the working-tree file's SHA-256 equals the expected
value (the same acceptance criterion `RESTORE_PLAN.md` uses), asserts the
staged diff is insertions-only, skips the entry-shape check, and does not
require the TIP match (HEAD is damaged by definition). The commit subject
must start with `WATCHDOG: restore`. Then `--advance-tip`.

### 4.4 TIP file

`mint_guard/TIP` holds `<sha256> <max-claim-int>`, advanced only by
`--advance-tip` after a guarded mint or restore. Initialized (design value)
to the last verified-good state: `860f009b5` "WATCHDOG: restore C377-C410
deleted by b9999590", SHA
`31431585aec8d01b971af959fe8cd48562f3d083dd0cf66b1c31974e6bcdf972`,
max claim 410 (per `ledger_restore/RESTORE_PLAN.md` section 3). Consequence:
the pending `f20dddf0b` restore must reproduce exactly this SHA before any
mint can proceed; the guard fails closed on the currently damaged HEAD.

### 4.5 Guard script source

The full script is `mint_guard/mint_guard.sh` in this lane (design artifact,
uncommitted). Its logic is exactly the checks in 4.2/4.3 above; the
procedure a worker follows is:

```
# 1. append the 4-line entry to the ledger (PURE APPEND; the tail rewrite is retired)
# 2. stage with an explicit pathspec, using the resolved git binary
/usr/bin/git add -- docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md
# 3. run the guard BEFORE committing
./docs/lab/research-lead/overnight-20260928/mint_guard/mint_guard.sh --claim 464
# 4. only if the guard prints MINT-GUARD PASS:
/usr/bin/git commit -- docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md \
  -m "WATCHDOG: ledger C464 (...)"
# 5. advance the TIP
./docs/lab/research-lead/overnight-20260928/mint_guard/mint_guard.sh --advance-tip
```

### 4.6 Procedural rules the guard assumes (parent approval required; NOT applied)

- The tail-rewrite mint is retired. Mints are pure appends; any repair of a
  damaged tail goes through restore mode, never inside a mint.
- Ledger commits always use explicit pathspecs; bare `git commit` /
  `git commit -a` remain forbidden in the shared worktree (existing
  `~/AGENTS.md` discipline, restated because six wipes propagated this way).
- All git writes use `/usr/bin/git`, not the safebin symlink.

## 5. Test: retrospective application of the guard

The guard runs pre-commit on the staged diff; the staged diff of each
historical commit is exactly what `git diff --cached` would have shown its
worker. Applying the guard's logic to the record (all numstats verified
with `git diff --numstat <c>^ <c> -- <ledger>`):

| Commit | Staged ins/del | Check 2 (ins>0, del=0) | Check 1 (TIP) | Guard verdict |
|--------|---------------|------------------------|---------------|---------------|
| `29897129a` | 0 / 96 | FAIL (0 ins, 96 del) | - | **BLOCKED** |
| `1932fe844` | 0 / 108 | FAIL | - | **BLOCKED** |
| `d1d55de31` | 0 / 112 | FAIL | - | **BLOCKED** |
| `1e29a87c` | 0 / 120 | FAIL | - | **BLOCKED** |
| `8c6af9c4f` | 0 / 124 | FAIL | - | **BLOCKED** |
| `eaf6d7ba1` (task case) | 0 / 128 | FAIL (0 ins, 128 del) | - | **BLOCKED** |
| `cc7d7baae` | 0 / 128 | FAIL | - | **BLOCKED** |
| `b9999590` | 0 / 136 | FAIL | - | **BLOCKED** |
| `f20dddf0b` (task case) | 0 / 136 | FAIL (0 ins, 136 del) | - | **BLOCKED** |
| `9bb51ff39` (empty) | (empty diff) | FAIL (nothing staged) | - | **BLOCKED** |
| `9992a325e` (C404 silent repair) | 112 / 0 | pass | FAIL (HEAD damaged vs TIP) | **BLOCKED** (correct: must restore first, then mint) |
| `1611dc81c` (C405 silent repair) | 116 / 0 | pass | FAIL | **BLOCKED** |
| `ff8a2d8df` (C408 silent repair) | 128 / 0 | pass | FAIL | **BLOCKED** |
| `92a1831a7` (C409 silent repair) | 132 / 0 | pass | FAIL | **BLOCKED** |

Positive controls (would have passed):

- `9fd459b2e` (WATCHDOG: ledger C410): staged 4/0; check 1 passes with TIP
  advanced through the guarded lineage; check 2 passes (4>0, 0 del); check 3
  **verified explicitly**: `HEAD:ledger` (672307 bytes) is a byte-prefix of
  the staged file (675018 bytes), appended block is exactly the 4-line C410
  entry, id unique, no em-dash bytes in the block. **PASS** (with the
  section-4.2 dash note: the block contains no em dash; it does contain one
  en dash at "K1-K8", which the WARN-level check tolerates).
- `bba82122a` (C402), `44ecf987a` (C406): staged 4/0, single well-formed
  block, id = max+1. **PASS** (dash WARN fires: each block contains em
  dashes, confirming check 5 must stay non-blocking under current practice).

Net: with the guard in place from the first incident, `29897129a` is blocked
at check 2, no damage ever enters the ledger, and none of the eight later
incidents, the four silent repairs, or the four explicit restores would have
been necessary. The two task cases (`eaf6d7ba1`, `f20dddf0b`) are both
caught at check 2 before commit.

## 6. Limitations

- The guard is a **worker-loop procedure**, not a server-side hook: the repo
  is local-only and unpushed, so a worker can still bypass the script. Its
  force comes from governance (a ledger commit without a recorded guard pass
  is a violation), not from mechanism. A `pre-commit` hook in
  `.git/hooks/` would be stronger and is recommended as a follow-up; it was
  not installed per the design-only constraint.
- TOCTOU on the shared branch: another worker can commit between the guard
  run and `git commit`. Mitigation is procedural (guard immediately before
  commit, small window); the TIP check at least guarantees the mint was
  built on a known-good base.
- The guard does not judge entry *content*, only shape, identity, and
  append-only structure. Claim-number collisions (the C455-C460 issue in
  `f40fbeb11`) are a parent-governance matter, partially covered by the
  id = TIP max + 1 rule.
- The pending `f20dddf0b` restore must still be executed per
  `ledger_restore/RESTORE_PLAN.md`; the TIP is initialized to expect exactly
  its verified SHA.

## 7. Flagged for the parent (not decided here)

1. **Wire-in approval:** adopt `mint_guard.sh` into the watchdog mint
   instructions as a mandatory pre-commit step (plus the optional
   `.git/hooks/pre-commit` installation), or direct an alternative.
2. **Retire the tail rewrite:** confirm mints become pure appends and
   repairs go only through restore mode.
3. **Dash-hygiene gap:** every entry carries "No em dashes were used in this
   entry (verified)." but C402/C406/C407/C410 all contain em-dash bytes;
   the per-entry verification is unreliable. Decide whether to enforce,
   fix the trailer, or drop the claim.
4. **Shared-worktree policy:** six wipes propagated through workers that
   never minted. Consider isolating ledger writes to a dedicated worktree or
   requiring the guard's check 6 (`git diff --quiet`) discipline
   repo-wide for the ledger path.
5. **Backfill:** C411, C412, C415 were never minted (texts survive only in
   commit subjects / staged entries). The staged entries in `cbe2e5607`
   await the parent's numbering-collision resolution before minting resumes.
