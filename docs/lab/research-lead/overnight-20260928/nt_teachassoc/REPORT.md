# REPORT: NT-TEACHASSOC -- teaching-stream association signal for the residual case

## Verdict

**ASSOC-CONFIRMED** per the frozen verdict mapping (PREREG Section 8,
as amended by Amendment 1).
K1=1, K2=1, K3=1, K4=1, K5=1, K6=1, K7=1. Every frozen number --
ttcA/probeA/nevict/phev, all 6+6 per-pass probe flags, avail100,
avail160, c/nc/u/forget, bprobe, resprobe, apin/dec/res/useless/
fprate, evh(160/161/170/171), all EVHIST bins -- matches the amended
prereg exactly.

## Frozen results (3/3 byte-identical)

- Run digest: `aec8cfc5ef734399c7e326d136bf35545a903cdc9e1bc122a5bccfa3939acfc1`
- Binary digest: `63eb84da13666916ee9f3bde9ce666c39d2313966d5d14f77ba1d23bb8e2cdae`
- Source digest: `57b7a91f7be1d0a0f33d3c8a950e150cfe01195a40486d2a0bcdf470113bb9a2`

```
NTTEACH R6 ttcA=2 probeA=8 nevict=22 phev=0
NTTEACH R6 PPROBE100 p1=0 p2=0 p3=1 p4=1 p5=1 p6=1 avail100=4
NTTEACH R6 PPROBE160 r1=1 r2=1 r3=1 r4=1 r5=1 r6=1 avail160=4
NTTEACH R6 RET c=2 nc=2 u=4 forget=0 bprobe=1 resprobe=1
NTTEACH R6 ASSOC apin=4 dec=1 res=1 useless=2 fprate=50 evh160=0 evh161=0 evh170=0 evh171=0
NTTEACH R6 EVHIST 140=5 141=6 143=6 144=5
NTTEACH K1=1 K2=1 K3=1 K4=1 K5=1 K6=1 K7=1
NTTEACH VERDICT=ASSOC-CONFIRMED
```

## Kill-bar evaluation

- K1 (learnability): PASS. ttcA = 2 (1..50), probeA = 8. No VOID.
- K2 (retention of uncontested structure): PASS. nc = 2, u = 4.
  No A-link was evicted (phev = 0, evh(118) = 0).
- K3 (the D6 rescue bar): PASS. avail160 = 4 exact (passes 3-6),
  resprobe = 1, evh(160) = 0 AND evh(161) = 0 (the residual chain
  was never evicted). Note r1 = r2 = 1 as well: the residual
  answers from pass 1, unlike NT-RESIDUAL where it never answered.
- K4 (final revision outcome): PASS. c = 2, forget = 0.
- K5 (pressure exercised, eviction discipline, mechanism
  attribution): PASS (amended bar). nevict = 22 exact;
  evh(148) = 0 (the D5 pin still holds on the revision target);
  phev = 0; EVHIST exact: 140=5, 141=6, 143=6, 144=5.
- K6 (discriminative validity): PASS. avail100 = 4 (the D5-covered
  probe passes when its link is present; not a broken probe) AND
  nevict > 0 (pressure actually exercised).
- K7 (false-positive control confirmation): PASS. dec_present = 1
  (the decoy chain survived to end-of-run) AND nassoc_useless = 2
  (both decoy entries never contributed to a successful query).

## What this establishes

1. **The teaching-stream association signal works where the stream
   carries the dependence.** D6 (same-subject: pin entries taught
   within W=20 ticks of an observed query start of the same
   subject) protected the residual chain (160,1)->161 and
   (161,1)->162 through the pass-1 eviction that killed it in
   NT-RESIDUAL. The pass-1 victims were instead the unpinned FREQ
   novels (144, 143, 141). avail160 went 0 -> 4, resprobe 0 -> 1,
   evh(160)=evh(161)=0. The residual case is rescuable by a
   learner-available signal -- provided the world supplies the
   dependence. This is the precise complement to NT-RESIDUAL's
   impossibility finding: the signal class NT-RESIDUAL left
   untested now has a positive existence proof.
2. **The signal is learner-available.** D6 uses only the teach
   event stream, the query event stream the learner itself
   processes, and a tick counter -- all in learner state. No
   oracle (the harness never labels usefulness, and the
   exploratory queries are indistinguishable from any other
   query event), no task labels, no frozen kill-bar knowledge.
   With qstart_obs all -INF the rule is provably inert and the
   learner reduces exactly to NT-RESIDUAL's D5 learner.
3. **The false-positive cost is real and measured: 50%.** The
   decoy chain (170,1)->171, (171,1)->172 had IDENTICAL
   stream-adjacency to observed query starts (gap 14 ticks, same
   W=20 window) and was assoc-pinned and protected to end-of-run
   (dec_present=1, evh(170)=evh(171)=0) -- yet q(170) was never
   probed for usefulness and both entries have reads=0
   (nassoc_useless=2, fprate=50). The signal is a question-answer
   association detector, NOT a usefulness detector: it cannot
   distinguish "asked then taught, later used" from "asked then
   taught, never used," because future usefulness is not in the
   observable stream. This mirrors NTNL's honest limitation for
   D5 and is the lane's second headline.
4. **Dissociation holds: D5 and D6 cover different links in the
   same run.** D5's pin still protects the revision target 148
   (avail100=4, evh(148)=0, pass-3 revision intact); D6 protects
   160/161/170/171; FREQ novels are covered by neither and absorb
   all 22 evictions. No new mode, bridge, or handler was added:
   D6 is one pin condition in the existing victim scan.

## What this does NOT establish (honest boundaries)

- The 50% FP rate is world-relative (one decoy chain, never used).
  It does not generalize; the directional claim is that the signal
  class cannot see future usefulness.
- Same-subject adjacency is the frozen operationalization. Chain
  continuation beyond the queried subject is NOT covered by D6 as
  frozen; this world supplies qstart_obs for both chain subjects
  via the exploratory episode. A world that only ever queries
  q(160) would leave (161,1) unprotected -- untested here.
- Capacity sensitivity (exploratory, not frozen): at CAP=20
  (1.25x) the four assoc pins structurally displace an A-link on
  pass 2 (every R=0 slot pinned), which would break K2. Pinning
  useless entries has opportunity cost; a capacity sweep is
  follow-up, not run here.
- Single capacity point (CAP=22, 1.14x); single contradiction
  magnitude; M=6; single arm (R6, K=6); W=20 fixed.
- No-exploratory control arm not run (D6 provably inert without
  it); recommended follow-up.
- The LINKS are memorized associations; no rule induction tested;
  no L2/L3 claim.
- Amendment 1 corrected a hand-derivation error (passes 3-6 have
  4 evictions each, not 3); the original numbers are preserved in
  git history. The bar was corrected, not weakened (still exact).

## Recommended follow-up (not preregistered; for the parent)

- No-exploratory control arm (D6 inert -> reproduces NT-RESIDUAL
  numbers at CAP=22): cheap, confirms the dependence claim.
- Capacity sweep (CAP=20/22/24): map the assoc pin's opportunity
  cost curve; at what pressure does protecting 4 entries break
  retention?
- Chain-continuation variant: exploratory queries only q(160)
  (not q(161)) -- does D6's same-subject rule leave (161,1)
  exposed? Tests the signal's multi-hop limit.
- W sensitivity: how tight can the window be before the residual
  is missed? (Gap here is 14 ticks by construction.)
- The stale-pin boundary (NTNL follow-up #2) still stands untested.

## Provenance

- Prereg frozen alone: commit `4aa6b2680f1aa725f94b2c453a5148ea0ba6d57c`
  on `tnn-native-lab` (PREREG.md + NAMECHECK.md only), strictly
  before implementation. Commit-order self-check: `git log`
  shows 4aa6b2680 strictly precedes the implementation commit
  below; no implementation file existed at prereg time.
- Amendment 1 (transparent correction of the Section 5
  hand-trace; rules/workload/protocol unchanged; K5 still exact):
  commit `5351f79ecc053006fe4d38f62f5edbdb6bd86a97` on
  `tnn-native-lab`, before any verdict was recorded. The original
  numbers remain in git history for audit.
- Implementation + results: this commit. Pure Zag, safebin-only
  PATH, pinned znc 2026.07.0-dev. `which python3` and `which
  python` return nothing under the worker PATH. Zero
  forbidden-executable invocations. The string "python" appears
  nowhere in the source.
- Source: `ntteach_full.zag`, written to PREREG Sections 2-4
  (learner: NT-RESIDUAL D1+D4+D5 verbatim + D6 assoc pin via
  tick/qstart_obs/W=20; oracles: NT-RESIDUAL verbatim plus the
  exploratory episode, the decoy chain, CAP=22). Layout: 20-byte
  header (tick at 16), 44-byte slots (assoc at field 10),
  qstart_obs region for subjects 100..171. A layout bug found at
  first run (qo/ck/evh regions sized for 66 subjects but 170/171
  need indices 70/71 -> slice-out-of-bounds panic) was fixed by
  extending all three regions to 72 subjects before any results
  were recorded; the fix is rule-neutral (sizes only).
- Build: `znc ntteach_full.zag -o ntteach_bin` under safebin-only
  PATH (exit 0; benign zagd-unavailable warning + 4 benign A0102
  warnings on the intentionally result-discarding exploratory
  queries). 3/3 runs byte-identical (cmp), exit 0, zero stderr.
- Audit: no protection/task-label/freeze/importance/mode/
  usefulness-label logic in the learner beyond the frozen D5 pin
  and the D6 assoc rule under test; the K selector, exploratory
  episode, and probe schedule are harness conditions.
  Compiler-defect workarounds honored (single-buffer cursor
  output + one raw syscall; no `as *i32`+slice; no `!(A && B)`
  in while conditions; no `[]u8 as *u8` casts; `_zag_malloc as
  *u8` threaded through).
- Debug instrumentation (per-pass nevict, per-eviction victim
  prints) was done ONLY in /tmp scratch copies, never in the
  committed source or binary.
- Commits local only, explicit pathspecs, never pushed. This is
  a non-ledger task (claim minting paused): no ledger update.
