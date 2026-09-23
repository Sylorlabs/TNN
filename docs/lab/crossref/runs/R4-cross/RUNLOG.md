# R4-CROSS RUNLOG — TP1 + SOURCE_AUTHORITY_LICENSE cross-check (Type C)

Crew: R4-CROSS (independent cross-check). Parent: crossref coordinator.
Frozen prereg: `docs/lab/crossref/PREREG_TIER1.md` §R4 + `SCOPE.md`, commit
`7b2100d09911c5c10252c5756c7def288e70bd1f` (branch `tnn-native-lab`, repo `sylorlabs/TNN`).

## 0. Clean-environment setup

- Fresh clone: `~/workspace/scratch-crossref/R4/clean-cross/` (branch `tnn-native-lab`,
  `--depth 50 --single-branch`; 59,534 files; clone exit 0).
- Checked out frozen commit: `7b2100d09911c5c10252c5756c7def288e70bd1f`
  ("crossref: scope + frozen preregs for the cross-reference / clean-environment replication program").
- Run dir: `~/workspace/scratch-crossref/R4/cross/` (this dir). Scratch only, never /tmp.
- TMPDIR=`~/workspace/tmp_commit`. znc: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- NON-INTERFERENCE: `~/workspace/scratch-crossref/R4/primary/` never read; the in-flight
  Zag-native TP1 oracle workstream's files untouched. Only committed evidence used.

## 1. Pin freeze (BEFORE any verification run)

All pins verified present in the fresh clone with matching commit subjects:

| Pin | Role | Commit subject | Status |
|---|---|---|---|
| `c85c9b41770c1878fb00a8dc991a5b4f17f8caaa` | TP1 result/evidence | third-path TP1 verdict: T1 licensed, T3 null, T2 conditional (evidence) | FROZEN |
| `44afdbefc168edddcae50e9dd91eac12cd9fa156` | TP1 prereg | PREREG-TP1: S1 third-path head-to-head (frozen 2026-09-22) | FROZEN |
| `b22ff31272d1789da4d35bf489d30d5e0d7c41f6` | round-3 sweep | round3: VERDICT-MW-R3 — source-authority reliability sweep COMPLETE | FROZEN |
| `3a3541ef62d05e929bdb47e4228e6e2b3a89fe02` | license law | SOURCE_AUTHORITY_LICENSE: final law (Micah-ordered 2026-09-22) | FROZEN |

Frozen at: 2026-09-22 ~17:00 PDT. All four `git cat-file -t` = commit; all under
`docs/lab/mixed-web/authority/` at those commits. No pin missing → no UNREPLICABLE-AS-IS.

Evidence inventory (from pinned trees):
- `third-path/evidence/`: `run0.log` (2,645 lines: 2,640 P + 3 H + S + C), `tp_data.json`
  (220 envelopes), `idmaps.json`, `SHA256SUMS` (5 × `d57fda22…`).
- `round3/evidence/`: `mw_r3{b,c,d}_r{0..4}.log` (15 logs, 421 lines each) + `.err` + `SHA256SUMS`.
- `round3/manifest_r3.txt`: 1,260 lines (420 qids × 3 arm-expectation lines).
- `round3/`: `PREREG-MW-R3.md`, `AMENDMENT-A2.md`, `AMENDMENT-A3.md`, `VERDICT-MW-R3.md`.
- `third-path/`: `PREREG-TP1.md`, `VERDICT-TP1.md`, `REPRODUCE.md`.
- `SOURCE_AUTHORITY_LICENSE.md` (Micah-signed, 2026-09-22).

## 2. Method (Type C — independent re-derivation)

1. Python glue (`prep_extract.py`) parses ONLY committed evidence into flat TSVs
   (no decision logic in Python beyond field extraction).
2. Independent Zag program (`r4_verify.zag`) re-implements the frozen decision
   procedures from the prereg text (shape classifier §3, T1/T2/T3 gates), recomputes
   EVERY decision from the corpus, and compares against the committed logs;
   recomputes every headline number (EVs, tie stats, tables, thresholds) from the
   raw decisions; checks digests, ledger heads, twin formulas, latent-truth rules.
3. Built with the pinned znc; run 3×; stdout sha256 must be byte-identical.
4. License audit (JOB 2) is a line-by-line document trace against the measured results.

## 3. Extraction

- 2026-09-23 ~00:10 PDT: `prep_extract.py` ran clean.
  - `tp_corpus.tsv`: 220 envelopes (180 U + 20 S + 20 G2; 4 rows each; structural
    assertions held: G2 levels unknown, S8 latent present).
  - `tp_log.tsv`: 2,640 decisions.
  - `r3.tsv`: 6,300 decision lines (3 arms × 5 runs × 420).
  - `tp_tail.txt`: 5 lines (H|T1/T2/T3, S|, C|).
  - Two glue bugs found and fixed (string/int year compare; space-containing
    manifest fields) — both in extraction plumbing, not in verification logic.

## 4. Independent Zag verifier

- Wrote `r4_verify.zag` fresh (~700 lines, pure Zag; imports only
  `sub/R33_NATIVE_IO_V1.zag` for file IO + the repo-proven `t_put32`/
  `t_get32` little-endian arena pattern from `tprobe.zag`).
- Re-implements from the frozen prereg text: PREREG-TP1 §3 shape
  classifier (S1_UNCORR / S8_TIE-before-CORROB ordering as written),
  T1/T2/T3 decision rules, twin formula `(i·n_A)%20<n_A ⟺ S1A`,
  S8 latent rule (i even ⟺ latent=prim), round-3 arm semantics,
  r̂_max / r̂_all estimators, gate-value analysis, k/(k+1) rounding,
  T2 frontier cells.
- Build: pinned znc, exit 0 (only A0102 ignored-return warnings).
- Two verifier-expectation bugs found via failing checks and fixed
  (both were wrong expectations in MY code, data was right):
  1. `r3_D_U_2rminus1` at r=.99: measured per-case +1.00 (20/20) vs
     theoretical 0.98 — one 20-case granularity step; the committed
     table itself prints +1.00. Check replaced with exact table-value
     match + within-one-case bound.
  2. `r3_gate_lenient_adm500`: r̂_all=0.5 ≥ t=0.5 admits all 20 — my
     expectation wrongly said 0. Fixed to 20.
- Final: **142/142 checks pass, SUMMARY,fails,0.**
- Determinism: 3 runs, stdout sha256 identical:
  `7789bdbb51ab5ad96ebfd13379569e06aa9673312b54cd0eb2c8e6fe4e595033`
  (run1.txt / run2.txt / run3.txt).

## 5. Digest verification (shell, 2026-09-23)

- TP1 `run0.log`: `d57fda225db8d54201ca443e6e39716aba4e5ca5a97683128a49ed61b432d1d9`
  — matches committed SHA256SUMS. **run1–run4.log are absent from the
  evidence tree**; SHA256SUMS attests they share run0's digest but there
  is no file to re-hash. Noted as ⚠ in VERDICT.md #24.
- Round-3: all 15 logs re-hashed; every digest matches the committed
  per-arm rerun digest (`14d81ec5…` B, `3b43d255…` C, `58ae289b…` D);
  all 15 `.err` files are empty-sha256 (`e3b0c44…`).
- Ledger heads + S|/C| tail lines: byte-identical to VERDICT-TP1
  (checked inside the Zag verifier: `tail_match`).

## 6. License audit (JOB 2)

- Read `SOURCE_AUTHORITY_LICENSE.md` (641 lines) in full from pin
  `3a3541ef`; frozen copy at `cross/license_frozen.md`.
- Every operative term traced to: measured (M), derived (D),
  governance (G), or unmeasured/provisional (U). Full trace table in
  VERDICT.md §3.
- Ten term-groups lack direct measured basis (named in VERDICT.md §3):
  k-table design, CI lower-bound gate, broad tie class, §3.1
  operational criteria incl. provisional 24-month recency, T2 channel
  qualification, frontier-as-applied, deferral lifecycle, §6.5–§6.9
  boundaries, §7 governance, Annex A debate record. The license itself
  admits most of these (Annex A.4).

## 7. Verdict

**PARTIAL** — all 47 numbered items / 142 atomic checks reproduce with
zero mismatches, but the license law is broader than its measured base
(see §6 list). Applied the frozen rule mechanically; no judgment calls.

Deliverables written (no commits made):
- `~/workspace/scratch-crossref/R4/cross/VERDICT.md`
- `~/workspace/scratch-crossref/R4/cross/RUNLOG.md` (this file)

Non-interference: `~/workspace/scratch-crossref/R4/primary/` never
accessed; no live workstream files touched; nothing committed.
