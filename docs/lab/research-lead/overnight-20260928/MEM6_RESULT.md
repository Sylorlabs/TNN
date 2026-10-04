# MEM6_RESULT.md -- H-MEM6: recency-weighted merit (builder result)

Verdict: H-MEM6 SURVIVES, 6/6 frozen kill bars. The H-MEM5 red-team
downgrade (X-M5-1 cost harm 0 -> 2, X-M5-2 one-query cliff) is repaired
by the preregistered mechanism. No em dashes are used in this file
(loop documentation rule).

## 1. Lineage

- Red-team finding: PREREG_MEM5_ADV.md (H-MEM5 red team, DOWNGRADE).
  H-MEM5 prereg: 0e457c276. H-MEM5 result: e5b786c65.
- H-MEM6 prereg: PREREG_MEM6.md, frozen alone in commit 45449f971
  BEFORE any H-MEM6 implementation, build, or execution.
- H-MEM6 implementation: mem6_learn.zag (this directory).
- H-MEM6 evidence: MEM6_RAW_OUTPUT.txt (this directory), three
  byte-identical runs, exit 0, zero FAIL lines.
- mem5_learn.zag is untouched (md5 918e40cb6690ecce0ed41867e57f8ea3);
  the H-MEM5 evidence stands as committed.
- Toolchain: znc 2026.07.0-dev (edition 2026), pure Zag throughout.
  No Python was used anywhere: no generators, no verifiers, no
  analysis scripts, no scratch computation. Hand derivations were done
  by reading the source; scratch validation used only the Zag compiler
  and shell diff/cmp/md5sum.

## 2. The repaired defect (what the red team proved)

H-MEM5 protected a slot within its age window iff all-time uses >= 2
(st_uses). Replay harm was computed over the 20-query operating window.
The scope mismatch: X-M5-1's slot7 had uses=2, both queries ancient and
absent from the active window. Protection shielded slot7 (cost-0
eviction target) and sacrificed slot6 (a queried procedure): cost harm
0 -> 2. X-M5-2 showed a one-query cliff: uses=1 vs uses=2 (all-time)
flips the outcome even when the marginal query is ancient.

## 3. The repair (R5, exactly as preregistered)

New function winuses(W,ST,Q,s,win): count of queries for slot s's
procedure in Q[max(0,nq-win)..nq), the same window replay_cost uses.

elig() is now: eviction-eligible iff stored and (not protected, or
seq >= prot, or winuses < MERITK). Within the age window a slot is
protected iff winuses >= MERITK (2). All-time uses alone no longer
protect: stale merit expires.

Threading: Q and win were threaded through elig, nelig, victim, and
every caller (argmin_pol, select_win, is_strict_up, fut_score2,
fut_score3, churn_verdict, pressure, main). pressure uses win=20 (its
hardcoded operating window); every main() victim call site uses
win=20. replay_cost was refactored to share winuses() with elig()
(identical loop, one implementation), so protection merit and eviction
harm are computed over the same evidence window. MERITK stays 2; only
the evidence scope changed (all-time -> window).

Source delta vs mem5_learn.zag: 310 changed lines (1150 vs 990 total
lines). The mechanism change itself is ~40 lines (winuses, elig,
replay_cost refactor, signature threading); the rest is the two
superseding fixtures and two new kill-bar sections.

## 4. Frozen kill bars and raw results

### K-M6-1: stale merit expires (X-M5-1 fixture)

Hand-derived before execution: winuses(proc7)=0 < 2, so slot7 is
evictable under protection. Protected LFU -> slot7 at cost 0;
unprotected LFU -> slot7; verdict 0.

Raw (from MEM6_RAW_OUTPUT.txt):
```
=== K-M6-1: X-M5-1 fixture (stale merit expires) ===
stale-merit: wprot=LFU vprot=slot7 wun=LFU vun=slot7 cprot=0
  [full counterfactual] protected: LFU victim=slot7(proc7) | unprotected: LFU victim=slot7(proc7)
  [selected-policy] protected-victim=slot7 unprotected-victim=slot7
  CHURN-FULL:0 (winner stable at LFU; eviction unchanged)
K-M6-1 PASS: stale merit expires; protected LFU evicts slot7 at cost 0
```
K-M6-1 PASS. The X-M5-1 cost-0->2 harm does not occur: protected and
unprotected modes agree, LFU evicts the stale-merit slot at cost 0.

### K-M6-2: no cliff at the margin (X-M5-2a uses=1, X-M5-2b uses=2)

Hand-derived before execution: both variants are window-absent
(winuses=0), so the 1->2 all-time flip changes nothing; both yield
verdict 0 with identical (wprot, vprot, cprot) = (LFU, slot7, 0).

Raw:
```
=== K-M6-2: X-M5-2 fixtures (no cliff at the margin) ===
  [full counterfactual] protected: LFU victim=slot7(proc7) | unprotected: LFU victim=slot7(proc7)
  [selected-policy] protected-victim=slot7 unprotected-victim=slot7
  CHURN-FULL:0 (winner stable at LFU; eviction unchanged)
cliff-1q: wprot=LFU vprot=slot7 cprot=0
  [full counterfactual] protected: LFU victim=slot7(proc7) | unprotected: LFU victim=slot7(proc7)
  [selected-policy] protected-victim=slot7 unprotected-victim=slot7
  CHURN-FULL:0 (winner stable at LFU; eviction unchanged)
cliff-2q: wprot=LFU vprot=slot7 cprot=0
K-M6-2 PASS: uses=1 and uses=2 both yield LFU evicts slot7 at cost 0, verdict 0 (no cliff)
```
K-M6-2 PASS. The one-query cliff is gone at the margin: the marginal
query is ancient, so it confers no protection in either variant.

### K-M6-3: fresh merit protects (F-M6-3b, setup_flip3)

Hand-derived before execution: every proc has >= 2 in-window queries
(costs p0:3, p1:2, p2:2, p3:2, p4:2, p5:4, p6:3, p7:2), so slot7's
uses=2 merit is fresh (winuses=2 >= MERITK) and slot7 is protected.
Protected (slot7 excluded): LFU -> slot5 (cost 4), LRU -> slot5
(cost 4), FIFO -> slot0 (cost 3), LIFO -> slot6 (cost 3),
RANDOM -> slot5 (cost 4); argmin -> FIFO, victim slot0, cost 3.
Unprotected: LFU -> slot5 (cost 4), LRU -> slot7 (cost 2),
FIFO -> slot0 (cost 3), LIFO -> slot7 (cost 2), RANDOM -> slot2
(cost 2); argmin -> LRU, victim slot7, cost 2. Verdict 1.

Raw:
```
=== F-M6-3b: setup_flip3 (fresh merit, :1 path) ===
flip3 state: wprot=FIFO vprot=slot0 wun=LRU vun=slot7
  [full counterfactual] protected: FIFO victim=slot0(proc0) | unprotected: LRU victim=slot7(proc7)
  [selected-policy] protected-victim=slot0 unprotected-victim=slot0
  CHURN-FULL:1 (winner flips FIFO->LRU; eviction slot0(proc0)->slot7(proc7))
F-M6-3b PASS: CHURN-FULL:1 honestly reports winner flips FIFO->LRU, eviction slot0(proc0)->slot7(proc7)
```
K-M6-3 PASS. Protection remains load-bearing: without it the winner
would be LRU, not FIFO. The :1 path shape is preserved exactly
(wprot=FIFO vprot=slot0, wun=LRU vun=slot7), only the fixture's Q
changed to make the merit fresh.

### K-M6-4: fallback under window merit (F-M6-3c)

Hand-derived before execution: every slot uses=2, seq=100 < prot=108,
every pid >= 2 window queries, so every slot is protected ->
FALLBACK-ALL-PROTECTED, fbf=1. Unprotected argmin: LFU -> slot0
(cost 3), LRU -> slot0 (cost 3), FIFO -> slot0 (cost 3),
LIFO -> slot7 (cost 2), RANDOM -> slot6 (cost 2); argmin -> LIFO,
victim slot7, cost 2; proc8 stored, no crash.

Raw:
```
=== F-M6-3c FALLBACK FIXTURE (all slots window-protected) ===
hand-built: all slots uses=2, seq=100 < prot_until=108, every pid >= 2 window queries, so every slot is window-protected
pressure event 9 (learn proc8, win=20):
  FALLBACK-ALL-PROTECTED: all slots protected; using unprotected choice
    LFU victim=slot0(proc0) cost=3
    LRU victim=slot0(proc0) cost=3
    FIFO victim=slot0(proc0) cost=3
    LIFO victim=slot7(proc7) cost=2
    RANDOM victim=slot6(proc6) cost=2
  selected: LIFO cost=2 TIE
  evict slot7 proc7 uses=2 lastq=98
  [full counterfactual] fallback path: no protected winner (all slots protected)
  CHURN-FULL:0 (fallback path; protection not applied)
  stored proc8 at slot7 prot_until=110
F-M6-3c check: fallback flag set, FALLBACK-ALL-PROTECTED emitted
F-M6-3c PASS: fallback to unprotected argmin, newcomer stored, no crash
```
K-M6-4 PASS. Every per-policy victim and cost matches the hand
derivation exactly (LFU/LRU/FIFO -> slot0 cost 3; LIFO -> slot7 cost 2;
RANDOM -> slot6 cost 2; selected LIFO cost 2 TIE; proc8 stored at
slot7).

### K-M6-5: preserved bars (regression)

The full MEM6_RAW_OUTPUT.txt was diffed against the frozen
MEM5_RAW_OUTPUT.txt. The ONLY differences are: (a) the K-M5-3b section
replaced by the F-M6-3b section (same frozen shape, fresh-merit
fixture); (b) the K-M5-3c section replaced by the F-M6-3c section
(all-window-protected fixture); (c) the K-M6-1 and K-M6-2 sections
appended. Diff hunks: lines 104-105, 108-114, 117-119, 156-157, 161,
180a181-196. All other output (STREAM A2/B2/C2 with band checks at
W=20/25/30, sweeps W=10..40 and full history, held-out futures,
pressure events, flat fixture, K-M4-1a, K-M4-2, K-M4-3a, K-M4-3b,
K-M5-1, K-M5-2, K-M5-3a, K-M3-1 ev1/ev2, K-M2-3, K-M2-5) is
byte-identical.

Inherited PASS lines in the official output include: K-M2-5 (A2-ev0,
B2-ev0, C2-ev0), K-M3-1 ev1 (LRU, CHURN-FULL:0) and ev2 (LFU,
CHURN-FULL:1), K-M2-3 (5 strict selections), K-M4-1a, K-M4-2, K-M5-3a,
K-M4-3a, K-M4-3b, K-M5-1, K-M5-2.

K-M6-5 PASS. The fixture-level analysis predicted exactly this: every
other selection event in the suite has its protection windows expired
(learn_stream prot=10, all streams run 40+ queries) or has its
within-window slots carrying >= 2 window queries (the A2/C2 pressure
newcomers with interleaved queries), so R5 provably changes nothing
there. The diff confirms the analysis, not just the hope.

### K-M6-6: determinism

Three consecutive runs of the committed binary: byte-identical
(cmp clean), exit code 0 each, zero FAIL lines in the raw output.
K-M6-6 PASS.

## 5. Causal interpretation

The defect was a scope mismatch between two evidence windows, not a
wrong threshold. H-MEM5 asked "was this procedure ever useful enough?"
(all-time uses) for protection but "would evicting it hurt now?"
(window queries) for harm. Any all-time merit rule admits the X-M5-1
shape: enough ancient queries to earn protection, zero current queries
to make eviction free. R5 asks the same question for both: "was this
procedure queried at least twice in the current window?" A slot with
window cost below MERITK can never be shielded, so the harm pattern the
red team demonstrated is structurally impossible, not just thresholded
away. The cliff moved with the scope: the remaining 1-vs-2 boundary
now sits inside the operating window, where the marginal query is
current by construction, so the marginal case is "one recent query vs
two recent queries" rather than "one ancient query flips everything."

## 6. Honest remaining boundaries

- The window-uses=1 vs 2 knife-edge remains, now in the correct scope:
  a single in-window query is not merit. A future red team may probe
  whether the in-window cliff produces harm; the scope unification
  bounds it (a shielded slot always has window cost >= 2, so shielding
  a cost-0 slot cannot recur).
- Protection can still raise replay cost when it shields a cost-2 slot
  while a cost-3 slot is sacrificed; that is the mechanism working as
  intended (merit protection doing its job), honestly reported by
  CHURN-FULL:1. K-M6-3 demonstrates exactly this shape with the roles
  reversed from the defect: the protected winner (FIFO, cost 3) is
  honestly reported against the unprotected winner (LRU, cost 2).
- The operating window (20), the policy menu, and MERITK (2) are
  authored constants. Nothing here invents a representation or a
  procedure. Classification: bounded L2, not L3.

## 7. Governance disclosures

- Preregistration strictly preceded implementation: PREREG_MEM6.md was
  committed alone (45449f971) before mem6_learn.zag existed in the
  repo. The pre-freeze work was hand derivation plus scratch
  validation in /tmp (Zag compiler + shell diff/cmp only); the
  committed implementation is byte-identical to the scratch-validated
  source. No results were seen before the freeze.
- Pure Zag: zero Python in editing, building, running, verifying, or
  analysis. Tool outputs used: znc, diff, cmp, md5sum, grep, shell.
- No em dashes in PREREG_MEM6.md, mem6_learn.zag, MEM6_RAW_OUTPUT.txt,
  or this file (verified by byte search).
- Supersessions are explicit and pre-registered: K-M5-3b is SUPERSEDED
  by F-M6-3b; K-M5-3c is SUPERSEDED by F-M6-3c. setup_flip2 remains in
  source as unfrozen lineage but is no longer asserted on. No frozen
  bar was weakened or redefined after results.
- Own error, caught before the freeze: during scratch construction the
  F-M6-2 cliff-2q line initially passed the policy index (m6b_wp) where
  the victim slot (m6b_vp) belonged in the replay_cost call. It was
  caught by re-reading the code, fixed in scratch, and the hand
  derivation re-verified against the corrected binary. It never
  reached the repo and never affected a frozen expectation.
- Toolchain notice (not an error): znc prints "warning: zagd
  unavailable; foreground compilation continues without background
  planning" on every build. Compilation succeeds; the binary is
  native and deterministic.
- Negative evidence preserved: the H-MEM5 defect fixtures
  (PREREG_MEM5_ADV.md, MEM5_ADV_RESULT.md) stand; H-MEM6 repairs the
  mechanism rather than disputing the finding.

## 8. Commit lineage (all local; nothing pushed)

- 45449f971 PREREG H-MEM6 FROZEN (alone, before
  implementation/build/runs). Recency-weighted merit R5; X-M5-1/X-M5-2
  frozen kill criteria; F-M6-3b/F-M6-3c supersede stale fixtures.
  Pure Zag.
- <this commit> H-MEM6 implementation + evidence: mem6_learn.zag,
  MEM6_RAW_OUTPUT.txt, MEM6_RESULT.md. Verdict: SURVIVES 6/6.
- Parent lineage: H-MEM5 prereg 0e457c276, H-MEM5 result e5b786c65,
  H-MEM5 red team PREREG_MEM5_ADV.md (DOWNGRADE).

## 9. Recommended next step

Spawn the independent H-MEM6 red team: assume the R5 claim is false
and attack the remaining in-window 1-vs-2 knife-edge, the fallback
path under window merit, and any fixture where window scope and age
window interact (e.g. a slot whose window merit straddles the age
deadline). The strongest remaining reason to doubt R5 is the
authored window itself: a fixed 20-query window is a regime choice,
and merit that decays smoothly rather than cliffs at 2 might dominate
it. That is the next hypothesis, not this verdict.
