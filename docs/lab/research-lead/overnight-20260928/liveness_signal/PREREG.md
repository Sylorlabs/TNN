# PREREG: LIVENESS-SIGNAL probe (owner-blind liveness reclamation vs multi-owner churn)

Frozen 2026-10-03. This preregistration strictly precedes implementation.
This prereg commit contains ONLY PREREG.md and NAMECHECK.md. No kill bar
below may be weakened or reinterpreted after results are seen. VOID is
terminal: it is corrected only by fresh preregistration plus a fresh run,
never by salvage or amend-and-promote.

Worker: LIVENESS-SIGNAL worker (non-ledger task; claim minting paused).
Lane: `docs/lab/research-lead/overnight-20260928/liveness_signal/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation; shell only for
znc invocation, binary execution, git ops, sha256sum, and file movement.
Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## Objective

CONSENT-MULTIOWNER (VERDICT=PASS 10/10, 2026-10-03) found owner-consent
reclamation holds retention (ret=100) under multi-owner churn but K8
showed the sharp verdict: when the consent mask misses every churner,
consent degenerates to no-reclaim pinning bit for bit. The report's
recommended follow-up: "an owner-blind liveness signal (K8 shows any
identity-keyed signal inherits a boundary)." This lane builds that
signal and asks the parent question directly: does an owner-blind
liveness signal avoid the boundary problem, and what are its failure
modes?

## Mechanism under test: policy 6 (PIN-LIVELINESS)

Substrate identical to CONSENT-MULTIOWNER (same header layout, same
pool, same primary, same conflict path, same owner-scoped reads, same
A family, same benign B writer, same multi-owner churn modes 1/2/3,
same single-owner churn). The touch side table (base 2624, 32 x 4
bytes, last-touch stamp per pool slot) already exists in the substrate;
it is stamped on pool install and on pool reads, and is currently
unused by any policy. The only new code is the policy-6 reclamation
rule: when the pool is full, scan all used slots and evict the one
with the minimum last-touch stamp (ties broken by lowest slot index,
deterministic); ev++; install the new entry with a fresh stamp. Owner
identity is never consulted anywhere in the reclamation decision.
This is the canonical owner-blind liveness signal: least-recently-
touched reclamation, using recency of reads/writes via the existing
touch stamps.

A frequency-count variant would order identically on this workload:
without re-reads every pool entry has exactly one touch (its install),
so frequency ties everywhere and the tie-break evicts benign slots
first, the same collapse. Frequency is therefore analyzed, not
reimplemented.

## Protocol (frozen)

Per condition, on a freshly zeroed workspace: 1. teach A family
(multi). 2. pre-test (expect 35). 3. teach B benign FULL (20
conflicts, 20 A victims pinned in pool slots 0..19, slots 20..31
free). 4. churn: single-owner key 3999 (w in {1,21,33}) or
multi-owner mode 1/2/3 (w=21 per key). 5. post-test; retention =
100*post/pre. 6. record conflicts, evictions, drop, B accuracy, rawA.

One new protocol variant: LIVR-M2 re-runs the full A test (35
owner-scoped queries, which re-stamp every benign pool entry through
the pool read path) after every churn round. This is the "recency of
reads" condition made load-bearing: it tests whether the liveness
signal protects pinned knowledge when the workload re-touches it.

Conditions (16). Anchors LIVCON-*/LIVPIN-* reproduce the frozen
CONSENT-MULTIOWNER table exactly (policies 3 and 5 on the new
substrate). New rows use policy 6.

| cond      | pol | adv        | pre | post | ret | cf | ev | drop | bacc | rawA |
|-----------|-----|------------|-----|------|-----|----|----|------|------|------|
| LIVCON-B0 | 5   | single w1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| LIVCON-A20| 5   | single w21 | 35  | 35   | 100 | 40 | 8  | 0    | 20   | 35   |
| LIVCON-A32| 5   | single w33 | 35  | 35   | 100 | 52 | 20 | 0    | 20   | 35   |
| LIVPIN-M2 | 3   | mode1      | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| LIVPIN-M3 | 3   | mode2      | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| LIVCON-M2 | 5   | mode1      | 35  | 35   | 100 | 60 | 11 | 17   | 20   | 35   |
| LIVCON-M3 | 5   | mode2      | 35  | 35   | 100 | 80 | 5  | 43   | 20   | 35   |
| LIVPIN-X2 | 3   | mode3      | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| LIVCON-X2 | 5   | mode3      | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| LIV-B0    | 6   | single w1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| LIV-A20   | 6   | single w21 | 35  | 19   | 54  | 40 | 8  | 0    | 20   | 27   |
| LIV-A32   | 6   | single w33 | 35  | 0    | 0   | 52 | 20 | 0    | 20   | 15   |
| LIV-M2    | 6   | mode1      | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| LIV-M3    | 6   | mode2      | 35  | 0    | 0   | 80 | 48 | 0    | 20   | 15   |
| LIV-X2    | 6   | mode3      | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| LIVR-M2   | 6   | mode1+reread| 35 | 35   | 100 | 60 | 28 | 0    | 20   | 35   |

## Derivation notes (frozen with the prereg)

Benign phase identical in all conditions: 20 A victims pin pool slots
0..19 with install stamps 1..20 (clock=20); slots 20..31 free.

LIV-A20: 20 churn conflicts. 12 fill slots 20..31 (stamps 21..32).
8 relocations under pool-full: min-stamp scan evicts slots 0..7
(stamps 1..8), the oldest benign entries, ev=8, drop=0. Evicted pool
keys: 1011,1012,1021,1022,1031,1032,1041,1042. post=test_A: loop1
(owner 1) i=1..4 miss, i=5..10 hit = 6; loop2 (owner 2) i=1..4 miss,
i=5..10 hit = 6; loop3 (owner 4) only i=5 fully hits = 1; loop4
(owner 8) i=5..10 hit = 6. post=19, ret=(100*19)/35=54 (integer).
rawA: owner-1 key reads hit for i=5..10 (12), (i,3)/owner-2 primary
reads hit (10), (2000+i)/owner-4 primary reads hit (5) = 27. bacc=20
(B primary untouched by key-3999 churn). cf=40.

LIV-A32: 32 conflicts = 12 fills + 20 evictions; slots 0..19 all
evicted (stamps 1..20 are the global minima throughout). ev=20,
drop=0. Every displaced A value gone: post=0, ret=0. rawA: only
primary-resident reads survive: (i,3)/owner-2 = 10, (2000+i)/owner-4
= 5, total 15. bacc=20, cf=52.

LIV-M2: 40 churn conflicts (cf=60) = 12 fills + 28 relocations.
Relocations 1..20 evict slots 0..19 (benign, stamps 1..20);
relocations 21..28 evict slots 20..27 (oldest churn installs, stamps
21..28; slots 0..19 now carry stamps 33..52). ev=28, drop=0. All
benign displaced values evicted: post=0, ret=0, rawA=15, bacc=20.

LIV-M3: 60 churn conflicts (cf=80) = 12 fills + 48 relocations.
Same ordering: all 20 benign evicted first, then oldest churn
installs. ev=48, drop=0, ret=0, rawA=15, bacc=20.

LIV-X2: 40 churn conflicts (cf=60) = 12 fills + 28 relocations,
identical footprint to M2. ev=28, drop=0, ret=0, rawA=15, bacc=20.
Sharp contrast with LIVCON-X2 (ev=0, drop=28, ret=100): where consent
degenerated to pinning and kept retention, liveness reclaims the
capacity by destroying the pinned entries.

LIVR-M2: each round ends with a full A re-read (60 pool stamps),
so after every round all benign stamps are newer than every churn
install stamp. Invariant at each eviction: min benign stamp >
min churn stamp, so the two oldest churn installs are evicted each
round and no benign slot is ever the minimum. Rounds 8..21: 28
evictions of churn history only. ev=28, drop=0, ret=100, rawA=35,
bacc=20, cf=60 (reads add no conflicts).

## Frozen kill bars

- K1 ANCHOR-CONSENT: LIVCON-B0/A20/A32 match the frozen
  CONSENT-MULTIOWNER consent rows exactly, every column
  (ret=[100,100,100], cf=[20,40,52], ev=[0,8,20], drop=[0,0,0],
  bacc=20, rawA=35). Else VOID: the substrate moved.
- K2 ANCHOR-PIN-MULTI: LIVPIN-M2/M3 match the frozen
  MULTI-OWNER-CHURN PIN rows exactly (ret=[100,100], cf=[60,80],
  ev=[0,0], drop=[28,48], bacc=20, rawA=35). Else VOID.
- K3 ANCHOR-CONSENT-MULTI: LIVCON-M2/M3/X2 match the frozen
  CONSENT-MULTIOWNER rows exactly (ret=100 x3, cf=[60,80,60],
  ev=[11,5,0], drop=[17,43,28], bacc=20, rawA=35); LIVPIN-X2 matches
  the frozen PIN-M2 row exactly. Else VOID: the baseline moved.
- K4 LIVE-COLLAPSE-M2: LIV-M2 ret==0 AND ev==28 AND drop==0 AND
  rawA==15. The owner-blind signal evicts the pinned knowledge
  first and restores full capacity doing it.
- K5 LIVE-COLLAPSE-M3: LIV-M3 ret==0 AND ev==48 AND drop==0 AND
  rawA==15.
- K6 LIVE-COLLAPSE-X2: LIV-X2 ret==0 AND ev==28 AND drop==0 AND
  rawA==15. Where consent kept ret=100 by reclaiming nothing,
  liveness reclaims everything by evicting the benign entries.
- K7 LIVE-SINGLE-LADDER: LIV-B0 ret==100, ev==0, drop==0;
  LIV-A20 ret==54, ev==8, drop==0, rawA==27;
  LIV-A32 ret==0, ev==20, drop==0, rawA==15. Exact white-box trace
  of the collapse on the single-owner ladder.
- K8 REUSE-SAVES: LIVR-M2 ret==100 AND rawA==35 AND ev==28 AND
  drop==0. The liveness signal protects pinned knowledge if and
  only if the workload re-touches it; then it restores full
  capacity with full retention.
- K9 BOUNDARY-RELOCATED: LIV-M2 ret (0) < LIVCON-M2 ret (100)
  AND LIV-M2 ev (28) > LIVCON-M2 ev (11). The owner-blind signal
  restores more capacity than consent but loses all retention:
  the boundary is relocated from identity to time, not removed.
- K10 ADV-FIXED: conflicts identical across policies per dose:
  40 at single w=21 (LIVCON-A20, LIV-A20); 52 at single w=33
  (LIVCON-A32, LIV-A32); 60 at mode1 (LIVPIN-M2, LIVCON-M2,
  LIV-M2, LIVR-M2); 60 at mode3 (LIVPIN-X2, LIVCON-X2, LIV-X2);
  80 at mode2 (LIVPIN-M3, LIVCON-M3, LIV-M3).
- K11 DETERMINISM: 3/3 runs byte-identical (sha256 equal). Else
  VOID.

Verdict: PASS iff K1..K11 all hold. Any kill-bar miss names the bar
and yields FAIL. K1, K2, K3, or K11 failure yields VOID. Thresholds
are frozen; they are not moved after results.

Discrimination design: K1/K2/K3 anchor the full consent baseline (a
moved substrate or baseline invalidates the probe); K4/K5/K6 test the
headline collapse prediction (liveness evicts pinned knowledge first,
the opposite of consent's guarantee); K7 tests the exact single-owner
ladder trace, which falsifies the worker's mechanism model if any
number is off; K8 tests the reuse condition under which the signal
can work; K9 is the direct consent-vs-liveness comparison; K10 bars
the "stronger adversary under one policy" confound.

## What this does NOT test

The liveness signal is least-recently-touched only; no frequency
counter is implemented (analyzed as ordering-identical in the
mechanism section). The re-read workload in LIVR-M2 is
researcher-scheduled, not learner-issued; learner-originated
re-touch is out of scope. The consent mask stays fixed at 16. No
repair is proposed or canonized: the measured prices are evidence,
not a work order for a LIVENESS-2. Owner-scoped reads are retained,
so the label-free routing caveat carries over unchanged.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first. Implementation
(liveness_signal.zag), build, runs, and REPORT.md only after.
