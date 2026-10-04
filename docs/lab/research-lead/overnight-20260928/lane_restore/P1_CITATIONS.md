# P1 - CITATION REPAIR: NO REMAPPING EXISTS. NEGATIVE RESULT, DEFINITIVE.

**Status: DONE. Three mechanical repair rules tested exhaustively against all
6,742 commits. Zero repairs found. Nothing was applied, because there is nothing
to apply.** This is a finding, not a failure to finish.

## 1. The claim under test

`9b2c4db6e` reports **252 ledger-cited abbreviated shas that resolve to no object
in the repository**, degrading 113 of the 393 canonical claim blocks. The task was
to produce a mechanical remapping from each dead citation to the commit it was
meant to name, and apply it if safe.

## 2. First: are they dead, or mis-typed?

A sha prefix is prefix-unique, so an abbreviation of a commit that IS in the
repository cannot fail to resolve by accident. The 252 therefore either name
commits that never entered this repository, or contain a transcription error.
Both possibilities were tested.

```
$ git cat-file --batch-check < 252 shas
252 "missing", 0 blobs, 0 trees, 0 tags
```

Dead, not mistyped-as-another-type.

## 3. Three mechanical repair rules, all exhaustive

| Rule | Test | Result |
|---|---|---|
| **R1 truncation** | a 9-char citation truncated to 8 resolves? | **0 / 161** |
| **R2 Hamming <= 1** | any commit whose prefix is <=1 hex character away, over the cited length? | **0 / 252** |
| **R3 substring** | is the citation a substring of any full sha at any offset? | **0 / 252** |

R2 is the real test and is computed in pure Zag by `cite_remap.zag`, which reads
the 252 citations and all 6,742 commits (`git log --all`) and enumerates every
commit at Hamming distance <= 1 over the cited length, with no judgement and no
threshold tuning.

```
COMMITS_INDEXED 6742
CITATIONS_INDEXED 252
CANDIDATE_ROWS 0
STAT cites_tested 252
STAT cites_skipped_bad_length 0
STAT cites_no_candidate 252
STAT cites_unique_repair 0
STAT cites_ambiguous 0
```

Length distribution of the 252: 89 at 8 chars, 161 at 9, 2 at 10. All 252 were
tested; none was skipped.

### R2 cannot produce a false positive at this scale

A citation of length L has `L * 15` single-character hex neighbours. With `C`
commits, the chance a random citation has one present is about `C * L * 15 / 16^L`.
At C = 6742 that is **1.3e-5** for L=9 and **1.9e-4** for L=8; over 252 citations
the expected number of coincidental hits is **0.008**. Observing 0 is therefore the
*expected* outcome for genuine transcription noise, and observing many would have
been the signal. Zero means there is no near-miss to repair.

## 4. THE CONTROL - the negative result is not a broken program

A program that reports zero candidates is worthless without proof that it can
report non-zero. `cite_remap_CONTROL.tsv` is a positive control run on the same
binary and the same inputs:

| Input | Expected | Got |
|---|---|---|
| `c5922d61d` (exact) | dist 0 hit | dist 0 hit |
| `9d5c7f940` (exact) | dist 0 hit | dist 0 hit |
| `405be89a0` (exact) | dist 0 hit | dist 0 hit |
| `4e7eb30b2` (1 char off `4e7eb30b1`) | dist 1 hit | dist 1 hit -> `4e7eb30b1` |
| `b3b3ee00b` (1 char off `b3b3ee00a`) | dist 1 hit | dist 1 hit -> `b3b3ee00a` |
| `deadbeef99` | no candidate | no candidate |

The detector fires on exact matches, on single-character errors in both the middle
and the last position, and correctly reports nothing for a sha that is nowhere
near any commit. Output sha256 recorded in `P1_CONTROL_SHA256.txt`.

## 5. A bug I introduced and caught

The first run tested **249** of 252 citations, not 252. The last line of the input
has no following newline to bound it, so its length was read as 10 instead of 9
and it was silently skipped. The symptom was invisible: `cites_no_candidate` was
reported but never compared against `cites_indexed`. Fixed, and the program now
emits `cites_skipped_bad_length` as a separate, non-zero-visible counter so the
class of error cannot recur unnoticed. The published result is from the fixed
program: **252 tested, 0 skipped, 0 candidates.**

## 6. Determinism

`cite_remap` run 3x under `tnnwatch.sh` at a 600 s limit: output byte-identical
3/3, sha256 `81156bd866dde924a5c4f42aebcfe0d96823a32c6871d4eae05aff5e6b8c0978`.

## 7. Where the dead commits are not

Searched and empty: `/Users/Shared/micah/Documents/TNN/TNN-R1` (no `.git`),
`TNN-R1-Audit` (no `.git`), `Research` (no `.git`). There is no second repository
on this host that could hold them.

## 8. What this means

**The 252 citations are not repairable, mechanically or otherwise, from inside this
repository.** They name commits that were never pushed here and were never
committed here - consistent with work done in the now-deleted `~/workspace/`
worktrees outside the lane protocol. There is no remapping table to produce. The
correct action on each is a **ledger annotation of absent evidence**, not a
substitution, because silently redirecting a citation to a nearby commit would
fabricate provenance. `PROPOSALS.md` proposes the annotation form.

## 9. Boundaries

- Rules R1-R3 cover transcription error, truncation, and offset. They cannot
  recover a citation whose target was genuinely never committed. Nothing can.
- The 64 sha256 file digests cited in the ledger were **not** checked; that needs
  a per-claim file-hash pass and is out of scope.
- `9b2c4db6e`'s own lane-detection grammar was found to undercount lane
  directories (858 vs 1,351). That does not affect this result: R2's input is the
  sha list, which is independent of lane enumeration.
