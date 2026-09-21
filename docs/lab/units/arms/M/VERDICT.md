# ARM M — Counter IDs — VERDICT

## VERDICT: KILLED (scoped); M-dedup claim SURVIVES (corrected 2026-09-21)

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

   **Does NOT fire (corrected evaluation 2026-09-21):** M7 dedup_barred =
   50.01 (ratio 0.5001 ≥ 0.4 bar) with the dedup mechanism actually running.
   The prior 0.00 was measured with the dedup path compiled out
   (`if(false && ...)`), which cannot falsify the claim — that evaluation
   was INVALID, not a kill. See "M-dedup correction" below.

## M-dedup correction (2026-09-21)

The 372252de02 verdict reported M7 dedup 0.00 and killed the M-dedup claim.
That measurement was taken with the dedup mechanism disabled in source
(`if(false && dedup==1)`), so the 0.00 tested pure issuance, not dedup.
A 0.00 from disabled code does not falsify the claim; the honest status
was BLOCKED.

Root cause found on re-investigation: the "znc multi-parameter corruption"
diagnosis was wrong. The hash table was keyed by buffer OFFSET
(`(bo+off) % HT_SIZE`), not by content — byte-identical chunks at different
offsets probed different chains and never met, so only same-offset
re-ingests (round 2) deduped. No compiler bug: the table mechanics were
proven sound in isolation (84,731 inserts + lookups, no panic), and the
plain i32 `&` operator was verified correct on this znc build (including
negative hashes). The fix keys the probe chain by the chunk's CONTENT hash
(`h & ht_mask`); exact byte-equality still decides, minimum id still wins
(== ID-ascending first match of the specified linear scan).

Validation: a 2,000-unit synthetic corpus with hand-computed expectations
(period-256 repeats + planted duplicates) produced exactly the predicted
ratios (barred 93.60, round-3 95.40), proving the mechanism implements the
specified scan. Full-protocol double run, byte-identical stdout:
`M7,counter-id,hit,100.0,reuse,3.02,dedup_barred,50.01,dedup_r3,66.34`.

Mechanical evaluation: 0.5001 ≥ 0.4 → the M-dedup claim SURVIVES. (The
barred metric's theoretical maximum over rounds 1–2 is 0.5; the extra
0.0001 is 17 within-round-1 duplicate 64-byte chunks in the prose corpus.)

## What survives

- **Store-local handle:** survives unconditionally per the frozen row.
  Counter IDs work perfectly as a within-store identity mechanism:
  M1 100.0/100.0 recall/boundary, 64/64 swaps detected, M3 CLEAR,
  M4 100.0 revision, M6 100.0 transfer, M8 byte-identical across perturbations.
- **M-dedup claim:** survives per the corrected M7 evaluation (dedup_barred
  50.01 ≥ 0.4 with the mechanism running). The hash-accelerated exact
  byte-equality scan over the last-W episodes works as specified: round 2
  fully deduped (84,714 ids for 84,731 units), round 3 minted only for the
  847/848 edited chunks. M7 reuse rose 1.01 → 3.02 (bar ≥1.5 now PASS).

## What died

- **Cross-store/global identity:** counter IDs cannot serve as a global
  identity across independently-issued stores. The remap table (148,678
  entries for store B) dominates merge compute at 39.14%. Any cross-store
  use requires explicit remapping with O(n) table cost.

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
| M7 reuse | 3.02 | — | ≥1.5 | PASS |
| M7 dedup (barred) | 50.01 | — | ≥0.4 | **PASS → claim survives** |
| M7 dedup (round 3) | 66.34 | — | — | informational |
| M8 recall/boundary | 100.0/100.0 | — | — | PASS |
| M8 image sha256 | d23b425c… | — | identical | PASS (5/5) |
| Merge dangling | 0 | — | 0 | PASS |
| Merge misdirected | 0 | — | 0 | PASS |
| Merge remap frac | 39.14% | — | ≤10% | **FAIL → scoped kill** |

Full JSON: `scorecard-1x.json`.

## 10x Status

**NOT ATTEMPTED.** The merge scoped kill fires at 1x (counter IDs die as
cross-store/global identity), so per the frozen rules 10x is not attempted.
(The M-dedup correction does not change this: the scoped kill is
independent of dedup.)

## Commit hashes

(No commits yet — pending.)

## Kill evidence

- Merge 1x stdout: `raw/merge-1x.stdout`
  - `MERGE,nA,84731,nB,148678,links,1487,dangling,0,misdirected,0,remap_frac_x10000,3914,kill,1`
  - `MERGE_VERDICT,SCOPED-KILL FIRES`
- M7 1x stdout (dedup ENABLED, corrected 2026-09-21): `raw/m7-1x.log`
  - `M7,counter-id,hit,100.0,reuse,3.02,dedup_barred,50.01,dedup_r3,66.34`
  - Double run, byte-identical stdout. Supersedes the 372252de02 M7 log,
    which was measured with the dedup path compiled out (`if(false && ...)`).

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
