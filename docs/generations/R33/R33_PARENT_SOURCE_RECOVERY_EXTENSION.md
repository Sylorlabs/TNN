# R33 parent source-recovery extension

Reviewer: GPT-6 Pro. Date: 2026-09-05.

Status: **EXTERNAL BACKUP LOCATED; NO ORIGINAL R27 CLASS/DIGEST SOURCE RECOVERED.**

Repository: `/Users/Shared/micah/Documents/TNN/TNN`.

This report extends the completed parent-payload and dependency audits without repeating their 14-archive or reachable-history searches. The extension used shell filesystem searches, archive listing/text streaming, byte hashing, and read-only Git object inspection. Python source was treated only as frozen text: no Python interpreter, legacy import, pickle load, reducer, learner, generator, migration, or experiment was run. No implementation or evaluator was authored. This Markdown report is the only file written by this task.

## 1. Inherited evidence and the changed implementation rule

The two earlier reports were read as needed and their actual SHA-256 values checked:

| Existing report under the repository's `Research/` directory | SHA-256 |
| --- | --- |
| `R33_PARENT_PAYLOAD_AUDIT.md` | `17a13c4c922ac55d20faf1f0b3c88923184317607e2072676e1901f081e84383` |
| `R33_PARENT_MIGRATION_DEPENDENCIES.md` | `47f5b2986a62727f8c821fc882c7b3a5464b7b35988266ce39e49048b064b6aa` |

Those reports establish the availability of the historical accepted parent bytes, root step60423/restarts0, and the remaining source/runtime gaps. Their completed observations were not rerun here. The historical parent-file SHA-256 remains `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a`; the separately reported accepted semantic digest remains `562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04`.

The latest instruction supersedes any earlier suggestion to execute recovered Python dependencies: historical source, if recovered, is evidence for static examination only. All new implementation, supervision and evaluation must be native Zag. This extension neither recreates the old runtime nor implements a replacement.

## 2. External filesystem search: actual scope and results

Both authorized roots exist:

- `/Users/Shared/micah/Documents`
- `/Users/Shared/micah/Downloads`

The recursive `find -P` search excluded the entire repository `/Users/Shared/micah/Documents/TNN/TNN` and directories named `.git`. It did not follow symbolic links. Case-insensitive basename-prefix searches covered the original bundle name `tnn-pre-v1-r27-general-learning*` and all eleven module stems below, including filename suffixes such as `.py` or download companions:

`r27_experiments`, `r26_experiments`, `r25_release`, `r25_experiments`, `r23_experiments`, `r22_experiments`, `r21_experiments`, `r20_experiments`, `r18_experiments`, `r17_experiments`, `r15_master_training`.

**Result: no matching file or directory names; the search completed with exit 0.** This is a filename-search result, not a content audit of every external file.

A separate archive-candidate pathname search in the same bounded roots selected ZIP, TAR, TAR.GZ, TGZ, TAR.XZ, TAR.BZ2, and ZIP/TAR.GZ download-companion names whose paths contained TNN or a relevant R15/R17/R18/R20/R21/R22/R23/R25/R26/R27 identifier. Its only result was:

`/Users/Shared/micah/Downloads/TNN_COMPLETE_R1_R32_FULL_BACKUP.tar.gz`

A shallow directory check also identified the existing `Documents/TNN`, `Documents/TNN/TNN-R1`, and `Documents/TNN/TNN-R1-Audit` locations. Their previously reviewed contents were not reopened. No global home-directory or personal filesystem search was performed.

## 3. Additional backup: measured identities and inspection

Absolute container path: `/Users/Shared/micah/Downloads/TNN_COMPLETE_R1_R32_FULL_BACKUP.tar.gz`

Size: **588,814,209 bytes**.

Actual container SHA-256: **`f966c0c7f1649feb1e83436b21d7c51a41442e8a9f3f4f41c33f08affbb3d748`**.

Its complete outer member listing succeeded and contained **1,190 entries**, including directories. No outer member component began with any requested module stem or the original R27 bundle name. No `.git/HEAD`, `.git/index`, or `.git/objects/pack/` member was found by the corresponding pathname filter.

All **147 outer `.py` members** were streamed to `rg` as text, not imported or executed. The search included all eleven module stems, `R27State`, the original bundle name, and the full expected semantic-digest string. It produced no matches. The source-count pipeline returned `0 0`; the text-search pipeline returned `0 1` (archive read successful, no regex match). These are targeted text checks, not a full semantic review, and they do not descend into nested archives.

### Nested recovery copies, not new original sources

The following members were independently streamed from this external backup and hashed, without disk extraction or opening their internal source contents:

| Exact member inside the backup | Actual member SHA-256 | Interpretation |
| --- | --- | --- |
| `TNN/Research/tnn-r27-native-master-shadow.zip` | `bfd755a76bff995bd8373fa88ed5922716a21c8926d7703199dc62ffe03e55ce` | Byte-identical to the R27 shadow archive already audited; not the original R27 source release |
| `TNN/Research/tnn-pre-v1-r28-aeif-no-graph-shadow.zip` | `b155570237d1560b82dcf5fd9ea7771772899ec06c19bef5b74438c517fac5b6` | Byte-identical to the previously audited R28 archive containing the accepted parent payload |

Both extraction-to-stdout/hash pipelines returned `0 0`. The backup therefore supplies additional recoverable copies of those exact archives, but no newly located class or digest implementation. The accepted pickle was not opened or rehashed in this extension.

The backup member `TNN/Research/tnn-r27-native-master-shadow-CHECKSUMS.txt` was read as metadata. Its first line records the matching R27-shadow ZIP hash above and a historical `/mnt/data/tnn-r27-native-master-release/` location. A historical pathname in a checksum file is not a presently recovered source directory. The other checksum assertions in that file were not independently verified here.

Other nested R5/R6/R27/R28/R30/R31/R32 and current-execution archives appeared in the outer inventory. Their contents were not rescanned. Only the two measured ZIP members above have newly established byte identity in this external backup; do not assume all similarly named nested artifacts match existing copies.

**Recoverable original-source paths/hashes: none found.** The hashes above identify recovery containers and previously known shadow archives, not the missing `r27_experiments.py` or its dependencies.

## 4. Cheap local unreachable Git pathname inspection

Repository HEAD observed: `04a7268ac5c08ce3b3f1f3a35f48a2425fdceec8`.

With optional Git locks and lazy fetch disabled, `git fsck --connectivity-only --unreachable --no-reflogs --no-progress` completed with exit 0. It listed **6 unreachable trees and 25 unreachable blobs**, and no unreachable commits. This is local object/connectivity discovery, not a learner verification or full object-content integrity audit. No fetch, checkout, `--lost-found` write, index change or Git repair was performed.

Each discovered tree was recursively listed with `git ls-tree -r --name-only`; all six tree reads exited 0. Requested module/bundle pathname filters returned no matches in every tree:

| Unreachable tree object ID | Pathname occurrences listed | Requested-name matches |
| --- | ---: | ---: |
| `0fe1bd776d63893528a524fd33d0718f0bee0712` | 3 | 0 |
| `938f46aae05397547bef2d4b7391676489c03277` | 30 | 0 |
| `02331653f245eededf58bc03512018e5afd808f2` | 1,391 | 0 |
| `f634f496873386a2e3d658df701145015190f413` | 11 | 0 |
| `075aa4241e8af10e3b2772448b4d098717a56829` | 41 | 0 |
| `56bebf1f400eb4bbd9c3e5a1a9350d7bb794aa49` | 1,435 | 0 |

These counts overlap across trees and are not counts of unique recovered files. Git object IDs are not SHA-256 file hashes. Blobs do not inherently supply filenames; the 25 unreachable blob bodies were not read or characterized as source, and no absence-of-source claim is made about their contents. The earlier 313-commit reachable-history search was not repeated.

## 5. Remaining actual dependency and mapping gaps

**Already available, not missing:** the exact accepted historical parent payload and accepted-policy companion, as established in the frozen audit. The external backup now adds a byte-identical copy of the R28 container. No newborn restart or regenerated parent is justified by source-recovery difficulty.

**Still unlocated in the completed scopes:** the original eleven custom-module implementations, `R27State` source-defined behavior, the original accepted semantic-digest algorithm and field-selection/canonicalization rules, original full-verifier source, and original runtime/version provenance. Additional imports or helpers cannot be enumerated completely without those sources. No exact source hash can be supplied for an implementation that was not recovered.

**Not established by this task:** semantic-digest recomputation, reproduction of the historical 33 checks, tensor/storage interpretation, complete external-blob closure, native full-state encoding, or a lossless continuing-state migration. File SHA-256 comparison, metadata assertions and successful filename searches do not establish any of those properties.

The field-mapping blockers in the previous dependency report remain: nested identity/aliases, numerical layout and shared storage, raw evidence and provenance, replay/optimizer/RNG state, pending actions, and non-rewindable supervisor accounting. Explicit null/empty accepted fields must not be silently initialized. The earlier inventory's graph and ByteBPE objects and retained VAD policy remain historical data, not permission to activate graph/BPE/VAD/supplied token boundaries in active TNN or Foundry. Keeping those bytes inert preserves evidence; it does not prove transfer of their learned capabilities into a compliant native representation.

Any recovered Python must remain frozen historical evidence. A later, separately authorized native Zag implementation would need source-grounded field mappings and an explicit digest-compatibility contract; it must not claim that new code is the recovered original or that a newly chosen hash algorithm reproduces the historical semantic digest. No such implementation is included here.

## 6. Search limits, interruptions and conclusion

Unsearched: symbolic-link targets; files outside the two authorized roots; `.git` directories outside the one explicitly inspected repository; archives with arbitrary names not selected by the candidate filter; generic non-Python source encodings or renamed files outside the targeted scans; nested archive contents other than inherited conclusions for the two byte-identical copies; unreachable blob bodies; remote/cloud-only backups; and complete external-state/runtime dependencies. This bounded negative result is not proof that original sources no longer exist elsewhere.

Two initial session-result polls were blocked before returning output. After read-only process-state checks showed the corresponding commands were no longer running, later polls successfully returned their settled results. Only those successful results support the completed filesystem-search and backup-hash observations above. Blocked polls and blocked attempts described in earlier reports are not counted as completed checks.

**Conclusion:** the additional locations provide a verified backup copy, not the missing original R27 source/runtime bundle. Original-source and semantic-digest closure remain the recovery blockers. R27 remains canonical; this result does not qualify parent migration, grant learner authority, establish promotion, or assess the main agent's native journal work. Prior reports, historical Python, parent archives, registries, current state and native journal code were not edited.
