# Preregistration: Diagnosis of H-STRESS Slot-0 Retention Failure (H-DIAG)

**Date:** 2026-09-29
**Status:** FROZEN (committed before investigation)
**Task:** Diagnose why procedure slot 0 (reverse, learned in E1) no longer maps
`hello`->`olleh` after the 16-event H-STRESS pressure sequence, while slots
1-15, bridge rules 0-3, and causal rules 0-15 remain intact.

**Background (from STRESS_RESULT.md, commit `8cd6d8cf0`):**
- E1 stores reverse at proc slot 0. Immediate check: PASS ("E1 slot 0 PASS").
- E2-E8: bridge rules 0-3 learned, proc slots 1-11 filled.
- E9: bridge full, honest -1, F-LEAK wastes proc slots 12,13.
- F1/F2: fill proc slots 14,15. Proc store 16/16 FULL.
- EK1/EK2: causal store filled 16/16, honest miss on overflow.
- Final: `proc_apply(W, PBASE(), 0, "hello", o)` fails (slot0_ok=0).
  Bridge rule 0 still dispatches correctly. Causal predictions correct.
- All 3 runs byte-identical (md5 272e75506ddcc91d46816e72a89a6382).

**Memory layout (from committed source):**
- pbase=0: proc store, 16 slots x 64 bytes (slot s at offset s*64)
  - slot offset+0: used flag (u32)
  - slot offset+4: nnodes (u32)
  - slot offset+8: program bytes (nnodes*3)
- bbase=1024: bridge store, 4 x 20 bytes
- cbase=1104: causal store, 16 x 28 bytes
- work=2048: bridge_learn scratch (seqbase, statbase, lenbase)
- pairbase=8192: pair descriptors (16 bytes each)
- ST_STR cursor at W+65000, string data from 16384 upward

**Diagnosis hypotheses (frozen):**

- **H1 (overwrite bug):** Some write after E1 corrupts W[0..64] (slot 0's
  used flag, nnodes, or program bytes). Candidates: (a) `z_alloc` heap
  collides with W region 0..64; (b) `bridge_learn` WORK-area write
  overflows backward into low W; (c) `pextract` writes past its 64-byte
  `sq` buffer; (d) `handle_proc_learn_unified` pair staging writes to a
  wrong offset. PREDICTION: dumping W[0..16] before/after the sequence
  shows changed bytes in slot 0's header or program area.

- **H2 (index confusion / read-path bug):** Slot 0's bytes are intact, but
  the final check reads the wrong slot or `proc_apply` mis-evaluates.
  Candidates: (a) `slot_rev` variable clobbered between E1 and final
  check (it is a main() local; verify it is still 0); (b) `proc_apply`
  with nnodes=0 or corrupted nnodes returns 0; (c) the final `o` buffer
  or `streq` comparison is at fault. PREDICTION: W[0..64] byte-identical
  before/after, but `proc_apply` returns 0 or wrong output.

- **H3 (intentional eviction):** The architecture deliberately evicts or
  reuses slot 0 under pressure. PREDICTION: source contains an eviction
  path (none seen in `proc_store`, which only scans for used==0; this
  hypothesis is expected to be REFUTED by code reading).

- **H4 (bridge interference):** `bridge_learn` or `br_store` writes outside
  the bridge region (1024..1103) into slot 0 (0..64). PREDICTION: the
  corruption appears exactly after a bridge_learn call (E2/E4/E6/E8/E9),
  and a per-event slot-0 dump pinpoints the corrupting event.

**Method (frozen):**
1. Pure Zag, no Python. Shell tools (grep, sed, md5sum) only for analysis.
2. Do NOT modify the mechanism. Only add diagnostic output in a COPY of
   the file built to /tmp, or use existing emit traces.
3. Steps:
   a. Code-read `proc_store`, `proc_apply`, `bridge_learn`, `br_store`,
      `handle_proc_learn_unified`, `pextract`, and the main() event
      sequence for any write to W[0..64] after E1.
   b. Build a diagnostic copy that dumps slot-0 header bytes
      (W[0..16]) after each event E1..E9, F1, F2, EK1. Identify the first
      event after which the bytes change (or confirm they never change,
      supporting H2).
   c. If bytes change: pinpoint the corrupting write by narrowing to the
      specific function call within that event.
   d. If bytes never change: test H2 by checking `slot_rev`, `nnodes`,
      `proc_apply` return value, and output bytes at the final check.
4. Determinism: diagnostic runs must reproduce the committed md5 when
   diagnostic output is excluded.

**Kill bars for this diagnosis:**
- **K-D1 (root cause identified):** PASS if the exact corrupting write
  (function, line, and reason) OR the exact read-path fault is identified
  with evidence. Vague "maybe X" = FAIL.
- **K-D2 (bug vs limitation classified):** PASS if the report states
  definitively whether this is a memory-safety bug (fixable with a
  bounded code change) or an architectural limitation (requires redesign),
  with reasoning.
- **K-D3 (fix sketched):** PASS if the report describes a concrete fix
  (or explains why no local fix exists), without implementing it
  (implementation is out of scope for diagnosis).

**What success looks like:** "Slot 0's nnodes at W[4] is overwritten by
function F at line L during event E because [reason]. This is a [bug /
limitation]. Fix: [concrete change]."

**What failure looks like:** No corrupting write found and no read-path
fault found; root cause remains unknown.
