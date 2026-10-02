# BLIND_RETEST.md -- E3BLIND blind re-examination: execution and verdicts

Wave: wave-20261002-0221pdt, lane E3BLIND.
Prereg: PREREG_E3BLIND.md (frozen alone, commit ff31d063b).
Implementation: commit 9471229c9 (worldgen, sealed worlds and
oracles, MANIFEST_E3BLIND, lane-local audit; no runs).

## Verdicts (per claim, Q4 mandate scope)

- IN-S1 (selection-dependence: correct compositions depended on
  the unmasked verifier to SELECT among multiple executable BFS
  chains): CONFIRMED-BLIND.
- IN-S2 (masked-mode selection: masked policy emits the
  first-executable chain, right or wrong): CONFIRMED-BLIND.
- IN-S3 (PF-A2 re-description: BFS enumeration plus oracle
  selection, not selective construction): CONFIRMED-BLIND.
- OUT-1 through OUT-8 (per Q4_SCOPE.md): OUT-OF-SCOPE; no verdict
  rendered.

The frozen CONFIRMED-BLIND signature matched on every
pre-registered element (section 1).

## 1. Results per condition (3 fresh-state runs each, byte-identical)

Blind = e3_blind_driver_bin (hash re-verified
3661a313b4fd85000bb3b9e92fd5c41bf3240db4f4faaa1cc42b5951b1962e3d;
oracle withheld at transport; ev_query called with expected=-2,
masked=1). Oracle-present = frozen freeze_shim2_bin, hash
verified 9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
before running.

| condition | transcript sha256 (r1=r2=r3) | bar probes |
|---|---|---|
| blind E3C | e7da5d83cfe7af85985b37a548b38af8a1709eb2931c47e7e7103a09a993a562 | 0/2: 91971, 91972 (targets 91921, 91922) |
| blind E3D | 6ff24519d43fa0a065ff6dab830fd465408381f077da7cf027fe747ffb83349e | 2/2: 91921, 91922 |
| oracle-present E3C | f21fdb650efaeead023ffc9a4af7dc1a68dc9a8e2999e810c70c1d8562b6eb9c | 2/2: 91921, 91922 |
| oracle-present E3D | 6ff24519d43fa0a065ff6dab830fd465408381f077da7cf027fe747ffb83349e | 2/2: 91921, 91922 |

Scorer output (e3_score_bin vs sealed oracles):
- blind E3C: PROBE 0 got 91971 want 91921 FAIL; PROBE 1 got
  91972 want 91922 FAIL; SCORE 0/2.
- blind E3D: PROBE 0 got 91921 want 91921 PASS; PROBE 1 got
  91922 want 91922 PASS; SCORE 2/2.
- oracle-present E3C: 2/2 PASS (validity gate: the sealed target
  is reachable and oracle-selectable).
- oracle-present E3D: 2/2 PASS (validity gate).

Every observed output equals the pre-registered prediction
exactly, including the predicted spurious blind outputs
[91971, 91972] on E3C.

## 2. White-box construction evidence (prereg criterion ii)

e3_inspect_bin on the blind state bins (r1; transcripts
byte-identical so r1 is representative):

E3C blind, MAP(91301,91619): node=19 root=12 ans=91971.
Graph walk: GUARD(lit 91301) -> SETREG(lit 91961, DEP-> fact
node=2 (91301 91631 91961)) -> GUARD(lit 91961) ->
SETREG(lit 91971, DEP-> fact node=3 (91961 91632 91971)).
MAP(91302,91619): node=30 root=23 ans=91972, same shape on the
spurious facts (91302 91631 91962), (91962 91632 91972).

E3D blind, MAP(91401,91619): node=17 root=10 ans=91921.
Graph walk: GUARD(lit 91401) -> SETREG(lit 91911, DEP-> fact
node=2 (91401 91611 91911)) -> GUARD(lit 91911) ->
SETREG(lit 91921, DEP-> fact node=4 (91911 91612 91921)).
MAP(91402,91619): node=30 root=23 ans=91922, same shape on
(91402 91611 91912), (91912 91612 91922).

Criterion (iii): no OBSERVE taught (subject, 91619, *) in any
world (lane-local audit; 91619 never appears as an OBSERVE
relation), so no direct-fact retrieval shortcut exists.

Conclusion: on fresh sealed worlds, the blind trial emits the
first-executable chain in teach/BFS order. On E3C the
first-executable chain is the spurious one (sealed target
91921/91922 missed with exactly the predicted outputs 91971/
91972); on E3D the first-executable chain is the valid one.
Unmasked, the same trial selects the sealed target on both
families. Selection among multiple executable chains depends on
the oracle; masked mode emits first-executable, right or wrong.

## 3. Pre-run and post-run audit record

K1. Blind driver SHA-256 re-verified
    3661a313b4fd85000bb3b9e92fd5c41bf3240db4f4faaa1cc42b5951b1962e3d
    before the first run. PASS.
K2. Lane-local audit (e3blind_audit_bin) PASS on both blind
    worlds: 8 OBSERVE + 2 QUERY each; query relation 91619 never
    as an OBSERVE relation; no third QUERY field; no other
    tokens. PASS.
K3. Oracle separation: no "e3blind_oracles"/".oracle" reference
    in any run command; negative test: blind driver on a 3-field
    QUERY fails closed (exit 1). PASS.
K4. freeze_shim2_bin SHA-256 verified
    9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
    before the oracle-present control. PASS.
N1. Byte-identical transcripts across 3 fresh-state runs in all
    4 conditions (table in section 1). PASS.
N2. Blind transcripts carry oracle values only as taught fact
    objects echoed in OBSERVED lines; ANSWER lines carry learner
    outputs only. PASS.
N3. World/oracle hashes at scoring time match MANIFEST_E3BLIND
    (committed pre-run in 9471229c9; sha256sum -c all OK). PASS.

Zero new semantic cases, modes, bridges, or handlers anywhere in
this lane. No Python was invoked at any point (safebin PATH;
Step 0 in NAMECHECK.md).

## 4. Blinding-integrity red team (self)

Was the re-test genuinely blind? Assessment:

R1. Learner-path blindness. The driver is the K-C0A-audited
transport: QUERY requires exactly 2 fields, ev_query is called
with expected=-2 and masked=1. The negative test proves a
3-field QUERY fails closed. The sealed oracles lived in
e3blind_oracles/, which no run command referenced. The trial
could not see the sealed targets. Genuinely blind at the
learner path.

R2. Prediction independence. The pre-registered blind outputs
were derived from the frozen-source trial-order analysis in the
prereg (teach order -> BFS candidate order), committed in
ff31d063b before the worldgen ran. They were not read out of
the oracle files.

R3. Post-hoc oracle tampering. Excluded by N3: the oracle
hashes committed pre-run in 9471229c9 match at scoring time,
so the sealed targets were not edited after the blind outputs
were observed.

R4. Driver tampering. Excluded by K1: the driver hash was
re-verified before the first run.

R5. Cherry-picking. Excluded by N1: 3 fresh-state runs per
condition are byte-identical; there is no variance to select
from.

R6. Designer knowledge. Residual, disclosed: the worker
designated the sealed-valid chain and chose teach order. This
is the standard preregistered-world design (same as E3). The
discriminator is teach-order-follows vs sealed-target-follows:
on E3C these point at different chains, so the outcome is
informative, and the trial had no channel to the designation.

R7. E3D mirror limitation. Disclosed: E3D blind 2/2 is expected
under both the confirmed hypothesis (teach-order wins) and the
overturn hypothesis (selection works), so E3D alone does not
discriminate. The verdict rests on E3C: 0/2 with exactly the
predicted spurious outputs plus the 2/2 oracle-present
validity gate. This is a predicted failure mode, not a generic
malfunction, which rules out the "something broke" alternative.

R8. Unavoidable exposure. The component facts (including the
objects 91921/91922) appear in OBSERVED lines because the
components must be experienced; this is the disclosed
unavoidable channel (prereg T4), identical to E3.

## 5. What this re-test does and does not establish

Establishes (within the frozen bar): on fresh sealed worlds,
the BATTERY-E3 selection-step claims reproduce. Masked
selection emits the first-executable chain; correct composition
outputs under unmasked QUERY depended on oracle verification
for selection. IN-S1, IN-S2, IN-S3 are CONFIRMED-BLIND.

Does not establish: broad generality, L3, or progress toward
L3. Criterion 0 is not met; no L3 language is used. OUT-1
through OUT-8 received no verdict (mandate scope respected).
No repair is proposed (no-patch-treadmill rule). Promotion or
demotion of BATTERY-E3 claims beyond the mandate is the
coordinator's business.

## 6. Commits (local only, never pushed; branch tnn-native-lab)

- e90d49ef0: E3BLIND NAMECHECK (Step 0 toolchain guard) +
  Q4_SCOPE.md (design/scoping only).
- ff31d063b: PREREG_E3BLIND frozen (design only, no
  implementation).
- 9471229c9: E3BLIND implementation: worldgen, sealed worlds
  and oracles, MANIFEST_E3BLIND, lane-local audit. No runs.
- (this commit): 12 sealed runs (3 fresh-state runs x blind
  E3C, blind E3D, oracle-present E3C, oracle-present E3D),
  BLIND_RETEST.md.

Commit-order self-check: prereg commit strictly precedes
implementation commit; world/oracle hashes committed before any
run.

## 7. Evidence paths

- docs/lab/rsi/runs/wave-20261002-0221pdt/E3BLIND/NAMECHECK.md
- docs/lab/rsi/runs/wave-20261002-0221pdt/E3BLIND/Q4_SCOPE.md
- docs/lab/rsi/runs/wave-20261002-0221pdt/E3BLIND/PREREG_E3BLIND.md
- docs/lab/rsi/runs/wave-20261002-0221pdt/E3BLIND/MANIFEST_E3BLIND
- docs/lab/rsi/runs/wave-20261002-0221pdt/E3BLIND/e3blind_worlds/
  (e3c_blind.txt 7712d96b763f5a91c070feb893dcfef886dbc44474fdf798f2fb30cc3c0fe3ee;
   e3d_blind.txt 0410ac2a1a50a10be88ac94d67e57c7e9895ec711ac5bf79ea77d3c3b073c894;
   e3c_oracle.txt ce5f79b70e3821f5bf1851524d9094d98a8d1531531780275100edcbb92d5092;
   e3d_oracle.txt bfcd1b8f8f52e4d3ac64892305574cb2d9a1b90b421329d4e990c7af82071e43)
- docs/lab/rsi/runs/wave-20261002-0221pdt/E3BLIND/e3blind_oracles/
  (e3c.oracle 7463355785271698e724d12593bf3a4dcea235a1eca292ee74b309d16b7496ba;
   e3d.oracle 7463355785271698e724d12593bf3a4dcea235a1eca292ee74b309d16b7496ba)
- docs/lab/rsi/runs/wave-20261002-0221pdt/E3BLIND/e3blind_runs/
  (12 transcripts + 12 state bins; transcript hashes in
  section 1)
- Tool sources and binaries: e3blind_worldgen, e3blind_audit
  (.zag + _bin); reused E3-lane e3_blind_driver_bin,
  e3_score_bin, e3_inspect_bin (hashes in PREREG_E3BLIND.md
  section 0)
