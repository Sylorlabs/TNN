# P6 / FORMAL-INDUCE — PREREG AMENDMENT 2

Status: frozen BEFORE any data was generated and before any learner code was
written. Disclosed. **No kill bar, prediction, threshold, seed, or criterion is
changed.** The amendment STRENGTHENS guard G2 and changes the packaging of the
supervision channel; the channel's content is exactly what PREREG section 6
specified.

## A1. THE DEFECT IN PREREG SECTION 1.3 G1/G2 PACKAGING

PREREG 1.3 G1 described the learner's translation unit as
`p6_learner.zag` + `p6_world.zag`, where `p6_world.zag` "emits the training
corpus and nothing else".

This is unimplementable as written. The world must decide which near-miss
edits are actually invalid, and deciding that requires the true checker.
Therefore either:

- the world links the checker, in which case **the checker code is inside the
  generating binary's address space** and guard G2 ("the generating binary has
  no checker code in it at all") is FALSE; or
- the world does not link the checker, in which case it cannot label anything.

The prereg asked for both at once. That was my error.

## A2. THE CORRECTION

The supervision channel becomes a **file**, not an in-process emitter.

Binaries (four, all pure Zag, all 3/3 byte-identical):

| binary | translation unit | role |
|---|---|---|
| `p6_gencorpus` | `p6_lang.zag` + `p6_ckcore.zag` + `p6_gencorpus.zag` | builds the stage corpus; writes `corpus_s<s>.txt`; also writes `truth_s<s>.txt` (the seed used) |
| `p6_train` | `p6_corpus.zag` + `p6_learner.zag` + `p6_train.zag` | reads the corpus file, induces, generates artifacts, writes `p6_out.txt` |
| `p6_check` | `p6_lang.zag` + `p6_ckcore.zag` + `p6_check.zag` | reads `p6_out.txt`, verifies against the true instance |
| `p6_stupid` | `p6_corpus.zag` + `p6_stupid.zag` | memorizer / random baselines; writes `p6_stupid_out.txt` |

Consequences, which are strictly stronger than the prereg:

- **G2 now holds literally.** The `p6_train` translation unit contains no
  checker function and no language-derivation function. The true instance
  does not exist in the generating binary. The learner cannot consult ground
  truth even by accident, and any ground-truth-conditional behaviour would
  have to come from the corpus file, which contains only token sequences and
  one bit each.
- **G1 now holds trivially and auditably.** `p6_learner.zag` + `p6_corpus.zag`
  + `p6_train.zag` contain no seed literal, no `lg_*` symbol, no `ck_*` symbol,
  no role code, no keyword subrole code, no type code. Verified by grep, listed
  in NAMECHECK.md.
- The learner's view of the world is a text file. This is also the more
  honest framing of "experience": the learner is not co-resident with the
  world simulator.

## A3. WHAT DID NOT CHANGE

Everything else. In particular the supervision channel content is exactly
PREREG section 6: 220 examples per stage, 130 VALID / 90 INVALID, INVALID
examples are single-token near misses, construction is deterministic from the
seed, and the learner receives only (token sequence, one bit). The corpus
files are committed as artifacts so that the exact experience set is auditable.
