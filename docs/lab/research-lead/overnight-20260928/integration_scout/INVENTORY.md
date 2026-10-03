# Integration Scout: Component Inventory and Gap Map

Date: 2026-09-30.
Scout task: map what exists, what is missing, and whether the program is
converging on one continuing learner or accumulating disconnected mechanisms.
Analysis only. No implementation. No new claims beyond committed results.

Style note: no em dashes in this document.

## 1. The requirement (verbatim from the directive)

"One continuing learner should eventually experience new vocabulary, concept
learning, procedure invention, conflicting evidence, active inquiry, causal
learning, memory pressure, unrelated interference, corrections, and delayed
reuse, with no process reset, no task label supplied to cognition, and no
recompilation per task."

## 2. Component inventory

### 2.1 Procedure discovery (proc_learn family)

Status: Bounded L2+ (11/12 L3 criteria; criterion 12 revision FAILED by proof).
Committed evidence: Family X 8/8 on adversary hidden tests; transfer PI-5 5/5;
RT2 authoritative verification.

What it provides: from input/output string pairs, extracts index sequences and
searches 1055 compositional programs for the smallest fitter. 85 distinct
behaviors (all affine f(k,n) = ak+bn+c).

Interface: pairs in, program bytes out (or -1 on failure). Pure function over
training data; no persistent state of its own.

What breaks on integration: requires unique input characters (RT2-C FAIL on
"aaa"); returns VACUOUS otherwise. No revision: H-REVISE KILLED with
mathematical proof. Uniform-length training overfits (3-K instead of n-1-k);
repaired only on the frontier (H-GENBIAS N-first two-pass) in unified_learn.zag
and stress_learn.zag. Five older copies (proc_learn.zag, bridge_learn.zag,
route_learn.zag, integ_learn.zag, proc_cond.zag) still carry the single-pass
search and inherit the overfit (documented as NQ5, unrepaired).

Integration verdict: usable as a component with the N-first fix, a uniqueness
precondition, and no expectation of self-revision.

### 2.2 Causal learning (causal_learn.zag)

Status: Bounded L2. 14/14 probes; 8 kill bars; beats 3 baselines; order robust.

What it provides: induces single-variable equality conditional rules from
(state, action, next_state) episodes; holds competing hypotheses (AMBIGUOUS);
refutes confounders with single counterexamples; WITHHOLDs under genuine
ambiguity; revises via CONTEST/RESOLVE with SUPERSEDED temporal provenance.

Interface: episodes in, rule set out; query (state, action) returns prediction
or WITHHOLD.

What breaks on integration: the full split/merge/contest machinery was NEVER
ported into the unified learner. H-UNIFIED and unified_learn.zag use a
simplified causal store (single-condition rules, no split/merge/contest).
The 14/14 validated machinery sits in causal_learn.zag, disconnected from the
continuing learner. Narrow vocabulary: single-variable equality only.

Integration verdict: the strongest causal component is stranded outside the
integration line. Porting it is gap G2.

### 2.3 Revision bridge (bridge_learn.zag)

Status: Bounded L2+. 7/7 kill bars; B-A6b slot-exhaustion bug FIXED via
pdiscover_dry (failed attempts consume 0 slots); cleared for integration.

What it provides: when discovery returns -1, searches (input position, byte
value) pairs for a split where both subsets are discoverable; learns IF
input[pos]==val THEN procA ELSE procB; both procedures preserved; dispatches at
query time.

Interface: failure signal in, conditional rule out. Binary conditions only:
one position, one value, two procedures. No conjunctions, no ranges, no
recursive bridging.

What breaks on integration: F-LEAK (confirmed in H-STRESS, unrepaired): when
the bridge store is full and a split fails, the return -1 path does not
release already-stored subset procedures (E9 wasted 2 slots). Under sustained
pressure this leaks silently.

Integration verdict: integrated into unified_learn.zag (functional). F-LEAK is
the known open wound.

### 2.4 Learned router (route_learn.zag)

Status: Bounded L2 integration infrastructure. 5/5 kill bars; 3/3
byte-identical; H-INTEG still 5/5 after port.

What it provides: replaces P/C/Q explicit prefixes with per-item structure
inference from format markers and field content; white-box ROUTE traces;
withholds on ambiguity.

Interface: raw line in, target handler out (PROC_LEARN / CAUS_LEARN / query).

What breaks on integration: predicates are authored. What is inferred is the
per-item decision, not the routing rules. The >=2 segment threshold is an
authored disambiguation rule. Format markers (>, ;, ,) are assumed. Learned
routing (NQ2) is unattempted: no worker has tried inducing predicates from a
marked curriculum.

Integration verdict: removes explicit labels but keeps researcher-authored
structure detection. The directive says "no task label supplied to cognition";
authored structural checks are a weaker form of supplied labeling.

### 2.5 Unified learner (unified_learn.zag)

Status: Bounded L2 integration. 9/9 checks; H-STRESS 17/17 SURVIVES after
H-GENBIAS repair; H-UNIFIED re-verified with no regression.

What it provides: the engineering backbone. One process, one item stream, no
labels, no reset. Router (2.4) + discovery (2.1, N-first) + bridge (2.3) +
simplified causal store. Graceful degradation: honest -1 on store exhaustion,
no crashes, no cross-store corruption, ambiguity withholds.

Interface: item stream in; learned state persists across items; queries
answered from stores.

What breaks on integration: simplified causal store (see 2.2). Procedure
queries report ALL slots/rules; no intent retrieval (documented gap). No
synergy measurement: coexistence is proven, mutual benefit is not. The honest
generality finding: the N-first bias is a search-order preference, not a
generality proof.

Integration verdict: this is the closest thing to the required "one continuing
learner" on the engineering line, but its cognitive components are the
simplified ones.

### 2.6 DEVINT1 (devint1.zag)

Status: BUILD-PASS (4/4 frozen bars). One process, 11 developmental stages,
raw sequence input, no task labels, no resets, no recompilation.

What it provides: the developmental checklist in one binary. New vocabulary
(S1-S3: segmentation from induced statistics, 4 concepts, 6/6 correct
segmentations); concept learning (S3); procedure learning (S6: 4 vs 5
examples); conflicting evidence (S7: 4 contradictions, 2 boundary violations);
active inquiry (S8: INQUIRY emitted and answered with a discriminating
episode); revision (S9: 1 rollback); memory pressure (S10: eviction under two
policies); delayed reuse (S11: 17/17 recognition, 3/3 procedure reuse).

Measured synergy (rare in this program): S1 concepts speed procedure learning
(4 vs 5 examples); S2 causal knowledge beats LRU on post-eviction probes
(8/12 vs 0/12); S3 contradiction drives representational refinement
(treatment 1, control 0). S4 neutral (control happens to match true morpheme
width).

Interface: stage functions are sequential code blocks; episodes are byte
strings; no stage labels reach cognition.

What breaks on integration: the world is toy (morpheme sequences). The S8
inquiry is researcher-answered: the learner emits INQUIRY but the harness
feeds the discriminating episode; the learner does not generate it. That is
the gap DDES is designed to fill. DEVINT1 is a separate binary from DEVINT2;
no single program runs both curricula.

Integration verdict: covers the most directive requirements in one process,
but in a toy domain with a prompted inquiry.

### 2.7 DEVINT2 (devint2_learn.zag)

Status: BUILD-PASS (6/6 frozen bars). One process, single main(), two exposed
operations (learn, query), integer-coded episodes.

What it provides: the memory and interference half of the directive. Twin
stores on identical sequences: STORE-C (eviction by cognitive consequence:
10*(correct-wrong) + 5*dependents - 8*contradictions + 1) vs STORE-R (LRU).
Unrelated interference (24 disjoint-key rules); delayed reuse (8 rules +
two-hop compositions after soak); correction with local provenance
(superseded_obj, 0/12 collateral); memory pressure (30 junk rules, 26
evictions per store; STORE-C preserves 8/8 useful-but-stale, STORE-R keeps 30
junk and forgets 8/8 useful).

Interface: learn(subj, rel, obj) / query(subj, rel, expected). Exact-match
retrieval only (no generalization/backoff; disclosed limit). Two-hop uses an
authored comparison operator.

What breaks on integration: token encoding is integer-coded and "disclosed as
not under test": there is no real vocabulary grounding. Retrieval is
exact-match; the interesting generalization work is future. The memory policy
is compared but not learned: neither store invents its policy (fifth frontier
unattempted).

Integration verdict: validates consequence-based eviction as a policy, but the
policy is supplied, and the world is integer codes.

### 2.8 H-CAUSALEXP-CONSTRUCT (cxconstruct.zag)

Status: SURVIVES-AS-L2 (bounded). L3 construction claim KILLED by A1 and A2.
Final governance verdict committed (45db44fab).

What it provides: a correctness-critical disagreement filter plus
efficiency-relevant search choices (simulation buys 35x-254x; deepening buys
shorter sequences) over a researcher-enumerated finite family. Measured value:
17x-85x fewer real-world actions than greedy; 4/4 novel-world generalization
vs 0/2 for memorization; filter load-bearing for correctness (4/4 to 0/4
without it).

Interface: hypothesis pair in, discriminating sequence out (or
NO-DISCRIMINATING-SEQUENCE), exactly one real execution.

What breaks on integration: the learner never inspects hypothesis structure
to propose candidates; generation is hypothesis-blind filtering of a fixed
1364-sequence stream; MAXD=5 hardcoded; silent false convergence outside the
hypothesis class (OOD-3); no compositional reuse (transfer K-TR4 FAIL).
Usable only as a filter component inside a genuinely constructive
architecture, not as the constructor.

Integration verdict: keep the filter; discard the construction reading. The
successor (DDES) is the integration-relevant artifact.

### 2.9 I2 learning-to-learn (l2l2.zag)

Status: BUILD-PASS (5/5). Bounded L2L, honest L1/L2 scope.

What it provides: minimal demonstration of state-dependent learning speed.
Family A (offset 3): 13 examples. Family B (offset 7) with retained
form_known: 10 examples. Fresh B: 13. Ablated B: 13. Transfer causally traced
to retained state; mechanism: skip the 4-example memorization preamble once
the offset form is known viable.

Interface: examples in; retained (offset_hyp, trusted, form_known) across
families.

What breaks on integration: the hypothesis form (fixed offset) is
researcher-supplied; only the constant and trust flag are learned. Transfer is
3 examples, within one supplied form. Nothing here generalizes to new forms.

Integration verdict: a clean existence proof of retention-accelerated
learning, too small and narrow to drive integration by itself. The pattern
(retain viable-form flags across tasks) is the reusable idea.

### 2.10 FDCR (rep_v2)

Status: L2 representational adequacy (NOT L3). K5/K2/K4/K3 PASS; H-INFER
repaired sibling inference (3/3); 3 red-team downgrades open (bar confound,
MERGE incomplete, spurious SPLITs); COMPOSE KILLED on utility (redundancy
theorem).

What it provides: FORM/MERGE/SPLIT/GRADE/CONTEXTUALIZE concept operators;
hierarchy, delayed split/merge, overlap; 24 entities / 36 concepts at 0.192s.

Interface: entities with features in; concept lattice out.

What breaks on integration: never integrated into any continuing learner.
DEVINT1 builds its own concept inventory from scratch; FDCR sits in rep_v2,
disconnected. The bar confound means adequacy rests on white-box structure
plus 3 genuine probes.

Integration verdict: the best concept machinery available, stranded outside
the integration line. Candidate for the concept layer of one learner.

### 2.11 Arena contestant (devint1_contestant.zag)

Status: competitive entry, score 0.573 (39/68), up from 0.352. C3 paraphrase
0 to 1.000; C5 correction 0 to 1.000; C14 restart 0.500 to 1.000. No
regression on prior perfects. Remaining zeros: composition, conflict, active
inquiry, causality, procedure learning, transfer, autonomous goals, language.

What it provides: the only mechanism scored against the 15-capability
competitive benchmark. Bugfix-driven gains (correction dispatch, "fact2"
alias) plus the DEVINT1 substrate.

What breaks on integration: the contestant is a fork of the DEVINT1 line
with arena-specific format handling. Whether arena fixes flow back to the
canonical learner is undocumented. The zeros list overlaps the integration
gaps (composition, causality, procedure learning, transfer), which suggests
the contestant inherits the same missing machinery.

Integration verdict: the competitive pressure is real, but the contestant is
a branch, not the trunk.

### 2.12 In-flight builders (status at scout time)

F1 (genexec2): learner-authored executable semantics; prereg frozen; builder
running; A1-Continued attacks pre-registered (AX-GX1/2/3). Highest priority
frontier. Not yet a component.

F2 (autosci): autonomous scientific discovery; builder running. Its lane
overlaps DDES (hypothesis-guided generation). Not yet a component.

F3 (devlang): developmental semantic language; builder running. Not yet a
component.

DDES (next_causal/DESIGN.md committed; builder spawned): difference-driven
experiment synthesis; targets strong L2 guided generation. Design only at
scout time.

## 3. Requirement coverage map

Directive requirement -> best current coverage -> status:

- new vocabulary: DEVINT1 S1-S3 (segmentation to concepts) -> BUILD-PASS,
  toy domain.
- concept learning: DEVINT1 S3; FDCR (unintegrated) -> partial.
- procedure invention: discovery 11/12; DEVINT1 S6; unified line -> bounded
  L2+, no revision.
- conflicting evidence: DEVINT1 S7; causal CONTEST (unported full version) ->
  partial.
- active inquiry: DEVINT1 S8 (prompted); H-CAUSALEXP-CONSTRUCT (filter only);
  DDES (design) -> gap G6.
- causal learning: causal_learn.zag 14/14 (unported); unified simplified
  store; DEVINT1 S5 rules -> partial, best version stranded.
- memory pressure: DEVINT2 STORE-C vs STORE-R; H-STRESS 17/17 -> BUILD-PASS /
  SURVIVES.
- unrelated interference: DEVINT2 S2/S4 -> BUILD-PASS.
- corrections: DEVINT2 S5 (local, 0/12 collateral); DEVINT1 S9 -> BUILD-PASS.
- delayed reuse: DEVINT2 S3/S7; DEVINT1 S11 -> BUILD-PASS.
- no process reset: DEVINT1, DEVINT2, unified (single process) -> yes.
- no task label to cognition: DEVINT1/DEVINT2 (none); unified router
  (structure-inferred, authored predicates) -> partial, gap G4.
- no recompilation per task: single binaries -> yes.

No single binary covers the full row. DEVINT1+DEVINT2 together cover every
functional requirement, but they are two programs in two toy domains.

## 4. Gap list (ordered by integration leverage)

G1. No single binary runs the full developmental curriculum. DEVINT1
(morpheme world) and DEVINT2 (integer-coded rule world) are separate
processes. The directive's "one continuing learner" does not exist yet as a
binary; it exists as two demos plus an engineering backbone.

G2. The full causal machinery (split/merge/contest, 14/14 validated) was
never ported into the unified learner. The integration line runs the
simplified causal store. This is the largest stranded asset.

G3. FDCR concept machinery was never integrated into any continuing learner.
DEVINT1 reinvents a smaller concept inventory from scratch.

G4. Routing predicates are authored (H-ROUTER). Learned routing (NQ2) is
unattempted. The directive's "no task label supplied to cognition" is met
literally but not in spirit.

G5. No procedure intent retrieval. Queries report all slots/rules; the
learner does not infer which procedure the querier intends. Documented gap in
H-ROUTER/H-UNIFIED, still open.

G6. Active inquiry is prompted, not generated. DEVINT1 S8 feeds the
discriminating episode from the harness; H-CAUSALEXP-CONSTRUCT selects from a
menu. Genuine generation waits on DDES/F2.

G7. Cross-mechanism synergy is measured once (DEVINT1 B3: positive on S1/S2/
S3, neutral S4) and never on the unified line. Coexistence is proven;
mutual benefit is mostly unmeasured.

G8. The arena contestant is a branch, not the trunk. Arena bugfixes and
format handling have no documented path back into the canonical learner.

G9. Five discovery copies still carry the single-pass overfit (NQ5). Only
the frontier copies have the H-GENBIAS fix. Any integration built on the old
copies inherits the generality gap.

G10. F-LEAK: bridge-full slot waste on failed splits (confirmed, unrepaired).
A slow memory leak inside the integrated revision path.

G11. Token encoding is not under test anywhere (DEVINT2 integer codes;
DEVINT1 byte strings). No component grounds real vocabulary.

G12. Memory policy is compared, not invented (fifth frontier unattempted).
STORE-C is supplied; the learner does not design its own policy.

G13. Revision is external (Bridge), not in core discovery (H-REVISE KILLED
by proof). Conditional revision exists; general revision does not.

## 5. Proposed integration architecture (not implementation)

One binary, one process, one main(), layered stores with a shared
episode stream. Each layer is a named component with the committed source it
derives from:

Layer 0, encoding: byte/integer input as today (DEVINT1/DEVINT2 style).
Real vocabulary grounding is future work (G11); the architecture must not
assume it.

Layer 1, segmentation and concepts: DEVINT1 S1-S4 segmentation plus FDCR
operators (FORM/MERGE/SPLIT) ported in, replacing DEVINT1's smaller
inventory. White-box concept lattice, queryable.

Layer 2, rules and causality: the FULL causal_learn.zag machinery
(split/merge/contest, SUPERSEDED provenance) ported into the unified
process, replacing the simplified causal store. This closes G2 and gives
conflicting-evidence handling the validated machinery.

Layer 3, procedures: discovery with the H-GENBIAS N-first fix as the single
canonical copy (close G9 by retiring the five stale copies), plus the
revision bridge with F-LEAK repaired (close G10). Binary conditionals only;
general revision stays out of scope per H-REVISE.

Layer 4, memory: STORE-C consequence-weighted eviction as the default policy
(from DEVINT2), with the twin-store harness retained as a regression test.
Policy invention stays a frontier (G12).

Layer 5, inquiry: DEVINT1-style INQUIRY emission now, wired to the
disagreement filter (H-CAUSALEXP-CONSTRUCT, bounded use) as an interim, and
to DDES once it reports. This closes G6 in stages: prompted -> filtered ->
generated.

Layer 6, routing: structure-inferred router (H-ROUTER) now; learned routing
(NQ2) as the defined next experiment (G4).

Layer 7, query and intent: exact-match and report-all as today; intent
retrieval (G5) as a defined gap with a prereg-shaped hole: the learner must
infer which stored procedure/rule the querier intends from query context.

Cross-cutting: single STATE-CONT persistence check after every stage (DEVINT1
B1 pattern); determinism 3/3 byte-identical; no task labels; no resets; the
I2 retention pattern (viable-form flags carried across tasks) applied to
procedure forms and rule schemas.

Integration order (each step is a preregistered worker, builder reports only):

Step A: retire stale discovery copies; single canonical N-first discovery
(closes G9).
Step B: port full causal machinery into unified_learn.zag (closes G2).
Step C: repair F-LEAK on the bridge path (closes G10).
Step D: merge DEVINT1 and DEVINT2 curricula into one binary on the unified
backbone (closes G1 functionally).
Step E: port FDCR operators into the concept layer (closes G3).
Step F: wire the disagreement filter into inquiry; replace with DDES when it
lands (closes G6 in stages).
Step G: learned routing experiment NQ2 (closes G4).
Step H: intent retrieval (closes G5).
Step I: synergy battery on the unified line (concepts -> procedures,
causality -> memory, contradiction -> refinement), mirroring DEVINT1 B3
(closes G7).
Step J: arena contestant rebased onto the canonical binary; arena fixes flow
back by construction (closes G8).

## 6. Answer to the key question

Are we building toward one learner, or accumulating disconnected mechanisms?

Both, and the split is measurable. Toward one learner: the unified line
(integ -> router -> unified -> stress -> repair) is a genuine engineering
backbone with 17/17 stress survival; DEVINT1+DEVINT2 jointly demonstrate the
full directive checklist in single processes; determinism and governance
hold throughout. Accumulating disconnected mechanisms: the best causal
machinery (14/14) and the best concept machinery (FDCR) were never ported
into the backbone; the arena contestant is a branch; five stale discovery
copies persist; the disagreement filter has no home yet.

The program is one porting-and-merging effort (Steps A-J) away from the
backbone deserving the name "one continuing learner". Until those steps run,
the honest description is: a validated backbone, two developmental demos, and
several stranded assets.

## 7. Claim ledger (scout records, no new verdicts)

All classifications cited from committed results: procedure discovery bounded
L2+ (11/12); causal learning bounded L2; integration v1 bounded L2; FDCR L2
adequacy; bridge bounded L2+; router bounded L2; unified learner bounded L2;
DEVINT1 BUILD-PASS; DEVINT2 BUILD-PASS; H-CAUSALEXP-CONSTRUCT SURVIVES-AS-L2
(L3 KILLED); I2 BUILD-PASS (bounded L2L); DDES design only. No mechanism at
L3. No SURVIVES claimed by this scout.

*End of inventory.*
