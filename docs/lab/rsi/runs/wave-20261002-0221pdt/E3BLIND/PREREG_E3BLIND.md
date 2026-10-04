# PREREG_E3BLIND.md -- Blind re-examination of BATTERY-E3 selection-step claims (debate Q4 mandate)

Wave: wave-20261002-0221pdt, lane E3BLIND.
Status: FROZEN DESIGN. This file is committed alone before any
E3BLIND world file, oracle file, or tool source is created. Kill
bars never move after freezing. Commit-order self-check: this
commit strictly precedes the implementation commit.

Mandate: debate Q4 (wave-20261001-2321pdt), ruling "OVERTURN (narrow
mandate)": "Blind re-test required for selection-step claims." The
in-scope claims are IN-S1, IN-S2, IN-S3 per Q4_SCOPE.md. All other
BATTERY-E3 claims are OUT-OF-SCOPE for this lane (reported as such
with Q4 quotes; no verdicts rendered on them).

## 0. Frozen binaries (no source edits; hash-verified before use)

Reused from the wave-20261001-2321pdt BATTERY-E3 lane, which
carries the K-C0A audit (cognition region K1-identical to the
frozen TNN-2 shim; transport-only driver; no new semantic cases,
modes, bridges, or handlers):

- e3_blind_driver_bin SHA-256:
  3661a313b4fd85000bb3b9e92fd5c41bf3240db4f4faaa1cc42b5951b1962e3d
- e3_score_bin SHA-256:
  4341e81065ad7ca11ea23fd02ddf1927a6f230e24e8274fd62c5c69ed4753173
- e3_inspect_bin SHA-256:
  e6c44b4d3fd77ec2ce2d6e41530ad340b3b1f24288561bb0160749a5b4dc7ea6
- freeze_shim2_bin (oracle-present control) SHA-256:
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954

Pinned znc SHA-256:
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

Pure Zag for all research logic. Shell only: invoke znc, run
binaries, git ops, move/copy files, sha256sum manifests. No
em-dashes in any doc; check with check_no_dash.sh before commit.
Commits local only under
docs/lab/rsi/runs/wave-20261002-0221pdt/E3BLIND/; never push;
never git reset --hard; never rebase.

## 1. Fresh sealed worlds (generated after this prereg freezes)

ID block 91000-91999, disjoint from E3 (80000-89999), PF
(60000-69999), v3 (50000-59999), and FW1-FW9. Generated once by the
lane-local e3blind_worldgen.zag; SHA-256 hashes committed in
MANIFEST_E3BLIND before any run. Two world families, each with
exactly 2 bar probes (the 0/2 collapse signature is per family).

Exposure teaches only OBSERVE facts. Components are experienced
separately. The target composites are never named in exposure: no
OBSERVE ever carries the query relation (91619), no type-15 LINK
edges, no compose_try demonstrations, no MAP relation sequences,
no supplied structure pointing at any answer. The query relation
is novel in every probe.

### 1.1 Family E3C: spurious-first adversarial family (fresh)

Fresh analog of E3B. The SPURIOUS chain is taught first so it
precedes the valid chain in the trial's deterministic BFS
candidate order. Nothing in the exposure marks either chain as
the target; the sealed oracle alone designates the valid
composite.

```
OBSERVE 91301 91631 91961
OBSERVE 91961 91632 91971
OBSERVE 91302 91631 91962
OBSERVE 91962 91632 91972
OBSERVE 91301 91611 91911
OBSERVE 91911 91612 91921
OBSERVE 91302 91611 91912
OBSERVE 91912 91612 91922
QUERY 91301 91619
QUERY 91302 91619
```

Sealed targets: probe 0 -> 91921, probe 1 -> 91922.

Trial-order analysis (from frozen source, pre-registered): fact
node ids follow teach order (n2..n9 as listed). BFS from 91301:
p0=(91301); head expansion finds n2 -> p1=(91301,91961),
n6 -> p2=(91301,91911); then p1 expands via n3 ->
p3=(91301,91961,91971); p2 expands via n7 ->
p4=(91301,91911,91921). The k=2 chain phase tries length-3 paths
in order: p3 (spurious) before p4 (valid).

Pre-registered predictions: blind -> [91971, 91972] (0/2);
oracle-present -> [91921, 91922] (2/2).

### 1.2 Family E3D: valid-first with competitor (fresh)

Mirror calibration family. The VALID chain is taught first, but
a competing spurious chain is present and executable, so the
oracle's selection role is load-bearing for the oracle-present
condition. If blind behavior follows teach order rather than the
sealed target, blind emits the valid chain here.

```
OBSERVE 91401 91611 91911
OBSERVE 91911 91612 91921
OBSERVE 91402 91611 91912
OBSERVE 91912 91612 91922
OBSERVE 91401 91631 91961
OBSERVE 91961 91632 91971
OBSERVE 91402 91631 91962
OBSERVE 91962 91632 91972
QUERY 91401 91619
QUERY 91402 91619
```

Sealed targets: probe 0 -> 91921, probe 1 -> 91922.

Trial-order analysis (from frozen source, pre-registered): BFS
from 91401 yields p1=(91401,91911) before p2=(91401,91961); the
k=2 chain phase tries p3=(91401,91911,91921) (valid) before
p4=(91401,91961,91971) (spurious).

Pre-registered predictions: blind -> [91921, 91922] (2/2, via
teach order, not selection); oracle-present -> [91921, 91922]
(2/2).

### 1.3 Oracle files (sealed, scorer-side only)

e3c.oracle (probe order): 91921, 91922.
e3d.oracle (probe order): 91921, 91922.
These files are never passed to any learner-path binary. The
blind world files carry QUERY lines with exactly 2 integer
fields (subject, relation); a third field is a transport-level
parse error in the blind driver.

### 1.4 Oracle-present control worlds

e3c_oracle.txt and e3d_oracle.txt: identical streams to the
blind worlds except each QUERY carries its oracle expected value
as the third field. These run under the frozen freeze_shim2_bin
(hash verified before running), replicating the unmasked PF
condition. They are validity controls, not part of the frozen
bar.

## 2. Blinding procedure (red-teamed below, section 6)

- Worlds are generated once by e3blind_worldgen.zag; the sealed
  oracles are written to e3blind_oracles/; MANIFEST_E3BLIND is
  committed before any run.
- The blind driver enforces oracle withholding at transport: the
  QUERY branch requires exactly 2 integer fields (a third field
  is a parse error; the run fails closed), and calls
  ev_query(W, subj, rel, -2, 1): expected=-2 (no oracle), flags=1
  (masked=1). Masked mode is TNN-2's own no-oracle trial path:
  t2_try_verify accepts the first candidate graph that executes
  successfully without comparing against any expected value.
- Run commands never reference the oracle files or the
  e3blind_oracles directory. Negative test: the blind driver is
  run once against a 3-field QUERY line and must fail closed
  (exit 1, ERROR line).
- state.bin is removed before each run (fresh state); 3 runs per
  family per condition; transcripts captured on stdout to
  e3blind_runs/.
- Scoring is scorer-side only, after all runs: e3_score_bin on
  each transcript vs the sealed oracle.
- White-box evidence: e3_inspect_bin on the blind state bins
  (scorer-side read-only probe, no cognition).

## 3. What counts as a blind composition (frozen)

A bar probe counts as a blind COMPOSITION iff all three hold:

(i) Value match: the transcript ANSWER equals the sealed target
    for that probe (scorer-side oracle comparison).
(ii) Constructed and used: the post-run state.bin contains a
    type-20 MAP node with field8 == probe subject and
    field4 == 91619 and field28 == the ANSWER value, whose graph
    root walks (SEQ edges plus BRANCHEQ true-targets) to a
    GUARD/SETREG cell sequence carrying ET_DEP edges to type-1
    fact nodes whose (s,r,o) triples are exactly taught
    component facts from the exposure stream.
(iii) No retrieval shortcut: no OBSERVE in the world taught
    (subject, 91619, *), so a direct-fact hit on the query
    relation is impossible by construction (audited).

If (i) holds without (ii), the probe is reported as
RETRIEVAL-OR-OTHER, not as a composition. If (i) fails, the probe
fails regardless of (ii).

## 4. Conditions and runs

- BLIND (the bar): e3_blind_driver_bin <world.txt> <state.bin>
  on e3c_blind.txt / e3d_blind.txt, 3 fresh-state runs per
  family. Transcripts must be byte-identical across the 3 runs
  (determinism gate); any mismatch is RUN-INVALID and
  investigated, not scored.
- ORACLE-PRESENT (validity control): frozen freeze_shim2_bin
  (hash verified before running) on e3c_oracle.txt /
  e3d_oracle.txt, 3 fresh-state runs per family,
  byte-identical transcripts required.
- Validity gates (must pass or the family run is WORLD-INVALID):
  E3C oracle-present = 2/2 on both bar probes in all 3 runs
  (proves the sealed target is reachable and oracle-selectable);
  E3D oracle-present = 2/2 on both bar probes in all 3 runs.

## 5. Frozen decision rule

CONFIRMED-BLIND: E3C blind = 0/2 with outputs exactly
[91971, 91972] (the pre-registered spurious-first outputs),
E3C oracle-present = 2/2, E3D blind = 2/2 with outputs exactly
[91921, 91922], E3D oracle-present = 2/2, all transcripts
byte-identical across 3 runs per condition, construction
criterion (ii)+(iii) confirmed for the blind outputs via the
inspector, and all audit gates pass (section 7). Verdict applies
per claim: IN-S1, IN-S2, IN-S3 are each CONFIRMED-BLIND. The
selection-step claims stand: masked selection emits the
first-executable chain; correct composition outputs under
unmasked QUERY depended on oracle verification for selection.

OVERTURNED-BLIND: any E3C blind probe emits the sealed-valid
composite (91921 or 91922) where the pre-registered BFS analysis
predicts the spurious composite, with all validity gates passing.
Verdict applies per claim: IN-S1, IN-S2, IN-S3 are each
OVERTURNED-BLIND. A selection mechanism beyond oracle
verification exists; the PF-A2 re-description is falsified.

E3BLIND-INCONCLUSIVE: any other pattern (1/2 splits, -2 outputs
where construction was predicted, non-identical transcripts,
audit failure, validity-gate failure). Report the exact observed
pattern; the in-scope claims are neither confirmed nor
overturned. No repair proposed (no-patch-treadmill rule).

## 6. Blinding-integrity red team (pre-registered threats)

T1. Sealed-target designation vs teach order. The worker (me)
designates which chain the sealed oracle calls valid, and also
chooses teach order. Could the trial's output be guided by the
sealed designation rather than teach order? No: the trial path
never sees the oracle files. The trial experiences only the
world file, where teach order is ordinary exposure (the same
mechanism E3 established for BFS candidate order). The
discrimination is teach-order-follows vs target-follows: on E3C
these point at different chains, so the outcome is informative.

T2. Oracle-present control contamination. The control worlds
carry 3-field QUERY lines. If a blind run ever consumed one, the
blind driver fails closed (parse error, exit 1). Run commands
for blind conditions reference only e3c_blind.txt /
e3d_blind.txt. The negative test proves the failure is closed.

T3. Prediction self-fulfillment. The pre-registered blind
predictions ([91971, 91972] for E3C; [91921, 91922] for E3D)
are derived from the frozen-source trial-order analysis, not
from the oracle files. The sealed oracle is generated by the
worldgen from the same designation table, but the driver and
trial cannot read it; the scorer comparison happens after all
runs. Prediction and oracle share a designer but not a channel
to the learner.

T4. Transcript oracle leakage (N2). ANSWER lines carry learner
outputs only. Oracle values appear in blind transcripts only
as taught fact objects echoed in OBSERVED lines (e.g. 91921 as
a fact object in an OBSERVE echo), which is unavoidable: the
components must be experienced. The audit checks no ANSWER line
carries a value that was not produced by the learner's own
execution.

T5. World-file smuggling (K3 analog). The lane-local audit
(e3blind_audit.zag) checks: every line is OBSERVE with exactly
3 ints or QUERY with exactly 2 ints (3rd QUERY field = FAIL);
the query relation 91619 never appears as an OBSERVE relation;
no other tokens exist. Run on both blind worlds before scoring.

T6. Hash drift (N3). World/oracle hashes at scoring time must
match MANIFEST_E3BLIND (committed pre-run). Any mismatch is
RUN-INVALID.

T7. Determinism (N1). Byte-identical transcripts across the 3
fresh-state runs per condition (sha256sum comparison). Any
mismatch is RUN-INVALID.

T8. Driver cognition drift. e3_blind_driver_bin SHA-256
re-verified against the frozen value in section 0 before the
first run. Any mismatch aborts the wave.

Residual risk (disclosed): the worker knows the sealed targets
while writing worlds. This is the standard preregistered-world
design (identical to E3); the learner path is provably blind
because withholding is enforced at the transport layer (2-field
QUERY, fail-closed) and at the command layer (oracles never
passed). The discriminator is whether outputs follow teach
order or the sealed target, which the trial cannot see.

## 7. Pre-run audit record (run before scoring)

K1. Blind driver hash re-verified (section 0 value).
K2. Lane-local audit PASS on e3c_blind.txt and e3d_blind.txt
    (T5 checks).
K3. Oracle separation: no "e3blind_oracles"/".oracle" reference
    in any run command; negative test: blind driver fails closed
    on a 3-field QUERY.
K4. Frozen binary integrity: freeze_shim2_bin SHA-256 verified
    before the oracle-present control runs.
N1. Byte-identical transcripts 3/3 per condition.
N2. Blind transcripts carry oracle values only as taught fact
    objects.
N3. World/oracle hashes at scoring match MANIFEST_E3BLIND.

## 8. What this re-test does and does not establish

Establishes (within the frozen bar): whether the selection-step
claims IN-S1/IN-S2/IN-S3 reproduce on fresh sealed worlds under
blind conditions with byte-identical determinism and white-box
construction evidence.

Does not establish: broad generality, L3, or progress toward L3.
Criterion 0 is not met; no L3 language is used. OUT-OF-SCOPE
claims (OUT-1 through OUT-8 per Q4_SCOPE.md) receive no verdict
here; the mandate's narrow scope is respected. Promotion or
demotion of BATTERY-E3 claims beyond the mandate is the
coordinator's business.
