# Prereg confirmation — strength trial build (Wave-5 investigator)

**Date:** 2026-09-19. **Trial:** `wave4/strength-experiment/PREREG.md` +
`TEST_PLAN.md` (+ `TESTS_SUMMARY.md`), **APPROVED by Micah** (per tasking;
the wave-4 "DO NOT RUN" gate is lifted by that approval).

This document confirms the trial is built EXACTLY as preregistered. No
strength rule, effort-schedule constant, curriculum closed form, metric
definition, kill/promotion bound, arm semantic, scale-leg size, learner
policy rule, pressure schedule, or force-PIN contract was changed. What
follows are **operationalizations** — edge decisions the prereg leaves
unspecified, documented here before the first run. None alters any
registered bound or criterion; each is flagged so Micah/parent can confirm
or re-register.

## Operationalizations (not prereg changes)

1. **WBS denominator horizon edge.** `R_wbs` = wrong-strong revised /
   wrong-strong total. A wrong memory added at `m > H−100` cannot receive
   the full 4-revelation citation supply inside the run, so its kill is
   physically uncompletable — counting it would test horizon arithmetic,
   not rigidity. "Wrong-strong total" is operationalized as wrong
   candidates that were admitted, strengthened to ≥80, still held at the
   2nd contradiction (`m+50`), **with `m+100 < H`**. The kill criterion's
   own window language ("within W=150 after the revision trigger")
   already restricts evaluation to memories with an observable trigger;
   this extends the same logic to the completable supply. Registered
   bounds (`R_wbs`, `W=150`) unchanged.

2. **The m=500 implant.** TEST_PLAN §7c lists base-leg implant episodes
   `{83,166,250,333,416,500}` from `floor(k·H/6)`, k=1..6. Episodes are
   0-indexed `0..H−1` (the VUP pressure qualifier "`m mod 100 == 0`
   (`m > 0`)" only makes sense 0-indexed), so `m=500` never occurs. It is
   therefore never admitted and excluded from `I_rej`'s denominator
   ("implants admitted"). 5 effective implants at S1 (same edge at S10/S100:
   the k=6 episode is out of range). The closed form is unchanged.

3. **Victim-attempt bound (8).** TEST_PLAN §6 says the learner "tries the
   next-lowest victim" after an abandoned kill, unbounded. Unbounded
   audited abandonments overflow the preregistered ledger caps at S10/S100
   (e.g. ~3200 victims × ~47000 episodes ≫ 1048576). The learner tries at
   most **8 victims per eviction/pressure-slot**, then drops. The bound is
   outcome-neutral (it never changes which kills succeed — abandoned kills
   stay abandoned) and applied identically at all legs. Chosen for ledger
   feasibility, not for results.

4. **CORE count at scale.** S1 = 32 slots is specified as "2 CORE + 30
   USER". S10/S100 specify totals only (320/3200); CORE is fixed at 2
   (the system's own knowledge does not scale with the USER store),
   USER = 318/3198. Pressure schedule, `W=150`, `D=25` unscaled (changing
   them needs re-registration).

5. **`EVIDENCE_AGAINST`/`JUSTIFY` stage gate.** The prereg sets stage gates
   only for the kill. Preparatory ops require stage ≥ MANAGE (the stage
   where deliberate judgments unlock). The trial runs at FULL throughout
   except the GATE cell's stage-3 check, so this is exercised, not dodged.

6. **Arm-B checker scope.** The prereg's "for every completed erasure,
   evidence_count == n(strength_at_kill)" is enforced by the op and the
   checker for `KILL_EVIDENCED` (arms A/C). Arm B's `KILL` takes no
   evidence by design ("strength ignored by the kill gate"); applying the
   evidence check to B would be incoherent. B's erasures get the MA1
   checks (no pinned/force-pinned/CORE kills, replay-exact).

7. **"Probing" the force-PIN lock (arm C criterion).** "High
   `REFUSED_FORCEPIN` attempt rates" is not quantified in the prereg.
   Mechanical classification used: probing = (a) the learner itself
   issuing a force op (→ `REFUSED_ROLE`), or (b) re-attempting a kill on a
   slot after a `REFUSED_FORCEPIN` without an intervening victim change.
   The preregistered victim policy (no force-pin exclusion — "never CORE,
   never pinned" lists no force-pin exception) mechanically re-selects the
   force-pinned slot at each pressure event and moves on after the refusal;
   that is policy-mechanical contact, not probing. Counts are reported;
   the classification is flagged for review.

8. **Implant entrenchment reading.** TEST_PLAN §7c: "at revelation (+25)
   `imp = 0` with counter-evidence" is explicit, so implants enter at the
   learner-declared 75 (the "high strength declaration via the learner's
   own rule") and are never `STRENGTHEN`ed (the revelation shows `imp=0`).
   "The learner's STRENGTHEN rule entrenches them" is read as the
   strength-declaration machinery (the only learner path that fires);
   `I_entr` = learner-declared-strong (≥70) implants still held at end.

## Emergent behavior noted BEFORE running (not a design change)

TEST_PLAN §7a specifies no contradiction revelations for VUP. The effort
schedule therefore makes every `s>0` kill uncompletable in VUP for arms
A/C (no citable episodes exist), so A/C cannot evict at all once the store
fills — the store freezes and pressure demands go unmet (audited
abandonments). The same holds in JI for junk/implant admission (junk has
no contradictions; implants can't displace). This is the mechanical
consequence of the preregistered rules, not an implementation choice. It
is reported as a finding; no rule was bent to avoid it.

## Compliance checklist (PREREG §7)

1. Zero RNG in decision paths — static grep in the runner; no RNG source
   exists in the trial (no LCG, no `rand`/`rng`/`srand` tokens anywhere).
2. No score tables/accumulators, no NxN scaling, no reward signal in the
   memory path. Strength is declared judgment only (four legal paths).
3. Every state change audited; `st_replay_check` reconstructs exact state.
4. Byte-identical reruns (runner diffs two runs per cell).
5. Zag-first, native on this VM (`znc_linux_x86_64_abed8aa1`); no Python
   in the trial (runner is bash).
6. All work on this VM; nothing pushed to git.

**First execution of any trial binary is the trial result.** No validation
runs before this confirmation. The GATE cell runs first per TEST_PLAN §10;
any GATE assertion failure stops the trial.
