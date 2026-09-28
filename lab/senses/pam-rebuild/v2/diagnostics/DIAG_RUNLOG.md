# DIAG_RUNLOG — diagnostic harness build + self-application (Team 7)

## Build
- 2026-09-23 ~18:06 PDT: substrate copies placed byte-identical from
  `round2/forks/R2-4/src/`:
  `R33_NATIVE_SHA256_V2.zag` sha256
  `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf`,
  `R33_NATIVE_IO_V1.zag` sha256
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`.
- 2026-09-23 ~18:15 PDT: `gen_case_record.py` generated `case_r24_rk3.txt`
  (11,840 trials) + `expect_r24_rk3.txt` from frozen R2-4 evidence
  (read-only). Glue asserts: 11,840 rows in all three sources, seq sets
  identical, RK-3 104/1,102 cross-check.
- 2026-09-23 ~18:19 PDT: `diagnose.zag` written (4 chunks, ~700 lines).
- 2026-09-23 ~18:21 PDT: `znc check` — OK, 3 analyzer warnings (2×A0102
  ignored nio_close return, 1×E0101 `+0`; same class as reference code,
  non-blocking). Native build clean:
  `znc_linux_x86_64_abed8aa1 diagnose.zag -o` → 109,331-byte binary.

## Self-application runs (R2-4 / RK-3)
- Run 1 ~18:22 PDT → `/tmp/diag_report1.txt`, exit 0.
- Run 2, run 3 → reports byte-identical (sha256
  `9ee3bdecdd103181e11e25201f425e1e1d6faba346a04c62f80f33ee142e7b0f`
  all three). DIAG_DONE digest identical:
  `aa037097ad4ae96baf3a2748ffeac0c1939686a5ef555ecce2ccf00ac88c5650`.
- KB-D1..KB-D6 all PASS (see DIAG_VERDICT_R24_RK3.md).

## Instrumentation catch (worth recording)
The harness's K2 (prog==PASS among correct-highconf = 824/1,102) disagreed
with a first Python estimate (826) because the Python used the
pre-deliberation `prog` field while the case record carries the gate's actual
input (`records.txt` prog == post-deliberation `final_prog`; verified 0
mismatches / 11,840). Trials 2366/2372 were deliberation-downgraded
PASS→UNRESOLVED (E2 BLOCK) and correctly land in the never-PASS bucket.
The instrument was right; the hand analysis was wrong — exactly the failure
mode the harness exists to prevent.

## Cleanup
- `.zag-cache/` and `.zagd.semantic-ready` removed before commit (never
  committed per program rule).
- Test binary lived in /tmp only; no binaries committed.
