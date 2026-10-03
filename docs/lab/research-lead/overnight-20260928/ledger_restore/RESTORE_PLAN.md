# RESTORE PLAN: C377-C410 deleted by f20dddf0b

**Worker:** LEDGER-RESTORE (analysis only; no modifications made)
**Date:** 2026-10-03
**Branch examined:** `tnn-native-lab`
**File:** `docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md`
**Toolchain note:** shell/git/grep only; no forbidden executables invoked.

## 1. Deletion verified

Commit `f20dddf0b8ee847749c8fae74ca7e302ec31db54`
("WATCHDOG: ledger C415 (META-GENERALIZE TRANSFER DEMONSTRATED...)",
2026-10-03 08:12:23 UTC) made exactly:

```
 docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md | 136 ----------
 1 file changed, 136 deletions(-)
```

136 deletions, **0 insertions**. The intended C415 entry was never written;
the commit only deleted.

## 2. Exactly what was deleted

34 ledger entries, **C377 through C410**, each a 4-line block:

```
(blank)
- Cnnn (<entry text, single physical line>)
(blank)
No em dashes were used in this entry (verified).
```

34 x 4 = 136 lines. Confirmed via diff header list; every deleted
entry header present exactly once.

Entry inventory (claim id | lane | verdict):

| C | Lane | Verdict |
|---|------|---------|
| C377 | XP-XXHIER-3 | XP-XXHIER-3-BOUND (cross-domain Z3 bound, depth-3 untested) |
| C378 | L3-NIV2-WAVE6 | HONEST NO-IMPROVEMENT (stage-3 never executes) |
| C379 | XP-HIER-TRANSFER | PASS (learned composites transfer across contexts) |
| C380 | XP-TRUNC-1 | XP-TRUNC-1-PASS (adaptive reuse by truncation) |
| C381 | IDX-PROBE | IDX-PROBE-PASS (indexed lookups, N=100, 30.5x user CPU) |
| C382 | XP-XDTRUNC-1 | XP-XDTRUNC-1-PASS (cross-domain truncation) |
| C383 | L3-NIV2-WAVE7 | YIELD-EXECUTION-PARTIAL (stage-3 executes, D5A unsolved) |
| C384 | XP-XXHIER-TRANSFER | XP-XXHIER-TRANSFER-PASS (cross-domain composite transfers) |
| C385 | H-CONTLIFE-5-DEEP7 | DEEP7-FAIL (crash; V7=20,851,022 measured) |
| C386 | WALL-N140 | WALL-REVISED (no wall at N=140) |
| C387 | XP-SUBST-1 | XP-SUBST-1-PASS |
| C388 | XP-ADAPT-1 | XP-ADAPT-1-BOUND |
| C389 | WALL-N141-160 | WALL-PINPOINTED-PASS (wall at exactly 144 MAPs) |
| C390 | XP-EXTEND-1 | XP-EXTEND-1-BOUND |
| C391 | L3-NIV2-WAVE8 | INSTRUMENT-DISCRIMINATES-A |
| C392 | XP-SPEC-1 | XP-SPEC-1-PASS |
| C393 | L2-INTERFERENCE | L2-INTERFERENCE-BOUND |
| C394 | L2-INTERFERENCE-D3 | L2-INTERFERENCE-D3-BOUND |
| C395 | XP-HIER-INVENT | BOUND |
| C396 | L2-INTERFERENCE-Q3 | L2-INTERFERENCE-Q3-BOUND |
| C397 | GPI-3 | L2+ not L3 (PARTIAL) |
| C398 | H-CONTLIFE-5-DEEP7-RC | DEEP7-RC-EXPLORATORY |
| C399 | H-INTVER-1 | BUILD-FAIL (K8 missed) |
| C400 | DOMAIN-BLINDNESS | DOMAIN-BLIND PASS |
| C401 | L3-NIV2-WAVE9 | COST-MEASURED-PRUNE-TESTED |
| C402 | MP-1 BELIEF REASONING | MP-1-PASS |
| C403 | NODE-BLINDNESS | NODE-BLIND PASS |
| C404 | MP-2 REGIME-CHANGE | MP-2-PASS |
| C405 | DEEP7-RC-CLEAN | DEEP7-RC-CONFIRMED |
| C406 | COGNITIVE-OPS-LEARNER | MIGRATION DEMONSTRATED |
| C407 | COMPAUDIT-1 | EXPANDING |
| C408 | MP-3 LEARNED MAGNITUDE | MP-3-PASS |
| C409 | JOINT-BLINDNESS | JOINT-BLIND PASS |
| C410 | COGNITIVE-OPS-COMPOSE | COMPOSITION DEMONSTRATED |

## 3. Restore source

`860f009b5` (2026-10-03, "WATCHDOG: restore C377-C410 deleted by b9999590").

Verified facts:
- `f20dddf0b`'s parent is exactly `860f009b5` (parent hash
  `860f009b5095f8fd4a45d8b1994fe905e3a97825`).
- The ledger file in `f20dddf0b^` is byte-identical to the ledger file in
  `860f009b5` (diff: empty).
- The deleted block is lines **7530-7665** of the `860f009b5` version
  (starts with a blank line, then `- C377 ...` at source line 7531,
  ends with `No em dashes were used in this entry (verified).` at source
  line 7665, the C410 trailer).
- SHA-256 of the full `860f009b5` ledger version:
  `31431585aec8d01b971af959fe8cd48562f3d083dd0cf66b1c31974e6bcdf972`

## 4. Current state on tnn-native-lab vs restore source

Current `tnn-native-lab` tip version of the file: 7529 lines, ends at the
C376 block (its trailing `No em dashes...` line). SHA-256:
`07c65224c71aa072f58b3d933f5018094e205c2ba354821059683b5a1480e113`.

Diff (current tip vs `860f009b5`):

```
7529a7530,7665
```

A single pure-addition hunk: append source lines 7530-7665 after current
line 7529. No other differences anywhere in the 7529-line common prefix.

## 5. Conflicts with subsequent commits

**None.** First-parent file history on `tnn-native-lab` shows `f20dddf0b`
as the newest commit touching `CLAIM_LEDGER.md`. Later tip commits
(`f40fbeb11` LEDGER-COLLISION-RESOLVE C463, `0f392ccf2` WORKSPACE-HYGIENE,
`9ead6569d` OPACITY-AMEND) do not touch the file. The restore is a clean
mechanical append with no merge content to reconcile.

## 6. Restoration procedure (for the parent to execute)

Preferred, on a `tnn-native-lab` checkout, using the resolved git binary
(`/usr/bin/git`; the `$HOME/safebin/git` symlink has known EPERM write
failures):

```
cd ~/workspace/tnn-rsi
git checkout tnn-native-lab
/usr/bin/git show 860f009b5:docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md \
  > docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md
sha256sum docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md
# must equal 31431585aec8d01b971af959fe8cd48562f3d083dd0cf66b1c31974e6bcdf972
```

This is exact because the only difference between the current tip file
and the `860f009b5` file is the 136-line deletion (proven by the single
`7529a7530,7665` diff hunk above). Alternative equivalent operation:
append source lines 7530-7665 to the current file, then verify the same
hash.

Commit with an explicit pathspec (shared-branch discipline), e.g.
"WATCHDOG: restore C377-C410 deleted by f20dddf0b (136 lines)".

## 7. Findings the parent should know (out of scope, flagged)

1. **The C415 entry was never written.** `f20dddf0b` has 0 insertions.
   If claim minting resumes, C415's META-GENERALIZE TRANSFER content exists
   only in the commit message, not in the ledger.
2. **C411 was also never written and is now permanently absent.**
   Commit `eaf6d7ba1` ("WATCHDOG: ledger C411", 2026-10-03) made 128
   deletions and 0 insertions; the follow-up restore `d238f75ca`
   restored to the pre-C411 state `ff8a2d8df`, dropping C411 entirely.
   Neither `860f009b5` nor the current tip contains a C411 entry.
   Its intended content (LIFETIME-META-2 META-LEARNING, B5a ADV_C=672>=350)
   survives only in the `eaf6d7ba1` commit message. This is a separate
   data-loss issue from the C377-C410 deletion and is NOT fixed by this
   restore plan.
3. **This is the fourth identical failure in the ledger's history:**
   `29897129a` (96 lines), `1e29a87c` (120 lines), `b9999590a` (136 lines),
   `f20dddf0b` (136 lines). Each time a watchdog or worker "ledger" commit
   deleted a C377-onward block instead of appending one entry. The first
   three were each repaired by a dedicated restore commit (`a481fbe82`,
   `07bb1cac2`, `860f009b5`). The recurrence suggests a tooling/editor bug
   in the append path worth investigating rather than repairing a fifth
   time.
4. **C455-C460 "occupied" claims (per the C463 collision-resolve commit
   `f40fbeb11`) do not exist in any committed ledger file.**
   `git log --all -S '- C455 '` found no commit introducing them.
   Minting state at C455+ needs reconciliation against wherever those
   entries actually live before the pause on claim minting is lifted.
5. Claim minting is paused per `f40fbeb11` (C463). This restore plan does
   not mint, renumber, or alter any entry; it only reinstates the deleted
   block.

## 8. Acceptance criteria for the restore

- Restored file SHA-256 ==
  `31431585aec8d01b971af959fe8cd48562f3d083dd0cf66b1c31974e6bcdf972`
- `grep -c '^- C[0-9]* '` returns the pre-deletion count and
  C377, C410 each appear exactly once
- Restore commit uses an explicit pathspec; no other files touched
