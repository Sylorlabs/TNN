# LI-1 scale-up — working resume notes (subagent scratch, not a deliverable)

## State as of 2026-09-23 (this turn)

- Status file: `corpus_snap_full/manifest_fetch_status.txt` — 56 F| records, in manifest order.
  - 54 ok with matching snapshot files (c001–c013 all p1–p4; c014 p2, p4).
  - 1 FAIL: c014-p1 (txwes.edu PDF) — `browser-service could not fetch the requested page`. Do NOT retry blindly; one justified retry allowed later, else leave FAIL.
  - 1 URLMISMATCH: c014-p3 — prior session fetched
    `https://amsi.org.au/content/uploads/2023/08/amsi-nsw-seed-6-7-fractions-decimals-and-percentages.pdf`
    which is NOT the manifest URL. Correct manifest URL (both forms agree):
    `http://amsi.org.au/teacher_modules/pdfs/Decimals_and_percentages.pdf`
    → fetch THIS exact URL next, snapshot it, then REPLACE the URLMISMATCH record
    with the ok record (keep manifest order). Wrong-URL scratch deleted; no snapshot taken from it.
- Snapshots: `corpus_snap_full/cXXX/cXXX-pN.txt` with `TITLE: ...` first line. 54 files present, each with an ok record; no orphans.
- Verified this turn: all 55 pre-existing status-record URLs match the authoritative manifest
  character-for-character (Python check). Only c014-p3 was wrong (caught before snapshotting).

## Still to fetch (manifest order): c014-p3 (correct URL), then c015–c055 (158 URLs).
- Per-URL protocol: grep exact URL from `li-1/urls_manifest.txt` → browser.open fetch →
  write `TITLE:` snapshot → append ONE `F|cluster|page|url|ok|title` record (manifest order).
- c001–c004 still need fresh re-fetch + compare (may be abbreviated transcriptions).
- Do NOT invent content; log FAIL/URLMISMATCH honestly. Zero RNG anywhere.

## Later pipeline (after all 213 URLs have records)
1. Two fresh passes via `run_li.py` with `li-1/urls_manifest_cu.txt` + `corpus_snap_full`
   into `run_full_pass1/`, `run_full_pass2/`; prove byte identity (cmp ledgers/logs, SHA-256).
2. Deliverables at run root: `knowledge_ledger_full.txt`, `refusal_ledger_full.txt`, `SCALEUP_REPORT.md`.
3. LI-K1–K6 assessment in final report. Do not commit (coordinator commits).
