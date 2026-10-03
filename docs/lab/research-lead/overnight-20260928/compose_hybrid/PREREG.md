# PREREG: Hybrid Widening -- Coverage-Selective First, Blind-Retry Backstop

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Step 0) strictly precedes all implementation.

## 1. Question

WIDEN-COMP (ledger C333, verdict MIXED) discriminated coverage-directed
selective widening (C) against failure-triggered blind retry (F): C wins iff
the coverage evidence is observable inside the admitted trial sequence (D1:
7 tries to 2); C pays a spurious cost when genuine misses are non-diagnostic
(D2: 3 tries to 5, WIDEN=1 where F has none); C fails where the misleading
MAP is never admitted (D3: F succeeds 44/2 via blind retry, C fails -2/1).
The worker's recommended follow-up (not claimed): a hybrid arm,
coverage-selective first with failure-triggered blind retry as backstop.
This battery builds that hybrid (H) and tests whether it inherits both wins.

## 2. Frozen background (not under test)

- C319 SUBSUMPTION (H1+H2 = behavior-contract composition); C325
  independent reproduction; C329 S2 pin (empty kind-set reads as universal
  {1,2} in all three admission positions; FROZEN, used here, not re-litigated).
- WIDEN-COMP MIXED verdict and boundary statement (ledger C333).
- Shared semantics: S2-pinned admission; ordered trial execution (admitted
  singles in MAP-id order, then admitted pairs in (a,b) id order); end-to-end
  verification; Amendment-2 success-recording into contract masks;
  missbits[m][p] per query, populated from FAILED trials only, every input a
  learner-observed probe_kind value; kinds 1=NODE, 2=NUM; one TRIAL = one
  single-MAP or one ordered-pair execution; 3/3 byte-identical runs per arm.

## 3. Hybrid design (frozen)

One composer, two trigger rules, both always on. No mode flag; the rule set
is the experimental manipulation, never learner-selected.

R1 (coverage-selective; WTRIG=2): On a failed trial that records at least one
NEW miss bit, while the backstop has not engaged, immediately admit every
ordered pair (x,y), x != y, that is ALL of: (i) currently filter-rejected,
(ii) not yet tried, (iii) kin in u_eff(x.inmask) and kout in u_eff(y.outmask),
(iv) junction-justified by the accumulated ledger:
(missbits[x][out] INTERSECTS u_eff(y.inmask) nonempty) OR
(missbits[y][in] INTERSECTS u_eff(x.outmask) nonempty).
Log WIDEN=1 once per query, WTRIG=2 once per query, WADD=x,y per admitted
pair. Try the admitted pairs immediately in (x,y) id order before resuming
the admitted sequence; rescan while new misses justify further pairs.

R2 (blind backstop; WTRIG=1): Engages exactly once per query, at the moment
the admitted trial sequence (every admitted single in MAP-id order, then
every admitted pair in (a,b) id order) is fully exhausted with no success.
Log WBACK=1 once per query and WTRIG=1 once per query. Then try every
filter-rejected, untried ordered pair in (x,y) id order.

During the backstop, R1 is DISARMED: backstop trials still record misses
into the ledger (the learner did observe those kinds; the ledger stays
honest), but a new miss triggers no selective admission. Rationale: during
the backstop every filter-rejected pair is already queued in id order, so
there is no selection left for R1 to do; disarming keeps the backstop
pure-blind (identical to arm F's retry), which is what makes the Section 3b
decomposition hold.

ARM summary line:
ARM=H PROB=.. ANS=.. TRIES=.. WIDEN=.. WTRIG=.. WBACK=.. INTER=..
WIDEN=1 if either rule fired; WTRIG=2 if R1 fired, else 1 if R2 fired, else 0;
WBACK=1 iff R2 fired. Event lines appear in firing order: selective events
(WIDEN=1, WTRIG=2, WADD=x,y per pair) and backstop events (WBACK=1, WTRIG=1).

### 3b. Decomposition theorem (preregistered)

Let A be the admitted tried-set (identical in all arms), S the R1-selective
tried-set, R arm F's blind-retry tried-set, B the hybrid backstop tried-set.

- If C succeeds on a problem: R2 never engages; H's tried-set, try count,
  WTRIG, WADD lines, and Phase-S ledger are IDENTICAL to C's.
- If C fails on a problem: H tries |A|+|S|+|B| with B = R minus S (rejected
  pairs not already tried); F tries |A|+|R|. S is a subset of R (R1 admits
  only filter-rejected pairs, disjoint from A), so |H| = |F| exactly, and a
  success pair (if any) is reached at the same blind position (it cannot lie
  in S, else C would have tried it and succeeded).
- Corollary 1: H is never strictly faster than F on any problem.
- Corollary 2: H is identical to C on any problem C succeeds on.
- Corollary 3 (D1/D2 indistinguishability): at the R1 trigger moment (first
  admitted single records an out-miss) D1 and D2 present identical
  learner-observable state (tried {m0}, missbits {m0:out:{1}}, same
  contracts). Any deterministic first-miss-triggered R1 fires on both or
  neither; firing late (e.g. after the admitted singles) collapses D1's win
  to F's 7 tries. Hence D2's spurious cost (5 vs 3 tries) is the unavoidable
  price of D1's win for this trigger family, and is PREREGISTERED as an
  exception to the match-best bar, not a hybrid failure.
- Consequence: HYBRID WINS (strictly better than both pure arms on one
  problem) is unreachable by construction; observing it would indicate an
  implementation bug. The live contest is HYBRID MATCHES BEST vs HYBRID FAILS.

## 4. Problems

D0-D3: replayed exactly as frozen in WIDEN-COMP PREREG Section 4 (worlds not
re-specified here; H predictions follow from Section 3b).

D4 HIDDEN PAIR, NO SPURIOUS MISS (new; C must fail, F must succeed, H must
match F):
Facts teach: (11,81,12),(12,81,13),(13,81,14); (70,82,71),(70,82,72);
(91,83,92),(92,83,93),(93,83,94); (31,81,32).
MAPs: id0 W=WALK(81) taught 11->14 (in{1},out{2}); id1 Q=COUNT(82) taught
70->2 (in{1},out{2}); id2 X=WALK(83) taught 91->94 (in{1},out{2}); id3
Y=IDENT taught 31->31 (in{1},out{1}).
Facts sealed: (41,81,42),(42,81,43),(43,81,44); (41,83,47); (47,84,471).
Query: s=41, kin=1, kout=1, exp=47, nm=4. Correct: pair (X,Y): X(41)=47,
Y(47)=47.
Design notes: X is hidden (outmask {2} contradicts kout=1, so X is rejected
in all admission positions and never executed); Y is the only admitted
single and it fails with no miss (41 is NODE, covered in both positions);
no admitted pairs exist; the blind backstop must find (2,3) 9th in id order.

D5 LONG BLIND TAIL (new; C must succeed fast, F must succeed slowly, H must
match C):
Facts teach: (11,81,12),(12,81,13),(13,81,14); (70,82,71),(70,82,72);
(75,84,751),(75,84,752); (60,83,61),(60,83,62).
MAPs: id0 A=COUNT(82) taught 70->2 (in{1},out{2}); id1 B=COUNT(84) taught
75->2 (in{1},out{2}); id2 X=WALK(81) taught 11->14 (in{1},out{2}); id3
Y=COUNT(83) taught 60->2 (in{1},out{2}).
Facts sealed: (41,81,42),(42,81,43),(43,81,44); (44,83,441),(44,83,442).
Query: s=41, kin=1, kout=2, exp=2, nm=4. Correct: pair (X,Y): X(41)=44
(44 is a subject, hence NODE; miss (2,out,1) against outmask {2}), Y(44)=2.
Design notes: four admitted singles, no admitted pairs; F's blind id order
reaches (2,3) 9th; C's R1 fires on try 3 (the X miss) and admits
(2,0),(2,1),(2,3).

## 5. Frozen predictions

Format: ANS / TRIES / WIDEN / WTRIG / INTER ; WBACK in parentheses for H.

| Prob | F | C | H |
|------|---|---|---|
| D0 | 2/3/0/0/34 | 2/3/0/0/34 | 2/3/0/0/34 (0) |
| D1 | 2/7/1/1/44 | 2/2/1/2/44 | 2/2/1/2/44 (0) |
| D2 | 2/3/0/0/-1 | 2/5/1/2/-1 | 2/5/1/2/-1 (0) |
| D3 | 44/2/1/1/44 | -2/1/0/0/-1 | 44/2/1/1/44 (1) |
| D4 | 47/10/1/1/47 | -2/1/0/0/-1 | 47/10/1/1/47 (1) |
| D5 | 2/13/1/1/44 | 2/6/1/2/44 | 2/6/1/2/44 (0) |

Tried-sets and event predictions:
- D0: all arms {Y,D2,(X,Y)}; no widening events; ledgers empty.
- D1: F {X,Y,D2,(D1,X),(D1,Y),(D1,D2),(X,Y)} via blind retry; C and H
  {X,(X,Y)} with WADD=(0,1),(0,3).
- D2: F {D,Q,W}; C and H {D,(D,Q),(D,W),Q,W} with WADD=(0,1),(0,2).
- D3: F {Y,(X,Y)} via blind retry; C {Y}; H {Y,(X,Y)} with WBACK=1, WTRIG=1.
- D4: F {Y,(0,1),(0,2),(0,3),(1,0),(1,2),(1,3),(2,0),(2,1),(2,3)} via blind
  retry; C {Y}; H the same 10-trial set with WBACK=1, WTRIG=1.
- D5: F {A,B,X,Y,(0,1),(0,2),(0,3),(1,0),(1,2),(1,3),(2,0),(2,1),(2,3)} via
  blind retry; C and H {A,B,X,(2,0),(2,1),(2,3)} with WADD=(2,0),(2,1),(2,3).

Ledger predictions (bit values 1<<(k-1); in/out per MAP):
- F: all zero on every problem (F never records misses).
- C: D1 m0 out=1; D2 m0 out=1; D5 m2 out=1; D0/D3/D4 all zero.
- H: D1 m0 out=1; D2 m0 out=1; D5 m2 out=1; D0/D3 all zero; D4 m2 out=1
  AND m3 in=2 out=2 (backstop-phase misses recorded while R1 is disarmed).

## 6. Frozen kill bars

- K1 REPLAY: H on D0-D3 exactly as Section 5; F and C on D0-D3 reproduce
  the WIDEN-COMP frozen values (fidelity check on this lane's copies). 3/3.
- K2 NEW PROBLEMS: F, C, H on D4/D5 exactly as Section 5. 3/3.
- K3 MATCH-BEST: H's try count equals the better pure arm's on D0, D1, D3,
  D4, D5; on D2 H equals C (5 tries; the preregistered Section 3b price).
  H's ANS is correct on all six problems.
- K4 BACKSTOP LOAD-BEARING (falsifies "just C-with-retries"): WBACK=1
  appears on D3 and D4 and on no other problem; on D3/D4 the successful pair
  is filter-rejected (checkable from the CENSUS masks: X's outmask {2}
  contradicts kout=1), so R2 delivered it; C's -2 on D3/D4 verifies that
  without R2 the hybrid fails there.
- K5 LEDGER: Section 5 ledger predictions hold exactly. 3/3.
- K6 DETERMINISM: 3/3 byte-identical whole-output per arm; sha256 recorded.
- K7 NO-MODE AUDIT: one composer; R1/R2 trigger on learner-observable state
  (new miss bit; admitted-exhaustion); no identifier selecting widening
  policies at runtime (grep for policy/mode/arm in h_hyb.zag: zero hits).
- K8 HYGIENE: zero em/en dash bytes in all docs; safebin guard attested;
  pure Zag for all scientific computation; pinned znc.

## 7. Frozen verdict mapping

- K1-K8 all PASS: HYBRID MATCHES BEST. The hybrid inherits C's selective
  wins (D1: 7 to 2; D5: 13 to 6) and F's blind robustness (D3, D4: success
  where C fails -2), never tries more than the worse pure arm, and pays only
  the preregistered D2 spurious price (5 vs 3), proved unavoidable for the
  first-miss trigger family in Section 3b.
- Any K1-K8 failure: HYBRID FAILS, with the exact failing bar and deviation
  named. VOID is terminal.
- HYBRID WINS (strictly better than both pure arms on one problem) is
  unreachable under Section 3b; observing it would falsify the
  implementation, not the design (diagnose as bug, do not claim).

## 8. Honest boundaries (pre-declared)

- D0-D5 discriminate the widening policy; they do not establish generality
  of the hybrid.
- missbits is per-query; cross-query growth uses only the shared
  Amendment-2 success-recording.
- Expected-answer verification still used (canonical boundary).
- Behaviors are installed as previously-learned MAPs (canonical standing).

## 9. Implementation plan (frozen order)

1. h_base.zag: w_base.zag plus setup_d4/setup_d5, arena field 1104 wback,
   report() prints WBACK. (Copy; the compose_widen lane is not touched.)
2. h_fail.zag: w_fail.zag with main() extended to D4/D5 (fidelity arm).
3. h_cov.zag: w_cov.zag with main() extended to D4/D5 (fidelity arm).
4. h_hyb.zag: hybrid composer (R1/R2 exactly as Section 3) + main() D0-D5.
5. Assemble with cat, compile with the pinned znc, run 3x per arm, record
   sha256.
6. REPORT.md with verdict per the Section 7 mapping.

Zag pitfalls: u8-backed z_alloc; dynamic content formatted into one buffer
with cursor helpers and a single raw-syscall flush (no _zag_print for
dynamic content); if-nesting at most 3; no !(A && B) in while conditions;
as []f64 / as []i64 do not rescale .len.
