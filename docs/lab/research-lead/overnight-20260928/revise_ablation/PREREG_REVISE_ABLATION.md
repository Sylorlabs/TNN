# PREREG: F3 REVISE Ablation (Pipeline Step 8)

Status: FROZEN. This document was committed alone before any
ablation learner file, build script, binary, or run existed.
No ablation artifact existed at freeze time.

Parent chain: design ca157c743; builder prereg c197e7cd8;
builder result 7009d711c (REVISE-PASS); sealed prereg 8cdf0992a;
sealed result 1df8addec (REVISE-SEALED-PASS); repro 7407dd4a7
(REVISE-REPRO-PASS); baseline prereg 4786633c5 plus amendment
db585360a; baseline result c810d5f55 (REVISE-BASELINE-PASS);
attack prereg 12da75511; attack result bbdb65c99
(REVISE-ATTACK-SURVIVES); OOD prereg 7bf467d35; OOD result
1125be9bb (REVISE-OOD-PASS). This prereg covers pipeline step 8
(ablation) only.

## 1. Purpose

Confirm the causal role of the two distinct rule-growth call
sites in the frozen learner, by independent excision. The sealed
evaluation already ablated the shared growth gate (condition (b),
falsifier F-RABLN, SILENT): removing it made the learner grow
contradictory garbage on both sealed worlds. That result does not
separate the two call sites. This step tests each call site alone.

Call site 1 (D1): goal-fail growth in the goal phase. On sealed
S-NEG2 it grew +lit=!Z@2 after attempt 1 failed, enabling attempt
2 to succeed. On sealed S-CONJ2 it never fired.

Call site 2 (OP-GROW): refutation-triggered growth in the Phase 3
trial loop. On sealed S-CONJ2 it grew the conjunction
[X@3 & Z@2] after the singletons were refuted. On sealed S-NEG2
no refutation occurred, so it never ran.

## 2. Frozen materials (hashes verified before any build)

- Frozen learner: docs/lab/research-lead/overnight-20260928/
  revise_attack/f3_revise_frozen.zag, sha256
  354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392.
- Sealed world S-CONJ2: revise_attack/w_sconj2_ref.zag
  (pristine, via git show from 1df8addec).
- Sealed world S-NEG2: revise_attack/w_sneg2_ref.zag
  (pristine, via git show from 1df8addec).
- Reference md5s (frozen learner + sealed worlds, from the
  sealed and attack steps): S-CONJ2 stdout
  84ab277e7535c740c5210c2065a8cef6; S-NEG2 stdout
  85ebb436b4f7d6eac370466bc98a878c. Each 3/3 byte-identical.

## 3. Ablation construction (frozen)

Ablated learners are built by copying f3_revise_frozen.zag into
revise_ablation/ and changing exactly one condition line each.
The excised code stays syntactically valid inside the false
branch. diff against the frozen learner must show exactly one
changed line per ablated learner, otherwise the construction is
rejected and the step is VOID pending a transparent amendment.

- A1 (no D1): file f3_revise_noD1.zag. Line 1231 of the frozen
  learner reads `      if(attempt<ATTEMPT_MAX){`. Replace with
  `      if(0==1){`. Effect: after a failed goal attempt the
  else branch runs (honest stop), the D1 growth block never
  executes, and the GOAL_FAIL_GROW_ATTEMPT line never prints.
- A2 (no OP-GROW): file f3_revise_noGROW.zag. Line 994 of the
  frozen learner reads `        if((rs[grb] as i32)<3){`.
  Replace with `        if(0==1){`. Effect: on rule refutation
  the GROW_FAIL path runs (rule dropped, Phase 2 behavior);
  F3_grow_search is never called from the trial loop.

If the Zag compiler rejects `if(0==1){`, the construction fails
and this prereg is amended transparently before any run; no
silent substitution is allowed.

## 4. Configurations (frozen)

Four configurations, each run 3x, all raw stdout/stderr
committed:

- a1n: f3_revise_noD1.zag + w_sneg2_ref.zag
- a1c: f3_revise_noD1.zag + w_sconj2_ref.zag (control)
- a2c: f3_revise_noGROW.zag + w_sconj2_ref.zag
- a2n: f3_revise_noGROW.zag + w_sneg2_ref.zag (control)

Build: concatenate learner + world, compile with the repo znc
only (/home/hatch/workspace/tnn-forkbattery-1121pdt/
local-tnn-native-lab/znc), run the binary 3x. The build script
verifies the frozen learner sha256 before deriving the ablated
copies.

## 5. Frozen harnesses

### H-A1N (A1 on S-NEG2; D1 is causally necessary for S-NEG2)

All must hold on all 3 runs:

- (a) exactly one line matching "F3P3 GOAL_REAL", and it reads
  "F3P3 GOAL_REAL 0 (attempt 1)".
- (b) zero lines matching "GOAL_FAIL_GROW_ATTEMPT".
- (c) zero lines matching "GROW_OK (goal-fail)".
- (d) one line "F3P3 FINALRULE V=Y rule=0 [X@2]" (single
  literal; no "&", no "!Z@2").
- (e) "F3P3 GOAL_OK 0" present.
- (f) "F3P3 RESULT REVISE-FAIL" present.
- (g) 3/3 byte-identical stdout, exit 0, zero stderr bytes.

### H-A1C (A1 on S-CONJ2; control, D1 never fired there)

- stdout md5 equals 84ab277e7535c740c5210c2065a8cef6 on all
  3 runs (byte-identical to the frozen sealed S-CONJ2 output),
  zero stderr bytes. If not identical, the A1 excision was not
  inert and the A1 pair is a construction failure.

### H-A2C (A2 on S-CONJ2; OP-GROW is causally necessary for S-CONJ2)

All must hold on all 3 runs:

- (a) zero lines matching "F3P3 GOAL_REAL 1".
- (b) no "F3P3 FINALRULE" line contains both "X@3" and "Z@2".
- (c) "F3P3 RESULT REVISE-FAIL" present.
- (d) 3/3 byte-identical stdout, exit 0, zero stderr bytes.

Note: the exact internal path (singleton drops, possible
PHASE3-FAIL no-effect-vars, or goal-phase failure) is not
verdict-bearing; only (a) through (d) are. The observed path
will be documented in the result.

### H-A2N (A2 on S-NEG2; control, no Phase 3 growth happened there)

- stdout md5 equals 85ebb436b4f7d6eac370466bc98a878c on all
  3 runs (byte-identical to the frozen sealed S-NEG2 output),
  zero stderr bytes. If not identical, the A2 excision was not
  inert and the A2 pair is a construction failure.

## 6. Verdict rule (frozen)

REVISE-ABLATION-PASS iff H-A1N and H-A1C and H-A2C and H-A2N
all hold, and K1, K2, K3 all pass.

REVISE-ABLATION-FAIL iff any harness fails (documented with the
observed lines), or either control world is not byte-identical
to its frozen reference (construction failure), or any kill bar
fails.

A control-world mismatch does not make the step VOID: it is
recorded as FAIL with the cause (the excision was not inert).

## 7. Kill bars (frozen)

- K1 (prereg frozen before ablation): PASS iff this document's
  commit strictly precedes every ablation learner file, build
  script, binary, and run (verified by commit ancestry).
- K2 (ablations run): PASS iff all four configurations ran 3x
  each with all raw logs committed.
- K3 (pure Zag, 3/3 identical): PASS iff only shell, znc, git,
  grep, diff, cmp, md5sum, sha256sum, wc, sed are used at every
  stage (authoring, derivation, build, run, analysis, byte
  checks); zero Python invocations; every reported
  configuration is 3/3 byte-identical with zero stderr bytes;
  no em/en dash bytes in any new file (checked with the
  shell-only worker_snippets/check_no_dash.sh).

## 8. Honest scope (frozen)

This step tests the causal necessity of the two growth call
sites on the two sealed worlds. It does not test other
mechanisms (discovery, trial search, planning), other worlds,
or transfer. A PASS keeps REVISE at bounded L2 and advances the
pipeline past step 8 only. Steps 9-11 remain open. The
contaminated research paper will not be touched.
