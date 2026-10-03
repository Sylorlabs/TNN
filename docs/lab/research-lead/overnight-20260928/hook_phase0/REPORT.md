# REPORT: HOOK-PHASE0

## Verdict

BUILD-PASS. All 7 frozen kill bars green (HP-R1, HP-A1, HP-A2, HP-A3,
HP-A4, HP-A5, HP-H1). Prereg 0563dab9f committed strictly before any
implementation.

This is infrastructure, not invention. Nothing in this lane claims
the learner learned, invented, or stamped anything. What was built:
(A2.6) a mutation-event counter bumped by both world-mutation
functions in lane base, and (A2.1) a bump allocator over a carved S
region plus a learner-writable registry table. Both are substrate
the learner could later use; neither is used by the learner here.

## 1. Task

MUTATION-HOOK recommended approving Phases 0-1 "as infrastructure
when capacity allows; keep Phases 2+ gated." This wave implements
Phase 0 (A2.6 + A2.1), which the report decomposed as independent
and buildable now with no protected-core change and no governance
needed. A2.2 (learner-created operation bodies) is explicitly not
implemented: it requires the protected-core EXECUTE primitive and is
gated on Micah's still-pending 2026-09-30 placement ruling.

## 2. Implementation (additive deltas over EPOCH-STRONG, frozen)

Lane `docs/lab/research-lead/overnight-20260928/hook_phase0/`,
file prefix `hp_`, built on the EPOCH-STRONG substrate (no
redesign).

- hp_world.zag, hp_module.zag, hp_learn.zag: byte copies of the es_
  originals (cmp-verified identical).
- hp_base.zag: es_base.zag plus exactly three deltas:
  (a) fact_add bumps S cell 932 inside the existing `if(n<64)`
  guard (a rejected store is not a mutation);
  (b) fact_set_obj bumps S cell 932 on every call;
  (c) appended A2.1 section: la_alloc (bump allocator, cursor in S
  cell 933, region S bytes [3736,4120) = cells 934..1029, 4-byte
  alignment, -1 on exhaustion/negative size) and la_reg
  (8-entry [cell, tag, ev0, ev1] table at S cells 1030..1061,
  count at 1062, -1 when full). Lane-base code only:
  get32/set32, arithmetic, branch. No protected-core change.
- hp_main.zag: es_main.zag plus STAGE HP-P0 (one contiguous block,
  zero removed lines) inserted before o_flush. It exercises the new
  machinery the way learner code could: reads the counters, runs a
  70-store guard probe on a scratch arena, allocates/writes/reads
  back two blocks across calls, probes exhaustion/alignment/
  negative size, and registers/reads back registry entries. All
  probe values are runtime-derived (fact 0 triple, r601x); no world
  literals in new code.
- hp_build.sh mirrors es_build.sh (pinned znc
  znc_linux_x86_64_abed8aa1, safebin PATH).

Cell audit (frozen in prereg): highest S cell touched by any
literal or computed access in the es_* sources is 3210;
zero_counters touches 7, 900-924. Cells 932, 933, 1030..1062 are
otherwise untouched. The counter is per-S-arena state, not global.

## 3. Results (frozen bars)

- HP-R1 (regression): PASS. hp_run1.txt lines 1-146 byte-identical
  to es_run1.txt lines 1-146. The new machinery is present but the
  pre-existing battery cannot observe it.
- HP-A1 (A2.6 exactness): PASS. `HP-MUTCNT s2=506 s=192` exactly.
  S2: 6x setup_worldA + 3x setup_worldA2 = 504 fact_add, plus the
  ES-C and ES-E fact_set_obj calls = 506. S: 2x setup_worldA (S1A,
  demo_cov_revise) + 2x setup_worldB (demo_cov_revise, S5) = 192.
  The per-arena split (506 vs 192, not a global 698)
  discriminates per-arena state from a global counter.
- HP-A2 (guard semantics): PASS. `HP-GUARD c0=506 c1=570 delta=64`
  exactly. 70 stores into a scratch arena advanced the counter by
  64: the bump sits inside the `if(n<64)` guard, so rejected stores
  do not count. A bump-on-call placement would have read delta=70.
- HP-A3 (A2.1 allocator): PASS.
  `HP-ALLOC a1=3736 a2=3752 a3=-1 a4=3784 a5=-1 rd1=1 rd2=1`
  exactly. Bump math (3736, 3752), exhaustion sentinel (-1, cursor
  uncorrupted: the 7-byte request still landed at 3784),
  alignment (7 -> 8), negative size (-1), and both blocks read back
  byte-exact after later allocations (rd1=rd2=1: persistence across
  calls).
- HP-A4 (A2.1 registry): PASS.
  `HP-REG e0=0 e1=1 r0=1 r1=1 full=-1` exactly. Two entries
  round-trip field-exact via the learner's own sg primitive; the
  9th registration returns -1.
- HP-A5 (protected core untouched): PASS. cmp-verified byte copies
  for world/module/learn; zero 932/933/la_* hits outside base+main;
  the base diff holds only the two bump lines and the la_alloc/
  la_reg section; no file outside the lane modified; znc untouched.
- HP-H1 (toolchain/hygiene): PASS. Safebin for all commands;
  `which python3`/`which python` empty; pure Zag; pinned znc;
  prereg committed alone before implementation (0563dab9f);
  3/3 byte-identical runs, stderr empty, exit 0; zero em/en dash
  bytes; no world literals in new executable code.
- `SUMMARY-HOOKPHASE0 mutcnt=506 alloc_ok=1 reg_ok=1`.

## 4. Honest labeling (what this is not)

- The counter is researcher-placed infrastructure, not a learner
  invention. A learner reading sg(S,932) would be observation, not
  stamping.
- The allocator hands out untyped bytes; assigning semantics is the
  learner's future job. The registry stores associations, not
  meanings: no meaning vocabulary is enumerated or learned here.
- Phase 0 changes nothing about what the learner can DO with
  mutation events: no dispatch table, no hook installation, no
  operation bodies. Behavioral change arrives no earlier than
  Phase 1 (inert dispatch, still no invention claim) and the strong
  sense no earlier than Phase 2 (gated on the EXECUTE ruling).
- The fn-value hook table (MUTATION-HOOK T1/T2) was not installed.
  Per G3/G4 of that report, installing it now would be dispatch
  infrastructure only, and any "learner installs a hook" demo
  before A2.2 would be menu selection wearing a hook's clothing.
- 56 facts is a toy world; the counter and allocator are O(1)
  machinery, not scaling results.

## 5. Artifacts

- `NAMECHECK.md`: toolchain guard Step 0, scope, commit discipline.
- `PREREG.md`: frozen kill bars (committed alone at 0563dab9f).
- `REPORT.md`: this file.
- `hp_base.zag`, `hp_world.zag`, `hp_module.zag`, `hp_learn.zag`,
  `hp_main.zag`, `hp_build.sh`: implementation.
- `hp_full.zag`, `hp_bin`, `hp_compile.txt`: build products.
- `hp_run1/2/3.txt`: 3/3 byte-identical (154 lines), stderr empty,
  exit 0.

## 6. Follow-ups (not started)

- Phase 1 (A2.3 inert dispatch): hook slot consult in both mutation
  functions, default 0 = no hook; preregistered bars: byte-identical
  regression with slot 0, a unit probe installs a researcher-written
  body via fn bits and observes exactly one fire per mutation,
  uninstall returns to byte-identical; the probe body labeled
  researcher-written, no invention claimed. Needs no governance per
  MUTATION-HOOK, but is a separate prereg.
- Phase 2+ (A2.2, A2.3 strong sense, A2.5, A2.4): gated on Micah's
  EXECUTE placement ruling (G1). Not started here.
