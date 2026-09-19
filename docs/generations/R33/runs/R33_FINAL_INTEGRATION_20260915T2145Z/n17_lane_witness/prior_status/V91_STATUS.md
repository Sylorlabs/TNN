# V91 native retained-generator recovery — 2026-09-15

Generator parity is **blocked / fail-closed**: zero historical strings have been
produced by native inference. The author dataset/order reconstruction fails all
16 row comparisons. Its native exit 1 is recorded as a failed reconstruction;
it is not a semantic qualification result and was not fitted to the oracle.

Closed input custody:

- Native traversal of the hash-admitted R27 map resolves
  `root.base_state.base_state.r24_state.r23_state.evidence.semantic_generation.examples`.
  All 16 `naive` strings match the bound oracle exactly. Every string receipt
  includes the resolved node, opcode, opcode offset, text offset, length and
  native SHA-256. Offsets refer to the **R27 parent serialization**, not an
  absent standalone R23 file. Memo aliases are resolved by the admitted inert
  map; reducers/classes/methods are never executed.
- The framed oracle receipt has SHA-256
  `8efe1df2c661e769f8eb9e4a39cb779970629cbfa0764583488f8f9369c09112`.
- All 11 model tensors are admitted as contiguous little-endian float32 inputs,
  with validated ranks, dimensions, strides and raw byte hashes: 619,544 bytes.
  The nested R23 and retained R27 tensor files are compared byte-for-byte.
- The BPE table has 340 payloads (256 base bytes and 84 merges). Every merge
  payload is checked against concatenation of its predecessors. Its 3,946-byte
  frame SHA-256 is
  `f83d2f7c63b2f40f386c37b96fc5d17ea120f715e503f58b62a6ca428cd21f6c`.
  Generic merge/decode components round-trip all 256 bytes and two independent
  strings. These checks do not admit historical encoding or special-token policy.

Native layout qualification measures i32/u64 slice stride 8, u8 stride 1, and
ordinary V91Row size 56. Flat scalar row storage and allocation sizes follow
those measured rules. Adjacent-row read/write checks pass. All qualification
builds use native import projection to preserve original constant definitions
under the pinned stable compiler; the V91 projector permits the existing
`@noalloc` annotations and `module:` parameter names without changing their bytes.

Numerical substrate qualification is limited to exact finite float32 decoding
into f64, explicit linear and isolated GRU components, bounded native activation
approximations, and categorical sampling from an explicitly supplied uniform.
Analytic tests and isolated retained-weight diagnostics pass. Those diagnostics
are not the original forward/generate method, do not produce the 16 historical
strings, and do not certify historical Torch dtype/rounding/RNG equivalence.

Negative admission covers corrupted manifests, missing and truncated table
pages, corrupted and truncated tensors, and corrupted BPE frames. The native
gate always returns 91/CLOSED, including with genuine extracted oracle evidence,
no evidence, and a caller-supplied purported generated receipt. Oracle custody
is never credited as an inference output.

Minimal unresolved exact inputs:

1. Original 63,069-byte R23 source SHA-256
   `517eb325096d5ae71ebb3bf659da77eac4266129136b888b469a99e366d4b642`:
   exact `_build_semantic_dataset`, BPE/forward and `generate` definitions are
   absent from the inspected local releases and recovered sources. Row order,
   input assembly, special tokens, precision, temperature, stopping and seeded
   multinomial semantics cannot be guessed from tensor dimensions.
2. Standalone 7,028,883-byte R23 state SHA-256
   `fc24881f104052c09a4cb6e596b01ae5c107d9ae0356c8799ec97eff3edf440b`
   is absent. Nested parent custody does not establish that serialized-file hash.
3. Independent 29,242-byte R23 summary SHA-256
   `74cdb944e1037e92100d0dee2eca6ffaebcabe53346bb114c4bd09b035e3a495`
   is absent; its lexical-offset comparison remains blocked.

No learning, authority, promotion, exposure, or canonical R27 mutation is granted.

Final origin binding: original oracle generator node 182274, model 183224,
BPE 182280, interpreter 183721, on the nested R23 path above. The retained
parity target is `root.semantic_generator`, node 281053, model 281994,
BPE 281056, interpreter 282428. They are distinct serialized nodes; no
historical runtime object-identity equivalence is claimed. All 11 model files,
the complete BPE frame, and interpreter W compare byte-for-byte equal.
Interpreter W is 768 x 42, 129,024 float32 bytes, SHA-256
`3f5c806cfa243f9fc5de398101d93a9fc59b8ea1d4cb55cbe08165d940e3e5c3`.
