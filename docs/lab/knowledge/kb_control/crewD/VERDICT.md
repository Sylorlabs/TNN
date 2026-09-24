# Crew D Verdict — Silent-Overwrite Red Team

## Battery description
GATE + F1–F5 red-team battery against the KB fast path, testing for silent
cross-slot overwrites (zero clobbers = kill bar).

- **GATE**: Bulk-fill to chunk rollover, then revise a pre-boundary fact. Must reproduce the known successful-revise/unrelated-clobber defect.
- **F1**: Boundary revise (exact, -1, +1, spanning boundary-size facts).
- **F2**: Padding geometry across 40–467 byte range.
- **F3**: Deterministic interleaved append/revise/delete schedules.
- **F4**: Power loss at every write stage (crashput/crashrevise).
- **F5**: Slot→blob offset validation and content hashes.

After every attack: full-store census, content hashes, slot→blob offset validation.
Any clobbered byte = KILL.

## Current-path (fast) verdict: KILL

All 5 chunk geometries KILL with byte-identical reruns:

| Variant | Chunk | Findings | Kill-bar | Reruns |
|---------|-------|----------|----------|--------|
| c4096 | 4096 | 45 | 44 | 2× identical |
| c8192 | 8192 | 49 | 48 | 2× identical |
| c65536 | 65536 | — | KILL | 2× identical |
| c1m | 1048576 | 24 | 23 | 2× identical |
| c33m | 33488896 | 4 | 3 | 2× identical (GATE) |

### Defect mechanism (confirmed)
`igb_append` omits rollover padding from `b.total`. `ig_revise` reconstructs
`bb.used = btotal % IG_BLOB_CHUNK`. A post-rollover revise writes into occupied
tail data, silently destroying unrelated facts.

c33m (genuine 33,488,896-byte geometry) reproduces:
- K1_clobber: 100 bytes changed in `blob_000002.dat` at offset 1062425
- GATE target 132889, K2/K3 counts 137109 each

## Conscious-fork verdict: BLOCKED

Crew B's `kbctl` binary (`~/workspace/kb_control/crewB/src/kbctl`, built 2026-09-24 08:03)
fails all `put` operations with `PUT rc=1` ("bad-textfile"), even with valid
nonempty text files. Both `--mode=conscious` and default mode fail identically.

The conscious fork cannot be tested until Crew B delivers a working binary.
No conscious verdict is possible.

## Rerun proof
All variants ran twice with byte-identical `findings.json` and `CHAIN.txt`:
- c4096: run0/run1 identical
- c8192: run0/run1 identical
- c65536: run0/run1 identical
- c1m: run0/run1 identical
- c33m: run0/run1 identical (GATE leg)

Zero RNG throughout; all fixtures deterministic; evidence hash-chained.

## Defects found
1. **Silent cross-slot overwrite** (KILL): The primary defect. Post-rollover revise clobbers unrelated tail data.
2. **Event seal overflow** (DoS): `sc_seal_final` panics when event log exceeds 3072 entries (fixed scratch overflow). Wrapper skips seal above threshold.
3. **Compact chain overflow** (DoS): `sc_compact_and_seal` panics on large compactions (fixed scratch overflow). Wrapper uses dynamically-sized scratch.
4. **c33m scale panic** (unresolved): Bulkfill panics between 276k–278k facts at 33MB chunk geometry. Root cause not localized. Used n=270000 for genuine-geometry GATE.

## Commits
- Prereg: `ba181ea59fb94e529e396c52242a97a474f542e6`
- Source: `5a2d932da2a58668f12a0f89d1fb3175d80b3914`
- Evidence: `d7f6d1ed73b1e280469d43f12aa010ce1f0e56ca`
