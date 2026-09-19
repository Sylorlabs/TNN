# N09 main-agent pre-exposure engineering review

The restore/export layer takes a live validated supervisor store, not a worker-
chosen path, grant flag or mutable cached authority. Its canonical header binds
current control sequence, head, counters, identity and exact current payload.
An authentic sibling history with equal counters is distinguished by head/state.
Both complete uncommitted intents and restrictions change receipt identity.
Successful payload restoration still advances the supervisor rather than rewinding
its accounting. Corrupt authoritative journal cannot be repaired by receipt data.

MAC/format/header/payload verification and sufficient output capacity precede
delivery. Internal authority aliases are rejected; caller packet/output overlap
uses separately staged expected bytes. Current store fields are trusted only
after N07's open/validation or its serialized authenticated transition. Arbitrary
struct corruption in the trusted controller is not a protected API guarantee.

The OS adapter is the bounded passing N08B design parameterized by trusted fixed
absolute paths, with quote/backslash/newline/NUL checks. It retains explicit
network/socket/fork/foreign-exec denial, descriptor closure, empty environment
and no unconfined fallback. The integrated worker receives only one exact cache
path and its log writes. Its binary imports SHA/IO only, no signer or authority.
Fresh authority recovery after the worker tests actual stored control integrity.

This combines a separately retained supervisor authority and a worker kernel
boundary; it does not solve administrator rollback of the entire trusted store,
real human identity/key custody, hard aggregate resource enforcement or native
R27 semantic migration. N07's valid-prefix counterexample remains true when all
trusted history can be replaced. No new permission follows from a test pass.

Sources and all known-case success/refusal expectations reviewed before exposure.
Any compile failure will be preserved with corrected new build before freeze;
any primary failure requires a separate correction identity. Main engineering
review is not independent approval or a cryptographic/security certification.
