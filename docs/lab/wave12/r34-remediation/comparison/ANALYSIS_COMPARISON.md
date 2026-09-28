# ANALYSIS — tainted (LCG) vs clean (deterministic) long-horizon battery

**Workstream:** COMPARISON (r34 remediation). **Prereg:**
`PREREG_COMPARISON.md` (frozen + committed as `a01a5e838935` BEFORE this
analysis; no amendments). **Date:** 2026-09-20. **Owner:** Micah.
Read-only: no new training run, the quarantined LCG arm was never
re-executed.

## A1. Explore-sequence reconstruction (prereg §4, F1 validation)

The tainted logs record no explore counts. The reconstruction replays ONLY
the explore-decision subsequence — the pure arithmetic
`v=(rng*997+7919) mod 1000003`, explore iff `v mod 5 == 0`, one draw per
training `choose` with `explore_enabled=1` — verbatim from the quarantined
core. No learning is simulated; no learning claims are produced. Pure Zag,
no RNG (standing law). Program: `lcg_reconstruct.zag`; output:
`lcg_reconstruct_output.txt` (two runs byte-identical).

**F1 VALIDATION — PASS.** Seed 12001, 480 draws, 48/block reproduces the
LH-P3 fixed arm's documented per-block explore counts **exactly**:
`11,7,8,8,7,12,10,7,9,5` (sum 84). The draw-consumption model (training
chooses only; eval `explore_enabled=0` chooses consume no draws via `&&`
short-circuit) is confirmed against logged evidence. All timing claims
below rest on this validation.

Reconstructed tainted explore schedules (seed, draws → per-block counts):

| Leg | Seed | Draws | Tainted explores (per block) | Total |
|---|---|---|---|---|
| LH-1 | 11001 | 480 | 13,9,9,9,6,7,7,11,9,8 | **88** |
| LH-2 | 22002 | 1920 | ~9.7/block, all 40 blocks (14,13,13,13,12,13,12,7,13,10,…) | **389** |
| LH-3 | 33003 | 4800 | ~9.9/block, all 100 blocks | **989** |
| LH-5 (each lineage) | 5555 | 480 | 10,9,10,13,10,12,10,7,9,8 | **98** |
| LH-4 (tainted-only) | 47111 | 288 | per-visit: 3,10,3,3,6,6,5,2,4,3,5,3 | **53** (18.4%) |
| LH-7 (tainted-only) | 55223 | 480 | ~0–3/cycle | **92** (19.2%) |

Clean-arm explores (from rerun evidence traces / VERDICT):

| Leg | Clean explores | Timing |
|---|---|---|
| LH-1R | **16** | ALL in block 0 (uncertainty path); budget refilled to 8 every phase afterwards, unspent (`bud=8`, `expl=16` flat blocks 1–9) |
| LH-2R | **16** | all in block 0; 0 in blocks 1–39 |
| LH-3R | **11** | all in block 0; 0 in blocks 1–99 |
| LH-5R 0% / 10% / 25% / 50% | **16 / 38 / 61 / 76** | disappointment path engages under corruption, scaling with noise |

**M1 finding — discovery is equivalent; the surplus is all confident-regime
flips.** Block-0 (initial margin separation) explore volumes match:
tainted 13 (LH-1) / 14 (LH-2) / 13 (LH-3) vs clean 16 / 16 / 11. The
deterministic uncertainty rule (`margin<=200`) does all the discovery work
the LCG did. Every explore beyond block 0 in the tainted arm — 75 (LH-1),
375 (LH-2), 978 (LH-3) — fired in settled regimes with clear margins and no
negative streak, where the clean rule fires zero. Ratios: 5.5× / 24× / 90×
more explores, zero endpoint difference (M0).

## A2. Guardrail M0 — headline parity (checked first, per prereg)

No clean leg failed a bar the tainted leg passed (rerun VERDICT headline):

- LH-1: 480 updates; all 20 block-probes 16/16 both arms; return-A 15/16,
  `active=0`, zero weight updates both; controls (disabled-update B 12/24,
  scrambled-reward A 0/16) identical; determinism byte-identical both.
- LH-2: 1920 updates; all 80 block-probes 16/16 both; return-A 15/16 both;
  saturation without rigidity both.
- LH-3: 4800 updates; drift schedule **byte-identical**
  `1,1,2,0,0,2,1,2,2,1` both; all 60 mode-0/1 blocks 16/16 both; all 40
  mode-2 blocks `ea=15/16, eb=16/16` both (the switch-cost probe artifact
  reproduced exactly, 40 `LH_FINDING`s); mirror context assignment
  (B-first decile claims ctx0 for B) both; return `ra=16`, `active=1` both.
- Switch cadence on clean legs is **identical**: LH-1 19/19, LH-2 79/79
  (training), LH-3 439/439. The LCG's 88/389/989 state-blind flips altered
  **zero** switch decisions and **zero** eval outcomes in the absence of
  corruption.

## A3. M2 — switch counts per corruption level (LH-5)

`LH5_FINAL` switch counts, tainted vs clean:

| Corruption | Tainted sw | Clean sw | Δ (clean−tainted) | Clean explores |
|---|---|---|---|---|
| 0% | 19 | 19 | 0 | 16 |
| 10% | 91 | 90 | −1 | 38 |
| 25% | 149 | 154 | +5 | 61 |
| 50% | 181 | 198 | +17 | 76 |

Supplementary seeds (learner seed 5555, tainted explores still 98/lineage):

| Seed | Tainted sw | Clean sw | Clean explores |
|---|---|---|---|
| (10%, 7777) | 84 | 91 | 34 |
| (10%, 4242) | 98 | 103 | 77 |
| (25%, 7777) | 137 | 159 | 72 |

Direction clean≥tainted in 5/6 comparisons, but magnitude does not track
the explore delta (Δexpl 60→Δsw −1 at primary 10%; Δexpl 22→Δsw +17 at
primary 50%). Systematic direction, chaos-modulated magnitude — see
mechanism 3 below.

## A4. M3 — saturation onset

| Leg | Tainted pin block (correct cells → +30000) | Clean pin block |
|---|---|---|
| LH-2 | **16** (28400→30000 within block) | **13** (29200→30000) |
| LH-3 | **16** | **14** |

≈300 net accepts pin a correct cell. Clean accumulates ~48/48 training
accepts per block on correct cells; tainted diverts ~1/5 to wrong cells
(~38/48), reaching the pin threshold 2–3 blocks later. The delay is a pure
cost of the surplus flips (mechanism 1).

## A5. M4 — endpoint scores

LH-1 endpoint (block 9): tainted `s00=18900, s11=18400` vs clean
`s00=22300, s11=22200` — max|score| **18900 vs 22300**. Wrong cells:
tainted `s01=−4800, s10=−5300` vs clean `s01=−1700, s10=−1800`.
LH-2 endpoint: correct cells +30000 both; wrong cells tainted
`−21100/−20100` vs clean `−4700/−4800`. Return gates identical
(15/16 LH-1/LH-2; 16/16 LH-3 mirror case, both arms).

## A6. M5 — knee shape (LH-5)

- **Knee location: identical.** Both arms: 0% clean (20/20 probes 16/16),
  10% already shows total 0/16 per-block collapses. The knee is between 0%
  and 10% with or without the RNG.
- **Collapse-block identity: byte-identical.** 10%: blocks **5-B, 9-A**
  both arms. 25%: blocks **3-A, 4-B, 9-A** both arms. Collapsed-probe
  counts: 0% → 0/20 both; 10% → 2/20 both; 25% → 3/20 both;
  50% → 13/20 vs 12/20.
- **50% endpoint: the sole headline delta.** Tainted `A=0/16, B=16/16`;
  clean `A=0/16, B=0/16`. Per-block 50% tables are otherwise the same
  qualitative picture (most probes collapsed both arms). **Chaos check
  (prereg H2):** the tainted arm's own supplementary seeds lose regime B
  at endpoint — (10%,7777) → `evalB=0/16`; (25%,7777) → `evalB=0/16` —
  and the clean supp seeds show the same spread (e.g. clean (10%,4242):
  6 collapsed probes, endpoint 16/16). Losing a regime at endpoint in the
  chaotic 50% envelope happens in BOTH arms depending on seed; the
  primary-seed 50% endpoint difference is seed luck, not a tainted-arm
  property. It cannot carry a HELPED claim (fails H2) and is classified
  under D2 as a chaotic-envelope delta — reported here, not smoothed over.

## A7. M6 — wrong-cell sink rate

- LH-2 block 39: tainted `s01=−21100, s10=−20100` (~−525/block) vs clean
  `s01=−4700, s10=−4800` (~−118/block). Touch census: tainted
  `n01=239, n10=229` vs clean `n01=47, n10=48`.
- LH-3 block 99: tainted `−30000/−30000` (pinned ~block 51/59) vs clean
  `−22100/−18800` (still sinking).
- **The clean sink is exactly accounted for:** each regime-change switch
  dumps one −100 into the alternate context's wrong cell (the accept
  applies to `target=alt`). LH-3R: 439 switches → ~−22000 predicted,
  observed −22100/−18800 ✓. LH-2R: 80 switches → ~−4000 + block-0
  discovery explores, observed −4700/−4800 ✓. Clean wrong cells are
  touched ONLY by discovery explores + switch episodes — zero steady-state
  exploration. The tainted surplus (~10/block) is ~190 extra wrong-cell
  taps per cell over 40 blocks (mechanism 1).

## A8. Mechanisms (each delta traced to a code path)

**Mechanism 1 — confident-regime wrong-cell tap (the RNG's tax).**
In a settled regime (`margin>>200`, correct active context), greedy picks
the correct object. The LCG flips it 1-in-5 regardless → wrong object
chosen → reward −1 → `r34v3_accept` with `pending_explore=1`: the switch
is blocked, but `learn=1` still applies **−100 to the wrong cell** and the
+100 the correct cell would have earned is lost. Per steady-state explore:
one lost correct-cell accept + one wrong-cell tap. This single mechanism
quantitatively explains M3 (2–3 block later pinning: ~38/48 vs 48/48
correct-cell accepts per block), M4 (18900 vs 22300; deeper wrong cells),
and M6 (the ~4.4× deeper sink; tainted `n01=239` vs clean `47`).
Discrimination never breaks because ordering (`s00>s01`) survives — the
tax is pure score movement, zero behavioral return (A2: identical switch
sequences and eval outcomes).

**Mechanism 2 — discovery equivalence.**
Block-0 explore volumes match across arms (13–14 vs 11–16); the
deterministic uncertainty predicate (`margin<=200`) performs all the
exploration the LCG usefully performed. Corroboration: LH-P3 C1
(quarantined comparison, mechanistically informative) — adaptive P3 with
29 explores beat fixed 1/5 with 84 explores on training positives
432/480 vs 379/480 with identical endpoints (16/16 evals, 15/16 return-A,
19 switches both). Fewer, state-driven explores dominate more,
state-blind ones.

**Mechanism 3 — incidental switch-damping under corruption (unreliable).**
Explore episodes are switch-immune: `r34v3_accept`/`r34_clean_accept`
require `pending_explore==0` for the switch trigger. Under corruption,
corrupted −1s arrive constantly; each explore episode is a trial on which
a corrupted negative CANNOT trigger a spurious switch. Tainted provides
~98 such immune episodes per lineage uniformly; clean provides 16–76 via
the disappointment path (`neg_streak>=3`), concentrated in negative
streaks. Direction clean≥tainted switches in 5/6 comparisons is consistent
with this, but the magnitude is chaos-modulated (Δexpl 60→Δsw −1 at 10%;
Δexpl 22→Δsw +17 at 50%), and the endpoint consequence sits inside the
chaotic envelope both arms exhibit (A6). This is damping of a pathology
(the uncorroborated switch trigger — LH-5's standing open item), not a
learning benefit; and per prereg F4 the function already exists honestly
in the clean rule (disappointment-path explores are equally switch-immune)
— the arms differ only in immune-episode volume, not in function.

**Mechanism 4 — the knee is RNG-independent.**
The fragility mechanism (switch rule treats every corrupted negative as a
regime-change signal; no corroboration requirement) reproduces
byte-exactly under the clean rule: identical knee, identical collapse
blocks at 10%/25%, identical 0% baseline. The RNG neither caused, moved,
nor cured the knee.
