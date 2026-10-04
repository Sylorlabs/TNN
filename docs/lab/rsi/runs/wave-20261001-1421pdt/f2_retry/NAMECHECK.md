# NAMECHECK.md - F2 retry lane (wave-20261001-1421pdt, f2_retry)

Lane: active experiment construction, F2 retry (harder sustained goal).
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab (no commits, no
pushes, no checkouts by this worker; all files left uncommitted).

## Step 0: Toolchain Guard Check (mandatory, recorded first)

Date: 2026-10-01. Before any work:

1. Ran `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   (output: 36 tools linked; znc OK at
   /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1;
   verify lines confirm python3 and python absent from safebin PATH;
   SAFEBIN-READY).
2. `export PATH="$HOME/safebin"` applied to every subsequent command.
3. `which python3` prints nothing (exit 1). `which python` likewise.

Result: python3 and python are absent from the active PATH. Pure Zag only:
every program written and run in this lane is Zag compiled with the pinned
znc. Zero Python at any stage (no glue, analysis, verifiers, harnesses).
Zero forbidden-executable invocations.

## Step 1: Prior-record reconciliation (read before drafting)

The task pointed at docs/lab/rsi/runs/wave-20261001-0821pdt/actexp/ and
LOOP_STATE.md verdict lines. Findings:

- docs/lab/rsi/runs/wave-20261001-0821pdt/actexp/ EXISTS BUT IS EMPTY.
  The 0821pdt WAVE_RECORD.md says "actexp (F2 retry harder goal prereg):
  worker alive" and later "actexp, redteam: empty". The worker never
  delivered records. There is no F1 design and no F2 v1 prereg in that
  directory.
- LOOP_STATE.md at the wave directory does not exist. LOOP_STATE.md at the
  repo root (~/workspace/tnn-rsi/LOOP_STATE.md) contains no lines about the
  F2 autonomous-scientist lane (its "F2" hits are all FS-F2C and unrelated).
- The actual F1/F2 history lives under
  docs/lab/research-lead/overnight-20260928/autosci/ (F2 v1) and
  docs/lab/research-lead/overnight-20260928/autosci2/ (F2 retry). Both
  preregs and both result reports were read in full before drafting.

Reconstructed F1/F2 history:

- F2 v1 (autosci, prereg 2a87efa77, result 4ebde580a, 2026-09-30):
  BUILD-FAIL on K-AS5b. The loop worked in both sealed worlds; World B's
  goal (transient Y=1 within 6 steps) was a weak goal instance with ~5%
  random base rate, and the frozen random control hit 1/20 on the a priori
  seed 12345. Bar failure, not loop failure. Follow-up recommendation in
  the result: re-run World B with a harder sustained-control goal.
- F2 retry (autosci2, prereg b9ab0acb6, result 2026-09-30): the harder
  World B goal B2 (three consecutive steps with OBS Y=1 AND OBS K=0;
  pre-freeze calibration 0/160 random) achieved BUILD-PASS on all seven
  kill bars K2-R1..K2-R7, no architectural changes, 3/3 byte-identical
  runs. Later: memorization control closed (F2 beats memorization 2-0),
  independent reproduction verified (md5-identical). Ceiling assessed as
  bounded L2, never L3 (enumerate-then-select over a researcher-fixed
  alphabet; DDES is the lane that escapes it).

PREMISE NOTE FOR THE PARENT: the standing order as literally stated
("F2 v1 was BUILD-FAIL on a WEAK GOAL; retry with a HARDER SUSTAINED
GOAL") has already been fulfilled by AUTOSCI2 (BUILD-PASS, 2026-09-30).
Repeating the B2 triple goal in this lane would duplicate completed work.
This lane therefore drafts PREREG_F2_V2.md for the next harder step that
is NOT yet done: the unchanged F2 loop against FRESH sealed worlds with a
harder sustained goal (dual contextual control: two gating variables, two
delays, three consecutive joint observations, both contexts actively
verified). The prereg documents this distinction explicitly so the parent
can redirect if a different retry was intended.

## Non-duplication

- DDES (ddes lane, BUILD-PASS): schema derivation, scaffold disconnect,
  persisted-schema application. This lane does not touch it.
- AUTOSCI2: B2 triple-sustain goal on the v1 World B physics. This lane
  reuses neither its worlds nor its goal predicate.

## Architecture accounting (this wave: prereg only, writing-only step)

- Cognition source lines added: 0 (no implementation in this step).
- New hardcoded semantic cases: 0.
- New modes / bridges / routers: 0.
- New task-specific handlers: 0.
- New learner-state structures: 0.
- The F2 learner loop is reused UNCHANGED; only sealed worlds and the goal
  predicate change. Worlds are authored sealed substrate, not cognition.

## Verdict status

PREREG-DRAFTED (frozen prereg written; implementation not started).

## Addendum 2026-10-01 14:38 PDT: parent correction re-check

The parent corrected that the F1/F2 history should be findable via
wave-20261001-0821pdt/WAVE_RECORD.md and LOOP_STATE.md F2 verdict lines
(grep LOOP_STATE.md for F2), or nearby wave records. Re-checked all of
these paths fresh:

- WAVE_RECORD.md (0821pdt) mentions actexp exactly twice: "actexp (F2
  retry harder goal prereg): worker alive" (lane status) and "actexp,
  redteam: empty" (partial evidence). No F1 design, no F2 v1 prereg, no
  frozen kill bars, no BUILD-FAIL evidence.
- Root LOOP_STATE.md: every "F2" hit refers to FS-F2C (Micah's colorconst
  front-end), CF2 (judgment-indexed revision), or the H-PI-REV2 adversary
  allowed set {i,j,k,l,m,n,o,r,t,u,v,w}. Zero lines concern the F2
  autonomous scientist. Greps for "autosci", "autonomous scientist",
  "F2 retry", and "harder goal" return nothing.
- Nearby wave records (1121pdt, 0521pdt, 0221pdt, 0930-2321pdt): no
  actexp/autosci mentions in any of them. The only K-AS/AUTOSCI hits
  under docs/lab/rsi/runs/ are this lane's own files.

Conclusion: the F2 v1 BUILD-FAIL evidence and its frozen kill bars
(K-AS1..K-AS7) are NOT in WAVE_RECORD.md, LOOP_STATE.md, or nearby wave
records. They live only in
docs/lab/research-lead/overnight-20260928/autosci/ (PREREG_AUTOSCI.md,
RESULT_AUTOSCI.md), as recorded in Step 1 above. No change to the
PREREG_F2_V2.md draft results from this re-check.
