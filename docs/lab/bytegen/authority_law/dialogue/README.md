# Dialogue — authority law instantiation (plan absolute)

Implements Micah's APPROVED option B for the dialogue path (2026-09-24):
**no output feedback authority. The plan is absolute.** Dialogue FAILS T3
categorically: output is propositional content; re-ingesting it risks
constructed→belief leakage. T1/T2 are vacuous (no sensor, no noise, no
plan-independent fault class).

## The rule, as built

1. **No emitted byte may ever enter** a retrieval key, a salience/topic
   structure, the user-claim store, the KB, or any tie-break, weight, or
   score used by generation. Enforced structurally:
   - `poison(port, emitted_bytes, len)` enumerates all 7 forbidden ports
     (retrieval-key, salience, topic, user-claim-store, KB, tie-break,
     score) and refuses them all (`NO_SUCH_PORT`): the composer exposes no
     input port for emitted bytes anywhere.
   - `uc_install_gated(..., prov)` accepts only `prov=USER`; system-composed
     claims (`prov=SELF`) are refused — the B1 wall.
   - `kb_write_guard` enforces write-once KB at install — the B1 wall, part 2.
2. **Grandfathered** (per AUTHORITY_RECOMMENDATION.md): the `last_fid`
   integer-id exact-tie preference (plan-side id, tie-only, never overrides
   a strictly better score); the correction branch excludes the previous
   answer fid (plan keeps last word).
3. **Deliberation-layer veto** (`check_response`): reads the *plan* (KB
   facts, committed candidate set, uc, discourse state) as ground truth and
   the composed text only as the artifact under test (defendant, never
   witness). Its only power: veto → plan-pure re-composition
   (`recompose_plan_pure`). It may not edit, blend, or arbitrate using the
   response's own content. Correction map constant in the checked text
   (dialogue Lipschitz-0): same plan fault → same re-composition,
   regardless of phrasing.
4. **Constructed-mode air-gap**: `joke:`/`imagine:` utterances compose from
   explicitly-marked constructed templates, touch no store, and are never
   eligible as checker input against the belief store.

## Files

- `dialogue_plan_absolute.zag` — the instantiation + adversarial probes.
- `dialogue_evidence.txt` — full probe output (SHAs included).
- `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag` — pinned integrity
  substrate (copied from `GOALB_STORY/src`).

## Build / run

```
cd ~/workspace/tnn-lab/bytegen/authority_law/dialogue
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 dialogue_plan_absolute.zag -o dialogue_bin
./dialogue_bin all        # B1, B2, veto, rerun
./dialogue_bin b1|b2|veto|rerun
```

Pure Zag, deterministic, zero RNG. `dialogue_bin` is a build artifact and
is NOT committed.

## Verification (see dialogue_evidence.txt)

- **B1** learning-from-own-output: KB write refused (`KB_FROZEN`), SELF
  claim install refused, all 8 port-poison attempts refused →
  **0 installs**.
- **B2** repeat-bias: 3 repeats of the same query with different
  `last_fid` seeds → same winner, byte-identical score vectors; exact-tie
  query flips winner with the plan-side id while scores stay identical →
  repetition is never evidence.
- **VETO**: planted plan-side fault (forbidden uc-override composition
  "the eiffel tower was built in 2000."):
  checker vetoes (`SRC_NOT_KB`); the subtler lie (claims KB source while
  contradicting the plan) vetoed (`COMPOSITION_INVARIANT`); a stale
  committed set (revoked fid still emitted) vetoed (`STALE_FID`).
  Plan-pure re-composition is **byte-identical** to composing from the
  corrected plan directly (SHA
  `8d4e9d6ab78032998d2c2cd6add8f6ded48eb8e9880cb164cc67a3903886b321`
  both sides), and **constant in the checked text** (two phrasings of the
  same fault → identical re-composition).
- **RERUN**: 8-turn mixed session (retrieval, assertion, constructed,
  correction) ×3 → byte-identical transcripts (SHA
  `72448e50aa81b2fd3bce70880c64f60881b08a366af9bf51d7a9bd61f17498ea` ×3).

Note: the frozen preregistered battery is NOT run here (needs Micah's
signature; a sibling crew is drafting it). These are smoke-level probes.
