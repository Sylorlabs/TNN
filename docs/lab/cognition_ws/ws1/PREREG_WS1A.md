# WS1-A PREREG — Verification of "deliberation cheaper than autopilot" (KB-control domain)

**Frozen:** 2026-09-24T08:10:00-07:00 (PDT). **Status:** FROZEN — never edit
after runs start; amendments go in a new file. **Agent:** WS1-A
(consciousness-bill verifier). **Coordinator:** parent orchestrator (WS1).

## Claim under test

The 2026-09-24 consciousness bill (docs/lab/consciousness_cost/BILL.md) found,
on the R27 frozen curriculum (4880 episodes): deliberate-trained KB control
cost **0.086 ms/episode** vs silent autopilot **0.312 ms/episode** — deliberation
3.6× CHEAPER per episode, with better probe accuracy (320/0/0 vs 128/128/64).
The bill also found the REVERSE on the H5 deliberation battery (batch autopilot
4.8× faster, 10× fewer ops, same 1.000). This prereg tests ONLY the
"deliberation cheaper than autopilot" direction, on a FRESH, LARGER battery
with NEW draws (no R27 fixtures reused), and maps the conditions where the
direction holds, ties, or flips.

## Battery (fresh draws, same instrumented substrates)

**Conditions** (18 cells; arms × cells × 3 runs = 162 runs):

| axis | values | meaning |
|---|---|---|
| cap (state size) | 32, 128, 512 | live-store slots (R27 used 32/128) |
| adv (ambiguity) | 0, 15, 35 | % of B-phase episodes that are adversarial (impostors + fabricated, unverified) |
| rep (repetition) | 1, 3 | repeats of the A→B→C→D cycle |

**Generator** (`src/w1a_gen.zag`): FRESH ground-truth functions (new constants,
not R27's t_op/t_param): `top(t)=1+((t*3+7*S)%5)`, `tparam(t)=((t*11+13*S)%9)`,
`tctx(t,k)=((t+2k+S)%4)`, seed S=7 fixed (one new draw; draws are fixed,
never RNG). Impostor: same id, wrong op/param, unverified. Fabricated:
ids 9000+k, unverified. Phases per cycle: A nt×8 verified true episodes
(establish); B nt×8 mixed (adv% adversarial); C nt×4 late true ids verified;
D nt×4 true verified (heal). nt = cap/2. Episodes/cell = 24·nt·rep
(min 384, max 18,432 — larger than the prior 4880 total on the big cells).

**Arms** (same instrumented substrates as the bill, additive counters only):
- **D1 DELIB-TRAINED** = kb_arm1 trained policy verbatim (suppress impostors,
  never install unverified, calibrated promote, audited MA ops) + white-box
  counters. Substrate: copied `memory_core.zag` with MA_CAP 256→512 and
  MA_AUDIT_CAP 4096→16384 (documented build notes; larger state/ledger).
- **D3 DELIB-UNTRAINED** = kb_arm3 naive policy verbatim + counters.
- **A2 AUTOPILOT** = psm.zag mode=0 logic verbatim (timer scan every 10
  episodes, raw-exposure promote, last-wins overwrite, lowest-conf eviction,
  no audit) + counters. nf=cap/2, ns=cap.

**Probe** (blind, identical for all arms): per true id (nt) — classify
correct / wrong / abstain; count spurious slots. Accuracy = correct/nt.
(Single probe point: end of curriculum; mid-probe dropped — the prior bill
already established the mid/end split; this battery is about cost.)

## Metrics

Per (cell, arm, run), all printed as tagged stdout lines:
- accuracy: correct/wrong/abstain/spurious, determinism digest
- **W (deterministic work index, PRIMARY):** W = find_steps + scan_steps +
  mutops, where find_steps = per-episode store-scan slot visits, scan_steps =
  slow/fast-tier scan slot visits (autopilot's periodic passes), mutops =
  add+kill+pin+unpin+promote+demote+setstage+consolidations+overwrites+
  evictions+suppressions. Counted once each, zero weights — honest index.
- W/ep = W / episodes.
- wall ns/ep (time_ns bracketing; SECONDARY — VM noise; pooled median of 3).
- arena bytes + ledger bytes (memory).
- determinism: digest from a second in-driver run must match (match=1).

Determinism holds: zero RNG in every source (grep gate), fixed generator,
3/3 byte-identical stdout (SHA256 per cell×arm in manifest).

## Kill / decision bars (read the verdict off these, no post-hoc edits)

- **K1 CONFIRM-gate:** median over the 18 cells of R = W(A2)/W(D1) ≥ 1.5
  (deliberate at least 1.5× cheaper on the deterministic index), AND the
  direction reproduces on the prior bill's matching regime (adv∈{15,35},
  cap∈{128,512}): R ≥ 2.0 on ≥75% of those cells.
- **K2 accuracy-gate:** no cell where D1 accuracy < A2 accuracy − 0.05.
- **K3 determinism-gate:** 3/3 byte-identical stdout on every cell×arm; grep
  `-iE 'rng|rand\('` clean on all new sources.
- **K4 mechanism-gate:** white-box counters must attribute ≥70% of the
  W-gap to a named mechanism family (periodic scans and/or overwrite churn);
  else the cost verdict is CONFIRMED-UNEXPLAINED — no mechanism may be claimed.
- **KILL:** median R ≤ 1.0 over all cells (autopilot cheaper-or-equal overall),
  OR K2 violated on ≥2 cells, OR K3 violated anywhere.
- **PARTIAL:** 1.0 < median R < 1.5, or K1's matching-regime sub-gate fails
  while the overall median passes — then the conditions map is the headline
  and the claim is marked regime-dependent.

## Predicted (not asserted) outcomes

- D1 cheaper on adversarial cells (adv≥15): A2's last-wins churn and
  every-10-episode full-tier scans burn work that D1's suppress-once policy
  never spends. Larger cap widens the gap (A2 scans scale with cap; D1's
  per-episode find is bounded and early-exits).
- A2 cheaper-or-equal on benign cells (adv=0): no impostor churn; A2's scans
  promote each true skill once and settle; D1 still pays audit appends.
- D3 (untrained) pays churn under repetition (rep=3): kill+add cycles per
  adversarial burst — the judgment-vs-structure cost split.
- Wall-clock corroborates W within VM noise; if it contradicts W on >1/3 of
  cells, flag and investigate before any verdict.

## Amendments

None yet. (New file per amendment; this file is frozen.)
