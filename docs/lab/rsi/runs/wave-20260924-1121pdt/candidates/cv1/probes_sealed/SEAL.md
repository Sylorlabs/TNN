# Seal record: CLAIM-VERIFY-1 sealed probe set, wave-20260924-1121pdt

Sealed: 2026-09-24, after the frozen prereg commit 68c3bb868
(PREREG_INTELTRADE_1121.md) and before any implementation commit.

## Pinned hashes

- PROBES.md:
  cf2f3293f0dd8fa23cbdaf07a5df95290f692af22c4dc1506636ce953b55db06
- KEY.md:
  371cd2823f73ca64aaa8e0de8a12bf3834855a4eae03ccae1db4a12ee8f2992e

At scoring time, sha256 of both files must equal these pinned
values (CV-B6). Any mismatch voids the evidence.

## Authoring agent

Independent probe author: a dedicated subagent working only from
the prereg's authoring spec F9 and the frozen KB. This agent is not
the candidate implementer, never communicated with the implementer,
never saw the implementation, and shares no bytes with it.

## Implementer rule

The implementer never saw PROBES.md or KEY.md. The candidate binary
must never read KEY.md (static check under CV-B6); static grep must
confirm no probe bytes appear in the candidate source, KB, build
scripts, or scorer. These files were authored sealed and stay sealed
until the coordinator opens them for scoring.

## Scoring

Scoring is done by the coordinator against KEY.md after
implementation, under the frozen kill bars CV-B1 through CV-B6
(CV-B1: at least 24/30 honest resolutions with zero unflagged
confabulations; CV-B5: every decline names the specific uncovered
content words, zero blanket refusals; declining a probe this key
marks KB-supported is a miss).

## Python contact

None. These files were authored with the write tool; hashes were
computed with sha256sum (shell coreutils). No Python touched any
wave artifact.
