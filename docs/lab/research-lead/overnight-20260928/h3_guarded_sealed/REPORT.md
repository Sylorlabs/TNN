# REPORT: H3-GUARDED-SEALED (sealed lane for the guarded consolidate)

Date: 2026-10-03. Worker: H3-GUARDED-SEALED worker (non-ledger task;
claim minting paused).
Prereg: committed alone as c61fcbd62 (strictly before implementation,
build, and runs), with transparent Amendment A (G14 correction,
10b747a9a) before implementation and before any results were seen.

## Verdict: GUARDED-SEALED-PASS (G0..G14 all hold)

3/3 runs byte-identical (sha256
5d031d57b19fcac26a222beb87ecfe139b62bd12a347e617f52fe79014522345).
Binary sha256
22fb1f69854b93d3327f86a484123b0d31a6e717deed0e6538dcdd23aceabe9c.

The guarded consolidate proposed by H3-INCORPORATED is CANONIZED as
the H3 release gate: the guarded gate reproduces all four sealed
adversary worlds exactly (no regression for reason-1 entries),
blocks the INCORPORATED reference hazard on the sealed substrate,
and does not over-block reason-2 entries without live references.

## Results (identical across run1/run2/run3)

| cond      | pre | post | ret | cf | ev | drop | bacc | rawA | rel | av | ai | lc | ar |
|-----------|-----|------|-----|----|----|------|------|------|-----|----|----|----|----|
| SEALED-W1 | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   | 0   | 0  | 0  | 12 | 0  |
| SEALED-W2 | 35  | 35   | 100 | 85 | 8  | 45   | 20   | 35   | 8   | 8  | 0  | 12 | 0  |
| SEALED-W3 | 35  | 35   | 100 | 48 | 0  | 16   | 20   | 35   | 13  | 8  | 5  | 12 | 5  |
| SEALED-W4 | 35  | 35   | 100 | 88 | 0  | 56   | 20   | 35   | 0   | 0  | 0  | 12 | 0  |

| cond       | cf | ev | drop | rel | av | ai | ar | lc | haz | trs      |
|------------|----|----|------|-----|----|----|----|----|-----|----------|
| GUARDED-W5 | 8  | 0  | 0    | 0   | 0  | 0  | 0  | 12 | 0   | -        |
| GUARDED-W6 | 8  | 0  | 0    | 8   | 8  | 0  | 0  | 12 | 0   | 22222222 |

Every measured row matches the frozen prereg predictions exactly.

Kill bars (in-band + external, all 3 runs):
- G0 IDENTITY: HOLD (39/39 pre-existing COND lines byte-identical
  to h3_sealed_b/run1.txt; 3/3 runs byte-identical; diff of
  h3_guarded_sealed.zag against h3_sealed_b/unpin_h3sealed.zag
  shows only the frozen delta: log stride 12->16, learner_revise_r
  + revise1 adapter, reason read-through in consolidate, the
  reason==2 no-live-reference conjunct, has_live_ref /
  install_composite / count_hazard additions, W5/W6 world drivers,
  main extensions, G-bar checks). Not VOID.
- G1 W1-NORECLAIM: HOLD (ev=0, drop=48, cf=80).
- G2 W1-SILENCE: HOLD (releases=0, av=0, ai=0, a_released=0).
- G3 W1-INTACT: HOLD (ret=100, lcheck=12).
- G4 W2-NODOUBLESPEND: HOLD (ev=8, drop=45, cf=85).
- G5 W2-EPISODES: HOLD (releases=8, av=8, ai=0).
- G6 W2-INTACT: HOLD (ret=100, lcheck=12).
- G7 W3-RELEASENOTDEATH: HOLD (releases=13, av=8, ai=5,
  a_released=5, ev=0, drop=16, cf=48).
- G8 W3-INTACT: HOLD (ret=100).
- G9 W4-NOPHANTOM: HOLD (releases=0, ev=0, drop=56, cf=88).
- G10 W4-INTACT: HOLD (ret=100, lcheck=12).
- G11 HAZARD-BLOCKED: HOLD (W5: releases=0, hazard=0, av=0, ai=0,
  lcheck=12, cf=8). The INCORPORATED reference hazard is fixed on
  the sealed substrate: all 8 absorbed entries blocked, zero
  dangling references handed to the absorbing composites.
- G12 NO-OVERBLOCK: HOLD (W6: releases=8, hazard=0, av=8, ai=0,
  lcheck=12, cf=8, trs=22222222). The guard is a no-live-reference
  precondition, not a blanket reason==2 block.
- G13 DETERMINISM: HOLD (3/3 byte-identical).
- G14 CLEAN: HOLD (ai=0, ar=0 in W1/W2/W4/W5/W6; lcheck=12 all 6
  rows; av==releases in W2 and W6).

In-band GUARDED-SEALED-VERDICT=PASS in all 3 runs; the governing
verdict is this external check.

## What this establishes

1. The guarded gate survives the same 4 sealed worlds. G1..G10
   reproduce the H3-SEALED-B frozen rows exactly: because every
   W1-W4 entry carries reason==1, the guard's precondition is
   identically false and the gate reduces to the sealed gate term
   by term. The 39-anchor byte-identity (G0) additionally proves
   the substrate did not drift: the only behavioral delta is the
   guard itself.
2. The guard fixes the INCORPORATED hazard without breaking the
   other worlds. G11 shows the transplant works: the hazard fix
   demonstrated gate-level in H3-INCORPORATED (R5) holds on the
   full sealed substrate with churn-capable machinery underneath.
3. The guard does not over-block. G12 discriminates the exact
   proposed semantics (block iff reason==2 AND live reference)
   from a blanket reason==2 block: reason-2 entries with no live
   references release exactly as before, trace reasons verbatim
   (22222222), audit clean.

## Canonization statement

The H3 release gate is now the GUARDED gate: release iff (learner
holds key AND key in learner's revision log AND log.old_value ==
pooled value AND belief-changed check) AND NOT (reason==2 AND a
live pooled entry references the key). REVISED and SUPERSEDED
behavior is unchanged from the sealed gate (proven, not assumed:
G1..G10). The H3-INCORPORATED caveat ("proposed, not canonized")
is discharged by this lane.

## Honest caveats

- The adversary is the worker in a second hat (same procedural
  seal as H3-SEALED: post-freeze designs from the published
  interface, frozen predictions, mechanism identity proof), not a
  second mind. W1-W4 designs are inherited from H3-SEALED's sealed
  set; W5/W6 were specified in this prereg before implementation.
- The learner remains simulated; reason codes are harness-written.
  The sealed claim is about the gate's behavior given reasons, not
  about a real learner producing them.
- The reference pattern (900000+k) is a harness convention
  modeling "the absorbing structure references the absorbed
  entry." A real substrate needs genuine reference tracking; this
  lane seals the decision logic, not the tracking.
- No churn phase in W5/W6 (deliberate isolation, as in
  H3-INCORPORATED): downstream retention/capacity behavior of the
  guarded gate under churn is untested. Note for future worlds:
  the churn value range (900001+j) overlaps the reference-pattern
  range, so a world mixing reason==2 with churn must re-derive the
  guard's interaction with churn-displaced values (in W2 the pool
  holds pattern-matching churn values, but all W2 entries are
  reason==1 so the guard cannot fire there).
- Amendment A corrected G14 before implementation (no results
  seen): the as-first-frozen G14 contradicted W3's frozen sealed
  row (ai=5, ar=5 are W3's expected sealed values). The correction
  is recorded transparently in PREREG.md; no frozen number
  changed.
- Non-ledger task: no claims minted.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which
python` return nothing under that PATH (verified 2026-10-03 before
the prereg commit); no forbidden executable invoked at any point
(shell used only for mkdir, file writes, znc invocation, binary
execution, sha256sum, cmp, diff, grep, sed, git ops). No
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

- c61fcbd62: frozen prereg (PREREG.md + NAMECHECK.md), alone,
  strictly before implementation, build, and runs.
- 10b747a9a: Amendment A (G14 correction), before implementation
  and before any results.
- This commit: h3_guarded_sealed.zag (source sha256
  2ebe5946ba143204d56eb09dde4bb688d89164ff025557bdca781f4450a21a86;
  diff against h3_sealed_b/unpin_h3sealed.zag shows only the frozen
  delta), h3_guarded_sealed_bin (sha256
  22fb1f69854b93d3327f86a484123b0d31a6e717deed0e6538dcdd23aceabe9c),
  build.err, run1/2/3.txt, run1/2/3.err, REPORT.md. Local only,
  never pushed.

## Follow-ups for the parent

- The guarded consolidate is CANONIZED as the H3 release gate
  (GUARDED-SEALED-PASS, G0..G14). The last open item from the H3
  arc named in H3-SEALED-B's follow-ups is now closed at the sealed
  level: reasons are exercised through the gate, the
  INCORPORATED/SUPERSEDED distinction is mechanized as a
  reason-specific release precondition, and the successful-episode
  importance source is specified (H3-INCORPORATED R7 + analysis).
- Open future work (unchanged): real learner credit assignment
  for episode-success weights; genuine reference tracking in the
  substrate; guarded-gate behavior under churn with reason==2
  entries (the value-range overlap noted above).
