# LEDGER EVIDENCE AUDIT - canonical_ledger/CLAIM_LEDGER.md (C1-C410)

**Lane:** `lane/recovery`. Read-only with respect to the ledger; no ledger byte was
written. Machine output: `evidence_audit.tsv` (393 rows).

## Question

For every claim ID in the canonical ledger, does the cited source lane actually exist
at the cited commit?

## What "canonical" means here

The ledger contains **393 claim blocks**, not 410. Blocks are detected in the two
shapes the file actually uses: `## C<digits>.` and `- C<digits> (`. The 17 IDs
C143-C159 are **not** headers: C143-C149 survive only as appendix sub-bullets inside
another claim's block, and C150-C159 are absent. The ledger discloses this
("commit dd704acd8 proposed C143-C152 for earlier completed work but was never
appended to this canonical ledger"). All 393 blocks are audited below.

`ledger_write/STAGED_LEDGER_ENTRIES.md` holds 49 staged entries (C411-C416, C418-C460;
C417 absent). These are **staging text, not canonical claims**, and are excluded.

## Method

Three stages, each auditable:

1. **`ledger_cites.zag` (pure Zag).** Reads the 675,018-byte ledger. Detects claim
   blocks in both shapes. For each block emits: every maximal hex run with
   `8 <= len <= 10` (`H<hex>:<len>`), the two explicit lane grammars, and - the
   addition this lane made - **every known lane basename mentioned anywhere in the block
   prose** (`L<name>:<athead>`), matched against a 1,116-entry lane index. Scanning the
   block prose rather than a token summary is required: the first build of this audit
   scanned the token summary and found 0 lane mentions, because the summary does not
   contain the prose.
2. **`git cat-file --batch-check` + `git rev-parse --verify` (plumbing).** Resolves
   each distinct abbreviation to `commit` or `missing`. The resolution path was
   sanity-checked against known-good abbreviations before use. Output: `sha_res.tsv`.
3. **`evidence_join.zag` (pure Zag).** Joins per claim: citation count, resolved count,
   absent count, lanes named, lanes gone. Assigns one verdict per claim by a fixed
   severity ladder.

Both programs were built with `--target macos-arm64` and run under `tnnwatch.sh`
(600 s limits). No forbidden interpreter was invoked.

## Definitions

- **SHA-UNRESOLVABLE** - at least one cited abbreviated commit id is absent from the
  object database. The claim's stated provenance cannot be checked.
- **LANE-GONE** - all cited shas resolve, but at least one named lane is absent at HEAD.
  **Recoverable**: the lane is present at `4e7eb30b1`.
- **NO-CITATION** - the block names no abbreviation and no known lane.
- **EVIDENCE-INTACT** - every cited abbreviation resolves and every named lane is at HEAD.

Ladder precedence: SHA-UNRESOLVABLE > LANE-GONE > NO-CITATION > EVIDENCE-INTACT.

## Results

| Verdict | Claims | Share |
|---|---|---|
| EVIDENCE-INTACT | 163 | 41.5% |
| LANE-GONE (recoverable) | 116 | 29.5% |
| SHA-UNRESOLVABLE | 113 | 28.8% |
| NO-CITATION | 1 | 0.3% |
| **Total** | **393** | |

**Union degraded: 228 of 393 (58.0%).** 81 claims are degraded on both axes.

Aggregate citation counts:

| Quantity | Value |
|---|---|
| Distinct hex tokens cited | 963 |
| - abbreviated commit ids (len 8/9/10) | 887 (92 / 793 / 2) |
| - sha256 file digests (len 64) | 64 |
| - full 40-char shas | 3 |
| - other tokens (len 12-51) | 9 |
| Abbreviations resolving to a commit | 635 |
| **Abbreviations ABSENT from the object DB** | **252** |
| Abbreviated-commit citation instances in blocks | 1,177 |
| **Citation instances unresolvable** | **446** |
| Lane mentions in blocks | 310 |
| **Mentions naming a lane absent at HEAD** | **301** |

### The single NO-CITATION claim

**C373** (`XP-HIER-3`) reads: *"PREREG.md frozen (sha256 ...) but FLAWED, no commits
made"* and returns `VOID - prereg design flaw`. This is an **honest self-declared
absence, not a gap.** It is the one claim in the ledger that correctly records that it
has no committed evidence. The audit flagging it is the audit working, not a defect.

### Worst offenders by unresolvable citation count

| Claim | absent | lanes gone |
|---|---|---|
| C384 | 13 | 1 |
| C360 | 12 | 1 |
| C353 | 11 | 2 |
| C409 | 10 | 0 |
| C395 | 9 | 1 |
| C357, C362, C366, C372, C378, C386, C403, C405, C408 | 8 each | 0-1 |

### The CALR / L3-NIV2 family (14 claims, not 5)

| Claim | shas cited | resolve | absent | lanes named | lanes gone | verdict |
|---|---|---|---|---|---|---|
| C294 | 1 | 1 | 0 | 0 | 0 | EVIDENCE-INTACT |
| C312 | 1 | 1 | 0 | 1 | 1 | LANE-GONE |
| C324 | 2 | 1 | 1 | 1 | 1 | SHA-UNRESOLVABLE |
| C334 | 3 | 2 | 1 | 1 | 1 | SHA-UNRESOLVABLE |
| C348 | 5 | 2 | 3 | 1 | 1 | SHA-UNRESOLVABLE |
| C350 | 4 | 4 | 0 | 2 | 2 | LANE-GONE |
| C358 | 8 | 1 | 7 | 2 | 2 | SHA-UNRESOLVABLE |
| C364 | 5 | **0** | 5 | 2 | 2 | SHA-UNRESOLVABLE |
| C367 | 7 | 2 | 5 | 0 | 0 | SHA-UNRESOLVABLE |
| C368 | 5 | **0** | 5 | 1 | 1 | SHA-UNRESOLVABLE |
| C378 | 8 | **0** | 8 | 1 | 1 | SHA-UNRESOLVABLE |
| C383 | 7 | **0** | 7 | 0 | 0 | SHA-UNRESOLVABLE |
| C391 | 6 | **0** | 6 | 0 | 0 | SHA-UNRESOLVABLE |
| C401 | 3 | **0** | 3 | 1 | 1 | SHA-UNRESOLVABLE |
| **TOTAL** | **65** | **13** | **52** | | | |

**80% of the CALR family's cited commits do not exist.** Six claims (C364, C368, C378,
C383, C391, C401) have **zero** resolvable citations, and their source lanes have zero
commits anywhere in the repository. Their BUILD-PASS / INTEGRATED-BUILD-PASS /
INSTRUMENT-DISCRIMINATES-A verdicts are **not citable**.

### Claims citing commits that do not exist

113 claims, led by the table above. The mechanism is uniform: "local only, never
pushed" commits made in external worktrees under `~/workspace/` on branches that no
longer exist as refs. Confirmed absent: `lane-compinteg2-20261002`,
`lane-l3niv2w5-20261002`, `lane-hcontlife5-20261002`, `lane-jointblind-20261003`.
`~/workspace` does not exist on this host.

### Claims whose cited lane is absent at HEAD

116 claims, 301 lane mentions. **All recoverable** from `4e7eb30b1`. This is the
quantified form of the false negative that produced the CALR "no source" error: the
lanes are not absent from the repository, only from the current working tree.

## Limits of this audit

1. This establishes **citation resolvability**, not claim truth. Nothing here verifies a
   digest, a determinism claim, or a PASS/FAIL bar.
2. The 64 sha256 file digests were **not** checked against file content.
3. "Named lane" detection is substring matching of 1,116 known lane basenames against
   block prose. A lane referenced only by an unlisted name would not be detected; a
   coincidental substring match would inflate the lane count. The five claims with
   `lanes=0` that nonetheless describe lane work (C367, C383, C391) are cases where the
   lane basename never appears literally in the entry.
4. `SHA-UNRESOLVABLE` is evidence about **this repository**. It does not establish that
   the commit never existed; it establishes that it is not here now and is not
   recoverable by any git mechanism available on this host.