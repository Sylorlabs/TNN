# HTD1 G-CO3 — Red-Team Verdict (Wave-2 crossref follow-up)

**Task:** Micah's directive (2026-09-24, verdicts round 2): *"HTD1 G-CO3 → more investigation + red team."*
Wave-2 crossref finding under review: *"G-CO3 KB2's 'planning share of ops' is computed on FROZEN-WEIGHTED COST … An unweighted/raw-count reading would flip the verdict to KILL … The weighted reading is the crew's interpretation; Micah did not rule on it."*

**Frozen authority:** commit `7b2100d09911c5c10252c5756c7def288e70bd1f`.
Verified from it (SHA-pinned, 2026-09-24):
- `prereg/HTD1_PREREG_FROZEN_2026-09-21.md` — git blob `76b5d3c531920f0025212974291123177d9391ae`
- `contracts/COST_MODEL_FROZEN.md` — git blob `e4064f3514f98de9abf611613c663608af459f4b`

**Red-team instrument:** independent pure-Zag verifier `src/gco3_verify.zag`, compiled with the
pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`),
run 3× byte-identical on `run_0/opcounts.bin`. Zero RNG in all decision paths.

---

## 1. Bottom line

**Recommend: weighted-PASS stands as the best-supported reading of the frozen contract — but the
raw-KILL reading is a genuine, textually available alternative, and the final governance call is
Micah's.** This report does not rewrite the Wave-2 verdict; it arms the decision.

The red team **failed to flip the verdict on any contract-faithful attack**. Every flip found
requires at least one of: (a) replacing the frozen weights with a different (unfrozen) metric,
(b) a coordinated all-class revaluation to the edge of the contract's own 2× calibration tripwire,
(c) an unnatural re-parse of the bar's denominator under which the bar's own negative control
stops working, or (d) a governance re-interpretation Micah has not issued.

The one thing the red team **did** establish as a real finding: **the weighted reading is the
crew's interpretation, not an explicit instruction.** Neither frozen document says "apply the §2
weights before forming the KB2 ratio." The weighted reading is strongly supported by the
contract's structure and intent, but the prereg's word "ops" gives the raw reading a legitimate
textual foothold. That is a governance gap, not a data defect.

---

## 2. What the data says (independently re-derived, pure Zag)

From `run_0/opcounts.bin` (124 items, verified byte-identical across 5 scored runs + 1 fresh
rebuild run — see §5):

| Quantity | Weighted (frozen) | Raw (uniform) |
|---|---|---|
| KB2a = planning share of first run | **0.6855 → PASS** (bar ≥ 0.60, +8.55 pp) | **0.4991 → KILL** (bar ≥ 0.60, −10.09 pp) |
| KB2b = amortized planning share | **0.1790 → PASS** (bar < 0.35) | **0.0906 → PASS** (bar < 0.35) |

Only KB2a flips. KB2b passes comfortably under both readings.

The pure-Zag verifier reproduces the scored milli-costs exactly:
`C_plan=122,525.540`, `C_exec=360,360.200`, `C_ver=201,667.200` — byte-match to `verdict.txt`.

Why the two readings diverge (class-contribution, weighted milli-cost):

| Class | Plan share of its class cost | Effect |
|---|---|---|
| OP-10 HASH (w=30) | plan 58,860 / total 178,860 ≈ **33%** | plan-heavy → lifts weighted KB2a |
| OP-07 WRITESC (w=20) | plan 4,960 / total 104,160 ≈ 5% | exec-heavy → drags weighted KB2a |
| OP-06 LBYTE (w=0.02) | plan 317 / total 20,902 ≈ 1.5% | exec-dominated; raw counts it equally |
| OP-05 MEMWRITE (w=0.5) | plan 13,320 / total 137,840 ≈ 10% | exec-heavy |

The raw reading lets the 944,860 exec-side LBYTE ops (weight 0.02 — nearly free) outweigh the
plan's hash/evidence work. The weighted reading prices each class at its frozen calibration.
**This is precisely the unpriced cross-class comparison the cost model's anti-Goodhart rule
(§1) and §9.1 were written to forbid.**

---

## 3. Red-team attacks — full record

| # | Attack | Result |
|---|---|---|
| A1 | **Raw-count steelman**: uniform weights, crew's denominator. Prereg says "ops"; raw vectors are mandatory committed evidence (§2). | **SUCCEEDS mathematically**: KB2a = 0.4991 → KILL. Genuine alternate reading; see §4 for why weighted is better-supported. |
| A2 | **Single-class weight flip**: for each class, exact boundary multiplier (thousandths) that flips weighted KB2a, all others frozen. | Closest: OP-10 HASH must drop 30 → **1.92** (×0.064, ~15.6× below frozen). OP-07 WRITESC 20 → 97.06 (×4.85). OP-05 MEMWRITE 0.5 → 4.07 (×8.13). OP-06 LBYTE 0.02 → 0.297 (×14.9). OP-09 GATE 0.05 → 1.04 (×20.9). **No single class flips within ±2×** — all boundaries far outside the contract's calibration tripwire (§2.1). |
| A3 | **Two-class ±2× combined perturbation** (worst pair: HASH ×0.5 + WRITESC ×2). | KB2a = 0.6199 → still PASS. |
| A4 | **Coordinated ±2× box**: all 2^10 corners over the 10 informative classes (OP-08 has zero counts; weight irrelevant). | Min corner KB2a = **0.5716 → KILL**. Requires plan-favoring classes ALL at 0.5× and exec-heavy classes ALL at 2× simultaneously — a conspiracy, not a calibration miss. Would need a Micah-approved amendment, not a silent reweight. |
| A5 | **Denominator re-parse**: "planning <60% of first-run ops" read as planning/(exec₀+ver₀) instead of planning/(planning+exec₀+ver₀). | Weighted: 2.18 → PASS. Raw: 0.9962 → PASS. **But**: under this parse the bar's own negative control (rubberstamp planner) PASSES weighted (0.79 ≥ 0.60) — the bar stops biting the degenerate case it was built to kill. The crew's denominator is the only parse under which the control works. Rejected. |
| A6 | **Ledger-overhead strip**: remove all mechanism-added entry costs from both sides (contract-INVALID attack — violates anti-Goodhart §1 and KB-HTD-1.5; run to test dependence). | Weighted 0.6855 → 0.7062 (still PASS). Raw 0.4991 → 0.4991 (still KILL). Verdict does not depend on ledger overhead. |
| A7 | **Per-item heterogeneity**: recompute KB2a per item (mean-run approx). | Weighted: min 0.5814, max 0.8310, mean 0.6982; **2/124 items below 0.60**. Raw: 95/124 below 0.60. Aggregate is the verdict unit per the frozen DESIGN; prereg does not require per-item clearance. Fragility note, not a flip. |
| A8 | **"Item 10" replay semantics**: "amortized planning ≥35% by item 10" re-read as "across the first 10 distinct items" rather than "10 replays of each committed plan". | Both readings PASS: weighted KB2b = 0.179 (10-replay) / raw = 0.0906; per-item max weighted KB2b = 0.3296 < 0.35. No flip under any parse. |
| A9 | **Stale-binary / decoy-bug resurrection**: rebuild scored binary from source with pinned znc; check the fixed decoy-length code is what's scored. | Rebuild is **byte-identical** to scored `gco3_bin_new` (SHA-256 `7daba46f…`). Fresh end-to-end run reproduces all 5 artifacts **byte-identical** to `run_0`. The decoy bug is dead; the scored binary contains the fix. |
| A10 | **Probe-manifest forgery**: verify all 124 spans against corpora (offsets + SHA-256), decoy validity. | **124/124 exact**; 0 self-decoys; 0 byte-identical decoys; 80 same-length decoy slots — matching the verdict sheet's claim that the post-fix SHA CHECK gains exactly 80 OP-03 over the buggy run. |
| A11 | **Control-suite discrimination under raw**: do the controls still behave if raw were the metric? | Rubberstamp raw 0.2520 KILL ✓, poison raw 0.1946 KILL ✓, mutate raw 0.6213 (not a KB2 control) ✓. Raw is a *working* discriminator — its only disagreement with weighted is the scored arm. This is a genuine metric dispute, not a broken-meter dispute. |

No contract-faithful attack flips the verdict. The flips that exist (A1, A4) each require
stepping outside the frozen contract's terms.

---

## 4. Weighted vs raw — the honest case for each

**For weighted-PASS (recommended as the better-supported reading):**
1. **Globality** (COST_MODEL §2): weights are "frozen for all of HTD-1 (global…)" — not scoped to
   efficiency comparisons. Gating bars are part of HTD-1.
2. **Explicit routing** (§5): G-CO3's KB2 is named as an "op-based bar" that uses "the same
   taxonomy" — the taxonomy whose classes are commensurable only through the frozen weights.
   The §5 default rule prices everything at frozen weights ("never the price").
3. **Anti-Goodhart intent** (§1, §9.1): the contract was written to prevent unpriced cross-class
   comparison. Raw KB2a lets 944,860 weight-0.02 exec-side byte-ops outweigh deliberate
   hash/evidence work — the exact gaming pattern the contract condemns.
4. **Control coherence** (§3 A5): the crew's denominator + weighted metric is the combination
   under which the rubberstamp negative control is killed most informatively (0.4421).
5. **Robustness**: survives every single-class and two-class ±2× perturbation; the §2.1
   calibration tripwire (2× deviation + Micah amendment) is never approached by any single-class
   flip boundary.
6. **Independent concurrence**: the Wave-2 closeout agent read it the same way; the raw
   alternative was disclosed in the verdict sheet itself per §2's transparency norm
   ("if re-weighting flips a champion, both champions are reported honestly").

**For raw-KILL (the legitimate steelman):**
1. **Textual fidelity**: the binding prereg says "ops", and reserves "FULL COST" for weighted
   cost. §5 says "taxonomy" (§1 = class definitions), not "weights" (§2).
2. **Purpose of weights**: weights price total cost C for savings comparisons; KB2 is a
   *structural* ratio (is planning substantial?), arguably not a costing.
3. **No explicit instruction exists.** The weighted reading is the best-supported
   *interpretation*, not a dictated computation. Micah never ruled.

**What would change this recommendation:** a Micah ruling for raw (governance, not evidence);
or measured calibration data showing a frozen weight off by >2× with an approved amendment
that moves a single-class boundary inside the envelope — currently no class is close.

---

## 5. Evidence-integrity verification (post-incident)

The 2026-09-23 vanishing-directory and daemon-restart incidents required treating all prior
state as suspect. Re-verified 2026-09-24:

- **Frozen docs**: re-fetched from commit `7b2100d0`; blob SHAs match (`76b5d3c5…`, `e4064f35…`).
- **Scored artifacts**: `run_0` ledger/steplog/outputs/opcounts/verdict hashes match the
  originally recorded values (5/5).
- **Binary provenance**: rebuilt `gco3.zag` from source with the pinned toolchain →
  **byte-identical** to the scored binary (SHA-256 `7daba46f7b012d85388929da0b577b917482f70ff959e8ed35dba4d498695092`).
- **End-to-end determinism**: fresh run from the rebuilt binary reproduces all five `run_0`
  artifacts **byte-identically** (R=5 previously recorded + this run = 6/6).
- **Probe integrity**: 124/124 spans verified against corpora (byte offsets + SHA-256).
- **Independent computation**: the pure-Zag verifier (no shared code with the scored binary
  beyond the IO substrate) reproduces all costs and all four KB2 readings exactly, 3×
  byte-identical stdout (SHA-256 `a6c19aa1…`).

No evidence of tampering, staleness, or silent data corruption was found. The stale-binary
incident from the original crew's log is fully resolved: the binary that produced the scored
evidence is proven to be built from the fixed source.

---

## 6. Recommendation to Micah

1. **Accept weighted-PASS as the contract-coherent reading of G-CO3 KB2** (recommendation, not
   a unilateral rewrite — the Wave-2 verdict stands as published either way until you rule).
2. **Close the governance gap explicitly**: amend the cost model or prereg with one sentence —
   *"Cross-class op-share bars (G-CO3 KB2a/KB2b) are computed on frozen-weighted costs"* — or
   rule for raw, which flips G-CO3 to KILL. Either ruling is defensible; the current state
   (crew interpretation, undisputed but unruled) is the weakest posture.
3. **Note the margin**: 8.55 pp on KB2a, 2/124 items individually below bar, adversarial ±2×
   corner flips at 0.5716. The PASS is real but not deep — worth one line in the Wave-2
   closeout.

## 7. Artifacts

- `src/gco3_verify.zag` (SHA-256 `5f63402a…`) — independent pure-Zag verifier + sensitivity
  scanner; `src/gco3_verify_bin` (SHA-256 `a68ddd82…`); `src/R33_NATIVE_IO_V1.zag` (SHA-256
  `e6379ddb…`, byte-copy of the build's IO substrate).
- `runs/verify_1.txt` / `verify_2.txt` / `verify_3.txt` — byte-identical (SHA-256 `a6c19aa1…`).
- `runs/gco3_rebuild_bin` — byte-identical to scored `gco3_bin_new` (SHA-256 `7daba46f…`).
- `runs/fresh/out/` — fresh end-to-end run, all artifacts byte-identical to `run_0`.
- `RUNLOG.md` — full command log.
- `prereg/` — SHA-verified frozen prereg + cost model excerpts used.

*Nothing was committed to `sylorlabs/TNN`; publication is the coordinator's call.*
