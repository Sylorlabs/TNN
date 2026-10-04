# LANE-RESTORE REPORT

**Lane:** `lane/restores`. **Worktree:** `/Users/Shared/micah/Documents/TNN/.worktrees/restores`.
**Base:** `87a822426`. **Date:** 2026-10-04. **Runs pushed to `origin/lane/restores`.**

Executes the recovery items proposed by `lane/recovery` (`9b2c4db6e`). Every change
is a commit that only ADDS. `canonical_ledger/CLAIM_LEDGER.md` was not modified.
No force-push, no amend, no rebase, no `git commit -a`.

## Commits

| sha | item | what |
|---|---|---|
| `e963a9b31` | **P0** | 33 unreachable commits re-referenced under `refs/recovered/` |
| `9d5c7f940` | **P3** | 160,514 paths restored; 1,351 lanes back at tip |
| `f055b522c` / `a2309f7d9` | P2 evidence | live hook test: addition PASS; 999-path deletion PASS |
| `3da437601` / `a3bba46f9` | P2 evidence | reverts of the two above; tree restored bit-identical |
| `07708b5822` | **P1 + P2** | citation-repair negative result; tripwire installed |

Order was P0 first, not P3. P0 is the only item whose loss is irreversible and
`git gc` is not under this lane's control.

## RESULTS

### P0 - 33 unreachable commits: ALL RECOVERED

All 33 confirmed unreachable (`git for-each-ref --contains` empty for every one),
then re-referenced. `git fsck --unreachable --no-reflogs | grep -c 'unreachable
commit'`: **33 -> 0**. Original shas, authors, dates and messages unchanged.

**They rescue nothing.** 0 of the 252 dead ledger citations matches any of them.
Orphaned *work*, not orphaned *evidence*.

### P3 - restore: 160,514 paths, 1,351 lanes, ZERO deletions

```
files=160514  insertions=44,104,409  deletions=0
status letters: A x160514 only. Zero M, zero D, zero untracked.
HEAD tree unchanged until the commit.
```

Verified at tip: **858/858** of the audit's lanes present, **1,351/1,351** of the
re-derived set. Tracked paths 5,276 -> 165,793. The CALR engine tree is
byte-identical to `4e7eb30b1` (`2a47a61abc9425d45d4dd9e910b09befbb0f6728`).

**Correction to the audit:** it counted 1,108 lanes / 858 missing. Re-derived from
`git ls-tree -r -t`: **1,601 lanes / 1,351 missing**. Its 858 are a strict subset;
493 further lane directories were missing and uncounted. The restore covered the
superset, and the superset was necessary: restoring only the 858 would have left
~106,000 non-lane paths (`src/`, `.github/`, `archive/`, `docs/lab/rsi`,
`docs/generations/R33`) invisible and the false-negative mechanism live.

### P1 - citation repair: DEFINITIVE NEGATIVE, nothing applied

Three exhaustive rules against all 6,742 commits: truncation 0/161, Hamming<=1
**0/252**, substring 0/252. All 252 absent as commit, blob, tree and tag. No second
repository on this host. A positive control proves the detector fires on exact hits
and on single-char errors mid-string and last-position. Determinism 3/3.

**There is no remapping table.** The 252 name commits never pushed and never
committed here. Applying a "repair" would mean redirecting citations to nearby
commits, which fabricates provenance. I did not do that.

One bug of my own, caught and fixed: the first run tested 249 of 252 because the
last input line has no trailing newline to bound it. `cites_no_candidate` was
printed but never compared against `cites_indexed`. The program now emits
`cites_skipped_bad_length` separately.

### P2 - tripwire: INSTALLED, AND IT BLOCKS

Installed at `<git-common-dir>/hooks/pre-commit`, so it covers all 25 worktrees
including those whose HEAD predates it. Fails CLOSED. Threshold 1000 **paths**;
renames count as deletions; the count is computed in pure Zag.

| Test | Result |
|---|---|
| `b3b3ee00a` (160,515) retrospective | **REFUSED** |
| `c721bcc61` (160,361) retrospective | **REFUSED** |
| `f461e812d` (147,296) retrospective | **REFUSED** |
| `169894404` (165,250) retrospective | **REFUSED** |
| `b688fa031`, `cef8c4095`, `84727be29`, `3c25ff8f1`, `7e4d7cffe` | **ACCEPTED**, 0 deletions each |
| live 1,501-path deletion | **REFUSED**, no commit produced |
| live 999-path deletion | ACCEPTED - not a blanket ban |
| additions only | ACCEPTED |

### P5 item - proposals

`PROPOSALS.md`, C650-C659, nothing minted. Ledger untouched. Records the CALR
downgrade **extended from the audit's 5 claims to all 14**, the UNVERIFIED
downgrade, the wipe entry with corrected figures, the standing no-tip-based-
existence-claim rule, the rejection of the citation-rewrite proposal, and the
tripwire registration.

## GENUINELY LOST - no recovery path

| Item | Evidence |
|---|---|
| 8 CALR lanes: waves 5-9, 2scalr, poolrepair, genrec | **0 commits across all refs, 0 files at tip**, re-checked *after* the restore |
| C350 red-team implementation | lane has 7 commits but only **2 files** survive (PREREG.md, NAMECHECK.md); impl, REPORT.md, `attacks/`, 12 run logs |
| 252 ledger-cited commits | 0 resolvable, 0 near-miss, 0 in any other repo on this host |

## BOUNDARIES

- 6.61 GiB of blobs were checked out. Compiled binaries in the restored set were
  restored as-is; nothing was rebuilt, regenerated or re-derived.
- `refs/recovered/*` **could not be pushed**: origin rejects 2 of the 33 for
  >100 MB files and all 33 for `workflow` OAuth scope. Local refs fully answer the
  stated threat (`git gc --prune`); a gc-independent off-repo bundle for the 31
  non-oversized commits is at
  `/Users/Shared/micah/Documents/TNN/.recovery/unreachable31.bundle`,
  sha256 `675825666275ffe08669f4b78ed5c9f6fec5f88172b7d27b9b71a577d5ff1af9`,
  `git bundle verify` = complete history. The 2 oversized commits are protected by
  local refs only.
- 255 blobs and 252 unreachable trees were NOT re-referenced. No ledger citation
  names one.
- The 64 sha256 file digests cited in the ledger were not checked.
- `13c557cd3` (182,300 deletions) is a deliberate path normalisation, not a wipe.
  A count-only rule flags it; that is why the threshold ships with an explicit
  `--no-verify` bypass rather than being treated as proof of an incident.
- No experiment was run. No digest re-verified. No audited mechanism re-executed.

## NEXT EXPERIMENT

Recompute the 393-claim evidence audit against a tip that carries the corpus. The
116 LANE-GONE verdicts should retire, and that pass is the real check on this
lane's central claim - that a tip-based existence query can no longer return a
false negative at this scale. It is bookkeeping, not science, and it is the
cheapest available falsification test of the restore.

Second: a sha256 file-digest pass over the 64 digests the ledger cites, which is
the one evidence axis still unmeasured.

## Provenance

Orchestration by `git` plumbing. Two pure-Zag programs, `cite_remap.zag` and
`mass_delete_guard.zag`, compiled `--target macos-arm64`, all runs behind
`tnnwatch.sh` at 600 s. `tnn_pure_zag_report` = `PURE-ZAG-CLEAN`.
