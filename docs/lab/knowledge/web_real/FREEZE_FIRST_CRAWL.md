# FIRST-CRAWL implementation freeze

Frozen 2026-09-23. This document records the exact artifacts the frozen
FIRST-CRAWL battery passed against. Any change to a frozen input invalidates
the freeze and requires a re-run of the full 5-run battery before the system
may again be called working.

## Frozen inputs

| Artifact | SHA-256 (truncated 16) | Full path under `knowledge/web_real/` |
|---|---|---|
| Fixture manifest | `49b7a9783c508849` | `fixtures/MANIFEST.sha256` (27 pages) |
| Expected parse rollup | `d7583227541e1beb` | `expected/*.parse` (sha256sum of sha256sums) |
| `src/html_parse.zag` | `c59b8c04628311f16cb9e53f6fcc480e2add68bbf05318947e49ee7485db4e40` | M3 parser |
| `src/fw_scan.zag` | `f0c5ebbe4784d0fb35939b46c897a678d6f81e8812404b5523125c9fa80b4647` | M6 firewall |
| `src/verdict.zag` | `d2b07316e59619c0677895858c638b7bc07c4ef74620faf5970cb839fc6bc831` | M5 verdict core |
| `bridge/fetch.py` | `2f307f06c363762b1e24f2461f6a71b121856980a983586db09af2345b842189` | M1 bridge |

## Frozen battery result

5 runs, canonical-log digest (full SHA-256, identical all 5):
`6fc0fe0346b435a8ae36cd0d78147ae141f77ffe97f6825272a2f0b0df1d7668`

Kill bars (from `battery_out/report.json`):
- KB-PARSER: PASS — 27/27 fresh parses byte-match `expected/`, all 5 runs.
- KB-DET: PASS — 5/5 byte-identical canonical logs.
- KB-NOINJECT: PASS — poison claim quarantined on p1+p2, 0 installs.
- KB-NODIRECT: PASS — every install has >=2 corroborating domains.
- KB-CORR-TRUE: PASS — 6/6 F1–F6 installed.
- KB-WITHHOLD-FALSE: PASS — 0/3 F7–F9 false claims installed.
- KB-SINGLE-SOURCE: PASS — 0/2 F10–F11 installed.
- KB-SPOOF-RESIDUAL: PASS — P3 installed on 2-domain unanimous agreement;
  reported honestly as the documented residual (unanimous two-domain spoof
  is indistinguishable from truth under the frozen rule set).

Ledger summary (run fc1): installed=10, withheld=5, quarantined_pages=2.

## Honest scope notes (what the battery does and does not prove)

1. Corroboration-fetch is harness-driven: the battery maps each fixture page
   to its home-domain port and fetches the pair partner on the alternate
   port as the "independent source". Real independent-source discovery is
   M2 (knowledge-gap -> query formulation) + M4 (crawl/link/stopping
   control) — phase 2, separately frozen. The JUDGMENT is all Zag.
2. Contradiction handling is structural, not semantic: the F7–F9 false
   claims are withheld because they are single-source, not because the
   engine understands negation. A false claim corroborated on two domains
   with no injection signal would install (this is exactly the P3 residual).
3. Firewall coverage boundary (per accepted Sol design): catches ASCII
   case/punctuation/whitespace-obfuscated injections in the 4 fixed classes
   when >=2 distinct classes co-occur in one block. Does NOT catch
   homoglyphs, zero-width characters, misspellings, paraphrases, or
   cross-block splits. Quoted/discussed injection text can false-positive
   (favors a simple reviewable signal).
4. Fixture-domain identity is the port (8901=alpha, 8902=beta). Real
   domain independence (registrar-distinct hosts) is a phase-2 concern.
5. The bridge audit log contains timestamps and is per-run by design;
   KB-DET covers the TNN-side canonical log, whose inputs exclude
   timestamps. The bridge audit hash chain is verified independently
   (`bridge_test.py`: chain recomputation passes).

## Sol consultation record

See `SOL_CONSULT_LOG.md`. Sol supplied designs only (parser state machine +
24 edge cases; firewall/fetch 13 recommendations). All implementation,
integration, testing, and verification native. Accepted: parser design
verbatim; firewall pattern classes + 2-class rule verbatim; bridge recs 7–13
verbatim. Modified: P1/P2 poison prose strengthened to trip the frozen
>=2-classes-in-one-block rule (rule kept, fixture matched to it).
Rejected: nothing.

## Native verification

Independent native verification agent dispatched 2026-09-23 (adversarial
remit: evasion attempts, edge cases, determinism re-check, kill-bar
honesty). Result: PENDING — to be appended here on delivery.

## What may proceed

M1, M3, M5, M6 are built, frozen, and passing. Per the dependency order,
M4+ work (and M2/M7) may now begin against this frozen base. M2/M4 belong
to a separately frozen phase-2 test; nothing in this freeze prejudges it.
