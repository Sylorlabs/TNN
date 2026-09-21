# Track A Closeout — Section-Verdict Spot-Check

**Crew:** section-verdict spot-check crew · **Date:** 2026-09-21
**Scope:** the 7 section verdicts in `docs/lab/units/arms/{E,I2,K2,M,M2,P,Z3}/VERDICT.md`
**Method:** (1) §3 kill criterion extracted *programmatically* from the frozen
`units/PREREG_FREEZE.md` (never from memory) and diffed against each verdict's
quotation; (2) cited evidence files checked for existence; verdict numbers
parsed from the scorecard JSONs and compared; (3) one cited measurement per
verdict re-run pure-Zag from the arm's build (`units/arms/<ARM>/`), byte-compared
against the evidence; (4) KILLED/PASS conclusion checked against
criterion + evidence for logic gaps.

**Headline:** 6 of 7 verdicts CONFIRMED. 1 (M) has a confirmed headline
(scoped KILL) but a stale secondary claim (M-dedup death) contradicted by the
arm's own corrected evidence, reproduced by this crew. 1 (Z3) has a confirmed
conclusion but a comparator-evidence gap that should be repaired.

---

## E — Ephemeral chunks — **CONFIRMED (KILLED)**

**§3 quote check:** The verdict quotes the kill criterion verbatim for its
binding sentence:
"Stored-bytes-per-recall ≥ 2× B-64's at equal M1 on either corpus at 10x
(copies-only strictly dominated by the dumbest persistent segmentation)."
The frozen row has one additional informative sentence the verdict omits from
the quotation block ("Expected to die informatively; its death certificate
reads 'references matter, transient segmentation does not.'") — but the
verdict reproduces that exact text separately as the death certificate. Minor
quotation-boundary difference, no effect on the kill. (Diff run
programmatically against `PREREG_FREEZE.md` §3 row.)

**Evidence:** `evidence/` holds `e_m5_10x.txt` (slot table **91,679,710**),
`b64_m5_10x.txt` (slot table **33,167,612**), and M1 10x legs for both arms on
both corpora. Ratio = 91,679,710 / 33,167,612 = **2.764× ≥ 2×** — the
criterion fires. `scorecard_r1_1x.json` matches the verdict's 1x row
(M1 100.0/100.0 both corpora, 84,731/148,678 units; M5 9,322,125 slot bytes,
85,731 ledger entries; M8 M8GATE PASS).

**Rerun (this crew):** `E/work/e_bin m5-10x <10x corpus root>` → METRIC_JSON
with `m5_slot_table_bytes: 91679710`, **byte-identical** to the evidence run;
`E/work/b64_10x/b64_10x_bin m5-10x` → `m5_slot_table_bytes: 33167612`.
Equal M1 at 10x confirmed in evidence: `M1,prose.bin,100.0,100.0,847301` and
`M1,code.bin,100.0,100.0,1486773` for both arms.

**Logic:** "either corpus" is satisfied on prose; audit ledger excluded per
the prereg's own M5 definition (verdict discloses the alternative reading:
including it gives 1.67×). Conclusion follows. The B-64-10x measurement-only
variant is disclosed as evidence tooling, not a new arm.

---

## I2 — DAG hierarchy — **CONFIRMED (KILLED)**

**§3 quote check:** Byte-identical to the frozen row: "Record savings over I1
< 10%, OR parent-arbitration error > 10% — I2 dies, I1 remains the hierarchy
candidate."

**Evidence:** `raw_logs/` holds `hier_run5.log`, `hier_final1.log`
(two full runs), `battery_run.log`, `build.log`. `scorecard_i2_1x.json`:
savings 75.5% (`i2_kill_savings: false`), arbitration error 55.9%
(`i2_kill_arb: true`), wrong 70,988 / right 55,778 / uncovered 37,709,
per-type 71.9% — all match the verdict.

**Rerun (this crew):** `I2/work/i2_bin i2-hier-1x <corpus>` → RC=0;
HIER/METRIC_JSON lines **byte-identical** to `hier_final1.log`:
savings 75.5%, error 55.9%, `i2_verdict: KILLED`.

**Logic:** OR criterion — condition 1 (75.5% ≥ 10%) passes, condition 2
(55.9% > 10%) fires → KILLED. Excluding uncovered occurrences from the error
denominator is the conservative choice and is disclosed; including them
(66.1%) fires the bar too. No gap.

---

## K2 — 64-bit FNV-1a identity — **CONFIRMED (PASS)**

**§3 quote check:** Matches the frozen row (byte-verified after whitespace
normalization): bidirectional chain-length / K1-comparison criterion.

**Evidence:** `raw_logs/` (m1p/m1c/m2/m3/m4c/m4p/m5/m5b/m6/m7/t-collision legs),
`scorecard_1x.json`. Every corpus run reports `K2CHAIN` with max_chain = 1,
collisions = 0; the synthetic `t-collision` honestly exercises the chain path
(3 forced, chain 3). Scorecard: M5 2.417× (bar 1.5, FAIL), audit 16.19/KB
(bar 10, FAIL), M7 hit 100.0 / reuse 2.97 / dedup 0.50. The verdict's cited
"per-add cost 153.7 bytes" is not a scorecard field but is derivable from
scorecard M5 numbers: (7,684,368 + 5,422,784) / 85,231 = 153.76. ✓

**Rerun (this crew):** fresh `znc` compile of `K2/cl/arm.zag` (pure Zag) →
`m1-1x-prose` → `K2CHAIN,prose.bin,1,0`, matching evidence. Kill bar (> 4)
never approached.

**Logic:** Chain direction — no fire. K1 direction — correctly reported
UNDECIDABLE (K1 has not reported dedup/cost), not assumed. M5 bar failures
correctly distinguished as scorecard bars, not kill triggers ("K2's kill
criterion does not include M5"). 10x blocked per the task rule since not all
1x bars pass. PASS follows; nothing was bent to reach it.

---

## M — Counter IDs — **HEADLINE CONFIRMED (KILLED, scoped); M-dedup sub-claim DISPUTED by arm's own corrected evidence**

**§3 quote check:** The verdict quotes the full criterion across two
blockquotes; the only omission vs the frozen row is the "**Scoped:**" bold
label — all binding content is present, and the verdict header reads
"KILLED (scoped)". Non-material.

**Evidence:** `raw/` logs exist for all 1x modes. `merge-1x.stdout`:
`MERGE,nA,84731,nB,148678,links,1487,dangling,0,misdirected,0,remap_frac_x10000,3914,kill,1`
— remap compute 39.14% > 10% bar fires; dangling/misdirected = 0.
`scorecard-1x.json` agrees (`merge_remap_frac: 0.3914`, `merge_scoped_kill`).

**Rerun (this crew):** `M/.work/m_bin_final3 merge-1x <corpus>` → the MERGE
line above, **byte-identical** to evidence. RC=0.

**Logic (scoped kill):** The criterion's "remap compute" is genuinely
ambiguous (the verdict discloses both: inclusive table-build + rewrites =
39.14% fires; pointer-rewrites-only alt = 0.38% does not). The inclusive
reading is the defensible one — building the 148,678-entry remap table IS
remap compute; the table exists solely because of remapping — and the raw
METRIC_JSON itself sets `merge_scoped_kill: true` / `merge_remap_frac_alt_x10000: 38`.
Headline conclusion follows: counter IDs die as cross-store/global identity,
survive as store-local handle.

**DISCREPANCY — M-dedup sub-claim:** The verdict says the M-dedup claim
DIES on `M7 dedup_barred = 0.00 (< 0.4 bar)`. But `units/arms/M/BUILD_LOG.md`
documents a later correction: that 0.00 was measured with the dedup path
*compiled out* (`if(false && dedup==1)`), so it never tested the mechanism —
an invalid measurement. The real bug was the hash table keyed by buffer
offset instead of content hash; after the fix, full M7 protocol, double run,
byte-identical stdout:
`M7,counter-id,hit,100.0,reuse,3.02,dedup_barred,50.01,dedup_r3,66.34`
— i.e. 0.5001 ≥ 0.4, the claim **SURVIVES**, and M7 reuse moves 1.01 → 3.02
(bar ≥ 1.5 now PASSES). **This crew reproduced the corrected measurement
exactly** with `M/.work/m_bin_dedupfix m7-1x <corpus>` (RC=0, byte-identical
M7 line). The verdict's "Coordinator corrections acknowledged" section does
not mention this re-evaluation, so the verdict document is stale on this
sub-claim. The headline scoped kill is unaffected (it rests on the merge
trial, which fires independently). **Needs a coordinator ruling:** does the
corrected evaluation supersede the verdict's M-dedup death, or does the
verdict's revert-to-pure-issuance stand?

---

## M2 — Compositional counter IDs — **CONFIRMED (KILLED)**

**§3 quote check:** Matches the frozen row: "Single-byte leaf edit
invalidates > 25% of cached compositions in the recall benchmark, OR ID
recomputation > 10% of recall latency on the 10x run."

**Evidence:** `k2_10x.json` records both official 10x runs with ns timings
(A: ratio 28.8%, B: 26.8%, stdout `M2K2,prose.bin,KILLED`); `k2_10x/`
holds run_A/B stdout+stderr and summary.txt; `DEATH_CERTIFICATE.md` present;
`scorecard_1x.json` has `binding_k1: PASS` (2 stale / 63,547 = 0.003%).

**Rerun (this crew):** `/home/hatch/workspace/m2scratch/m2_bin m2-k2 <corpus>`
(1x) → `M2K2,prose.bin,KILLED`, ratio 30.7% (verdict's own 1x: 25.8%;
official 10x A/B: 28.8%/26.8% — wall-clock variance, verdict line stable and
always > 3× the bar).

**Logic:** K1 (0.003% ≤ 25%) passes; K2 fires on the official 10x run (both
legs) → KILLED. The verdict's `m7-1x: PENDING` does not touch the binding
criterion. No gap.

---

## P — Emergent vocabulary — **CONFIRMED (PASS)**

**§3 quote check:** Matches the frozen row (verdict also quotes the mechanism
line; the binding-kill text is verbatim).

**Evidence:** `scorecard_1x.json` `binding` block: emergent 267/500, baseline
0/500, margin 53.4 (bar ≥ 3), churn 42/90 = 46.7% (bar > 50% to fire),
`killed: false`. Note: the docs dir carries no dedicated mbind-1x raw log
(modes list lacks `mbind-1x`); the binding numbers live in the scorecard.
This crew's rerun output is preserved in the spotcheck dir as a raw record.

**Rerun (this crew):** `P/work/P_bin mbind-1x <harness dir>` → RC=0:
`TAG BINDKILL,words_k7,180,words_k3est,180,words_k14est,180`;
`TAG BINDKILL,probes,500,base,0,emer,267,margin_thou,534`;
`TAG BINDKILL,churn,42/90`; `TAG BINDKILL,verdict,PASS,none`.
Exact match to the verdict's binding-trial table.

**Logic:** Branch 1: 53.4 ≥ 3 → no fire. Branch 2: 46.7% ≤ 50% → no fire.
→ PASS. The verdict's limitations are honest (sensitivity calibration
uninformative on this corpus subset; M5 timeout is performance, not
correctness; "held-out" means stale-via-LRU, not untrained). The 53.4-point
margin vs the 3-point bar and the symmetric treatment of baseline vs
emergent make the conclusion robust to the held-out caveat.

---

## Z3 — Budgeted chunks — **CONFIRMED (SURVIVE), with a comparator-evidence gap to repair**

**§3 quote check:** Byte-identical to the frozen row, including the A-53
sentence.

**Evidence:** `evidence/` holds per-mode raw logs, `GATE.txt`,
`battery.log`, `scorecard_raw_shared.json`; `scorecard_z3_1x.json` matches the
verdict: total cost 9,056,909 (= 826,700 + 1,419,712 + 1,387,776 +
5,422,721 ✓), b64 14,336,873, ratio 0.6317, bar 11,469,498 (0.8 × b64 ✓);
half-B diagnostic 100.0 → 100.0 on both corpora, 0% drop (bar > 15%).

**Rerun (this crew):** fresh `znc` compile of `Z3/cl/arm.zag` → `m5-1x` →
`M5,21183,5422721,826700,1419712,-1`, matching the scorecard components
exactly. Cost arithmetic and ratio re-verified from components.

**Logic:** Prong 1: Z3 36.8% below the best fixed-granularity arm at equal
M1 (both 100.0/100.0 both corpora) — bar requires Z3 NOT ≥ 20% below, so the
kill does not trigger. Prong 2: 0% drop on halving B — no cliff. A-53 is
stated in ARM_SPEC §2. → SURVIVE.

**Evidence gap (flag, not fatal):** the comparator cost numbers
(b64 = 14,336,873, b16 = 40,518,457, b8 = 75,427,217) exist ONLY as asserted
values in the scorecard and verdict — no comparator raw logs, binaries, or
battery runs are preserved anywhere (not in `evidence/`, the arm dir, or
`~/workspace/z3scratch/battery1x_v2/`; the verdict's cited
`battery1x_v2/work/` has no comparator runs). Related: `evidence/scorecard_raw_shared.json`
is labeled `"arm": "b64"` but contains Z3's own numbers (21,183 units, budget
4M, economic ledger) — a mislabeled assembly artifact. First-principles
sanity check supports the asserted b64: scaling E's measured b64 10x
slot-table cost (33,167,612 B / 847,301 u ≈ 39.15 B/u) to 1x 84,731 units
gives ≈ 14.16M total vs asserted 14.34M (within ~1.2%); flipping prong 1
would need b64 ≤ 11.32M (~21% lower), which is implausible. The conclusion
is robust, but the evidence trail should be repaired: preserve the
comparator raw logs and fix the mislabeled file before the closeout is
signed.

---

## §7 metric-count recommendation: "8 scored metrics"

**The ambiguity:** frozen §7 rule 2 says "≥ 6 of the **8 scored metrics**
(M1–M7 scored; M8 is eligibility only; M9 informational, never counts)" —
M1–M7 is seven metrics, contradicting the numeral. METRICS.md's formal
blowout rule repeats it: "≥ 6 of the 8 scored metrics (M1–M8 excluding
M8-as-gate; M8 contributes only eligibility, M9 is informational and never
counts)" — again seven families.

**Disambiguating evidence (all from frozen text, extracted programmatically):**

1. §5 M1 is the only metric whose definition explicitly splits it into
   separately-scored components: "Sub-scores: content recall rate (returned
   bytes == source bytes for the claimed span) and boundary fidelity
   (claimed span == ingest-assigned span), **recorded separately, never
   folded**."
2. §7 rule 4's example only works with denominator 8: "an arm with M7 N/A
   needs ≥ 6 of 7" — 8 total minus 1 N/A = 7 applicable; threshold =
   max(6, ceil(0.75 × 7) = 6) = 6 of 7. With a 7-metric reading it would be
   "≥ 6 of 6".
3. METRICS.md's machine-readable schema already separates M1 into
   `m1_recall_*` / `m1_boundary_*` columns.
4. The scorecard schemas in this battery do the same (e.g.
   `scorecard_r1_1x.json` has `m1` with recall/boundary sub-fields plus a
   separate `m1_id_probe`).

**Recommendation:** read "8 scored metrics" as
{M1-content-recall, M1-boundary-fidelity, M2, M3, M4, M5, M6, M7}.
M8 remains eligibility-only, M9 informational. Blowout threshold: ≥ 6 of
*applicable* scored metrics (75%), with N/A exclusion per rule 4.

**Rejected alternatives:** counting M4's two revision classes or M6's two
transfer directions as the 8th — neither metric's definition carries
"recorded separately, never folded" scoring language; reading the numeral
as a typo for 7 — breaks rule 4's arithmetic as shown above.

**Governance note:** METRICS.md states that counting-rule changes need
Micah's re-approval. This is presented as the defensible *interpretation*
of frozen text for sign-off, not a unilateral amendment — the numeral 8
and rule 4's example are already in the frozen text, so this reading
requires no textual change.

---

## Appendix — spot-check rerun record

| Arm | Rerun command (pure Zag) | Result vs evidence |
|---|---|---|
| E | `e_bin m5-10x <10x root>` → 91,679,710; `b64_10x_bin m5-10x` → 33,167,612 | byte-identical METRIC_JSON; ratio 2.764× fires |
| I2 | `i2_bin i2-hier-1x <root>` | byte-identical to `hier_final1.log`; savings 75.5%, error 55.9%, KILLED |
| K2 | fresh `znc` build → `m1-1x-prose` | `K2CHAIN,prose.bin,1,0` matches evidence |
| M | `m_bin_final3 merge-1x <root>` | byte-identical MERGE line (`remap_frac_x10000,3914,kill,1`) |
| M | `m_bin_dedupfix m7-1x <root>` | `dedup_barred,50.01` — reproduces the corrected (post-verdict) evaluation |
| M2 | `m2_bin m2-k2 <root>` (1x) | `M2K2,prose.bin,KILLED`, 30.7% > 10% bar |
| P | `P_bin mbind-1x <harness>` | exact match: 180 words, 267/500, 53.4 margin, 42/90 churn, PASS |
| Z3 | fresh `znc` build → `m5-1x` | `M5,21183,5422721,826700,1419712` matches scorecard |

Rerun outputs preserved in this directory (`spotcheck/`): E_m5_10x.stdout,
B64_m5_10x.stdout, I2_hier.stdout, K2_m1.stdout, M_merge.stdout,
M_m7dedup.stdout, M2_k2.stdout, P_mbind.stdout, Z3_m5.stdout. The two
fresh-compile binaries (`k2_bin`, `z3_bin`) are local rerun tooling only and
are **not** part of the committed record.
