# E3_RUN.md -- Discriminating experiment E3: execution and verdict

Wave: wave-20261001-2321pdt, lane BATTERY-E3.
Prereg: PREREG_E3.md (frozen alone, commit a17a276c8).
Implementation: commit ce46b327a (worldgen, sealed worlds, blind
driver, scorer, inspector, audit; no runs).

## Verdict: E3-ORACLE-DEPENDENT

SIGNATURE-ORACLE-DEPENDENT matched on every pre-registered
element. H1d is SUPPORTED in refined form (see section 5). It is
not killed.

## 1. Results per condition (3 fresh-state runs each, byte-identical)

Blind = e3_blind_driver_bin (oracle withheld at transport;
ev_query called with expected=-2, masked=1). Oracle-present =
frozen freeze_shim2_bin, hash verified
9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
before running.

| condition | transcript sha256 (r1=r2=r3) | bar probes | distractors |
|---|---|---|---|
| blind E3A | 34d1c05a5d211232b0c3f79faf00a9dce229afbe3feeb87c98dd3ea583856a0e | 2/2: 80921, 80922 | 80921, 80922 (spurious; target -2; observation only) |
| blind E3B | c09be5abe7a8f13cd2855f259a00239cc6f76ec85e634a220bebd9a2d404777e | 0/2: 80971, 80972 (targets 80921, 80922) | n/a |
| oracle-present E3A | 316a07dafc46d8d9c7f3baa53dd09c878096d01ba229cd3904d9ce32b10fc911 | 2/2: 80921, 80922 | -2, -2 correct |
| oracle-present E3B | 2eaab735754e72a3d2ab522084f6ea1a25b35a86208af5a76262209583a49de4 | 2/2: 80921, 80922 | n/a |

Scorer output (e3_score_bin vs sealed oracles):
- blind E3B: PROBE 0 got 80971 want 80921 FAIL; PROBE 1 got
  80972 want 80922 FAIL; SCORE 0/2.
- oracle-present E3B: 2/2 PASS (validity gate: the sealed target
  is reachable and oracle-selectable).
- blind E3A bar probes: 2/2 PASS (calibration: blind assembly
  intact).
- oracle-present E3A: 4/4 PASS.

Every observed output equals the pre-registered prediction
exactly, including the predicted spurious blind outputs
[80971, 80972] and the predicted blind distractor behavior.

## 2. White-box construction evidence (prereg criterion ii)

e3_inspect_bin on the blind state bins:

E3B blind, MAP(80301,80619): node=19 root=12 ans=80971.
Graph walk: GUARD(lit 80301) -> SETREG(lit 80961, DEP-> fact
node=2 (80301 80631 80961)) -> GUARD(lit 80961) ->
SETREG(lit 80971, DEP-> fact node=3 (80961 80632 80971)).
MAP(80302,80619): node=30 root=23 ans=80972, same shape on the
spurious facts (80302 80631 80962), (80962 80632 80972).

E3A blind, MAP(80201,80619): node=17 root=10 ans=80921.
Graph walk: GUARD(lit 80201) -> SETREG(lit 80911, DEP-> fact
node=2 (80201 80611 80911)) -> GUARD(lit 80911) ->
SETREG(lit 80921, DEP-> fact node=4 (80911 80612 80921)).
Distractor MAP(80201,80629): node=39 ans=80921, same valid-chain
shape (relation-agnostic enumeration confirmed in state).

Criterion (iii): no OBSERVE taught (subject, query-relation, *)
in any world (audited; 80619/80629 never appear as OBSERVE
relations), so no direct-fact retrieval shortcut exists.

Conclusion: the blind trial assembles executable 4-op ISA graphs
at runtime, licenses each step with ET_DEP edges to taught facts,
promotes them as MAP nodes, and executes them to produce the
answers. Construction (assembly plus execution) works with no
oracle access. What fails blind is SELECTION: with two executable
chains available, the trial emits the first in BFS order.

## 3. K-C0A audit record

K1. Cognition identity: bytes 1-1591 of e3_blind_driver.zag are
    byte-identical to freeze_shim2.zag lines 1-1591 (diff empty;
    SHA-256 580db3ac0d2f2abaa9da19089acc97e75a580559ab7125daf254e64e5e707f0c). PASS.
K2. Transport-only driver: driver-section diff shows the only
    behavioral changes are (a) QUERY requires exactly 2 fields
    (third field is a parse error), (b) ev_query(W,subj,rel,-2,1)
    instead of ev_query(W,subj,rel,exp,0). No new semantic cases,
    no modes, no bridges, no handlers, no task identities. PASS.
K3. No smuggled answer: e3_audit_bin PASS on both blind worlds
    (E3A: 6 OBSERVE + 4 QUERY; E3B: 8 OBSERVE + 2 QUERY; query
    relations never in OBSERVE lines; no other tokens). PASS.
K4. Oracle separation: no ".oracle"/"e3_oracles" reference in any
    driver source; run commands never pass oracle paths to the
    driver; negative test confirmed the blind driver fails closed
    (exit 1, ERROR line 7) on a 3-field QUERY. PASS.
K5. Frozen binary integrity: freeze_shim2_bin SHA-256 verified
    9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
    before the oracle-present control. PASS.

Zero new semantic cases added anywhere in this lane.

## 4. No-leak and determinism record

N1. Byte-identical transcripts across 3 fresh-state runs in all
    4 conditions (table in section 1). PASS.
N2. Blind transcripts carry oracle values only as taught fact
    objects echoed in OBSERVED lines; ANSWER lines carry learner
    outputs only. PASS.
N3. World/oracle hashes at scoring time match MANIFEST_E3
    (committed pre-run in ce46b327a). PASS.

## 5. Interpretation: H1d supported in refined form

The naive H1d prediction ("blind composition emits nothing")
does not hold: the trial constructs executable graphs blind and
emits answers. The refined H1d holds: every correct composition
observation in the PF battery depended on the trial's unmasked
verifier (t2_try_verify: accept iff executed output equals the
QUERY-carried expected value) to SELECT the right candidate among
multiple executable BFS chains. With the oracle withheld, the
trial's masked policy (accept first executable candidate) emits
the first chain in deterministic BFS order, right or wrong.

Consequences, per the cluster analysis warning:

- PF-A2's 2/2 valid-composition result is re-described: BFS
  enumeration plus oracle selection, not selective construction.
  The valid chain happened to be first in trial order there; E3B
  shows what happens when it is not.
- Every construction claim in the wave whose evidence came from
  unmasked QUERY runs must be re-examined under blind
  conditions. The PF battery's mechanism (a) verdict (FAILS)
  stands and is sharpened: the failure is not merely
  retrieval-shadowing (PF-A1) but oracle-dependent selection.
- The blind distractor probes (E3A probes 2-3: spurious 80921 /
  80922 on the novel relation 80629, with MAP(80201,80629) in
  state) show the trial cannot withhold composition either: it
  enumerates chains relation-agnostically. Oracle verification
  was doing both jobs in the PF runs: selecting the right chain
  AND rejecting all chains (via expected=-2 disabling
  verification).

What this does not establish: no repair is proposed
(no-patch-treadmill rule). A HOLD-style result would have
required a selection mechanism beyond oracle verification; none
was observed. Criterion 0 not met; no L3 language used.

## 6. Commits (local only, never pushed; branch tnn-native-lab)

- a17a276c8: PREREG E3 frozen (design only) + NAMECHECK.
- ce46b327a: E3 implementation: worldgen, sealed worlds and
  oracles, MANIFEST_E3, blind driver, scorer, inspector, audit.
  No runs.
- (this commit): 12 sealed runs, E3_RUN.md, JUDGE_BRIEF.md.

Commit-order self-check: prereg commit strictly precedes
implementation commit; world/oracle hashes committed before any
run.

## 7. Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/PREREG_E3.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/NAMECHECK.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/MANIFEST_E3
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/e3_worlds/
  (e3a_blind.txt 42d041058d003cb9d74e1be536efefba4df7fab6bb95239a1b12bb50ca214615;
   e3b_blind.txt 5ace9e16a5f2855c690a94f7b0795dc5c8517f953d83d7e495894cd279744517;
   e3a_oracle.txt e33625e2cc82c40a2d0de5fd893731f1afb30d74bd3ad6aaaecbc652e185eb9d;
   e3b_oracle.txt a271614b83822ff0b4b99e9d51e50afdf748c8897b75a42149390146ae5be173)
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/e3_oracles/
  (e3a.oracle 8cbc074cd343c060c8f72517cce347112c87277c744577ccacc3f9ab2dfe6b61;
   e3b.oracle 21678ca9569505099aff427e2a642696f55fe70039e3f8194a135688ac86060f)
- docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/e3_runs/
  (12 transcripts + 12 state bins; transcript hashes in
  section 1)
- Tool sources and binaries: e3_worldgen, e3_blind_driver
  (cognition region K1-identical), e3_score, e3_inspect,
  e3_audit (.zag + _bin)
