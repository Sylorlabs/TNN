# R2-CROSS VERDICT — deliberation ceiling (CEILING-CONFIRMED) cross-check

**Top-line verdict: REPRODUCED.**

An independent clean-environment rebuild re-derived the full deliberation
ceiling table cell-for-cell (Type C, pure-Zag verifier, 3 byte-identical runs)
and re-ran the full contradiction battery from verified source (Type A, fresh
build, 15 runs, all byte-identical to the committed logs). Every committed
number matches. No scientific divergences.

## Frozen pins (verified in fresh clone before any runs, 2026-09-22)

| Pin | SHA | Role |
|---|---|---|
| program / frozen crossref prereg | `7b2100d09911c5c10252c5756c7def288e70bd1f` | tnn-native-lab commit |
| QB prereg | `39d4ccb6b4ea550dd7e12ac8af863aae59bcc08b` | quality-buying prereg |
| QB synthesis | `3314fc1fdd6fb45ec4d73169817cc9820ce520a1` | quality-per-cost curve |
| mechanism implementation + verdict | `b447c367677ff351f240675293eee445bdb97993` | new-mechanisms code+verdict |
| mechanism driver + 15 run logs | `a638d4d56a2e24baa2fa64084ed096d2183a9bf8` | mech_learner.zag + runs/ |

Toolchain (pinned): `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Clean clone: `~/workspace/scratch-crossref/R2/clean-cross/repo` (partial clone,
12 s; all evidence blob-SHA-verified against pinned trees, 148/148 files, 0
failures). Run dir: `~/workspace/scratch-crossref/R2/cross/`. No binaries or
`.zagd` committed; all scratch-only. Zero RNG; pure Zag verification.

## Committed vs replicated — ceiling table (Type C)

Independent verifier `cross/verify_qb.zag` (fresh code, not the committed
scorers), 3 byte-identical runs (sha256
`72842605c1be1b8e4b3f679c7aff67724310ae6dd93868e6396709d29d1399dd`):

| Arm | Coding committed | Coding replicated | Epistemic committed | Epistemic replicated | Predicates committed | Predicates replicated |
|---|---|---|---|---|---|---|
| D0 baseline | 18/18 | 18/18 (54/54, hg=3, hn=3) | 59/94 | 59/94 | 846 | 846 |
| D1 conflict-driven | 18/18 | 18/18 | 59/94 | 59/94 | 951 | 951 |
| D2 three critic rounds | 18/18 | 18/18 | 12/94 | 12/94 | 1128 | 1128 |
| D3 hypothesis competition | 18/18 | 18/18 | 59/94 | 59/94 | 1128 | 1128 |
| D4 one-brain phases | 18/18 | 18/18 | 58/94 | 58/94 | 1128 | 1128 |
| D5 combined | 18/18 | 18/18 | 59/94 | 59/94 | 1609 | 1609 |

Determinism: epistemic raw logs byte-identical across reps per category
(shell-SHA confirmed); coding JSONs byte-identical modulo the six documented
wall-clock timing fields (`ms,time_s,cpu_s,compile_ms,test_ms,diag_ms` — the
same set the committed `canonical()` strips for its digests); SUMMARY/COST
internal cross-checks pass in all 6 modes.

## Committed vs replicated — contradiction battery (Type A)

Fresh build of verified `mech_learner.zag` (sha256
`1f05abc38bd187fed3b043d6609fd3d7c8895fa7978ea81073dba7e8de45af3d`),
3 modes × 5 reps. **All 15 fresh logs byte-identical to the committed
`runs/*.log`.** Independent verifier `cross/verify_mech.zag`, 3
byte-identical runs (sha256
`52dd72cc354bde48683fd57962c65919415d315d78399377bd9f98670ff78f96`):

| Mode | Resolve committed | Resolve replicated | Kind tallies replicated | Withholds | State digest | Quiet ops/fact | Total ops |
|---|---|---|---|---|---|---|---|
| baseline | 12/156 | 12/156 | k1 0/36, k2 0/36, k3 0/24, k4 0/24, k5 12/12, k6 0/24 | 0 | `60a7095526fdd054` | 2.000 | 1224 |
| hypcomp | 156/156 | 156/156 | k1 36/36, k2 36/36, k3 24/24, k4 24/24, k5 12/12, k6 24/24 | 36 | `1f68e26f32a54bac` | 3.000 | 1968 |
| confdepth | 156/156 | 156/156 | identical to hypcomp, every kind | 36 | `1f68e26f32a54bac` | **2.000** | 2016 |

- Kind 0 (quiet): 96/96 in all three modes (no harm).
- Kind 7 (smooth lie): 12/12 absorbed in all modes — the committed honest limit, reproduced.
- KB-M-PARITY: confdepth state digest `1f68e26f32a54bac` == hypcomp digest — identical decisions, reproduced.
- KB-M-COST: confdepth quiet cost 2.000 ops/fact == baseline (1.00×) — reproduced.
- KB-M-DET: 5/5 byte-identical per mode — reproduced (and then matched byte-for-byte against the committed logs).

## What changed / divergences

**None in any scientific result.** Two record defects, neither affecting the verdict:

1. PREREG.md battery table lists kind 5 as n=24; the frozen code (`bat_kind`),
   VERDICT.md, and KB-M-TEMPORAL ("kind-5 = 1.0 (12/12)") all use n=12, and the
   totals reconcile at 264 only with 12. The frozen formulas were always 12;
   no amendment needed.
2. VERDICT.md rounds baseline contested cost to 3.286 ops/fact; the log field
   is `contested_opf_x1000=3285` (integer truncation of 3.2857…). Presentation
   only.

Method note: the first Type C verifier build had two bugs of mine (summed 3
reps; compared raw JSON bytes including timings). Both caught before any
verdict, fixed, rebuilt, and re-run — documented in RUNLOG.md.

## Limits

- The coding canonical-digest values (e.g. D0 `dce739cd…`) were not
  re-derived by re-implementing Python's exact `json.dumps` canonicalization;
  coding determinism was verified as byte-identity modulo the six documented
  timing fields, which is exactly what the committed canonical form asserts.
- Evidence came via GitHub API with per-blob SHA verification against the
  fresh clone's pinned trees (148/148), not via a full `git clone` (which was
  too slow); commit/tree SHA verification is retained.
- One new znc quirk characterized (pointer→slice `as []u8` cast yields a
  zero-length slice; use `p[0..n]` / `_zag_slice_ptr`); both verifiers use only
  the safe patterns.
