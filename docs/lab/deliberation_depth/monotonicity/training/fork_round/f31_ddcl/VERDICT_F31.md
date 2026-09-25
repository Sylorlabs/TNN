# VERDICT_F31 — F31 DDCL (Depth-Discounted Calibration Ledger), mechanism 31

Date: 2026-09-24/25 (PDT). Frozen authority: `tnn-native-lab` commit
`3a2eef44`; `fork_round/PREREG_FORKROUND.md` §3 F31 + §10; ideas file
Mechanism D / FORK 4 (`ideas/fable_forks.md`).

## Verdict: **KILLED**

Failing bars: **B2** (theater V2=260), **B3** (strict law, 30 G-violations),
**B13** (underconfidence floor, 9 cells). F31-specific falsifiers fired:
**(b)** redteam tiny-n B3 ≥ base (F31 Gviol=3 vs NEC m9=2), and **(c)**
B13 failure with over-correction signature (9 fails, 7 at positive-offset
depths). Failure mode: **FM6 (selection)** — the per-depth mean ledger
cannot subtract selection-driven G dynamics; frozen training offsets do not
transfer to deployment bias. §6 100× horizon NOT run (short bars did not
all clear, per task gate).

## What was built

- `src/train_f31.zag` — deterministic coordinate-descent base head
  (init w1..w8=0,b=0; steps ±50/±8/±1; 8 sweeps/step; fixed order) over all
  4,222 training released cells, then the online per-depth DDCL pass:
  expandable chunked `[]u8` ledger (256-entry chunks, doubling growth, LE
  accessors; per-depth FIFO 2048 as inert test constant), closed-loop
  (emitted post-offset conf appended after emission), offset =
  clamp(tdiv(G_thousandths·damp,1000),±200), damp∈[200,800] meta-adapted
  (−50 on G-sign flip, +50 after 100 stable appends), causal pre-update damp.
- Fitted: w=(472,85,0,28,320,145,350,470), b=246; offsets per depth-slot
  (d1,d2,d4,d8,d16,d32,d64) = (3, 37, 5, −1, −2, 74, 0); damp 200→650
  (40 ups, 5 downs, 5 flips over 4,222 cells; flip_rate 0.12%).
- Cap hits: offset ±200 clamp — 0 hits (max |off|=74); damp 800 ceiling —
  touched (max_observed=800); 2048-FIFO — never bound (max depth count 940);
  ledger growth 256→512→1024 exercised on depths 1–16.
- `src/policy_f31.zag` — frozen harness + M4 release skeleton, conf =
  clamp(B(s) − off[dslot], 0, 1000), gate01 forced 0, cert `f31-ddcl`.

## Determinism gates (all passed)

- Trainer build A/B byte-identical
  (sha256 `b5221c99…`); training twice → params AND logs byte-identical.
- Policy build A/B byte-identical (sha256 `e2fd94a0…`).
- 37-leg battery via `run_eval.sh f31full … 31 0`: 37/37 legs, all
  A/B run pairs byte-identical; B9 release+correct identity vs M4 =
  5240/5240 (100%).

## Kill-bar table (37 legs, run A)

| Bar | Result |
|---|---|
| B1 accuracy 1→0 | 0 — PASS |
| B2 theater | V1=0, **V2=260 — FAIL** |
| B3 strict law | **30 G-violations — FAIL** (NEC m9: 6) |
| B4 / B4b / B5 | 0.9319 / all ≥0.93 / sep 0.308 — PASS |
| B6 recall | 1.00 everywhere (2 vacuous, M4 releases none) — PASS |
| B7 abstention | 0.1475 — PASS |
| B8 amended | PASS on 7 fams; VOID on trap/redteam (tiny-n, <4 feasible slots) |
| B9 vs M4 | 5240/5240 — PASS |
| B12 (recorded) | G>0 crossings: P 6, redteam 5, D 3, trap 3 |
| B13 | **9 (F,d) with G<−0.100 — FAIL** |
| B3pi (recorded) | 2598 rising / 3467 adjacent released pairs |

F31 falsifiers: (a) oscillation — CLEAR (no flip storm; 0 eval ping-pong
families; offsets never hit cap); **(b) redteam tiny-n B3 ≥ base — KILL**
(3 ≥ 2); **(c) B13 from over-correction — KILL** (7 of 9 fails at depths
with positive offsets, i.e. the ledger subtracted where the base was
already underconfident).

## Why it died (mechanism reading)

The ledger measured a tiny training gap (G ≤ 0.115 at every depth —
the base head was already near-calibrated on training) and froze tiny
offsets. On heldout batteries the deployment gap is large (e.g. admit
d1 G=−0.162, cost d1 −0.295): the frozen offsets (3, 37, 5, …) are two
orders of magnitude too small to matter, and where positive they push
the wrong way — classic over-correction on top of base underconfidence.
Per-depth mean correction cannot touch selection-driven G-rise (B3: G
rises d1→d8 on admit/cost/revoke while the offset subtracts a constant
3). The ideas file's predicted weakness — tiny-n redteam — materialized
exactly (F31 strictly worse than NEC m9 there). This is FM6: selection
was measured as a mean and hoped away; it was not subtracted.

## §5 checkpoint

GO per frozen §5: weights ≠ init, DDCL live (7/7 depths ledgered, 6/7
nonzero offsets, 45 damp adaptations). The base-head veto diagnostics
(theater=175, v3 fail on the base head) are reported as evidence; the
§5b veto scope is F24–F27 only and does not VOID F31 (documented in
PROTOCOL.md pre-eval). The final head's theater/underconfidence were
adjudicated by B2/B13 on the battery instead — both failed.

## Artifacts

- `params/f31_params_a.zag` (= `_b.zag`, byte-identical) — canonical params
- `logs/train_a.tsv` (= `train_b.tsv`) — full training + ledger log
- `logs/eval_f31full.log` — battery run log
- `results/killbars_f31.txt` — full bar table
- `analysis/killbars_f31.py` — analyzer
- `src/train_f31.zag`, `src/policy_f31.zag`, `PROTOCOL.md`

No `[]u8` slice over 2^25 was created; no `zalloc` used; pure Zag, zero
RNG. §6 horizon not run (gated on all short bars clearing).
