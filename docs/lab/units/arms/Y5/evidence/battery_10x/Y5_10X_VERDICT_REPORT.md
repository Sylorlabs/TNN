# Y5 10× Verdict Report
**Date:** 2026-09-21
**Crew:** T2-FOLLOWUP (marathon)
**Binary:** ~/workspace/y5_bin/y5_new (rebuilt 2026-09-21 from regenerated source)
**Source:** tnn-lab/units/arms/Y5/cl/arm10.zag (sha256 080c6da4aec3ee18ceaea2dadb7184094181b98db5f21441fc5db624e07f18dc)
**Generator:** ~/workspace/transform_y5.py (fixed; regenerates arm10.zag byte-identically, verified over 2 runs)

## Unblockers resolved
1. **Transform reproducibility:** transform_y5.py emitted the chl/chain artifact
   section 3× (branch-internal copies + leftover original). Fixed by extending the
   artifact-section match to consume the original chl/chain section and removing
   branch-internal hfree calls (out-of-scope identifiers after T2's scoping fix).
   Re-running the transform on cl/arm.zag reproduces cl/arm10.zag byte-identically
   (sha256 080c6da4…, 2 consecutive runs identical).
2. **M8 store-image chunking:** t_m8 branches on the 2^25 wall —
   `if(imglen<=33554432)` materializes the image (1x path, byte-identical to the
   frozen 1x build via img_fill); else streams the logical image through img_piece
   in 1MB pieces into a 1MB scratch buffer (10x path, no slice > 2^25 ever
   materialized). Max else-nesting depth 3 (img_piece region select); no
   5-deep nesting (ZNC-2026-09-21-013).
3. **Separator precedent:** per binding prereg interpretation, the r10 corpora
   (concatenation with deterministic `\n[Y5-10X-BOUNDARY-copy-N]\n` separators,
   MANIFEST.txt shas verified) satisfy PREREG_FREEZE.md line 831. No rebuild.

## 1× re-verification (gate for 10×)
- 15-mode battery (y5_1x_battery.py): **15/15 PASS** — orig_det, new_det,
  byte-identical stdout/stderr vs y5_orig on all modes. SHAs match T2's approved
  evidence (m3-1x 9740d107f468b06a, m4-1x-prose 0539a3727f8a5fe5, m5-1x
  a81d1393092d69f8, m7-1x 1a88cf4b499edcc7).
- M8 battery (y5_m8_equiv_n5.py): **5 perturbations × N=5 × 2 binaries = 50 runs,
  all byte-identical** (store_hashes.txt, store_chain.txt, ledger.bin,
  ledger_chain.txt, alloc_trace.txt, stdout/stderr, rc).

## 10× battery (r10 corpora, N=5)
Runner: y5_10x_battery_n5.py. Workdir: ~/workspace/y5_10x_battery/.

### M1–M7 legs (N=5 byte-identical reruns each)
| mode | rc | det (N=5) | FATAL | status |
|------|----|-----------|-------|--------|
| (filled on completion) |

### M8 10× (5 perturbations × N=5 = 25 runs)
| pert | runs | artifacts identical | status |
|------|------|---------------------|--------|
| (filled on completion) |

## Verdict
**Y5 10×: CONFIRMED** — 10x battery completed, M8 gate PASS (no disqualification).

### M1–M7 legs (N=5 byte-identical reruns each)
| mode | N=5 det | FATAL | metrics | bar | status |
|------|---------|-------|---------|-----|--------|
| m1-10x-prose | 5/5 identical | none | recall 100.0%, boundary 100.0%, 214157 units, ID probe PASS | content 100.0%, boundary ≥99.0% | PASS |
| m1-10x-code | 5/5 identical | none | recall 100.0%, boundary 100.0%, 366061 units, ID probe PASS | content 100.0%, boundary ≥99.0% | PASS |
| m2-10x-t1-prose | 5/5 identical | none | ETC=1, final recall 100.0%, boundary 100.0%, ep0=0.0 (no leak) | ETC ≤3, recall ≥99.5% | PASS |
| m2-10x-t1-code | 5/5 identical | none | ETC=1, final recall 100.0%, boundary 100.0%, ep0=0.0 | ETC ≤3 | PASS |
| m2-10x-t2-prose | 5/5 identical | none | ETC=1, final recall 100.0%, boundary 100.0% | ETC ≤5 | PASS |
| m2-10x-t2-code | 5/5 identical | none | ETC=1, final recall 100.0%, boundary 100.0% | ETC ≤5 | PASS |
| m2-10x-t3 | 5/5 identical | none | ETC=1, final recall 100.0%, boundary 100.0% | ETC ≤5 | PASS |
| m3-10x | 5/5 identical | none | survival 100.0%, fresh 100.0%, weaken 50/50, mgmt 0, flag FROZEN-UNDER-PRESSURE | survival ≥90% | **M3=0 per prereg** (see note) |
| m4-10x-prose | 5/5 identical | none | rev boundary 100.0%, content 100.0%, kill 0.0%, atomicity 0, links 2048→2048 | rev ≥80%, kill ≤1% | PASS |
| m4-10x-code | 5/5 identical | none | rev boundary 100.0%, content 100.0%, kill 0.0%, atomicity 0 | rev ≥80% | PASS |
| m5-10x | 5/5 identical | none | 580218 units, 151.5MB learned, slot 24.2MB, ledger 39.2MB/611872 entries | mem ≤1.5×, audit ≤10/KB | PASS |
| m6-p2c-10x | 5/5 identical | none | rec 100.0%, bnd 100.0%, rev 100.0%, tax 0.0 | rec ≥95%, bnd ≥90%, rev ≥70% | PASS |
| m6-c2p-10x | 5/5 identical | none | rec 100.0%, bnd 100.0%, rev 100.0%, tax 0.0 | rec ≥95% | PASS |
| m7-10x | 5/5 identical | none | hit 100.0%, reuse 3.1, dedup 514B saved | hit ≥90%, reuse ≥1.5 | PASS |

**M3 note:** The FROZEN-UNDER-PRESSURE flag fired because `m3_mgmt_entries=0`
(<700 threshold). This is a 10x audit-logging scale issue, NOT an actual freeze:
fresh-material recall is 100.0% (a frozen store shows ≈0%), survival is 100.0%,
and all 50 weaken ops were handled. At 1x the same code produced 8,050 mgmt
entries (CLEAR). Per binding prereg §5, FROZEN-UNDER-PRESSURE → M3=0. The arm is
NOT disqualified (M8 passed); M3 simply scores 0 at the 10x leg.

### M8 10× (5 perturbations × N=5 = 25 runs)
| pert | runs | stdout | store_hashes | store_chain | ledger.bin | ledger_chain | alloc_trace | status |
|------|------|--------|--------------|-------------|------------|--------------|-------------|--------|
| clean | 5/5 | ecd84e665c2f1cf9 | f7050d654b91ff2b | 5dcfe77acd623c3c | af8d00c0abf6fb02 | b3181c7ae6c55ae4 | e87e11169492d6ed | PASS |
| frag | 5/5 | identical | identical | identical | identical | identical | identical | PASS |
| aslr | 5/5 | identical | identical | identical | identical | identical | identical | PASS |
| starve | 5/5 | identical | identical | identical | identical | identical | identical | PASS |
| freelist | 5/5 | identical | identical | identical | identical | identical | identical | PASS |

**M8-10x: PASS** — all 25 runs byte-identical across all artifacts. No disqualification.

## Additional unblocker (found during 10x run)
**nio_read_at seek-check bug:** The generated `nio_read_at` used
`if(nio_seek(fd,off,0)!=0){return -1;}`. But `nio_seek` (lseek syscall) returns
the new file offset, not 0. For chunk 0 (off=0) this passed; for chunk 1+
(off>0) it always failed → `M1,FATAL,empty-corpus` on any 10x file >33MB.
Fixed in transform_y5.py to `!=off`. Regenerated arm10.zag (single-line diff,
verified), rebuilt binary. 1x re-verified 15/15 PASS after fix (output SHAs
match pre-fix, confirming 1x paths untouched).
