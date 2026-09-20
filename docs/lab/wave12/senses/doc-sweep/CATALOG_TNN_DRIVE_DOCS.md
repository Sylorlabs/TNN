# Catalog — TNN Drive Documents

**Date:** 2026-09-20
**Root:** `My Drive / TNN` (ID `13279S7nBlFewa8sGZtRWO3fUpxJKl0WF`), read-only.
**Enumeration:** 3,595 folders, 44,285 files. **1,068 document entries** (653 `.md`, 415 `.txt`; 63,732,366 listed bytes). No `.doc`/`.docx`, no Google-native docs.

## Machine-readable files (in this directory)

| File | Contents |
|---|---|
| `docs.json` | 1,068 entries: Drive id, name, mimeType, size, modifiedTime, full Drive path |
| `manifest.json` | 872 primary downloads: drive_id → local file, Drive path, size, modified time |
| `dedupe_by_content.json` | SHA256 → all entries sharing that exact content |
| `content_hashes.json` | per-file SHA256 for the primary 872 |
| `download_rest_ckpt.json` | 196 remainder downloads: drive_id → local file, size, SHA256 |
| `error_payload_entries.json` | superseded record of the failed first attempt at the 196 (missing `--output` flag; error payloads, not documents) |
| `enumerate.py`, `enumerate.log`, `tiers.json`, `checkpoint.json` | enumeration tooling and tier grouping |

## Verification

- All 1,068 entries downloaded; every byte count verified against Drive metadata; SHA256 computed over actual downloaded bytes.
- The 196 remainder entries initially returned CLI error payloads (the download script omitted the required `--output` flag) — detected by content inspection, re-downloaded with the correct invocation, sizes re-verified. The error payloads were never documents; stale payload files were deleted from the corpus.
- **892 unique contents**; 103 duplicate groups covering 279 entries (all byte-identical).
- Duplicate groups are operational copies: `.scratch/` extraction trees duplicating `Research/` files, run directories (FINAL_FROZEN / FINAL_INTEGRATION / REQUAL / REMEDIATION) duplicating each other's summary/pin/review files, preflight/postrun pin files, checksum inventories, review witnesses, empty placeholders, 2-byte flag files. No substantive document hides inside a duplicate group. Groups of ≥3 listed below; the 78 pairs are all in `dedupe_by_content.json`.

## Coverage

- 12 reader agents; all 872 primary documents at least skim/keyword-passed; Tier-1 (416 high-signal) fully read; promising Tier-2 fully read.
- The 196 remainder entries: 135 duplicate already-read main-batch content; the 57 remainder-only unique contents are machine inventories, diff witnesses, inert reference dumps, run-metadata flags, and one procedural checklist — all content-classified, none carrying new scientific signal.
- Targeted sweeps: PAM/audio/speech/TTS/vision/sensor/perception; memory operations; abandoned/retired/failure/NO_GO/PASS; architecture origins; koryphaios/ghost.
- Per-batch findings: `findings/tier1_batch0.md` … `findings/tier1_batch7.md`, `findings/tier2_batch0.md` … `findings/tier2_batch3.md`, `findings/tier2_gaps.md`.
- Known gap: `findings/tier2_batch0.md` truncated mid-write at finding 11 of 18; its range was independently covered by `findings/tier2_batch3.md`, so no range lost coverage.
- Synthesis: `NEW_KNOWLEDGE_FROM_DRIVE_DOCS.md`.

## Tree shape

Nearly all documents sit under `TNN/TNN/Research/` (1,066 of 1,068; one each under `TNN/TNN-R1/` and `TNN/TNN-R1-Audit/`). Depth: 400 at depth 3, 275 at depth 4, the rest scattered to depth 15 (deep `.scratch/` extraction trees and `R33_*` run directories). The `.scratch/` subtrees are workflow-extraction copies — flags, pins, receipts, and run metadata, not research prose.
## Duplicate groups of 3+ (25 groups; the 78 pairs live in `dedupe_by_content.json`)

1. **13x** — 2-byte run flags (`BYTE_IDENTICAL` / `SOURCE_PIN_GATE` / `RUN_ATTEMPT` / `EXIT_CODE`) across `.scratch/` e51ah/e51ai/e51aj trees, N13 launch, and the E50 negative-rescue dir
2. **11x** — V91 `import_paths.txt` across FINAL_FROZEN / FINAL_INTEGRATION / REQUAL / N17 continuity run dirs (2,900 B)
3. **6x** — `R32_E51AH_GROUNDED_PRESERVATION_REPLAY_PREREG.md`: Research original + 5 `.scratch/` extraction copies (8,065 B)
4. **6x** — N19 `results.summary.txt` across the five 2026-09-15 run dirs + process-supplement copy (23 B)
5. **6x** — N19 `reap.summary.txt`, same spread (22 B)
6. **6x** — N19 `supplement.summary.txt`, same spread (22 B)
7. **6x** — N10 artifacts-verified record across N10/N11/N12 preflight/postrun/preparation dirs (12,950 B)
8. **5x** — `R32_E51AI_LONGITUDINAL_CONTEXT_PREREG.md`: Research original + 4 `.scratch/` copies (9,647 B)
9. **5x** — N19 `results.results.txt` across the five run dirs (3,283 B)
10. **5x** — N19 `supplement.results.txt`, same spread (320 B)
11. **5x** — N19 `final.summary.txt` variants across runtime-boundary recovery lanes (23 B)
12. **4x** — N19 lane review witness (`c_review.md`) across final-frozen / integration / requal / runtime-boundary (7,728 B)
13. **4x** — `INDEPENDENT_INTEGRATOR_REVIEW.md` across FINAL_FROZEN timestamps + REQUAL (1,831 B)
14. **4x** — N11 artifacts-verified across N11/N12 dirs (14,446 B)
15. **4x** — N12 final source pins across dispatch/postrun/preflight (6,771 B)
16. **4x** — N11 preflight/postrun source pins (3,271 B)
17. **4x** — 2-byte exit-code flags across `.scratch/` trees + N13A launch (2 B)
18. **4x** — empty files: V91 recovery evidence placeholders, blob-search placeholder, R34 v3 `isolation.forbidden.txt` (0 B)
19. **3x** — `R32_E51AJ_REPLAY_ORDER_DOSE_PREREG.md`: Research original + 2 `.scratch/` copies (12,783 B)
20. **3x** — N19 `final.results.txt` variants across recovery lanes (3,445 B)
21. **3x** — `NEXT_AGENT_START_HERE.md` shared by continuing-life history, N14 sensor preflight, and remediation-before (23,139 B)
22. **3x** — N12 artifacts-verified: closeout snapshot / final / native (8,943 B)
23. **3x** — N17 `VERIFY_CONTRACT.md` across lane-witness / FINAL_B / terminal-supplement (4,643 B)
24. **3x** — N10 preflight/postrun source pins (1,677 B)
25. **3x** — compiler SHA256SUMS across the three `.scratch/` extraction trees (111 B)

The 78 pairs (156 entries) are dominated by: `.scratch/` copies of Research files, run-dir duplicated summaries/pins/reviews, and the `TNN_NEXT_RUN_ARCHITECTURE_PLAN.md` = `R31_HANDOFF.md` / N13 DESIGN.md pairs. Full listing in `dedupe_by_content.json`.

## What the catalog does not claim

- Filename/size similarity was not accepted as duplicate proof anywhere; all dedupe is by SHA256 over downloaded bytes.
- The 19 preliminary "machine/reference/noise" files were content-classified: 4 lane diff-witnesses (machine-generated line diffs of review docs), 4 path/object inventories (`local_files.txt` 23MB, `git_objects.txt`, `candidates_deep.txt`, `log_inventory_paths.txt`), 8 inert reference source dumps (CPython pickle, NumPy, PyTorch, RFC 6234, generated `acodegen` Zag), 1 procedural checklist (`PREFREEZE_MANIFEST_REQUIREMENTS.md` — freeze-manifest discipline, no scientific content), plus duplicated copies of the same under a second run dir. The small flag/stat/receipt files among the remainder are run metadata (exit codes, checksums, run IDs); spot-reads (`E50` exit code 1 on the negative-rescue, R34 v2 receipt `failures=0`) held no new scientific signal.
- Google-native docs, if any existed, would not appear in this file listing; none were found.
