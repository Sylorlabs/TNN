# SEALED_EVAL_H5R2: sealed evaluation verdict

Lane TNN3H5R, wave-20261001-2321pdt. Evaluator: the lane worker (single
worker acting as coordinator, builder, and evaluator; mitigations frozen
in PREREG_H5R2.md section 5.6). Frozen substrate: tnn3_h5r2.zag at
commit 9db334bd4 (SHA-256
04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a);
frozen binary SHA-256
19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287
(3/3 byte-identical builds). Sealed worlds: TNN3H5R/sealed/ (w_c1,
w_c2, w_w3a, w_w3b), assembled post-implementation from the frozen
driver template; pre-run SHA-256 recorded in SEALED_H5R2.md. Pure Zag
throughout; safebin PATH; `which python3` printed nothing at lane
startup (NAMECHECK.md Step 0); zero forbidden-executable invocations.

## KB-S1 (substrate gate, pre-run): PASS

Verified on the committed file (9db334bd4) before any sealed world was
assembled: `fn t2_prov_ok` defined once; the gate present at all four
t2_trial promote sites (chain f/k, sum ff/c, count f/len-1, single-hop
f/1); the H5R activate tag-20 admission hunk present; zero occurrences
of the promote_graph `ev_teach_in(W,s,r,ans);` shadow-fact call.
NC-0R2 does not fire; the battery ran.

## KB-W0 (white-box, PRIMARY): 36/36 PASS

Across all 36 MAP-key probe snapshots in the C battery (18 in w_c1, 18
in w_c2): zero live tag-1 facts on (s_m,r_m) in all 36 SNAP-IN lines;
every probe returned the f28 of the single live tag-20 MAP with
(f8,f4)==(s_m,r_m) (36 "W0 ok", livemap=1, f28==returned value on every
probe). Zero W0-IN-FAIL, W0-OUT-FAIL, VAL-FAIL, or FRESH-FAIL lines in
either world. The original sin stays corrected under the new gate.
NC-2R2 does not fire.

## C battery (revert worlds)

- KB-W2R: 12/12 PASS. On all 12 probes (8 double-contradiction + 4
  revert), the final dump shows exactly 2 superseded tag-20 MAPs with
  (f8,f4)==(s_m,r_m) carrying CON self-edges, exactly 1 live tag-20 MAP
  with f28 equal to the probe's final expected value, and every DEP
  (type-1) edge of the live MAP targets a live tag-1 non-superseded
  fact. The killed bar now passes: the stale-provenance failure mode is
  gone. Sample (w_c1 C1R1, the exact probe family that killed H5R):
  `C1R1 W2R sup=2 liveid=316`, `W2R dep->254 tag=1 sup=0`,
  `W2R dep->288 tag=1 sup=0` (node 288 is the live reverted fact; the
  superseded original fact is no longer a DEP target). Identical
  structure on C1R2, C2R1, C2R2.
- KB-B2R: 24/24 PASS. On all 8 double-contradiction probes the
  post-first-contradiction probe returned c1 and the
  post-second-contradiction probe returned c2 (16/16); on all 4 revert
  probes the post-contradiction probe returned c1 and the post-revert
  probe returned c0 (8/8), each via a fresh MAP (strictly increasing
  node ids).
- NC-1R2: not fired (MAPCON-ALL=12 in w_c1, 12 in w_c2).
- NC-3R2: not fired (no FRESH-FAIL; every post-contradiction probe
  promoted a fresh MAP).

## W3 battery (provenance-chain worlds)

- KB-W3: 8/8 PASS. On all 8 chained probes (4 in w_w3a, 4 in w_w3b),
  the final dump shows exactly 3 superseded tag-20 MAPs with
  (f8,f4)==(s_m,r_m) carrying CON self-edges, exactly 1 live tag-20 MAP
  with f28==c0 (the reverted value), and every DEP edge targets a live
  tag-1 non-superseded fact. Sample (w_w3a W3A1): `W3A1 W3 sup=3
  liveid=103`, `W3 dep->2 tag=1 sup=0`, `W3 dep->66 tag=1 sup=0` (node
  66 is the live reverted fact after two successive revisions). The
  revert lands on the latest fact after two revisions.
- KB-B3: 24/24 PASS. On all 8 chained probes the post-first-revision
  probe returned c1, the post-second-revision probe returned c2, and
  the post-revert probe returned c0, each via a fresh MAP (strictly
  increasing ids; B3-FRESH-FAIL, B3-C1CON-FAIL, B3-C2CON-FAIL,
  B3-F28-FAIL all zero).

## Architecture and process

- KB-G1R: PASS. Incremental committed diff (verified H5R base ->
  tnn3_h5r2.zag): 13 added cognition lines (non-blank, non-comment; 9
  for the t2_prov_ok helper, 4 modified-in-place gate sites), 4
  removed, net +9; budget <= 15. No new modes, bridges, routers, or
  handlers. No core-ISA additions (only existing field reads, COMPARE,
  and the existing is_superseded predicate). None of the forbidden
  protected semantic operations. No time/clock/random reads.
  Cumulative vs the TNN-2 base (1591 lines): 1587 lines, net -4, still
  net negative. NC-4R2 does not fire.
- KB-D1: PASS. 3/3 byte-identical full-stdout runs per world:
  - w_c1: 76e5794c194b2e6d86e4776322048d6dfd05aac3d3f0c3bc411d6b14c1b673cc (x3)
  - w_c2: 9d227a3a5d3eaf8b463844b2e17be91faf44f2f3c83237c4b72fba197c422685 (x3)
  - w_w3a: 95be21ca740822971596bc40303c3c9fbabb87032caa5ef7e865dbcb36f9b941 (x3)
  - w_w3b: efb5c2cecc63ed0b96fb98ddf8652d528f3ae0f0d7f9851f535e2046743d96c0 (x3)
  NC-5R2 does not fire.
- KB-P1: PASS. Zero forbidden-executable invocations; safebin PATH for
  every command; `which python3` empty at startup and the toolchain
  guard recorded in NAMECHECK.md Step 0.
- NC-6R2: not fired (fresh 83xxx-86xxx ranges; the W3 family is new; no
  trivial variants).
- NC-7R2: not fired. Commit order: prereg dc7df4aba (2026-10-02
  06:30:12 UTC) strictly before implementation 9db334bd4 (06:31:39
  UTC) strictly before world assembly. Base copy SHA-256 matches the
  frozen record. No world output was used to tune the substrate.

## Verdict: H5R2 ADVANCES (BUILD-PASS)

All frozen bars pass; no killing negative control fires; no void
condition fires. Per the frozen verdict rules, H5R2 ADVANCES.

What the evidence says, precisely: the t2_prov_ok provenance gate
corrects the flaw that killed H5R. KB-W2R 12/12 (was 8/12) shows every
revert MAP now anchors DEP edges to live facts; the new KB-W3 8/8 shows
the gate holds across two successive revisions before a revert, with
the revert landing on the latest fact. The behavioral bars (KB-B2R
24/24, KB-B3 24/24) confirm no behavioral regression from declining
dead-lineage candidates, and KB-W0 36/36 confirms the H5R original-sin
correction is preserved. The fix costs 9 net cognition lines, adds no
modes, bridges, handlers, or ISA operations, and leaves the cumulative
architecture diff net negative against the TNN-2 base.

Scope note: this advances the H5R2 hypothesis (provenance carried
forward through revision steps in the trial loop) on the frozen sealed
battery. It establishes no broad generality claim and no L3 claim; the
C and W3 worlds test exactly the preregistered revision-provenance
behavior.
