# R3-CROSS RUNLOG

Crew: R3-CROSS (independent cross-check, teacher showdown Legs A/B).
Date: 2026-09-22. Task: reproduce every committed R3 number from the frozen
evidence with an independently written pure-Zag verifier; zero trust in
R3-PRIMARY code/output.

## Frozen pins (recorded before running)

- Crossref prereg commit: `7b2100d09911c5c10252c5756c7def288e70bd1f`
  (tree `a88b8b9f3374be980628b8999b6c3ad0aabacb9a`)
- Evidence commit: `d915f0258e2e056b954bfd5f40f831ebcff2f064`
  (tree `ebf7eae62d93f398c34b24a4a53ccb8ce01da86a`)
- Tier-1 prereg: `docs/lab/crossref/PREREG_TIER1.md`
  (blob `64d498d7ea2c93e8be12c2306e8c82e619c46c5b`)
- R3 prereg: `docs/lab/GROK47_OVERNIGHT/teacher/PREREG.md`
  (blob `054277af9cce76e8277b75a6afdd81648fb1c50b`)
- Final verdict: blob `801f077faca256c88d37f0f8a9dbe224e2ba9e19`
- Toolchain: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  SHA256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
  (verified 2026-09-22)
- Substrate: `R33_NATIVE_IO_V1.zag`
  (`e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`),
  `R33_NATIVE_SHA256_V2.zag`
  (`9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bc`)

## Inputs staged (all SHA-verified against the commit tree)

`~/workspace/scratch-crossref/R3/cross/`:
- `corpora/corpus_grok47.json` (96,880 B;
  `111f588f29f23c7864f4842401516e9b30d98c495f5d1a0b68642a71d67f467a`)
- `corpora/corpus_grok46_english.json`
  (`7f3a25739981c8276082ceeda7de3628afd88977e7a16bd0a5f220eba2bc2508`)
- `batches/dump_batch00..19.txt`, `batches/teach_batch00..19.txt` (40 files,
  each blob SHA verified) + `SHA256SUMS.txt`
- `batches/legC47/teach47_run1..5.log` (committed tree: all five paths share
  blob `1ec9f7c8277077ac47c74c77b18d3faa9c1dae22`)
- `batches/legA47/grok47_rep0..4.log` (standardized-driver reruns)
- `batches/leg46_teacher_leg.log` (grok-4.6 frozen English legC log,
  blob `11543a6c02806e5fc7d61312d537d3c16cfecf28`)

Method deviation (disclosed): no `git` on this VM and no clone path
succeeded, so `clean-cross/` is a GitHub-API-extracted mirror (each blob
SHA-verified), not a `git clone`. Integrity is by per-blob SHA, which is
strictly stronger than a clone for this purpose.

## Build

```
znc_linux_x86_64_abed8aa1 r3_cross.zag --no-zagd --no-analyze \
  --no-foreground-cache -o r3_cross_bin
# -> wrote native binary r3_cross_bin (113267 bytes main, 0 external tools)
```

`r3_cross.zag` (~790 lines, pure Zag): hand-written JSON parser, channel
diffs, Leg-B scorer with token-level prose checks (`has_token` maximal
digit-run matching), SHA256 batch verification, digest extraction, and an
independent reimplementation of the Zharovia `t5_truth` oracle + probe
permutation for the skip-set audit. Python used only as download glue.
Zero RNG. No R3-PRIMARY code read or reused.

Debugging notes (kept for the record):
- Parser initially missed whitespace after JSON colons and the per-object
  closing `}` — fixed; parser now validates 240/240/240 with strict
  structural checks (rc=0).
- Teach-file tail guard: `"PROBE_VALUE:"` includes the colon (12 chars);
  guard checks digits-to-EOF after it.
- 4.6 distractor toward-true is 11/12, not 12/12 — matches the committed
  `ERROR_INVENTORY.md` (`id 71: dis=other(22)`); expectation set to 11.

## Runs (byte-identical ×3)

```
./r3_cross_bin > run1.txt   # exit 0, fails=0
./r3_cross_bin > run2.txt   # exit 0
./r3_cross_bin > run3.txt   # exit 0
sha256sum run1.txt run2.txt run3.txt
# 5233088ac7427ad9ad8c7e15b9c128eecdc92219620757725a32ffde959e7a9d (×3)
```

## Result digest (from run output)

- parse 47/46: rc=0; input_claims identical; false-plant table crosscheck ok
- Leg A: obs_diff=0, probe_diff=0 (dump_diff=7 @88–94; distr_diff=84, info only)
- Leg B 47: E_dump=0, E_obs=0, E_prb=0, inconsistent=0; faithful 12/12;
  prose_ok 12/12; distr_true 12/12
- Leg B 46: E_dump=7 @88–94, E_obs=0, E_prb=0, inconsistent=0; faithful 12/12;
  prose_ok 12/12; distr_true 11/12 (id71=other(22), as inventoried)
- Capture: present 40/40, sha_ok 40/40, idcov12 40/40, guards 40/40
- Digest: 5 legC47 logs byte-identical; digests agree 5/5; match 4.6 frozen;
  value `be5dba8498fffd515f6b9a3b16068300a1d58b00d963338e2b9a0dfad7e9e05d`
- Skip audit: attempted 192, skipped 187, accepted 5 (48,50,52,138,191);
  differentiators 88–94: 4 taught, 4 skipped, 0 accepted;
  driver log independently reports skipped=187
- Rule: legA_tie=1 → champion=47 (grok-4.7)
- Defect 1 (digest domain substitution): as described, verdict-neutral
- Defect 2 (187 skips): as described; denominator is 192 (8×24 slice loop),
  not 240; verdict-neutral per (a)(b)(c) in VERDICT.md
- fails=0 → exit 0

Full output: `run1.txt` (== `run2.txt` == `run3.txt`).
Verdict: **REPRODUCED** — see `VERDICT.md`.
