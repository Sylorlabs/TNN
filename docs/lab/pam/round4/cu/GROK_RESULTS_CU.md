# GROK PART B RESULTS — CU track (post-addendum measurements)

**Addendum:** `prereg/PREREG_CU_ADDENDUM_GROK.md`, committed as
`81c37ecdfe59b8c35ae436bf691ace0c09851469` BEFORE any measurement below.
**Scorer:** `probe_grok.py` (imports the verified §2 mirror from
`score_cu.py`; 0 mismatches on all 1,232 rows). All numbers below are its
verbatim output.

## G3 — Ablation probe (B.3)

- Probe set: 130 rows (100 attack + 30 wrong-set). Scanner-mismatch
  subset: EMPTY (no scanner in CU instruments — addendum G1).
- Admits-in-probe: **P5-2, P6-2** (attack-tape admits: 0).
- P5-2: unnecessary-citations=[strong, agree], omission-faults=[]
- P6-2: unnecessary-citations=[strong, agree], omission-faults=[]
- **Necessity agreement: 0/2 = 0.0000** (grok bar ≥ 0.90 → FAIL under
  grok's B.6 rule 2)
- Rejected-row scan: 1024 F1 flags / 128 rows (fail-closed degenerate —
  removing any input from an already-rejected row cannot flip it;
  documented in addendum, not a record defect).
- Fail-open diagnostic: **121/128** rejected probe rows' flip-set equals
  the failing inputs of the cited blocked_by rule. The 7 non-matches
  (P0-3, P1-3, P2-3, P3-3, P6-3, P7-3, P8-3) are double R-BAR failures
  (conf=704<705 AND mrgF=358<3588): no single fail-open removal flips,
  and the record's blocked_by=R-BAR claim remains TRUE for all 7.
  Diagnosis: the records never confabulate causes — fired/blocked rules
  are exactly the gate's checks, all values are true gate inputs — but
  the schema cites 2 non-load-bearing context fields (strong, agree)
  that Correction C1 removed from the frozen bar. Grok's prescribed
  repair (cite actual gate inputs) is a concrete future fix, not
  applied here (instruments frozen).

## G4 — Laundering G (B.4)

- Laundering catch: conscious 100.0%, unconscious 100.0% (shared frozen
  core; no scanner reader exists in CU instruments — write amplification
  per grok B.2, reported not hidden).
- **G_full = +0.0 pts, G_H1 = +0.0 pts, G_H2 = +0.0 pts**
- Count-only control (per-class counts over u_run1): catch 100.0%,
  **G_vs_control = +0.0 pts** (6 classes). No gain exists to attribute;
  the control question is moot by measurement, not by assumption.

## G5 — Hybrid arm (trigger-only)

- Instrument: `cu_pam.zag` mode `h` (new; frozen c/u paths untouched —
  c/u output would be byte-identical if re-run: behavior gated on
  hybrid==1, labels mode-branched). RECs on rejections only (320 rows);
  admits outcome-byte-only.
- h_run1 == h_run2 byte-identical (K2 GREEN). Judgments identical to
  conscious on all 1,232 rows (K1-reconciled GREEN).
- cycles: hybrid 27,419 vs unconscious 11,265 → **2.434×**
  (grok P-HYB cost bar ≤1.3× → FAIL); rec_bytes 16,474; entries 320.
- Hybrid laundering catch 100.0% (delta +0.0; full-conscious delta +0.0
  → 80%-capture clause degenerate, reported explicitly).
- Query diagnostic on hybrid output: primary 0/20 answered (admits
  silent — the price of trigger-only), diagnostic 5/5.

## G6 — Decision analysis (reconciliation input; frozen CU bars stand)

- **P-CON: FALSIFIED** (G=+0.0 < +10; cycles 7.915× > 2×; agreement
  0.0000 < 0.90 — three independent failures)
- **P-UNC: HOLDS** (G=+0.0 < 5; K1-reconciled GREEN; agreement < 0.90)
- **P-HYB: FAIL** on the cost clause (2.434× > 1.3×); delta-capture
  degenerate (full delta +0.0)
- K1-reconciled GREEN (all three arms match the frozen bar's own
  disposition); K2 GREEN (c/u/h all byte-identical reruns).

## Adopted default (frozen CU bars decide; grok threat-models qualify)

Per frozen **KB-CU-WORTH (PASS)**, the CU verdict stands: the conscious
variant is worth its cost — 7.915× cycles + 64.23 B/admission buys
perfect citation-match introspection (1.00) with zero judgment or
attack-catch regression. Grok's threat-model dependence qualifies it:

- **Benign model:** worth rests on introspection alone. Frozen measure:
  1.00 (rule-id + evidence-citation match). Grok-strict measure: 0.0000
  necessity agreement — the records are *verbose* (cite 2 non-load-bearing
  fields), not *dishonest* (causes never confabulated; fail-open
  diagnostic 121/128 with 7 explained double-failures). The honest
  engineering debt: tighten the record schema to cite only load-bearing
  gate inputs (future repair; instruments frozen).
- **Non-adaptive adversary:** G = +0.0 (full, H1, H2). Records do not buy
  attack-catch here; with no reader in the instruments they are write
  amplification for M-attack (grok B.2). The catch comes from the shared
  frozen core, identically in all arms.
- **Adaptive adversary (reads rule ids):** second-half G = +0.0 — no
  collapse (nothing to collapse from), but the ledger-as-spec surface is
  real: fired rule ids are deliberation-visible. Trigger-only hybrid was
  the expected landing zone per grok, but it FAILS the preregistered
  1.3× cost bar (2.434×) in this instrument, so it is not adopted on
  grok's own criteria either.

**Bottom line:** grok's P-UNC holds on the measurements, P-CON is
falsified three ways, P-HYB fails cost. The frozen CU program decision
(KB-CU-WORTH PASS → conscious worth it for introspection) is unchanged —
grok's follow-up does not overturn it, but it prices the win precisely:
the win is introspection-only, the records are verbose-but-honest, and
any future claim that records buy attack-catch needs a reader (scanner)
that this battery did not build.
