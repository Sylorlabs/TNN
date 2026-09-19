# N18 pre-freeze manifest requirements

This is a checklist for a future freeze. It is not a freeze, reservation or
execution authorization.

The final immutable input manifest must hash every input file, not only a
directory name or parent manifest. At minimum it must include:

- canonical R27 accepted-state bytes, size and SHA256;
- every N10 parent-map file, including all raw/node/edge/opcode/memo/global
  pages and the map manifest, with ordered names and individual SHA256 values;
- copied, read-only N12/N13A substrate sources and every transitive native
  import, with individual hashes;
- the native parent adapter, evaluator, telemetry, filesystem adapter and
  refusal fixtures;
- the exact N16 arm19 source-level mechanism reference and separately authored
  N18 sidecar source;
- compiler, flags, target, OS/build identity and all build inputs;
- C0/C1/C2/C3 configuration, seed/allocation manifest, probe fixtures and
  negative fixtures;
- the governing contract, selected route record, review records and all source
  references.

The preflight must also record, for every run-local parent copy and condition:

- canonical path resolution and unconditional rejection of symlinks and
  hardlinks for immutable inputs unless the selected route explicitly pins the
  link identity and its target hash;
- file descriptor identity and size before reads;
- hash before and after each condition and after stage settlement;
- refusal on TOCTOU, short read, duplicate row, missing row, malformed row,
  duplicate seed allocation or unexpected condition identifier;
- collision-checked seed namespaces against the consumed-evidence registry,
  not merely proposed integer values.

The final freeze must list explicit expected failures for every negative
fixture, native resource/capacity refusal, and literal-result-substitution
attempt. Operational hashing may capture receipts but may not become the
scientific evaluator or gate.
