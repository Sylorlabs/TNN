# PREREG: PINNING-RECLAMATION comparison

Frozen 2026-10-03. This preregistration strictly precedes implementation.
This prereg commit contains ONLY PREREG.md and NAMECHECK.md. No kill bar
below may be weakened or reinterpreted after results are seen. VOID is
terminal: it is corrected only by fresh preregistration plus a fresh run,
never by salvage or amend-and-promote.

Worker: PINNING-RECLAMATION worker (non-ledger task). Lane:
`docs/lab/research-lead/overnight-20260928/pinning_reclamation/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation; shell only for
znc invocation, binary execution, git ops, sha256sum, cmp, and file
movement. Pinned compiler via safebin `znc` (byte-identical to
src/tools/toolchain/znc_linux_x86_64_abed8aa1, 2026.07.0-dev).

## Objective

EVICTION-POLICY (VERDICT=PASS, 2026-10-03) measured the price of pinning:
ret=[100,100,100] at churn doses r in {0,20,32} with ev=[0,0,0], but
drop=[0,8,20]: permanent pool occupancy, a slow memory leak with no
tested reclamation. Its report names this lane as the natural follow-up.
This lane holds the churn adversary fixed and compares three pinning
reclamation regimes on the same frozen substrate:

- Policy 3, PIN-NORECLAIM: pinning without reclamation (exact replica
  of EVICTION-POLICY policy 2). Baseline anchor for this lane.
- Policy 4, PIN-LRU: pinning with LRU reclamation. Every pool entry
  carries a monotonic last-touch stamp (written on relocation placement
  and on pool read hits). When a relocation finds the pool full, the
  entry with the minimum last-touch is evicted (evict++), its slot
  reclaimed, and the drop counter is retained but expected never to fire.
- Policy 5, PIN-CONSENT: pinning with owner-consent reclamation. When a
  relocation finds the pool full, the first used slot whose owner
  bitmask intersects the consent mask (header 32, frozen to 16: B
  consents to release its own entries) is evicted (evict++) and
  reclaimed. Slots outside the consent mask stay pinned forever.
  drop++ only if no consenting slot exists (not expected under the
  frozen protocol).

The experimental question: does reclamation restore capacity without
losing robustness? What does each reclamation regime pay?

## Substrate (frozen; changes vs EVICTION-POLICY enumerated)

Single file pinning_reclamation.zag, self-contained, built directly on
eviction_policy.zag with these frozen differences:

- Policies 0-2 removed; policies 3 (PIN-NORECLAIM), 4 (PIN-LRU),
  5 (PIN-CONSENT) added. The parent FIFO/PART numbers are not rerun;
  they are frozen reference values.
- Header layout: parent offsets unchanged (0 bumpA, 4 conflicts,
  8 evictions, 12 table_full_errors, 16 pool_size (=32), 20 policy,
  24 bumpB, 28 drop) plus 32 consent_mask (=16) and 36 clock
  (monotonic last-touch stamp, incremented on every pool placement and
  every pool read hit).
- Pool base 2112, 32 slots x 16 bytes (key, val, owners, used), unchanged.
  New side table at base 2624: 32 x 4 bytes, last-touch per pool slot.
  Workspace 4096 still bounds everything (2624+128=2752).
- Conflict path, teach protocol, read path (owner-scoped), test
  functions, and R layout are byte-identical in logic to the parent
  lane: conflicts++ on every same-key different-value write, policy
  relocation, new value installs in the primary table. Read path is
  extended only by the last-touch stamp on pool hits.

## Learned structures and writers (frozen; unchanged)

Owner bits: A_BASE=1, A_EXT=2, A_SPEC=4, A_TRUNC=8, B=16. A family
taught exactly as in the parent (35 distinct keys, 35 queries).
Benign writer: teach_B cond=2 (FULL), 20 conflicting writes on
ka(i,hop) = 1000+i*10+hop, i=1..10, hop=1..2, val=777000+i*10+hop.
Churn adversary (held fixed across all policies): after the benign
writer, write key 3999 (fresh B-owned key) `w` times with values
900001+w. First write allocates; each subsequent write conflicts and
relocates a B-owned (owner 16) victim. Churn doses are relocation
counts r = w - 1, with w in {1, 21, 33}, i.e. r in {0, 20, 32}.

## Protocol (frozen)

Per condition, on a freshly zeroed workspace with pool_size=32 and the
policy set: 1. teach A family (multi). 2. pre-test (expect 35).
3. teach B benign FULL (20 conflicts). 4. churn adversary with w
writes. 5. post-test; retention = 100 * post_ok / pre_ok. 6. record
conflicts, evictions, drop, B accuracy (20 B reads), rawA (key-level
owner-scoped survival over A's 35 distinct keys).

Conditions (9): PINR-B0 (policy 3, w=1), PINR-A20 (policy 3, w=21),
PINR-A32 (policy 3, w=33), PINLRU-B0 (policy 4, w=1),
PINLRU-A20 (policy 4, w=21), PINLRU-A32 (policy 4, w=33),
PINCON-B0 (policy 5, w=1), PINCON-A20 (policy 5, w=21),
PINCON-A32 (policy 5, w=33).

## Predicted values (frozen; these ARE the kill-bar targets)

| cond       | pol | w  | pre | post | ret | cf | ev | drop | bacc | rawA |
|------------|-----|----|-----|------|-----|----|----|------|------|------|
| PINR-B0    | 3   | 1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| PINR-A20   | 3   | 21 | 35  | 35   | 100 | 40 | 0  | 8    | 20   | 35   |
| PINR-A32   | 3   | 33 | 35  | 35   | 100 | 52 | 0  | 20   | 20   | 35   |
| PINLRU-B0  | 4   | 1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| PINLRU-A20 | 4   | 21 | 35  | 19   | 54  | 40 | 8  | 0    | 20   | 27   |
| PINLRU-A32 | 4   | 33 | 35  | 0    | 0   | 52 | 20 | 0    | 20   | 15   |
| PINCON-B0  | 5   | 1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| PINCON-A20 | 5   | 21 | 35  | 35   | 100 | 40 | 8  | 0    | 20   | 35   |
| PINCON-A32 | 5   | 33 | 35  | 35   | 100 | 52 | 20 | 0    | 20   | 35   |

Derivation notes (frozen with the prereg).

PINR (policy 3): code path is the parent PIN path unchanged: 20 benign
victims scan into slots 0..19 (pinned); churn fills the 12 free slots
then drops. ev=0 always; drop=[0,8,20]; ret=100, rawA=35 at every dose.
Bit-for-bit replica of the parent PIN row, re-measured to anchor the
modified substrate (new header fields, side table, read-stamp logic).

PINLRU (policy 4): benign placements stamp t=1..20 in B-teaching order
(slots 0..19). Churn placements stamp t=21..32 (slots 20..31). No pool
reads occur during the churn phase: pre-test reads happened before any
pool placement existed (pool fills only during B teaching and churn),
teach_B and teach_churn are write-only, and post-test reads happen
after the last relocation. Therefore last-touch order == placement
order == the parent FIFO bump order. r=20: 8 reclamations evict the
minimum-timestamp entries (slots 0..7: the 8 oldest benign victims,
i=1..4 both hops, exactly the parent FIFO-A20 eviction set), ev=8,
drop=0, post=19, ret=54, rawA=27. r=32: 20 reclamations evict slots
0..19 (all 20 benign victims, exactly the parent FIFO-A32 eviction
set), ev=20, drop=0, post=0, ret=0, rawA=15. The read-stamp code is
present (genuine LRU semantics) but inert under this protocol, which is
why the exact FIFO equivalence is predicted rather than merely
ret < 100. The finding under test: under an adversary that churns
never-re-read keys, recency cannot separate dead churn history from
live benign entries, so LRU reclamation degenerates to FIFO.

PINCON (policy 5): benign victims carry owner bitmasks {15,7,11,3}
(never bit 16, since B never co-wrote those keys before the benign
writer); churn victims carry owner exactly 16. Consent mask 16 admits
only churn entries for reclamation. r=20: 12 fills, 8 reclamations
each evicting the oldest owner-16 slot (slot 20 repeatedly), ev=8,
drop=0, benign untouched, ret=100, rawA=35. r=32: 12 fills, 20
reclamations, ev=20, drop=0, ret=100, rawA=35.

B accuracy stays 20/20 in every condition: B's 20 benign primary
entries are never relocated away from owner 16 in any policy (a
conflict relocates the old value and installs B's new value in the
primary; reclamations and the PINR fallback only touch key 3999, which
the B test does not read).

## Frozen kill bars

- K1 BASELINE: pre_ok == 35 and bacc == 20 in all 9 conditions. Else
  BUILD-FAIL; no verdict on the policies is drawn.
- K2 NORECLAIM-REPRO: PINR conditions ret == [100,100,100],
  conflicts == [20,40,52], evict == [0,0,0], drop == [0,8,20]. The
  no-reclamation replica must reproduce the frozen parent PIN row
  exactly on the modified substrate.
- K3 LRU-CAPACITY: PINLRU conditions drop == [0,0,0]. LRU reclamation
  eliminates the permanent-occupancy leak: no relocation ever falls
  back to destroy-in-place.
- K4 LRU-FIFO-EQUIV: PINLRU conditions ret == [100,54,0] and
  evict == [0,8,20] (exact parent FIFO dose-response, including the
  dose-20 and dose-32 eviction counts). LRU reclamation restores
  capacity but pays the full robustness price: under this adversary
  it degenerates to FIFO.
- K5 CONSENT-HOLDS: PINCON conditions ret == [100,100,100],
  evict == [0,8,20], drop == [0,0,0]. Owner-consent reclamation
  restores capacity with zero retention loss: churn history is
  reclaimed, benign entries are never touched.
- K6 ADVERSARY-FIXED: conflicts per dose identical across all three
  policies: dose r=0 -> 20 in PINR-B0, PINLRU-B0, PINCON-B0; r=20 -> 40
  in the three A20 conditions; r=32 -> 52 in the three A32 conditions.
  The churn adversary's footprint must be policy-invariant; only the
  eviction outcome may differ.
- K7 DETERMINISM: 3/3 runs byte-identical (sha256 equal). Else VOID.

Verdict: PASS iff K1..K7 all hold. Any kill-bar miss names the bar and
yields FAIL. K1 or K7 failure yields VOID. Thresholds are frozen; they
are not moved after results. rawA is reported as a diagnostic and is
not kill-barred.

Discrimination design: K2 anchors the no-reclaim baseline on the new
substrate (must match the parent PIN bit-for-bit). K3 vs K2 shows LRU
kills the leak; K4 vs K2 shows LRU pays the full robustness price, and
the exact FIFO equivalence is the sharp form of the tradeoff (a
recency policy cannot price dead history it never sees re-read).
K5 vs K3 separates consent from LRU: both reclaim, but consent keeps
ret=100 while LRU falls to 54/0. K6 bars the "weaker adversary under
reclamation" confound.

## What this does NOT test

- The consent mask (16) aligns with the churn adversary's owner, just
  as the parent PART boundary did. A multi-owner churn adversary would
  test whether consent generalizes beyond the aligned case; that probe
  needs its own prereg.
- LRU is tested with the churn interleaved after benign teaching and
  with no pool reads during churn. A protocol that re-reads benign
  entries during the churn phase would differentiate recency from
  arrival; not tested here.
- The churn adversary is a mechanism stressor on the reclamation rule,
  not a sealed world and not a claim about realistic learner behavior.
  Owner-scoped reads carry over the parent caveat unchanged.
- Per the no-patch-treadmill rule, this lane does NOT canonize a
  reclamation policy. Each regime carries a measured price; choosing
  between them belongs to fresh preregistered work.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first. Implementation
(pinning_reclamation.zag), build, runs, and REPORT.md only after.
