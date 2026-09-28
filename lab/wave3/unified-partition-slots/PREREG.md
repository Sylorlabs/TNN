# PREREG — UPT1: switching ops over unified partition-slots (BUILT 2026-09-19)

## Amendment record (program law, Micah, 2026-09-19 — applied before any run)

1. **Scaling allowed.** Added explicit scale dimension (§6 of
   UNIFIED_DESIGN.md): 10x/100x arguments for slots, horizon, regimes,
   audit; next scale test ST2 named. No trial has been run yet, so no
   results are amended.
2. **No RNG in the AI.** The design contains no RNG in any decision path
   (UNIFIED_DESIGN.md §4): first-free-slot allocation, slot-order verify
   scan, first-verified commit, label alternation, deterministic streaks.
   Nothing was removed — the design was RNG-free from the first draft.
3. **Designed adversarial curriculum.** The harness uses **zero RNG** —
   not even seeded scaffolding. Every probe batch is an explicitly
   designed (hits,total) pair targeting a named mechanism property (table
   below). The verdict will distinguish "the system is deterministic"
   (byte-identical runs; no randomness in any path) from "the test was
   adversarial" (designed boundary cases).

## Amendment 2026-09-19, post-first-run (honest correction, not silent)

First run: `UPT1_FAILURES,1` — only `rollback_switch` failed. Cause: the
prereg's rollback battery expected the second `ROLLBACK_LAST` to walk back
to the older RECORD op; the implemented (and MA1-inherited) semantic is
**single-level undo**: the ledger is append-only, so the second rollback
finds the same SWITCH entry and re-applies the same undo (idempotent).
This is a semantics clarification, not a mechanism failure: the design
doc §2 now states single-level/idempotent explicitly, the trial asserts
the repeat leaves state unchanged, and criterion 8 below is corrected.
No other expectation changed; nothing was silently rerun.

## Hypothesis

One unified slot type can serve as both a memory-agency slot
(ADD/KILL/PIN/UNPIN/PROMOTE/DEMOTE, CORE/USER, staged autonomy) and a
context partition (declared label + recorded evidence, verified SWITCH)
with **no cross-family interference**: memory ops never corrupt evidence,
context ops never corrupt memory fields or destroy knowledge by
switching, one ledger replays to exact full state (slots + stage +
active), and the refusal semantics of both families compose under one
documented precedence table.

## Apparatus

Native Zag on this Linux VM (`znc` at
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
`up_core.zag`: unified store, UP_CAP=8 slots, audit cap 1024 entries × 19
words. `trial_upt1.zag`: the protocol below. `run_upt1.sh`: compile, run
twice, require byte-identical stdout, require every `CL_CHECK` line
actual==expected. **No git pushes.**

The learner policy (when to probe, verify, propose) is protocol-fixed in
the harness — the honest boundary inherited from MA1/HT1. What is under
test is the *mechanism*: the unified op set, its refusals, its ledger.

## Mechanics

**Stage setup.** Scratch store S0: at stage NONE, `UP_ADD`/`UP_PROPOSE`/
`UP_RECORD`/`UP_SWITCH`/`UP_KILL` must all refuse `REFUSED_STAGE`; at
stage ADD, `UP_PIN`→`REFUSED_STAGE`, `UP_SWITCH`→`REFUSED_STAGE`
(precedence: STAGE before UNVERIFIED); at stage MANAGE, `UP_PIN`→OK,
`UP_KILL`→`REFUSED_STAGE`.

**Main store** at stage KILL(3):
1. `UP_ADD(10,USER)`→A, `UP_ADD(90,USER)`→B, `UP_ADD(100,CORE)`→C.
   `UP_PIN(B)`. `UP_PROMOTE(A)`→LONG (tier moves, region untouched).
2. `UP_PROPOSE(0,60)`→P0, `UP_SEED(P0)`, `UP_PROPOSE(1,60)`→P1,
   `UP_PIN(P0)` — pinned partition keeps recording (the §3b test).

**Designed curriculum** (40 episodes; every probe batch is a designed
`(hits,total)`; the "learner" never sees `true_reg`):

| Phase | Eps | true_reg | Designed batches (active unless noted) | Expected mechanism behavior |
|---|---|---|---|---|
| P0 baseline | 0–7 | 0 | ep0: 16/16; ep1–6: 15,14,15,14,15,14 /16; ep7: measurement block (read-only) | no verify, no switch; bad streak 0 |
| P1 false alarm | 8–11 | 0 | ep8: active 3/16 → verify: P1 2/16 → PROPOSE(1)→P2, P2 2/16 → SWITCH refused | **1 REFUSED_UNVERIFIED**, 0 commits; active still P0 |
| | | | ep9–10: 15,14/16; ep11: measurement block | recovery, no switch |
| P2 true flip | 12–15 | 0→1 at ep12 | ep12: active 2/16 → verify: P1 15/16 → SWITCH commits | **exactly 1 committed switch** |
| | | | ep13–14: 16,15/16; ep15: measurement block | |
| P3 boundary | 16–23 | 1 | ep16: 8/16 (exactly half — neither majority) | no verify (bad stays 0) |
| | | | ep17: 9/16 | no verify |
| | | | ep18: active 2/16 → verify: P0 8/16, P2 8/16 → PROPOSE(0)→P3, P3 8/16 → SWITCH refused | **1 REFUSED_UNVERIFIED** at the boundary |
| | | | ep19–22: 15,14,15,16/16; ep23: measurement block | |
| P4 rapid double flip | 24–31 | 1→0 at ep24, 0→1 at ep26 | ep24: active 2/16 → verify P0 15/16 → SWITCH commits | **2 committed switches** (designed churn) |
| | | | ep25: 16/16; ep26: active 2/16 → verify P1 15/16 → SWITCH commits | both labels survive, distinct |
| | | | ep27–30: 15,16,15,16/16; ep31: measurement block | |
| P5 pressure | 32–39 | 1 | ep32–39: 15,16,15,16,15,16,15,16/16 (no verify) | no curriculum switches |
| | | | scripted: KILL(P2)→OK (fields zeroed); ROLLBACK_LAST→P2 restored; KILL(P2)→OK; PROPOSE(0)→P4 (fills slot 5); PROPOSE(1)→P5 (fills slot 7, store full); PROPOSE(0)→REFUSED_FULL | deliberate destruction + restore + capacity gate |
| | | | refusal battery: KILL(active=P1)→REFUSED_ACTIVE; KILL(P0 pinned)→REFUSED_PINNED; KILL(C)→REFUSED_CORE; KILL(P4 just killed)→REFUSED_NOTLIVE; RECORD on plain slot A→REFUSED_NOTPARTITION; SWITCH to plain slot A→REFUSED_NOTPARTITION; PROPOSE(-1)→REFUSED_BADLABEL; RECORD(P1,17,16)→REFUSED_BADVAL | every refusal kind exercised |
| | | | rollback battery: RECORD(P1,2,16); RECORD(P3,15,16); SWITCH(P3)→OK (switch #4); ROLLBACK_LAST→active back to P1, P3 at pre-switch 15/16; ROLLBACK_LAST again→same undo re-applied, state unchanged (single-level) | rollback over both families incl. store-level active |
| | | | settle: 4 eps regime 0 (designed 15/16, verify may fire — counted), 4 eps regime 1, then uncorrupted 16-probe reads per regime | endpoints 16/16, 16/16 |

Measurement blocks (ep 7,11,15,23,31 + settle): uncorrupted 16 probes on
the active partition, read-only, never fed to RECORD. Designed probes
make these exact: 16/16 iff declared label == true_reg.

**In-trial audit scans** (same binary, after the script):
- `up_audit_clean_refusals`: every refused entry has before==after.
- `up_replay_check`: replay from genesis == exact live state (all slot
  fields + stage + active).
- `up_switch_verified_scan`: every committed SWITCH carried
  target-majority-positive AND old-active-majority-negative evidence.
- `up_isolation_scan`: for every committed SWITCH/SEED, all slot
  snapshots before/after identical (only `active` moved); for every
  RECORD, only the target slot's hits/total/bad changed.
- Structural: ≥2 live partitions with distinct declared labels;
  no partition-kind slot with region==CORE; `active` always a live
  partition; pinned slots live at endpoint.

## Pass / fail criteria (falsification)

UPT1 PASSES iff ALL hold (each is a `CL_CHECK`):
1. `stage_gates`: all stage-battery refusals exact, all legal stage ops OK.
2. `false_alarm_no_commit`: P1 produced ≥1 REFUSED_UNVERIFIED and 0
   committed switches; active unchanged across P1.
3. `flip_commits`: P2 produced exactly 1 committed switch; P4 exactly 2.
4. `boundary_refuses`: P3's near-miss verify produced REFUSED_UNVERIFIED,
   0 commits; the 8/16 batch did not increment the bad streak.
5. `no_collapse`: zero measurement blocks ≤4/16 (designed: all 16/16).
6. `endpoints`: settle reads 16/16 in regime 0 AND regime 1 (per-regime,
   never aggregate-only).
7. `kill_semantics`: KILLed partition fields all zero; ROLLBACK restored
   P2 fully (live, label, value, evidence, pinned, tier, region, step,
   created); REFUSED_ACTIVE/PINNED/CORE/NOTLIVE/FULL all exact with state
   untouched; pinned partition accepted RECORD throughout.
8. `rollback_switch`: after the battery, active==P1 and P3's evidence ==
   pre-switch snapshot (15/16); a repeated ROLLBACK_LAST re-applies the
   same undo idempotently (single-level semantic, amended 2026-09-19).
9. `audit_clean`, `replay_exact`, `switches_verified`, `isolation_holds`,
   `structural`: all scans pass.
10. `determinism`: runner requires byte-identical stdout across two runs
    (no RNG anywhere in binary — system or harness).

**FAIL the unification** (NEGATIVE verdict) if any of 1–10 fails, and
name which falsification story from UNIFIED_DESIGN.md §8 it instantiates
(cross-talk / ledger incoherence / refusal conflict / PIN paradox / CORE
leakage / switch-as-destruction).

**FAIL the trial design** (not the mechanism) if a *designed* sequence
turns out not to exercise what it claims (e.g. a phase produces no
verify) — report honestly, fix the sequence, rerun; do not silently
adjust expectations.

## What it does NOT show

- Learner-driven probe timing or label choice (protocol-fixed; HT2).
- CORE graduation (external gate; future).
- Scale: UP_CAP=8, 40 episodes, 2 regimes. The scale argument and ST2 are
  in UNIFIED_DESIGN.md §5 — this trial does not claim them.
- Multi-user region keying.
- That the learner's declared values are *good* judgments (values are
  protocol-fixed; judgment quality is MA3/Phase-4 work).
