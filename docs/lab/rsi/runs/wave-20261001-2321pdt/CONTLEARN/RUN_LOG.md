# RUN_LOG: CONTLEARN learner-ownership probe execution

Wave: wave-20261001-2321pdt. Lane: CONTLEARN. Date: 2026-10-01.
Binary: `lo_driver`
(`35f78f8c3eb6fce9dec2262875f8cb1cb0efef1f7cffa824bdfaebb9a7a0ac4a`).

## Runs (K1a/K1c)

Harness `run.sh`: 2 modes x 3 reps = 6 learner processes. Each run launched
via `printf '%s' "$mode" | bash -c 'exec -c ./lo_driver'` (empty argv, empty
env). harness.log records: 6 spawns total (3 TREAT, 3 NOSTORE), all exit 0,
zero stderr bytes on all 6 runs, pid_leak_check=0 (no PID appears in any
transcript), znc_invocations.log holds exactly 1 entry throughout.

## K6 determinism

- TREAT stdout SHA-256 (3/3 identical):
  `1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9`
- NOSTORE stdout SHA-256 (3/3 identical):
  `839e66149ffc1f455d661452d860981adb1f846ade28b4638469b8c0e949a920`
- FNV-1a arena checksums equal across reps: TREAT 1570275895, NOSTORE
  -2062244938. Exit code 0 on all 6 runs. Zero stderr bytes.

## K3 no-regression (2021pdt battery, read-only re-run)

Committed 2021pdt binary `cl_driver`
(`c8c089b8a0a25f9727719d386aad31fd584a171b3ccbe5ed3bc0b5a72c0e81b7`)
re-run 3x in TREAT mode, read-only. Stdout SHA-256 on all 3 reps:
`53ff2c990e4f7f8d29c8b1bb809cf6616226b9f6bd3dd28d06210dc54446bc44`,
matching the 2021pdt RUN_LOG.md value. Transcript lines: R1C 6, R2C 3,
R3C 3, R4C 12, R5C 6, REUSE_COUNT 30, AUDIT_PASS. Zero stderr bytes.

## K4 probe results (TREAT, identical on all 3 reps)

- K4A_STOREOK 13/13. All 13 masked STORE queries promoted MAPs with alive
  DEP edges to their licensing facts: 7x map(6001+i,202) -> fact(5001+i,
  101,5101+i), 6x map(8001+i,402) -> fact(7001+i,301,7101+i). No answer key
  was supplied on any query (every query line reads `EV 2 <s> <r> -2 MK`).
- K4B_REUSEOK 20/20. All 20 masked REUSE probes returned the stored values
  with the content-expected live fact as the serving node: 7x 5101+i on
  (5001+i,101), 7x 5101+i on (6001+i,202), 6x 7101+i on (8001+i,402).
- K4C_R2ORIG 0/20, K4C_R2NEWV 20/20. After the 13 ABLATE contradicts
  (transcript shows `rv=0` contradiction returns), zero masked REUSE2 probes
  return original stored values, and all 20 return the post-ablation values
  (9901+i on families A/B, 9801+i on family C). The family-B corrected
  values 9901+i can only exist via `t2_revise_graph`'s corrected reteach,
  confirming the in-arena deletion path (supersede marks plus MAP-cell
  tombstone/revision) fired as designed.
- K4D (NOSTORE): K4D_MISS 20/20, K4D_UNCERT 20. All 20 masked probes on the
  fresh arena took the true miss path (returned -2); exactly 20 UNCERTAINTY
  (tag 30) nodes in the final arena.

## K5 machinery sanity

TREAT UNCERT (tag 30) node count = 0 on all 3 reps: no true miss anywhere
in the treatment run (every STORE masked query promoted, every REUSE/REUSE2
probe exact-hit). Final alive node census (REUSE2): N1=59, N20=13, N30=0,
N101=26, N102=26, N902=79; well below the 1024-node cap, so no eviction.

## Per-phase census (TREAT r1; identical across reps)

- CENSUS STORE: N1=39 N20=13 N30=0 N101=26 N102=26 N902=65 E1=52 E12=13
  Eall=154. (39 = 26 teaches + 13 promoted answer facts; 13 MAPs.)
- CENSUS REUSE: N1=39 N20=13 N30=0 (exact-hits add no nodes).
- CENSUS ABLATE: N1=59 N20=13 N30=0 N101=26 N102=26 N902=79 E1=59 Eall=233.
  (13 reteaches + 7 corrected answer facts; stale cells tombstoned, MAPs
  alive with updated answer fields.)
- CENSUS REUSE2: N1=59 N20=13 N30=0 (exact-hits add no nodes).

## K0 commit order

Prereg committed alone at 408ffdcdc. `git merge-base --is-ancestor
408ffdcdc HEAD` true at verdict time. All implementation and result files
first appear strictly after the prereg commit.
