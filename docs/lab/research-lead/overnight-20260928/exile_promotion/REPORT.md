# REPORT: EXILE-PROMOTION (promotion / reheat dynamics)

Date: 2026-10-03. Worker: EXILE-PROMOTION (non-ledger task; claim
minting paused). Lane:
`docs/lab/research-lead/overnight-20260928/exile_promotion/`.

## Verdict

**PASS 7/7** under the amended prereg (K1..K6 in-binary, K7
external: 3/3 runs byte-identical,
sha256 `791bce75b3552a0ae9702aac48dfddc18899b313dfc4f48224b7e8f87ff762af`).

Honest accounting of the amendment: the initial frozen run produced
VERDICT=FAIL on two worker-side errors, both corrected through the
transparent erratum process (no mechanism or implementation change
to the promotion machinery):
- E1: K4's frozen cc4 bound `<575` was a derivation error. The
  worker forgot P2's R4 reheats entries the second churn pushed to
  high cold slots (40..47). Corrected: cc4=712 exactly
  (2 x (41+...+48)); the run produced 712.
- E2: K6's in-binary assertions read cold_drop at the wrong R
  field offset (+48 instead of +32). Test-code bug; bar intent
  unchanged; measured values already satisfied the corrected bar.

Toolchain incident (E3): during post-run inspection the worker
accidentally invoked `python3 -c "print('skip')"` in the lane
shell. It performed no scientific computation, touched no files,
and ran after all runs completed — but per the worker toolchain
guard the invocation is self-disclosed here and the initial wave
is automatically PROCESS-FAIL; its measurements stay exploratory.
This verdict rests SOLELY on the clean re-freeze: errata E1+E2
applied, binary rebuilt from the amended assertions, three fresh
runs with `command -v python3` verified empty under the safebin
PATH before the build and before the runs. No python was invoked
during the re-freeze.

## What was built

The promotion extension on the RECLAMATION-H2 substrate (hot
mechanism, cold tier, exile, FIFO cold overflow all carried over
unchanged; K1 proves pm=0 reproduces H2 bit-for-bit). Additive
machinery only:
- Recovery-count side table (base 4032, 64 x u8), reset on every
  exile install.
- Promotion trigger: per-entry recovery count reaching frozen
  threshold T=2 on the recovery path (pm-gated).
- promote_slot: MOVE cold->pool, never copy. First free pool slot
  if available; else the minimum last-touch pool slot is evicted
  and re-exiled (priced demotion, never destruction). promote++
  per move (header 60).
- The hot read path is untouched and never consults cold.

## Measured table

Anchors (pm=0): bit-for-bit H2's frozen rows (EXH2-B0/A32/M2/OVF,
EXCON-M2); see K1.

Promotion conditions (pm=1):

| cond | pre | post | cf | ev | drop | exile | cdrop | R1 (postR/rec/cc/prm) | R2 | R3 | postH | recT | ccT | prmT | R4 (postR/rec/cc/prm) | postH2 |
|------|-----|------|----|----|------|-------|-------|------------------------|----|----|-------|------|-----|------|------------------------|--------|
| PXP-B0 | 35 | 35 | 20 | 0 | 0 | 0 | 0 | 35/0/0/0 | 35/0/0/0 | 35/0/0/0 | 35 | 0 | 0 | 0 | - | - |
| PXP-M2 | 35 | 0 | 60 | 28 | 0 | 48 | 0 | 35/40/420/20 | 35/0/0/0 | 35/0/0/0 | 35 | 40 | 420 | 20 | - | - |
| PXP-M2C2 | 35 | 0 | 80 | 48 | 0 | 76 | 0 | 35/40/420/20 | 35/0/0/0 | 35/0/0/0 | 35 | 56 | 1132 | 28 | 35/16/712/8 | 35 |
| PXP-OVF | 35 | 0 | 170 | 138 | 0 | 138 | 74 | 0/0/3200/0 | 0/0/3200/0 | 0/0/3200/0 | 0 | 0 | 9600 | 0 | - | - |

Note cc1=420 exactly matches the prereg's non-binding positional
derivation (2 x 210), confirming the cold-scan cost model under
promotion.

## Answers to the design questions

**What triggers promotion?** Per-entry recovery-count threshold
T=2 (frozen). The exact rec1=40 is the discriminating evidence:
each A entry's 1st and 2nd hits stay cold, its 3rd+ hits go hot
— the threshold visibly separates one-off demand from repeated
demand mid-pass. Counterfactuals the bars kill: no-promotion
gives rec1=60/cc1=575; promote-on-first-hit (T=1) would give
rec1=20; copy-not-move would give rec1=60 (later reads still
cold). Recency was rejected for this lane (needs cold
timestamps); it stays a named follow-up.

**What gets demoted to make room?** Yes — promotion causes hot
eviction when the pool is full. Victim = minimum last-touch pool
slot (the LRU rule, consistent with policy 6's own reclamation).
In P1, 20 promotions evict 20 pool entries; all 20 are re-exiled
(exile 28 -> 48), never destroyed. With a free pool slot,
promotion installs without eviction (not exercised here; pool is
full in every promotion condition).

**Does promotion break the "priced, delayed destruction"
accounting?** No. K6: exile == ev + drop + promote holds exactly
in all four promo conditions (48==28+0+20; 76==48+0+28;
0==0+0+0; 138==138+0+0). cold_drop remains the ONLY destruction
counter. Promotion moves entries (exclusive tier occupancy: each
entry lives in exactly one tier at a time), so no duplication
leak is constructible.

**Real hierarchy or slower leak?** The evidence says real
two-tier hierarchy, on four independent legs:
1. Amortization: 3-pass cold-scan cost 420 vs the frozen
   no-promo 3-pass total 1725 (4.1x reduction; K3).
2. Hot restoration: after the passes, hot-path-only test_A
   scores postH=35 — the full working set reheats; the recovery
   path becomes unnecessary (R2/R3: rec=0, cc=0).
3. Bounded cold: cold occupancy pinned at 28 across all passes
   (each promotion frees one slot and fills one); nothing grows.
4. Reheat survives rechurn: P2's second churn re-exiles 8 hot
   entries; R4 re-promotes exactly those 8 (prmT=28, rec4=16),
   postH2=35.
And the recursion result stands: P3 shows promotion cannot
resurrect what cold FIFO destroyed (prmT=0, postR=0, cdrop=74).
Promotion is a hierarchy discipline for the recoverable case,
not a fix for destruction.

Honest finding from E1: reheat cost is POSITIONAL. R4's 8
re-exiled entries sat at cold slots 40..47, so reheating them
cost cc4=712 — above a no-promo single pass (575). The hierarchy
still wins on totals (1132 < 2300 = no-promo 4-pass), but the
positional price is exactly the argument for H2's named
follow-up: LRU/importance ranking *within* cold.

## Kill-bar summary

- K1 ANCHOR-NOPROMO: five pm=0 rows bit-for-bit H2's frozen
  rows. PASS (substrate unchanged).
- K2 PROMO-BENIGN: P0 identical to H2 B0; prmT=0; all per-pass
  ledgers empty; postH=35. PASS (machinery inert, nothing exiled).
- K3 PROMO-AMORTIZE: postR1/2/3=35; rec1=40, rec2=rec3=0;
  cc1=420<575, cc2=cc3=0; ccT=420<1725; prmT=20; postH=35;
  exile=48; cdrop=0. PASS.
- K4 PROMO-REHEAT: P1-prefix fields match; R4 postR4=35,
  rec4=16, cc4=712 (amended), prm4=8; postH2=35; prmT=28;
  exile=76; evT=48; cfT=80; cdrop=0. PASS (amended).
- K5 PROMO-NORESURRECT: prmT=0, recT=0, ccT=9600, postR=0,
  postH=0, cdrop=74, exile=138. PASS.
- K6 PROMO-LEDGER: exile == ev+drop+promote in P0..P3;
  cdrop==0 except P3 (74). PASS (amended offsets).
- K7 DETERMINISM: 3/3 byte-identical (clean re-freeze). PASS.

## Toolchain and hygiene

- Safebin mandatory: PATH=$HOME/safebin for every build/run;
  `which python3` / `command -v python3` return nothing under it
  (verified before the re-freeze build and runs); znc pinned
  2026.07.0-dev, cmp-verified byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 before the
  prereg commit.
- grep audit on the implementation: no `while.*!(` negated
  conjunctions, no _zag_print, no `as *i32` slice construction;
  single approved `as *u8` in z_alloc (unchanged from H2);
  if-nesting at most 3 (cold_lookup hit block uses hoisted flags).
- E3: self-disclosed accidental python3 invocation post-run;
  initial wave PROCESS-FAIL per the guard; verdict rests solely
  on the clean re-freeze (no python invoked; per-step
  verification). Recorded in PREREG erratum E3 and NAMECHECK.
- Commits local only, never pushed, explicit pathspecs, no
  reset. Prereg committed alone first (81a707a0e); erratum
  committed separately (48233870f) before the re-freeze.

## What this does NOT test (honest accounting)

- Recency-based promotion triggering (frozen as count
  threshold T=2; only T=2 tested, not T=1/3+ sensitivity).
- Any ranking within cold (FIFO only); the cc4 positional
  finding motivates LRU/importance ranking as the next lane.
- Combining exile+promotion with H1's importance signal or H3's
  learner-issued unpin.
- Sustained alternating churn/recovery thrash (one rechurn
  episode only, P2).
- Cold-tier compression/dedup (the honest memory-price
  reduction, still open from H2).
- Sealed post-freeze worlds; the adversary is the same
  mechanism stressor family as the arc (doses, multi-owner
  modes).

## Artifacts

- `exile_promo.zag`: implementation (pure Zag; H2 substrate +
  additive promotion machinery).
- `exile_promo_bin`: built binary (clean re-freeze build).
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical runs
  (sha256 `791bce75b3552a0ae9702aac48dfddc18899b313dfc4f48224b7e8f87ff762af`).
- `err1.txt`, `err2.txt`, `err3.txt`: empty stderr logs.
- `PREREG.md` (with dated errata E1/E2/E3), `NAMECHECK.md`,
  `REPORT.md`.
