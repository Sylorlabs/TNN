# H5 Results v2 — deliberation depth vs accuracy (measured)

**Supersedes** `results/RESULTS_H5.md` (Crew 5, commit `bca4caf3`), which
verified the instrument but was BLOCKED on measurement. This document
reports the full measurement taken under the coordinator-signed §12
amendment (`AMENDMENT_S12.md`, commit `bc4da5d2`): the harness adaptive
rule brought to DEPTH_DEF §6 verbatim (`harness_v2/`, commit `fbf85acf`)
and the 877 frozen items translated by the frozen `ITEM_ENCODING_SPEC.md`
v1 (`items_v2/`, commit `393f4d9`).

Frozen inputs: prereg `c317d36082d6d6f6b9828d71d96c38c95df81087`.
Binary: pinned znc `znc_linux_x86_64_abed8aa1`, SHA256
`526bccd0c1fb925fa92fcde451091e636df15a35b7daa7dbfd5e4f1c8a23032e`
(two builds byte-identical; determinism re-proved, `DETERMINISM_V2.md`).

## 1. What changed vs the blocked run

**Rule diff (the §12 fix).** The frozen harness stopped adaptive
deliberation when `rounds ≥ min`, `confidence ≥ threshold`, the leader
held for `stability_window` rounds, and the *cumulative margin gain over
the window* was `< epsilon` — a margin *drop* counted as settled, and two
extra conditions (confidence threshold, leader stability) had no basis in
§6. The v2 rule is §6 verbatim: per-round absolute confidence gains
`g_i = |c_i − c_{i−1}|` with `c_0 := c_1` (so `g_1 = 0`); stop iff
`r ≥ k = 3` and **all** of the last 3 gains are `< ε = 0.02`; hard cap at
16, recorded as `cap=1` in the VERDICT ledger detail. Confidence drops
never count as settled (absolute value). `conf_threshold` and
`stability_window` remain required config keys but are ignored by the
rule. Three hand-computed unit tests discriminate old from new
(`DETERMINISM_V2.md`): settle-at-5, drop-never-settles (the old rule
would stop at round 3 on a −90 signed drop; v2 stops at 5), cap-at-16
with `cap=1`.

**Item encoding (the input bridge).** `encoding/ITEM_ENCODING_SPEC.md` v1
(frozen before translation, commit `bc4da5d2`): mechanical,
deterministic translation of the 877 items into harness items —
hypotheses from structural fields, evidence as weighted supports/attacks
by fixed constants or fixed scalings of payload numbers, ground truths
charset-mapped (`/`→`_`, space→`_` — verified collision-free; only the 5
`KILL/SURVIVE` revoke items and 5 `P and not-Q` wason items needed it).
Fidelity gates, all PASS before measurement:

| Gate | Check | Result |
|---|---|---|
| F1 | independent full-score argmax re-derivation vs GT | 877/877 |
| F2 | independently written 10% re-implementation, byte-compare | 90/90 |
| F3 | v2 harness parse + deep-16 convergence | 877/877 |
| F4 | one-round trap baseline selects `shallow_answer` | 127/127 |

## 2. Sweep design

6 configs × 5 batteries × 2 runs = 60 cells, every cell twice
(A/B, byte-identical binaries). Configs built directly from frozen
prereg values — Crew 5's `results/proposed/` configs were not used:

| Config | Mode | Rounds | ε | k | cap |
|---|---|---|---|---|---|
| d1/d2/d4/d8 | shallow (fixed) | 1/2/4/8 | 20 | 3 | 16 |
| deep16 | deep (fixed) | 16 | 20 | 3 | 16 |
| adaptive | adaptive (§6) | ≥3, cap 16 | 20 | 3 | 16 |

Prereg gates, all PASS: parse 877/877 in all 60 cells; A/B
byte-identical results+ledgers in all 60 cells; effective config
consistency (ledger CONFIG echo: mode/rounds/ε=20/k=3/cap=16/elim=900/
refute=600 in every cell); trap depth-1 bait rate ≥90% in all 24 families
(actually 100% everywhere — F4).

## 3. Measured curves

Accuracy (fraction correct), 877 items:

| battery | n | d1 | d2 | d4 | d8 | deep16 | adaptive |
|---|---|---|---|---|---|---|---|
| admit | 248 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| revoke | 113 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| logic | 264 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| trap | 127 | 0.000 | 0.331 | 0.961 | 1.000 | 1.000 | 1.000 |
| cost | 125 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| **pooled** | 877 | 0.855 | 0.903 | 0.994 | 1.000 | 1.000 | 1.000 |

Mean rounds used (compute cost):

| battery | d1 | d2 | d4 | d8 | deep16 | adaptive |
|---|---|---|---|---|---|---|
| admit | 1.00 | 1.97 | 3.63 | 6.20 | 9.11 | 4.15 |
| revoke | 1.00 | 2.00 | 3.16 | 5.10 | 5.63 | 3.72 |
| logic | 1.00 | 2.00 | 2.06 | 2.11 | 2.12 | 2.07 |
| trap | 1.00 | 2.00 | 3.48 | 3.81 | 3.81 | 3.81 |
| cost | 1.00 | 2.00 | 4.00 | 5.48 | 5.48 | 4.84 |

Mean evidence consumed tracks rounds almost 1:1 (admit 4.12, revoke
3.32, logic 1.23, trap 3.49, cost 4.84 under adaptive).

## 4. The knee

Only the trap battery has a non-flat curve — it is the depth signal
(see §7). Marginal accuracy gains on trap: d1→d2 **+0.331** (+0.331/round),
d2→d4 **+0.630** (+0.315/round), d4→d8 **+0.039** (+0.010/round),
d8→deep16 +0.000. **The knee is at depth 4**: returns collapse by two
orders of magnitude per round past d4. Pooled (all 877): d1→d2 +0.048,
d2→d4 +0.091, d4→d8 +0.006 — same knee.

Per-family flip timing (trap): at d2, 42/127 flipped; 15 of 24 families
still take the bait. At d4, 122/127 flipped; only **C6-wason-selection**
(5 items, 6 premises each — the longest misleading runs) still takes the
bait. By d8 every family flips (127/127).

## 5. Adaptive verdict

Adaptive matches deep-16 accuracy on **all five batteries** (1.000
everywhere, 877/877) while using fewer rounds on three of them:

| battery | adaptive rounds | deep16 rounds | saved | §6 early stops |
|---|---|---|---|---|
| admit | 4.15 | 9.11 | 54% | 181/248 |
| revoke | 3.72 | 5.63 | 34% | 63/113 |
| logic | 2.07 | 2.12 | 2% | 3/264 |
| trap | 3.81 | 3.81 | 0% | 0/127 |
| cost | 4.84 | 5.48 | 12% | 40/125 |

Read carefully — the mechanism differs by battery. On
admit/revoke/cost the §6 rule fires early (284/486 items stop before
their deep-16 length) with zero accuracy loss: genuine adaptive savings.
On logic, both stop at ~2 rounds via natural termination (single small
evidence sets; nothing left to deliberate). On trap, adaptive stops at
*exactly* the deep-16 round on all 127 items (0 §6 early stops): the
corrective evidence keeps moving confidence until the evidence runs out,
and natural termination fires first. The adaptive verdict still holds
(deep accuracy, no extra rounds), but on trap the §6 rule is vacuous —
length is set by evidence exhaustion, not by settling.

**Censoring (prereg §3): cap-hit rate 0/877.** No adaptive run in any
battery reached the 16-round cap, so the adaptive measurement is
uncensored — the §6 rule settled every item before the cap. (The `cap=1`
ledger flag exists and is proven live by the U-cap unit test; it simply
never fired in the sweep.)

## 6. Traps

- Depth-1 takes the bait 127/127 (F4), ≥90% in every one of the 24
  families — the trap battery is a valid depth probe: shallow always
  wrong, deep always right.
- The flip is sharp: 0.000 → 0.331 → 0.961 → 1.000 across d1/d2/d4/d8.
- Wason selection (C6) is the hardest family: 6 misleading premises
  (the maximum; still under the 900 elim margin by design) delay the
  flip past d4.
- B1-lied-to vs B1-world-changed both flip by d4 — the harness does not
  distinguish the two worlds by accuracy here (both converge to GT);
  the distinction, if any, would be in rounds, not verdicts.

## 7. Costs

Compute cost ≈ rounds ≈ evidence consumed (one evidence item per round
plus elimination/refutation phases). Cheapest correct configuration:
adaptive on every battery (4.15/3.72/2.07/3.81/4.84 mean rounds at
1.000 accuracy). Fixed d4 reaches 0.994 pooled at (3.63/3.16/2.06/3.48/
4.00) rounds — the knee depth is also near the cost optimum. Fixed d8
buys the last 0.006 pooled accuracy (the 5 wason items) at roughly
double the trap/admit rounds.

## 8. Limitations (do not overclaim)

1. **The base batteries are convergence checks, not reasoning tests.**
   The admit/revoke/logic encodings anchor evidence weights to the
   source program's verdict (gate policy text, kill-bar definitions, and
   multi-hop logic inference are not mechanically recoverable from the
   payloads). Their flat 1.000 curves at every depth — including depth
   1 — measure that the harness converges on verdict-anchored evidence,
   not that it reasons. The spec documents this openly
   (`ITEM_ENCODING_SPEC.md` §6); the depth signal lives in the trap
   battery.
2. **The cost battery does not discriminate depth either.** All eight
   D-classes score 1.000 at every depth including d1: the D1 treadmill's
   first-round delta sign always matches the eventual winner on these
   20 items (balanced pairs), and D2–D8 items are single-sided. The
   preserved `optimal_stopping_depth` metadata could not be exercised.
   A cost battery that discriminates would need first-round-misleading
   D1 items.
3. **Harness confidence is clamped margin, not calibrated belief.**
   Confidence = clamp(leader − runner-up, 0, 1000) in thousandths (1000
   if one hypothesis survives). The §6 rule therefore settles on score
   stability, which on verdict-anchored evidence is nearly immediate.
   Whether the knee at depth 4 generalizes beyond this harness's
   score mechanics is untested.
4. **Adaptive never hit the cap here.** The no-censoring result is a
   property of this item distribution (evidence sets ≤ 9 items,
   decisive weights); longer or noisier evidence streams could still
   censor. The `cap=1` flag is proven live by unit test, not by sweep
   data.
5. **Zero RNG throughout** (pinned toolchain, byte-identical reruns);
   the determinism claim covers the harness, not the Python
   translator — the translator's fidelity is covered by F1/F2 instead.

## 9. Provenance

- Frozen prereg: `c317d36082d6d6f6b9828d71d96c38c95df81087`
- Crew 5 (instrument verified, measurement blocked): `bca4caf3`
- §12 amendment + frozen encoding spec (spec-first): `bc4da5d2`
- harness_v2 (§6 verbatim implementation): `fbf85acf`
- items_v2 + configs_v2 (translation + approved configs): `393f4d9`
- This results document: `bd386f97bcd66d8c0eeec9e393e242bcabdd68d6`
