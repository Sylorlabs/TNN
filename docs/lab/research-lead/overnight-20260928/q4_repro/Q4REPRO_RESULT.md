# Q4 F-PARCOND Independent Reproduction Result

## Verdict: REPRODUCED

All three kill bars pass. The F-PARCOND BUILD-PASS result reproduces exactly from committed source.

## Method
Source extracted via `git show 5f56cc491:docs/lab/research-lead/overnight-20260928/q4_parcond/q4_parcond.zag`.
Compiled with `/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`.
Three independent runs executed.

## Results

### K1: Source from commit - PASS
Source extracted from commit 5f56cc491 via git show. Working tree not used.

### K2: Reproduction matches - PASS
- Exit code: 0 on all 3 runs.
- md5: e9be97dd8a0c8428ce4f616e087a6433 on all 3 runs (matches reported).
- Byte-identical: all 3 runs identical.
- Content: diff against committed Q4PARCOND_RAW_1.txt shows zero differences.
- Stderr: 0 bytes on all 3 runs.

Output:
```
Q4-PARCOND
P1-PARCOND BEST node=1105 ev_correct=32/32 obs_correct=22 opc=7 keep=1
P1-PARCOND TRUE correct=64/64 bobs_true=40/64
P1-PARCOND trace_events=3860 nodes=3868
D1 kept=1105
P2-REUSE hit_iv=0 final_true=64/64
P2-SCRATCH hit_iv=24 final_true=52/64
REUSE_IV 0
SCRATCH_IV 24
KB3 1
DONE
```

### K3: Purity - PASS
- Pure Zag: only znc compiler and shell commands used.
- Zero Python invocations.
- Zero em/en-dash bytes in committed files.
- 3/3 deterministic.

## Conclusion
The F-PARCOND result (BUILD-PASS, 5f56cc491) is independently reproducible from committed source. Promotion pipeline step 4 complete.

## Files
- PREREG_Q4REPRO.md (this prereg)
- Q4REPRO_RAW_1.txt, Q4REPRO_RAW_2.txt, Q4REPRO_RAW_3.txt (identical outputs)
- Q4REPRO_RAW_1.err, Q4REPRO_RAW_2.err, Q4REPRO_RAW_3.err (empty)
