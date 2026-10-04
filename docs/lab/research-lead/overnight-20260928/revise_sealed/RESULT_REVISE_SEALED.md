# RESULT: F3 REVISE Sealed Evaluation

Verdict: REVISE-SEALED-PASS.

Parent prereg: revise_sealed/PREREG_REVISE_SEALED.md (commit
8cdf0992a), frozen alone before any sealed world file, build
script, binary, or run existed. K1 holds by commit ancestry.
Parent chain: design ca157c743, builder prereg c197e7cd8,
builder result 7009d711c (REVISE-PASS, bounded L2).
Pipeline: this completes step 3 (sealed evaluation) only.

## 1. What was tested

The FROZEN, BYTE-IDENTICAL learner from the builder's commit
was tested on NEW sealed worlds designed by the independent
evaluator after the builder's commit, which the builder never
saw. The learner was not modified, tuned, or rebuilt for the
sealed worlds.

Frozen bytes verified by sha256 before any run (both match
commit 7009d711c exactly):
- f3_revise.zag:
  354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392
- f3_revise_abl.zag (condition-(b) ablation):
  4e3bdf0680f11778d9226ac127d20588b40a42295e85af2efaf3a1b77ea786b2

Sealed worlds (section 2 of the prereg, written after the
frozen prereg commit):
- S-CONJ2 (world_sconj2.zag, "SQ3-beta-combine"):
  Y(t) = X(t-3) AND Z(t-2). Passive: X at t=1,7; Z at t=2,8.
  Y=1 exactly at t=4,10. Goal: final-state Y=1 from all-zero.
- S-NEG2 (world_sneg2.zag, "SQ7-delta-causal"):
  Y(t) = X(t-2) AND NOT Z(t-2). Passive: X alone at t=3,9;
  Z never pulsed. Y=1 exactly at t=5,11. Goal setup: Z=1
  inhibitor present at t=0.
- Renamed variants world_sconj2r.zag / world_sneg2r.zag:
  verified by diff to differ ONLY in the w_worldname string.

Setup validation (prereg step 1, /tmp scratch, not sealed
evidence): the evaluator's build/run pipeline reproduces the
builder's committed outputs byte-for-byte on the original
worlds (md5 f37d0acfa02f4906e0885ddc0cac4c27 for T-CONJ,
a1ad9ac2b972e4c862c45238f38daa82 for T-NEG, all 3 runs each).
Pipeline validated before sealed runs.

## 2. Sealed runs (pure Zag: shell + znc only; zero Python)

Unmodified frozen learner, 3/3 byte-identical runs per
configuration, zero run-stderr bytes on all 18 runs:

- S-CONJ2: F3P3 RESULT REVISE-PASS. Discovery found [X@3]
  and [Z@2]; trial phase refuted each singleton and grew the
  conjunction via condition (b) (TRIALS 7 REFUTED 3 GREW 2);
  GOAL_REAL 1 on attempt 1; D1 trigger correctly did NOT
  fire (no GOAL_FAIL line). NEXPS 8, COST_OK 1.
  FINALRULE V=Y rule=0 [X@3 & Z@2].
  md5 84ab277e7535c740c5210c2065a8cef6 (3/3).
- S-NEG2: discovery found [X@2]; GOAL_REAL 0 (attempt 1);
  GOAL_FAIL_GROW_ATTEMPT fired; GROW_OK (goal-fail) V=Y
  rule=0 +lit=!Z@2; replanned around the inhibitor;
  GOAL_REAL 1 (attempt 2). NEXPS 3, COST_OK 1, GOAL_OK 1.
  FINALRULE V=Y rule=0 [X@2 & !Z@2].
  md5 85ebb436b4f7d6eac370466bc98a878c (3/3).
  The learner's self-reported line reads F3P3 RESULT
  REVISE-FAIL solely because DRILL_OK=0; see section 4.

## 3. Falsifier outcomes (all frozen in the prereg)

- F-RNAME: SILENT. All six renamed pairs byte-identical
  (cmp clean): sealed_c == sealed_cr (84ab277e...), sealed_n
  == sealed_nr (85ebb436...), 3/3 each. The H-NAME regression
  does not recur on unseen worlds.
- F-RABLN: SILENT. The ablated learner (condition (b)
  removed, frozen bytes) grows contradictory garbage on both
  sealed worlds: [X@3 & !X@3] and [Z@2 & X@1 & !X@1] on
  S-CONJ2; [X@2 & !X@2] on S-NEG2. REVISE-FAIL on both; it
  achieves neither GOAL_REAL 1 nor the answer key on either
  world. Condition (b) is causally necessary on unseen
  structure, not decorative.
- F-RNAMEAUDIT: SILENT. Token w_worldname occurs zero times
  in f3_revise.zag outside comments (one occurrence inside a
  header comment describing the ban itself; zero code
  occurrences verified by grep excluding comment lines).
- F-RCOST: SILENT. NEXPS 8 (S-CONJ2) and 3 (S-NEG2);
  bound nexps<=8 met; COST_OK 1 everywhere.
- F-RDET: HOLDS. 3/3 byte-identical stdout per configuration
  (md5s above), zero stderr bytes on all 18 runs. Build
  stderr contains only znc compiler warnings (zagd
  unavailable notice, A0102/A0101 lints), identical in kind
  to the builder's own build logs; no build errors.
- H-SCONJ2 (harness): PASS. FINALRULE contains (X,+,3) and
  (Z,+,2); GOAL_REAL 1 (attempt 1); no GOAL_FAIL line.
- H-SNEG2 (harness): PASS. FINALRULE contains (X,+,2) and
  (Z,-,2); GOAL_FAIL_GROW_ATTEMPT present; GROW_OK with
  +lit=!Z@2; GOAL_REAL 1 (attempt 2).

## 4. Central finding: the REFUTE-DRILL misfires on S-NEG2

The sealed evaluation exposed a world-calibrated assumption
in the frozen learner that the builder's tests could not
expose (both original worlds satisfy it).

The REFUTE-DRILL (f3_revise.zag lines ~1096-1138) is a
disclosed embedded mechanism self-test. It runs a hardcoded
poisoned rule set {(X,+,1),(Z,+,2),(X,+,2)} for Y through the
trial machinery on a scratch copy and expects (X,+,2) to be
refuted (obs=0). That expectation encodes the original
T-CONJ world's truth: on world_adv1, [X@2] alone is indeed
false for Y.

On S-NEG2, [X@2] is the TRUE 1-literal rule (it is exactly
what discovery found). The drill trial [SX,W,W,OY] observes
Y=1, the correctly functioning machinery refuses to refute
a true rule (DRILL_NOREFUTE obs=1), and the drill reports
DRILL-FAIL. The machinery behaved correctly; the self-test's
expectation was wrong for this world.

Scope of the blemish, verified in source:
- The drill runs on a scratch copy (lines ~1101-1110); it
  cannot alter the real rule set, the D1 trigger decision,
  the growth search, or any plan.
- Every mechanism-relevant output on S-NEG2 is correct:
  discovery [X@2], D1 fired exactly once on the real goal
  failure, grown literal !Z@2 via condition (b), successful
  replan, GOAL_OK 1, correct FINALRULE.
- The drill affects only the diagnostic verdict conjunction
  (goal_ok && drill_ok && split_ok && search_ok, frozen in
  the builder's prereg), which is why the learner's
  self-reported line reads REVISE-FAIL on S-NEG2 while every
  mechanism output is correct.

This is a blemish in the frozen artifact's self-test, not a
defect in the REVISE mechanism (D1-D6). It does not fire any
preregistered falsifier. Recommended: a future builder
revision should make the drill world-agnostic (derive the
poison from the discovered rule set) or remove it from the
verdict conjunction. The drill is disclosed infrastructure;
this evaluation reports the finding rather than hiding it.

## 5. Kill bars

- K1 (sealed prereg frozen first): PASS. Commit 8cdf0992a
  contains only PREREG_REVISE_SEALED.md and strictly precedes
  every sealed world file, build script, binary, and run.
- K2 (all falsifiers run): PASS. F-RNAME, F-RABLN,
  F-RNAMEAUDIT, F-RCOST, F-RDET, H-SCONJ2, H-SNEG2 all
  executed with byte-identical raw evidence committed.
- K3 (pure Zag, 3/3 identical): PASS. Shell, znc, grep, cmp,
  diff, md5sum, sha256sum, wc only; zero Python invocations
  at every stage. All 18 runs 3/3 byte-identical per
  configuration with zero run-stderr bytes. No em/en dash
  bytes in any new file (shell byte check before commit).

## 6. Verdict rule application (frozen)

Per PREREG_REVISE_SEALED.md section 7: REVISE-SEALED-PASS
iff F-RNAME silent, F-RABLN silent, F-RNAMEAUDIT silent,
F-RCOST silent, F-RDET holds, H-SCONJ2 passes, H-SNEG2
passes. All seven conditions hold. The drill finding of
section 4 is reported as a diagnosed blemish; it fires no
falsifier and the verdict rule is applied exactly as frozen.

Verdict: REVISE-SEALED-PASS.

## 7. Honest scope

REVISE-SEALED-PASS is a bounded L2 infrastructure verdict:
goal-failure revision is a generic mechanism (no world-name
gating) that operates correctly on world structure the
builder never saw, with the ablation-backed growth condition
still doing the work. It claims no L3, no T-NEG-class
generality, and does not revive the F3 Phase 3 BUILD-PASS
(that verdict stays retracted). The frozen learner's
self-test carries a world-calibrated expectation (section 4);
the mechanism does not. Pipeline steps 4-11 (independent
reproduction, baseline, alternative-explanation attack, OOD,
ablation, transfer/reuse, independent red team, governance
audit) remain.

## 8. Evidence index (all under revise_sealed/)

- PREREG_REVISE_SEALED.md (commit 8cdf0992a, frozen first)
- world_sconj2.zag, world_sneg2.zag (sealed worlds)
- world_sconj2r.zag, world_sneg2r.zag (renames; diff shows
  name-string-only change)
- SEALED_BUILD.sh (build script with frozen-sha256 gate)
- run_sealed_{c,cr,n,nr,abl_c,abl_n}.zag (concatenations)
- bin_sealed_{c,cr,n,nr,abl_c,abl_n} (binaries)
- raw_sealed_{c,cr,n,nr,abl_c,abl_n}_r{1,2,3}.txt/.err
  (byte-identical raw evidence; all .err zero bytes)
- build_sealed_*.err (znc warnings only; no errors)
- RESULT_REVISE_SEALED.md (this file)
