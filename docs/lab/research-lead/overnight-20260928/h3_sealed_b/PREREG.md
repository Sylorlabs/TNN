# PREREG: H3-SEALED-B (fresh preregistration with corrected W2 derivation)

Frozen 2026-10-03. This preregistration strictly precedes all
implementation and all runs in this lane. This prereg commit contains ONLY
PREREG.md and NAMECHECK.md. No kill bar below may be weakened or
reinterpreted after results are seen. VOID is terminal: it is corrected
only by fresh preregistration plus a fresh run, never by salvage or
amend-and-promote.

Worker: H3-SEALED-B worker (non-ledger task; claim minting paused).
Lane: `docs/lab/research-lead/overnight-20260928/h3_sealed_b/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation; shell only for
binary execution, git ops, sha256sum, cmp, diff, grep, awk, and file
movement. Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`), byte-identical to `~/safebin/znc`
(sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
verified 2026-10-03 before this prereg).

## Why this lane exists

H3-SEALED closed with SEALED-FAIL on bar S4: the frozen prereg predicted
SEALED-W2 `conflicts==84, drop==44, ev==8`; the 3/3 byte-identical runs
measured `conflicts==85, drop==45, ev==8`. The H3-SEALED report
root-caused this as a builder derivation error with [B] provenance (the
worker's own arithmetic, not a mechanism surprise): the second
`teach_churn(M,21)` on key 3999 contributes 21 conflicts, not 20, because
its j=0 write (900001) meets the resident value 900021 left by the first
churn, whereas the first churn's j=0 write was a fresh install.

Per governance the H3-SEALED SEALED-FAIL verdict stands and is not
amended. This lane is the prescribed fresh-preregistration-plus-fresh-run
correction. The mechanism is NOT modified in any way; only the prereg
derivation changes.

## Objective (inherited from H3-SEALED, unchanged)

The four sealed post-freeze adversary worlds W1..W4, their attack
hypotheses (F1/F2/F3/phantom-release), their protocols, and the published
decision-authority claims under test are exactly those of the H3-SEALED
prereg (commit c0f96a743 lane `h3_sealed/`). Nothing is redesigned here;
the adversary hat's designs were sealed in H3-SEALED. The only change in
this fresh prereg is the corrected W2 exact-count derivation below, which
the H3-SEALED worker owned and froze in its report ("cf=85, drop=45, ev=8
... frozen in the report for any future fresh prereg").

## The mechanism under test (frozen, unchanged)

The sealed binary is built from a source file that is copied ENTIRELY
verbatim from `h3_sealed/unpin_h3sealed.zag` (source sha256
0b26c74d377d599fc0490cd41ed8611bca04c27b6f7eb9dbcf73c9ebde7250dc).
Whole-file byte-identity is the mechanism-identity proof (stronger than
H3-SEALED's 934-line region check, which it subsumes: lines 1-934 remain
the frozen H3 mechanism, lines 935-end the four sealed world drivers plus
the extended main, all unmodified).

Instrument honesty: the in-band S-lines in that verbatim file compute
against the OLD frozen constants (cf==84, drop==44). They are instrument,
not mechanism, and they are not edited here because the file must stay
byte-identical. Consequently the in-band S4/SEALED-VERDICT lines will
print FAIL in these runs exactly as in H3-SEALED. The governing verdict
is the external worker check against THIS prereg's bars, following the
H3B K20 precedent (verbatim frozen instrument; external reading governs).

## Sealed worlds (unchanged from H3-SEALED)

W1 SILENT-PRESSURE, W2 TWO-EPISODE, W3 HASTY-FIRST, W4
REVISE-AFTER-PRESSURE: protocols, adversary information sets, and attack
hypotheses are exactly as preregistered in H3-SEALED. Only W2's frozen
exact counts change.

## Corrected W2 derivation (frozen here, [B] provenance, supersedes the H3-SEALED W2 derivation)

W2 protocol: teach A -> pre -> scratch -> teach B -> revise ->
consolidate (episode 1) -> churn single w=21 (churn1) -> scratch ->
revise -> consolidate (episode 2) -> churn single w=21 (churn2) ->
post-test.

Conflict accounting ([B], from the validated `mem_write` rule: a conflict
is counted only on same-key different-value; same-value rewrites are
no-ops; fresh key installs are 0 conflicts):

- teach_B: 20 conflicts (UNPIN-A20 row).
- scratch1 (episode 1): 0 conflicts. Fixed keys 5001..5008 are written
  with 70000i for the first time: fresh installs.
- revise1 (episode 1): 8 conflicts (same-key different-value on the 8
  scratch keys; displaced old values relocate into the full pool).
- churn1: `teach_churn(M,21)` writes key 3999 twenty-one times with
  values 900001+j, j=0..20. The j=0 write is a fresh install (0
  conflicts); j=1..20 are same-key different-value (20 conflicts).
  churn1 contributes 20.
- scratch2 (episode 2): 8 conflicts (keys 5001..5008, 70000i -> 60000i).
- revise2 (episode 2): 8 conflicts.
- churn2: j=0 writes 900001 while the resident value is 900021 (left by
  churn1) -> same-key different-value -> a conflict. j=1..20 are likewise
  conflicts. churn2 contributes 21. THIS is the term the H3-SEALED prereg
  miscounted as 20.

cf = 20 + 0 + 8 + 20 + 8 + 8 + 21 = 85.

Drop accounting: churn1's 20 conflicts = 4 fills + 16 relocations -> 8
evict (the 8 released slots) + 8 drop. scratch2: 8 conflicts -> pool
full -> 8 drops. revise2: 8 conflicts -> pool full -> 8 drops. churn2:
21 conflicts -> 21 relocations -> 0 released slots -> 21 drops.

drop = 8 + 8 + 8 + 21 = 45. ev = 8 (churn1 only; churn2 meets zero
released slots). releases = 8, av = 8, ai = 0, a_released = 0, ret =
100, pre = post = rawA = 35, bacc = 20, lcheck = 12.

Frozen W2 row: cf==85, ev==8, drop==45.

## Frozen kill bars

R offsets: W1 -> 1568, W2 -> 1632, W3 -> 1696, W4 -> 1760 (64-byte
stride, same 13-column layout as run_cond_h3 rows). The governing verdict
is the external worker check (same reading as H3B's K20 note and the
H3-SEALED S-line note).

- S0 IDENTITY (external): the 39 pre-existing COND lines are byte-identical
  to reclamation_h3b/run1.txt (first 39 `^COND=` lines), AND 3/3 runs are
  byte-identical (sha256 equal), AND the built binary is byte-identical
  to the H3-SEALED binary (sha256
  38d5da296073687c9f6f8820d19a98bd0ba297e12713490314d34d3da44d1ade,
  deterministic rebuild check). Else VOID: the mechanism moved or the
  build is nondeterministic; the sealed test is invalid.
- S1 W1-NORECLAIM: ev==0 AND drop==48 AND cf==80.
- S2 W1-SILENCE: releases==0 AND av==0 AND ai==0 AND a_released==0.
- S3 W1-INTACT: pre==35 AND post==35 AND ret==100 AND rawA==35 AND
  bacc==20 AND lcheck==12.
- S4 W2-NODOUBLESPEND: ev==8 AND drop==45 AND cf==85. (CORRECTED: was
  drop==44, cf==84 in H3-SEALED. This is the only bar that changed.)
- S5 W2-EPISODES: releases==8 AND av==8 AND ai==0 AND a_released==0.
- S6 W2-INTACT: pre==35 AND post==35 AND ret==100 AND rawA==35 AND
  bacc==20 AND lcheck==12.
- S7 W3-RELEASENOTDEATH: releases==13 AND av==8 AND ai==5 AND
  a_released==5 AND ev==0 AND drop==16 AND cf==48.
- S8 W3-INTACT: pre==35 AND post==35 AND ret==100 AND rawA==35 AND
  bacc==20 AND lcheck==12.
- S9 W4-NOPHANTOM: releases==0 AND av==0 AND ai==0 AND ev==0 AND
  drop==56 AND cf==88 AND a_released==0.
- S10 W4-INTACT: pre==35 AND post==35 AND ret==100 AND rawA==35 AND
  bacc==20 AND lcheck==12.

Verdict: SEALED-PASS iff S0..S10 all hold. S0 failure -> VOID (terminal).
Any S1..S10 failure names the bar and yields SEALED-FAIL: the adversary
wins that world, i.e. a published decision-authority claim did not
generalize to a sealed post-freeze world. Thresholds are frozen; they are
not moved after results. The H3-SEALED SEALED-FAIL (S4) verdict is not
altered by this lane; it stands as recorded.

## Discrimination design (unchanged from H3-SEALED)

- S0 bars the moved-mechanism confound and the nondeterminism confound
  (VOID, not FAIL); the binary byte-identity check additionally bars the
  moved-build confound.
- S1 is the pressure generalization of K18: a hidden auto-reclaim path
  would show ev>0 exactly here (48 drops with ev=0 is a strong, falsifiable
  shape).
- S4 is the flag-lifecycle probe H3 never ran: stale release flags would
  show ev=16 (double-spend) instead of 8; a leak would show releases != 8.
- S7 dissociates release from eviction for the first time: 5 critical
  entries released but present. If release damaged reads, ret<100.
- S9 tests the old_value conjunct under a novel cause (drops instead of
  installs). Phantom releases would show releases>0.
- S2/S3/S5/S6/S8/S10 are the intactness preconditions: if the world setup
  itself disturbed knowledge, the outcome bars would be vacuous.

## What this does NOT test (honest accounting)

- The adversary is the worker in a second hat (see the H3-SEALED
  two-hat honesty statement, inherited here). The seal is procedural
  (post-freeze design, published-interface-only hypotheses, frozen
  predictions, mechanism identity proof), not a second mind.
- The learner remains simulated; only the release-decision authority is
  probed, not learner intelligence.
- INCORPORATED/SUPERSEDED reasons remain unexercised (same code path,
  reason codes 2/3 never emitted); the successful-episode importance
  source from the H1 follow-ups remains unrun.
- A bar failure caused by a builder derivation error (wrong [B] number)
  is still SEALED-FAIL per the frozen bars; the report must root-cause it
  as derivation error vs mechanism surprise, without moving the bar.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first, alone. Implementation
(verbatim source copy), the build, the runs (run1/2/3.txt), and REPORT.md
only after. Commit-order self-check: this prereg commit must strictly
precede the implementation commit and the runs.
