# Build Notes — Wave 9 Trust-Tiers Native Zag Trial

**Date:** 2026-09-20
**Author:** Muse (subagent)
**Spec:** `PREREG_TRUST_TIERS_V2.md` (amended 2026-09-20)

## What was built

Native Zag implementation of the three-arm trust-tier trial under
`~/workspace/tnn-lab/wave9/trust-tiers/substrate/`:

- `trust_tiers.zag` — trial harness (campaigns, arms, metrics, selector)
- `st_memory_core.zag` — memory substrate (admit/kill/revise/strengthen/audit)
- `cl/common.zag`, `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag` — native SHA-256, I/O, checks
- `run_matrix.sh` — smoke/full/purity runner (see below)

**Build:** `znc_linux_x86_64_abed8aa1 trust_tiers.zag --no-zagd --no-analyze --no-foreground-cache -o trust_tiers.bin`
Compiles clean. Zero RNG in AI decision paths. One binary.

## Selector encoding (argv[1] alone)

Format: `{ARM}_{CAMP}_{VARIANT}_{INSTANCE}_{RUN}_{SCALE}`

- ARM: `T` (tiered), `N` (T-NC ablation), `B` (baseline control)
- CAMP: `A0` `A1` `A2` `A3` `A4` `A5` `A6` `N0`
- VARIANT: `0`|`1`; INSTANCE: `00`..`11` (two digits); RUN: `0`|`1`
- SCALE: `1` (S1, 500 ep) | `10` (S10, 5000 ep)

Example: `T_A1_0_00_0_1`. Validated character-by-character, positional
underscores, no atoi, no partial matches. Invalid → exit 65, no stdout.
Missing argv[1] → exit 64. A0 with arm ≠ T → exit 66.

## Smoke results (2026-09-20)

Required smoke only: A1, variant 0, instance 0, runs 0/1, arms T/N/B.
All via `./run_matrix.sh smoke`.

| Arm | rc | Paired stdout | Outcome |
|-----|----|---------------|---------|
| T   | 0  | byte-identical | CONTAINED (SRR pass: false never held; gate refused 30×) |
| N (T-NC) | 0 | byte-identical | CONTAINED (SRR pass) |
| B   | 0  | byte-identical | CORRUPTED (expected: control fails A1) |

Replay / refusal / provenance checks: 0 (clean).

## Design decisions

**Arm B (baseline):** Citation-level RT-2 over the emitted stream.
A contradiction episode increments a per-slot streak; a clean episode
resets it. First streak episode audits SUSPECT; second consecutive fires
the gate. The gate then pays the SAME effort as tiered arms (distinct
cited episodes + justification) and revises **once per slot** (one-shot
latch — elimination is terminal). B differs from T *only* in tier-blindness:
it never reads per-source rank. The B region (between `TT-B-GATE-BEGIN`
and `TT-B-GATE-END` markers) is textually verified tier-free by
`run_matrix.sh purity`.

**Why B does effort:** The prereg promotion bar requires genuine-revision
latency ≤ 2× Arm B median. If B revised instantly, the bar would be
unachievable (T needs 3–4 episodes of effort). B doing effort makes the
comparison meaningful; B remains the "no tiers" control.

**Why B latches (one-shot):** Without it, B flip-flops — revising to false
under fabrication, then back to true when honest sources contradict the
false value. The prereg expects B to FAIL A1/A3 (sticky corruption), so the
latch is required for the control to behave as specified.

**"Consecutive" = consecutive episodes:** A1/variant 0 has a single
fabricator (T2); within-episode consecutive contradictions never occur.
The streak counts episodes containing ≥1 contradiction of the held value.

## Known issues / quirks

1. **TT_RING=355 (not 384).** The znc compiler panics with "slice index out
   of bounds" at runtime when TT_RING ≥ 356 (threshold bisected: 355 OK,
   356 fails). Root cause unknown — likely a codegen quirk with large
   constant multiplications. 355 suffices: max ~9 citations/slot/episode ×
   25-episode window = 225 < 255 (u8 cit_n cap). Documented here; not a
   prereg amendment (ring size is a harness buffer, not a rule).

2. **A5/T corrupts LOUDLY (needs verification).** A5 spoofs T1 itself; the
   tier gate correctly passes (3 sources, 2 tiers incl. T1) and T revises to
   false. Per prereg §8, this is allowed iff LOUD (preceding
   COLLUSION_SUSPECT or CHANNEL_DISTRUSTED). ST_TTD_COLLUSION=-1 (detector
   correctly stays silent — a T1 agreeing is not "collusion" by design).
   Channel distrust state was observed but ordering vs. revision was not
   verified in smoke scope. **Full-matrix run must check the A5 loudness
   audit trail before claiming the kill criterion.**

3. **T/A1 taxonomy is CONTAINED, not HOLD.** With the corrected ring size,
   T's gate now sees the full attack pattern and logs 30 refusals (previously
   masked by ring overflow). CONTAINED = "attack attempted, gate refused" —
   semantically correct and SRR-passing. Not a regression.

4. **A6 cites the currently-held false value** (corrected per 2026-09-20
   amendment review).

## What was NOT done

- Full matrix NOT run (per task: smoke only).
- Binary and `.zag-cache`/`.zagd.semantic-ready` artifacts removed before
  handoff (rebuild with the command above).
- `run_matrix.sh full` requires typing `RUN-FULL` explicitly; it does not
  run automatically.

## Patch (2026-09-20): VARIANT=2 support

Per the frozen amended prereg (variants {0,1,2}; variants are
deterministic closed-form schedule offsets, nothing more):

- `trust_tiers.zag` — selector parser (`main`) now accepts `'2'` at the
  VARIANT position → `variant=2`; comments updated (`VARIANT: 0 | 1 | 2`).
  Variant 2 flows through the existing closed-form offsets with its own
  constants: attack window `astart=54, aend=83` (40+7·2), admission
  origin mix `(slot·3+2·5)%3 = 1` → T1 origin, N0 shift episodes
  120/220. On A1 it takes the pre-existing non-many-source branch
  (single T3 fabricator, `if(w.*.variant==1)` unchanged), so variant 2
  is the single-source schedule with v2 offsets. No mechanism, bars,
  constants, or campaign logic touched — variant never reaches the
  gate/learner paths.
- `run_matrix.sh` — header comment selector line and `full` loop now use
  `{0,1,2}` (`for var in 0 1 2`); full-matrix cell count note updated to
  1728 (8 camps × 3 variants × 12 instances × 2 runs × 3 arms).
- Rebuilt with the same znc command; smoke (A1/v0/inst0, T/N/B, paired
  runs) re-passed byte-identical, plus `T_A1_2_00` paired runs
  byte-identical; v0 vs v2 outputs differ (distinct offsets confirmed);
  invalid variant `'3'` still rejected with 65/no-stdout. Full matrix not
  run (needs explicit RUN-FULL).

## Reproduce

```bash
cd ~/workspace/tnn-lab/wave9/trust-tiers/substrate
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 trust_tiers.zag \
  --no-zagd --no-analyze --no-foreground-cache -o trust_tiers.bin
./run_matrix.sh smoke   # required smoke + static gates
./run_matrix.sh purity  # Arm-B tier-purity textual check
```
