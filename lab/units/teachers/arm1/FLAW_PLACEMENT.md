# Flaw Placement Map — FROZEN (parent-wired)

**Status: FROZEN — wired by the parent (Muse) on 2026-09-21.** The placement function below
is unchanged from the draft; only its status is frozen. Deterministic placement of the 12
flaws per slice: no RNG anywhere. Placement is a pure function `f(slice_hash, flaw_index)`;
the resulting positions are tabulated per slice for auditability.

## f — the placement function (normative)

```
slice_hash = SHA-256(b"TNN-TRACKB-ARM1-SLICE-v1|" || corpus_id || b"|" || slice_id
                     || b"|" || ASCII(corpus_start))      # 32 bytes, hex in manifest
u[j] = LE64(slice_hash[8*j .. 8*j+8])                        # j = 0..11

elig(S) = positive-judgment, non-ambiguous vocab entries with >= 2 in-slice occurrences,
          sorted by chunk_id; each used at most once per slice (linear probe on collision).
wrong-span (j=0..3):      pick elig[u[j] % len]; oi=(u[j]>>32) % occ; shift true span by
                          m=1+(u[j]>>40)%3 bytes, sign=(u[j]>>63)&1 ? +1 : -1 (flip if OOB);
                          grounds = next 2 true occurrences.
false-confidence (j=4..7): pick elig; span = true span; conf = 255; grounds = none (even j)
                          or 2 occurrences of a *different* eligible entry (odd j).
missing-grounding (j=8..9): pick elig; span = true span; conf = CONF(J,0); grounds = none.
plausible-false (j=10..11): letter-only fragment (3-8 bytes) near a true occurrence,
                          not equal to any true span or prior flaw span; conf = CONF(J,1).
```

Reference implementation: `gen_draft_reference.py :: gen_flaws()` (deterministic,
stdlib-only). The frozen manifest tabulates the resulting spans (slice-relative).

