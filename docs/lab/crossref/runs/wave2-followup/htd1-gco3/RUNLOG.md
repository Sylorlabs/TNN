# HTD1 G-CO3 Red-Team — Run Log

Subagent task: *"more investigation + RED TEAM it"* (Micah, 2026-09-24 verdicts round 2).
All work in `~/workspace/scratch-crossref/T2/HTD1/gco3-redteam/`. No commits to `sylorlabs/TNN`.
Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`).
Zero RNG in every decision path. Times in PDT.

## 2026-09-24 ~15:30 — resumed red-team session

Prior session (compacted) had established: frozen docs SHA-verified from commit
`7b2100d09911c5c10252c5756c7def288e70bd1f`; `run_0` artifact hashes matched originals;
independent Python parse of `opcounts.bin` gave weighted KB2a=0.6855 / raw=0.4991;
single-class flip boundaries, ±2× two-class check, per-item heterogeneity, and negative
controls computed. Remaining: build the pure-Zag verifier, rebuild test, probe spot-check,
denominator-semantics check, ledger-strip attack, and the two deliverables.

## Build of the independent verifier

Wrote `src/gco3_verify.zag`: standalone pure-Zag program (no shared code with the scored
binary except the IO substrate). Reads `opcounts.bin`, accumulates the 11-class raw vectors,
recomputes weighted milli-costs vs `verdict.txt` expectations, KB2a/KB2b weighted+raw (×1000
integer floor), single-class flip-boundary scans (multiplier in thousandths, 1..20000), and
the 2^10 ±2× calibration-box corner sweep.

- Copied `R33_NATIVE_IO_V1.zag` from `~/workspace/htd-1/builds/ref-baselines/` into `src/`
  (SHA-256 `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`) —
  needed for `nio_alloc`/`nio_free`; `@import` added to the verifier.
- First compile failed: `nio_alloc` unknown without the import (expected).
- Compiled clean (only L0012 leak lints, non-fatal):
  `znc gco3_verify.zag -o gco3_verify_bin` → 38,721 bytes,
  SHA-256 `a68ddd829d4ffc56484d2f9fd798160364ac287d50e886080fcff1a0715d7f93`.
- Source SHA-256: `5f63402a69ebb063f48a3153964c8cd12659b94711bf8a30bfb736e32fd50781`.

## Verifier runs (3× determinism)

```
./src/gco3_verify_bin ~/workspace/htd-1/builds/gco3/run_0/opcounts.bin > runs/verify_N.txt  (N=1,2,3)
```
SHA-256 of all three: `a6c19aa1a28cb28d0373924c3c51448cfbcec4f8cb83f48386e3f80a91d0429c` — byte-identical.

Output:
```
GCO3-VERIFY
nitems=124
C_plan_milli=122525540 expect=122525540
C_exec_milli=360360200 expect=360360200
C_ver_milli=201667200 expect=201667200
KB2a_w_x1000=685 bar>=600
KB2b_w_x1000=178 bar<350
KB2a_raw_x1000=499 bar>=600
KB2b_raw_x1000=90 bar<350
FLIP class=0 raise_to=0 lower_to=0
FLIP class=1 raise_to=0 lower_to=0
FLIP class=2 raise_to=0 lower_to=0
FLIP class=3 raise_to=0 lower_to=0
FLIP class=4 raise_to=8134 lower_to=0
FLIP class=5 raise_to=14873 lower_to=0
FLIP class=6 raise_to=4853 lower_to=0
FLIP class=7 raise_to=0 lower_to=0
FLIP class=8 raise_to=0 lower_to=0
FLIP class=9 raise_to=0 lower_to=64
FLIP class=10 raise_to=0 lower_to=0
BOXMIN_x1000=571 corners=1024
VERIFY_DONE
```
Interpretation: no single class flips within ×0.001–×20 except OP-05 (raise to ×8.134),
OP-06 (raise to ×14.873), OP-07 (raise to ×4.853), OP-10 (lower to ×0.064). Worst ±2×
corner = 0.5716 (KILL) — requires all 10 informative classes at their tripwire edges.

## Rebuild-from-source test (stale-binary incident closure)

```
cd ~/workspace/htd-1/builds/gco3
znc gco3.zag -o ~/workspace/scratch-crossref/T2/HTD1/gco3-redteam/runs/gco3_rebuild_bin
sha256sum runs/gco3_rebuild_bin gco3_bin_new
```
Both: `7daba46f7b012d85388929da0b577b917482f70ff959e8ed35dba4d498695092` — **byte-identical**.
The scored binary provably contains the decoy-length fix.

Fresh end-to-end run from the rebuilt binary (5.5 s):
```
mkdir -p runs/fresh && cd runs/fresh
../gco3_rebuild_bin run ./out <probes/prose_rec.txt> <probes/code_rec.txt>
```
`out/verdict.txt`: KB2a_first_run_share_x1000=685 PASS, KB2b_amort10_share_x1000=178 PASS,
C_plan_milli=122525540, C_exec_milli=360360200, C_ver_milli=201667200.
`cmp` of all five artifacts vs `run_0`: **IDENTICAL** (ledger.bin, steplog.bin,
outputs.bin, opcounts.bin, verdict.txt).

## Probe-manifest spot check

Python check of both manifests against corpora (`pg100.txt` 5,638,480 B, `sqlite3.c` 9,515,341 B):
**124/124 spans exact** (byte offsets + SHA-256); 0 self-decoys; 0 byte-identical decoys;
80 same-length decoy slots (matches verdict sheet's "+80 OP-03" claim).

## Denominator-semantics check (attack A5)

| Reading | run weighted | run raw | rubberstamp weighted | rubberstamp raw |
|---|---|---|---|---|
| (a) crew: planning/(planning+exec₀+ver₀) ≥ 0.60 | 0.6855 PASS | 0.4991 KILL | 0.4421 KILL ✓ | 0.2520 KILL ✓ |
| (b) literal-alt: planning/(exec₀+ver₀) ≥ 0.60 | 2.1801 PASS | 0.9962 PASS | 0.7923 PASS ✗ | 0.3370 KILL ✓ |

Reading (b) lets the degenerate rubberstamp planner PASS weighted — the bar stops biting its
own negative control. Crew's denominator (a) is the only parse under which the control works.

## Ledger-overhead strip (attack A6, contract-invalid by design)

Removed all mechanism-added entry costs (OP-05×16, OP-06×64, OP-07×1, OP-09×56 per entry,
OP-11×1 per mechanism-added entry) from both sides:
weighted KB2a 0.6855 → **0.7062** (still PASS); raw KB2a 0.4991 → **0.4991** (still KILL).
Ledger share: 6.8% of plan, 15.5% of first-run exec+ver. Verdict does not depend on it.
(One scripting slip on the first attempt mixed per-run means with 10-run entry counts and
produced nonsense 1.3692/1.6336 with a negative class — caught by the min≥0 assertion,
redone correctly.)

## Negative-control discrimination under raw (attack A11)

From control opcounts.bin files: rubberstamp raw KB2a = 0.2520 (KILL), poison raw = 0.1946
(KILL), mutate raw = 0.6213 (not a KB2 control). Scored control verdicts on disk confirm:
`rubberstamp_first_run_share_x1000=442`, all three controls `*_PASS`. Raw is a working
discriminator; its only disagreement with weighted is the scored arm.

## Frozen-document text analysis (weighted-vs-raw provenance)

- `prereg/HTD1_PREREG_FROZEN_2026-09-21.md` §3b: kill bar reads "planning <60% of first-run ops
  or amortized planning ≥35% by item 10". Elsewhere the prereg says "FULL COST" when it means
  weighted cost — the diction distinction is real. §7 verdict rubric is silent on the metric.
- `contracts/COST_MODEL_FROZEN.md` §2: weights "frozen for all of HTD-1 (global…)";
  §5 routes G-CO3's KB2 through "the same taxonomy" and names "G-CO3 KB2 planning-op share";
  §5 default rule prices at frozen weights; §9.1 rejects unpriced cross-class comparison.
- Neither document explicitly says "apply weights before forming the KB2 ratio" — the
  governance gap is real and is the basis for the recommendation's caveat.

## Deliverables written

- `VERDICT.md` — red-team verdict, attack table (A1–A11), weighted-vs-raw case for each
  side, evidence-integrity section, recommendation to Micah (weighted-PASS recommended;
  governance call his; one-sentence amendment proposed).
- `RUNLOG.md` — this file.

Nothing committed to `sylorlabs/TNN`. Workdir only:
`~/workspace/scratch-crossref/T2/HTD1/gco3-redteam/`.
