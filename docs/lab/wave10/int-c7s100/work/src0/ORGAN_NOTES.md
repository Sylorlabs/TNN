# ORGAN_NOTES.md — INT-1 organ implementation notes (2026-09-20)

## Architecture

All five organs are native Zag modules in `impl/`. Imported Zag modules
cannot hold mutable globals (globals are root-only, scalar-only,
zero-initialized), so every organ threads its state as an explicit first
argument `*O#S`, with `o#_init` constructors returning the state struct.
This is a forced architectural constraint, not a design choice.

- **O1** (`o1_memory.zag`) is a thin organ layer over the ported store
  substrate (`substrate/st_memory_core.zag`): deliberate add/kill/pin/
  promote/demote/evidence, staged autonomy, amendment-B pin expiry
  (serving-trace pins expire after 50 `o1_new_episode` ticks without
  re-service; re-service resets the clock; expiry lifts are ledgered as
  `O1_OP_PIN_EXPIRE` and are not rollbackable).
- **O2–O5** keep their own chunked append-only audit ledgers via
  `substrate/o_audit.zag` (4 MiB chunks, 16-word entries, organ tag in
  the op-word high 16 bits, fail-close code 107 on a full ledger).
  Audit layout everywhere: stage word 13 / byte 52, d1 word 14 / byte 56,
  d2 word 15 / byte 60.

## Frozen laws honored

- Zero randomness anywhere in AI decision paths (static scan clean;
  O4's pool selectors are pure modular functions of the trace index).
- O1 arm B only: `o1_kill`/`o1_kill_evidenced` force `ST_ARM_B`;
  strength never gates a kill. Pins, force-pins, CORE, stage still gate.
- O2 corroborated elimination only (2 positive observations confirm,
  2 contradictions refute); HDE v1 excluded. Disconnect is audit-first
  and idempotent.
- O3 never silently drops: empty candidate pool is an audible `310`
  refusal. Pins/force-pins are skipped via O1's legal-victim query;
  PREEMPT takes the caller-provided legal candidates and selects
  weakest strength, ties broken by lowest slot (deterministic).
- O4 verifies at composition time; blind apply; refusal codes
  2101–2105; ABSTAIN opens O2 via the seam (out of organ scope).
- O5 R=50 frozen (constitution refusal 204); ELIM_STRICTNESS excluded
  from INT-1 (224). Constructive commits need only a staged, in-bounds
  proposal; destructive commits (lowering) additionally require stage
  FULL, ≥2 justifications, and prediction ≥0.

## Substrate repairs made (not in the protected list)

1. `substrate/st_memory_core.zag` had two corrupted lines where a
   comment swallowed the following statement (`// INT-1: mask organ
   taglet rc:i32=...`); restored the `rc`/`slot` declarations.
2. `st_evidence_audit` demanded justification for arm-B evidenced kills,
   contradicting the arm-B law the substrate itself implements (arm B
   bypasses the evidence/effort gate). The checker now reads the applied
   arm from d2 and skips the evidence/justification checks for arm-B
   kills.

## Verification (native, 2026-09-20)

Temporary harness `zz_organ_harness.zag` (deleted before handoff)
exercised the full task API: 60+ checks across all organs, including
refusal paths (O4 2101/2105/2106/2107, O5 204/221/222/223/224, O3
310/311/312, O2 201/202/203, O1 pin/force-pin/stage gates), the O1→O3
PREEMPT chain, O1 pin expiry (49 ticks still pinned, 50th expires,
re-service resets), and every organ's `replay_check`. Result: 0
failures. Two consecutive runs produced byte-identical stdout
(deterministic). Static scan: no RNG/clock/rdtsc in any organ.

## Known glue incompatibility (NOT fixed — glue is owned elsewhere)

The current `loop.zag`/`_check.zag` still use the stub signatures from
`organ_stubs.zag` and will not compile against these organs. The
coordinator must update the glue; the task API (INTERFACE_HASHES.md)
is authoritative:

- `o2_init_cal()` → `o2_init(cap:i32)`
- `O3S{.n=0}` → `o3_init()` (opaque state; no struct literals)
- `O4S{.needs=0}` → `o4_init()`
- `O5S{.v=2,.r=50,.pv=2}` → `o5_init()` (defaults V=2,R=50)
- `o3_preempt(o,id,out)` → `o3_preempt(o,candidates,n,strengths,obs,out)`
- 5-arg `o4_need` → 8-arg `o4_need(o,qid,req_ent,req_ops,prov,max_age,kind,just,out)`
- `o4_compose(o,need,scan_count,out)` → `o4_compose(o,need,out)`
- integer cue/output `o4_apply` → 32-byte vector `o4_apply(o,trace_id,cue,out)`
- `loop_stage_enter` must call `o1_set_stage` (currently missing)
- O3's PREEMPT needs the caller (seam) to supply legal candidates from
  `o1_victim_candidates`, excluding pins/force-pins and the loop's CORE
  slots by index (`exclude_lo`)
