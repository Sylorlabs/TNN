# FROZEN PREREG: H5R2-SKEPTIC3, the two-live-facts separator family

Lane: H5R2-SKEPTIC3, wave-20261001-2321pdt. Status: FROZEN PREREG.

Lineage: H5R2-SKEPTIC2 reached SKEPTIC-SURVIVES (EVAL_SKEPTIC2.md):
NEWEST-LIVE-ON-KEY matched H5R2 8/8 on chained decoys with
byte-identical full stdout. The skeptic2 lane named the next
discriminating family: a world where the node-id-first all-live
candidate licenses a live-but-not-newest fact on some key while the
key-newest live fact licenses a later candidate. This lane builds it.

ORDERING RULE: this prereg is committed (with NAMECHECK.md) before any
implementation file is written. Any separator artifact whose mtime
predates the prereg freeze commit is UNVERIFIABLE ORDERING and the
comparison is VOID. Kill bars never move after freezing.

## 1. The hard design problem: two live facts on one key, protocol-licensed

Frozen protocol facts (read from the H5R2 substrate
tnn3_h5r2.zag, SHA-256
04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a):

- ev_teach(s,r,o) allocates a fresh type-1 node and writes (s,r,o).
  It never writes a supersession edge. Nothing in the frozen protocol
  forbids two teaches on the same (subject, relation) key.
- ev_observe(s,r,o) with a differing object supersedes exactly one
  node: the single best-bid live fact returned by activate(s,r).
- is_superseded(n) is true iff n carries a CON self-edge.

Frozen separator sequence per probe (tag SEPxPy), key K=(b,RF2):

1. ev_teach(a,RF1,b): fact F_ab on (a,RF1).
2. ev_teach(b,RF2,c_old): fact F_old on K, lower node id.
3. ev_teach(b,RF2,c_new): fact F_new on K, higher node id.

No OBSERVE is issued on K, so no supersession edge is ever written on
K. After step 3, K holds exactly two live tag-1 non-superseded facts:
F_old (object c_old) and F_new (object c_new), F_old < F_new by node
id (alloc_node scans upward from 2; nothing is freed). This is the
re-teach path the skeptic2 lane named: a second teaching that does
not trigger supersession. It is licensed by the frozen protocol, not
a hack: ev_teach is a frozen event and its non-superseding behavior
is the substrate's own semantics.

Why the arms must diverge here (frozen prediction):

- Trial enumeration is node-id order (t2_gather scans n=2..1024; the
  k=2 loop takes the first len-3 path). The first verifying candidate
  on the chain is the path [a,b,c_old] via facts [F_ab, F_old].
- H5R2 t2_prov_ok accepts any all-live non-superseded licensing set,
  so it promotes the F_old-licensed candidate: live MAP with DEP
  edges to {F_ab, F_old}, MAP f28 = c_old, query answer c_old.
- NEWEST-LIVE-ON-KEY rejects the F_old-licensed candidate because
  sk2_newest_on_key(F_old) scans higher ids and finds F_new live on
  K; it promotes the later-enumerated [a,b,c_new] candidate via
  [F_ab, F_new]: live MAP with DEP edges to {F_ab, F_new}, MAP f28 =
  c_new, query answer c_new.

The query runs with flags=1 (masked=1, dc=0, di=0): the E-ruling that
the expected value is post-hoc feedback only, so any successful chain
execution verifies and the candidate-selection policy (not the
verifier) decides the anchor. With masked=0 the verifier would filter
by expected and the arms could not be discriminated by policy; the
named family requires masked=1. Frozen: every separator query is
ev_query(W,a,RM,-2,1).

Pre-registered divergence signature (SC-1): on every separator probe
the H5R2 arm emits SEP-OLD (live MAP anchors DEP to F_old, the older
live fact; f28 = v = c_old) and the NEWEST-LIVE-ON-KEY arm emits
SEP-NEW (live MAP anchors DEP to F_new, the newest live fact; f28 =
v = c_new).

Pre-registered favored arm: the separator favors NEWEST-LIVE-ON-KEY.
Rationale: the second teaching is the teacher's latest statement
about K, an update without contradiction; the protocol's own revision
semantics (ev_observe contradiction leaves the newest fact live and
the revert MAP anchors to it) agrees that current knowledge wins. The
gate's oldest-first pick is a creation-order artifact of forward
node-id enumeration, not a provenance principle, since both facts are
live and non-superseded and the gate's own "a superseded fact
licenses nothing" rule does not discriminate them.

## 2. Separator world family (frozen spec)

Per separator probe (tag SEPxPy), with chain relations RF1/RF2 and
MAP relation RM, all fresh per world:

1. ev_teach(a,RF1,b).
2. ev_teach(b,RF2,c_old).
3. ev_teach(b,RF2,c_new).
4. SC-4 white-box: exactly two live tag-1 non-superseded facts on
   K=(b,RF2), objects c_old (older id) and c_new (newer id); else
   SEP-TWOLIVE-FAIL and the probe (and its world) is VOID as
   adversarial-by-brokenness.
5. QUERY(a,RM,-2,flags=1): promote the separator MAP (masked=1).
6. White-box SEP-check on the live MAP (section 3).

Frozen constraints: no OBSERVE on any key in any separator world (the
two-live state must never be disturbed); no OBSERVE on any MAP key;
per-probe (subject, relation) ranges disjoint within each world; key
ranges 91xxx-92xxx, disjoint from FW1-FW9 (3xxxx), the 1421pdt
battery (43xxx), the killed H5 battery (51xxx-54xxx), the killed H5R
battery (61xxx-65xxx, 71xxx-72xxx), the H5R2 sealed battery
(83xxx-86xxx), the decoy family (87xxx-88xxx), the chained decoy
family (89xxx-90xxx), and all smoke keys.

### Seeds (frozen before implementation; SHA-256 computed pre-freeze)

- s1: "TNN3H5R2|wave-20261001-2321pdt|sep1" ->
  15bfc81e6c8aee1d65c98f197e498a3b91e542b238f9185a92790aab69926c55 ->
  first 4 hex "15bf" = 5567 -> vo = 5567 mod 7 = 2
- s2: "TNN3H5R2|wave-20261001-2321pdt|sep2" ->
  ecd2955f9d0ba53599debc5c3d378ba7c52cbb62d5b2bc5eb1304b1026b4e423 ->
  first 4 hex "ecd2" = 60626 -> vo = 60626 mod 7 = 6

Object values: c_old = base + vo + 10*i (i = 0..3 per probe),
c_new = c_old + 1, with base 91401 (s1) / 92401 (s2).

### World s1 (chain 9101/9102, MAP 9103)

- S1P1: a=91101 b=91301 c_old=91403 c_new=91404
- S1P2: a=91102 b=91302 c_old=91413 c_new=91414
- S1P3: a=91103 b=91303 c_old=91423 c_new=91424
- S1P4: a=91104 b=91304 c_old=91433 c_new=91434

### World s2 (chain 9201/9202, MAP 9203)

Materially different relation family and subject distribution from s1.

- S2P1: a=92101 b=92301 c_old=92407 c_new=92408
- S2P2: a=92102 b=92302 c_old=92417 c_new=92418
- S2P3: a=92103 b=92303 c_old=92427 c_new=92428
- S2P4: a=92104 b=92304 c_old=92437 c_new=92438

8 separator probes total (N=8, satisfies N>=8).

## 3. The SEP-check (frozen white-box bar, per probe, arm-neutral)

On the live MAP for (a,RM) after step 5, with F_old/F_new the two
live tag-1 non-superseded facts on K=(b,RF2) ordered by id, and F_ab
the single live tag-1 fact on (a,RF1):

- exactly 2 live tag-1 non-superseded facts on K, with objects c_old
  and c_new on the older and newer id respectively (else
  SEP-TWOLIVE-FAIL; this is SC-4);
- exactly 1 live MAP on (a,RM) (else SEP-MAP-FAIL);
- the MAP carries exactly 2 DEP (type-1) edges, one to F_ab and one
  to exactly one of {F_old, F_new} (else SEP-DEP-FAIL);
- MAP f28 == query answer v == object of the anchored b-link fact
  (else SEP-VAL-FAIL);
- the query did not miss (else SEP-MISS).

"SEP ok" is emitted only if all conjuncts pass. The arm-neutral
anchor marker is then emitted: "SEP-OLD" if the b-link DEP target is
F_old (f28 = v = c_old), "SEP-NEW" if it is F_new (f28 = v = c_new).

## 4. Compared arms (sources extracted read-only from recorded commits)

- H5R2: source extracted via git show from
  9db334bd4a01d21cce52da3bb2a1c45a10c4c172, SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a
  (must match before use).
- NEWEST-LIVE-ON-KEY: source extracted via git show from f461e812d
  (bl_newest.zag), SHA-256
  e5df3ddb28858b60efb01f3d8df524a98ce79686e199532e53713c24f367b649
  (must match before use). Do NOT rebuild from working files.

## 5. Frozen kill bars

SC-1 (DIVERGE, exact pre-registered signature): on all 8 separator
probes the H5R2 arm emits SEP-OLD and the NEWEST-LIVE-ON-KEY arm
emits SEP-NEW. The two arms' live MAPs anchor to different facts on
K (F_old vs F_new) with different answers (c_old vs c_new).

SC-2 (direction): (H5R2 SEP-OLD count >= 1) OR (skeptic SEP-NEW
count >= 1), AND NOT (both arms show zero SEP-OLD/SEP-NEW markers
across all 8 probes). At least one arm lands in its pre-registered
direction; both arms failing outright yields no verdict.

SC-3 (determinism): 3/3 byte-identical full-stdout runs per arm per
world, SHA-256 compared (the KB-D1 protocol).

SC-4 (two-live state): SEP-TWOLIVE ok on all 8 probes on both arms:
exactly two live tag-1 non-superseded facts on K with objects c_old
(older) and c_new (newer), verified by white-box inspection.

## 6. Frozen decision rule

- SEPARATED iff SC-1 and SC-2 and SC-3 and SC-4 all hold: the gate
  and the skeptic are finally discriminated on the named family.
  Report which arm the separator favors: NEWEST-LIVE-ON-KEY, per the
  pre-registered rationale in section 1.
- NOT-SEPARATED iff SC-3 and SC-4 hold and the arms coincide on all 8
  probes (both SEP-OLD, both SEP-NEW, or both the same non-anchor
  marker): the design failed to separate the arms; report honestly.
- Otherwise INCONCLUSIVE: report the exact per-arm per-bar numbers
  with hashes; no verdict claimed. A probe with SEP-TWOLIVE-FAIL
  makes its world VOID as adversarial-by-brokenness (not scored).

## 7. Worlds and evaluation protocol (frozen)

7.1. Assembly per arm per world (4 worlds), after the implementation
commit, by the frozen rule: byte-copy of the arm substrate with the
single line `fn main()i32 { return run_all(); }` changed to
`fn main()i32 { return sealed_main(); }` (verified by diff: exactly
one line differs), plus the frozen DRIVER_TMPL.zag appended (SHA-256
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af,
extracted from 9db334bd4), plus the frozen SEP_FRAG.zag appended
(SHA-256 recorded before assembly), plus one alias line selecting the
world (`fn sealed_main()i32 { return sealed_main_s1(); }`, etc.).

7.2. World file SHA-256s recorded before any run. Each world compiled
separately with the pinned znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1); 3/3 runs;
full-stdout SHA-256 compared per world (SC-3).

7.3. Scoring uses the driver's own markers: "SEP ok" (target 8 per
arm: 4 per world), "SEP-OLD" / "SEP-NEW" (target 8 each on the
respective arm), "SEP-TWOLIVE ok" (target 8 per arm),
"SEP-TWOLIVE-FAIL" / "SEP-DEP-FAIL" / "SEP-MAP-FAIL" /
"SEP-VAL-FAIL" / "SEP-MISS" counts, and zero unexpected FAIL marker
lines. The canonical full state dump ends each world for SC-3.

7.4. Negative controls: NC-S0 (a world file is not a valid assembly
per 7.1: that arm is VOID, not scored); NC-S1 (any
forbidden-executable invocation: PROCESS-FAIL, terminal); NC-S2
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
