# D3 — CON post-result update: WRAPS signed

**Verdict: CON concedes.** The appeal battery returned the NULL reading on
every regime, with 2× byte-identical reruns and 0 scorer cross-check errors,
exactly the falsifier D1 published before results. The frozen mechanical
rule (§6) yields WRAPS. No RECOVERY fired. We sign.

## 1. Falsifier walk-through

| Test | D1 NULL reading | Measured | Verdict |
|---|---|---|---|
| R1 (L0–L6 sweep) | bits ≤ 0.15 all levels, both senses; no fooled/correct separation | Max pooled 0.0296 (L4); max per-sense 0.0541 (L3, A). Curves flat; L5–L6 collapse to ~0.000 bits (near-universal WITHHOLD) | **Concede** |
| R2 (N=5 majority) | bits ≤ 0.15 both configs, both senses | L3: 0.0173; L5: 0.0000 pooled (near-constant function) | **Concede** |
| R3 (alt transforms) | bits ≤ 0.15 every valid cell, i.e. identity holds or F3-void | All valid cells: J(T(x))==L(J(x)) everywhere → 0.0000 bits (A/vflip, A/signflip, B/signflip). fshift legibility-void both senses; vflip void on B — excluded per frozen rule | **Concede** |
| R4 (structured noise) | bits ≤ 0.15 both variants, both senses | V1: 0.0102; V2: 0.0167 pooled | **Concede** |

Every false-install sat ≥ 0.267 against a bar requiring < 0.15 (lowest: R3 signflip 0.283,
bits 0.0000). 14/14 members
NULL; the strongest single reading (R1-L4, 0.0296 pooled) sits 5× below the
bar. The NULL is not marginal — it is decisive.

## 2. Recovery mechanisms: all four refuted

- **R1 boundary-distance separation** — refuted. Agreement curves show no
  fooled-vs-correct separation at any of 7 amplitudes; C3's single point was
  representative of the whole curve, not an underdetermined one.
- **R2 majority amplification** — refuted. The 4–5pt agreement gap in the
  measured direction did not amplify; L5 majority votes to bits = 0.0000,
  exactly as PRO's mechanics predicted.
- **R3 DPI-identity-breaking** — refuted. The J(T(x))==L(J(x)) identity holds
  on every transform where the judge stayed legible. DPI death is not
  family-specific; it is deterministic-re-reading-specific.
- **R4 noise-distribution artifact** — refuted. Block-correlated and ternary
  noise return the same NULL. The null is not a noise-choice artifact.

None survives even in weakened form. There is no residual reading (no
near-miss, no rising tail) pointing to an unprobed notch — the highest bit
counts are 3–5× under the bar with false-installs 3× over it.

## 3. Signature and remaining demands

CON **signs WRAPS for the frozen threat model** per the frozen §6 rule.

D1's "Why G1 alone does not satisfy us" — status after measurement:

1. **Exhaustion must rest on an explored space, not a point.** MET.
   7 amplitudes × 2 majority configs × a new transform family × 2 structured
   noise variants — "measured exhaustion" is now a claim over an explored
   space, as D1 demanded.
2. **DPI generality must be tested, not assumed.** MET. R3 extended the
   identity to alternative transforms wherever F3 legibility held.
3. **No silent re-widening.** STANDS AS GOVERNANCE. This is no longer an
   evidence demand — it is a rule: any "permanent" language beyond the frozen
   construction needs a new preregistered battery (G1), and any C* reopening
   applies member-by-member. We sign WRAPS *for this threat model* — the
   retirement inherits nothing elsewhere.

The family is dead, not parked. Sol's pre-result prediction held in full.
