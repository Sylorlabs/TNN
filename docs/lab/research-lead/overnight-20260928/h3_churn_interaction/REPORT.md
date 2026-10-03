# REPORT: H3-CHURN-INTERACTION (churn x reason==2 interaction)

Date: 2026-10-03. Worker: H3-CHURN-INTERACTION worker (non-ledger
task; claim minting paused).
Prereg: committed alone as 12e63d937 (strictly before
implementation, build, and runs). No amendments.

## Verdict: CHURN-INTERACTION-PASS (C0..C5 all hold)

3/3 runs byte-identical (sha256
4d1a4c277e447b461cb9ae7d0b6b2f7bcb805954fbd3ca2dfe1bcbc47b3e57e1).
Binary sha256
7b8ad20f065d0edbfcdd974c811f18535e343ea40bf89d14b99d59152d713a47.

The H3-GUARDED-SEALED churn caveat is RESOLVED. The canonized
guarded gate behaves exactly as specified with reason==2 entries
under churn: it still blocks the genuine INCORPORATED reference
hazard (W7), it does not over-block from churn per se (W9), and
the value-range overlap's exact effect is now measured and
re-derived (W8): the guard is provenance-blind, so
churn-displaced values that land on 900000+k block a reason==2
candidate k exactly as a genuine reference would.

## Results (identical across run1/run2/run3)

| cond     | cf | ev | drop | rel | av | ai | ar | lc | haz | trs      |
|----------|----|----|------|-----|----|----|----|----|-----|----------|
| CHURN-W7 | 28 | 0  | 4    | 0   | 0  | 0  | 0  | 12 | 0   | -        |
| CHURN-W8 | 16 | 0  | 0    | 0   | 0  | 0  | 0  | 12 | 0   | -        |
| CHURN-W9 | 28 | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 22222222 |

Every measured row matches the frozen prereg predictions exactly.
The 45 pre-existing COND lines (39 anchors + SEALED-W1..W4 +
GUARDED-W5/W6) are byte-identical to h3_guarded_sealed/run1.txt,
and the in-band GUARDED-SEALED-VERDICT=PASS still holds, so the
churn worlds caused no regression.

Kill bars (in-band + external, all 3 runs):
- C0 IDENTITY: HOLD (45/45 pre-existing COND lines byte-identical
  to h3_guarded_sealed/run1.txt; 3/3 runs byte-identical; diff of
  h3_churn_interaction.zag against
  h3_guarded_sealed/h3_guarded_sealed.zag shows only the frozen
  delta: lane header/tag, R alloc 2048->4096, run_churn_wx driver,
  3 main call sites, C1..C4 checks, verdict line). Not VOID.
  Builder erratum (no effect on verdict): PREREG.md wrote "41
  pre-existing COND lines"; the true count is 45 (39 anchors +
  4 sealed + 2 guarded). The executed check covered all 45 and
  all are byte-identical, so the bar holds under either count;
  the number is corrected here transparently, not moved as a
  threshold.
- C1 W7-HAZARD-BLOCKED-UNDER-CHURN: HOLD (rel=0, haz=0, av=0,
  ai=0, cf=28, ev=0, drop=4, lc=12). The guard's true positive
  survives churn: genuine references installed before the churn
  phase still block all 8 releases. drop=4 is the derived
  pool-full signature (policy 8 no-reclaim pinning: 16 churn
  debris fill slots 16..31, the last 4 relocates drop++ and
  destroy in place).
- C2 W8-DEBRIS-BLOCKS: HOLD (rel=0, haz=0, av=0, ai=0, cf=16,
  ev=0, drop=0, lc=12). Collision-band churn debris
  (905001..905008, zero genuine references) fires the guard for
  all 8 candidates. This is the re-derived interaction made
  observable.
- C3 W9-NO-OVERBLOCK: HOLD (rel=8, haz=0, av=8, ai=0, cf=28,
  ev=0, drop=0, lc=12, trs=22222222). Churn per se does not
  block: natural churn debris (900001..900020, implying k in
  1..20) never matches the candidate keys, and all 8 reason==2
  entries release exactly as in W6.
- C4 CLEAN: HOLD (ai=0, ar=0 in W7/W8/W9; lc=12 all three;
  av==rel in W9).
- C5 DETERMINISM: HOLD (3/3 byte-identical).

In-band CHURN-INTERACTION-VERDICT=PASS in all 3 runs; the
governing verdict is this external check.

## The re-derived guard x churn interaction (frozen)

1. Guard predicate (provenance-blind): the canonized gate blocks
   a reason==2 release candidate with key k iff some USED pool
   slot holds value exactly 900000+k at consolidate time.
   Genuine absorbing references, churn debris, or any other
   entry with a matching value are indistinguishable to the
   guard. Proven by C1 vs C2: genuine references (W7) and debris
   only (W8) both yield rel=0 through the identical code path.
2. The overlap is structural and total in value space: churn
   debris values 900001+j (j >= 0) lie inside the
   reference-pattern band [900000,910000) for all j <= 9998.
   The H3-GUARDED-SEALED caveat is confirmed as a real overlap,
   not a false alarm.
3. Activation condition: the overlap FIRES the guard iff a live
   debris value equals 900000+k for a reason==2 candidate key k.
   With the frozen key allocation (5001..5008) and natural churn
   (w=21, debris implying k in 1..20), the overlap is LATENT:
   it can never fire (W9 proves the guard stays inert). W8
   activates it by construction and measures the consequence:
   rel=0 with zero genuine references, i.e. a false-positive
   over-block under the guard's intended semantics (true
   positive under its value-based letter).
4. Capacity bound (policy 8): churn debris accumulates only until
   the pool fills (32 slots); further displaced values are
   destroyed in place (drop++), never displaced. Debris is
   therefore bounded and oldest-first: a wide natural churn
   cannot smuggle old colliding debris past consolidate, because
   the colliding values would be the oldest debris and the pool
   fills with newer debris first (in a w=5009 natural churn the
   905001..905008 values are debris #5001..5008 and are destroyed
   in place once the pool fills at #24). Under no-reclaim
   pinning, natural churn alone cannot activate the overlap
   against the frozen keys at any width.
5. Ordering: genuine references installed BEFORE churn survive
   it (W7: first-free fill occupies slots 16..31; slots 8..15
   untouched; no eviction without releases). References installed
   AFTER pool-full churn would never land (install_composite
   silently no-ops on a full pool; harness limitation, avoided
   by install-before-churn ordering).

Consequence for the canonized gate: no change is proposed or
needed. The gate behaves exactly as specified in all three churn
worlds. The overlap's practical consequence is a false-positive
over-block IF debris ever value-matches a reason==2 candidate
key: unreachable by natural churn under the frozen key
allocation and policy 8 at any width (clauses 3+4), reachable by
adversarial/targeted churn or by small candidate keys. Any
future substrate with small keys or adversarial churn must keep
the reference band disjoint from churn debris values, or replace
value-sniffing with genuine reference tracking (already an open
item from H3-GUARDED-SEALED).

## What this establishes

1. The hazard fix survives churn. C1 shows the W5 true positive
   is not dislodged by a 21-wide churn phase: the guard still
   blocks all 8 releases, hazard stays 0.
2. Churn per se does not over-block. C3 shows 8/8 releases with
   trace reasons verbatim (22222222) under the same churn that
   W7/W8 see; the guard's block is driven by value-match, not by
   churn or by reason==2 alone (C2 vs C3 discriminate this: the
   only difference between W8 and W9 is debris values).
3. The noted hazard is resolved with a frozen re-derivation
   (clauses 1..5 above), verified term-by-term against measured
   rows. Future worlds mixing reason==2 with churn inherit this
   derivation instead of the caveat.

## Honest caveats

- The adversary is the worker in a second hat (same procedural
  seal as H3-GUARDED-SEALED), not a second mind. W7/W8/W9 were
  specified in the prereg before implementation.
- The learner remains simulated; reason codes are harness-written.
- W8's collision-band churn is a targeted probe: same churn key
  (3999), owner (16), and conflict/displace mechanics as
  teach_churn, with values in the collision band (the tail a wide
  natural churn would produce). It is not a natural
  teach_churn(M,w) run; per clause 4, no natural width activates
  the overlap against the frozen keys under policy 8.
- install_composite silently no-ops when the pool is full
  (harness limitation, verbatim H3-INCORPORATED); W7 avoids it by
  installing before churn.
- Builder erratum in PREREG.md: "41 pre-existing COND lines"
  should read 45 (39 anchors + 4 sealed + 2 guarded). The check
  covered all 45; all byte-identical; no threshold moved, no
  effect on the verdict. Recorded here transparently.
- Non-ledger task: no claims minted.
- The guarded consolidate was NOT modified in this lane (test
  only, per the task constraint).

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which
python` return nothing under that PATH (verified 2026-10-03 before
the prereg commit); no forbidden executable invoked at any point
(shell used only for mkdir, file writes, znc invocation, binary
execution, sha256sum, cmp, diff, grep, git ops). No
PROCESS-FAIL condition triggered. Pinned znc verified
byte-identical to src/tools/toolchain/znc_linux_x86_64_abed8aa1
before the prereg commit (sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
Build ran in foreground (zagd unavailable warning only), first
try, no defect symptoms. New-code audit: no negated-conjunction
while conditions, no `as *i32` slice construction, no `[]u8 as
*u8` casts, if-nesting at most 3. Git writes via /usr/bin/git
directly (safebin git symlink EPERM lesson); explicit pathspecs;
no git reset; local only, never pushed.

## Commits

- 12e63d937: frozen prereg (PREREG.md + NAMECHECK.md), alone,
  strictly before implementation, build, and runs.
- This commit: h3_churn_interaction.zag (source sha256
  837903879e01a6175cd815143c3babc958ad8bd24cd343299afdc9c8091eb698;
  diff against
  h3_guarded_sealed/h3_guarded_sealed.zag shows only the frozen
  delta), h3_churn_interaction_bin (sha256
  7b8ad20f065d0edbfcdd974c811f18535e343ea40bf89d14b99d59152d713a47),
  build.err, run1/2/3.txt, run1/2/3.err, REPORT.md. Local only,
  never pushed.

## Follow-ups for the parent

- The H3-GUARDED-SEALED churn caveat is CLOSED: the re-derived
  interaction (clauses 1..5) is frozen and verified. The
  canonized guarded gate stands unchanged.
- The guard is provenance-blind by construction (value-sniffing).
  This is sealed and characterized, not fixed: a future substrate
  with small candidate keys or adversarial churn needs either a
  reference band disjoint from churn debris or genuine reference
  tracking. The latter was already open from H3-GUARDED-SEALED.
- Suggested next probe (not started): a world where churn
  arrives AFTER a guarded release decision was already taken
  (release-then-churn ordering), to check the hazard definition
  against post-release reference installation. Left for the
  parent to prioritize.
