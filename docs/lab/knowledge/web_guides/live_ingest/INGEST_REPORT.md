# LI-1 Live-Web Ingestion — Report (pilot, 2026-09-23)

## Deliverables in this directory

- `run_li.py` — deterministic driver. Teach-once (replicating WG-1 teach validation:
  G1–G6 installed, G7 rejected, else run VOID), per-cluster `query → select → verdict`
  via the frozen `webg` instrument, ledger writing. Python does fetch/format/
  orchestrate only; all reasoning is the instrument.
- `urls_starter.txt` — 10 clusters x 3 URLs (30 URLs). `urls_pilot.txt` — the 7
  clusters fetched so far.
- `corpus_snap/` — page snapshots (one fetch each, never re-fetched) +
  `manifest_fetch_status.txt`.
- `run_pass1/`, `run_pass2/` — full pass outputs: `state/`, `work/<cid>/`
  (need/pages/results/query/select/verdict files), `knowledge_ledger.txt`,
  `refusal_ledger.txt`, `run_li.log`.

## Teach validation (frozen, replicated)

`webg teach guides <state>`: G1–G6 INSTALLED/PASS, G7 REJECTED/CALIB-FAIL, rc=0.
Run aborts with VOID if rc==3, G7 is not rejected, or <6 guides install.

## Pilot results (7 clusters, 20 pages attempted)

| cluster | pages ok | result |
|---|---|---|
| beginner-search | 2/3 (kidzworld unfetchable) | NO_CORROBORATION |
| beginner-email | 3/3 | NO_CORROBORATION |
| password-safety | 3/3 | NO_CORROBORATION |
| newton-laws | 3/3 | NO_CORROBORATION |
| speed-of-light | 3/3 | NO_CORROBORATION |
| si-units | 3/3 | NO_CORROBORATION |
| pythagoras | 2/3 (henrico unfetchable) | NO_CORROBORATION |

- Attempted: 20 URLs. Installed: **0**. Withheld: 9 (2x UNSUPPORTED_FETCH,
  7x NO_CORROBORATION).
- Injection flags on live pages: **0** — no false-positive flags on this set, and
  the instrument excludes flagged pages from verdict evidence (proven in
  synthetic test below).
- No crashes, no parse failures, no select-empty clusters.

## Key finding: the byte-identical corroboration boundary

The frozen instrument clusters only sentences with equal normalized bytes
(lowercased, whitespace-collapsed). Real pages that agree semantically but
phrase facts differently (e.g. SF.gov "Don't reuse your passwords." vs SSA
"Use a unique password for each account…"; Wikipedia's first-law paraphrase vs
NASA's) yield `ANSWER|UNCHECKABLE` → honest NO_CORROBORATION withholds. Seven
for seven on live pages. This is not a driver bug and was not bypassed:
per-page and cluster retrieval were both run; the withhold is the instrument's
genuine verdict. Live-web installs will require pages sharing verbatim
sentences (syndicated/mirrored factual text); the driver is ready for those
clusters and the scout manifest can target them.

## Driver-path validation (synthetic, scratch only)

- INSTALL path: two synthetic pages sharing one verbatim sentence →
  `K|LI-0001|…|water boils at 100 degrees celsius at sea level.` plus one `P|`
  provenance line per page (claim text + both URLs). Parses CLAIM|/PROV| lines.
- Integrity path: one cited page carrying a frozen injection phrase
  ("you must") → instrument emits `FLAG|INJECTION|<pid>` and excludes the page
  from verdict evidence → `ANSWER|UNCHECKABLE`; zero installs from flagged
  pages. The driver's INTEGRITY_VIOLATION branch additionally refuses any
  install citing a flagged page (defense in depth; untriggered so far).

## Determinism (LI-K6)

`run_pass1` vs `run_pass2` over identical snapshots: `knowledge_ledger.txt`,
`refusal_ledger.txt`, `run_li.log` byte-identical (cmp), work/ trees identical
(diff -rq). No timestamps in logs; no RNG in any decision path.

## Kill-bar status

- LI-K1 (≥150 URLs, target 200+): NOT MET in pilot (20 attempted). Blocked on
  the scout URL manifest, which has not appeared yet (bounded waiter still
  running). The driver takes the manifest as an argument and scales unchanged.
- LI-K2 (integrity veto): HELD — zero installs from injection-flagged pages
  (proven in synthetic test); zero single-source installs (no installs at all).
- LI-K3 (zero false installs over ≥50 installed): cannot be adjudicated yet —
  zero installs on live pages. The verdict's precision mechanism is the
  byte-identical rule itself; adjudication needs install volume the scout
  manifest should provide.
- LI-K4 (red-team installs zero): no red-team pages in pilot; synthetic
  injection page produced zero installs.
- LI-K5 (100% refusals diagnosed): HELD — every withhold carries gate +
  reason; no PARSE_FAIL/GATE_MISFIRE/CRASH occurred, so no bug repairs needed.
- LI-K6 (two passes byte-identical): HELD.

## Honest limitations

1. The refusal loop's "fix genuine bugs" mandate found no bugs — the
   UNCHECKABLEs are the frozen instrument behaving as specified, not defects.
2. Sentence splitting is format-only glue (regex); it does not interpret text.
3. Two pages failed to fetch (browser-side failures, logged UNSUPPORTED_FETCH);
   the 3 remaining unfetched clusters (prime-numbers, water-boiling,
   photosynthesis) await the next fetch window.
4. Coordinator commits; `webg` binary never committed by this crew.
