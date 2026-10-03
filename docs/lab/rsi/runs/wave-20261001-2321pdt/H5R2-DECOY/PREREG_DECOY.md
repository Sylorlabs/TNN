# FROZEN PREREG: H5R2-DECOY, the discriminating world the baseline battery lacked

Lane: H5R2-DECOY, wave-20261001-2321pdt. Status: FROZEN PREREG.

Lineage: H5R2-BASELINE reached BASELINE-MATCHES via baseline (a)
REVERT-TO-LATEST (EVAL_BASELINE.md): the recency heuristic matches the
t2_prov_ok provenance gate on all five bars of the four sealed worlds
w_c1, w_c2, w_w3a, w_w3b. The battery cannot discriminate the gate from
recency. The lane named the missing discriminating world: one where
the NEWEST fact is NOT the LIVE one. This lane builds it.

ORDERING RULE: this prereg is committed (with NAMECHECK.md) before any
implementation file is written. Any decoy artifact whose mtime predates
the prereg freeze commit is UNVERIFIABLE ORDERING and the comparison is
VOID. Kill bars never move after freezing.

## 1. Question under test

Is the t2_prov_ok provenance gate necessary, or does the recency
heuristic explain H5R2's sealed results? The discriminating world
family: after a revert sequence on key K=(b,RF2), a decoy OBSERVE
teaches a NEW fact on an UNRELATED key K2=(b,RD) (newer creation
timestamp, live, but irrelevant to K's revert). A further probe on K
requires the revert MAP to anchor its DEP edges to K's live (older)
fact, not the decoy.

Mechanism (verified against the committed H5R2 source before freezing):
t2_gather enumerates chain paths from the query subject in node-id
order, so for the revert query the len-3 candidates are, in order:
[a,b,c0 via stale original fact], [a,b,c1 via superseded c1 fact],
[a,b,c0 via live reverted fact], [a,b,c0 via decoy fact]. H5R2 tries
them forward and the gate declines the superseded lineages, promoting
the live-reverted-fact candidate. REVERT-TO-LATEST tries them in
reverse and promotes the decoy-licensed candidate first. The decoy
candidate verifies because the chain graph is built from value
literals and executes to c0. Hence the predicted failure signature:
the live revert MAP carries a DEP edge to the decoy fact.

## 2. Compared arms (sources extracted read-only from recorded commits)

- H5R2: source extracted via git show from
  9db334bd4a01d21cce52da3bb2a1c45a10c4c172, SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a
  (must match before use).
- (a) REVERT-TO-LATEST, (b) NO-GATE, (c) RANDOM-ANCHOR: sources
  extracted via git show from 1203b865d352ae8ba380f57350218edd4d637b3a
  (bl_latest.zag, bl_nogate.zag, bl_random.zag); SHA-256 recorded at
  extraction and checked before world assembly. Do NOT rebuild from
  working files.

## 3. Decoy world family (frozen spec)

Per decoy probe (tag DiPj), with chain relations RF1/RF2, MAP relation
RM, decoy relation RD, all fresh per world:

1. ev_teach(a,RF1,b); ev_teach(b,RF2,c0).
2. QUERY(a,RM,c0): promote MAP1 (probe P1, full h5r2_probe protocol).
3. ev_observe(b,RF2,c1): contradiction.
4. QUERY(a,RM,c1): promote MAP2 (probe P2).
5. ev_observe(b,RF2,c0): REVERT, teaches the new live fact on K.
6. ev_observe(b,RD,c0): DECOY, teaches a NEW live fact on the unrelated
   key K2=(b,RD). Newer than the reverted fact, live, non-superseded.
7. Decoy answerability: QUERY(b,RD,c0) must return c0 (D-ANS check).
   The K2 fact is itself answerable correctly; the world is not
   adversarial by brokenness.
8. QUERY(a,RM,c0): promote MAP3, the revert MAP (probe P3).
9. White-box D-check on the live MAP (section 4).

Frozen constraints: no OBSERVE on any MAP key; per-probe (subject,
relation) ranges disjoint within each world; key ranges 87xxx-88xxx,
disjoint from FW1-FW9 (3xxxx), the 1421pdt battery (43xxx), the killed
H5 battery (51xxx-54xxx), the killed H5R battery (61xxx-65xxx,
71xxx-72xxx), the H5R2 sealed battery (83xxx-86xxx), and all smoke keys.

### Seeds (frozen before implementation; SHA-256 inputs recorded here)

- d1: "TNN3H5R2|wave-20261001-2321pdt|decoy1" -> f456 -> s5=62550, vo5=5
- d2: "TNN3H5R2|wave-20261001-2321pdt|decoy2" -> 7900 -> s6=30976, vo6=1
First 4 hex digits of each SHA-256 digest as the seed integer; value
offset = seed mod 7.

### World d1 (chain relations 8701/8702, MAP relation 8703, decoy 8704)

- D1P1: a=87101 b=87301 c0=87406 c1=87407
- D1P2: a=87102 b=87302 c0=87416 c1=87417
- D1P3: a=87103 b=87303 c0=87426 c1=87427
- D1P4: a=87104 b=87304 c0=87436 c1=87437

### World d2 (chain relations 8801/8802, MAP relation 8803, decoy 8804)

Materially different relation family and subject distribution from d1.

- D2P1: a=88101 b=88301 c0=88402 c1=88403
- D2P2: a=88102 b=88302 c0=88412 c1=88413
- D2P3: a=88103 b=88303 c0=88422 c1=88423
- D2P4: a=88104 b=88304 c0=88432 c1=88433

8 decoy probes total (N=8, satisfies N>=8).

## 4. The D-check (frozen white-box bar, per probe)

On the live MAP for (a,RM) after step 8, with the decoy fact id found
as the single live tag-1 fact on (b,RD) and the K-live fact id found as
the single live tag-1 fact on (b,RF2):

- exactly 2 superseded MAPs on (a,RM); exactly 1 live MAP with f28==c0
  (else D-SUP-FAIL / D-LIVE-FAIL / D-F28-FAIL);
- every DEP (type-1) edge target of the live MAP is live tag-1
  non-superseded (else D-DEP-FAIL);
- no DEP edge target is the decoy fact (else D-DECOY-FAIL; this is the
  pre-registered recency failure signature);
- at least one DEP edge target is the live fact on K=(b,RF2) (else
  D-KEY-FAIL: wrong-key anchor).

"D ok" is emitted only if all conjuncts pass. Value checks (VAL-FAIL,
FRESH-FAIL via h5r2_probe) are scored separately and reported.

## 5. Frozen kill bars

DB-1 (gate necessity, H5R2): H5R2 emits "D ok" on 8/8 decoy probes:
every revert MAP anchors DEP edges to live tag-1 non-superseded facts
on the K lineage, never the decoy, never a superseded fact.

DB-2 (predicted recency failure): REVERT-TO-LATEST emits D-DECOY-FAIL
(DEP edge to the decoy fact, the pre-registered failure signature) on
a frozen majority (>=5/8) of decoy probes. Expected: 8/8.

DB-3 (controls behave as in the baseline lane): NO-GATE scores 0/8 on
the D-check, failing via D-DEP-FAIL (DEP edge to the superseded
original fact, its baseline-lane failure mode); RANDOM-ANCHOR does not
reach 8/8 on the D-check (chance-level anchoring, expected about 1/3
per probe).

DB-4 (determinism): 3/3 byte-identical full-stdout runs per arm per
world, SHA-256 compared (the KB-D1 protocol).

DB-5 (decoy genuineness): the D-ANS check passes on all 8 probes on all
4 arms. Any D-ANS failure makes the affected world VOID as
adversarial-by-brokenness.

Verdict DECOY-DISCRIMINATES iff DB-1 and DB-2 and DB-3 and DB-4 and
DB-5 all hold: the gate is necessary, recency fails as predicted.
Verdict DECOY-NOT-DISCRIMINATING otherwise, with the exact per-arm
per-bar numbers reported honestly. Either outcome is informative.

## 6. Pre-registered expectations (not kill bars; recorded for honesty)

- H5R2: 8/8 "D ok"; value answers correct on all probes.
- REVERT-TO-LATEST: 0/8 "D ok", 8/8 D-DECOY-FAIL; value answers still
  correct (the decoy-licensed MAP returns c0), so the failure is
  provenance-only, exactly like NO-GATE's failure was in the baseline
  lane. This is the point: answers do not discriminate; DEP edges do.
- NO-GATE: 0/8 "D ok" via D-DEP-FAIL to the superseded original fact.
- RANDOM-ANCHOR: about 2-3/8 "D ok" (one of three verifying candidates
  is the correct one: stale, live, decoy).

## 7. Worlds and evaluation protocol (frozen)

7.1. Assembly per arm, after the implementation commit, by the frozen
rule: byte-copy of the arm substrate with the single line
`fn main()i32 { return run_all(); }` changed to
`fn main()i32 { return sealed_main(); }` (verified by diff: exactly
one line differs), plus the frozen DRIVER_TMPL.zag appended (SHA-256
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af,
extracted from 9db334bd4), plus the frozen DECOY_FRAG.zag appended
(decoy probe functions and sealed_main_d1/sealed_main_d2; SHA-256
recorded before assembly), plus one alias line selecting the world
(`fn sealed_main()i32 { return sealed_main_d1(); }`, etc.).

7.2. World file SHA-256s recorded before any run. Each world compiled
separately with the pinned znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1); 3/3 runs; full-stdout
SHA-256 compared per world (DB-4).

7.3. Scoring uses the driver's own markers: "D ok" (target 8: 4 per
world), "D-ANS ok" (target 8), "D-DECOY-FAIL" / "D-DEP-FAIL" /
"D-KEY-FAIL" / "D-SUP-FAIL" / "D-LIVE-FAIL" / "D-F28-FAIL" counts, and
zero unexpected FAIL marker lines. The canonical full state dump ends
each world for DB-4.

7.4. Negative controls: NC-D0 (a world file is not a valid assembly
per 7.1: that arm is VOID, not scored); NC-D1 (any
forbidden-executable invocation: PROCESS-FAIL, terminal); NC-D2
(prereg freeze does not strictly precede implementation: UNVERIFIABLE
ORDERING, VOID).

## 8. Pure-Zag construction

Builder PATH is $HOME/safebin (36 tools, no python3, verified at lane
startup and recorded in NAMECHECK.md Step 0). All research logic is
Zag compiled/run with the pinned znc. Shell is used only to invoke
znc, run binaries, do git ops, and move/copy files.

## 9. Documentation

No em-dashes in any lane documentation. Every doc is checked with
sh docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
before commit.
