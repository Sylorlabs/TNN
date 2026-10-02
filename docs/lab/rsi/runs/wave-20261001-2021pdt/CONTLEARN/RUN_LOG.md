# RUN_LOG.md: CONTLEARN per-phase results

Wave: wave-20261001-2021pdt. Lane: CONTLEARN. Date: 2026-10-01.
Binary: `cl_driver` (SHA-256
`c8c089b8a0a25f9727719d386aad31fd584a171b3ccbe5ed3bc0b5a72c0e81b7`).
Harness: `run.sh`; spawn/exit record in `harness.log`.
Transcripts: `transcript_<MODE>_r<rep>.txt` (21 total), stderr captures
`stderr_<MODE>_r<rep>.txt` (all 0 bytes).

## Treatment run (TREAT, one process, 149 events, rep 1 shown; reps 2-3 byte-identical)

Event script per prereg section 3 tuples (see the 149-event erratum note in
DRIVER.md; P4 contributes 6 events, total 149).

- P1: 12 TEACH + 12 QUERY. P1_SCORE 12/12.
  Census: N1=12 N20=0 N30=0 N101=0 N102=0 N902=0 E1=0 E12=0 Eall=23.
- P2: 6 TEACH + 6 QUERY. P2_SCORE 6/6. R1C 6 (floor >= 4). T = 0 1 2
  (frozen selection rule: first 3 engaged chains by ascending subject).
  Census: N1=24 N20=6 N30=0 N101=12 N102=12 N902=30 E1=24 E12=6 Eall=95.
  (6 MAPs promoted, each with DEP edges to its 2 licensing facts; 12 SETREG
  cells and 12 guards; 24 literals plus 6 trial frames.)
- P3: 3 OBSERVE + 6 probes. P3_PROBES 6/6. R2C 3 (floor >= 2, |T| = 3).
  Census: N1=30 N20=6 N30=0 N101=12 N102=12 N902=36 E1=27 E12=6 Eall=113.
  (Each contradiction revised its chain's MAP in place: corrected SETREG
  cell with DEP to the contradicted fact, literal holding the new value,
  guard true-target rewired; old answer facts superseded, corrected answer
  facts taught.)
- P4: 3 OBSERVE + 3 QUERY. P4_SCORE 3/3. R3C 3 (floor 3/3). E4_EDGES 33.
  Census: N1=33 N20=6 N30=0 N101=12 N102=12 N902=36 E1=27 E12=6 Eall=125.
  (Fact-level supersede plus reteach; the contradicted P1 facts for i=9..11
  carry CON self-edges; replacements taught with REF edges.)
- P5: 40 TEACH + 40 QUERY. P5_SCORE 40/40.
  Census: N1=73 N20=6 N30=0 N101=12 N102=12 N902=36 E1=27 E12=6 Eall=196.
  (Pure unrelated load: 40 new facts, more than double the P1-P4 structure
  count; no MAP/cell/literal/DEP/SEQ counts moved.)
- P6: 18 probes. R4C 12 (floor >= 10). R5C 6 (floor >= 4).
  Census: N1=73 N20=6 N30=0 N101=12 N102=12 N902=36 E1=27 E12=6 Eall=214.
  (All probes exact-hit; the +18 edges are USE self-edges from exact hits.)

Oracles: R1C=6, R2C=3, R3C=3, R4C=12, R5C=6.
REUSE_COUNT = 30 (ceiling; floor >= 20).
K4A_MISSING 0 (all 33 E4 edges alive at end of run).
K4B_MAPS 6/6. K4C_R4C 12.
K4D: zero lost facts, zero unanswerable chains; no DIAG lines emitted.
UNCERT 0 (every probe designed to hit; none missed).
FNV-1a arena checksum: -1613571771.
AUDIT_PASS (149/149 events through the choke point).

## Control runs (fresh arena each; rep 1 shown; reps 2-3 byte-identical)

- C-P1 (P1 events): P1_SCORE 12/12. UNCERT 0. FNV 1910485975. AUDIT_PASS.
- C-P2 (P1 teaches + P2 events): P2_SCORE 6/6, R1C 6, T = 0 1 2.
  UNCERT 0. FNV -206355851. AUDIT_PASS.
- C-P3 (P1 teaches + P2 events + P3 events): P2_SCORE 6/6, R1C 6,
  T = 0 1 2, P3_PROBES 6/6, R2C 3. UNCERT 0. FNV 828349911. AUDIT_PASS.
- C-P4 (P1 teaches + P4 events): P4_SCORE 3/3, R3C 3. E4_EDGES 0
  (no MAPs exist in this control, so no DEP/SEQ edges; expected).
  UNCERT 0. FNV -1288513866. AUDIT_PASS.
- C-P5 (P5 events): P5_SCORE 40/40. UNCERT 0. FNV 1885019507. AUDIT_PASS.
- C-P6 (P6 probes only): R4C 0, R5C 0. K5B_SCORE 0/18. K5B_N20 0.
  K5B_TAG1_BAD 0 (every tag-1 node has field24 == -999; guide markers only).
  18 DIAG no-fact lines (one per probe; the K4d diagnostic path exercised).
  UNCERT 18 (one per missed probe; expected, since the arena is empty).
  FNV -1942145419. AUDIT_PASS.

## K5a comparison (control per-phase score >= treatment per-phase score)

- P1: C-P1 12/12 vs TREAT 12/12. Equal.
- P2: C-P2 6/6 and R1C 6 vs TREAT 6/6 and R1C 6. Equal.
- P3: C-P3 R2C 3 and probes 6/6 vs TREAT R2C 3 and 6/6. Equal.
- P4: C-P4 3/3 vs TREAT 3/3. Equal.
- P5: C-P5 40/40 vs TREAT 40/40. Equal.

No treatment advantage on any phase; nothing to investigate.

## K6 determinism

SHA-256 of stdout transcripts, 3 reps per mode, all identical:

- TREAT: `53ff2c990e4f7f8d29c8b1bb809cf6616226b9f6bd3dd28d06210dc54446bc44`
- C-P1: `89a1513e31da061821acfa70748ac28c11d36622054251ac96e7446644f48839`
- C-P2: `4ca2c9227e15b4dc0c12bf9f7ef6af368d395b24b602aa509b90226586aed48f`
- C-P3: `4e0115b3e7c595085a83e1ec204ed8d440332e77f94884fdafe108622b5dd1b9`
- C-P4: `51abd456568d5d0a6063c0b8c8fb8a1b289856a6a5622d1c0d26eb350f9de269`
- C-P5: `5f99764724e649bb7f61cf7dcc6106cb4459db6842463b48c162d64e4fd75255`
- C-P6: `218854b0cc91580580aafc86f404bcab6c5df8eba14ceca65ed00756251adc81`

Printed FNV-1a checksums equal across reps within each mode. Exit code 0
on all 21 runs. Zero stderr bytes on all 21 runs. Transcripts contain no
PID, no timestamps, no paths (pid_leak_check=0 in harness.log).
Zero randomness in decision paths (the core has no RNG; z_alloc zero-fills;
all scans are deterministic id-ascending scans).
