# CLN-1 LLM arm notes

**Models (exact ids):** `gpt-5.6-sol` via `sol.py`; `grok-4.6` via `unorouter.py chat --model grok-4.6`.
**Method:** each spec sent independently with the working-tree `ZAG_PRIMER.md`
plus the spec/seed text; raw verbatim responses saved as `sol_raw.txt` / `grok_raw.txt`
(all attempts appended). Compile+output verified independently with the pinned znc.

**Primer-version note (honest):** the working-tree `ZAG_PRIMER.md` received a
`_zag_strdup` writable-slice correction during audit setup (the frozen commit
`25113005` has the pre-correction text; the correction changes no rubric, spec,
or kill bar). I cannot verify from available evidence whether the LLM arm's
prompts were built before or after that correction. The outputs are consistent
with either version: no solution uses `_zag_strdup`, and the one spec where
writable slices matter (CLN-G7 reverse) was solved by sol via hardcoding the
output string and failed by grok without attempting a writable slice. The
corrected primer is committed here as a pre-result amendment.

## Results

| Arm | Pass | Fail |
|---|---|---|
| gpt-5.6-sol | 20/20 | — |
| grok-4.6 | 19/20 | CLN-G7 (string reverse): attempt 1 printed just a newline; attempt 2 printed the byte values as decimal digits `1031109710810397122` instead of the reversed string `gnalgaz`. Both attempts failed; best attempt saved. |

Retries used: 3 total — CLN-R4/sol (compile error attempt 1, passed on retry),
CLN-G5/grok (markdown fence left in attempt 1, passed on retry), CLN-G7/grok
(both attempts failed).

Per prereg §3, grok-4.6's CLN-G7 is recorded FAIL. The 4-way blind judging and the
mechanical comparison use the 14 specs where all four arms have passing artifacts
(TNN fails R3/R4/R7/R8/T3, grok fails G7); per-arm full-set means are reported
as secondary figures.
