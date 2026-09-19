# N06 pre-exposure integration review

Main-agent engineering review of complete new sensor/driver source and the
frozen N05B/C02 imports. No independent science/authority qualification claimed.
N05B's341 source/build/run artifacts were verified before this next component.

The sensor path does not reduce raw evidence to an invariant summary. A packet's
complete physical metadata and bytes are retained; the observer decodes every
signed sample or reads every interleaved pixel channel without semantic units,
normalization, subsampling, or an evaluator argument. Distinction fixtures include
the known odd-position and equal-histogram failure shapes, declared reused controls.

Raw storage needs a separate persistent reservation because process death may
occur before the telemetry attempt exists. The implementation scans a bounded
blob namespace, counts incomplete/orphan reservations, refuses its33rd blob and
uses a monotonically increasing explicit blob reference in the evidence slot.
It does not derive blob identity from committed event count. Fresh recovery
checks every referenced full packet and digest before exposing any usable state.
Unpublished blobs consume quota but never become observer input. They are not
discarded or silently reclaimed. The two corruption mutations and missing-file
rename occur only in new diagnostic directories with retained preimages.

Output validation and staging precede observer mutations. Eight-byte native
integer extents are used for aliases; physical signed16 decoding and signed32
wire fields remain distinct. The nominal all-codeword test covers all65,536 PCM
codewords in the actual file/trace/reload path, not just an in-memory helper.
Counters are native and required totals are frozen before exposure.

Failure seams simulate a partial raw write and actual exit73 between raw sync
and trace creation. They do not simulate hardware power loss. File/single-writer
and parent/dependency limitations remain explicit. Local payload repeat tracking
does not prove historical/global freshness. The process supervisor is trusted
direct-child only; no learner authority, physical sensor or full parent is run.

Host SDK inspection confirmed Darwin ftruncate201 and renameat465 before
authoring diagnostic file operations. Existing evidence, canonical bytes,
compiler source and unrelated worktree edits are not mutation targets.
