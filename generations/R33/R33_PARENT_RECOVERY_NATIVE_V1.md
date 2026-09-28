# R33 accepted-parent materialization and native byte custody

Date: 2026-09-05 Pacific. This closes an artifact-recovery step, not parent
semantic migration, learner qualification or an R33 experimental primary.

## Exact materialized parent

Source container: `Research/tnn-pre-v1-r28-aeif-no-graph-shadow.zip`, SHA-256
`b155570237d1560b82dcf5fd9ea7771772899ec06c19bef5b74438c517fac5b6`.
Member prefix: `tnn-pre-v1-r28-aeif-no-graph-shadow/`.
The preceding continuation exclusively materialized the following members into
`Research/R33_PARENT_RECOVERED_V1/`; this continuation verified the retained
copies and removed their write bits. The original archive was not modified.

| Archive member below prefix | Saved filename | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `state/parent-r27-accepted-state.pkl` | `parent-r27-accepted-state.pkl` | 15871908 | `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a` |
| `state/parent-r27-accepted-policy.json` | `parent-r27-accepted-policy.json` | 712 | `983db6a9c771f4952392d288459d65dfb04c33a7cbca37ac9f10a4365c7887a8` |
| `state/LINEAGE.txt` | `LINEAGE.txt` | 246 | `43553e7315a1105657240d31f503cf8c385670254a9fbf3f579d8f0c3a3a2a92` |
| `verification/r27_parent_rerun.log` | `r27_parent_rerun.log` | 404 | `67a74e11090f57aa0084924735f096d6bdc55e7f7514da4ce078e01aff8be349` |

All four recovered copies now have mode0400. These permissions reduce accidental
edits; they are not protection against a hostile owner or a signed trust root.
An archive-path verification corrected the narrative's initial LINEAGE locator
to `state/LINEAGE.txt`; no member bytes, native result or identity changed.

## Native verification actually completed

Verified all ten source/build pins from `R33_NATIVE_N02A_FREEZE.json`. Invoked
the already-qualified native N02A binary in its read-only `file` utility mode,
not its consumed `check` experiment mode. The previous attempted invocation was
not dispatched at compaction; this is the first executed invocation against this
new materialization. Exact arguments:

```
Research/R33_NATIVE_N02A_BUILD_01/n02a file Research/R33_PARENT_RECOVERED_V1 parent-r27-accepted-state.pkl 31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a
```

Observed exit0 and three matching checks: hashing returned0, file digest matched,
and the output-tail sentinel remained211. No object loading, deserialization,
legacy source execution, learner or Python was involved. Host elapsed2.21s,
user2.15s, system0.02s, maximumRSS48,906,240bytes. This is byte identity only.

Retained stdout SHA-256:
`4b4d08e6afd8fde07ba273556d7d2e74ae1cf35d082c475f4508878b791f4f49`.
Retained host resource log SHA-256:
`c394db4d843e7e585d4e3b4f852c318daace5ee9f56422b50d60c4a34dea0e7a`.
Both logs are in the recovered directory and were created without replacement.

## Bounded follow-up recovery evidence

The preceding continuation retained observations under
`R33_PARENT_RECOVERY_FOLLOWUP_20260905/`; they are not new experimental populations.
The recorded remote inventory has four heads and no additional tag. The saved
unreachable-object inventory has six trees and25 blobs. The small-blob search
record covers24 blobs; the4,259,280-byte blob was separately searched and its
saved match output is empty. The checkpoint identifies that large blob as an
E50 Zag manifest, not original R27 source. These are bounded negative searches,
not proof of global absence or a semantic verification of every object.

The retained Drive checksum names the full-backup TAR.GZ and asserts
`f966c0c7f1649feb1e83436b21d7c51a41442e8a9f3f4f41c33f08affbb3d748`, matching
the already audited local backup identity. Remote chunks were not downloaded,
reassembled or freshly rehashed; the checksum alone does not independently
verify remote contents. The recorded Downloads inventory did not identify a new
original-source release. Unrelated software archive contents were not opened.
The checkpoint also records an empty GitHub release listing and no useful
default-branch code-search hit; those responses were not retained as local raw
artifacts and are not claimed to be covered by the manifest.

A targeted prior-context lookup in this continuation returned historical release
names/checksum and33-check metadata, but no new download URL, attachment ID or
original-source locator. It supplies no additional executable source recovery.

## Unclosed dependency and honest next work

The original eleven custom modules, original R27 semantic-digest implementation
and field selection/canonicalization, original full verifier, and source-derived
runtime/transitive dependency closure remain unlocated in the searched scopes.
See `R33_PARENT_MIGRATION_DEPENDENCIES.md` and
`R33_PARENT_SOURCE_RECOVERY_EXTENSION.md` for exact unresolved mappings.

The semantic digest `562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04`
is inherited metadata, NOT the byte hash above and NOT recomputed here. The
historical33/33PASS log was preserved, not rerun. No learned field, alias,
optimizer/RNG state, external storage, pending action or legacy capability has
been certified as migrated. Graph/BPE/VAD-bearing historical objects stay inert;
their existence is not authority to activate prohibited mechanisms or replace
missing/null state with a newborn.

R27 remains canonical at step60423/restarts0. Sixteen consumed diagnostic batches,
zero R33 training runs, no promotion or new learner grant. Continue native
authorization and complete-state/causal foundations while original-source
continuity remains an explicit training prerequisite.
