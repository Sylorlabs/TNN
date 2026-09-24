# RT-CASCADE — fault containment (contender A)

**Method:** clean `seq+mix` render vs fault renders on `plans/pv_seq.txt`
(1,323,000 samples). Fault family: pre-fault gen [0,fat), fault applied to
[flat,fat+flen), post-fault gen [fat+flen,nsamp) — the fault window is NEVER
regenerated, so any difference outside it is a genuine cascade. Sample-level
`cmp` of s32 mix dumps. Tool: `evidence/cascade.py`.

**2026-09-24 results (rebuilt renderer with corrected fault scheduling):**

| Fault | at | len | pre diffs | window diffs | post diffs |
|---|---|---|---|---|---|
| single-bit (XOR 1) | 3 s | 1 | 0/132,300 | 1/1 | **0**/1,190,699 |
| burst (deterministic) | 10 s | 44,100 | 0/441,000 | 44,100/44,100 | **0**/837,900 |
| dropout (zero) | 10 s | 44,100 | 0/441,000 | 44,098/44,100 | **0**/837,900 |
| DC shift (+2^30) | 10 s | 44,100 | 0/441,000 | 44,100/44,100 | **0**/837,900 |

Dropout note: 2 of 44,100 window samples were already exactly 0 in the clean
render (verified offsets 2826, 28406), so zeroing changed nothing there —
44,098/44,100 is the honest expected count.

**Native baseline (independently rerun):** single-bit fault → **5,791**
post-fault propagating differences.

**Why zero cascade is structural for A:** generation never reads the mix
buffer — every sample is a pure function of (plan, t). Corrupting the mix
cannot influence any subsequently generated sample. The fault models above
are empirical confirmation of a construction guarantee.

**Fault-scheduling fix (2026-09-24):** the original fault family regenerated
[fat,nsamp) *after* applying the fault, so the fault window contained
fault+clean (burst/DC) or nothing (dropout: clean overwrote the zeros).
Corrected to regenerate only [fat+flen,nsamp). All four models now show the
fault landing exactly in its window and zero propagation.
