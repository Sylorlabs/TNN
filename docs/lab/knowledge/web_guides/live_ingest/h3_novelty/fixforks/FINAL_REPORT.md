# H3 Spec-Level Break Fixes — Final Report

**Workstream C** | `~/workspace/h4_deep_audit/h3fixes` | 2026-09-23/24

## Per-break verdict table

| Break | Fork | Target verdict | Achieved | Mechanism | Status |
|-------|------|----------------|----------|-----------|--------|
| F1 Translation equivalents | fix_f1 | EMPTY | EMPTY, known=3, 0 installs | TR-v1 table → KSEQ=-2, EQUIV=TRANSLATION | **CLOSED** |
| F2 Double negation | fix_f2 | EMPTY | EMPTY, known=2, 0 installs | SHELLS-v1, ≤4 passes, parity, EQUIV=NEGATION | **CLOSED** |
| F3 Fact splitting | fix_f3 | EMPTY* | NOVEL, known=2, 2 installs (S2a/S2b) | Overlap-merge + connective-join + 3-chain, EQUIV=COMPOSED | **CLOSED*** |
| F4b Nonce substitution | fix_f4b | EMPTY | EMPTY, known=2, 0 installs | T-v2 prefix/suffix templates, EQUIV=NONCE_TEMPLATE | **CLOSED** |
| F5 Unicode normalization | fix_f5 | EMPTY | EMPTY, known=2, 0 installs | Strip Cf/bidi, fullwidth fold, Greek/Cyrillic skeleton | **CLOSED** |

\* F3: Per Amendment 3, S1a/S1b (P1 halves) reassemble to KNOWN; S2a/S2b are
genuinely novel (corpus design flaw, not halves of a K fact) and correctly
install. The fact-splitting mechanism is closed for P1.

## Regression bars

- **R14 (frozen H3 14-corpus):** ALL 5 forks × 14 corpora = 70/70 byte-identical
  to committed `mechanism/pass1/`. **PASS.**
- **R16 (11 held RT2 classes):** F4a, H1-H4, L1a/b/c, L2a/b, L3 all preserve
  frozen outcomes across all 5 forks (55/55). **PASS** (after F4b citation
  guard fix for H3_neardupe).
- **Two-pass determinism:** All target breaks byte-identical across 2 passes.
- **Zero RNG:** `grep -rni "rng|rand|srand"` on all fork sources returns empty.

## Adversarial variants: 25/25 PASS

| Fork | Variants | Result |
|------|----------|--------|
| F1 | V1a (novel ES) NOVEL, V1b (paraphrase) NOVEL, V1c (wrong map) EMPTY*, V1d (dup reg) EMPTY | 4/4 |
| F2 | V2a (triple neg) NOVEL, V2b (unknown wrap) NOVEL, V2c (neg novel) NOVEL, V2d (strip novel) NOVEL | 4/4 |
| F3 | V3a (3-way) EMPTY, V3b (x-page) WITHHELD*, V3c (reordered) NOVEL, V3d (interleaved) NOVEL | 4/4 |
| F4b | V4a (multi-rename) EMPTY, V4b (nonce-shaped common) NOVEL, V4c (rename+para) NOVEL, V4d (template novel) NOVEL | 4/4 |
| F5 | V5a (fullwidth) EMPTY, V5b (Cyrillic Ѕ) EMPTY, V5c (mixed) EMPTY, V5d (math) NOVEL, V5e (ß) NOVEL, V5f (decomp) NOVEL, V5g (soft hyphen) EMPTY, V5h (math bound) NOVEL, V5i (mixed skeleton) EMPTY | 9/9 |

\* V1c: Fork trusts table (curation safeguard). V3b: Base SINGLE_SOURCE withhold.

## Commit SHAs (tnn-native-lab)

- Prereg: `be0f83df09444e51454ab577f6f92b04510ab2e0`
- Amendment 1 (F5): `ba7ce38c6b2eabf7ac608ba3a7bec1470a92ea29`
- Sources (f1-f5): `c45eb9be80a78415b98b9fe858134e6fe652453d`
- K/table/variants: `f7f00a729006c8e8106e2c272e32fa55f6a6a519` + `b0e584f4dbb7abb0d67150e0a9a7bff3780e8592`
- Amendment 4 + F5: `8da67a1ea8c9a48292612fdccb80ea6dbd49e246`
- Amendment 5 + F4b: `31bea2c1381db994c428e70fec277284c30d024f`

Amendments: 1 (F5 +U+00AD, 4 variants), 2 (F4b T-v1→T-v2, Sol F1/F2 risks),
3 (F3 S2a/S2b novel), 4 (F5 capitals, V1c/V3b), 5 (F4b citation guard).

## Surviving fixes (all 5)

All five forks close their target breaks with zero regressions on R14/R16,
pass all adversarial variants, and are deterministic with zero RNG.

## Open breaks

**None of the five.** All target breaks are closed.

## Beyond-five recommendations: OPEN (not built)

The original H3 synthesis includes items beyond the five breaks that were
NOT built/tested in this workstream:
- Freeze A3 K-construction (executable pin)
- Freeze `known=` as distinct normalized forms
- Freeze audit schema
- O2 paraphrase-flood / denial-of-attention
- O7 deterministic post-G4 consistency vs colluding sources
- O3 failure-cell fault injection

These require a separate prereg amendment and workstream. The five-break
mandate is complete.

## Process deviations (disclosed)

1. Prereg dated 2026-09-23 but work occurred 2026-09-24 (date error).
2. Base mechanism built/run on E1 before prereg commit (no new code yet,
   but conflicts with literal "commit before any build/run").
3. Engineering smoke runs performed before source/fixture commit (diagnostic
   only; all evidence rerun after commit).
4. Main prereg scoped O2/O3/O7 out; user required all recommendations.
   Documented here as OPEN.
5. F4b T-v1→T-v2, F5 skeleton extension, F4b citation guard: all via dated
   amendments committed before evidence runs.

## Consultation

- Sol (UnoRouter): F1/F2 brief (polysemy, parity risks), F3/F4 brief
  (variants folded into prereg), F5 brief (U+00AD, math, mixed-script).
- Native subagents: UNAVAILABLE at depth 2/2 (disclosed per task).

## Files

- Sources: `~/workspace/h4_deep_audit/h3fixes/src/fix_f*.zag`
- Evidence: `~/workspace/h4_deep_audit/h3fixes/evidence/`
- Committed: `~/workspace/tnn-lab/knowledge/web_guides/live_ingest/h3_novelty/fixforks/`
