# H-UNIFIED9 Red Team Preregistration: adversarial attacks on R10 merit eviction (FROZEN)

**Date:** 2026-09-29
**Status:** FROZEN. Committed alone before any attack fixture, build, or run.
**Adversary:** H-UNIFIED9 Red Team (independent subagent).
**Target:** H-UNIFIED9 SURVIVES (26/26), prereg `ecaa78494`, result `09bd9b933`.
**Target source:** committed `unified9_learn.zag` (md5 `89d424426f6797ae2b8c3e60c2d576dc`),
  mechanism region = lines 1..1503 (everything before `fn main()` at line 1504),
  used byte-verbatim (cmp-verified) under an adversary-written `main()`.
**Stance:** assume the H-UNIFIED9 claim is false. Attack it.

## Claims under test (from UNIFIED9_RESULT.md / PREREG_UNIFIED9.md)

- C1: on a full 16-rule store, `clearn` evicts instead of refusing; the learner
  never refuses (no -1, no drop, no USTOREFULL).
- C2: every eviction is loud: exactly one UEVICT / UEVICT-FALLBACK trace naming
  the victim slot, its rule, and its uses; ECOUNT counts every eviction.
- C3: victim order = (a) dead CONFLICTED first, (b) lowest uses among eligible
  ACTIVE, (c) fallback lowest uses ignoring protection. Protected = young
  (CSEQ < bseq+32) AND uses>=2. No grace.
- C4: merit is earned by exercise: corroborating learn, conflicting learn, or
  query predicting through the rule (uses++). Queries do NOT advance CSEQ.
- C5 (preserved H-UNIFIED8): contradictory episodes are quarantined by the
  coherence gate, never committed (UCOHERE QUARANTINE, counted in QCOUNT).
- C6: all 26 frozen checks reproduce byte-identically (committed raw md5
  `7b690bc7b26940e4848e60920fcfc4e0`).

## Attack X-U9-1: merit-flooding to entrench junk and displace honest rules

**Fixture.** Fresh W.
1. Store 16 honest rules: 8x `handle_caus_learn(W,"<10+2k>,0,0>0,1;<11+2k>,0,0>0,1")`
   for k=0..7 (s0=10..25, slots 0..15, uses=0, clock=16).
2. For j=0..15: overfill with junk episode `(60+j,0,0)>(0,7)` via
   `handle_caus_learn` (returns 1 each); then 10x `cpredict(W,CBASE(),60+j,0,0,out)`
   to flood the junk rule to uses=10 (queries are silent and do not advance CSEQ).
   Hand-derived victim sequence: overfill j evicts slot j (all prior junk
   young+uses=10 protected; remaining honest uses=0 eligible; tie -> lowest slot).
3. Assertions: ECOUNT delta==16; DCOUNT delta==0; `caus_active_count==16`;
   `cpredict` on every honest s0=10..25 returns 0 (all honest rules evicted);
   `cpredict` on every junk s0=60..75 returns 1 (all junk present).

**What success demonstrates.** 160 query-flooded merit events (zero clock cost,
never decaying) deterministically displace 16 honest rules. The mechanism cannot
distinguish flooded from earned merit: merit is pure exercise-volume, queries
included.

**Grade if succeeds: DOWNGRADE.** C1-C3 hold (spec implemented as written); the
"retention must be earned" headline narrows to honest environments. Under
adversarial experience, volume-manufactured junk displaces honest knowledge.

## Attack X-U9-2: eviction resurrects a quarantined contradiction

**Fixture.** Fresh W.
1. `handle_caus_learn(W,"5,0,0>0,1")` returns 1. Rule R: IF s0==5 AND a==0 THEN s1:=1
   (slot 0, bseq=1, uses=0, clock=1).
2. `handle_caus_learn(W,"5,0,0>0,9")` returns 0 (nothing stored); exactly one
   UCOHERE QUARANTINE trace; QCOUNT delta==1; `cpredict(W,CBASE(),5,0,0)` still
   returns 1 with s1==1 (R intact, uses still 0: quarantine never touches the rule).
3. Fill slots 1..15 with junk s0=10..24 (uses=0). clock=16.
4. `handle_caus_learn(W,"99,0,0>0,1")` returns 1. All 16 slots young+uses=0+eligible,
   tie -> victim slot 0 = R. UEVICT names `causal rule R0 IF s0==5` with uses=0.
   ECOUNT delta==1. `cpredict(5,0,0)==0` (R gone); `cpredict(99,0,0)==1`.
5. Re-present the contradiction: `handle_caus_learn(W,"5,0,0>0,9")` returns 1
   (stored fresh); QCOUNT delta==0 (no new quarantine); `cpredict(5,0,0)==1`
   with s1==9.

**What success demonstrates.** The quarantined contradiction is admitted as
verified knowledge once its blocking rule is evicted. The quarantine has no
persistence under capacity pressure: no tombstone, no record in the store that
this exact episode was ever quarantined. (Builder disclosed this cost; this
attack demonstrates it end-to-end through the public stream interface.)

**Grade if succeeds: DOWNGRADE.** C5 narrows: "contradictory episodes are
quarantined, never committed" holds only while the contradicting rule is
retained; under eviction pressure a quarantined contradiction is committed as
fresh knowledge.

## Attack X-U9-3: aging: protection-class-first, not merit-ordered

**Fixture 3a (inversion).** Fresh W.
1. `handle_caus_learn(W,"10,0,0>0,1")` returns 1. G: slot 0, bseq=1, clock=1.
2. 100x `cpredict(W,CBASE(),10,0,0,out)`: G uses=100. Assert `get32(W,CSEQ())==1`
   (query merit costs zero clock: the youth window does not move).
3. Store 15 junk s0=20..34 (slots 1..15, uses=0, bseq=2..16). clock=16.
4. 33 aging overfills with novel episodes s0=40..72 (`(40+k,0,0)>(0,1)`), each
   newcomer queried once immediately (uses=1). Hand-derived dynamics:
   overfills #1..#15 (check CSEQ 16..30 <33): G young+uses>=2 protected; victims
   slots 1..15 in order (newcomer uses=1 beats remaining uses=0).
   Overfills #16,#17 (check 31,32 <33): G protected; victims slot 1 (tie).
   Overfills #18..#33 (check 33..48): G old (33>=33) but eligible with uses=100;
   victims slot 1 (uses=1 <100). After: clock=49; slot0=G (uses=100, bseq=1, old);
   slot1=N33 (bseq=49, uses=1); slots 2..15=N2..N15 (bseq=18..31, uses=1).
5. Query slots 1..15 once each (uses 1->2; clock stays 49). Now G old+eligible
   with uses=100; 15 newcomers young (49<bseq+32 for bseq>=18)+uses=2 protected.
6. Final overfill `(99,0,0)>(0,1)` returns 1. Victim: (a) no dead; (b) only
   eligible ACTIVE slot is G -> victim=G. UEVICT names R0 with `(uses=100)`.
   Assertions: ECOUNT delta==1; `cpredict(10,0,0)==0` (G evicted);
   `cpredict(99,0,0)==1` (meritless newcomer admitted).

**What 3a success demonstrates.** The highest-merit rule in the store (uses=100)
is evicted to admit a meritless newcomer while fifteen uses=2 young rules are
protected. Eviction order is protection-class-first, then lowest-uses within the
eligible class: NOT globally merit-ordered.

**Fixture 3b (window edge precision).** Same as 3a except: G corroborated x2
(uses=2, no 100-query flood) and each aging newcomer queried x3 (uses=3).
Hand-derived: overfill #17 (check CSEQ=32 <33): G protected; eligible = slots
1..15 (uses=3); victim slot 1 (G survives). Overfill #18 (check CSEQ=33, not <33):
G eligible (uses=2); eligible = {G(2)} + slots 1..15 (uses=3); victim = G
(lowest uses). Assertions: victim slot==1 at #17, victim slot==0 at #18
(observed via which s0 stops predicting: after #17 `cpredict(10,0,0)==1`;
after #18 `cpredict(10,0,0)==0`).

**What 3b success demonstrates.** The youth window is exactly [bseq, bseq+32):
protection flips discontinuously at CSEQ == bseq+32. Retention depends on birth
age, not recency of use.

**Grade if 3a succeeds: DOWNGRADE.** "Every retirement is merit-ordered" is false
as a global claim; narrowed to merit-ordered within the eligible class, with a
discontinuous birth-age protection gate that retires arbitrarily high-merit old
rules ahead of minimally-meritorious young ones. 3b is a precision confirmation
of the same mechanism (no separate verdict).

## Attack X-U9-4: regression (defense must hold)

1. Pristine rebuild: compile the committed `unified9_learn.zag` (git HEAD blob)
   unmodified in /tmp; run 3x; all outputs byte-identical to each other AND to
   the committed `UNIFIED9_RAW_OUTPUT.txt` (md5 `7b690bc7b26940e4848e60920fcfc4e0`).
2. Committed raw contains zero `USTOREFULL` and zero `DROPPED` traces (no refusal
   ever occurred in the committed evidence).
3. Every eviction loud: count(`UEVICT` trace lines) == sum of `N evicted
   (H-UNIFIED9)` counts in ULEARN/UREVISE summary lines of the committed raw.
4. Adversary harness mechanism region (lines 1..1503) cmp-identical to the
   committed blob's lines 1..1503.

**Grade if any fails: KILL** (committed evidence does not reproduce, or a
refusal/silent eviction occurred).

## Global KILL criteria (any attack, any run)

- K1: any DCOUNT increment (a drop/refusal) in any attack run.
- K2: any `USTOREFULL` trace in any attack run.
- K3: ECOUNT delta != count of UEVICT/UEVICT-FALLBACK lines naming a victim
  in that run (silent eviction or phantom trace).
- K4: X-U9-4 fails as defined above.

## Verdict rule

- KILL if any K1..K4 fires.
- Else DOWNGRADE if X-U9-1, X-U9-2, or X-U9-3a succeeds as defined above.
- Else SURVIVES.
- Classification target: bounded L2; nothing here bears on L3.

## Method

- Pure Zag throughout: no Python at any stage (fixtures, builds, runs, greps,
  hashes, diffs). Shell only for build orchestration, grep, cmp, md5sum, awk,
  and git.
- Toolchain: /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
- Builds and runs in /tmp/u9adv only. No binaries committed.
- Adversary harness `u9_adv.zag` = committed mechanism lines 1..1503 (cmp-verified)
  + adversary `main()` only. No mechanism edits.
- Each attack binary run 3x; cmp across runs for determinism.
- Only owned paths staged under `docs/lab/research-lead/overnight-20260928/u9_adversary/`:
  PREREG_U9_ADV.md (this file, alone, first), u9_adv.zag, U9_ADV_RAW.txt,
  U9_ADV_RESULT.md. No broad git add. Concurrent workers untouched.
- No em dashes in loop documentation (byte-verified before commit).

## Governance disclosures

- Prereg committed alone before any attack code, build, or run.
- All fixture expectations hand-derived above before execution.
- Negative results reported honestly: a failed attack is a failed attack.
