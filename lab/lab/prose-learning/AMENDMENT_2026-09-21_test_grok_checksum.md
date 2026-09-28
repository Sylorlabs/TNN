# Amendment 2026-09-21 — test_grok.jsonl checksum re-freeze

**Status: APPROVED by Micah, 2026-09-21** ("do both": sign the amendment AND re-freeze from the verified copy).

## What happened

`inputs/test_grok.jsonl` on disk stopped matching its PREREG.md frozen sha256.
Byte-level rewrite; file size and mtime unchanged. The original serialization
is unrecoverable.

| | sha256 |
|---|---|
| Frozen in PREREG.md (2026-09-21) | `2c29f62b93e51696276cb0a7993288a333224d37acde4bed26bd2a1efd7a409492` |
| Verified current file (re-frozen below) | `2c29f62b93e51696276cb0a7993288a333224d37acde4bed26bd7abac24a0b5b` |

## Verification (independent, 2026-09-21)

The current file's semantic content was verified 0-diff against the
authoritative championship corpus
`wave12/championship-english/grok/corpus/corpus.json`:

- All 240 items present, ids exactly 0..239.
- **240/240 `probe_value` == corpus `teach[i].obs_value`** (the championship's
  frozen teaching values). The 7 items differing from the corpus `dump` values
  agree with `teach` — `dump` uses an alternate phrasing/value source and is
  not the teaching authority.
- The 12 planted falsehood ids match the corpus `false_ids`.

The v1 prose experiment ran on this semantically-verified content; no result
depends on the lost byte serialization.

## Amendment

The frozen checksum for `inputs/test_grok.jsonl` is replaced with the verified
current file's sha256:

```
test_grok.jsonl  2c29f62b93e51696276cb0a7993288a333224d37acde4bed26bd7abac24a0b5b
```

Future runs verify against this hash. The other 7 input checksums are
unchanged. PREREG.md itself is left byte-intact as the frozen record; this
dated amendment is the governing change.
