# N17 R25 lineage requirements

The recovered R26 digest and verifier link to R25 material. N17 cannot claim
full continuity while treating that linkage as a literal witness only.

## Static lineage record recovered so far

The 2026-09-08 source-recovery report statically records these exact original
member hashes. They are provenance leads, not native R25 inputs and not proof
that the corresponding bytes are present in this N17 directory:

| Required member | Recorded SHA-256 | N17 availability |
| --- | --- | --- |
| `src/r25_experiments.py` | `c8c40fbdeba5c9e8067bf83499f7c6c581c8c2234988c875a41f25e69b30b880` | absent |
| `src/r25_release.py` | `41f32d0fd2c94c8dec28d516bd2caeecdda8a868f76e8c08558a5e04d5473a57` | absent |
| R25 accepted state | exact member path/bytes not recovered into N17 | absent |
| R25 release manifest | exact member path/bytes not recovered into N17 | absent |
| R25 accepted policy/receipt | exact member path/bytes not recovered into N17 | absent |

The recorded `r25_sha256` value inside the accepted R26 parent is also not
enough by itself: native closure needs the exact accepted-state bytes and the
source-defined linkage semantics bound to individual input hashes. Until those
are copied or otherwise immutably bound into the N17 source index, the R25
dependent rows remain `DEFERRED_BLOCKER`.

Before the native R26 digest or full verifier can be frozen, one of the
following must happen:

- the exact R25 accepted-state/source/manifest witnesses and their individual
  hashes are added to the immutable N17 source index, then mapped into native
  supported views; or
- the affected R25-dependent checks are explicitly classified as
  `DEFERRED_BLOCKER`, which prevents the full-continuity disposition.

The historical R25 receipt may corroborate provenance but cannot substitute for
native recomputation. No recursive R25 digest implementation may be invented;
the native boundary must follow the recovered source's actual R26 digest
preimage and its reviewed R25 linkage semantics.

## Admission checklist

The following fields must be non-null before R26 digest implementation review:

1. R25 accepted-state member path, size and SHA-256;
2. R25 source-member paths, sizes and SHA-256s for every source function used
   by the recovered linkage/verifier;
3. R25 release-manifest path, exact bytes and SHA-256;
4. R25 accepted-policy and historical receipt paths, exact bytes and hashes;
5. native map selectors for every R25-linked field actually consumed by the
   R26 digest or verifier; and
6. negative fixtures for changed linkage, missing member, manifest tamper and
   witness-literal substitution.
