# RUNLOG.md — T2-CERT re-verification (replacement coordinator)

## 2026-09-23 — resume
Replacement coordinator. Adopted frozen REVERIFY_PREREG.md (commit 5f067515)
as binding authority; previous coordinator never ran implementation
(no reverify/ dir on branch). Preregistration step: SATISFIED by adoption.

## Tier-3 de-dup amendment (flagged per prereg protocol)
Tier-3 H1 (commit de09f984, ARTIFACT-BOUND) completed overlapping CERT legs
after the prereg froze. Deviation: the H1-equivalent tally is re-derived via
DIFFERENT code (fresh Zag tally + Python tally, not a rebuild of
flipcount.zag); the H1-equivalent red-team plant uses a DIFFERENT angle
(nio_-API device access vs H1's raw-syscall clean-room plant).
Agree/diverge stated in VERIFY.md. No Tier-3 work was redone.

## RV1 — 0-flip tally
- Fetched results.tsv via GitHub API @ branch tnn-native-lab;
  blob 7e7f0b4e... verified byte-identical to committed evidence.
- Wrote tally2.zag (fresh): nio file read, \n/\t split, flip rule per KB-FLIP.
  Built with pinned znc 2026.07.0-dev: `znc tally2.zag --no-zagd -o tally2_bin`.
- Runs: run1/2/3.out all SHA-256 a2245358dbcb57eeda1a0f417a30c62792162514fdbbf8a3234b110e946a76d7.
  rows=35 flips=0 confirmed=34 inconclusive=1 void=0.
- Python cross-check: identical. old==stored non-YES only on t1_plant07
  (INCONCLUSIVE by construction).

## RV3 — nio-API urandom plant
- Wrote plant_nio_urandom.zag (pure Zag, zero RNG): byte-built "/dev"+"urandom",
  nio_open_root/nio_open_child/nio_read_exact, branch on buf[0]&1.
- Builds clean with pinned znc. Runtime: vary_expr(42)=42 x N — INERT
  (nio_read_exact fails on char device; substrate regular-file guard).
- Rebuilt rngscan_v3_rb.zag (blob 45e06c39...) with pinned znc
  (needed work/cert/substrate/{R33_NATIVE_IO_V1,R33_NATIVE_SHA256_V2}.zag;
  IO substrate SHA-256 e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8).
- Scan attempts 1-3: 4.3 uninitialized-use hits (conservative dataflow;
  incl. a use-after-nio_free false positive on the early-return path, cur=2
  after saw_free — analyzer is not path-sensitive). Fixed by canonical inline
  init loops + single-tail frees. Attempt 4: hits=0 verdict=PASS exit 0.
- Honest replay evidence: 8 runs, byte_identical=1, varies_with_state=0,
  exit_ok=1, layouts=2 (all true of the plant binary).
- Finding: certifier PASSes an inert /dev/urandom-via-nio plant. Blind spot
  recorded in VERIFY.md with the defense-in-depth recommendation.

## Committed
- reverify/VERIFY.md, reverify/RUNLOG.md, reverify/evidence/{tally2_run1.out,
  plant_nio_urandom.zag, plant_attest_PASS.json, results_tsv.sha256}
  (to be committed via commit_racefree.py; binaries excluded)
