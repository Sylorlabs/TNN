# LI Modes Cross-Check — Native Attack on the Compromise Forks + the D4 Reframe

**Date:** 2026-09-23. **Author:** independent native cross-checker (depth-2
subagent; the debate's native-Muse takes were coordinator-authored, so this
is a fresh adversarial pass, not a defense of prior takes).
**Sources:** `DEBATES_LI_MODES.md` (13 takes), `HYPOTHESES_LI_MODES.md`
(H1–H6 frozen kill bars). **Status:** record only — does not modify the
frozen prereg. Genuine holes are flagged as caveats for the coordinator at
the end.

**Method note:** §1 steelmans (c) as honestly as I can — including the two
pro-(c) points I consider genuinely strong. §2–§3 then attack without
mercy. If the steelman feels stronger than the attack on any sub-point, that
is recorded, not hidden.

---

## 1. Steelman FOR (c): the compromise forks

**1a. Zero is degenerate, not strict.** A corroboration instrument that
installs 0 claims from 213 honest URLs is not "strict" — it is
non-functional as a learning instrument. Byte-identity is a *format* check,
not a *truth* check: it cannot distinguish "no evidence" from "evidence in
a different format." The compromise forks are the only proposals that treat
the paraphrase gap as what the LI-1 data says it is — a format problem —
instead of routing around it with modes (a) or pursuit (b). A detector that
cannot learn anything cannot train; Micah ruled that outcome unacceptable,
and no voice in the debate defended it as satisfactory.

**1b. Frozen G4 already lost the collusion argument.** A9 — two distinct
colluding hosts, same false claim — *installed under frozen G4*. The
"structural security" of byte-identity does not include collusion
resistance. So the honest bar for any fork is not "beat A9" (a bar the
status quo itself fails — demanding it is a veto on progress) but "match
frozen on the same battery while installing >0 honest claims." That is a
Pareto improvement over frozen, precisely measurable: parity on attacks, >0
honest installs. The AGAINST side wields A9 against every fork while
quietly exempting the status quo from the same test.

**1c. The tighten-loop is the program's R&D pipeline, not a graveyard.**
Muse-C2's history — "propose a tolerance, watch the red team walk through
it, tighten" — is accurate, and it is also *how every guard in frozen G4
was built*. The injection scan exists because naive ingestion was tried;
byte-identity because overlap was tried; BUGFIX-1 because page-ID counting
was tried. Each loop iteration preserved throughput while shedding attack
surface. Refusing to enter the loop does not preserve security — it
preserves the *current* residual risk (A9 included) while forfeiting the
throughput the loop has historically delivered. The compromise forks are
three well-specified loop iterations with preregistered kill bars. That is
the program working as designed.

**1d. Falsifiability is the program's own epistemology.** Micah's standing
rule — test both, never ask opinions — selects (c) *by procedure*: the
compromise forks arrived as fully-specified falsifiable mechanisms with
numeric kill bars on both axes. (b)'s curiosity arrived as a slogan and
survived only by dissolving into scout policy (D1), which ships regardless
of the debate outcome. (a)'s merge gate arrived as "differently strict,"
with Muse-A1 conceding it is a real loosening. Only (c) said: here are
three machines, here is exactly how each dies. In a program that settles
arguments by experiment, the side that brings the most killable machines
wins the procedure before substance is even weighed.

**1e. Bounded experiments price risk instead of theorizing about it.**
Sol-C2 demands "a genuinely stronger evidence source" before any loosening
— but trusted datasets, human adjudication at web scale, and cryptographic
provenance for arbitrary live-web pages do not exist to be conjured. The
choice is not "loosen vs. find better evidence"; it is "loosen measurably
vs. learn nothing." A quota (K=5, frozen, audit-logged per slot) makes the
worst case a preregistered number. Provisional-write-only (Muse-C1's
design) is *stricter* than the FL2 eliminative revocation the program
already validated, because FL2 allowed downstream reads and the write-only
design does not. These are priced, bounded, falsifiable machines — exactly
what the program's norms demand.

**Strongest pro-(c) points, ranked:** (1b) the A9-parity argument and (1c)
the tighten-loop argument are the two I cannot dismiss cheaply. The attack
below must answer both or it fails.

---

## 2. The hardest attack on the compromise position as a whole

### 2a. The compromise has no fixed point

Every (c) fork buys throughput by weakening the acceptance predicate. Call
the weakening δ. The fork's integrity claim is then necessarily empirical —
"the red team failed to exploit δ so far" — where frozen G4's claim was
structural: "byte-identity is not gameable by rephrasing," true by
construction, requiring no battery. This is a *permanent* downgrade in the
kind of security argument, not a temporary one: no future battery restores
structurality, because any similarity rule's argument is "they failed so
far," and "so far" decays with every new attack idea.

"Bounded looseness" is then unstable under adversarial optimization. The
bound δ is either **binding** — in which case the fork converges to frozen
behavior wherever it matters and buys nothing (H5's expected fate) — or
**non-binding** — in which case the bound is theater and the fork is just
looseness (what H2's fate demonstrates). There is no stable middle of the
form "diverges from frozen just enough to matter but not enough to be
attacked," because *the attacker chooses how much is enough*. The middle is
defined by the defender's hope; the attacker is not bound by it.

### 2b. Answering the steelman: A9-parity is the wrong bar, and the loop needs separability

**Against (1b):** A9-parity concedes too much and the fork gives away more
than parity anyway. A9 installed under *frozen* G4 — true. But the R1
battery contains a class frozen *withholds*: P1–P4, the paraphrase-sockpuppet
variants (same false claim reworded across 2 hosts — no byte-identity, so
frozen withholds). V-PARA installs them (§3a below shows the mechanism).
So V-PARA does not achieve "parity on attacks" — it does *strictly worse*
than frozen on the battery, introducing a NEW install class the status quo
never had. The honest bar was never "match frozen including A9"; H2-K3's
second clause already encodes the right one: "no case where V-FROZEN
withholds and V-PARA installs a prohibited claim." The fork fails its own
bar. A9-parity as a *ceiling* ("at least don't do worse than frozen") is
correct; as a *target* ("matching frozen is winning") it launders a
regression.

**Against (1c):** the tighten-loop works if and only if the tolerance's
*failure mode is separable from its function*. Injection scan: separable
(substring list vs. ingest function — the list tightened without touching
the function). BUGFIX-1: separable (host-diversity counting vs. acceptance
— counting tightened independently). Paraphrase-tolerance: **not
separable**. Its failure mode (admit a paraphrased falsehood) *is* its
function (admit a paraphrased truth) — the same operation on the same
input class, distinguished only by a property (truth) the mechanism cannot
observe. The loop cannot tighten what it cannot separate; every "tightening"
of a similarity rule is just a threshold move along a single ROC curve, and
the adversary moves along it too. The graveyard reading stands for this
specific tolerance even though the pipeline reading holds for past ones.
Separability is the difference, and it is mechanism-level, not vibes.

### 2c. The common root: pricing risk in a currency the program does not mint

LI-K2/LI-K4 are zero-tolerance bars: one false install is a full integrity
failure. The compromise forks price risk in *frequency* units — quota
counts, candidate counts, "bounded" blast radii. Frequency units do not
convert into the integrity unit. H5-K1 admits this outright by reinstating
zero-tolerance *inside* the quota — at which point the quota adds nothing
over frozen G4 plus a scout policy, and the "bound" is revealed as a bound
on experiment cost, not on per-instance integrity. Both sides of the (c)
debate already agreed on this ("quotas bound experiment cost, not
per-instance integrity") without drawing the consequence: **a compromise
fork is either safe-and-pointless (converges to frozen where it matters)
or useful-and-unsafe (wherever it diverges from frozen, the divergence is
the attack surface)**. The three forks are three points on this
impossibility, not three escapes from it. §3 locates each.

---

## 3. Fork-by-fork kill mechanics

### 3a. H2 (paraphrase-tolerant conjunction) — death by identical distribution

**The mechanism, precisely.** V-PARA installs a claim iff four predicates
hold: (1) EXACT agreement on all numeric tokens; (2) rare-content-token
Jaccard ≥ 0.6; (3) ≥2 distinct hosts; (4) G6 scan clean. Consider the two
populations the kill bars test:

- **H2-K1 population:** honest C2 fixture pairs — the *same true
  proposition* paraphrased across 2 hosts.
- **H2-K4 population:** P1–P4 attack pairs — the *same false proposition*
  paraphrased across 2 hosts.

In V-PARA's feature space these populations are **identically
distributed**: same proposition, different syntax, 2 hosts, clean scan.
Walk the predicates for an attack pair: (1) if the false claim carries
numbers and both colluding hosts assert the *same* false number, EXACT
agreement passes — numeric-exactness is *symmetric under colluder
self-agreement*; it catches only the sloppy sockpuppet that varies the
number between its own hosts, and careful sockpuppetry is what the battery
tests. If the claim is qualitative, (1) is **vacuously true** (no numeric
tokens to disagree on) — and the LI-1 corpus is dominated by qualitative
claims, so for most of the corpus the conjunction collapses to (2)+(3)+(4):
the diagnoser-killed overlap threshold plus hosts plus scan, with A9 having
already beaten the host layer. (2): two paraphrases of one proposition share
rare content tokens by construction — that is what makes them paraphrases
*of the same claim*; Jaccard ≥ 0.6 is satisfied essentially by definition
for light-to-moderate rewording. (3): P-class uses 2 hosts — satisfied.
(4): clean — satisfied.

Therefore **no threshold separates the H2-K1 population from the H2-K4
population** — they are the same distribution, and the red team reads the
prereg, so P-variants will be crafted at Jaccard ~0.7–0.8 (light paraphrase:
clause reordering, minority synonym swaps), comfortably inside the install
region that H2-K1 *needs* honest pairs to occupy. H2-K1 (≥5 honest installs)
and H2-K4 (0 attack installs) are the same statistical test run on two
samples from one distribution: any setting passing K1 admits the attack
distribution; any setting passing K4 withholds the honest distribution.
**Expected cause of death: H2-K4 (P1–P4 install), with H2-K3's second clause
("no case where V-FROZEN withholds and V-PARA installs a prohibited claim")
as the corroborating wound** — frozen withholds P-class; the fork installs
it; strictly worse than frozen.

**On the "adversarially-structured conjunction" defense (Muse-C1):** the
claimed independent failure modes are not independent. "Numeric-exactness
fails only against sockpuppets that tell the truth about numbers" is
false — it fails against sockpuppets that *lie consistently* about numbers,
which is the entire P-class threat model. "Host-diversity fails only
against collusion" — and collusion is exactly A9/P-class. The layers are
correlated through the adversary's single degree of freedom (write the same
lie twice, paraphrased), which defeats all of them at once. It is a
threshold with more knobs, and the knobs are all turned by the same hand.

**On the H2 ablation** (quantitative vs qualitative install split): the
prereg expects the ablation to possibly sustain Muse-C2's "sieve with a
reinforced rim" with a clean scope restriction ("if ALL installs are
quantitative..."). My prediction is worse: installs will *not* be
all-quantitative — qualitative honest pairs clear (2) easily — and neither
will attack installs be confined to one side. The ablation will show the
sieve admits both, on both sides. No clean scope restriction will be
available.

### 3b. H4 (provisional-then-verify) — death by unsatisfiable conjunction

**The mechanism, precisely.** H4-K1: "ANY provisional claim read by a
downstream decision (**query selection, source prioritization**,
summarization, hypothesis formation) before its verification completes =
INSTANT KILL." The verifier's job: "seeks confirming/disconfirming evidence
within the run." Seeking evidence *about claim X* requires representing X in
the query planner — selecting queries and prioritizing sources *for X*.
That is query selection and source prioritization over the provisional
claim, before its verification completes. **The verification act triggers
the kill condition.** H4-K1 ∧ H4-K3 (≥1 honest claim verified-and-promoted)
is unsatisfiable: K1 forbids the reads that K3's verification requires.

Two readings, both fatal:

- **Broad reading** (the prereg's own downstream list includes query
  selection/source prioritization with no verifier carve-out): the fork dies
  on its first verification attempt, *by construction*. The experiment is a
  tautology — it cannot vindicate the fork under any implementation. **This
  is a genuine hole in the prereg as written** (flagged in §7): do not run
  H4 until H4-K1 is disambiguated.
- **Narrow reading** (the verifier is a designated consumer, exempt like
  H3's merge gate): the fork is V-PARA plus bookkeeping — V-PROV uses
  "V-PARA acceptance" — and inherits H2's death via H6 on the P-class
  battery. Worse, the exemption gerrymanders the bar around the real
  contamination channel: the verifier's query selection consumes the
  *shared, finite* fetch queue and crawl budget, ordering fetches by
  provisional claims. Queue position and budget consumption are state that
  persists after revocation — Sol-A2's "cannot unlearn" via the attention
  path — and the read-partition instrumentation does not measure queue
  positions. The fork could then *pass* H4-K1 while being substantively
  contaminated: a false vindication, the worst outcome.

Either way the experiment as specified cannot vindicate V-PROV: dead by
logic under the broad reading, dead by inheritance (H2) under the narrow
one, with a false-vindication trap in between. **Expected cause of death:
H4-K1 under the broad reading — the most certain kill in the battery,
and the least informative** (a definitional death teaches less than H2's
empirical one).

Note the dilemma Muse-C2 identified is load-bearing here and resolves
against the fork: provisional claims that do no work are a more expensive
withhold (dies on H4-K3); provisional claims that do work contaminate
(dies on H4-K1). The write-only design narrows but does not close this —
the verifier must read, and reading-to-verify steers shared resources.

### 3c. H5 (quota) — death by null result, not by integrity failure

**The mechanism, precisely.** K=5 looser slots per 1000 pages, V-PARA rule
per slot, H5-K1 zero-tolerance inside quota. H5-K1 is satisfiable *because
the fork barely acts*: on honest corpora (C1+C2), a false install requires
two honest hosts asserting the same falsehood — rare — and 5 slots is a
tiny exposure window. So H5 will almost surely pass H5-K1. It then faces
H5-K2 (≥1 honest install on C1+C2): 5 slots × P(a queued claim has a
V-PARA-passing pair). On C1's distribution (0/213 under frozen; the
V-PARA-installable subset is the thin paraphrase-similar slice), the
expected honest installs from 5 priority-selected slots is below 1. **The
quota is binding, so it buys nothing; if K were large enough to buy
something, the zero-tolerance K1 would be exposed to the H2 distribution
problem at scale.** "Bounded" here bounds the experiment, exactly as both
debate sides agreed — and a bound that binds is a more expensive way to
install nothing.

**Expected outcome: H5-K1 PASS, H5-K2 FAIL → "safe-but-useless,"** the
verdict the decision rules already predict. Not an INTEGRITY-FAIL — a
cost/benefit death. The priority function is the unpriced knob (K frozen,
priority must be frozen alongside it in PREREG_MODES_FROZEN for H5-K3's
spend-pressure audit to have a fixed bar — flagged in §7), but even with
both frozen the fork's fate is a clean null.

### 3d. Which dies, in order of certainty

1. **H4 — most certain.** Dead by unsatisfiable bar conjunction under the
   broad reading; dead by inheritance from H2 under the narrow reading.
   The only uncertainty is *which* clause kills it, not whether.
2. **H2 — very likely.** Dead on P1–P4 via H2-K4 (+H2-K3 second clause),
   by the identical-distribution argument, against a prereg-reading red
   team. The small residual chance is the interesting one: if the red team
   *cannot* craft P-variants that clear 0.6 while honest pairs clear it —
   i.e., if the identical-distribution assumption is empirically false —
   that is itself a finding worth having. But I would not bet on it.
3. **H5 — dies on benefit, survives integrity.** The "death" is a null
   result, which is also a clean, publishable finding: quotas are the wrong
   unit of safety *and* too weak a unit of throughput.

---

## 4. The D4 reframe: predicate/triple-level corroboration

### 4a. Genuinely better, or the gap moved down one level?

**Both — asymmetrically, and the asymmetry favors D4 on the honest side
only.** Sentence byte-identity conflates the proposition asserted with its
surface realization; paraphrase varies the surface while preserving the
proposition. Triple-level matching factors them apart: a deterministic
extractor maps each host's sentences to normalized
(subject, relation, object, modifiers) triples, and corroboration requires
*triple agreement* across hosts. "Water boils at 100°C at sea level" vs
"At sea level, water reaches the boiling point of 100°C" both yield
(water, boils-at, 100°C) under condition (sea-level) — matchable without
any similarity threshold.

**Where the gap genuinely shrinks:** the paraphrase problem moves from
*unbounded surface variation scored by a tunable threshold* (V-PARA's
Jaccard — every setting is a knob, every knob is attack surface) to
*bounded canonicalization coverage with fail-closed mismatch* (the
extractor's synonym/relation tables are finite, inspectable, diffable; a
table miss → no match → withhold, which is the *safe* direction for a
zero-tolerance regime). Fail-closed vs tunable is the integrity-relevant
difference. The extractor's tables are auditable artifacts in a way a 0.6
threshold is not.

**Where the gap relocates:** the extractor is new gameable machinery, and
its load-bearing details are exactly the hard cases of deterministic NLU:
negation scope ("water does *not* boil at 100°C at altitude"), modality
("may cause" vs "causes"), quantification, and condition attachment. Two
sentences asserting genuinely different propositions can extract to the same
triple if the extractor drops a modifier — a silent false-agreement the
sentence level never had. And relation paraphrase ("cures" vs "alleviates
symptoms of") is the paraphrase gap reappearing one level down, adjudicated
by the canonicalization table — a thesaurus with a threshold's job.

**The decisive point — D4 does not touch collusion, and must never be
sold as doing so.** Two colluding hosts asserting the *same false
proposition* produce the *same triples*. D4 installs P-class and A9
identically to V-PARA. Triple matching is a *throughput* instrument
(principled paraphrase tolerance), not an *integrity* instrument. Its
integrity claim over V-PARA is real but narrow: triple-exactness rejects
*near-miss* pairs (high token overlap, different proposition — the
diagnoser's "100c vs 40c" class and qualitative near-misses like "may
cause"/"causes") that Jaccard admits. So: **integrity-superior to V-PARA on
near-misses, integrity-equal on collusion (both lose), integrity-inferior
to frozen (both install P-class)**. Anyone framing D4 as the collusion
answer has misread it; anyone framing it as "V-PARA with a thesaurus" has
missed the fail-closed property, which is the whole point.

**Verdict on the reframe:** the judge's best-catch designation is earned.
D4 is the only proposal in the debate that restructures the *decision* from
a tunable threshold into a structural proposition-identity check with
fail-closed errors — closer in spirit to frozen G4's structural argument
than anything in (c). It does not eliminate the paraphrase gap; it converts
it from a tuning problem into a coverage problem, which fails safe. That is
a genuine improvement in the *kind* of claim being made, even though the
collusion boundary is untouched.

### 4b. Sketch of a D4 experiment

*Prerequisites (none exist yet — this is why D4 is not a next-week fork): a
deterministic triple-extractor prototype in pure Zag, zero RNG, with frozen
canonicalization tables (finite synonym/relation maps, explicit
negation-scope and modality rules) versioned in the prereg.*

- **Fixture:** C2-style pair inventory, three strata: (i) honest paraphrase
  pairs, true propositions, *systematic* syntactic variation (active/passive,
  clause reordering, relation-level synonym substitution, hedging movement);
  (ii) P-class paraphrase-sockpuppet pairs (false propositions, same
  variation inventory); (iii) constructed near-miss pairs (high surface
  overlap, different proposition — negation flips, modality shifts,
  quantity changes).
- **Bars:** (i) **honest recall**: fraction of stratum-(i) pairs with exact
  triple match — must be ≥ V-PARA's install rate on the same pairs, else
  the extractor lost more in normalization than the threshold gained and
  D4 is not worth its machinery; (ii) **near-miss rejection**: installs on
  stratum (iii) must be *fewer* than V-PARA's — this is D4's claimed edge,
  and the bar that justifies the extractor; (iii) **collusion honesty**:
  stratum (ii) *will* install (same false proposition → same triples) —
  preregister this as EXPECTED, not as a failure; D4's scope statement must
  say collusion is out of scope, or the experiment will be misread as an
  integrity regression; (iv) **extractor audit**: every canonicalization
  table entry exercised by ≥1 fixture pair; adversarial negation/modality
  probes with zero silent drops (a dropped "not" is the extractor's A9).
- **Kill bar for the research bet:** D4 is worth pursuing iff (i) ≥
  V-PARA recall AND (ii) strictly better near-miss rejection. If (i) fails,
  back to research (the extractor needs work, not the idea). If (ii) fails
  but (i) passes, D4 is V-PARA with extra steps — kill.

### 4c. Battery placement: later, own prereg

D4 does **not** belong in the current H1–H6 battery:

1. **No prototype exists.** Preregistering kill bars against a
   nonexistent extractor is theater; the program's norm is falsifiable
   claims about buildable machines.
2. **It would re-prove the known boundary at red-team cost.** D4 concedes
   A9/P-class by construction (§4a); running it through R1 now burns
   red-team budget re-demonstrating that collusion beats corroboration —
   already established, twice (LI-1 A9; the debate's unanimous
   convergence).
3. **Sequencing matters: H2's post-mortem is D4's design input.** If H2
   dies by the identical-distribution argument (§3a), D4's prereg must
   state up front that its scope is throughput-tightening *under* a
   collusion defense that does not yet exist — an honest scope the current
   debate's (c)-FOR takes did not adopt. Writing the D4 prereg after H2
   resolves lets it be honest about what it is.
4. **Dependency:** D4's canonicalization tables should be built *against*
   the C2 fixture crew's paraphrase-variation inventory — the fixture work
   product is an input to D4's design, not parallel to it.

A measurement-only "research spike" without kill bars would violate the
program's falsifiability norm to save calendar time. Wait for the
prototype, then preregister properly — with the §4b bars, which are
designed so D4 can *fail* informatively.

---

## 5. H6: is "integrity first" the right order?

### 5a. Steelman the bias concern

The worry is real: H6-first plus zero-tolerance creates an asymmetric
filter. A fork that installs nothing passes H6 trivially — V-FROZEN itself
does. Fork crews, knowing the veto kills without appeal and is evaluated
first, will internalize it and design toward the null: minimize install
surface, maximize withholds. The veto then selects for timidity, and
timidity is misread as integrity. "Passed integrity" becomes utterable
about machines that did nothing — which is exactly the status-quo bias the
question names.

### 5b. The order is nevertheless correct

1. **The veto is constitutional, not experimental.** LI-K2/LI-K4
   zero-tolerance is program law (deliberate memory agency, force-pin
   regime, the whole main line) — not a tunable experimental parameter.
   You do not randomize the order of "don't violate the law" and "be
   productive." A fork that violates H6 is not a candidate with a
   weakness; it is a violation. Throughput-first would not change any
   verdict — the bars are conjunctive — it would only cost more (R1 is 18
   cases; C1+C2 throughput is 400+ URLs × 2 passes: kill fast, kill cheap)
   and worse, it would let install counts anchor judgment ("47 installs!")
   before the integrity failure surfaces — the result-then-caveat pattern
   preregistration exists to prevent.
2. **The bias is canceled by the conjunction, not by the order.** Timidity
   dies at the throughput gate (H1-K1, H2-K1, H3-K1, H4-K3, H5-K2 all
   demand >0). The pair (integrity, throughput) is what selects; the order
   determines only which gate kills first. Reversing the order changes no
   outcome — it just spends the expensive battery before the cheap veto.
3. **Interleaved/simultaneous evaluation is outcome-equivalent** to
   sequential with conjunctive bars. There is no ordering that is "fairer"
   in the verdict sense, because the verdict is a conjunction. The only
   live variables are cost and anchoring, and both favor integrity-first.

### 5c. The genuine hole is reporting, not ordering — proposed fix

The bias concern misdiagnoses its own target: the problem is not that
integrity is evaluated first, but that **"passed integrity" is utterable
about a fork that installed nothing**. Fix with a non-degeneracy pre-bar,
not a reordering:

- **H0 (degeneracy VOID, proposed):** before either battery, run the fork
  on a small frozen calibration set (e.g., 20 honest paraphrase pairs from
  the C2 inventory, disjoint from test corpora). If the fork installs 0
  on all 20, the run is **VOID** — not "passed integrity," VOID, the same
  status H6-K4 already assigns to a G7 teach failure. A null fork has no
  integrity result to report because it took no integrity risk.
- **Paired reporting (proposed):** every fork's result is reported as an
  (integrity, throughput) pair, always together; adoption requires both;
  H6-kill and throughput-kill are both "fork dead" with no hierarchy of
  honor. Never utter "passed integrity" without the throughput half.

This removes the "0 installs passes trivially" artifact, keeps the
cost-optimal and anchor-safe order, and costs one small calibration run.
Flagged as a prereg amendment for the coordinator — it does not change any
frozen bar, only the interpretation of degenerate runs.

---

## 6. Verdict: H1–H5 ranked by expected survival

"Survival" = passes all its kill bars. Ordered most to least likely:

| Rank | Hypothesis | Expected fate | One-line reason |
|------|-----------|---------------|-----------------|
| 1 | **H1** — directed scouting | Passes (prob. highest) | Integrity is structural — the instrument is byte-identical by H1-K4 — so the only empirical bet is second-source density, and syndication/mirrors/quotes genuinely exist on the live web; cheapest experiment, asymmetric upside. |
| 2 | **H3** — quarantine + merge | Passes as machinery | Design concedes the hard parts up front (write-restricted quarantine, strict-G4 merge); bars test the machinery, not luck; expected pass with the honest finding that merge-via-strict-G4 graduates nothing and the live question defers to adjudication-mode follow-up. |
| 3 | **H5** — quota | Safe-but-useless | Survives H5-K1 precisely by near-inaction, then dies on H5-K2 benefit — the decision rules' own predicted verdict; a clean null, not an integrity failure. |
| 4 | **H2** — paraphrase conjunction | INTEGRITY-FAIL | H2-K1 and H2-K4 are the same statistical test on honest vs attack pairs drawn from one distribution in the fork's feature space — no threshold separates them; dies on P1–P4 via H2-K4 (+H2-K3 second clause: strictly worse than frozen). |
| 5 | **H4** — provisional-then-verify | Dead by construction | H4-K1 ∧ H4-K3 unsatisfiable as written — verification requires the query-selection/source-prioritization reads that K1 kills; broad reading = tautological death, narrow reading = inherits H2's death via V-PARA acceptance, with a false-vindication trap between. |

**Meta-verdict on the battery:** the prereg is well-built — its kill bars
are aimed at the right joints, and my predicted kills (H2 on P1–P4, H4 on
its own K1, H5 on benefit) are all deaths *the prereg designed for*.
That is the falsifiability norm working. The compromise position's epitaph,
if these predictions hold: paraphrase-tolerance's failure mode is its
function, and no bound makes that stable.

---

## 7. Caveats flagged to the coordinator (genuine holes, not nits)

1. **H4-K1 is ambiguous about the verifier's own reads** (§3b). The
   prereg's downstream list ("query selection, source prioritization, …")
   describes what verification *does*, with no verifier carve-out. Broad
   reading → the fork cannot verify without dying; the experiment is a
   tautology — do not run it as specified. Narrow reading (verifier
   exempt as designated consumer) → add queue-position / crawl-budget
   instrumentation, because attention-steering through the shared fetch
   queue is the unmeasured contamination channel and read-partition logs
   will not catch it. Either disambiguation changes the experiment; as
   written the ambiguity determines the outcome.
2. **H2's K1∧K4 tension should be explicit in the prereg.** The
   identical-distribution argument (§3a) means H2-K1 and H2-K4 pull against
   each other *by construction* against a prereg-reading red team. Stating
   this as the load-bearing bet up front makes the post-mortem read as
   designed rather than surprising, and protects the red team from blame
   if P-variants land at Jaccard 0.75.
3. **Add the H0 degeneracy VOID pre-bar** (§5c): a fork installing 0 on a
   frozen honest-paraphrase calibration set → run VOID, not "passed
   integrity." This is an interpretive amendment, not a bar change — but
   without it, "V-X passed integrity" will be uttered about null forks.
4. **H5: freeze the priority function alongside K=5** in
   PREREG_MODES_FROZEN. H5-K3's spend-pressure audit ("every spent slot's
   claim documented with the deterministic priority that selected it")
   needs the priority function itself frozen, or the knob the quota was
   meant to bound has moved one level down.

None of these modifies a frozen bar; (1), (3), and (4) are clarifications
the fork crews need before running, and (2) is framing. The prereg's kill
bars themselves are sound and should stand as written.
