# H2 Masked-Probe Readiness Checklist

Date: 2026-09-30 (PDT). Verdict: **H2-READINESS-COMPLETE**.

This document records what is ready for the H2 masked verification probes
(roadmap Step 1, `67a420cca`) and what still blocks execution. It is a
readiness audit only. No probe was run.

---

## 1. Ready: probe design

- **Document:** `docs/lab/research-lead/overnight-20260928/tnn2_h2probes/H2_PROBE_DESIGN.md`
- **Commit:** `4631c5918` (H2-PROBE-DESIGN-COMPLETE)
- **Contents confirmed present:**
  - Masked-probe definition (4 conditions: key absent from trial loop, learner
    commits before reveal, offline scoring, paired unmasked control).
  - Three masking modes: withhold (masked flag, `t2_try_verify` masked branch),
    lie (corrupted `expected`), withhold plus held-back facts.
  - Three probes: A (withhold the key), B1 (confirmable lie), B2
    (unconfirmable lie), C (own-criterion).
  - Search-order traps: worlds must make the first executable candidate in the
    frozen search order (chains k=2..4, then sums, then counts, then single
    hops) WRONG. Source-grounded in `t2_try_verify` (lines 497-510), `t2_trial`
    (lines 586-666), `mp_run` (lines 668-671).
  - Prediction for frozen TNN-2: FAIL all probes (withhold promotes first
    executable; lie unmasked branch matches `v == expected`; no refusal path;
    DOF map records 0 pure-learner decisions, `d2af26581`).
  - 7-condition PASS definition (masked accuracy above baseline, refusal
    competence, lie resistance, causal learner-state involvement with
    ablation, criterion revisability, domain neutrality, reuse coupling).
  - Draft K-H2-1..K-H2-4 kill-bar language, guard clauses, executor notes,
    lineage.
- **Status:** Design only. No probe code written, no binary built, no probe
  executed. Confirmed: `tnn2_h2probes/` contains only `H2_PROBE_DESIGN.md` and
  `NAMECHECK.md`.
- **Toolchain provenance of design work:** safebin PASS at design time
  (recorded in `tnn2_h2probes/NAMECHECK.md` Step 0).

## 2. Ready: sealed trap worlds

- **Directory:** `docs/lab/research-lead/overnight-20260928/h2_trapworlds/`
- **Commit:** `86389b108` (H2-TRAPWORLDS-COMPLETE)
- **Worlds:** H2A (withhold trap), H2B (lie trap), H2C (own-criterion trap).
- **Seal integrity (re-verified 2026-09-30 by this checker):**
  - `h2a_world.txt`: `be358e7ae423d55d99018288f9a6e14c72b2e86d649637652e1eb22a0ddf7499` MATCH
  - `h2b_world.txt`: `6cac9f6b22c8e303e75bfadac0cd13459ce1e0c64a999c25c8a0b0e2ca31ca6c` MATCH
  - `h2c_world.txt`: `2b721d49e0f04e9aef915eaec69fa9d5ec3db71c5c8d0293eafa75418eb846ba` MATCH
  - All three match `SEAL_H2.md` byte-for-byte. Contents were NOT opened (hash
    check only).
- **Permissions:** `-rw-------` (root only), confirmed on disk.
- **ID ranges:** H2 uses [50000, 59999], disjoint from FW [30000,39999] and GW
  [40000,49999]; H2A [50000,50099], H2B [50100,50199], H2C [50200,50299].
  Zero collisions per `SEAL_H2.md`.
- **Not run:** seal statement confirmed; no evaluator output exists in
  `h2_trapworlds/` (only NAMECHECK.md, SEAL_H2.md, TRAPWORLD_DESIGN.md,
  gen_h2.zag, substrate/, worlds/); no other file under
  `docs/lab/research-lead/overnight-20260928/` references H2A/H2B/H2C.
  The only history on the world files is the builder commit `86389b108`.
- **Generator provenance:** `gen_h2.zag` (pure Zag, pinned znc) implements
  `TRAPWORLD_DESIGN.md` sections 1-3; substrate copied from
  `../postfreeze_adversary/seal_src/substrate/`.
- **Toolchain provenance of build work:** safebin PASS at build time
  (recorded in `h2_trapworlds/NAMECHECK.md` Step 0).

## 3. Ready: frozen target and kill-bar drafts

- **Frozen target:** TNN-2 build `f4de7ff46` (TNN2-BUILD-PASS; 46/46 assertions;
  3/3 byte-identical). Binary present at
  `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2_bin`
  (presence confirmed; not executed by this checker).
- **Kill-bar text:** K-H2-1 (masked accuracy), K-H2-2 (lie resistance),
  K-H2-3 (criterion causality and revisability), K-H2-4 (domain neutrality
  and reuse), with guard clauses. Source drafts: `H2_PROBE_DESIGN.md`
  section 7 (`4631c5918`) and gap-bars synthesis (`36e5a70e1`).

---

## 4. Blocked: what Micah must do

The following items are NOT complete. Each requires Micah's explicit action.

### B1. Freeze K-H2-1..K-H2-4

- Current status: **DRAFT-NOT-FROZEN.** No freeze prereg commit exists. This
  checker searched git history (`git log --all --grep` for K-H2 variants);
  the only K-H2 commits are the design draft (`4631c5918`), the gap-bars
  draft (`36e5a70e1`), and the bar inventory (`1722884ad`).
- Open parameters in the draft that must be fixed at freeze: N (sealed trap
  world count), M (accuracy margin above the first-executable baseline), F
  (lie-resistance fraction), and the definition of the world families for
  K-H2-1. The draft text names these explicitly.
- Freeze requirement: a prereg commit whose FIRST commit strictly precedes
  any implementation (per the loop governance ruling), so the bar governs
  rather than follows results.
- Related pending input: the six kill-bar open questions from the review
  (`eb354e3a2`) are banked with Micah; several (world counts, signature
  functions, bar vs falsifier framing) apply directly to K-H2-1..K-H2-4.

### B2. Authorize the evaluator

- The H2 trap-world seal (`SEAL_H2.md`) names the authorized reader: the H2
  probe evaluator, AFTER Micah freezes K-H2-1..K-H2-4.
- Until then, no builder, analyst, or other worker may open the world files.
  This seal is intact and has been honored (this check recomputed hashes
  only, without opening contents).
- The evaluator will need: the frozen bar text (B1), an independent
  adversary for post-freeze world design if the bar requires additional
  worlds beyond the three sealed here (K-H2-1 names "at least two
  independently designed world families"), and the paired unmasked-control
  protocol from the design (section 8).

### B3. Sequencing note

- H2 probes are roadmap Step 1 and must precede Step 4 (H1 widening) per the
  treadmill warning (`67a420cca`, Risk 3). This check does not evaluate H1
  readiness; it records the ordering constraint.
- Bundle v16 is separately blocked on freeze reconciliation (`dcf8ae371`);
  that is not an H2 probe blocker, but its outcome may touch shared
  evaluator infrastructure.

---

## 5. Open questions from the checklist author

1. Should K-H2-4 (reuse coupling) be measured against the reuse path once
   it exists, or deferred until the reuse-path design (`5f15b9309`) is
   implemented? The design assumes the current query path reads only tag-1
   facts, so K-H2-4 is predicted FAIL on frozen TNN-2 regardless; freezing
   the bar now does not presuppose the reuse fix.
2. K-H2-3 requires an experience log showing the criterion changing after a
   prediction error; the design does not yet specify the log format. Suggest
   resolving at freeze time alongside the N/M/F parameters.

---

## Verdict

**H2-READINESS-COMPLETE.** Design ready (`4631c5918`). Worlds sealed and
verified (`86389b108`; hashes match; permissions and ID ranges correct; not
run). Kill bars draft but NOT frozen. Execution is gated on Micah freezing
K-H2-1..K-H2-4 and authorizing the evaluator. Check only; no probe run.
