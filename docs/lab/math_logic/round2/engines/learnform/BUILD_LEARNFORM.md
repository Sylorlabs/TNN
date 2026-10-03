# BUILD_LEARNFORM.md — Engine (c) LEARN-FORM build notes

## Toolchain
- Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Build (from this directory; `@import` paths resolve relative to CWD):
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 learnform.zag -o learnform_bin`
- ONE source verified: `~/workspace/math_r2/r1/engines/one/one.zag`
  SHA-256 `0bdbfe52f7f63f2192e32455a5af22fb71b0b5b3d6bc0e8e09eb449e189b25df`
  (identical to `~/workspace/tnn-lab/math_logic/engines/one/one.zag`).
- The `one_emit`..`one_run` span in `learnform.zag` is byte-identical to the
  original (programmatic diff: identical, 5194 bytes).

## Vendored round-1 common files
`common/cx_*.zag` (7 files) and `harness/R33_NATIVE_IO_V1.zag`,
`harness/dlb_util.zag` are verbatim copies of the round-1 sources, except
`common/cx_fwd.zag`: its `@import` directives were stripped so the file can be
textually included from `learnform.zag` (function bodies unchanged). Original
SHA-256 values are recorded in the build log below.

## Architecture
- `learnform_bin learn <kb_md> <schemas_md> <b1_list> <pair_nl> <pair_form> <trace_list> <store_out> <ledger_out>`
  Learner. Starts with an EMPTY pattern store (no store is read; outputs are
  truncated). Learns only from: frozen `KNOWLEDGE_STORE.md`, frozen
  `COMMIT_SCHEMAS.md`, B1 NL statements, one B1 NL→formal pair (P01), frozen
  round-1 traces. Emits `FORMALIZER_STORE` + `PROVENANCE_LEDGER`. Exit 3 on any
  `sealed` path.
- `learnform_bin solve <nl_problem> <formalizer_store> <kb_store> <out>`
  Solver. Reads the frozen store (never learns). Fires learned cues, applies
  the learned template, builds an in-memory `.form`, runs round-1 `one_run`
  3× and asserts byte identity (exit 5 on divergence), prepends a
  formalization audit header to ONE's output. Emits `FORMALIZE-ABSTAIN`
  (distinct from ONE's `WITHHELD`) when no learned pattern yields a
  formalization. Exit 3 on any `sealed` path.

## Learned patterns (from the committed run)
- 5 learned stopwords (majority docfreq over 22 B1 docs): prove, that, the, of, is.
- 10 retained CUE patterns (fired ≥1 doc), 14 dropped (zero-fire):
  S_MP: from, and; S_PBC: proof, not; S_UI: induction, for, every, positive, integer, then.
- 1 TEMPLATE: task="prove", premises=[imp(p,q), p], target=q, support=1,
  from the P01 NL→formal pair.
- Every cue cites its knowledge-store anchor line (KS:9 = K001, KS:17 = K005)
  and the B1 docs it fired on. Full per-word provenance in PROVENANCE_LEDGER.

## Verification results (2026-09-25)
- Learner 3×: byte-identical FORMALIZER_STORE and PROVENANCE_LEDGER.
- Solver 3× (P01): byte-identical reports.
- P01 training smoke (NL→formalize→ONE): VERDICT: DERIVED, CLAIM: q via S_MP.
- P10 (cues, no template): content-atom formalization; ONE WITHHELD
  (derivation-level, distinct from formalize-abstain).
- Synthetic no-pattern input: VERDICT: FORMALIZE-ABSTAIN.
- Sealed path: exit 3 without reading contents.
- Zero-RNG grep: clean. No hand-written NL→schema word literals: clean.

## Toolchain workarounds and bug fixes applied
1. ZNC-2026-09-21-007: all tables use `[]u8` arenas with `au_get32/au_put32`
   little-endian accessors; no `as []i32/u32/u16` casts anywhere.
2. Uninitialized heap: `lfwt_init` explicitly zeroes `ac`, `cite`, `fire`,
   `firen`, `seen`, `fmask` arenas (znc does not zero heap allocations;
   without this, anchor counts and provenance cites were garbage).
3. `_zag_argc()` is unreliable (returns 0); `main` reads `_zag_arg(n)`
   directly and treats "" as absent. `_zag_arg` results are never freed.
4. `lf_next_tok`'s last parameter is `alpha_only` (1 = alpha-only tokens,
   0 = alnum), not a lowercase flag; call sites were audited for the correct
   value. Formal premises/targets use the separate `lf_next_raw`
   (whitespace-delimited) so `imp(p,q)` is not split.
5. Anchor-mining tokenizer is bounded by the clause end (`g2`), not the line
   end, preventing cross-clause word leaks.
6. `lf_find_sect` returns the header-line start so the section's own NL gloss
   quote (the frozen K005/K001 citation) is included as an anchor; section end
   also stops at `## ` headings to prevent leaks from later sections.
7. `lfwt_add_anchor` records the FIRST anchor line's cite (first-wins), so
   provenance cites the original discovery, not the last contributor.
8. Slice `==` is never used for content comparison (`nio_equal` instead).

## Inputs used for the committed run
- KB: `~/workspace/math_r2/r1/knowledge/KNOWLEDGE_STORE.md`
- Schemas: `~/workspace/tnn-lab/math_logic/engines/COMMIT_SCHEMAS.md`
- B1 NL list: `b1_nl.list` (22 × `~/workspace/math_r2/r1/problems/P01.txt`..`P22.txt`)
- Pair: `~/workspace/math_r2/r1/problems/P01.txt` +
  `~/workspace/tnn-lab/math_logic/problems/formal/P01.form`
- Traces: `traces.list` (22 × `~/workspace/math_r2/r1/traces/TRACE_P01.txt`..`P22.txt`)
- Solver KB: `~/workspace/tnn-lab/math_logic/knowledge/KB_SMOKE.md`
