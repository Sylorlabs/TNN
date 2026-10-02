# REVISE8_RESULT: H-REVISE8 (multi-slot rollback)

**Verdict: H-REVISE8 SURVIVES (117/117).** X-RV7-3 (multi-slot
interference) is closed at the mechanism level. Classification: bounded
L2+ revision with a firing-set contradiction protocol. Not L3.

## Lineage

- Prereg `PREREG_REVISE8.md` committed alone as `94d5d0c97` before any
  implementation edit, build, or run. Verified strict ancestor via
  `git merge-base --is-ancestor`. No amendments.
- `revise8.zag` = `revise7.zag` copied verbatim (cmp-verified) plus
  exactly the frozen R6 change set: header comment (R6 description),
  `vs3_firing_set`, `vs3_apply_skip_set`, rewritten
  `diagnose_rollback_check` (two branches), banner/verdict rename,
  Phase O (19 CHECKs). `vs3_apply`, `vs3_apply_skip`,
  `vs3_firing_slot`, `vs3_revise`, `diagnose_confirm_check`,
  `diagnose_corroborate_v6`, `diagnose_propose`, and all Phase A-N
  fixture code untouched.

## The repair (R6)

`diagnose_rollback_check` now iterates the skip-test over the full
firing set. Branch A: the most-recent firing member gets the exact old
single-slot test (store without it predicts the trusted label ->
PROVISIONAL rolls back returning 1, ACTIVE demotes returning 2).
Branch B: if Branch A did not fire, every firing member's own program is
run directly; if all mispredict the trusted label AND the store without
the whole firing set predicts it, the contradiction protocol applies to
every member: PROVISIONAL -> ROLLED_BACK, ACTIVE -> PROVISIONAL. Return
1 if any member rolled back, 2 if any demoted, else 0. If the uncovered
baseline also mispredicts, no action is taken (X-RV5-1 underdetermination
treatment preserved).

## Frozen kill-bar evidence

Raw: `REVISE8_RAW.txt` (md5 `631cd08786189b0596c0811f92168032`), 3/3 runs
byte-identical via cmp, exit 0, zero FAIL lines.

- **K-RV8-1 PASS:** X-RV7-3 replay (O1-O5). `diagnose_rollback_check`
  returns 1 (nonzero); both slots ROLLED_BACK; `vs3_apply` on "zbq"
  predicts "qqq" exactly (restoration).
- **K-RV8-2 PASS:** X735 control (O6-O7). Single provisional revision:
  returns exactly 1; status ROLLED_BACK. Single-slot semantics preserved.
- **K-RV8-3 PASS:** All 82 inherited named CHECK lines byte-identical to
  the frozen REVISE7 raw (md5 `6b783965c82d1b5483808a36ed4f78e7`);
  raw lines 2-195 byte-identical. Full diff contains only the
  pre-declared categories: banner rename, the Phase O block (19 CHECKs),
  R6 ROLLBACK/DEMOTE emit lines from Phase O only, and the final
  `=== RESULT: 117/117 ===` / `H-REVISE8 SURVIVES` lines.
- **K-RV8-4 PASS:** 3/3 byte-identical, exit 0.

Phase O extras (all frozen, all PASS): O8-O13 mixed ACTIVE+PROVISIONAL
firing set (provisional rolled back, active demoted, return 1); O14-O16
no correct uncovered baseline -> return 0, no state change; O17-O19
most-recent overrode a correct fellow revision -> only the wrong top
revision rolled back, fellow untouched.

## Revised claim

1 contradiction fells a provisional revision and 2 fell a confirmed one.
When multiple live revisions fire on the contradicted input, all
mispredict, and the store without them predicts the trusted label, the
contradiction protocol applies to every firing member. If no correct
uncovered baseline exists, no action is taken. This replaces the
narrowed K-RV7-4 bound (which carried the undisclosed single-firing
caveat).

## Boundaries (carried forward)

X-RV5-1 append-time underdetermination; forged-label dual-use
(X-RV7-1/X-RV7-2); duplicate append of an ACTIVE revision (X-RV7-4);
tombstone capacity (X-RV7-5). Branch B demotes an ACTIVE member on one
shared contradiction, consistent with the per-member graded rule; it
does not authenticate labels.

## Governance disclosures

1. Pure Zag throughout; zero Python at any stage (implementation,
   fixtures, builds, runs, hashes, diffs, file edits).
2. No em dashes in loop documentation (byte-checked).
3. Binaries built in /tmp/rv8 only, never committed.
4. Only owned paths staged: `revise8.zag`, `REVISE8_RAW.txt`,
   `REVISE8_RAW_R2.txt`, `REVISE8_RAW_R3.txt`, `REVISE8_RESULT.md`
   (plus the already-committed prereg). Concurrent workers' files
   untouched.
5. No push attempted or authorized.

## Files (branch `tnn-native-lab`)

- `docs/lab/research-lead/overnight-20260928/PREREG_REVISE8.md`
  (commit `94d5d0c97`)
- `docs/lab/research-lead/overnight-20260928/revise8.zag`
- `docs/lab/research-lead/overnight-20260928/REVISE8_RAW.txt`
  (+ `_R2`, `_R3`)
- `docs/lab/research-lead/overnight-20260928/REVISE8_RESULT.md`
  (this report)

## Suggested follow-ups

Independent red team on H-REVISE8 (natural attacks: forged firing sets
crafted to trigger Branch B demotions; Branch B vs Branch A precedence
gaming with three stacked revisions; firing-set enumeration with
tombstoned slots interleaved).
