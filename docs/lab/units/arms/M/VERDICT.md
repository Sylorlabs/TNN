# ARM M — Counter IDs — VERDICT

## VERDICT: KILLED (scoped)

**Quoting the fired criteria:**

1. Scoped kill (frozen §3 row):
   > "KILL counter IDs as the cross-store/global identity if, in the two-TNN
   > merge trial, remapping produces ≥1 dangling/misdirected pointer OR remap
   > compute > 10% of total merge compute. (Survives unconditionally as the
   > store-local handle.)"

   **Fired:** remap compute = 39.14% of total merge compute (> 10% bar).
   Dangling = 0, misdirected = 0 (pointer integrity held).

2. M-dedup death (frozen §3 row):
   > "Separately: the M-dedup claim dies (revert to pure issuance) if M7
   > dedup ratio < 0.4 on the repetition protocol."

   **Fired:** M7 dedup_barred = 0.00 (< 0.4 bar).

## What survives

- **Store-local handle:** survives unconditionally per the frozen row.
  Counter IDs work perfectly as a within-store identity mechanism:
  M1 100.0/100.0 recall/boundary, 64/64 swaps detected, M3 CLEAR,
  M4 100.0 revision, M6 100.0 transfer, M8 byte-identical across perturbations.
- **Pure issuance:** the M-dedup claim dies, but the arm reverts to pure
  issuance (which is what the 1x evidence actually ran).

## What died

- **Cross-store/global identity:** counter IDs cannot serve as a global
  identity across independently-issued stores. The remap table (148,678
  entries for store B) dominates merge compute at 39.14%. Any cross-store
  use requires explicit remapping with O(n) table cost.
- **M-dedup claim:** the repetition-protocol dedup ratio was 0.00, failing
  the 0.4 bar. The hash-accelerated dedup scan is blocked by a znc compiler
  bug; the linear-scan fallback is too slow for the full corpus. The claim
  "M-dedup provides ≥0.4 dedup ratio" is dead. Pure issuance stands.

## 1x Scorecard (M1–M9)

| Metric | Prose | Code | Bar | Verdict |
|---|---|---|---|---|
| M1 recall | 100.0 | 100.0 | — | PASS |
| M1 boundary | 100.0 | 100.0 | — | PASS |
| M1 swap | 64/64 | 64/64 | 64 | PASS |
| M2 ETC T1 | 1 | 1 | — | — |
| M2 ETC T2 | 1 | 1 | — | — |
| M2 ETC T3 | 1 | — | — | — |
| M3 recall/boundary | 100.0/100.0 | — | — | CLEAR |
| M4 revision | 100.0 | 100.0 | — | PASS |
| M4 kill-substitution | 0.0 | 0.0 | — | PASS |
| M5 units | 84,731 | — | — | — |
| M5 slot bytes | 2,389,540 | — | — | — |
| M5 ledger bytes | 5,486,784 | — | — | — |
| M6 transfer | 100.0 | 100.0 | — | PASS |
| M6 tax | 0.0 | 0.0 | — | PASS |
| M7 hit rate | 100.0 | — | ≥90% | PASS |
| M7 reuse | 1.01 | — | ≥1.5 | FAIL |
| M7 dedup (barred) | 0.00 | — | ≥0.4 | **FAIL → claim dies** |
| M7 dedup (round 3) | 0.00 | — | — | informational |
| M8 recall/boundary | 100.0/100.0 | — | — | PASS |
| M8 image sha256 | d23b425c… | — | identical | PASS (5/5) |
| Merge dangling | 0 | — | 0 | PASS |
| Merge misdirected | 0 | — | 0 | PASS |
| Merge remap frac | 39.14% | — | ≤10% | **FAIL → scoped kill** |

Full JSON: `scorecard-1x.json`.

## 10x Status

**NOT ATTEMPTED.** The valid 1x gate does not permit 10x: the merge scoped
kill fires at 1x and the M-dedup claim dies at 1x. Per the task instructions,
10x runs only if the 1x gate permits.

## Commit hashes

(No commits yet — pending.)

## Kill evidence

- Merge 1x stdout: `raw/merge-1x.stdout`
  - `MERGE,nA,84731,nB,148678,links,1487,dangling,0,misdirected,0,remap_frac_x10000,3914,kill,1`
  - `MERGE_VERDICT,SCOPED-KILL FIRES`
- M7 1x stdout: `raw/m7-1x.stdout`
  - `M7,counter-id,hit,100.0,reuse,1.01,dedup_barred,0.00,dedup_r3,0.00`

## Ambiguities

1. **M4 revision semantics:** ALPHABET_M-R.md describes changed-byte revision
   minting a new ID plus supersedes link; METRICS.md M4 requires same ID plus
   revise/repair lineage. Implemented same-ID repair per METRICS.md (the
   scoring authority). If the frozen prereg specifies otherwise, this needs
   correction.
2. **Merge "remap compute":** No frozen definition found. Reported both:
   inclusive (table-build + pointer-rewrites) = 39.14% (fires kill);
   pointer-rewrites-only = 0.38% (does not fire). Verdict uses inclusive
   per the mechanism description (the table is the load-bearing cost).
3. **M8 artifact sufficiency:** Only digest files preserved (image sha256 +
   stdout). If M-34–M-36 require full store images, ledgers, or allocator
   traces, the artifacts are insufficient.
4. **A17 combined vs separate:** Whether M1/M3 should be combined (as run)
   or separate remains unfrozen.

## Coordinator corrections acknowledged

1. The original "Fixed-32B IDs" dispatch (≥90%/≥97%/99%-swap) was VOIDED;
   the uncommitted implementation was deleted.
2. The coordinator's memory-paraphrase of §3 was superseded by the verbatim
   row, byte-verified against `b0b9140c0eda`; `briefs/M.json` matches.
