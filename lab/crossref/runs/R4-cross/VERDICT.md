# R4-CROSS VERDICT — TP1 + SOURCE_AUTHORITY_LICENSE (Type C cross-check)

**Verdict: PARTIAL**

All committed numbers reproduce exactly under independent re-derivation
(142/142 Zag checks green; 3 byte-identical runs; all present-file digests
match). However, several license terms have no direct measured basis —
they are debate/governance decisions, derived math, or explicitly
provisional per the license's own Annex A.4. They are named in §3 below.

**NOT REPRODUCED does not apply:** zero number mismatches were found.

## Method (independent, Type C)

- Fresh clone at `~/workspace/scratch-crossref/R4/clean-cross/`
  (branch `tnn-native-lab`, frozen commit `7b2100d0`), run dir
  `~/workspace/scratch-crossref/R4/cross/`. R4-PRIMARY scratch never read;
  live workstreams untouched.
- Python glue only extracted fields from committed evidence into TSVs
  (`prep_extract.py`); **all reasoning and verification is pure Zag**
  (`r4_verify.zag`, built with the pinned znc, zero RNG).
- The verifier re-implements the frozen decision procedures from the
  prereg text (PREREG-TP1 §2–§3 shape classifier + T1/T2/T3 rules;
  round-3 arm semantics from PREREG-MW-R3/AMENDMENT-A2/A3), recomputes
  every decision from the raw corpus rows, and compares against the
  committed logs; recomputes every headline number from the raw
  decisions; checks digests, ledger heads, twin formulas, latent-truth
  rules, estimator definitions, gate-value analysis, k/(k+1) arithmetic,
  and the T2 frontier table.
- Output digest (3 runs): `7789bdbb51ab5ad96ebfd13379569e06aa9673312b54cd0eb2c8e6fe4e595033`
  — byte-identical across all three runs.

## §1 Frozen pins (verified before any run)

| Pin | Role | Commit subject | Status |
|---|---|---|---|
| `c85c9b41770c1878fb00a8dc991a5b4f17f8caaa` | TP1 result + evidence | third-path TP1 verdict: T1 licensed, T3 null, T2 conditional (evidence) | present, frozen |
| `44afdbefc168edddcae50e9dd91eac12cd9fa156` | TP1 prereg | PREREG-TP1: S1 third-path head-to-head (frozen 2026-09-22) | present, frozen |
| `b22ff31272d1789da4d35bf489d30d5e0d7c41f6` | round-3 sweep | round3: VERDICT-MW-R3 — source-authority reliability sweep COMPLETE | present, frozen |
| `3a3541ef62d05e929bdb47e4228e6e2b3a89fe02` | license law | SOURCE_AUTHORITY_LICENSE: final law (Micah-ordered 2026-09-22) | present, frozen |

Toolchain: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.

## §2 Every tested number vs committed value

### TP1 (evidence commit `c85c9b41`)

| # | Tested | Committed | Re-derived | Match |
|---|---|---|---|---|
| 1 | envelopes in `tp_data.json` | 220 (180 U + 20 S8 + 20 G2) | 220 (180/20/20) | ✓ |
| 2 | decision lines in `run0.log` | 2,640 (220×4×3) | 2,640 | ✓ |
| 3 | shape census (independent classifier) | 200 S1 / 20 S8 / 0 other | 200 / 20 / 0 / 0 | ✓ |
| 4 | per-envelope shape vs block expectation | 0 violations | 0 | ✓ |
| 5 | decisions recomputed vs log | 0 mismatches | 0/2640 | ✓ |
| 6 | chosen-id recomputed vs log | 0 mismatches | 0/2640 | ✓ |
| 7 | reason-code recomputed vs log | 0 mismatches | 0/2640 | ✓ |
| 8 | reason histogram | 380/340/80/80/880/380/420/80 | identical | ✓ |
| 9 | T1 Block-U EV @ t=500 (k=1) | +78/180 | +78 | ✓ |
| 10 | T1 Block-U EV @ t=667 | +74/180 | +74 | ✓ |
| 11 | T1 Block-U EV @ t=750 | +66/180 | +66 | ✓ |
| 12 | T1 Block-U EV @ t=833 | +54/180 | +54 | ✓ |
| 13 | T1 fires per level @500 | 0,0,20,20,20,20,20,20,20 | identical | ✓ |
| 14 | T1 wrong per level @500 | 0,0,10,8,6,4,2,1,0 | identical | ✓ |
| 15 | T3≡T1 identical decisions | 880/880 | 880/880 | ✓ |
| 16 | S8 converges (T1/T2/T3) | 0/0/0 | 0/0/0 | ✓ |
| 17 | T1-TIEGUARD lines | 80 (20×4) | 80 | ✓ |
| 18 | G2 T1 fires / T3 fires | 0 / 0 | 0 / 0 | ✓ |
| 19 | twin formula `(i·n_A)%20<n_A ⟺ S1A` | 0 violations/200 | 0 | ✓ |
| 20 | S8 latent rule (i even ⟺ latent=prim) | 0 violations/20 | 0 | ✓ |
| 21 | ledger heads H\|T1/T2/T3 | `e17861ba…` / `3c030dd4…` / `d2f45295…` | byte-identical | ✓ |
| 22 | S\|880\|880\|880, C\|1\|200\|2\|20\|3\|0\|0\|0 | as committed | byte-identical | ✓ |
| 23 | `run0.log` sha256 | `d57fda22…1d9` | `d57fda22…1d9` | ✓ |
| 24 | run1–4.log digests | `d57fda22…1d9` (SHA256SUMS) | **files absent from tree** — attested only | ⚠ |

Note on #24: the evidence tree contains only `run0.log`; `SHA256SUMS`
attests run1–run4 share its digest, but the files are not present to
re-hash. The substantive replication (all 2,640 decisions recomputed
from the corpus, 0 mismatches) does not depend on them.

### Round 3 (evidence commit `b22ff312`)

| # | Tested | Committed | Re-derived | Match |
|---|---|---|---|---|
| 25 | manifest envelopes | 420 | 420 | ✓ |
| 26 | log lines (3 arms × 5 runs × 420) | 6,300 | 6,300 | ✓ |
| 27 | run-identity per arm (runs 1–4 vs run 0) | 0 diffs | 0/0/0 | ✓ |
| 28 | per-arm rerun digests | `14d81ec5…` / `3b43d255…` / `58ae289b…` | identical, all 15 logs | ✓ |
| 29 | `.err` files | empty sha256 | empty (`e3b0c44…`) | ✓ |
| 30 | arm B withholds | 420/420 | 420 | ✓ |
| 31 | arm C block-U withholds (frozen C) | 180/180, EV 0 | 180, EV 0 at all 9 levels | ✓ |
| 32 | arm D block-U EV per level | −8,−4,0,4,8,12,16,18,20 | identical | ✓ |
| 33 | arm D block-U per-case EV (table) | −.40,−.20,0,+.20,+.40,+.60,+.80,+.90,+1.00 | identical (×1000) | ✓ |
| 34 | 2r−1 identity | exact (8 rows); 9th within one case | bound holds; measured +1.00 vs theoretical 0.98 at r=.99 is one 20-case step | ✓* |
| 35 | crossover r* | 0.50 (EV −4 @.40, 0 @.50) | −4 / 0 | ✓ |
| 36 | arm D block-U total (ungated D) | +66/180 | +66 | ✓ |
| 37 | R block C≡D verdict-identical | 180/180 | 180/180 | ✓ |
| 38 | R block loose−conservative Δ per level | +0.00 ×9 | 0 ×9 | ✓ |
| 39 | S8: C conv / C wrong / D conv / D wrong | 20 / 10 / 20 / 10 | 20 / 10 / 20 / 10 | ✓ |
| 40 | G r̂_max per envelope | 0/3 ×20 | sum 0/60 | ✓ |
| 41 | G r̂_all per envelope | 2/4 ×20 | sum 40/80 | ✓ |
| 42 | G2 estimators constant in block | twin-identical | range 0; values 0/3, 1/3 | ✓ |
| 43 | strict-gate admitted/value @ t=.3/.5/.7/.9 | 0 / 0 | 0 / 0 ×4 | ✓ |
| 44 | lenient-gate admitted @ t=.3/.5/.7/.9 | 20 / 20 / 0 / 0 | 20 / 20 / 0 / 0 | ✓ |
| 45 | lenient-gate value | 0 at all t | 0 ×4 | ✓ |
| 46 | k/(k+1) rounded ×1000, k=1,2,3,5,10 | 500/667/750/833/909 | identical | ✓ |
| 47 | T2 frontier ρ_min ×1000 (9 cells) | 200/238/294/333/500/385/455/556/625 | identical | ✓ |

\* #34: the verdict's "exactly" is exact for 8 rows; at r=.99 the
20-case measurement is 20/20 = +1.00 vs theoretical 2r−1 = 0.98 — a
one-case granularity step, and the committed table itself prints +1.00.
Not a discrepancy; the table value is what was tested and it matches.

**Zero mismatches across all 47 numbered items (142 atomic Zag checks).**

## §3 Term-by-term SOURCE_AUTHORITY_LICENSE.md trace

Basis codes: **M** = directly measured (re-derived above);
**D** = derived from measured values by stated math;
**G** = governance/debate decision (no trial measurement);
**U** = explicitly unmeasured/provisional (license admits it).

| License term | Basis | Measured support (item #) / gap |
|---|---|---|
| §1.1 T1 fires iff shape+tie+reliability+cost+boundaries | M/D/G | conjunction; components traced below |
| §1.2 uncorroborated = only shape where loose beats conservative; corroborated Δ +0.00/case | M | #37, #38 (180/180 identical, Δ 0 at all 9 levels) |
| §1.3 tie = hard veto regardless of reliability | M (narrow) | #16, #17 (0/20 S8 installs; 80 TIEGUARD lines) |
| §1.4 CI lower-bound gate, strict > k/(k+1) | D+G | trials used stipulated r; strictness from measured EV=0 at equality (#35) |
| §1.5 cost gate k per §1.1 | G+D | table is governance; formula from #32–#35 |
| §1.6 boundary check | mixed | see §6 rows |
| withhold EV = 0, safe default | M | #30, #31 |
| §1.1 k/(k+1) table (k=1) | M | #32–#35 |
| §1.1 k/(k+1) table (k=2..10) | D | #46 (arithmetic verified; license: "derived") |
| §1.1 k-table design: versioned, human-governed, claim-type × consequence class, default k=1, frozen at intake, backdoor seal, disjoint maintenance | G | **no trial measurement — debate decision (unanimous)** |
| §1.1 KB-K1/K2/K3 | G | standing rules, not measured |
| §2.1 tie = 2v2 S8 shape | M | #16, #17, #39 |
| §2.1 tie = broad class (n:n, weighted, multi-candidate, 1v1v1) | U | **no trial data — license's own kill bar requires adversarial coverage before deployable** |
| §2.2 PARK: never install, no confidence, TIE_PARKED, re-open only on new evidence | M (2v2) | #16 (0 installs, 0 confidence emissions on 2v2) |
| §2.2 never ages into install (no timeout/refresh/serialization path) | G | **no temporal trial run** |
| §2 kill bar (0/20 + adversarial coverage; breach suspends all licenses) | M (2v2) + U (rest) | 2v2 half measured; adversarial half pending |
| §3.1 operational criteria (n≥20, independent ground truth, no cherry-picking, stratification, 24-mo recency, disjoint maintenance) | G+U | **trials used stipulated r — never measured whether these criteria establish reliability; 24 months explicitly PROVISIONAL (A.4)** |
| §3.2 EV(install)=(k+1)r−k, EV(withhold)=0 | D | algebra over #32–#35 |
| §3.2 destruction regime −0.40/−0.20 at r=.30/.40 | M | #32, #33 |
| §3.2 twin-identity ⇒ nothing dispute-internal excludes low r | M | #40–#42, #43–#45 (estimators constant; gated value 0) |
| §4.1 channel qualification (6 criteria + anti-syndication + test≠qualification) | G | **no channel trial — debate decision; only the negative measured** |
| §4 T2 withholds 880/880 absent a channel | M | #7 (T2-SUSPECT ×880) |
| §4.2 (ρ,q,δ) frontier formula + table | D | #47 (preregistered math, arithmetically verified; no measured channel trial) |
| §4.3 deferral lifecycle (DEFER_RETIRED_UNRESOLVED, no retroactive install, no T1 preemption) | G | **policy; unmeasured** |
| §5 T3 null: 880/880 identical, no license beyond T1, audit value | M | #15 |
| §6.1 ties | M (2v2) + U (broad) | as §2.1 |
| §6.2 no usable external reliability → withhold | M | #18 (G2: 0 fires), #32 (destruction regime) |
| §6.3 r ≤ k/(k+1) kills license | M | #13 (0 fires @ r=.30/.40), #35 |
| §6.4 corroborated disputes | M | #37, #38 |
| §6.5 skepticism-category exclusion | G | **standing law; not measured by these trials** |
| §6.6 non-factual installs | G | **policy boundary** |
| §6.7 untested shapes → withhold | G | **by construction unmeasured** |
| §6.8 pending T2 preemption | G | **adopted from debate; no trial** |
| §6.9 un-oracle-verifiable installs | G | **boundary by construction** |
| §6.10 high-k audit flag | D+G | derived thresholds (#46) + governance flag |
| §7 governance (human-owned tables, Micah re-approval, review triggers) | G | **governance; not trial-measured** |
| Annex A debate record / kill-bar table | record | process record, not trial evidence |
| Annex A.4 honest gaps (recency, k>1, CI gate, Sol Q3, no fan-out) | admitted | consistent with this trace |

### Terms lacking direct measured basis (the PARTIAL list)

1. **§1.1 k-table design** — versioned human-governed cost table keyed by
   claim-type × consequence class, default k=1, frozen-at-intake,
   backdoor seal, disjoint maintenance, KB-K1/K2/K3: unanimous debate
   decision, no trial measurement.
2. **§1.4 CI lower-bound gate** — derived statistical law; the trials
   used stipulated r (license A.4 admits this).
3. **§2 broad tie class** — n:n, weighted, multi-candidate ties,
   stale-refresh/timeout/aging/serialization behavior: no trial data;
   the license's own kill bar makes deployability conditional on
   adversarial coverage not yet run.
4. **§3.1 operational reliability criteria** — including the
   **provisional 24-month recency window**: never measured (stipulated r
   in trials).
5. **§4.1 T2 channel qualification** — six criteria + anti-syndication
   rules: debate decision; no second channel was ever trialed (only the
   no-channel negative: 880/880 SUSPECT withholds).
6. **§4.2 frontier as applied** — the table arithmetic verifies, but no
   measured channel trial exists behind (ρ,q,δ).
7. **§4.3 deferral lifecycle** — governance policy, unmeasured.
8. **§6.5–§6.9 boundaries** (skepticism, non-factual, untested shapes,
   T2 preemption, oracle-verifiability) — policy/governance boundaries,
   not trial results.
9. **§7 governance** — human ownership, amendment re-approval, review
   triggers: governance, not measured.
10. **Annex A debate record** — process record; the cross-check did not
    independently verify the debate events (out of Type-C scope).

## Verdict rationale

The frozen verdict rule is mechanical: REPRODUCED requires every number
to match **and** every license term to carry measured support. All 47
numbered items match (142/142 atomic checks, byte-identical reruns,
digests confirm for every file present). Ten term-groups above lack
direct measured basis — most are openly labeled as governance decisions
or provisional in the license itself (Annex A.4). Hence **PARTIAL**:
the evidence fully reproduces; the law is broader than the evidence.

## Files

- Verifier: `~/workspace/scratch-crossref/R4/cross/r4_verify.zag`
- Extraction glue: `~/workspace/scratch-crossref/R4/cross/prep_extract.py`
- Evidence TSVs: `~/workspace/scratch-crossref/R4/cross/ev/`
- Run outputs (3×, sha256 `7789bdbb…e6fe`): `run1.txt`, `run2.txt`, `run3.txt`
- Frozen license copy: `~/workspace/scratch-crossref/R4/cross/license_frozen.md`
- This verdict: `~/workspace/scratch-crossref/R4/cross/VERDICT.md`
- Run log: `~/workspace/scratch-crossref/R4/cross/RUNLOG.md`
