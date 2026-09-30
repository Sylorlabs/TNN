# H-NEW-3 Pilot Implementation Plan

Date: 2026-09-30.
Design: `d83d53075` (HNEWP3_PILOT_DESIGN.md, DESIGN-COMPLETE).
Status: PLANNED. Plan only; no implementation; no empirical claims.

## K1: OP-RECRUIT v2 status checked

Checked 2026-09-30 06:20 UTC against committed ancestry on `tnn-native-lab`.

- Design: `c6ef7ffcf` (committed).
- Prereg: `1df644256` (committed, strictly precedes implementation).
- C0 integration design (depends on v2): `9aa1fb0b5` (committed, DESIGN-COMPLETE).
- Implementation: **NOT landed.** The implementer has finished the work in the
  worktree: `oprecruit2.zag`, `OPRECRUIT2_RESULT.md`, and run1/2/3 logs are
  staged in the git index (`git status` shows `A` entries) but are not yet
  committed. The staged result doc claims BUILD-PASS on the non-adversarial
  battery with T-ADV (independent post-freeze adversary) still PENDING.
- H-NEW-1 (C0INTEG Phase A): design committed (`9aa1fb0b5`); implementation
  has not started.

Conclusion: OP-RECRUIT v2 has NOT landed in ancestry. The pilot implementer
must treat it as unavailable at prereg-freeze time unless the implementation
commit lands first. K1 PASS.

## K2: E3 mechanism specified

The design (lines 144-149, 330-332) specifies: the pilot is specified now
against the form-inventor baseline; the prereg names which E3 mechanism is
frozen (baseline inventor now, recruited-operator variant as a named upgrade
once H-NEW-1 lands).

Decision rule, frozen in this plan:

1. **Default: baseline form-inventor.** E3 uses the L3 bridge
   (`ebdc4fd3e`, BRIDGE-TESTED) generic construction mechanism. This is the
   only E3 mechanism available at prereg-freeze time.
2. **Upgrade condition (strict):** the recruited-operator variant may be named
   in the prereg ONLY IF, before the pilot prereg commits, both (a) the
   OP-RECRUIT v2 implementation commit lands in ancestry, and (b) H-NEW-1
   Phase A (C0INTEG) is implemented and passes its gates. Partial satisfaction
   keeps the baseline.
3. **Freeze:** whichever variant the pilot prereg names is frozen and
   unalterable after results. The other variant is recorded as a named
   follow-up wave, not a mid-wave substitution.
4. Rationale for not waiting: the pilot measures non-interference and
   retention across five experiences, not the E3 mechanism itself. Running the
   pilot on the baseline now banks the Arm A vs Arm B comparison structure;
   the E3-mechanism comparison is a clean second wave.

K2 PASS.

## K3: Prereg structure defined

The pilot prereg (to be committed by the implementer before any pilot
implementation) must contain these sections, in order:

1. **Frozen workloads:** the exact E1-E5 workloads from the design, with seeds
   frozen. Includes E3's frozen experience and the E5 reuse probe derived
   from the E3 form.
2. **E3 mechanism freeze:** which variant is used (baseline vs
   recruited-operator), with the decision rule from K2 cited and the landed
   commits named.
3. **Retention floors:** F-E1..F-E4x immediate, F-D1/F-D2/F-D4/F-D5 delayed,
   F-REL relative (Arm A delayed vs Arm B immediate minus frozen margin),
   F-CAP capacity bound. Values frozen here; unalterable after results.
4. **Arm B control:** five separate fresh processes, one experience each, same
   frozen workloads and probes, same frozen binary. Reference-score protocol.
5. **Falsifiers:** F-INTERFERE, F-CORRUPT (white-box canary audit),
   F-REUSE-FAIL, F-FLOOR, F-LABEL (D1 channel-tag audit), F-NONDET, F-PYTHON.
6. **D1 disclosure:** channel tags name the sense (CH_VOCAB etc.), never the
   task; disclosed as weaker than undifferentiated input. Audit criteria.
7. **Partitioned-regions disclosure:** the pilot tests non-interference and
   retention, explicitly not shared representation (central limitation,
   design section 9).
8. **Upgrade path:** the named follow-up wave (recruited-operator E3, second
   order E4-before-E2, scale-up battery on PILOT-PASS) with its own prereg
   requirement.

Kill bars for the pilot implementation wave (proposed, to be frozen by the
implementer): K1 prereg-before-implementation; K2 all five experiences run in
one process (Arm A) with no resets and no recompilation; K3 all floors met;
K4 pure Zag, deterministic, no em dashes; K5 Arm B control run and compared.

K3 PASS.

## Sequencing

Per the frontier: pilot after C0INTEG Phase A (H-NEW-1). The design allows the
pilot to be specified now against the baseline. This plan recommends:
implement the pilot prereg against the baseline E3 now, so the pilot does not
block on the OP-RECRUIT v2 commit landing and H-NEW-1 Phase A completing.
The recruited-operator E3 variant becomes a named, separately preregistered
second wave. If the parent prefers strict sequencing (pilot only after Phase
A), that is a parent-level sequencing decision, not a plan defect.

## Verdict

**PLANNED.** All three kill bars pass. Zero Python used in this plan.
Zero em dashes (byte-verified below). Committed local-only with pathspec
restricted to the owned path.
