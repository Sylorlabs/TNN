# REPORT: H3-SEALED (sealed post-freeze adversary worlds)

Date: 2026-10-03. Worker: H3-SEALED worker (non-ledger task; claim minting
paused).
Prereg: committed alone as 497408373 (strictly before implementation and
runs; mechanism source lines 1-934 verified byte-identical to the frozen
H3 artifact before the build).

## Verdict: SEALED-FAIL (S4 miss; builder derivation error, not an adversary win)

3/3 runs byte-identical (sha256
9336393b58fe6f858b2309e1c8d6c687b2e3c9073591097177d04d54234a811a).
S0 (mechanism identity) holds: all 39 pre-existing COND lines are
byte-identical to reclamation_h3b/run1.txt, and the old K1..K22 + VERDICT
lines are identical too. The sealed binary's mechanism is the unchanged H3
mechanism (binary sha256
38d5da296073687c9f6f8820d19a98bd0ba297e12713490314d34d3da44d1ade).

S1, S2, S3, S5, S6, S7, S8, S9, S10 all hold. **S4 MISSES**: SEALED-W2
measured `conflicts=85 evict=8 drop=45`; the prereg froze `cf==84`,
`drop==44`, `ev==8`. Per the frozen rules the bar is not moved: the
verdict is SEALED-FAIL, naming S4.

Root cause (builder derivation error, [B] provenance): the W2 cf/drop
derivation treated the second single-owner churn as 20 conflicts by analogy
with UNPIN-A20. But `teach_churn(M,21)` writes key 3999 twenty-one times
(values 900001+j, j=0..20). The FIRST churn's j=0 write is a fresh install
(0 conflicts, hence 20 conflicts total, as in UNPIN-A20); the SECOND
churn's j=0 write meets the resident value 900021 with 900001 -> a
conflict. So churn2 contributes 21 conflicts, not 20: cf =
20+8+20+8+8+21 = 85, and the extra conflict's relocation drops: drop =
8+8+8+21 = 45. The mechanism behaved exactly per its published rules
(`mem_write` conflict counting); the error is entirely in the worker's
[B]-provenance arithmetic.

What did NOT fail: the [A]-provenance core of S4, which is the actual
adversary hypothesis F3. `evict==8` held exactly: across two learner
episodes, the 8 episode-1 releases were consumed once by churn1 and never
re-spent. No double-spend, no stale-flag eviction, no leak.

## The adversary won no world

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
  old K-lines identical). Not VOID.
- S1 W1-NORECLAIM: HOLD (ev=0, drop=48, cf=80).
- S2 W1-SILENCE: HOLD (releases=0, av=0, ai=0, a_released=0).
- S3 W1-INTACT: HOLD (ret=100, lcheck=12).
- S4 W2-NODOUBLESPEND: MISS (cf=85 vs 84, drop=45 vs 44; ev=8 as frozen).
- S5 W2-EPISODES: HOLD (releases=8, av=8, ai=0, a_released=0).
- S6 W2-INTACT: HOLD (ret=100, lcheck=12).
- S7 W3-RELEASENOTDEATH: HOLD (releases=13, av=8, ai=5, a_released=5,
  ev=0, drop=16, cf=48).
- S8 W3-INTACT: HOLD (ret=100: released-but-present entries serve reads).
- S9 W4-NOPHANTOM: HOLD (releases=0, ev=0, drop=56, cf=88).
- S10 W4-INTACT: HOLD (ret=100, lcheck=12).

## Answers to the parent questions

(1) Sealed in this lane means: worlds designed post-freeze from the
published interface only (protocol steps, published rows, claims), no
source access for the designs; predictions frozen before implementation;
mechanism proven unchanged by S0 behavioral identity (39/39 rows) plus a
byte-identical mechanism source region. The two-hat honesty statement in
the prereg records that the adversary was this worker in a second hat (no
second agent available at depth 2/2); the enforced barrier was
informational (designs fixed before source consultation) and procedural
(frozen predictions, identity proof).

(2) Decision authority survived all four sealed worlds: no auto-reclaim
under 3x pressure (W1), no double-spend across episodes (W2), release
dissociated from eviction with exact audit (W3), no phantom releases
(W4). The single miss is the worker's own [B] arithmetic on W2's exact
counts, root-caused above.

(3) Corrected W2 derivation for any future fresh preregistration: cf=85,
drop=45, ev=8 (churn2 contributes 21 conflicts: the install-turned-
conflict on key 3999). Not re-run in this lane; a re-run would require a
fresh preregistration per governance.

## Honest caveats

- The adversary is me in a different hat (stated in the prereg before the
  runs). The seal is procedural, not a second mind.
- The learner remains simulated; only release-decision authority was
  probed.
- INCORPORATED/SUPERSEDED reasons remain unexercised; the
  successful-episode importance source remains unrun.
- The in-band S-lines and SEALED-VERDICT=FAIL are instrument convenience;
  the governing verdict is the external check recorded here.
- The old binary's in-band K20/VERDICT lines print FAIL in the sealed
  binary too (verbatim frozen instrument, superseded H3 values); the H3B
  external reading governs those bars, unchanged.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
return nothing under that PATH (verified 2026-10-03 at startup, before the
prereg commit, and before the runs); no forbidden executable invoked at any
point (shell used only for mkdir, file writes, binary execution, sha256sum,
cmp, diff, grep, awk, git ops). No PROCESS-FAIL condition triggered. Pinned
znc verified byte-identical to
src/tools/toolchain/znc_linux_x86_64_abed8aa1 before the prereg commit.
Git writes via /usr/bin/git directly (safebin git symlink EPERM lesson);
explicit pathspecs; no git reset; local only, never pushed.

## Commits

- 497408373: frozen prereg (PREREG.md + NAMECHECK.md), alone, strictly
  before implementation and runs.
- This commit: unpin_h3sealed.zag (mechanism lines 1-934 byte-identical to
  the frozen H3 source; only 4 new world drivers + main extensions added),
  unpin_h3sealed_bin, run1/2/3.txt, run1/2/3.err, REPORT.md. Local only,
  never pushed.

## Follow-ups for the parent

- H3-SEALED: SEALED-FAIL (S4) on a builder derivation error; zero
  adversary wins. All four sealed worlds support the decision-authority
  claim: the mechanism never reclaims without a learner release (W1),
  never double-spends releases across episodes (W2), never confuses release
  with eviction (W3), and never phantom-releases (W4). The corrected W2
  counts (cf=85, drop=45) are frozen here for any future fresh prereg.
- Still open from H3/H3B: INCORPORATED/SUPERSEDED reasons and the
  successful-episode importance source.
