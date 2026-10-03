# E6_RUN.md -- Guide-store lifecycle inspector execution report

Wave: wave-20261001-2321pdt, lane BATTERY-E6 (replacement worker).
Prereg: PREREG_E6.md, frozen alone with NAMECHECK.md at commit
58811f3a5, SHA-256
80ea66f7f9cf292b0d15f5b586e968fea280a39d303c1698985a8d5f3c7f87a0
(re-verified unchanged from git at run time: `git diff 58811f3a5`
on the prereg path is empty). Implementation committed after the
freeze at fbe5ab33e (worldgen, inspector, ablator, runner, 5 sealed
worlds; no runs yet). All work pure Zag (pinned znc) and shell under
PATH=$HOME/safebin; no Python invoked. TNN-2 frozen; no source edits.

## Prereg erratum (transparent correction, not a bar change)

PREREG_E6 section 1.1 glosses the POLICY_ROOT index as "i32 at
workspace offset 20". The frozen source's pol_get/pol_set read and
write ng(W,0,20), i.e. node-0 field-20 = workspace offset 84, not
offset 20 (offset 20 is the header allocation counter). The
implementation (e6_inspect.zag, e6_ablate.zag) uses sng(W,0,20),
verified against the frozen pol_get/pol_set. The guide-record
predicate as specified (DEP edge to a live type-30 node plus MEM
edge from POLICY_ROOT) is what governed the tools; the section 4
decision rule never references the offset. No kill bar, signature,
or decision condition is altered by this correction. A smoke test
caught the gloss before the experimental runs; no run executed
under the wrong offset.

## Process bars

- E6-K1 (prereg ordering): PASS. Prereg (+ NAMECHECK.md) committed
  alone (58811f3a5) before implementation (fbe5ab33e) and before any
  run; SHA-256 re-verified unchanged at run time.
- E6-K2 (determinism): PASS. 3/3 byte-identical dumps and
  transcripts per stage (s0..s6), 3/3 byte-identical degenerate
  transcripts, 3/3 byte-identical ablation probe transcripts per
  class (NONE F4 F20 UC PRES).
- E6-K3 (frozen binary): PASS. freeze_shim2_bin and tnn2.zag match
  the section 0 hashes before the first run and after the last run.
- E6-K4 (seal integrity): PASS. All five generated world files
  hash to their prereg section 2 values:
  - e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    e6_s0_world.txt
  - a12acfe5989e04e26ccf505f75b600b0a715ad601ef741593d567530d02888d0
    e6_s1_world.txt
  - 8c0222254050b10cc247418dfecc1424c6dd0326480b413632adad57bc380d87
    e6_act_world.txt
  - e10ac056d807a0d8aea07611dc8b0be6bbaea527554b75fcc330c11f5c4fa920
    e6_s3_world.txt
  - a38bd1ebd64e97ef14a2ef4a26b19ec416aac971bfbc42c00351b8eb616c4f22
    e6_s5_world.txt
- E6-K5 (block calibration): PASS. Degenerate control (ACT on
  empty state) yields CHOICE 0 on all 3 runs; the presence bit
  reads in this id block.
- E6-K6 (no leak): PASS. The E6 id set (95001 95101 95011 95002
  95202 95012) returns zero matches in the frozen cognition sources
  (tnn2_build, core_freeze_tnn2_shim).
- K-C0A (zero new semantic cases): PASS.
  (1) e6_worldgen.zag emits only the exact prereg section 2
  streams via fixed string literals; each of the six ids appears
  exactly twice (the s1 QUERY pair and the s3/s5 OBSERVE lines);
  no id-conditioned or value-conditioned branching exists.
  (2) e6_inspect.zag and e6_ablate.zag contain zero world-id
  literals (grep count 0); guide detection is the structural
  predicate of prereg section 1.1; ablation classes are argv
  strings applied uniformly to all predicate-matching nodes.
  (3) e6_run.sh performs no transcript transformation and no
  logic keyed on world ids, subjects, relations, or CHOICE values
  beyond the byte comparisons required by the prereg section 4
  decision rule and the E6-K5 gate; its single id-literal line is
  the E6-K6 anti-smuggling grep itself (line 45), which scans the
  frozen sources, not the lane.
  (4) grep for python across the lane finds only NAMECHECK.md and
  PREREG_E6.md (toolchain-guard documentation); no invocation
  occurred. `which python3` under the safebin PATH prints nothing
  (NAMECHECK.md Step 0).

## Lifecycle evidence (inspector reports, chain r1; r2/r3 byte-identical)

After guide creation (d1, two QUERY misses):

```
PR 3
GUIDE id=4 f4=95001 f20=30 f24=-999 f28=0 f32=0 uncert=2
GUIDE id=6 f4=95002 f20=30 f24=-999 f28=0 f32=0 uncert=5
UNCERT id=2 f4=-4 f20=95001 f24=95101 f28=2 f32=0
UNCERT id=5 f4=-4 f20=95002 f24=95202 f28=2 f32=0
GUIDES 2 UNCERTS 2
NODES 7 EDGES 5 LOG 2
```

After resolving guide 1 (d3, OBSERVE 95001 95101 95011):

```
PR 3
GUIDE id=4 f4=95001 f20=30 f24=-999 f28=0 f32=0 uncert=2
GUIDE id=6 f4=95002 f20=30 f24=-999 f28=0 f32=0 uncert=5
UNCERT id=2 f4=-4 f20=95001 f24=95101 f28=2 f32=0
UNCERT id=5 f4=-4 f20=95002 f24=95202 f28=2 f32=0
GUIDES 2 UNCERTS 2
NODES 8 EDGES 7 LOG 4
```

The GUIDE/UNCERT lines are byte-identical between d2 and d3 and
between d4 and d5 on all three chains (runner diffs: UNCHANGED on
both resolutions, 3/3 chains). The resolution OBSERVE teaches one
fact node (NODES 7->8->9, EDGES 5->7->9) and advances the log, but
no guide record is retired, updated, unlinked, or aged: every field
of both guide nodes and both uncertainty nodes persists
byte-identical through both resolutions. No overwrite, no aging
counter, no eviction, no retire operator fires. H2c lifecycle
sub-verdict: H2C-STICKY (H2c confirmed as a lifecycle property).

## Behavior across the natural sequence (chain r1; r2/r3 byte-identical)

- s2 (ACT, 2 live guides): CHOICE 30
- s4 (ACT, guide 1 resolved): CHOICE 30
- s6 (ACT, both guides resolved): CHOICE 30
- d (degenerate ACT, empty state): CHOICE 0

Natural invariance N holds: the action is invariant while guide
content varies (two distinguishable contents) and while resolution
state varies (0, 1, 2 resolved guides). The presence bit reads
(0 vs 30); content and resolution do not move the action.

## Read-path evidence (ablation probes on d1, ACT probe world)

| class | mutation | CHOICE (3/3 chains) |
| NONE | byte copy | CHOICE 30 |
| F4 | GUIDE.field4 = 0 (content: subject) | CHOICE 0 |
| F20 | GUIDE.field20 = 0 (action-value field) | CHOICE 0 |
| UC | UNCERT.field20/24/28 = 0 (uncertainty content) | CHOICE 30 |
| PRES | GUIDE.field36 = 0 (presence removal) | CHOICE 0 |

The F4 ablation transcript is byte-identical to the degenerate
empty-state transcript (SHA-256
65d029bf7ad1f390ec4eb4b8ac8a99f9e23a8620c91f922c865841ecf6bd592d,
same as E2-D): zeroing the guide subject makes the guides
unreadable to the ACT path exactly as if no guide existed. The
NONE/UC transcripts are byte-identical to the live-guide ACT
transcript (SHA-256
07837a992456f7afae8d3102a423a2061fa45e595ad8c550bba16add3e25134a).

Established ACT-path reads (prereg section 1.4 operational
definition): the guide node's subject field (F4 flips 30->0) and
the guide node's action-value field (F20 flips 30->0). The
uncertainty node's (subject, relation, marker) content fields are
never observably read by the ACT path (UC: 30->30). The positive
control flips (PRES: 30->0), proving probe sensitivity; the
negative control holds (NONE: 30).

## Decision rule outcome (prereg section 4, frozen)

- ch(F4) = "CHOICE 0" != ch(NONE) = "CHOICE 30" as byte strings,
  replicated 3/3. The SIGNATURE-CONTENT-READ read condition is met.
- ch(UC) == ch(NONE) (uncertainty content unread).
- N holds (c2 == c4 == c6 = "CHOICE 30" on every chain).
- H2c lifecycle: H2C-STICKY.

Signature: SIGNATURE-CONTENT-READ.
Verdict: E6-CONTENT-READ.

Reading: an ACT-path read touches guide content fields (the guide
subject field gates candidacy; the guide action-value field is
emitted as the choice), yet the action does not vary across
naturally differing guide contents or resolution states. Per the
frozen rule this redirects Cluster 2 toward H2d (the bandwidth
hypothesis): the distinguishing uncertainty content
(relation, count, resolution state) has no read path into ACT at
all, and the only content that reaches ACT is the subject tag
(used as a recency gate) plus a construction-constant action value
(30), which the output cannot vary. The sticky lifecycle
(H2C-STICKY) is decided evidence alongside: because no
retire/update operator exists, resolution can never change what
ACT sees, which is why PF-B1's post-resolution ACT stayed 30.

## Evidence paths

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E6/PREREG_E6.md
- Tools: e6_worldgen.zag, e6_inspect.zag, e6_ablate.zag (+ _bin),
  e6_run.sh
- Worlds and manifest: e6_worlds/ (E6_MANIFEST.sha256)
- Dumps, transcripts, reports: e6_runs/ (per-chain per-stage
  .bin/.trans, e6_rep*.txt, E6_EVIDENCE_SHA256.txt)
- Per-run SHA-256: e6_runs/E6_EVIDENCE_SHA256.txt
