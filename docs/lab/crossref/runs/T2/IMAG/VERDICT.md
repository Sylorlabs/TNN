# T2-IMAG — VERDICT (replication crew report)

Crew: T2-IMAG (REPLACEMENT — predecessor killed mid-run by runtime daemon restart 2026-09-23).
Type A: full rerun from committed sources in a clean checkout. Date: 2026-09-23 (PDT).

## 1. Frozen prereg section (verbatim, extracted by this crew)

Source: `sylorlabs/TNN`, branch `tnn-native-lab`, commit
`7b2100d09911c5c10252c5756c7def288e70bd1f`,
`docs/lab/crossref/PREREG_TIER2.md`, section T2-IMAG (blob
`b1178370036bffbda6eb68ea0989c0e427dc31b7`, decoded and byte-verified by this crew):

> ## T2-IMAG — imagination trial: TNN can imagine (Type A)
>
> **Claims:** commit `a39aadf`: mechanism constructs, holds, edits, and answers questions about internal scenes with zero external rendering — 36/36 scene QA in both machine-way (RGB/coords/frequencies) and human-way (warm, balanced, tense) modes vs 2/36 text-only control; logo-redesign taste showdown vs documented human preferences: machine-way 6/8, human-way 4/8 → preregistered MARGINAL band, no winner between modes; video imagination 12/12 both modes on the temporal battery (trajectory, speed change, re-entry, midpoint). Pending (excluded): Q4 blind ratings packet.
> **Method:** rerun the scene-QA, taste, and video-temporal batteries from committed sources in clean checkout; ≥3 byte-identical.
> **Rule:** REPRODUCED if 36/36 both modes, 2/36 control, 6/8 vs 4/8 MARGINAL, 12/12 both video modes; NOT REPRODUCED if the control scores above 2/36 (mechanism claim breaks) or any battery figure differs.

## 2. Claims checklist — committed vs measured

| # | Claim (frozen) | Committed | Measured (this rerun) | Match |
|---|---|---|---|---|
| 1 | Scene QA, machine-way (RGB/coords/frequencies) | 36/36 | **36/36** | ✅ |
| 2 | Scene QA, human-way (warm, balanced, tense) | 36/36 | **36/36** | ✅ |
| 3 | Text-only control | 2/36 | **2/36** (both modes) | ✅ |
| 4 | Logo taste, machine-way | 6/8 | **6/8** | ✅ |
| 5 | Logo taste, human-way | 4/8 → MARGINAL, no winner | **4/8** → MARGINAL, \|6−4\|=2 → NO-DIFFERENTIATION | ✅ |
| 6 | Video temporal, machine-way (trajectory, speed change, re-entry, midpoint) | 12/12 | **12/12** | ✅ |
| 7 | Video temporal, human-way | 12/12 | **12/12** | ✅ |
| — | Q4 blind ratings packet | EXCLUDED (pending) | not run (excluded per prereg) | n/a |

Scoring: `verify_imag.py` (committed, unmodified) for Q1/Q3; `verify_q1v.py`
(committed, unmodified) for Q1V; text-only control via committed
`verify_q1_textonly.py` logic (only its two hardcoded absolute path
constants repointed to the local mirror — byte-diff of the patch proves
logic untouched).

Byte-identity (the prereg's cross-reference criterion — digests must match exactly):

| Battery | Committed SHA256 (from committed SHA256SUMS) | This rerun (3 reps Q1/Q3, 5 reps Q1V) |
|---|---|---|
| q1 machine | `df2d1b1c72150f214e9744263b9611c7099b31565c92a248e4e9befed34c1e48` | identical, all reps |
| q1 human | `d5eede6f8a11d4831996df9a251924b0be1d7dbbd9fc1f1509b7fea08eef4152` | identical, all reps |
| q3 machine | `f7f82ae06399720f8da6365545e28876de19399f515277bd3ad9fdc930288f52` | identical, all reps |
| q3 human | `cfbaecf87186650a494df4ea5b6ec100406197fdb122ccd71b60f5f62dbc0ad2` | identical, all reps |
| text-only control | `71d3738f6d8980ee37b7303202ea8c3af588d79f2d68072577049aa8a70b8ce3` | identical |
| q1v machine | `55b26e0579528345ee218668557227d1fe6f3806f2566bd7b76c5fea6a221f40` | identical, all 5 reps |
| q1v human | `5bb4428240b6591662339150330275548c4a22c6277f7d4d5c84799b1190faa3` | identical, all 5 reps |

Q3 per-pair detail (matches committed RUN-LOG table exactly): machine hits
Gap/Tropicana/New Coke/UC/Mastercard/Apple, misses Cracker Barrel +
Starbucks; human hits Gap/Tropicana/New Coke/UC, misses Cracker Barrel +
all three MODERATE pairs. Zero ties. STRONG tier 4/5 both modes; MODERATE
machine 2/3, human 0/3.

Control detail: text-only lookup hits are scene 5 q1 and scene 7 q1
(answer=4 appears verbatim) in both modes — 2/36, well under the <12/36 guard.

## 3. Verdict

**REPRODUCED.** Every battery figure matches the committed value exactly:
36/36 both scene-QA modes, 2/36 control (not above 2/36 — mechanism claim
holds), 6/8 vs 4/8 taste → MARGINAL band with no mode winner, 12/12 both
video-temporal modes. No battery figure differs. Q4 remains excluded per
the frozen prereg.

## 4. Frozen pins (recorded before running)

- Frozen crossref prereg: `sylorlabs/TNN` @ `tnn-native-lab`,
  `7b2100d09911c5c10252c5756c7def288e70bd1f` (verified via GitHub API;
  commit message "crossref: scope + frozen preregs…", 2026-09-22T22:54:44Z).
- Evidence pin (Q1/Q3/control): `a39aadf` → full
  `a39aadf6e563ca470c37a4770afbe350c023c98b` ("Imagination-design trial:
  mechanism, evidence, verdicts", 2026-09-22T05:07:31Z). ✅ present as expected.
- Evidence pin (Q1V video battery): `4d1a40ecaa` → full
  `4d1a40ecaaecaf53cd13cf492737f605d17f35a2` ("imagination: Q1V video
  battery PASS 12/12 both modes; taste probe verdict;", 2026-09-22T05:26Z).
- znc: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
  `znc 2026.07.0-dev (edition 2026)`, flags
  `--no-zagd --no-analyze --no-foreground-cache` (matching the trial RUN-LOG).
- IO substrate: `R33_NATIVE_IO_V1.zag` from the committed tree
  (`docs/lab/wave1/toolchain/R33_NATIVE_IO_V1.zag` at each pin; byte-identical
  between the two pins — `git diff` shows no change).

## 5. Caveats and findings (do not affect the verdict)

1. **Video pin correction.** The frozen T2-IMAG section attributes the video
   battery to commit `a39aadf`, but Q1V does not exist at `a39aadf` — there
   it is only a *proposed* amendment (`PROPOSED-amendment-video-2026-09-22.md`,
   "NOT APPLIED"). The battery was built, run, and committed at
   `4d1a40ecaa` (same branch, ~19 min later). The diff `a39aadf..4d1a40ecaa`
   on `imagine.zag` is purely additive for Q1V (207 insertions, 1 removed
   line = an updated comment); all Q1/Q2/Q3 code paths are untouched, so the
   Q1/Q3/control figures verified at `a39aadf` stand for both pins. Later
   commits touching `docs/lab/imagination/` (9b7fb3d85c, 852e0b9317,
   ab51007283) only *added* new files (emit.zag, field.zag, …) and never
   modified `imagine.zag` or any battery — verified via commit file lists.
   **Recommendation:** amend the frozen pin to `a39aadf` (Q1/Q3/control) +
   `4d1a40ecaa` (Q1V), or accept this report as the documented correction.
2. **Import placement.** `imagine.zag` does
   `@import("../../toolchain/R33_NATIVE_IO_V1.zag")`, resolved by this znc
   build relative to the source file's directory (empirically: the error
   message showed `../toolchain/…` when invoked as `src/imagine.zag` from the
   trial dir). No such path exists in the committed tree — the original crew
   must have placed it untracked. This crew used the byte-identical
   committed copy from `docs/lab/wave1/toolchain/`, placed at the
   import-expected location inside the scratch build mirror (never in
   `clean/`). Build fidelity is proven, not assumed: znc reported
   `205365 bytes main` for the `a39aadf` build — exactly the byte count in
   the trial RUN-LOG ("205365 bytes after the 2026-09-22 Q3 rebuild") — and
   every run log reproduces the committed SHA256 digests.
3. **Q2 design generation** (12/12, 12/12, 24/24 in the trial VERDICT.md) is
   committed evidence at `a39aadf` but is NOT part of the frozen T2-IMAG
   claims or decision rule (the frozen method names only scene-QA, taste,
   and video-temporal batteries). Not rerun; noted for completeness.
4. **Q4** excluded per the frozen prereg (blind ratings packet pending a
   human rater). Not run.
5. Predecessor state: the prior crew left only `crew/CREW_NOTES.md` (clone in
   progress, pins, znc path, TMPDIR) and an empty `clean/.git` (clone killed
   mid-run). No partial battery outputs existed to resume; this crew
   re-cloned from scratch and recorded the inherited notes in RUNLOG.md.
6. Environment incident: a stale `git clone` process from the first timed-out
   attempt later reaped the recreated `clean/` directory mid-task (see
   RUNLOG.md). Recovered by re-init + shallow `--filter=blob:none` fetch +
   sparse checkout of `docs/lab/imagination` only (the full tree is far too
   large for a full checkout on this VM). The sparse checkout contains every
   file the batteries need; `git status` clean, `git fsck` clean at both pins.

## 6. Reproduction recipe (for auditors)

```
# clean checkout (sparse; full tree is GBs of unrelated generations dumps)
git init clean && cd clean && git remote add origin https://github.com/sylorlabs/TNN.git
git fetch --depth 1 --filter=blob:none origin a39aadf6e563ca470c37a4770afbe350c023c98b
git sparse-checkout init --cone && git sparse-checkout set docs/lab/imagination
git checkout a39aadf6e563ca470c37a4770afbe350c023c98b
# build mirror: docs/lab/imagination/{src/imagine.zag @ a39aadf} + docs/lab/toolchain/R33_NATIVE_IO_V1.zag
#   (substrate bytes from docs/lab/wave1/toolchain/R33_NATIVE_IO_V1.zag @ same commit)
cd <mirror>/docs/lab/imagination
znc --no-zagd --no-analyze --no-foreground-cache src/imagine.zag -o src/imagine_bin
./src/imagine_bin q1 m all | sha256sum   # expect df2d1b1c…
./src/imagine_bin q1 h all | sha256sum   # expect d5eede6f…
./src/imagine_bin q3 m    | sha256sum   # expect f7f82ae0…
./src/imagine_bin q3 h    | sha256sum   # expect cfbaecf8…
# repeat for Q1V at 4d1a40ecaa: ./src/imagine_bin q1v m all → 55b26e05…; q1v h all → 5bb44282…
python3 verify_imag.py --q1m <q1m> --q1h <q1h>   # expect 36/36 both
python3 verify_imag.py --q3m <q3m> --q3h <q3h>   # expect 6/8, 4/8, MARGINAL, NO-DIFFERENTIATION
python3 verify_q1v.py <q1vm>                      # expect 12/12
```

Run dir: `~/workspace/scratch-crossref/T2/IMAG/crew/` (this VERDICT.md,
RUNLOG.md, build mirrors under `build/` and `build_v/`, run logs under
`build*/docs/lab/imagination/runs/`).
Clean checkout: `~/workspace/scratch-crossref/T2/IMAG/clean/` (sparse,
resting at `a39aadf`, `git status` clean).
