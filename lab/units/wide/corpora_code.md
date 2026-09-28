EXPLORATORY — NOT EVIDENCE

# Wide track: non-C code corpora — selection, license verification, characterization

Nothing in this document counts as program evidence. It is exploratory
groundwork for the representation program's wide track: five code corpora in
languages other than C, each pinned to an exact version, license-verified by
quoting the governing license text, measured at the byte level with pure-Zag
tooling, plus informational transfer-probe designs. No corpora were committed
to the repo; fetch outputs live only in ephemeral `/tmp`.

## 1. Selected corpora

| # | Language | Source | Pinned version | Subtree (test suites excluded) | Files | Bytes | SHA-256 (corpus file) |
|---|----------|--------|----------------|-------------------------------|-------|-------|----------------------|
| 1 | Python | CPython (python/cpython) | v3.14.7 | `Lib/**/*.py` minus `Lib/test/` | 721 | 12,210,912 | `b15ef969…2af73` |
| 2 | Lua | luvit/luvit | 2.18.1 | `deps/**/*.lua` + `init.lua`, `main.lua`, `package.lua` (tests/examples/bench excluded) | 48 | 311,751 | `e8626221…785e4a` |
| 3 | JavaScript | nodejs/node | v26.9.0 | `lib/**/*.{js,mjs}` | 420 | 5,624,616 | `bb79d8d6…84902e4` |
| 4 | Rust | serde (crates.io) | 1.0.229 | `src/**/*.rs` | 24 | 535,530 | `c8d46ca4…89bd130d` |
| 5 | Go | golang/go | go1.27.1 | `src/{encoding/json,fmt,strings}/**/*.go` minus `*_test.go` | 61 | 845,270 | `3a49f439…510038cc` |

Full hashes and tarball hashes are in the fetch manifest
(`/tmp/code-corpora/MANIFEST.txt`, ephemeral). Corpus files are the
deterministic concatenation of the listed members in `LC_ALL=C` sorted path
order, each file appended verbatim with at-least-one trailing `\n` enforced,
so concatenation does not depend on upstream trailing newlines.

Why these five: they span the structural spectrum the transfer probes need —
brace+semicolon languages (JS, Rust, Go) for near-transfer from C, and
non-brace languages (Python: indentation; Lua: `end`-delimited) for far
transfer. Assembly (musl) was investigated and dropped for this round: no
clean single-subtree assembly corpus with unambiguous licensing was verified
in the time available; it remains a candidate for a follow-up.

## 2. License verification (governing text quoted, coverage explained)

Each license file below was fetched directly from the pinned tag/commit and
read in full. SPDX metadata alone was not accepted (TinyStories precedent).

**Python — PSF License 2.1** (`https://raw.githubusercontent.com/python/cpython/v3.14.7/LICENSE`).
Covers `Lib/`: the LICENSE's grant clause names "Python" as "this software …
in source or binary form and its associated documentation", and the stdlib
ships inside the same release tarball under that agreement. Quote:

> PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
> 1. This LICENSE AGREEMENT is between the Python Software Foundation
> ("PSF"), and the Individual or Organization ("Licensee") accessing and
> otherwise using this software ("Python") in source or binary form and
> its associated documentation.
> 2. Subject to the terms and conditions of this License Agreement, PSF hereby
> grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
> analyze, test, perform and/or display publicly, prepare derivative works,
> distribute, and otherwise use Python alone or in any derivative version…

Verdict: GRANTED for analysis, measurement, and derivative statistics.

**Lua — Apache License 2.0** (`luvit` tag `2.18.1`, file `LICENSE.txt`).
The repository root carries the standard Apache-2.0 text; it governs all
files in the repo including `deps/`. Quote:

> Apache License
> Version 2.0, January 2004
> http://www.apache.org/licenses/
> TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
> 1. Definitions. …

Verdict: GRANTED (Apache-2.0 §§2–4 cover reproduction and analysis).

**JavaScript — MIT (Node.js)** (`nodejs` tag `v26.9.0`, file `LICENSE`).
The file opens by scoping itself to the whole distribution:

> Node.js is licensed for use as follows:
> """
> Copyright Node.js contributors. All rights reserved.
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to
> deal in the Software without restriction, including without limitation the
> rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
> sell copies of the Software…

`lib/` is part of "this software". Verdict: GRANTED.

**Rust — dual MIT / Apache-2.0 (serde 1.0.229).** The `.crate` tarball ships
both `LICENSE-MIT` and `LICENSE-APACHE`; `Cargo.toml` declares
`license = "MIT OR Apache-2.0"`. Either license alone suffices. MIT quote:

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software…

Verdict: GRANTED under either; analysis uses the MIT prong.

**Go — BSD-3-clause-style** (`golang` tag `go1.27.1`, file `LICENSE`).
Single short license at repo root covering `src/`. Quote:

> Copyright 2009 The Go Authors.
> Redistribution and use in source and binary forms, with or without
> modification, are permitted provided that the following conditions are
> met:
> * Redistributions of source code must retain the above copyright
> notice, this list of conditions and the following disclaimer. …

Verdict: GRANTED for analysis and redistribution of derived statistics
(notice-retention condition applies to redistributed source, not to
measurements).

Rejected candidates: `tarantool/tarantool` (GitHub license metadata
`NOASSERTION` — rejected per the no-ambiguity rule), `prosody/prosody`
(repository lookup failed — rejected unverified), musl assembly (exact
release/subtree/license triple not verified this round — parked, not rejected).

## 3. Fetch method

`units/wide/fetch_code_corpora.sh` (in-repo, corpus-free). It downloads the
five pinned tarballs (URLs + sha256 recorded in the manifest), extracts ONLY
the listed members (never the full trees — the Node tarball is 127 MB and
/tmp is a 512 MB tmpfs), and builds each corpus deterministically as described
in §1. It refuses to write inside the repo. Rerunning it with the same
tarballs reproduces the corpus files byte-for-byte (sha256-checked).

Rule-interaction note (not an amendment proposal): the track task explicitly
says "write fetch scripts" while the frozen law requires pure Zag for
*executable analytical work*. Fetch is data acquisition, not analysis — Zag
has no TLS/network stack, so the fetch script is POSIX shell by necessity and
the *analysis* (`charz.zag` below) is pure Zag. If Micah reads the frozen rule
more broadly, this becomes an amendment proposal; until then it is documented
as the working interpretation.

## 4. Characterization method

Two tools, both deterministic (byte-identical reruns verified):

- **`units/wide/charz.zag`** (new, pure Zag): single-pass lexer per language
  mode (`python | lua | javascript | rust | go | asm`). Emits byte counts in
  three buckets (code/comment/string), a 256-entry byte histogram, bracket
  nesting depth (`()`, `[]`, `{}` tracked separately, sampled per code byte;
  depth histogram in 64 bins), and identifier statistics via a deterministic
  FNV-1a 64 open-addressed table (524,288 slots): total occurrences, distinct
  count, top-40 by frequency with deterministic tie-break (count desc, slot
  asc). Output is `KEY value` lines; reruns are byte-identical (verified on
  the 12 MB Python corpus — only the corpus label line differs, as intended).
- **`units/wide/char_prose.zag`** (pre-existing): byte-class stats and the
  token-ish repetition estimate — 8-byte windows at stride 16 hashed into a
  65,536-slot table; `REP_EXTRA_PERMILLE` = permille of sampled windows that
  repeat a previously seen window (i.e. near-duplicate 8-byte sequences).

Lexer approximations (documented in `charz.zag`'s header; determinism is
unaffected): multi-byte openers split across the 1 MiB read-chunk boundary are
not re-examined (~1e-6 probability per closer); Python `r""` prefixes are not
special-cased; Rust/Go char literals recognized only as `'x'`, `'\e'`,
`'\u{…}'` (lifetimes like `'a` count as code); Rust raw identifiers lex as
ident + `#` + ident; JS template `${}` interpolation is not tracked (the
template runs to its closing backtick honoring backslash escapes); asm covers
`#`/`;` line comments and `/* */` blocks only.

## 5. Results

All numbers below are measured on the exact corpus files in §1
(sha256-pinned). Ratios are permille (‰) of total bytes.

### 5.1 Byte-bucket ratios (code / comment / string)

| Corpus | Bytes | Code ‰ | Comment ‰ | String ‰ | Lines | Mean line len |
|--------|------:|-------:|----------:|---------:|------:|--------------:|
| python | 12,210,912 | 554 | 162 | 283 | — | 35 |
| lua | 311,751 | 696 | 250 | 53 | — | 24 |
| javascript | 5,624,616 | 519 | 162 | 318 | — | 28 |
| rust | 535,530 | 710 | 269 | 20 | — | 30 |
| go | 845,270 | 508 | 452 | 39 | — | 31 |

Read it as: **comment density is project culture, not language.** Go's 452‰
is the famous Go doc-comment discipline in `encoding/json`+`fmt`+`strings`;
Rust's 269‰ is serde's heavy doc-comments; Lua's 250‰ is luvit style. The
string-ratio extremes are structural: Python's 283‰ is docstrings
(triple-quoted strings ARE strings to the lexer, correctly), JS's 318‰ is
template literals and message strings in Node's lib. A C-trained
comment/string segmenter that assumes "comments are rare" (sqlite3.c is
~low-single-digit percent comments) will be badly miscalibrated on Go and
Python — this is exactly what Probe A tests.

### 5.2 Nesting depth (brackets only: `()`, `[]`, `{}`)

| Corpus | Max depth | Mean depth | Depth histogram shape |
|--------|----------:|-----------:|----------------------|
| python | 8 | 0.34 | 0:4.7M 1:1.7M 2:228k 3:24k 4:3.3k … — shallow, paren-only |
| lua | 5 | 0.32 | 0:159k 1:47k 2:9.6k 3:1.1k … — shallowest |
| javascript | 23 | 6.10 | bimodal: peaks at 5–6 AND 14–15, tail to 23 |
| rust | 12 | 2.57 | 0:28k 1:83k 2:100k(peak) 3:68k … 12:15 |
| go | 10 | 2.38 | 0:35k 1:104k 2:111k(peak) 3:77k … 10:33 |

Python and Lua barely nest *brackets* (their block structure is
indentation/`end`, invisible to a bracket counter) — mean depth 0.3. The brace
languages nest 7–18× deeper on average. JS is the outlier: max depth 23 with a
second hump at depths 14–15 (deeply nested conditionals/callbacks in Node's
lib). Any C-learned nesting prior (sqlite3.c nests braces deeply) transfers
natively to JS/Rust/Go and has *nothing to attach to* in Python/Lua — the
cleanest predicted dissociation in the probe set.

### 5.3 Repetition

**Byte-level** (`REP_EXTRA_PERMILLE`, 8-byte windows stride 16):

| Corpus | REP_EXTRA ‰ | WS ‰ | Max line len |
|--------|------------:|-----:|-------------:|
| python | 337 | 308 | 175 |
| lua | 295 | 231 | 153 |
| javascript | 407 | 220 | 609 |
| rust | **562** | 301 | 141 |
| go | 293 | 200 | 181 |

**Identifier-level** (from `charz`):

| Corpus | Ident occurrences | Distinct | Distinct/occ | Top-1 ident (share) |
|--------|------------------:|---------:|-------------:|---------------------|
| python | 573,490 | 28,969 | 5.1% | `self` 54,611 (9.5%) |
| lua | 26,246 | 1,589 | 6.1% | `end` 1,892 (7.2%) |
| javascript | 229,980 | 13,259 | 5.8% | `const` 10,368 (4.5%) |
| rust | 35,006 | 1,015 | **2.9%** | `self` 1,592 (4.5%) |
| go | 50,900 | 2,455 | 4.8% | `return` 2,159 (4.2%) |

Rust/serde is the most repetitive corpus on both measures (562‰ byte
repetition, only 2.9% of identifier occurrences are distinct) — the signature
of generated-feeling `impl` blocks: `self`, `de`, `Error`, `E`, `fn`,
`Self`, `Result`, `where`, `Ok`, `Value` dominate. Python's top idents read
like a language fingerprint: `self if def return None not in is else`.

### 5.4 Top bytes (all corpora)

Byte 32 (space) is #1 everywhere (19–28% of bytes); `e`, `t`, `a`, `n`, `r`,
`s`, `i`, `o` round out the top 8 in every corpus — the Latin-letter
dominance is language-independent. The first byte that distinguishes corpora
is structural punctuation, and it arrives at different ranks per language
(e.g. `(` / `)` / `;` / `=` / `.` ordering differs between the brace
languages and Python/Lua). Full `TOP_BYTE` lists are in the raw outputs
(ephemeral `/tmp/rz_*.txt`); the pattern to carry forward is that the
*letter* distribution is near-universal while the *punctuation* distribution
is syntax-specific.

## 6. The interesting bit (for the parent's handoff)

Three dissociations fall out of the tables without any modeling:

1. **Letters are universal, punctuation is parochial.** The top-8 bytes are
   the same letters in all five corpora; what differs is structural
   punctuation rank-order. A C-trained byte policy should therefore transfer
   its letter/identifier machinery everywhere and its punctuation/delimiter
   machinery only to brace languages.
2. **Nesting depth is the sharpest C→X variable.** Mean bracket depth spans
   0.32 (Lua) to 6.10 (JS) — a 19× range. If a frozen C policy's nesting arm
   transfers to JS/Rust/Go but goes inert on Python/Lua, that is evidence the
   nesting machinery learned *syntax*, not *structure*.
3. **Comment density is the calibration trap.** 162‰ (Python/JS) to 452‰
   (Go). Any fixed comment-prior from C will misfire somewhere in this set —
   the probes must measure segmentation calibration per corpus, not just
   aggregate accuracy.

## 7. Transfer probe designs (informational only — no frozen bars touched)

These probes use the corpora above as *test* material for policies trained on
the frozen main corpora (sqlite3.c for code). They are measurement-only:
they may inform a future amendment proposal, they change nothing frozen.

### Probe A — Frozen C policy, zero-shot cross-language transfer

*Question.* Which regularities learned from C are language-general, and which
are C-syntax priors?

*Method.* Take the representation program's trained C policy (whatever its
current form — parameters frozen, learning disabled). Run it inference-only
over each of the five corpora. Score three sub-tasks against `charz`'s
deterministic lexer as ground truth:
  (a) **Segmentation**: per-byte code/comment/string classification —
      report per-class F1 *per corpus* (the Go/Python comment-density trap
      makes aggregate accuracy misleading).
  (b) **Identifier repetition**: rank-correlation between the policy's
      predicted next-identifier distribution and the measured identifier
      frequency table (Spearman on the top-1k idents per corpus).
  (c) **Nesting**: predicted vs measured bracket-depth histogram distance
      (L1 on the 64-bin distribution).
*Baselines.* (i) Chance/uniform; (ii) a corpus-marginal baseline (predict each
corpus's own marginals — separates "learned structure" from "matched
statistics"); (iii) per Micah's test-both law, ALSO run the mirror: freeze a
policy trained on Python and zero-shot it to C — asymmetry localizes
direction of generality.
*Predicted dissociation.* (b) transfers everywhere (letters universal);
(a) miscalibrates on Go/Python comments; (c) transfers to JS/Rust/Go, goes
inert on Python/Lua. Any deviation from this pattern is the finding.

### Probe B — Component ablation across languages

*Question.* If transfer fails, *which arm* failed?

*Method.* Decompose the C policy into three arms — identifier/repetition
machinery, delimiter/nesting machinery, comment/string segmentation — and
transfer each arm **alone** (other arms zeroed or replaced by the
corpus-marginal baseline) to each corpus. 3 arms × 5 corpora = 15 cells, each
scored on the matching sub-task from Probe A. Add the full-policy transfer
cell and the no-transfer (from-scratch on target) cell per corpus.
*Reads.* If the identifier arm transfers everywhere but the nesting arm only
to brace languages, the arm family — not the policy — is the unit of
generality, and future architecture work should make the nesting arm
syntax-parameterized rather than syntax-bound. If the segmentation arm fails
specifically where comment density diverges from C (Go 452‰), the fix is a
density-adaptive prior, not a better segmenter.
*Cost control.* All 15+10 cells are inference-only (no training), so the
matrix is cheap; the from-scratch cells reuse the program's existing training
harness unchanged.

### Probe C (optional, cheap) — Repetition-prior universality check

Fit a Zipf exponent to each corpus's identifier frequency table and to the
8-byte-window repetition curve. If the exponents cluster across all five
languages (and Shakespeare/sqlite3.c), the repetition prior can be a frozen
universal; if Rust/serde is an outlier, the prior needs a
burstiness/repetitiveness parameter. Pure measurement, no policy involved —
do it first, it costs one script.

## 8. Limitations and honest gaps

- Lexer approximations listed in §4; the largest known bias is JS template
  `${}` interpolation (nesting not tracked — string bytes slightly
  over-counted in template-heavy files) and Python `r""` prefixes (rare).
- Corpus scope choices are judgments: CPython minus `Lib/test`, luvit
  `deps/`+roots (not tests/examples/bench), Go only three packages, serde as
  the Rust representative (a derive-heavy crate — NOT typical Rust; the 562‰
  repetition is a serde property first, a Rust property second).
- Single pinned version each; drift over versions unmeasured.
- `charz`'s identifier table (524,288 slots) is ample here (max 28,969
  distinct) but the table-full drop path is untested.
- Raw tool outputs live in ephemeral `/tmp` (`rz_*.txt`, `rp_*.txt`,
  `/tmp/code-corpora/`); rerunning `fetch_code_corpora.sh` + `charz`
  reproduces everything deterministically.

## 9. Files

- `units/wide/charz.zag` — pure-Zag byte-level code characterizer (new).
- `units/wide/fetch_code_corpora.sh` — deterministic fetcher (new; writes
  only outside the repo, refuses repo paths).
- `units/wide/corpora_code.md` — this document.
- Pre-existing `units/wide/char_prose.zag` used for byte-class/repetition
  stats; not modified.
