# R5-PRIMARY RUNLOG — KB4 autopsy Type A replication

Crew: R5-PRIMARY (independent replication). Date: 2026-09-22/23 (UTC run on 2026-09-23).
Prereg commit (frozen): `7b2100d09911c5c10252c5756c7def288e70bd1f`.
Scope/prereg read and retained: `~/workspace/scratch-crossref/R5/SCOPE.md`,
`~/workspace/scratch-crossref/R5/PREREG_TIER1.md`.

## 1. Pin freeze (all observed 2026-09-23 UTC, before any run)

| Pin | Expected | Observed | Status |
|---|---|---|---|
| Evidence commit | `66fbb329aa831c14f3f3100a20e177bbb12e27b1` | fetched via `git fetch --depth 1 --filter=blob:none`; `git cat-file -t` = commit | FROZEN |
| `docs/lab/kb/autopsy/` file count | exactly 37 | `git ls-tree -r` → tree `b4585b7123c0a8dd430202c60b802b7715468d29`, **37 files** | FROZEN |
| WHY_REPORT commit | `bc6d130539e4a5539ea3361f57e02e39378f26ba` | fetched; contains `docs/lab/kb/autopsy/WHY_REPORT.md` blob `bd12da7161fa30b9d24d17d4cf7744f90eb493c6` | FROZEN |
| Toolchain | `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` | exists, used for all builds | FROZEN |

Notes:
- A full clone of the repo into `~/workspace/scratch-crossref/R5/clean/` failed
  mid-fetch (~932 MB, `fetch-pack: unexpected disconnect` / `early EOF`); the
  directory was reinitialized and only the exact pinned commits/trees were
  fetched with `--depth 1 --filter=blob:none`. All three pins verified by hash.
- The 37 autopsy files were fetched from the GitHub content API into
  `primary/evidence/docs/lab/kb/autopsy/`; each file was re-hashed as a Git
  blob (`SHA1("blob <len>\0" + content)`) against the committed blob id from
  `git ls-tree`. **All 37 passed.** (An early check compared raw-content SHA1
  against blob ids and appeared to fail — that was a verifier bug, not
  repository corruption; corrected before proceeding.)
- At prereg commit `7b2100d…` the autopsy subtree holds 38 files (WHY_REPORT.md
  added later); the 37-file pin at `66fbb329…` is the evidence under test.
- `PREREG_DRAFT_SUSPECT_GATE.md` (unsigned) present in evidence; excluded from
  all verification per the ruling.
- `TMPDIR=/home/hatch/workspace/tmp_commit` set for every git/python/build
  invocation (never `/tmp`; lab `/tmp` is a shared 512 MB tmpfs).
- All slices < 2^25; zero RNG anywhere; no binaries or `.zagd` committed
  (binaries kept local-only in `primary/probes/`; `.zag-cache`/`.zagd.semantic-ready`
  removed after build; none will be committed).

## 2. Build (pure Zag, pinned znc, from probe directory)

Sources copied verbatim from evidence into `primary/probes/`:
`probe_pl1.zag`, `probe_pl2.zag`, `probe_pa1.zag`, `probe_pa2.zag`,
`R33_NATIVE_IO_V1.zag`, `batch_A.txt`, `batch_B.txt`, `pbatch_pa1.txt`,
`pbatch_pa2_A.txt`, `pbatch_pa2_B.txt`, `pa1_truth.json`.

`znc_linux_x86_64_abed8aa1 probe_<p>.zag -o probe_<p> --no-analyze`
(all from `primary/probes/`; imports resolve relative to cwd):

| binary | build | sha256 (local only, not committed) |
|---|---|---|
| probe_pl1 | OK, 29877 B | `c51cae45183a58097535b12fa7bcf4686f9c6000ada8daddf4bcdaca9d7bf27b` |
| probe_pl2 | OK, 33973 B | `1deb7c9d6b4005f10808e36ebcbea146dc6a5a97c38dbbb83794fad319c3253c` |
| probe_pa1 | OK, 25491 B | `00cafd76a9ba018b4e87d7da33ed4552b7e4258c33c2acdb5dd1aa817fd43d5d` |
| probe_pa2 | OK, 33973 B | `2a8274bf5c697de6788db29bb0c10972f5665b5f3fa80eeeb54e07d30f261365` |

(`znc: warning: zagd unavailable` on all four — foreground compilation only;
outputs verified byte-identical, so the warning is immaterial.)

## 3. Runs (3× each, byte-identical required)

From `primary/probes/`, workdir arg `.`:

| # | command | output |
|---|---|---|
| 1–3 | `./probe_pl1 . batch_A.txt 370` | `runs/out_pl1_A_rep{1,2,3}.txt` |
| 4–6 | `./probe_pl1 . batch_B.txt 370` | `runs/out_pl1_B_rep{1,2,3}.txt` |
| 7–9 | `./probe_pl2 . batch_A.txt 370` | `runs/out_pl2_A_rep{1,2,3}.txt` |
| 10–12 | `./probe_pl2 . batch_B.txt 370` | `runs/out_pl2_B_rep{1,2,3}.txt` |
| 13–15 | `./probe_pa2 . pbatch_pa2_A.txt 1110` | `runs/out_pa2_A_rep{1,2,3}.txt` |
| 16–18 | `./probe_pa2 . pbatch_pa2_B.txt 1110` | `runs/out_pa2_B_rep{1,2,3}.txt` |
| 19–21 | `./probe_pa1 . pbatch_pa1.txt` | `runs/out_pa1_rep{1,2,3}.txt` |

Rep-consistency: all 7 combos 3× byte-identical (sha256 of rep1=rep2=rep3).
vs committed: **all 7 rep1 outputs byte-identical to committed
`out_<k>_rep1.txt`** (sha256 match).

Output sha256 (rep1):
- `out_pl1_A_rep1.txt` `1f47a16d3b324e00107c5c37e11e39aac18aedcf05ac060b0b586426dd7bf2f6`
- `out_pl1_B_rep1.txt` `c03963ca2902f7ff98d8845d7d42e5ca55fb71bd01718818eb3bd1e32358bafe`
- `out_pl2_A_rep1.txt` `a52b61cef54c3cd20899c4b1b06038080efeda552b3ce4a1b3019494273085e1`
- `out_pl2_B_rep1.txt` `89f32a61e8a7aa874040888b2f9fa85e2cacf21d8cee7735fa8319e7f9e5bc32`
- `out_pa2_A_rep1.txt` `e28eb30c966c87e81fb99e9a5abf1e102f8954d78aa7c7c70465a6b56ec470e4`
- `out_pa2_B_rep1.txt` `2a2ab03ed52e5f5b79b2dc18a127ec45bcc5828b3af0b6b2f4c9e48759962b76`
- `out_pa1_rep1.txt` `411fc737c7843fd06bd276ae70ab3fcd56bbf2ab6d10755151c01ef8bca164c0`

Probe SUMMARY lines (mine = committed):
`pl1_A 813/111`, `pl1_B 799/126`, `pl2_A 924/0`, `pl2_B 925/0`,
`pa2_A 924/0`, `pa2_B 925/0`, `pa1 855/69`.

## 4. Independent scoring (pure-Zag verifier, Python only glue)

Committed `score_probes.py` is not verification authority (and hardcodes a
local path). I built `primary/probes/scorer.zag` — a pure-Zag scorer joining
probe outputs with truth by line number and computing
adv_false/adv_installs with the frozen bars
(≤15% PASS / 15–30% MARGINAL / >30% FAIL / <50 true adv installs DEGENERATE).

Truth sourcing (committed only, hash-verified):
- `docs/lab/prose-learning/epistemic_wave/kb4_rerun/truth.json`
  blob `dd1f4bcb32bd5023dcab254773ffdc534eeba289` @ prereg commit —
  converted by Python glue to `truth_A.tsv` (924 lines) / `truth_B.tsv`
  (925 lines): `<variant_id>\t<correct>`, line order = batch order.
  Key counts verified: A/0..A/923 (924), B/0..B/924 (925) — exactly the
  batch line counts.
- `pa1_truth.json` (committed in the 37) → `truth_pa1.tsv` (924 lines):
  `<variant_id>\t<adv_correct>` in numeric key order.

Scorer built with pinned znc (`probes/scorer`, sha256
`816f16fa2c821fd72dab6ac219a31297244ee7d838e5f6755792bbe095e8ed4c`,
local only). Results on my rep1 outputs:

| probe | adv_installs | adv_false | adv_true | ‰ | verdict | lines |
|---|---|---|---|---|---|---|
| pl1_A | 80 | 33 | 47 | 412 | DEGENERATE | 924/924 OK |
| pl1_B | 93 | 41 | 52 | 440 | FAIL | 925/925 OK |
| pl2_A | 184 | 93 | 91 | 505 | FAIL | 924/924 OK |
| pl2_B | 185 | 101 | 84 | 545 | FAIL | 925/925 OK |
| pa2_A | 184 | 93 | 91 | 505 | FAIL | 924/924 OK |
| pa2_B | 185 | 101 | 84 | 545 | FAIL | 925/925 OK |
| pa1 | 115 | 50 | 65 | 434 | FAIL | 924/924 OK |

Every cell is **exactly** the committed `probe_scores.json`
(33/80 = 0.4125; 41/93 = 0.44086; 93/184 = 0.50543; 101/185 = 0.54594;
50/115 = 0.43478).

## 5. Claim-by-claim verification (independent, from committed evidence)

- **L8 removal (P-L1):** original frozen gate outputs fetched from
  `kb4_rerun/out_{A,B}_rep1.txt` (blobs `b85f2abf…`, `826ca09c…`,
  hash-verified). P-L1 A decisions **0/924 flips** vs original A
  (evidence column differs where the +20 printed — expected); rate
  33/80 = 41.25% unchanged. B: **exactly 6 decision flips**
  (lines 433/443/448/452/469/472, all INSTALL→WITHHOLD); truth check:
  5 were false installs, 1 true. 46/99 = 46.46% → 41/93 = 44.09%
  (−2.37pp ≈ −2.4pp). "Did NOT cause the consistent-error installs; only
  six B-side re-challenge flips, −2.4pp" — CONFIRMED.
- **L4 removal (P-L2):** 93/184 = 50.54% / 101/185 = 54.59% — raw ~50%+
  exposed. CONFIRMED.
- **1:1 trade (P-A2):** P-A2 vs P-L2 INSTALL/WITHHOLD streams
  **line-identical** (0 mismatches, 924/924 A, 925/925 B); scores identical.
  (Full bytes differ only in the audit evidence column — re-keyed stimulus
  slots print different evidence numbers, which is expected.) CONFIRMED.
- **Corroboration (P-A1):** 50/115 = 43.478% FAIL; all 50 both-fooled-and-
  agreeing fixtures installed (verified in `pa1_truth.json`: 184 adversarial
  fixtures in the common batch, 50 agree∧¬adv_correct, all INSTALL).
  43.5% > 41.2% — corroboration fails worse. CONFIRMED.
- **WHY_REPORT audit (hole hunt):**
  - W1 "A = match rule exactly": recomputed from committed truth.json +
    frozen A output — **0/184 deviations** on adversarial lines. CONFIRMED.
  - W5/W1 confidence anti-informative (adversarial lines): recomputed means
    **exactly** the reported 429.8/439.1 (+9.3) A and 849.4/861.4 (+12.0) B.
    CONFIRMED. (All-lines means differ — the claim is scoped to adversarial
    lines, where the gate is tested; verified the scoping.)
  - M3 cells: recomputed **44/184 A (23.9%)**, **31/185 B** — exact match.
    CONFIRMED.
  - W3's Python gate model / W1 bit-counts (0.019/0.033) / W5 LP proof:
    scripts live in uncommitted `~/workspace/kb4-why/` — not re-runnable
    from committed evidence; noted as unaudited, not contradicted. Every
    checkable quantitative claim reproduced exactly; no hole found in the
    impossibility argument from committed evidence.

## 6. Corrections / deviations from prereg prose (documentation-level only)

1. Tier-1 prereg line 99 says P-A1 has "50 of **185** paired fixtures" fooled
   correlatively. The committed pa1 common batch contains **184** adversarial
   (stim,variant) fixtures (A∩B intersection; A has 184, B has 185
   adversarial keys in truth.json). The 50 both-fooled-and-agreeing fixtures
   and the scored 50/115 = 43.5% are unaffected — this is a prose
   over-correction in the prereg (the 185 figure belongs to B's standalone
   adversarial count per WHY_REPORT correction #1), not a data discrepancy.
2. AUTOPSY.md's "P-L1 byte-identical 41.2% on A": decisions and scores are
   byte-identical (0/924 flips, 33/80); the audit evidence column differs
   where L8's +20 no longer prints. No contradiction — claim holds at the
   decision/score level verified here.
3. WHY_REPORT.md (commit `bc6d1305…`) was fetched and read for the
   impossibility/falsifier audit above; no holes found.

## 7. Verdict

**REPRODUCED.** All seven probe outputs byte-identical to committed; all
seven scored cells exactly the committed values via an independent pure-Zag
scorer; every structural sub-claim (6 B-flips/−2.4pp, 0 A-flips, P-A2≡P-L2
decisions, 50/115 corroboration failure, A=match-rule, anti-informative
confidence, M3 44/31) confirmed from committed evidence. No hole in the
impossibility argument found.
