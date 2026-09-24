# RUNLOG — story plan-absolute instantiation

Date: 2026-09-24. Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Source: `story_plan_absolute.zag` (pure Zag, zero RNG). Full output: `story_evidence.txt`.

## Build
- `znc story_plan_absolute.zag -o story_bin` — clean build, no errors
  (E0101/E0102 arithmetic-simplification lints only, from `(b*12+0)*4` indexing).

## Bugs found during bring-up (fixed)
1. Class table order misaligned with word order → wrong beat plan. Fixed by
   reordering the classes literal to word order.
2. `heal_beat` wrote the healed length at `blen_o + b*4` into a 4-byte arena →
   runtime "slice index out of bounds". Fixed to single-slot semantics.
3. Fault-3 injection only destroyed the first anchor occurrence ("detective"
   appears twice in beat 0) → detector correctly reported 0. Fixed to destroy
   all occurrences.

## Probes (all PASS)

| Probe | Result |
|---|---|
| A fault injection | dropped anchor (b1), dropped closing line (b3), corrupted run (b0): all detected=1, healed byte-identical=1; clean beats: 0 detections, heal no-op |
| B (G)-ban | gate_register(PLAN\|RENDERED) refused (rc=1), registry unchanged; attempt_g_wire output == plan-pure render; story SHA unchanged `ffa24a2f…56d` |
| C plan event | external edit accepted (r=5, seq 12→13); beats 0/2/3 byte-identical old vs new, beat 1 differs exactly by the planned annotation sentence; unknown code refused, seq unchanged |
| D reruns | full plan+render ×3: SHA `ffa24a2f…56d` ×3, byte-identical |
| E thread audit | dropped object-thread anchor detected from rendered text; r=4 AUDIT_REPAIR logged; plan-pure re-render byte-identical, anchor present |

## Notes
- `seq_r` extended: r=4 AUDIT_REPAIR, r=5 EXTERNAL_EDIT (rule_name covers both).
- Frozen battery not run (needs Micah's signature; sibling crew drafting).
