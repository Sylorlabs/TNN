# B1 NEGATION FIXER — FIX REPORT (hell-hole V4)

**Deliverable:** `crews/b1/r12_neg.zag` (SHA256 `da3bae36d81364bc6ac8730cd48048488cf92c585bb6ae99c342e0025e549c13`, 1405 lines)
**Frozen base:** `hellhole/r12_v3.zag` — **untouched** (no commit, per instructions).
**Toolchain:** `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, always `--no-zagd`.
**Method:** surgical repair, zero RNG, pure Zag, no web. Only `r12_neg.zag` was edited.

## Headline results

| Bar | Result |
|---|---|
| Seed failures flip | 3/3 → DENY (`S1 2 neg-scope`, `S2 2 deny-lex`, `S3 2 neg-scope`) |
| A1 corpus (52) | **52/52 = 100%** (frozen baseline was 18/52) |
| REG382 | 374/382 byte-identical; 8 diffs, all intended (table below) |
| Curated-18 | **18/18** — tags `2,2,0,1,0,2,1,1,2,1,0,0,2,1,0,1,1`... see §5 |
| K-DET | 3 runs × 4 corpora, all byte-identical (SHAs §6) |
| K-PURE | pure Zag; no RNG/time/pid/`/dev/urandom` (grep-verified) |

Curated-18 observed tags: `2,2,0,1,0,2,1,1,2,1,2,0,0,2,1,0,1,1` — matches the expected sequence exactly.

## 1. Exact rule/function changes

### 1.1 Lexicon changes

| Lexicon | Change | Why |
|---|---|---|
| `lex_strong` (strong deny-lex) | **added:** `contradict`, `denie`, `deny`, `disput`, `reject` | The old list (`debunk/disprov/refut/...` prefixes + nouns) missed the actual verb stems this codebase's `z_stem` produces: "denies"→`deny`, "denied"→`denie`, "rejected"→`reject`, "contradicts"→`contradict`. ("disputes"→`dispute`, which matches `lex_strong`'s `disput` entry only via the `deny_prefix("disput")` prefix below, not the exact entry.) |
| `deny_prefix` | **added:** `deny`, `reject`, `disput`, `contradict` | Catches the full verb families regardless of inflection ("denies/denied/denial", "disputes/disputed", "rejects/rejection", "contradicts/contradiction"). |
| `lex_evid` | **new:** `evidence proof studies data research findings results study` | Generalizes the old literal `"no evidence"` substring. |
| `lex_barrier` | **new:** `although though despite while whereas however but` | Clause-boundary veto: a marker after a barrier word scopes to the subordinate clause, not the claim predicate. |
| `lex_cmp` | **new:** 15 comparatives (`faster slower better worse higher lower bigger smaller greater less more easier harder quicker sooner longer`) | "No X cures disease faster" veto (NEG-14). |
| `lex_cog` | **new:** `think thinks thought believe believes believed feel feels felt seem seems seemed appear appears` | Cognitive-verb guard: "no one thinks X" does not deny X. |

### 1.2 New helper functions

| Function | Purpose |
|---|---|
| `neg_marker_at(clause,tokC,nct,j,tmp)` | Single source of truth for negation markers: `not never no none neither nor nothing nobody nowhere`, `n't`, curly `n't` (U+2019t), minus `never fails to` (double negation → 0). |
| `next_content(clause,tokC,nct,j,tmp)` | Next non-filler token index (skips stopwords; "very"/"so" treated as filler). |
| `has_barrier(clause,tokC,nct,j,tmp)` | Barrier word in the 3 tokens before `j`. |
| `find_word(clause,tokC,nct,w,from,tmp)` | Case-insensitive token search from index. |
| `strip_eq(a,b)` | ASCII lowercase equality (for antonym table keys). |
| `antonym(w)` / `antonym_tail(w)` | Antonym table: `effective↔ineffective`, `blind↔sighted`, `flat↔spherical`, `active↔inactive`, `true↔false`, `possible↔impossible`, `safe↔dangerous`, `healthy↔unhealthy`, `real↔fake`, `beneficial↔harmful`. (**Bug fixed during repair:** the table originally mapped to `"activ"`, but this `z_stem` leaves `"active"` unchanged — the key would never match.) |
| `veto_idiom(clause,tokC,nct,j,tmp,firstA,pi,stemC,cstmC)` | Returns 1 when a marker must NOT deny: "not only/just/merely", "never fails to", `no <firstA> … <comparative>` ("no treatment cures disease faster"), and the general `not X but Y <pred>` subject-focus veto. (**Bug fixed during repair:** `w` aliased `tmp`, which `next_content` clobbers — the `no`-check read corrupted bytes. Now uses an `is_no` int flag captured before the clobbering call.) |
| `matrix_deny(clause,tokC,nct,j,tmp,stemC,cstmC,pi)` | Distant/matrix negation: a marker whose next content word is a reporting/cognition verb (`say/says/said/believe/...`, plus cognitive verbs) denies the embedded claim **unless** the verb is cognitive + complement is positive, or the next word is `true`/`the case` ("It is not true that X" affirms X). "neither"/"nor" before the predicate with claim overlap → 1. |

### 1.3 `neg_scope` — rewritten (signature extended)

Old: 4-tokens-before-predicate substring scan (`not/never/no` within `pi-4..pi-1`), blind to everything after the predicate.
New `neg_scope(clause,tokC,nct,pi,stemC,cstmC,stemA,cstemA,ncs,firstA,subjA,pred,cadj,tmp)`:
- **(A) cleft deny:** `It is not <claim-subject> but <other> that <pred>` → 1. Subject matched against `firstA` **or** `subjA` (first non-stop claim-token stem — needed because "Tea" is too short for the content-word filter, NEG-44).
- **(B) token loop** over every marker position `j` in the clause, in order:
  1. `veto_idiom` → skip.
  2. `has_barrier` → skip (marker scopes to subordinate clause).
  3. `j < pi`: classic pre-predicate negation → 1, except copula + complement mismatch (`is not X` where X ≠ claim complement and X has no antonym link → 0).
  4. `j > pi`: `matrix_deny` → 1; **post-copula complement**: `are not <adj>` where `<adj>` stem = claim complement stem (`cadj`) → 1 ("bats are NOT blind", seed S1); complement = antonym(`cadj`) → 0 ("is not ineffective" affirms "effective"); **double negation** (`not un-X` / `not in-X` / `not im-X` where X=cadj → 0); **negative-prefix subject** (`none/nothing` before pi → 1, "None of the trials showed benefits", NEG-01).
  5. `j == pi` (negated auxiliary, "doesn't cause") → 1.

### 1.4 DENY(a) (deny-lex) changes in `scan_text`

- **Generalized no-evidence:** old literal `z_has(low,"no evidence")` → token-level: `no` followed within 3 tokens by any `lex_evid` word ("No clinical evidence…", "No credible study shows…"). The old literal is gone.
- **Polarity-aware "no longer":** old literal substring (always → weak) → token-level: `no longer <w>` denies only if `<w>` stem = claim complement (`cadj`) or `<w>` is a reporting verb ("no longer says coffee causes cancer" → DENY, rows P2S-7-4/P2H-7-2/CUR-02 verified unchanged); suppressed when `<w>` is the complement's antonym ("no longer suspended" affirms "active") or unrelated.
- **`none/nothing/nobody/nowhere` subject deny:** new pre-predicate block — fires even when `pi<0` (no predicate found), fixing NEG-01 where `showed` is a reporting verb and the old code found no predicate.

### 1.5 Predicate / claim analysis changes in `r12_classify`

- **Reporting-verb pred fallback:** if no non-reporting verb is found, fall back to the first reporting verb (was: straight to aux/copula). Fixes "None of the trials showed benefits" (`pred=show`).
- **`cadj` (new):** stem of the claim's copula complement ("The drug is ineffective" → `ineffect`). Used by post-copula resolution and "no longer" polarity. Scratch-carved at `CADJB=sc[97928..97992]`.
- **`subjA` (new):** stem of the first non-stop claim token ("Tea causes cancer" → `tea`). Used only by the cleft rule.
- Signatures: `scan_text` and `neg_scope` gained `cadj`/`subjA` params; both `scan_text` call sites updated.

### 1.6 Endorsement (AFFIRM) guards in `scan_text`

- **`lhedge` (new):** if the stream's last non-space byte is `?`, no endorsement anywhere in the stream. (Rationale: `?` is a clause separator so it never appears *inside* a clause — the old code had no interrogative hedge at the stream level. A trailing question hedges the proposition: "…or doesn't it?" → NEUTRAL, NEG-28.)
- **`whether` (new):** a clause containing "whether" never endorses ("doubt cast on whether…" hedges the proposition).
- Unchanged: `framed` (conspiracy/legend), `is_interrog` whaux-first, `comp` competing-subject blocks.

### 1.7 Scratch-map changes (collision fixes found during repair)

- `DENYA` was carved at `sc[96512..96608]`, colliding with `CLVSB=sc[96512..96992]` — moved `DENYA` to `sc[97992..98056]`.
- `TMPS/OUTS/VBS` moved to `sc[99600..]` (out of the way of `NUMA`/`CLAUA` growth).
- `CADJB=sc[97928..97992]` added (`cadj` at +0, `subjA` at +32).

## 2. Seed results (both failures flip)

| Seed | Snippet | Result |
|---|---|---|
| S1 "Bats are blind." | "bats are NOT blind" | **2 neg-scope** (post-copula complement = cadj) |
| S2 "Celery juice cures disease." | "No clinical evidence supports the claim that celery juice cures disease" | **2 deny-lex** (generalized no-evidence) |
| S3 "Coffee causes cancer." | "Coffee doesn't cause cancer" | **2 neg-scope** (negated auxiliary at pi) |

## 3. A1 corpus: 52/52 (100%)

Frozen baseline was 18/52. All 34 previously-missed rows now correct, including: NEG-01 (none-subject), NEG-04/05 (not un-X / not ineffective double negation), NEG-06/07 (neither/nor), NEG-09 (no longer says → DENY), NEG-10 (no longer suspended → suppressed), NEG-11/12 (post-copula), NEG-13 (no scientist believes), NEG-14 (no…faster comparative veto), NEG-15/16 (not only), NEG-18/19 (never fails to), NEG-21/22 (cleft), NEG-23 (not X but Y affirm), NEG-24/25 (n't / curly n't), NEG-28 (trailing-? hedge), NEG-43/44 (cleft short subject), NEG-46–52 (deny-verb lexicon), NEG-08/17/20 (affirm holds), NEG-26/27/29/30/31 (neutral holds), NEG-32–42/45 (scope vetoes).

## 4. REG382: 8 diffs, all intended

374/382 rows byte-identical to `hellhole/reg382_tags.txt` (tag AND reason). The 8 diffs:

| # | idx | frozen | new | justification |
|---|---|---|---|---|
| 73 | P2S-8-1 | 1 endorse | 0 neutral | Snippet is the bare question "What evidence is there that Earth is flat?" — `lhedge` blocks endorsement. A question is not endorsement evidence (R1: AFFIRM needs positive endorsement). Old AFFIRM was a false affirm. |
| 80 | P2S-8-2 | 1 endorse | 0 neutral | Same quora pattern as #73. |
| 241 | P2H-8-1 | 1 endorse | 0 neutral | Same quora pattern as #73. |
| 246 | P2H-8-0 | 1 endorse | 0 neutral | Same quora pattern as #73. |
| 76 | P2S-8-4 | 1 endorse | 2 neg-scope | "…the Bible **nowhere states** categorically that the earth is flat" — `matrix_deny` via `nowhere` + reporting verb `states`. Consistent with NEG-13 ("no scientist believes" → DENY). Old AFFIRM was a false affirm. |
| 244 | P2H-8-4 | 1 endorse | 2 neg-scope | Same as #76 (P2H twin). |
| 354 | P2H-8-96 | 2 competing-subject | 2 neg-scope | **Tag unchanged (DENY).** Reason improved: "The Earth is not flat" now via post-copula neg-scope instead of the competing-subject heuristic. |
| 361 | P2H-15-96 | 1 endorse | 2 deny-lex | "No credible study shows chocolate cures insomnia" — generalized no-evidence rule fires correctly. Old AFFIRM was a false affirm (affirmed on overlap despite "No credible study shows"). |

Pre-identified regression risks verified **unchanged**: P2S-7-4 / P2H-7-2 / CUR-02 (`2 deny-lex`, polarity-aware "no longer says"); P2H-0-96 ("No credible source disputes this" → `1 endorse`, protected by the overlap gate since "disputes" scopes opposition to the claim); P2S-0-2 / P2H-0-2 ("not only to water" → `1 endorse`, veto holds).

## 5. Curated-18: 18/18

Extracted from `hellhole/proto_r12.py` `__main__` block. Observed tags `2,2,0,1,0,2,1,1,2,1,2,0,0,2,1,0,1,1` — exact match to expected.

## 6. K-DET — three runs, byte-identical

| Corpus | SHA256 (all 3 runs) |
|---|---|
| seeds (3) | `825a491ff118f77d4d16dcf662f3ea1ba904a9a85c715429981d76f2e47e160a` |
| A1 corpus_neg (52) | `e14c3e2408181815aee24b860ba748af5283e62c494a6ab80e4fa7c23815a413` |
| reg382 (382) | `bbedad78dc4a901a846768dc506a74f364d1238a30c0332dbf5ed1495746482a` |
| curated-18 | `55367a0fb4a38b6c010be36f4447ca811e1c8500a3e458d46684178f441ee79c` |

## 7. K-PURE

Pure Zag. No RNG, no time/clock reads, no pid, no `/dev/urandom`, no network — grep-verified. Deterministic given input by construction.

## 8. Build notes

- `znc check` clean; `znc build` wrote native binary. The two analyzer warnings (A0107 `read_all` loop, A0101 `main` loop bound) are pre-existing in the frozen base, untouched.
- Bugs caught and fixed during the repair itself (not pre-existing): `veto_idiom` tmp-aliasing (`is_no` flag), `antonym()` `"activ"`→`"active"` key error, scratch-region collisions (`DENYA`/`CLVSB`, `CADJB` carve).

## 9. Caveats / judgment calls

- Rows 76/244 ("nowhere states that X" → DENY): absence-of-statement is weaker than outright denial, but treating matrix negation of a reporting verb as DENY is consistent with NEG-13 and the old AFFIRM was unambiguously wrong.
- `lhedge` uses the stream's last non-space byte; a trailing "?" hedges the whole stream even if earlier clauses endorse (conservative; only the 4 quora rows were affected in 382).
- The old literal `"no longer"` substring rule is fully replaced by the polarity-aware token rule; any "no longer <w>" with unrelated `<w>` now yields NEUTRAL rather than DENY (intended — the old rule was polarity-blind).
