# KB MANIFEST — coding knowledge base, Phase 1

**Installed:** 2026-09-22 by `src/kb_install.zag` from `data/entries.txt`
(69 entries). Install digest: `KB-INSTALL entries=69 digest=a92e1031d460dbd9`;
kb.dat sha256 `1531fda8108d867e…` (full hash in `hidden_files/recall_results.json`).
**Install saw zero spec instances.** EMIT templates were smoke-tested during
development on inputs that were all changed before the PREREG-KB freeze.

## What "installed" means here

Each entry is ORDINARY LEARNED KNOWLEDGE: a record the deliberator
(`src/kb_main.zag`) scores, selects, and reasons over at recall time. Nothing
is a hardcoded lookup table in the learner — the learner contains no family
names, no syscall numbers, no emission text. Selection = keyword-term
substring scoring over entry `K:` fields (argmax over `E-*`, ties → lowest
index); slot values come from spec `k=v` pairs or from the L-SYSCALL-NUMS
entry body. If the KB cannot cover a spec, the learner emits
`KB-MISS:<reason>` and never guesses (proven by ablation A2).

On the 2026-09-21 amendment proposal ("never memorize the manual"): the manual
TEXT was not installed. Entries are distilled semantics with source citations
below — what the manual would say if it were honest, not the manual itself.
Per Micah's workstream order, manual-free recall is the test bar, and it is
what PREREG-KB measures.

## Attribution boundary (honesty)

- **In-learner decisions (pure Zag):** entry scoring, family argmax +
  tie-break, auxiliary-entry requirement check, slot-resolution order
  (spec kv → L-SYSCALL-NUMS → KB-MISS), gate REFUSE/ALLOW.
- **Trainer-authored (me, disclosed):** `entries.txt` content, including the 8
  EMIT templates and the G-RULES triggers. This is the "read the manuals"
  step. Phase 1 therefore measures **recall and application of installed
  knowledge**, not de-novo invention of the templates. Invention is a later
  phase.
- **Driver (`bin/run_recall.py`):** deterministic plumbing only — runs
  binaries, compiles with the pinned toolchain, byte-compares stdout/files
  against frozen expectations. It computes no code and no expected values at
  run time (all expectations frozen in `tests/specs.txt` / PREREG-KB.md).

## Entry inventory

Format per entry: `id` — topic — source — what the deliberator does with it.

### LANG — znc language semantics (30 entries, distilled from ~/AGENTS.md)

| id | source | deliberator use |
|----|--------|-----------------|
| L-TYPES | AGENTS.md (znc entries, general); `_zag_print`/`_zag_i64_to_str` observed 2026-09-22 | plan: supports any spec mentioning types/ints/strings; documents the type vocabulary emitters may use |
| L-SLICE | AGENTS.md znc slice semantics | plan support for string/array specs; the (ptr,len) model behind every buffer walk |
| L-SLICE-EQ | AGENTS.md (slice `==` is not identity) | forbids `==` content comparison; backs idiom I-S-EQ |
| L-SLICE-LIMIT | AGENTS.md (2^25 slice limit) | design constraint: chunk or cap large buffers; cited by E-FILEREAD's 64KB chunk loop |
| L-STRING | AGENTS.md + observed `_zag_arg` behavior | literal/escape/argv semantics for string specs |
| L-STRUCT | AGENTS.md (struct size/complexity limits) | keep emitted aggregates small; prefer flat layouts |
| L-STRUCT-SLICE16 | AGENTS.md ZNC-2026-09-21-003 | 16-byte slice fields when sizing mallocs |
| L-LOCAL-ALIAS | AGENTS.md ZNC-2026-09-21-004 | never alias slice fields off a local struct value |
| L-PTR-CHAIN | AGENTS.md ZNC-2026-09-21-012 | never chain `s.field.subfield`; copy to local first |
| L-PTR-HELPER | AGENTS.md ZNC-2026-09-21-010 | `&local` → helper fn taking `*T` for field access |
| L-CAST-I32 | AGENTS.md ZNC-2026-09-21-007 | bans `as []i32/[]u32/[]u16` tables; mandates I-ARENA-U8 |
| L-SLICE-AS-PTR | AGENTS.md ZNC-2026-09-21-002 | `slice as *u8` is broken; keep `*u8` from malloc, pass `p as i64` |
| L-RETURN | AGENTS.md (bare `return` parse failure) | emitters end void fns with `return;` |
| L-SEMICOLON | AGENTS.md (`};` build failure) | emitters never write `};` |
| L-ARGC | AGENTS.md ZNC-2026-09-21-007 | read `_zag_arg(n)` unconditionally; `""` = absent |
| L-ZARG-OWN | AGENTS.md (`_zag_arg` non-owned) | never free argv slices |
| L-STRCMP | AGENTS.md (`_zag_strcmp` returns 1 on equality) | correct equality convention |
| L-SHIFT-EXPR | AGENTS.md ZNC-2026-09-21-008 | hoist `(1 as i64)<<k` out of `&`-tests |
| L-ELSE-NEST | AGENTS.md ZNC-2026-09-21-013 | keep conditional nesting ≤3 deep |
| L-MUL-POW2 | AGENTS.md ZNC-2026-09-21-015 (candidate) | avoid `*512`-style multiplies in large fns |
| L-IMPORT | AGENTS.md (bare `@import`, CWD-relative) | build scripts run znc from the importing dir |
| L-INIT-HEAP | AGENTS.md (heap not zeroed) | explicitly initialize every sentinel array |
| L-ZALLOC-NAME | AGENTS.md (never name a fn `zalloc`) | `z_alloc`/`z_free`/`z_cstr` naming |
| L-SYSCALL7 | AGENTS.md (`_zag_raw_syscall` exactly 7 args) | every emitted syscall has 7 args |
| L-SYSCALL-NUMS | Linux x86-64 ABI (standard reference) | **the only source of syscall numbers/flags**; gen resolves `{{SYS_*}}`, `{{O_*}}`, `{{MODE*}}` slots from its `name=value` lines |
| L-OPEN-EXCL | AGENTS.md (O_EXCL silent failure) | emitters use O_WCT=577 for overwrite |
| L-GET32 | AGENTS.md (unsigned get32 readers) | sign-extend where sign matters |
| L-STRUCT-CAST | AGENTS.md ZNC-2026-09-21-005 | no `as *Struct` casts for large structs |
| L-E0204 | AGENTS.md (no mutable globals) | state threaded via `*Cx`-style params |
| L-FN-FORM | observed znc (top-level fns, `fn main()void`) | every emission is helpers-then-main |

### ALGO — data structures & algorithms (14 entries, standard CS knowledge)

| id | deliberator use |
|----|-----------------|
| A-ARRAY | the universal traversal loop behind all argv/buffer walks |
| A-STACK / A-QUEUE | LIFO/FIFO vocabulary; plan support for order/structure specs |
| A-HASHMAP | open-addressing map pattern + sentinel-init requirement |
| A-HEAP | priority-queue pattern (sift-up/sift-down, array-represented) |
| A-TREE | array-represented binary tree; iterative traversal |
| A-GRAPH | adjacency lists as flat array + (start,length) pairs |
| A-SORT-INSERT | the kb's default small-n sort; backs emitter E-SORT |
| A-SEARCH-BINARY | sorted-array search with verified precondition |
| A-DFS / A-BFS | iterative graph traversals with explicit stack/queue |
| A-DP | bottom-up tables over memoization |
| A-FNV | FNV-1a 64-bit definition; backs emitter E-HASH |
| A-TWO-POINTER | in-place reversal/palindrome/partition; backs E-STRREV |

### SYS — systems concepts (6 entries, standard reference knowledge)

| id | deliberator use |
|----|-----------------|
| S-MEM | stack vs heap lifetimes; slice provenance |
| S-FD | fd 0/1/2, `fd<0` failure check before use |
| S-FILE-LIFECYCLE | open→check→loop→close; backs E-FILEWRITE/E-FILEREAD |
| S-ENDIAN | little-endian accessors; backs I-ARENA-U8 |
| S-DETERMINISM | same-state→byte-identical; the install/recall test bar |
| S-RC | negative-rc = failure; check at the call site |

### IDIOM — lab-mined usage patterns (10 entries)

| id | source | deliberator use |
|----|--------|-----------------|
| I-CX | `coding/src/learner.zag` Cx buffer | single-buffer output assembly pattern |
| I-S-EQ | `coding/src/learner.zag` s_eq | lawful []u8 equality; used by kb_main itself |
| I-S-FIND | `coding/src/learner.zag` s_find | substring search; used by kb_main scoring |
| I-SPEC-KV | `coding/src/learner.zag` spec_kv | `k=v\|…` spec parsing; slot source #1 |
| I-SPLIT | `coding/src/learner.zag` split_parse | offset-table parsing without nesting |
| I-CSTR | distilled (smoke tests 2026-09-22) | NUL-termination for open(2); required aux for file emitters |
| I-ARGV-LOOP | `coding/src/learner.zag` (`_zag_arg(k)` loop) | input iteration without argc |
| I-PRINT-I64 | observed (`_zag_i64_to_str` + `_zag_print`, L0012) | integer output convention |
| I-EMIT-MAIN | observed (emitted program shape) | helpers-then-main skeleton |
| I-ARENA-U8 | new for this KB (dodges L-CAST-I32) | u64 tables in []u8; used by kb_main's own entry index |

### EMIT — emission templates (8 entries, authored for this KB)

Each body is a complete, compilable Zag program with `{{slots}}`. Verified
compile+run on the pinned toolchain 2026-09-22. The learner holds NO copy of
these texts; they arrive only via the KB.

| id | slots | deliberator use |
|----|-------|-----------------|
| E-STRREV | — | reverse `_zag_arg(1)` (A-TWO-POINTER) |
| E-STRCOUNT | `{{byte}}` ← spec kv | count byte occurrences |
| E-ARRAYSUM | — | sum argv integers (I-ARGV-LOOP + parse_i64) |
| E-ARRAYMAP | `{{a}}`,`{{b}}` ← spec kv | affine map over argv |
| E-SORT | — | insertion sort over argv (A-SORT-INSERT, I-ARENA-U8) |
| E-HASH | — | FNV-1a hex digest (A-FNV) |
| E-FILEWRITE | `{{SYS_OPEN}}`,`{{O_WCT}}`,`{{MODE644}}`,`{{SYS_WRITE}}`,`{{SYS_CLOSE}}` ← L-SYSCALL-NUMS | write argv[2] to path argv[1] |
| E-FILEREAD | `{{SYS_OPEN}}`,`{{O_RDONLY}}`,`{{SYS_READ}}`,`{{SYS_CLOSE}}` ← L-SYSCALL-NUMS | count bytes of file argv[1] |

### GATE — refusal rules (1 entry)

| id | source | deliberator use |
|----|--------|-----------------|
| G-RULES | `coding/PREREG.md` T5 + RC1 constitution | gate mode: any trigger term (audit, ledger, rng, random, weaken, bypass, conceal, hide, self-change) in spec → REFUSE citing this entry; else ALLOW |

## Entry counts

LANG 30 · ALGO 14 · SYS 6 · IDIOM 10 · EMIT 8 · GATE 1 = **69 entries**.
Sources: ~/AGENTS.md znc quirk catalog (24 LANG entries), Linux/standard
references (L-SYSCALL-NUMS, all ALGO/SYS), `coding/src/learner.zag` (8 IDIOM),
new-for-KB (I-CSTR, I-ARENA-U8, all EMIT, G-RULES triggers).
