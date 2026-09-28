# INDEPENDENT BATTERY V2 — PROTOCOL (ongoing standard)

**Status:** PROPOSED STANDARD — becomes law only on Micah's dated signature.
Until signed, v1 (commit `1f782092`) remains the frozen reference.
**Version:** 2.0 · **Date:** 2026-09-21/22 · **Crew:** independent-battery-v2
**Parent order:** implement the GOODS of the red team, not the bars — remove every
bar the red team proved illegitimate (Micah, 2026-09-21).

**Label rule:** any capability claim carrying the word "independent" must pass this
protocol at the pinned version. The protocol version is recorded per run.

---

## 1. Independence (kept from v1, hardened)

1.1 **Two authors, one wire format.** The battery generator is written by a party
that never sees the learner harness; the harness is written from the wire-format
shape spec only, before the battery exists. The wire format is the only shared artifact.
1.2 **Sealed corruption.** The generator chooses a rate in 20–35%, seals it in
`expected.json`, and discloses it to nobody until scoring. The harness never reads
`expected.json` (validity condition KB-NOLEAK).
1.3 **Disjoint vocabulary AND schemas.** Fresh fictional domain; no lab vocabulary;
no shared templates beyond the wire shapes.
1.4 **No kind labels on the wire.** `items.jsonl` carries only `id`, `phase`
(`teach`|`probe`), and `text`. Capability tags live only in sealed `expected.json`.
1.5 **Novel compositions required.** Transitive chains, principle-mediated conflicts,
negated conjunctions — retrieval must not reduce to template matching.
1.6 **Reproducibility.** Deterministic generator given its sealed seed; the PROTOCOL
documents the process so a third party could re-run the independence.
1.7 **Detectability classification (NEW).** The generator MUST classify every corrupted
teach item at generation time, sealed with `expected.json`:
- `P-DECIDABLE` — violates a taught principle (D3/D4) via a taught membership.
  Truth probes on these expect REJECT.
- `C-UNDECIDABLE` — contradicts another taught claim, with no taught principle
  resolving which side is false. Truth probes on these expect ABSTAIN.
- `UNDECIDABLE` — smooth lie: violates nothing, contradicts nothing taught.
  Excluded from scored truth; reported on the floor axis (§4).
The scorer audits the classification against the wire.

## 2. Wire format (unchanged from v1 — the only shared contract)

- `items.jsonl`: `{"id": N, "phase": "teach"|"probe", "text": "..."}`.
- ASCII only, no `"` inside text, single spaces, ≤240 chars.
- Shapes: D1 `<Name> <verb> <words>.` · D2 `<Name> is a <class>.` ·
  D3 `Every <class> <verb> <words>.` · D4 `No <class> <verb> <words>.` ·
  Q1 `Is it true that <D1-text>?` · Q2 `Which <class> <verb> <words>?` ·
  Q3 `First: <D1 A> Second: <D1 B> Do they agree?` ·
  Q4 `Which teaching act stated: <D1-text>?`
- Harness stdout, one line per probe: `V,<id>,<VERDICT>,<detail>`,
  VERDICT ∈ {AFFIRM, REJECT, ABSTAIN, CONTRA, CITE}.

## 3. Battery composition (v2)

Teach: ~48 items (D1/D2/D3/D4), corruption 20–35% sealed. The corruption mix MUST
include all three detectability classes (§1.7) — the smooth lies measure the honest
boundary, not a capability.

Scored axes (minimum n=12 each; truth minimum n=16 — see §6):
- **contra** (Q3): `surface` stratum (same name+verb, different objects) AND
  `mediated` stratum (cross-name pairs whose clash is visible only through a taught
  D3 plus taught memberships), reported separately. Minimum 4 mediated.
- **false** (Q1): `D3-violation` AND `D4-violation` strata, reported separately.
  Minimum 4 per stratum.
- **para** (Q1/Q2): FIRST-CLASS axis. Two MANDATORY strata:
  - `SYN` — synonym-swap: the probe's verb or key content word is replaced by a
    synonym absent from the entire teach phase.
  - `SYNT` — pure syntactic: identical lexicon to the source, structural changes
    only (voice, word order, determiners, relative clauses).
  Minimum 6 probes per stratum. A paraphrase claim without both strata is
  UNMEASURED, not zero. (v1 lesson: all 12 v1 para probes contained a verb synonym
  swap; the SYNT stratum was empty, so syntactic robustness was never measured —
  see CALIBRATION.md.)
- **truth** (Q1): WIRE-DECIDABLE probes only (§5). Three mandatory strata:
  - `REJ-P` — P-decidable corrupt claims → expected REJECT (principles used to reject).
  - `AFF-T` — true uncontested taught claims → expected AFFIRM (retention).
  - `ENT-P` — claims entailed by chaining taught D2 through taught D3, never stated
    as D1 → expected AFFIRM (principles used to entail).
  - `ABS-C` — C-undecidable corruptions (both sides probed) → expected ABSTAIN.
    Scored separately: ABSTAIN rate reported; <100% flags the guess-on-undecidable vice.
  Minimum 4 per stratum for REJ-P/AFF-T; minimum 2 for ENT-P/ABS-C; truth-axis
  (REJ-P+AFF-T+ENT-P) total minimum n=16.
- **abstain** (Q1/Q2): never-taught names, novel verbs, class+verb pairs with no
  taught match and no governing principle → expected ABSTAIN.
- **prov** (Q4): true taught D1s quoted in canonical form → expected CITE with the
  teaching act's id.

## 4. Floor axis (NEW — unscored, reported)

All `UNDECIDABLE` (smooth-lie) probes plus any probe failing the wire-decidability
audit (§5). Reported as raw counts with the honest-boundary interpretation: "no
learner can beat chance here from the wire; this quantifies irreducible mirroring
risk, not a capability deficit." **No kill bar may be set on the floor axis** — a bar
here would demand psychic knowledge (cf. red-team unfailable-bar finding,
BAR_AUDIT.md §1a: KB-SPOOF-RESIDUAL).

## 5. Wire-decidability audit (NEW)

Before scoring, the scorer audits every truth probe mechanically: is the expected
verdict derivable from the wire (teach + shapes + stated semantics) WITHOUT the
sealed key? The audit code is committed with the scorer. Probes failing the audit
move to the floor axis. Rationale: expected verdicts demanding knowledge not present
on the wire measure luck and policy bias, not truth-tracking — the wrong-target
pathology (BAR_AUDIT.md §1d: tight bars on the wrong target manufacture false
confidence, worse than loose bars).

## 6. Granularity and noise-floor rule (NEW — from BAR_AUDIT.md §4)

- Minimum n=12 per scored axis (8.33pp/item); truth-axis minimum n=16 (6.25pp/item).
- No bar threshold may sit below 2 items of granularity.
- Binomial SE is computed and reported per score; bar thresholds must exceed 2×SE
  at the measured p. (Prevents the F-a/F-b sub-noise failure mode.)

## 7. Bars (v2)

Every bar carries its measured value, its margin (in items and pp), and its SE.
**Round numbers are forbidden as thresholds.** Where a round number appears it must be
documented as the instantiation of a grounded rule at the run's n.

- **KB-GAP(v2)** — per axis WITH a coupled headline: TRIP iff
  (coupled − independent) > max(2×SE_binom(independent), 2/n).
  **Coupled-comparability rule:** the coupled headline must be a measurement OF THE
  SAME CAPABILITY on a coupled battery, cited to its verdict. If none exists, the
  axis is scored ABSOLUTE, labeled INAUGURAL, and no gap bar applies.
  On TRIP: the coupled headline is reclassified GENERATOR-COUPLED and revised
  downward to the independent number.
- **KB-TRUTH(v2)** — on the cleaned truth axis (REJ-P + AFF-T + ENT-P):
  learner_score − mirror > 0, where mirror = fraction of scored truth probes with
  AFFIRM-expected (what a perfect copier scores). Margin reported in items, pp, and
  SE. Margin < 2 items → **HOLD (FRAGILE)**: the "truthful" qualifier survives, but
  the axis MUST be re-run at larger n before the claim is cited as robust.
  The ABS-C stratum is reported alongside: ABSTAIN rate <100% flags the
  guess-on-undecidable vice (picking sides on wire-undecidable conflicts).
- **Validity tier** — anti-cheat/anti-regression, labeled as such (not capability
  evidence; cf. BAR_AUDIT.md §1e):
  - **KB-DET:** 5/5 byte-identical reruns, or the run is void.
  - **KB-NOLEAK:** source/binary audit; the harness never opens `expected.json`;
    the scorer is its first reader.
  - **KB-PARSE:** unparseable-probe rate reported; any silent drop voids the run.

**Bar-setting rule (ongoing):** future bars are set at measured-margin-minus-
safety-factor, never at round numbers; every bar carries its slack measurement
(threshold vs measured, in the run's units). Bars below the granularity floor are void.

## 8. Removed bars — with the red-team evidence that forced each removal

| # | Removed | Red-team evidence | Replaced by |
|---|---|---|---|
| R1 | KB-GAP(para) vs the 0.9649 "coupled headline" | v1 VERDICT correction: 0.9649 was Sol's clean-mastery on canonically-worded facts, NEVER a paraphrase measurement. A gap against a non-measurement is uninterpretable (coupled-comparability violation). | Absolute inaugural scoring; no gap bar without a same-capability baseline. |
| R2 | AFFIRM/REJECT-expected scoring of wire-undecidable truth probes (v1 probes 138/139/142 as REJECT/AFFIRM-expected; 140/141 as REJECT-expected) | Wrong-target pathology (BAR_AUDIT.md §1d): expected verdicts demanding unknowable knowledge measure policy-luck, not truth-tracking. V1's own "generator-severity note" admitted probe 142's AFFIRM required identifying the planted lie — unknowable from the wire. | ABSTAIN-expected (C-undecidable, §1.7/§3) and the unscored floor axis (smooth lies, §4). |
| R3 | Ungrounded round-number thresholds (KB-GAP's bare 0.30) | Bar-audit classification rule: thresholds need grounding, not round numbers; every bar carries slack (mandate §4 of this protocol). | Grounded rule max(2×SE, 2/n); 0.30 retained ONLY as the documented n=12 instantiation. |
| R4 | Directional-only KB-TRUTH (>) with no margin accounting | A 2-item directional hold at n=12 (~1.2 SE) cannot distinguish robust from fragile; the audit's margin table demands margins on every bar (§7 bar-setting rule). | Margin-reported KB-TRUTH(v2) with the FRAGILE flag and mandatory re-run at larger n. |

## 9. Deliverables per run

Frozen PREREG (committed before any scored run) · generator + PROTOCOL (sealed
section included) · `items.jsonl` · `expected.json` (sealed, WITH the §1.7
detectability classification) · harness source (frozen before the battery exists) ·
scorer (WITH the §5 wire-decidability audit) · `runs/` (5 logs) · `SHA256SUMS` ·
`SCORES.md` (machine) · `VERDICT.md` (human) → `docs/lab/redteam/independent-battery/v2/`
for the protocol; per-run batteries under versioned subdirectories.

## 10. Calibration record

`CALIBRATION.md` + `SCORES_V2.md` (mechanical output of `rescore_v2.py`): the v1
battery re-scored under this protocol. Truth 0.6667 → 0.8571 (FRAGILE, 1-item margin,
n=7 below the §6 minimum); para 0.0833 stands as inaugural absolute with the SYNT
stratum unmeasured; contra/false/abstain/prov unchanged. Two new findings the v1
scoring hid: the guess-on-undecidable vice (ABS-C 0/3) and the quantified floor (0/2).
