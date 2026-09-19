# Lane B continuity audit — 2026-09-15

Completed read-only native engineering audit; full verifier continuity remains
fail-closed. Exact commands, exit codes, source/binary/input pins, exclusions
and row-specific blockers are in `AUDIT.json`, `commands.tsv`, `exits.tsv`,
`FROZEN_FINAL.sha256` and `BINARY_FINAL.sha256`.

The stable compiler `/Users/Shared/micah/Documents/zag/znc` was not replaced.
Frozen native sources freshly reproduced:

- R26: `44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649`
  from 391221 preimage bytes.
- R27: `562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04`
  from 17764 preimage bytes.
- Raw parent and map manifest: unchanged exact expected hashes.
- 38 native parent static rows, three source-line digest rows, and nine
  hash-bound shell policy rows: 50 direct static passes (R27 26; R26 24).
- Native empty/abc SHA known answers and short-output refusal `-7403` with
  a 34-byte unchanged canary; separate wrong-step/restart and null/absent
  static expectations reject as required.

Stored experiment metrics/decisions were inspected, not regenerated. Type
descriptors and map alias equality have zero runtime-equivalence credit.
R27's existing cached R26 preimage value was independently recomputed first;
a fused typed digest dependency service has not been qualified.

## Exact terminal blocker accounting

32 = 7 unresolved R27 source-line rows + 23 unresolved R26 source-line rows
+ V91 native-generator parity + fresh independent closure review.

R27 unresolved: 01, 06, 08, 09, 18, 32, 33.

R26 unresolved: 01, 06–09, 16–22, 34, 38–47. R26-46 is historical witness
only without a native lineage replacement; it is a required native deficit,
not a pass. The other 29 unresolved source rows are deferred blockers.

Minimal input/runtime blockers are recorded for every row in `AUDIT.json`.
Repeated root causes are not extra rows. V2's coarse labels differ from V3's
recovered source-line rows; every V2 row now has a V3 cross-reference or an
explicit obsolete-placeholder disposition. Its three obsolete slots are not
three extra blockers. V3 and the R26 matrix define the 80-row accounting.

R25 runner compilation exits 1 on absent
`r27_native_state_semantics_v1.zag`; exact release input files are not supplied
in the inspected local roots. The enclosing R27 archive manifest/verifier
identities differ from the original R25 gate's expected identities, requiring
explicit release/member disambiguation. No R25 digest/lineage closure claimed.

V91 tests/emitter compile exits 1 (undefined allocation helpers/unsupported
`new` syntax). Subsequent absent-binary attempts exit 127, not test results.
Its native admission gate exits 91 and says CLOSED. Printing 16 expected
oracle literals cannot substitute for native generator reproduction of all
16 exact strings. No V91 source or V92 file was changed by this lane.

## Artifact boundaries

All original review and authoring manifests remain historical witnesses; no
fresh integrity claim is made for their old hashes after current status edits.
`CLOSEOUT.sha256` pins this additive audit and the updated current status
documents. Full known-answer/mutational fixture admission remains incomplete;
the narrow static controls do not close the 20-fixture negative suite.

No Python, Torch, NumPy, pickle/reducer, foreign ML or historical verifier
execution; no learn, learner authority, scientific exposure, successor
promotion, canonical mutation, commit/push/reset/checkout/clean or deletion.
Canonical R27 stays development step 60423, newborn restarts 0.
