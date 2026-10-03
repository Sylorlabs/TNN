# REPORT: RANK-PATTERN (K2 pattern-sensitivity + T_rank=1 variant)

Date: 2026-10-03. Worker: RANK-PATTERN (non-ledger task; claim
minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_pattern/.

## Verdict

**FAIL (4/8)** under the frozen prereg (K1..K7 in-binary, K8
external: 3/3 runs byte-identical,
sha256 `bcf493aa13e560b3f25c297c882ee480fd5fd8497ab4982f1aad69948727c05e`).

K1 PASS, K2 FAIL, K3 FAIL, K4 FAIL, K5 FAIL, K6 PASS, K7 PASS,
K8 PASS. The failures are all informative scientific negatives,
not mechanical errors: the simulator validates exactly on all
five base worlds (simcc==ccT4, simpay==rkT4, event sequences
identical), which isolates K2's failure to the first-order
formula itself; T_rank=1 loses decisively on all five worlds;
the prospective simulator predicts the win/lose sign correctly
on both unseen patterns but misses the prereg's strict
magnitude bar.

## What was built

Additive on RANK-LAZY's rank_lazy.zag (no redesign):
- Cold event trace (diagnostic; read-only on M): per world, a TR
  buffer records (etype,key,slot,aux). etype 1=cold hit (pre-move
  slot), 2=cold install (fresh or overflow; aux=exile-seq),
  3=promote (slot logged), 4=passmark (R1..R4 id), 5=cold miss
  (charges 64). Hooks in cold_lookup, exile_victim,
  promote_slot, run_promo. Capacity 1536 records; overflow flag
  voids the predictor.
- thresh_rerank_t(M,s,t): rk=5 uses t=2 (carried); rk=6 uses
  t=1 (frozen T_rank=1: fires on the first cold hit of each
  residency, below the promotion threshold T=2).
- In-binary simulators (operate on TR and R only, never touch M):
  Sim A replays the rk4 trace exactly (installs/promotes at
  recorded slots; swaps re-applied on every 8th hit) with a
  per-hit assert that the sim slot equals the recorded pre-move
  slot, plus per-swap attribution (pay - s*xh + s*yh). Sim B
  (prospective) replays the rk0 trace's events with recomputed
  install slots (sim first-free; sim min-seq on overflow using
  logged exile-seq) and the swap schedule applied.
- 19 rows x 144 bytes: M2C2/V1/V2/V3/V4 x rk0/rk4 (rows 0-9),
  M2C2/V1..V4 x rk6 (rows 10-14), V5 (mode=1,w=30) x rk0/rk4
  (rows 15-16), V6 (mode=3,w=40) x rk0/rk4 (rows 17-18).
  V5/V6 predictions printed prospectively from the FIFO trace
  before the rk4 row runs.

Implementation corrections C1-C2 (instrumentation, not bar
changes; the prereg's scientific bars are untouched):
- C1: etype 5 (cold miss) added. The prereg specified etypes
  1-4, but cold misses charge 64 slots each and V1/V2/V5/V6
  have them (V1: 24 misses = 1536 of ccT4=2351). Without miss
  logging the sim cannot validate. The trace spec was
  incomplete; the correction was required for K2 to be
  meaningful.
- C2: records are 4xi32 (not 3xi32) to carry exile-seq for Sim
  B's overflow handling. The prereg's K2/K3 scientific content
  is unaffected.

## Measured table (per world, NET = ccT + rkT)

| world | NET0 (FIFO) | NET4 (lazy) | delta | NET6 (T_rank=1) |
|-------|-------------|-------------|-------|-----------------|
| M2C2  | 1132        | 1097        | -35   | 1189            |
| V1    | 2388        | 2357        | -31   | 2432            |
| V2    | 1100        | 1089        | -11   | 1157            |
| V3    | 1036        | 1045        | +9    | 1091            |
| V4    | 408         | 410         | +2    | 439             |
| V5    | 1244        | 1191        | -53   | -               |
| V6    | 2310        | 2277        | -33   | -               |

## Kill-bar summary

- K1 SUBSTRATE-ANCHOR: PASS. Row 0 bit-for-bit equals the frozen
  RANK-LAZY values (35 fields checked). Trace hooks are
  read-only on M.
- K2 PREDICTOR-EXACT: FAIL. The simulator validates exactly on
  all five base worlds: event sequences identical (eseq=1),
  simcc==ccT4 (1091, 2351, 1083, 1039, 408), simpay==rkT4
  (6,6,6,6,2), per-hit layout asserts all pass. But the
  first-order per-swap formula does not predict the measured
  delta: M2C2 pred=6 vs meas=-35; V1 pred=6 vs meas=-31;
  V2 pred=-14 vs meas=-11; V3 pred=6 vs meas=+9; V4 pred=9
  vs meas=+2. The logging is proven correct, so the failure
  falsifies H1's first-order formula: it is incomplete.
- K3 PREDICT-NEW: FAIL on magnitude, PASS on sign. Sim B
  (prospective, FIFO trace only) predicts V5 predB=-75 vs
  meas=-53 (d5=22) and V6 predB=-51 vs meas=-33 (d6=18);
  both signs correct (-1), both magnitudes outside the frozen
  |diff|<=2 bar. Sim B is exact on the no-overflow world
  (M2C2: simcc=1091=ccT4); the gap appears on overflow worlds.
- K4 TRANK1-HEADLINE: FAIL. NET6=1189 > NET4=1097 on M2C2.
  T_rank=1 does not beat the schedule.
- K5 TRANK1-ROBUST: FAIL, 0/5. NET6 > NET0 on all five worlds
  (deltas +57, +44, +57, +55, +31). T_rank=1 loses everywhere.
- K6 O1-MAINTENANCE: PASS. rkT6=55 <= recT6=56,
  rkmT6 <= recT6, rkT6=55 < 553. (rkT4=6 carried.)
- K7 INVARIANCE+LEDGER: PASS. Outcome offsets identical across
  rk within each world (12 pairs); exile == ev+drop+promote on
  all 19 rows (cdrop=23/5/3/22 on V1/V2/V5/V6, reported
  unconstrained per RANK-LAZY's K6 finding).
- K8 DETERMINISM: PASS. 3/3 byte-identical,
  sha256 `bcf493aa13e560b3f25c297c882ee480fd5fd8497ab4982f1aad69948727c05e`.

## Mechanism-level findings

1. **What reverses the win in V3/V4 (per-swap attribution).**
   V3 (mode=3, no owner-16): all 6 swaps fire with xh=0 and
   yh=0. The 8th-hit schedule systematically fronts entries
   that are never re-hit while resident, and displaces entries
   that are never re-hit either. Each swap is pure +1 cost
   (first-order +6); the measured +9 includes a +3
   second-order term. The schedule fires on entries at the end
   of their cold residency.
   V4 (mode=0, single-owner, lightest churn): only 2 swaps fire.
   The first (s=7, x=1042, y=1011) displaces y=1011, which IS
   re-hit once (yh=1), incurring a +7 displacement penalty
   (contrib=8). With so few swaps, one bad displacement
   dominates. The pattern difference: V3's churn produces a
   cold-hit sequence whose 8th hits land on dead entries; V4's
   light churn leaves a live entry at slot 0 when the swap
   fires.

2. **The headline wins are second-order, not first-order.**
   This is the largest surprise. In M2C2 and V1 (deltas -35,
   -31), ALL swaps have xh=0 and yh=0: first-order predicts +6
   (pure cost), but measured is -35/-31. The win comes
   ENTIRELY from second-order layout divergence (-41, -37):
   swaps change which slots get freed on promote and hence
   which slots later installs use, shifting the positions of
   subsequently installed keys. V2's win (-11) is the only one
   with a first-order component: one swap (k=5, s=20, x=1102)
   has xh=1, contrib=-19. RANK-LAZY's "fronts entries that stay
   resident" story is wrong for M2C2/V1; the mechanism is
   layout perturbation, not fronting.

3. **Principled predictor: full simulation, not the formula.**
   H1's first-order formula (pay - s*xh + s*yh) is falsified as
   an exact predictor by K2. H2's procedure (simulate the swap
   schedule on the FIFO trace) is the correct predictor: Sim B
   gets the win/lose sign right on both unseen patterns (V5,
   V6) and is exact on no-overflow worlds. The magnitude gap
   on overflow worlds (d5=22, d6=18) marks where the model
   needs the second-order term. Prediction rule: run FIFO
   once, simulate the every-8th-hit swap schedule with
   recomputed install slots, read the sign.

4. **T_rank=1 is a decisive negative.** Fronting on every first
   cold hit (rkT6=55 of 56 hits on M2C2) churns the layout
   constantly: ccT barely moves (1134 vs 1132) while rkT=55
   is pure overhead. "Fronting entries that stay resident" is
   not sufficient; the schedule must be INFREQUENT. The
   periodic schedule wins (when it wins) via rare, not
   constant, perturbation. This kills the follow-up's
   hypothesis in the informative direction.

5. **Cold misses matter.** V1's ccT4=2351 includes 24 cold
   misses (1536 points). Any scan-cost model that counts only
   hits is wrong on heavy-churn worlds. (Correction C1.)

## Toolchain and hygiene

- Safebin mandatory: PATH=$HOME/safebin for every build/run;
  `command -v python3` / `command -v python` verified empty
  before the prereg commit; znc byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1. No python
  invoked in this lane; no PROCESS-FAIL condition triggered.
- grep audit: no `while.*!(` negated conjunctions, no
  _zag_print, no `as *i32` slice construction; if-nesting at
  most 3; single approved `as *u8` in z_alloc (carried over).
- Commits local only, never pushed, explicit pathspecs, no
  reset. Prereg committed alone first (80dc69ee4);
  implementation and artifacts committed after the verdict.
  No errata on the bars; implementation corrections C1-C2
  documented above.

## What this does NOT test (honest accounting)

- A closed-form second-order term for the install-slot
  divergence; sealed post-freeze worlds; whether Sim B's
  overflow gap closes with a corrected min-seq model; other
  policies, pm values, or promotion thresholds; whether a
  sparser-than-every-8th schedule wins bigger.

## Artifacts

- `rank_pattern.zag`: implementation (pure Zag; RANK-LAZY
  substrate + cold event trace + thresh_rerank_t + rk=6 +
  Sim A / Sim B + 19-row main).
- `rank_pattern_bin`: built binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical runs
  (sha256 `bcf493aa13e560b3f25c297c882ee480fd5fd8497ab4982f1aad69948727c05e`).
- `err1.txt`, `err2.txt`, `err3.txt`: empty stderr logs;
  `err_build.txt`: benign znc warnings (zagd unavailable,
  two E0101 style warnings).
- `PREREG.md` (frozen 2026-10-03, committed alone as
  80dc69ee4), `NAMECHECK.md`, `REPORT.md`.
