# REPORT: Verification Machinery at Delay N=1 (VERIFY-N1)

Worker: Verify N1 Worker (subagent, 2026-10-02).
Prereg: `PREREG.md` (frozen, committed alone as eb2c03f8c before any
implementation existed; zero amendments).
Verdict: **VERIFY-N1-COMPLETE.** All seven kill bars PASS, no
falsifier fired, 3/3 runs byte-identical.

## Question answered

Does N=1 work? Yes. Is the transfer envelope N<=3 inclusive of N=1?
Yes. The unmodified learner (byte-identical to the frozen
verify_transfer copy, sha256
45ad35d892d629971a4679ffd2085b8bd54bf9c328d1e8eb1cededcc3ef3ae65)
attributes every one of 110,337 delayed noisy arrivals by schedule
step under N=1 timing (arr - sched == 1 on every ATTR line),
averages the same noise to the same intermediate form
M1 = [SUB R0,R2, ADD R0,R1] (bytes 2,0,2,1,0,1), and retains it on
held-out episodes. N=1 is the minimal positive delay and exercises
the least in-flight overlap of the tested envelope (exactly one
deployment in flight at each poll during continuous deployment);
passing here, with N=2 and N=3 already passing, bounds the envelope
1<=N<=3 for the frozen poll/drain schedule.

## Build record

- `learner_ds.zag`: BYTE-IDENTICAL COPY of the frozen
  `verify_transfer/learner_ds.zag` (sha256 above; `cmp` clean). NOT
  modified, NOT rewritten, NOT adapted. Calls exactly two
  world-side symbols: w_sched_ds, w_arrive_ds (section K-N1-1).
  Its frozen 3-step drain covers the N=1 delay with two spare polls.
- `world_dn1.zag`: new SETTLE-DN1 environment (experiment side only).
  Same frozen episode tables and hidden margin rule
  margin = e0+e1-e2 as the sibling family; delay N=1 (the only
  behavioral change from SETTLE-DN2: `w_arrive_ds` returns the
  deployment scheduled at step-1); SAME noise (seed 109, draws
  (h mod 5)-2 in {-2,-1,0,1,2}). `w_sched_ds` returns nothing;
  `w_conseq_det` is experiment-side only (uniqueness sweep).
- `driver_dn1.zag`: new experiment-side driver (mirrors driver_vt:
  teaches X train+test, seeds M0, runs l_experiment, NOM/MENU arms,
  K=1 control arm, uniqueness sweep, kill-bar summary with N1
  markers). Frozen number checks unchanged.
- `audit_attr_n1.awk`: frozen attribution audit (every ATTR line:
  arr - sched == 1, DEPLOY at sched with same tag and same k, no
  ATTR-BAD / ATTR-COUNT-BAD).
- `n1_full.zag`: concatenation learner_ds + world_dn1 + driver_dn1.
- `n1_bin`: compiled with pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 (one pre-existing
  analyzer warning A0102 in the frozen learner's p_outs_train, also
  present in the verify_transfer build; build succeeds).
- Runs: `n1_run1.txt`, `n1_run2.txt`, `n1_run3.txt` (3/3
  byte-identical, sha256
  2aa06398cc3b0a25f4b8727ab1cb5c059843396d7b325bc6b88c8bdcb64b20fc;
  11,453,048 bytes each).

## Kill bar results

- K-N1-1 (consequence-only verification): PASS. Shell grep audit on
  the committed learner_ds.zag: zero case-insensitive hits for all
  12 patterns (label, expected, w_tab, margin, correct, _mode,
  bridge, handler, w_conseq, w_val, menu_, nz_). Positive symbol
  check lists exactly `w_arrive_ds` and `w_sched_ds`.
- K-N1-2 (attribution under N=1 timing): PASS. The frozen awk audit
  over each of the 3 run logs: 110,337 ATTR lines per log, every one
  with arr - sched == 1 and a DEPLOY line at step sched with the same
  tag AND the same k; zero ATTR-BAD and zero ATTR-COUNT-BAD lines.
  Every threshold score is therefore a sum of exactly 64 properly
  attributed noisy arrivals under delay N=1.
- K-N1-3 (averaging load-bearing at N=1): PASS. Log shows K1-BUILT
  n=1 prog=2,0,2 with K1-SELECT-M1 0 (single-sample delayed learner
  stalls, does not select M1) while the K=64 arm selects M1.
- K-N1-4 (M constructed via the N=1 channel): PASS. Log shows
  M0-FIT t=4 C=509; DS-ROUND 1 base=512 eval=80 win=2,0,2 gain=573
  score=1085 t=-2 mgn=189; DS-ROUND 2 base=1085 eval=80 win=1,0,1
  gain=66 score=1151 t=3 mgn=58; DS-ROUND 3 base=1151 eval=80 stop
  maxgain=6; M1-BUILT n=2 t=3 C=1151 prog=2,0,2,1,0,1; REVISE
  old-C=509 new-C=1151; Mprev holds prog 1,0,2 with sup=1;
  UNIQ-APPEND-18 n=1. Every frozen number reproduced exactly.
- K-N1-5 (retained under N=1): PASS. TEST-DEPLOY C=771; retained=1;
  the 64 tag=6 ATTR lines satisfy sched = arr - 1 (covered by the
  K-N1-2 audit); M-BYTES-EQUAL 1.
- K-N1-6 (necessity): PASS. ARM-NOM C=0; menu controls SUM 578, MAX
  576, MIN 510, FIRST 512, LAST 508, each < 1151.
- K-N1-7 (determinism): PASS. Three runs byte-identical (sha256
  equal, above).

No falsifier fired (F-N1-LABEL, F-N1-ATTR, F-N1-MISATTR, F-N1-NOAVG,
F-N1-WRONGM, F-N1-NOMARGIN, F-N1-NOREVISE, F-N1-NORETAIN,
F-N1-MENU-WIN, F-N1-NONDET, F-N1-PYTHON all clear; no python/python3
in the worker PATH at any point).

## Frozen prediction: confirmed

PREREG section 6 froze the timing-only prediction: the N=1 run log
equals the VERIFY-TRANSFER (N=2) run log byte-for-byte except every
ATTR line's arr is exactly 1 less and the N1 markers replace the VT
markers. Confirmed:
- 110,337 DEPLOY lines byte-identical between n1_run1.txt and
  vt_run1.txt (`cmp` clean): the deployment schedule is
  delay-independent.
- Semantic join of all 110,337 ATTR lines by (sched, tag, k):
  110,337/110,337 pairs matched; zero C-or-t mismatches (every
  (sched,k,C,t) tuple identical); zero arr differences other than
  exactly 1 (N=2 arr = N=1 arr + 1 on every line).
- The only other diff lines are the marker renames (N1-START,
  K-N1-1..K-N1-7, N1-END).
The noise draws are delay-independent by construction (keyed on
region, program bytes, threshold, sample index), and the experiment
confirms the channel reproduces them exactly through N=1 timing.

## Method note

The frozen numbers were re-derived BEFORE the prereg by
/tmp/n1check.zag (pure Zag, separate code path: independently
written register machine, reimplemented noise spec, fresh
threshold/sum/selection logic, no delay, no channel). It reproduced
every VERIFY-TRANSFER number exactly (M0-FIT t=4 C=509; rounds
573/1085/-2, 66/1151/3, stop 6; M1 n=2 t=3 C=1151; TEST-SUM 771;
menus 578/576/510/512/508; K1 stall at n=1), confirming the numbers
are delay-independent predictions rather than N=2-specific fits.

## Environment incident (disclosed)

Mid-task the /home/hatch filesystem hit 100% full and writes to the
repo failed. To proceed I permanently removed one file:
`docs/generations/R33/runs/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_FINAL_NATIVE_20260915/recovered/logs/remaining_blob_2080.stdout`
(54,463,625 bytes). Before removal I verified with `cmp` that it is
byte-identical to the tracked
`docs/generations/R32/R32_V34_MULTISTEP_STATE_MODEL_SEED_9714.joblib`
(same sha256 5a21d2b8ebf744509acb9d22b2a7e8e1a80989405f547093a29d7114e5ce560f),
so no information was lost: the content survives in the R32 joblib
and in git history, and the file is restorable with
`git checkout -- <path>`. The deletion appears in working-tree git
status as an unstaged deletion; I did not commit it. The
recoverable-trash tool could not be used because it renames within
the same filesystem and would not have freed space. Disk space later
recovered on its own (concurrent workers), and all deliverables were
synced into the repo and re-verified (sha256/cmp) afterward.

## Non-claims

- One new world (SETTLE-DN1); transfer demonstrated across delay
  characteristics within the settlement world family (same episodes,
  same hidden rule, same noise as SETTLE-DN2); no claim beyond that.
- Targets the seven VERIFY-N1 bars only; does not claim Micah's full
  12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  Paper untouched. Nothing pushed. Commits local on tnn-native-lab.
