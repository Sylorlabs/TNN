# REPORT: Verification Machinery Transfer to a New World (VERIFY-TRANSFER)

Verdict: **VERIFY-TRANSFER-COMPLETE** (all seven frozen kill bars
pass, no falsifier fires).

Date: 2026-10-02. Worker: Verification Transfer Worker.
Prereg: `PREREG.md` (frozen ad0de3bcf; committed alone before any
implementation existed; zero amendments). Determinism: 3/3
byte-identical runs (sha256
58ac08c8d957a639c58451a889bf018a9960cb5fc5afca008e3a4f6ee4ea6004).

## What was built

The learner was NOT built: `learner_ds.zag` is a byte-identical copy
of the frozen `l3_delayed_stochastic/learner_ds.zag` (sha256
45ad35d892d629971a4679ffd2085b8bd54bf9c328d1e8eb1cededcc3ef3ae65,
`cmp` clean). It was not modified, rewritten, or adapted in any way.
New files, concatenated to `vt_full.zag` (learner + world + driver),
compiled with the pinned znc
(`src/tools/toolchain/znc_linux_x86_64_abed8aa1`) to `vt_bin`:

- `learner_ds.zag`: COPIED UNMODIFIED from the frozen sibling. Same
  ledger + K-averaging machinery: per-step ledger (tag, cand, thri,
  k), attribution by schedule step never recency, K-sample sums with
  per-cell count verification, greedy construction (gain > K/2),
  confidence policy. It calls exactly two world-side symbols,
  `w_sched_ds` and `w_arrive_ds`. Its 3-step drain covers the new
  N=2 delay with one spare poll step; nothing in the file names a
  delay value in behavior.
- `world_vt.zag`: new SETTLE-DN2 environment (experiment side only).
  Same frozen episode tables and hidden margin rule
  margin = e0+e1-e2 as the sibling family, but delay N=2 (not 3) and
  NEW noise: seed 109, draws (h mod 5)-2 in {-2,-1,0,1,2}
  (symmetric, zero-mean, wider than SETTLE-DS). `w_sched_ds` returns
  nothing; each noisy consequence is computed only when
  `w_arrive_ds(s+2)` is polled. `w_conseq_det` is the
  experiment-side deterministic immediate oracle (uniqueness sweep
  only; forbidden to the learner). Five menu controls.
- `driver_vt.zag`: new experiment-side driver. Teaches X train+test,
  seeds the inherited wrong M0, creates the world state, runs the
  learner's `l_experiment` (K=64 main arm: inherit, construct+revise,
  deploy held-out), evaluates the NOM and MENU arms (menu via
  experiment-side immediate noisy K=64 sums; delay shifts arrival
  time only, never values), runs the K=1 single-sample control arm
  through the new delayed channel, runs the experiment-side
  uniqueness sweep, and prints the kill-bar summary with the new
  frozen numbers. It never invents the intermediate.
- `audit_attr_vt.awk`: frozen attribution audit over the run logs
  (every ATTR: arr - sched == 2, DEPLOY at sched with same tag and
  same k, no ATTR-BAD / ATTR-COUNT-BAD).

Output via one preallocated 16MB buffer and a single raw syscall
write. 110337 deployments, 110337 arrivals, every arrival attributed
by (schedule step, sample index) under the new N=2 timing (first
arrival: `ATTR arr=2 sched=0 tag=1 k=0`).

## The transfer trace (K-VT1 through K-VT5)

Stage 0: M0 = [ADD R0,R2] (bytes 1,0,2, seeded experiment-side) is
fit through the NEW delayed noisy channel only: 8 thresholds x 64
samples deployed at consecutive steps, arrivals interleaved 2 steps
later, each arrival routed by (sched_step, k). First-max over the
attributed 64-sample sums:

```
M0-FIT t=4 C=509
M0-DEPLOY-ATTR C=509 bestC=509 conf=1
```

Stage 1: the unmodified learner constructs from the empty program.
Every candidate score is a 64-sample sum of delayed noisy arrivals
under the new noise; no label, no immediate consequence, no seed, and
no draw is ever consulted:

```
DS-ROUND 1 base=512 eval=80 win=2,0,2 gain=573 score=1085 t=-2 mgn=189
DS-ROUND 2 base=1085 eval=80 win=1,0,1 gain=66 score=1151 t=3 mgn=58
DS-ROUND 3 base=1151 eval=80 stop maxgain=6
M1-BUILT n=2 t=3 C=1151 prog=2,0,2,1,0,1
REVISE old-C=509 new-C=1151
M n=2 gen=1 sup=0 t=3 prog=2,0,2,1,0,1,...
MPREV n=1 gen=0 sup=1 prog=1,0,2,...
UNIQ-APPEND-18 n=1
```

Round 1: SUB R0,R2 is the winner (gain 573 > 32; winner-to-runner-up
189). Round 2: ADD R0,R1 is the winner (gain 66 > 32; margin 58).
Round 3 stops (maxgain 6 <= 32). The final intermediate
M1 = [SUB R0,R2, ADD R0,R1] (R0 = e0+e1-e2 exactly) appears nowhere
in the learner source, which is byte-identical to the sibling's.
Because 1151 > 509, the learner revises: M0 moves to Mprev with
sup=1, M1 becomes incumbent (bestC=1151, conf=2).

Attribution check: the round-1 winner bytes are 2,0,2, not any
misattribution artifact. F-MISATTR does not fire. The awk audit
confirms all 110337 arrivals satisfy arr - sched == 2 with matching
DEPLOY tag and k: the ledger machinery routed the new timing
without any code change.

Stage 1b (control): the identical learner code with K=1 through the
new delayed channel:

```
K1-ROUND 1 base=8 eval=80 win=2,0,2 gain=11 score=19 t=-2 mgn=3
K1-ROUND 2 base=19 eval=80 stop maxgain=0
K1-BUILT n=1 prog=2,0,2
K1-SELECT-M1 0
```

The single-sample delayed learner stalls at n=1 and does not select
M1: averaging is load-bearing under the new noise, not just the old.

Stage 2: M1 deployed 64 times (k=0..63) on the four held-out
episodes at t=3:

```
TEST-DEPLOY C=771 retained=1
M-BYTES-EQUAL 1
```

The 64 noisy consequences arrive 2 steps after their deployments,
are routed by (schedule step, k), sum to 771 > 0, so the learner
retains M1; its structural bytes are byte-identical across the
deployment.

## Kill bars

- K-VT1 (new-channel consequence-only verification): PASS. Shell
  grep audit on the committed byte-identical `learner_ds.zag`: all
  12 frozen patterns return 0 hits (label, expected, w_tab, margin,
  correct, _mode, bridge, handler, w_conseq, w_val, menu_, nz_;
  case-insensitive). The only world-side symbols referenced are
  `w_sched_ds` and `w_arrive_ds`.
- K-VT2 (every arrival attributed under N=2; every score a true
  K-sum): PASS. The frozen awk attribution audit passes on all 3 run
  logs (ATTR-AUDIT PASS, nattr=110337 each): every ATTR line
  satisfies arr - sched == 2 with a matching DEPLOY tag and k, and
  no ATTR-BAD or ATTR-COUNT-BAD line exists.
- K-VT3 (averaging is load-bearing under the new noise): PASS
  (in-Zag). K1-BUILT n=1 prog=2,0,2 with K1-SELECT-M1 0, while the
  K=64 arm selects M1 (revised=1, n=2, t=3, C=1151, bytes
  2,0,2,1,0,1).
- K-VT4 (correct M constructed via the new delayed noisy channel):
  PASS (in-Zag). M0-FIT t=4 C=509; DS-ROUND 1 win=2,0,2 gain=573
  score=1085 t=-2 mgn=189; DS-ROUND 2 win=1,0,1 gain=66 score=1151
  t=3 mgn=58; DS-ROUND 3 stop maxgain=6; M1-BUILT n=2 t=3 C=1151
  prog=2,0,2,1,0,1; REVISE old-C=509 new-C=1151; Mprev holds 1,0,2
  with sup=1; UNIQ-APPEND-18 n=1.
- K-VT5 (retained under the new delay+noise): PASS (in-Zag).
  TEST-DEPLOY C=771; retained=1; 64 ATTR lines with tag=6, each
  satisfying sched = arr - 2; M-BYTES-EQUAL 1.
- K-VT6 (necessity): PASS (in-Zag). ARM-NOM C=0 (wiped M: no
  decisions, no deployment, no consequence); menu controls SUM 578,
  MAX 576, MIN 510, FIRST 512, LAST 508, all < 1151.
- K-VT7 (determinism): PASS. 3/3 byte-identical (sha256 above;
  11,453,048 bytes per run log).

No falsifier fired: F-LABEL (audit clean), F-ATTR (awk audit pass),
F-MISATTR (winner bytes 2,0,2), F-NOAVG (K=1 arm n=1 prog=2,0,2,
K1-SELECT-M1 0), F-WRONGM (every frozen sum/gain/t/bytes reproduced
exactly), F-NOMARGIN (round-3 maxgain 6 <= 32, winner margins 189
and 58), F-NOREVISE, F-NORETAIN, F-MENU-WIN (best menu 578),
F-NONDET, F-PYTHON (safebin PATH, `which python3 python` empty for
the whole task; all computation in pure Zag).

## Pre-prereg independent verification

Before the prereg was written, all frozen numbers were derived by an
independent pure-Zag checker (/tmp/vtcheck.zag: closed-form program
evaluation, no register machine, reimplemented noise spec with seed
109 and (h mod 5)-2 draws, fresh threshold/sum/selection logic). It
confirmed: M0 at (t=4, sum=509); empty at (t=1, sum=512); round-1
winner SUB R0,R2 at (t=-2, sum=1085, gain=573, mgn=189); round-2
winner ADD R0,R1 at (t=3, sum=1151, gain=66, mgn=58); round-3
maxgain 6; K=1 arm at (n=1, prog=2,0,2) with round-1 (t=-2, sum=19,
gain=11, mgn=3) and round-2 maxgain 0; M1 test deployment sum=771;
menus at 578/576/510/512/508. Seed selection: candidates 100, 101,
... in order; seeds 100..108 were REJECTED because on each the K=1
arm appended a second instruction (the wider noise lets single
samples get lucky there; averaging not cleanly load-bearing); seed
109 was the first satisfying every criterion, and was frozen. The
implementation reproduced every number through the new delayed noisy
channel with the learner file byte-identical.

## Disclosed residual footprint and non-claims

- The op basis, register machine, greedy search, ledger, delayed
  noisy sweep, K-sample averaging loop, the gain bound K/2, the
  confidence policy, and the counter-based noise model with its seed
  are researcher-authored generic machinery. The transfer claim is
  narrow and explicit: the SAME learner file, byte-identical,
  verifies the intermediate through a new delay (N=2, every arrival
  2 steps late) and new noise (seed 109, draws in {-2..2}),
  attributing by schedule step and averaging over 64 routed
  arrivals per score.
- Transfer demonstrated is across delay/noise characteristics
  within the settlement world family (same episodes, same hidden
  rule). The transfer envelope is disclosed: the frozen 3-step
  drain covers any N <= 3; N=2 is the largest delay not equal to 3
  the unmodified machinery supports. No claim beyond that.
- The "DS-" log labels persist because the learner file is
  unchanged; they name the code path, not the world.
- This build targets the seven VERIFY-TRANSFER bars above. It does
  not claim Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.

## Files

All under `docs/lab/research-lead/overnight-20260928/verify_transfer/`:
NAMECHECK.md (toolchain guard Step 0 + build record), PREREG.md
(frozen), REPORT.md (this file), learner_ds.zag (byte-identical copy
of the frozen sibling; sha256
45ad35d892d629971a4679ffd2085b8bd54bf9c328d1e8eb1cededcc3ef3ae65),
world_vt.zag, driver_vt.zag, audit_attr_vt.awk, vt_full.zag, vt_bin,
vt_run1.txt, vt_run2.txt, vt_run3.txt.

Commit record:
- ad0de3bcf: PREREG.md + NAMECHECK.md alone (frozen,
  pre-implementation; explicit pathspecs).
- (this commit): implementation + REPORT (explicit pathspecs; the
  frozen sibling directory untouched).
- Nothing pushed; branch tnn-native-lab.
