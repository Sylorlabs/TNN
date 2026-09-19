# N13 memory accumulation: source-grounded diagnosis

The N13 primary is consumed and failed. This is source inspection and retained
artifact analysis, not a second execution or a revised acceptance threshold.

## Evidence

Independent postrun review: Research/R33_NATIVE_N13_TORCH_VIEWS/POSTRUN_INDEPENDENT_REVIEW.md,
SHA256 f5ffe72118bcacae5d21f1b4db810d952db7c9c51c8e8b108e59a837ebb19dfa.
The saved compiler source REFERENCES/acodegen_7cacbfc0.zag.txt has SHA256
cf4d60fc0778a1982324c01d11966ad6360bf6ee0e0f49246423645c71663596 and Git blob
c4efe3d3e6501c07dfb29b395398fb07d584d13d at immutable compiler commit
7cacbfc04f6cffec02ea9b1d5ff6702fe2e93f3c. The reviewer matched that commit's
bootstrap compiler to the selected binary. No new self-host parity claim follows.

At compiler source line2129, _zag_free evaluates its argument but does not reclaim
memory. At3540 onward, the allocator bumps through64MiB arenas. Thus logical
owner close does not imply physical reuse in this compiled target.

The original inventory child reported409862144bytes RSS, above402653184 by7208960.
Its4560 successful header-record attempts each request30720bytes of tables:
140083200 cumulative bytes before headers/alignment. Its two full-parent
fingerprints each hash55166836bytes (input and all seven resident tables), giving
110333672 logical bytes. SHA256_V2 allocates a padded full-message copy plus
working arrays for each call, and those allocations are not reclaimed. Other
row hashes, inherited loader staging/hashes, owned rows/shapes, seen table,
logging and compiler allocations also remain resident cumulatively.

These extents establish an accumulation mechanism consistent with the failed
RSS gate. They are not a measured per-allocation trace or exact RSS attribution.
No runtime allocator OOM was injected or observed.

## Narrow corrective hypothesis

Change only the evaluator's eight-message fingerprint implementation to a native
direct-block SHA-256 with1216bytes of scratch allocated once per fingerprint and
reused across all eight complete messages. Reset the state for each independent
message; read original64-byte blocks directly; use at most128bytes of final
padding. Preserve the exact complete-message digest, before/after coverage,
logical work charges and every original reader/row/page/loader behavior.

The expected removal is the fingerprint-specific full-message allocation path,
not all temporary allocations. The remaining140083200-byte header-map pressure
and inherited loader/row/logging allocations are explicitly unchanged. The
original finite inventory is known engineering data, not new scientific evidence.
Actual fit under the unchanged384MiB RSS gate is an outcome to measure once in
a separately reviewed, registered, frozen and admitted N13A primary.

New independent hash-padding/reset/disjointness/argument controls must precede
the copied matrix/refusal/inventory/replay regression in that primary. Old N13
outputs stay retained and unqualified; no standalone replay or old-binary retry.
No compiler global arena reset, interior munmap, learner update or promotion.
