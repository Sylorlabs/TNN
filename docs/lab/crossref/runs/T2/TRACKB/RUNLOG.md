# RUNLOG — T2-TRACKB (replacement crew)

## 2026-09-22 ~21:36 PDT — crew start (replacement after daemon restart)

**Inherited state** (from predecessor crew, killed mid-run by runtime daemon restart):
- `~/workspace/scratch-crossref/T2/TRACKB/clean/TNN/` — git clone of sylorlabs/TNN exists; `.git` object store intact (`git fsck` clean, no errors); working tree has ~35,945 uncommitted deletions (checkout interrupted by the restart). HEAD = `dbabd53e9ef0266f56a26bda217ac2acb4fc84bc` (main).
- `crew/PREREG_TIER2_FROZEN.md` — predecessor's frozen copy of the tier-2 prereg.
- `crew/SCOPE_FROZEN.md` — predecessor's frozen copy of the scope doc.
- `crew/evidence/TRACKB_VERDICT.md`, `crew/evidence/HARNESS_CLOSEOUT.md` — predecessor's evidence copies (will be re-extracted from git and byte-compared, not trusted).
- No predecessor VERDICT.md or RUNLOG.md existed; this log starts fresh.

**Frozen prereg extraction (done by this crew, not trusted from predecessor):**
- Extracted `docs/lab/crossref/PREREG_TIER2.md` at frozen commit `7b2100d09911c5c10252c5756c7def288e70bd1f` via `git show` → `/tmp/trackb_prereg_frozen_extract.md` (207 lines).
- `diff` vs predecessor's `crew/PREREG_TIER2_FROZEN.md`: **byte-identical**. Predecessor's copy is faithful.
- T2-TRACKB section is at line 89. Claims checklist and decision rule quoted verbatim in VERDICT.md.

## Pin freeze (BEFORE running) — recorded 2026-09-22

| Item | Expected (frozen prereg §T2-TRACKB) | Observed | Status |
|---|---|---|---|
| Frozen prereg commit | `7b2100d09911c5c10252c5756c7def288e70bd1f` | object type=commit, present | OK |
| Closeout head | `47c48d3e7cf9f` (full `47c48d3e7cf9f4033a3bfbb35e805b7a203775fe`) | "Track B closeout: finalize verdict sheet…" | OK |
| arm-1 DONE | `89745ce1117c` (full `89745ce1117ceff1909735b9d119d8ee7997a3b6`) | "Track B arm-1: parent-wired teacher in pure Zag, verified byte-identical"; ancestor of closeout | OK |
| C3 FORCE-PIN B.6 PASS | `d921459a` (full `d921459af52b9d37cdd8eec103adff9742c691e2`) | "Track B C3: B.6 force-pin implementation (PASS)"; ancestor of closeout | OK |
| pcodec fix | `4a6d898c1e66` (full `4a6d898c1e6653ae6e4c6266a4aac8efc7b39d76`) | "Track B W5 (learner+harness): pcodec repaired to frozen §B.3 + verdict sheet + verify evidence"; ancestor of closeout | OK |
| pcodec fixup | `6adb2fa5930c` (full `6adb2fa5930cec80db8b66798281dd80152e367b`) | "Track B W5: verdict-sheet SHA fill + frozen-hash typo fix"; ancestor of closeout | OK |

**DISPATCH-PIN DISCREPANCY (recorded, does not stop the run):** the dispatch text named an
"Expected" pin `8d0d6b9e9c9c` with "Missing → STOP → UNREPLICABLE-AS-IS". Exhaustive check:
- Not a git object locally (`git cat-file -t` → "Not a valid object name"); not in the local
  object store under any type.
- Not on the remote (`git ls-remote origin` → no ref; `git fetch origin 8d0d6b9e9c9c` →
  "couldn't find remote ref").
- GitHub API `GET /repos/sylorlabs/TNN/commits/8d0d6b9e9c9c` → HTTP 422 "No commit found for SHA".
- Not a substring of any prereg pin's full SHA; not referenced by any file in the closeout tree
  (`git grep -l "8d0d6b9" 47c48d3e7cf9f` → empty).
- **Not present anywhere in the frozen PREREG_TIER2.md §T2-TRACKB** (the AUTHORITATIVE source,
  extracted byte-identical by this crew). Sibling crews' convention ("Expected evidence pin
  (from frozen PREREG_TIER2.md §T2-…)") confirms the expected pin should come from the prereg section.
- Per the frozen SCOPE §2.2, the STOP condition is "a pin listed in the tier prereg doesn't hold
  the expected files" — every pin listed in the prereg holds. The dispatch pin matches nothing
  authoritative; treating it as a transcription/dispatch error per AGENTS.md ("verify EVERY task's
  spec text programmatically against the source document"). Run proceeds on the authoritative pins.

## Work plan (Type C — committed-evidence re-derivation)

1. Extract Track B evidence subtree at closeout commit into `crew/work/evidence/` (fresh from git;
   byte-compare predecessor's copies).
2. Extract arm-3 rebuild commits' verdict records (7d056be varA, d7929bb varB, f0031d9 varC —
   on origin/tnn-native-lab, not ancestors of closeout).
3. Independent Zag verifier (`crew/work/verify_trackb.zag`): parse the committed verdict sheet,
   mechanically re-derive each arm disposition from the arm evidence docs, confirm W9 BLOCKED
   names no winner, confirm arm-3 FAIL→rebuild-PASS×3 record, recompute sha256 digests of key
   evidence files vs recorded digests. ≥3 byte-identical runs.
4. Write VERDICT.md with the frozen claims checklist quoted and each claim vs measured.

## Evidence extraction

- Extracted 12 key evidence docs fresh from git at closeout `47c48d3e7cf9f` into
  `crew/work/evidence/` via `git cat-file -p` (per-file; full-subtree `git archive`
  aborted/timed out on the large wire binaries — extraction method recorded).
- Predecessor's `crew/evidence/TRACKB_VERDICT.md` and `crew/evidence/HARNESS_CLOSEOUT.md`:
  `cmp` vs fresh git extractions → **byte-identical**. (Not trusted; re-extracted anyway.)
- Arm-3 rebuild verdicts extracted from their commits (on `origin/tnn-native-lab`,
  not ancestors of closeout): `7d056be` varA, `d7929bb` varB, `f0031d9` varC →
  `crew/work/evidence/arm3rebuild/`. All three record `Verdict: PASS`.
- WIRING_SPEC.md extracted; system `sha256sum` = `d333bc45…f32`, exactly the pinned
  hash in committed WIRING_HASHES.txt (independent Zag re-derivation below recomputes it).
- Commit-content spot checks: `89745ce1117c` holds `arm1/teacher.zag`; `d921459a` holds
  `learner/FORCE_PIN_VERDICT.md`; `4a6d898c1e66` holds `pcodec.zag` +
  `learner/verify/w5_pcodec_frozen.zag` + `LEARNER_HARNESS_VERDICT.md`.

## Mechanism re-derivation — pcodec frozen-§B.3 fix (Part B)

- Rebuilt `w5_pcodec_frozen.zag` from W5 commit `4a6d898c1e66` sources with the pinned
  znc (`znc_linux_x86_64_abed8aa1`, `--no-zagd --no-analyze --no-foreground-cache`).
  Layout note: znc resolves a nested `@import` relative to the importing file's
  import-path dir (observed: `pcodec.zag`'s `@import("R33_NATIVE_IO_V1.zag")` needed the
  file at `pcodec_rebuild/R33_NATIVE_IO_V1.zag` when the top import was `../pcodec.zag`).
- 3 runs, all rc=0: `p_decode rc=0 / teacher=1 / session=1001 / seq=0 / kind=1 /
  span=36097..36100 / ground_count=2 / FROZEN_DECODE_PASS`.
- Outputs byte-identical 3/3: sha256 `395111cc0ad8b970db5c076859a80bdfb48a3e47d43007c7d86ca0650555b882`.
- Re-derives the prereg's pcodec parenthetical (FROZEN_DECODE_PASS; pre-fix rc=3
  P_V_BAD_TEACHER per the committed verifier's own comment).

## Document re-derivation — independent Zag verifier (Part A)

- Wrote `crew/work/verify_trackb/verify_trackb.zag` (pure Zag, zero RNG): reads the 12
  committed evidence docs + 3 rebuild verdicts, runs 25 mechanical substring/digest
  checks (C01–C25) mapping 1:1 to the frozen prereg's claim list, recomputes the
  wiring-spec sha256 with `ns_sha256` and compares against the pinned hash.
- Built with pinned znc; ran 3× → all rc=0, outputs byte-identical 3/3:
  sha256 `67c9d1207f6a8c2fd79bea2a35557f004e2edf7eff8495c30a08b2e711e01503`.
- Result: **25/25 checks PASS, fails=0, TRACKB_REDERIVED_ALL_PASS.**

## PIN CORRECTION (coordinator, 2026-09-22 ~23:16 PDT)

The coordinator confirmed: the dispatch pin `8d0d6b9e9c9c` was a transcription artifact
(returns 422 "No commit found" in sylorlabs/TNN) — **disregard it**. The frozen prereg
governs; do not stop over the bad pin. This matches this crew's own prior determination
(recorded above before the correction arrived): the pin matched nothing authoritative and
the run proceeded on the prereg's pins.

Per the correction, each T2-TRACKB pin from the frozen prereg was additionally verified
to resolve via the GitHub API (`GET /repos/sylorlabs/TNN/commits/<sha>`), 2026-09-22:

| Pin | GitHub API result |
|---|---|
| `7b2100d09911c5c10252c5756c7def288e70bd1f` | resolves — "crossref: scope + frozen preregs for the cross-reference / clean-envir…" |
| `47c48d3e7cf9f` | resolves — "Track B closeout: finalize verdict sheet (flaw-score FAIL honest, harn…" |
| `89745ce1117c` | resolves — "Track B arm-1: parent-wired teacher in pure Zag, verified byte-identic…" |
| `d921459a` | resolves — "Track B C3: B.6 force-pin implementation (PASS)" |
| `4a6d898c1e66` | resolves — "Track B W5 (learner+harness): pcodec repaired to frozen §B.3 + verdict…" |
| `6adb2fa5930c` | resolves — "Track B W5: verdict-sheet SHA fill + frozen-hash typo fix" |

Verdict stands: **PARTIAL** (all claims re-derived; arm-3 rebuild three-way ambiguity named
per the frozen rule). VERDICT.md + RUNLOG.md delivered in
`~/workspace/scratch-crossref/T2/TRACKB/crew/`.

## Verdict reasoning (frozen rule applied)

Frozen rule: "REPRODUCED if all arm verdicts re-derive; PARTIAL if the arm-3 rebuild's
three PASS variants create ambiguity about which is 'the' arm (name it)."
- All arm verdicts re-derive (arm-1 DONE/PASS, arm-3 FAIL, arm-4 PASS, arm-5 PASS;
  C3 force-pin PASS; W9 BLOCKED honestly with no winner named; W5 B.4 FAIL(blocked)/
  B.5 PARTIAL; W8 BLOCKED + accounting verified; pcodec fix + 5/5 + 15/15).
- BUT the rule's named PARTIAL condition is satisfied: three substantively different
  rebuilds all PASS — varA pure-Zag deliberative adaptive teacher (`7d056be`), varB
  phase-scheduler teacher (`d7929bb`), varC engagement-meter teacher (`f0031d9`) —
  and the closeout explicitly parks "which becomes the arm" as governance call #1
  for Micah ("needs his decision — nothing here is approved").
- The more specific clause governs: verdict = **PARTIAL** (nothing failed; the
  ambiguity is the committed state, accurately recorded — and it is exactly what the
  frozen rule says to name).
