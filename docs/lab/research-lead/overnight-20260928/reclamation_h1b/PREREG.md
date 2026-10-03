# PREREG: RECLAMATION-H1B (importance-weighted liveness, corrected K13)

Frozen 2026-10-03. This preregistration strictly precedes the binary
copy and all runs. This prereg commit contains ONLY PREREG.md and
NAMECHECK.md. No kill bar below may be weakened or reinterpreted after
results are seen. VOID is terminal: it is corrected only by fresh
preregistration plus a fresh run, never by salvage or amend-and-promote.

Worker: RECLAMATION-H1B worker (non-ledger task; claim minting paused).
Lane: `docs/lab/research-lead/overnight-20260928/reclamation_h1b/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation (embodied in
the frozen binary; no new code is written or compiled in this lane).
Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## Objective

RECLAMATION-H1 achieved FAIL (14/15 kill bars pass) with an owned
worker derivation error on K13: the frozen prereg derived the benign
importance distribution as 10 entries at popcount 4, 5 at 3, 5 at 2,
predicting ret=28/post=10/rawA=25 under 3-owner adversarial inflation.
The correct distribution is 5 at popcount 4, 10 at popcount 3, 5 at
popcount 2, because hop-1 keys i=6..10 carry owners {1,2,8} (mask 11,
popcount 3), not {1,2,4,8} (mask 15, popcount 4); owner 4 was only
taught on i=1..5. An eviction trace on a debug build verified the
mechanism implements the specified rule exactly, and the corrected
derivation predicts the measured values (ret=14/post=5/rawA=20)
bit-for-bit.

This lane puts the adversarial dose-response on the books cleanly: a
fresh preregistration with the corrected K13 derivation, then a fresh
run of the UNCHANGED mechanism. The mechanism is the frozen H1
official binary, byte-identical, copied after this prereg commit:

- mechanism identity (frozen): sha256
  c0f48d00b43966bcc06e4cd9d9aad863c668d970a8d1674d2335f42073f7774d
  (the H1 lane's official binary, from which H1's 3/3 runs,
  sha256 ee983703e689459fe4e67dab94698b126140f4e1ef38330cbeeb8c8355d830c6,
  were produced).

No source change, no rebuild, no check-code change. The only delta
relative to H1 is this prereg's K13 derivation and frozen numbers.
The binary still stamps its output header as LANE=RECLAMATION-H1;
that is expected (unchanged binary) and recorded, not a mismatch.

## Mechanism under test: policy 7 (PIN-IMP)

Unchanged from H1 (see the H1 PREREG for the full frozen
specification): importance is the popcount of the pool entry's owner
bitmask, maintained by the existing mem_write owner-merge machinery;
no researcher-set importance path exists in policy 7. Reclamation
rule: when the pool is full, scan all used slots; evict the slot with
the minimum (importance, then oldest last-touch stamp, then lowest
slot index). Strict less-than comparisons. Recency is only a
tiebreaker; owner identity is never directly consulted. Adversarial
churn drivers: mode 4 (2-owner inflation, churn popcount 2) and mode 5
(3-owner inflation, churn popcount 3); 40 churn conflicts, cf=60 total,
in both.

## Protocol (frozen, unchanged from H1)

Per condition, on a freshly zeroed workspace: 1. teach A family
(multi). 2. pre-test (expect 35). 3. teach B benign FULL (20
conflicts, 20 A victims pinned in pool slots 0..19, slots 20..31
free). 4. churn: single-owner key 3999 (w in {1,21,33}) or
multi-owner mode 1/2/3/4/5 (w=21 per key). 5. post-test; retention =
100*post/pre. 6. record conflicts, evictions, drop, B accuracy, rawA.

Conditions (29). Column order:
pre, post, ret, cf, ev, drop, bacc, rawA.

| cond       | pol | adv        | pre | post | ret | cf | ev | drop | bacc | rawA |
|------------|-----|------------|-----|------|-----|----|----|------|------|------|
| IMPCON-B0  | 5   | single w1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| IMPCON-A20 | 5   | single w21 | 35  | 35   | 100 | 40 | 8  | 0    | 20   | 35   |
| IMPCON-A32 | 5   | single w33 | 35  | 35   | 100 | 52 | 20 | 0    | 20   | 35   |
| IMPPIN-M2  | 3   | mode1      | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| IMPPIN-M3  | 3   | mode2      | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| IMPCON-M2  | 5   | mode1      | 35  | 35   | 100 | 60 | 11 | 17   | 20   | 35   |
| IMPCON-M3  | 5   | mode2      | 35  | 35   | 100 | 80 | 5  | 43   | 20   | 35   |
| IMPPIN-X2  | 3   | mode3      | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| IMPCON-X2  | 5   | mode3      | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| IMPLIV-M2  | 6   | mode1      | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| IMPLIV-M3  | 6   | mode2      | 35  | 0    | 0   | 80 | 48 | 0    | 20   | 15   |
| IMPLIV-X2  | 6   | mode3      | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| IMPFIFO-B0 | 0   | single w1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| IMPFIFO-A20| 0   | single w21 | 35  | 19   | 54  | 40 | 8  | 0    | 20   | 27   |
| IMPFIFO-A32| 0   | single w33 | 35  | 0    | 0   | 52 | 20 | 0    | 20   | 15   |
| IMPPART-B0 | 1   | single w1  | 35  | 27   | 77  | 20 | 4  | 0    | 20   | 31   |
| IMPPART-A20| 1   | single w21 | 35  | 27   | 77  | 40 | 8  | 0    | 20   | 31   |
| IMPPART-A32| 1   | single w33 | 35  | 27   | 77  | 52 | 20 | 0    | 20   | 31   |
| IMPLRU-B0  | 4   | single w1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| IMPLRU-A20 | 4   | single w21 | 35  | 19   | 54  | 40 | 8  | 0    | 20   | 27   |
| IMPLRU-A32 | 4   | single w33 | 35  | 0    | 0   | 52 | 20 | 0    | 20   | 15   |
| IMP-B0     | 7   | single w1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| IMP-A20    | 7   | single w21 | 35  | 35   | 100 | 40 | 8  | 0    | 20   | 35   |
| IMP-A32    | 7   | single w33 | 35  | 35   | 100 | 52 | 20 | 0    | 20   | 35   |
| IMP-M2     | 7   | mode1      | 35  | 35   | 100 | 60 | 28 | 0    | 20   | 35   |
| IMP-M3     | 7   | mode2      | 35  | 35   | 100 | 80 | 48 | 0    | 20   | 35   |
| IMP-X2     | 7   | mode3      | 35  | 35   | 100 | 60 | 28 | 0    | 20   | 35   |
| IMPADV-M2  | 7   | mode4      | 35  | 25   | 71  | 60 | 28 | 0    | 20   | 30   |
| IMPADV3-M2 | 7   | mode5      | 35  | 5    | 14  | 60 | 28 | 0    | 20   | 20   |

## Derivation notes (frozen with the prereg)

Benign phase identical in all conditions: 20 A victims pin pool slots
0..19 with install stamps 1..20 (clock=20); slots 20..31 free. The 20
pool entries carry owner masks from the multi-owner teaching (owner 4
was taught only on i=1..5; owner 16's writes conflicted and installed
only in the primary, leaving the A masks in the pool):

- 5 hop-1 keys i=1..5: mask 15 = {1,2,4,8} (popcount 4), stamps
  1,3,5,7,9.
- 5 hop-1 keys i=6..10: mask 11 = {1,2,8} (popcount 3), stamps
  11,13,15,17,19. (This is the correction: H1's prereg wrongly
  assigned these mask 15.)
- 5 hop-2 keys i=1..5: mask 7 = {1,2,4} (popcount 3), stamps
  2,4,6,8,10.
- 5 hop-2 keys i=6..10: mask 3 = {1,2} (popcount 2), stamps
  12,14,16,18,20.

So the benign importance distribution is 5 at popcount 4, 10 at
popcount 3, 5 at popcount 2.

IMP-A20: 20 churn conflicts (key 3999, owner 16, popcount 1). 12 fill
slots 20..31 (stamps 21..32); 8 relocations. Every churn entry has
importance 1, strictly below every benign entry (2/3/4), so all 8
evictions take churn history, oldest first. ev=8, drop=0, ret=100,
rawA=35, bacc=20, cf=40. The recency signal destroyed 8 benign entries
here (LIV-A20 ret=54); importance destroys none.

IMP-A32: 32 conflicts = 12 fills + 20 relocations, all churn
(importance 1). ev=20, drop=0, ret=100, rawA=35, cf=52.

IMP-M2 (mode1): 40 churn conflicts = 12 fills + 28 relocations; churn
entries are keys 3998 (owner 8) and 3999 (owner 16), each single-owner,
importance 1. All 28 relocations evict churn history. ev=28, drop=0,
ret=100, rawA=35, cf=60.

IMP-M3 (mode2): 60 churn conflicts = 12 fills + 48 relocations, all
churn (importance 1). ev=48, drop=0, ret=100, rawA=35, cf=80.

IMP-X2 (mode3): 40 churn conflicts = 12 fills + 28 relocations, all
churn (importance 1). ev=28, drop=0, ret=100, rawA=35, cf=60.

IMPADV-M2 (mode4): churn entries have importance 2 (masks 24). The
minimum importance in the pool is 2: the 5 benign hop-2 keys i=6..10
(popcount 2, stamps 12,14,16,18,20) and all churn entries (stamps
21+). Tie-break by oldest stamp evicts the 5 benign entries first
(relocations 1..5), then the 23 oldest churn entries. Destroyed benign
keys: 1062,1072,1082,1092,1102. post: loop1 (owner 1) i=1..5 pass = 5;
loop2 (owner 2) i=1..5 pass = 5; loop3 (owner 4) i=1..5 pass = 5 (keys
1011..1051, 1012..1052, 2000+i intact); loop4 (owner 8) 10 pass.
post=25, ret=(100*25)/35=71 (integer). rawA: owner-1 hop1 (10) +
hop2 i=1..5 (5) = 15; owner-2 hop3 (10); owner-4 (2000+i) (5) = 30.
bacc=20, cf=60, ev=28, drop=0.

IMPADV3-M2 (mode5, CORRECTED): churn entries have importance 3 (masks
28, stamps 21+). The 15 benign entries at importance <= 3 (5 at
popcount 2 with stamps 12..20; 10 at popcount 3 with stamps 2..19)
are all tied-or-below every churn entry and older than every churn
entry, so relocations 1..15 evict all of them (popcount-2 first, then
popcount-3 by stamp), then relocations 16..28 evict the 13 oldest
churn entries. The 5 popcount-4 benign entries (hop-1 keys i=1..5:
1011,1021,1031,1041,1051, stamps 1,3,5,7,9) survive. Destroyed: all 10
hop-2 keys, and hop-1 keys i=6..10. post: loop1 (owner 1) i=1..10
needs hop-1 AND hop-2 per i: all hop-2 gone = 0; loop2 (owner 2)
needs hop-3 as well: all hop-2 gone = 0; loop3 (owner 4) i=1..5
needs 2000+i (primary, intact) AND hop-1 AND hop-2 per i: hop-2 gone
= 0; loop4 (owner 8) i=1..10 needs hop-1 only: i=1..5 survive with
mask 15 containing owner 8 and A's values i*100+7 = 5. post=5,
ret=(100*5)/35=14 (integer). rawA: owner-1 hop1 i=1..5 (5);
owner-1 hop2 (0); owner-2 hop3 (10, B never touched these keys, still
in primary); owner-4 (2000+i) (5, still in primary) = 20. bacc=20,
cf=60, ev=28, drop=0.

## Frozen kill bars

- K1 ANCHOR-CONSENT: IMPCON-B0/A20/A32 match the frozen
  CONSENT-MULTIOWNER consent rows exactly, every column
  (ret=[100,100,100], cf=[20,40,52], ev=[0,8,20], drop=[0,0,0],
  bacc=20, rawA=35). Else VOID: the substrate moved.
- K2 ANCHOR-PIN-MULTI: IMPPIN-M2/M3 match the frozen
  MULTI-OWNER-CHURN PIN rows exactly (ret=[100,100], cf=[60,80],
  ev=[0,0], drop=[28,48], bacc=20, rawA=35). Else VOID.
- K3 ANCHOR-CONSENT-MULTI: IMPCON-M2/M3/X2 match the frozen
  CONSENT-MULTIOWNER rows exactly (ret=100 x3, cf=[60,80,60],
  ev=[11,5,0], drop=[17,43,28], bacc=20, rawA=35); IMPPIN-X2 matches
  the frozen PIN-M2 row exactly. Else VOID.
- K4 ANCHOR-FIFO: IMPFIFO-B0/A20/A32 match the frozen
  EVICTION-POLICY-COMPARE FIFO rows exactly, every column
  (ret=[100,54,0], post=[35,19,0], cf=[20,40,52], ev=[0,8,20],
  drop=[0,0,0], bacc=20, rawA=[35,27,15]). Else VOID.
- K5 ANCHOR-PART: IMPPART-B0/A20/A32 match the frozen
  EVICTION-POLICY-COMPARE PART rows exactly, every column
  (ret=[77,77,77], post=27 x3, cf=[20,40,52], ev=[4,8,20],
  drop=[0,0,0], bacc=20, rawA=31 x3). Else VOID.
- K6 ANCHOR-LRU: IMPLRU-B0/A20/A32 are bit-for-bit equal to
  IMPFIFO-B0/A20/A32 in every column, and ret=[100,54,0].
- K7 ANCHOR-LIVENESS: IMPLIV-M2/M3/X2 match the frozen
  LIVENESS-SIGNAL liveness rows exactly (ret=0 x3, cf=[60,80,60],
  ev=[28,48,28], drop=[0,0,0], bacc=20, rawA=15 x3). Else VOID.
- K8 IMP-COLD-SAVED: IMP-B0/A20/A32 ret==100 x3; IMP-A20 ev==8,
  drop==0, rawA==35, post==35; IMP-A32 ev==20, drop==0, rawA==35,
  post==35. Cold-but-critical knowledge survives the full
  single-owner ladder that recency destroyed (54/0).
- K9 IMP-MULTI-SAVED: IMP-M2/M3/X2 ret==100 x3; ev==[28,48,28];
  drop==0 x3; rawA==35 x3. Full retention under multi-owner churn
  with full capacity restoration.
- K10 IMP-BEATS-LIVENESS: IMP-M2 ret (100) > IMPLIV-M2 ret (0) AND
  IMP-M2 ev (28) == IMPLIV-M2 ev (28) AND both drop==0. Identical
  capacity restoration, opposite retention: the importance signal
  protects exactly what recency destroys.
- K11 IMP-BEATS-CONSENT-CAPACITY: IMP-M2 ev (28) > IMPCON-M2 ev (11)
  AND IMP-M2 drop (0) < IMPCON-M2 drop (17) AND IMP-M2 ret (100) ==
  IMPCON-M2 ret (100). H1 beats consent's capacity price with no
  retention loss under the aligned adversary.
- K12 ADV-GAMED: IMPADV-M2 ret==71 AND post==25 AND rawA==30 AND
  ev==28 AND drop==0 AND cf==60 AND bacc==20. The adversary games
  the importance signal: inflating churn importance to 2 kills the 5
  least-important critical entries while capacity metrics look
  healthy.
- K13 ADV-DOSE (CORRECTED): IMPADV3-M2 ret==14 AND post==5 AND
  rawA==20 AND ev==28 AND drop==0 AND cf==60. Higher inflation kills
  deeper: the policy protects exactly the entries with importance
  strictly above the adversary's inflated level. The 15 benign
  entries at importance <= 3 die (5 at popcount 2, 10 at popcount
  3); only the 5 popcount-4 entries survive.
- K14 ADV-FIXED: conflicts identical across policies per dose:
  40 at single w=21 (IMPCON-A20, IMPFIFO-A20, IMPPART-A20,
  IMPLRU-A20, IMP-A20); 52 at single w=33 (IMPCON-A32,
  IMPFIFO-A32, IMPPART-A32, IMPLRU-A32, IMP-A32); 60 at mode1
  (IMPPIN-M2, IMPCON-M2, IMPLIV-M2, IMP-M2); 60 at mode3
  (IMPPIN-X2, IMPCON-X2, IMPLIV-X2, IMP-X2); 60 at mode4
  (IMPADV-M2); 60 at mode5 (IMPADV3-M2); 80 at mode2 (IMPPIN-M3,
  IMPCON-M3, IMPLIV-M3, IMP-M3).
- K15 DETERMINISM: 3/3 runs byte-identical (sha256 equal). Else
  VOID.

Verdict: PASS iff K1..K15 all hold. Any kill-bar miss names the bar
and yields FAIL. K1, K2, K3, K4, K5, K7, or K15 failure yields VOID.
Thresholds are frozen; they are not moved after results.

Discrimination design: K1..K7 anchor all six baseline policies (a
moved substrate or baseline invalidates the probe); K6 additionally
checks the LRU==FIFO equivalence inside this run; K8/K9 test the
headline cold-but-critical prediction (importance holds 100 where
recency fell to 54/0); K10 is the direct H1-vs-recency comparison at
identical capacity; K11 is the direct H1-vs-consent comparison at
identical retention; K12/K13 are the adversarial-scoring controls
that discriminate "signal protects" from "signal is ungameable";
K14 bars the "stronger adversary under one policy" confound.

## What this does NOT test

- The importance source is dependency-count (owner-mask popcount),
  one of the two sources the synthesis named; the
  successful-episode weight variant is not implemented.
- The learner does not decide importance; H1 is a new signal type,
  not a new decision authority (that is H3).
- The adversarial controls inflate importance through the workload
  (mechanism-computed source kept identical); no direct
  researcher-scored importance path exists in policy 7.
- Owner-scoped reads are retained, so the label-free routing caveat
  carries over unchanged.
- No repair is proposed or canonized: the measured prices are
  evidence, not a work order for an H1-2.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first. The frozen H1 binary
is copied (byte-identical, sha256 verified) only after this commit;
it is not rebuilt or modified. Runs and REPORT.md only after the
binary copy. Commit-order self-check: this prereg commit must be the
first commit in this lane and must strictly precede the binary copy,
the runs, and the report.
