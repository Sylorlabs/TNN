# T2-INFORICH VERDICT — information richness: emergence confirmed (Type C)

Crew: T2-INFORICH (REPLACEMENT — predecessor killed mid-run by the 2026-09-23
runtime daemon restart; no predecessor RUNLOG/VERDICT existed, fresh start).
Wave 2, Tier 2, authorized by Micah's 2026-09-22 "run everything" ruling.
Method: Type C — committed-evidence re-derivation. NO live-web recapture.

## 1. Frozen claims checklist (exact quote from the frozen prereg)

Source: sylorlabs/TNN branch `tnn-native-lab`, commit
`7b2100d09911c5c10252c5756c7def288e70bd1f`,
`docs/lab/crossref/PREREG_TIER2.md` §T2-INFORICH (extracted by this crew
directly from the frozen commit via the GitHub API; not from any summary):

> ## T2-INFORICH — information richness: emergence confirmed (Type C)
>
> **Claims:** commit `25c2a18b2416`: facts-only learner absorbs 12/12 planted
> falsehoods; with live web-search sense, read-only installs 0/12, catches
> 12/12, answers 4/4 unknowns provisionally; corroboration-gated editable
> installs 0/12 falsehoods, installs the true value on all 12, answers all 4
> unknowns; corroboration-gated still installs colluding-domain spoofs 2/2
> (sensor-deceivable boundary). Three axes: parameters→cost, mechanisms→resolve
> competing claims, information→decides truth.
> **Method:** Type C — re-derive all figures from committed evidence; independent
> check of the 2/2 colluding-spoof installs.
> **Rule:** REPRODUCED if all figures re-derive; PARTIAL if any axis figure
> differs (name it).

Claim checklist used for the verdict:
- C1. Facts-only learner absorbs 12/12 planted falsehoods.
- C2. With live web-search sense, read-only: installs 0/12, catches 12/12,
  answers 4/4 unknowns provisionally.
- C3. Corroboration-gated editable: installs 0/12 falsehoods, installs the true
  value on all 12, answers all 4 unknowns.
- C4. Corroboration-gated still installs colluding-domain spoofs 2/2
  (sensor-deceivable boundary).
- C5. Three axes: parameters→cost, mechanisms→resolve competing claims,
  information→decides truth.

## 2. Frozen pins

| Pin | Expected | Found |
|---|---|---|
| Frozen prereg | `7b2100d09911c5c10252c5756c7def288e70bd1f` | EXISTS (API-verified; "crossref: scope + frozen preregs…") |
| T2-INFORICH evidence (per frozen §T2-INFORICH) | `25c2a18b2416` | EXISTS → `25c2a18b2416e6d1b80d7d11771d3909c9eddee6` ("info-source: falsehood detection emerges with information richness", 2026-09-22T02:25:10Z) |
| Task-template pin | `23c4fc6ea5a9` | **MISSING — discrepancy.** GitHub API: 422 "No commit found for SHA: 23c4fc6ea5a9" in sylorlabs/TNN and sylorlabs/zag; zero occurrences in any workspace `.md` or in `scratch-crossref/`. DECISION: the frozen prereg is authoritative per the task's own §1 ("the prereg section governs"); its evidence pin resolves and matches this family. Proceeding on `25c2a18b2416`; the template SHA is recorded as an unresolved discrepancy, not a stop condition. |
| znc toolchain | `…/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` | EXISTS on disk; used for all builds |

Clean checkout: fresh git repo at `~/workspace/scratch-crossref/T2/INFORICH/clean/`,
`git fetch --filter=blob:none --depth=1 origin 25c2a18b2416…` +
`git checkout 25c2a18b2416… -- docs/lab/info-source`. `git fsck` clean
(only the expected dangling single-commit notice). Checked-out blob SHAs for
PREREG.md/VERDICT.md match the API-fetched blob SHAs independently.

## 3. Re-derivation performed

Three independent legs, all pure Zag for reasoning/verification (Python glue
for I/O and mechanical transforms only), zero RNG:

**(a) Full-pipeline rebuild from committed source.** `src/is_trial.zag` +
`src/is_cases.zag` + `src/ws2_sense.zag` compiled with the pinned znc (build
warnings only — L0012 string-buffer-leak lints, non-fatal). Ran `all` 3× and
each arm 3×:
- 3/3 full runs: sha256 `cda86333df6d83b79e6da671227ce64045bd2cacab2fb1b27322bf8f698a0a81`
  — byte-identical to committed `runs/run_1.txt`…`run_5.txt` and to the hash
  pinned in committed `SHA256SUMS` and `VERDICT.md`.
- Per-arm 3/3: R0 `af63c7e0…73862`, R1 `2fe7843e…0c89d2`, R2 `fc57de6b…0510ca`
  — all byte-identical to the committed per-arm runs. Exit code 0 every run
  (all per-case assertions in the trial's check functions passed, including
  the R1 install-refusal `rc==8` assertions and the R2 stored-value assertions).

**(b) Independent extraction cross-check (glue).** Re-applied the frozen
mechanical rule (V-regex first, case-insensitive, over title+" "+snippet, per
committed `gen_is.py`) to all 16 frozen `live/*.json` envelopes: every
per-result (domain, answer) pair re-extracts exactly as embedded in committed
`src/is_cases.zag` (0 mismatches over 140 results). C1/C2/C3/C4 hand-assemblies
verified against the committed assembly code (C3 = two DISTINCT domains,
rebuilt per the documented fix); S1/S2 spoof constructions verified as exactly
`spoof-1.example`/`spoof-2.example` with answers Poseidonia/Uo. Spot
re-computation of sha256 tamper hashes over whitespace-collapsed runtime bytes
for all quote-bearing results: 0 mismatches (the build note's hash-convention
fix holds). Committed run-log internal consistency: all 44 R1/R2 case lines
present with G1, all 12 R0 lines `slot=0`, all 9 SUMMARY lines and
`VERDICT|all|PASS` as committed.

**(c) Independent Zag verifier (`indep_is.zag`, written from scratch, shares no
code with the artifact).** Re-implements the frozen decision rule from the
frozen prereg (top first-seen answer; ≥2 → PROVISIONAL if single answer else
PROVISIONAL_MAJORITY; else WITHHOLD; exact (domain,answer) dedup; cap-6; rel=1
+ non-empty filter) over the 22 cases / 140 results parsed from committed
evidence, and derives every claim figure:
- 20/20 case dispositions + chosen answers agree with the committed
  `CASE_MANIFEST.txt` AND with the committed run logs (C1=2, C2=6/Everest,
  C3=1/Paris, C4=2, all F/U=1 with the true value).
- V-domain counts agree with the manifest everywhere except F08 and U02
  (7→6): the mechanism's documented cap-6 (`ws_add_result`: `if(n<6)`)
  drops the 7th V-domain result (answers.com / periodictable3d.com). This is
  the mechanism's own committed rule, faithfully replicated — an observation,
  not a claim difference; the prereg premise (≥2 V-domains) holds either way.
- 3/3 byte-identical runs, exit 0, `INDEP_VERDICT|PASS`.

**Independent check of the 2/2 colluding-spoof installs (per the frozen
Method):** S1/S2 each have exactly 2 distinct supporting domains
(`spoof-1.example`, `spoof-2.example`), unanimous on the fiction
(Poseidonia / Uo) → disp=1. R1: provisional-wrong with no install (read-only
by construction — re-verified via the rebuilt trial's `rc==8` refusal
assertions). R2: R-CORR fires (≥2 independent domains agree, fresh handle so
no contradicting installed belief) → 2/2 spoofed values installed. The
sensor-deceivable boundary reproduces exactly as the frozen prereg describes.

Kill bars from the frozen info-source `PREREG.md` §4, applied mechanically to
the re-derived figures: KB-R0-BASE 12/12 ≥10 PASS; KB-CATCH 0/12 & 0/12 PASS;
KB-CATCH-RATE 12/12 ≥10 PASS; KB-CORR-INSTALL 12/12 ≥10 and 4/4 ≥3 PASS;
KB-CONTEST 4/4 PASS; KB-SPOOF-RESIDUAL reproduced honestly PASS;
KB-DET byte-identical (committed 5/5, this crew 3/3 rebuild + 3/3 verifier) PASS.

## 4. Verdict: REPRODUCED

| Claim | Committed | Re-derived (this crew) | Status |
|---|---|---|---|
| C1 facts-only absorbs 12/12 | 12/12 | 12/12 — rebuilt trial: all 12 teacher claims installed verbatim (`slot=0`, value==teacher); independent verifier: 12/12 | re-derived |
| C2 read-only installs 0/12 | 0/12 | 0/12 — structural (no install path; rebuilt trial's check fns assert install-refused `rc==8` and no installed fact on all 16 search cases) | re-derived |
| C2 read-only catches 12/12 | 12/12 | 12/12 — independent verifier from committed case data | re-derived |
| C2 answers 4/4 unknowns provisionally | 4/4 | 4/4 — independent verifier; run logs agree | re-derived |
| C3 gated installs 0/12 falsehoods | 0/12 | 0/12 — independent verifier (no case has chosen==teacher with disp∈{1,6}) | re-derived |
| C3 installs true value on all 12 | 12/12 | 12/12 — independent verifier; rebuilt trial asserts stored==V per case | re-derived |
| C3 answers all 4 unknowns | 4/4 | 4/4 — independent verifier; run logs agree | re-derived |
| C4 gated installs colluding spoofs 2/2 | 2/2 | 2/2 — independent check (domains, unanimity, R-CORR firing, R1 provisional-wrong + 0 installs) | re-derived |
| C5 three axes | interpretation | Follows from C1–C4: the capability jump tracks the information environment, not arm parameters. The parameter-axis premise (16/19 param configs byte-identical, zero truth-detection at any size) is cited external evidence, out of scope for this Type-C re-derivation — recorded honestly, not re-tested. | re-derived as conclusion |

No axis figure differs. Per the frozen rule: **REPRODUCED**.

## 5. Caveats / notes for the parent

1. **Pin discrepancy (recorded, non-blocking):** the task template named
   expected pin `23c4fc6ea5a9`; it does not exist in sylorlabs/TNN or
   sylorlabs/zag and appears nowhere in the workspace. The frozen prereg —
   authoritative per the task — names `25c2a18b2416`, which resolves and is
   exactly this family's evidence commit. Recommend the parent check whether
   `23c4fc6ea5a9` was a template copy-paste error.
2. **Cap-6 observation:** F08/U02 show 7 pre-cap V-domains in the manifest but
   6 in the mechanism's view (documented `if(n<6)` rule). Not a claim
   difference; the verifier replicates the mechanism exactly.
3. **C2 semantic ambiguity** (Everest vs Mauna Kea) stands as the committed
   verdict's caveat #2 — confirmed present as described.
4. Build artifacts (`is_trial_rebuild`, `indep_is_bin`, run outputs) live in
   `crew/` (scratch, never `/tmp`); nothing committed anywhere by this crew.
   A predecessor `clean/` dir vanished mid-run (04:15→05:20 UTC, cause
   unknown); it was recreated and re-fetched — recorded in RUNLOG.
5. Type-C boundary respected: no live web access was used at any point; all
   figures come from the frozen recorded envelopes.

## 6. Deliverable paths

- [VERDICT.md](sandbox://workspace/scratch-crossref/T2/INFORICH/crew/VERDICT.md)
- [RUNLOG.md](sandbox://workspace/scratch-crossref/T2/INFORICH/crew/RUNLOG.md)
- Independent verifier: `crew/indep_is.zag` (+ generated `crew/indep_data.zag`),
  glue `crew/extract_indep.py`; clean checkout `clean/docs/lab/info-source/`.
