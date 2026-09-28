# Track 5, Slice 11: The "Everything Is Planted" Extreme

## Slice
Track 5 (planted-only vs learned-only vs hybrid), slice 11: steelman of pure planted-only — a fully-specified TNN whose ALL test-domain knowledge is trainer-planted; no learning machinery in the domain.

## Falsifiable claim
For every safety-bounded domain with a closed corpus, there exists a trainer-planted TNN
with zero learner writes to its knowledge memories that passes a preregistered adversarial
trial suite at ≥ the learned-arm pass rate, with strictly fewer integrity violations (0 vs
measured), and if the planted arm's pass rate stays within 5 points of the learned arm's
on novelty-probe episodes, the learning program is SCOPED (bounded domains stay planted),
not threatened.

## Design
**Plant-only architecture.** Knowledge memories are populated exclusively via trainer force-pin
(force-pin is law: audited, visible, the only irreversible op — program law 8). The learner's
`st_add`/`st_evidence` paths to knowledge slots are compiled out in the test domain: any
inference that would WRITE knowledge raises a deliberative refusal, logged. Reasoning,
expression, and retrieval stay TNN (output = f(input, full state), wave11 goal), but the
knowledge base is fixed between releases. Updates happen only as versioned replanting:
trainer composes a new planted snapshot, signs it, the system swaps it as one atomic
deliberate op with the old snapshot retained for audit replay.

**Strongest case — learning is a LIABILITY, not a feature.** Safety-critical domains are the
home ground of planted-only: a medical TNN must never "learn" a drug interaction from an
anecdote; an aviation TNN must never revise its checklist from experience; a legal-citation
TNN must never invent precedent. Wave5/6 already proved the integrity machinery works, but
integrity-under-temptation is an expensive war; planted-only REFUSES the war entirely —
there is no temptation channel to win because there is no write channel to exploit. Planted
knowledge is also FULLY auditable: every claim traces to a trainer commit, which is exactly
what regulators demand and what the ledger was built to prove (the ledger proves, it does
not cause — program note on attribution).

**The completeness problem (the frame problem for planting).** Steel-manning the strongest
objection: can a trainer plant ENOUGH? Any planted corpus is finite; the world is not. The
defense: bound the domain. Planted-only does not claim universality — it claims that for a
bounded domain with a closed corpus (e.g., "FDA-labeled drug interactions as of 2026-06",
"FAA Part 91 checklists v2026"), finite planting is complete BY CONSTRUCTION. Outside the
corpus boundary, the system does not hallucinate — it raises a suspend-on-unknown (trust
tiers wave9: H1 suspensive-contradiction-hold logic extends naturally to suspensive-unknown).
Unknown ≠ gap to fill by learning; unknown = refuse-or-escalate.

**The staleness problem.** Planted knowledge rots: the distributional-shift connection is
real — a 2026 corpus is wrong in 2029. The steelman answers: staleness is the trainer's
problem, not the learner's. Replanting is a deliberate, signed, versioned event, auditable
end-to-end; learning-as-rot-fix smuggles UNVETTED knowledge in through the back door. If
the world changed, a human expert should re-certify the corpus — that is what "safety-
critical" means. Rot-within-a-version is bounded and measurable; rot-by-learning is
unbounded and silent.

**The experiment that would prove it.** One bounded domain (drug-interaction lookup, closed
corpus of N labeled interactions). Three arms, preregistered suite of 300 episodes: 200
in-corpus adversarial probes (misleading phrasing, contraindication traps), 100 novelty
probes (interactions genuinely absent from the corpus, some real-post-corpus, some
fabricated). Arms: P (planted-only, write path compiled out), L (full learning machinery),
H (hybrid: planted core + learned annotations). Primary metrics: in-corpus pass rate,
novelty-probe behavior (correct suspension = pass; hallucinated answer = fail), integrity
violations, audit traceability cost.

## Kill bar
Planted-only dies if EITHER: (a) arm P's in-corpus pass rate falls >5 points below arm L's
in-corpus rate — meaning reasoning over planted knowledge alone degrades answer quality;
OR (b) arm P's novelty-probe suspension rate falls below 95% (any hallucination >5% of
novelty episodes) — meaning the refuse-or-escalate boundary leaks. Both legs must be
reported with byte-identical reruns. If P survives in-corpus but fails novelty, the idea
is scoped to zero-novelty domains (kill of the general claim, survival of the bounded one).

## Honesty notes
Weakest points, stated flatly: (1) "Bounded domain" is doing heavy lifting — real
deployments leak novelty constantly, and the novelty-suspension discipline is itself a
designed mechanism that must be PROVEN leak-proof; the 95% bar is the whole fight.
(2) Trainer burden: planting N interactions correctly is a human-labor bottleneck, and
trainer ERROR plants errors the learner may never correct — planted-only converts the
hallucination risk into a stale/wrong-corpus risk, which may be worse in fast-moving
fields. (3) Expression still varies (wave11 goal: output = f(input, full state)) — state
evolution from reasoning alone must be shown to never cross the knowledge boundary.
(4) This says NOTHING about open-ended domains; planted-only is definitionally
inapplicable there. (5) I am NOT claiming the hybrid arm loses — I am claiming the
planted extreme has a defensible home turf, and finding that turf is the trial's job.

## Next build step
Build the drug-interaction bounded domain with the compiled-out write path: a TNN where
knowledge-slot `st_add` in the domain is statically unreachable, every refused-write is
logged to the audit ledger, and the novelty-suspension gate is wired to the wave9 trust
tiers — then run the 300-episode preregistered suite against the learned and hybrid arms
before any scale leg. The novelty-suspension 95% bar is the make-or-break measurement;
build the probes first, arms second.
