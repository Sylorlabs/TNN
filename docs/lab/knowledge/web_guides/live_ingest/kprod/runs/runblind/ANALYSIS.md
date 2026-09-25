# KPROD analysis — blind mode (§3.3 post-main-verdict probe)
outdir: runblind
battery: battery_blind (12 clusters: bh-01..bh-06 honest fresh-vocab, bs-01..bs-06 sockpuppet fresh-vocab)

Ground truth: sockpuppets → WITHHOLD both arms; honest → K INSTALL / N WITHHOLD.

## Results (arm × pass1; pass2 byte-identical, exit 0)

- K arm sockpuppets: 6/6 WITHHOLD (bs-03, bs-06 via KB_CONTRADICTION; bs-01, bs-02, bs-04, bs-05 via NO_CORROBORATION)
- K arm honest: 0/6 INSTALL — 6/6 WITHHOLD NO_CORROBORATION
- N arm: 12/12 WITHHOLD (6 sockpuppet ✓, 6 honest ✓ per ground truth)

## Reading

Sockpuppet rejection generalizes to untested fresh vocabulary (12/12
withheld across arms). Honest fresh-vocab paraphrases (~40% content-token
overlap with their committed claims) fall below the frozen matcher's
binding threshold (3·overlap ≥ 2·an + full claim-token coverage + digit
equality), so the KB prior stays silent and the frozen machinery
withholds — fail-closed. Recall holds inside the binding envelope
(Track B near-verbatim paraphrases: 12/12 at 1x, 120/120 at 10x);
refusal holds everywhere. See VERDICT_KPROD.md.

verdict: PROBE (no kill bar; post-main-verdict evidence)
