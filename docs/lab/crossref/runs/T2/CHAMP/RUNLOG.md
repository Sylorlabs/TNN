# T2-CHAMP — RUNLOG

Replacement replication crew, Wave 2 Tier 2. Type C (committed-evidence re-derivation).
All work 2026-09-23 (UTC). Scratch only: `~/workspace/scratch-crossref/T2/CHAMP/`.

## 0. Inherited state (recorded, not redone)

- `clean/` had no git checkout (empty dir); `crew/` held the frozen prereg
  (`PREREG_TIER2.md`, blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`, 38,417 bytes),
  prior evidence downloads, and a partial `verify_champ.zag` that did not compile.
- Two HTTPS clone/fetch attempts had failed earlier (timeout; 31-min fetch → early EOF).
  Strategy per brief: fetch frozen files via GitHub API with locally recomputed
  git blob-SHA verification instead of a full clone.
- Frozen prereg commit API-verified: `7b2100d09911c5c10252c5756c7def288e70bd1f`
  (tree `a88b8b9f3374be980628b8999b6c3ad0aabacb9a`, parent prefix `3edd14867296`).

## 1. Pin freeze (BEFORE running)

| Pin | Value | Status |
|---|---|---|
| Frozen prereg commit | `7b2100d09911c5c10252c5756c7def288e70bd1f` | API-verified 2026-09-23 |
| Frozen tree | `a88b8b9f3374be980628b8999b6c3ad0aabacb9a` | from commit object |
| Prereg doc blob | `b1178370036bffbda6eb68ea0989c0e427dc31b7` (38,417 B) | SHA-verified |
| znc toolchain | `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` | SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`, `znc 2026.07.0-dev (edition 2026)` |
| Brief-expected `b9d7a6` | — | **422 No commit found**; 0 hits in commit search, 0 hits among 1,513 frozen championship-tree object SHAs, 0 occurrences in prereg text, 0 hits in sylorlabs/zag. Coordinator PIN AUDIT (`T2/_wave2_tally/VERDICTS.md`, 2026-09-23 ~06:10 UTC) classifies it a **transcription artifact** from the replacement batch briefs and instructs affected crews to fall back to the prereg's own pins. Proceeding on the verified frozen commit per that instruction. |

## 1b. PIN CORRECTION from coordinator (received 2026-09-23 ~07:36 UTC, after verdict)

Coordinator confirms: the evidence pin `b9d7a6` in the replacement brief was a
transcription artifact — 422 "No commit found" in sylorlabs/TNN. **Disregard it.**
Per task §1 the frozen prereg governs; pins extracted from the frozen
`docs/lab/crossref/PREREG_TIER2.md` at commit
`7b2100d09911c5c10252c5756c7def288e70bd1f` (verified to resolve via GitHub API
before running) are the authority. Do NOT stop over the bad pin.

Discrepancy record: this crew had already independently reached the same conclusion
during the pin-freeze step (§1 above) — `b9d7a6` resolved to nothing, and the
coordinator's own PIN AUDIT (`T2/_wave2_tally/VERDICTS.md`) had already classified it
as a transcription artifact with a fallback-to-prereg instruction. The replication
proceeded on the prereg's authority throughout; no work was gated on the bad pin,
and the REPRODUCED verdict is unaffected. No re-run required.

## 2. Evidence assembly (all blob-SHA verified against the frozen tree)

- Batch 1 (`manifest.txt`): 121 files — bind logs (12 reps × muse-native/sol/step/grok/curated),
  btrap rep0 per box, together teach/teacher logs, conflict matrix, flags JSON,
  faithfulness JSON, source verdicts/analyses. 12 sol btrap files missed (wrong
  filename pattern), corrected to `btrap_M2_repN_s1.log` and fetched.
- Batch 2 (`manifest2.txt`, `manifest3.txt`): SWE class-3 raw log, curated/bestof
  direct+teacher logs, bestof bind rep0–11.
- Batch 3 (`manifest4.txt`, this session): **77 trap files** — per-rep btrap logs for
  all 6 class-4 boxes (12 reps each: `btrap_M2_repN.log`, sol `..._s1.log`,
  step `m2.btrap.repN.log`, grok `m2_trap_rN.log`, bestof `btrap_M2_repN.log`)
  plus together `btrap_0..4_run0.txt`. All 77 OK, 0 failed.
- Frozen corpus SHA-256 pins (from committed SHA256SUMS): sol `41aa8f5b…9015d7`,
  grok `7f3a2573…2bc2508`, step `c52e4f52…2ea69ab`, SWE `ca1e7b85…b92456b7f`,
  muse-native `1d5c2ede…9c51e07`, curated `6fbfdb6…67ac62`, bestof `0177c7f0…beb0ad5a5`.
- Staged into `clean/evidence/boxes/` and `clean/evidence/together/`
  (72 per-rep box btrap files + 5 together btrap files copied from verified downloads).

## 3. Verifier build (pure Zag, zero RNG)

- Source: `crew/verify_champ.zag` (693 lines, SHA-256
  `fedc7db5ddf668a4759e71b2eefaecd35216fa2d8d499f855f3a2736d429bf82`).
- Independent re-derivation: parses bind `RESULT` lines and per-rep btrap logs,
  recomputes Track-5 composites in integer arithmetic (units 1/10000, round-half-up),
  checks class-1 genuine-only revisability asymmetry, matrix 1,140 rows / 0 splits /
  12 planted IDs, SWE class-3 (revisions, mastery, §B.7, zero-gates, cost, composite),
  curated flags 12/12 with 0 non-planted, bestof faithfulness + legB/legC figures.
- Python used only as download/analysis glue; all verdict arithmetic in Zag.
- Debugging (all fixed, none in final binary):
  - Packed-return field overlap (mask ≤4095 contaminating adjacent fields) → widened
    to non-overlapping ranges (mask field 10⁴).
  - `SWEC_TEACH_DIGEST` false-positive prefix match → require `,` after tag.
  - `CL_CHECK` tag length 8, not 9 → zero-gates parsed.
  - Trip/leak accumulators initialized to 9 → 0.
  - znc codegen: call expressions rejected as print args → `pnum()` helper; added
    tested `i64s()` (strips `_zag_i64_to_str` trailing newline).
  - Each rep now paired with its OWN committed trap log (previously rep0 reused);
    grok traps found under `m2_trap_rN.log` naming.
- Built with pinned znc: `--no-zagd --no-analyze --no-foreground-cache`.
  Binary + `.zagd`/`.zag-cache` removed after final runs (source and text outputs kept).

## 4. Runs (byte-identical ×3)

```
./verify_champ > run1.txt && ./verify_champ > run2.txt && ./verify_champ > run3.txt
cmp run1.txt run2.txt && cmp run2.txt run3.txt  →  BYTE-IDENTICAL x3 CONFIRMED
SHA-256 (all three): e4b45499137d786224680d638b72bd542cb0e9b6dfbf0e9bedec58637c380e5c
```

Full output in `crew/run1.txt` (27 lines, `ALL_CHECKS_PASS`).

## 5. Notes / limitations

- No full `git clone` of the frozen commit exists (HTTPS clone/fetch failed pre-handoff);
  all evidence is API-fetched with per-blob SHA verification against the frozen tree —
  content-identical to a clean checkout for every file used.
- Class-1 traps: `teacher.txt` is a single run; paired with committed `btrap_0.txt`
  (together rep 0). No per-run trap file exists for the teacher in the frozen tree.
- The 5-source (not 6) class-2 acceptance question is Micah's call per prereg; it
  changes no figure (rule: PARTIAL only if a figure is affected — none is).
- `TMPDIR` scratch used; nothing written outside `~/workspace/scratch-crossref/T2/CHAMP/`;
  no live workstreams touched.
