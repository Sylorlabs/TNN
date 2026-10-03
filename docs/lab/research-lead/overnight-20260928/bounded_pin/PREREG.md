# PREREG: BOUNDED-PIN-LIFETIME comparison

Frozen 2026-10-03. This preregistration strictly precedes implementation.
This prereg commit contains ONLY PREREG.md and NAMECHECK.md. No kill bar
below may be weakened or reinterpreted after results are seen. VOID is
terminal: it is corrected only by fresh preregistration plus a fresh run,
never by salvage or amend-and-promote.

Worker: BOUNDED-PIN-LIFETIME worker (non-ledger task). Lane:
`docs/lab/research-lead/overnight-20260928/bounded_pin/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation; shell only for
znc invocation, binary execution, git ops, sha256sum, cmp, and file
movement. Pinned compiler via safebin `znc` (byte-identical to
src/tools/toolchain/znc_linux_x86_64_abed8aa1, 2026.07.0-dev).

## Objective

MULTI-OWNER-CHURN (VERDICT=PASS 8/8, 2026-10-03) measured pinning under
the multi-owner churn adversary: ret=100 at both doses, zero evictions,
but the drop leak grows with the dose (drop 28 in M2, 48 in M3, of 32
slots). PINNING-RECLAMATION (VERDICT=PASS 7/7) compared reclamation
regimes under the single-owner adversary: LRU reclamation restored
capacity but collapsed exactly to FIFO (ret 100/54/0), while
owner-consent reclamation kept ret=100 with drop=0. Its report
caveated consent: the mask aligned with the churner's owner, and a
multi-owner adversary would test whether the mechanism generalizes.
This lane holds the multi-owner churn adversary fixed (M2/M3 exactly
as in MULTI-OWNER-CHURN) and compares bounded pin lifetime against
unbounded pinning and explicit unpin:

- Policy 3, PINR: unbounded pinning, no reclamation (exact replica of
  MULTI-OWNER-CHURN policy 2). Baseline anchor for this lane.
- Policy 4, PINTTL-10: pinning with bounded lifetime N=10.
- Policy 5, PINTTL-50: pinning with bounded lifetime N=50.
- Policy 6, PINTTL-100: pinning with bounded lifetime N=100.
- Policy 7, PINUNPIN: pinning with explicit owner-scoped unpin.

The experimental questions: does bounded lifetime restore capacity
without losing robustness? What is the optimal N? Does explicit unpin
generalize beyond the single-owner aligned case?

## Substrate (frozen; changes vs MULTI-OWNER-CHURN enumerated)

Single file bounded_pin.zag, self-contained, built directly on
multiowner_churn.zag with these frozen differences:

- Policies 0-2 removed; policies 3 (PINR), 4/5/6 (PINTTL with N from
  the header), 7 (PINUNPIN) added. The parent FIFO/PART numbers are not
  rerun; they are frozen reference values.
- Header layout: parent offsets unchanged (0 bumpA unused, 4 conflicts,
  8 evictions, 12 table_full_errors, 16 pool_size (=32), 20 policy,
  24 bumpB unused, 28 drop) plus 32 pin_ttl_N (10/50/100 per condition,
  read by policies 4/5/6) and 36 clock (monotonic pin-creation tick,
  incremented on every pool placement).
- Pool base 2112, 32 slots x 16 bytes (key, val, owners, used),
  unchanged. New side table at base 2624: 32 x 4 bytes, pin-created
  tick per pool slot. Workspace 4096 still bounds everything
  (2624+128=2752).
- Conflict path, teach protocol (teach_A multi, teach_B cond=2 FULL),
  multi-owner churn routine (teach_churn_multi, modes 1 and 2, w=21
  per key, interleaved per round), read path (owner-scoped), test
  functions, and R layout are byte-identical in logic to the parent
  lane. One frozen addition to the churn routine: a per-round unpin
  call, active only under policy 7 (see below).

## Pin semantics (frozen)

One operation = one pool placement (one pin-creation tick). Every pool
placement, whether a fill or a reclaim, stamps side_table[slot] with
the current clock and then increments the clock. Benign placements
therefore occupy ticks 0..19 and the clock stands at 20 when churn
begins; churn relocation r (1-indexed) decides at clock 19+r.

- PINR (policy 3): code path is the parent PIN path unchanged: first
  free slot scan; drop++ and destroy-in-place fallback when the pool
  is full. The side table is stamped but never consulted, so behavior
  is bit-identical to the parent by construction; K2 verifies it.
- PINTTL (policies 4/5/6): when a relocation finds the pool full, scan
  slots s=0..31 for the first used slot with (clock - created) >= N;
  evict it (evict++), reclaim its slot, and place the new entry with a
  fresh stamp. If no slot satisfies the age bound, drop++ and fall
  back to destroy-in-place, exactly as in PINR.
- PINUNPIN (policy 7): unpin(key, owner_mask) marks every used pool
  slot with slot.key == key and (slot.owner & owner_mask) != 0 as
  unpinned by setting its created tick to -1. When a relocation finds
  the pool full, scan s=0..31 for the first used slot with created < 0;
  evict it (evict++), reclaim its slot, and place the new entry pinned
  with a fresh stamp. If no unpinned slot exists, drop++ and fall back
  to destroy-in-place. An owner can only unpin entries whose owner
  bitmask intersects its own: unpin is owner-scoped.

## Unpin protocol (frozen)

Under policy 7 only, after each churn round the B-owner issues
unpin(3999, 16): it releases its own key's stale pool entries. Owners
4 and 8 (the A-family churners) issue no unpins. This is the
deliberate multi-owner generalization test: the unpin signal covers
exactly one of the two (M2) or three (M3) churners, so the lane
measures whether one owner's unpins survive a commons shared with
non-consenting churners. The all-churners-unpin variant is explicitly
not run here; it would re-derive the aligned consent outcome and is
recorded as a follow-up.

## Protocol (frozen)

Per condition, on a freshly zeroed workspace with pool_size=32 and the
policy set (pin_ttl_N set for policies 4/5/6): 1. teach A family
(multi). 2. pre-test (expect 35). 3. teach B benign FULL (20
conflicts). 4. churn: M2 (mode 1, w=21 per key, 40 relocations) or M3
(mode 2, w=21 per key, 60 relocations); under policy 7 each round ends
with unpin(3999, 16). 5. post-test; retention = 100 * post / pre.
6. record conflicts, evictions, drop, B accuracy (20 B reads), rawA
(key-level owner-scoped survival over A's 35 distinct keys).

Conditions (10): PINR-M2 (policy 3, M2), PINR-M3 (policy 3, M3),
TTL10-M2 (policy 4, M2), TTL10-M3 (policy 4, M3), TTL50-M2 (policy 5,
M2), TTL50-M3 (policy 5, M3), TTL100-M2 (policy 6, M2), TTL100-M3
(policy 6, M3), UNPIN-M2 (policy 7, M2), UNPIN-M3 (policy 7, M3).

## Predicted values (frozen; these ARE the kill-bar targets)

| cond     | pol | pre | post | ret | cf | ev | drop | bacc | rawA |
|----------|-----|-----|------|-----|----|----|------|------|------|
| PINR-M2  | 3   | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| PINR-M3  | 3   | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| TTL10-M2 | 4   | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| TTL10-M3 | 4   | 35  | 0    | 0   | 80 | 48 | 0    | 20   | 15   |
| TTL50-M2 | 5   | 35  | 20   | 57  | 60 | 10 | 18   | 20   | 25   |
| TTL50-M3 | 5   | 35  | 0    | 0   | 80 | 30 | 18   | 20   | 15   |
| TTL100-M2| 6   | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| TTL100-M3| 6   | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| UNPIN-M2 | 7   | 35  | 35   | 100 | 60 | 11 | 17   | 20   | 35   |
| UNPIN-M3 | 7   | 35  | 35   | 100 | 80 | 5  | 43   | 20   | 35   |

Derivation notes (frozen with the prereg).

PINR (policy 3): bit-for-bit replica of the parent PIN row on the
modified substrate (side table present but never consulted):
M2 drop=28, M3 drop=48, ev=0, ret=100, rawA=35.

PINTTL-10 (policy 4): benign pins are created at ticks 0..19 and the
churn decides at clocks 20..59 (M2) / 20..79 (M3). With N=10 every
benign pin is expired before the pool fills (the 12 free slots fill at
relocs 1..12), so from reloc 13 the first-expired scan evicts in
placement order, oldest first: relocs 13..32 evict benign slots 0..19,
and the remaining relocs evict churn history. No pool entry is ever
re-touched during churn, so expiry order equals placement order
equals the parent FIFO bump order. The observable footprint is
exactly the frozen FIFO-M2/FIFO-M3 row: ret=[0,0], ev=[28,48],
drop=[0,0], cf=[60,80], rawA=[15,15]. This is the same degeneracy
mechanism as the LRU to FIFO collapse in PINNING-RECLAMATION, now in
the time domain: a pure age signal cannot separate dead churn history
from live benign entries when age order is placement order.

PINTTL-50 (policy 5): a pin expires when created <= clock-50. M2:
relocs 13..30 decide at clocks 32..49 with no entry aged 50 yet, so 18
drops; relocs 31..40 (clocks 50..59) each evict the next benign slot
(slots 0..9, created 0..9), ev=10. Benign slots 10..19 survive: these
are B's writes for i=6..10 (both hops), so post=20 (5 owner-1 pairs +
5 owner-2 triples + 5 owner-8 singles, guards fail), ret=57,
rawA=25 (5+5 owner-1 keys, 10 hop-3 keys, 5 guards). M3: relocs 13..30
drop (18), relocs 31..50 evict all 20 benign slots (ev=20), relocs
51..60 evict churn fill slots 20..29 (ev=30 total), drop stays 18,
ret=0, rawA=15.

PINTTL-100 (policy 6): the latest decision clock is 79 (M3 reloc 60),
so no pin ever reaches age 100 during the run. Behaviorally identical
to unbounded pinning: the TTL100 rows equal the PINR rows exactly,
ret=[100,100], ev=[0,0], drop=[28,48].

PINUNPIN (policy 7): unpinned slots are a shared commons consumed by
every churn relocation, while only owner 16 replenishes them (one new
unpinned 3999 entry per round). M2: rounds 1..6 fill slots 20..31
(3998 history pinned at even slots, 3999 history unpinned at odd
slots); rounds 7..11 each consume 2 unpinned slots (one 3998 reloc and
one 3999 reloc, both evicting 3999 history), net -1 unpinned per
round; round 12 consumes the last unpinned slot for the 3998 reloc
and drops the 3999 reloc; rounds 13..20 drop both relocs. Totals:
12 fills + 11 evictions (all of 3999 history) + 17 drops = 40,
ev=11, drop=17. M3: rounds 1..4 fill slots 20..31; round 5 consumes 3
unpinned slots (ev=3); round 6 consumes 2 more (ev=5) then drops the
3999 reloc; rounds 7..20 drop all 42 relocs. Totals: 12 fills +
5 evictions + 43 drops = 60, ev=5, drop=43. In both doses every
eviction and every drop falls on churn history: benign slots 0..19
are never unpinned and the scan always finds an unpinned churn slot
before reaching them while any exists, so ret=100, rawA=35.

Structural note (frozen): under this protocol the protected benign
entries are always strictly older than any churn entry (placed at
ticks 0..19, never re-touched), so pin age order is placement order
and any expiry bound that reclaims churn history necessarily expires
benign history first. No N can therefore achieve ret=100 with
drop=0: the N landscape is a strict Pareto frontier between
retention and reclamation, and the "optimal N" is a tradeoff choice,
not a dominant point. The UNPIN arm is predicted to sit off that
frontier (ret=100 with partial reclamation), which is what K6 vs K4
discriminates.

B accuracy stays 20/20 in every condition: churn keys 3997/3998/3999
are distinct from every benign key, and a conflict relocation only
ever moves the churn key's own previous value, so B's 20 benign
primary entries are never disturbed. Conflicts are 20 benign + churn
relocations = 60 (M2) / 80 (M3) in every policy.

## Frozen kill bars

- K1 BASELINE: pre_ok == 35 and bacc == 20 in all 10 conditions. Else
  VOID; no verdict on the policies is drawn.
- K2 PINR-REPRO: PINR-M2 and PINR-M3 reproduce the frozen
  MULTI-OWNER-CHURN PIN rows: ret == [100,100], evict == [0,0],
  drop == [28,48], conflicts == [60,80], post == [35,35],
  rawA == [35,35]. The no-reclamation replica must match the parent
  bit-for-bit on the modified substrate.
- K3 TTL10-FIFO-EQUIV: TTL10-M2 and TTL10-M3 reproduce the frozen
  FIFO-M2/FIFO-M3 footprint exactly: ret == [0,0], evict == [28,48],
  drop == [0,0], conflicts == [60,80], rawA == [15,15]. Bounded
  lifetime with N below the benign placement horizon degenerates to
  FIFO exactly: it restores capacity (drop 0) but pays the full
  robustness price.
- K4 TTL50-PARTIAL: TTL50-M2: post == 20, ret == 57, evict == 10,
  drop == 18, rawA == 25. TTL50-M3: post == 0, ret == 0, evict == 30,
  drop == 18, rawA == 15. The interior N reclaims partially and loses
  partially: at M2 ten benign victims survive, at M3 none do.
- K5 TTL100-NORECLAIM-EQUIV: TTL100-M2 and TTL100-M3 equal the PINR
  rows exactly: ret == [100,100], evict == [0,0], drop == [28,48].
  N beyond the run horizon is behaviorally unbounded pinning.
- K6 UNPIN-PARTIAL: UNPIN-M2: ret == 100, evict == 11, drop == 17,
  rawA == 35. UNPIN-M3: ret == 100, evict == 5, drop == 43,
  rawA == 35. Explicit owner-scoped unpin keeps full robustness (no
  benign entry is ever unpinned or evicted) but restores capacity only
  partially: the unpinned commons is consumed by the non-consenting
  churners, so the leak persists at 17/43 vs 28/48 with no reclamation.
- K7 ADV-FIXED: conflicts == 60 in all five M2 conditions and
  conflicts == 80 in all five M3 conditions. The churn adversary's
  footprint must be policy-invariant; only the eviction outcome may
  differ.
- K8 DETERMINISM: 3/3 runs byte-identical (sha256 equal). Else VOID.

Verdict: PASS iff K1..K8 all hold. Any kill-bar miss names the bar and
yields FAIL. K1 or K8 failure yields VOID. Thresholds are frozen; they
are not moved after results. The parent questions are answered as
preregistered: bounded lifetime does not restore capacity without
losing robustness (K3/K4/K5 trace the strict Pareto frontier, and the
structural note gives the reason: age order is placement order under
this protocol); the optimal N is a tradeoff choice along that
frontier, with N=50 the measured interior point; explicit unpin keeps
ret=100 but its capacity restoration is partial and dose-sensitive
under multi-owner churn (K6).

Discrimination design: K2 anchors the no-reclaim baseline on the new
substrate. K3 vs K2 shows short lifetime kills the leak but pays the
full robustness price, in the sharp exact-FIFO form. K4 vs K3/K5 makes
N=50 the interior point that separates the degenerate regime from the
unbounded regime on both retention and reclamation. K5 vs K2 shows a
beyond-horizon N is behaviorally unbounded, pinning down the
frontier's upper end. K6 vs K2/K4 separates the unpin mechanism from
the lifetime frontier: it alone keeps ret=100 while reclaiming, but
its drop numbers (17/43) show the commons-consumption limit that the
aligned single-owner consent result did not face. K7 bars the
"weaker adversary under reclamation" confound.

## What this does NOT test

- The unpin protocol covers only owner 16. The variant where every
  churn owner unpins its own history is not run; it is expected to
  re-derive the aligned consent outcome and belongs to a follow-up
  prereg if the K6 partial-restoration result makes it interesting.
- Bounded lifetime is tested with benign entries placed strictly
  before churn and never re-touched. A protocol that re-pins benign
  entries during churn (benign re-reads refreshing pins) would break
  the age-order degeneracy and could rescue short N; not tested here.
- "Optimal N" is answered as a measured tradeoff along a frozen
  frontier, not as a canonized constant. Per the no-patch-treadmill
  rule, this lane canonizes no reclamation policy and no N value.
- The churn adversary is a mechanism stressor on the reclamation
  rule, not a sealed world and not a claim about realistic learner
  behavior. Owner-scoped reads carry over the parent caveat unchanged.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first. Implementation
(bounded_pin.zag), build, runs, and REPORT.md only after.
