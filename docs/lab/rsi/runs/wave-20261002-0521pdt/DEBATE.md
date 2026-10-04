# DEBATE TRANSCRIPT: wave-20261002-0521pdt verdict slate

Lane: mandatory debate group. Working copy ~/workspace/tnn-rsi,
branch tnn-native-lab. All commits local only, never pushed.
Role: docs/governance lane. No new experiments were run; this
transcript judges the lane evidence committed this wave against the
frozen bars and the standing governance rules.

## STEP 0 (mandatory, recorded first)

At session start this worker ran
docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh,
then exported PATH="$HOME/safebin". Result: SAFEBIN-READY,
/home/hatch/safebin, 36 tools linked, pinned znc OK. Verification:
`which python3` returns nothing (exit 1); `which python` returns
nothing. No Python was invoked anywhere in this lane: the debate
group read lane evidence only (docs/governance lane, read-only
toward all experiment lanes).

## SKEPTIC'S PROVENANCE PROBE (verbatim, in the skeptic's voice)

Before any adoption is argued, the skeptic demands the provenance
accounting, verbatim:

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

The skeptic's elaboration: every verdict below must say which
binaries, worlds, keys, and sources are new this wave versus
inherited from 0221pdt or earlier, because inherited artifacts
carry inherited assumptions (tuned thresholds, generator families,
substrate behaviors) that a fresh verdict can silently adopt. Where
a lane rebuilt byte-identical binaries from committed sources
(COMP A/B/C/C0, ARENA v6_base, TRADES INQ cross-check), the
provenance is clean and the skeptic stands down. Where a lane
carried forward a frozen substrate (HPI H5R3 prereg on byte-identical
H5R2; CONTLEARN on the continuing-learner core), the inheritance is
declared in the verdict and the claim is bounded to it. Where the
provenance has gaps (COMP D base-SHA string matches no computable
prefix; A line range off by one), the skeptic insists the gaps stay
in the record attached to the verdict, which the COMP lane did.

---

## 1. COMP comparative adversarial: BUILD-PASS (per-family verdicts)

Coordinator verdict: battery BUILD-PASS. D `satisfy` BUILD-PASS,
adopted as the single composition operation; C BUILD-PASS but
strictly dominated; B PARTIAL (causality unproven); A INCOMPLETE
(unadopted); C0 control PASS. KB2 subsumption HOLD all axes; KB3
strict extension HOLD (D passes COMP5/NOSUP, genuine C fails);
KB4 no-COMPOSE_MODE HOLD; KB5 architecture HOLD (0 modes/bridges/
handlers, 299 cognition lines); KB6 PARTIAL (B-ABL confounded);
KB7 COLLAPSE-SUPPORTED with caveats. Criterion 0: no mechanism
meets all four clauses (C0-C fails for all; C0-D unmeasured). No L3.

ADVOCATE: The subsumption evidence is the four genuinely isolating
tests, COMP3, COMP5, D4, NOSUP, the only tests the red team certifies
as mechanism-isolating rather than trial-path artifacts. On those,
D scores 4/4 with mechanism attribution (SAT-SEGS/SAT-FIX markers),
C scores 2/4, B scores 0/4. KB7 holds in its measured form: no
completed test exists where any mechanism passes and D fails, and D
strictly extends C where C is structurally incapable (5-segment
COMP5, unsupervised NOSUP). KB4 holds (zero "compose" in patch_d;
C0 answers -2), KB5 holds (299 cognition lines, zero new modes,
bridges, handlers, semantic cases, or opcodes; ISA unchanged). The
owner ruling already forbids integrating three engines; adopting
D's `satisfy` as the working single operation is that ruling
implemented, not a new claim. The caveats are all recorded, none
patched over.

SKEPTIC: The collapse was engineered toward the thesis; Amendment
A1's rationale is explicit, so COLLAPSE-SUPPORTED is a verified
construction, not a discovered identity. The trial-path confound
shrinks the field D subsumes: B's PART/D3H passes and C's
PART/ADVA/SINGLE passes are trial artifacts, and the B-ABL control
is BUILD-FAIL, so B's causality is unproven and D may be subsuming
nothing real on the B axis. A is INCOMPLETE (bin_a stalled 70+
minutes in D4's goal query, O(MAPs^2 x paths^2) against 40
distractors), so the ADV-A exhaustive-grounding axis is untested
and KB1 is unverifiable for A: the coverage claim has a hole. C0-C
fails for every mechanism (no independent-adversary family) and
C0-D is unmeasured, so nothing here approaches L3. Adopting D as
THE single composition operation on this evidence generalizes from
a battery whose hardest axis was never completed.

JUDGE: UPHOLD. The adoption is narrowly scoped and matches the
per-family verdicts exactly: keep D's `satisfy` as the working
single operation for continuing-learner work, keep A/B/C sources
and binaries as frozen baselines, integrate nothing. The
engineered-collapse caveat limits the claim to a verified
construction; it does not falsify it, because the isolating tests
are mechanism-attributed for D (4/4) while C and B fail them. The
trial-path confound cuts against B/C credit, not D. A's
incompleteness is recorded as a hole (ADV-A untested, results
unadopted), not papered over. The collapse thesis is adopted only
in its measured form: D covers every genuine measured win of
A/B/C. No L3 is claimed or adopted. UPHELD.

---

## 2. DDES steps 7+8: BUILD-PASS

Coordinator verdict: step 7 OOD BUILD-PASS (6 fresh worlds match
frozen predictions exactly on decision lines, 3/3 byte-identical,
zero SILENT-WRONG); step 8 ablation BUILD-PASS (C1 clamp
load-bearing, C2 wait-counts load-bearing, C3 earliest-frontier
partially load-bearing; no decorative component). Steps 1-8 all
BUILD-PASS. Bounded L2 ceiling; three binding caveats intact.

ADVOCATE: Step 7's numbers are exact: 6/6 decision-line rows match
the prereg prediction table, sha f7a7ec52... 3/3 byte-identical,
zero SILENT-WRONG across 12 cells, and the negative control O6
fails loudly exactly as predicted rather than silently. Step 8's
ablation is decisive on the decision lines: removing C1 flips O3
CORRECT to SILENT-WRONG; fixed w=2 flips O1/O2/O4/O5 to LOUD-FAIL;
only O3's plan changes without C3. The three binding citation
caveats are restated verbatim and untouched; the ceiling claimed is
bounded L2 with persistence, nothing more.

SKEPTIC: The OOD set was worker-designed, not adversary-designed.
The same worker who built the t*-derived guidance chose the six
worlds, so the worlds cannot exceed the worker's imagination; step
7 may be measuring self-consistency against a friendly distribution
(two-hop chains, t*=12, decoys, competing frontiers, fan-in are the
shapes the mechanism was built for). The genuine guard against
this is step 10 (independent red team) and step 11 (governance
audit), and both remain open. A BUILD-PASS on step 7 without them
is a progress marker, not a generality result.

JUDGE: UPHOLD. The frozen prediction rows preceded the runs and
matched exactly; the honesty markers are present (O6's predicted
loud failure, zero silent-wrong, binding caveats intact). The claim
is bounded L2, not generality, and the worker-designed-worlds
concern is precisely why steps 10 and 11 exist and remain open.
The frozen bars 7a/7b/7c all HOLD as written. UPHELD.

---

## 3. TRADES WIDE-EIG-10: BUILD-PASS

Coordinator verdict: BUILD-PASS on all 10 frozen bars. WIDE 8/8 x3
reps (24/24) vs SINGLE 5/8 (chance 1/6). Honest cost: structural
deliberation exactly 10.0x (30 vs 3 EIG searches), forward-sim
ratio 11.01x aggregate within frozen [8,12], wall-clock 4.77x.
Kept as L2 causal-inquiry infrastructure; gain is
ensemble-plus-pooling reliability, not EIG superiority
(pre-disclosed; F_CM also 8/8).

ADVOCATE: All ten frozen bars PASS, none moved. K1: 8/8 on all 3
reps. K2: 8-5=3. K3: 8>=8 non-inferiority, with the prereg-required
plain statement that EIG contributes nothing at 30 pooled
interventions. K4: structural 10.0x exact, aggregate sim ratio
11.01x inside the frozen [8,12] band, wall 4.77x disclosed. The
per-world ratio readings (8.92 to 15.96) are disclosed in the
record, not hidden. The bar as written used the aggregate, matching
the dev prototype's single 10.0x figure.

SKEPTIC: Four of eight per-world sim ratios exceed the frozen 12
cap: 14.50, 13.93, 13.96, 15.96, the last 33% over. The worker's own
disclosure says sims per search scale with hypothesis-set size,
which is world-dependent, so the aggregate averages away exactly
the cost variance the bar was meant to bound. Had K4 been written
per-world, it FAILS on half the battery. And the headline
capability gain is matched by F_CM at 8/8: what is adopted is an
expensive ensemble (11x sims, 10x deliberation) whose EIG component
is inert. "L2 causal-inquiry infrastructure" is a grand name for a
pooled ensemble.

JUDGE: UPHOLD. The frozen bar as written specified the aggregate,
and the aggregate 11.01x holds inside [8,12]. The per-world numbers
are in the record attached to the verdict by the worker's own
disclosure; the debate's job is to keep them there, and they are.
No bar was weakened retroactively, and the K3 non-overclaim (gain
from ensemble-plus-pooling, not EIG) is the honest scope of what is
adopted. The verdict names its ceiling: candidate mechanism, L2
infrastructure, no L3, no generality beyond the 3-variable chain
intervention domain. UPHELD.

---

## 4. F1-FOLLOWUP: FINDING CONFIRMED (with process incident)

Coordinator verdict: FINDING CONFIRMED (greedy-trial
seed-sensitivity is a constructor property; R=13/40, T=2 stable;
mechanism: depth-1 greedy argmin over seed-driven buffer; wrong law
is a trap with no unbuild). Filed, not patched. Process incident:
one exec without safebin PATH ran a no-op `python3 -c "print('no')"`
environment check; self-disclosed; no research computation, no
artifact depends on it. Coordinator ruling: incident recorded,
chain uncontaminated, finding stands. Referred to the debate group.

ADVOCATE: The finding's evidence is strong and independent of the
incident. R=13/40 (32.5%) overfit seeds with T=2 stable across
three batteries (pooled 22/104=21.2%); D_ops=9 structural
convergence paths; Cmax_ops 15/40. K-SS-TRIAL/OVERFIT/CONV/DET all
PASS on 40 seeds x 3 reps byte-identical; NC-HARNESS reproduces the
prior Part 2 phenomenon 6/6 byte-identically. The white-box
mechanism is in the raw op/operand lines (repeated feature-adds,
accumulator doubles, strictly decreasing err), and the 13 overfits
fall into 4 overfit-only structural groups. The invocation printed
"no" and its output was used for nothing; every artifact (prereg,
methodology, fixtures, 40x3 runs, analysis) was produced under the
verified safebin PATH. Contamination is ruled out by positive
evidence, not by absence of evidence.

SKEPTIC: The worker toolchain guard is automatic and exceptionless:
"If a forbidden executable is invoked, that worker's current
scientific wave is automatically PROCESS-FAIL and must be cleanly
re-frozen if its result matters." There is no de-minimis clause and
no self-disclosure exception. The coordinator substituted judgment
for a bright-line rule, and bright lines exist because twelve
prior incidents proved case-by-case adjudication fails. Excusing a
"no-op, self-disclosed" check writes the exception the guard
refused to write, and the next worker will excuse a "no-op"
analysis script. The 1000-MAP scaling wave went PROCESS-FAIL this
same wave for a self-disclosed python3 invocation; its measurements
stay exploratory pending clean reproduction. Identical treatment is
required: the guard cannot mean one thing for one lane and another
for this one.

JUDGE: OVERTURN. The coordinator's ruling ("incident recorded,
chain uncontaminated, finding stands") is overturned on the
adoption. Cited evidence: the mandatory worker toolchain guard
(AGENTS.md), which makes PROCESS-FAIL automatic on any forbidden
executable invocation during the lane's scientific wave, with clean
re-freeze required when the result matters; and REDTEAM_SELF.md
Attack 6, which admits the invocation. The contamination analysis
is good science and stays in the record, but the guard is
governance, and governance overrides. The F1 lane is declared
PROCESS-FAIL; the sealed measurement (R=13/40, T=2, D_ops=9,
Cmax_ops 15/40, NC-HARNESS 6/6) stands as exploratory evidence
only, adoptable only after a clean pure-Zag re-freeze and re-run.
The debate group will not create a de-minimis exception by
precedent. OVERTURNED.

---

## 5. CONTLEARN CLH2: REBIND-DEMONSTRATED, BUILD-PASS

Coordinator verdict: BUILD-PASS. 12/12 rebind into 148-event-old
never-re-taught chains; NOPHASE discriminator 12/12. New red-team
note: rebind is frozen-core behavior (proposal gate contributes
ordering provenance only); all six CONTLEARN3 binding caveats still
bind.

ADVOCATE: The battery is the evidence: 166 events, 6 novel 2-hop
chain integrations, 96-fact memory pressure, an unrelated
conflict-plus-correction episode, a second chain family, then 12
new rebind problems at new entry points into the old chains, all
3/3 byte-identical, no reset, no task label, no recompilation.
CP-R1 12/12 with answers served by new MAPs DEP-citing the
never-re-taught phase-A facts; CP-R2/R3/R4 all PASS; and the
NOPHASE discriminator returns 12/12 answers==1 on identical
machinery and identical problems with the structure absent. That
control is exactly what structure-dependence claims require. The
red-team note narrows attribution (gate gives ordering provenance,
CP-R0 24/24), it does not erase the measured capability.

SKEPTIC: CONTROL reproduces TREAT on every rebind bar (CP-R7, no
anomaly): the proposal gate, the mechanism under test, contributes
nothing to rebind. The finding is that frozen-core machinery does
what it does. Six binding caveats still bind: fixed template
proposal content, event-triggered initiation, no learner agency,
refusal branch unexercised for the third consecutive lane,
no L3/generality, machinery-enabled citation. Head-family value
selection is allocation-order-determined. What is adopted beyond
"the battery ran and the core behaved"?

JUDGE: UPHOLD. The claim under test was the continuing learner's
delayed-rebind capability under the binding caveats, not gate
authorship of rebind. CP-R1 12/12 (DEP-citing phase-A facts) plus
the NOPHASE 12/12 discriminator (same machinery, structure absent,
answers differ exactly as predicted) is genuine evidence of
structure-caused delayed rebind, and the tail family (unique path)
carries it cleanly. The red-team note is a scope tightening
recorded inside the verdict, not a kill; the six caveats travel
with the verdict as binding. UPHELD.

---

## 6. ARENA C9: CAUSAL-PASS (0.000 to 1.000)

Coordinator verdict: CAUSAL-PASS on the 0221pdt causal contestant
(two-stage interventional protocol, HI=0.75, integer arithmetic,
zero chain literals). 57/68=0.838 (3/3 runs), C9 3/3, zero
regressions vs v6 (54/68=0.794; only the C9 line changed), 3/3
byte-identical, ablation per-capability identical to v6 (C9 to 0/3),
order-swap invariant. +66 cognition lines; 0 modes/bridges/
handlers. L1/L2, no L3. C9 worldgen D5 fix GEN-PASS (fixrun2
supersedes fixrun1); C15 ABSTAIN-FAIL with scope bounding; C8/C12
TRANSFER-PASS (same generator family).

ADVOCATE: The protocol was frozen in 0221pdt (fdaa5c0a4) before
fixrun2 existed, so nothing about the eval substrate could have
shaped it. 57/68 vs v6's 54/68 with only the C9 line changed is a
clean delta; C9 moves 0.000 to 1.000 with 3/3 byte-identical runs.
Gaming is blocked structurally: K5 order-swap invariance holds, the
reply is built from variable indices and falls back to UNKNOWN, and
there is no path from question format to a correct answer except
through the statistics. HI=0.75 comes from C9BAT's pre-registered
statistical basis with enormous margins (tracking fractions 36/40,
40/40). The protocol deviation was forced: fixrun1 is unscorable by
the frozen scorer (DIVERGENCE on C9 item27, independent confirmation
of D5) and the frozen scorer panics on 291-turn worlds (256-entry
buffers); arena_512 differs only in allocation sizes and was
cross-validated byte-identical on the 131-turn world. Kill bars
applied exactly as frozen.

SKEPTIC: The eval substrate is not the prereg's named substrate:
fixrun2 instead of fixrun1, arena_512 instead of the frozen scorer.
Disclosure is honest, but the bars were calibrated against the
named substrate, and a scorer swap plus a worldgen fix is a
material change however validated. HI=0.75 matches this generator
family's noise model (p=0.05): frozen or not, it is tuned to the
family. C9 3/3 is three items. "CAUSAL-PASS" and "0.000 to 1.000"
will be read as causal capability; the 1.000 is overclaimable the
moment it leaves this transcript.

JUDGE: UPHOLD, with the scope pinned to the transcript. The
deviation was forced by post-freeze discoveries, and both changes
were validated to equivalence (arena_512 byte-identical
cross-validation; fixrun2 same seed, battery path byte-identical).
The 1.000 is the C9 line (3 items x 3 runs), reported as 3/3, and
the verdict line is CAUSAL-PASS bounded to this frozen battery;
the multi-seed C9 battery is already queued, which is the correct
next step before any broader claim. +66 cognition lines, zero new
modes/bridges/handlers, no L3 claimed. UPHELD.
---

## 7. DEVANG5: BUILD-FAIL on K_ABL leg 1 (bar-miscalibration classification)

Coordinator verdict: BUILD-FAIL. Killing bar: K_ABL leg 1
(ablation 6/12 vs frozen <=5/12). Classified as
bar-miscalibration/test-design, not a mechanism defect; FINREG
mechanism kept (K_SEG 12/12, K_SEAL 14/20, K_DISC 6/6).

ADVOCATE: The verdict follows the bar: BUILD-FAIL stands, the bar
was not weakened, and the prereg's prediction is not retrofitted.
The miscalibration evidence is specific and falsifiable: the
<=5/12 threshold was copied from DEVANG4's prereg without
recalibrating for B-doubleprime's 3-char-heavy composition, where
fixed-width-3 chunking is accidentally correct on about half the
utterances (DEVANG4's B-prime words were longer; its ablation
scored 1/12). The mechanism's independent validation is intact:
K_DISC 6/6 vs the frozen devang4 binary's 2/6, the gap attributable
solely to the FINREG delta per the K_DELTA audit (119 diff lines,
46 code, under the 120 cap); learner 12/12 vs ablation 6/12 on
K_SEG; K_AUD PASS (statistics segmentation-dependent); K1 leg of
K_ABL passes (gap 2). Family A dev output byte-identical to
DEVANG4: no regression.

SKEPTIC: The prereg's own section 13 classification mapping maps
K_ABL failure to architectural recurrence, and the builder
unilaterally overrode it. The leg-1 bar exists to test whether the
front end is load-bearing; the ablation scoring 6/12, above the
5/12 bar, means the front end's contribution is smaller than the
bar demanded. "Miscalibration" is the classification every failed
bar would prefer, and keeping the mechanism while failing the bar
is face-saving unless the bar error is proven, not asserted.

JUDGE: UPHOLD, both the verdict and the classification. The
verdict letter governs and it stands as BUILD-FAIL: the bar was not
moved and the failure is not hidden. The classification is the
worker's evidence-based interpretation, recorded transparently with
a concrete mechanism (word-length composition of the B family) and
a concrete DEVANG6 recalibration (defeat fixed-3 by construction,
or learner-minus-ablation >= 4). Keeping a mechanism after a
bar-attributed BUILD-FAIL is legitimate when the mechanism passes
independent bars (K_DISC 6/6 with the gap isolated to FINREG,
K_SEG 12/12, K_AUD). The section 13 override is disclosed, not
hidden. UPHELD.

---

## 8. BATTERY E10: all three new mechanisms MECHANISM-WEAK

Coordinator verdict: M1, M2, M3 all MECHANISM-WEAK on nine new
sealed worlds (8 of 9 mechanism bars FAIL as predicted from source
reading; T-K13 precision control PASS, battery CALIBRATED). Kills
precisely scoped: M1 nesting/join/fabrication (T-K5 nesting 0/2,
T-K6 chained join 0/2, T-K7 fabricated 60399 instead of -2); M2
information-carrying/stopping/re-selection (T-K8 selection 0/6,
T-K9 12 non-NULL ACTs vs budget 6 with 0 keys stopped early, T-K10
population change 0/4); M3 lookup-correctness/propagation (T-K11
patched MAP_B's orphan instead of MAP_A's live SETREG, T-K12 zero
downstream propagation). Bounded keeps: M1 forward composition, M2
presence gate, M3 first-contradiction terminal revision (in-world
behaviors that held). Shared-cause clusters recorded as TNN-3
substrate hypotheses, not patch requests.

ADVOCATE: MECHANISM-WEAK is the honest verdict: the general
mechanism claims are dead, killed on their own preregistered bars,
with the failures matching source-reading predictions exactly
(which is what a calibrated battery looks like). T-K13's 8/8 PASS
shows the kills are specific, not blanket: the battery can pass a
mechanism-shaped bar, so the failures are informative. The bounded
keeps are not adopted mechanisms; they are the precise boundary of
what the battery did not kill (M1 engagement probes 2/2 per world,
collateral 2/2; M3 validity probes 3/3). The shared-cause clusters
(fixed-topology search; constant action channel; local patch plus
global lookup with no dependency tracking) are hypotheses for TNN-3,
per the no-patch-treadmill rule.

SKEPTIC: A mechanism that fails every hard probe is not a
mechanism, and "bounded keeps" are scraps that invite the repair
treadmill: each keep (forward composition, presence gate, terminal
revision) is a seed for a lineage that will grow researcher-written
machinery one failure at a time. MECHANISM-WEAK should mean
discard, full stop; keeping anything warm keeps the treadmill warm.

JUDGE: UPHOLD. MECHANISM-WEAK discards the general-mechanism
claims; that is the verdict, and it is terminal for those claims
this wave. The bounded keeps are behaviors that held in-world,
recorded as the boundary of the kill, not as surviving mechanisms;
nothing in the record adopts them as mechanisms or authorizes a
repair lineage on them. The shared-cause clusters are substrate
hypotheses, which is the correct output of a killing battery under
the no-patch-treadmill rule. UPHELD.

---

## 9. INDEX-EVICT: EVICT-PASS

Coordinator verdict: EVICT-PASS. All 8 frozen bars hold, 3/3
byte-identical. One hook line in evict_node plus ~90 lines pure
Zag; 0 modes/bridges/handlers. V1 stale membership and V2 chain
invalidation both handled; W2 NEW gather 59 vs OLD 32760 (555x
collapse avoided); answers preserved run-for-run; NEW cheaper than
the fallback it prevents (1m27s vs 1m46s).

ADVOCATE: The bars are comprehensive: (i) OLD demonstrates both
corruption shapes (cause=3 V2 chain break, cause=1 V1 dead member,
cause=4 FACT-side), not vacuous; (ii) NEW gates=1 after every
eviction; (iii) no collapse (W1 39 vs 56, W2 59 vs 32760, 555x);
(iv) NEW==OLD answers run-for-run; (v) 3/3 byte-identical; (vi)
healthy-state no-op byte-identical to canonical eee373a2; (vii)
mechanism accounting (unmap=6, unfact=18, unchain=1); (viii) MTF
cache cleared on victim death. The mid-run seq fix (last-wins to
first-wins, matching seq_nx exactly) was a soundness hardening; the
governing set re-ran byte-identical and the superseded set is not
the verdict basis.

SKEPTIC: The bounded gaps are real and unfired, which is exactly
when they matter: tag 40/900 infrastructure-node victims untested,
t2_revise_graph tombstoning chain nodes outside evict_node untested,
plen-2/4 bucket victim positions untested. The sealed set had
exactly one type-12 out-edge per node, so the seq fix's behavioral
equivalence is asserted on the easy case. The emergent learner
indexing keys surviving eviction (QPOST2 q1 scan=0 via new winner
8093) is noted but uncharacterized: an unmeasured interaction
between the hook and the emergent index.

JUDGE: UPHOLD. The 8 frozen bars are the verdict's scope and all
hold; the gaps are queued with specificity (t2_revise_graph
chain-killer coverage, infrastructure-node eviction guard, longer
soak storms), not firing, and they bound the claim rather than
undermine it. The seq fix matched seq_nx exactly per the prereg's
"mirroring rb_chain_plen exactly" instruction, and the governing
run set is byte-identical. UPHELD.

---

## 10. ARENA-ENG: APPROACH-VIABLE (trial-garbage reclamation)

Coordinator verdict: APPROACH-VIABLE. Prototype only; integration
queued. S1: steps 0-20 in 2.76s total vs ORIG step-15 marginal
~84s; S2: zero evictions, 165/1024 live at step 20; S3: per-query
(k, ans, tried, rej) byte-identical ORIG vs RECLAIM on all 15
feasible steps; S4: success-path scenarios identical including
promoted MAPs; S5: pure Zag, 2/2 byte-identical. Exactness, not
pruning. No transfer scoring run.

ADVOCATE: The diagnosis was corrected first (not branching-factor
explosion: trial-garbage accumulation, ~65 nodes/query never freed,
workspace fills at step 15, evict_node bid() catastrophe ~3s per
eviction, 28 evictions on step 15), then the approach broke the
wall differentially: identical trial outcomes on 15 prefix steps
plus 3 success scenarios, flat time curve, zero evictions. No ISA
change, no new opcodes or modes; the verbatim ORIG core is
untouched in the same binary. "Approach viable" claims exactly
what was shown.

SKEPTIC: APPROACH-VIABLE is a generous name for a prototype on one
transfer replica (T_A). The hg(W,20) telemetry is left as gross
allocs, a known wart. No TNN-3 integration exists; the open
question on miss_inquire uncertainty/guide node lifecycle is
unresolved. Viability on a verbatim prototype is the weakest form
of the claim.

JUDGE: UPHOLD. The verdict asserts approach viability, not
mechanism adoption: the wall is broken by eager reclamation with
differentially verified identical trial outcomes (byte-identical
fields, identical promoted MAP sets on success paths). The
prototype scope, the telemetry wart, and the queued integration
design are all explicit. The evidence (wall broken plus exactness)
is sufficient for "approach viable" and claims nothing more.
UPHELD.

---

## 11. SENSORY SA1 and H4: both BUILD-FAIL (queued as new preregs)

Coordinator verdict: SA1 BUILD-FAIL (stationarity design failure,
informative: B1 gap shrink 0% vs >=40%, B3 entropy ratio 0.305 vs
>=0.5; root cause: frozen global phase-locked harmonic model assumes
5s stationarity, per-1s T0s vary wildly, residual RMS ~= signal
RMS). H4 BUILD-FAIL (knowledge gap: cirrus sparsity; KB4 shadow
frac 0.0156 vs [0.03,0.60], KB5 corr 0.000 vs >0.60, KB6 mean 0.00
vs [-25,-0.5]; mechanism correct: 21,032 bytes differ at 1024, all
darker, sky/moon 0.00, no artifacts). Queued: SA1b short-time
chunked pitch tracking; H5 denser/stronger cloud shadows. Both as
new preregs, not patches.

ADVOCATE: Both failures are diagnosed to root causes with numbers.
SA1's 6x contrast gate correctly fired on nothing: the model, not
the gate, was wrong. H4's mechanism passed every correctness bar
(KB1 3/3 identical, KB2/KB3 sky/moon 0.00, KB7 0.93x, KB8 acutance
1.000); the failure is localized to a measured knowledge input
(0.67% significant shadow at sun-ray sample points). The queued
directions are structurally new hypotheses: SA1b replaces the
global model with short-time chunked pitch tracking (different
model class), H5 changes the world's cloud field while the
mechanism stands untouched.

SKEPTIC: The line between "new prereg" and "patch with a prereg
label" needs policing. H5 "denser shadows" tunes the world until
the mechanism's numbers pass; SA1b abandons the failed global model
after the fact. If every BUILD-FAIL is followed by a prereg shaped
by the failure, the prereg discipline becomes repair with extra
steps.

JUDGE: UPHOLD, no objection to the queued SA1b/H5 directions. The
test is structural: SA1b is a different model class (short-time
vs global phase-lock), not a parameter tweak of the failed model;
H5 changes the world's cloud field, not the mechanism, and the
mechanism's correctness bars already hold. Neither amends the
failed prereg; both are fresh preregs with fresh predictions, which
is what the discipline requires. UPHELD.

---

## 12. F2 v6: PARTIAL

Coordinator verdict: PARTIAL. Mechanism validated (wave-1 conv=1
REVISION to wave 2; wave-2 conv=2 REVISION to wave 3; wave-3 conv=3
with S2_VERIFY_RESULT 3); negative controls all PASS (NC2 0, NC3
VOID CONDITION satisfied with v5 PROGRAM_FAIL, NC4/NC5 nrev=1 no
over-revision); K6-R8 regression PASS nrev=0. Eval incomplete:
wave-3 11-action planning killed at 79 min under severe CPU
contention (18 min CPU for 79 min wall); K6-R4 unmeasured; 3x
byte-identical runs incomplete. Engineering constraint, not
scientific flaw. Commit-order PASS.

ADVOCATE: The mechanism's designed behavior was observed end to
end: two contradiction-triggered revisions across the double regime
shift, converging to Regime 3, with the one-revision-cap v5
provably unable to survive (NC3). No over-revision on single-shift
or oscillating worlds (NC4/NC5 nrev=1), no spurious revision on
static worlds (K6-R8 nrev=0). The incompleteness is an engineering
constraint of the shared environment, and the remedy is queued (3x
sealed eval on a less-contended machine, or iterative-deepening
planner in a new prereg).

SKEPTIC: The frozen bar required 3x byte-identical sealed runs;
they were not completed. PARTIAL is a soft verdict that parks
incomplete work; the verdict-governed outcome is BUILD-FAIL, with
the rerun queued. A taxonomy that lets "mechanism validated, eval
incomplete" avoid the FAIL label will be reached for whenever a
FAIL looms.

JUDGE: UPHOLD PARTIAL. BUILD-FAIL would misreport the evidence:
contradiction-triggered revision was observed through wave-3
convergence and every completed control passed. PARTIAL is the
accurate category: validated mechanism, incomplete sealed eval,
K6-R4 unmeasured, nothing adopted or counted as PASS anywhere. The
bar is not weakened: the 3x runs remain the requirement, and the
queued rerun is the path to a PASS verdict. UPHELD.

---

## 13. HPI H5R3: prereg frozen alone (no implementation)

Coordinator verdict: prereg FROZEN ALONE at b675b1d5a; sealed
evaluation queued next wave. Targets the untested H5R2 gap:
whether the revision chain fires through the revert step.
Substrate: frozen H5R2 source byte-identical (zero new cognition
lines). Kill bars: KB-CY 6/6, KB-RR 2/2, KB-BCY 18/18, KB-BRR 6/6,
KB-W0 32/32, KB-S1 byte-identity gate (VOID if absent),
KB-G3/KB-D3/KB-P3. Negative controls NC-0R3 through NC-8R3,
including NC-4R3 (the full-cycle chain control).

ADVOCATE: NC-4R3 is structurally sharp: the revert-after-revert
probe places the dead candidate (F1, the lowest node-id c1 fact,
whose executed output c1 verifies) first in enumeration order, so
without the gate the fresh MAP anchors to the dead fact: the exact
H5R killing configuration in a new structural position. Luck cannot
pass it. KB-CY/KB-RR require every DEP edge of the live MAP to
target live tag-1 non-superseded facts; the supplementary
selectivity check guards indiscriminate supersession (Attack 1);
dead-candidate starvation fails loudly via the exact-value bars
(Attack 2). The prereg even pre-registers that a KILL via NC-4R3 is
informative negative evidence. Commit-order PASS; kill bars never
move after freezing.

SKEPTIC: Prereg only, no implementation; one worker acted as
coordinator, builder, and evaluator with no independent adversary
this wave. The anti-triviality defenses are self-graded white-box
checks. Sharp on paper is not sharp in execution; the
discriminator's bite is untested until the sealed eval runs, and
self-grading is exactly where subtle loopholes survive.

JUDGE: UPHOLD the prereg freeze. The discrimination logic is
sound: the probe is constructed so the dead candidate verifies
first, which makes passing require the gate rather than luck. The
self-grading concern is real but it belongs to steps 10 and 11
(independent red team, governance audit), which remain open; it is
not a defect in the prereg itself. No adoption is asserted; the
sealed eval is queued. UPHELD.

---

## 14. FORK battery and RECORDS charter

Coordinator verdict: FORK 0 FAIL across 64 refs; repaired tip
FRESH PASS (resolves the 0221pdt UNTESTABLE); 2 FRESH PASS, 1 FRESH
UNTESTABLE (notes/commits, standing), 59 RE-CERT PASS, 2 RE-CERT
UNTESTABLE. RECORDS: charter complete (C181-C188 exploratory
ceiling, adoption BLOCKED), supersession bindings updated, SHA-256
typo fixed (commit 59dc25ece).

ADVOCATE: FORK resolves the prior wave's UNTESTABLE cleanly:
GIT-REPAIR 3c25ff8f1 restored src/tools/toolchain and the
extracted znc sha256-matches the frozen pin 498abcb5...; archive
immutability 48/48; all instrument pins re-verified unchanged. The
charter closes the zombie-investigation gaps with commit-cited
verification: mli run-2/run-3 transcripts and the C189 ledger entry
are in the record; C181 is BLOCKED honestly because REPORT.md lists
binaries and compile logs that commit d52666a8b does not contain.
The ceiling stands: exploratory BUILD-PASS, none citable as
SURVIVES, generality, or L3.

SKEPTIC: The corrupted 79-char SHA-256 string persists in three
other 2321pdt lane docs (LEARNER-MECH/JUDGE_BRIEF.md:82,
MECH-VERIFY/MECH_VERIFY_REPORT.md:17, GAP-DOC/GAP_DOCUMENTATION.md:
121): the sweep is incomplete and the corruption is still citable.
The charter admits the protect-how retry Step 0 "has not and cannot"
enter the record, so a required gap stays open. Adoption BLOCKED
for all eight makes the charter a ceiling document, not progress.

JUDGE: UPHOLD. The remaining typo instances are recorded with
exact paths and a follow-up sweep is queued; incompleteness is
disclosed, not hidden. C181 BLOCKED is the honest ceiling given
the missing artifacts, and the ceiling is the point: the charter
bounds what may be cited. 0 FAIL across 64 refs with the repaired
tip FRESH PASS is a clean battery result. UPHELD.

---

## PROCESS INCIDENTS

### (a) F1 no-op python3 invocation

Ruled under item 4 above. The coordinator's ruling (incident
recorded, chain uncontaminated, finding stands) is OVERTURNED on
the adoption: the F1 lane is PROCESS-FAIL per the mandatory worker
toolchain guard, and the FINDING CONFIRMED measurement stands as
exploratory evidence only, pending a clean pure-Zag re-freeze and
re-run. The self-disclosure and the contamination analysis are
commended and remain in the record; they do not create an exception
to an automatic rule.

### (b) Cross-lane commit contamination

Coordinator ruling: non-voiding hygiene blemish. DEVANG5's eval
commit ec84a9721 swept 4 pre-staged COMP-lane files; BATTERY's
d22862d07 swept 72 ARENA-lane files; SENSORY's 983e3073d contained
15 COMP files. Content intact in all cases; do not reset.

ADVOCATE: No sealed evidence, key file, or source was altered; the
contamination is attribution and commit-message only. Resetting is
prohibited. Workers were re-briefed on verifying `git status` and
committing own lane paths only, and a standing rule was proposed
(pathspec-only freeze commits). The substance of every lane's
evidence is untouched.

SKEPTIC: `git commit` without pathspec sweeping the whole index
shows workers are not verifying `git status` before committing.
The same inattention could one day sweep a sealed world file or a
key file into the wrong commit, or worse, stage and commit a file
that breaks another lane's seal. "Hygiene blemish" understates a
process gap that touches seal integrity machinery.

JUDGE: UPHOLD the non-voiding ruling. No content was altered and
no seal was touched; voiding would be disproportionate to an
attribution error. The skeptic's process point is valid and is
answered by the structural fix (pathspec-only freeze commits as a
standing rule), not by voiding this wave's evidence. UPHELD.

### (c) F2 sealed worlds committed 9s before prereg freeze

Coordinator treatment: transparent; world hashes frozen in the
prereg.

ADVOCATE: The seal's substance is world-fixity before the prereg
records the hashes, and that held: the worlds were fixed, their
hashes frozen in PREREG_F2V6, and the implementation (50693d022)
came after the prereg (8f99040b3). Nine seconds of commit-timing
skew is not peeking; no world output was used to tune anything.

SKEPTIC: The ordering rule exists so the prereg cannot be informed
by the worlds. Worlds committed before the freeze means the freeze
commit could have been shaped by them; "hashes frozen in prereg"
cuts both ways, since the prereg author held the worlds first. The
commit-order self-check is a governance bar, and it was tripped,
however narrowly.

JUDGE: UPHOLD the transparent treatment. The seal's substance
(worlds fixed before the prereg hashed them) held, and the
ordering rule's intent (prereg before implementation) held for the
implementation. This is recorded as a process wrinkle, and it is
moot for adoption: F2 is PARTIAL with nothing adopted. UPHELD.

### (d) Concurrent other-wave commits on the shared branch

Status quo: no adverse ruling; 0707pdt commits (XDOMAIN, WATCHDOG,
and others) landed on tnn-native-lab during this wave's runs.

ADVOCATE: Lanes work in pathspec-isolated directories and verify
their own artifact hashes; no interference with 0521pdt sealed runs
is evidenced.

SKEPTIC: Concurrent writes to the shared branch during sealed runs
are a standing contamination risk: a lane rebuilding from a moved
tip mid-run, or a shared-index commit sweeping another lane's
staged files (as seen in incident (b)). The .wave_lock does not
cover the branch.

JUDGE: No adverse ruling; the status quo stands. No verdict
changes. The risk is real and is recorded here for the
coordinator: consider branch-per-wave isolation or a freeze window
for sealed-run periods. UPHELD (no action).

---

## TALLY

Rulings rendered: 17 (14 verdict-slate items plus incidents
(b), (c), (d); incident (a) was ruled under item 4 and is not
double-counted).

- UPHELD: 16 (items 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14;
  incidents (b), (c), (d))
- OVERTURNED: 1 (item 4: the coordinator's ruling that the
  F1-FOLLOWUP finding stands despite the no-op python3 invocation)

The single overturn: F1 lane declared PROCESS-FAIL per the
mandatory worker toolchain guard (automatic consequence, no
de-minimis exception). The sealed measurement (R=13/40, T=2,
D_ops=9, Cmax_ops 15/40, NC-HARNESS 6/6, K-DET 40x3 byte-identical)
remains in the record as exploratory evidence only; adoption
requires a clean pure-Zag re-freeze and re-run. The contamination
analysis (Attack 6) and the self-disclosure stay in the record
undisturbed.

## Notes for the coordinator

1. The F1 overturn creates a same-wave precedent question the
   coordinator already answered once: the 1000-MAP scaling wave went
   PROCESS-FAIL for a self-disclosed python3 invocation with its
   measurements held exploratory. The debate group applied the
   identical standard here. Consistency is now on the record.
2. The debate group considered but did not adopt a middle path
   (uphold the contamination finding while suspending the verdict),
   because the guard's text makes the lane-level consequence
   automatic; a middle path would still be a coordinator-grade
   reinterpretation of a Micah-level rule.
3. Items 6 (C9) and 12 (F2) both carry "nothing adopted beyond the
   bounded verdict" riders; the queued multi-seed C9 battery and the
   F2 3x rerun are the highest-information follow-ups in their
   lanes.
4. The provenance probe's standing demand: lanes that inherit frozen
   substrates or binaries should keep stating the inheritance in
   the verdict line, as COMP, ARENA, and HPI did this wave.

No em-dashes were used in this transcript.
