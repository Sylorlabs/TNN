# PREREG: NT-PRESSURE -- Scale the D1+D2 pressure ratio to 2x/3x/5x

## 1. Question

NT-PORT (C437 PORT-PASS) confirmed the D1+D2 rules transfer from the
minimal surrogate to the shared continuing-learner substrate at 1.3x
pressure (CAP=20, 26 subjects): MAIN revision 6/6, FORGET=0,
nevict=20, all victims novel subjects; ABL reproduced the NT2 failure
signature on the same substrate. NT-PORT PREREG Section 9 preregisters
this lane as the next step: scale the pressure ratio (1.3x -> higher)
with the same bars and the forget regime stated explicitly.

This battery asks: at what pressure does D1+D2 break? Three pressure
points, frozen: 2x, 3x, 5x (subjects vs capacity). At each point: does
FORGET stay 0? Does revision stay 6/6? Does eviction stay at the
traced minimum with the victim set confined to novel subjects?

## 2. Subject (frozen: the NT-PORT port verbatim, novelty load scaled)

The subject is NT-PORT's port unchanged: the continuing-learner
skeleton (associative instance memory, sequential lifetime phases,
single main(), no resets, no task labels) with ONLY the D1+D2 memory
rules installed (slot fields subj/rel/obj/dom/valid/sup/ref/ins; NT-
frozen evidence update; D1 checkpoint/restore keyed by (subj,rel); D2
evict-youngest by max ins; ABL arm = same substrate, NT2 lowest-net
comparator, no checkpoint table). This is the same skeleton, not a
redesign. The ONLY frozen changes vs NT-PORT are the scaled numeric
inventory and the storage sizing it requires:

- N (novel) subject count per pressure point (Section 3); C/K/U
  partitions and phase 1 are byte-identical to NT-PORT.
- D1 checkpoint table: 104 entries x 16 bytes (subjects 100..203),
  indexed (subj-100) exactly as NT-PORT indexed 30 entries.
- Eviction histogram (measurement-only): 104 bins, subjects 100..203.
- Arena allocation 4096 bytes (2736 used: 16 header + 640 slots +
  1664 checkpoints + 416 histogram).
- CAP = 20 slots, unchanged. The N range is the single pressure
  variable; nothing else in the learner moves.

The checkpoint table and histogram are sized, not cognitive: they hold
no oracle information and influence no learner decision (histogram) or
only the learner's own prior evidence (checkpoints, as in NT-PORT).

## 3. Workload (frozen numeric inventory; opaque identifiers)

Identical to NT-PORT except the N range:

- O1(k) = 200 + ((k*37 + 11) mod 64), all k. (Oracle, phase 1.)
- O2(k) = 200 + (((O1(k)-200)+32) mod 64) for contradicted subjects,
  guaranteed different from O1(k). (Oracle, phase 2.)
- Phase 1 ("early experience"): 16 subjects 100..115, obj O1(k).
  Train to criterion: repeat passes; after each pass probe all 16.
  Criterion = 16/16 correct for 2 consecutive passes. Max 50 passes
  (fail-safe; hitting it = arm FAIL at that pressure point).
  Records TTC1.
- Phase 2 ("world change + novel experience"): 3 FIXED passes over,
  in ascending order: C (contradicted) subjects 100..105 taught
  O2(k); K (kept/agreed) subjects 106..109 taught O1(k); N (novel)
  subjects 120..(119+N_n) taught O1(k). U (untouched) subjects
  110..115 are never taught in phase 2.
- Retention probe: query all 16+N_n subjects. Score C (100..105) vs
  O2, K (106..109) vs O1, U (110..115) vs O1, N presence
  (120..119+N_n). FORGET = subjects among C+K+U answering neither
  their phase-1-correct nor (for C) their phase-2-correct obj
  (absent -> -1 counts as forgotten).

Pressure points (frozen; CAP=20 fixed, total distinct = 16+N_n):

- P2: N_n = 24, N = 120..143, total 40 subjects, ratio 40/20 = 2.0x.
- P3: N_n = 44, N = 120..163, total 60 subjects, ratio 60/20 = 3.0x.
- P5: N_n = 84, N = 120..203, total 100 subjects, ratio 100/20 = 5.0x.

Arms per pressure point (each on a FRESH learner): MAIN (D1+D2),
ABL (rules removed). One binary runs all six arms sequentially and
emits all lines; 3 runs must be byte-identical.

## 4. Frozen predictions (hand-derived by tracing the NT-PORT rules
##    with general N_n; two independent traces)

The NT-PORT hand-trace (PREREG Sections 4.1/4.2) generalizes with
N_n replacing 10. Phase 1 is identical at all points (no pressure):
TTC1 = 2, probe 16/16, nevict = 0. Phase 2, per pass, teaching order
C (6), K (4), N (N_n subjects s_1..s_{N_n}, s_i = 119+i):

MAIN (D1+D2). C subjects keep installation order 1..6 (oldest); K
7..10; U 11..16; every N subject gets a larger ins than all phase-1
subjects, so the D2 victim (max ins) is always an N subject; no
phase-1 subject is ever evicted, at any N_n. C subjects: ref=1
(pass 1), ref=2 (pass 2, no revise), ref=3 > sup=2 (pass 3, revise
in place to (O2,1,0); ins untouched, invisible to the comparator).
Pass 1: s_1..s_4 fill the 4 free slots; s_5..s_{N_n} revolving-door
evictions on the last slot: N_n-4 evictions. Pass 2: s_1..s_3 hits;
s_4..s_{N_n} restored via D1 (each restore evicts the current
newest): N_n-3 evictions. Pass 3: same as pass 2: N_n-3 evictions.
Total MAIN nevict = 3*N_n - 10 = (3*(N_n-4) pigeonhole lower bound
under FORGET=0) + 2 traced revolving-door overhead (passes 2 and 3:
the re-inserted s_4 evicts s_{N_n}, re-taught later in the same
pass). End state: C = (O2,1,0); K = (O1,5,0); U = (O1,2,0);
s_1..s_3 = (O1,3,0); s_{N_n} = (O1,2,0); s_4..s_{N_n-1} absent.

ABL (no D1, lowest-net). The NT2 mechanism replays with N_n novel
subjects: pass 1 victims slot-0 revolving (100, then s_5..s_{N_n-1}):
N_n-4 evictions; pass 2 (100-insert evicts s_{N_n}; 101..105 reach
net 0; s_5..s_9 evict them; s_10..s_{N_n} revolving door on slot 0):
N_n-3 evictions; pass 3 (100..105 inserts revolving on slot 0;
s_10..s_{N_n} revolving on slot 0): N_n-3 evictions. Total ABL
nevict = 3*N_n - 10, same count as MAIN, opposite victim set. End
state: C subjects all absent; K = (O1,5,0); U = (O1,2,0);
s_1..s_9 and s_{N_n} present.

Frozen numeric predictions per pressure point:

P2 (N_n=24):
- MAIN: ttc=2, probe1=16, nevict=62, RET c=6 k=4 u=6 npres=4
  forget=0. EVHIST (nonzero only): 123..142=3, 143=2; 100..115=0.
- ABL: ttc=2, probe1=16, nevict=62, RET c=0 k=4 u=6 npres=10
  forget=6. EVHIST: 100=3, 101..105=2, 124..128=1, 143=2,
  129..142=3.

P3 (N_n=44):
- MAIN: ttc=2, probe1=16, nevict=122, RET c=6 k=4 u=6 npres=4
  forget=0. EVHIST: 123..162=3, 163=2; 100..115=0.
- ABL: ttc=2, probe1=16, nevict=122, RET c=0 k=4 u=6 npres=10
  forget=6. EVHIST: 100=3, 101..105=2, 124..128=1, 163=2,
  129..162=3.

P5 (N_n=84):
- MAIN: ttc=2, probe1=16, nevict=242, RET c=6 k=4 u=6 npres=4
  forget=0. EVHIST: 123..202=3, 203=2; 100..115=0.
- ABL: ttc=2, probe1=16, nevict=242, RET c=0 k=4 u=6 npres=10
  forget=6. EVHIST: 100=3, 101..105=2, 124..128=1, 203=2,
  129..202=3.

### Predicted breaking point (frozen, directional)

The traced dynamics are scale-invariant in N_n: the tenure ordering
(C/K/U older than every N subject by construction) does not depend
on how many N subjects arrive, and the D1 restore path is
capacity-sufficient (104 checkpoint entries for at most 84 N
subjects). Directional prediction: NO break at 2x/3x/5x -- K1..K5
hold at all three pressure points (PORT-PASS-ALL). The predicted
breaking point lies beyond 5x, outside this battery. If K2 or K4
fails at a probed point instead, that point is the measured breaking
point and the histogram names the mechanism; a break would falsify
the scale-invariance argument above and is the highest-information
outcome of this battery.

## 5. Assembly, build, run (frozen)

- Single source file `nt_pressure_full.zag`: the NT-PORT source with
  only the frozen Section 2/3 changes (parameterized N range,
  104-entry checkpoint table, 104-bin histogram, 4096-byte arena,
  per-pressure-point arms and kill bars). Canonical helpers copied
  verbatim (z_alloc, get32, set32, o_app, o_i64, o_nl, o_flush).
- Build: `znc nt_pressure_full.zag -o nt_pressure_bin` under
  safebin-only PATH.
- Run `nt_pressure_bin` 3 times; outputs `nt_pressure_run1.txt`,
  `nt_pressure_run2.txt`, `nt_pressure_run3.txt`. Require
  byte-identical (cmp) and record sha256.
- Output lines (all numeric): per pressure point and arm: TTC1,
  probe1, nevict, retention (c/k/u/npres/forget), nonzero
  eviction-histogram bins, MAIN phase-1-eviction count (bins
  100..115, for K2), and per-point K1..K5 verdict bits plus a
  per-point verdict line.
- Compiler-defect workarounds (mandatory, from AGENTS.md): no
  `as *i32`+slice construction (get32/set32 only); dynamic output
  only via the single-buffer cursor helpers + one `_zag_raw_syscall`
  write (never `_zag_print`); no `!(A && B)` in while conditions
  (De Morgan); if-nesting at most 3 deep with hoisted call results;
  no `[]u8 as *u8` casts (thread `_zag_malloc as *u8`).

## 6. Frozen kill bars (per pressure point p; N_n(p) = 24/44/84)

- K1_p (learning intact under capacity; else VOID at p): ttc_main
  in 1..50 AND probe1_main = 16 AND ttc_abl in 1..50 AND
  probe1_abl = 16. Else VOID at p (capacity itself broke learning;
  redesign, do not reinterpret).
- K2_p (eviction minimal, no churn, victims confined to N):
  nevict_main == 3*N_n - 10 AND phev_main == 0 (zero evictions of
  phase-1 subjects 100..115 in MAIN, from the histogram).
- K3_p (uncontested retention survives): k_main = 4 AND u_main = 6.
- K4_p (revision survives pressure): c_main = 6 AND forget_main = 0.
- K5_p (discriminative validity): (c_abl = 0 AND forget_abl = 6)
  AND (u_abl = 6 AND nevict_abl = 3*N_n - 10). If the ABL signature
  matched MAIN's at p, the apparatus cannot distinguish fragility
  modes there -> INCONCLUSIVE at p, never PASS at p.

## 7. Verdict mapping (frozen)

Per pressure point: K1 fails -> VOID at p. K1 holds, K5 fails ->
INCONCLUSIVE at p. K2 fails (K1, K5 hold) -> FAIL-K2 at p. K3 or
K4 fails (K1, K2, K5 hold) -> FAIL-RETENTION at p. K1..K5 all hold
-> PORT-PASS at p.

Overall: PORT-PASS at P2, P3, and P5 -> **PORT-PASS-ALL**: D1+D2
survives to 5x with the NT1 selective-retention pattern intact; the
breaking point lies beyond the probed envelope. Any FAIL at a point
-> the lowest FAIL pressure point is the measured breaking point;
report the failed bars with the histogram-derived mechanism (K2-fail
= churn escaped the N set or exceeded the traced minimum; K4-fail =
revision preempted / contradicted subjects forgotten under higher
pressure).

## 8. Honest boundaries (pre-declared)

- Same skeleton as NT-PORT, not a redesign; the port boundary from
  NT-PORT PREREG Section 1.1 stands (contlearn2 schema machinery and
  H-CONTLIFE-1 hash-table memory remain unported).
- Subjects are memorized (subj,rel)->obj associations; no L2/L3
  claim. The experiment measures retention/revision/eviction
  dynamics only.
- Three capacity points (2x/3x/5x); single contradiction magnitude;
  graded contradiction out of scope.
- The eviction histogram is measurement-only; the checkpoint table
  holds only the learner's own prior evidence.
- Whether LIFO's tenure principle holds when novel subjects are NOT
  re-taught every pass remains the preregistered open boundary
  (NT-PORT honest boundaries); it is NOT tested here and is the
  recommended next probe.

## 9. Amendment record (transparent; committed before implementation)

(none yet)
