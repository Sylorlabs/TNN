# PREREG: Verification Subsystem Build (A2 spec implementation)

Date: 2026-09-30 UTC
Builder: Verification Builder (subagent)
Spec: docs/lab/research-lead/overnight-20260928/verify_attack/VERIFY_RESULT.md (frozen, 483b0e61f)
Base: docs/lab/research-lead/overnight-20260928/generic_attack/v6_c4mem.zag (unmodified v6)
Attack worlds: docs/lab/research-lead/overnight-20260928/verify_attack/gen_verify.zag (V1..V5)

This prereg is committed alone BEFORE any implementation. No source
has been written or modified at the time of this commit.

## Frozen kill bars

- K1: Spec implemented. Per-slot verification metadata: 1-byte
  SUSPECT flag, 16-byte superseded value, 1-byte source tag
  (EXPO=1 vs OBSERVE=2), 4-byte tick of last write. Doubt triggers
  T1..T4 implemented on the write path of fact_store and rel_store.
  Write mismatches route to the existing conflict store (conf_store).
- K2: V1..V5 (regenerated from committed gen_verify.zag) show
  DETECT=yes where the attack recorded silence. DETECT=yes means
  conf_n > 0 or a hedged/CONFLICT-form reply on the turn where the
  attack got a bare last-wins value. Minimum bar: conf_n > 0 on
  all five worlds, with T1 firing on V1/V5 and T2 firing on V2.
- K3: Normal learning unaffected. A no-contradiction control world
  (teach facts, ask, observe missing fact, re-ask, relation teach,
  hop2 ask) must produce conf_n = 0, zero SUSPECT flags, and
  byte-identical cognitive replies to the unmodified v6 baseline.
  No false positives.
- K4: Pure Zag at every stage (source, build via znc, execution,
  analysis). Zero Python invocations. Zero em-dash or en-dash
  bytes in committed files (byte-checked via grep). Each world
  run 3 times; cognitive outputs byte-identical across runs.

## Revision policy (named, per spec section 5)

P-source-priority: EXPO beats OBSERVE; newer EXPO beats older
EXPO; OBSERVE beats OBSERVE by last-wins. On a T2 trigger
(OBSERVE contradicting EXPO), the EXPO value is kept and the
observation is recorded as UNCONFIRMED (superseded slot holds
the rejected observation); the reply is hedged. This policy
must change at least one answer relative to last-wins (V2 is
the predicted case: v6 answered "bogus"; this build must not).

## Verification actions implemented

- A3 (hedge): while a fact's SUSPECT flag is set, fact queries
  return the CONFLICT form "stored|superseded" instead of a bare
  value.
- A4 (source priority): as defined in the revision policy above.
- A1 (re-observe) and A2 (compositional cross-check): specified
  in the frozen spec but NOT implemented in this build. The
  known==0 gate on want_observe is left intact; the generic
  attack showed unbounded re-observation degenerates into the
  refuted always-observe policy. Documented as future work, not
  silently omitted.

## Doubt triggers (frozen)

- T1: observe_result value != stored value for the same (e,a).
- T2: observe_result value != expo-taught value for the same (e,a).
- T3: two observe_results for the same (e,a) disagree with no
  intervening expo.
- T4: expo relation update changes a stored (a,r) mapping
  (composition path may have changed).

Any trigger firing sets the SUSPECT flag and routes the
(old,new) pair to the conflict store.

## State layout (additive only; no existing offsets move)

- VERF base 13120: 64 entries x 24B. Per fact slot:
  byte 0 SUSPECT flag, byte 1 source tag, bytes 2..5 tick (u32),
  bytes 6..21 superseded value (16B), bytes 22..23 reserved.
- VERR base 14656: 64 entries x 24B, same layout per relation slot.
- Region ends 16192. ST_SIZE stays 16384. Existing fact (4928),
  relation (8000), and conflict (11072) regions are untouched.

## Falsification

This build FAILS if: conf_n = 0 on any of V1..V5; or the
no-contradiction control world shows conf_n > 0 or any reply
differing from the v6 baseline; or any K4 purity check fails.

## Bar discipline

No kill bar is altered after results. If the implementation
misses a bar, the verdict is BUILD-FAIL with the miss named.
