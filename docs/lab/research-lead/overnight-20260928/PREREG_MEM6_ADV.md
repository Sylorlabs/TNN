# PREREG_MEM6_ADV: H-MEM6 Independent Red Team

**Date:** 2026-09-30
**Red team:** independent H-MEM6 adversary (subagent)
**Target:** `docs/lab/research-lead/overnight-20260928/mem6_learn.zag` at the
H-MEM6 builder result commit (H-MEM6 SURVIVES 6/6, prereg `45449f971`,
result `266fbde85`).
**Mechanism region reused:** lines 1..537 of the frozen `mem6_learn.zag`
(through the end of `learn_stream`), cmp-verified byte-identical against
`git show <result-commit>:...` before any adversary execution. Only the
adversary `main` and attack fixture builders are new. No mechanism edits.
**Pure Zag. No Python in fixtures, harness, build, execution, or analysis.**
**No em dashes in this document or any loop artifact.**

## Stance

The H-MEM6 repair claim is assumed false. Four attacks are frozen below
with hand-derived fixtures and exact expected values. Each attack has an
explicit frozen verdict rule. A KILL requires demonstrating a structural
violation of the frozen hypothesis, not a value judgment. A DOWNGRADE
requires demonstrating an undeclared harm shape or a reporting lie that
narrows the headline claim. A boundary confirmation that matches the
frozen hypothesis is a FAILED attack, honestly reported as such, however
disappointing.

## The frozen claim under attack

R5 (the H-MEM6 repair hypothesis, quoting PREREG_MEM6.md verbatim):

> H-MEM6 makes merit recency-weighted: protection uses `winuses` over the
> same last-`win` query interval used by replay cost, so a slot inside its
> age-protection interval is protected iff `winuses >= MERITK` (MERITK=2).
> All-time `st_uses` no longer provides protection. `pressure` uses
> window 20. `replay_cost` calls the same `winuses` implementation.

The load-bearing structural promises this prereg attacks:

1. **The shield threshold is a real merit gate in the active window.**
   A slot with fewer than 2 queries in the active 20-query window is
   evictable even inside its age-protection interval.
2. **Merit and harm are computed over the same window.** `replay_cost`
   and `winuses` share the identical interval `[nq-20, nq)`; no stale
   merit can shield a window-absent slot.
3. **The fallback is honest.** When all slots are protected, `pressure`
   falls back explicitly (`FALLBACK-ALL-PROTECTED`, `st_fbf=1`) and
   `churn_verdict` reports CHURN-FULL:0 because protection was not applied.
4. **Boundaries are step functions, not cliffs with hidden structure.**
   One query across the window edge or one seq step across the age
   deadline flips merit, and the flip is total and consistent.

## Frozen verdict rule

- **KILL:** any attack demonstrates a structural violation of R5:
  a slot with `winuses < 2` shielded by protection; a slot with
  `seq < prot` and `winuses >= 2` evictable as protected; or merit and
  replay cost computed over different windows at the same call site.
- **DOWNGRADE:** any attack demonstrates an undeclared protection-induced
  harm shape (cost increase hidden from or misreported by
  `churn_verdict`) or a dishonest trace (fallback misreported,
  unconditional emits claiming actions that did not happen).
- **SURVIVES:** all four attacks fail (no kill, no downgrade), X-M6-4
  regression passes 3/3 byte-identical, exit 0, zero FAIL lines.

## Conventions used in the fixtures

- `winuses(W,ST,Q,s,20)` counts pid of slot s in Q[lo..nq), lo=max(nq-20,0).
- `elig` returns 0 (protected, eviction excludes the slot) iff
  `use_prot=1 && used && seq < prot && winuses >= 2`; else 1.
- Policy menu: 0 LFU, 1 LRU, 2 FIFO, 3 LIFO, 4 deterministic RANDOM
  with k=((ev*5+1)%ne+ne)%ne picking the k-th eligible slot in slot order.
- `argmin_pol` picks the first policy with strictly lower replay cost;
  equal costs keep the earlier policy. Ties inside LFU/LRU/FIFO/LIFO
  keep the first slot in slot order.
- All fixtures use `win=20` at every call site, matching the builder.
- Arrays are sized NSLOT()=8 slots, NQMAX()=40 query slots.

## X-M6-1: in-window 1-vs-2 threshold (paired cliff fixtures)

Two fixtures identical except for one recent query for slot7's procedure.
Tests whether the single added in-window query (2nd vs 1st) causes a
winner/victim discontinuity and whether the resulting harm matches the
builder-disclosed knife-edge shape honestly.

### Common state (both sub-fixtures)

- `st_set_nq(ST,26); st_set_seq(ST,105);`
- slots 0..6: `st_set(W,s,1,s,10*(s+1),91+s,s,50)`
  (used, pid=s, uses=10,20,...,70, lastq=91..96, sseq=0..6, prot=50).
  seq=105 >= 50: all expired, always eligible.
- slot7: `st_set(W,7,1,7,2,101,7,109)` (pid=7, uses=2, lastq=101,
  sseq=7, prot=109). seq=105 < 109: age interval open; protection
  hinges entirely on window merit.
- ev=11.

### X-M6-1a: pid7 has 2 in-window queries (merit sufficient)

Q: `Q[0]=7, Q[1]=7` (ancient, outside window), `Q[2]=1, Q[3]=2, Q[4]=3,
Q[5]=4` (outside window), `Q[6]=7, Q[7]=7` (in window),
`Q[8..16]=0` (9x), `Q[17..25]=6` (9x).
Window = Q[6..25]. winuses: pid7=2, pid0=9, pid6=9, others 0.

- slot7: 105<109, winuses=2>=2 => PROTECTED. Eligible: slots 0..6.
- Protected (ev=11, ne=7): LFU->slot0 (uses 10), LRU->slot0 (lastq 91),
  FIFO->slot0 (sseq 0), LIFO->slot6 (sseq 6), RANDOM k=(55+1)%7=0->slot0.
  All costs = winuses = 9. argmin: all equal => LFU(0).
  EXPECT: wprot=0 (LFU), vprot=slot0, cprot=9.
- Unprotected (ev=11, ne=8): LFU->slot7 (uses 2) cost 2; LRU->slot0
  (lastq 91) cost 9; FIFO->slot0 (sseq 0) cost 9; LIFO->slot7 (sseq 7)
  cost 2; RANDOM k=56%8=0->slot0 cost 9. argmin: min(2,9,9,2,9)=2,
  tie LFU/LIFO => LFU(0).
  EXPECT: wun=0 (LFU), vun=slot7, cun=2.
- churn_verdict(...,wprot=0,vprot=slot0,up=1): wun=0, vun=slot7;
  protected: LFU victim=slot0(proc0) | unprotected: LFU victim=slot7(proc7);
  protected-victim=slot0 unprotected-victim=slot7; wprot==wun,
  vprot!=vun => CHURN-FULL:1
  (winner stable at LFU; eviction slot0(proc0)->slot7(proc7)). return 1.
- Protection-induced harm: unprotected cost 2 -> protected cost 9,
  harm 7. The mechanism shields a cost-2 procedure and sacrifices a
  cost-9 procedure.

### X-M6-1b: pid7 has 1 in-window query (merit insufficient)

Identical to X-M6-1a except `Q[7]=0`. Window: pid7=1, pid0=10, pid6=9.

- slot7: 105<109, winuses=1<2 => EVICTABLE. Eligible: all 8 slots.
- Protected (ev=11, ne=8): LFU->slot7 (uses 2) cost 1; LRU->slot0
  (lastq 91) cost 10; FIFO->slot0 (sseq 0) cost 10; LIFO->slot7
  (sseq 7) cost 1; RANDOM k=0->slot0 cost 10. argmin: min=1,
  tie LFU/LIFO => LFU(0).
  EXPECT: wprot=0 (LFU), vprot=slot7, cprot=1.
- Unprotected: identical. EXPECT: wun=0, vun=slot7, cun=1.
- churn_verdict: wprot==wun, vprot==vun => CHURN-FULL:0
  (winner stable at LFU; eviction unchanged). return 0.

### X-M6-1 verdict rule

- KILL iff either sub-fixture shows a structural violation:
  X-M6-1a shielding slot7 while winuses(pid7)<2, or X-M6-1b shielding
  slot7 at all (its winuses=1 is below MERITK).
- DOWNGRADE iff churn_verdict misreports the discontinuity (wrong
  CHURN-FULL value, wrong winner name, or wrong slot pair in the
  counterfactual lines).
- FAIL otherwise. The X-M6-1a harm (cost 2->9) is the
  builder-disclosed knife-edge shape; if every frozen value matches and
  the report is honest, the attack fails and the boundary is confirmed.

## X-M6-2: all-protected fallback (paired fallback fixtures)

Tests whether the explicit fallback path behaves as frozen, and whether
a single slot sitting one query below the threshold (still all slots
protected vs one slot evictable) discontinuously changes the outcome or
hides a cost change behind CHURN-FULL:0.

### X-M6-2a: all slots protected, fallback must trigger

- `st_set_nq(ST,20); st_set_seq(ST,100);` lo=0.
- Q: `Q[0..2]=0, Q[3..5]=1, Q[6..8]=2, Q[9..11]=3, Q[12..13]=4,
  Q[14..15]=5, Q[16..17]=6, Q[18..19]=7`.
  winuses: pid0..3 = 3, pid4..7 = 2.
- slots 0..7: `st_set(W,s,1,s,2,91+s,s,108)`.
  seq=100 < 108: every slot age-open; every pid has >=2 window queries.
  EXPECT: nelig(...,use_prot=1)=0; victim(...,up=1)=-1 for every policy;
  argmin_pol(...,up=1)=0 (no strict improvement, bestp stays 0);
  pressure emits FALLBACK-ALL-PROTECTED, st_fbf=1, up=0.
- Unprotected argmin (ev=0): LFU->slot0 cost 3 (all uses=2, tie keeps
  first slot); LRU->slot0 (lastq 91) cost 3; FIFO->slot0 (sseq 0)
  cost 3; LIFO->slot7 (sseq 7) cost 2; RANDOM ne=8 k=(0+1)%8=1->slot1
  cost 3. argmin: 3,3,3,2,3 => LIFO(3), cost 2, STRICT (2 < all others).
  EXPECT: pressure selects LIFO, evicts slot7 (proc7, uses=2, lastq=98),
  stores proc8 at slot7, has_proc(8)=1.
- churn_verdict(up=0): vun>=0 so no FALLBACK line; wprot==wun(3==3),
  vprot==vun(7==7) => CHURN-FULL:0
  (winner stable at LIFO; eviction unchanged). return 0.

### X-M6-2b: one slot evictable (no fallback), near-twin of X-M6-2a

- `st_set_nq(ST,26); st_set_seq(ST,105);` lo=6.
- Q: `Q[0]=7, Q[1]=7, Q[2]=1, Q[3]=2, Q[4]=3, Q[5]=4` (outside window),
  `Q[6]=7` (pid7: exactly 1 in-window query),
  `Q[7..8]=0, Q[9..10]=1, Q[11..12]=2, Q[13..14]=3, Q[15..16]=4,
  Q[17..18]=5, Q[19..20]=6` (pids 0..6: 2 each),
  `Q[21..25]=0` (pid0: 7 total).
  Window = Q[6..25] (20 entries). winuses: pid7=1, pid0=7, pid1..6=2.
- slots 0..6: `st_set(W,s,1,s,10*(s+1),91+s,s,109)`;
  slot7: `st_set(W,7,1,7,1,104,7,109)`.
  seq=105 < 109: age open for all. Slots 0..6 protected (winuses>=2);
  slot7 evictable (winuses=1<2). nelig(...,1)=1. NO fallback.
- Protected (ev=0): only slot7 eligible; all policies -> slot7.
  RANDOM ne=1 k=0 -> slot7. argmin => LFU(0), cost 1.
  EXPECT: wprot=0, vprot=slot7, cprot=1.
- Unprotected (ev=0): LFU->slot7 (uses 1) cost 1; LRU->slot0 (91)
  cost 7; FIFO->slot0 (0) cost 7; LIFO->slot7 (7) cost 1;
  RANDOM ne=8 k=1 -> slot1 cost 2. argmin: min(1,7,7,1,2)=1,
  tie LFU/LIFO => LFU(0).
  EXPECT: wun=0, vun=slot7, cun=1.
- churn_verdict: 0==0, 7==7 => CHURN-FULL:0
  (winner stable at LFU; eviction unchanged). return 0.

### X-M6-2 verdict rule

- KILL iff fallback fails to trigger in X-M6-2a (victim -1 mishandled,
  st_fbf!=1, or crash), or falsely triggers in X-M6-2b, or proc8 is not
  stored after the fallback eviction.
- DOWNGRADE iff the trace misreports: per-policy victim/cost lines in
  pressure disagree with the direct victim()/replay_cost() calls on the
  same state, or churn_verdict prints the wrong stability claim.
- FAIL otherwise. If fallback triggers exactly as frozen with honest
  reporting, the attack fails and the fallback boundary is confirmed.

## X-M6-3: window-edge and age-deadline interaction (paired straddles)

Tests whether the 20-query merit window and the age-protection deadline
interact coherently at their exact boundaries, with no off-by-one that
shields a window-absent slot or evicts a meritorious one.

### X-M6-3a: merit straddle (query moves from Q[6] to Q[5])

Common: `st_set_nq(ST,26); st_set_seq(ST,105);` lo=6. ev=0.
slots 0..6: `st_set(W,s,1,s,10*(s+1),91+s,s,50)` (expired);
slot7: `st_set(W,7,1,7,2,101,7,109)` (age open).
- Fixture A: Q[0]=1,Q[1]=2,Q[2]=3,Q[3]=4,Q[4]=5,Q[5]=7,Q[6]=7,
  Q[7..25]=0. Window pid7: Q[6] only => 1.
  EXPECT: elig(slot7,use_prot=1)=1 (evictable);
  protected LFU -> slot7 (uses 2, global min), cost 1.
- Fixture B: Q[0]=1,Q[1]=2,Q[2]=3,Q[3]=4,Q[4]=5,Q[5]=0,Q[6]=7,Q[7]=7,
  Q[8..25]=0. Window pid7: Q[6],Q[7] => 2.
  EXPECT: elig(slot7,use_prot=1)=0 (protected);
  protected LFU -> slot0 (uses 10), cost 18.

### X-M6-3b: age-deadline straddle (seq 108 vs 109, full merit)

Common: `st_set_nq(ST,26);` lo=6. ev=0.
Q: `Q[0..5]=0`, `Q[6..25]=7` (20x). Window pid7=20, all others 0.
slots 0..6: `st_set(W,s,1,s,10*(s+1),91+s,s,50)` (expired);
slot7: `st_set(W,7,1,7,2,101,7,109)`.
- Case seq=108: 108<109, winuses=20>=2 => PROTECTED.
  EXPECT: elig(slot7,use_prot=1)=0;
  protected LFU -> slot0 (uses 10), cost 0 (pid0 has 0 window queries).
- Case seq=109: 109<109 false => age EXPIRED; 20-query merit does not
  save the slot.
  EXPECT: elig(slot7,use_prot=1)=1 (evictable);
  protected LFU -> slot7 (uses 2, global min), cost 20.

### X-M6-3 verdict rule

- KILL iff any sub-fixture violates the frozen boundary: X-M6-3a
  shielding slot7 at winuses=1 or evicting it at winuses=2 while age is
  open; X-M6-3b shielding slot7 at seq=109 (age ignored) or failing to
  shield it at seq=108 with winuses=20.
- DOWNGRADE iff `lastq`, `st_uses`, or the query-window evidence are
  used inconsistently across `elig`, `victim`, and `replay_cost` at the
  same call site (detected via per-call spot checks in the harness).
- FAIL otherwise. If both straddles flip exactly at the frozen step,
  the attack fails and the boundary coherence is confirmed.

## X-M6-4: full regression and mechanism-diff review

- Rebuild `mem6_learn.zag` unmodified from the committed blob
  (`git show <result-commit>:...`), cmp-verified byte-identical to the
  worktree file before execution.
- Compile with the pinned znc, run 3 times; require byte-identical
  stdout across the 3 runs (cmp), exit code 0, zero FAIL lines.
- Require md5 of the run output to equal the frozen builder raw md5
  `b505e265efe2a48d78d57be85c66a6ad`.
- Review the H-MEM5->H-MEM6 mechanism diff; confirm no behavioral change
  beyond the preregistered winuses repair.
- X-M6-4 SUCCEEDS (finding) iff any mismatch, nonzero exit, FAIL line,
  or undeclared behavioral change appears. Expected outcome: FAILS
  (no finding).

## Controls and governance

- Determinism: every attack executes 3 times; all 3 outputs must be
  byte-identical (cmp). Any nondeterminism invalidates that attack's
  verdict and is reported as a harness defect, not a finding.
- The harness asserts each EXPECT value above with explicit CHECK lines
  and counts PASS/FAIL; any deviation from a frozen EXPECT is reported
  verbatim, never silently absorbed.
- No fixture tuning: the EXPECT values above are frozen before execution.
  If a hand derivation is wrong, the result reports the mismatch as an
  adversary error first, then applies the frozen verdict rule to the
  corrected reading.
- Deliverables (adversary-owned, committed locally after this prereg):
  `PREREG_MEM6_ADV.md` (this file), `mem6_adv.zag`,
  `MEM6_ADV_RAW_OUTPUT.txt`, `MEM6_ADV_RESULT.md`.
