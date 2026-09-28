# VERDICT — T2-SENSESINT (replacement crew)

**Family:** T2-SENSESINT — senses-integrity: 140/140 (Type C: committed-evidence re-derivation)
**Verdict: REPRODUCED** (amended 2026-09-23 — see §10; original PARTIAL verdict in §§1–9 stands as the record at closeout time)
**Crew:** T2-SENSESINT REPLACEMENT (predecessor killed by daemon restart; no inherited state)
**Date:** 2026-09-23

## 1. Frozen prereg section (verbatim, authoritative)

Source: `docs/lab/crossref/PREREG_TIER2.md` at frozen commit
`7b2100d09911c5c10252c5756c7def288e70bd1f`
(blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`):

> ## T2-SENSESINT — senses-integrity: 140/140 (Type C)
>
> **Claims:** worker COMPLETED: 140/140 manifest items; VERDICT_SHEET.md in `docs/lab/GROK47_OVERNIGHT/senses-integrity/`; info-source verdict spot-verified vs evidence; sol red-team attack #2 SUSTAINED as headline-reframing (R0→R2 confounds information with gating policy; proposes IS-R3 arm); cross-item: KB4 failure + web-search spoof residual = same structural hole (corroboration gates disagreement, not collusion/confident error; neither rule family calibrates confidence).
> **Method:** Type C — re-derive the 140/140 from committed evidence; verify the spot-verification claim on a sample.
> **Rule:** REPRODUCED if 140/140 re-derives; PARTIAL if any item's evidence is missing (name it).

## 2. Pins frozen (before running)

| Pin | Value | Status |
|---|---|---|
| Prereg commit | `7b2100d09911c5c10252c5756c7def288e70bd1f` | VERIFIED (`git rev-parse HEAD` after checkout) |
| Toolchain | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` | VERIFIED present/executable |
| Evidence commit | `6d30417e6db9` (2026-09-22, "GROK47 overnight: 7 sector verdict sheets…", 80 files — the only commit touching the evidence dir) | Recorded |
| Task-named pin `ddc9a1b04f1a` | — | **TRANSCRIPTION ARTIFACT — does not exist.** Exhaustively checked: GitHub commits API 422 on sylorlabs/TNN, zag, ghost_engine, ghost_cli, ghost_research, zag-grammar; full tnn-native-lab history paged (no SHA with that prefix); blob/tree/sha256 checks; org code search = 0 hits. The frozen prereg names no such pin. Parent's own PIN AUDIT (2026-09-23 ~06:10 UTC, `_wave2_tally/VERDICTS.md`) independently lists `ddc9a1b04f1a (SENSESINT)` as a transcription artifact and directs crews to fall back to prereg pins. Fell back to prereg pins per that audit. |

## 3. Method

Pure-Zag verifier `t2_sensesint_verify.zag` (built from source with the pinned
znc; no `.zagd`/binary copies), run from the frozen checkout root against the
committed `ITEMS_DONE.tsv`. For each of the 140 rows it: parses the TSV,
checks `status=done`, tallies tiers, checks for duplicate paths, opens
`docs/lab/<path>` at the frozen commit and compares the committed byte size
(via fstat) against the manifest's `size` field. It then spot-checks the
info-source verdict headlines (claim 3) and the VERDICT_SHEET §9/§12 phrases
(claims 4–5) by substring search over the committed files. Zero RNG.
**3 runs, byte-identical** (sha256 `8886a7f8147d6488c9f1f53fc8135a70d8848910614555541e21be0248636985`).

## 4. Claim-by-claim findings

| # | Frozen claim | Measured | Holds? |
|---|---|---|---|
| 1 | worker COMPLETED: 140/140 manifest items | TSV has exactly 140 data rows; all 140 `status=done`; tier split 65 P0 / 62 P1 / 10 P2 / 3 P3 — exactly the split VERDICT_SHEET §13 claims; 0 duplicate paths | Record re-derives: YES |
| 2 | VERDICT_SHEET.md in `docs/lab/GROK47_OVERNIGHT/senses-integrity/` | Present at frozen commit (28,492 bytes); full text read and quoted in RUNLOG | YES |
| 3 | info-source verdict spot-verified vs evidence | Committed `docs/lab/info-source/VERDICT.md` carries every headline the VERDICT_SHEET §9 says was spot-verified: R0 arm hash prefix `af63c7e0` (per-arm N=5 table), `12/12 true values installed`, `4/4 installed`, `2/2 spoofed values installed`, `EMERGENCE CONFIRMED` — 5/5 substring checks PASS | YES (on the committed record) |
| 4 | sol red-team attack #2 SUSTAINED as headline-reframing (R0→R2 confounds information with gating policy; proposes IS-R3 arm) | VERDICT_SHEET §9 text verified present: "**SUSTAINED — headline-reframing.** The R0→R2 comparison confounds information with policy… What the trial shows is: *corroborating information + a gating policy* stops teacher-absorption; no truth-detection capability emerged… proposed **IS-R3**: R0 install policy + search access" | YES, verbatim |
| 5 | cross-item: KB4 failure + web-search spoof residual = same structural hole | VERDICT_SHEET §12 text verified present: "**corroboration gates disagreement, not collusion or confident error**… the rebuild's KB4 failure (confident wrong percepts) and the web-search residual (confident unanimous spoof) are the same structural hole at two layers. Neither rule family calibrates confidence" | YES, verbatim |

## 5. Evidence-missing finding (drives the verdict)

**10 of the 140 manifest items have evidence paths that do not exist anywhere
in the frozen commit's tree** (verified via `git ls-tree` on the frozen
commit AND a full 23,715-file `docs/lab` tree listing — zero matches for
these basenames anywhere; zero commits in branch history ever touched these
paths; the evidence commit `6d30417e6db9` added only the two senses-integrity
files, never these):

- `senses/web-search/v2/src/gk1_trial.zag` (P0, PASS, manifest size 5285)
- `senses/web-search/v2/src/gk2_trial.zag` (P0, PASS, manifest size 6329)
- `senses/web-search/v2/src/gk3_trial.zag` (P0, PASS, manifest size 4235)
- `senses/web-search/internet-trial/evidence/phase1/blind-solo.jsonl` (P2, review-note)
- `senses/web-search/internet-trial/evidence/phase1/captured-solo.jsonl` (P2, review-note)
- `senses/web-search/internet-trial/evidence/phase1/corrupt-solo.jsonl` (P2, review-note)
- `senses/web-search/internet-trial/evidence/phase1/gullible-solo.jsonl` (P2, review-note)
- `senses/web-search/internet-trial/evidence/phase1/idle-solo.jsonl` (P2, review-note)
- `senses/web-search/internet-trial/evidence/phase1/oracle-helper.jsonl` (P2, review-note)
- `senses/web-search/internet-trial/evidence/phase1/oracle-solo.jsonl` (P2, review-note)

Severity: the 3 missing P0 files are the **GK1/GK2/GK3 trial sources** — the
load-bearing HTRF batteries behind "H1, H2, H3 all SUSTAINED" and the
`488af9ab…` / `7f351a53…` / `94575a9a…` digests. Their sources were never
committed (VERDICT_SHEET §13 says "sources retained" after removing untracked
binaries — but no such sources exist in the repo). The headline digests
cannot be re-derived from the committed record.

**2 further record-integrity mismatches** (evidence present, but manifest
record disagrees with committed bytes):
- `senses/rematch/code/kb5.py` — manifest size 2189, committed blob 2731
- `senses/rematch/code/run_all.py` — manifest size 4302, committed blob 5801
(Both P1, review-note. Working tree clean — the manifest measured different
file versions than what was committed.)

## 6. Verdict

**PARTIAL** — per the frozen rule's named condition ("PARTIAL if any item's
evidence is missing (name it)"): 130/140 items' evidence present with
matching sizes; 10 items' evidence missing (named above, incl. 3 P0);
2 items' manifest sizes disagree with committed bytes (named above).
The 140/140-done record itself re-derives, the tier split matches §13, the
info-source spot-verification claim checks out against the committed
verdict, and the §9/§12 texts are present verbatim. Nothing was re-run live
(Type C); the GK battery digests are unverifiable from the committed record.

## 7. Caveats / follow-ups for the parent

1. The missing GK sources may exist in the original worker's local scratch
   (`~/workspace/grok47/senses/gk-scratch/`, cited in VERDICT_SHEET §1 but
   local-only and outside clean-env rules). If they are committed, this
   verdict upgrades on re-run.
2. `clean/tnn/` vanished once mid-run (dir present, contents gone) — matches
   the Wave-2 "vanishing-tree" anomaly the parent is already tracking; the
   IMAG crew's zombie-clone hypothesis fits (my first clone attempt timed
   out at tool dispatch). Recovered via fresh blobless fetch; HEAD
   re-verified at the frozen commit before all measurements.
3. No live-web recapture was performed (Type C). The info-source "run files"
   (`runs/arm_r2_1.txt` etc.) cited in §9 were worker-local, not committed;
   claim 3 was verified against the committed VERDICT.md only.
4. Non-interference held: only the frozen checkout + own run dir touched;
   no live workstream files read or written.

## 8. Deliverables

- `~/workspace/scratch-crossref/T2/SENSESINT/crew/VERDICT.md` (this file)
- `~/workspace/scratch-crossref/T2/SENSESINT/crew/RUNLOG.md`
- `~/workspace/scratch-crossref/T2/SENSESINT/crew/t2_sensesint_verify.zag` (verifier source)
- `~/workspace/scratch-crossref/T2/SENSESINT/crew/run1.txt` (= run2/run3, byte-identical; sha256 `8886a7f8…`)
- `~/workspace/scratch-crossref/T2/SENSESINT/crew/frozen_section.txt` (verbatim frozen section)

---

## 9. Crew-of-record addendum (2026-09-22 ~23:15–23:45 PDT)

**Crew transition:** sibling crew f3e9de78 stood down by coordinator; this
session (247aa7b5, T2-SENSESINT REPLACEMENT) is the crew of record and adopts
the shared run state above, including the frozen pins, the pure-Zag verifier
`crew/t2_sensesint_verify.zag`, its 3 byte-identical runs (sha256
`8886a7f8147d6488c9f1f53fc8135a70d8848910614555541e21be0248636985`), and the
PARTIAL verdict.

**PIN CORRECTION (coordinator, 2026-09-22 23:15 PDT):** the task-named pin
`ddc9a1b04f1a` was a transcription artifact — GitHub commits API returns 422
"No commit found" in sylorlabs/TNN. DISREGARDED per the correction; the crew
proceeds on the frozen prereg's authority (which names no evidence-commit
pin; evidence frozen at prereg commit `7b2100d09911c5c10252c5756c7def288e70bd1f`
per SCOPE.md's unknown-pin rule). This matches the sibling's independent
exhaustive check and the parent's own PIN AUDIT
(`_wave2_tally/VERDICTS.md`, 2026-09-23 ~06:10 UTC), which reached the same
conclusion before the correction arrived.

**Independent confirmation by the crew of record** (method differs from the
sibling's — index-level `git cat-file`/`git ls-tree` on the frozen commit,
not sparse-checkout fstat; Python glue):
- ITEMS_DONE.tsv: 140 data rows, all `status=done`; tiers P0=65 / P1=62 /
  P2=10 / P3=3 (matches VERDICT_SHEET §13); verdicts 39 PASS / 98 review-note /
  3 inventory; kinds 49 md / 45 zag / 37 py / 9 jsonl. 0 duplicate paths.
- Evidence paths rooted at `docs/lab/`: 130/140 present; **10 missing**
  (identical list to §5: `senses/web-search/v2/src/gk{1,2,3}_trial.zag` —
  P0/PASS — plus 7 `senses/web-search/internet-trial/evidence/phase1/*.jsonl`
  — P2/review-note); missing basenames have zero hits in a full-tree
  basename scan of the frozen commit.
- **2 size mismatches**: `senses/rematch/code/kb5.py` manifest 2189 vs blob
  2731; `senses/rematch/code/run_all.py` manifest 4302 vs blob 5801 (working
  tree clean → manifest measured different versions than committed).
- Info-source spot-check against committed `docs/lab/info-source/VERDICT.md`:
  R0 arm hash prefix `af63c7e0` present in the per-arm N=5 table (line 91);
  R2 headline row present: 0/12 falsehoods absorbed, **12/12 true values
  installed**, **4/4** unknowns installed (Ouagadougou, W, Mariana Trench,
  Swiss franc), **2/2** spoofed values installed as the documented honest
  boundary, **EMERGENCE CONFIRMED** — all consistent with VERDICT_SHEET §9's
  "the info-source numbers stand."
- VERDICT_SHEET §9 (sol attack #2 SUSTAINED — headline-reframing; IS-R3
  proposed) and §12 (cross-item structural hole; "Neither rule family
  calibrates confidence") texts read verbatim from the frozen commit and
  match the prereg's claim language.
- Sibling run outputs re-verified: run1.txt = run2.txt = run3.txt,
  sha256 `8886a7f8147d6488c9f1f53fc8135a70d8848910614555541e21be0248636985`.
- Frozen prereg blob re-verified:
  `b1178370036bffbda6eb68ea0989c0e427dc31b7` (working tree = HEAD).

**Verdict (unchanged): PARTIAL** — 130/140 items' evidence present with
matching sizes; 10 items' evidence missing (named in §5, incl. the 3 P0
GK1–GK3 trial sources); 2 items' manifest sizes disagree with committed
bytes (named in §5). Nothing re-run live (Type C); the GK battery digests
(`488af9ab…` / `7f351a53…` / `94575a9a…`) are unverifiable from the
committed record. If the GK sources are committed, the verdict upgrades on
re-run.

---

## 10. Recovery amendment (2026-09-23, Wave-2 crossref evidence-recovery coordinator)

**Verdict: PARTIAL → REPRODUCED.** The frozen rule's named PARTIAL condition
("any item's evidence is missing") no longer holds.

Recovery executed per the frozen `RECOVERY_PREREG.md`
(`docs/lab/crossref/runs/T2/SENSESINT/RECOVERY_PREREG.md`, committed alone at
`a94cc0e7a4025edfb41635a15ec008176fe82b90`):

- **3 P0 GK sources RECOVERED** (restored from the frozen crew workdir
  `~/workspace/grok47/senses/gk-scratch/`, byte-identical, exact manifest sizes
  5285/6329/4235, zero edits, zero commits ever in branch history):
  `senses/web-search/v2/src/gk{1,2,3}_trial.zag` (commit
  `16ddf755fee7ab41765d961f01e0d2a3f0f2c875`).
- **7 P2 jsonl RECOVERED** (workdir copies, exact manifest sizes, all lines valid
  JSONL): `senses/web-search/internet-trial/evidence/phase1/*.jsonl` (commit
  `c9bd2b210f781eb60bc9ebcaa1a280225a758184`). No P2 downgrades needed.
- **3 manifest sizes CORRECTED** in `ITEMS_DONE.tsv` (kb5.py 2189→2731, run_all.py
  4302→5801 at `0e9b6ccf5eb42915fca58e9fcf0be49b1c0cc759`; PROPOSED_BARS.md
  11587→11846 at `79fb9a7b9b1494235b2b11e651a8107c8246fca7` — a third stale size
  the closeout checker missed, found by the coordinator's own 140/140 sweep).

**Digest re-derivation (honest bar, committed sources, pinned
`znc_linux_x86_64_abed8aa1`, N=3 runs each, zero RNG, zero source edits):**
GK1 `488af9ab375eae17cf65015240fb5c8a2f111ed6ca2eee354778b12b74a0db5c` —
**YES**; GK2 `7f351a53524d67fdb182357dcbf0215af526a6b70d7f6d66ce008d0c301fdf4b` —
**YES**; GK3 `94575a9a6c9e4aaa916676b6301a57d643c65f28d51d748f36492ac359814d13` —
**YES**. All three byte-identical across reruns and byte-identical to the crew's
original run logs; case-level outcomes and kill bars (tamper=1 only on GK2-15
positive control; GK1 7/7, GK2 8/8, GK3 4/4) match VERDICT_SHEET §3.

**140/140 verification at head:** recursive subtree trees
(`docs/lab/senses|redteam|info-source|mixed-web`) — 140/140 paths present,
140/140 sizes match the amended manifest.

Full record: `docs/lab/crossref/runs/T2/SENSESINT/RECOVERY_VERDICT.md`.
Caveats: recovery is restore-not-reimplementation; scratch verification preceded
the frozen prereg (recorded honestly in the verdict); concurrent branch commits
mean the parent should re-run the cheap tree check before closing the track in
`VERDICT_TABLE.md`; Type C — no live-web recapture of the internet-trial jsonl.
