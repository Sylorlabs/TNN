# L2L2 Repair Report: Mode 2 Causal Ablation

**Verdict: REPAIR-PASS.** P3 closed as specified. L2L2 may now be cited as
ablation-verified.

## What was done

Per audit `af9a9765a`, added mode 2 to an unfrozen copy of `l2l2.zag`
(`l2l2_repair.zag`). Mode 2 runs family B with A's retained hypothesis state
(`offset_hyp`, `trusted` copied from post-A) but `form_known` forced to 0.
Differs from mode 0 ONLY in `form_known_in` (0 vs 1).

Prereg amendment `0872a412d` committed before implementation.
`git merge-base --is-ancestor 0872a412d <impl>` verified below.

## Results (3/3 byte-identical, exit 0, zero stderr)

```
A ex=13
B ex=10
B_FRESH ex=13
B_ABL ex=13
TRACE offset_A=3 offset_B=7 form_known_after_A=1
P1=1 P2=1 P3=1 P3a=1
```

- P1 TRANSFER: PASS (10 < 13, diff 3 >= 2).
- P2 NO-PSEUDO-TRANSFER: PASS (13 >= 13).
- P3a ABLATION SLOWS: PASS. `B_ABL=13`, `|13-13|=0 <= 2`. Ablating `form_known`
  returns B to A speed.
- P3b SPECIFICITY: PASS by construction. Mode 2 differs from mode 0 only in
  `form_known_in`.
- Determinism: 3/3 byte-identical (SHA-256 `5530f0ac...cd72`).
- Governance: pure Zag, zero em dashes.

## Causal interpretation

The 3-example transfer (13 to 10) is causally attributable to `form_known=1`,
the retained knowledge that the offset form is viable. With `form_known=0`,
the learner must pay the 4-example memorization preamble (`fit_ok` requires
`used>=5`) before fitting the offset, returning to 13 examples.

The retained mem table is not causal: B overwrites it from index 0 (`mcnt`
is local), and the x-ranges are disjoint. The retained `offset_hyp=3` /
`trusted=1` are actively wrong for B (offset 7) and are discarded after one
example. Only `form_known` carries the transferable value.

## Classification

L2L2 remains bounded L1/L2 (the offset form is researcher-supplied; only the
constant and the form-viability flag are learned). The original BUILD-PASS
(5/5) verdict is not retroactively validated; this repair closes P3 and P4
prospectively under the amended prereg.

## Downstream correction

`l2l_analysis/L2L_ANALYSIS.md` lines 40-46 may now accurately cite L2L2 as
ablation-verified, referencing this repair (`L2L2_REPAIR.md`) rather than the
original misdescribed result.

## Files

- `l2l2_repair.zag`: unfrozen variant with mode 2
- `l2l2_repair_bin`: built binary
- `L2L2_REPAIR_RUN1.txt`, `L2L2_REPAIR_RUN2.txt`, `L2L2_REPAIR_RUN3.txt`
- `L2L2_PREREG_AMENDMENT.md`: frozen before implementation (commit `0872a412d`)
