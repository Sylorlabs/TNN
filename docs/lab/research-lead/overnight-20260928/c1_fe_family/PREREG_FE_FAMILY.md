# PREREG: C1 F-E Family (periodic-demo key ambiguity confirmer)

Status: FROZEN. Committed alone before any implementation.

## Hypothesis under test

The D3 miss from the C1 law-revert attack (6a329511b, REVERT-ATTACK-SURVIVES)
was caused specifically by the rotation class's largest-match-k tie-break
interacting with a periodic demo: the word "lblb" has period 2, admitting
rotation keys k=1 AND k=3. The rotation class takes the LARGEST matching k
per demo (k=3 for the periodic demo, k=1 for the normal demo), producing
inconsistency and collapsing the entire rotation class to fallback, even
though k=1 is consistent with both demos.

A smallest-consistent-k rule would have fired k=1 and hit. This family
tests whether the failure reproduces systematically when the periodic-demo
condition is constructed by design.

## Family F-E design (sealed generator)

Structure mirrors F-A (exact revert) for comparability, with one
structural change in the post-change demo regime:

1. Setup: 3 demos of pa under reversal (as in F-A).
2. Setup: 3 demos of pb under kold, where kold is drawn from {2,3} (never 1).
3. Law change: kold -> k2, where k2 = 1 (fixed by design, not drawn).
4. Post-change demos (2): demo 1 is a PERIOD-2 word [a,b,a,b] with output
   rot([a,b,a,b],1) = [b,a,b,a]; demo 2 is a normal aperiodic word with
   output rot(word,1). The period-2 demo admits keys {1,3}; the rotation
   class takes the largest (3). The normal demo admits {1}. 3 != 1, so the
   rotation class collapses by construction.
5. R1 query: rotation query under k2=1 (word drawn from 110-122, demos from
   97-109, so query chars are unmapped and the char-map class cannot fire).
6. Law change (revert): k2 -> kold. 2 demos under kold (normal words).
7. R2 query: rotation under kold. R3 query: pa reversal (retention control).

RNG: xorshift64 seeded from the 8-byte seed file, mixed with worldidx, as in
the attack wave. 8 worlds, seeds from /dev/urandom AFTER the freeze commit,
hashes recorded, values never viewed. Each world generated twice,
byte-identical (turns.jsonl + key.json).

## Preregistered predictions

- P-FE1 (primary): R1 miss rate >= 20/24 runs (8 worlds x 3 reps). Baseline
  for comparison: F-A R1 miss rate was 0/24. The predicted misses are
  fallback-collapse misses caused by rotation-class inconsistency.
- P-FE2 (location): every R1 miss is located at APPLICATION by D3 (diag's
  independent cascade predicts the contestant's exact wrong answer), with
  zero UNCLASSIFIED. Detection (D1) and diagnosis (D2) remain clean.
- P-FE3 (controls): R2 hits 24/24, R3 hits 24/24. The revert path and the
  pa retention control are unaffected by the periodic-demo construction.

## Kill bars

- K1 ORDERING: this prereg strictly precedes the freeze; the freeze strictly
  precedes world generation (seeds drawn post-freeze). Verifiable from the
  commit graph.
- K2 COVERAGE: 8 worlds x 3 reps = 24 runs, all executed; per-world replies,
  scores, and state byte-identical across reps; results recorded honestly
  against P-FE1/P-FE2/P-FE3.
- K3 PURITY: pure Zag end to end (generator, contestant, diag, agg are
  znc-compiled binaries; bash only sequences processes). Zero Python.
  No em dashes (shell-only check_no_dash.sh). Contaminated paper untouched.
  New Zag code uses u8-backed cells with the st32/ld32 little-endian idiom
  (no as *i32 slice construction, per the 2026-09-30 toolchain lesson).

## Interpretation

- If P-FE1 holds (>= 20/24 R1 misses): the periodic-demo key ambiguity
  hypothesis is CONFIRMED as a systematic failure mode. The recommended
  follow-on is a revision experiment swapping the tie-break to
  smallest-consistent-k, preregistered before implementation.
- If P-FE1 fails (< 20/24 R1 misses): the hypothesis is REFUTED; the D3 miss
  was an idiosyncratic world, not a systematic mode. Report honestly.
