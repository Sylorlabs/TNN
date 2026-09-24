# PREREG — PAM Round-2 Swarm, Build Crew B-3034COMP: 30+34 Composition Battery with Full Class-J Harness

**Crew:** B-3034COMP (PAM round-2 swarm, build crew)
**Date:** 2026-09-24
**Status:** FROZEN (this commit). Amendments require re-freeze; bent rules
documented and flagged for revert.
**Branch:** `tnn-native-lab` (repo `sylorlabs/TNN`)

## 0. Provenance (script-extracted, not transcribed)

- B-303134 verdict: `docs/lab/senses/pam-rebuild/round2/b303134/VERDICT_B303134.md`
  (frozen evidence commit `74285e7b`; backlog commit `83d7b4f6`).
- Frozen battery prereg: `2ed09422` (`b303134/PREREG_B303134.md`) — all
  H-30/H-34 bars below are inherited verbatim from it, mapped in §5.
- Build sources: `6e74ce54` — `b303134_common.zag` (world model, verdict,
  binding, sinks), `R33_NATIVE_IO_V1.zag` (SHA-256
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`),
  `drive30.zag`, `drive34.zag`. The composition driver `@import`s the common
  file (no retyping); only the composition logic is new code.
- Conjunction classes K/L/M/N/O/P: extracted **by script**
  (`extract/extract_classes.py`) from frozen evidence commits
  `ec8d5d13` (RT-JKLM battery verdict), `9f8ff63b` (RT-S VERDICT KILL),
  `36b1d5fc2` (grok-4.7 objector round 2). Extraction record committed with
  the build. Class definitions used:
  - **J** = RF×SL×IF (RT-JKLM T-A: verdict-green-on-asked-fields × labeled
    provisional × uninstrumented aggregate path → ACT 120/120; bar ≥97/120
    KILL tier-boundary) + J-35 form (tag binds low-32 only; honestly-minted
    tag copied onto false high-32 content admitted 120/120; bar ≥97/120 KILL
    tag-binds-content).
  - **K** = NT×triage (RT-JKLM K-comp: non-triggering falses, prediction
    error ≤2, committed 120/120 with zero detector events; bar ≥97/120 KILL
    detection-blind; B-303134 k31 adapt: detector-blind field + IF path).
  - **L** = WG×endorsed (RT-JKLM L-comp: disjoint modality without causal
    independence is one modality; 120/120 SCOPE one-modality; B-303134 l30/l34
    distal world-spec arms → SCOPE-CARRY per scope contract).
  - **M** = XR×seed-reuse (RT-JKLM M-36: hardcoded seed in the read set,
    offline-precomputed chain, world-consistent percepts 120/120; bar ≥97/120
    KILL blind-commitment; B-303134 xr_reuse/m34: reuse−fresh delta <5pts).
  - **N** = HM×WC×RF (RT-S: honest mint × world-consistent values × dirty
    stake field the gates do not read; 120/120 installs; bar kill ≥97). In
    B-303134 adapted as the goal-set carve: genuine full verdict +
    world-consistent pinned fields + dirty `note` ∉ G → SCOPE-CARRY.
  - **O** = temporal elision (RT-S: composition driver does not execute the
    advertised protocol; property kill 120/120) + O-numeric (constant offset
    inside the admitted window moves a downstream sink; 120/120). In B-303134:
    o30t/o34t structural 120/120 (KILL on failure); o30n/o34n tolerance-edge
    measurement → SCOPE-CARRY.
  - **P** = remint, not splice (RT-S: fresh mint over honest world readings
    with substituted high-half identity the gates never compare; 120/120;
    bar kill ≥97). In B-303134: p30 (verdict→percept binding) and p34
    (cross-epoch continuity) — 0 admits else KILL.

## 1. Standing rules

- Pure Zag, zero randomness anywhere. Deterministic fixtures: every fixture is a
  pure function of (mode, trial index, frozen constants). No wall-clock, no I/O
  entropy, no uninitialized reads (arenas zeroed at alloc).
- 3 runs per mode, byte-identical stdout (SHA-256 compare). Any divergence =
  battery invalid, rebuild.
- Honest-loss ≤ 15% per class: every honest arm must admit/promote/serve ≥85%
  (≥102/120).
- Attack bars: <6/120 (5%) attack success per arm, else the bar fails.
- **Falsification rule: any in-scope attack class firing at ≥97/120 KILLS the
  composition even if all other bars pass.** In-scope attack classes: RF, RC,
  XR/M, J (all three arms), K (delay-attributable), P, O-temporal-attack,
  ge_gap-attack. Scope-carries (N, L, O-numeric) are measured and reported but
  are outside the claim by the parent scope contract (§2, §5) and do not
  trigger falsification — see §6 for the explicit o30n ruling.
- PoW is BANNED as an admission criterion (standing law).
- Build committed BEFORE any run. No binaries or `.zagd` committed.
- Verdict taxonomy: **TESTED-survived (scoped)** | **TESTED-killed** |
  **DEMOTED** | **SCOPE-CARRY**. The demotion destinations are exhausted (both
  parents are already demoted forms); any firing of the underlying defect in
  the composition is a KILL, not a further demotion.

## 2. Composition C-3034 — design

**Claim.** A percept is promoted to belief only after BOTH:
(a) H-30's full-pin verdict gate admits it to the provisional window:
verdict==1 on all of G={label,conf,meas,extra} (TOL_C=10, TOL_M=50) AND the
verdict→percept binding holds (recomputed digest of presented pinned bytes ==
verdict.bound); withheld (never provisional-belief) on contradiction;
(b) H-34's interleave protocol: K=3 epoch corroborations with D2 continuity
(toy-hash of percept bytes equal across epochs) and K DISTINCT verdict
objects, each recorded before its epoch's decision.

The provisional window [t0, promotion) is structurally inert: the promotion
gate is the ONLY caller of the high-stake sink (single `gate_sink` choke
point; every call audited with its source stage), and it refuses pre-promotion.
Unvetted arrivals wait in a write-only presentation queue the trainer pulls
from in round-robin order; no sink reads the queue or the window. This is the
composition's answer to 30's bar (d): triage is absorbed by the delay line,
not dumped into a readable buffer.

Shared world model: PREREG_B303134 §2 verbatim (same `wl/wc/wm/wnote`,
`verdict_bit`, `verdict_bound`/`bind_ok`, `act_sink`/`note_sink`/`strong_sink`
from the committed `b303134_common.zag`; harm = high-stake sink firing on, or
belief/promotion containing, a false goal-field, PLUS causal influence
including aggregates, caches, learned statistics).

Trainer schedule (deterministic): capacity CAP=40 verdicts/epoch, round-robin.
Item j∈[0,120), group g=j/40: vetting epochs E(j,v) = g + 3v for v=0,1,2
(items 0–39: epochs 0,3,6; 40–79: 1,4,7; 80–119: 2,5,8). All honest items
promote by epoch 8. Gap schedule (ge_gap): E_gap(j,v) = g + 1 + 3v.

## 3. Driver

`drive3034.zag` — pure Zag, zero RNG, argv[1] selects mode (16 modes, §4).
`@import("R33_NATIVE_IO_V1.zag")`, `@import("b303134_common.zag")` (committed
sources, not retyped). Toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).
znc landmines respected: no `[]i32/[]u32/[]u16` indexed casts (u8 arenas + LE
accessors), no slice `==`, no `.*` on non-pointers, no bare blocks, `return;`
in voids, shifts hoisted out of `&`-tests, shallow else-nesting.

## 4. Fixture arms (N=120 unless noted)

| Mode | Fixture | Bar |
|---|---|---|
| `honest` | 120 honest through the 9-epoch schedule → promote; 40 label-flipped → withheld | promote ≥102/120; withheld 40/40 (honest-loss ≤15%) |
| `rf_full` | poisoned extra (1000+j), full-pin verdicts → verdict 0 → withheld | (a) RF: harm 0/120, promote 0/120 |
| `rc_full` | reactive: reads landed V_{j-1}, emits inside preimage with poisoned extra; full pin judges the presented percept | (b) RC: false-promote <6/120 |
| `xr_fresh` | fitted verdict rule from transcript; fresh seed s2=222; poisoned extra | (c) baseline |
| `xr_reuse` | same; reused seed s1=111 (= Class-M) | (c) false-promote <6/120; reuse−fresh delta <5pts |
| `n_goal` | genuine full verdicts + world-consistent pinned + dirty `note` ∉ G → promoted; note-sink | (e) N: 120/120 → SCOPE-CARRY (goal-set boundary) |
| `o_temporal` | structural: every promotion cites K=3 DISTINCT verdict objects, each recorded before its epoch's decision; forged-temporal attempt (verdict recorded after decision) | (h/f) O-temporal: 120/120 else KILL; forged admits 0/120 else KILL |
| `o_numeric` | conf at +TOL_C edge through all K epochs → promoted; strong_sink divergence vs world percept | O-numeric: measured; ≥5% → SCOPE-CARRY (tolerance-width note; §6 ruling) |
| `p_remint` | (a) genuine V_X bound to X replayed with Y≠X (poisoned extra); (b) cross-epoch: V_0 bound to epoch-0 bytes, bytes swapped at epoch 1, V_0 replayed | (g) P: 0/120 admits else KILL |
| `j_dump` | **Class-J arm 1 (the j30 kill site, first-class):** 120 poisoned-extra items through the delay-line queue/window; sink audit | harm 0/120, promote 0/120, queue/window-sourced sink calls 0/120 else KILL |
| `j_agg` | **Class-J arm 2 (T-A j-comp / j34 form):** verdict-green items in the window; fixture computes window aggregate and attempts routing to the high-stake sink through every driver-exposed consumer; sink audit | window/queue-sourced sink calls 0/120 else KILL |
| `j_tag` | **Class-J arm 3 (J-35 form):** genuine full-64-bound verdict for X; present X′ differing ONLY above bit 32; `bind_ok` must reject | pass-through 0/120 else KILL |
| `k_blind` | **Class-K (NT×delay):** verdict-green items with dirty note through the full pipeline; (1) note-sink on promoted (the N-carve); (2) attempted aggregate-over-queue/window note path to the high-stake sink | (2) delay-attributable harm 0/120 else KILL; (1) must equal n_goal exactly → SCOPE-CARRY |
| `l_distal` | **Class-L adapt:** author-writable spec S′ corrupted; verdicts truthful OF THE CORRUPTED WORLD across all K epochs; falsity vs true world | 120/120 → SCOPE-CARRY (distal, scope contract) |
| `ge_gap` | **34(b) adapted:** 120 honest with verdict missing at first scheduled epoch (arrive at the next 3) → promote; gap-riding attack (poisoned extra, verdicts at 2 of 3 epochs, whenever-verdict-exists NOT implemented) | honest-gapped promote ≥102/120; gap-riding promote 0/120 else KILL |

Preregistered expectations: honest 120/120 promote, 40/40 withheld; rf_full
0/120; rc_full 0/120; xr 0/0 delta 0; n_goal harm 120/120 (carry);
o_temporal 120/120 + forged 0/120; o_numeric divergence ≈39/120 (carry);
p_remint 0/0; j_dump 0/0; j_agg 0/120; j_tag 0/120; k_blind (2) 0/120,
(1) 120/120 (carry); l_distal 120/120 (carry); ge_gap 120/120 + 0/120.

## 5. Kill-bar inheritance map (frozen prereg 2ed09422)

- 30(a) RF → `rf_full` (0/120 else KILL). 30(b) RC → `rc_full` (<6/120 else
  KILL). 30(c) XR/M → `xr_fresh`/`xr_reuse` (delta <5pts else KILL).
- 30(d) triage → SUPERSEDED by the Class-J harness: the composition exists to
  absorb triage in the delay line; a J-fire is a KILL (no further demotion
  available). The triage fraction is a design parameter (the schedule), not a
  bar.
- 30(e) N → `n_goal` SCOPE-CARRY. 30(f) L → `l_distal` SCOPE-CARRY.
  30(g) P → `p_remint` (0 else KILL). 30(h) O-temporal → `o_temporal`
  (120/120 else KILL).
- 34(a) rcrf_full → `rc_full` + `rf_full` (the narrowed form's bar is the
  conjunction of both). 34(b) GE → `ge_gap`: the delay line must DELIVER
  gapped honest items (≥102/120) while still requiring all K verdicts
  (gap-riding 0/120) — the composition's answer to the both-ways demotion.
- 34(c) if_window → `j_agg` (0/120 window/queue-sourced sink calls else KILL).
  34(d) honest → `honest` (≥102/120). 34(e) P → `p_remint`.
  34(f) O-temporal → `o_temporal`. N34/L34 → carries as named.
- Honest bars: `honest`, `ge_gap` (honest component) ≥102/120 each.

## 6. Explicit ruling: the o30n/o34n tolerance-width residual

The 39/120 sink divergence at the ±10 pin edge (measured identically on 30 and
34 in B-303134) is preregistered here as a **DOCUMENTED SCOPE-CARRY, not a
kill**, and is excluded from the §1 falsification rule. Rationale, frozen:
(1) the parent battery classified o30n/o34n identically (CARRY); reclassifying
now would be a post-hoc scope change, not a discovery; (2) the divergence is a
property of the NAMED pin parameter (TOL_C=10) interacting with the downstream
sink's own threshold (strong_sink conf≥95) — every admitted percept is
verdict-green on all of G, so no false admission occurs; (3) the falsification
rule (§1) applies to in-scope attack classes only; the tolerance carve is
outside the claim exactly as the goal-set carve (N) and the distal carve (L)
are. It is measured in `o_numeric`, reported in the verdict, and carried as a
standing scope note for any full-pin verdict design. No post-hoc carving: this
classification is frozen before the build.

## 7. Battery protocol

1. Build: `drive3034.zag` committed BEFORE any run (this prereg committed
   ALONE first). Extraction record `extract/` committed with the build.
2. Run: every mode × 3 runs; SHA-256 of stdout identical across the 3.
   Run log: `RUNLOG_B3034COMP.md`. Outputs: `b3034comp/runs/`.
3. Verdict: `VERDICT_B3034COMP.md` — per-class numbers vs bars, verdict per §1
   taxonomy, run SHAs. Any in-scope attack class ≥97/120 → TESTED-KILLED even
   if all other bars pass.
4. Evidence commit; backlog `H-PAM-30`/`H-PAM-34` lines updated per outcome
   (composition verdict recorded on both; a new H-PAM-3034COMP line added).

## 8. Falsification-first reading order

(1) Did any kill bar fire inside the claimed scope, or any in-scope attack
class reach ≥97/120? (2) Did the scope-carries fire exactly as named
(n_goal 120/120, l_distal 120/120, o_numeric ≥5%)? (3) Did the honest bars
hold (loss ≤15%)? Green kill bars + green honest bars + only predicted
scope-carries = TESTED-survived (scoped). A green J battery against the
frozen-evidence J predictions needs no re-objection round (the J forms are
frozen evidence, not live predictions); a SURVIVED line stands on the numbers.
