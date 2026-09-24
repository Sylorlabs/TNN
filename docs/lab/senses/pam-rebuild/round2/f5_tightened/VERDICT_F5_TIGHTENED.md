# VERDICT — F5 counter-corroboration trap, tightened-window fork

Date: 2026-09-24. Arm: F5 round-2 tighten crew (Crew 2, PAM round-2 swarm).
Prereg: `docs/lab/senses/pam-rebuild/round2/f5_tightened/PREREG_F5_TIGHTENED.md`
(prereg commit `7f10d5ed0a0b1636246c141a2dcf760ebfe1295a`, committed alone
before any code, 2026-09-24).

## Measured result

| Bar / metric | Rule | Measured | Outcome |
|-----|------|----------|---------|
| (a) Delay bar | ≤ 25% of the 300 delayed > 50 trials (primary model) | **0/300 = 0%** | PASS |
| (b) Far-control bar | 0/60 far controls blocked | **0/60** | PASS |
| (c) Distribution | delay histogram + sensitivities reported | reported below | — |
| Over-block on the 300 | reported | **0/300 BLOCKED** | — |
| Backtest false-block retention | reported (frozen trap: 8/9) | **0/9** | — |
| Backtest true-block cost | reported (frozen trap: 0/34) | **0/34** | — |

**Verdict: SURVIVE on the frozen bars — but the preregistered function
clause (§7) fires: NO-GO for the F5 live-gate build.**

## Detail (tightened predicate, pure Zag, 3 byte-identical runs per binary)

- Windows derived mechanically from the frozen exemplar bank (conf span 17,
  measure span 29): |Δconf| ≤ 9, |Δmeasure| ≤ 15 (ceil of half-span per
  axis). No threshold tuning.
- Battery binary `f5_tight` built from `f5_tight.zag` (byte-identical to the
  frozen `f5_rt300.zag` except the two window constants and the SANITY
  line; diff committed as evidence) + byte-identical copy of
  `R33_NATIVE_IO_V1.zag` (SHA `e6379ddb...`).
- 360 fixture trials processed (`fixtures_ledger.txt`, SHA
  `0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0`,
  re-verified before every run — the identical red-team battery): 300 NEAR
  + 60 FAR, all truth-correct, all DISP=ACCEPT_INSTALL.
- Bank = the 6 frozen exemplars (`exemplars.tsv`, SHA matches the
  backtest's `13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`).
- NEAR: **0/300 BLOCKED** — reproduces the preregistered hand-computed
  sanity count exactly (tightened measure union [2603, 2662]; no grid
  measure in 2200, 2700, 3200, … lands inside). Zero CORRUPT lines
  (judgment == truth asserted on every line).
- FAR: **0/60 BLOCKED**.
- Delay-length distribution (primary model: FIFO queue, 1 deliberate
  re-inspection/trial, 3 per blocked percept → delay_k = 3k), over the 300
  NEAR: `0:300 | 1–3:0 | 4–10:0 | 11–50:0 | 51–100:0 | 101–300:0 | 301+:0`.
- Sensitivities: S1 (1 re-inspection / 5 trials) → 0/300 delayed > 50;
  S2 (unbounded parallel confirmation) → 0/300.
- Retention replay (`f5_tight_replay`, byte-identical to the frozen
  `f5_pred.zag` except the two constants; same parser, same 43 candidates):
  backtest evidence ledger `v2/redteam/evidence/ledger_d_withhold.txt`
  (SHA `63ea591d8cbb9d8b3e1cd088364e96d8fdfa19d435e337dfac0ad17a0326c2b1`,
  read-only — the 8 TMB-5 false accepts are all detected FALSE but
  **ALLOWED** under the tightened windows; the COL-4 false accept stays
  correctly ALLOWED by family scope): **false blocked 0/9, true blocked
  0/34**.

## Determinism

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Three battery runs, stdout SHA-256:
  `170f53b3e4720b9e698fa8bb5c30f19a9444f56084a86057622e82b5d4392268`
  (run1.out = run2.out = run3.out, byte-identical). Zero RNG.
- Three replay runs, stdout SHA-256:
  `1d6bee687b899230f8cbc871f8f54857ce099a69ecc11f88414c97e768c3ca1c`
  (replay1.out = replay2.out = replay3.out, byte-identical). Zero RNG.

## Reading the result honestly

The two bars PASS — but vacuously. The tightened trap blocks literally
nothing on the battery (0/300) and retains none of the backtest's false
accepts (0/9, was 8/9). This is the preregistered tension from §3 playing
out exactly as stated: the 8 false accepts the frozen trap caught live
**outside the exemplar cluster's scale** (nearest 245 measure units from
the cluster edge, 8.4× the tightened measure radius). The frozen windows
caught them only by being 8–10× wider than the cluster. Tightening to the
cluster's actual scale removes the over-block (110/300 → 0/300) by deleting
the trap's catch power (8/9 → 0/9) — the two were the same phenomenon, not
two separable dials.

There is no honest window between "wide enough to catch the known false
accepts" and "narrow enough not to eat correct percepts," because the false
accepts and the near-exemplar correct percepts occupy the same
conf/measure neighborhood outside the cluster. A window that reaches the 8
false accepts (|Δmeas| ≥ 245 from the cluster) necessarily re-admits the
36.7% over-block region the red-team killed.

## Go / no-go for the F5 live-gate build

**NO-GO, per the preregistered function clause (§7).** The bars pass, but
the trap no longer performs its backtest-demonstrated function — there is
nothing left to build the gate on. Honest paths forward (separate preregs,
no window-tuning retries under this one): the correctness-aware gate fork
(H-PAM-2, a cheap independent correctness check before the block, which
could keep the wide windows' catch power while sparing truth-correct
percepts), or the full-mechanism fork (H-PAM-3, built fast confirmation
machinery re-running this battery) — both are the swarm's remaining live
options for F5.

## Caveats (frozen in the prereg, not post-hoc)

- `measure` is the task-specific raw quantity (spectral-centroid-like), NOT
  the classification margin mrgF — substitution carried exactly as the
  backtest and red-team. A true-margin replay remains the documented
  upgrade path.
- The confirmation machinery is still unbuilt; the delay numbers rest on
  the preregistered queue-model assumption (§6 of the prereg), reported
  with S1/S2 sensitivities.
- The 300-grid measures window occupancy over the anchored region; no
  real-world over-block frequency claim is made.
