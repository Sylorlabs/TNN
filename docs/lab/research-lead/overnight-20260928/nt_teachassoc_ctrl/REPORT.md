# REPORT: NT-TEACHASSOC-CTRL -- no-exploratory control arm for the D6 association signal

## Verdict

**CTRL-CONFIRMED** per the frozen verdict mapping (PREREG Section 7).
K1=1, K2=1, K3=1, K4=1, K5=1, K6=1, K7=1. Every frozen number --
ttcA/probeA/nevict/phev, all 6+6 per-pass probe flags, avail100,
avail160, c/nc/u/forget, bprobe, resprobe, apin/dec/res/useless/
fprate, evh(160/161/170/171), all EVHIST bins -- matches the prereg
exactly. The hand-derived Section 4 trace was byte-exact against
the binary on the first run.

## Frozen results (3/3 byte-identical)

- Run digest: `2c3b9f3f71fd27a7a41c83774c669e5a8826dfc61eef7504d28a44970865821f`
- Binary digest: `8a22ba1b0fbbec54f5d80ddee3477f60c9de0d3fccbee63d35326a0f17b26d3a`
- Source digest: `9e011ed9523f070a76612f1ccb5d12eadfeec26f7d841d551c608eadbb178f07`

```
NTTCTRL R6 ttcA=2 probeA=8 nevict=3 phev=0
NTTCTRL R6 PPROBE100 p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail100=4
NTTCTRL R6 PPROBE160 r1=0 r2=0 r3=0 r4=0 r5=0 r6=0 avail160=0
NTTCTRL R6 RET c=2 nc=2 u=4 forget=0 bprobe=3 resprobe=0
NTTCTRL R6 ASSOC apin=0 dec=0 res=0 useless=0 fprate=0 evh160=0 evh161=1 evh170=1 evh171=1
NTTCTRL R6 EVHIST 161=1 170=1 171=1
NTTCTRL K1=1 K2=1 K3=1 K4=1 K5=1 K6=1 K7=1
NTTCTRL VERDICT=CTRL-CONFIRMED
```

## Kill-bar evaluation

- K1 (learnability): PASS. ttcA = 2 (1..50), probeA = 8. No VOID.
- K2 (retention of uncontested structure): PASS. nc = 2, u = 4.
- K3 (D6 inertness): PASS. apin = 0 exact -- with D6's code IN the
  binary, the assoc pin was never granted. The inertness claim
  holds at the mechanism level, not by code removal.
- K4 (final revision outcome): PASS. c = 2, forget = 0.
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): PASS. nevict = 3 exact; evh(148) = 0 (the D5 pin
  still holds on the revision target); phev = 0; EVHIST exact:
  evh(161)=1, evh(170)=1, evh(171)=1, evh(160)=0, evh(140)=0,
  evh(141)=0, evh(143)=0, evh(144)=0.
- K6 (discriminative validity): PASS. avail100 = 4 AND nevict > 0
  (pressure actually exercised).
- K7 (no-rescue confirmation): PASS. avail160 = 0 AND resprobe = 0
  AND evh(161) = 1 -- the (161,1) link was evicted on pass 1 and
  never returned; q(160) never answered on any pass.

## What this establishes

1. **The rescue in NT-TEACHASSOC is attributable to the
   exploratory queries.** With the identical learner (D6 code
   present), identical capacity (CAP=22), identical teach order
   (residual + decoy on pass 1), and identical probe schedule --
   minus only the four exploratory query events -- the residual
   chain is not rescued: avail160 = 0, resprobe = 0, the
   continuation link (161,1) is the first pass-1 eviction victim
   and never returns. D6 granted zero pins (apin=0). The
   alternative explanations -- D6's mere presence in the binary,
   the CAP=22 capacity point, the decoy teachings, the per-pass
   q(160) probes stamping qstart_obs[160] -- are all ruled out by
   this arm: none of them armed the pin.
2. **D6 is provably inert without the exploratory episode.** The
   frozen argument (PREREG 2.2) is confirmed behaviorally: no
   install of 160/161/170/171 ever occurs within W=20 ticks of
   an observed query start of the same subject, so the pin
   condition can never fire. The learner reduced exactly to the
   D5 learner at every eviction decision.
3. **NT-RESIDUAL's headline reproduces at the mechanism level.**
   NT-RESIDUAL (CAP=20): avail160=0, resprobe=0, residual links
   evicted, never return. This arm (CAP=22, NT-TEACHASSOC world):
   avail160=0, resprobe=0, (161,1) evicted pass 1, never
   returns. The eviction bookkeeping differs mechanically
   (nevict=3 vs 12; at CAP=22 the youngest-of-R=0 victims are
   161, then the incoming 170, then the incoming 171 -- 160
   survives but is unanswerable without its continuation), and
   those differences were frozen predictions, not
   discrepancies. The directional finding is identical: no
   learner-available signal in this workload predicts the
   residual link's usefulness, and without the exploratory
   queries there is no rescue.

## What this does NOT establish (honest boundaries)

- Single-factor control (exploratory episode only). Partial
  exploratory coverage (q(160) only), W sensitivity, and the
  capacity sweep remain untested follow-ups.
- The control does not re-test NT-RESIDUAL's CAP=20 world; it
  tests NT-TEACHASSOC's world at CAP=22 minus the exploratory
  episode. The NT-RESIDUAL comparison is mechanism-level
  (headline numbers), not bin-level.
- The LINKS are memorized associations; no rule induction
  tested; no L2/L3 claim.
- Single capacity point (CAP=22, 1.14x); single contradiction
  magnitude; M=6 fixed; single arm (R6, K=6).

## Recommended follow-up (not preregistered; for the parent)

- The W-sensitivity and chain-continuation variants from
  NT-TEACHASSOC's follow-up list now have their control arm in
  place; any of them can reuse this binary's harness.
- Capacity sweep (CAP=20/22/24) for the assoc pin's opportunity
  cost curve (NT-TEACHASSOC follow-up #2) is still open.

## Provenance

- Prereg frozen alone: commit
  `02cd84a3d75756dd767a894fff76be108fb20680` on `tnn-native-lab`
  (PREREG.md + NAMECHECK.md only), strictly before
  implementation. Commit-order self-check: `git log` shows
  02cd84a3d strictly precedes the implementation commit below;
  no implementation file existed at prereg time.
- Implementation + results: this commit. Pure Zag, safebin-only
  PATH, pinned znc 2026.07.0-dev (same build as NT-TEACHASSOC).
  `which python3` and `which python` return nothing under the
  worker PATH. Zero forbidden-executable invocations. The string
  "python" appears in the source only in the comment "Pure Zag.
  No Python."
- Source: `ntctrl_full.zag` = NT-TEACHASSOC's `ntteach_full.zag`
  verbatim EXCEPT: (a) the four exploratory h_query calls in
  run_arm deleted; (b) output tag NTTEACH -> NTTCTRL; (c) the
  fprate print guarded against apin=0 (prints fprate=0; no
  division by zero); (d) kill bars / verdict codes rewritten per
  the frozen PREREG Sections 6-7. No learner rule touched.
- Build: `znc ntctrl_full.zag -o ntctrl_bin` under safebin-only
  PATH (exit 0; benign zagd-unavailable warning only -- the 4
  benign A0102 warnings from NT-TEACHASSOC are gone with the
  exploratory calls). 3/3 runs byte-identical (cmp), exit 0,
  zero stderr.
- Compiler-defect workarounds honored (single-buffer cursor
  output + one raw syscall; no `as *i32`+slice; no `!(A && B)`
  in while conditions; no `[]u8 as *u8` casts;
  `_zag_malloc as *u8` threaded through; K5 bar assembled from
  hoisted 0/1 flags with a single flat product check to keep
  if-nesting at 3 or fewer).
- Audit: no protection/task-label/freeze/importance/mode/
  usefulness-label logic in the learner beyond the frozen D5 pin
  and the D6 assoc rule under test (inert here); the K selector
  and probe schedule are harness conditions.
- Commits local only, explicit pathspecs, never pushed. This is
  a non-ledger task (claim minting paused): no ledger update.
