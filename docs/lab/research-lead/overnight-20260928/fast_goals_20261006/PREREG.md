# Fast goals wave: preregistered three-question audit

Date 2026-10-06. Base ownership 91b2acc29. Branch fast/method-identifiability.
Science pure Zag; shell assembly/build/log/hash only. Original sources unchanged.
Historical reports are evidence leads, not automatically validated claims.
No new ledger claim ID. This tests small mechanisms, not canonical TNN or AGI.

## Q1 / T01: can contract growth admit a historical reject?
H-preserve: retained reject 6 stays rejected after a new success at 8.
H-hull: u_grow expands an interval through rejected intermediate values.
Minimum world: one field; accepts 2,4; rejects 6. Then observe success 8.
Reuse unmodified u_induct/u_check/u_grow. Independent predicate: even values
in 2..8 except 6. Test heldout x=1..10 before/after; frozen copy control.
Reinduct on accepts 2,4,8 and reject 6: oracle-supported representability control.
Expect initial identity interval [2,4] admits 2 and 4, rejects 6 and 8. Growth to
[2,8] admits 6 plus odd 3,5,7. Reinduction can use mod4 [0,0] OR alternative
training-consistent clause; do NOT require one specific clause. Require accepts
2,4,8 and reject 6, count its heldout errors separately.
Discriminator: old reject 6 flips to admitted only after growth; reinduction can
retain reject while including all successes. Kills reject-preserving semantics
for this growth operation; does not kill legitimate predictive widening or prove
these historical rejects are immutable authorized human rules.

## Q2 / T02: are revision histories per-contract or arena-global?
H-local: failures of A do not alter B's failure history/revision request.
H-global: u_invalidate uses shared cells 900/901, u_revise(B) consumes A's request.
Minimum world: arena S size 8192; contract A cbase=100, B cbase=200; one
active identity clause each. B [20,30], A [2,4]. Three A disagreements.
Check B clause and local counters unchanged, inspect shared request, call
u_revise on B with no B failures. Judgment table deliberately matches B's
existing [20,30] so any revision is not evidence it needed repair.
Control: fresh isolated B with same table, no A failures, u_revise call.
Expect shared req=1, A clause retired, B active unchanged before revision;
shared B revision count=1, isolated count=0. Instrument no concealed write path.
Kills per-contract failure isolation in a shared arena using this API, not proof
actual production core stores multiple contracts in one arena or has cross-talk.

## Q3 / T03: are learned singleton kinds necessary in the LCONT fixture?
H-kind: refined candidate/outer choice differs from a flat probe table rival.
H-flat: each kind is singleton so candidate admission is probe_has(s,target).
Reuse original LCONT prefix functions. Run original two worlds to acquire state.
Rival: among operations with probe_has(s,y)==1 pick maximal O_SUCCO, same ID tie
order. No access to hidden world law; facts retained, no kind state consulted.
Exhaust y=0..40 (41 goals), compare all 6 candidate flags and chosen outer ID
in each world, after refinement. Empty-candidate cases both select -1.
Coarse contract control should diverge because kind 0 admits every operation.
Expected refined vs flat zero mismatches, all six kinds unique each world;
coarse vs flat >0 mismatches. This is a selection-mechanism result only: not
end-to-end heldout task success, novel methods, or all possible kind learners.

## RUN / acceptance / artifacts
Prereg committed alone before driver source. Fresh compile gates execution;
portable output _zag_print, no Linux raw syscall output path executed.
Per probe assemble original prefix with driver into contract_probe.zag or
flat_probe.zag. Compare prefixes byte-for-byte. Three fresh builds each;
raw run outputs and binary hashes must agree. Each output contains measured
metrics, not a bare canned PASS. Nonzero instrumentation mismatch exits 1.
Predicting a defect is not passing the tested capability.
Artifacts in this directory: PREREG.md; contract_driver.zag; flat_driver.zag;
contract_probe.zag; flat_probe.zag; environment.txt; provenance.txt;
contract_compile{1,2,3}.txt; contract_run{1,2,3}.txt;
flat_compile{1,2,3}.txt; flat_run{1,2,3}.txt; REPORT.md; run.sh.
Generated extensionless executables ignored, not committed. End-to-end fresh
reproductions of original LCONT/contract-unification may be added as explicitly
post-prereg sanity checks with output-only host shim and separate filenames.

## Next questions
Q1: separately encode hard authority and learned applicability; regression-test
growth against stored counterexamples, then test noise and revoke/replay.
Q2: qualify multiple-contract ownership of episode/revision state before persistence.
Q3: need transfer across shared behavior classes/non-singleton kinds to justify the
extra representation; facts-only must remain a strong same-information baseline.
