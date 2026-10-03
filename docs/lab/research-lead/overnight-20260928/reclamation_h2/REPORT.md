# REPORT: RECLAMATION-H2 (exile, not destruction)

Date: 2026-10-03. Worker: RECLAMATION-H2 (non-ledger task; claim
minting paused). Lane:
`docs/lab/research-lead/overnight-20260928/reclamation_h2/`.

## Verdict

**PASS 13/13** under the amended prereg (K1..K12 in-binary, K13
external: 3/3 runs byte-identical,
sha256 `96c56985422dae8ddce047c28f598ea5b5ea7fca4379cb1cb848da9af3215c41`).

Honest accounting of the amendment: the original frozen K10 predicted
cold_cost=3840 for EXH2-OVF; the frozen run produced 3200 with the
other 12 K10 assertions passing. Root cause was a worker derivation
error, not a mechanism deviation: test_A_recov's loop1 reads are
inline in the if condition and znc's && short-circuits, so on a cold
miss the second read never executes (50 cold misses, not 60;
50x64=3200). Verified by lane-external instrumented debug builds:
50 cold lookups, 15 true primary hits (the 10 owner-2 hop3 keys and 5
owner-4 2000+i keys, logged by key). The PREREG carries a dated
erratum (3840 -> 3200, derivation corrected, no mechanism or
implementation change to the exile machinery; only the K10 assertion
constant was updated and the binary rebuilt). Original frozen K10 is
recorded as FAIL (derivation error); amended K10 re-frozen and PASS.
No other derivation was affected (in every other condition loop1's
first read always hits, so the short-circuit never fires).

## What was built

The exile substrate: LIVENESS-SIGNAL hot mechanism byte-identical,
plus a recoverable cold tier (base 2752, 64 slots x 20 bytes: key,
val, owner, used, exile-seq; 1280 bytes). Every hot-tier displacement
(pool eviction victims for policies 0/1/4/5/6, and drop-path primary
old values for policies 3/5) is moved to the cold tier, never
destroyed: exile == ev + drop in all 26 conditions (K11). Cold-tier
overflow uses FIFO by exile-seq (cold_drop). The hot read path never
consults the cold tier; the recovery path (mem_read_recov) falls
through to a cold scan on hot miss, counting recoveries and slots
scanned (cold_cost), with NO promotion back to pool (frozen).

Policy 0/1 branches carried verbatim from EVICTION-POLICY-COMPARE,
policy 4 verbatim from PINNING-RECLAMATION; all six baselines
reproduce their frozen rows bit-for-bit on the exile substrate
(K1..K5).

## Measured table (26 conditions; pre=35 everywhere)

| cond | post | ret | cf | ev | drop | bacc | rawA | postR | retR | exile | recover | cdrop | ccost |
|------|------|-----|----|----|------|------|------|-------|------|-------|---------|-------|-------|
| EXFIFO-B0 | 35 | 100 | 20 | 0 | 0 | 20 | 35 | 35 | 100 | 0 | 0 | 0 | 0 |
| EXFIFO-A20 | 19 | 54 | 40 | 8 | 0 | 20 | 27 | 35 | 100 | 8 | 28 | 0 | 124 |
| EXFIFO-A32 | 0 | 0 | 52 | 20 | 0 | 20 | 15 | 35 | 100 | 20 | 60 | 0 | 575 |
| EXPART-B0 | 27 | 77 | 20 | 4 | 0 | 20 | 31 | 35 | 100 | 4 | 14 | 0 | 34 |
| EXPART-A20 | 27 | 77 | 40 | 8 | 0 | 20 | 31 | 35 | 100 | 8 | 14 | 0 | 34 |
| EXPART-A32 | 27 | 77 | 52 | 20 | 0 | 20 | 31 | 35 | 100 | 20 | 14 | 0 | 34 |
| EXLRU-B0/A20/A32 | bit-for-bit = EXFIFO rows in all 14 columns (K3) |
| EXPIN-M2 | 35 | 100 | 60 | 0 | 28 | 20 | 35 | 35 | 100 | 28 | 0 | 0 | 0 |
| EXPIN-M3 | 35 | 100 | 80 | 0 | 48 | 20 | 35 | 35 | 100 | 48 | 0 | 0 | 0 |
| EXPIN-X2 | 35 | 100 | 60 | 0 | 28 | 20 | 35 | 35 | 100 | 28 | 0 | 0 | 0 |
| EXCON-B0 | 35 | 100 | 20 | 0 | 0 | 20 | 35 | 35 | 100 | 0 | 0 | 0 | 0 |
| EXCON-A20 | 35 | 100 | 40 | 8 | 0 | 20 | 35 | 35 | 100 | 8 | 0 | 0 | 0 |
| EXCON-A32 | 35 | 100 | 52 | 20 | 0 | 20 | 35 | 35 | 100 | 20 | 0 | 0 | 0 |
| EXCON-M2 | 35 | 100 | 60 | 11 | 17 | 20 | 35 | 35 | 100 | 28 | 0 | 0 | 0 |
| EXCON-M3 | 35 | 100 | 80 | 5 | 43 | 20 | 35 | 35 | 100 | 48 | 0 | 0 | 0 |
| EXCON-X2 | 35 | 100 | 60 | 0 | 28 | 20 | 35 | 35 | 100 | 28 | 0 | 0 | 0 |
| EXH2-B0 | 35 | 100 | 20 | 0 | 0 | 20 | 35 | 35 | 100 | 0 | 0 | 0 | 0 |
| EXH2-A20 | 19 | 54 | 40 | 8 | 0 | 20 | 27 | 35 | 100 | 8 | 28 | 0 | 124 |
| EXH2-A32 | 0 | 0 | 52 | 20 | 0 | 20 | 15 | 35 | 100 | 20 | 60 | 0 | 575 |
| EXH2-M2 | 0 | 0 | 60 | 28 | 0 | 20 | 15 | 35 | 100 | 28 | 60 | 0 | 575 |
| EXH2-M3 | 0 | 0 | 80 | 48 | 0 | 20 | 15 | 35 | 100 | 48 | 60 | 0 | 575 |
| EXH2-X2 | 0 | 0 | 60 | 28 | 0 | 20 | 15 | 35 | 100 | 28 | 60 | 0 | 575 |
| EXH2R-M2 | 35 | 100 | 60 | 28 | 0 | 20 | 35 | 35 | 100 | 28 | 0 | 0 | 0 |
| EXH2-OVF | 0 | 0 | 170 | 138 | 0 | 20 | 15 | 0 | 0 | 138 | 0 | 74 | 3200 |

## Answers to the design questions

**How does recovery work? What triggers it?** Recovery is
demand-driven and explicit: the hot read path (primary -> pool,
owner-scoped) is unchanged and never consults the cold tier. When a
workload uses the recovery path, a hot miss falls through to a cold
scan (key + intersecting owner); on hit the value is returned and
recover++ counts it. There is no promotion (no reheat): the cold tier
is recoverable storage, not a second cache level, so repeated reads
pay repeated cost. Trigger = a recovery-path read for a key the hot
tier no longer holds.

**What is the cost of the cold tier?** Memory: 64x20 = 1280 bytes for
64 entries (hot pool: 32x16 = 512 bytes for 32 entries); no
compression or dedup in this lane, the price is stated, not
optimized. Lookup time: O(64) scan per recovery lookup vs O(32) pool
scan, measured exactly by cold_cost (slots examined: position+1 on
hit, 64 on miss). Example bills: EXH2-M2 pays 575 slot-scans to
recover all 35 queries; EXH2R-M2 pays 0 (warm knowledge needs no
recovery); EXH2-OVF pays 3200 slot-scans and recovers nothing.

**Does this break the trilemma? Or just move the problem?** It moves
the problem one level down; it does not break the trilemma. K6+K7+K8:
the catastrophic LRU ranking still destroys hot knowledge bit-for-bit
(ret 0, ev 28/48), but recoverable retention is 100 with an exact
retrieval-cost ledger: the miss case becomes a capacity bill, not
knowledge loss. K10 (the honest-risk recursion test): with churn
sustained past the cold tier's capacity (138 exiles into 64 slots),
cold-tier FIFO destroys the 74 oldest entries including all 20 benign
ones: retR collapses to 0 exactly as hot ret did. The destruction
question recurses. Exile converts "destruction" into "priced, delayed
destruction"; with a bounded cold tier the trilemma is reframed, not
removed. A bigger cold tier only moves the overflow point; an
unbounded cold tier is just PIN's leak relocated.

## Comparison against the six baselines

All six reproduce their frozen hot rows bit-for-bit on the exile
substrate (K1..K5), so the comparison is apples-to-apples with one
added dimension (recoverability):

- FIFO / PART / PIN-LRU / PIN-LIVENESS: hot retention collapses as
  before (54/0, 77, 54/0, 0), but retR=100 everywhere the cold tier
  holds: the collapse is now recoverable at a measured scan cost
  (124/575 for FIFO/LRU, 34 for PART's 4-entry loss).
- PIN (no-reclaim): ret=100 hot; its drop-path displacements are now
  exiled rather than destroyed (exile=28/48/28, recover=0 since hot
  never misses). The leak becomes cold-tier occupancy, not loss.
- PIN-CONSENT: ret=100 hot, recover=0 (nothing ever needs recovery);
  exile=ev+drop shows the capacity price is now cold-tier occupancy
  instead of destruction.
- The discriminating contrast: under the standard doses every
  policy's miss case is recoverable (retR=100); under overflow only
  the policies that never displaced benign entries (consent, pin)
  keep retR=100, while LRU/FIFO/PART lose it exactly when the cold
  tier overflows. Exile does not change which entries a ranking
  sacrifices; it changes what "sacrifice" means.

## Kill-bar summary

- K1..K5 ANCHOR-*: all six baselines bit-for-bit (hot) + exact new
  columns. PASS.
- K6 H2-HOT-COLLAPSE: LRU hot columns bit-for-bit the frozen
  liveness rows. Exile changes nothing hot. PASS.
- K7 H2-RECOV-100: postR=35, retR=100 on all six H2 rows. PASS.
- K8 H2-LEDGER: exact (exile, recover, cold_drop, cold_cost) on all
  six H2 rows. PASS.
- K9 H2-REREAD: hot = LIVR-M2; empty recovery ledger (recover=0,
  ccost=0). PASS.
- K10 H2-RECURSION: overflow destroys cold too (cdrop=74, retR=0).
  PASS (amended; see erratum).
- K11 NO-HOT-DESTRUCTION: exile == ev+drop in all 26 conditions;
  cold_drop==0 except OVF. PASS.
- K12 ADV-FIXED: conflicts identical across policies per dose. PASS.
- K13 DETERMINISM: 3/3 byte-identical. PASS.

## Toolchain and hygiene

- Safebin mandatory: PATH=$HOME/safebin for all builds/runs;
  `which python3` / `which python` return nothing under it. Pure Zag
  for all scientific computation. No forbidden executable invoked;
  no PROCESS-FAIL condition.
- Pinned compiler znc 2026.07.0-dev, byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 (cmp before prereg
  commit).
- grep audit on implementation: no `while.*!(` negated
  conjunctions, no _zag_print, no `as *i32` slice construction;
  single `as *u8` is the approved `_zag_malloc` pattern in z_alloc;
  if-nesting at most 3.
- Commits local only, never pushed, explicit pathspecs, no reset.
  Prereg committed alone first (5ce207a82); erratum amendment
  committed separately before the report.
- Lesson for future lanes: znc's && short-circuits. Any derivation
  that counts executed reads must account for reads inline in &&
  conditions being skipped on false LHS; let-bound reads always
  execute. (This lane's K10 erratum.)

## What this does NOT test (honest accounting)

- No compression/dedup/summarization in the cold tier; the 1280-byte
  price is the measured cost of the naive form.
- No promotion/reheat on recovery; a promoting cold tier is a
  different hypothesis with its own recursion dynamics.
- Cold-tier overflow rule is FIFO-by-exile-order only; LRU or
  importance ranking within cold not tested.
- Ranking policy stays LRU; H1's importance signal and H3's
  learner-issued unpin are not combined with exile here.
- The adversary is the same mechanism stressor family as the arc
  (doses, multi-owner modes); no sealed post-freeze world.
- Owner-scoped reads retained; the label-free routing caveat carries
  over unchanged.
- No repair proposed or canonized: K10's recursion result is
  evidence about the hypothesis, not a defect to patch with a
  bigger cold tier.

## Artifacts

- `exile_h2.zag`: implementation (pure Zag).
- `exile_h2_bin`: built binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical runs
  (sha256 `96c56985422dae8ddce047c28f598ea5b5ea7fca4379cb1cb848da9af3215c41`).
- `err1.txt`, `err2.txt`, `err3.txt`: empty stderr logs.
- `PREREG.md` (with dated erratum), `NAMECHECK.md`, `REPORT.md`.
