# PREREG: NT-LIFOBOUND -- The LIFO boundary: novel subjects NOT re-taught

## 1. Question

NT-PRESSURE (C439, PORT-PASS-ALL) proved D1+D2 survives to 5x pressure
with novel subjects re-taught every pass: MAIN revision 6/6, FORGET=0,
nevict=3N_n-10, zero phase-1 subjects evicted across 426 MAIN
evictions. NT-PRESSURE PREREG Section 8 left one boundary explicitly
open (preregistered, untouched): "Whether LIFO's tenure principle
holds when novel subjects are NOT re-taught every pass."

This battery probes that boundary. Novel subjects are taught ONCE
(phase-2 pass 1 only), never re-taught. The liability hypothesis: the
once-taught novel subjects become permanent residents under LIFO
tenure-protection and block revision of the contradicted entries. The
null (mechanism) hypothesis: revision is in-place via the frozen
evidence update, the once-taught novel subjects remain
eviction-eligible (youngest-first), and the evidence machinery handles
it -- no liability.

## 2. Subject (frozen: the NT-PRESSURE port verbatim, one protocol change)

The subject is NT-PRESSURE's subject unchanged: the continuing-learner
skeleton (associative instance memory, sequential lifetime phases,
single main(), no resets, no task labels) with ONLY the D1+D2 memory
rules installed (slot fields subj/rel/obj/dom/valid/sup/ref/ins;
NT-frozen evidence update; D1 checkpoint/restore keyed by (subj,rel);
D2 evict-youngest by max ins; ABL arm = same substrate, NT2
lowest-net comparator, no checkpoint table). This is the same
skeleton, not a redesign. The ONLY frozen change vs NT-PRESSURE is
the phase-2 teaching protocol:

- Phase-2 pass 1: C (100..105) taught O2(k); K (106..109) taught
  O1(k); N (120..nhi) taught O1(k). Identical to NT-PRESSURE.
- Phase-2 passes 2 and 3: C (100..105) taught O2(k); K (106..109)
  taught O1(k); N subjects NOT taught (no re-teaching).
- Everything else (phase 1 to criterion, retention probe, FORGET
  definition, CAP=20, arena layout, D1/D2/ABL rules, evidence update)
  is NT-PRESSURE's verbatim.

Rationale for the minimal change: the preregistered question is
specifically about the re-teach regime. Any other change would
confound the boundary.

## 3. Workload (frozen numeric inventory; opaque identifiers)

Oracles identical to NT-PRESSURE (opaque numeric subject ids
100..203; no semantic labels anywhere):

- O1(k) = 200 + ((k*37 + 11) mod 64), all k. (Oracle, phase 1.)
- O2(k) = 200 + (((O1(k)-200)+32) mod 64) for contradicted subjects,
  guaranteed different from O1(k). (Oracle, phase 2.)
- Phase 1 ("early experience"): 16 subjects 100..115, obj O1(k).
  Train to criterion: repeat passes; after each pass probe all 16.
  Criterion = 16/16 correct for 2 consecutive passes. Max 50 passes
  (fail-safe; hitting it = arm FAIL at that pressure point).
- Phase 2 ("world change + single novel exposure"): 3 passes over,
  in ascending order: pass 1: C (100..105) taught O2(k), K (106..109)
  taught O1(k), N (120..119+N_n) taught O1(k); passes 2-3: C taught
  O2(k), K taught O1(k), N not taught. U (110..115) never taught in
  phase 2.
- Retention probe: query all 16+N_n subjects. Score C (100..105) vs
  O2, K (106..109) vs O1, U (110..115) vs O1, N presence
  (120..119+N_n). FORGET = subjects among C+K+U answering neither
  their phase-1-correct nor (for C) their phase-2-correct obj
  (absent -> -1 counts as forgotten).

Pressure points (frozen; CAP=20 fixed; same three points as
NT-PRESSURE for direct comparability):

- P2: N_n = 24, N = 120..143, total 40 subjects, ratio 2.0x.
- P3: N_n = 44, N = 120..163, total 60 subjects, ratio 3.0x.
- P5: N_n = 84, N = 120..203, total 100 subjects, ratio 5.0x.

Arms per pressure point (each on a FRESH learner): MAIN (D1+D2),
ABL (rules removed). One binary runs all six arms sequentially and
emits all lines; 3 runs must be byte-identical.

## 4. Frozen predictions (hand-derived by tracing the NT-PRESSURE rules
##    under the no-reteach protocol; general N_n, then per-point)

Phase 1 is identical to NT-PRESSURE at all points (no pressure):
TTC1 = 2, probe1 = 16/16, nevict = 0. Slots hold 100..115 with
(O1, sup=2, ref=0); MAIN ins stamps 1..16.

MAIN (D1+D2), phase 2. Pass 1: C hit+mismatch -> ref=1 (in place,
ins untouched, still 1..6, oldest); K hit+match -> sup=3 (in place);
s_1..s_4 (120..123) fill the 4 free slots (ins 17..20);
s_5..s_{N_n} revolving-door evictions on the youngest slot: N_n-4
evictions, victims 123 then 124..118+N_n (each once), all D1
checkpointed. End of pass 1: present = 100..115 (ins 1..16),
120,121,122 (ins 17,18,19), 119+N_n (ins 16+N_n). Pass 2: C
ref 1->2 (in place); K sup 3->4 (in place); N not taught -> 0
evictions (no absent-subject insertions). Pass 3: C ref 2->3 >
sup 2 -> revise in place to (O2,1,0), ins untouched; K sup 4->5;
0 evictions. Total MAIN nevict = N_n-4 (pass-1 revolving door
only; the pigeonhole lower bound for inserting N_n novel subjects
into 4 free slots). phev_main = 0 (no phase-1 subject is ever the
max-ins victim). Retention: C = O2 (6/6), K = O1 (4/4), U = O1
(6/6), N presence = {120,121,122,119+N_n} = 4, FORGET = 0.
EVHIST_main: bins 123..118+N_n = 1 each.

ABL (no D1, lowest-net comparator, no ins stamps), phase 2. Pass 1:
C ref=1 (net 1); K sup=3 (net 3); s_1..s_4 fill slots (net 1);
s_5..s_{N_n} revolving door on slot 0 (lowest net 1, lowest slot
index): N_n-4 evictions, victims 100 then 124..118+N_n. End of
pass 1: slot 0 = 119+N_n (net 1); 100 absent; 101..105 (O1,2,1,
net 1); 106..109 (net 3); 110..115 (net 2); 120..123 (net 1).
Pass 2: C 100 absent -> insert, evicts slot 0 (119+N_n; net 1,
lowest slot index among net-1 candidates): 1 eviction. C 101..105
hit+mismatch -> ref=2 (net 0). K sup=4. Pass 3: C 100 hit+match ->
sup=2; C 101..105 hit+mismatch -> ref=3 > sup=2 -> revise in place
to (O2,1,0); K sup=5; 0 evictions. Total ABL nevict = N_n-3.
Retention: C = O2 (6/6 -- the contradicted subjects revise even in
ABL); K = 4/4; U = 6/6; FORGET_abl = 0; phev_abl = 1 (subject 100
evicted in pass 1). EVHIST_abl: bin 100 = 1, bins 124..119+N_n = 1
each.

Frozen numeric predictions per pressure point:

P2 (N_n=24):
- MAIN: ttc=2, probe1=16, nevict=20, RET c=6 k=4 u=6 npres=4
  forget=0 phev=0. EVHIST: 123..142=1 each; 100..115=0.
- ABL: ttc=2, probe1=16, nevict=21, RET c=6 k=4 u=6 forget=0
  phev=1. EVHIST: 100=1, 124..143=1 each.

P3 (N_n=44):
- MAIN: ttc=2, probe1=16, nevict=40, RET c=6 k=4 u=6 npres=4
  forget=0 phev=0. EVHIST: 123..162=1 each; 100..115=0.
- ABL: ttc=2, probe1=16, nevict=41, RET c=6 k=4 u=6 forget=0
  phev=1. EVHIST: 100=1, 124..163=1 each.

P5 (N_n=84):
- MAIN: ttc=2, probe1=16, nevict=80, RET c=6 k=4 u=6 npres=4
  forget=0 phev=0. EVHIST: 123..202=1 each; 100..115=0.
- ABL: ttc=2, probe1=16, nevict=81, RET c=6 k=4 u=6 forget=0
  phev=1. EVHIST: 100=1, 124..203=1 each.

### Predicted outcome (frozen, directional; two dimensions separated)

DIMENSION A -- the liability question (MAIN arm, K1..K4): NO
LIABILITY. The trace predicts K1..K4 HOLD at all three points:
revision completes in pass 3 (c=6), FORGET stays 0, churn is at the
pigeonhole minimum (N_n-4) confined to novel subjects, zero
phase-1 subjects evicted. Mechanism: revision is in-place via the
frozen evidence update (never needs a slot), and the once-taught
novel subjects are eviction-eligible (youngest-first under D2),
not permanent blockers. The liability hypothesis is predicted
FALSIFIED on this skeleton.

DIMENSION B -- discriminative validity (K5): FAILS at all three
points -> INCONCLUSIVE per the frozen mapping. The ABL arm is
predicted to revise the contradicted subjects successfully
(c_abl=6, forget_abl=0, nevict_abl=N_n-3), NOT reproduce the NT2
failure signature (c=0, forget=6). Mechanism: the NT2 signature was
churn-dependent -- in NT-PRESSURE, the re-taught novel subjects'
revolving door kept evicting ABL's contradicted subjects (net 0)
before ref could exceed sup. Without re-teach churn, even
lowest-net eviction with no checkpoints completes revision. The
no-reteach regime is too easy to discriminate fragility modes;
that is an apparatus finding, not a D1+D2 finding.

Predicted per-point verdict: K1=1, K2=1, K3=1, K4=1, K5=0 ->
INCONCLUSIVE at P2/P3/P5 (K5 fails while K1..K4 hold). Predicted
overall: INCONCLUSIVE, with Dimension A (no liability) and
Dimension B (apparatus cannot discriminate here) reported
separately.

### What would falsify the prediction (honest INFORMATIVE-FAIL triggers)

If the binary shows, at any point, any of the following, the
no-liability prediction is falsified and the verdict is an
INFORMATIVE-FAIL naming LIFO as a liability (verdict mapping
Section 7 prioritizes these over K5):

- c_main < 6 or forget_main > 0: once-taught novel subjects
  blocked revision of contradicted entries, or contradicted
  entries were forgotten -> the dark side is REAL
  (FAIL-RETENTION).
- phev_main > 0: a phase-1 subject was evicted in MAIN ->
  tenure-protection failed under the no-reteach regime
  (FAIL-K2).
- nevict_main != N_n-4: untraced churn (more) or missing
  insertions (fewer) -> the trace is wrong; mechanism unknown
  (FAIL-K2).

## 5. Assembly, build, run (frozen)

- Single source file `nt_lifobound_full.zag`: the NT-PRESSURE source
  (`nt_pressure_full.zag`, C439) with ONLY the frozen Section 2
  change (teach_p2 takes a pass index; N taught only on pass 1) and
  the Section 6 kill-bar literals. D1/D2/ABL rules, evidence
  update, arena layout (4096 bytes; 104-entry checkpoint table;
  104-bin histogram, subjects 100..203), oracles, and protocol are
  NT-PRESSURE's verbatim. Output tag `NTLIFO`.
- Canonical helpers copied verbatim (z_alloc, get32, set32, o_app,
  o_i64, o_nl, o_flush).
- Build: `znc nt_lifobound_full.zag -o nt_lifobound_bin` under
  safebin-only PATH.
- Run `nt_lifobound_bin` 3 times; outputs `nt_lifobound_run1.txt`,
  `nt_lifobound_run2.txt`, `nt_lifobound_run3.txt`. Require
  byte-identical (cmp) and record sha256.
- Output lines (all numeric): per pressure point and arm: TTC1,
  probe1, nevict, retention (c/k/u/npres/forget), nonzero
  eviction-histogram bins, MAIN phase-1-eviction count (bins
  100..115, for K2), ABL phase-1-eviction count, and per-point
  K1..K5 verdict bits plus a per-point verdict line.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic output
  only via the single-buffer cursor helpers + one `_zag_raw_syscall`
  write (never `_zag_print`); no `!(A && B)` in while conditions
  (De Morgan); if-nesting at most 3 deep with hoisted call results;
  no `[]u8 as *u8` casts (thread `_zag_malloc as *u8`).

## 6. Frozen kill bars (per pressure point p; N_n(p) = 24/44/84)

- K1_p (learning intact under capacity; else VOID at p): ttc_main
  in 1..50 AND probe1_main = 16 AND ttc_abl in 1..50 AND
  probe1_abl = 16. Else VOID at p.
- K2_p (eviction minimal, no churn, victims confined to N):
  nevict_main == (N_n - 4) AND phev_main == 0 (zero evictions of
  phase-1 subjects 100..115 in MAIN, from the histogram).
- K3_p (uncontested retention survives): k_main = 4 AND u_main = 6.
- K4_p (revision survives without re-teaching): c_main = 6 AND
  forget_main = 0.
- K5_p (discriminative validity; NT2 signature, UNCHANGED from
  NT-PRESSURE): (c_abl = 0 AND forget_abl = 6) AND (u_abl = 6 AND
  nevict_abl = 3*N_n - 10). If the ABL signature matched MAIN's at
  p, the apparatus cannot distinguish fragility modes there ->
  INCONCLUSIVE at p, never PASS at p. NOTE: K5 is deliberately NOT
  redefined for the no-reteach regime; redefining it to fit the
  regime would be moving the goalposts. Its predicted failure is
  the Dimension B finding.

## 7. Verdict mapping (frozen; liability-prioritized)

Per pressure point (K5 checked LAST so a genuine liability is
never masked by the predicted K5 failure):

- K1 fails -> VOID at p.
- K2 fails -> FAIL-K2 at p (tenure/churn liability: victims
  escaped the N set, or churn exceeded/trailed the traced
  minimum).
- K3 or K4 fails -> FAIL-RETENTION at p (revision liability: the
  dark side -- once-taught novel subjects blocked revision or
  caused forgetting).
- K1..K4 hold, K5 fails -> INCONCLUSIVE at p (predicted: the
  apparatus cannot discriminate fragility modes in the
  no-reteach regime; the ABL signature is churn-dependent).
- K1..K5 all hold -> LIFOBOUND-PASS at p (no liability AND the
  apparatus discriminates; NOT predicted).

Overall: INCONCLUSIVE at P2, P3, P5 -> overall INCONCLUSIVE
(predicted), reported with Dimension A (liability: none found)
and Dimension B (discrimination: not achieved here) separated.
Any FAIL-K2 or FAIL-RETENTION at any point -> that point is an
INFORMATIVE-FAIL: LIFO's tenure-protection IS a liability under
the no-reteach regime; report the failed bars with the
histogram-derived mechanism.

## 8. Honest boundaries (pre-declared)

- Same skeleton as NT-PRESSURE, not a redesign; the port boundary
  from NT-PORT PREREG Section 1.1 stands (contlearn2 schema
  machinery and H-CONTLIFE-1 hash-table memory remain unported).
- Subjects are memorized (subj,rel)->obj associations; no L2/L3
  claim. The experiment measures retention/revision/eviction
  dynamics only.
- The no-reteach regime removes the churn that produced ABL's NT2
  signature; this battery therefore cannot re-establish the K5
  discrimination NT-PRESSURE achieved. That limitation is the
  predicted Dimension B outcome, not a flaw to patch mid-battery.
- Three capacity points (2x/3x/5x); single contradiction
  magnitude; graded contradiction out of scope.
- The eviction histogram is measurement-only; the checkpoint table
  holds only the learner's own prior evidence.
- Recommended next probe (not this battery): restore churn WITHOUT
  re-teaching by supplying FRESH novel subjects each pass (each
  taught once). That tests LIFO victim-choice under genuine
  pressure while keeping "taught once", and should restore K5
  discrimination if the churn-dependence account is correct.

## 9. Amendment record (transparent; committed before implementation)

(none yet)
