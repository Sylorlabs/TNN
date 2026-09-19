# R33-N07 — bounded authenticated-control engineering passed

The sole frozen BUILD_01 primary exited0. All37 top-level children and the one
nested lock contender were reaped. All642 verified checks from completed child
modes and368 parent checks matched. The native result records366 parent checks
before result-save and root-close; those final two checks and the terminal marker
also passed. Intentional crash exits71..75 were expected, not failed checks.

Evidence: [native result](R33_NATIVE_N07_RUN_PRIMARY_V1/NATIVE_RESULT.json),
[supervisor output](R33_NATIVE_N07_RUN_PRIMARY_V1/supervisor.stdout),
[protocol](R33_NATIVE_N07_AUTHORITY/PREREGISTRATION.md),
[crashed restriction recovery](R33_NATIVE_N07_RUN_PRIMARY_V1/revoke-crash-replay.stdout),
[nested lock](R33_NATIVE_N07_RUN_PRIMARY_V1/lock-owner.stdout),
and [required negative anchor witness](R33_NATIVE_N07_RUN_PRIMARY_V1/prefix-limit.stdout).

## Positive evidence in the registered engineering lane

The native HMAC implementation matched all seven public RFC4231 SHA256 cases;
case5 compares the specified128-bit prefix, while runtime authentication always
requires the full256-bit tag. First/last tag-byte changes and truncated tags
were refused. All256 independently tampered grant-byte positions were rejected.
Re-signed wrong actor, instance, scope, milestone, epoch, nonce, state version,
logical interval, length, reserved bytes and dependency/state/policy/candidate
hash controls were rejected with the exact source-frozen codes. Candidate swaps,
private-buffer aliases and short output were refused without admitted-state or
quota mutation. No cryptographic certification follows from these public tests.

A4096-byte synthetic snapshot, an empty snapshot and an authenticated restoration
of the original synthetic bytes survived fresh replay: version14, nonce3, spent6
and all three commits remained. This demonstrates non-refund across this learner-
payload restoration, not rollback protection against control-store replacement.
Quota saturation, restriction below already-spent resources, old-epoch refusal,
authenticated attempted widening, maximum signed31-bit nonce and32-attempt
capacity all matched. A second fresh cooperating process was denied while the
owner held the lock; the owner committed and reopened successfully afterward.

Empty and partial intent files refused fresh recovery with empty state/keys and
closed handles. Complete uncommitted state intents retained charge3 and nonce1
without exposing the candidate. Reuse was rejected; subsequent valid admission
used the next attempt and produced spent5. After published-but-not-reflected
in-memory commits, fresh processes recovered the committed version and retained
charges. A returned diagnostic failure invalidated handles and preserved intent.

A complete restriction intent followed by crash before acknowledgement still
recovered epoch1/budget1/version11/one orphan. Neither old epoch nor old allowance
revived. Corrupted intent MAC, missing first intent, corrupted root MAC and a
valid but wrong commit link all refused recovery with closed/empty state. Exact
preimages or renamed retained originals remain in each corruption fixture root.

## Required negative: authentic older history is still accepted without an anchor

The separately created prefix clone contained authentic root, first intent and
first commit bytes. It opened at version12 while the source store had reached13.
This is the preregistered limitation witness, not unexpected corruption and not
a claim of full protected-runtime qualification. An authentic MAC chain alone
does not tell this implementation that a newer suffix once existed elsewhere.

The next protection layer needs an independently protected high-water authority
outside learner rollback, plus genuine process/OS isolation and human identity/
key provisioning. Advisory cooperating-writer locking, MAC-protected records and
private-looking struct fields do not establish that security boundary. The
fixture keys are deterministic and public; no real human grant was issued.

## Source, resources and scope

All29 source/compiler/config/protocol/review/reservation/build pins verified
before admission at2026-09-06T02:55:51Z. Both independently compiled binaries
are byte-identical at
`85e633876a48fb2f5b0dfc7584f5a4d4f596daee88376e2a133dfbe3e1c18bb9`.
Native result SHA256:
`fc3e48a56e3d4b850f65ccb35c75ed8ea16670ecde4f45c72bb72c290ec2f2f0`.
Supervisor output SHA256:
`9bdf365b73f479314addc24cd6da0b321557798650ad1e51a7aed342c8779307`.

Native top-level-child CPU274,686us, summed observed nonmonotonic wall413,621us,
peak top-level-childRSS2,654,208bytes. Nested contender separately measured
CPU985us, observed wall6,332us and peakRSS1,540,096bytes; its own process row is
retained. These are labeled observations, not a hard aggregate descendant budget.
Host elapsed0.77s, user0.25s, system0.10s, maximumRSS11,239,424bytes. No surviving
n07 process matched the scoped post-run observation.

Source change is generic native keyed integrity plus bounded control admission,
restriction, persistent accounting, recovery and synthetic tests. It is not a
full learner, lossless parent migration, actual executable-module verifier,
wall-clock expiry, externally anchored antirollback, asymmetric signatures,
human-key custody, hostile containment, full causal integration or hardware
power-cut guarantee. Known intermediate arena copies are not guaranteed wiped.
Main engineering review is not independent scientific or security approval.

Seventeen diagnostic batches now consumed, including historical negatives and
mixed-language C03. Zero R33 training runs, zero newborn restarts, no canonical
change, no promotion and no actual learner authority grant. R27 remains canonical
at step60423. Original-source/semantic continuity, protected-runtime integration,
full sensory/causal qualification and later scientific milestones remain open.
The full eighteen-stage R33 program is not complete.
