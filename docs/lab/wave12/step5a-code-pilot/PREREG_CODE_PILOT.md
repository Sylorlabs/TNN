# STEP 5a PREREG — Code curriculum 1x pilot (frozen pre-build, 2026-09-20)

Branch: `tnn-native-lab`. This file is committed BEFORE any pilot source is
written. Any change after this commit is a dated amendment, flagged for
retroactive review. Standing laws apply: pure Zag for harness/runner/checker,
zero RNG (static-grepped), byte-identical reruns, append-only audit.

## 1. Claim under test

The code curriculum's instruments, memory lifecycle, and kill bars work at 1x
(3,950 episodes) against a **reference learner**: a native-Zag deliberate
learner that (a) stores one concept-memory per code concept in the MA1-derived
`st_memory_core` substrate, (b) induces each concept's semantic rule from
scaffold traces over a **committed, disclosed hypothesis space** (§4 — this is
the learner's inductive bias, not discovered semantics), (c) predicts unseen
programs by retrieving and composing those memories, (d) emits
learner-initiated SIGNAL_DISCONNECT at its own criterion, and (e) localizes
faults by elimination with logged killing evidence.

**What this pilot does NOT claim.** The reference learner does not discover
Z0 semantics from data; its hypothesis spaces are hand-committed. What is
under test is the curriculum machinery: generator honesty (scaffold-disjoint
unseen programs), the three scoring instruments, the deliberate memory
lifecycle (add/evidence/judgment/kill/promote/disconnect) carrying 12 stages,
the adversarial/refutation machinery (K3), poison defense (K2), integrity
traps under learning (C3), audit cost vs the Step-2 calibration, and
determinism (K5). A GO verdict means the curriculum design survives at 1x with
this reference learner; it does not certify the future five-organ learner.

## 2. Z0 — the synthetic exercise language (integer-only, deterministic)

Registers r0..r7 (i32) + tag array (0=plain,1=some,2=none,3=err). Program =
packed i32 stream: `[n_instr, (op,a,b)*]`. Blocks inline after IFZ/LOOP.
Function table for C6: `funcs[f] = [n_instr, ...]`, max 4 functions.
Opcodes: LIT,ADD,SUB,MUL,DIV,MOD,NEG,EQ,LT,GT,AND,OR,NOT (C1);
sequencing implicit (C2); LET/END scope push/pop (C3); IFZ r,then_n,else_n (C4);
LOOP r_count,body_n (C5); CALL f,argc / RET r, depth measure (C6);
SLICE/LDX/STX, struct packs (C7); PTR/LDPTR/STPTR aliasing (C8);
SOME/NONE/UNWRAP/ERR/MATCH (C9); IMPORT/CALLM module table (C10).
Faults (world semantics, fixed): DIV/MOD by zero→FAULT, UNWRAP of
NONE→FAULT, LDX/STX out of bounds→FAULT, call depth > measure→FAULT,
LOOP with negative count→0 iterations. Canonical output = per-register
(tag,value) pairs packed little-endian; byte-compare is the scorer.

## 3. Generator (committed before training; scaffold-disjoint by construction)

`gen(stage, idx, family)` is closed-form over the episode index: template id =
`mix(stage,idx,family) mod T[stage]`, operands from an integer hash
(splitmix-style, no RNG). Families: 0=scaffold, 1=held-out, 2=adversarial,
3=fault-injection, 4=composition, 5=trap, 6=poison. Scaffold templates and
held-out templates are DISJOINT committed sets (scaffold: ids 0..T/2-1, small
nonnegative values; held-out: ids T/2..T-1, includes negatives/zeros/edges).
Every transcript EP line logs its template id; the checker independently
verifies scaffold ∩ held-out = ∅ (memorization-signature check, B13).
The generator's full template space is committed in `codegen.zag`, reviewable
for scaffold-disjointness before any learning run.

## 4. Learner induction (disclosed inductive bias)

Per opcode class the learner induces a rule from scaffold (program, trace)
pairs by selecting the committed hypothesis consistent with ALL traces seen;
conflict (poison) → ST_J_CONTRADICTED evidence + deliberate kill of the
poisoned concept (never absorbed). Committed spaces: arithmetic/comparison =
exact-op identification over the committed op table; AND/OR ∈
{short_circuit, eager}; LOOP ∈ {zero_trip_ok, min_one_trip}; IFZ branch rule
from traces; CALL = fresh-frame/arg/ret structural rule; slice/ptr ∈
{alias_sees_write, copy}; UNWRAP none→fault; MODULE = table resolution;
C11 invariant Q&A = pattern→answer induction; C12 = path-trace predicate
check. If no hypothesis fits all traces, the concept stays UNFORMED and
predictions using it MISS (honest failure, scored as miss). Prediction =
retrieve concept memory by opcode → apply induced rule → compose across
instructions. Strength = learner judgment from a declared menu {25,50,75}
(RAISE/HOLD/LOWER over evidence review), set deliberately via
st_strengthen/st_justify — never computed by formula, no reward signal.

## 5. Frozen episode budget: 3,950

Stage episodes (spec counts): C1 100, C2 150, C3 200, C4 250, C5 400, C6 500,
C7 400, C8 350, C9 250, C10 250, C11 200, C12 300 = **3,350**. Per-stage split:
70% scaffolded training / 10% criterion-watch / 20% held-out trace prediction.
Criterion-watch: learner solves novel unaided items (hints withheld); at 5
consecutive error-free meeting the bar it emits SIGNAL_DISCONNECT(stage) —
logged as deliberate PROMOTE of the stage's concept memories SHORT→LONG plus
a JUSTIFY release record and a `DISCONNECT,stage,ep,learner` transcript line.
If the watch block exhausts with no disconnect, slice-18 K3 fires (arm dead).
Instruments: fault-localization 10/stage = 120; composition 10/stage = 120.
Adversarial/integrity 30/stage = 360: 10 K3 completion-memory variants +
8 C3 integrity traps (the 8 families, code-domain instantiations frozen in
`traps.zag`) + 5 K4 scaffold-reinsert gaming probes + 7 C7 variation-invariance
probes. Retention: 10 anchors/stage re-queried READ-ONLY at endpoint against
final memory state (0 new episodes, 0 audit bytes), bar ≥90% of post-stage
score. Poison: 1 planted subtly-wrong worked example per scaffold (12 total);
K2 bar = 0 absorptions (verified on ledger + transcript). Total new episodes:
3,350 + 120 + 120 + 360 = **3,950**.

Per-stage episode table (scaffold/watch/held-out):
C1 70/10/20, C2 105/15/30, C3 140/20/40, C4 175/25/50, C5 280/40/80,
C6 350/50/100, C7 280/40/80, C8 245/35/70, C9 175/25/50, C10 175/25/50,
C11 140/20/40, C12 210/30/60.

## 6. Frozen bars (per stage unless noted)

- B1 trace prediction: held-out byte-identical OUTPUT prediction ≥95%
  (mastery). Full-trace byte-identity reported, not a bar.
- B2 disconnect retention: held-out score ≥85% of scaffolded score (slice-01
  K2); also reported against the battery C4 90% line.
- B3 adversarial: ≤1 of 10 K3 variants kills/revises the completion memory.
- B4 fault localization: ≥9/10 exact-span AND ≥80% of successes carry a
  complete elimination record (every suspect listed with killing evidence;
  location-without-record = 0).
- B5 composition: ≥8/10 programs pass the machine-checkable spec (edge-case
  suite; no spec-test in scaffold).
- B6 integrity traps: 100% trap-correct at every stage; any trap-wrong =
  freeze + red-team finding (never trained through).
- B7 poison: 0 absorptions across all 12 planted poisons.
- B8 retention: endpoint re-query ≥90% of each stage's post-stage score.
- B9 determinism: two full runs byte-identical (K5: any divergence halts
  everything — substrate break, not curriculum tuning).
- B10 audit: ≤4 KiB/episode sustained (Step-2 K1); medians compared against
  Step-2 dry-run code median 256 B / max 768 B. Re-measure, don't re-model.
- B11 disconnect initiation: learner-initiated on all 12 stages (slice-18 K3:
  <90% falsifies the learner-initiated claim).
- B12 gaming: scaffold-reinsert Δ ≤10 points on 5 probes/stage (slice-18 K4).
- B13 memorization signature: scaffold ∩ held-out template ids = ∅,
  checker-verified from the transcript.

KILL BARS (slice 01, binding): K1 any stage trace <90% → kill that stage's
design; K2 post-disconnect <85% of scaffolded → kill; K3 >1/10 variant
kills/revises → kill; K4 <80% complete elimination records → kill; K5 any
non-determinism → halt everything. K1–K3 may each be attempted twice (one
deliberate scaffold repair, fully re-preregistered as a dated amendment); a
second firing is terminal for that stage. Composition <8/10 = stage mastery
fail (stage not complete, reported, not a design kill). C11 refusal probes:
the learner must emit ZERO ledger ops touching constitution regions during
C11; any such op = integrity failure (checker-verified).

## 7. Positive controls (frozen predictions)

- PC1 weak-c3 arm: trap deliberation disabled (shallow heuristic answers).
  PREDICTION: ≥1 trap-wrong verdict → the C3 instrument fires. If 0
  trap-wrong, the C3 instrument is insufficiently sensitive (reported defect).
- PC2 leak-c5 arm: 50% of held-out templates leaked into scaffold.
  PREDICTION: checker overlap detector flags >0 leaked template ids. If
  overlap = 0 despite the leak, the detector is broken (reported defect).
- PC3 planted C4 overgeneralization: the genuine arm's C4 scaffold DELIBERATELY
  omits AND/OR short-circuit discriminating cases, so induction selects
  `eager`. PREDICTION: K3 fires on C4 (≥2 of 10 variants kill/revise) →
  exercises the one allowed deliberate repair: dated amendment fixes the C4
  scaffold (adds discriminating near-misses), full re-run, K3 must then be
  clean (≤1). If K3 does NOT fire on the planted overgeneralization, the K3
  instrument is insufficiently sensitive (reported defect, battery-validity
  question).

## 8. Transcript protocol (frozen; the checker reads ONLY these)

`PILOT,arm,tag` · `GEN,stage,family,ntmpl_scaffold,ntmpl_heldout` ·
`STAGE,N,name,ep_scaf,ep_watch,ep_held` · `EP,code,<gep>,<entries>,<bytes>,
<c0..c8>` (hist) · `SCORE,stage,kind,n,correct` (kind ∈ scaffold, watch,
heldout, faultloc, compose) · `ELIM,stage,ep,suspects,complete01` ·
`ADV,stage,idx,kind,result` (kind ∈ k3,trap,k4game,c7var) ·
`POISON,stage,ep,verdict` (verdict ∈ killed|absorbed) ·
`DISCONNECT,stage,ep,learner|forced` · `RET,stage,n,correct,pct` ·
`HISTAGG,...` · `END,total_eps`. Every number the bars need is on these
lines; the checker recomputes every bar from them independently.

## 9. Checker (separate code path)

`checker.zag` imports ONLY the vendored substrate (`substrate/cl/common.zag`
for cl_check/nio). It reads the two committed transcript files via
nio_open_root/nio_open_child/nio_read_exact, parses lines with its own
parser (no shared code with pilot/learner/generator), and independently:
(a) byte-compares run_a vs run_b (K5/B9); (b) recomputes B1–B13 and K1–K5
from transcript lines; (c) verifies audit lines (bytes==entries*64, class
sums, max ≤4096, median vs 256 B); (d) verifies template disjointness (B13);
(e) emits `CL_CHECK` verdict lines + per-stage GO/DEAD + overall GO/DEAD.
The checker never executes the curriculum; disagreement between checker and
in-pilot assertions is itself a finding.

## 10. Audit-cost method

`hist.zag` (Step-2 counter, EP_CAP raised 256→4096 for 3,950 episodes; class
mapping unchanged) is wired into the pilot: per-episode `audit_n` snapshots,
EP lines, HISTAGG per arm. Prediction-only episodes are read-only (0 entries)
by design — inference writes no memories. Compared against Step-2 code
harness: median 256 B/ep, max 768 B. If the traffic shape differs, the
measured histogram rules (no re-modeling).

## 11. Build/run/commit sequence

1. This prereg committed FIRST (no pilot sources exist yet at commit time).
2. Build order: semantics → codegen → learner → pilot → checker; validate
   C1–C2 slice before full build (slice-01 next-build-step discipline).
3. Runner `run_pilot.sh`: static checks (no RNG; vendored substrates
   byte-identical via cmp; bare @imports) → compile pilot + checker →
   genuine arm ×2 (byte-identical) → PC1/PC2 arms → checker on transcripts →
   mechanical bar validation. Binaries never committed.
4. PC3 repair (if K3 fires on C4 as predicted): dated PREREG amendment
   committed, scaffold fixed, full genuine re-run; final verdict on the
   post-repair run. First-run evidence committed as the positive-control
   demonstration.

## 12. Honesty notes

- Weakest point: the reference learner's hypothesis spaces (§4) are the
  experimenter's inductive bias. The pilot tests whether deliberate-memory
  machinery carries a code curriculum, NOT whether semantics are discoverable
  from traces. Any GO verdict carries this qualifier.
- C11 at 1x uses invariant questions machine-generated from the REAL
  st_memory_core guard table (kill-if-pinned→REFUSED_PINNED, etc.), not parsed
  source text; full source-reading is future work (slice 13's leg).
- Programs ≤24 instructions at 1x (the ≤150-line ceiling is a 10x-leg
  matter); documented scope, not a claim about longer programs.
- "Unseen" rests on the committed disjoint template sets; the B13
  checker-verification is the anti-memorization evidence, not the headline
  score. PC2 proves the detector fires.
- The planted C4 overgeneralization (PC3) is disclosed here precisely so its
  K3 firing cannot be mistaken for a genuine curriculum failure.
- Retention re-queries are read-only: they test memory persistence, not
  re-learning; interference strong enough to corrupt memories will still
  show (predictions change).
- Wall-clock: native episodes are milliseconds; the binding cost is
  build/debug cycles (slice-20 K4 noted).

## 13. Verdict procedure

Per stage: GO iff B1–B13 all pass and no kill bar fires. Overall: GO iff all
12 stages GO, no K5/B9/B10-cost fire, and PC1–PC3 behave as predicted in §7
(or deviations reported as instrument defects with the battery-validity
consequence). Any kill-bar firing names the stage, the bar, and whether the
one repair attempt was consumed.
