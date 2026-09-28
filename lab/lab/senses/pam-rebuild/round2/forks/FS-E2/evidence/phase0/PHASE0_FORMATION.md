# FS-E2 Phase 0 — Independent formation-accuracy reproduction

**Date:** 2026-09-24. **Crew:** FS-E2 build+eval. **Status:** COMPLETE.

## Method

Independent reimplementation of the six R2A formation functions from the
frozen task definitions (PREREG_FS-E1 "Formation" section — the definitions
FS-E1 froze verbatim from R2-16). The implementation
(`src/fs2_form.zag`, pure Zag, integer math only, zero RNG) was written
fresh for this phase: own function names, own structure, own IO wrappers;
no code shared with FS-E1/R2-16 formation paths. Algorithms are the frozen
definitions (same spec, independent implementation).

Formation definitions reproduced (from the frozen spec):
- t0 colordisc: mean-RGB distance of two 32x32 patches, DIFFERENT iff >= 18
- t1 colorconst: warm mean-chromaticity L1 x1000, DIFFERENT iff >= 80
- t2 shapetrans: 96x96 bbox fill-ratio -> class (CIRCLE>=700, SQUARE 550-699, TRIANGLE<550; default SQUARE)
- t3 pitchdisc: zero-crossing counts -> endpoint ratio in 0.01%; HIGHER if r>50, LOWER if r<-50
- t4 timbredisc: Goertzel m=1..8 (exact 440*m Hz coeffs) spectral centroid -> PURE<520<DARK<950<RICH<1550<BRIGHT
- t5 motiondir: 23 block-match votes (16x16 block, search +/-4, negate to window direction), plurality

Fixtures: the frozen R2A battery (`forks/R2-7/fixtures_R2A/r2n/`, R2FX
containers). Truth from `<fixture>.truth` sidecars. Judgment names match the
truth vocabulary exactly (SAME/DIFFERENT, SAME_SURFACE, CIRCLE/SQUARE/TRIANGLE,
HIGHER/LOWER, PURE/BRIGHT/DARK/RICH, N/NE/E/SE/S/SW/W/NW/STILL).

Provenance:
- Source SHA-256: `f20a3f816f748cb7fb48d26abd4e132aa2547623ae9c6db2e3c9cdf875ea3e58`
- Binary SHA-256: `49e353716788fd3f1f5f58a4b79351f992d6c93ebcfa546e1710e0a4b8546634`
  (built with the pinned toolchain `znc_linux_x86_64_abed8aa1`; binary NOT committed)
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Results (A) — direct reproduction on FS-E1's control battery (b_ctrl, n=2000)

| Task | n | correct | FS-E2 indep. | FS-E1 (ledger) | Agreement |
|---|---|---|---|---|---|
| colordisc | 1080 | 1004 | 92.96% | (overall only) | per-fixture 1080/1080 |
| colorconst | 720 | 409 | 56.81% | (overall only) | per-fixture 720/720 |
| motiondir | 200 | 193 | 96.50% | (overall only) | per-fixture 200/200 |
| **OVERALL** | **2000** | **1606** | **80.30%** | **80.30%** | **2000/2000 fixtures** |

- FS-E1's Bar-4 number (overall formation accuracy 80.30%) is reproduced
  EXACTLY: 1606/2000 = 80.30%.
- Per-fixture cross-check against FS-E1's frozen ledger
  (`forks/FS-E1/evidence/batt_b_ctrl_union_r1.ledger`): **2000/2000 judgments
  agree, 0 disagree** (`src/crosscheck_phase0.py`). The independent
  implementation is judgment-identical to FS-E1's formation on every control
  fixture.
- Determinism: two full runs byte-identical
  (SHA `5e35be21d8b5094ab286f75da632a999da219f2347157adff8a1cda544588fab` x2).

## Results (B) — per-task formation on the full R2A normal sets (scoping input)

| Task | n (normals) | correct | accuracy | >=85%? |
|---|---|---|---|---|
| colordisc | 1080 | 1004 | 92.96% | YES |
| colorconst | 720 | 409 | 56.81% | no |
| shapetrans | 1296 | 1044 | 80.56% | no |
| pitchdisc | 720 | 705 | 97.92% | YES |
| timbredisc | 720 | 280 | 38.89% | no |
| motiondir | 564 | 545 | 96.63% | YES |

Consistency notes:
- colordisc/colorconst b_ctrl sets ARE the full normal sets (identical numbers).
- motiondir b_ctrl (200/564 subset): 96.50% vs full-set 96.63% — consistent.
- colorconst 56.81% is consistent with R2-14's reported colorconst formation
  error (42.5% wrong -> 57.5% right) on a different formation revision.
- timbredisc 38.89% confirms the Goertzel-centroid formation as the weakest
  front end (R2-14 timbredisc f1 36.20% formation-adjacent figure).

## Scoping derivation (for the Phase-1 prereg)

Scoping rule (Debate E FS-E2 spec): in-scope = tasks with reproduced
formation accuracy >= 85%.

- IN SCOPE: colordisc (92.96%), pitchdisc (97.92%), motiondir (96.63%)
- ABSTAIN: colorconst (56.81%), shapetrans (80.56%), timbredisc (38.89%)

Three tasks clear the bar, so the fork is FEASIBLE-AS-SCOPED (not
INFEASIBLE-AS-SCOPED). The scoping list is frozen in PREREG_FS-E2.md; the
numbers above are the audit trail (recomputable from the committed TSVs).

## Evidence files (committed)

- `evidence/phase0/form_bctrl_r1.tsv` / `form_bctrl_r2.tsv` (2000 rows each, byte-identical)
- `evidence/phase0/form_r2n_<task>.tsv` (6 files, full normal sets)
- `evidence/phase0/lists/r2n_<task>.list` (fixture lists)
- `src/fs2_form.zag` (independent implementation), `src/run_phase0.py`, `src/crosscheck_phase0.py`
- `src/R33_NATIVE_IO_V1.zag` (IO substrate copy; FS-E1's formation code NOT present anywhere in FS-E2)

## Conclusion

Phase 0 COMPLETE. FS-E1's Bar-4 formation measurement is independently
reproduced: overall 80.30% exact, 2000/2000 per-fixture agreement. The
formation precondition binds on colorconst, shapetrans, and timbredisc;
colordisc, pitchdisc, and motiondir clear the 85% scoping bar.
