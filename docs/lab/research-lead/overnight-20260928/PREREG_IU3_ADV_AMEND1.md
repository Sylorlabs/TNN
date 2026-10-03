# PREREG AMENDMENT 1: H-INTENT-UNIFIED3 red team (IU3-ADV)

## Timeline (honest record)

1. PREREG_IU3_ADV.md frozen at commit a88de0031, before any attack code.
2. Attack harness iu3_adv.zag built from the repaired unified_learn.zag
   mechanism (lines 1..1311, verified byte-identical by diff), main()
   replaced by the frozen fixtures.
3. First execution: X-IU3-1a fixture VOID. The bridge training string
   "qab>zzz;qcd>zzz;abc>ccc;def>ccc;abcde>eeeee" returned rc=-1
   ("ULEARN FAIL: no program and no bridge"). The prereg's setup-void
   condition fired exactly as written: the bridge did not learn as a
   bridge, so the fixture was not scored.
4. Diagnosis: the non-'q' side {abc>ccc, def>ccc, abcde>eeeee} admits
   no single program. G1's known-good bridge string uses
   {abc>ccc, def>fff, abcde>eeeee}, which yields the "repeat last
   input char" program (abc->ccc, def->fff, abcde->eeeee). My
   "def>ccc" broke that pattern (last char 'f' repeated would be
   "fff", not "ccc"), so no split admitted programs on both sides.
5. This amendment: replace the X-IU3-1a bridge string with G1's exact
   known-good string "xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee"
   (condition input[0]==120, confirmed in G1) and move the colliding
   input to "xab", trained as the 17th (unrecorded) proc pair
   "xab>bax". The attack logic is unchanged: a genuine training-data
   contradiction ("xab>bax" as proc pair 17 vs "xab>xxx" recorded in
   the bridge) where the proc side's verbatim evidence falls outside
   the 16-input record cap.
6. The amended fixture is named X-IU3-1a' to distinguish it from the
   voided frozen fixture. The frozen X-IU3-1a is scored VOID (setup),
   not failed.

## What changed

- X-IU3-1a (frozen): VOID, setup. Bridge string did not learn.
- X-IU3-1a' (this amendment): colliding input "xab"; proc string ends
  "...;tuv>vut;xab>bax" (17 pairs); bridge string is G1's exact
  "xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee"; query "xab".
- Kill criterion unchanged from the prereg: kind != -2 AND no
  "INTENT VERBATIM-CONFLICT" line AND control workspace answers
  "bax" AND trace shows proc exact_match=0 with bridge
  exact_match=1. Verdict on success: DOWNGRADE (no frozen bar broken).

## What did not change

- X-IU3-1b, X-IU3-2, X-IU3-3, X-IU3-4: frozen as written.
- The amendment was decided during execution after observing the
  void, under the prereg's own setup-void clause. It is recorded
  here before the attack results are committed.

## Commit order

PREREG_IU3_ADV.md (a88de0031) strictly precedes this amendment,
which strictly precedes the attack implementation and results.
