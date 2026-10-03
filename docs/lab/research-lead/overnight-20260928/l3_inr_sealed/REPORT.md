# L3-INR Sealed Battery REPORT
Adversary: L3-INR-SEALED (independent instance, post-freeze design).
Implementation freeze: 2026-10-03 07:15:15 UTC (commit 106c8e99c).
Sealed design: 2026-10-03 ~07:26-09:00 UTC (strictly post-freeze).
Battery runs: 3/3 byte-identical (summaries SHA256 2d5a886a...,
traces SHA256 b633f9e8...).

## Verdict: L3-KILLED

Multiple frozen bars are red. The implementation does not achieve L3.

## Per-bar verdicts (frozen PREREG C363)

### K1 (final structure not in source): PASS
Source audit: no sealed order, entity set, pair, or edge set appears in
learner source. The sealed worlds (S1,S2,S3a,S3b,S1p) were designed
post-freeze by the adversary. A-LIT holds.

### K2 (created after experience): PASS
T1 trace: OBSERVE/TEST-PAIR strictly before first CONSTRUCT event.
(SEQ ordering verified in trace.log.)

### K3 (persistent learner state): FAIL (RED)
Requires T2 passes with zero CONSTRUCT for slot G after T1 commit.
T2 result: DEV_VERDICT FAIL (HELD 4/6). The persisted edge set does not
solve the transfer task.

### K4 (white-box creation trace): PASS
A-TRACE: every propose, TEST, REVISE, DEFINE, COMMIT logged with
monotonic SEQ and parent pointers. Trace sufficient to replay.

### K5 (hidden instances solved): FAIL (RED)
Requires: T1 >=5/6 with |E|<=10; T3 exact; T3b >=5/6; T4 >=5/6;
T5a commits correct; T5b DEFERS.
- T1: 4/6, 12 edges -> FAIL. (Adversarial kill: incomplete-disambiguation
  trap. Three gaps (z4,z5),(z5,z6),(z6,z7); HYP identifies sole survivor
  but probe materializes only the first disagreeing pair; commit has 12
  edges; heldout 4/6.)
- T3: PASS (exact order match).
- T3b: 0/0 -> FAIL. (Protocol: no heldout loaded; see caveat.)
- T4: 6/6 -> PASS.
- T5a: PASS (correct edge set committed, 6/6).
- T5b: PASS (DEFERRED honestly).
K5 RED via T1 and T3b.

### K6 (ablation destroys advantage): PASS
C0 fails T1 (HELD 4/6 < 5/6): construction advantage destroyed. C4
comparison available for KC0D.

### K7 (reused later): FAIL (RED)
Requires T2 passes. T2: DEV_VERDICT FAIL (4/6). The learned structure
does not reuse successfully.

### K8 (transfers across recode): FAIL (RED)
Requires T3b passes AND C5 fails. T3b: FAIL (0/0). C5: PASS (control,
fails task as required). K8 RED via T3b.

### K9 (beats controls): PASS
C0 (4/6), C1 (4/6), C2 (5/18), C3 (fails training) all fail as specified.
G1e holds. NOTE: C3 exhibits idx<90 boundary (cannot add from id 9).

### K10 (independent red team): PENDING
Requires follow-up worker (different instance). Not run in this battery.
A KILL verdict stands on other red bars; SURVIVES would need K10.

### K11 (revisable after counterexample): PASS
T4: 6/6 WITH valid edit lineage (8/12). Lineage bar satisfied.
CAVEAT: S2's regime change was mild (only 1 true gap; S1's G pre-covered
2 of 3 gap positions). T4's revision succeeded but was not strongly
stressed. The id-alignment requirement (S2 PAIR order matches S1's) is
documented in SEALED_KEY.md.

### K12 (7/12 rule): L3-KILLED
K3, K5, K7, K8 are RED. Any red is L3-KILLED. Partial credit does not exist.

### KC0A (runtime-defined semantics): PASS
Source audit: no branch/case/literal keyed to dominance, order, rank, or
sealed-world property. Only generic machinery (slot store, LINK, neighbor
lookup, expansion, consequence channel).

### KC0B (open structural form): PASS
G1e holds (C2/C3 fail). Construction enumerates no edge-set family.
Variable-size under 200-cap. Final topology assembled incrementally.

### KC0C (sealed post-freeze worlds): PASS
S1,S2,S3a,S3b,S1p sealed; designed by independent adversary (this worker)
post-code-freeze. At least one adversarial family (incomplete-
disambiguation). Design/implementation/adversary are distinct instances.

### KC0D (cognitive reuse): FAIL (RED)
Requires: T3 TEST <= half C4 TEST AND T3b passes.
- T3 NTEST=1, C4 NTEST=399. 1 <= 199.5 -> sample-efficiency holds.
- T3b: FAIL -> KC0D RED.

## Adversarial findings (beyond the bars)

1. **Incomplete-disambiguation trap (S1 family)**: The learner's HYP_BUILD
   correctly identifies the sole training-consistent hypothesis variant via
   the consequence channel, but commits E without materializing the
   survivor's edges. The probe path fixes only the FIRST disagreeing pair
   (id order); remaining gaps are never resolved. Result: 12 edges (over
   the 10 compression bar), 4/6 heldout. This is a structural limitation
   in the probe-then-commit logic, not a training failure (18/18).

2. **C3 idx<90 boundary**: The exact C3 greedy constructor never considers
   edges from id 9 (loop bound idx<90). On S1, this prevents adding
   (z5,z7),(z5,z8), contributing to C3's training failure. This is a
   frozen-code boundary defect, exhibited in the key.

3. **T4 id-alignment fragility**: T4's toxic-purge compares S1's G edges
   (S1 ids) against S2's training (S2 ids) without remapping. If S2's PAIR
   order differs from S1's, the purge is arbitrary. S2 was designed with
   matching first-appearance order to give T4 a clean test. A robust
   revision mechanism should map by entity identity, not positional ids.

4. **T3b protocol limitation**: T3b loads zero heldout pairs after
   SLOT_READ+OBSERVED (HELDOUT pairs=0), so it cannot pass even in
   principle in this sequence. The DEV battery's T3b PASS must have used
   a different setup. This is documented as a caveat; the adversarial
   intent (transfer fails) is satisfied, but via protocol rather than
   rank quality.

## Reclassification by evidence
Per K12, L3-KILLED with reclassification: the evidence supports **L2+**
(structural learning with persistent state and revision, but without
reliable hidden-instance generalization or transfer). The invention
mechanism works on DEV but does not survive the sealed adversarial
family. It is not L2 (there is genuine structure construction and reuse
attempt), but it is not L3.

## Artifacts
- Worlds: worlds/s1.world, s2.world, s3a.world, s3b.world, s1p.world
- Key: SEALED_KEY.md
- Battery runs: battery_run1/, battery_run2/, battery_run3/ (3/3 identical)
- Summaries SHA256 (content): 2d5a886a3dc2b5a2cb4411a24a7b1a22fa3092f48b96d736164189ebe2228df5
- Traces SHA256 (content): b633f9e857b1cdabad067a3776b79f663587565fa8fbb516aad2638458117698

## Constraints honored
- Pure Zag, safebin mandatory. No Python invoked.
- Frozen implementation never modified (git diff clean, verified).
- Learner never opened world file (two-process protocol via run_arm.sh).
- Sealed worlds designed post-freeze, materially different from DEV.
- Commits local, never push, explicit pathspecs.
