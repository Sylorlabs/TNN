# Worker byte-check instructions (shell only, no Python)

## Standing rule

Micah's pure-Zag rule is literal: no Python anywhere, including editing,
diagnostics, byte checks, verification, analysis, and scratch work.
The 2026-09-30 governance audit found that 5 of the 6 newest K4 violations
were `python3 -c` invocations used only for em-dash / en-dash byte checks.
Disclosure does not cure use. Do not reach for Python for this.

## The snippet

`check_no_dash.sh` (same directory) checks files for em dash and en dash
byte sequences using only shell and GNU grep.

### Usage

Run from the repo root:

```
sh docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh <file> [file ...]
```

### Exit codes

- 0: every file is clean
- 1: a forbidden byte sequence was found, or a file could not be read
- 2: no file arguments given (usage printed to stderr)

Output lines are `EMDASH-FOUND: <file>`, `ENDASH-FOUND: <file>`, or
`UNREADABLE: <file>`. A clean file prints nothing.

## How it works

- Em dash (U+2014) is the 3-byte sequence E2 80 94 in UTF-8.
- En dash (U+2013) is the 3-byte sequence E2 80 93 in UTF-8.
- The script builds both patterns with `printf '\342\200\224'` and
  `printf '\342\200\223'`, so the script file itself contains no dash
  bytes (verified with `od -c`).
- `LC_ALL=C grep` matches raw bytes, which avoids locale-dependent
  multibyte misreads.
- There is no other way to run this check that is cleaner: `grep -P`
  is not portable and adds nothing here.

## Self-check the snippet

The snippet was validated on fixtures: a clean file passes (exit 0),
a file with an em dash is flagged (exit 1), a file with an en dash is
flagged (exit 1), a mixed batch fails, a missing file is reported
unreadable, and zero arguments print usage (exit 2). The script file
itself was byte-scanned with `od -c` and contains no dash bytes.

## When to use it

Run it on every loop document you author before committing: preregs,
result docs, freeze notes, amendments. It is a read-only check; it
never modifies files.
