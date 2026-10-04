# ADDENDUM to PREREG_SATSEARCH.md (2026-09-30)

## OOM during pilot; sharded execution

The timing pilot (single binary, all 72 ids) was OOM-killed (SIGKILL,
exit 137) after 4m41s having completed ids 0..35, on an 8GB VM. Root
cause: the frozen v2_score allocates a fresh 1024-byte stack per
scoring and never frees (pre-existing leak in frozen code); V3
full-enumeration candidates leak ~1.6GB each. This is a resource
limit, not a logic issue.

## Remedy (frozen oracle preserved)

The search is sharded. Each shard is a separate build with the
BYTE-IDENTICAL v2gen.zag oracle (same sha256 verification) and a
table containing CAL-0 as id 0 plus a contiguous run of original
candidate ids remapped to shard ids 1..k via SHARD_BASE. The frozen
main validates all ids in each shard; the union over shards covers
all 72 original ids. No validation logic is altered in any byte.
Each shard is run 3x with byte-identical logs.

This addendum is committed before the sharded runs.
