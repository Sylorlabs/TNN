# Phase 4 differentiation — VERDICT (2026-09-27)

## Verdict: claim C UPHELD — TNN differentiates people by interlocutor identity, not by name tag

**8/8 battery probes PASS · 6/6 red-team attacks WITHSTOOD · kill bars K1–K7 all hold.**
Determinism: all 14 probes byte-identical across 3 runs (2× plain + 1×
MALLOC_PERTURB_=165). Clean-room rebuild reproduces the binary byte-identically
(SHA-256 `2cb66f16daccec82ef2c0e75a1c1d003e99a71afa5809b22971031ef147d74e9`).

## What was proven (each tied to a preregistered bar)

| Bar | Result | Evidence |
|---|---|---|
| K1 name-lookup discrimination | HOLD | S1: facts follow the person across a rename (`heidi`→`ruth`, recall still `cat`). S2: a NEW person reusing the old name (`heidi`) inherits nothing (WITHHOLD). S3: two persons, same presented name (`mallory`), keep separate partitions (`london` vs `tennis`). R1: case-variant names (`xena`/`Xena`) do not merge. R2: rename ping-pong + mid-way name-squatter sees nothing |
| K2 leakage | HOLD | 0 cross-person leaks across S2/S3/S4/S6/R3: every cross-person recall WITHHOLDs; `topics` never lists another person's topics; secrets never enumerated anywhere |
| K3 withhold | HOLD | 0 confabulations: unknown/closed/untaught persons and topics all WITHHOLD (S4, S5, S8, R4, R5); `close` deletes (S8: all ops WITHHOLD after close; reopen starts fresh) |
| K4 belief | HOLD | S5: `carol` asserts `river=blue`, `victor` asserts `river=fish` — both attributions exact; `judge` reports `CONFLICT blue fish`, never collapses. R4: single-holder `judge` = `SINGLE`, unheld = `NONE` |
| K5 correction | HOLD | S7: correcting `carol`'s `sport` (`closed`→`open`) leaves `victor`'s byte-unchanged. R6: same with identical starting values (no value-dedup corruption) |
| K6 determinism | HOLD | 14/14 probes: 3-run sha256 identical (see results/SHA256SUMS_RESULTS.txt) |
| K7 red team | HOLDS | 6 novel attacks (fresh seed 20260928, content the implementation never saw) all withstood; hardcode audit clean (see redteam/REDTEAM.md) |

## The honest answer to the sharpest question

**Does TNN differentiate people, or partition facts by name tag? It
differentiates people.** The name is a mutable attribute of the person record:
renaming never moves facts (S1/R2), recycling a name never inherits them
(S2), and two persons can share a name without merging (S3/R1). A name-keyed
lookup table fails S1, S2, S3, R1, and R2; this implementation passes all of
them, so the "it's just a name-keyed lookup" hypothesis is dead by the
preregistered discrimination.

## Honest scoping (what this verdict does and does not cover)

- **Proven:** the differentiation *machinery* — per-person partitions keyed on
  interlocutor identity (the session handle), with person-semantics:
  attribution, withholding, zero leakage, person-scoped correction, beliefs
  held per-person without collapse. The per-person "model" = the partition +
  the `profile` summary (name, fact/belief/secret/correction counts) +
  attributed beliefs.
- **Not tested:** inferring personality traits from free dialogue;
  common-ground/shared-knowledge semantics (strict partitioning was
  preregistered; common ground is a follow-up line); multi-session
  long-horizon persistence.
- At the bottom every implementation is a keyed store — the preregistered
  discrimination was behavioral (identity-handle vs name-string keying), and
  the battery separates exactly that. "The table is the notebook, the
  mechanism is the hand": the mechanism here keys on the hand, not the label.

## Implementation notes (deviations / details, no prereg amendment needed)

- `correct` on a never-taught topic upserts (creates + counts the correction):
  uniform keyed-slot lifecycle, same philosophy as workbuddy round-2 T3.
- `teach` preserves an existing secret flag (only `secret` sets it); there is
  no unsecret op.
- Sealed value `V_PARIS=open` coincides with the `open` op keyword; it is
  handled purely as data (S7 passes) — opcodes and content never confuse.
- `close` marks the record unreachable; pool entries are not recycled (bounded
  bump pools: 64 persons / 4096 facts / 4096 beliefs — test-harness bounds,
  not architectural claims).
- Builder and red-teamer were the same agent (depth limit; disclosed in
  PREREG.md §7). Mitigations held: frozen prereg, sealed content bound by SHA
  before the build, fresh-seed novel red-team probes, clean hardcode audit.

## Reproduction

```
cd docs/lab/phase4/build
<toolchain>/znc_linux_x86_64_abed8aa1 p4.zag -o p4_bin   # -> 2cb66f16...
./p4_bin ../sealed/probes/s1.txt
bash ../battery/run_probe.sh s1        # 3x, byte-identical required
python3 ../battery/score.py ../results # strict: exact R-lines + FNV chain
```

Toolchain pinned: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Frozen prereg: commit `d97743268a8ff3ccedc637ecfdab07f8293ec965`
(`docs/lab/phase4/PREREG.md`).
