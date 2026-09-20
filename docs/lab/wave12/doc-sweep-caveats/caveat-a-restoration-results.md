# Caveat (a): `restoration.results.txt` `expected=0 / actual=127` anomalies

**Date:** 2026-09-20
**Verdict: PROCEDURAL ARTIFACT — not a real problem.**

## The file

`~/workspace/tnn-lab/wave12/senses/doc-sweep/docs_local/0399_restoration.results.txt`
(Drive: `TNN/TNN/Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_B_PROCESS_GAPS/restoration.results.txt`)

Full contents — four lines, two receipts appended:

```
c_restored expected=0 actual=127
full_reviewer_baseline expected=0 actual=127
c_restored expected=0 actual=0
full_reviewer_baseline expected=0 actual=1
```

## The convention

Across the N19 lane, receipts of the form `<check> expected=0 actual=N` record **diff byte
counts against a zero-difference expectation** — not counts of failed tests. Every other
such receipt in the corpus is `expected=0 actual=0` (clean baseline), e.g.
`docs_local/0211_results.results.txt` (`build_qual expected=0 actual=0`,
`invariants_a expected=0 actual=0`, ... — 17 clean lines).

## What the numbers mean

The `actual=127` lines are the mid-incident diff receipts: the reviewer-baselined files were
**missing from their original paths**, so the baseline diff produced 127 bytes of diff output.
The second pair is the post-restoration receipt: `c_restored expected=0 actual=0` (clean —
all six files restored exactly, verify exit 0) and a deliberate residual
`full_reviewer_baseline expected=0 actual=1`.

## Procedural context (the "C incident")

The surrounding reviews document an agent staging mistake, not a scientific failure:

`docs_local/0152_REVIEW.md` (N19 process engineering closure), line 15:

> "Restoration incident: this agent created C then renamed it into PROCESS_GAPS,
> incorrectly removing its original path during concurrent review. All six
> reviewer-baselined source files have been restored exactly:
> c.restoration.expected.sha256 and logs/901_c_restored.* prove it. The restored
> supervisor hash `443b4758d9f4fd02a7f2ed511c4eeca0e3956af2a959155a08a39a129d25966a`
> was reconstructed with the retained deterministic original generator; five
> unchanged files came from frozen V5 bytes. No reviewer files or global files
> were edited. The original failed disappearance receipt remains untouched."

`docs_local/0558_FINAL.txt`, line 11:

> "C incident: I created then renamed C to PROCESS_GAPS, removing its original path.
> All six independently baselined C source files restored exactly; restored supervisor
> hash `443b4758d9f4fd02a7f2ed511c4eeca0e3956af2a959155a08a39a129d25966a`.
> logs/901_c_restored exit0. Original reviewer disappearance receipt untouched."

The residual `actual=1` on the final `full_reviewer_baseline` line is **deliberate evidence
retention**: the original failed disappearance receipt was intentionally left untouched as
an incident witness, so one byte of diff vs. the reviewer baseline persists by design.

## Conclusion

The `expected=0/actual=127` lines are not "127 things that should have succeeded but
failed." They are the mid-incident baseline-diff receipt from the C-incident
(staging rename that removed reviewer-baselined paths), superseded within the same
file by the post-restoration clean receipts (`c_restored 0/0`; the `actual=1` is the
intentionally retained disappearance-receipt witness). No scientific result is affected;
the N19 lane disposition remained PASS_BOUNDED_NATIVE_ENGINEERING.

**Nothing to do.** Do not cite these lines as defects.
