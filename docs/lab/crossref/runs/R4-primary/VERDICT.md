# R4-PRIMARY VERDICT — TP1 third-path trial + source-authority reliability sweep

**Verdict: PARTIAL**

All committed numbers reproduce exactly under an independent pure-Zag
reimplementation (2,640/2,640 decisions byte-identical, all ledger heads
match, every round-3 sweep cell recomputed). The tie guard kills false
confidence (100% → 0%) and T3 has null value (880/880 identical to T1).
Per the frozen Tier-1 rule, however, the family is PARTIAL — not
REPRODUCED — because nine signed operative license terms lack direct
measured basis (named in §3 below). Nothing is contradicted; the
license's empirics are sound, but the law claims more than the trials
measured. The license itself honestly marks most of these as derived,
provisional, or governance (Annex A.4, §1.1, §6.10) — the PARTIAL
verdict records that gap rather than overriding that honesty.

Frozen scope: `7b2100d09911c5c10252c5756c7def288e70bd1f`.
Method: two independent pure-Zag verifiers (see RUNLOG.md); Python used
only as data-transcription glue. Zero RNG; 3 byte-identical runs each.

## §1 Committed vs observed — every number matches

### TP1 (220 envelopes × 4 thresholds × 3 paths = 2,640 decisions)

| Committed claim | Observed (independent Zag) |
|---|---|
| 2,640 `P\|` decisions as committed | byte-identical to `evidence/run0.log` (`cmp` clean) |
| T1/T2/T3 ledger heads as committed | all three match exactly |
| `S\|880\|880\|880` | `S\|880\|880\|880` |
| `C\|1\|200\|2\|20\|3\|0\|0\|0` (shapes) | identical |
| T1@0.500 Block-U aggregate EV **+78/180** | **+78** |
| Per-level EV = 2r−1 where it fires | (10,10),(12,8),(14,6),(16,4),(18,2),(19,1),(20,0) right/wrong at r=0.50…0.99 = round(20·(2r−1))/20 at all 9 levels |
| §7 threshold-gated EV: 0.500→+0.557, 0.667→+0.740, 0.750→+0.825, 0.833→+0.900 | **557, 740, 825, 900** (thousandths) |
| Wrong installs land where reliability says (10/20 at 50%, 0/20 at 99%) | confirmed at all 4 thresholds × 9 levels |
| S8: false confidence 100% → **0%**, all three paths | 0 fires on T1/T2/T3 (80 decisions each) |
| G2 no-reliability: 0 fires, every path | 0 fires on T1/T2/T3 |
| T3 ≡ T1: **880/880** verdict/chosen identical, no incremental value | 0 mismatches / 880 |
| T2: withhold on all 880 (conditional only off-corpus) | 880/880 withhold |
| T2 frontier: beat-withholding needs ρ>~0.20 at q=1.0, δ=0.25 | 1000·250/1250 = **200** (ρ>0.200); beat-T1 at r=0.9 → **840** |

### Round-3 sweep (420 envelopes × 3 arms; evidence hashes all OK)

| Committed claim | Observed (independent Zag) |
|---|---|
| Loose−conservative EV = 2r−1 at all 9 levels | −8,−4,0,+4,+8,+12,+16,+18,+20 (×20) = −0.40…+1.00; matches 2·round(20r)−20 at every level; C arm EV = 0 throughout |
| Crossover r* = **0.50** | **500** (thousandths, integer interpolation) |
| Licensed-EV row: 0.50→+0.557, 0.60→+0.650, 0.70→+0.740, 0.80→+0.825, 0.90→+0.900, 0.95→+0.950 | **557, 650, 740, 825, 900, 950** |
| Block R: loose vs conservative verdict-identical 180/180; per-level delta +0.00 | **180**; delta 0 at all 9 levels |
| S8 old rules: 20/20 converge, 10/20 wrong, 100% false confidence (C, D); B withholds | B: 0/0/0%; C: **20/10/100%**; D: **20/10/100%** |
| Self-estimation: estimators twin-identical | holds on G and G2 |
| Strict estimator (rhat_max) admits nothing | 0 admitted at t=0.30/0.50/0.70/0.90, G and G2 |
| Lenient estimator (rhat_all) all-or-nothing, value 0 | G: 20/20 admitted at t≤0.50; G2: 20/20 at t=0.30; admitted-set EV **0** everywhere |

## §2 Why not NOT REPRODUCED

No number differs. The tie guard works (the kill bar — 0/20 installs,
0/20 false-confidence emissions on the genuine 2v2 corpus — is met on
all three TP1 paths). T3 is null (880/880 identical, no non-null value).
No license term is contradicted or baseless.

## §3 Why not REPRODUCED — signed terms lacking direct measured basis

The frozen rule requires REPRODUCED ⟺ "every license term traces to a
measured result". The following signed operative terms of
`SOURCE_AUTHORITY_LICENSE.md` do not — most are honestly marked by the
license itself as derived, provisional, or governance (cited below),
but the Tier-1 bar is mechanical and they fail it:

1. **§1.1 — k/(k+1) thresholds for k = 2, 3, 5, 10** (0.667/0.750/0.833/
   0.909). Only k=1's crossover r*=0.50 was directly measured; the rest
   are derived from the EV formula ("validated by oracle-confirmed
   expectation"). License: §1.1 parenthetical; Annex A.4.
2. **§3.1.6 — lower one-sided 95% CI gate (strict >)**. Derived
   statistical law; the trials used stipulated r and never measured a
   CI gate. License: Annex A.4 ("derived law … not a measured trial
   result").
3. **§3.1.1 — n ≥ 20 scored predictions.** Statistical convention; no
   trial measured 20 as the minimum. (The 20/level corpus design is a
   design choice, not a measurement of the threshold.)
4. **§3.1.4 — no cross-type transfer (stratification).** Assumed; never
   tested across claim-types in any trial.
5. **§3.1.5 — 24-month recency default.** Explicitly PROVISIONAL, not
   measured. License: §3.1.5, Annex A.4.
6. **§2.1 — broad tie class** (n:n, weighted, multi-candidate ties).
   Only the literal 2v2 was measured; the license's own acceptance
   criterion requires adversarial coverage "until that bar is met, the
   tie guard is not deployable" — i.e. not yet met.
7. **§1.1 — k-table governance** (versioned human-governed table keyed
   by claim-type × consequence class; k frozen at intake; backdoor
   seal; disjoint maintenance). Policy design from the debate; no trial
   measured these mechanisms.
8. **§4.2 — the (ρ, q, δ) frontier.** Pure math; no second channel
   exists in any corpus (the verdict itself calls it parametric). My
   re-derivation confirms the arithmetic, not the empirics.
9. **§6.5 / §6.6 / §6.7 — skepticism exclusion, non-factual-install
   exclusion, untested-shape default.** Governance boundaries; the
   trials contained no skepticism claims, non-factual installs, or
   untested shapes to measure them on.

Terms WITH direct measured basis (confirmed above): T1's gated firing
rule and all its EVs; the 2v2 tie guard (100%→0%); G2 no-fire; T3's
880/880 null; T2's in-corpus withhold; corroborated +0.00; k=1
crossover r*=0.50; the sub-threshold destruction regime (−0.40 at
r=0.30, −0.20 at r=0.40); S8 old-rule failure mode; self-estimation
no-go.

## §4 Notes and caveats

- The per-level "2r−1" law holds in its discretized form
  round(20·(2r−1))/20 (corpus granularity ±0.025); at r=0.99 the
  observed EV is +1.00 vs 2r−1=0.98 — consistent with the verdict's
  "+1.00/case" prose. Not a discrepancy.
- Checkout-method disclosure: the clean checkout was built via
  `git init` + filtered fetch (not a literal final `git clone`) after
  two clone attempts failed; see RUNLOG.md §0. HEAD and all pins
  verified as commit objects.
- No binaries or `.zagd` files committed. The in-flight TP1 Zag oracle
  was not touched. All evidence used is committed.

## §5 Frozen pins

- TP1 prereg: `44afdbefc168edddcae50e9dd91eac12cd9fa156`
- TP1 result: `c85c9b41770c1878fb00a8dc991a5b4f17f8caaa`
- round-3 sweep: `b22ff31272d1789da4d35bf489d30d5e0d7c41f6`
- license: `3a3541ef62d05e929bdb47e4228e6e2b3a89fe02`
- scope (HEAD): `7b2100d09911c5c10252c5756c7def288e70bd1f`
