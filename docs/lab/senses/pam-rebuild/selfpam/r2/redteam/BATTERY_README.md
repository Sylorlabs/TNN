# H6 revival round 2 — blind red-team attack battery

Frozen under ATTACK_PREREG.md (committed alone) + AMENDMENT_01.md (committed alone).
All programs are pure Zag, zero RNG, pinned toolchain
`znc_linux_x86_64_abed8aa1` with `--no-zagd --no-analyze --no-foreground-cache`.

## Layout

- `src/rt_common.zag` — shared library: allocator helpers, LE byte-arenas,
  syscall file IO, string/line/field/FNV helpers.
- `src/build_para.zag` — deterministic paraphrase/avalanche generator.
  Inputs: `battery/rules.tsv`, `battery/bases.tsv`.
  Outputs: `pairs_sm.tsv` (150), `pairs_ss.tsv` (150), `pairs_flip.tsv` (100),
  `aval.tsv` (45 chains x 7 rows). No RNG; iteration order fixed.
- `src/gen_trace.zag` — deterministic trace + ground-truth generator.
  Inputs: the 8 hand-authored ITEM files, STORE.tsv, pairs, aval, ANNOT, FAB.
  Outputs: `TRACE.tsv` (1521 lines), `GT.tsv` (705 lines).
- `src/validate.zag` — pure-Zag battery validity checker. Run as
  `validate <battery-dir>`; prints VALIDATE_OK or VALIDATE_FAIL lines.
  Checks: exact counts, 5/7/4/6-field shapes, unique ids, label vocab,
  rule-id vocab per pair set, SS token edit distance <= 3 (Amendment 01),
  avalanche 45x7 step ordering, STORE 40 WORLD + 10 GENERATOR,
  TRACE id coverage + sequential steps, GT/ANNOT one-to-one coverage.
- `src/manifest.zag` — pure-Zag manifest generator: MANIFEST.tsv with
  path, byte size, FNV-1a-32 per file. SHA256SUMS.txt is the external
  auditable counterpart.
- `battery/` — the frozen corpora:
  - Hand-authored (blind, no fork influence): CONF.tsv (150 CATCH),
    GOLD.tsv (150 KEEP), ALIBI.tsv (60), RECUR.tsv (60), SMUGGLE.tsv (100),
    UTYPE.tsv (60), CALIB.tsv (40), POINTER.tsv (40) = 660 items.
  - Generated deterministically: pairs_*.tsv, aval.tsv.
  - Ground truth + traces: GT.tsv, TRACE.tsv, ANNOT.tsv, FAB.tsv, STORE.tsv.
  - `TRACE_README.txt` documents trace row semantics.
  - MANIFEST.tsv, SHA256SUMS.txt.

## Provenance

- Hand-authored corpora were written by hand in this session with zero
  knowledge of fork internals (forks' build commits had not landed when
  drafting began; attacks only start after their commits land on
  tnn-native-lab). No generator-authored drafts were used anywhere.
- Held-out fixtures (HELD 500) are NOT in this commit; they are generated
  only after the main attacks, per the frozen prereg (M7).

## Determinism evidence

See DETERMINISM.txt: build_para x2 byte-identical; gen_trace x2
byte-identical; validate prints VALIDATE_OK on the frozen set.
