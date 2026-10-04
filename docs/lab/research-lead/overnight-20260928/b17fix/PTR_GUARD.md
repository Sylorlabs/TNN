# PTR_GUARD — standing detector for the B17 defect class

Extends the guard family installed by `lane/restores`
(`mint_guard/mint_guard_v2.sh`, the >1000-path-deletion tripwire). Same shape:
a bash driver, an explicit invariant, fail-closed exit codes, and a
`--selftest` that demonstrates the guard actually fires.

## What it forbids

`[]u8 as *u8` is a **REAL COMPILER DEFECT (B17 / C500)**, not a style rule.
The cast yields an address that is not the slice's data pointer. Measured on
this host:

* a literal **7** written into `b[0]` reads back as **8** through
  `(b as *u8)[0..64]` (9/9 runs);
* the same program using `_zag_slice_ptr(b)` reads back **7** (3/3);
* writing 42 through a cast-derived slice turns the original `b[0]` into **0**
  (5/5) — neither the old value nor the new one, so **no aliasing semantics
  explains it**.

The only sound `*u8` sources are `_zag_malloc(n) as *u8` and `null as *u8`.
An existing slice's address comes from `_zag_slice_ptr(b)`.

## Usage

```sh
./ptr_guard.sh                  # scan the corpus, exit 1 on any CORRUPT site
./ptr_guard.sh --selftest       # prove the guard fires (5 fixtures)
./ptr_guard.sh --root PATH      # scan a different tree
./ptr_guard.sh --allowlist PATH # reviewed pins
```

Exit: `0` pass, `1` REFUSED (a CORRUPT site exists), `2` infra error.

## Design

The **analysis is pure Zag** (`ptr_guard.zag`), per the charter. Zag has no
directory-listing builtin, so the bash driver's only jobs are to enumerate the
tree with `find` and hand the scanner a manifest; every SAFE/SUSPECT/CORRUPT
decision is made inside the Zag binary.

Comment- and string-literal-awareness is **load-bearing, not cosmetic**. In this
corpus the overwhelming majority of textual hits for this pattern are PROSE:
prohibition headers like ``// never `[]u8 as *u8` ``, and assertion labels like
`ck("... (b as *u8) ...", ...)`. All **31** `as *i32` hits are likewise comments.
A naive grep therefore reports hundreds of phantom violations — which is how the
`lane/tcdefects` lane arrived at a 320-file blast radius for a defect with zero
occurrences in the research corpus. A guard that cries wolf gets switched off.

Classification of each code-level `as *u8`:
* **SAFE** — operand is `null` or `_zag_malloc(...)`
* **CORRUPT** — operand is a bare slice identifier **and** the bound pointer is
  later dereferenced (`NAME[`)
* **SUSPECT** — any other operand (e.g. integer reconstruction), or a slice
  cast with no deref found

## Allowlist

`ptr_guard.allow` pins reviewed sites as `path<TAB>lineno`, matched as a path
**suffix** so a committed relative-path allowlist works from any worktree. Two
categories are pinned, each with a written justification:

* **(I)** `gen_cogops_unify` — pointer addresses stored as two i32 cells and
  rebuilt as `(lo|(hi<<32))`. The operand is an integer, not a slice, and the
  store side uses `_zag_slice_ptr`. Sound.
* **(R)** the defect reproducer files in `tcdefects/` and this lane. These files
  *are* the demonstration and must contain the construct; pinning them is what
  lets the guard run over the corpus at all.

A pin is a review record, not a suppression. If a pinned file is deleted, its
pins must be deleted too.

## Self-test — 5/5, with exact counts asserted

| fixture | expected rc | CORRUPT | SUSPECT |
|---|---|---|---|
| slice cast + deref | 1 (REFUSED) | 1 | 0 |
| **prohibition comment only** | 0 | 0 | 0 |
| canonical `malloc`/`null`/`slice_ptr` | 0 | 0 | 0 |
| slice cast, never dereferenced | 0 | 0 | 1 |
| mixed good+bad corpus | 1 (REFUSED) | 1 | 0 |

Case 2 is the one a naive-grep guard fails. Counts are asserted, not just exit
codes, because a guard that flags *everything* also exits 0 on clean input.

## Live evidence (this host, `znc --target macos-arm64`)

* **Corpus:** 1036 files — SAFE 740, SUSPECT 0, CORRUPT 0, pinned 5 → **PASS**,
  deterministic **3/3 byte-identical**.
* **In-situ negative control:** a `slice as *u8` + deref was injected into
  `formal_compose_e2e/ex_learner.zag` (a load-bearing composition file). The
  guard reported **CORRUPT 1 → REFUSED**. The file was then restored and
  re-verified **byte-identical** (sha256 `c2a60ef50febcffe`), and the corpus
  scan returned to PASS. This is the evidence that the defect cannot silently
  reappear.
