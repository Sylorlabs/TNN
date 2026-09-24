# Fork W No-RNG Certification — 2026-09-24

## Certification

The Fork W witness mechanism contains **zero randomness in decision paths**.

## Evidence

1. **Source audit**: `grep -ri "rand\|rng\|random\|seed"` over all `*.zag` sources returns no RNG calls, seeds, or random number generation. The only match is a print statement: `"NORNG deterministic: no RNG in decision paths; byte-identical rerun required"`.

2. **Byte-identical reruns**: Three complete runs produce byte-identical stdout:
   - run1.txt: `eff00337cadc3528a8b1fe85b53cc8892efe38eb0c4f233fd65b7426837fe407`
   - run2.txt: `eff00337cadc3528a8b1fe85b53cc8892efe38eb0c4f233fd65b7426837fe407`
   - run3.txt: `eff00337cadc3528a8b1fe85b53cc8892efe38eb0c4f233fd65b7426837fe407`

3. **Deterministic mechanisms**:
   - String interning uses sequential pool allocation (no hash randomization)
   - Canonicalization applies fixed rewrite rules in fixed order
   - Verification follows the frozen prereg decision tree with no tie-breaking randomness
   - Ledger uses SHA-256 (deterministic) for hash chaining
   - All loops iterate in fixture/atom/step index order

## Scope

This certification covers the witness decision paths (verification, deliberation, verdict aggregation, scoring). Python was used only for generation (`gen_fixtures.py`, `mk_layout.py`), glue, and analysis — not in the Zag decision paths.
