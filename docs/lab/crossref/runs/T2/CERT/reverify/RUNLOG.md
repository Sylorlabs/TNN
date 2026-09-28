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

## 2026-09-24 — RV2 + RV3 corrective completion (follow-up commit)

Prereg: 5f067515 (frozen; adopted, committed alone pre-implementation).

### RV2 — symbol gap proven at toolchain level
- Pinned-znc builds of `nio_open_readonly`/`_zag_rand` callers abort with
  "native: call to unknown function" for each; full dirty1 variation.zag build
  aborts with both errors at plant_urandom line 102. Neither symbol in the
  vendored R33_NATIVE_IO_V1.zag. dirty1 binary unreproducible — VERIFIED AS
  DESCRIBED. Original plant.bin absent from lab tree (search negative).
- Deterministic shim (_zag_rand=42, raw-syscall nio_open_readonly) builds;
  3x byte-identical outputs c524e5f2b... but NOT a reproduction (semantics changed;
  plant_urandom is dead code in the committed source; certifier flagged the
  _zag_rand source token, R6a, not behavior).
- Battery scan: dirty1_urandom is the ONLY module with unresolvable references
  (plant11 defines its own deterministic _zag_rand — no gap; dirty2/3/5, r1: 0 hits).

### RV3 — 5-plant red team + rngscan second leg
- gen_plants.py (deterministic glue) built 14 cases: P1 empty, P2 4MiB/4MiB+1,
  P3 truncated-ev/runs7/ident0/bad-manifest, P4 missing-module/-evidence/-manifest,
  P5 128/129 manifest entries + binary at/over 33,554,431 cap.
- run_rv3.py ran each 3x old + 3x new with pinned thincert binaries.
- Result: 0 flips. 13/14 agree exactly (verdict + byte-identical attestations);
  P4c: both exit 2 (no manifest -> usage-IO), no attestation.
- P5a_128 / P5b_129: thincert_old CRASHES ("invalid or double free", no
  attestation); thincert_new PASS/FAIL-correct. Bisect: PASS<=64, crash>=70,
  follows manifest count not builddir count.
- White-box: old binary's manifest tables = 3 consecutive same-size
  `as []i32` casts (thincert_orig.zag:763-765) = exact ZNC-2026-09-21-007 trigger.
  Minimal probe on pinned toolchain PROVES 2nd/3rd casts' slots 0-2 alias the
  previous array's slots 65-67 (layout-dependent offset; 2026-09-21 probe saw 9-11).
  At <=65 entries the aliased slots are uninitialized heap (historical verdicts
  survived by allocator luck); at >=66 entries live values crash the heap.
  thincert_new (arena transform) immune at 128 entries.
- Historical impact: NONE. Largest historical manifest: 2 M/S entries; no
  historical row changes class. Instrument-robustness divergence, not a verdict
  flip. Reported plainly in VERIFY.md.
- rngscan leg: rs1_empty FAIL both (vendored BAD), rs2_clean PASS both
  (fixed module with valid deterministic vary_expr), rs3_badev FAIL both
  (1 REPLAY hit). All 3x deterministic, all agreeing.

### Kill-bar disposition: RV-CONFIRM
RV1 (35,0,34,0,0,1) re-derived; RV2 gap proven with failed-build evidence;
RV3 0 flips. The 0-flips claim REPRODUCES; dirty1 gap VERIFIED AS DESCRIBED.

Evidence committed: reverify/evidence/{rv2_symbol_gap.txt, rv3_summary.tsv,
rv3_p5a_crash.txt, thincert_full_digests.txt, rngscan_digests.txt, gen_plants.py,
run_rv3.py, bisect_crash.py, bisect2_crash.py} + updated VERIFY.md/RUNLOG.md.
No binaries committed.
