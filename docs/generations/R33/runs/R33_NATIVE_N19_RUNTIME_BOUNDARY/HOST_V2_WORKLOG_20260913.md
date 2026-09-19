# N19 host adapter V2 authoring checkpoint

Status: source authored; native compilation and execution unverified.

The new `n19_host_v2.zag` provides an explicit retained-root interface, borrowed
root descriptors for leaf operations, operation-specific open versus I/O error
classification, bounded syscall detail, nonblocking regular-file admission,
and owned-descriptor invalidation on close. It contains no learner or parent
state reader. The existing BUILD_06 source and result records are unchanged by
this authoring work.

`n19_host_v2_tests.zag` is a native engineering test driver. It declares unit
checks and filesystem fixtures for exclusive creation, observed missing-file
and existing-file errors, path refusal, symbolic/hard links, FIFO refusal,
retained-root access after directory rename/replacement, byte preservation,
and double-close refusal. Run filesystem checks only with a new empty
owner-created directory whose path itself has no followed symlink components.
On macOS, `/tmp` commonly resolves through `/private/tmp`; `O_NOFOLLOW_ANY`
correctly refuses that alias. Use a repository-owned fixture directory for the
runtime qualification. Failed setup and I/O must count as positive test
failures rather than cancelling other failures.

No compilation result or execution result has been obtained. The compilation
request and subsequent inspection request were rejected with an invalid,
expired, or revoked turn-token error. Tool failure is not a compiler failure
or a test failure. Do not report these declared checks as passed or create a
qualification receipt without an actual native execution witness.

Remaining work:

1. Reinspect these files and verify the current working state.
2. Build using the pinned native Zag compiler and retain build output/hashes.
3. Run the unit and filesystem checks under bounded native supervision.
4. Integrate this adapter into a separate version of the N19 journal driver so
   write, append, and recovery actually share the retained root handle.
5. Test fresh-process recovery, transactional failure poisoning, telemetry and resource
   accounting, then obtain independent review of the executed version.
6. Continue N17 verifier-equivalent R27 continuation and complete learner
   integration before enabling `learn` or admitting a scientific campaign.

This work does not establish R27 behavioral continuity, integrated learning,
full N19 qualification, crash/power-loss durability, or scientific capability.
