# Pig-Front Experiment Run Log

**Date:** 2026-09-26  
**Binary:** `pigfront_bin` (built from `pigfront.zag` via `znc_linux_x86_64_abed8aa1`)  
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Run 1
- **Command:** `./pigfront_bin run /home/hatch/workspace/forkB-scratch/frames/donor ./run1 /home/hatch/workspace/pigfront/forka`
- **RC:** 0
- **Outputs:** `front_construct.ppm`, `epistemic_map.ppm`, `trace_pigfront.txt`, `metrics.txt`

## Run 2
- **Command:** `./pigfront_bin run /home/hatch/workspace/forkB-scratch/frames/donor ./run2 /home/hatch/workspace/pigfront/forka`
- **RC:** 0
- **Outputs:** identical to Run 1

## SHA-256 (both runs identical)

```
4463bbced42f7b2ba7c6684a79238f102db4032bce270c3a597a861aeb8e88ad  epistemic_map.ppm
4b413a240f8f6d134e8d306ffe17f0ee2c3a597a861aeb8e88ad  front_construct.ppm
7ccb71bb0d047d4ea21897a2aa4f022c67133a796dff533bde214f0b06ee6787  metrics.txt
903130750fd3d933b535f50c9a75be1b894db671b794de151c7663407920d699  trace_pigfront.txt
```

**Determinism:** `diff -r run1 run2` → IDENTICAL. Zero RNG in decision paths.

## Bugs Found & Fixed During Development

1. **PLAN buffer OOB:** `h_put64(PLAN, 224, ...)` on a 224-byte allocation → fixed to 232 bytes.
2. **CMP buffer OOB:** `h_put64(CMP, 160, ...)` on a 160-byte allocation → fixed to 168 bytes.
3. **Hardcoded "0/24" vs measured 17/24:** Deliberation text hardcoded "eye-pair test 0/24"
   but the detector fired 17/24. Fixed to report the measurement honestly and explain
   why side-view spot pairs ≠ frontal-face observations.
4. **label_comps O(C×n) → O(n):** Bbox/centroid accumulation moved into the flood
   (was a separate full-frame scan per component; 8+ min → 4 sec).
