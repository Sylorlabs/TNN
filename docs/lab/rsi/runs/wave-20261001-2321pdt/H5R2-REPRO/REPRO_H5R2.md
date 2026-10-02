# REPRO_H5R2: independent reproduction of the TNN3H5R H5R2 sealed evaluation

Lane: H5R2-REPRO, wave-20261001-2321pdt. Reproduction worker for the
TNN3H5R lane, which reported BUILD-PASS (H5R2 ADVANCES). This worker
independently extracted every artifact from the recorded commits, rebuilt
the binary from scratch with the pinned znc, and re-ran the full sealed
evaluation 3/3. Pure Zag; safebin PATH; `which python3` printed nothing
(exit 1) at startup (NAMECHECK.md Step 0); zero forbidden-executable
invocations.

Scope: this is a reproduction of a specific sealed battery. It confirms
that the numbers in SEALED_EVAL_H5R2.md were produced by the committed
source and re-execute exactly. It establishes no new generality claim and
no L3 claim; the scope note in the lane's SEALED_EVAL_H5R2.md stands.

## 1. Source extraction (from recorded commits, read-only git show)

- tnn3_h5r2.zag extracted from commit 9db334bd4:
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a
  MATCHES the lane's recorded substrate hash in SEALED_H5R2.md.
- DRIVER_TMPL.zag extracted from commit 9db334bd4:
  f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af
  MATCHES the prereg's frozen template hash (PREREG_H5R2.md section 3).
  Note: the template file is not present in the prereg commit
  dc7df4aba (the prereg was committed alone); its hash is bound in the
  prereg text and the file appears in the implementation commit. This
  matches the prereg ordering rule.

## 2. Independent rebuild (pinned znc, no lane binaries copied)

The pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1 compiled
tnn3_h5r2.zag three times. 3/3 builds byte-identical, SHA-256:

19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287

MATCHES the lane's frozen binary hash bit for bit (the lane's
tnn3_h5r2.bin was never copied or executed; only the newly built
binaries were used). Build log shows only pre-existing A0102
ignored-return-value warnings, no errors.

## 3. Sealed world extraction and integrity (commit e20ba5402)

World files extracted with git show from e20ba5402; pre-run SHA-256
all match SEALED_H5R2.md exactly:

- w_c1.zag 3246e635488c0b7c46d4a0fe41ea267a6777827a9d64333ecf3a869b8defd0e7 MATCH
- w_c2.zag 28831f3b49e6fcf436a4537b0e8d6ae8bfdec15c8703037fce619beb5d88f0b8 MATCH
- w_w3a.zag 3ec3b1631127c4c7ac1758329c32f65661396a11847c2c6b14a59aea65289843 MATCH
- w_w3b.zag 7e69965d4c6a7e86486a370f68bc0e827bd289c076c10a1e4d49e781d5159e41 MATCH

Assembly structure verified independently per the frozen rule: each
world is 1878 lines = 1587 (substrate) + 290 (driver template) + 1
(alias line). Lines 1-1587 of each world are byte-identical to the
extracted committed substrate tnn3_h5r2.zag except line 1353, which is
`fn main()i32 { return sealed_main(); }` (one changed line, as frozen).
The embedded substrate is therefore the exact source that builds the
frozen binary.

## 4. Full sealed re-run, 3/3 runs per world (repro-built world binaries)

Each world file was compiled separately with the pinned znc into its
own binary and run 3 times; full stdout SHA-256 compared to the lane's
KB-D1 record:

| world | repro runs 1/2/3 SHA-256 | lane-reported | match |
|---|---|---|---|
| w_c1 | 76e5794c194b2e6d86e4776322048d6dfd05aac3d3f0c3bc411d6b14c1b673cc (x3) | 76e5794c194b2e6d86e4776322048d6dfd05aac3d3f0c3bc411d6b14c1b673cc | YES |
| w_c2 | 9d227a3a5d3eaf8b463844b2e17be91faf44f2f3c83237c4b72fba197c422685 (x3) | 9d227a3a5d3eaf8b463844b2e17be91faf44f2f3c83237c4b72fba197c422685 | YES |
| w_w3a | 95be21ca740822971596bc40303c3c9fbabb87032caa5ef7e865dbcb36f9b941 (x3) | 95be21ca740822971596bc40303c3c9fbabb87032caa5ef7e865dbcb36f9b941 | YES |
| w_w3b | efb5c2cecc63ed0b96fb98ddf8652d528f3ae0f0d7f9851f535e2046743d96c0 (x3) | efb5c2cecc63ed0b96fb98ddf8652d528f3ae0f0d7f9851f535e2046743d96c0 | YES |

All 12 repro runs are byte-identical within their world and
byte-identical to the lane's reported outputs. Since every number the
lane reported was emitted by these stdout streams, byte equality is the
strongest form of reproduction; the marker-level rescoring below
confirms each bar from the repro outputs directly.

## 5. Bar-by-bar comparison (rescored from repro run outputs)

| bar | lane-reported | repro observed | match |
|---|---|---|---|
| KB-W0 | 36/36 | 36 "W0 ok"; 0 SNAP-IN with t1live nonzero; 0 W0-IN-FAIL/W0-OUT-FAIL/VAL-FAIL/FRESH-FAIL | YES |
| KB-W2R | 12/12 | 12 "W2R ok"; 12 "W2R sup=2"; 0 DEP edges to superseded facts (all dep lines sup=0); sample repro: C1R1 liveid=316 dep->254 tag=1 sup=0, dep->288 tag=1 sup=0 | YES |
| KB-B2R | 24/24 | 16 "B2R ok" (8 double-contradiction probes x 2 answers) + 4 "B3R ok" (4 revert probes x 2 answers each) = 24; 0 Q-line v!=exp mismatches | YES |
| KB-W3 | 8/8 | 8 "W3 ok"; 8 "W3 sup=3"; 0 DEP edges to superseded facts; sample repro: W3A1 liveid=103 dep->2 tag=1 sup=0, dep->66 tag=1 sup=0 | YES |
| KB-B3 | 24/24 | 24 "B3 ok" (12 w_w3a + 12 w_w3b); 0 B3-FRESH-FAIL/B3-C1CON-FAIL/B3-C2CON-FAIL/B3-F28-FAIL | YES |
| KB-D1 | 3/3 byte-identical x4 worlds | section 4 table: all four world hashes match lane report x3 | YES |
| NC-1R2 | not fired (MAPCON-ALL=12 x2) | MAPCON-ALL=12 in w_c1, w_c2, w_w3a, w_w3b; all DONE-OK; 0 FAIL lines anywhere | YES |
| NC-3R2 | not fired | 0 FRESH-FAIL; every post-contradiction probe promoted a fresh MAP (strictly increasing ids on Q lines) | YES |
| NC-5R2 | not fired | section 4 table | YES |
| KB-S1 | PASS | re-verified on the extracted committed file: `fn t2_prov_ok` defined once; gate at all four t2_trial promote sites; H5R activate tag-20 admission hunk present; 0 occurrences of the promote_graph `ev_teach_in(W,s,r,ans);` shadow-fact call | YES |
| KB-G1R | PASS (13 added cognition lines, budget <= 15) | re-verified by diff of extracted substrate against the verified H5R base (commit 830f95ab7 blob d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384): the diff shows the t2_prov_ok helper (9 non-blank non-comment lines) plus the four modified-in-place gate sites; no new modes, bridges, routers, handlers; no core-ISA additions; none of the forbidden protected semantic operations; no time/clock/random reads | YES |

KB-P1: PASS. Safebin PATH for every command; `which python3` empty at
startup and at every check during this reproduction (exit 1); zero
forbidden-executable invocations.

## 6. Prereg commit-order verification (NC-7R2)

`git merge-base --is-ancestor` results:

- dc7df4aba -> 9db334bd4: ANCESTOR (strict; timestamps 06:30:12 ->
  06:31:39 UTC)
- dc7df4aba -> e20ba5402: ANCESTOR (strict; 06:30:12 -> 06:34:48 UTC)
- 9db334bd4 -> e20ba5402: ANCESTOR (strict; 06:31:39 -> 06:34:48 UTC)

Prereg freeze commit strictly precedes implementation, which strictly
precedes sealed evaluation. No ordering violation; no UNVERIFIABLE
ORDERING.

## Verdict: REPRO-PASS

Every number in SEALED_EVAL_H5R2.md reproduces exactly from the
committed sources, the independently rebuilt binary is bit-identical to
the frozen binary (19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287),
all four sealed world outputs are byte-identical to the lane's 3/3 runs,
and the commit order is clean. The lane's BUILD-PASS (H5R2 ADVANCES)
verdict survives independent re-execution.

## Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-REPRO/NAMECHECK.md
  (Step 0 toolchain guard)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-REPRO/REPRO_H5R2.md
  (this file)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-REPRO/JUDGE_BRIEF.md
- lane record (read-only reference):
  docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/
- recorded commits: prereg dc7df4aba1db84e71e3e0b61c84adbf77244e590;
  implementation 9db334bd4a01d21cce52da3bb2a1c45a10c4c172;
  sealed eval e20ba54020dde7e38050dda9e54727d826fc7b45
