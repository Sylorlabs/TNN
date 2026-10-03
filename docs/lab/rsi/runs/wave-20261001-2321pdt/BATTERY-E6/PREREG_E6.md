# PREREG_E6.md -- Guide-store lifecycle inspector (tests H2c within Cluster 2)

Wave: wave-20261001-2321pdt, lane BATTERY-E6 (replacement worker).
Status: FROZEN DESIGN. This file is committed alone (with NAMECHECK.md)
before any E6 world is generated, any tool is built, or any run executes.
Kill bars never move after freezing.

## 0. Freeze record and provenance

E6 is the sixth-priority discriminating experiment from the
BATTERY-CLUSTER analysis
(docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-CLUSTER/CLUSTER_ANALYSIS.md),
testing H2c (sticky guide lifecycle: guides are append-only, no
update/retire operator exists) within Cluster 2 (GUIDE CONTENT
DECOUPLING, "the presence bit"). E2 (E2-CONTENT-BLIND, lane BATTERY-E2)
confirmed H2a (absent content channel at the guide-to-ACT interface)
as Cluster 2's root cause and killed H2b (concurrency collapse). The
remaining within-cluster hypotheses are H2c and H2d. E6 inspects what
the frozen TNN-2 binary actually does with guide records over time:
which records are written, which fields are populated, whether records
are overwritten, aged, evicted, or retired on resolution, and whether
any ACT-path read touches the content fields.

Runs target the frozen TNN-2 binary, no source edits:

- `tnn2.zag` SHA-256:
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
- `freeze_shim2_bin` SHA-256:
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
- Pinned znc SHA-256:
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

Binary hashes are verified before the first run and after the last
(E6-K3). Frozen sources are read-only; the anti-smuggling grep
(E6-K6) runs before execution. The state file is the raw 110656-byte
workspace dump (no checksum); the shim loads and stores it verbatim,
so external staged dumps and field-level ablation are possible with
no source modification.

## 1. Inspector design (pure Zag, external probe)

Two pure-Zag tools, built only after this prereg freezes. Both use
the frozen workspace layout (header 64 bytes; nodes 1024 x 40 bytes
at 64+n*40; edges 4096 x 16 bytes at 41024+e*16; log 128 x 32 bytes
at 106560) with the u8-cell ig/put32 accessor idiom. Neither tool
contains any world-id literal (K-C0A).

### 1.1 Guide-record predicate (structural, id-free)

Let pr = i32 at workspace offset 20 (the POLICY_ROOT node index).

- Node n (2 <= n < 1024) is a GUIDE iff: live (field36 == 1) AND
  node type (field0) == 1 AND there exists an edge e with
  from(e)==n, type(e)==1 (DEP), to(e)==u where u is live and node
  type(u)==30, AND there exists an edge e2 with from(e2)==pr,
  type(e2)==10 (MEM), to(e2)==n.
- Node u is an UNCERTAINTY iff live and node type(u)==30.

This predicate mirrors the frozen miss_inquire constructor (guide:
type-1 node, DEP edge to a type-30 UNCERTAINTY node, MEM edge from
POLICY_ROOT) without naming any id.

### 1.2 Field classification (frozen per this prereg)

For a GUIDE node g with DEP-linked UNCERTAINTY node u:

- Guide content fields: g.field4 (guide subject, identifies which
  uncertainty), u.field20 (uncertainty subject), u.field24
  (uncertainty relation), u.field28 (uncertainty state marker).
- Guide action field: g.field20 (the emitted choice value written
  at construction). Reported separately; not a content field.
- Routing/filler: g.field24, u.field4, liveness field36, edges.

### 1.3 e6_inspect.zag

Usage: e6_inspect_bin <state.bin>. Read-only. Emits a canonical
report, node ids ascending:

```
PR <pr>
GUIDE id=<n> f4=<v> f20=<v> f24=<v> f28=<v> f32=<v> uncert=<u>
UNCERT id=<u> f4=<v> f20=<v> f24=<v> f28=<v> f32=<v>
NODES <live-count> EDGES <live-count> LOG <count>
```

The GUIDE/UNCERT lines are the lifecycle evidence: diffing them
across staged dumps shows exactly which guide records and fields
survive, change, or vanish.

### 1.4 e6_ablate.zag

Usage: e6_ablate_bin <in-state.bin> <class> <out-state.bin>.
Applies one mutation class to every predicate-matching node,
writes the mutated dump. Classes (argv string match only):

- NONE: byte-identical copy (negative control; validates copy/reload).
- F4: set GUIDE.field4 = 0 on all guides (content field: subject).
- F20: set GUIDE.field20 = 0 on all guides (action-value field).
- UC: set UNCERT.field20 = 0, field24 = 0, field28 = 0 on all
  uncertainty nodes (the (subject, relation) uncertainty content).
- PRES: set GUIDE.field36 = 0 on all guides (positive control:
  presence removal must move the observation).

The runner then runs the single-ACT probe world on each mutated
dump. An ACT-path read is ESTABLISHED for a field iff mutating it
changes the probe's CHOICE line versus the NONE control, replicated
3/3. Recorded limitation: ablation detects reads with an observable
effect on the CHOICE line; a read with no observable effect is not
detectable by any external probe, so the signatures below are
operational on observable reads.

## 2. Guide-event sequence (fresh sealed worlds)

The frozen binary exposes exactly one guide constructor
(miss_inquire on a true miss), so "multiple guide types" here means
two guides with distinguishable (subject, relation) content observed
across three lifecycle phases (both live, one resolved, both
resolved). Id block 95000-95999: the six ids below return zero
matches in the frozen cognition sources (verified pre-freeze) and
zero matches in the wave run dirs.

Exact world streams (byte-exact; hashes pinned before any run):

e6_s0_world.txt (empty, init baseline):
SHA-256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

e6_s1_world.txt (create two guides, distinguishable content):
```
QUERY 95001 95101 95011
QUERY 95002 95202 95012
```
SHA-256 a12acfe5989e04e26ccf505f75b600b0a715ad601ef741593d567530d02888d0

e6_act_world.txt (single ACT probe; reused for behavior stages,
degenerate control, and ablation probes):
```
ACT
```
SHA-256 8c0222254050b10cc247418dfecc1424c6dd0326480b413632adad57bc380d87

e6_s3_world.txt (resolve guide 1):
```
OBSERVE 95001 95101 95011
```
SHA-256 e10ac056d807a0d8aea07611dc8b0be6bbaea527554b75fcc330c11f5c4fa920

e6_s5_world.txt (resolve guide 2):
```
OBSERVE 95002 95202 95012
```
SHA-256 a38bd1ebd64e97ef14a2ef4a26b19ec416aac971bfbc42c00351b8eb616c4f22

QUERY lines carry the oracle expected value per the PF protocol;
the inspector never reads world files and the decision rule uses
only state dumps and CHOICE lines, so the oracle value cannot enter
the verdict.

## 3. Stage sequence and observation channels

Per replicate chain r (1..3), one state file, stages run in order
(state removed before s0 for a fresh start):

- s0: e6_s0_world.txt -> dump d0 (init baseline).
- s1: e6_s1_world.txt -> dump d1 (two guides live).
- s2: e6_act_world.txt -> dump d2, transcript t2 (CHOICE c2).
- s3: e6_s3_world.txt -> dump d3 (guide 1 resolved).
- s4: e6_act_world.txt -> dump d4, transcript t4 (CHOICE c4).
- s5: e6_s5_world.txt -> dump d5 (guide 2 resolved).
- s6: e6_act_world.txt -> dump d6, transcript t6 (CHOICE c6).
- d: e6_act_world.txt on a separate fresh state -> transcript
  td (CHOICE cd; degenerate control).

Ablation probes per chain: e6_ablate_bin d1 <class> m_class.bin
for class in NONE F4 F20 UC PRES, then e6_act_world.txt on each
m_class.bin -> transcript ta_class (CHOICE a_class).

Observation channels: (i) the staged dumps d0..d6 via
e6_inspect_bin (lifecycle: which records written, which fields
populated, what resolution changes); (ii) the CHOICE lines c2/c4/c6
(behavior across contents and resolution states); (iii) the
ablation CHOICE lines a_class (read-path evidence); (iv) the
degenerate cd (presence-bit baseline).

## 4. Frozen decision rule

Notation: ch(X,r) = CHOICE line (byte string) of ablation class X
on chain r. G(dN) = the GUIDE/UNCERT lines of the inspector report
on dump dN. All equalities are byte-string equalities; the frozen
binary is deterministic so byte identity is available.

Determinism gate: E6-K2 (section 5) must hold; any
non-byte-identical replicate voids the affected comparison.

Natural invariance N: c2 == c4 == c6 as byte strings on every
chain (guide content varies 2-live / 1-resolved / 2-resolved; the
action must not move for the CONTENT-READ "without affecting the
action" clause).

H2c lifecycle sub-verdict (cluster-analysis bar):
- H2C-STICKY iff G(d2) == G(d3) and G(d4) == G(d5) byte-identical:
  no guide record is retired, updated, unlinked, or aged by either
  resolution event. Confirms H2c.
- H2C-RETIRED otherwise: a resolution retired or updated a guide
  record. Kills H2c per the cluster-analysis bar
  ("inspector shows the resolved guide retired; PASS kills H2c").

Read-path signatures:

- SIGNATURE-DEAD-CONTENT iff ch(F4,r) == ch(NONE,r) AND
  ch(UC,r) == ch(NONE,r) for all r, with ch(PRES,r) != ch(NONE,r)
  for all r (probe sensitivity proven). Guide content fields are
  written but never observably read by any ACT-path read. Supports
  H2c as the concrete form of H2a.
- SIGNATURE-CONTENT-READ iff (ch(F4,r) != ch(NONE,r) OR
  ch(UC,r) != ch(NONE,r)) for all r as byte strings, with N
  holding. Some ACT-path read touches guide content fields without
  the action varying across naturally differing contents.
  Redirects the cluster toward H2d (the bandwidth hypothesis).
  (The F20 action-field outcome is reported alongside but does not
  enter the signature condition; it is not a content field.)

Verdict names: E6-DEAD-CONTENT or E6-CONTENT-READ. If neither
signature's conditions are fully met, the lane reports
E6-INCONCLUSIVE with the full evidence; no verdict is forced.

## 5. Process bars

- E6-K1 (prereg ordering): PASS iff this prereg (+ NAMECHECK.md)
  is committed alone before any E6 world is generated, any tool is
  built, or any run executes; SHA-256 re-verified unchanged from
  git at run time.
- E6-K2 (determinism): PASS iff all dumps d0..d6 and all
  transcripts are byte-identical across the 3 chains per stage,
  and every ablation probe transcript is byte-identical across
  chains per class.
- E6-K3 (frozen binary): PASS iff freeze_shim2_bin and tnn2.zag
  match the section 0 hashes before the first run and after the
  last run.
- E6-K4 (seal integrity): PASS iff every generated world file
  hashes to its section 2 prereg value before execution.
- E6-K5 (block calibration): PASS iff the degenerate control
  yields CHOICE 0 on all 3 runs. A different value voids block
  calibration and the comparisons carry no verdict weight.
- E6-K6 (no leak / anti-smuggling): PASS iff the exact E6 id set
  (95001 95101 95011 95002 95202 95012) returns zero matches in the
  frozen cognition sources (tnn2_build, core_freeze_tnn2_shim).
- K-C0A (zero new semantic cases): PASS iff (1) e6_worldgen.zag
  emits only the exact section 2 streams via fixed string
  literals, with no branching on ids or values; (2)
  e6_inspect.zag and e6_ablate.zag contain zero world-id literals
  (guide detection is the structural predicate of section 1.1;
  ablation classes are argv strings applied uniformly);
  (3) e6_run.sh performs no transcript transformation and no
  logic keyed on world ids, subjects, relations, or CHOICE values
  beyond the byte comparisons required by the section 4 decision
  rule and the E6-K5 gate; (4) the audits in (1)-(3) are recorded
  as greps in E6_RUN.md. A process-bar failure voids the affected
  stage or probe; K-C0A failure voids the lane result.

## 6. Execution and sealing

Tools (pure Zag, pinned znc; built only after this prereg
freezes): e6_worldgen.zag (emits the five section 2 world files
into e6_worlds/); e6_inspect.zag (section 1.3);
e6_ablate.zag (section 1.4). Runner: shell script e6_run.sh that
verifies binary hashes (E6-K3), greps the frozen sources (E6-K6),
generates the worlds and checks them against the section 2 hashes
(E6-K4), runs the 3 chains stage by stage via
`freeze_shim2_bin <world> <state.bin>` (exit 0 required), saves
dumps and transcripts to e6_runs/ with sha256 records, runs the
inspector on each dump, diffs the GUIDE/UNCERT lines across
d2/d3 and d4/d5, runs the 5 ablation probes per chain, and applies
the section 4 decision rule as byte comparisons of CHOICE lines.
No Python anywhere. A process-bar failure VOIDs the affected
stage or probe. A calibration-gate failure (E6-K5) VOIDs the
comparisons. There is no partial verdict.

## 7. No-patch-treadmill compliance

This is a discriminating experiment, not a repair. The outcome
(H2c lifecycle sub-verdict plus the E6-DEAD-CONTENT or
E6-CONTENT-READ verdict) goes back into the BATTERY-CLUSTER
analysis as decided evidence for H2c vs H2d. No mechanism change
is proposed on any outcome.

## 8. Criterion 0 status (binding)

C0-A through C0-D are NOT MET. This experiment probes a frozen
researcher-authored mechanism on fresh structures. No score here
may be described as L3, L3-adjacent, or progress toward L3. Report
as mechanism-targeted evidence only.
