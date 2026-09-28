# R-3 RECOMMENDATION — B-T2 dual≈raw tolerance ε + minimum compression ratio

R-3 debate swarm · Track R0 · 2026-09-21
Recommends; Micah signs the amendment. **Do NOT commit** — coordinator commits.

## 1. Recommendation (what Micah is asked to sign)

- **ε (dual≈raw tolerance): |dual − raw| ≤ 25/1000** on hard-grounding score
  (n=200, milli-point units), i.e. `abs_delta_mp ≤ 25`.
- **Minimum compression ratio: ≥ 1.15** (i.e. `ratio_mp ≥ 1150`, where
  `ratio_mp = source·1000/stored`, integer-truncated; equivalently the dual
  route must store at most ⌊source/1.15⌋ bytes).

Proposed amendment text for the frozen prereg, §0 I / §2 R0.2:

> R-3 (signed 2026-09-21): B-T2 passes iff, per leg, (a) |dual−raw| ≤ 25/1000
> on the hard-grounding battery, (b) compression ratio ≥ 1.15
> (ratio_mp ≥ 1150), and (c) chunk_active < dual_active and chunk_active <
> raw_active on hard grounding. Both legs (recovered and re-derived
> parameters) are evaluated; the bar is one bar (R-7/R-8 test-both).

Under these numbers **both legs pass**: leg 0 (Δ=0, 1.417), leg 1 (Δ=0, 1.195).

## 2. Measured evidence (formal leg, frozen)

Byte-identical to the descriptive pass; N=5 + repeated baseline, 6/6 runs
byte-identical per leg; pure Zag, zero RNG in decision paths; expected-value
readback probe 0 fails (standing rule C — miscompile risk covered).

| leg | raw (/1000) | chunk (/1000) | dual (/1000) | \|dual−raw\| (/1000) | ratio | chunk<dual | chunk<raw |
|---|---|---|---|---|---|---|---|
| 0 (recovered params) | 950 | 550 | 950 | 0 | 1.417 | yes | yes |
| 1 (re-derived params) | 950 | 250 | 950 | 0 | 1.195 | yes | yes |

Compression internals (from `BT2_COMPRESSION` log lines, identical corpus):

| leg | source (bytes) | stored (bytes) | payload (live chunks) | promoted chunks | vocab_check |
|---|---|---|---|---|---|
| 0 | 30821 | 21740 | 5237 | 700 | 24/24 |
| 1 | 30821 | 25773 | 452 | 88 | 12/24 |

stored = payload + 4·nunits + nlit (chunk-bank re-encoding cost model),
ratio = source·1000/stored truncated. Leg 1 stores 4033 more bytes because
its smaller bank falls back to literals more often.

## 3. Debate 1 — candidates steelmanned

- **Strict** (ε ≤ 10/1000, ratio ≥ 1.2): means "dual within 1% of raw; ≥20%
  storage saving — substantial compression, not token." Consequence: leg 1
  fails the ratio bar (1.195 < 1.2) → R-3 FAILS. The descriptive crew's
  unsigned proposal. Note 1.2 is a round number that happens to split the
  two legs — data-fitted in the strict direction.
- **Lenient** (ε ≤ 25/1000, ratio ≥ 1.15): means "dual within 2.5% of raw;
  ≥13% saving — real compression with regime headroom." Consequence: both
  legs pass. Note 1.15 sits just below leg 1's 1.195 — data-fitted in the
  lenient direction.
- **Knee-based / structural**: no knee exists — only two operating points,
  no curve. Collapses into a structural reading: derive the floor from what
  the bar *means* ("adds compression" = rules out the degenerate dual-is-raw
  case; must not reject a pre-registered legitimate regime) rather than from
  the measurements' neighborhood.

## 4. Test 1 — sensitivity + the leg-gap investigation

### 4a. Candidate × outcome table

ε is **non-binding** on this evidence (Δ=0 exactly, both legs — every ε ≥ 0
passes). The ratio floor is the only binding choice:

| ratio floor | leg 0 (1.417) | leg 1 (1.195) | R-3 outcome |
|---|---|---|---|
| ≥ 1.0 (code's internal `ratio_gt_1000`) | pass | pass | PASS |
| ≥ 1.1 | pass | pass | PASS |
| ≥ 1.15 | pass | pass | PASS |
| ≥ 1.2 (descriptive proposal) | pass | **FAIL** | FAIL |
| ≥ 1.25 | pass | **FAIL** | FAIL |
| ≥ 1.4 | pass (barely) | **FAIL** | FAIL |

Every floor in (1.0, 1.195] is compatible with the evidence — the data
**underdetermine** the floor. The knife-edge is not resolvable *by* the
numbers; only by the pre-registered *meaning* of the legs.

### 4b. Is the 1.417 vs 1.195 gap structural or noise?

**Structural, by construction — zero noise involved.** Findings:

1. Within-leg variance is exactly zero: 6/6 runs byte-identical per leg
   (formal gate). There is no sampling noise to average out.
2. The legs are *different programs by pre-registered design* (`r0_init` in
   `r0_core.zag`): leg 0 recovered params (LRN_MINSUP=3, MARGIN=2, GAIN=0),
   leg 1 re-derived params (MINSUP=4, MARGIN=3, GAIN=500, CONFLICT=500) —
   a strictly tighter promotion gate.
3. The manifest's pre-execution amendment (frozen) *anticipates* leg 1's
   lower inventory: "uses a strictly tighter promotion gate; it promotes
   fewer vocabulary spans (observed 12/24 in development)" and defines
   leg 1's role: "tests whether the ablation conclusion survives
   independently re-derived parameters, not to reproduce leg 0's inventory."
4. The ratio gap follows structurally: fewer/smaller chunks (88 vs 700;
   payload 452 vs 5237) → more of the identical corpus (source=30821 both
   legs) falls back to literal storage → stored 25773 vs 21740 → ratio
   1.195 vs 1.417. The *ordinal* gap (leg 1 < leg 0) is derivable from the
   frozen parameters without measuring; only the *cardinal* 1.195 is not.
5. No miscompile confound: the expected-value readback probe (standing
   rule C, incl. the T=2 golden mini-run) passes first in every binary;
   the formal verdict confirms probe 0 fails.

The local toolchain (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`)
exists but a rerun was unnecessary: the question is answered by construction
plus byte-identical evidence, and rerunning a deterministic binary reproduces
the same numbers by the proven property.

## 5. Debate 2 — positions moved

A hostile second opinion (gpt-5.6-sol, via UnoRouter) attacked the lenient
position on three points; the swarm's positions moved as follows:

1. **"1.15 is indistinguishable from data-fitting."** Conceded in part: the
   *upper bound* of the floor cannot be derived without the cardinal
   measurement — any floor in [1.05, 1.19] is evidence-compatible, so the
   choice inside that interval is judgment, disclosed as such. But the
   "pre-registered legitimacy" defense is **not** circular: leg 1's
   legitimacy comes from the frozen pre-execution manifest amendment and
   frozen source constants, not from wanting the conclusion to survive.
   The lenient-vs-strict framing is the wrong axis entirely — the right
   rule is: **the floor must sit strictly above the degenerate point with
   margin, and strictly below the lowest pre-registered legitimate
   operating point with headroom.** A floor ≥ 1.2 rejects a regime the
   manifest pre-registered as legitimate — that is a bug in the bar, not a
   finding about the mechanism, and would contradict the amendment's stated
   purpose for leg 1.
2. **"Derive the floor from an external utility/budget instead."** Rejected
   as inapplicable: there is no deployment budget at this lab stage. The
   bar's purpose, derivable from the frozen prereg, is anti-degeneracy
   (rule out a dual route that stores everything verbatim, ratio = 1.0)
   plus regime-consistency (test-both). The floor's lower bound comes from
   the first purpose: 1.15 sits 150× the ratio quantization unit (1/1000)
   above the degenerate point, and truncation *understates* the ratio, so
   a measured 1150 guarantees true ≥ 1.150. It expresses a real claim: the
   dual route saves **≥ 13.0%** of stored bytes (1 − 1/1.15).
3. **"ε=25/1000 vs the chunk deficit is irrelevant; the data can't
   distinguish ε=0 from ε=50."** Conceded that the data can't discriminate
   (Δ=0); ε is precedent-setting for future re-applications of this bar
   structure. The chunk-deficit comparison is *not* irrelevant, contra the
   reviewer: the bar is a conjunction on one probe set in one unit, and its
   meaning ("dual≈raw AND chunk loses") requires ε ≪ raw−chunk, else the
   tolerance could swallow the rejected effect. 25/1000 is 28× below the
   smallest chunk deficit (700/1000, leg 1; 16× below leg 0's 400/1000).
   Resolution note (reviewer's question): scores are g·1000/200, so
   effective resolution is 5/1000 per probe label; ε=25/1000 = 5 labels =
   2.5 points — "within a handful of labels." ε=10/1000 (2 labels) would
   also be satisfied today; 25 is the more future-proof allowance and matches
   the descriptive crew's unsigned ε, so we move only the ratio, not both.

## 6. Test 2 — stress-testing (ε ≤ 25/1000, ratio ≥ 1.15)

1. **Survives both legs?** Leg 0: Δ=0 ≤ 25 ✓, 1417 ≥ 1150 ✓ (stored headroom
   5060 bytes, 23%). Leg 1: Δ=0 ≤ 25 ✓, 1195 ≥ 1150 ✓ (stored budget at
   floor = ⌊30821·1000/1150⌋ = 26800; actual 25773; headroom 1027 bytes ≈
   4.0% of stored). Under amended code the `BT2_BAR` verdict line would
   print PASS in both legs.
2. **Chunk-only rejection still meaningful?** Untouched by the floor: the
   rejection is a separate conjunct; chunk loses by 400 mp (leg 0) and
   700 mp (leg 1) — 16× and 28× the ε tolerance. No gaming path: the
   conjunction requires all three; no single conjunct can be satisfied
   degenerately (a ratio-1.0 dual fails; a dual 30/1000 worse than raw
   fails; a chunk-beating-dual fails).
3. **Teeth against degeneracy:** a dual route storing everything raw
   (ratio=1.0) fails; a trivial 2% compression (1.02) fails; only ≥13%
   saving passes.
4. **Quantization safety:** ratio_mp truncates, so the measured value
   understates the true ratio — the floor errs strict, never lenient.
5. **Fallback documented:** if Micah wants more headroom against future
   re-derivations compressing less than leg 1, **1.1** (≈8.7% stored
   headroom, ≥9.1% saving claim) is the evidence-compatible fallback.
   If he wants the bar to *reject* the tighter-gate regime, sign ≥ 1.2 —
   but that contradicts the frozen manifest amendment's purpose for leg 1
   and would need a manifest amendment alongside.

## 7. Why this is principled, not arbitrary

- The **rule** (not the number) is derived from frozen text: anti-degeneracy
  from §2's "while adding compression," regime-consistency from R-7/R-8
  test-both plus the manifest's pre-registered leg-1 role. Any floor
  violating either is wrong regardless of the measurements.
- The rule yields an **interval**, [1.05, 1.19]: above the degenerate point
  with real margin, below leg 1's 1.195 with structural headroom.
  **1.15** is the recommended judgment call inside it: the largest round
  number with genuine (~4%) headroom below the lowest legitimate operating
  point and a non-vacuous compression claim (≥13% saving). The residual
  data-dependence of the upper bound is disclosed, not hidden.
- ε = 25/1000 is derived from the bar's conjunction semantics (ε ≪
  raw−chunk deficit, 28× separation) and the probe resolution (5 labels),
  and it keeps the descriptive crew's unsigned ε — only the knife-edge
  parameter moves.

## 8. Files consulted

- `docs/lab/units/r0/evidence/ablation/FORMAL_VERDICT_R3.md` (branch
  `tnn-native-lab`, commit `13bbaf07067e`) — formal verdict, verdicts above
- `docs/lab/units/r0/impl/ablation/b_t2.zag`, `bt_common.zag`,
  `../core/r0_core.zag` — mechanism, compression formula, leg parameters
- `docs/lab/units/r0/evidence/ablation/MANIFEST_BT2_BT3.md` — pre-execution
  manifest incl. the leg-1 promotion-scope amendment
- `docs/lab/units/r0/evidence/ablation/b_t2_leg{0,1}.md` + `logs/b_t2_leg{0,1}_p0.log`
- Hostile second opinion: gpt-5.6-sol via UnoRouter (prompt + reply in
  /tmp — ephemeral; substance incorporated in §5)
- This file: `~/workspace/r0params/R3_RECOMMENDATION.md` (uncommitted —
  coordinator commits)
