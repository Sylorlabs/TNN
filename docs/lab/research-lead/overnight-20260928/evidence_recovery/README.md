# EVIDENCE-RECOVERY LANE - README

Lane `lane/recovery`. Worktree `/Users/Shared/micah/Documents/TNN/.worktrees/recovery`.
Purpose: audit the integrity of the scientific record after the `b3b3ee00a` whole-tree
wipe, recover what is recoverable, and grade the ledger's evidence.

**This lane ran no experiment.** All computation is `git` plumbing (orchestration) plus
two pure-Zag programs. All program runs went through `tnnwatch.sh` with 600 s limits.
`canonical_ledger/CLAIM_LEDGER.md` was **not modified**.

## Read these

| File | What it is |
|---|---|
| `RECOVERY_REPORT.md` | Main findings: wipe characterisation, lost-vs-recoverable, CALR recovery, other gaps |
| `LEDGER_EVIDENCE_AUDIT.md` | Method + results for the 393-claim evidence audit |
| `C640_PROPOSALS.md` | Proposals C640-C649. **Nothing minted.** Ledger untouched |
| `RECOVERY_MANIFEST.txt` | sha256 of every recovered file + blob SHA1 of the 17.1 MB not duplicated |

## Programs (pure Zag)

| File | Role |
|---|---|
| `ledger_cites.zag` | Reads the 675 KB ledger; emits per claim: abbreviated-commit tokens, lane-grammar tokens, and known-lane mentions scanned against block prose |
| `evidence_join.zag` | Joins per-claim citations against `sha_res.tsv` and `all_lanes.tsv`; assigns one verdict per claim |

Inputs (produced by plumbing, consumed by Zag):
- `cites2.tsv` - extractor output
- `sha_res.tsv` - `<short-prefix>` TAB `OK|ABSENT`, from `git cat-file --batch-check`
- `all_lanes.tsv` - `<lane-basename>` TAB `1|0`, `1` = present at HEAD

Output: `evidence_audit.tsv`, 393 rows.

## Reproduce

```sh
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
tnn_pure_zag_report                       # must print VERDICT: PURE-ZAG-CLEAN
D=docs/lab/research-lead/overnight-20260928/evidence_recovery
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
/Users/Shared/micah/Documents/TNN/.bin/znc --target macos-arm64 \
  --no-zagd --no-analyze --no-foreground-cache $D/ledger_cites.zag
/Users/Shared/micah/Documents/TNN/.bin/znc --target macos-arm64 \
  --no-zagd --no-analyze --no-foreground-cache $D/evidence_join.zag
$W reg cites 600 ./$D/ledger_cites
$W reg join  600 ./$D/evidence_join
```

Compiled binaries are build artifacts and are deliberately **not** committed, per the
lane-hygiene precedent in `70175302b`.

## Determinism

Both programs were run 3x. stdout 3/3 byte-identical
(`147158d6065537fda8250267cbdf8d5b43df98de59c3e5aba1de636f7c93c789`);
`evidence_audit.tsv` 3/3 byte-identical
(`6e4ae6b035d6f62af57784cd2294abc0a8bfb08014439a6335afccfcec4a9b91`).

## Headline numbers

- `b3b3ee00a`: 160,517 paths, 234 insertions, 44,104,446 deletions. **Zero content lost** -
  160,515/160,515 deleted paths are in its parent `4e7eb30b1`, which is on origin.
- Real damage: 165,288 -> 5,276 tracked paths at HEAD; **858 of 1,108 research lanes
  absent from every current tip.** All recoverable from `4e7eb30b1`.
- CALR `isa.zag:5-11`: alphabet is C281's **5 opcodes**, 80 forms, "ZERO new opcodes".
  **L1**, not L2+. Proposal P1.
- Ledger: 393 blocks; 228 (58%) degraded; **113 claims cite commits that do not exist**;
  8 CALR-family lanes were never committed at all.