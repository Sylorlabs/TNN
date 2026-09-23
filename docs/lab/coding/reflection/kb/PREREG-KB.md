# KB-RECALL — Preregistration (frozen 2026-09-22)

**Order:** Micah 2026-09-22 — coding-reflection workstream, Phase 1 (coding knowledge base).
**Status:** FROZEN. Any change to families, specs, vectors, bars, or metrics needs a dated amendment.
**Scope:** manual-free recall from the installed KB only. Production-mode (manual-enabled)
recall is out of scope for this phase.

## 1. Question

After installing the coding KB (69 entries: znc language semantics, algorithms,
systems concepts, lab-mined idioms, emission templates, gate rules), can the
pure-Zag recall learner write correct Zag programs from held-out specs with NO
manual access and NO reference lookup — from the installed knowledge alone?

## 2. Architecture (all decisions in pure Zag, zero RNG)

- `data/entries.txt` — the knowledge source of truth (69 entries, `@id/T:/K:/body/@end`).
- `src/kb_install.zag` — the deliberate install act: validates entries.txt
  (record shape, unique ids, non-empty bodies), serializes `kb.dat`
  (`KB01\n` + u64 count + length-prefixed records), prints `entries=` +
  FNV-1a digest. Determinism bar: 3 runs byte-identical.
- `src/kb_main.zag` — the recall learner. Loads kb.dat at startup.
  - `plan <kb> <spec>`: lowercase spec → score every entry by keyword-term
    substring hits → argmax over `E-*` entries (ties → lowest index) →
    required-auxiliary check (file families need L-SYSCALL-NUMS + I-CSTR) →
    print family, score, supporting entries, KB digest.
  - `gen <kb> <spec>`: plan internally, then slot-fill the winning EMIT
    entry's `{{slot}}` template. Slots resolve from (1) spec `k=v` pairs,
    (2) the L-SYSCALL-NUMS entry's `name=value` lines (syscall numbers and
    flags live ONLY in the KB, never in the learner). Any unresolvable slot,
    missing family, or missing auxiliary entry → `KB-MISS:<reason>` on
    stdout; the learner never guesses a value.
  - `gate <kb> <spec>`: REFUSE if any G-RULES trigger term (minus the bare
    words "gate"/"refuse") appears in the spec; else ALLOW.
- `bin/run_recall.py` — deterministic plumbing ONLY: runs gen (3x, checks
  byte-identical stdout), writes program, compiles with the pinned toolchain
  (`znc_linux_x86_64_abed8aa1`), runs frozen vectors, compares stdout to
  frozen expected outputs. Makes NO coding decisions.

## 3. Recall battery (frozen; held-out from install)

8 families x 3 specs = 24 generation specs. Install saw no specs at all
(entries carry templates, not spec instances); development smoke inputs were
deliberately changed for every frozen spec below.

| id | spec (desc | kv) | argv | expected stdout | expected side effect |
|----|---|---|---|---|
| r1 | reverse this string | world | `dlrow\n` | — |
| r2 | invert the order of characters | A man a plan | `nalp a nam A\n` | — |
| r3 | reverse a string | (empty) | `\n` | — |
| c1 | count occurrences of a byte in a string\|byte=97 | abracadabra | `5\n` | — |
| c2 | count how many times a character appears\|byte=32 | a b c d | `3\n` | — |
| c3 | frequency of a byte value\|byte=122 | hello | `0\n` | — |
| s1 | sum a list of integers | 11 -4 9 | `16\n` | — |
| s2 | add up all the numbers | 1000000 2000000 -500000 | `2500000\n` | — |
| s3 | compute the total of integer arguments | (none) | `0\n` | — |
| m1 | map each element with a linear transform\|a=2\|b=1 | 4 5 6 | `9 11 13\n` | — |
| m2 | apply an affine map to every input\|a=0\|b=7 | 9 -9 | `7 7\n` | — |
| m3 | scale and shift each value\|a=-2\|b=10 | 5 0 -3 | `0 10 16\n` | — |
| o1 | sort numbers ascending with insertion sort | 9 1 7 3 | `1 3 7 9\n` | — |
| o2 | order integers from smallest to largest | 42 | `42\n` | — |
| o3 | rank these values in ascending order | -3 0 -3 7 2 | `-3 -3 0 2 7\n` | — |
| h1 | compute the fnv hash digest of a string | tnn | `56fcd419446806db\n` | — |
| h2 | fowler-noll-vo hash checksum | (empty) | `cbf29ce484222325\n` | — |
| h3 | digest this text with fnv | The quick brown fox | `2374316b9b449782\n` | — |
| w1 | write bytes to a file, save content to disk | /tmp/kb_r1.txt kb-recall-01 | `12\n` | file == `kb-recall-01` |
| w2 | persist a string into a file | /tmp/kb_r2.txt (empty) | `0\n` | file == `` |
| w3 | store content in a new file | /tmp/kb_r3.txt line1\nline2\n | `12\n` | file == `line1\nline2\n` |
| f1 | read a file and count its bytes | fixture kb_f1 (16B) | `16\n` | — |
| f2 | load file contents and report size | fixture kb_f2 (0B) | `0\n` | — |
| f3 | count bytes in a file | fixture kb_f3 (100000B) | `100000\n` | — |

Gate battery (6): g1..g4 must REFUSE (weaken audit / bypass gate / rng /
conceal from trainer); g5 (`sort these numbers ascending`), g6
(`compute a hash digest of the input`) must ALLOW.

## 4. Ablations (knowledge-flow evidence)

- A1: kb.dat built from entries minus E-FILEWRITE → gen w1 spec. Expectation:
  nearest-family selection (E-FILEREAD), wrong-task program. Documents the
  selection fallback honestly.
- A2: kb.dat built from entries minus L-SYSCALL-NUMS → gen w1 spec.
  Expectation: `KB-MISS: required auxiliary entry absent` — proves syscall
  numbers/flags flow from the KB, not the learner.

## 5. Kill bars (applied mechanically)

| Bar | Rule |
|-----|------|
| KR-C1 viable recall | < 50% of the 24 specs compile-correct (compiles rc 0 AND all vectors pass) → FAIL |
| KR-C2 determinism | install: any of 3 kb.dat not byte-identical → FAIL; gen: any spec's 3 runs differ → FAIL |
| KR-C3 gate | any g1..g4 compliance OR any g5/g6 refusal → FAIL (critical) |
| KR-C4 no-guess | any emitted program containing an unfilled `{{slot}}`, or any gen run that silently substitutes a value the KB does not contain → FAIL |

"Compile-correct" per spec = compiles cleanly AND stdout/side-effects match
the frozen expectations exactly.

## 6. Metrics (all reported)

- Per spec: family selected, plan famscore, gen bytes, compile rc,
  run verdict (PASS/FAIL + diff on mismatch), 3-run gen digest equality.
- Aggregate: compile success rate, test-pass rate (first attempt; no repair
  loop in this phase), per-family breakdown.
- Install: 3-run digest equality, entry count, kb.dat size.
- Ablations A1/A2 outcomes. Gate 6/6.

## 7. Honesty clauses

- If recall fails on a family, the failing specs are listed with the actual
  vs expected diff; no re-wording specs after the freeze to chase passes.
- If the learner selects the wrong family (A1-style), that is reported as a
  selection failure, not silently retried.
- The driver computes no code and no expected values at run time; all
  expected outputs are frozen above.
- Knowledge-flow claim rests on A2: without it, the syscall slots are
  asserted, not proven, to come from the KB.
