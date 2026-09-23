# Gap-Closure Prereg — 1GB Ingest Data-Coverage Gaps

**Frozen:** 2026-09-23 (UTC). **Scope:** the three open items in REPORT.md §7
(Wiktionary 56% partial; 9 CAL-rejected lessons; WordNet transport deviation).
**Standing rule:** a PARTIAL never ends a track — each gap closes by
root-cause-first evidence, or by proven-correct rejection, never by guess.

**Global rules:** pure Zag for mechanisms/learners/verification; Python only
for glue/analysis/extraction. Zero randomness. Byte-identical reruns proven by
SHA. Deterministic pipeline (extract → merge → ingest) for all data changes.
Commits to `tnn-native-lab` via `~/workspace/commit_racefree.py` with
`TMPDIR=~/workspace/tmp_commit`; lab-relative paths; never binaries/`.zagd`;
never tree-replace across branches.

---

## Gap 1 — Wiktionary stopped at 5M/9M pages (56%)

**Root-cause method (instrument, don't guess).**
1. Read `run/wikt.ckpt` (contains `5000000`), `run/wikt_extract.log`
   (resume attempt: skip progress 0.5M/1M/1.5M of 5M, then silence — died
   during skip), file mtimes (`wikt.bin` 12:56 UTC, `wikt.ckpt` 12:55 UTC),
   `STATUS.md` (12:15 UTC claims "stopped due to time").
2. Check for exception/traceback evidence (none in logs), OOM evidence
   (none), and parser-defect evidence (structural validation passed per
   REPORT.md §2; extractor is a pure byte scanner — no page-count limit in
   code; the only exit paths are EOF-break and kill).
3. Reconcile the contradiction: STATUS.md's "stopped due to time" (12:15)
   predates the last write (12:56) — the note was written while extraction
   was still running. The checkpoint file is removed ONLY on clean
   completion (`wikt.py` end-of-main); its presence proves no clean exit.
   Verdict to record: **interrupted run (process kill; consistent with the
   2026-09-23 daemon-restart wave that wiped sibling crews), not a parser
   bug.** The resume attempt was itself killed during the 5M-page skip phase.

**Completion plan.**
1. Fix `extract/wikt.py` first (Gap-2 degenerate-record fix — §Gap 2 —
   so the remaining ~4M pages emit no gate-failing records).
2. Resume `wikt.py` from the intact checkpoint (`wikt.ckpt` = 5000000) under
   `nohup`/`setsid` in background; monitor progress lines; do NOT delete the
   checkpoint manually.
3. Resume-overlap accounting: pages parsed between the 5M checkpoint write
   (12:55) and the kill (12:56) were appended, and will be re-parsed and
   re-appended on resume (by design of the checkpoint scheme). These exact
   duplicates are removed by the fixed merge (§Gap 2); quantify them via the
   G2-dupe count delta before/after if needed.
4. One-time deterministic remediation: filter the legacy 5M-page portion's
   degenerate records (kind-1 text len<4; kind-2 empty word segment) with a
   committed Python filter — the fixed extractor only governs new pages.

**Acceptance bars.**
- `run/wikt.ckpt` absent (script removes it only on clean EOF completion).
- Page counter reaches the dump's full page count (≈9M; exact number recorded
  from the completed run).
- `wikt.bin` parses end-to-end with the record scanner (no truncation):
  independent Python scan reaches EOF cleanly; record count recorded.
- Determinism: fixed merge dedupes all resume-overlap duplicates (final
  `facts.bin` G2-dupe count = 0 by independent gate simulation).
- New facts merged through extract → merge → ingest; store fact count grows;
  seal recomputes (see Gap 2 bars).

---

## Gap 2 — 9 CAL-rejected lessons (report claimed 1,110,933 records)

**Root-cause method (instrument the CAL gate).**
1. Decode `run/store_full/audit.log` lesson lines:
   `LESSON {3,14,23,28,31,39} CAL=REJECT mask=1`,
   `LESSON 43 CAL=REJECT mask=15`,
   `LESSON 48 CAL=REJECT mask=8`,
   `LESSON 50 CAL=REJECT mask=4` — each `dropped=65536`.
   Mask semantics (from `build/ingest.zag` `ig_process_lesson`): bit p (0–3)
   = must-accept dry-run record p failed `ig_gate`; bits 4–7 = synthetic
   must-reject probes misbehaved (none fired — all four probes behaved).
2. Byte-exact Python mirror of `ig_gate` (G1 wellformed / G2 adjacent-dupe /
   G3 kind-specific) run over all of `run/facts.bin` in stream order, plus
   boundary probes at each rejected lesson's first 4 records.
3. **Findings (recorded as evidence, obtained 2026-09-23 pre-freeze):**
   - Lessons 3/14/23/28/31/39 (mask=1): lesson record 0 key == previous
     lesson's last record key → G2 adjacent-dupe fired in the must-accept
     dry-run (which compares all 4 dry-run records against the carried
     `prev_key`). Root cause: **`extract/merge_sort.py` never deduplicated —
     it counted 539,418 duplicate keys and wrote every one of them.**
     REPORT.md §3's "Duplicate keys removed: 539,418" / "deduplicated in
     merge" is FALSE. Gate simulation over `facts.bin`: G2 verdict on exactly
     539,418 records.
   - Lesson 43 (mask=15, all 4 failed), 48 (mask=8, rec 3), 50 (mask=4,
     rec 2): degenerate `wikt.py` kind-1 records — G3 `text.len<4` fired.
     In `facts.bin`: 96,741 kind-1 records with `len(text)<4`
     (95,279× `"."`, plus `":"`, `"()"`, `", ."`, `"()."`, 95 distinct —
     extractor `clean_def` collapsing sense lines to punctuation), and 3
     kind-2 records with malformed keys (`wikt:en::*band:plural:*bands:01`
     — empty word segment → `ig_key_word` returns −1 → G3).
   - Report arithmetic correction: CAL-dropped = 9×65536 = **589,824**
     records, not 1,110,933. The remaining 521,109 = individual G1/G2/G3
     rejects inside accepted lessons (g2=462,263, g3=58,846, g1=0 per
     audit.log sums; 3,707,990 − 589,824 − 521,109 = 2,597,057 installed ✓).
   - Verdict: rejection of the degenerate/dupe RECORDS was correct; rejection
     of the 9 lessons AS A UNIT was a data-pipeline defect (merge never
     deduped; extractor emitted gate-failing records). The lessons contained
     ~hundreds of thousands of good records. Fix the data, re-ingest through
     the genuine path with CAL active.

**Completion plan.**
1. Fix `extract/merge_sort.py`: drop 2nd+ records with equal adjacent keys
   (keep first) in the k-way merge — the dedupe the report claimed.
2. Fix `extract/wikt.py` `parse_page`: skip kind-1 records with
   `len(text)<4` and kind-2 records whose word segment is empty (exact mirror
   of the gate's G3 bars; the extractor already carries a partial "G3
   pre-check" — extend it).
3. One-time deterministic filter for the legacy 5M-page `wikt.bin` portion
   (committed script; counts removed).
4. Re-run fixed merge → new `run/facts.bin` (keep previous as
   `run/facts_v1.bin` for audit). Verify by independent scan:
   record count = 3,707,990 − 539,418 − 96,744 = **3,071,828** (pre-Gap-1-
   completion), G2 verdict count = 0, G1 = 0.
5. Re-run merge a second time → byte-identical SHA (determinism proof).
6. Re-ingest with the genuine `build/ingest_bin` (frozen CAL+G1–G4, negative
   control) into `run/store_full_v2/`. Run ingest TWICE → seals must match
   byte-identically (also closes REPORT.md §7.6 single-run caveat).
7. E1 retrieval eval (1,000 deterministic keys) against the new store.

**Acceptance bars.**
- New `audit.log`: 0 `CAL=REJECT` lines; every lesson `CAL=OK`.
- Installed count = independent-scan accept count (3,071,828 pre-Gap-1;
   formula re-verified post-Gap-1: installed = records − dupes − gate rejects).
- Negative control 1,200/1,200 rejected; synthetic CAL probes behave
  (no mask bits 4–7).
- Two ingest runs → identical seal SHA256.
- E1: 1,000/1,000 keys retrieved.
- REPORT.md §4 caveat corrected (589,824 vs 1,110,933; merge-dedupe claim
  struck).

---

## Gap 3 — WordNet transport deviation (NLTK zip vs Princeton tarball)

**Root-cause method.**
Probe Princeton endpoints for the canonical WordNet 3.1 distribution named
in the frozen spec. `https://wordnetcode.princeton.edu/3.1/WordNet-3.1.tar.gz`
→ 404 (confirmed 2026-09-22 and 2026-09-23). BUT the actual Princeton 3.1
database distribution,
`https://wordnetcode.princeton.edu/wn3.1.dict.tar.gz`, is LIVE on Princeton's
own server: HTTP 200, `application/x-gzip`, 16,358,468 bytes (probed
2026-09-23). The frozen spec named a file Princeton never shipped under that
name for 3.1 (3.1 was "database files only").

**Completion plan (equivalence proof, then amendment).**
1. Download `wn3.1.dict.tar.gz` from `wordnetcode.princeton.edu` into
   `corpus/` work area (not committed — 16MB; record SHA256 in manifest).
2. Byte-compare the four files `wn.py` reads
   (`data.noun`, `data.verb`, `data.adj`, `data.adv`) against the
   `wordnet31/` members of the NLTK `wordnet31.zip`. Record per-file SHA256.
3. Run the `wn.py` extraction logic against the Princeton files →
   require **byte-identical** `wn.bin` (SHA256 must equal
   `575bab57e195f27908cfcd660cd42ba38bccec3bf363c34f4922a48bd205cbb7`,
   the committed `run/wn.sha1`).
4. If byte-identical: file a prereg amendment approving the NLTK
   `wordnet31.zip` transport as content-identical to the canonical Princeton
   3.1 database distribution, documenting the corrected canonical filename.
   If ANY byte differs: switch extraction to the canonical tarball, re-run,
   document the delta.

**Acceptance bars.**
- 4/4 data files byte-identical (SHA256 table in the verdict doc), OR all
  differences enumerated with per-file hashes and extraction re-run from
  the canonical source.
- Extraction from the independent Princeton copy → SHA-identical `wn.bin`.
- Prereg amendment committed (deviation formally approved with evidence).

---

## Deliverable

`docs/lab/knowledge/ingest_1gb/gaps/GAPS_VERDICT.md`: root cause per gap,
closure evidence per gap (or verified-correct-rejection proof), updated fact
counts, SHA table, and the corrected REPORT.md caveats. Committed to
`tnn-native-lab`.
