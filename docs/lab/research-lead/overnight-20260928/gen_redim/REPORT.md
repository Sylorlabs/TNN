# REPORT: GEN-REDIM -- Dynamic Arena Re-dimensioning

Worker: gen-redim. Date: 2026-10-03. Branch: lane-genredim-20261003.
Governs: PREREG.md (commit e5709c139, strictly before implementation).

## 1. Verdict

**PASS (exploratory).** C1-C11 all PASS. GEN-REDIM executes the frozen GEN
rules faithfully at NM=2,3,4,6,8: the frozen nm<=4 batteries are
byte-identical to the frozen artifact, and S1-S5 behave per the original
predictions (S2 per the preregistered corrected trace).

The PASS is labeled **exploratory**, not canonical: during lane setup the
worker invoked `python3 -c "print('no')"` as a stray keystroke (see
INCIDENT.md). The invocation performed no research computation, consumed
no inputs, and produced nothing used by the work; it is self-disclosed
per the toolchain guard, which makes this wave PROCESS-FAIL by rule. The
build pipeline (build.sh) re-verifies every digest, byte-identity claim,
and kill bar from the committed sources alone, so an untainted worker
re-running build.sh from the committed prereg + sources constitutes the
clean reproduction required before canonical promotion.

## 2. What was built

GEN-REDIM = the frozen GEN composer with a dynamic, NM-parameterized
scratch layout (PREREG.md Section 2). NM is stored at arena offset 772;
every region after the MAP table is placed by exact size chaining. The
MAP table keeps base 776, stride 40. At NM=4 every frozen offset is
reproduced exactly (tries=936, m2g=968, V=1024, tried1=2304, t2c=3328,
nv=3588, vs=3596, done=3660); the allocation shrinks to 3724 bytes
(all accesses verified below it).

Files (all in this lane):
- ref_rd_base.zag, ref_rd_gen.zag, ref_gs_new.zag: byte-copies of the
  GEN-STRESS frozen files (digests verified in build.sh Step 1; cmp
  against ../gen_stress/ in Step 2).
- rbase.zag: ref + Section 2 accessor fns (r_nm..r_dn, r_vp_nm,
  r_size_nm) + world_new_nm + m2g/m2p rebase + layout comments.
- rgen.zag: ref + the Section 3 literal->accessor substitutions +
  old-main world_new_nm updates.
- rd_dmain.zag / rd_gmain.zag / rd_smain.zag: drivers (mains only;
  setups live in rbase.zag / are byte-exact extracts).
- build.sh: the full fail-closed pipeline (digest checks, C10/C11
  audits, assembly, compile, 3x runs, expected-block extraction from
  PREREG.md, section comparisons, S5 counts).

## 3. Kill-bar results

| Bar | Result | Evidence |
|-----|--------|----------|
| C1 COMMIT-ORDER | PASS | PREREG.md+NAMECHECK.md committed alone as e5709c139; implementation committed after (see Sec 6). |
| C2 DETERMINISM | PASS | 3/3 runs pairwise byte-identical (cmp), stderr empty, for all five binaries. Output sha256: fz_dbin=rd_dbin 37d22e2a..; fz_gbin=rd_gbin d12645a2..; rd_sbin 25a6acdc... |
| C3 DIAMOND-REGRESSION | PASS | rd_dbin stdout byte-identical to the frozen-regenerated baseline (cmp, empty diff). |
| C4 GENERALITY-REGRESSION | PASS | rd_gbin stdout byte-identical to the frozen-regenerated baseline (cmp, empty diff). |
| C5 STRESS-S1 | PASS | Section byte-identical to PREREG exp-S1: ANS=2, TRIES=29, no WIDEN. |
| C6 STRESS-S2 | PASS | Section byte-identical to the PREREG Section 6 corrected exp-S2: ANS=219, TRIES=43, no WIDEN. |
| C7 STRESS-S3 | PASS | Section byte-identical to PREREG exp-S3: WIDEN=1 (exactly once), ANS=207, TRIES=8. |
| C8 STRESS-S4 | PASS | Section byte-identical to PREREG exp-S4: ANS=-2, TRIES=48, zero WIDEN=1 lines. |
| C9 STRESS-S5 | PASS | ARM line exactly `ARM=GEN PROB=S5 ANS=-2 TRIES=2734`; 3 INTER= lines; 2731 INTER2= lines; 0 WIDEN=1 lines. |
| C10 MINIMAL-DIFF | PASS | build.sh Step 3 allowlist audit: base diff 52 changed lines, gen diff 122 changed lines, every added/removed line matches the authorized classes (accessor defs, r_* calls, world_new_nm, layout comments; scratch literals / old defs removed). |
| C11 OPACITY | PASS | build.sh Step 4: no banned tokens in built sources, PREREG.md, or this REPORT outside the PREREG Section 4 definitional list. |

Binary sha256 (pinned znc 2026.07.0-dev):
- rd_dbin 8a88af16e232047940ea6fe7de514a8c9eeedab85820292af8b18dcc80858e45
- rd_gbin aad5e969a2ad4fd0ca186f0208649cdb86e6a36baf9adb700af1286009a7499a
- rd_sbin ef6ee431ae2eae2bf864edcd0d7866949e598b090841d04a83721eb71997ae98

## 4. The S2 correction, confirmed empirically

GEN-STRESS's S2 block (ANS=219, TRIES=48) contained four hand-derivation
errors against the frozen rules (PREREG.md Section 6, E1-E4: phantom
kind-rejected tries in R3/R4, wrong R4 pool order, 50 lines vs TRIES=48).
The preregistered corrected block (ANS=219, TRIES=43) is what the binary
prints, byte for byte. The trace follows the rules exactly: kind-1-only
admission for m2/m4, id-ordered 2-input MAPs (m3's pairs before m5's),
lex pair order, rejected-not-tried. S2 now PASSES as originally
predicted (a 6-structure DAG resolving to 219); the frozen artifact had
printed ANS=-2 TRIES=62 with spurious WIDEN=1 (arena corruption).

## 5. Design note: the allocation invariant

During verification, an initial build allocated the generality worlds
with world_new_nm(2) while the setups define 4 MAPs; map_new for m2/m3
then wrote over the TRIES/FOUND/ANS counters (C4 caught it: one extra
INTER2=-2, TRIES=7 vs 6). The frozen setups define up to 4 MAPs while
some queries run fewer; the frozen 4-slot table absorbed this harmlessly.
The invariant, now specified: world_new_nm(nm) must satisfy
nm >= (number of MAPs the setup defines); the query's active count
(gen_solve's nm) may be smaller. All batteries satisfy this (P1: 2/2;
P2a/b/P3 and diamond: 4/4; S1: 6/6; S2: 6/6; S3: 3/3; S4: 8/7;
S5: 4/4). The drivers were corrected to the PREREG-specified values
(rd_gmain.zag: P1 nm=2, P2a/P2b/P3 nm=4); no PREREG change was needed.

## 6. Commit record

- e5709c139 GEN-REDIM prereg (frozen): NAMECHECK.md + PREREG.md only.
- (this commit) implementation: INCIDENT.md, build.sh, rbase.zag,
  rgen.zag, rd_dmain.zag, rd_gmain.zag, rd_smain.zag, ref_*.zag,
  subst.sed, build logs and run outputs, this REPORT.md.

## 7. Boundaries and follow-ups

- The pre-declared boundaries (PREREG.md Section 10) stand: installed
  MAPs, expected-answer verification, one generic 2-input class,
  unchanged 64/64/64/6-round resource bounds, NM>8 not exercised,
  WIDEN semantics unchanged (S3's contract-violating success is
  reproduced exactly, as characterized by GEN-STRESS).
- The addressable limit is now ARENASZ(NM), not 4. The 5/10+
  structure-combination question is unblocked at the arena level.
- Recommended follow-up: the clean reproduction (untainted worker
  re-runs build.sh from the committed sources) to lift the
  exploratory label; then NM=10+ batteries for the 10+ structure
  question.
