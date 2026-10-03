# PREREG: EXILE-PROMOTION (promotion / reheat dynamics)

Date: 2026-10-03. Worker: EXILE-PROMOTION (non-ledger task; claim
minting paused). Lane:
`docs/lab/research-lead/overnight-20260928/exile_promotion/`.

Parent: RECLAMATION-H2 (VERDICT=PASS 13/13, 2026-10-03). H2's frozen
design decision: "the recovery path falls through to a cold scan on
hot miss, counting recoveries and slots scanned, with NO promotion
back to pool." This lane tests the follow-up H2 named explicitly:
promotion/reheat dynamics. The question: is exile + promotion a real
two-tier memory hierarchy, or just a slower leak?

## Frozen design

Build on RECLAMATION-H2; do not redesign. The hot mechanism
(primary, pool, touch stamps, all six policy branches), the cold
tier (64 slots x 20 bytes), exile_victim, the FIFO cold-overflow
rule, and the recovery path are carried over unchanged. pm=0
reproduces H2 bit-for-bit (K1 anchors prove it). New machinery is
additive only:

1. Header offset 60: `promote` counter (successful cold->pool moves).
2. Recovery-count side table: base 4032, 64 x u8, one per cold slot
   (fits the 64 free bytes 4032..4095 exactly; mem_zero already
   clears them). Mirrors the pool touch side-table pattern.
3. exile_victim resets the slot's recovery count to 0 on every
   install (fresh slot and FIFO-drop overwrite alike).
4. cold_lookup(M,key,owner,pm): on a cold hit, the slot's recovery
   count increments (capped at 250). If pm==1 and count reaches the
   frozen threshold T=2, promote_slot fires, then the value returns.
   pm==0 never promotes.
5. promote_slot(M,cs): MOVES the entry, never copies. The cold slot
   is freed (used=0, count reset). Target pool slot: first free slot
   if the pool is not full; else the used slot with minimum
   last-touch stamp (ties: lowest index), mirroring policy 6's
   reclamation exactly. A displaced pool victim is re-exiled via
   exile_victim (priced demotion), never destroyed. promote++ per
   move.

The hot read path (mem_read) is untouched and never consults cold.
The recovery path is mem_read -> cold scan on miss, as in H2, plus
the promotion trigger on the T-th recovery of one entry.

## Answers to the design questions (frozen predictions)

**What triggers promotion?** Per-entry recovery-count threshold
T=2 (frozen constant). First recovery = demand signal; second
recovery = confirmed repeated demand -> reheat. Recency was
considered and rejected for this lane: it needs cold-tier
timestamps (more machinery); the count is the minimal honest
mechanism that tests "frequently-recovered cold entries get
promoted back to hot". Recency stays a named follow-up.

**What gets demoted to make room?** Yes, promotion causes hot
eviction when the pool is full: the victim is the minimum
last-touch pool slot (the LRU rule, consistent with policy 6's own
reclamation). The victim is re-exiled, so demotion is priced in
the ledger (exile++), not silent destruction. When the pool has a
free slot, promotion installs without eviction.

**Does promotion break the "priced, delayed destruction"
accounting?** Prediction: no. The invariant extends to
exile == ev + drop + promote (K6), given every promotion in these
conditions finds a full pool. cold_drop remains the ONLY
destruction counter. Promotion moves entries between tiers
(exclusive occupancy: an entry lives in exactly one tier at a
time), so no duplication leak is possible by construction.

**Headline hypothesis:** exile + promotion is a real two-tier
hierarchy: repeated access amortizes (3-pass cold cost strictly
below the frozen no-promo 3-pass total), the working set reheats
(hot-path retention returns to 100), and cold occupancy stays
bounded (no growth across passes). The kill form: if the 3-pass
cold cost does not beat no-promo, or hot retention is not
restored, or cold occupancy grows across passes, the hierarchy
claim FAILS (it would be a slower leak).

## Conditions

Anchors (pm=0; 14-column rows; must equal H2's frozen rows
bit-for-bit):
- A0 EXH2-B0: pol 6, churn w=1, mode 0 (H2 row @1008)
- A1 EXH2-A32: pol 6, churn w=33, mode 0 (H2 row @1120)
- A2 EXH2-M2: pol 6, churn w=21, mode 1 (H2 row @1176)
- A3 EXH2-OVF: pol 6, churn w=51, mode 2, mw=51 (H2 row @1400)
- A4 EXCON-M2: pol 5, churn w=21, mode 1 (H2 row @840)

Promotion conditions (pm=1; 32-field rows; driver: teach, churn,
three recovery passes R1/R2/R3 with per-pass deltas, hot test_A
after R3 = postH; optional second churn then R4):
- P0 PXP-B0: pol 6, mode 0, w=1, c2w=0 (benign; nothing exiled)
- P1 PXP-M2: pol 6, mode 1, w=21, c2w=0 (collapse + reheat)
- P2 PXP-M2C2: pol 6, mode 1, w=21, c2w=10 (reheat, then partial
  rechurn, then reheat again)
- P3 PXP-OVF: pol 6, mode 2, w=51, c2w=0 (overflow recursion)

Promo row layout (128 bytes): 0 pre, 4 post, 8 bacc, 12 raw,
16 cf, 20 ev, 24 drop, 28 exile, 32 cdrop,
36 postR1, 40 rec1, 44 cc1, 48 prm1,
52 postR2, 56 rec2, 60 cc2, 64 prm2,
68 postR3, 72 rec3, 76 cc3, 80 prm3,
84 postH, 88 recT, 92 ccT, 96 prmT,
100 postR4, 104 rec4, 108 cc4, 112 prm4,
116 postH2, 120 cfT, 124 evT.
Anchor rows at R offsets 0, 56, 112, 168, 224 (H2's 14-field
layout). Promo rows at 512, 640, 768, 896.

## Frozen derivations

### P1 (PXP-M2)
Churn phase is identical to H2 EXH2-M2 (promotion cannot fire
before the first recovery read): cf=60, ev=28, exile=28 into cold
(20 A entries: 10 owner-15 +1-keys and 10 owner-7 +2-keys in cold
slots 0..19 in eviction order, then 8 churn-olds), pool = 32 churn
entries, post=0 (hot), rawA=15, bacc=20, drop=0.

R1 (75 reads): 15 primary hot hits. Owner-1 loop: 20 cold hits
(counts 0->1, no promotion yet). Owner-2 loop: +1/+2 reads are the
2nd cold hit per A entry (count 1->2 -> promote, 20 promotions);
+3 reads hot. Owner-4 loop (i=1..5): g hot; a2/b2 now HOT
(promoted). Owner-8 loop: all HOT. Hence postR1=35, rec1=40
(exact: 20 first-hits + 20 second-hits; 3rd/4th hits are hot),
prm1=20 (exact: each of the 20 A entries promoted exactly once;
promoted entries take max stamps so are never re-victims in R1),
cc1<575 (relational: 40 cold hits vs H2's frozen 60-hit 575;
positional derivation gives 420 = 2x210, recorded as
non-binding). exile rises 28->48 (20 re-exiled pool victims;
every promotion found a full pool).

R2: all 20 A entries hot -> 75 hot reads -> postR2=35, rec2=0,
cc2=0, prm2=0 (exact). R3 identical. postH=35 (exact: 15 primary
+ 20 pool via hot path only). Totals: recT=40, ccT=cc1<575<1725,
prmT=20, exile=48, ev=28, cdrop=0 (cold occupancy pinned at 28:
each promotion frees one slot and fills one).

The frozen no-promo 3-pass total 1725 = 3 x 575: H2's frozen K8
single-pass ccost; no-promo reads mutate no tier state, so passes
are identical. Derived from frozen values, frozen here.

### P2 (PXP-M2C2)
Prefix identical to P1 through postH=35. Second churn
teach_churn_multi(1,10): keys 3998/3999 already in primary with
different vals -> 20 conflicts, 20 relocations, pool full ->
20 evictions (12 never-re-read churn1 leftovers with oldest
stamps, then 8 A entries with oldest R3 stamps = i=1..4's
+1/+2). cfT=80, evT=48, exile=68, cold occupancy 48.

R4: the 8 re-exiled A entries: owner-1 loop 8 cold hits
(count 0->1); owner-2 loop a/b 8 cold hits (count 1->2 ->
promote, 8 promotions); all else hot. postR4=35, rec4=16
(exact), prm4=8 (exact), cc4<575. Promotion victims: 8 churn2
entries (their stamps predate R4's re-stamps of i=5..10's A
entries), re-exiled. exile=76, prmT=28, cdrop=0 (max occupancy
48). postH2=35 (exact: pool = 12 A (i=5..10) + 12 churn2 + 8
re-promoted (i=1..4) = 20 A -> 15+20 hot).

### P0 (PXP-B0)
Nothing exiled; recovery passes all hot. Identical 14 base
columns to H2 EXH2-B0; prmT=0; per-pass rec/cc/prm all 0;
postH=35; recT=0; ccT=0.

### P3 (PXP-OVF)
Identical to H2 EXH2-OVF per pass: cold FIFO already destroyed
the benign entries, so zero cold hits -> zero counts -> zero
promotions across all three passes. postR1=postR2=postR3=0,
recT=0, ccT=9600 (=3x3200, H2's frozen amended single-pass
value), postH=0, prmT=0, cdrop=74, exile=138, ev=138, cf=170,
drop=0. Promotion cannot resurrect what cold FIFO destroyed:
the recursion result stands.

## Kill bars (frozen)

- K1 ANCHOR-NOPROMO: all five pm=0 anchor rows bit-for-bit equal
  H2's frozen 14-column rows (B0 @1008, A32 @1120, M2 @1176,
  OVF @1400, CON-M2 @840). Any drift = substrate changed = FAIL.
- K2 PROMO-BENIGN (P0): base 14 columns = H2 B0; prmT=0;
  rec1=rec2=rec3=0; cc1=cc2=cc3=0; prm1=prm2=prm3=0; postH=35.
  (Promotion machinery must be inert with nothing exiled.)
- K3 PROMO-AMORTIZE (P1): postR1=postR2=postR3=35;
  rec1=40, rec2=0, rec3=0; cc1<575, cc2=0, cc3=0; ccT<1725;
  prm1=20, prm2=0, prm3=0, prmT=20; postH=35; exile=48; ev=28;
  drop=0; cdrop=0.
  Discrimination: no-promotion gives rec1=60/cc1=575/ccT=1725;
  T=1 (promote-on-first-hit) gives rec1=20; copy-not-move gives
  rec1=60; destroy-not-exile on demotion gives exile=28.
- K4 PROMO-REHEAT (P2): P1-prefix fields (postR1=35, rec1=40,
  prm1=20, postH=35); postR4=35; rec4=16; cc4<575; prm4=8;
  postH2=35; prmT=28; exile=76; evT=48; cfT=80; drop=0; cdrop=0.
- K5 PROMO-NORESURRECT (P3): prmT=0; recT=0; ccT=9600;
  postR1=postR2=postR3=0; postH=0; cdrop=74; exile=138; ev=138;
  cf=170.
- K6 PROMO-LEDGER: in P0..P3, exile == ev + drop + prmT;
  cdrop==0 except P3 (74). (K11 analog with the promotion term.)
- K7 DETERMINISM: 3/3 runs byte-identical (external sha256).
  VOID-grade, as in H2.

Verdict rule: PASS requires K1..K7 all PASS. Any bar may not be
weakened or reinterpreted after results (H2's erratum process is
the only allowed correction path: dated, transparent, derivation
errors only, never mechanism changes to force a pass).

## Toolchain and audit notes (frozen)

- safebin mandatory: PATH=$HOME/safebin; `which python3` /
  `which python` return nothing; znc pinned 2026.07.0-dev,
  cmp-verified byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 before this
  commit.
- Pure Zag for all scientific computation. No forbidden
  executable; no PROCESS-FAIL condition.
- New code audit: no `while.*!(` negated conjunctions; if-nesting
  at most 3 (cold_lookup hit-block flattened with hoisted flags);
  u8-backed cells with put32/ig only; byte side-table access via
  direct u8 index (the approved pattern class); output via one
  preallocated buffer + single _zag_raw_syscall; single approved
  `as *u8` in z_alloc (unchanged from H2).
- && short-circuit lesson (H2 K10 erratum): all test reads that
  must execute are let-bound (as in H2's test_A_recov); the
  owner-1 loop's inline && is unchanged from H2 and both reads
  succeed in every pass here, so no short-circuit fires.
- Commits local only, never pushed, explicit pathspecs, no reset.
  This prereg is committed alone before implementation.
