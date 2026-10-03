# PREREG: RECLAMATION-H1 (importance-weighted liveness)

Frozen 2026-10-03. This preregistration strictly precedes implementation.
This prereg commit contains ONLY PREREG.md and NAMECHECK.md. No kill bar
below may be weakened or reinterpreted after results are seen. VOID is
terminal: it is corrected only by fresh preregistration plus a fresh run,
never by salvage or amend-and-promote.

Worker: RECLAMATION-H1 worker (non-ledger task; claim minting paused).
Lane: `docs/lab/research-lead/overnight-20260928/reclamation_h1/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation; shell only for
znc invocation, binary execution, git ops, sha256sum, and file movement.
Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## Objective

RECLAMATION_SYNTHESIS (2026-10-03) closed the five-lane
reclamation arc on a trilemma: among retention, capacity, and
boundary-freedom no tested policy achieves all three, and it posed the
hard problem: who decides an entry is dead when the knowledge is
cold-but-critical (never re-touched, must survive), no researcher
supplies the signal, and the adversary is shaped by the workload. It
proposed three structurally distinct hypotheses. This lane implements
H1: importance-weighted liveness (new signal type: learner-owned
value, not identity, not time). It asks: does an importance signal
protect cold-but-critical knowledge where recency destroys it, and can
the adversary game the importance signal?

## Mechanism under test: policy 7 (PIN-IMP)

Substrate identical to LIVENESS-SIGNAL (same header layout, same pool,
same primary, same conflict path, same owner-scoped reads, same A
family, same benign B writer, same single-owner churn, same
multi-owner churn modes 1/2/3, same touch stamps). Policy 0/1 branches
are carried verbatim from EVICTION-POLICY-COMPARE and the policy 4
branch verbatim from PINNING-RECLAMATION, so all six baseline policies
(FIFO, PART, PIN, PIN-LRU, PIN-CONSENT, PIN-LIVENESS) reproduce their
frozen rows on this substrate.

### The importance source (preregistered; the honest-risk control point)

Importance is defined as the popcount of the pool entry's owner
bitmask: the number of distinct cognitive structures (owners) that
referenced the entry during the learner's teaching history. It is
maintained by the existing mem_write owner-merge machinery on every
write; there is no researcher-set importance path anywhere in policy 7.
No mask comparison, no identity test, and no researcher-authored score
appears in the reclamation decision. The researcher designs workloads
(as in every lane of this arc); the importance VALUES are
mechanism-computed from the learner's experience at decision time.

This is deliberately a new SIGNAL type, not a new DECISION authority:
the learner does not decide importance (that is H3's question). H1
tests whether a learner-history-derived value signal protects
cold-but-critical knowledge where recency fails, and whether the
adversary can game it. The adversarial-scoring control (modes 4/5)
keeps the signal source byte-identical and has the researcher score
importance adversarially THROUGH the workload: the churn adversary
accumulates owner references on its own entries, inflating their
importance past the least-important critical entries. If importance
were researcher-scored directly it would collapse to the consent-mask
pattern; this control instead tests the honest failure mode of the
learner-derived source.

### Policy-7 reclamation rule (frozen)

When the pool is full: scan all used slots; evict the slot with the
minimum (importance, then oldest last-touch stamp, then lowest slot
index). Strict less-than comparisons, so ties resolve to the lowest
slot index deterministically. ev++; install the new entry with a fresh
stamp. Recency is only a tiebreaker; owner identity is never directly
consulted.

### Adversarial churn drivers (frozen)

- mode 4 (2-owner inflation): per round, key 3998 written with owners
  8 then 16 (same key, same val: merge path, no extra conflict), key
  3999 with owners 16 then 8. Displaced churn entries carry masks of
  popcount 2. Round 0 allocates (0 conflicts); rounds 1..20 produce 2
  conflicts each: 40 churn conflicts, cf=60 total.
- mode 5 (3-owner inflation): per round, each key written with owners
  8, 16, 4 (masks of popcount 3). Same footprint: 40 churn conflicts,
  cf=60 total.

## Protocol (frozen)

Per condition, on a freshly zeroed workspace: 1. teach A family
(multi). 2. pre-test (expect 35). 3. teach B benign FULL (20
conflicts, 20 A victims pinned in pool slots 0..19, slots 20..31
free). 4. churn: single-owner key 3999 (w in {1,21,33}) or
multi-owner mode 1/2/3/4/5 (w=21 per key). 5. post-test; retention =
100*post/pre. 6. record conflicts, evictions, drop, B accuracy, rawA.

Conditions (29). Anchors reproduce the frozen tables of all six
baseline policies. New rows use policy 7. Column order:
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
| IMPADV3-M2 | 7   | mode5      | 35  | 10   | 28  | 60 | 28 | 0    | 20   | 25   |

## Derivation notes (frozen with the prereg)

Benign phase identical in all conditions: 20 A victims pin pool slots
0..19 with install stamps 1..20 (clock=20); slots 20..31 free. The 20
pool entries carry owner masks from the multi-owner teaching: the 10
hop-1 keys have mask 15 (popcount 4, stamps 1,3,..,19); the 5 hop-2
keys i=1..5 have mask 7 (popcount 3, stamps 2,4,..,10); the 5 hop-2
keys i=6..10 have mask 3 (popcount 2, stamps 12,14,..,20).

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
1011..1052, 2001..2005 intact); loop4 (owner 8) 10 pass. post=25,
ret=(100*25)/35=71 (integer). rawA: owner-1 hop1 (10) + hop2 i=1..5
(5) = 15; owner-2 hop3 (10); owner-4 (2000+i) (5) = 30. bacc=20,
cf=60, ev=28, drop=0.

IMPADV3-M2 (mode5): churn entries have importance 3 (masks 28). The 10
benign hop-2 keys (popcount 2 and 3, stamps 2..20) are all strictly
below 3 and older than every churn entry, so relocations 1..10 evict
all 10 benign hop-2 keys, then 18 churn entries. Destroyed: every
hop-2 key. post: loop1 0 (hop2 gone for all i), loop2 0, loop3 0
(hop2 gone for i=1..5), loop4 10 (hop1 intact). post=10,
ret=(100*10)/35=28 (integer). rawA: owner-1 hop1 (10), owner-2 hop3
(10), owner-4 (2000+i) (5) = 25. bacc=20, cf=60, ev=28, drop=0.

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
- K13 ADV-DOSE: IMPADV3-M2 ret==28 AND post==10 AND rawA==25 AND
  ev==28 AND drop==0 AND cf==60. Higher inflation kills deeper: the
  policy protects exactly the entries with importance strictly above
  the adversary's inflated level.
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

PREREG.md + NAMECHECK.md commit strictly first. Implementation
(importance_h1.zag), build, runs, and REPORT.md only after.
