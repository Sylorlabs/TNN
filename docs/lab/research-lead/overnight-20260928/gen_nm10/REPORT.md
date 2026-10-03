# REPORT: GEN-NM10 -- NM=10+ Batteries on the Canonical GEN-REDIM Composer

Worker: gen-nm10. Date: 2026-10-03. Branch: lane-gennm10-20261003.
Governs: PREREG.md (commit a256719a1, strictly before implementation;
Section 5 block amended transparently post-run, see Section 4).

## 1. Verdict

**INFORMATIVE.** N1, N2, N3, N5, N6, N7 all PASS. N4 is INFORMATIVE,
not PASS: the B2 fenced block as frozen in commit a256719a1 held 64
lines due to a transcription slip (four lines dropped in the R2/R3
region); the Section 5 derivation specifies 68 lines and the binary
trace follows that derivation exactly, line by line, verified by hand
against the frozen rules. Per PREREG Section 8 the prereg block is
amended transparently and N4 is INFORMATIVE (never weakened to fit).

Substantive findings (all empirically established):

- The dynamic NM-parameterized layout holds at NM=11. B1's 10-chain
  declines cleanly at the 6-round cap with the exact predicted
  67-line trace (ANS=-2, TRIES=66, zero WIDEN=1). Any arena aliasing
  at nm=11 would have corrupted the trace; it did not.
- Composition works at 10+. B2's 9-structure fan-out/fan-in DAG (11
  structures live, nm=11) resolves in 4 rounds with the exact
  predicted trace (ANS=315, TRIES=67, zero WIDEN=1): three chains fan
  out from 301 and converge through one ADD2 structure.
- The binding limit at 10+ is the 6-round cap for deep chains (B1),
  exactly as at nm=8 (GEN-STRESS S4). The 64-pool and 64-tried2
  bounds are NM-independent constants, unchanged by construction,
  already characterized by GEN-REDIM S5; they were intentionally not
  re-stressed here.

## 2. What was built

Two driver mains only; the canonical GEN-REDIM mechanism
(rbase.zag, rgen_nomain.zag) is referenced by relative path and
verified byte-identical to the GEN-REDIM-CLEAN canonical digests
(N5). No mechanism source was copied, edited, or re-derived.

Files (all in this lane):
- nm_b1main.zag: setup_b1 (10-chain + IDENT distractor, 11 MAPs) +
  main (world_new_nm(11); gen_solve s=201 exp=3).
- nm_b2main.zag: setup_b2 (chains A/B/C + ADD2 converge + 2
  distractors, 11 MAPs) + main (world_new_nm(11); gen_solve s=301
  exp=315).
- nm_b1full.zag / nm_b2full.zag: assemblies (canonical rbase.zag +
  canonical rgen_nomain.zag + driver); one main each.
- build.sh: fail-closed pipeline (canonical digests, N6 opacity,
  assembly, znc compiles, 3x runs, expected-block extraction from
  PREREG.md, N3/N4 comparisons, WIDEN/ARM checks).

Binary sha256 (pinned safebin znc; stable across both pipeline runs):
- nm_b1bin 3820f7f5efccaad9b8b5cdaa24d04443ffedcc3adc117b754b673116f79db7c2
- nm_b2bin 89111f870986961de0b5b4a5bf898d4953a4869a433c682aace98799af4b3e36
Run-output sha256 (3/3 byte-identical):
- nm_b1bin 62fc35319be87add35a05a0b41212b024c2a2e519caa74a85a154439d04e8235
- nm_b2bin 0475e80b0756b3a66c4124d93911c6868d85a7d544108287ac9d3de0409ee628

## 3. Kill-bar results

| Bar | Result | Evidence |
|-----|--------|----------|
| N1 COMMIT-ORDER | PASS | PREREG.md+NAMECHECK.md committed alone as a256719a1; implementation after (see Sec 5). |
| N2 DETERMINISM | PASS | 3/3 runs pairwise byte-identical (cmp), stderr empty, both binaries; digests above. |
| N3 B1-LAYOUT | PASS | nm_b1bin stdout byte-identical to PREREG Section 4 exp-B1 (67 lines; ANS=-2, TRIES=66, 0 WIDEN). |
| N4 B2-COMPOSE | INFORMATIVE | Binary trace verified line-by-line against the frozen rules (Sec 4); original 64-line frozen block had transcription errors; corrected 68-line block is byte-identical. |
| N5 NO-MODIFY | PASS | build.sh Step 1: canonical digests match; lane held only the 2 drivers pre-assembly, 4 .zag files post-assembly. |
| N6 OPACITY | PASS | build.sh Step 2: no banned tokens outside the definitional list (drivers + PREREG). |
| N7 TOOLCHAIN | PASS | Safebin from the first command; `which python3`/`which python` return nothing; zero forbidden-interpreter invocations; pure Zag. |

## 4. The B2 transcription correction (transparent)

The first pipeline run: N3 PASS; N4 byte-compare failed at exp-B2
line 21. Re-derivation of the binary trace from the frozen rules by
hand (round snapshots, kind admission, id-ordered 1-input MAPs,
lex pair order, tried1/tried2 marking):

- R1 (10 lines): m0->311, m3->321, m6->331, m10->301 dup; rest -2.
  Pool [301,311,321,331].
- R2 (30 lines): m1(311)->312, m4(321)->322, m7(331)->3,
  m10 dups; rest -2. m8: snapshot has no kind-2 (3 added
  mid-round), 0 tries. Pool +[312,322,3].
- R3 (20 lines + 1 INTER2): m2(312)->313, m5(322)->2, m10 dups;
  rest -2 (kind-2 value 3 rejected by all in{1} MAPs). m8:
  (6,6)=6. Pool +[313,2,6].
- R4 (6 INTER2): 1-input MAPs all reject (new values all kind-2).
  m8 kind-2 indices {6,7,8,9}, tried (6,6); lex new pairs
  (6,7)=316, (6,8)=5, (6,9)=9, (7,6)=316, (7,7)=626,
  (7,8)=315=exp. FOUND at the 6th pair.
- ARM=GEN PROB=B2 ANS=315 TRIES=67; zero WIDEN=1 lines.

Every one of the 68 lines follows the rules; the predicted counts
(ANS=315, TRIES=67, 60 INTER, 7 INTER2, zero WIDEN) and the pair
sequence in the Section 5 derivation are all correct. The frozen
fenced block was missing 4 lines (transcription slip in the R2/R3
region), not a derivation or mechanism error. The block is amended
in PREREG.md with an explicit amendment note; the original 64-line
block remains in commit a256719a1 for audit. N4 stays INFORMATIVE.

## 5. Commit record

- a256719a1 GEN-NM10 prereg (frozen): NAMECHECK.md (Steps 0-2) +
  PREREG.md only.
- (this commit) implementation: nm_b1main.zag, nm_b2main.zag,
  build.sh, PREREG.md Section 5 block amendment (transparent, see
  Sec 4), assemblies, binaries, compile logs, run outputs, this
  REPORT.md.

## 6. Where the limits are at 10+

- ROUNDS (binding, empirical): B1 shows the 6-round cap governs
  cleanly at nm=11 exactly as at nm=8. A 10-link chain needs 10
  rounds; the composer declines with ANS=-2 and the exact
  rule-derived trace. Depth beyond 6 rounds is the first wall, and
  it is unchanged by NM.
- POOL (not binding here, characterized): 64-value cap with silent
  drop is a constant, not a function of NM. B2's pool peaks at 12
  values. GEN-REDIM S5 (TRIES=2734) remains the empirical
  characterization; nothing about NM=11 changes it.
- TRIED2 (not binding here, characterized): 64-entry cap with retry
  inflation is a constant. B2's m8 records 7 entries (max pair code
  6*4096+7*64+8=25048, well inside i32). The encoding is NM-general
  by construction (max entry at nm=11 is 45055).
- ARENA (not binding): ARENASZ(11)=5900 bytes; all regions disjoint
  by exact size chaining; B1/B2 traces prove no aliasing at nm=11.

## 7. Boundaries and follow-ups

- The pre-declared boundaries (PREREG.md Section 9) stand:
  installed MAPs, expected-answer verification, one ADD2 class,
  NM>11 not exercised, pool/tried2 intentionally not re-stressed,
  WIDEN semantics unchanged.
- B2's composition core is 9 structures (chains A/B/C + m8) with 2
  distractor structures live through every round (11 total, nm=11).
  A future battery could widen the genuine DAG core further, but the
  10+ episode scale (arena, trial loop, tried1/tried2 at nm=11) is
  what this battery tested.
- Suggested follow-up: a pool-flood battery at nm=11 to confirm the
  silent-drop signature is identical under the dynamic layout
  (expected: same S5-class behavior, since the cap is constant).
