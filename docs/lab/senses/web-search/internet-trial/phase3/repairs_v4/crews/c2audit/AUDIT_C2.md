# AUDIT — C2 LOGIC-CORE (hell-hole V4, auditor: C2-AUDIT crew)

**Target:** `crews/c2/logic.zag` (1,018 lines), `crews/c2/logic_bin`, `crews/c2/batteries/` (10 TSVs), `PROOF.md`, `PROPSYNTAX.md`, `BATTERIES_FROZEN.md`.
**Method:** full end-to-end source read; independent runs of the shipped binary; fresh rebuild from source with the pinned toolchain (`znc_linux_x86_64_abed8aa1 --no-zagd`); battery regeneration; 22 self-authored red-team probes.
**Nothing in `crews/c2/` was modified.** All audit work in `crews/c2audit/`.

## Bottom line

The engine is a genuine structural logic engine — checks 2, 3, 4 pass solidly, determinism holds, v3proof 3/3 and mlogic 5/5 reproduce. **But the headline claim 167/168 = 0.9940 does not reproduce (measured 154/168 = 0.9167), and the battery freeze chain is broken: the frozen SHAs match none of the current TSVs, the batteries were rewritten after the binary was built, and PROOF.md's "post-run hashes match frozen" table is false.** The 167/168 figure cannot be verified from the current artifacts.

## Check-by-check verdicts

### 1. Batteries frozen before scoring — FAIL

- `BATTERIES_FROZEN.md` (frozen 2026-09-23 15:21:21 UTC) lists 10 SHAs. **Current SHA-256 of the 10 TSVs matches none of them** (verified file by file).
- mtimes (UTC): `BATTERIES_FROZEN.md` 15:21:44 · `logic.zag` 15:39:14 · `logic_bin` 15:40:20 · `gen_batteries.py` 15:44:56 · all 10 TSVs 15:44:57 · `PROOF.md` 15:46:05. The batteries were **rewritten at 15:44 — after the binary build, inside the scoring window**.
- `gen_batteries.py` regenerates the *current* TSVs byte-identically (10/10 IDENTICAL, verified), but **not** the frozen SHAs. PROOF.md checklist item 11 ("re-derives the frozen LOGIC-CORE batteries byte-identically — verified: 10/10 IDENTICAL") is false with respect to the frozen record.
- PROOF.md's "Battery input hashes (post-run, must equal BATTERIES_FROZEN.md)" table (all 10 "✓") is **false** as of now.
- The current batteries contain oracles that contradict the engine's own documented spec:
  - `g_hedge.tsv` GH-02/07/13/15/19 (`MAYBE(p)` vs `MAYBE(p)`) carry oracle **1**, but `PROPSYNTAX.md` "Deliberate non-rules" says `MAYBE(p)` vs `MAYBE(p)` → NEUTRAL. The engine follows the spec (→ 0) and is marked wrong 5 times.
  - `g_qnt.tsv` GT-15: claim `QTY(goldfish_memory,at_least,six_months)` vs evidence `QTY(goldfish_memory,exactly,3sec)`, oracle **0** — while the same quantity pair reversed is GT-14 (oracle 2) and VP-GOLDFISH (oracle 2, the kill-bar-cleared behavior). Disjoint intervals → DENY is sound; oracle 0 is indefensible.
  - `g_tmp.tsv` GP-04 (claim `AFTER(b,a)` vs `BEFORE(b,a)`, oracle 1) and GP-19 (claim `AFTER(a,b)` vs `NOT(BEFORE(b,a))`, oracle 1): both are genuine contradictions after `AFTER→BEFORE` canonicalization; the engine's DENY is correct, the oracles are wrong. GP-06 is the one miss PROOF.md documents; GP-04/GP-19 are two more of the same kind, undocumented.
- No git repo or backup exists under `scratch-hellhole/`, so the frozen (15:21) battery contents are **unrecoverable**. It is impossible to determine whether 167/168 was ever achieved on them, or whether the frozen SHAs were ever correct.

### 2. Not a prose keyword classifier — PASS

Full 1,018-line read. Verdicts derive from proposition structure:
- Operator dispatch via `pkind` (not/cause/qty/all/some/none/if/maybe/before/atom); structural negation matching (`is_not` + byte-equality, double-negation eliminated in canonicalization); quantifier polarity algebra (`r_qnt_deny`); interval arithmetic on canonicalized quantities (`r_qty`, open/closed-bound aware); temporal reversal after `AFTER(x,y)→BEFORE(y,x)` canonicalization; modus ponens over the evidence set (`R-COND-MP`, requires a separate matching antecedent prop).
- The only English-ish tables are `word_num` (one–ninety, closed number grammar) and `unit_code_for` (time-unit suffixes, closed value grammar) — the proposition **value grammar**, explicitly allowed. They never decide a verdict by themselves; quantities flow through interval comparison. String-literal audit of the source confirms: zero negation word lists, zero antonym tables, zero endorsement/sentiment heuristics, zero content-word → verdict mappings. Atoms compare by lowercased byte-equality — purely syntactic.

### 3. Native numeric/range comparison — PASS

Exercised through the rebuilt binary (all verified):
- Ranges: `22_to_33` and `between_22_and_33` both parse; `range 22–33` vs `exactly 25` → AFFIRM (`R-QTY-AFFIRM`).
- Bounds: `more_than 5` vs `exactly 10` → AFFIRM (subset); `more_than 5` vs `exactly 5` → DENY — the open-boundary exclusion is handled correctly.
- Unit conversion: `60sec` vs `one_min` → AFFIRM (both canonicalize to 60 sec); `5` (count) vs `5sec` → NEUTRAL (unit classes never mix, per spec).
- Word-numbers: `twenty_two` ≡ `22`, `eighty` ≡ `80` → AFFIRM. The documented whole-token-first fix works — no `eight`+`y` digit-substring hack (`parse_qty_value` tries the whole token as a number first, then longest unit suffix with backtracking requiring a numeric remainder).
- Month/year use fixed approximations (mo = 2,592,000 s, yr = 31,536,000 s) — mechanical and applied symmetrically to both sides; noted as an approximation, not a hack.

### 4. No seeded verdicts — PASS (mechanically verified)

- `process_line` splits the TSV line on tabs and reads only field indices 0,1,2 (`id`, `claim_prop`, `evidence_props`). Field 3 (oracle) slots are **never fetched anywhere in the source** (grep for field-index access confirms zero reads of slots 6–7).
- No verdict tables, no id→verdict mappings, no reads of any other column. The scorer (`score.py`) is a separate Python process. The engine cannot see the oracle even in principle.

### 5. Faithful v3 mapping — PASS, with the documented residual (qualified)

Spot-checked against `hellhole/ev_r12_input.tsv` and `hellhole/v3_course.json`:
- VP-ICE: V3-03 claim "Ice floats on water because water expands when it freezes" → `FLOATS(ice,on_water)` + `CAUSE(LESS_DENSE(ice,than_water),FLOATS(ice,on_water))` — faithful; AFFIRM via `R-CAU-AFFIRM` ✓.
- VP-GOLDFISH: V3-05 claim "Goldfish have a memory of only three seconds" → `exactly 3sec`; evidence "spatial memory of at least six months" (line 35) → `at_least six_months` — faithful; DENY ✓.
- VP-SENSES: V3-07 claim "Humans have exactly five senses" → `exactly five`; evidence "between 22 and 33 senses" (line 51) → `range 22_to_33` — faithful; DENY ✓.
- K-V3PROOF **3/3** and K-MLOGIC **5/5** both reproduced by my runs.
- Residual (honestly documented in PROOF.md, assessed here): each mlogic item compresses its seed's composition step ("X entails ¬claim") into the authored `CAUSE(r, NOT(claim))` link — the first two evidence props (e.g. `CONTAINS(chocolate,caffeine);STIMULANT(caffeine)`) are never used by the engine; only the pre-composed third prop fires `R-CAU-DENY`. **The 5/5 genuinely exercises the verdict-derivation machinery, but it does not demonstrate native composition** — the key inference step arrives human-authored inside the evidence proposition. The battery measures verdict machinery, not the "R6 composition" its name implies. Does not invalidate the 5/5; does limit what it proves.

### 6. Determinism — PASS on determinism; claimed SHA NOT reproduced

- 3× full runs over all 168 rows: **byte-identical**, SHA-256 `4eb534ac18f98dc364ad2552cefdfd14489467aeab6d640fb8321c8f457d5039` ×3.
- Claimed `32706efb1bb2e4cad4ec692ffa28a9a8fb0aaa0511a98cee422f11cbac20e8f9` does **not** match (expected: outputs differ because scores differ).
- Fresh rebuild of current `logic.zag` with the pinned toolchain → output **byte-identical** to shipped `logic_bin`. The shipped binary is faithful to the current source.
- Extern surface: `_zag_arg`, `_zag_malloc`, `_zag_free`, `_zag_print`, `_zag_println`, `_zag_raw_syscall`, `_zag_slice_ptr` only; raw syscalls are 0/2/3 (file I/O). No RNG, no clock, no network. `znc check` capability proof not re-run (not needed for the audit findings).

### 7. RED TEAM — 22 self-authored adversarial probes

Probes run through the freshly built binary; expected verdicts from independent logical analysis (`E` = engine, `L` = logic).

| ID | Probe | E | L | Result |
|---|---|---|---|---|
| RT-01 | Transitivity: `BEFORE(a,c)` vs `BEFORE(a,b);BEFORE(b,c)` | 0 | 1 | miss — accepted exclusion (documented: no order-theoretic completion) |
| RT-02 | Antonym pair: `FLOATS(ice,on_water)` vs `SINKS(ice,in_water)` | 0 | 0* | correct per spec (documented: no antonym knowledge) |
| RT-03 | 3-hop causal chain to `NOT(Q())` | 1† | 2 | probe design flaw — 3rd prop's consequent directly matched; see RT-23 |
| RT-04 | Nested negation `NOT(NOT(P()))` vs `NOT(P())` | 2 | 2 | correct |
| RT-05 | Vacuous hedge: `P()` vs `MAYBE(P())` | 0 | 0 | correct |
| RT-06 | Double-neg evidence: `P()` vs `NOT(NOT(P()))` | 1 | 1 | correct |
| RT-07 | Detached consequent: `B()` vs `IF(A(),B())` | 0 | 0 | correct |
| RT-08 | MP w/ denied antecedent: `B()` vs `IF(A(),B());NOT(A())` | 0 | 0 | correct |
| RT-09 | Temporal contraposition: `BEFORE(x,y)` vs `NOT(BEFORE(y,x))` | 0 | 1 | miss — accepted exclusion (documented non-rule) |
| RT-10 | Unit-class mixing: `exactly 5` vs `exactly 5sec` | 0 | 0 | correct |
| RT-11 | `twenty_two` vs `22` | 1 | 1 | correct |
| RT-12 | `eighty` vs `80` (substring-hack trap) | 1 | 1 | correct — no digit hack |
| RT-13 | `60sec` vs `one_min` | 1 | 1 | correct |
| RT-14 | `more_than 5` vs `exactly 10` | 1 | 1 | correct |
| RT-15 | `more_than 5` vs `exactly 5` (open boundary) | 2 | 2 | correct |
| RT-16 | `between_22_and_33` vs `exactly 25` | 1 | 1 | correct |
| RT-17 | `exactly 25` vs `range 22_to_33` (mere overlap) | 0 | 0 | correct |
| RT-18 | **Vacuous cause**: `WAKES_UP(coffee,drinker)` vs `CAUSE(NOT(CONTAINS(coffee,melatonin)),WAKES_UP(coffee,drinker))` | 1 | 0 | **GENUINE HOLE** (see below) |
| RT-19 | Detached antecedent: `CAUSE(r,q)` vs `r` alone | 0 | 0/1 | scope gap; engine's 0 is defensible (r alone ≠ causation) |
| RT-20 | `BEFORE(a,a)` vs `BEFORE(a,a)` | 1 | 0 | minor wart — identity affirms an unsatisfiable proposition |
| RT-21 | Case-insensitivity: `FLOATS(ice)` vs `floats(ice)` | 1 | 1 | correct |
| RT-22 | `exactly eight` vs `exactly 8y` (count vs years) | 0 | 0 | correct |
| RT-23 | True multi-hop: `Q()` vs `CAUSE(A(),B());IF(B(),Q());A()` | 0 | 1 | miss — accepted exclusion (documented: no chained MP) |
| RT-24 | Denying the antecedent: `NOT(B())` vs `CAUSE(A(),B());NOT(A())` | 0 | 0 | correct — avoids the fallacy |
| RT-25 | `CAUSE(A(),B())` vs `NOT(CAUSE(A(),B()))` | 2 | 2 | correct |
| RT-26 | Nested cause: `CAUSE(A(),CAUSE(B(),C()))` vs `NOT(CAUSE(B(),C()))` | 2 | 2 | correct |
| RT-27 | `BEFORE(a,b)` vs `AFTER(a,b)` | 2 | 2 | correct |
| RT-28/29 | Malformed input / empty evidence field | 0 | 0 | graceful degradation (opaque `lit()` fallback) |

\* L=0 per the documented no-antonym-knowledge scope; a human judge would say 2.
† RT-03's evidence contained `CAUSE(C(),NOT(Q()))` whose consequent structurally equals the claim, so single-hop `R-CAU-AFFIRM` fired — my probe accidentally tested the 1-hop case. RT-23 is the true multi-hop probe.

**Genuine holes vs accepted exclusions:**
- **RT-18 (load-bearing limitation, not a code bug):** `R-CAU-AFFIRM` fires on *any* `CAUSE(r,q)` whose consequent matches the claim — including vacuous/absurd reasons such as `NOT(...)` mechanisms. An adversarial evidence author can force AFFIRM of any `q`. By design the engine has no world knowledge (that's the point of Track G), so this is a design boundary: the rules are only as trustworthy as the evidence author. In adversarial settings this is load-bearing; under the trusted-evidence contract it is accepted.
- **RT-20 (minor):** structural identity affirms even unsatisfiable propositions (`BEFORE(a,a)`). No satisfiability check exists.
- **MAYBE asymmetry (minor):** `r_ident_affirm` excludes `MAYBE` from affirming, but `r_neg_deny` still fires on `MAYBE(A())` vs `NOT(MAYBE(A()))` (GH-08 → DENY), while PROPSYNTAX.md says "`MAYBE(p)` never affirms/denies anything". Doc/engine tension.
- Accepted exclusions (all documented in PROPSYNTAX.md, probed and confirmed): transitivity, multi-hop composition, temporal contraposition, antonym pairs, detached consequents, lone conditionals.

## Reproduced scores (independent runs of the shipped binary)

| Battery | Measured | Claimed | Bar | Bar met? |
|---|---|---|---|---|
| g_neg | 20/20 | 20/20 | ≥18 | yes |
| g_con | 18/20 | 20/20 | ≥18 | yes (misses GC-03, GC-19) |
| g_cau | 20/20 | 20/20 | ≥18 | yes |
| g_qnt | 18/20 | 20/20 | ≥17 | yes (misses GT-15, GT-18) |
| g_cond | 20/20 | 20/20 | ≥17 | yes |
| g_hedge | 14/20 | 20/20 | ≥17 | **NO** (6 misses, all MAYBE-identity vs spec) |
| g_tmp | 16/20 | 20/20 | ≥17 | **NO** (GP-04, GP-06, GP-09, GP-19) |
| g_cmp | 20/20 | 20/20 | ≥17 | yes |
| v3proof | 3/3 | 3/3 | 3/3 | yes |
| mlogic | 5/5 | 5/5 | 5/5 | yes |
| **Total** | **154/168 = 0.9167** | **167/168 = 0.9940** | — | K-FAM50 (≥0.95/family) **fails** |

## Honest limits of this audit

1. The frozen (15:21 UTC) battery contents are unrecoverable (no git/backups under `scratch-hellhole/`), so I cannot rule on whether 167/168 was ever truly achieved — only that it is not reproducible from current artifacts and the freeze chain is broken.
2. The English→proposition mapping (v3 claims → proposition encodings) is human-authored, declared out of scope for Track G; I verified fidelity of the mapping, not the mapping process.
3. Red-team "expected" verdicts for the accepted-exclusion probes reflect classical logic; the engine's documented scope deliberately excludes them — those misses are spec compliance, not defects.
4. `znc check` capability proof was not re-run; extern/syscall surface was verified by source audit instead.
