# EVAL_SKEPTIC3: sealed evaluation on the two-live-facts separator family

Lane H5R2-SKEPTIC3, wave-20261001-2321pdt. Evaluator: the lane worker.
Implements the frozen protocol in PREREG_SKEPTIC3.md (freeze commit
6bf257048, 2026-10-02 ~07:34 UTC; implementation commit 2affa9bcd,
07:36:48 UTC; ordering clean). Pure Zag; safebin PATH; `which python3`
printed nothing at lane startup and at every check (NAMECHECK.md Step
0); zero forbidden-executable invocations.

## Compared arms

- H5R2 (t2_prov_ok provenance gate): substrate extracted via git show
  from 9db334bd4a01d21cce52da3bb2a1c45a10c4c172, SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a.
- NEWEST-LIVE-ON-KEY (stronger skeptic): substrate extracted via git
  show from f461e812d (bl_newest.zag), SHA-256
  e5df3ddb28858b60efb01f3d8df524a98ce79686e199532e53713c24f367b649.

No working-tree file was used as a build input for either committed
source. Both hashes re-verified at sealed-assembly time.

## World files (assembled post-implementation, per prereg 7.1)

Byte-copy of each arm substrate with the single main line changed
(diff-verified: exactly one line differs), plus the frozen
DRIVER_TMPL.zag appended (SHA-256
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af,
extracted from 9db334bd4), plus SEP_FRAG.zag from the implementation
commit 2affa9bcd (SHA-256
65875ee5ea47dbb0866e9611204739c3d8b3c494f84e1f93d84a1327221447c2),
plus the world alias line. Pre-run SHA-256:

- h5r2_s1.zag 2ce3d5122dfd9ca7e325356f62e2c6779df81a3f59b444d9b4df12d6f2f92245
- h5r2_s2.zag 6f357b6370278df121b4cbb2147101c4fb1a0de4df0f143018af25dcce5ea55b
- bl_newest_s1.zag 0f6532ee88e8c9aa59a6ead4e89e5675bf31750f1dfb40ddac63084e88ebbc0c
- bl_newest_s2.zag 52f0c61bb459b6064a28a249f1869fe41b41974dc39f1e5a66eeeed32541183b

Each world compiled separately with the pinned znc (exit 0, zero
errors, only the pre-existing A0102 warnings); 3/3 runs; full-stdout
SHA-256 (identical across the 3 runs in every world):

- h5r2_s1 04c29441c746f0e216cca0d92e02f06c62b85f2f367907276f89bc420dd862e7
- h5r2_s2 4cd6ceb0571e22fad9a88fdedcc691c43ba2d0cc144e90aec7abbebe9ce8018c
- bl_newest_s1 1766b7ffc3e158e32d2ac3f31324e9343def56c08f3ea26a6f4b5f2c606c58af
- bl_newest_s2 1f1fb027ac0cc7deee47b248e06f960b1b2fc96ea92092a057d8f030d5cdff01

Exit codes: all four worlds exited 1 (all checks passed; the
driver's ok polarity). Every run completed and dumped.

## SC-4 (two-live state): PASS on both arms, all 8 probes

"SEP-TWOLIVE ok" on 8/8 probes per arm. White-box sample (s2 P1, both
arms identical): `S2P1 TWOLIVE n=2 old=3 new=4`: exactly two live
tag-1 non-superseded facts on K=(b,RF2), older id holding c_old
(92407), newer id holding c_new (92408). The re-teach path left two
live facts on one key with no supersession edge, as designed. No
SEP-TWOLIVE-FAIL anywhere; no world VOID. NC-CON-FAIL count 0 on all
worlds (MAPCON-ALL=0: no accidental supersession anywhere).

## Marker scores (run 1; runs 2-3 byte-identical)

Per world: "SEP ok" / "SEP-OLD" / "SEP-NEW" / "SEP-TWOLIVE ok" /
any FAIL-or-MISS line / DONE:

- h5r2_s1: 4 / 4 / 0 / 4 / 0 / DONE-OK
- h5r2_s2: 4 / 4 / 0 / 4 / 0 / DONE-OK
- bl_newest_s1: 4 / 0 / 4 / 4 / 0 / DONE-OK
- bl_newest_s2: 4 / 0 / 4 / 4 / 0 / DONE-OK

Bar totals (8 separator probes: 4 per world):

| bar | H5R2 | NEWEST-LIVE-ON-KEY |
|---|---|---|
| SEP ok (target 8) | 8/8 | 8/8 |
| SEP-OLD (pre-registered H5R2 direction) | 8/8 | 0/8 |
| SEP-NEW (pre-registered skeptic direction) | 0/8 | 8/8 |
| SEP-TWOLIVE ok (target 8) | 8/8 | 8/8 |
| SEP-TWOLIVE-FAIL | 0 | 0 |
| SEP-DEP-FAIL | 0 | 0 |
| SEP-MAP-FAIL | 0 | 0 |
| SEP-VAL-FAIL | 0 | 0 |
| SEP-MISS | 0 | 0 |
| SEP-AB-FAIL | 0 | 0 |

## What each arm shows (white-box, s2 P1)

- H5R2: `S2P1 TWOLIVE n=2 old=3 new=4`,
  `S2P1 Q v=92407 livemap=1 id=14 f28=92407`,
  `S2P1 SEP dep->2 tag=1 o=92301 sup=0`,
  `S2P1 SEP dep->3 tag=1 o=92407 sup=0`,
  `S2P1 SEP-OLD`: the separator MAP anchors DEP edges to the a-link
  fact (id 2) and to F_old (id 3, the OLDER live fact on K,
  object 92407 = c_old). The gate's first verifying candidate in
  node-id order licenses the live-but-not-newest fact.
- NEWEST-LIVE-ON-KEY: `S2P1 TWOLIVE n=2 old=3 new=4`,
  `S2P1 Q v=92408 livemap=1 id=23 f28=92408`,
  `S2P1 SEP dep->2 tag=1 o=92301 sup=0`,
  `S2P1 SEP dep->4 tag=1 o=92408 sup=0`,
  `S2P1 SEP-NEW`: the separator MAP anchors DEP edges to the a-link
  fact (id 2) and to F_new (id 4, the NEWEST live fact on K,
  object 92408 = c_new). The skeptic rejects the F_old-licensed
  candidate and promotes the later-enumerated F_new-licensed one.

Per-probe answers: H5R2 returns c_old on all 8 probes
(91403/91413/91423/91433, 92407/92417/92427/92437); the skeptic
returns c_new on all 8 probes (91404/91414/91424/91434,
92408/92418/92428/92438). The arms' full stdouts differ (unlike the
chained family, where they were byte-identical).

## Frozen kill bars

- SC-1 (DIVERGE, exact pre-registered signature): PASS. H5R2 emits
  SEP-OLD on 8/8 probes; NEWEST-LIVE-ON-KEY emits SEP-NEW on 8/8
  probes. The live MAPs anchor to different facts on K (F_old vs
  F_new) with different answers (c_old vs c_new), exactly as
  pre-registered.
- SC-2 (direction): PASS. H5R2 SEP-OLD count 8 (>= 1); skeptic
  SEP-NEW count 8 (>= 1); neither arm failed outright.
- SC-3 (3/3 byte-identical): PASS for all 4 worlds (one unique
  full-stdout SHA-256 per world across 3 runs).
- SC-4 (two-live state): PASS. SEP-TWOLIVE ok on 8/8 probes on both
  arms; exactly two live tag-1 non-superseded facts on K with
  objects c_old (older) and c_new (newer), white-box verified.

## Verdict: SEPARATED

All four frozen kill bars hold with the exact pre-registered
divergence signature. The gate and the skeptic are finally
discriminated on the named family: t2_prov_ok's first-verifying
candidate in node-id order anchors the re-derived MAP to the older
live teaching (F_old, answer c_old); NEWEST-LIVE-ON-KEY rejects that
candidate and anchors to the newest live teaching (F_new, answer
c_new).

Favored arm (pre-registered): NEWEST-LIVE-ON-KEY. The second teaching
is the teacher's latest statement about K, an update without
contradiction; the protocol's own revision semantics (ev_observe
contradiction leaves the newest fact live and the revert MAP anchors
to it) agrees that current knowledge wins. The gate's oldest-first
pick is a creation-order artifact of forward node-id enumeration,
not a provenance principle: both facts are live and non-superseded,
so the gate's own "a superseded fact licenses nothing" rule does not
discriminate them. On a re-teach, the gate re-derives from stale
knowledge.

Caveat (reported honestly): the world story reads the second teach
as an update/correction. Under a strict monotonic reading (both
teachings are equally live beliefs), neither answer is privileged
and the family merely discriminates the two tie-breaking policies
(creation-order-first vs newest-live). The pre-registered update
reading is the standard belief-revision one and matches the
protocol's own contradiction behavior.

## Negative controls

NC-S0: all 4 worlds are valid assemblies per 7.1 (exactly one line
differs from each arm substrate; hashes recorded pre-run). No arm
VOID. NC-S1: no forbidden-executable invocation (PROCESS-FAIL not
triggered). NC-S2: prereg freeze commit 6bf257048 strictly precedes
implementation commit 2affa9bcd strictly precedes this eval; ordering
clean.

## Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-SKEPTIC3/sealed/
  (4 assembled world sources + 4 compiled world binaries + 12 run
  logs; sub_h5r2.zag, sub_newest.zag, DRIVER_TMPL.zag, SEP_FRAG.zag
  as assembled)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-SKEPTIC3/SEP_FRAG.zag
  (separator fragment, SHA-256
  65875ee5ea47dbb0866e9611204739c3d8b3c494f84e1f93d84a1327221447c2)
- stdout hashes in the table above (run 1 = run 2 = run 3 per world)
