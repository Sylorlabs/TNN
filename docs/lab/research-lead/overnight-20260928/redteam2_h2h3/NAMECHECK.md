# NAMECHECK.md -- REDTEAM2 H2/H3 (second red team on the repaired mechanisms)

## Step 0: toolchain guard (PASS)

Ran at worker startup, before any research work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with NO output from `which python3 python`.
Zero forbidden executables in worker PATH. All computation in pure Zag
compiled with the pinned `znc` (`~/safebin/znc` ->
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`). Shell used only to
invoke znc, run binaries, move/copy files, and hash outputs.

## Identity

- Lane: Fixed-Mechanism Red-Team Worker (H2/H3 second red team).
- Parent: TNN research orchestrator. Session is persistent for follow-ups.
- Mission: INDEPENDENT adversarial verification of the repaired H2
  (fragment recombination, commit f4dafef3b area) and H3 (constraint
  invention, uncommitted worker files) mechanisms. The fixer is not the
  verifier. No fixes applied here; kills are reported, not repaired.

## Provenance of mechanism sources (attacked, NOT modified)

H2 fixed mechanism (from `invention_h2_fix/`):
- `h2f_base.zag` SHA-256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  (matches the fix REPORT.md record; byte-identical to the red-team base)
- `h2f_patch.zag` SHA-256
  fe38482c187f0637930fcd29d57de5adb0da5ca479ada364bebef808fb7aac60
  (matches the fix REPORT.md record; the repaired fragment patch)
- `h2f_bin` (the fixer's binary) was NOT used directly: its driver bakes
  in the fixer's worlds. Red-team 2 builds its own attack binaries from
  byte-identical copies of the two files above plus a NEW adversarial
  driver. The repaired patch is never edited.

H3 fixed mechanism (from `invention_h3_fix/`):
- `fix_base.zag` SHA-256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  (matches the fix NAMECHECK.md record)
- `fix_mech.zag` SHA-256
  3cc2d2c9be6623a15682263c9f9da7d15df2ccfa1471b9c31a1174d64b4380dc
  (the fixer's repaired mechanism file as found on disk, uncommitted;
  derived from frozen `invent_patch.zag`
  4fc5493061363bc8ab9a228cb6a67db17f080a01114a5a920efcc87ced47d0bf
  per the fix REPORT.md)
- Same treatment: new attack binaries built from byte-identical copies
  plus a NEW adversarial driver. The repaired mechanism is never edited.

## Attack plan (all NEW; none tried by the first red-team or the fixer)

H2 (fixed frag binary, frag_on=1):
- B1 TRUNC-LOSS: 16 decoy [9,9,9,9] MAPs plus 3 true [1,1,1] MAPs, 9-link
  goal needing (T1,0,3)+(T2,0,3)+(T3,0,3). At DFS level 1 the 48
  per-level cap keeps 48 decoy fragments and drops the true second
  fragment. Attack arm teaches decoys first (true frags enumerate past
  the cap); control arm teaches trues first (identical knowledge, true
  frags inside the cap). Tests whether truncation LOSES a genuine
  solution (the fixer's stress test proved truncation happens; it never
  proved the dropped candidates were expendable).
- B2 ORDER-FORM: two genuine 2-fragment solutions to one goal (A-form
  [1,1,1]+[2,2,2] via r1/r2 facts, B-form [3,3,3]+[4,4,4] via parallel
  r3/r4 facts). Same knowledge taught in opposite orders. Tests whether
  the promoted invented FORM is teach-order determined (H2 kept
  first-hit-wins; the H3 repair added a tie-break policy, H2 did not).
- B4 DEPTH4: 12-link goal needing 4 fragments against the depth-3 cap.
  Tests the boundary the fixer's bound proof reasons about: clean
  refusal (BOUND) versus crash or corruption.

H3 (fixed invent mechanism):
- C1 TIEBREAK-WRONG: genuine hub-revisiting chain
  [1000,1010,1020,1010,2000] (1 repeat, legitimate) versus a clean
  distractor shortcut [1000,1100,1200,1300,2000] (0 repeats). Both
  satisfy the constraints, both verify answer-only. Tests whether the
  new fewest-repeats rule picks the WRONG chain.
- C2 FIRSTLIT-VACUITY: (a) first_lit=s versus first_lit unset on the
  same world (vacuity: identical winners expected); (b) poison-only
  world with first_lit=s (the stutter chain matches first_lit, so the
  entry check cannot stop it). Tests the enforcement claim's real
  content.
- C3 VERIFY-BLOWUP: layered DAG facts, loose constraints (every
  length-plen path satisfies), expected value unreachable so EVERY
  candidate fails verification after a full scratch-workspace copy,
  assembly, and verify. The exponential case the fixer deferred.
  Measures the per-candidate cost the repair added.
- C4 SCRATCH-HYGIENE: double invent_try on one workspace plus
  fact-chain stability checks. Tests the repair's "real workspace is
  never polluted" claim under heavy backtracking. Never tested before.

## Determinism requirement

Every attack binary runs 3x; transcripts must be byte-identical 3/3
(SHA-256 recorded per run). A non-deterministic attack is VOID.

## Outputs (this directory)

- `NAMECHECK.md` (this file)
- `REPORT.md` (per-attack KILL/SURVIVE/BOUND verdicts)
- `rt2_h2_base.zag`, `rt2_h2_patch.zag` (byte-identical copies of the
  fixed H2 sources, hashes above)
- `rt2_h2_driver.zag` (new H2 attack driver), `rt2_h2_full.zag`
  (assembled), `rt2_h2_bin` (binary), `rt2_h2_run1/2/3.txt`
- `rt2_h3_base.zag`, `rt2_h3_mech.zag` (byte-identical copies of the
  fixed H3 sources, hashes above)
- `rt2_h3_driver.zag` (new H3 attack driver), `rt2_h3_full.zag`
  (assembled), `rt2_h3_bin` (binary), `rt2_h3_run1/2/3.txt`
- build logs `rt2_h2_build.log`, `rt2_h3_build.log`

## Standing rules observed

Pure Zag for all research logic. No em/en dashes in documentation.
Paper untouched. Commits local only; nothing pushed.
