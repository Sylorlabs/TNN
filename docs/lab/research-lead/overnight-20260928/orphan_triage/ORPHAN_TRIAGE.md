# ORPHAN TRIAGE: Category C (24 orphaned lane branches)

Date: 2026-10-03 ~04:30 PDT. Worker: ORPHAN-TRIAGE. Analysis only; no deletions, no merges performed.
Source: FINAL_SWEEP.md Category C list, verified against `tnn-native-lab` in `~/workspace/tnn-rsi`.

## Method

For each branch: (1) listed commits unique vs `tnn-native-lab` (`git log tnn-native-lab..BRANCH`); (2) listed files unique vs merge-base; (3) blob-level content check of every unique file against the full `tnn-native-lab` tree (1053 unique blobs) to distinguish "content captured elsewhere" from "content only on this branch"; (4) ancestor analysis between the 24 branches; (5) cross-referenced experiment verdicts against the canonical `CLAIM_LEDGER.md` on `tnn-native-lab` (224 claims, C64 through C376) and against the retained wave-archive branches.

## Headline findings

1. **11 of the 24 branches are a single linear consolidation lineage.** Workers kept committing whole-wave results onto one branch line, renaming the ref as lanes changed. Nine refs are strict ancestors of the line head and hold ZERO unique commits: `lane-xhier3-20261002`, `lane-gensubsumesu-20261003`, `lane-genstress-20261003`, `lane-genstatefix-20261003`, `lane-genredim-20261003`, `lane-l3rx-20261003`, `lane-gennm10-20261003`, `lane-hcontlife5-20261002`, `lane-ma4redteam-20261003` are all ancestors of `lane-ledgerreconcile-20261003` (verified via `git merge-base --is-ancestor`). Only the two heads matter: `lane-ledgerreconcile-20261003` (tip 10:19 UTC) and the diverged side branch `lane-ma4rt-fix-20261003` (tip 10:27 UTC, forked at `lane-gennm10`).

2. **The main line holds ~50 experiment results from the 2026-10-03 wave, most with frozen preregs and 3/3 byte-identical runs.** None of the post-C376 verdicts are in the canonical ledger on `tnn-native-lab` (HEAD ledger ends at C376; entries C377-C415 were deleted by faulty worker commits during the night, see the LEDGER-RESTORE saga). `lane-ledgerreconcile-20261003` is the recovery vehicle: its `CLAIM_LEDGER.md` runs to C400 (248 claims), it stages ledger entries C401-C460 for approval, and it carries the LEDGER-RECONCILE C457 proposal.

3. **The 8 wave-20261002-1421pdt lane branches were all adjudicated** by the retained wave-archive's closure debate (`tnn-native-lab-wave-archive-20261002-1421pdt`, Category D): contlearn-integrate NARROWED to NON-INTERFERENCE (bounded), contlearn-rebind ADOPT-BOUNDED, trades-finer NARROWED to chain-true-tie scope, hpirev2-clean NARROWED to residue claim, l2adapt-BC NARROWED to PASS (scaffolded), devang-kseal measurement ADOPTED / retirement DEFERRED, arena-c8 REJECTED (uncommitted impl). Verdicts are captured in the archive; lane-level evidence (binaries, run logs) lives only on the orphan branches.

4. **Two branches hold significant verdicts captured NOWHERE else**: `lane-f1-20261002-0821pdt` (F1 sealed seed-sensitivity re-freeze, ALL-PASS, FINDING CONFIRMED) and `lane-xdagfan-20261002` (XP-DAGFAN-1-PASS, fan-out DAG composition; directly relevant to overnight priority 1). Both need verdict documentation before deletion.

5. **Foreign stray commits found on two branches** (documented, not acted on): `lane-arena-c8-20261002-1421pdt` carries a ddes RT4 prereg (57794a82d); `lane-contlearn-int-20261002-1421pdt` carries an L3-SEALED-1 prereg (fae03954c). Both are redundant: the canonical RT4 prereg and its H1-SURVIVES verdict live on the active ddes branches; the canonical L3-SEALED-1 freeze lives on active `lane-l3-20261002-1421pdt`.

6. **Duplicate ref confirmed**: `lane-l3niv2fg-20261002` and `lane-l3niv2w5-20261002` point at the identical commit 5f08dc9d3. One ref is pure redundancy.

## Per-branch analysis

### KEEP (2)

**lane-ledgerreconcile-20261003** (02f3bf13d, 2026-10-03 10:19 UTC) -- KEEP
Main consolidation line head. Unique content (1175 at-risk files by blob check): (a) reconciled `CLAIM_LEDGER.md` with 248 claims through C400, the only recovery source for ledger entries C377-C400 deleted from main's ledger; (b) `ledger_write/STAGED_LEDGER_ENTRIES.md` staging C401-C460 for parent approval (with a documented C455-C460 numbering collision warning); (c) LEDGER-RECONCILE C457 proposal (6 collisions mapped to C455-C460, 43 watchdog-only claims listed, C417 flagged probable duplicate of C410); (d) ~15 new experiment results 10:06-10:19 UTC not on any other branch: COGOPS-PERIOD impl+report (C452 BUILD-PASS), tmplinv impl+REPORT (REQUIREMENT-TEMPLATE DERIVATION DEMONSTRATED K1-K9), MP-10 analysis+FINDING-S, L3-RX-K10 prereg + Amendment A1, INTEGRATION-STRESS prereg, MA4 red-team BUILD (REPORT identical on ma4rt-fix), C11-REFIX prereg amendment; (e) the full 03:37-10:06 UTC wave result set inherited from the ancestor line (L3-RX, INTEGRATION-B1B2, MP-7/8/9, COGOPS-OSCILLATORY/CYCLES/3WAY/COMPOSE, NT series, invention series RS/PP/DF/SRCPOOL/PRIMINV/OPINVENT/WEAKSEED, DEEP7-RERUN, GEN-NM10, FHAT-GROWTH/REVISION/COMPOSITION, CONTRACT-UNIFICATION, U-RETIREMENT, COGCOMP-1, MP-3/4/5, GEN-STRESS, COMPAUDIT-1, COL-1, MP-2, META-RECOVERY). Verdicts C377+ are NOT in main's ledger. Deletion would destroy the ledger recovery path. Recommendation: KEEP until the ledger is restored and the wave results are merged or formally superseded.

**lane-ma4rt-fix-20261003** (b2c5c6817, 2026-10-03 10:27 UTC) -- KEEP
Side branch diverged from the main line at `lane-gennm10` (10:06 UTC). Unique vs `lane-ledgerreconcile` (9 commits): INTEGRATION-STRESS implementation + artifacts + REPORT (STRESS SURVIVED K1-K10 PASS; note the prereg lives on ledgerreconcile, implementation here, the two must be reunited), COMP-2 implementation (Opportunity 7: parameterized diag7 driver, 2950 lines removed, byte-identical outputs), SELFTRIG prereg (self-triggered revision), FORMCLASS prereg (form-class invention), L3-RX-K10 PREREG AMENDMENT A2. The MA4 red-team BUILD commit is byte-identical on both branches (duplicated, not unique). Recommendation: KEEP; merge together with ledgerreconcile so INTEGRATION-STRESS prereg and implementation reunite.

### DOCUMENT-THEN-DELETE, verdict already captured elsewhere (8)

**lane-contlearn-int-20261002-1421pdt** (ee44ac546) -- DOCUMENT-THEN-DELETE
CONTLEARN-INT: full experiment (frozen prereg + amendment, implementation, 18 transcripts, REDTEAM_INT.md, REPORT.md, VERDICT_INT.md = PASS / INTEGRATION-COMPOSES, 352/352 checks). REPORT.md is byte-identical in retained `tnn-native-lab-wave-archive-20261002-1421pdt`; verdict adjudicated in the archive's closure debate (NARROWED to NON-INTERFERENCE, bounded). 39/57 files unique by blob (implementation sources, run logs). Also carries foreign stray L3-SEALED-1 prereg (2 files); canonical freeze lives on active `lane-l3-20261002-1421pdt`. Nothing would be lost verdict-wise by deletion; the 39 evidence files are unmerged.

**lane-l2adapt-20261002-1421pdt-2** (c920cff65) -- DOCUMENT-THEN-DELETE
l2adapt B/C battery (amendment 2): B PASS 7/7 bounded, C PASS 6/6 bounded, 3/3 byte-identical, REPORT_BC.md with root-cause (rebind_try hijack diagnosis) and red team. REPORT_BC.md byte-identical in retained 1421pdt archive; closure debate NARROWED to PASS (scaffolded). 25 files, all unique by blob.

**lane-devang-20261002-1421pdt-2** (c5ee8f3b3) -- DOCUMENT-THEN-DELETE
DEVANG-KSEAL-CAL sealed evaluation: 6 frozen seeds, 54 runs 3/3 byte-identical, K_DET PASS, K_CAL DRAW-DOMINATED, bar-retirement recommendation. Closure debate ADOPTED the measurement and explicitly DECLINED the retirement recommendation. 77 files unique by blob (sealed packages, run logs, binaries, sources). Verdict captured in archive; evidence unmerged.

**lane-hpirev2-20261002-1421pdt** (0ef5cdd8e) -- DOCUMENT-THEN-DELETE
HPIREV2 clean reproduction: 40 sealed worlds + fresh pure-Zag validator + executor + 24-run matrix, BUILD-PASS verdict. Closure debate NARROWED to the residue claim with qualifications. 87 files, all unique by blob. Verdict captured in archive; evidence unmerged.

**lane-trades-finer-20261002-1421pdt** (ea0f89092) -- DOCUMENT-THEN-DELETE
TRADES-FINER: Occam tie-break + abstention arm, 12/12 on frozen 1121pdt worlds, 6/6 ties, red team R1-R4, BUILD-PASS verdict. Closure debate NARROWED to chain-true-tie scope. 80 files, all unique by blob (sealed worlds, implementation, runs). Verdict captured in archive; evidence unmerged.

**lane-arena-c8-20261002-1421pdt** (9ec262c7a) -- DOCUMENT-THEN-DELETE
ARENA-C8: NAMECHECK + frozen PREREG_QIA only; no implementation was ever committed. Closure debate REJECTED the lane (uncommitted impl). PREREG_QIA.md byte-identical in retained `tnn-native-lab-wave-archive-20261002-1121pdt`. Carries foreign stray ddes RT4 prereg (57794a82d); the canonical RT4 prereg and its H1-SURVIVES verdict live on the active ddes branches. Nothing of scientific value beyond the archived prereg.

**lane-l3niv2fg-20261002** (5f08dc9d3) -- DOCUMENT-THEN-DELETE
L3-NIV2 wave 5: 3S-CALR stage-3 implementation + 3/3 runs + report, verdict BUILD-FAIL (budget, as predicted). Verdict fully captured in main ledger C368 (which cites these exact commits: prereg 298f084e9, impl 5f08dc9d3). 29 files unique by blob (wave-5 implementation detail). Delete one of the two duplicate refs now; the remaining ref can go once the merge/keep decision on the wave-5 implementation detail is made.

**lane-h5r2-skeptic2** (709e1e82e) -- DOCUMENT-THEN-DELETE
Old wave-20260924 debate/fork-battery evidence re-committed 2026-10-02, plus H5R2-SKEPTIC2 frozen prereg (never executed, no results) and Meta-applicability APPL gate (FAIL K7, mechanism demonstrated). 323/327 at-risk files are byte-identical in the retained 1421pdt wave-archive. Only 4 files are unique to this branch: root `LOOP_STATE.md`, `redteam_wave3/adv_idx_stale_run1.txt`, `wave-20260924-1721pdt/VERDICT_CV1_CITE_1721.md`, `wave-20261001-2321pdt/WAVE_RECORD.md`, plus the unexecuted H5R2-SKEPTIC2 prereg pair. Low scientific value; record the 4 files + prereg, then delete.

### DOCUMENT-THEN-DELETE, verdict NOT captured anywhere (document first) (2)

**lane-f1-20261002-0821pdt** (655c8d7d6) -- DOCUMENT-THEN-DELETE (verdict must be recorded first)
F1 sealed seed-sensitivity re-freeze: the clean pure-Zag re-run of the 0521pdt battery that went PROCESS-FAIL on a no-op python3 invocation. Sealed fixture manifest committed before any run; methodology committed before fixtures; K-DET PASS, NC-HARNESS PASS, all bars ALL-PASS (R=13, T=2, D_ops=9, Cmax_ops=15); FINDING CONFIRMED: overfit 13/40, pooled unquarantined rate 22/104. 1337 files, all in `wave-20261002-0821pdt/F1/`, unique by blob; not in the ledger, not in any archive. This is a completed sealed experiment whose verdict exists only here. Recommendation: mint or record the verdict (ledger entry or equivalent) before deletion; the 1337 files are evidence, not required for the verdict to stand.

**lane-xdagfan-20261002** (d00850b4a) -- DOCUMENT-THEN-DELETE (verdict must be recorded first)
XP-DAGFAN-1: fan-out/fan-in composition beyond pipelines. Verdict XP-DAGFAN-1-PASS (K1-K10): frozen xhier_compose handles fan-out DAG (one MAP_Z feeding two composites) with zero source changes; fan-in is an honest predicted arity bound; no diamond handler built, per the 2026-10-03 architectural clarification. 10 files, all unique by blob; not in the ledger, not in any archive. Directly relevant to overnight priority 1 (general DAG/fan-out/fan-in composition). Recommendation: record the verdict before deletion.

### DELETE, nothing of value (2)

**lane-arena-zeros-20261002-1421pdt** (047786685) -- DELETE
Single file: `arena-zeros/NAMECHECK.md`. No prereg, no implementation, no results.

**lane-trades-20261002-1421pdt-2** (483211cbd) -- DELETE
Single file: a mislabeled ARENA-C8 NAMECHECK.md (branch name says trades, content is arena-c8). The actual TRADES work is on `lane-trades-finer-20261002-1421pdt`.

### Redundant ancestor refs, safe to delete once the two heads are preserved (9)

All verified strict ancestors of `lane-ledgerreconcile-20261003` via `git merge-base --is-ancestor`; each holds zero commits not reachable from the head. Content-safe to delete conditional on keeping `lane-ledgerreconcile-20261003` (and `lane-ma4rt-fix-20261003` for its divergent commits):

- `lane-xhier3-20261002` (17f11bf9b)
- `lane-gensubsumesu-20261003` (96393c2a5)
- `lane-genstress-20261003` (79396e5a4)
- `lane-genstatefix-20261003` (983a46331)
- `lane-genredim-20261003` (b739f81ee)
- `lane-l3rx-20261003` (d00850b4a)
- `lane-gennm10-20261003` (190731d61)
- `lane-hcontlife5-20261002` (be8b5fa6d)
- `lane-ma4redteam-20261003` (012be9fb9)

### Duplicate ref (1)

- `lane-l3niv2w5-20261002` -- identical commit to `lane-l3niv2fg-20261002` (5f08dc9d3). Delete the ref; zero unique content by construction.

## Recommendation summary

| Recommendation | Branches | Count |
|---|---|---|
| KEEP | lane-ledgerreconcile-20261003, lane-ma4rt-fix-20261003 | 2 |
| DOCUMENT-THEN-DELETE (verdict captured) | lane-contlearn-int-20261002-1421pdt, lane-l2adapt-20261002-1421pdt-2, lane-devang-20261002-1421pdt-2, lane-hpirev2-20261002-1421pdt, lane-trades-finer-20261002-1421pdt, lane-arena-c8-20261002-1421pdt, lane-l3niv2fg-20261002, lane-h5r2-skeptic2 | 8 |
| DOCUMENT-THEN-DELETE (verdict NOT captured, record first) | lane-f1-20261002-0821pdt, lane-xdagfan-20261002 | 2 |
| DELETE (nothing of value) | lane-arena-zeros-20261002-1421pdt, lane-trades-20261002-1421pdt-2 | 2 |
| DELETE redundant ancestor ref (keep heads) | lane-xhier3-20261002, lane-gensubsumesu-20261003, lane-genstress-20261003, lane-genstatefix-20261003, lane-genredim-20261003, lane-l3rx-20261003, lane-gennm10-20261003, lane-hcontlife5-20261002, lane-ma4redteam-20261003 | 9 |
| DELETE duplicate ref | lane-l3niv2w5-20261002 | 1 |

## Notes and caveats

- "Captured" above means blob-identical content exists on `tnn-native-lab` or a retained archive branch, or the verdict is recorded in the canonical ledger / retained closure debate. "Unique by blob" means the exact file content exists nowhere else; it does not mean the result is scientifically irreplaceable (most are reproducible from frozen preregs + pinned toolchain).
- The ledger on `tnn-native-lab` HEAD ends at C376. Verdicts minted as C377-C415 during the night were deleted by faulty worker commits; `lane-ledgerreconcile-20261003` is the recovery source (ledger to C400 + staged C401-C460). Any merge plan must resolve the staged C455-C460 numbering collision documented in `STAGED_LEDGER_ENTRIES.md` before approval.
- INTEGRATION-STRESS is split across the two heads: prereg on `lane-ledgerreconcile-20261003`, implementation + REPORT on `lane-ma4rt-fix-20261003`. Merge both or neither.
- The wave-20261002-1421pdt lane evidence (binaries, run logs) on the DOCUMENT-THEN-DELETE branches is unmerged; the closure debate in the retained archive is the verdict record. If lane-level reproducibility is ever needed, the evidence must be merged, not just the verdicts.
- No deletions or merges were performed. All 24 branches verified present at the tips listed in FINAL_SWEEP.md.
