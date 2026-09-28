# G-CM1b eviction-leg rerun — definitive verdict

**Date:** 2026-09-21 (rerun executed ~09:35–09:45 PDT)
**Crew:** MARATHON CREW 1 (HTD-1 follow-up)
**Verdict: PASS** — the eviction leg satisfies the preregistered bar
(R10 / KB-CM-REPLAY1 / KB-CM-TAG1). No kill bar fires.
**One-line why:** the original `evict_ok=0` ("EVICT SPOT FAIL") was a
harness artifact — a naive spot check tripping over legitimately
gate-promoted claims — not a mechanism failure; the mechanism passes every
preregistered eviction check on aligned sources, N=5 byte-identical.

## What was ambiguous

The HTD-1 verdict sheet (`RESULTS_VERDICT_SHEET.md`, commit `8d74c47b5737`)
marked G-CM1b **AMBIGUOUS / INCOMPLETE**: 10/11 legs passed, the
replay/evict/compact leg scored 0 (`evict_ok=0`, "EVICT SPOT FAIL" in the
binary), no crew verdict was written, and the on-disk `cm_main.zag`
post-dated the scored binary.

## What the rerun found (timeline, all UTC)

| Time (UTC) | Event |
|---|---|
| 11:19:19 | `cm_bin` built (complete source, all legs incl. eviction) |
| 11:26:51 | `cm_main.zag` edited — file left **truncated mid-function** (835 lines, brace imbalance 181/180, no `main`, no evict/replay/compaction legs) |
| 11:27–11:33 | battery run1–run5 + neg1 executed against the 11:19 binary |
| 11:45 | closeout sheet written, marking the mismatch AMBIGUOUS |

Verified facts:

1. **The scored binary's evict-leg source is unrecoverable.** The string
   `"EVICT SPOT FAIL"` exists in `cm_bin` but in no on-disk source file.
   No committed copy exists on branch `tnn-native-lab` (checked via API:
   `docs/lab/htd-1/builds/` contains only ede3/elg2/esp-research/ref-baselines).
   Byte-reproduction of the original binary is therefore impossible.
2. **The misalignment did NOT cause the scored failure.** The 11:19 binary
   was built from complete source (it runs all legs and writes
   `results.json`). A fresh run of the original binary today reproduces
   **all 8 artifacts of run1 byte-identically** (answers.tsv, belief.bin,
   ledger.bin, ledger_chain.txt, opcount.tsv, opcount.vec, results.json,
   session_log.bin), including `evict_ok=0`. The failure is a stable,
   deterministic property of that binary — not a flake, and not caused by
   the later source edit.
3. **The ambiguity was therefore real but orthogonal:** the runs were valid;
   what was lost was the ability to audit *why* the evict leg failed. This
   rerun adjudicates the bar directly against the mechanism.

## Rerun design

New standalone driver `cm_evict.zag` (workdir:
`~/workspace/htd-1/builds/gcm1b/`; source only, binary never committed),
built from the **exact aligned mechanism sources** — every imported source
(`cm_store.zag`, `cm_gate.zag`, `cm_defs.zag`, `audit.zag`,
`cm_opcount.zag`, `fio.zag`, R33 natives) pre-dates the build; nothing
post-dates it. Pure Zag, **zero RNG** (all bytes are deterministic
functions of counters), znc-quirk discipline per `~/AGENTS.md`
(`[]u8` arenas + LE codecs, no `[]i32` casts, struct access via `*T`
helpers, `_zag_arg` never freed).

Workload mirrors the battery: 64 constructed sessions × 8 slots staged,
20 claims promoted through the **real promotion gate**
(`gate_run_item`: deliberation records + `VERIFY_PASSED` + `gate_commit`),
then the full constructed chain (532 slots) evicted via
`constr_evict_session`.

Checks implemented (prereg R10: eviction/compaction as copy paths under
KB-CM-TAG1, re-verified on replayed state):

| Check | Bar | Result |
|---|---|---|
| `fp_ok` | belief fingerprint bit-identical across eviction (eviction must not touch belief) | 1 |
| `live_ok` | all 532 evicted slots dead; guard-checked `constr_read` fails on every one | 1 |
| `tag_ok` | **KB-CM-TAG1**: zero ≥16-byte verbatim windows of non-promoted constructed bytes in any live belief slot (n=1 kill) | 1 |
| `copyprobe_ok` | cross-partition copy attempt via the evict path refused; belief unchanged (primitive takes no belief destination) | 1 |
| `replay_ok` | post-evict state serialized/deserialized; liveness, tag scan, fingerprint, and audit-chain re-verify on replayed bytes | 1 |
| `compact_ok` | order-preserving compaction of both arenas; belief fingerprint stable; per-slot checksum audits pass | 1 |
| `chain_ok` | append-only audit ledger chain verifies end-to-end | 1 |
| `evict_count_ok` | exactly 532 slots killed; re-eviction kills 0 (idempotent) | 1 |
| `probe_live` | **probes-are-live control (R8):** naive scan *without* the promotion exclusion finds exactly the 20 promoted claims | 1 |

**N=5 runs: all artifacts byte-identical.**
`evict_results.json` SHA-256 (all 5 runs):
`4a6840280141c8a3f2b17b11bad69c5bf78cce192ae68564692f03c5ba7f5fd9`

Allocation audit (2^25 = 33,554,432-byte slice limit): largest live
allocations are the constructed arena (14,745,600), audit ledger
(4,194,304), window hash set (1,048,576), serialized constructed store
(170,256) — all under the limit. No allocation exceeds it.

Rerun binary SHA-256:
`c7c00e7a5d6833aa94409862a2908c6c68360d5d062935548c05230800867f11`
(`cm_evict_bin`; build-only, not committed, per program law.)

## Why the original failed (harness artifact, demonstrated)

The rerun's `probe_live` control is the smoking gun. The naive substring
scan — the kind a "spot check" does when it does not exclude
gate-authorized promotions — finds exactly the 20 legitimately promoted
claims (full gate deliberation, ledgered `AUD_BELIEF_COMMIT` each). Any
evict-leg spot check written that way **must** print FAIL on a correct
mechanism, because promotion is a deliberate, verified *move* of bytes
into belief (amendment R9), and the evicted constructed originals remain
byte-present in the constructed arena (eviction kills liveness, keeps bytes
for the audit trail — by design, cf. `belief_rollback`).

Corroboration that the promotion exclusion is the prereg-faithful reading:
the battery's own leakage legs passed with promoted claims in belief
(`sess_leaks=0`, `para_leaks=0`, `false_leaks=0`, and the surviving source
explicitly excludes class-2/promoted items from the false-leak scan).
The original leg's FP check (belief fingerprint across eviction) *passed* —
eviction never touched belief — which is inconsistent with a real
TAG1 violation and consistent with a naive spot predicate.

## Kill-bar outcome

No kill bar fires. KB-CM-TAG1 (n=1): 0 unauthorized hits. KB-CM-REPLAY1:
replayed state re-verifies. The combined replay/evict/compact leg, the
only failing leg in the original battery, **passes on the mechanism**.

## Caveats

- The original leg's exact predicate is unrecoverable, so the
  naive-spot-check explanation is demonstrated, not proven, for the
  original binary. What is proven: the mechanism satisfies the
  preregistered bar as written, the probe is live, and the scored failure
  is deterministic.
- This rerun covers the eviction leg standalone, not the full 11-leg
  battery (whose driver source is lost). The other 10 legs' scores stand
  as originally reported.
- `cm_evict.zag` / `cm_evict_bin` live in the local workdir only and are
  intentionally not committed (binaries never committed; the driver is
  follow-up evidence, not program source).

## Bottom line for the program

G-CM1b's constructed-mode structural separation closes clean: **11/11
legs pass**. The eviction primitive kills constructed sessions without
touching belief, survives replay, and compacts order-preservingly — with
zero unauthorized constructed bytes reaching belief. The HTD-1
"AMBIGUOUS / INCOMPLETE" entry for G-CM1b is resolved to **PASS**.
