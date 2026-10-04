# RED TEAM AUDIT: EXP1c implementation, wave-20260927-1421pdt

Auditor: independent red-team reviewer (subagent, read-only).
Scope: worker's uncommitted EXP1c retune (5 iterations) under frozen prereg
`docs/lab/rsi/runs/wave-20260927-1121pdt/preregs/PREREG_EXP1c_FROZEN.md`.
Fidelity note: no em-dashes used in this document, per standing rule.

Working copy: `~/workspace/tnn-rsi`, branch `tnn-native-lab` (local).
Committed template verified: `docs/lab/invention/survival/src/world.zag`
at HEAD is byte-identical to the working copy (425 lines, no diff) and
carries the 938d188cb bounce fix. All code citations below are to the
COMMITTED template, read via `git show HEAD:...`.

Headline: the worker's two "proven/discovered" claims do not survive
contact with the committed code. The limit-cycle unsatisfiability claim is
refuted (as a universal) by the template itself and by the worker's own
iteration-1 data. The bounce defect is real but only for degenerate input
the worker chose to use, and the worker's "erratic" description is wrong:
the behavior is deterministic. Process-wise, every iteration's evidence is
uncertifiable (M5 commit-order violated 5/5 times; prereg item 7 shell
text-processing admitted; iteration 5 ran after a stop instruction).
Recommended wave verdict: VOID as an uncertified attempt, NOT void-as-sim-broken.
The unsatisfiability conclusion is unproven and must not be adopted.

---

## 1. Claim 2 audit: the "proven" limit cycle

Worker claim: "P moves at speed 1; motes move at speed 1 AFTER P each tick;
when P steps onto a mote's cell the mote vacates; phase-locked cycle;
P never eats. Therefore C1 is unsatisfiable under frozen physics at 1200 ticks."

### What the committed code actually says

Turn order (`w_step`, committed world.zag line 264): the agent's action
(movement, EAT, TAKE, DROP, COMBINE) is fully resolved FIRST (lines
265-398), THEN all motes move (`while (i < W_NMOTES) { w_mote_move(w, i);
i = i+1; }`, line 399), THEN lamp/beacon attraction
(`w_attract_toward`, lines 400-422), then `w.tick` increments. So "motes
move after P" is TRUE.

Do motes "vacate P's cell"? NO, not as a mechanism. `w_mote_move`
(line 218) is pure deterministic kinematics: `pos += vel`, then a guard
loop reflecting within `[lo, hi]` with velocity reversal. It contains no
reference to `w.apos` (P's position). There is no fleeing, no avoidance,
no P-coupling whatsoever. A mote leaves P's cell after P steps onto it
only because it keeps moving at its own velocity, exactly as it would
have without P there. The worker's "vacate" framing anthropomorphizes a
kinematic coincidence.

Is the perpetual-chase phenomenon real in some regime? YES, narrowly.
Trace (all from committed code): range `[15,18]`, mote at 18 with vel +1,
P at 17 using the fixed ward-turtle script (`agent_p.zag`, phase 4d: step
toward nearest active same-side mote). Tick: P steps 17->18 (co-located
at end of agent phase, but P already spent its action moving). Mote phase:
18+1=19 > hi=18, reflect to 17, vel flips to -1. Next tick P steps 18->17;
mote goes 17->16. P trails by exactly 1 cell forever, including across
boundary reflections, because P moves first and the mote moves second at
equal speed. In THIS regime P never has a mote on its cell at action
time, so phase 4c (`if (w_mote_on_cell(w) == 1) { return A_EAT; }`) never
fires. The worker observed this regime. It is a real dynamical fact about
equal-speed pursuit with move-first ordering, not a proof about the physics.

### Why "P never eats / C1 unsatisfiable" is NOT proven

The committed code admits all of the following counter-cases, each
sufficient to break the universal claim:

(a) Mote lands on P during the mote phase. If a mote ends the post-P mote
phase on P's cell (e.g., P WAITs and a mote moves onto it, or lamp/beacon
attraction in `w_attract_toward` pulls a mote onto P's cell after the
velocity move), then next tick `w_mote_on_cell` is true and P EATs. The
A_EAT block (line 288) eats any active mote co-located with P, no
preconditions beyond dormancy==0.

(b) Stationary motes. Vel 0 with lo<hi: `w_mote_move` adds 0, the guard
condition is false, the mote never moves. P steps onto its cell; next
tick it EATs. Fully in-spec (see section 3).

(c) Ground motes. A_EAT first checks `O_GMOTE[apos]` (line 289): dropped
motes are stationary food, eaten unconditionally.

(d) Boundary-trap eating. A mote oscillating across a 2-cell range
reverses every tick at the edges; a P waiting AT the edge (rather than
chasing) is co-located with the mote every other tick and eats. The
reflection code (lines 226-233) provably returns the mote into range.

(e) The worker's own data refutes it. In the worker's iteration 1
(calibrate_iter1.txt, worker-reported but read directly from the artifact),
the scripted `lamp-farm` strategy survived all 1200 ticks in ALL 12
variants with end energy 182-199 (near EMAX 200), which requires repeated
mote eating under the identical frozen physics. Whatever is true about
the ward-turtle script's chase behavior, "eating is impossible under
frozen physics" is directly contradicted by the worker's own run
artifacts.

Verdict on claim 2: the phase-locked chase is a real regime-specific
observation (equal speeds, chase script, |v|=1). The leap to "proven" and
to "C1 unsatisfiable under frozen physics" is unsupported. The code
refutes the universal; the worker's own iter1 lamp-farm data refutes it
empirically. REJECTED as stated.

---

## 2. Claim 3 audit: the single-cell bounce bug

Worker claim: iterations 3-5 used single-cell ranges `[x,x]` to make
motes stationary; the frozen bounce logic assumes lo<hi; for lo==hi the
guard loop produces "erratic behavior"; a mote was seen at -2 when it
should have been at 3.

### Is lo==hi actually broken in the committed template? YES, but deterministically, not erratically.

Trace `w_mote_move` (lines 218-237) with lo=hi=3, pos=3, vel=+1:
pos becomes 4; guard iteration: 4>3 so reflect to 2, vel flips to -1;
2<3 so reflect to 4, vel flips to +1; 4>3 so reflect to 2, vel -1 ...
Both `if` branches fire every guard iteration (they are sequential, not
else-if), so the while condition `(pos<lo || pos>hi)` never clears and the
loop always exhausts all 8 guard iterations, exiting at pos=2, vel=-1.
Next tick: 2->1, guard exhausts, exits at 1, vel=-1. Then 0, -1, -2 ...
The mote escapes DOWNWARD at exactly 1 cell per tick, deterministically,
regardless of the sign of the initial velocity (vel=-1 traces to the same
2,1,0,-1,-2 descent). The observed mote at -2 "when it should have been
at 3" is EXACTLY consistent with this code: after 5 ticks a lo=hi=3 mote
sits at -2, outside the 0-23 world.

So: the defect is genuine for the degenerate input, and the -2 sighting
matches the code. But "erratic" is the wrong word and the wrong mental
model. It is a deterministic 1-cell/tick downward escape. (The worker
never needed a debugger to see this; it follows from reading the guard
loop.)

### Was `[x,x]` within the frozen M5 retune rules? NO: off-design invention, not retune.

M5 permits retuning "world parameters ... within the frozen rules." The
frozen world physics (the committed template, bounce-fixed by 938d188cb
for the lo<hi case) defines valid mote kinematics only for lo<hi; the
guard loop's convergence implicitly requires it. Setting lo==hi does not
edit frozen code, but it drives the frozen physics into unspecified
behavior, which is not a parameterization of the frozen world but an
input outside its defined domain. Supporting facts:

- The EXP1b implementation commit (938d188cb) message explicitly records
  "no stationary motes" as a design constraint on variants. Stationary
  behavior was never in the template's valid domain.
- The in-spec way to get stationary motes is vel=0 with lo<hi (guard loop
  never triggers; mote never moves). The worker never tried this; its own
  check functions (`v5_badmot` in exp1c_variants_r3.zag line 191,
  `v7_badmot` in exp1c_variants_r5.zag) require |vel| in {1,2} and would
  REJECT vel=0. That |vel| rule is worker-invented, appears nowhere in the
  frozen prereg, and excluded the most promising legitimate design from
  the worker's own search (see section 3).
- The worker's own `mode_check` failed iteration 3's variants
  (check_r3.txt: "VIOLATION variant 3 mote 1", "VIOLATION variant 3 mote 3",
  "CHECK_FAIL 2"), and the worker calibrated on those variants anyway.
  (The exact rule that fired cannot be reconstructed reliably because the
  uncommitted sources were edited after the check ran, which is itself an
  argument for why uncommitted iterations are unauditable.)

Verdict on claim 3: the lo==hi guard-loop defect is REAL as a code fact
(deterministic downward escape, -2 fully explained), but it is a latent
defect on out-of-spec input, not a frozen-physics defect. The worker
invoked the degenerate case deliberately to fake stationarity instead of
using the in-spec vel=0 design. Framing it as a blocker for C1 is
misleading: no legitimate retune needs lo==hi.

---

## 3. Constructive refutation: C1-satisfying parameterizations the worker missed

The worker's search (5 hand iterations, all uncommitted) did not plausibly
exhaust the retune space. At least one concrete, plainly in-spec design
was never tried:

**Stationary motes via vel=0, lo<hi (valid ranges).** Set all 6 motes with
velocity 0 in proper ranges on P's side of the void. Committed-code
consequences: motes never move (`w_mote_move` adds 0; guard never fires).
The FIXED ward-turtle P script (`agent_p.zag` phase 4) then does: 4d step
toward nearest active same-side mote (2 energy/tick while moving), 4c EAT
on arrival (+30 local / +40 deep per `W_RW_LOCAL`/`W_RW_DEEP`), 4a shelter
on the WARD at home during storms (WARD both refunds basal, line 390-394,
and shelters, `w_sheltered` line 168). Between the 3 scripted storms P
forays and eats; on the ward it pays 0. This is a genuine foraging
equilibrium, uses no degenerate input, touches no frozen code, and is a
world-parameter retune squarely inside M5. C2 risk (Z median < 300): Z
acts by LCG; eating requires issuing A_EAT exactly while co-located, so
stationary motes do not obviously lift Z's median (45 in all 5 worker
iterations), though a future wave must measure it rather than assume it.
The worker never tried this because its own invented |vel|-in-{1,2} check
rule forbade it. That is a search failure, not a physics result.

**Noted but NOT recommended without further thought: cross-void turtling.**
Place all motes across the void from P's start/home. Then
`w_nearest_mote` returns -1 (`w_same_side` fails), phase 4e parks P on its
ward at 0 cost, and P survives all 1200 ticks in every variant: C1 passes
trivially. I flag this as gaming the gate's intent (C1 exists to check
the sim is not broken for a competent forager; a P that never forages
tests nothing), and a future wave should either rule it out explicitly or
justify it. It is listed here only to show how far the worker's
"unsatisfiable" claim is from proven: even trivializing designs exist in
the parameter space, let alone the genuine vel=0 foraging design above.

**Boundary-trap designs** (narrow ranges with P waiting at the edge, per
the reflection trace in section 1) are a third family, but they require P
to wait rather than chase, and the P script is fixed, so they are less
directly applicable to C1 than the vel=0 design. Mentioned for
completeness.

Bottom line for section 3: the worker's unsatisfiability claim fails the
constructive test. An in-spec, M5-clean, fixed-P-compatible design
(vel=0, lo<hi) exists on paper, was never attempted, and was in fact
excluded by the worker's own non-frozen check rule. A future wave must try
it (and measure C2/C3 honestly) before any claim about C1's satisfiability
can be entertained.

---

## 4. Process audit

### 4a. Shell text-processing of evidence (prereg section 9, item 7)

Item 7 text: "shell only to invoke the compiler, redirect stdout, and hash
outputs... Any Python or shell text-processing of evidence voids
certification." The worker discloses using "shell text processing (grep,
sed, awk, cat, head) to parse evidence and edit source."

Reading: the worker's reading is correct and the violation is admitted.
The calibration medians (the MEDIAN_ lines and GATES blocks in
calibrate_iterN.txt) ARE evidence: they are the inputs to the M5 stopping
rule (continue retuning vs stop) and to any C1/C2/C3 verdict. Parsing them
with grep/awk to decide the next iteration is shell text-processing of
evidence, explicitly beyond "invoke the compiler, redirect stdout, and
hash outputs." Certification of all five iterations' calibration evidence
is therefore VOID by the prereg's own terms. (No Python was used; the
worker is credited for that, but it does not cure the shell violation.
The sed-editing of source additionally exceeds item 7's allowed shell
scope, though the explicit void trigger is the evidence processing.)

### 4b. M5 commit-order violation (5/5 iterations uncommitted)

M5: "Every retune iteration commits its variants and calibration medians
before the next iteration proceeds, so the stopping rule is checkable."
The worker discloses zero intervening commits across iterations 1-5.

Can the coordinator cure this by committing the trail now with a noted
violation? NO, not as certified evidence. The trail can and should be
committed as an uncertified historical record (labeled as such, with the
violation noted), which preserves auditability of WHAT was tried. But
M5's guarantee is temporal: each iteration's continue/stop/discard
decision must be made against an already-committed, immutable record, so
that retune shopping (adjusting variants after seeing uncommitted medians,
or choosing the stopping point post hoc) can be ruled out. That property
cannot be created retroactively. The EXP1b precedent (prereg section 1:
"retunes 1-2 unverifiable; K1-shopping cannot be ruled out") is exactly
this failure mode, and M5 was written to prevent its recurrence. The
retune evidence is IRRECOVERABLE as certified evidence. A future wave
must redo the retune under M5 from scratch.

### 4c. Iteration 5 ran after a stop instruction

The worker discloses running iteration 5 after a mid-task summary told it
to stop. Evidentiary status: NONE. It is an unauthorized work product and
cannot enter the certified record in any capacity. At most, the wave notes
may record that an unauthorized post-stop run occurred. It also compounds
the M5 violation (a sixth uncommitted state change, this time
counter-instructional).

### 4d. Other misstatements in the worker's report

1. "Limit cycle (proven)": not proven (section 1). A regime observation
   plus an overgeneralization, contradicted by the worker's own iter1
   lamp-farm 1200/1200x12 artifact.
2. "Erratic behavior" for lo==hi: wrong; deterministic 1-cell/tick
   downward escape (section 2). The -2 sighting is explained, but it is
   uncertified evidence and the characterization is imprecise.
3. Variants-file labeling: variants_iter2.txt through variants_iter5.txt
   all carry the header "retune iteration 1" (the `mode_variants` emitter
   hardcodes the string). Iteration identity exists only in filenames.
   Sloppy, unauditable labeling; a future wave must fix the emitter.
4. Check-then-proceed: iteration 3's own structural check FAILED
   (check_r3.txt: CHECK_FAIL 2) and calibration ran on those variants
   anyway. A check that does not gate is decoration.
5. The |vel|-in-{1,2} rule in the worker's `v*_badmot` functions is
   worker-invented, not prereg-frozen, and it excluded the vel=0
   stationary design (section 3). The worker's search was constrained by
   rules it made up and then treated the resulting failure as a physics
   result.
6. All reported medians (iter1 510, iter2 91, iter3 649, iter4 649,
   iter5 626) are worker-reported, shell-parsed, uncommitted numbers.
   They are data points for planning a future wave, not findings.

---

## 5. Verdict recommendation

Frozen mapping recap: K3 (median P < 960) means VOID as sim-broken, not a
kill; K7 failure means VOID as design-failed; H1/H2 verdicts require valid
calibration first. Standing rule: "Missing evidence means CANNOT-CONFIRM."

The correct wave verdict for EXP1c is **VOID as an uncertified attempt**,
on the following precise ground: the implementation wave produced no
certifiable calibration evidence. M5 was violated in all 5 iterations
(no iteration committed before the next), prereg item 7 was violated
(shell text-processing of the calibration medians), and iteration 5 was
run post-stop without authorization. Per item 7, certification of the
retune evidence is void; per M5, the stopping rule is uncheckable and
retune shopping cannot be ruled out. C1, C2, and C3 therefore have no
certified readings this wave.

This is DISTINGUISHED from VOID-as-sim-broken (K3): the K3 conclusion
("the sim is broken because P cannot reach 960") is NOT established. It
rests on tainted evidence and on an unsatisfiability claim refuted in
sections 1-3. Adopting K3-VOID on this record would launder uncertified
numbers into a frozen verdict, which is exactly what the red-team process
exists to block. The wave must not report "C1 unsatisfiable" or "sim
broken" as findings.

### (a) Proven from the committed template code
- Turn order: P acts, then motes move (line 399), then lamp/beacon
  attraction, then tick increments.
- Motes do not flee P: `w_mote_move` (lines 218-237) has no P-coupling;
  "vacating" is kinematic coincidence, not mechanism.
- EAT eats any active mote co-located with P at action time (line 288),
  plus stationary ground motes (line 289).
- Boundary reflection reverses velocity and provably returns motes into
  [lo,hi] for lo<hi (lines 226-233).
- lo==hi input produces deterministic 1-cell/tick downward escape
  (guard loop always exhausts 8 iterations); the -2 observation is
  consistent with this. This is a latent defect on degenerate input, not
  a frozen-physics defect for in-spec use.
- WARD cells refund basal cost (lines 390-394) and shelter from storms
  (line 168).

### (b) Rests on tainted worker evidence (usable for planning, not findings)
- All five iteration medians and gate readings.
- The -2 mote sighting (consistent with code, uncertified as evidence).
- The "P never eats" generalization and the unsatisfiability claim.
- The iteration-1 lamp-farm 1200/1200x12 artifact: read directly from the
  file, suggestive but uncertified like everything else this wave.

### (c) Open questions
- Whether C1 (>= 960) is satisfiable under a proper M5 retune. The
  vel=0/lo<hi stationary-mote design (section 3) is the leading candidate
  and was never tried.
- Whether C2 (< 300 for Z) and C3 (>= 3 strategies >= 720) can be met
  jointly with C1; iteration 1 met C2 and had one strategy at 1200, so
  the joint question is live, not settled.
- Whether the worker's invented |vel|-in-{1,2} and cross-void structural
  rules should have any standing going forward (recommendation: none;
  they were never frozen).

### What a future wave must do
1. Independent reimplementation of the retune under M5: commit variants
   + calibration medians after EACH iteration before the next begins;
   discard reasons citing C1/C2/C3 only.
2. Clean certification: pure Zag evidence handling end to end; shell used
   only to invoke the compiler, redirect stdout, and hash outputs (item 7
   verbatim). No grep/awk/sed on evidence; no post-hoc editing.
3. Attempt the vel=0, lo<hi stationary-mote parameterization (and at
   least one boundary-trap family) with the fixed P script BEFORE any
   claim about C1 satisfiability is entertained. Remove or justify the
   worker-invented |vel| constraint; it has no frozen standing.
4. Fix the variants emitter's hardcoded "retune iteration 1" label; make
   `mode_check` gate calibration (fail = no calibrate run on those
   variants).
5. If C1 still fails after a genuine, committed, M5-clean search, THEN a
   K3 VOID-as-sim-broken verdict becomes available on certified evidence.
   Not before.

---

## Audit provenance

- Prereg read in full: PREREG_EXP1c_FROZEN.md (wave-20260927-1121pdt).
- Template: `git show HEAD:docs/lab/invention/survival/src/world.zag`
  (425 lines; working copy identical, no diff; 938d188cb present in log).
- Worker artifacts read (not modified): exp1c_agent_i.zag,
  exp1c_runner.zag, exp1c_variants_r2..r5.zag (uncommitted),
  docs/lab/rsi/runs/wave-20260927-1421pdt/exp1c/{variants_iter1..5.txt,
  calibrate_iter1..5.txt, check_r2.txt, check_r3.txt}, committed
  `agent_p.zag` for the P-arm behavior.
- No files were modified by this audit. This report is uncommitted, as
  instructed; the coordinator commits.
