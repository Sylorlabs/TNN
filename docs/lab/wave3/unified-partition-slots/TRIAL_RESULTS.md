# UPT1 — Trial results: switching ops over unified partition-slots

**Investigator:** wave-3, slug `unified-partition-slots` · **Date:** 2026-09-19
**Branch:** `tnn-native-lab` (no push) · **Prereg:** `PREREG.md` (written
before any run; one honest post-first-run amendment recorded there)
**Apparatus:** native Zag on this Linux VM · **Result: PASS —
`UPT1_FAILURES,0`, 18/18 checks, byte-identical across two runs.**

## What was built

`up_core.zag`: one slot type carrying both MA memory-agency fields
(`live/value/pinned/region/tier/step`) and CTX partition fields
(`kind/label/hits/total/bad/created`), one 8-slot store with a
store-level `active` pointer, one 19-word append-only ledger entry format
(`op,slot,rc,b1..b6,a1..a6,old_active,new_active,stage,clock`) covering
all 12 ops (ADD/KILL/PIN/UNPIN/PROMOTE/DEMOTE/SETSTAGE/ROLLBACK +
PROPOSE/RECORD/SEED/SWITCH). `trial_upt1.zag`: the preregistered
protocol. **Zero RNG anywhere in the binary** — system and harness both
fully deterministic; every probe batch is an explicitly designed
`(hits,total)` pair.

## The run (designed adversarial curriculum, 40 eps + settle)

| Phase | Designed adversity | Mechanism behavior |
|---|---|---|
| P0 baseline (0–7) | clean + mild batches | no verify, no switch |
| P1 false alarm (8–11) | true regime *unchanged*, active records designed 3/16 | verify finds nothing verifiable; fresh alternate hypothesis proposed, probed, **no commit**; active unchanged |
| P2 true flip (12–15) | active 2/16, alternate 15/16 | **exactly 1 committed switch** |
| P3 boundary (16–23) | 8/16 batches (exactly half — neither majority); near-miss verify (targets 8/16) | 8/16 does not move the bad streak; ambiguous verify produces **no commit** |
| P4 rapid double flip (24–31) | flips two episodes apart (designed churn) | **2 committed switches**; both labels survive with distinct partitions |
| P5 pressure (32–39) | scripted: KILL stale partition → fields zeroed; ROLLBACK restores it fully; REFUSED_FULL at capacity; refusal battery (ACTIVE/PINNED/CORE/NOTLIVE/NOTPARTITION/BADLABEL/BADVAL/SEEDED/SELF); pinned partition keeps RECORDing; 2 corroboration unit-refusals; 1 manual verified switch + rollback restoring `active` | all exact |
| settle | follow the regime both ways | endpoints 16/16, 16/16 |

Totals: **6 committed SWITCHes** (3 curriculum + 1 manual + 2 settle),
**2 REFUSED_UNVERIFIED** (both from the unit battery), 0 collapsed
blocks (all five measurement blocks 16/16), 103 ledger entries.

## What UPT1 proves (the hard questions, answered by measurement)

1. **KILL on a partition retires the context; switching never destroys
   knowledge.** KILL zeroed every field of a live USER partition;
   ROLLBACK restored it bit-exact (label, value, 8/16 evidence, USER
   region). The active partition cannot be KILLed (`REFUSED_ACTIVE`,
   precedence over PINNED/CORE — asserted). Across all 6 committed
   SWITCHes, every slot snapshot was byte-identical before/after (only
   `active` moved): switching preserves knowledge structurally.
2. **PIN means existence, not stasis.** The pinned partition accepted
   RECORD throughout (evidence kept fresh: 14/16 recorded while pinned)
   and refused KILL (`REFUSED_PINNED`). No PIN paradox in any reachable
   sequence.
3. **One ledger stays coherent across both op families.** Replay from
   genesis reconstructed exact live state — all 12 slot fields × 8 slots,
   stage, and `active` (`replay_exact` = 0). Every refused entry had
   before==after and old_active==new_active (`audit_clean` = 0).
4. **Corroboration survived the boundary.** The audit-level scan proved
   every committed SWITCH had target majority-positive AND old-active
   majority-negative recorded evidence (`switches_verified` = 0); the
   designed 8/16 near-miss verify committed nothing.
5. **CORE/USER × partitions: no leakage.** PROPOSE forces USER; no
   partition-kind slot had region==CORE at endpoint; CTX ops on plain
   slots refused NOTPARTITION; KILL on the CORE memory refused CORE;
   PROMOTE moved tier LONG without touching region.
6. **Cross-family isolation holds.** Per-op field-discipline scan over all
   103 entries: memory ops touched only w1 (+defined zeroing on KILL),
   RECORD touched only hits/total/bad, SWITCH/SEED touched only `active`
   (`isolation_holds` = 0 mismatches).
7. **Determinism is a property of the system, adversity of the test.**
   Two runs byte-identical (SHA256 `b02e131f…`); no RNG in any decision
   path (first-free-slot, slot-order verify, first-verified commit,
   label alternation). The stress came from designed boundary sequences,
   not stochastic scaffolding.

## The one failure and its honest amendment

First run: `UPT1_FAILURES,1` (`rollback_switch`). The prereg expected the
second `ROLLBACK_LAST` to walk back to the older RECORD op; the
implemented (MA1-inherited) semantic is **single-level undo** — the
ledger is append-only, so the repeat finds the same SWITCH entry and
re-applies the same undo (idempotent). Design §2 and the trial now state
and assert this; PREREG.md carries the dated amendment. This was a
specification clarification, not a mechanism failure — the rollback
itself (slot snapshot + `active` restore over both families) worked
exactly as preregistered on the first application.

## Honest boundaries

- Learner policy (when to probe, which label to propose) is
  protocol-fixed in the harness — UPT1 proves the *mechanism*, as
  MA1/HT1 did.
- Scale: UP_CAP=8, 40 episodes, 2 regimes, audit cap 1024. The 10x/100x
  scaling argument and the named next test (ST2: 80 slots, 400 episodes,
  10 regimes) are in UNIFIED_DESIGN.md §5 — not claimed here.
- Single-level undo only; multi-level undo is an explicit non-goal.
- CORE graduation gate, learner-driven probe timing (HT2), multi-user
  region keying: future work, unchanged.

## What it means for the program

1. **The open item from CTX_DESIGN.md §6 is closed:** a context partition
   *is* a USER-region memory slot whose value is a declared label +
   evidence — implemented, trialed, passing. The two wave-2 mechanisms
   share one substrate with no interference.
2. **Switching is proven non-destructive at the audit level**, not just
   by policy: the isolation scan shows no switch ever touched a slot
   field. "Is knowledge ever destroyed by switching?" — measured answer:
   no.
3. **The refusal families compose.** Fourteen refusal codes across two op
   families, one documented precedence table, every refusal audited with
   state provably untouched. No refusal conflict was found in any
   reachable sequence (falsification story §8.3 did not trigger).
4. Next: ST2 scale trial (UNIFIED_DESIGN.md §5), then HT2
   (learner-driven probe timing) on the unified substrate.

Evidence: `EVIDENCE_20260919T002121Z/` (compile + two runs + SHA256SUMS);
binary `upt1_trial_linux`; runner `run_upt1.sh`.
