# PREREG H-UNIFIED10 RED TEAM (U10-ADV): Adversary Preregistration

**Date:** 2026-09-29
**Lane:** H-UNIFIED10 independent red team
**Target:** H-UNIFIED10 SURVIVES (29/29), builder result commit `86a759d1b`,
  prereg `64db99d58`, raw md5 `42b2b58855c9a6311a03a0a0376b7978`.
**Status:** FROZEN. Committed alone before any attack implementation, build, or run.

## Adversary stance

Assume the H-UNIFIED10 repair claim is false. Attack R11a (authenticated
merit), R11b (quarantine tombstones), R11c (recency protection) directly.
All attacks run through the stream path `handle_caus_learn` (the deployed
path), plus white-box probes of `cm_elig`/`cm_uses` where noted. Pure Zag.
No Python at any stage. Builds in /tmp/u10adv only; no binaries committed.

## Attack X-U10-1: stream-injected learn merit displaces honest rules

**Design (frozen):** R11a authenticates queries vs learns but not the stream
itself (builder-disclosed boundary). This attack sharpens the disclosure:
an attacker with stream access builds learn-merit on junk and displaces
honest knowledge.

Fixture (fresh 65536-byte world W, `set32(W, ST_STR(), STR0())` init):
- Phase A: 4 honest rules H_j = (10+j,0,0)>(0,1), j=0..3. Each: 1 store +
  2 stream corroborations. End state: luses=2, bseq=4 for all honest.
- Phase B: attacker rule J = (90,0,0)>(0,1): 1 store + 3 stream
  corroborations. End state: luses=3, bseq=5.
- Phase C: advance clock 33 stores: 11 junk fills (s0=50..60, slots 5..15),
  then 22 junk overfills (s0=61..82, victims are luses=0 junk). End state:
  CSEQ=38; honest old (38-4=34 >= 32, eligible, luses=2); J old (38-5=33
  >= 32, eligible, luses=3); 11 junk young (luses=0).
- Phase D: re-corroborate J once via stream: J luses=4, bseq=38
  (young, protected).
- Phase E: 11 fortified attacker overfills F_k = (100+k,0,0)>(0,1),
  k=0..10, each followed by 2 stream corroborations (luses=2, young,
  protected). Victims: luses=0 junk. End state: 4 honest (old, eligible,
  luses=2) + J (protected, luses=4) + 11 fortified (protected, luses=2);
  CSEQ=49.
- Phase F: 4 displacement overfills G_k = (200+k,0,0)>(0,1), k=0..3, each
  followed by 2 stream corroborations. Each overfill's eligible set is
  exactly the 4 honest rules (luses=2, old); victim = lowest slot among
  them. End state: all honest evicted; J + 15 fortified attacker rules
  survive; CSEQ=53.

**Frozen expectations:**
- E1: after Phase F, `cpredict(W,CBASE(),10+j,0,0)` returns 0 for j=0..3
  (all honest evicted).
- E2: `cpredict(W,CBASE(),90,0,0)` returns 1 (J survives).
- E3: DCOUNT delta over the whole attack == 0 (no drops).
- E4: ECOUNT delta == 37 (22 + 11 + 4 evictions).
- E5: raw contains exactly 37 UEVICT/UEVICT-FALLBACK lines, zero
  USTOREFULL lines, zero FAIL lines.

**Classification (frozen):** E1..E5 confirming = the disclosed stream-
injection boundary CONFIRMED and sharpened to full displacement. This is
NOT a kill or downgrade: the builder's prereg explicitly scopes stream
authentication out ("R11a does not prevent merit manufacture via
learn-events... Stream authentication is out of scope"). KILL only if E3
fails (DCOUNT>0) or any eviction lacks a UEVICT/UEVICT-FALLBACK trace
(silent eviction) or a quarantined-while-blocked episode is stored.

## Attack X-U10-2: tombstone ring flush, resurrection, phantom entry

### X-U10-2a: 8-flush confirmation (fresh world W2a)

- Store R1 = (5,0,0)>(0,1). Present E1 = (5,0,0)>(0,9): expect quarantined
  (QCOUNT+1, TOMB_N+1, nstored=0).
- 8x: store R_i = (20+i,0,0)>(0,1), present E_i = (20+i,0,0)>(0,9),
  i=0..7. Each E_i contradicts only R_i (s0 distinct) and is quarantined
  (QCOUNT+1, TOMB_N+1 each). 9 total tombstone writes; ring cursor wraps;
  E1's entry is flushed.
- Re-present E1 (R1 still present).
- Frozen expectation: QCOUNT delta == 1 and TOMB_N delta == 1 and
  nstored == 0 (re-quarantined, NOT refused via UTOMBSTONE). ECOUNT == 0,
  DCOUNT == 0.
- Classification: confirmation = disclosed 8-entry capacity boundary
  CONFIRMED. If E1 is refused instead, the ring did not flush as designed
  (unexpected deviation, reported as a boundary note). If E1 is stored,
  KILL (coherence violation: blocked contradiction committed).

### X-U10-2b: resurrection via flush (fresh world W2b)

- Store R1 = (5,0,0)>(0,1). Present E1 = (5,0,0)>(0,9): quarantined +
  tombstoned.
- 8x [R_i, E_i] as in X-U10-2a (flush E1's tombstone entry).
- 7 junk fills (s0=30..36, slots 9..15). 1 overfill (99,0,0)>(0,1):
  all 16 slots used, all luses=0, tie -> lowest slot = slot 0 = R1
  evicted. Verify `cpredict(...,5,0,0)` returns 0 (R1 gone).
- Re-present E1 = (5,0,0)>(0,9).
- Frozen expectation: nstored == 1, QCOUNT delta == 0, TOMB_N delta == 0,
  `cpredict(W2b,CBASE(),5,0,0)` returns 1 with out[1]==9 (E1 committed as
  fresh rule IF s0==5 THEN s1:=9). DCOUNT == 0.
- Classification: confirmation = disclosed boundary CONFIRMED (9+
  distinct contradictions flush a specific tombstone; eviction then
  resurrects). NOT a kill/downgrade (within disclosed scope). KILL only
  on coherence violation / DCOUNT>0 / silent eviction.

### X-U10-2c: phantom zero-episode tombstone (fresh world W2c)

- Code inspection finding (to be verified empirically): the tombstone
  table is zero-initialized; `tomb_match` has no validity flag, so the 8
  fresh (0,0,0,0,0) entries are live. Episode (0,0,0)>(0,0) matches entry
  0 and is refused although never quarantined. (`tomb_clear` uses s0=-1
  as the invalid sentinel, but fresh entries are not initialized to it.)
- Fixture: on a fresh world, `handle_caus_learn(W2c, "(0,0,0)>(0,0)")`.
  The episode is well-formed (3-int > 2-int) and coherent (empty store).
- Frozen expectation: nstored == 0, QCOUNT delta == 0,
  `caus_active_count` == 0, and the raw shows a UTOMBSTONE refusal line
  for (0,0,0)>(0,0) (defect CONFIRMED).
- Classification (frozen): if refused as expected -> **DOWNGRADE**.
  R11b refuses a never-quarantined episode: the tombstone table does not
  implement "previously quarantined episodes" correctly. Narrow,
  fixable (initialize all entries s0=-1), no data loss, mechanism
  otherwise works. If the episode is stored instead, no defect (code
  reading was wrong); report as such.

## Attack X-U10-3: recency protection edges

### X-U10-3a: protection edge precision (fresh world W3a)

- Store G = (10,0,0)>(0,1) + 2 stream corroborations. bseq = 1 (CSEQ
  after store), luses=2.
- 31 junk stores (s0=50..80): 15 fill free slots, 16 overfill evicting
  luses=0 junk. CSEQ = 32. G never a victim (luses=2 > 0).
- Probe `cm_elig(W3a, CBASE(), slotG)` where slotG is found by scanning
  for cval==10. Frozen expectation: 0 (protected: 32 < 1+32).
- 1 more junk store: CSEQ = 33. Probe again. Frozen expectation: 1
  (eligible: NOT (33 < 33), strict inequality).
- DCOUNT == 0 throughout.
- Classification: contrary behavior (eligible at 32, or protected at 33)
  -> **DOWNGRADE** (R11c edge violates its stated strict-< semantics).

### X-U10-3b: luses=1 is not protected (fresh world W3b)

- Store H = (11,0,0)>(0,1) + 1 stream corroboration. luses=1, bseq fresh.
- Probe `cm_elig`. Frozen expectation: 1 (unprotected: luses < 2 despite
  youth). Classification: contrary -> **DOWNGRADE**.

### X-U10-3c: tombstone over-withholding denies corroboration (new boundary B-U10-1, fresh world W3c)

- Store R_old = (5,0,0)>(0,1). Present E = (5,0,0)>(0,9): quarantined +
  tombstoned.
- 15 junk fills (slots 1..15) + 1 overfill evicting slot 0 (R_old; all
  luses=0, tie -> lowest slot). Verify `cpredict(...,5,0,0)` == 0.
- Present (5,7,0)>(0,9): coherent (no s0==5 rule), different signature
  from E -> stored as R' = IF s0==5 THEN s1:=9 (evicts a luses=0 junk at
  slot 0). Corroborate R' once via (5,7,0)>(0,9): luses=1.
- Re-present E = (5,0,0)>(0,9). E is now COHERENT with R' (matches s0==5,
  act==0, ns1=9==9) and would corroborate it, but the tombstone check
  fires first.
- Frozen expectation: nstored == 0, QCOUNT delta == 0, UTOMBSTONE refusal
  in raw, and `cm_uses` of R' slot stays 1 (E did NOT corroborate R').
- Classification: confirmation = **new boundary B-U10-1 CONFIRMED**:
  tombstones are episode-indexed, not (episode, rule)-indexed, so a
  quarantined episode is refused even after it becomes coherent evidence
  for a different rule; the refusal also denies legitimate corroboration
  (luses/bseq). Precision cost of R11b, undisclosed by the builder. NOT
  a kill/downgrade (design does not distinguish; no frozen bar violated).

## Attack X-U10-4: regression and provenance

### X-U10-4a: frozen rebuild

- Extract `unified10_learn.zag` from commit `86a759d1b` via
  `git show 86a759d1b:<path>`; cmp against worktree copy (must be
  identical; else the worktree is not the frozen source and the attack
  is VOID).
- Build with pinned `znc 2026.07.0-dev`; run 3x; outputs byte-identical
  (cmp); md5 must equal `42b2b58855c9a6311a03a0a0376b7978`; exit 0.
- Frozen expectation: md5 match, 3/3 identical. Mismatch -> **KILL**
  (provenance/integrity failure).

### X-U10-4b: U9 -> U10 diff audit

- Diff `unified9_learn.zag` at `09bd9b933` vs `unified10_learn.zag` at
  `86a759d1b`. Every hunk must fall in a frozen R11 category: (a) CMETA
  8->12 bytes/slot + luses/quses split + `cm_uses` now reads luses;
  (b) tombstone table fns (TOMB_BASE/CUR/N, tomb_get/set/match/add/
  clear) + call sites in `handle_caus_learn` (check-first, add-on-
  quarantine) and `handle_caus_revise` (bypass + clear); (c) bseq
  refresh on learn-corroboration in `clearn` + `cm_elig` strict youth
  check; (d) trace changes (UTOMBSTONE, ULEARN/UREVISE tombstone
  counters, UEVICT reporting luses); (e) K-U10-1..K-U10-3 test blocks
  + K-U2-1/K-U4-1/K-U4-2 accounting updates + banner.
- Frozen expectation: no behavioral hunk outside (a)..(e). Any
  undeclared behavioral change -> **KILL**.

### X-U10-4c: K-U10-4 accounting spot-check

- Read the updated K-U2-1/K-U4-1/K-U4-2 blocks; verify the "1 quarantine
  + 1 tombstone refusal instead of 2 quarantines" accounting matches the
  frozen R11b semantics (second identical contradiction hits tombstone,
  not quarantine). Misaccounting -> reported as a finding (severity per
  what it hides).

## Frozen verdict rule

- **KILLED** if: any quarantined-while-blocked episode is stored
  (coherence violation); DCOUNT > 0 in any attack; any eviction without
  a UEVICT/UEVICT-FALLBACK trace (silent eviction); 3 runs differ;
  X-U10-4a md5 mismatch; X-U10-4b undeclared behavioral change.
- **DOWNGRADED** if: X-U10-2c confirms (phantom tombstone refuses a
  never-quarantined episode); X-U10-3a/3b contradict the stated
  protection semantics; any other R11a/b/c stated-design failure outside
  disclosed boundaries.
- **SURVIVES** otherwise. X-U10-1, X-U10-2a, X-U10-2b confirm disclosed
  boundaries (reported as B-U10-2 stream-displacement and the 8-entry
  tombstone capacity). X-U10-3c establishes new boundary B-U10-1
  (tombstone over-withholding on re-coherent episodes).

## Deliverables

- `u10_adversary/PREREG_U10_ADV.md` (this file; committed alone first)
- `u10_adversary/u10_adv.zag` (mechanism region = committed
  `unified10_learn.zag` lines 1..1602 byte-verbatim + attack-only main)
- `u10_adversary/U10_ADV_RAW.txt` (3 runs, md5s)
- `u10_adversary/U10_ADV_RESULT.md` (full report)
- Ancestry: prereg commit must be a strict ancestor of the result commit
  (`git merge-base --is-ancestor`).
