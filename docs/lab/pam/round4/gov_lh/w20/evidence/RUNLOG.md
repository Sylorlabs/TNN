# W20 GOV-LH RUNLOG (resume after daemon restart — 2026-09-24 ~15:35 PDT)

## Inherited state (verified 2026-09-24 by resume agent)
- PREREG freeze commit: c564e6e8a99b29a2005c6447a95566c34726bba3 (2026-09-24T22:16:28Z),
  adds EXACTLY ONE file docs/lab/pam/round4/gov_lh/w20/PREREG_W20_GOVLH.md,
  remote sha256 0caa9803...f4793f MATCHES local byte-for-byte.
- Build integrity: w20gov_R.zag vs w20gov_K.zag differ in exactly line 1559
  (the prereg-specified one-line R-AUTH change). §6.0: BOTH sources rebuilt
  with pinned znc (~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1)
  from within build/ cwd — fresh binaries reproduce committed evidence
  w20_run1.txt / w20_zerodecl1.txt BYTE-IDENTICALLY (run + zerodecl), and match
  the predecessor's integrity_R/K_run/zerodecl.out outputs. Binaries sound.
- Battery tapes (tapes_s1/s10/s100): 117 rows/shard, manifest (producer,decl)
  consistent with tape fields, SHASUMS.txt verified. Predecessor's tapes are
  adopted as-is (deterministic generator output; no need to re-generate).
- Scorer (score/score_w20gov.py) reviewed: matches frozen prereg §2.5
  attribution, §3 kill bars, §5 enumeration. legs.sh reviewed: correct
  invocation (BIN 20 <mode> <tape> <probes> <corpus>).

## Leg runs

## Coordinator completion (2026-09-24 ~16:45 PDT, after 6th daemon restart)

- Scoring crew killed by restart; coordinator ran the frozen scorer
  unmodified: `score/score_w20gov.py evidence/legs_s{1,10,100}
  evidence/tapes_s{1,10,100}` → SCORE_REPORT_s{1,10,100}.json.
- Adjudicated per frozen prereg §3 kill bars; wrote VERDICT_GOVLH_W20.md.
- No new legs run; no prereg amendment; no binaries committed.
