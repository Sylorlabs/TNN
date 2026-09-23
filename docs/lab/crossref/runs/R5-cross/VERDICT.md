# R5-CROSS Verdict — Independent cross-check of the KB4 autopsy (Type C)

**Verdict: NOT REPRODUCED** (mechanical, per the frozen R5 decision rule)

Observed 2026-09-23. Independent Zag verifier (`r5cross.zag`, ~1,380 lines, zero RNG,
pure-Zag reasoning, Python glue only) re-derived every probe number from committed
evidence. Three runs, byte-identical.

## Frozen pins (verified in fresh clone before official runs)

- Prereg: `7b2100d09911c5c10252c5756c7def288e70bd1f`
- Autopsy evidence: `66fbb329aa831c14f3f3100a20e177bbb12e27b1`
  ("KB4 autopsy — bad learning or bad architecture? (Micah's question)")
- WHY_REPORT evidence: `bc6d130539e4a5539ea3361f57e02e39378f26ba`
  (tree `3b2081d3bcf0833cf4b7bb0e065d47a78ae9956b`, blob `bd12da7161fa30b9d24d17d4cf7744f90eb493c6`)
- Toolchain: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
  `znc 2026.07.0-dev (edition 2026)`

## What reproduced exactly (committed = derived, all 9 probe outputs)

Original KB4 gate:

| Leg | Adversarial fixtures | Installs | False | True | False-install rate |
|---|---:|---:|---:|---:|---:|
| A | 184 | 80 | 33 | 47 | 41.25% |
| B | 185 | 99 | 46 | 53 | 46.4646% |

A is DEGENERATE, B is FAIL. Join integrity: 0 misaligned fields on both legs.

L8 removed (P-L1): A 80/33/47 @41.25%, 0 flips; B 93/41/52 @44.086%, 6 flips, 0 M2 flips.
L4 removed (P-L2): A 184/93/91 @50.543%; B 185/101/84 @54.595%.
P-A2: line-identical to P-L2 (A 924/924, B 925/925); binding trade 60/44 (1.36:1) A,
55/31 (1.77:1) B.
P-A1 cross-sense: 184 common adversarial fixtures, 115 installs (50 false, 65 true)
@43.478%; 50 both-wrong-and-agreeing, all 50 install.
Match/differ contingency reproduced exactly (A: match 47/33, differ 44/60;
B: match 52/41, differ 32/60).
MI(match-bit; adv-correct) = 0.019265 bits (A), 0.032740 bits (B).
Confidence means (×10, rounded): A 4298 correct / 4391 wrong; B 8494 correct /
8613 wrong — wrong ≥ correct on both legs (anti-informative).
Impossibility over the gate's operational observable (match-bit): max true installs
at ≤15% false-install rate = 0/420 (A), 0/541 (B); oracle-partition minimum rates
28.4% (A), 42.2% (B). All coefficients positive, so the ≤15% bar forces zero
installs, violating the ≥50 true-install anti-degeneracy bar.
All seven falsifiers hold.

## What did NOT reproduce — the three numeric claims (mechanical reason)

The frozen prereg R5 prose makes three numeric claims the frozen evidence contradicts.
The WHY_REPORT itself corrects the record; my independent code confirms the corrected
numbers, not the prereg prose:

1. **Binding trade "1:1"** — derived: A 60 false installs per 44 recovered truths
   (1.36:1), B 55 per 31 (1.77:1). Total errors +16 (A), +24 (B). The 1:1 claim is false.
2. **"50 of 185 paired fixtures"** — derived: 184 common adversarial fixtures, not 185
   (B alone has 185; the A∩B common set is 184). 50 both-wrong-and-agreeing of 184.
3. **"The original gate is already Bayes-optimal"** — the *policy form* (install iff
   match) is the unique accuracy maximizer on both legs (A: 107/184 = 58.15% = ceiling;
   B: 112/185 = 60.54% = ceiling). But the *implemented B gate* deviates from it 6
   times (history/L8 re-challenges): 108/185 = 58.38% < 60.54% ceiling. The blanket
   claim does not hold for the implemented B gate. On A the gate is exactly optimal
   (0 deviations).

Per the frozen rule — REPRODUCED only if numbers, Bayes result, impossibility, and
attribution all hold; NOT REPRODUCED on any number mismatch — the verdict is
**NOT REPRODUCED**. PARTIAL is unavailable (requires all numbers to match; they do not).

## Attribution assessment

The core causal attribution **survives** all seven falsifiers and is the supported
verdict: **architecture primary, learning secondary/complicit**.

- Architecture primary: observational identity / information starvation (MI ≈ 0.02–0.03
  bits), wrong perturbation binding (1.36:1 / 1.77:1, not 1:1), correlated-channel
  failure (50 common fixtures fool both senses while agreeing, all install), no
  independent causal anchor.
- Learning secondary/complicit: L4 models "sense wrong" rather than "world changed";
  L8 is a narrow B-only rejected-judgment attractor (0 A flips, 6 B flips, none M2);
  confidence is anti-informative. Correction retained: L8 did not cause M2 decisions —
  M2 installs were sealed before L8.

## Caveats

- P3 (finest-observable impossibility) is reported as **informational only**: the
  full-observation simplex admits a memorizing lookup-table policy on the frozen set,
  so the impossibility holds over the gate's *operational* observable (match-bit),
  which is what the WHY's W5 / autopsy S6 claim states. No hole in the proof as stated.
- The /tmp scratch violation during development (see RUNLOG.md) was removed and did
  not touch evidence or results.
- Prereg prose rates (41.2%/44.1%, 50.5%/54.6%, 43.5%) all reproduce; only the three
  claims above fail.

## Determinism

Build: pinned znc, one binary. Three official runs, SHA-256
`6713f286a9518bad759728fa9fa0b05cb9ec8f1b2370a45b0536794c6e621922` for all three,
`cmp`-identical. Binary and build cache removed after the runs.
