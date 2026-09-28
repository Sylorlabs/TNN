# RUNLOG.md — T2-TRACKA (replacement replication crew, Wave 2 / Tier 2)

## 0. Task and authority

- Role: T2-TRACKA replacement replication crew (representation Track A closeout).
- Frozen prereg: `docs/lab/crossref/PREREG_TIER2.md`, section **T2-TRACKA**, at commit
  `7b2100d09911c5c10252c5756c7def288e70bd1f` (repo `sylorlabs/TNN`, branch `tnn-native-lab`).
- Required deliverables: `VERDICT.md` + `RUNLOG.md` under
  `~/workspace/scratch-crossref/T2/TRACKA/crew/`.
- Method: Type C — re-derive the verdict sheet from committed arm evidence; verify a
  sample of kill/pass applications with independent Zag checks. Pure Zag for
  reasoning/verification; Python only as glue; zero RNG; ≥3 identical runs.

## 1. PIN CORRECTION (coordinator, 2026-09-22 23:15 PDT)

The coordinator issued a PIN CORRECTION: the evidence pin `02ffbc1be27a` in the
original brief was a **transcription artifact** — it returns HTTP 422 "No commit
found" in `sylorlabs/TNN` and does not exist as a git object (`git cat-file -t`
invalid, `git fetch origin` → "couldn't find remote ref", no SHA prefix match in
`git rev-list --all`, GitHub commits API 422).

**Discrepancy recorded:** the brief's §1 "expected freeze pin" did not exist, so the
clean-environment STOP rule predicated on it could not fire meaningfully. Per the
correction, the pin is DISREGARDED. Authority reverts to the frozen prereg itself:
the T2-TRACKA pins were extracted from `PREREG_TIER2.md` at the frozen commit
`7b2100d09911c5c10252c5756c7def288e70bd1f` and each was verified to resolve via the
GitHub API before running:

| Pin (from frozen prereg) | GitHub API resolution | Result |
|---|---|---|
| `1706708005a9` (closeout verdict) | `1706708005a9a348cb710f6e2a65427ae700cc1e` — "Track A consolidated verdict sheet: provisional blowout Y5 (cross-stream span se…" | RESOLVES |
| `76849610b8` (arm R kill) | `76849610b897075bfcbc6201c0a7e55f70480f00` — "Arm R: optimization port, bug fix, 1x battery, KILL verdict" | RESOLVES |

Both pins resolve. Work proceeded on the prereg's authority. The GitHub API was used
**only** to confirm pin existence, never to recapture evidence (all evidence read
from the frozen local clone).

## 2. Predecessor state and reclone

- At 2026-09-23 04:04 UTC the predecessor's `clean/.git` was an unborn repository
  (no refs/commits); `crew/` was empty.
- Initial large fetches timed out; a filtered/deep fetch then succeeded.
- At ~05:19 UTC the clone's `.git` was found reduced to an empty object directory;
  it was reinitialized and refetched.
- A runtime service restart occurred ~05:47 UTC during sparse-checkout work; checkout
  state survived.
- `git fsck` / `git status` run before resuming; working tree is clean at
  `7b2100d09911c5c10252c5756c7def288e70bd1f`.
- Sparse checkout covers: `docs/lab/crossref/`, `docs/lab/tracka-closeout/`,
  `docs/lab/units/PREREG_FREEZE.md`, `docs/lab/units/arms/`.

## 3. Evidence inspected (all committed, frozen head unless noted)

- `docs/lab/tracka-closeout/TRACKA_VERDICT_SHEET.md` — final amended sheet (§3 §6 §7 §8 §10).
- `docs/lab/tracka-closeout/scorecards/_manifest.json` + 47 JSON scorecards (33 arms).
- Closeout verdict commit `1706708005a9a348cb710f6e2a65427ae700cc1e` (2026-09-21 10:05:53 -0700):
  original consolidated sheet — "Y5 provisional blowout", body count **16 / 20 / 13 / 3**,
  I1 classified **PROVISIONAL**.
- Arm verdicts: R (`76849610b8` — OR-kill M1 clause), G2 (<2pt binding), T (→X degeneration),
  K1 (`d85f42c` — kill (ii)), U (`9c6d938` — PASS), F-B (`d2c35d7` — KILLED), F-S (PROVISIONAL),
  I1 final (`074153044897cdffa2b8971d2ee435057c4a59ab`, 2026-09-21 14:05:20 -0700 — **KILLED**,
  kill (ii); file unchanged to frozen head).
- I1 chronology: `8feb65b` (00:09, "survives all kill criteria") → `3af67c0` (03:46, kill (ii)
  SURVIVE on synthetic corpus) → `1706708` (10:05, PROVISIONAL) → `0741530` (14:05, KILLED).
- U adjudication `docs/lab/units/arms/U/ADJUDICATION.md`: M1 100.0% recall / 99.9% boundary,
  M4 93.0/100.0, M3 100.0/CLEAR.
- Frozen `docs/lab/units/PREREG_FREEZE.md` §3 arm table (52-arm count check).
- F-S final verdict: **PROVISIONAL** (kill (iii) blocked on D's M3).
- Y5 10× leg: complete/confirmed at `f225a71f` (frozen head).

## 4. Independent Zag verification

- `gen_verify.py` (Python glue) emits `verify_tracka.zag` from the extracted scorecard
  values; all verification LOGIC is hand-designed Zag (straight-line §7 champion
  computation with tax-then-cost tie-breaks, integer-milllis harmonization arithmetic,
  kill-criterion boolean re-derivation). Zero RNG.
- Built with the pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  (Two build iterations: `!` is not valid Zag — rewrote with De Morgan; `pname` needed an
  explicit `void` return type. L0012 string-leak warnings only; harmless for a verifier.)
- Ran **3× byte-identical**: SHA-256 `170d6cee8cbafd983e0e5720694952f8de6685a8729675303be98a3f34148f68`
  (`run1.txt`, `run2.txt`, `run3.txt`), exit code 0, `VERIFY=PASS`.
- Zag independently re-derived:
  - Harmonization: U = 2.902 B/B, Y5 = 1.659 B/B, margin 74.9%, tie-break Y5 < U.
  - Champions: Y5 wins M1-content, M1-boundary, M2, M3, M4, M6-tax, M7 (7/8); L1 wins M5.
  - Kill applications: R (OR-clause), G2 (<2 pts), T (→X), I1 (kill ii, 22.1% > 20%),
    K1 (kill ii) — all correctly applied.
- `metrics.tsv` / `extract_metrics.py`: scorecard extraction (glue). Known messiness:
  several arms lack closeout scorecards (B-64, D, R, T, U, W, … — verdict-only or
  thesis arms); K2's M1 stored in tenths; X's M2 "50+"; arm-name normalization
  required. None affect the decided columns (all threats checked per sheet §6).
- 52-arm count: 49 §3 table rows; B row expands to 3, C row to 2 → **52** distinct arms.
  The footer's "48 rows → 53 arms" is arithmetically wrong on its own terms
  (48−2+3+2=51≠53; actual rows=49). Y2 absent (unfrozen). Correction VERIFIED.

## 5. I1 adjudication (explicit, not punted)

- Correct source: final committed arm verdict `0741530` (2026-09-21 14:05:20 -0700),
  ancestor of frozen head; file byte-identical at frozen head.
- Deciding evidence: prose maintenance-churn audit 24,164/109,295 = **22.1%** > frozen
  20% kill bar → **kill (ii) FIRES**. (The earlier 12.4% "survive" was a 512-unit
  synthetic corpus that formed only L1 chunks; the final verdict explicitly supersedes it.
  Kill (i) survived; kill (iii) blocked — not needed for the binding verdict.)
- **I1 = KILLED.** The prereg's "I1 SURVIVES" phrase is stale (matches superseded
  `8feb65b`); the prereg's own "F-B, R2, I1 killed" phrase is the correct one.

## 6. Files in this directory

- `VERDICT.md` — final verdict (this crew's deliverable).
- `RUNLOG.md` — this file.
- `PREREG_TIER2.frozen.md` — frozen prereg section (reference).
- `TRACKA_VERDICT_SHEET.committed.md` — committed verdict sheet snapshot (reference).
- `verify_tracka.zag` / `gen_verify.py` — independent Zag verifier + generator (glue).
- `run1.txt` / `run2.txt` / `run3.txt` — 3× byte-identical verifier outputs (SHA above).
- `metrics.tsv` / `extract_metrics.py` — scorecard extraction (glue).
- `logs/` — predecessor logs.

## 7. Non-interference

All work confined to `~/workspace/scratch-crossref/T2/TRACKA/`; no commits, no builds
inside the repo clone except reads; compiled verifier binary removed after the 3 runs
(sources and outputs retained). No live workstreams touched.
