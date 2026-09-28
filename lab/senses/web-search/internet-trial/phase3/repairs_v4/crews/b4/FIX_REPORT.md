# B4 Fix Report — r12_cqht.zag (conditionals, quantifiers, hedging, temporal, comparatives)

Date: 2026-09-23. Pure Zag, deterministic, zero RNG. Frozen source copied from
`hellhole/r12_v3.zag`; only this crew's copy was edited. Built with
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(`check --no-zagd` clean apart from 3 pre-existing analyzer warnings; `build -o r12_cqht`).

## Headline results

| Family | Frozen | Fixed | Bar (≥0.85/family) |
|---|---|---|---|
| Conditional (13) | 6/13 (46.2%) | **12/13 (92.3%)** | ✅ need ≥12 |
| Quantifier (12) | 4/12 (33.3%) | **12/12 (100%)** | ✅ need ≥11 |
| Hedge (12) | 1/12 (8.3%) | **12/12 (100%)** | ✅ need ≥11 |
| Temporal (12) | 3/12 (25.0%) | **12/12 (100%)** | ✅ need ≥11 |
| Comparative (10) | 1/10 (10.0%) | **10/10 (100%)** | ✅ need ≥9 |
| Total (59) | 15/59 | **58/59 (98.3%)** | |

- REG382: **2 diffs** (rows 57, 225), both justified hedge-rule flips (see §4).
- Curated-18 (rows 365–382): **18/18**, tags exactly
  `2,2,0,1,0,2,1,1,2,1,2,0,0,2,1,0,1,1`.
- Original task seeds: S1 0✓ S2 2✓ S3 0✓ S4 2✓ S5 1✓; unhedged controls S6/S7 still 1✓.
- Determinism: 3 full runs (reg382 + 5 corpora + seeds) byte-identical,
  SHA-256 `e4b8cabcc39fe31b7c2f46a0c446f03fa13abe3b682f943f2199ccdb623ab19a` ×3.

## 1. Conditionals — 12/13 (miss: C8 only)

**Mechanism** (`scan_text` + new `cond_satisfied`):
- New per-clause pre-pass records conditional markers (`if/unless/whether/
  provided/assuming/suppose`) into `CONDM`/`CONDA`; `whether X or not` is
  treated as concessive, not conditional.
- A clause that would otherwise AFFIRM but carries a marker must pass
  `cond_satisfied`: the antecedent span (marker+1 … claim-predicate, or to
  clause end) is satisfied iff another (or the same) clause asserts it —
  ≥2 antecedent stems prefix-matched, or an antecedent number repeated, or
  1 antecedent stem + 1 claim stem.
- Bare/counterfactual conditionals → blocked → NEUTRAL (C1, C3, C5, C6, C7,
  C9, C10); satisfied antecedents → AFFIRM (C2 via "kettle reached 100C",
  C4 via "Smokers…had more cancer", C11 via same-clause "thermometer read
  100C"); negated consequent still DENY via neg-scope (C13); "whether or
  not" concessive → AFFIRM (C12).

**Before/after** (oracle → frozen → fixed): C1 0/1/0, C2 1/0/1, C3 0/1/0,
C4 1/0/1, C5 0/1/0, C6 0/1/0, C7 0/1/0, C8 1/0/**0**, C9 0/1/0, C10 0/1/0,
C11 1/0/1, C12 1/1/1, C13 2/2/2.

**Known miss (accepted, out of scope):** C8 "Birds use tools" — `use` is
3 chars so it never becomes a claim content word and `pred` stays empty;
fixing that is the M3 blind spot (predicate-less claims), deliberately not
touched to avoid REG382 churn. 12/13 still clears the bar.

## 2. Quantifiers — 12/12

**Mechanism** (new `quant_code`; claim quantifier `Qc` from claim's first
token, evidence quantifier `Qe` from each clause's first token; rules gated
on the usual `nclm>=need && anch==1`):
- (a) `Qe`=no/none/neither vs `Qc`∈{all,most,many,some} → DENY (Q11, Q12)
- (b) `Qc`=no/none/neither vs `Qe`∈{all,most,many,some,one} → DENY (Q2, Q6;
  fires pre-predicate so the M3 `pred=""` cases work)
- (c) negated predicate (`neg_scope` **or post-predicate `not`** within 3
  tokens after the predicate) vs `Qc`∈{all,most,many} → DENY (Q1, Q3, Q7);
  bare claim + existential `Qe`∈{most,many,some,one,few} → DENY (Q8)
- (d) universal/most claim vs strictly weaker existential evidence →
  suppress AFFIRM → NEUTRAL (Q5; "All" is not proven by "Some")
- (f) few↔most either direction → DENY (Q10)
- Weaker→stronger (Q4 some→all, Q9 bare→all) still AFFIRM.

**Before/after:** every row flipped from frozen mistag to oracle (frozen
gave endorse on Q1/Q3/Q5/Q6/Q7/Q8/Q10/Q11/Q12).

## 3. Hedging — 12/12

**Mechanism** (new `lex_hedge`: may/might/could/suggest(s/ed)/possibly/
appear(s)/seem(s)/thought/believe(s/d/ing)/probably/perhaps/likely/maybe):
- Hedged clause → cannot AFFIRM (clause-local, title and snippet streams).
- Hedged **denial** → cannot DENY via neg-scope, but only when the hedge
  sits inside the negation's scope (4 tokens before the predicate):
  "Coffee may not cure colds" → NEUTRAL (H9); incidental hedges elsewhere
  ("Coffee doesn't cause cancer, but hot drinks might") do NOT cancel a
  genuine denial — this narrowing was required to keep REG382 rows 69/164/
  239/344/365 and CUR-01 at their frozen DENY tags.

**Before/after:** H1–H9,H11,H12 0 (frozen: all 1 except H9→2); H10 stays
1 (genuine unhedged endorsement preserved).

## 4. Temporal order — 12/12

**Mechanism** (new `temporal_decide`, runs after the overlap gate;
`anchor_left/right` = nearest non-stop, non-number token, stemmed;
numbers are skipped as anchors — a year is not an entity):
- Same entity, different date → DENY (T12).
- Order pairs normalized to earlier(A,B); evidence reversed → DENY
  (T1, T7, T8, T9, T10); date arithmetic on entity-anchored years confirms
  or denies (T4 confirm, T5 deny).
- All pairs confirmed → AFFIRM, returned directly (needed because event
  verbs like "happened" are absent from `lex_verb`, leaving `pred` empty
  and the pipeline unable to affirm — e.g. the Hastings same-order seed).
- No order info in evidence → suppress AFFIRM → NEUTRAL (T3, T11).

**Before/after:** T1 2, T2 1, T3 0, T4 1, T5 2, T6 2 (via competing-subject;
"she" is a stopword so no temporal anchor — tag still correct), T7–T10 2,
T11 0, T12 2.

## 5. Comparatives — 10/10

**Mechanism** (new `comp_decide`; comparative = token before "than", else
two before ("more apples than"); entities = nearest non-stop anchors):
- Same entities + gradable-antonym comparative (`antonym_pair`: 14 pairs
  incl. faster/slower, more/fewer, more/less, better/worse) → DENY
  (P1, P3–P7, P9).
- Same comparative, swapped entity roles → DENY (P8, P10).
- Identical comparison present → pipeline AFFIRMs (P2).
- "than"-claim with no comparable evidence → suppress AFFIRM → NEUTRAL.

## 6. REG382 diffs (2, both justified)

| Idx | ID | Old | New | Why |
|---|---|---|---|---|
| 57 | P2S-5-2 | 1 endorse | 0 neutral | Both endorsing clauses hedged: title "…Strongly **Suggest** Lab Leak", snippet "New evidence **suggests** Covid-19 lab leak…". Hedged endorsement → NEUTRAL per the hedge oracle (H1–H12). |
| 225 | P2H-5-2 | 1 endorse | 0 neutral | Same row, H-stream twin; same justification. |

No quantifier/temporal/comparative/conditional diffs: no REG382 claim
starts with a quantifier word, none contains before/after/than, and no
frozen-AFFIRM clause carries a conditional marker (verified by probe).
The hedge narrowing (§3) reverted 5 incidental flips (rows 69/164/239/344,
CUR-01) back to frozen tags.

## 7. Integration notes (for the 4-crew merge)

- Return-code encoding changed from `tag*8+reason` to **`tag*16+reason`**
  to fit new reasons; `process_line` now does `tag=r/16`. New reasons:
  7 `temporal`, 8 `comparative`, 9 `quantifier` (deny-side only).
- `scan_text` signature gained `tsup:i32, Qc:i32, sc:[]u8`; scratch map
  grew 100000 → **120000** bytes; `[100000,106352)` is the conditional
  scratch (`CONDM/CONDA/SAT_TOK/SAT_STM/SAT_SB`). `r12_classify` carves
  nothing new for temporal/comparative — they reuse `TOKA/TOKB/LOWB/OUTS/
  VBS` (free after the gate, before `scan_text`).
- New functions: `lex_hedge`, `quant_code`, `tok_is`, `prefix_match`,
  `stemset`, `anchor_left`, `anchor_right`, `tok_num`, `comp_word`,
  `cpair`, `antonym_pair`, `cond_satisfied`, `temporal_decide`,
  `comp_decide`. Changed: `scan_text` (pre-pass, hedge/quantifier logic,
  AFFIRM gate), `r12_classify` (early temporal/comparative decisions,
  `Qc`), `reason_str`, `process_line`, `main` (alloc size).

## 8. Artifacts & hashes

- Source: `/home/hatch/workspace/scratch-hellhole/crews/b4/r12_cqht.zag`
  SHA-256 `7a7627936375a63961ecf534483fdf921b86ff18cb5e4565067d861f188e769f`
- Binary: `/home/hatch/workspace/scratch-hellhole/crews/b4/r12_cqht`
  (built `znc build r12_cqht.zag -o r12_cqht --no-zagd`)
- Determinism: 3× full runs (reg382 + 5 corpora + 7 seeds) byte-identical,
  SHA-256 `e4b8cabcc39fe31b7c2f46a0c446f03fa13abe3b682f943f2199ccdb623ab19a`
- No commit made (per instructions).
