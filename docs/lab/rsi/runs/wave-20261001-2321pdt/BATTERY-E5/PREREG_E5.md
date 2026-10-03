# PREREG_E5.md -- Discriminating experiment E5: double-revision law world (tests H1b)

Wave: wave-20261001-2321pdt, lane BATTERY-E5.
Status: FROZEN DESIGN. This file is committed alone before any E5
world file, spec file, or tool source is created. Kill bars never
move after freezing.

## 0. Freeze record and provenance

E5 is the fifth-prioritized discriminating experiment from
BATTERY-CLUSTER/CLUSTER_ANALYSIS.md (Cluster 1, DERIVATION
SUBORDINATION). It tests hypothesis H1b: "Instance-only write path
(locus: the revision/contradiction operator). GENERAL substrate
property. Contradiction and promotion writes go only to the
instance layer (last-write-wins facts, per-instance patches); no
operator writes to an abstraction or law layer, so there is nothing
for a revision pattern to transfer through."

Motivating result: BATTERY-E1 returned E1-FIRSTCLASS, killing H1c
as stated. E1-W3 (cross-relation revision transfer) found two
single-evidence per-instance structures and no law-level derived
structure (DERIVED=0), supporting H1b. E5 decides whether revision
ever lifts from instances to the law level.

E5 discriminates, in one sealed world, between:
- "revision stays per-instance" (H1b confirmed): contradicting two
  instances of one law leaves an unseen third instance on the old
  law and an analogous relation untouched; and
- "revision lifts to the law" (H1b killed for this instrument):
  the unseen third instance follows the revised pattern, or a
  cross-instance law-level structure forms in state.

Frozen binary (no source edits permitted; the inspector and the
blind driver are external probes built from committed lineage):
- `tnn2.zag` SHA-256:
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  (path: docs/lab/research-lead/overnight-20260928/tnn2_build/
  tnn2.zag)
- `freeze_shim2_bin` SHA-256:
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
  (path: docs/lab/research-lead/overnight-20260928/
  core_freeze_tnn2_shim/freeze_shim2_bin)
- Blind driver: e5_blind_driver, copied byte-identical from the
  committed e3_blind_driver.zag lineage (BATTERY-E3, commit
  ce46b327a); K1 re-verified in the K-C0A audit (section 7).
- Pinned znc SHA-256:
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (path: src/tools/toolchain/znc_linux_x86_64_abed8aa1)

World id block: 72000-72999. Fresh and disjoint from v3
(50000-59999), the PF battery (60000-69999), and E1
(71000-71999). Material differences from E1-W3/PF-C2: the law is
a TWO-HOP derived law (the composed answer is never taught, the
E1-W4 family) taught across three instances of one law relation;
two instances receive licensed systematic contradictions; an
unseen third instance and an analogous-relation probe discriminate
the lift; the discriminating probes run blind per the E3
wave-shaping result (E3-ORACLE-DEPENDENT: assembly works blind,
selection does not; an oracle-present discriminating probe would
let t2_try_verify mask a genuine law-write behind the stale
chain). No world is a trivial FW1-FW9 variant.

## 1. Global constraints

PURE ZAG ONLY for all research logic. Shell only: invoke znc, run
binaries, git ops, move/copy files, sha256sum manifests. The world
runs 3 times from fresh state under EACH of two drivers:
(a) oracle-present `freeze_shim2_bin <oracle-world> <state.bin>`
for validity, controls, and the masking demonstration;
(b) blind `e5_blind_driver_bin <blind-world> <state.bin>` for the
verdict-determinative discriminating probes (oracle withheld at
transport, ev_query with expected=-2, masked=1, the E3 lineage).
Transcripts and state.bin saved per run per driver. No em-dashes
in any doc; check with check_no_dash.sh before commit. Commits
local only under
docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E5/; never push;
never git reset --hard; never rebase. This prereg is committed
alone first; world generation, tool building, sealed worlds,
oracles, and the manifest follow in a separate commit; runs and
the verdict follow in a third commit (commit-order self-check).
The BATTERY, BATTERY-CLUSTER, BATTERY-E1, and BATTERY-E3 lane
directories are read-only for this lane; lineage sources are
extracted with git show from the recorded commits.

## 2. World design (frozen)

### 2.1 The two-hop law

Law L on relation 72809: for instance s in {72301, 72302, 72303},
OBSERVE (s, 72801, s+10) [P hop] and OBSERVE (s+10, 72802, s+20)
[Q hop]. The law answer s+20 on 72809 is DERIVED (never taught on
72809), the E1-W2/E1-W4 family.

Analogous law L2 on relation 72819: for instance s in {72401,
72402}, OBSERVE (s, 72811, s+10) and OBSERVE (s+10, 72812, s+20).

### 2.2 Licensed contradictions

Two instances of law L receive a systematic +20 shift on the law
relation, mirroring PF-C2's licensed +20 pattern:
OBSERVE (72301, 72809, 72341) and OBSERVE (72302, 72809, 72342).
"Licensed" means world-consistent and systematic across both
instances, not singleton noise.

### 2.3 Probe plan (frozen)

- Promotion probes (pre-contradiction): the two-hop law composes
  on instances 1, 2 and on the analogous relation.
- Control probes (post-contradiction): instances 1 and 2 return
  the revised values, confirming the contradictions took (the
  E1-W2 flat-shadowing precedent: 71213).
- Discriminating probes: unseen third instance 72303 on 72809,
  and analogous instance 72401 on 72819. Run BLIND (driver b).
- Validity probes: analogous untouched instance 72402, the
  held-out instance's taught hops, and instance 1's Q hop
  (confirming the contradiction did not clobber the hop layer).

### 2.4 The oracle-masking control

E3 established that the trial's unmasked verifier
(t2_try_verify: accept iff executed output equals the
QUERY-carried expected value) SELECTS among executable chains.
The stale chain for instance 3 (72303 -> 72313 -> 72323) remains
executable under any law-write, so an oracle-present
discriminating probe carrying the composed value 72323 would
verify-accept the stale chain and mask a genuine law-write. The
discriminating probes therefore run blind, where the trial emits
the first executable candidate in BFS order (E3 blind policy).
The oracle-present run records the same probes as a masking
demonstration (expected: stale-chain values regardless of the
blind outcome); it carries no verdict weight for probes 5 and 6.

## 3. World streams (fresh sealed worlds; pinned verbatim)

World files are generated byte-exact from these streams after
this prereg freezes (e5_worldgen.zag). Two driver variants share
the OBSERVE stream and differ only in QUERY arity:
- e5_w1_oracle.txt: 3-field QUERY lines (oracle values are the
  world-determined composed/taught values, scorer convention).
- e5_w1_blind.txt: 2-field QUERY lines (the blind driver fails
  closed on a third field, E3 K4).
The sealed oracle record e5_oracles/e5w1.oracle holds the 11
world-determined probe values in order, scorer-side only.
E5_MANIFEST.sha256 (both world files plus the oracle record) is
committed before any run.

### E5-W1: double-revision law world (H1b discriminator)

```
OBSERVE 72301 72801 72311
OBSERVE 72302 72801 72312
OBSERVE 72303 72801 72313
OBSERVE 72311 72802 72321
OBSERVE 72312 72802 72322
OBSERVE 72313 72802 72323
OBSERVE 72401 72811 72411
OBSERVE 72402 72811 72412
OBSERVE 72411 72812 72421
OBSERVE 72412 72812 72422
QUERY 72301 72809 72321
QUERY 72302 72809 72322
QUERY 72401 72819 72421
OBSERVE 72951 72960 72971
OBSERVE 72952 72960 72972
OBSERVE 72301 72809 72341
OBSERVE 72302 72809 72342
OBSERVE 72953 72960 72973
OBSERVE 72954 72960 72974
QUERY 72301 72809 72341
QUERY 72302 72809 72342
QUERY 72303 72809 72323
QUERY 72401 72819 72421
QUERY 72402 72819 72422
QUERY 72303 72801 72313
QUERY 72313 72802 72323
QUERY 72311 72802 72321
```

ANSWER indices (0-based, in stream order):
- ANSWER[0]=72321, ANSWER[1]=72322, ANSWER[2]=72421:
  promotion probes (validity).
- ANSWER[3]=72341, ANSWER[4]=72342: control probes
  (contradiction took; validity).
- ANSWER[5]: unseen third instance (discriminating, blind run).
- ANSWER[6]: analogous relation (discriminating, blind run).
- ANSWER[7]=72422, ANSWER[8]=72313, ANSWER[9]=72323,
  ANSWER[10]=72321: validity probes.

The sealed oracle record (world-determined values, in order):
72321, 72322, 72421, 72341, 72342, 72323, 72421, 72422, 72313,
72323, 72321.

## 4. Frozen decision rule

Let the oracle-present runs be condition A and the blind runs be
condition B (3 fresh-state runs each).

Process preconditions (any failure yields E5-INCONCLUSIVE, an
instrument failure, not an H1b verdict): all 3 transcripts
byte-identical within each condition (E5-K2); per-condition
state.bin SHA-256 equal across the 3 runs (E5-K2); E5-VALID on
every condition-A run; E5-K1, E5-K3, E5-K4, E5-K6 all PASS;
calibration controls PASS.

E5-VALID (condition A, all 3 runs) iff:
ANSWER[0]=72321 and ANSWER[1]=72322 and ANSWER[2]=72421
(promotion: the two-hop law composes pre-contradiction), and
ANSWER[3]=72341 and ANSWER[4]=72342 (control: both contradictions
took), and ANSWER[7]=72422 and ANSWER[8]=72313 and
ANSWER[9]=72323 and ANSWER[10]=72321 (validity probes).

Discriminating signatures (condition B, all 3 runs):
- SIGNATURE-INSTANCE-ONLY: ANSWER[5]=72323 (the old law's derived
  answer on the unseen third instance) and ANSWER[6]=72421 (the
  analogous relation untouched).
- SIGNATURE-LAW-REVISED: ANSWER[5]=72343 (the third instance
  follows the revised +20 pattern). ANSWER[6] is recorded as a
  secondary: 72441 means the lift crossed relations; 72421 means
  the lift is relation-scoped.

White-box secondary (condition-A state bins, all 3 runs; the
e1_inspect_state lineage, unchanged): LAWSTRUCT=1 iff there
exists a STRUCTURE with rel=72809 whose EVIDENCE contains both
(72301,72809,72341) and (72302,72809,72342) (cross-instance
aggregation at the law relation). Pre-registered
interpretation: LAWSTRUCT=1 falsifies H1b as stated ("no
operator writes to an abstraction or law layer") at the state
level even if behavior is instance-only; the locus then refines
to the read path (the H1a family), reported to the cluster
analysis.

Verdicts:
- E5-INSTANCE-ONLY iff E5-VALID and SIGNATURE-INSTANCE-ONLY on
  all 3 condition-B runs and LAWSTRUCT=0 on all 3 condition-A
  runs. Confirms H1b: revision never lifts from instances to the
  law level.
- E5-LAW-REVISED iff E5-VALID and SIGNATURE-LAW-REVISED on all
  3 condition-B runs (LAWSTRUCT reported alongside). Kills H1b
  for this instrument.
- E5-LAW-TRACE iff E5-VALID and LAWSTRUCT=1 on all 3 condition-A
  runs and not SIGNATURE-LAW-REVISED. Kills H1b as stated at the
  state level; behavior stays instance-only (read-path locus).
- E5-AMBIGUOUS otherwise. Report only; no H1b verdict. This
  includes blind -2 oracle-limit outcomes (the E3 selection
  caveat) and any mixed pattern (for example ANSWER[5]=72323
  with ANSWER[6]=72441); the exact pattern is reported.

## 5. Process bars E5-K1 through E5-K6

- E5-K1 (prereg ordering). PASS iff this file's commit strictly
  precedes the first commit containing any E5 world file, spec
  file, or tool source, and this file's SHA-256 is unchanged
  after the battery.
- E5-K2 (determinism). PASS iff all 3 transcripts are
  byte-identical within each condition AND the per-condition
  state.bin SHA-256 is equal across the 3 runs.
- E5-K3 (frozen binary). PASS iff freeze_shim2_bin and tnn2.zag
  match the section 0 hashes before and after the battery, and
  zero modifications under the frozen cognition paths.
- E5-K4 (seal integrity). PASS iff E5_MANIFEST.sha256 verifies
  (all files OK) and grep of 72000-72999 over tnn2.zag,
  freeze_shim2_bin, and e5_blind_driver_bin returns zero
  matches.
- E5-K6 (no-leak). PASS iff e5_audit_noleak reports zero leaks
  across all world/transcript pairs of both conditions.

## 6. Calibration

- Competent control (LAW-REVISED): a synthetic inspector report
  containing a LAWSTRUCT-conformant structure (rel=72809,
  EVIDENCE containing both contradiction triples) plus a
  synthetic blind transcript with ANSWER[5]=72343; the checker
  must print LAWSTRUCT=1 and verdict E5-LAW-REVISED.
- Competent control (INSTANCE-ONLY): a synthetic report with
  only per-instance structures plus a synthetic blind transcript
  with ANSWER[5]=72323 and ANSWER[6]=72421; the checker must
  print LAWSTRUCT=0 and verdict E5-INSTANCE-ONLY.
- Degenerate control: a synthetic blind transcript with -2 on
  the discriminating probes; the checker must print
  E5-AMBIGUOUS.
- Inspector machinery cross-check: run e5_inspect_state on the
  committed E1 w2/w3 state bins with their world files; the
  STRUCTURE lines must match the committed E1 inspector reports
  exactly (detection machinery unchanged).
- Blind driver K1: bytes 1-1591 of e5_blind_driver.zag are
  byte-identical to freeze_shim2.zag lines 1-1591
  (re-verified); negative test: the blind driver fails closed
  (nonzero exit) on a 3-field QUERY line.

## 7. K-C0A audit (zero new semantic cases)

Frozen audit procedure, executed after the tools are built and
before runs:

1. e5_inspect_state.zag is byte-identical to the committed
   e1_inspect_state.zag (diff empty); e5_blind_driver.zag is
   byte-identical to the committed e3_blind_driver.zag (diff
   empty). Both are reused lineage, not new instruments.
2. e5_inspect_state.zag and e5_blind_driver.zag contain zero
   integer literals in 72000-72999 and zero string literals
   naming a world, role, or relation; verified by grep.
3. The inspector collects OBSERVE lines only; QUERY lines are
   never read (oracle-blind by construction). The blind driver
   differs from the frozen shim only in transport (QUERY arity,
   expected=-2, masked=1); the K1 byte-identity check pins the
   cognition section.
4. World parameters (id ranges, derived values, probe indices,
   bar values) appear only in e5_worldgen.zag (generator),
   e5_check.zag (scorer data, the e1_struct_check lineage), and
   e5_controls.zag (synthetic control data); never in the
   inspector or the blind driver.
5. The audit prints K-C0A PASS/FAIL. K-C0A FAIL voids the
   instrument; rebuilding requires a new prereg section, never
   a silent fix.

## 8. Predicted outcome (recorded before execution)

E5-INSTANCE-ONLY. Basis: E1-W3 found per-instance structures with
no law-level derived structure (DERIVED=0); v3 M3 showed
per-key patching with generalization 0/2; PF-C2 showed no
cross-relation transfer of the +20 shift. No evidence to date
suggests a revision write above the instance layer.

## 9. Criterion 0 status (binding)

This experiment probes frozen researcher-authored mechanisms
with a white-box inspector and a blind transport driver. C0-A
through C0-D are NOT MET. No score here may be described as L3,
L3-adjacent, or progress toward L3. Report as
mechanism-targeted evidence for H1b only.
