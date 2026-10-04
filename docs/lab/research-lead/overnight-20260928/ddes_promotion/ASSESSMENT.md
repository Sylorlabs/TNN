# DDES Promotion Assessment: 11-Step Pipeline

Date: 2026-09-30. Analysis only. No implementation. No Python. Pure documentation.

## Verdict

**DO NOT PROMOTE.** DDES (repaired) remains at BUILD-PASS plus REPAIR-PASS.
It does not yet qualify for SURVIVES under the 11-step pipeline.

This is not a downgrade. The repaired mechanism is what it claims to be:
genuine one-shot derivation with zero enumeration, zero bound, zero menu,
now sound at the t*=0 boundary. But promotion to SURVIVES requires all 11
steps, and 5 of the 11 are missing or incomplete. The honest target was
always strong L2 guided generation, not L3, so the promotion question is
whether DDES becomes SURVIVES-AS-L2 (bounded), analogous to
H-CAUSALEXP-CONSTRUCT. It is not there yet.

## Evidence inventory (all commits verified to exist)

- Design: `af8121780` (DDES design doc, implementation-free)
- Builder prereg: `d42294620` (K-NX1..K-NX8, V-NX1..V-NX3, frozen before implementation)
- Builder implementation: `56db8d606` (BUILD-PASS, 9/9, all bars pass, pure Zag)
- Adversary prereg: `5fd7ef448` (K1/K2/K3 frozen before attack code)
- Adversary result: `e40bdfc9b` (ATTACK-SUCCEEDS via K2, t*=0 hole; K1 fails; K3 confirms L2 ceiling)
- Repair prereg: `0f10fd0f2` (frozen alone, strict ancestor of implementation)
- Repair implementation: `17c97a2cd` (REPAIR-PASS, 11/11, all K-R1..K-R5 pass)
- Repair binary evidence: `963661e68` (binaries, zero-byte stderr logs)

Classification throughout: strong L2 (guided generation), NOT L3. The
researcher owns action vocabulary, hypothesis format, analysis algorithm,
and schema set. This ceiling is disclosed, confirmed by the adversary (K3),
and unchanged by the repair.

## Step-by-step assessment

### Step 1: Committed preregistration. COMPLETE.

`d42294620` froze K-NX1..K-NX8 and V-NX1..V-NX3 before any implementation.
Commit order verified via git merge-base --is-ancestor. The repair has its
own frozen prereg (`0f10fd0f2`), committed alone, also order-verified.
Process note: the builder prereg file was swept into a concurrent commit by
the shared git index; content verified byte-identical, ordering preserved.
The builder also disclosed a single Python use for an em-dash byte check,
redone with shell tools; no Python in artifacts. Disclosed, not cured, but
contained.

### Step 2: Implementation. COMPLETE.

`56db8d606`: pure Zag, 3/3 byte-identical (md5 a81b98fc788f4649b9f9d86d8887a84a),
exit 0, zero stderr. Repair `17c97a2cd`: pure Zag, 3/3 byte-identical
(md5 fca91df99502c54625665dc32da0df93). Both committed locally.

### Step 3: Sealed evaluation. COMPLETE with one deferred sub-bar.

Worlds A and B were frozen in the prereg. Worlds C (A2 sealed killer, length
6), D (Z-only), and E (empty frontier) were sealed instances designed after
freeze, testing K-NX3 (design-level), K-NX4, K-NX5, K-NX7, K-NX8. The
adversary added sealed World F (t*=0) after freeze. Results: 9/9 on the
frozen set, 11/11 on the repaired binary including F.

Deferred: K-NX3 promised a sealed L>=8 depth test ("awaits post-freeze
adversary" per DDES_RESULT.md). The adversary tested t*=0 instead of depth.
World C (length 6) passed at design level, but the L>=8 sealed depth run
has never been executed. This is the single largest open item inside step 3.

### Step 4: Independent reproduction from committed source. INCOMPLETE.

What exists: the adversary reused the frozen DDES functions verbatim inside
killer.zag and reproduced their behavior (a partial functional reproduction).
The repair worker verified that committed run1.txt md5 matches the tested
binary output. The builder ran 3/3 byte-identical runs.

What is missing: no second party has independently rebuilt the binary from
the committed source (`ddes.zag` / `ddes_repair/ddesr.zag`) and reproduced
the byte-identical outputs. Self-reproduction is not independent
reproduction. This step is standard and cheap; it should be done by a party
that did not write the code.

### Step 5: Simple-baseline comparison. MISSING.

No simple baseline has been run against DDES. Candidates the pipeline
expects: a memorization control, a brute-force enumeration baseline with a
pruned bound, or a random-plan control, scored on the same sealed worlds.
K-NX2 bounds enumeration behaviorally (plans_built=8, kill at >=100), which
is evidence against the enumeration alternative, but it is a bar, not a
baseline comparison. H-CAUSALEXP-CONSTRUCT had memorization 0/2 vs mechanism
4/4 and simulation 35x-254x savings; DDES has no analogous numbers.

### Step 6: Alternative-explanation attack. COMPLETE.

The adversary's K1 was exactly this: static audit plus behavioral
instrumentation for hidden enumeration of candidate experiments.
ATTACK-FAILS; the zero-enumeration claim stands. K3 confirmed the disclosed
authorship (researcher-written guidance), which kills any future L3 reading
but confirms the L2 claim as stated. The strongest alternative explanations
(disguised menu, hidden enumeration, dedicated semantic cases) are defeated
on the current source.

### Step 7: OOD test. PARTIAL.

In-favor: World C (length 6) exceeds the predecessor's MAXD=5 bound; World D
observes a different variable (Z not Y); World F probes the t*=0 boundary.
These are genuine distribution shifts relative to the frozen A/B pair.

Missing: no broader OOD suite. Untested dimensions include more than 3
variables, rule arities beyond single-precondition chains, longer delays
(L>=8, which overlaps the deferred K-NX3 item), noisy or stochastic
observations, and hypothesis pairs that differ in structure rather than
timing. The mechanism has only ever seen 3-variable rule-delay worlds.

### Step 8: Ablation. MISSING.

No component has been removed to show it is load-bearing. Natural ablations:
arrival analysis replaced by a fixed heuristic; frontier argmin replaced by
first-variable selection; schema loop removed; eff_waits clamp removed
(post-repair). The K-NX6 source audit shows no dedicated cases, which is a
static property, not an ablation. For H-CAUSALEXP-CONSTRUCT the ablation
(48cf64979) was decisive (filter correctness-critical, simulation
efficiency-critical, MAXD correctness-critical). DDES has no equivalent.

### Step 9: Transfer/reuse test. MISSING.

DDES has never been applied outside the 3-variable rule-delay domain. No
test asks whether the arrival-analysis machinery transfers to a new action
vocabulary, a new rule format, or a new domain (compare H-CAUSALEXP-CONSTRUCT
transfer 486136c15, which was TRANSFER-PARTIAL, and the DDES design's honest
admission that the researcher owns the vocabulary and format). For a guided
generation claim, transfer of the guidance machinery is the natural step 9.

### Step 10: Independent red team. COMPLETE on the unrepaired build; STALE on the repaired build.

The adversary (5fd7ef448 to e40bdfc9b) was a genuine independent red team: it
found a real soundness hole (K2 ATTACK-SUCCEEDS), confirmed K1 fails, and
confirmed the L2 ceiling (K3). That is the red team working as intended.

But the red team attacked `56db8d606` (unrepaired). The repaired binary
(`ddesr.zag`, `17c97a2cd`) has not faced a fresh red team. The repair is
small and generic (eff_waits clamp), and K-R5 audits for new enumeration,
but a fresh adversarial pass on the repaired source is required before
promotion. The adversary's repair sketch was implemented verbatim from the
frozen repair prereg, which is good discipline, not a substitute for
re-attack.

### Step 11: Governance audit. MISSING.

No formal governance audit of DDES exists. H-CAUSALEXP-CONSTRUCT received a
full 11-step governance report with prereg/result ancestry checks, pure-Zag
and em-dash audits, and reproduction verification (FINAL_VERDICT.md).
DDES has builder disclosures (prereg sweep, one Python use for a byte check)
but no independent audit consolidating ancestry, purity, determinism, and
bar integrity. This step is procedural and should be straightforward given
the clean commit record.

## What remains, in information order

1. Sealed L>=8 depth run on the repaired binary (completes the deferred
   K-NX3 sub-bar; directly tests the "no bound" claim at a depth the
   predecessor could not reach).
2. Fresh red team on the repaired source (step 10 must cover the artifact
   being promoted, not its ancestor).
3. Independent reproduction from committed source by a non-author (step 4;
   cheap, standard).
4. Ablation of arrival analysis, frontier argmin, and the eff_waits clamp
   (step 8; identifies what is load-bearing).
5. Simple-baseline comparison on sealed worlds (step 5; memorization and
   bounded-enumeration controls).
6. Transfer probe to a new vocabulary or rule format (step 9; tests whether
   guidance generalizes or is domain-fitted).
7. Broader OOD suite beyond 3-variable timing worlds (extends step 7).
8. Formal governance audit consolidating ancestry, purity, determinism, and
   disclosures (step 11; procedural).

## Recommendation

Hold at BUILD-PASS plus REPAIR-PASS. Do not promote to SURVIVES until items
1 through 3 and 8 are complete at minimum; items 4 through 7 are the
substantive evidence the pipeline exists to demand. If all 11 steps pass,
the correct promotion is SURVIVES-AS-L2 (bounded), with the disclosed
researcher authority recorded in the verdict, not an L3 claim. The K3
finding permanently forecloses an L3 reading of this lineage: the plan is a
deterministic function of the hypothesis pair, and the guidance is
researcher-written. That is compatible with a bounded-L2 SURVIVES verdict
and is, in fact, the honest target the design doc set.

Note for the pipeline: the repair-after-red-team sequence worked correctly
here. The adversary found a real hole without voiding the frozen BUILD-PASS
(no frozen world had t*=0), the repair was preregistered before
implementation, and the sealed killer world became a regression test. This
is the process functioning, not failing.
