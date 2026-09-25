# Binary rebuild resolution — PENDING `kbp` implementation

**Date:** 2026-09-25 UTC
**Question:** BUILDLOG.md (implementation worker) claims binary 530,572 B at `/tmp/kbp_test`;
the battery coordinator's binary at `~/workspace/pending-run/bin/kbp` is 535,011 B,
SHA-256 `81b34ac86e8c53bed55bb2827f3cf0b09eec88f0027188af6b3e902b721f90bd`.
Which is right, and why do they differ?

## Procedure (independent rebuild from committed sources)

1. Fetched committed sources from `tnn-native-lab` branch,
   `docs/lab/live-ingestion/pending/`: `pending_track.zag` (45,521 B),
   `pending_cmds.zag` (35,516 B), `make_fork.py` (10,092 B).
2. Verified fork base
   `tnn-lab/knowledge/web_guides/live_ingest/knowledge/sources/instrument_kb.zag`
   SHA-256 = `d7ce44ffe8866f7fb5869250cfba40fcd8140e22eb79d4a23b773969dedede41`
   (matches the pinned value in RUNLOG_PENDING.md).
3. Ran committed `make_fork.py` → `instrument_kbp.zag` (168,955 bytes on disk;
   the script's "168900 bytes" message counts characters, BUILDLOG recorded the
   character count — cosmetic).
4. Built with the pinned toolchain
   `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
   (SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`,
   matches pin), from a directory containing `R33_NATIVE_IO_V1.zag` for the
   `@import` resolution. Build: EXIT 0 (56 analyzer warnings, none fatal).

## Result

| Binary | Size | SHA-256 |
|---|---|---|
| Independent rebuild (this round) | 535,011 B | `81b34ac86e8c53bed55bb2827f3cf0b09eec88f0027188af6b3e902b721f90bd` |
| Coordinator's `bin/kbp` (battery runs) | 535,011 B | `81b34ac86e8c53bed55bb2827f3cf0b09eec88f0027188af6b3e902b721f90bd` |
| BUILDLOG `/tmp/kbp_test` (worker) | 530,572 B | unknown (ephemeral, deleted) |

**The rebuild is byte-identical to the coordinator's binary.** Two independent
builds from the committed sources with the pinned toolchain produce the exact
same 535,011-byte binary.

## Root cause

The BUILDLOG's 530,572 B figure is **stale**: it was recorded from `/tmp/kbp_test`,
an ephemeral pre-final test build made during the implementation worker's
development session, before the final source state was committed. That binary no
longer exists (`/tmp` is ephemeral) and its exact source iteration is
unrecoverable. The committed sources — which include the final IO corrections
(`kpp_read_chunk`, `kpp_write_chunked`, `kpp_read_proc`) documented in the
BUILDLOG itself — deterministically build to 535,011 B.

**Authoritative binary:** 535,011 B,
SHA-256 `81b34ac86e8c53bed55bb2827f3cf0b09eec88f0027188af6b3e902b721f90bd`.
All battery evidence (including the official P5 two-pass below) was produced by
this binary. The BUILDLOG size figure should be read as superseded; the build
*procedure* in the BUILDLOG is confirmed correct and reproducible.

## Smoke check

Rebuilt binary: `kbhold off` → `HOLD|OFF`; `kbpend` on empty input →
`PENDING|ERROR|read-fail` (correct rejection). Functional.
