# E5_RUN.md -- Discriminating experiment E5 execution and verdict

Wave: wave-20261001-2321pdt, lane BATTERY-E5.
Prereg: PREREG_E5.md, frozen alone at commit 282c8301e, SHA-256
bc15a264293469319e8de3b63aee755e50410547c48648e08ab2ae963bffeefd
(re-verified unchanged after the battery). Implementation
(worldgen, checker, controls, inspector, audit, blind driver,
sealed worlds, oracles, manifest): commit c8d9f14e1. Executed:
2026-10-02. All work pure Zag (pinned znc) and shell; safebin
PATH; no Python invoked. Frozen binary used as-is; the inspector
and the blind driver are external probes built from committed
lineage (E1 and E3), byte-identical to the recorded sources.

## Verdict: E5-INSTANCE-ONLY

SIGNATURE-INSTANCE-ONLY matched on every pre-registered element,
unanimously across 3 fresh-state runs in both driver conditions.
H1b (instance-only write path) is CONFIRMED for this instrument:
contradicting two instances of one law never lifts revision to
the law level.

## Process bars (battery validity)

- E5-K1 (prereg ordering): PASS. Prereg committed alone at
  282c8301e; implementation commit c8d9f14e1 strictly after;
  prereg SHA-256 re-verified unchanged
  (bc15a264293469319e8de3b63aee755e50410547c48648e08ab2ae963bffeefd).
- E5-K2 (determinism): PASS. All 6 transcripts byte-identical
  within condition (cmp clean: 3 oracle-present, 3 blind); all 6
  state.bin files SHA-256 equal
  (0d1ce315afd43dcbf7e35b49f492d39196f4b2d2e0b81122b87480fead7307a4).
  The two drivers produce identical state; only emitted answers
  differ.
- E5-K3 (frozen binary): PASS. freeze_shim2_bin hashes to
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954
  and tnn2.zag to
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
  before and after; zero modifications under frozen paths.
- E5-K4 (seal integrity): PASS. E5_MANIFEST.sha256 verifies (3/3
  OK); grep of 72000-72999 over tnn2.zag, freeze_shim2_bin, and
  e5_blind_driver_bin returns zero matches.
- E5-K6 (no-leak): PASS. e5_audit_noleak reports LEAKS 0 across
  all 6 world/transcript pairs.

## Calibration gates

- Competent control (LAW-REVISED): checker prints LAWSTRUCT=1
  and VERDICT E5-LAW-REVISED on the synthetic revised-law
  inputs (PASS).
- Competent control (INSTANCE-ONLY): checker prints LAWSTRUCT=0
  and VERDICT E5-INSTANCE-ONLY on the synthetic per-instance
  inputs (PASS).
- Degenerate control: checker prints VERDICT E5-AMBIGUOUS on
  the -2 synthetic transcript (PASS).
- Inspector machinery cross-check: e5_inspect_state on the
  committed E1 w2/w3 state bins reproduces the committed E1
  STRUCTURE lines exactly (PASS).
- Blind driver K1: lines 1-1591 byte-identical to
  freeze_shim2.zag (SHA-256
  580db3ac0d2f2abaa9da19089acc97e75a580559ab7125daf254e64e5e707f0c,
  matching the E3 record); the only delta is the transport
  section (QUERY arity, ev_query with expected=-2, masked=1)
  (PASS).
- Blind driver negative test: fails closed (rc=1, ERROR line)
  on a 3-field QUERY (PASS).
- K-C0A audit: PASS. Inspector and blind driver byte-identical
  to the committed E1/E3 lineage sources; zero 72000-72999
  literals; inspector never reads QUERY lines.

## Per-condition results (frozen TNN-2; identical across 3 runs)

### Condition A: oracle-present (validity, controls, masking demo)

Transcript (e5_runs/e5_w1_orc_r1.trans):
- Promotion probes: ANSWER[0]=72321, ANSWER[1]=72322,
  ANSWER[2]=72421. The two-hop law composes pre-contradiction on
  both revised instances and on the analogous relation.
- Control probes: ANSWER[3]=72341, ANSWER[4]=72342. Both
  contradictions took (flat shadowing, the E1-W2 precedent).
- Discriminating probes (masking demonstration, no verdict
  weight): ANSWER[5]=72323, ANSWER[6]=72421. The oracle-carried
  composed values verify-accept the stale chain, exactly the E3
  masking model.
- Validity probes: ANSWER[7]=72422, ANSWER[8]=72313,
  ANSWER[9]=72323, ANSWER[10]=72321. All hit.
E5-VALID on all 3 runs.

### Condition B: blind (verdict-determinative)

Transcript (e5_runs/e5_w1_blind_r1.trans):
- ANSWER[0..2]=72321, 72322, 72421 (promotion, blind assembly
  intact).
- ANSWER[3]=72341, ANSWER[4]=72342: the flat contradiction facts
  shadow even blind (no candidate competition on the revised
  instances).
- ANSWER[5]=72323: the unseen third instance returns the OLD
  law's derived answer.
- ANSWER[6]=72421: the analogous relation is untouched.
- ANSWER[7..10]=72422, 72313, 72323, 72321 (validity shape
  holds blind).

Checker (all 3 runs):
BAR E5-W1 VALID=1 CTRL=1 THIRD=72323 ANALOG=72421 LAWSTRUCT=0
NANS_O=11 NANS_B=11
VERDICT E5-INSTANCE-ONLY

## White-box inspector findings (condition-A state bins)

Five licensed derived structures, identical across all 3 runs
and both conditions:
- id=21 subj=72301 rel=72809 answer=72321,
  EVIDENCE (72301,72801,72311) (72311,72802,72321)
- id=32 subj=72302 rel=72809 answer=72322,
  EVIDENCE (72302,72801,72312) (72312,72802,72322)
- id=43 subj=72401 rel=72819 answer=72421,
  EVIDENCE (72401,72811,72411) (72411,72812,72421)
- id=62 subj=72303 rel=72809 answer=72323,
  EVIDENCE (72303,72801,72313) (72313,72802,72323)
- id=73 subj=72402 rel=72819 answer=72422,
  EVIDENCE (72402,72811,72412) (72412,72812,72422)

The two-hop law forms licensed derived structures per instance,
including on the held-out third instance (id=62). The
contradiction facts (72301,72809,72341) and (72302,72809,72342)
left NO persistent structure and did NOT revise the derived
structures: instances 1 and 2 keep their original derived
answers (72321, 72322) in state while behavior returns the flat
revised values (72341, 72342), the exact E1-W2 subordination
pattern. No structure carries either contradiction triple as
evidence. LAWSTRUCT=0 on all runs: zero cross-instance
aggregation at the law relation.

## What this decides for H1b (Cluster 1)

H1b is CONFIRMED for this instrument, at both the behavioral and
the state level:

1. Behavior: two licensed systematic contradictions on one law
   (+20 on two instance keys) do not move the unseen third
   instance (72323, the old law) or the analogous relation
   (72421, untouched).
2. State: the contradiction writes land only in the flat
   instance-fact layer. The derived layer is not revised, and no
   operator aggregates the two contradiction writes into a
   law-level structure. There is nothing for a revision pattern
   to transfer through, exactly as H1b states.

The E1-W3 support for H1b (per-instance structures, DERIVED=0)
is now joined by a stronger form: even with a genuine two-hop
derived law and licensed derived structures present per
instance, revision writes stay instance-flat. Combined with
PF-C2 (no cross-relation transfer) and v3 M3 (generalization
0/2, per-key patching), the instance-only write path is now the
best-supported locus in Cluster 1, and the law-level write path
remains unobserved in frozen TNN-2.

## No-patch-treadmill compliance

No repair is proposed. E5 is a discriminating experiment; its
outcome goes back into the cluster analysis as decided evidence
for H1b. A confirmed substrate change (a law-level write path
for the revision operator) would be one general change behind
PF-C2, v3 M3 generalization, and the E5 signature at once, but
that is TNN-3 business after E6-E8, not this lane.

## Criterion 0 status

Unchanged from the prereg: C0-A through C0-D NOT MET. Nothing
here is L3, L3-adjacent, or progress toward L3. The licensed
derived structures are frozen-mechanism artifacts
(trial-constructed graphs), not learner-invented
representations.

## Evidence paths

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E5/
  PREREG_E5.md (frozen alone at 282c8301e, SHA-256
  bc15a264293469319e8de3b63aee755e50410547c48648e08ab2ae963bffeefd)
- Implementation: commit c8d9f14e1 (tools, sealed worlds,
  oracles, E5_MANIFEST.sha256; no runs)
- Tools: e5_worldgen.zag, e5_check.zag, e5_controls.zag,
  e5_inspect_state.zag (byte-identical to e1_inspect_state.zag),
  e5_audit_noleak.zag (byte-identical to e1_audit_noleak.zag),
  e5_blind_driver.zag (byte-identical to e3_blind_driver.zag)
  (and _bin binaries)
- Worlds and manifest: e5_worlds/ (E5_MANIFEST.sha256; world
  SHA-256: oracle
  31fed776cc88f4b28f59567ace16e25647adc29c42e4cf10317e5a9abbf9aee0,
  blind
  27a5f484ddbb5e77916c753e20cbb47d8e5db70f25003710d734a979f92bcfe9;
  oracle record e5_oracles/e5w1.oracle
  e1c459560e88f5d2133d849531c88abf16bcb98a4bff3a130f61944d91e42c3d)
- Transcripts, state bins, inspector reports, check outputs:
  e5_runs/ (per-condition per-run .trans/.bin,
  _inspect_*.txt, _check_*.txt)
- Control outputs: e5_controls_out/
- State bins (all 6 runs): SHA-256
  0d1ce315afd43dcbf7e35b49f492d39196f4b2d2e0b81122b87480fead7307a4
