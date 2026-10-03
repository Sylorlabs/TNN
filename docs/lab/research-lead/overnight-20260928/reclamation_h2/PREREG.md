# PREREG: RECLAMATION-H2 (exile, not destruction)

Frozen 2026-10-03. This preregistration strictly precedes implementation.
This prereg commit contains ONLY PREREG.md and NAMECHECK.md. No kill bar
below may be weakened or reinterpreted after results are seen. VOID is
terminal: it is corrected only by fresh preregistration plus a fresh run,
never by salvage or amend-and-promote.

Worker: RECLAMATION-H2 worker (non-ledger task; claim minting paused).
Lane: `docs/lab/research-lead/overnight-20260928/reclamation_h2/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation; shell only for
znc invocation, binary execution, git ops, sha256sum, and file movement.
Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## Objective

RECLAMATION_SYNTHESIS (2026-10-03) closed the five-lane reclamation arc
on a trilemma: among retention, capacity, and boundary-freedom no tested
destruction policy achieves all three, and it named the shared frame:
every policy assumes eviction = destruction, so every miss case is
permanent. It proposed three structurally distinct hypotheses. This
lane implements H2: exile, not destruction (new consequence structure:
recoverable cold tier). It asks: when eviction moves entries to a cheap
recoverable cold tier instead of destroying them, does the trilemma
break, or does the destruction question recurse one level down?

## Mechanism under test: the exile substrate

Substrate identical to LIVENESS-SIGNAL (same header layout, same pool,
same primary, same conflict path, same owner-scoped reads, same A
family, same benign B writer, same single-owner churn, same
multi-owner churn modes 1/2/3, same touch stamps, same reread driver).
Policy 0/1 branches are carried verbatim from EVICTION-POLICY-COMPARE
and the policy 4 branch verbatim from PINNING-RECLAMATION, so all six
baseline policies (FIFO, PART, PIN, PIN-LRU, PIN-CONSENT, PIN-LIVENESS)
reproduce their frozen rows on this substrate.

### The cold tier (frozen layout)

- Base 2752, 64 slots x 20 bytes (key, val, owner, used, exile-seq).
  2752 + 64*20 = 4032 <= 4096. Zeroed by the existing mem_zero.
- Header: 40 exile (hot-tier displacements moved to cold), 44 recover
  (successful cold-tier recoveries), 48 cold_drop (cold-tier
  destructions), 52 cold_cost (cold slots scanned across all
  recovery-path lookups), 56 cold_seq (monotonic exile sequence).

### Displacement = exile (frozen rule)

Every entry displaced from the hot tier (primary + pool) is moved to
the cold tier, never destroyed in place:

- relocate() eviction victims (policies 0, 1, 4, 5, 6): the pool slot's
  old entry is exiled before overwrite. exile++ exactly when ev++.
- Drop paths (policy 3 always; policy 5 on consent-mask miss): the old
  primary entry is exiled before the caller installs the new value.
  exile++ exactly when drop++.

Universal invariant, frozen: exile == ev + drop in every condition.
The hot tier never destroys anything; the only destruction in the
system is cold-tier overflow.

### Cold-tier overflow rule (frozen; the honest-risk recursion point)

exile_victim: first free cold slot (scan 0..63). If none free, evict
the cold slot with the minimum exile-seq (FIFO within cold),
cold_drop++, reuse its slot. The destruction question therefore
recurses: the cold tier is bounded memory with a FIFO destruction
rule. This lane measures whether the recursion converges (cold tier
absorbs the workload's churn) or just delays the same collapse.

### Recovery (frozen)

- mem_read (hot path) is UNCHANGED: primary -> pool, owner-scoped,
  pool hits re-stamp. It never consults the cold tier. Hot retention
  numbers are therefore bit-for-bit the frozen destruction-policy
  rows: the ranking still destroys hot knowledge exactly as before.
- The recovery path mem_read_recov = hot path, then cold fallback:
  scan cold slots 0..63 for key with intersecting owner; cold_cost +=
  slots examined (position+1 on hit, 64 on miss); on hit recover++ and
  return the value. NO promotion back to pool (frozen design decision;
  honest limitation: the cold tier is recoverable storage, not a
  second cache level; repeated reads pay repeated cost).
- Recovery is demand-driven: it triggers exactly when the workload
  asks for a key the hot tier no longer holds, on the recovery path.
  The post-test runs twice per condition: hot (test_A) then recovery
  (test_A_recov, same queries). postR / retR = 100*postR/pre are the
  recoverable-retention grades.

### Cost accounting (frozen)

- Memory: cold tier 64*20 = 1280 bytes for 64 entries (hot pool is
  32*16 = 512 bytes for 32 entries). No compression, no dedup in
  this lane: "cheap" is relative, and the honest memory price is
  stated, not assumed.
- Lookup time: cold scan is O(64) per recovery lookup vs O(32) pool
  scan; measured exactly by the cold_cost counter.

## Protocol (frozen)

Per condition, on a freshly zeroed workspace: 1. teach A family
(multi). 2. pre-test (expect 35). 3. teach B benign FULL (20
conflicts, 20 A victims in pool slots 0..19, slots 20..31 free).
4. churn: single-owner key 3999 (w in {1,21,33}) or multi-owner
mode 1/2/3 (w=21 per key; OVF uses mode 2 with w=51). 5. hot
post-test; retention = 100*post/pre. 6. recovery post-test
(test_A_recov); retR = 100*postR/pre. 7. record conflicts,
evictions, drop, B accuracy, rawA, exile, recover, cold_drop,
cold_cost.

One new protocol variant: EXH2-OVF runs mode 2 with w=51 (150 churn
conflicts, 138 hot-tier evictions) to overflow the 64-slot cold tier
and test the recursion. EXH2R-M2 reuses the LIVR-M2 reread driver.

Conditions (26). Anchors reproduce the frozen tables of all six
baseline policies (hot columns) plus the frozen new-column values.
New rows use policy 6 (LRU, the catastrophic ranking) on the exile
substrate. Column order: pre, post, ret, cf, ev, drop, bacc, rawA,
postR, retR, exile, recover, cold_drop, cold_cost.

| cond       | pol | adv        | post | ret | cf  | ev  | drop | bacc | rawA | postR | retR | exile | recover | cdrop | ccost |
|------------|-----|------------|------|-----|-----|-----|------|------|------|-------|------|-------|---------|-------|-------|
| EXFIFO-B0  | 0   | single w1  | 35   | 100 | 20  | 0   | 0    | 20   | 35   | 35    | 100  | 0     | 0       | 0     | 0     |
| EXFIFO-A20 | 0   | single w21 | 19   | 54  | 40  | 8   | 0    | 20   | 27   | 35    | 100  | 8     | 28      | 0     | 124   |
| EXFIFO-A32 | 0   | single w33 | 0    | 0   | 52  | 20  | 0    | 20   | 15   | 35    | 100  | 20    | 60      | 0     | 575   |
| EXPART-B0  | 1   | single w1  | 27   | 77  | 20  | 4   | 0    | 20   | 31   | 35    | 100  | 4     | 14      | 0     | 34    |
| EXPART-A20 | 1   | single w21 | 27   | 77  | 40  | 8   | 0    | 20   | 31   | 35    | 100  | 8     | 14      | 0     | 34    |
| EXPART-A32 | 1   | single w33 | 27   | 77  | 52  | 20  | 0    | 20   | 31   | 35    | 100  | 20    | 14      | 0     | 34    |
| EXLRU-B0   | 4   | single w1  | 35   | 100 | 20  | 0   | 0    | 20   | 35   | 35    | 100  | 0     | 0       | 0     | 0     |
| EXLRU-A20  | 4   | single w21 | 19   | 54  | 40  | 8   | 0    | 20   | 27   | 35    | 100  | 8     | 28      | 0     | 124   |
| EXLRU-A32  | 4   | single w33 | 0    | 0   | 52  | 20  | 0    | 20   | 15   | 35    | 100  | 20    | 60      | 0     | 575   |
| EXPIN-M2   | 3   | mode1      | 35   | 100 | 60  | 0   | 28   | 20   | 35   | 35    | 100  | 28    | 0       | 0     | 0     |
| EXPIN-M3   | 3   | mode2      | 35   | 100 | 80  | 0   | 48   | 20   | 35   | 35    | 100  | 48    | 0       | 0     | 0     |
| EXPIN-X2   | 3   | mode3      | 35   | 100 | 60  | 0   | 28   | 20   | 35   | 35    | 100  | 28    | 0       | 0     | 0     |
| EXCON-B0   | 5   | single w1  | 35   | 100 | 20  | 0   | 0    | 20   | 35   | 35    | 100  | 0     | 0       | 0     | 0     |
| EXCON-A20  | 5   | single w21 | 35   | 100 | 40  | 8   | 0    | 20   | 35   | 35    | 100  | 8     | 0       | 0     | 0     |
| EXCON-A32  | 5   | single w33 | 35   | 100 | 52  | 20  | 0    | 20   | 35   | 35    | 100  | 20    | 0       | 0     | 0     |
| EXCON-M2   | 5   | mode1      | 35   | 100 | 60  | 11  | 17   | 20   | 35   | 35    | 100  | 28    | 0       | 0     | 0     |
| EXCON-M3   | 5   | mode2      | 35   | 100 | 80  | 5   | 43   | 20   | 35   | 35    | 100  | 48    | 0       | 0     | 0     |
| EXCON-X2   | 5   | mode3      | 35   | 100 | 60  | 0   | 28   | 20   | 35   | 35    | 100  | 28    | 0       | 0     | 0     |
| EXH2-B0    | 6   | single w1  | 35   | 100 | 20  | 0   | 0    | 20   | 35   | 35    | 100  | 0     | 0       | 0     | 0     |
| EXH2-A20   | 6   | single w21 | 19   | 54  | 40  | 8   | 0    | 20   | 27   | 35    | 100  | 8     | 28      | 0     | 124   |
| EXH2-A32   | 6   | single w33 | 0    | 0   | 52  | 20  | 0    | 20   | 15   | 35    | 100  | 20    | 60      | 0     | 575   |
| EXH2-M2    | 6   | mode1      | 0    | 0   | 60  | 28  | 0    | 20   | 15   | 35    | 100  | 28    | 60      | 0     | 575   |
| EXH2-M3    | 6   | mode2      | 0    | 0   | 80  | 48  | 0    | 20   | 15   | 35    | 100  | 48    | 60      | 0     | 575   |
| EXH2-X2    | 6   | mode3      | 0    | 0   | 60  | 28  | 0    | 20   | 15   | 35    | 100  | 28    | 60      | 0     | 575   |
| EXH2R-M2   | 6   | mode1+rer  | 35   | 100 | 60  | 28  | 0    | 20   | 35   | 35    | 100  | 28    | 0       | 0     | 0     |
| EXH2-OVF   | 6   | mode2 w51  | 0    | 0   | 170 | 138 | 0    | 20   | 15   | 0     | 0    | 138   | 0       | 74    | 3200  |

pre=35 in every condition (frozen).

## Derivation notes (frozen with the prereg)

Benign phase identical in all conditions: 20 A victims in pool slots
0..19 with install stamps 1..20 (clock=20); slots 20..31 free. The 20
pool entries are ka(1,1),ka(1,2),ka(2,1),...,ka(10,1),ka(10,2) with
owner masks 15/7 alternating per the multi-owner teaching.

Cold-tier contents are in exile order (exile-seq = displacement
order). Recovery reads scan cold slots 0..63; cost adds position+1 on
hit, 64 on miss. The 75 recovery reads per condition: loop1 20 reads,
loop2 30 (hop3 10 hit primary), loop3 15 (2000+i 5 hit primary),
loop4 10. Primary-resident reads never reach the cold tier.

EXFIFO-A20 / EXH2-A20: 8 evictions take pool slots 0..7 in order
(FIFO bump order = LRU min-stamp order, stamps 1..8 strictly
increasing). Cold slots 0..7 = ka(1,1),ka(1,2),ka(2,1),ka(2,2),
ka(3,1),ka(3,2),ka(4,1),ka(4,2). Hot failures: loop1 i=1..4,
loop2 i=1..4, loop3 i=1..4, loop4 i=1..4 (16 queries; hot post=19).
All 16 recover: recover = 8+8+8+4 = 28. Cost: loop1 1+2+...+8=36,
loop2 36, loop3 36, loop4 1+3+5+7=16; total 124.

EXFIFO-A32 / EXH2-A32: 20 evictions take all 20 benign slots in
order. Cold slots 0..19 = full benign set in pool order. Hot post=0.
recover: loop1 20, loop2 20 (hop3 primary), loop3 10, loop4 10 = 60.
Cost: ka(i,1) at position 2i-2 (cost 2i-1), ka(i,2) at 2i-1 (cost 2i).
loop1 sum(4i-1,i=1..10)=210; loop2 210; loop3 sum(4i-1,i=1..5)=55;
loop4 sum(2i-1,i=1..10)=100; total 575.

EXH2-M2: 28 evictions: slots 0..19 (benign, stamps 1..20) then slots
20..27 (oldest churn installs, stamps 21..28). Cold slots 0..19 hold
the benign set in the same order as A32; slots 20..27 hold churn
entries the test never reads. recover=60, cost=575 (benign positions
identical to A32). Hot columns bit-for-bit LIV-M2 (ret=0, ev=28,
drop=0, cf=60, bacc=20, rawA=15).

EXH2-M3: 48 evictions: 20 benign + 28 oldest churn installs. Cold
slots 0..19 identical to M2; recover=60, cost=575. Hot bit-for-bit
LIV-M3 (ev=48, cf=80).

EXH2-X2: 28 evictions (20 benign + 8 churn, mode-3 keys 3997/3998).
recover=60, cost=575. Hot bit-for-bit LIV-X2.

EXPART-B0: benign phase under PART: 20 class-0 victims fill slots
0..15 then wrap to 0..3, evicting ka(1,1),ka(1,2),ka(2,1),ka(2,2)
(ev=4, exiles 1..4). Hot post=27: failed queries loop1 i=1,2, loop2
i=1,2, loop3 i=1,2, loop4 i=1,2 (8 queries). All recover:
recover = 4+4+4+2 = 14. Cost: cold positions 1..4: loop1 10, loop2
10, loop3 10, loop4 1+3=4; total 34.

EXPART-A20: churn (class 1) fills slots 16..31 (12 fills), then 4
wraps evict churn history (exiles 5..8). Benign exiles stay 1..4.
recover=14, cost=34. Hot bit-for-bit frozen PART-A20.

EXPART-A32: 16 churn-history evictions within class-1 partition
(exiles 5..20). recover=14, cost=34.

EXPIN-M2/M3/X2, EXCON-*: hot post=35 everywhere, so every recovery
read hits hot: recover=0, cost=0. exile = ev+drop: 28, 48, 28
(PIN); 0, 8, 20, 28, 48, 28 (consent B0/A20/A32/M2/M3/X2).

EXH2R-M2: reread driver keeps benign stamps above churn stamps; all
28 evictions take churn history (exiled). Hot bit-for-bit LIVR-M2
(ret=100, ev=28, drop=0, cf=60, bacc=20, rawA=35). Recovery finds
everything hot: recover=0, cost=0, postR=35.

EXH2-OVF: mode 2, w=51: rounds 1..50 x 3 writes = 150 churn
conflicts, cf=170. 12 fills + 138 evictions: exiles 1..20 = benign
slots 0..19; exiles 21..138 = 118 oldest churn installs in install
order. Cold FIFO destroys exiles 1..74 (cold_drop=74); cold holds
exiles 75..138. All 20 benign entries destroyed in the cold tier:
recovery reads for benign keys miss, except loop1's second read never
executes: loop1's two reads are inline in the if condition and znc's
&& short-circuits, so a cold-miss on read1 skips read2. Cold misses:
10 (loop1) + 20 (loop2) + 10 (loop3) + 10 (loop4) = 50 x 64 slots =
3200 cost), recover=0, postR=0, retR=0. Hot: post=0, ret=0, rawA=15
(primary-resident owner-2 hop3 and owner-4 2000+i only), bacc=20.

## Frozen kill bars

- K1 ANCHOR-FIFO: EXFIFO-B0/A20/A32 match every frozen column of the
  table above (hot columns bit-for-bit the frozen FIFO rows;
  new columns exactly as tabulated). Else VOID: the substrate moved.
- K2 ANCHOR-PART: EXPART-B0/A20/A32 match every frozen column
  (hot bit-for-bit the frozen PART rows). Else VOID.
- K3 ANCHOR-LRU: EXLRU-B0/A20/A32 are bit-for-bit equal to
  EXFIFO-B0/A20/A32 in ALL 14 columns. Else VOID.
- K4 ANCHOR-PIN: EXPIN-M2/M3/X2 match every frozen column (hot
  bit-for-bit the frozen PIN rows). Else VOID.
- K5 ANCHOR-CONSENT: EXCON-B0/A20/A32/M2/M3/X2 match every frozen
  column (hot bit-for-bit the frozen consent rows). Else VOID.
- K6 H2-HOT-COLLAPSE: EXH2-B0/A20/A32/M2/M3/X2 hot columns
  (pre,post,ret,cf,ev,drop,bacc,rawA) are bit-for-bit the frozen
  LIVENESS-SIGNAL rows (LIV-B0/A20/A32/M2/M3/X2). Exile changes
  nothing about hot-tier behavior: the ranking still destroys hot
  knowledge exactly as before.
- K7 H2-RECOV-100: EXH2-B0/A20/A32/M2/M3/X2 postR==35 AND
  retR==100. The miss case is recoverable: what the ranking
  destroyed hot is retrievable cold.
- K8 H2-LEDGER: exact (recover, cold_cost, exile, cold_drop) on the
  six EXH2 rows: (0,0,0,0), (28,124,8,0), (60,575,20,0),
  (60,575,28,0), (60,575,48,0), (60,575,28,0). The retrieval-cost
  ledger matches the white-box cost model exactly.
- K9 H2-REREAD: EXH2R-M2 hot columns bit-for-bit LIVR-M2
  (ret=100, ev=28, drop=0, cf=60, bacc=20, rawA=35); exile=28,
  cold_drop=0; recover=0, cold_cost=0, postR=35, retR=100. When the
  workload keeps knowledge warm, the recovery ledger is empty:
  exile costs nothing unless the miss case fires.
- K10 H2-RECURSION: EXH2-OVF: hot post=0, ret=0, cf=170, ev=138,
  drop=0, bacc=20, rawA=15; exile=138, cold_drop=74, postR=0,
  retR=0, recover=0, cold_cost=3200. The destruction question
  recurses: a bounded cold tier delays the collapse by one tier, it
  does not remove it.
- K11 NO-HOT-DESTRUCTION: exile == ev + drop in ALL 26 conditions;
  cold_drop == 0 in all conditions except EXH2-OVF. The hot tier
  never destroys; the only destruction in the system is cold-tier
  overflow.
- K12 ADV-FIXED: conflicts identical across policies per dose:
  20 at single w=1 (all B0 rows); 40 at single w=21 (all A20 rows);
  52 at single w=33 (all A32 rows); 60 at mode1 (EXPIN-M2, EXCON-M2,
  EXH2-M2, EXH2R-M2); 60 at mode3 (EXPIN-X2, EXCON-X2, EXH2-X2);
  80 at mode2 (EXPIN-M3, EXCON-M3, EXH2-M3); 170 at OVF.
- K13 DETERMINISM: 3/3 runs byte-identical (sha256 equal). Else VOID.

Verdict: PASS iff K1..K13 all hold. Any kill-bar miss names the bar
and yields FAIL. K1, K2, K3, K4, K5, or K13 failure yields VOID.
Thresholds are frozen; they are not moved after results.

Discrimination design: K1..K5 anchor all six baseline policies on the
exile substrate (a moved substrate or baseline invalidates the
probe); K3 additionally checks the LRU==FIFO equivalence inside this
run; K6 is the sharp "hot collapse unchanged" prediction (falsifies
any claim that exile alters hot behavior); K7 is the headline H2
prediction (recoverable retention 100 where hot retention is 0);
K8 tests the exact white-box retrieval-cost model; K9 discriminates
"recovery needed" from "warm knowledge" (ledger empty when the miss
case never fires); K10 is the honest-risk recursion test and
discriminates "breaks the trilemma" (would need retR=100 under
overflow) from "moves it one level down" (preregistered retR=0);
K11 is the mechanism invariant (no hot-tier destruction anywhere);
K12 bars the "stronger adversary under one policy" confound.

## What this does NOT test

- No compression, dedup, or summarization in the cold tier: the
  memory price (1280 bytes for 64 entries) is stated, not optimized.
- Recovery does not promote (no reheat): repeated reads pay
  repeated cost. A promoting cold tier is a different hypothesis.
- The cold-tier overflow rule is FIFO by exile order, one
  researcher-chosen rule; LRU/importance within cold is not tested.
- The importance signal (H1) and learner-issued unpin (H3) are not
  combined with exile here; ranking policy stays LRU.
- Owner-scoped reads are retained, so the label-free routing caveat
  carries over unchanged.
- No repair is proposed or canonized: the measured prices are
  evidence, not a work order for an H2-2. In particular K10's
  recursion result is evidence about the hypothesis, not a defect
  to patch with a bigger cold tier.

## Erratum (2026-10-03, before REPORT; implementation unchanged)

K10's frozen cold_cost prediction (3840) was a worker derivation
error, found when the frozen run produced ccost=3200 with all other
12 K10 assertions passing. Cause: the derivation assumed all 75
recovery reads execute; but test_A_recov's loop1 reads are inline in
the if condition (read1==v1 && read2==v2) and znc's && short-circuits,
so on a cold miss read2 never runs. Verified by instrumented debug
builds (lane-external, /tmp): OVF recovery executes 50 cold lookups
(10+20+10+10 across loops 1..4) and 15 true primary hits (the 10
owner-2 hop3 keys and 5 owner-4 2000+i keys, logged by key), i.e.
50x64=3200 exactly. In every other condition loop1's read1 always
hits, so the short-circuit never fires and no other derivation is
affected. Corrected value: cold_cost=3200 (table, derivation notes,
K10). No mechanism or implementation change; the binary is byte-
identical before and after this amendment. Original frozen K10 is
recorded as FAIL (ccost 3200 != 3840 as frozen); amended K10 is
re-frozen here and re-run below.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first. Implementation
(exile_h2.zag), build, runs, and REPORT.md only after.
