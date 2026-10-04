# VERIFY BUILD RESULT: Verification Subsystem (A2 spec implementation)

Date: 2026-09-30 UTC
Builder: Verification Builder (subagent)
Prereg: PREREG_VERIFY_BUILD.md (82ab9f40e, committed alone before
any implementation; ancestor verified via merge-base)
Spec: docs/lab/research-lead/overnight-20260928/verify_attack/VERIFY_RESULT.md
Base: docs/lab/research-lead/overnight-20260928/generic_attack/v6_c4mem.zag
Verdict: **BUILD-PASS. All four kill bars pass.**

## What was built

v6_verify.zag implements the frozen A2 verification specification
as an additive subsystem on the unmodified v6 contestant:

1. **Per-slot verification metadata** (prereg K1). Two new regions
   in previously free state space, no existing offsets moved:
   VERF at 13120 (64 x 24B, one per fact slot) and VERR at 14656
   (64 x 24B, one per relation slot). Per entry: byte 0 SUSPECT
   flag, byte 1 source tag (1=EXPO teacher, 2=OBSERVE oracle),
   bytes 2..5 tick of last write, bytes 6..21 superseded value
   (16B), bytes 22..23 reserved. Region ends 16192; ST_SIZE stays
   16384. Global 16192 holds the T1/T3 trigger count and 16196
   the oracle-unreliable flag (spec T5; counted, no behavioral
   gating in this build).
2. **Contradiction detection on the write path** (spec section 1).
   fact_store and rel_store compare the stored value with the
   incoming value before overwriting. On mismatch the doubt
   trigger fires: the (old,new) pair is routed to the existing
   conflict store via conf_store, the SUSPECT flag is set, and
   the superseded value is recorded. Same-value rewrites refresh
   metadata only; no false positives.
3. **Provenance tags** (spec section 2). learn_fact and learn_rel
   take a source parameter. Expo teachings and corrections are
   EXPO(1); observe_result turns are OBSERVE(2). Four call sites
   updated; no other callers exist.
4. **Doubt triggers T1..T4** (spec section 3, frozen). T1: observe
   != stored. T2: observe != expo-taught. T3: two observes
   disagree with no intervening expo. T4: expo relation remap.
   Observation-path triggers increment the T1/T3 counter; at 2
   the oracle is marked unreliable.
5. **Revision policy: P-source-priority** (named, spec section 5).
   EXPO beats OBSERVE; newer EXPO beats older EXPO; OBSERVE beats
   OBSERVE by last-wins. On T2 the teacher's value is kept and
   the observation is recorded UNCONFIRMED in the superseded
   slot; the stored value does not change.
6. **Verification actions A3 and A4** (spec section 4). A3 hedge:
   while a fact's SUSPECT flag is set, fact queries return the
   CONFLICT form "stored|superseded" instead of a bare value.
   A4 source priority: as defined in the revision policy.
   A1 (re-observe) and A2 (compositional cross-check) are NOT
   implemented: the known==0 gate on want_observe is left intact,
   because the generic attack showed unbounded re-observation
   degenerates into the refuted always-observe policy. This is
   documented scope, not silent omission.

One deliberate deviation from the spec's letter: mismatches are
routed via conf_store directly rather than the full
learn_conflict wrapper. The wrapper would feed derived
contradiction strings into the lexicon as learning events,
conflating detection with learning; conf_store is the conflict
machinery's storage and conf_n is the falsification metric.

## Kill bars

- **K1 PASS.** Contradiction flags, 16B superseded values, source
  tags, and T1..T4 triggers implemented per the frozen layout.
  Source audit confirms all experience writes pass through the
  verified fact_store/rel_store with explicit source tags.
- **K2 PASS.** Worlds V1..V5 regenerated from the committed
  gen_verify.zag and run turn-by-turn with fresh state dirs.
  DETECT=yes on all five where the attack recorded silence:

  | World | Trigger | conf_n | suspect_n | Final reply (was) |
  |-------|---------|--------|-----------|-------------------|
  | V1 | T1 | 1 | 1 | w2\|w1 (was w2) |
  | V2 | T2 | 1 | 1 | v2\|bogus (was bogus) |
  | V3 | T2/T3 | 1 | 1 | truev\|bogus (was truev) |
  | V4 | T4 | 1 | 1 | X, relation remap flagged |
  | V5 | T1/T3 | 1 | 1 | second\|first (was second) |

  V2 is the world where P-source-priority changes the answer
  relative to last-wins, as the spec requires: the teacher's
  value v2 is kept, the oracle's lie is marked UNCONFIRMED, and
  the reply is hedged. The bare-value silence is gone everywhere.
- **K3 PASS.** A no-contradiction control world (teach, ask,
  idempotent re-teach of the same value, observe-missing,
  re-ask, relation teach, hop2 ask) run on both the unmodified
  v6 baseline and v6_verify: conf_n=0 and suspect_n=0 on both,
  and the full reply streams are byte-identical (same md5
  43ddb77c9b831b16eab02f12e988e8ce after stripping only timing
  fields and the new suspect_n metric). No false positives;
  normal learning is unaffected.
- **K4 PASS.** Pure Zag at every stage: source, znc build,
  execution, analysis. Zero Python invocations. Zero em-dash or
  en-dash bytes in committed files (byte-checked). All six
  worlds (V1..V5 plus control) run 3 times with fresh state
  dirs; cognitive outputs byte-identical across runs
  (3/3 each). All stderr empty, exit 0.

## Honest scope

This build implements detection, provenance, doubt, hedging,
and source-priority revision. It does not implement re-observe
(A1) or compositional cross-check (A2), and hop2 answers over
SUSPECT relations are not hedged (V4 detection is via conf_n).
The oracle-unreliable flag is counted but does not gate
behavior. The no-verification bound is now a no-*active*-verification
bound: the contestant detects, records, hedges, and prioritizes
sources, but does not yet spend asks to resolve doubt.

## Files

- PREREG_VERIFY_BUILD.md (prereg, 82ab9f40e)
- v6_verify.zag (implementation)
- V1_VERIFY_RAW.txt .. V5_VERIFY_RAW.txt (run 1 replies; runs
  2/3 byte-identical)
- CTL_VERIFY_RAW.txt (control world replies)
- VERIFY_BUILD_RESULT.md (this file)

**Builder label: BUILD-PASS** (K1/K2/K3/K4 all pass; no bar altered)
