# C501/C502 — B17 BLAST RADIUS, REMEDIATION, AND INVALIDATION

Lane `b17fix`. Classifier is `ptr_guard.zag` (pure Zag, comment- and
string-literal-aware, self-tested). Counts below are from the guard plus a
fixed-string cross-check; the two agree.

## 1. THE TRUE BLAST RADIUS

Corpus: **1036** git-tracked `.zag` files under `overnight-20260928/`.
Textual `as *u8` occurrences: **829**. Code-level `as *u8` occurrences: **760**.

| class | occurrences | files | verdict |
|---|---|---|---|
| **SAFE** — `_zag_malloc(n) as *u8` | 514 | 473 | canonical allocator idiom (brief 3.1) |
| **SAFE** — `null as *u8` | 222 | 219 | canonical null-check idiom (brief 5) |
| **SUSPECT** — `(lo\|(hi<<32)) as *u8` | 8 | 2 | integer reconstruction; fed by `_zag_slice_ptr` on the store side. Sound. Allowlisted. |
| **CORRUPT** — `slice as *u8`, dereferenced | **5** | **4** | all 5 are the defect **reproducers** |
| **CORRUPT** in the research corpus | **0** | **0** | — |

Files containing a code-level `as *u8`: **474**. Of those, **468 contain only
the two SAFE forms.** The 6 that do not are the 4 reproducer files and the 2
`gen_cogops_unify` glue files.

### The 320 figure is wrong, and wrong in an instructive way
`lane/tcdefects` reported "**320 of 1064** `.zag` files contain a
`<identifier> as *u8` cast", naming `l3_suf_scaling` (19),
`l2_metareuse_compose2` (11), `ns_invariant` (9) as highest-count audit targets.

Those counts are real; their **interpretation is inverted**. Each is a count of
files containing the *safe* forms, not the defective one:

| lane | files w/ `as *u8` | files w/ `_zag_malloc..as *u8` | files w/ a PROHIBITION comment | non-canonical casts |
|---|---|---|---|---|
| `l3_suf_scaling` | 19 | **19** | **19** | **0** |
| `l2_metareuse_compose2` | 11 | **11** | 0 | **0** |
| `ns_invariant` | 9 | **9** | 0 | **0** |
| `l2_metareuse_adversary` | 8 | **8** | 0 | **0** |

`l3_suf_scaling` — the lane flagged as the worst offender — has **all 19** files
carrying the canonical `_zag_malloc as *u8` idiom **and all 19** carrying an
explicit prohibition header: ``// never `as *i32` + slice, never `[]u8 as *u8` ``.
**The lane with the highest count is the lane that most explicitly forbids the
construct.** It is evidence of compliance, not of exposure.

Two further consequences:
* **A text grep for this pattern is dominated by prose.** Every one of those
  prohibition headers, and all **31** `as *i32` occurrences in the corpus (which
  are *also* all comments — there is no `[]u8 as *i32` code anywhere), are hits.
  This is why `ptr_guard` strips comments and string literals before
  classifying, and why its self-test pins a comment-only fixture.
* **`lane/tcdefects`'s own claim that its grep "deliberately excludes the
  legitimate `_zag_malloc(n) as *u8` form" did not hold.** Excluding that form
  still leaves 474 files, because `null as *u8` (222 sites) and the malloc form
  dominate every file. The exclusion was not applied.

## 2. ARE ANY PUBLISHED RESULTS INVALID? — NO

**No completed experiment requires downgrade or re-run.** The reasoning is
structural, not statistical:

* Zero CORRUPT sites exist outside the reproducer programs. A lane whose
  published numbers came from code that never performs `slice as *u8` cannot
  have been corrupted by it.
* The reproducer programs' only "results" **are** the defect evidence
  (`7 -> 8`, `7 -> 0`). Those are correct and are what filed B17.
* Per the mission's own conservatism bar — *nondeterminism in an unused path is
  not a result defect* — the `gen_cogops_unify` integer-reconstruction sites
  are SUSPECT, not CORRUPT, and are load-bearing but sound: the store side uses
  `_zag_slice_ptr` (`gu_glue.zag:62`, `gu_full.zag:472`), so the addresses
  being rebuilt are genuine data pointers.
* Independent corroboration: brief §4.1 already showed a 340 KB flat-arena
  program (`c8_full.zag`) reproducing **byte-identically** on this host. Indexed
  reads through properly-constructed slices are not miscompiled.

The frozen cores, the canonical scaling results, the L3/composition claims and
the belief lane are **all untouched**. This is a toolchain finding with a
narrow blast radius, not a corpus-wide invalidation.

## 3. REMEDIATION APPLIED

* **No published lane source was modified.** Consequently **no historical hash
  in the ledger goes stale** — there is nothing to disclose. The 5 CORRUPT sites
  were deliberately left in place: they are the reproducers, and removing the
  construct from them would destroy the evidence for B17.
* **Detector installed** (`ptr_guard.zag` + `ptr_guard.sh` + `ptr_guard.allow`)
  — see `PTR_GUARD.md`. Corpus scan: 1036 files, SAFE 740, SUSPECT 0,
  CORRUPT 0, pinned 5. Deterministic 3/3 byte-identical.
* **Correct constructs, for the record:** address of an existing slice is
  `_zag_slice_ptr(b)` (as `i64` for a syscall argument); null-terminated syscall
  strings are `z_cstr(s)`. The only legitimate `*u8` sources are
  `_zag_malloc(n) as *u8` and `null as *u8`.
* **`getc32`/`setc32`:** not needed here. Those guarded wrappers address the
  separate `get32`/`set32` byte-offset trap, and since no CORRUPT site exists
  there is nothing to route through them. They remain available from
  `tcdefects/C10_guarded_wrappers.zag`; adopting them is a separate decision.

## 4. C502 — CORRECTION TO THE RECORD

`lane/tcdefects` §6 "Blast radius" should be amended: the count of candidate
files is **0 in the research corpus** (5 sites, 4 files, all reproducers), not
320. Its triage rule — *`let q:*u8 = <slicevar> as *u8;` is always a bug* — is
correct and is what `ptr_guard` implements; only the enumeration feeding it was
wrong. Its other conclusions (defect real, `_zag_slice_ptr` is the fix) stand
and were re-verified independently here (9/9, 3/3, 5/5).
