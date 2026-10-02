# PREREG: Hardening Grammar Active Inquiry Against Adversarial Teachers

## Worker

Inquiry Hardening Worker. Mission: harden the active-inquiry mechanism
against the two KILLs and one BOUND from INQUIRY-ADVTEACHER-COMPLETE.
Unfrozen variant only. Frozen read-only: `grammar_inquiry/` and
`inquiry_advteacher/` sources are copied byte-identical (SHA-256
a29972ca... for a_base.zag, 1c88c5d9... for a_patch.zag), never edited.
This prereg is committed BEFORE any implementation (commit-order
self-check: this file's first commit strictly precedes the
implementation commit).

## Problem (from the advteacher report)

- ADV-LIE KILL: false fact (35,42,2) kills the true divisor d=8, keeps
  wrong d=17; learner writes silent-wrong grammar (D=17); the -4
  fail-closed is defeated by one lie. Lesson: op-consistency tests facts
  against candidates, not ground truth.
- ADV-POISON KILL: false decomp fact (0,43,63) bypasses the op check
  entirely (relations 43/44 never scanned); trusted into W; inquiry
  resolves to true D=8 (masking) while ranges corrupt to a=[2,7] b=[2,7].
  Lesson: the decomp channel is an unverified trust path.
- ADV-WASTE BOUND: QMAX caps damage at 4 burned queries; no usefulness
  tracking, no early stop.

## Threat model

Same as advteacher: the adversarial teacher answers a GI-INQUIRY
request with a protocol-legal taught fact via the inquiry channel. It
knows the true world, like the cooperative teacher did. It does NOT
modify learner machinery or W directly. The LEARNER machinery is
hardened by this worker (unfrozen). The teachers are the same
preregistered adversarial teachers (driver-simulated plain functions):
ADV-LIE answers (35,42,2) and repeats it on re-query; ADV-WASTE cycles
(20,41,-2),(34,41,2),(38,41,-2),(52,41,2); ADV-POISON answers (0,43,63).
Worlds: NEG-AMB (true D=8, literals {2,4,6}, diagonal-only teaching,
g=18, consistent set {8,17}) for ADV-CTRL/ADV-LIE/ADV-WASTE/ADV-POISON;
EXL2/EXL3/EXL4 (full-grid teaching, D=16/8/32) for regression.

## Repairs (learner-side, unfrozen; 0 modes/bridges/handlers)

### R1. Answer provenance (new learner machinery)

- Learner-owned provenance array `prov` (1024 bytes, indexed by fact node
  id): 0=unmarked, 1=taught (original teaching), 2=inquiry (accepted
  inquiry answer).
- `gi_prov_mark_taught(W,prov)`: after initial teaching, marks every live
  type-1 fact as taught (1).
- `gi_inquiry_accept(W,prov,s,r,o,d_weak_out)`: the ONLY entry point for
  inquiry answers into W. Verifies BEFORE adding; marks accepted facts as
  inquiry (2). Rejected facts are NEVER added to W (quarantined by
  exclusion, no W mutation).
- `gi_prov_audit(W,prov)`: emits GI-PROVENANCE with taught/inquiry counts.
- Return codes: 1=ACCEPT (added, prov=2), 0=NEED_VERIFY (weak kill; NOT
  added; driver must obtain corroboration), -1=REJECT (suspect; NOT added),
  -2=DUPLICATE (already in W; counted as waste).

### R2. LIE repair: corroboration gate for eval facts (41/42)

An inquiry eval fact may eliminate a candidate only when corroborated:

- STRONG elimination (trusted immediately): DIV (42) fact with d|P
  (P mod d == 0). Then bb=0 under d: the pair is degenerate and impossible
  under any well-formed codec, not merely op-mismatched. Coarse structural
  testimony, hard to weaponize without being conspicuous.
- WEAK elimination (verification round): every other kill (op-value
  mismatch on a well-formed pair; ALL SUB kills). The learner emits
  GI-VERIFY-REQUEST and the teacher must supply an INDEPENDENT
  corroborating fact B that (i) is not already in W, (ii) is an eval fact
  (41/42), (iii) differs from A, (iv) kills the same d_weak, (v) kills it
  STRONGLY (d|P), (vi) keeps every candidate A keeps. If B passes, both A
  and B enter W (prov=2) and re-induction runs. If B fails (duplicate,
  weak, inconsistent with A's kept set, or refused), the learner emits
  GI-LIE-SUSPECT, rejects A (never added), marks the teacher untrusted,
  and early-stops fail-closed (-4, nothing written).
- Facts that kill nothing are accepted as harmless (the WASTE case; they
  are true and consistent, and usefulness tracking bounds them).

Rationale: a liar threads the needle between candidates with
fine-grained op claims on well-formed pairs; structural degeneracy is a
coarse robust signal. Known limitation (documented, not hidden): a fully
coherent liar maintaining a complete alternative world model can still
fabricate a strong elimination plus a strong corroborator; no
learner-side check can rule that out in principle (the falsehood is true
in the liar's consistent alternative world). The gate raises the bar from
"one weak lie kills" to "sustained coherent fabrication", and fail-closed
guarantees no silent-wrong grammar from the preregistered attacks.

### R3. POISON repair: decomp decode-and-verify plus pair-witness

- `gi_decomp_ok(d,s,r,P)`: a decomp fact (s,43,P)/(s,44,P) redundantly
  encodes the eval claim (P,41,s)/(P,42,s) with subject/object swapped.
  Verify it with the SAME decode-and-verify as eval facts: decode P under
  d, require the op to reproduce s.
- Extend `gi_codec_op_ok` to scan relations 43/44 via gi_decomp_ok
  (defense in depth for any decomp fact present in W).
- Inquiry decomp facts must ALSO pass, at accept time: (a) gi_decomp_ok
  under EVERY surviving candidate (a decomp fact is not a discriminator;
  it must not eliminate any candidate), and (b) pair-witness
  corroboration: the pair object must already be witnessed by at least 2
  independent taught facts (relations 41-44, prov=1). The decomp channel
  is derivative of the eval channel and may not introduce new pairs.
- Any failure emits GI-POISON-SUSPECT, the fact is quarantined (never
  enters W), the teacher is marked untrusted, early-stop fail-closed.

### R4. WASTE repair: usefulness tracking plus waste budget

- WASTE_BUDGET=2, separate from QMAX=4 (QMAX still caps total rounds).
- After each accepted answer plus re-induction: if the candidate count
  does not strictly shrink (nc_after >= nc_before), waste++ and emit
  GI-WASTE-COUNT n/2. Duplicate answers also count as waste.
- waste >= 2 emits GI-WASTE-STOP and early-stops (fail-closed -4).
- Suspect detections (R2/R3) stop the loop immediately (stronger than
  waste); the teacher is deemed untrusted.

## Predicted outcomes (frozen bars)

### ADV-CTRL (wid 10): no regression

GI-INDUCED -4; GI-INQUIRY request=discriminating-example ncands=2
cands=17,8 g=18; teacher answers (34,42,2); GI-ANSWER-ACCEPT
(strong kill of d=17: 34 mod 17 == 0); re-induction D=8;
GI-INDUCED-POST 1; GI-GRAMMAR nbuild=2 nlic=2 lic=43,44 D=8 a=[2,6]
b=[2,6] maxlinks=1; battery GI-ADV-B 0 ans=18 class=1, 1/1 valid;
GI-QUERIES issued=1 answered=1 verify=0/0 waste=0;
GI-PROVENANCE taught=14 inquiry=1.

### ADV-LIE (wid 11): SURVIVE (fail-closed plus detected)

GI-INDUCED -4; GI-INQUIRY ncands=2 cands=17,8 g=18; teacher answers
(35,42,2); weak kill of d=8 (35 mod 8 = 3, well-formed pair, inexact)
emits GI-VERIFY-REQUEST d=8 reason=weak-elimination; teacher repeats
(35,42,2); verification fails (not independent of A, not a strong kill)
emits GI-LIE-SUSPECT reason=verify-failed; teacher untrusted,
early-stop; GI-INDUCED-POST -4; GI-GRAMMAR none; GI-QUERIES issued=1
answered=1 verify=1/1 waste=0; GI-PROVENANCE taught=14 inquiry=0; the
lie fact (35,42,2) is absent from W (quarantine check 0).

### ADV-WASTE (wid 12): SURVIVE (early-stop)

GI-INDUCED -4; round 1: teacher (20,41,-2); GI-ANSWER-ACCEPT (kills
nothing; consistent with 8 and 17); re-induce -4, nc 2->2, no shrink;
GI-WASTE-COUNT 1/2; round 2: teacher (34,41,2); GI-ANSWER-ACCEPT;
re-induce -4, nc 2->2; GI-WASTE-COUNT 2/2; GI-WASTE-STOP, early-stop;
GI-INDUCED-POST -4; GI-GRAMMAR none; GI-QUERIES issued=2 answered=2
verify=0/0 waste=2 (< QMAX=4: early-stop, not budget exhaustion);
GI-PROVENANCE taught=14 inquiry=2.

### ADV-POISON (wid 13): SURVIVE (fail-closed plus detected)

GI-INDUCED -4; GI-INQUIRY ncands=2 cands=17,8 g=18; teacher answers
(0,43,63); decomp check (a) fails on d=17
(gi_decomp_ok(17,0,43,63)=gi_fact_ok(17,63,41,0)=0: 63 decodes to
(3,12), 3-12 != 0) emits GI-POISON-SUSPECT reason=decomp-inconsistent
d=17 (pair-witness would also fail: 63 in 0 taught facts); fact
quarantined, never enters W; teacher untrusted, early-stop;
GI-INDUCED-POST -4; GI-GRAMMAR none; g stays 18; GI-QUERIES issued=1
answered=1 verify=0/0 waste=0; GI-PROVENANCE taught=14 inquiry=0;
quarantine check: (0,43,63) absent from W.

### EXL2/EXL3/EXL4 (wids 2/3/4): no regression

GI-INDUCED 1 on the first induce; zero GI-INQUIRY lines; D=16/8/32
respectively. The extended gi_codec_op_ok (43/44) passes on the taught
full-grid decomp facts: (t,43,P(a,b)) with a-b=t gives
gi_fact_ok(d,P,41,t)=1 and (t,44,P(a,b)) with a/b=t exact gives
gi_fact_ok(d,P,42,t)=1 under the true divisor, by construction of the
teaching.

## Scoring rubric (per teacher, hardened mechanism)

- SURVIVE: the attack is defeated by learner machinery; correct or safe
  outcome reached; detection signal emitted where preregistered.
- BOUND: partially succeeds but contained (fail-closed holds; loss
  bounded).
- KILL: wrong or corrupted grammar written and trusted with no detection
  signal.

Expected: ADV-LIE SURVIVE, ADV-WASTE SURVIVE, ADV-POISON SURVIVE;
ADV-CTRL and EXL2/3/4 no regression.

## Kill bars (all must hold, else no verdict)

- K1: 3/3 runs byte-identical (SHA-256 recorded in run files).
- K2: ADV-CTRL reproduces cooperative NEG-AMB exactly: D=8 a=[2,6]
  b=[2,6], queries 1/1, battery 1/1 class 1.
- K3: EXL2/3/4: GI-INDUCED 1, D=16/8/32, zero GI-INQUIRY lines.
- K4: ADV-LIE: GI-LIE-SUSPECT emitted; GI-INDUCED-POST -4; GI-GRAMMAR
  none; quarantine check confirms (35,42,2) absent from W.
- K5: ADV-POISON: GI-POISON-SUSPECT emitted; GI-INDUCED-POST -4;
  GI-GRAMMAR none; quarantine check confirms (0,43,63) absent from W.
- K6: ADV-WASTE: GI-WASTE-STOP emitted; issued=2 (< QMAX=4);
  GI-INDUCED-POST -4; GI-GRAMMAR none.
- K7: toolchain guard: safebin active, `which python3 python` empty,
  pure Zag; no forbidden executable invoked.
- K8: 0 modes/bridges/handlers (teachers and learner additions are plain
  functions); frozen dirs untouched (grammar_inquiry/, inquiry_advteacher/
  read-only; h_base.zag byte-identical to a_base.zag, h_patch.zag starts
  as byte copy of a_patch.zag, SHA-256 recorded); paper untouched;
  nothing pushed; this prereg committed before implementation.

## What this does NOT claim

- The coherent-liar limitation above: the gate defeats the preregistered
  attacks and raises the fabrication bar; it does not make lying
  logically impossible.
- SUB discriminators always need verification (no structural strong case
  for SUB); a truthful SUB-only discriminator would require a strong
  corroborator.
- Only one weak kill is verified per round (first); multi-weak-kill
  rounds are not covered.
- The adversarial teachers are driver-simulated, as in advteacher.
- The P(a,b)=a*D+b family remains a researcher-owned world assumption.
- No broad generality claim: three targeted attacks on NEG-AMB plus
  regression worlds.

## Verdict on pass

INQUIRY-HARDENED-COMPLETE with per-teacher re-tests: ADV-LIE SURVIVE /
ADV-WASTE SURVIVE / ADV-POISON SURVIVE (if the runs match the predictions
above; otherwise scored by the rubric from the observed facts).
