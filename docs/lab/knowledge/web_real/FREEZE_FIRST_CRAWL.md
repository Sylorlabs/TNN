# FIRST-CRAWL implementation freeze — v2 (2026-09-23)

Supersedes the v1 freeze (same day). v1's battery passed, then independent
native verification found two genuine robustness bugs (below); they are fixed
here and the full 5-run battery was re-run clean. This v2 is the current
freeze. Any change to a frozen input invalidates the freeze and requires a
fresh 5-run battery before the system may again be called working.

## Frozen inputs

| Artifact | SHA-256 (full) | Notes |
|---|---|---|
| Fixture manifest | `49b7a9783c508849` (trunc) | `fixtures/MANIFEST.sha256`, 27 pages — UNCHANGED from v1 |
| Expected parse rollup | `d7583227541e1beb` (trunc) | `expected/*.parse` — UNCHANGED from v1 |
| `src/html_parse.zag` | `d7db1c64581c02512b531a0cc963663788d6ae3714fbc8bb12838f91f35fa5d4` | read_all: frees dir/base scratch |
| `src/fw_scan.zag` | `865d25c9ac868616f814d06d09ede2405b322c06c6e2d2ed80fb1d991859cd2f` | read_all: frees dir/base scratch |
| `src/verdict.zag` | `7f1450caeec452577b66880a26877245781994c7f2edacdb0e9b8fe9f05ee19c` | leak fix + visible drops |
| `bridge/fetch.py` | `2f307f06c363762b1e24f2461f6a71b121856980a983586db09af2345b842189` | UNCHANGED from v1 |

## Frozen battery result (v2, clean re-run)

5 runs, canonical-log digest (full SHA-256, identical all 5):
`17d2553cea8fadd9c5ad7f330d3566e941e16cd136f2abb49c82a5b1586b420d`

`battery_run.log` shows all 8 bars PASS directly (exit 0); `battery_out/report.json`
recomputed independently from the frozen artifacts. Ledger summary (fc1):
installed=10, withheld=5, quarantined_pages=2, dropped=0.

Kill bars: KB-PARSER, KB-DET, KB-NOINJECT, KB-NODIRECT, KB-CORR-TRUE (6/6),
KB-WITHHOLD-FALSE (0/3), KB-SINGLE-SOURCE (0/2), KB-SPOOF-RESIDUAL — all PASS.

## What v1's verification found, and what changed

Independent native verification agent (adversarial remit, 2026-09-23) confirmed:
all 8 bars pass under fully independent recomputation; KB-DET artifact is sound
(no timestamps/PIDs/run-varying data in canonical.log — the one 10-digit number
is part of a parse SHA); Python files are transport/test only (no judgment
decisions in `fetch.py`/`serve.py`); parser 24/24 edge cases re-verified;
firewall sweep re-verified (p1/p2 flagged, 25/25 clean CLEAR).

Two genuine bugs found and fixed in v2:

1. **verdict crashed on large manifests (was: rc=1, no ledger).** `read_all`
   allocated dir+base+buf per call and never freed; each manifest row made 2
   calls, so ~1040 rows exhausted the runtime's large-allocation provenance
   registry. Fixed: `read_into(path, buf)` reuses one caller-owned 1MB scratch
   buffer for all fw/parse reads and frees dir/base on every path; the manifest
   gets its own persistent buffer. Verified: 1200-row manifest → rc=0,
   installed=1 (was: crash). Same read_all pattern in `html_parse.zag` /
   `fw_scan.zag` now frees its dir/base scratch (called once per run there;
   hygiene, no behavior change — KB-PARSER re-verified byte-identical).
2. **Silent claim drops (were: invisible).** Claims ≥ CTLEN (2048) bytes were
   skipped with no ledger trace; claims beyond MAXC=512 got SUSPECT lines but
   were never decided. Fixed: both now emit visible ledger lines
   (`C|DROP|TOO_LONG|<len>|<pageid>`, `C|DROP|OVER_CAP|<claim>|<pageid>`) and a
   `|dropped=N` counter on the DONE line. Verified: 600 distinct claims →
   withheld=512, dropped=88, rc=0; 3000-byte claim on 2 domains → 2×
   `C|DROP|TOO_LONG`, dropped=2, rc=0.

Neither fix changes any frozen expected output (the 27-row battery has zero
drops); the v2 canonical digest differs from v1 only via the DONE line's new
`|dropped=0` field.

## Honest scope notes (unchanged from v1, plus verification clarifications)

1. Corroboration-fetch is harness-driven (fixture page → partner port as the
   "independent source"). Real independent-source discovery is M2+M4, phase 2.
   The JUDGMENT is all Zag.
2. **KB-WITHHOLD-FALSE naming (verification honesty note):** F7–F9 false claims
   were withheld by the single-source rule, not by contradiction detection —
   the architecture performs NO contradiction detection. The bar is
   mechanistically identical to KB-SINGLE-SOURCE; the name must not be read as
   "withholds because false". P3 proves the converse: a false claim with
   2-domain agreement and no injection signal IS installed (KB-SPOOF-RESIDUAL).
3. Firewall coverage boundary: catches ASCII case/punctuation/whitespace-
   obfuscated injections in the 4 fixed classes iff ≥2 distinct classes
   co-occur in one block. A single strong class in a block does NOT flag
   (frozen design rule, not a bug — but it is the cheapest attacker evasion and
   is documented here as the residual, not hidden). Homoglyphs, zero-width
   chars, misspellings, paraphrases, cross-block splits: not caught.
4. Fixture-domain identity is the port (8901=alpha, 8902=beta).
5. The bridge audit log contains timestamps by design; KB-DET covers the
   TNN-side canonical log, whose inputs exclude timestamps. Bridge audit chain
   verified independently (bridge_test.py: 0 failures).
6. v1's `battery_run.log` briefly showed two FAIL lines from a Python-harness
   off-by-two slice bug (`ln[7:]` instead of `ln[5:]`) in the bar evaluator —
   the Zag machinery and installs were correct throughout. The v2 battery was
   re-run end-to-end with the fixed harness; its log shows all-PASS directly.
   This note exists so the v1 log (kept in git history) is not misread.

## Sol consultation record

See `SOL_CONSULT_LOG.md`. Sol supplied designs only. All implementation,
integration, testing, and verification native. The v2 fixes (leak, visible
drops) are native findings from native verification — no Sol involvement.

## What may proceed

M1, M3, M5, M6 are built, frozen at v2, and passing. M2/M4/M7 are phase 2
(separately frozen). Nothing in this freeze prejudges phase 2.
