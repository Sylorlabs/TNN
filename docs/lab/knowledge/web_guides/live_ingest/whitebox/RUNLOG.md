# WHITEBOX RUNLOG

## 2026-09-24 runlog

- Read all 2226 lines of frozen webg.zag; mapped teach/query/select/verdict cores.
- Verified pins: 872e22a9 (mode prereg freeze) and 59b4efa9 (mode synthesis) both resolve in ~/workspace/selfpam_run/tnn-lab.

## trace runs

- Built webg_trace.zag (additive TRACE on new `tverdict` cmd); frozen vs trace `verdict` output byte-identical; teach outputs+state identical.
- wb_driver.py: 61 fixed cases (A20/B24/P4/A9/K10/Kpara2). Pass1: A 20/20 INSTALL, B 0/24, P 0/4, A9 1/1 INSTALL, K 10/10, Kpara 0/2.
- Pass2 byte-identical (dispositions.tsv + all work/ diff-clean). Exact break: cluster_best byte-equality; all 24 B cases -> all-singleton clusters -> UNCHECKABLE.
- TRACE_REPORT.md written.
