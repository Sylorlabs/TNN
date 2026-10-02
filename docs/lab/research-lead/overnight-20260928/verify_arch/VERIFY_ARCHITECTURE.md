# Verification Subsystem: Unified Architecture Specification

Date: 2026-09-30 UTC
Author: Verification Architecture Documenter
Status: ARCH-DOCUMENTED (document only; no implementation)

This document consolidates three committed verification phases into
one coherent subsystem specification. Every claim below is traceable
to a committed prereg, implementation, and result. The subsystem is a
builder-verified PASS through all three phases, not an L3 invention
claim and not a SURVIVES verdict.

## 1. Phase lineage (evidence)

| Phase | Name | Prereg | Implementation/Result | Verdict |
|-------|------|--------|-----------------------|---------|
| 0 | Attack | dce1f3d6e | 483b0e61f | VERIFY-TESTED |
| 1 | Passive verification build | 82ab9f40e | a07f9b9a6 | BUILD-PASS |
| 2 | Active verification build | 7e178c075 | 1c92aa353 | BUILD-PASS |

Phase 0 (verify_attack/): an adversarial test of the unmodified v6
contestant across five lying-oracle worlds (V1..V5). All five
hypotheses CONFIRMED: silent self-contradiction (V1), lie beats
teacher (V2), correction without detection (V3), relation overwrite
in composition (V4), rapid contradiction (V5). DETECT=no,
REVISE=no (overwrite only), PERSIST=yes everywhere. conf_n=0 in
every reply of every world. Verdict: the no-verification bound is
structural, not a missing feature. The phase also froze the
verification specification (VERIFY_RESULT.md sections 1..6) that
serves as the requirements contract for Phases 1 and 2.

Phase 1 (verify_build/): implements the frozen spec as v6_verify.zag,
additive on the unmodified v6 base. Detection, provenance, doubt,
hedging (A3), and source-priority revision (A4). V1..V5 regenerated
from the committed generator now show DETECT=yes everywhere with
conf_n=1, suspect_n=1 per world. V2 demonstrates the named revision
policy changing an answer relative to last-wins (teacher value kept,
lie marked UNCONFIRMED). A no-contradiction control world shows
conf_n=0, suspect_n=0, and byte-identical replies to the v6
baseline: no false positives.

Phase 2 (verify_active/): implements bounded A1 (re-observe) and A2
(compositional cross-check) as v6_verify_active.zag, additive on the
v6_verify base. Two new worlds: V6 demonstrates the full A1 doubt
cycle (lie -> SUSPECT -> hedged reply + one observe request ->
truthful re-observe -> SUSPECT cleared -> bare reply). V7
demonstrates A2 hedging when a suspect remap is compositionally
live. The no-degeneration bound reobserve_n <= suspect_episodes
holds on all worlds and runs; CTL shows zero A1 requests.

## 2. The five-stage pipeline

The subsystem is organized as a pipeline:

  detection -> recording -> hedging -> prioritization -> active investigation

Detection (Phase 1): contradiction detection on the write path of
fact_store and rel_store. Before overwriting an existing slot, the
stored value is compared with the incoming value. On mismatch, a
doubt trigger fires.

Recording (Phase 1): the mismatch is recorded in two places. The
(old,new) pair is routed to the existing conflict store via
conf_store (conf_n increments). Per-slot verification metadata
records the contradiction state: SUSPECT flag, superseded value,
source tag, tick, and episode bookkeeping.

Hedging (Phase 1, action A3): while a fact slot's SUSPECT flag is
set, fact queries return the CONFLICT form "stored|superseded"
instead of a bare value. The learner reports doubt in its answers
rather than silently picking a winner.

Prioritization (Phase 1, action A4, policy P-source-priority): on a
T2 trigger (OBSERVE contradicting an EXPO-taught value), the
teacher's value is kept and the observation is recorded as
UNCONFIRMED in the superseded slot. EXPO beats OBSERVE; newer EXPO
beats older EXPO; OBSERVE beats OBSERVE by last-wins. This is the
only implemented revision policy.

Active investigation (Phase 2, actions A1 and A2): the learner
spends bounded resources to resolve doubt. A1 issues a budgeted
re-observe request for a SUSPECT fact (1 per suspect episode). A2
internally cross-checks a SUSPECT relation slot's current vs
superseded mapping during hop2 composition and hedges when they
differ. A1/A2 are bounded so they cannot degenerate into the
always-observe policy that the generic attack refuted.

## 3. Component specification

### 3.1 Detection

Mechanism: fact_store and rel_store compare the stored value with
the incoming value before overwriting. Same-value rewrites refresh
metadata only and fire nothing.

Doubt triggers (frozen, all implemented in Phase 1):
- T1: observe_result value != stored value for the same (e,a).
  Worlds V1, V5.
- T2: observe_result value != expo-taught value for the same (e,a).
  Worlds V2, V3.
- T3: two observe_results for the same (e,a) disagree with no
  intervening expo. Worlds V1, V3, V5.
- T4: expo relation update changes a stored (a,r) mapping, so a
  composition path may have changed. Worlds V4, V7.

Any trigger firing sets the SUSPECT flag and routes the (old,new)
pair to the conflict store.

Deliberate deviation from the spec's letter: mismatches route via
conf_store directly rather than the full learn_conflict wrapper.
The wrapper would feed derived contradiction strings into the
lexicon as learning events, conflating detection with learning;
conf_store is the conflict machinery's storage and conf_n is the
falsification metric. This deviation is disclosed in the Phase 1
result and was part of the BUILD-PASS.

### 3.2 Recording

Per-fact metadata region VERF at byte offset 13120: 64 entries of
24 bytes, one per fact slot. Per-relation metadata region VERR at
14656: 64 entries of 24 bytes, one per relation slot. Regions are
in previously free state space; no existing offsets move; region
ends 16192; ST_SIZE stays 16384. Existing fact (4928), relation
(8000), and conflict (11072) regions are untouched.

Per-entry layout:
- byte 0: SUSPECT flag (0/1)
- byte 1: source tag (1=EXPO teacher, 2=OBSERVE oracle)
- bytes 2..5: tick of last write (u32)
- bytes 6..21: superseded value (16 bytes)
- bytes 22..23: reserved in Phase 1; claimed by Phase 2 for A1
  budget bookkeeping (byte 22 = re-observes issued in current
  episode, byte 23 = bit 7 corroborated flag, bits 0..6 episode
  id). This reservation is the explicit cross-phase interface.

Global counters (VGLOB region):
- global 16192: T1/T3 trigger count
- global 16196: oracle-unreliable flag (spec T5; counted in Phase
  1, no behavioral gating)
- global +8 (Phase 2): suspect_episodes counter
- global +12 (Phase 2): reobserve_n counter

Provenance: learn_fact and learn_rel take a source parameter. Expo
teachings and corrections are EXPO(1); observe_result turns are
OBSERVE(2). All experience writes pass through the verified
fact_store/rel_store with explicit source tags (source-audited in
Phase 1).

### 3.3 Hedging (A3)

While a fact slot's SUSPECT flag is set, fact queries return the
CONFLICT form "stored|superseded" instead of a bare value. The
hedged form names both the kept value and the recorded alternative.
In Phase 1, hop2 answers over SUSPECT relations are not hedged (V4
detection is via conf_n); Phase 2 adds A2 hedging for that case
(see 3.5).

### 3.4 Prioritization (A4, P-source-priority)

Named revision policy, frozen in the spec and implemented in
Phase 1: EXPO beats OBSERVE; newer EXPO beats older EXPO; OBSERVE
beats OBSERVE by last-wins. On T2 the teacher's value is kept and
the observation is recorded UNCONFIRMED in the superseded slot;
the stored value does not change. V2 is the world where this
policy changes an answer relative to last-wins (the unmodified v6
answered "bogus"; the build answers "v2|bogus" and keeps v2).
The spec names two unimplemented alternatives for future work:
P-last-wins (status quo, rejected) and P-suspend (answer UNKNOWN
while SUSPECT is set, not implemented).

### 3.5 Active investigation

A1 (re-observe, Phase 2):
- Trigger: a fact|e|a (or fact2|e|a) test query hits a SUSPECT
  fact slot AND the per-episode budget is unspent
  (va1_may: vflag==1 AND issued < 1).
- Action: the reply carries BOTH the hedged A3 answer AND an
  observe request for (e,a). The known==0 gate on want_observe is
  lifted ONLY on this SUSPECT-with-budget path (source-audited).
- Budget: 1 re-observe per suspect episode. A 0->1 SUSPECT
  transition starts a new episode (byte 22 reset, episode id
  bumped, global suspect_episodes incremented).
- Stopping rule (on observe_result for a SUSPECT fact):
  incoming == stored: clear SUSPECT, clear superseded, reset
  budget. Doubt resolved by confirmation.
  incoming == superseded: set corroborated bit (byte 23 high);
  P-source-priority still governs; budget exhausted. The hedged
  answer stands with stronger evidence for the alternative.
  third distinct value: superseded is replaced with the new
  value; SUSPECT stays; budget exhausted. The newest
  contradiction is the live alternative.

A2 (compositional cross-check, Phase 2):
- Trigger: a hop2|start|rel1|rel2 query traverses a relation slot
  with SUSPECT set in VERR.
- Action: compute the chain via the CURRENT mapping and via the
  SUPERSEDED mapping, then compare:
  both resolve to the same value: bare answer (the remap is not
  compositionally live on this chain).
  both resolve to different values: hedge as current|alt.
  current resolves, superseded does not: bare current answer.
- A2 is internal computation, never issues observe requests, so
  it cannot degenerate into always-observe. It does not clear
  SUSPECT by itself; it produces evidence a future revision
  policy or A1 can use.

Anti-degeneration invariant (frozen, measured): reobserve_n <=
suspect_episodes on every world and run. An always-observe
degenerate would issue an observe on every test query for every
known fact; the measured counts are bounded by suspect episodes,
and CTL shows zero A1 requests. The bound is the load-bearing
difference between bounded active verification and the refuted
always-observe policy.

## 4. Interfaces between phases

Phase 0 -> Phase 1 interface: the frozen verification specification
(VERIFY_RESULT.md sections 1..6, commit 483b0e61f). It names the
exact v6 functions that change (fact_store, rel_store, the
observe_result handler), the exact new state each carries, the
frozen doubt triggers T1..T4, the frozen verification actions
A1..A4, and the frozen revision-policy options. It also names the
falsification rule for any future verification claim (DETECT=yes on
V1..V5 at least at T1 and T2, plus a new V6 double-lie world with a
hedged reply). Phase 1 implements detection, recording, A3, A4
from this spec and explicitly defers A1/A2 with documented
rationale (the generic attack refuted unbounded re-observation).

Phase 1 -> Phase 2 interface has three parts:
(a) Byte 22..23 reservation: Phase 1 reserves verify slot bytes
22..23 without using them; Phase 2 claims them for episode
tracking (issued count, episode id, corroborated bit). Phase 2
additionally moves no existing offsets.
(b) Behavior preservation: Phase 2 is additive. V1..V5 DETECT=yes
is a regression gate (Phase 2 prereg K2 falsification rule); the
CTL no-contradiction control must match the v6_verify baseline
output modulo the two new metric fields.
(c) Deferred-action handoff: Phase 1 documents A1/A2 as specified
but not implemented, with the exact degeneration risk; Phase 2's
design is bounded A1/A2 addressing that risk, and its K3 bar is
the no-degeneration bound.

External interfaces of the subsystem:
- Write path: fact_store/rel_store carry (slot, value, source);
  callers must pass the source tag (EXPO=1/OBSERVE=2). Any new
  experience writer that bypasses these functions bypasses
  detection; this is the integration contract for future writers.
- Observe path: observe_result calls learn_fact with source
  OBSERVE(2); the A1 stopping rule hooks the same handler for
  SUSPECT slots.
- Reply path: test handlers emit hedged forms when SUSPECT is
  set (A3), optionally attach an A1 observe request, and emit
  reobserve_n/suspect_episodes metrics.
- Composition path: hop2 checks VERR SUSPECT on traversed
  relation slots and applies A2 comparison.

## 5. Test coverage matrix

| World | Trigger | Phase 1 signal | Phase 2 addition |
|-------|---------|----------------|------------------|
| V1 self-contradiction | T1 | conf_n=1, "w2\|w1" | preserved |
| V2 lie vs teacher | T2 | conf_n=1, "v2\|bogus", teacher kept | preserved |
| V3 correction after lie | T2/T3 | conf_n=1, "truev\|bogus" | preserved |
| V4 relation remap | T4 | conf_n=1, remap flagged | A2 hedging when compositionally live |
| V5 rapid contradiction | T1/T3 | conf_n=1, "second\|first" | preserved |
| V6 double lie | T2 then A1 | n/a (new) | full A1 cycle: "v0\|w1" + ask -> confirm -> bare "v0" |
| V7 remap + composition | T4 then A2 | n/a (new) | A2 hedge "altfin\|fin"; sticky SUSPECT after correction |
| CTL no contradiction | none | conf_n=0, byte-identical to v6 baseline | reobserve_n=0, baseline-identical |

All worlds run 3 times with fresh state dirs; cognitive outputs
byte-identical across runs (one distinct md5 per world after
stripping timing fields); all stderr empty; exit 0.

## 6. Kill bar summary

Phase 0 (VERIFY-TESTED): K1 worlds specified; K2 v6 behavior
measured 3-run byte-identical; K3 verification specification
frozen. One read-only python3 byte-check during setup, redone
with shell grep as the verification of record.

Phase 1 (BUILD-PASS): K1 spec implemented (metadata, triggers,
conflict routing); K2 DETECT=yes on V1..V5 with T1 on V1/V5 and
T2 on V2; K3 no false positives on the control world; K4 pure Zag,
zero em/en-dash bytes, 3/3 deterministic. Zero Python.

Phase 2 (BUILD-PASS): K1 bounded A1/A2 implemented (budget of 1,
gate lifted only on SUSPECT-with-budget path); K2 doubt
resolution measured (V6 full cycle, V7 A2 hedging, V1..V5
DETECT=yes regression); K3 no degeneration
(reobserve_n <= suspect_episodes; CTL zero A1); K4 pure Zag,
zero em/en-dash bytes, 3/3 deterministic. One read-only python3
byte-check during development, redone with pure-shell grep as the
verification of record.

## 7. Honest scope: NOT built

The following are documented gaps, not silent omissions:

1. Automatic promotion: when an A1 re-observation matches the
   superseded value, the system corroborates (sets the bit) but
   does not promote the alternative to stored. The stored value
   only changes via a new write through the normal path.
2. Revision from A2 evidence alone: A2 hedges and produces
   evidence, but no revision policy consumes A2 output without
   an EXPO write or a confirming re-observation.
3. Multi-hop A2: cross-check covers 2-hop composition only.
4. Budget above 1: the per-episode budget is hard at 1; whether
   repeated doubt deserves repeated asks is untested.
5. Oracle gating: the oracle-unreliable flag (spec T5) is counted
   but does not gate behavior. No policy discounts or quarantines
   an unreliable oracle.
6. P-suspend: answering UNKNOWN while SUSPECT is set is specified
   but not implemented.
7. SUSPECT is sticky: a teacher correction does not erase the
   contradiction history. The Phase 2 result argues this is the
   conservative correct behavior for provenance, but it means
   long-lived learners accumulate unresolved contradiction
   records; no archival or decay policy exists.
8. Multi-episode correlation: repeated T1/T3 from the same oracle
   marks unreliability, but there is no pattern mining over
   episodes (e.g., learning which sources lie about which
   attributes).
9. Doubt in planning: the verification subsystem lives in the
   inquiry/answer path. It is not integrated with the causal
   planner (F2/F3) or with goal-directed action selection; a
   SUSPECT causal model does not currently gate planning.
10. Transfer: no test shows verification behavior transferring
   to new domains or reusing doubt machinery for new attribute
   families.
11. C0 assessment: the subsystem is researcher-designed
   infrastructure for honest belief maintenance. It does not
   invent representations; it satisfies no part of Criterion 0.
   Its value is as a trust substrate the continuing learner can
   build on, not as an L3 result.

## 8. Integration points for the continuing learner

The subsystem is designed additive on the v6 contestant so the
continuing learner can adopt it wholesale:

- All experience writes flow through fact_store/rel_store with
  source tags; the integration contract is "never write
  experience state through a path that bypasses the verified
  write functions."
- The A1 mechanism is the natural host for the C8 inquiry loop:
  doubt becomes a budgeted ask, compatible with ask-cost
  accounting.
- The A2 mechanism is the natural host for C4 composition:
  suspect remaps are cross-checked where they are used.
- The conflict store (conf_n) is the existing honest metric for
  contradiction load; dashboards and the continuing learner's
  self-monitoring can read it directly.
- Open integration work: wiring SUSPECT into planning gates
  (a suspect causal rule should not drive irreversible action),
  archival of stale contradiction records, and an oracle
  reliability policy that consumes the T5 flag.

## 9. Files and provenance

- verify_attack/PREREG_VERIFY_ATTACK.md (dce1f3d6e)
- verify_attack/VERIFY_RESULT.md (483b0e61f; frozen spec)
- verify_attack/gen_verify.zag (V1..V5 world generator)
- verify_build/PREREG_VERIFY_BUILD.md (82ab9f40e)
- verify_build/v6_verify.zag (a07f9b9a6)
- verify_build/VERIFY_BUILD_RESULT.md (a07f9b9a6)
- verify_active/PREREG_VERIFY_ACTIVE.md (7e178c075)
- verify_active/v6_verify_active.zag (1c92aa353)
- verify_active/VERIFY_ACTIVE_RESULT.md (1c92aa353)
- verify_arch/VERIFY_ARCHITECTURE.md (this file)

All commits are local on branch tnn-native-lab. Nothing pushed.
All three phases: pure Zag implementation and execution; 3/3
byte-identical determinism; zero em-dash or en-dash bytes
(byte-verified); two disclosed read-only python3 byte-checks,
each redone with pure-shell grep as the verification of record.

**Document label: ARCH-DOCUMENTED.** All three kill bars pass:
K1 architecture specified for all three phases; K2 interfaces
defined (spec contract, byte 22..23 reservation, additive
regression gates, write/observe/reply/composition contracts);
K3 limitations documented in section 7.
