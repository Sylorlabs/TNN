# DDES L3 Gap Analysis (A1 Architecture-Adversary)

Prereg: 7abe1ef66 (frozen before this analysis). Analysis only. No
implementation. No Python. No em dashes.

Target: frozen repaired DDES, `ddesr.zag` @ 17c97a2cd (REPAIR-PASS),
with the generalization work @ 843c45fee used only as evidence of
where researcher authority lives.

Adversarial posture: the L3 claim is assumed false. The question is
not what patch gets closest, but what structurally forecloses L3.

## K1: Criterion 0 gap analysis

### C0-A (runtime-defined semantics): FAIL

The source-audit kill bar asks: "where are the semantics implemented?"
For DDES, the answer is: in dedicated researcher-written source, at
every level. Nothing semantic lives in learner-created persistent
state.

1. Action vocabulary and encoding. `synthesize_plan` (line 162)
   writes codes: 0 for S, 1 for W, and the observation code computed
   as `obs = 4 - v_star` (line 178). The meaning of these codes is
   implemented in `world_step` (line 221): `a==0` sets X, `a==1`
   advances time and propagates, `a==2` reads st[8], else reads
   st[4]. Both sides are researcher-written; the code-to-effect
   mapping is a shared convention between them. The learner never
   observes an action effect, never tries an alternative code,
   never infers the mapping. (The generalization @ 843c45fee
   replaced the formula with `obs = 2 + v_star`, a one-time
   researcher-authored change to a generic rule. Authority did not
   move to the learner.)

2. State layout. Values at st[v*4], time at st[12], timestamps at
   st[16+v*4]: researcher-designed, shared verbatim between
   synthesis, world_step, and predict. The learner does not define
   or discover the layout.

3. Hypothesis format. (src, dst, delay) triples as parallel arrays:
   researcher format. The learner receives hypotheses in this
   format; it does not construct or choose a representation for
   causal structure.

4. Schema menu. The driver (line 277) loops `schema` over {1, 0}:
   1 = set-X, 0 = null. Two researcher-enumerated interventions,
   tried in fixed order, best (earliest t*) kept. This is a
   two-element menu, not a constructed intervention.

5. Derivation algorithm. `compute_arrivals` (line 67, min-arrival
   propagation), `compute_frontier` (line 108, argmin over
   variables), `eff_waits` (line 148, boundary clamp): all
   researcher-authored analysis. The learner executes the
   algorithm; it does not invent, select, or modify it.

The only persistent learner-side state across a run is the
`plans_built` counter and the emitted plan bytes, neither of which
defines semantics. C0-A fails at five independent points; fixing
any subset leaves the rest.

### C0-B (open structural form): FAIL

The synthesized plan is exactly one complete answer from a family
parameterized by (V*, t*, schema): an optional S, then
eff_waits(t*) copies of W, then one terminal observation O(V*).
`synthesize_plan` assembles it by formula in a single pass; there
is no incremental construction, no growth, no extension, split,
or connection of fragments, no revision. The "derivation" selects
(V*, t*) by argmin and schema by a 2-element loop, then emits the
complete plan. Variable plan length (13 for 4-var, 15 for 5-var)
is parametric length, not open structural form: the shape
[S? W* O] never varies. Nothing is built up across steps; nothing
persists to be extended later.

### C0-C (unforeseen solutions): FAIL as L3 evidence

Post-freeze sealed families exist: World C (length 6), D (Z-only),
E (empty frontier), F (t*=0, first adversary), G (depth 9/8),
H (4-variable, RT2), I (5-variable, generalization worker).
But every one instantiates the same functional form: rule-delay
causal chains differing only in delay values, variable count,
target variable, and boundary conditions. None requires a
materially different representation: no conditional branching, no
repeated or recursive structure, no relational coupling, no
periodic regimes, no hierarchical composition of hypotheses.
These are parametric variations of the family the researcher
designed the derivation for, not unforeseen forms.

The RT2/H attack is genuine adversarial evidence, but note what
it did: it bounded a generality claim (killed "works for N
variables" as stated), rather than demonstrating the learner
handling an unforeseen representation family. For C0-C's purpose,
DDES fails: the machinery has only ever seen (src, dst, delay)
triples and only ever emits [S? W* O] plans.

### C0-D (cognitive reuse): FAIL

The synthesized plan is executed once and discarded. Nothing
persists across `ddes_world` calls. No structure is promoted to a
reusable named object. No later task benefits: each world is
solved from scratch by re-running the identical deterministic
derivation. The one-shot character of DDES, which is its strength
as L2 (zero enumeration, zero bound), is exactly what kills C0-D:
there is no invented structure whose reuse improves later
cognition, because nothing invented is kept.

### K1 summary

C0-A: FAIL (five independent researcher-owned semantic loci).
C0-B: FAIL (single complete plan by formula; fixed shape).
C0-C: FAIL as L3 evidence (sealed worlds are parametric, not
representationally novel).
C0-D: FAIL (no persistence; one-shot by design).
DDES fails all four conjunctive requirements. The failures are
independent: C0-D fails even if C0-A were somehow fixed, because
the architecture discards its output.

## K2: Learner-derived action-effect model (design)

This designs the minimal change that would move the action
semantics (C0-A item 1) into learner state. It does not fix items
2-5, C0-B, C0-C, or C0-D; it isolates the encoding-authority
question the generalization worker surfaced.

Persistent learner state: an action-effect table E, one entry per
action code c. Each entry holds an effect description in a fixed
generic schema the researcher provides once: (cell_changed |
time_advanced | value_returned, which_cell, magnitude). The
schema is generic machinery (a struct layout), not domain
semantics; the entries' contents are learner-created. Plus a
confidence counter per entry. Initially all entries are UNKNOWN.

Probe phase: before any discrimination task, the learner runs a
probe episode. For each candidate code c in a small range, it
snapshots state, emits c, snapshots again, and records the
difference using a generic state-diff primitive (compare two
buffers cell by cell; record which cell changed, or what value
the action returned). From this it induces, for example: code 0
sets cell 0 to 1; code 1 advances the time cell and propagates;
code k >= 2 returns the value of cell (k-2). The induction rule
is: the cell that changed (or the returned value's source cell)
is the effect. The range of candidate codes to probe is itself
discovered by probing until codes stop producing effects.

Synthesis using the induced map: `synthesize_plan` no longer
computes `obs` arithmetically. It looks up: find c such that
E[c].effect == OBSERVE and E[c].which_cell == cell(v_star).
If no entry matches with confidence above threshold, synthesis
refuses and requests more probing. The arithmetic
`2 + v_star` is replaced by a lookup over learner-populated
entries.

Falsification experiment (preregisterable): freeze the learner;
in a sealed world, permute the action-effect mapping (e.g.,
observation codes start at 10, or code 2 observes Z instead of
Y). The learner-derived version must induce the new mapping
from probes and still converge; current DDES would emit the
wrong code and fail to discriminate. If the learner cannot
induce the mapping without researcher help (e.g., it needs to
be told which codes are safe to probe, or it cannot attribute
an effect when two cells change at once), the design fails at
the induction step, and the gap is deeper than action-effect
modeling: it is effect-attribution, which needs its own
generic machinery.

Honest note: this design moves exactly one of the five C0-A
loci into learner state. The hypothesis format, schema menu,
state layout, and derivation algorithm remain researcher-owned.

## K3: Incremental vs fundamental

Fundamental redesign. The result would not be DDES.

What survives: `compute_arrivals` and `compute_frontier` are
genuinely generic derivation machinery. RT2 copied them verbatim
into 4-variable worlds; the generalization worker changed nothing
in them. They would survive as the analysis core of any
successor.

What is replaced:

1. The synthesis-to-execution contract. Today synthesis and
   world_step share a researcher-designed encoding. The K2 design
   needs a probe/induction phase, a persistent effect table, and
   a lookup-based synthesizer. `synthesize_plan` as written
   (formula assembly) is replaced, not extended.

2. The schema menu. {set-X, null} is a 2-element researcher
   menu. A learner that models action effects has no use for a
   menu of named interventions; it would need to discover
   interventions from the effect table (e.g., "which code sets a
   cell I can use as a source?"). The menu is a C0-A violation
   independent of the encoding.

3. For full C0-A, the hypothesis format and derivation algorithm
   would also need to become learner-representable. At that
   point the architecture is no longer "guided one-shot
   derivation from a hypothesis pair." It is either the F2 lane
   (the learner constructs hypotheses and experiments) or the
   GENEXEC2/Q3 lane (the learner constructs executable
   representations). The arrival-analysis core could serve as a
   component inside such a learner, the way a sort routine
   serves inside a larger program, but the system would not be
   DDES.

The structural reason L3 is foreclosed for this lineage: DDES's
identity is the guidance. The researcher contributes what to
derive (discriminating observation), in what vocabulary (action
codes), over what representation (rule triples), from what
options (two schemas), by what algorithm (arrival analysis).
Each contribution is load-bearing; the BUILD-PASS results depend
on all of them. Removing them one by one does not converge to a
learner; it converges to an empty harness. The L3 path is not
through DDES but through architectures where the learner owns
the representation from the start: F2's hypothesis construction,
Q3's operator recruitment (ALLOCATE_OP), Q4's explanatory
variables.

Terminal classification, unchanged: DDES is a strong bounded L2
derivation engine. If the remaining pipeline steps pass, the
correct verdict is SURVIVES-AS-L2 (bounded), with the five
researcher-owned loci recorded in the verdict. It cannot become
L3 by repair; the K3 finding from the first adversary
("guidance fully researcher-authored") is structural, not a
bug.

## Verdict

L3-GAP-ANALYZED. All three kill bars pass. DDES fails C0-A, C0-B,
C0-C (as L3 evidence), and C0-D independently. A learner-derived
action-effect model is specifiable and falsifiable (K2), but it
replaces the synthesis contract and leaves four other
researcher-owned loci untouched; full C0 compliance requires a
different architecture, not a repaired DDES.
