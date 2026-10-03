# REPORT: LEARNER-EPOCH

## Verdict: all 9 kill bars green (LE-R1, LE-S1, LE-B1, LE-B2, LE-B3, LE-B4, LE-B5, LE-K1, LE-H1)

Non-ledger task. Branch `tnn-native-lab`, lane
`docs/lab/research-lead/overnight-20260928/learner_epoch/`, file prefix
`le_`. All commits local, never pushed.

## What was built

Act 5 (stages S14A-S14G) on top of the STALE-INDEX-RECOVERY battery,
as the follow-up to its open item: "the epoch bump discipline is
stage-code instrumentation in this experiment, not learner-owned
mutation tracking."

Additive deltas over si_*: le_base.zag gains `w_epoch_bump(S)` /
`w_epoch_get(S)` (direct get32/set32 on byte 931*4, since sg/ss are
defined later in the module file), `fact_add` gains the S parameter
and stamps inside the `n<64` success guard, and the new
`fact_set_obj(S,A,idx,o)` performs in-place object mutation plus one
stamp; le_world.zag threads S through the three `setup_world*`;
le_module.zag and le_learn.zag are byte-copies of si_*; le_main.zag
threads the in-scope state through every `setup_world*` call site,
deletes all seven stage-code `ss(S2,931,sg(S2,931)+1)` bumps, routes
the adversarial in-place mutation through `fact_set_obj`, and replaces
the S13 block with the S14 battery. No mechanism redesigned. No new
state cells: S+930, S+931, L+14020, L+14036, L+14040 reused.

## Design answers

**Q1: what signal does the learner use to bump the epoch?** Mutation
events at its own world interface: every successful `fact_add` and
every `fact_set_obj` advances the epoch exactly once. Reads never
stamp (LE-B4: e0=337 e1=337 across three queries). The epoch is a
conservative mutation counter, not a content comparison; the checksum
stays the precise content signal.

**Q2: is the stamping unilateral?** Yes, in the operation sense:
`le_main.zag` contains zero occurrences of the epoch cell literal
(LE-S1), yet the N1 reorder is still detected (LE-B1: ver_stale=7)
and the adversarial same-nf mutation is still detected (LE-B3:
ver_stale=7). Deleting every stage bump changed nothing observable;
in SI the same deletion would have yielded ver_stale=0.

**Q3: honest status, is this researcher code in disguise?** Partly,
and the prereg froze this verdict in advance (A4), so it is not a
post-hoc hedge. The epoch cell, its monotonic semantics, the choice
of mutation events as the signal, and the placement of the bump inside
the two operations are researcher-designed. The learner did not invent
versioning, did not choose the signal, and does not deliberate about
when to bump. No L2/L3 invention evidence is claimed. What genuinely
moved is the maintenance of the invariant: from harness discipline
(every stage-code mutation site must remember to bump, the exact
discipline whose breach caused the N1 stale-index bug) to operation
guarantee (the mutation itself stamps). The bug class eliminated is
"the harness forgot to instrument a mutation path". The bug class NOT
eliminated is "a future mutation path bypasses the two ops with raw
array writes": that stays a discipline issue, auditable by the LE-S1
style grep, not enforced by the compiler. Against overnight priority
5 (learner-created cognitive-operation bodies): this is the weak
sense only. The "stamp version on mutation" operation body now lives
in the learner's world interface rather than the harness. The strong
sense, the learner creating that operation body itself from
experience, is not demonstrated and is named below as future work.

## Results per bar

- LE-R1 regression: PASS. le_run1.txt lines 1-97 byte-identical to
  si_run1.txt lines 1-97 (diff empty).
- LE-S1 no stage-code epoch touches: PASS. `grep -c 931 le_main.zag`
  is 0. Epoch writes exist only in le_base.zag (`w_epoch_bump`,
  called by `fact_add` and `fact_set_obj`); the only other `931`
  occurrences in the lane are the four pre-existing `sg(S,931)` reads
  in le_learn.zag (three specialization recordings plus the
  `spec_ver_stale` compare).
- LE-B1 N1 reorder, zero stage bumps: PASS. S14B line exactly
  `LE-PROBE nf_stale=0 ck_stale=7 ver_stale=7`.
- LE-B2 proactive recovery: PASS. S14C zero RETRY lines; LEQ0 single Q
  line `goal=820 st=2 vers=2 ans=2:1,611 agree=1 cs=16 cg=56`
  (byte-identical shape to SIQ0); `LE-AUTO entry_mask=7`.
- LE-B3 adversarial, learner-op mutation: PASS. `LE-MUTATE nf=56
  dup_at=4 from=5` (runtime-derived indices, same as SI); S14D probe
  exactly `LE-PROBE nf_stale=0 ck_stale=7 ver_stale=7`; zero RETRY;
  LEQ0A single Q line st=1 vers=2 agree=1; `LE-AUTO entry_mask=7`.
- LE-B4 read-no-stamp control: PASS. `LE-EPOCH-READ e0=337 e1=337`
  (e0 == e1, queries do not stamp); `LE-EPOCH-MUT e1=337 e2=338`
  (e2 == e1+1, one learner-op add stamps exactly once).
- LE-B5 reactive safety net: PASS. S14F exactly 2 RETRY lines; LEQ0R
  3 times with (agree=0,vers=2), (agree=0,vers=2), (agree=1,vers=0);
  RETRY att=1 `dc=1,0,0 active=1,1,1 req=0 first=500`; att=2
  `dc=2,0,0 active=0,1,1 req=0 first=500`.
- LE-K1 cost preserved: PASS. `LE-VERDICT proactive_total=984
  reactive_total=1152`, 984 < 1152. The absolute totals reproduce
  SI's exactly (proactive q=648 steps=336; reactive q=1152 steps=0),
  so learner-owned stamping preserves the SI cost structure with no
  added step cost.
- LE-H1 toolchain/hygiene: PASS. Safebin for all build/run/verify
  commands (two read-only recon calls predate the export, noted in
  NAMECHECK); pure Zag; pinned znc; prereg committed alone before
  implementation (fe96d7874); 3/3 byte-identical (sha256
  14f17da5ce1a67607fc58594ac95bfa918f941b1c67b0894e6e44904969726ca),
  stderr empty, exit 0; zero em/en dash bytes in authored files;
  43 A0102 warnings, same count as si_compile.txt; no world literals
  in new executable code (S14 region scanned: tags/rels/objs/goals,
  mutation indices, and the S14E triple all runtime-derived).

SUMMARY-LEARNEREPOCH (frozen, reproduced exactly):
`agree=29 plans_built=5 plans_loaded=29 trials=12 declines=0 cs=1728
cg=3808 hook=1 covdc=2,0,0 steps=2464`.

## Recommendation

Adopt operation-owned stamping as the epoch discipline going forward:
it eliminates the N1 missed-bump bug class for every mutation path
through `fact_add`/`fact_set_obj`, at zero measured step cost, with
the checksum kept as the audit signal for content precision and the
reactive trigger-B path kept as the safety net. Do not claim more
than mechanism placement: the epoch concept remains
researcher-designed.

## Follow-ups (not claimed here)

1. Learner-created stamping (strong sense of priority 5): the learner
   installs or revises the stamping operation itself from experience
   of a missed-bump failure, rather than receiving it by placement.
2. Content-change-only epoch: bump only when the mutation changes
   content, instead of the frozen conservative per-op-call choice.
3. Enforcement for the two-op rule: raw `set32(A,...)` writes still
   bypass stamping; options are audit (LE-S1 grep), op-only world
   handles, or capability discipline.
4. SI follow-ups 2-4 remain open: checksum audit policy, cost
   structure at scale, proactive placement (do_query entry vs compose
   spec-dispatch).

## Commits (local only)

- fe96d7874 (prereg + namecheck, alone, pre-implementation)
- (implementation: le_*.zag sources + le_build.sh)
- (artifacts: le_full.zag, le_bin, le_compile.txt, le_run1/2/3.txt/err)
- (this report)

## Artifacts

- `le_base/world/module/learn.zag`: sources (base = si_base plus
  w_epoch_bump/w_epoch_get/stamping fact_add/fact_set_obj; world =
  si_world with S threaded; module/learn byte-copies of si_*)
- `le_main.zag`: si_main with state threaded through setup_world*
  call sites, zero stage-code epoch writes, S13 replaced by S14
- `le_build.sh`: build script
- `le_full.zag`, `le_bin` (sha256
  5cd709047e0ecf40d9b84f0f870fe839b16ecba9ad56fd4d2860caa0f18bead)
- `le_run1/2/3.txt`: 3/3 byte-identical (143 lines), stderr empty
- `le_compile.txt`: clean compile log (43 pre-existing A0102 notes,
  same count as si_compile.txt)
