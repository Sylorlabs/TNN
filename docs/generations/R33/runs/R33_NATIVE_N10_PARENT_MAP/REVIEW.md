# N10 main-agent native mapping review before exposure

The native scanner contains no global-name import, resolver, arbitrary function
dispatch, tensor/storage constructor or Python call. Every potentially executable
pickle operation becomes a typed inert record. Source-opcode arguments are bounded
before access; frame crossing, invalid stacks/memo and exhausted capacity refuse.
Memo references are preserved without recursive traversal, including cycles.
All literal spans point into the unchanged owned input; full raw input is included
in the output bundle so metadata never stands in for lost bytes.

Special distinctions retained: None versus absent lookup, bytearray versus bytes,
raw IEEE floats including negative zero, long integer bytes beyond signed64,
encoded Unicode versus normalization, ordered container updates versus invented
Python key semantics, recorded BUILD arguments versus actually applied __setstate__,
and unresolved persistent/extension/out-of-band references versus fabricated data.
Data-structure relations are serialization bookkeeping, not graph cognition.

Both node and operation table allocation use explicit8-byte native integer words;
page encoding uses range-checked4-byte signed words. All relevant raw offsets,
lengths, IDs, memo bounds and linked-list ownership counts are checked. Manifest
load validates counts before allocation, page order/full coverage/source binding,
whole source SHA and invariants. Fresh reparse compares all reconstructed tables,
not merely a handful of printed fields. Known metadata is a disclosed expected
inventory from historical static evidence, never a rerun of original behavior.

All corruption targets are newly authored synthetic fixtures with preimages.
The accepted source is opened read-only and never modified. Mapping itself does
not execute a learner or call graph/BPE/VAD mechanisms preserved inside payloads.
The actual parent audit has a declared512MiB observed ceiling and60second child
deadline; ordinary controls5seconds, parent180seconds. No hard RSS or production
container security claim follows. Unknown unsupported opcodes must fail rather
than being silently skipped or interpreted as code.

Source review corrected an extra byte in the unexecuted empty-LONG control and
added protocol-minimum checks for binary bytes plus aggregate opcode invariants.
All expectations are still pre-exposure. This is main-author engineering review,
not independent protocol/security certification or a recovered original method
implementation. Full parent semantic/behavioral migration remains false.
