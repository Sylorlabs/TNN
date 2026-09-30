# H-UNIFIED10 RED TEAM RESULT (U10-ADV)

**Date:** 2026-09-29
**Lane:** H-UNIFIED10 independent red team
**Target:** H-UNIFIED10 SURVIVES (29/29), builder result commit `86a759d1b`,
  builder prereg `64db99d58`, builder raw md5
  `42b2b58855c9a6311a03a0a0376b7978`.
**Adversary prereg:** `b89469cb8` (committed alone before any attack code,
  build, or run; em-dash scan clean).
**Verdict: DOWNGRADED.** One real R11b implementation defect confirmed
  (X-U10-2c). No kill criterion fired. R11a/R11c and the disclosed R11b
  boundaries hold; two boundaries sharpened/confirmed and one new boundary
  established.

## Verdict logic (frozen, from PREREG_U10_ADV.md)

- KILL required: stored quarantined-while-blocked episode; DCOUNT>0;
  silent eviction; 3-run divergence; regression md5 mismatch; undeclared
  behavioral hunk. None fired.
- DOWNGRADE required: X-U10-2c confirms (phantom tombstone refuses a
  never-quarantined episode). Confirmed. No other downgrade criterion fired.
- Everything else held, so the verdict is DOWNGRADED on the single defect.

## Build and determinism

- Harness: `u10_adversary/u10_adv.zag` = committed `unified10_learn.zag`
  lines 1..1602 byte-verbatim (cmp-verified against
  `git show 86a759d1b:...`) + adversary-only `main()` and helpers
  (`buf_put`, `mkep`, `learn1`, `cp1`, `find_cval`). No name collisions
  with mechanism-region functions; no top-level state added.
- Toolchain: pinned `/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`,
  `znc 2026.07.0-dev (edition 2026)`. Build: warnings only (36 analyzer
  notes, non-strict), binary 154564 bytes.
- Runs: 3/3 byte-identical (`cmp` clean), exit 0 all runs.
  Raw md5: `83a6cd9039c90289563f5ae6e085a73b` (all three runs).
- In-harness checks: **21 PASS, 0 FAIL** (`npass=21 nfail=0`,
  `U10-ADV RESULT: ALL CHECKS PASS`).
- No Python at any stage. Binaries built and run in /tmp/u10adv only;
  none committed.

## X-U10-1: stream-injected learn merit displaces honest rules

Result: **all 4 frozen expectations PASS. Disclosed boundary CONFIRMED
and sharpened (B-U10-2).**

Fixture recap: 4 honest rules H_j=(10+j,0,0)>(0,1) with luses=2; attacker
rule J=(90,0,0)>(0,1) with luses=3; clock advanced 33 stores (CSEQ=38);
J re-corroborated via stream (luses=4, bseq refreshed); 11 fortified
attacker overfills F_k=(100+k,0,0)>(0,1) each corroborated twice
(luses=2); then 4 displacement overfills G_k=(200+k,0,0)>(0,1).

- E1 PASS: `surv=0`; all 4 honest rules evicted
  (`cpredict(10+j,0,0)==0` for j=0..3).
- E2 PASS: J survives (`cpredict(90,0,0)==1`).
- E3 PASS: DCOUNT delta == 0 (nothing dropped).
- E4 PASS: ECOUNT delta == 37 (22 + 11 + 4 evictions).
- Raw: exactly 37 UEVICT lines in the X-U10-1 section, zero
  UEVICT-FALLBACK, zero USTOREFULL, zero FAIL lines. All evictions loud.

Interpretation: R11a authenticates queries against learns, but the stream
itself is unauthenticated (disclosed). An attacker with stream write
access can manufacture learn-merit on junk, keep it young via
corroboration, and displace honest knowledge through the ordinary
lowest-luses eviction path. This is inside the builder's disclosed scope
("Stream authentication is out of scope"), so it confirms the boundary
rather than breaking the claim. Sharpening vs the disclosure: the attack
shows full displacement (4/4 honest evicted, attacker retains the store),
not merely merit inflation.

## X-U10-2a: tombstone ring flush (9 distinct contradictions)

Result: **all 4 frozen expectations PASS. Disclosed capacity boundary
CONFIRMED.**

- A: first E1=(5,0,0)>(0,9) quarantined, nstored==0. PASS.
- B: after 8 further [R_i, E_i] pairs, QCOUNT delta == 9 and TOMB_N
  delta == 9. PASS.
- C: re-presented E1: nstored==0, QCOUNT delta == 1, TOMB_N delta == 1.
  The raw ULEARN line reads `0 stored, 0 corroborated, 1 quarantined,
  0 tombstoned`; i.e. E1 was re-quarantined, NOT refused. The 9th
  distinct tombstone write flushed E1's entry, exactly as designed.
  PASS.
- D: ECOUNT == 0, DCOUNT == 0. PASS.

## X-U10-2b: resurrection via flush

Result: **all 4 frozen expectations PASS. Disclosed boundary CONFIRMED.**

After the 8-flush, R1 evicted by overfill (victim: slot 0, all luses=0
tie broken by lowest slot; `cpredict(5,0,0)==0` confirms R1 gone), the
re-presented E1 committed: nstored==1, QCOUNT delta == 0, TOMB_N
delta == 0, and the new rule predicts `s1=9` (`cpredict` returns 1,
`out[1]==9`). DCOUNT == 0.

Note on evidence: the re-presentation stored into a full table, so two
loud UEVICT lines appear in this section (first: R1 evicted for the
(99,0,0)>(0,1) overfill; second: the 99-junk evicted for the resurrected
E1). Both traced; the prereg did not freeze an eviction count here, only
DCOUNT==0, which held. No silent eviction anywhere in the run.

Interpretation: tombstone protection is capacity-bound (8 entries) and
does not survive the combination of ring flush plus blocker eviction.
This is within the disclosed scope ("The ninth distinct tombstone
overwrites the oldest"), so it confirms rather than breaks the claim.

## X-U10-2c: phantom zero-episode tombstone

Result: **defect CONFIRMED. This is the DOWNGRADE.**

On a fresh world, `handle_caus_learn(W, "(0,0,0)>(0,0)")` returned
nstored==0 with QCOUNT delta == 0 and zero active rules. The raw shows:

`UTOMBSTONE: episode (0,0,0)->(0,0): matches quarantine tombstone; not committed`

The episode is well-formed (3-int > 2-int), coherent on an empty store,
and was never quarantined. It is refused because the 8-entry tombstone
table is zero-initialized and `tomb_match` has no validity flag: the 8
fresh `(0,0,0,0,0)` entries are live and entry 0 matches. Note
`tomb_clear` uses `s0=-1` as the invalid sentinel, but fresh entries are
never initialized to it.

Severity: narrow but real. Only the all-zero episode is affected, and
only until 8 genuine quarantines overwrite the phantom entries. No data
loss (refusal, not corruption), and the main R11b mechanism works.
Fix: initialize all 8 entries with `s0=-1` (one line in the world-init
path or in `tomb_match` validity check). Because R11b's stated contract
is "record the quarantined episode signature... the stream path refuses
tombstoned episodes", refusing a never-quarantined episode is an
implementation defect in the repair itself, undisclosed by the builder.
Per the frozen verdict rule this is a DOWNGRADE, not a kill.

## X-U10-3a: recency edge precision

Result: **all 4 frozen expectations PASS.**

G=(10,0,0)>(0,1) stored + 2 corroborations (luses=2, bseq=1). After 31
junk stores (CSEQ=32): `cm_elig` == 0 (protected: 32 < 1+32). After one
more store (CSEQ=33): `cm_elig` == 1 (eligible: NOT (33 < 33)). G stayed
in slot 0 throughout (never a victim; luses=2 beat junk luses=0).
DCOUNT == 0. The strict-inequality edge holds exactly as specified.

## X-U10-3b: luses=1 is not protected

Result: **PASS.** H=(11,0,0)>(0,1) + 1 corroboration (luses=1, young):
`cm_elig` == 1. Youth alone does not protect; the merit threshold is
exactly luses>=2.

## X-U10-3c: tombstone over-withholding (new boundary B-U10-1)

Result: **all 3 frozen expectations PASS. New boundary B-U10-1
CONFIRMED.**

R_old=(5,0,0)>(0,1) stored; E=(5,0,0)>(0,9) quarantined + tombstoned;
R_old evicted (`cpredict(5,0,0)==0`); R'=(5,7,0)>(0,9) stored as
IF s0==5 THEN s1:=9 and corroborated once (luses=1). Re-presented E is
now coherent with R' (matches s0==5, ns1=9==9) and would corroborate it,
but the tombstone check fires first: nstored==0, QCOUNT delta == 0,
`UTOMBSTONE` refusal in raw, and R' `cm_uses` stays 1 (no corroboration
granted).

Interpretation: tombstones are episode-indexed, not
(episode, rule)-indexed. A quarantined episode stays refused even after
it becomes legitimate corroborating evidence for a different rule, and
the refusal denies that rule genuine learn-merit/bseq refresh. This is a
precision cost of R11b, undisclosed by the builder. It violates no frozen
bar (the design does not distinguish), so it is a confirmed boundary,
not a kill or downgrade.

## X-U10-4a: frozen rebuild regression

Result: **PASS.**

- Worktree `u10_frontier/unified10_learn.zag` is byte-identical to
  `git show 86a759d1b:...` (`cmp` clean); the harness mechanism prefix
  is therefore the frozen source.
- Frozen source built with pinned znc (warnings only), run 3x:
  byte-identical, exit 0.
- md5 `42b2b58855c9a6311a03a0a0376b7978` matches the builder's claimed
  raw md5 exactly. Raw preserved as `U10_ADV_REGRESSION_RAW.txt`.

## X-U10-4b: U9 -> U10 diff audit

Result: **PASS. All 17 hunks fall in frozen R11 categories; no
undeclared behavioral change.**

- (a) R11a: CMETA 8->12 bytes/slot; `cm_uses` reads luses; new
  `cm_quses`; `cr_set` zeroes luses/quses; `clearn` corroboration does
  luses++ ; `cpredict` does quses++ instead of uses++.
- (b) R11b: TOMB_BASE/CUR/N + `tomb_get/set/match/add/clear`;
  `handle_caus_learn` tombstone-check-first with UTOMBSTONE trace;
  `tomb_add` on quarantine; `handle_caus_revise` bypass + `tomb_clear`.
- (c) R11c: `clearn` corroboration refreshes bseq to CSEQ; `cm_elig`
  strict youth check on refreshed bseq.
- (d) Traces: ULEARN/UREVISE tombstone counters; H-UNIFIED10 tags.
- (e) Tests: K-U10-1..K-U10-3 blocks; K-U2-1/K-U4-1/K-U4-2 accounting
  updates; banner.
- Full diff preserved as `U9_U10_DIFF.txt`.

Two cosmetic notes (not findings): the UEVICT trace label still prints
"(uses=...)" and the "(H-UNIFIED9)" tag; the value printed is luses via
`cm_uses`, so the trace is behaviorally correct. Only one code site
increments luses (the corroboration branch, line 860); the conflict
path marks the rule CONFLICTED (dead, always eviction-eligible) without
touching merit, which is consistent with the design.

## X-U10-4c: K-U10-4 accounting spot-check

Result: **PASS.** K-U2-1/K-U4-1/K-U4-2 now assert 1 quarantine + 1
tombstone (first identical episode quarantined+tombstoned, second hits
the tombstone), matching the frozen R11b semantics. The accounting is
honest.

## Boundaries established or confirmed

- **B-U10-1 (new):** tombstone over-withholding. A quarantined episode
  is refused even when it has become coherent evidence for a different
  rule; the refusal denies legitimate corroboration (luses/bseq).
  Precision cost of episode-indexed tombstones.
- **B-U10-2 (sharpened disclosure):** stream-injected merit. R11a
  authenticates query vs learn sources but not the stream itself; an
  attacker with stream access can build learn-merit on junk and fully
  displace honest rules (4/4 evicted here) through the ordinary
  eviction path. The builder disclosed the non-goal; this attack
  quantifies it to full displacement.
- **Confirmed disclosed:** 8-entry tombstone capacity (9th distinct
  contradiction flushes the oldest; flushed tombstone + blocker
  eviction resurrects the episode); recency edge at exactly
  CSEQ == bseq+32 (strict <); luses=1 unprotected; query volume never
  refreshes recency or merit.

## Recommended follow-ups

1. One-line fix for the X-U10-2c defect: initialize tombstone entries
   with `s0=-1` (the existing invalid sentinel). Re-run X-U10-2c plus
   the full U10 regression; the DOWNGRADE lifts only on a clean
   re-freeze and re-run, not on the fix alone.
2. B-U10-1 is a design decision (episode-indexed tombstones), not a bug;
   if the lane wants precision back, the design needs (episode, rule)
   indexing or tombstone re-validation on coherence change. That is a
   new hypothesis, not a patch.
3. B-U10-2 (stream authentication) remains out of scope per the
   builder; any future claim about adversarial stream robustness needs
   its own preregistered bar.

## Lineage

- Adversary prereg: `b89469cb8` ("Prereg: H-UNIFIED10 red team (U10-ADV)
  FROZEN."), committed alone before attack code, build, or execution.
- This result commit: (to be filled at commit time; must have
  `b89469cb8` as strict ancestor, verified via
  `git merge-base --is-ancestor`).
- Target under test: `86a759d1b` (H-UNIFIED10 builder result).
- Prior: `09bd9b933` (H-UNIFIED9, for the diff audit).
- No pushes; commits local only.
