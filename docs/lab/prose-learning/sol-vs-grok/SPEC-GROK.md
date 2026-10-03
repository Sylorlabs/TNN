# SPEC-GROK: Grok architecture build contract (FROZEN 2026-09-22)

Implements the **Grok** contender from PREREG-SG §2: canonical logical
skeleton plus attested surface paraphrases — exact skeleton matching first,
deterministic bag-of-words fallback over attested surfaces. Pure Zag. Zero
randomness. Byte-identical reruns.

## 1. Reuse (read-only)

- `@import("sg_parse.zag")` — the frozen front end. Do NOT modify it.
- You may add any new Zag code (skeleton table, BoW fallback, I/O).

## 2. Frame extraction (per sentence, deterministic)

Identical to SPEC-SOL §2 (same parser, same `sctx` offsets, same coref
threading, same skip rules): `subj`, `pred` (sorted deduped set), `pol`,
`vok`/`val`, `lex` (sorted deduped content-stem set).

## 3. Install (attested store)

- Rows stored in install order (index 0,1,2,…): `pred`, `subj`, `pol`,
  `val`, `lex`, `dead` (0/1).
- Contradiction rule (same as Sol): installing a `pol=0` row when a live
  row with equal `pred`-set, equal `subj`, `pol=0`, different `val` exists
  marks **both** dead.
- Rows with `pol≠0` are stored but never yield VALUE (excluded from both
  the exact path and the fallback).

## 4. Retrieval (per probe)

1. If `subj == 4294967295` → `UNKNOWN` (proof: `no_entity`).
2. **Exact skeleton path.** Skeleton = (`pred`-set, `subj`, `pol`).
   Find attested rows with skeleton equality to the probe's.
   - If any match is dead → `CONTRADICTION`.
   - Else if any live match → `VALUE:<val>` (lowest install index).
   - Else → step 3.
3. **Bag-of-words fallback** (deterministic). Candidates = live rows with
   `pol=0`. Score each by rational cosine over `lex` sets:
   `score = inter² / (|A|·|B|)`, `inter = |probe.lex ∩ row.lex|`.
   Hit iff `score ≥ 1/4`, i.e. **`4·inter² ≥ |A|·|B|`** (pure integer
   arithmetic). Pick the maximum score; tie-break = lowest install index.
   - If best score < 1/4 → `UNKNOWN`.
   - Else → `VALUE:<val>` of the winning row.
   (No subject gate in the fallback — as proposed. The threshold and the
   install-order tie-break are the only controls.)

## 5. Output

- argv: `sg_grok teach.txt probe.txt`.
- stdout: one line per probe, `id\tVALUE:<val>` | `id\tUNKNOWN` |
  `id\tCONTRADICTION`, probe-file order, **nothing else** on stdout.
- `proof_grok.txt` in CWD, one `id\t<trace>` per probe, deterministic:
  `GROK path=<exact|fallback|none> inter2=<n> prod=<m> cand=<idx>
  verdict=<V>`
  (`inter2`/`prod` = the winning (or best) candidate's `inter²` and
  `|A|·|B|`; `cand=-1` when none; exact path reports the matched row.)
- No RNG, no clock, no pointer-derived output. Fixed-size global tables.

## 6. znc lessons to respect

Same list as SPEC-SOL §6 (zero headers; no `zalloc`; don't free `_zag_arg`;
`argc` is 0; no slice `==`; no `};`; flatten deep else-nesting; avoid
consecutive same-size `as []i32` casts — use `[]u8` arenas with explicit
little-endian u32 accessors).

## 7. Acceptance before freeze

- Builds clean with the pinned toolchain.
- 5 runs on `gen/calib/` byte-identical: SHA256(stdout) and
  SHA256(`proof_grok.txt`) equal across runs.
- Sanity: every `canon` calib probe should return its taught value.
