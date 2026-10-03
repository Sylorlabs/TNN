# REPORT: H3-SEALED-B (fresh preregistration, corrected W2 derivation)

Date: 2026-10-03. Worker: H3-SEALED-B worker (non-ledger task; claim
minting paused).
Prereg: committed alone as 25a864719 (strictly before implementation and
runs; source copy target sha256 pre-recorded in NAMECHECK.md before the
prereg commit).

## Verdict: SEALED-PASS (S0..S10 all hold under the corrected prereg)

3/3 runs byte-identical (sha256
9336393b58fe6f858b2309e1c8d6c687b2e3c9073591097177d04d54234a811a,
identical to the H3-SEALED run hash: same binary, same output).

S0 (mechanism identity) holds on three independent checks:
- the 39 pre-existing COND lines are byte-identical to
  reclamation_h3b/run1.txt (diff clean);
- 3/3 runs byte-identical;
- the rebuilt binary is byte-identical to the H3-SEALED binary (sha256
  38d5da296073687c9f6f8820d19a98bd0ba297e12713490314d34d3da44d1ade):
  the source was copied ENTIRELY verbatim (whole-file sha256
  0b26c74d377d599fc0490cd41ed8611bca04c27b6f7eb9dbcf73c9ebde7250dc,
  cmp clean), so this is a deterministic-rebuild check as well as an
  identity check. The mechanism was not modified in any way.

S4 (corrected): SEALED-W2 measured `conflicts=85 evict=8 drop=45`,
exactly the corrected frozen values. The H3-SEALED builder derivation
error is resolved: churn2's j=0 write (900001) meets the resident 900021
left by churn1 -> 21 conflicts, not 20. cf = 20+0+8+20+8+8+21 = 85;
drop = 8+8+8+21 = 45; ev = 8. The [A]-provenance core of S4 (the F3
no-double-spend hypothesis: ev==8 exactly across two episodes) holds, as
in H3-SEALED.

S1, S2, S3, S5, S6, S7, S8, S9, S10 all hold, unchanged from H3-SEALED.

Governance note: the H3-SEALED SEALED-FAIL (S4) verdict is NOT amended by
this lane; it stands as recorded. This lane is the prescribed
fresh-preregistration-plus-fresh-run correction. The in-band
`SEALED-VERDICT=FAIL` line (line 78) and the old K20/VERDICT=FAIL lines
print verbatim in these runs because the source file is byte-identical
to the H3-SEALED file, whose in-band instrument computes against the old
frozen constants (84/44). As preregistered, those lines are instrument
convenience; the governing verdict is the external check recorded here.
This follows the H3B K20 precedent.

## The adversary won no world (unchanged from H3-SEALED)

- F1 (fool the careful learner into releasing critical entries):
  unattemptable from the published interface. The release gate's first
  conjunct is membership in the learner's own revision log, which no world
  step can write (only `learner_revise` appends, only for keys 5001..5008).
  Recorded as an honest negative in the prereg, not as a pass.
- F2 (mechanism overrides a silent learner under pressure): W1 falsified
  it. Under 60 mode-2 conflicts with zero releases, evict==0 and drop==48:
  the mechanism reclaimed nothing on its own. K18 generalizes to 3x
  pressure.
- F3 (release-flag double-spend across episodes): W2 falsified it.
  evict==8 exactly; episode-2 consolidation released 0 (nothing stale in
  the pool); audit stayed 8/0 across the cumulative 16-entry log.
- Phantom releases (W4): revise-after-exhaustion released 0; the old_value
  conjunct held under a novel cause (drops instead of installs).
- Release vs eviction (W3): 5 critical A entries released by the corrupted
  log, zero evictions after (churn ran first), retention 100, audit
  exactly 8 valid / 5 invalid. Release authorizes; only eviction destroys.
  The failure locus stays the learner's judgment, as K21 established.

## Results (identical across run1/run2/run3)

| cond      | pre | post | ret | cf | ev | drop | bacc | rawA | rel | av | ai | lc | ar |
|-----------|-----|------|-----|----|----|------|------|------|-----|----|----|----|----|
| SEALED-W1 | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   | 0   | 0  | 0  | 12 | 0  |
| SEALED-W2 | 35  | 35   | 100 | 85 | 8  | 45   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| SEALED-W3 | 35  | 35   | 100 | 48 | 0  | 16   | 20   | 35   | 13  | 8  | 5  | 12 | 5  |
| SEALED-W4 | 35  | 35   | 100 | 88 | 0  | 56   | 20   | 35   | 0   | 0  | 0  | 12 | 0  |

Kill bars (external verification, all 3 runs):
- S0 IDENTITY: HOLD (39/39 COND lines identical; 3/3 byte-identical;
  binary byte-identical to H3-SEALED). Not VOID.
- S1 W1-NORECLAIM: HOLD (ev=0, drop=48, cf=80).
- S2 W1-SILENCE: HOLD (releases=0, av=0, ai=0, a_released=0).
- S3 W1-INTACT: HOLD (ret=100, lcheck=12).
- S4 W2-NODOUBLESPEND: HOLD (ev=8, drop=45, cf=85; corrected bar).
- S5 W2-EPISODES: HOLD (releases=8, av=8, ai=0, a_released=0).
- S6 W2-INTACT: HOLD (ret=100, lcheck=12).
- S7 W3-RELEASENOTDEATH: HOLD (releases=13, av=8, ai=5, a_released=5,
  ev=0, drop=16, cf=48).
- S8 W3-INTACT: HOLD (ret=100: released-but-present entries serve reads).
- S9 W4-NOPHANTOM: HOLD (releases=0, ev=0, drop=56, cf=88).
- S10 W4-INTACT: HOLD (ret=100, lcheck=12).

## Answers to the parent questions

(1) Sealed in this lane means the same as in H3-SEALED: worlds designed
post-freeze from the published interface only, predictions frozen before
implementation, mechanism proven unchanged. The world designs are
inherited unchanged from H3-SEALED; nothing was redesigned here. The
identity proof is strictly stronger in this lane (whole-file source
byte-identity plus binary byte-identity, subsuming the 934-line region
check).

(2) Decision authority survived all four sealed worlds under the
corrected prereg: no auto-reclaim under 3x pressure (W1), no
double-spend across episodes (W2, now with exact corrected counts),
release dissociated from eviction with exact audit (W3), no phantom
releases (W4).

(3) The corrected W2 derivation (cf=85, drop=45, ev=8) is confirmed
empirically: the measured row matches the derivation term-by-term, and
the corrected S4 bar holds. No further correction is pending.

## Honest caveats (inherited from H3-SEALED)

- The adversary is the worker in a second hat (stated in the H3-SEALED
  prereg before the runs). The seal is procedural, not a second mind.
- The learner remains simulated; only release-decision authority was
  probed.
- INCORPORATED/SUPERSEDED reasons remain unexercised; the
  successful-episode importance source remains unrun.
- The in-band S-lines and SEALED-VERDICT=FAIL are instrument convenience
  (verbatim frozen instrument against the old constants); the governing
  verdict is the external check recorded here.
- The old binary's in-band K20/VERDICT lines print FAIL in the sealed
  binary too (verbatim frozen instrument, superseded H3 values); the H3B
  external reading governs those bars, unchanged.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
return nothing under that PATH (verified 2026-10-03 at startup, before
the prereg commit, and before the build and runs); no forbidden
executable invoked at any point (shell used only for mkdir, file writes,
binary execution, sha256sum, cmp, diff, grep, awk, git ops). No
PROCESS-FAIL condition triggered. Pinned znc verified byte-identical to
src/tools/toolchain/znc_linux_x86_64_abed8aa1 before the prereg commit.
The build ran in foreground (zagd unavailable warning only); the
resulting binary is byte-identical to the H3-SEALED binary, so the build
is deterministic. Git writes via /usr/bin/git directly (safebin git
symlink EPERM lesson); explicit pathspecs; no git reset; local only,
never pushed.

## Commits

- 25a864719: frozen prereg (PREREG.md + NAMECHECK.md), alone, strictly
  before implementation, build, and runs.
- This commit: unpin_h3sealed.zag (whole-file byte-identical to the
  H3-SEALED source; mechanism NOT modified), unpin_h3sealed_bin
  (byte-identical to the H3-SEALED binary), build.err, run1/2/3.txt,
  run1/2/3.err, REPORT.md. Local only, never pushed.

## Follow-ups for the parent

- H3-SEALED-B: SEALED-PASS (S0..S10) under the fresh preregistration with
  the corrected W2 derivation (cf=85, drop=45, ev=8). The H3-SEALED
  SEALED-FAIL (S4) stands as recorded; this lane is its prescribed
  fresh-prereg correction, not an amendment.
- Decision authority claim for the learner-issued unpin mechanism now
  holds across all four sealed post-freeze adversary worlds: no
  auto-reclaim without release, no release-flag double-spend across
  episodes, release dissociated from eviction, no phantom releases.
- Still open from H3/H3B: INCORPORATED/SUPERSEDED reasons and the
  successful-episode importance source.
