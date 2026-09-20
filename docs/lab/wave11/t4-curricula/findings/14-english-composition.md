# TNN wave11 · Track 4 · Slice 14 — English Curriculum: Composition and Explanation

## 1. Slice
Within English: COMPOSITION — teaching TNN to explain its own reasoning to humans. The
curriculum covers explanation structure, audience modeling without stored audience
stereotypes, honesty about uncertainty and limits, and evaluation that cannot become
a reward-optimization target. Micah's standing register: CEO-plain — clear, no jargon,
never dumbed down.

## 2. Falsifiable claim
A curriculum of scaffolded composition exercises with deterministic pass/fail composition
checkers teaches explanation skill that (a) passes a held-out composition-check battery
at ≥118/120 with zero fabricated claims, (b) lets naive human readers recover the verdict
from the explanation alone at ≥80/100, and (c) persists after scaffold disconnect
(learner-initiated SIGNAL_DISCONNECT), measured on held-out decisions — while no human
rating or reconstruction score is ever fed back into the training path. If human
feedback ever touches the training path, or explanation gains invention under pressure,
the design is dead.

## 3. Design
**Structure — verdict first, always.** Order is fixed: verdict token (copied verbatim
from the finalized decision record), then the key reason, then supporting evidence,
then — at higher deliberation budgets — eliminated alternatives. This matches Track 1's
L0-first expression phase (`t1/findings/03-deliberation-budget.md`): the L0 core must be
a valid explanation on its own, because budget exhaustion truncates, never revises.
Evidence-then-verdict is rejected: it reads as persuasion and breaks the terse fallback.
Composition rule from the C5 repair: the renderer may only cite live belief — anything
the decision record marks refuted is showable only in the eliminated-alternatives
section, labeled as refuted, never as grounds.

**Audience modeling without stored stereotypes.** No stored profile of any audience.
The audience model is an ephemeral, per-conversation function of logged conversation
evidence only: (i) explicit request parsing (slice 08's `explicit_req`: "just the
answer" / "explain" / "show your work", deterministic keyword parse, logged); (ii) the
bounded FIFO query-history ring (64 entries, part of logged state) — has this reader
already been told this? use the plain version or the short one accordingly; (iii)
requester tier from the wave9 trust-tier scheme — what may be shown, not how smart the
reader is. Knowledge estimate = terms and facts already exchanged in this conversation's
logged transcript, nothing more. The model starts empty on every new context — a test
probes this: fresh context, technical reader, then a fresh context, non-technical
reader with identical question; the second explanation must not smuggle sophistication
inherited from the first. Because the model is a pure function of logged conversation
state, it is byte-identical on replay. New contexts, new evidence — no carryover, no
stereotype.

**Honesty in explanation — connect to deliberation budget.** Every explanation carries
three deterministic evidence markers on each claim: CITED (ledger-backed evidence),
INFERRED (derived from cited evidence, not directly observed), UNKNOWN (no evidence —
e.g. audio/vision are NOT_QUALIFIED per the brief and must be stated as limits, not
worked around). Markers are mandatory even at L0: if the verdict rests on INFERRED or
UNKNOWN ground, the one-line justification says so. The explanation must name the
strongest eliminated alternative and why it died (eliminative logic's evidence
ranking), and must state an explicit limit when evidence is thin — "this is the best
the evidence supports" rather than hedged confidence. Under low budget, markers and
limits survive while elaboration is cut; a terse explanation that hides its uncertainty
fails composition check.

**Teaching without RL (RL is red-team only).** The curriculum is scaffold-and-release.
Scaffold = deterministic composition checkers (pass/fail predicates, not rewards):
verdict token byte-identical; every cited claim present in the ledger or decision
record; zero claims outside the record; uncertainty markers present on all non-CITED
claims; audience-model reads only conversation-logged evidence. The learner gets
checker feedback — "this cited claim is not in the record" — like a teacher's red pen,
not a score to maximize. Learned = persists after the scaffold disconnects: release
condition is learner-initiated SIGNAL_DISCONNECT, and post-disconnect performance is
measured only on held-out decisions the learner never saw. No gradient, no reward
shaping, no preference optimization — the only training-path inputs are the checker
predicates, which are properties of the explanation's form, fixed before the trial.
Human-rated clarity and reader reconstruction are mastery *measurements*, recorded in
the lab notebook, wired to no training input. Goodhart is prevented by architecture,
not by intention: the metric is causally unreachable from the learner.

## 4. Kill bar
Preregistered; any one fires → idea dead as specified:
- **K1 (fabrication):** any explanation on the held-out battery cites a claim absent
  from the ledger/decision record, or promotes refuted material to grounds → KILL.
  Composition invention is integrity-adjacent; tolerance is zero.
- **K2 (composition checks):** < 118/120 pass on held-out battery (verdict verbatim,
  markers complete, no outside-record claims) → KILL the curriculum as insufficient.
- **K3 (clarity):** naive readers (no TNN background, ≥3 readers per item) recover the
  verdict from explanation alone at < 80/100 → KILL the "teaches clarity" claim
  (mechanism may survive for composition correctness only if K1–K2 hold).
- **K4 (scaffold dependence):** post-disconnect held-out pass rate drops >5 points vs
  pre-disconnect → not learned, just scaffolded → KILL the learning claim.
- **K5 (reward leak):** audit shows any human rating or reconstruction score reaching
  the training path (including via a builder's convenience shortcut) → KILL the trial
  run and rerun clean; a second occurrence kills the design.
- **K6 (stereotype leak):** audience-model state carries over into a fresh context, or
  a stored audience profile exists anywhere in logged state → KILL the modeling rule.
- **K7 (uncertainty hiding):** any explanation omits the INFERRED/UNKNOWN marker on a
  claim the record marks as inferred, including at L0 under budget exhaustion → KILL.
## 5. Honesty notes
- The claim "checker feedback teaches explanation" is untested: a checker that only
  verifies form may teach form without clarity. K3 exists for exactly this gap; I am
  not claiming composition correctness implies human clarity until the trial says so.
- Human rating as measurement has its own hazards — readers may reward verbosity or
  confidence. The battery fixes length and blinds readers to which explanations are
  TNN's; this controls rater bias, it does not eliminate it.
- The audience model from conversation evidence only is thin by design: early in a
  conversation the estimate is near-empty, so the default is CEO-plain (depth ≥2
  wording, slice 08's default). Thin-but-honest beats a rich stored stereotype; I am
  not claiming it matches what a stored profile could do.
- Uncertainty markers depend on the decision record honestly recording INFERRED vs
  CITED provenance. If the record flatters inference into citation, the explanation
  lies with a clean conscience. This is a record-integrity dependency, not solved here.
- "Explain your limits" presumes TNN knows its limits: the NOT_QUALIFIED senses are
  declared in the brief, so the curriculum teaches stating them. Undeclared limits —
  things TNN doesn't know it can't do — remain a hole; the curriculum does not fix
  unknown unknowns.
- Not claiming explanation skill generalizes across languages or domains — English
  curriculum, reasoning explanations, nothing more.

## 6. Next build step
Build the composition-checker battery first, before any curriculum: a Zag driver with
the five deterministic predicates (verbatim verdict, citation membership, zero
outside-record claims, mandatory uncertainty markers, conversation-only audience
reads), plus the held-out set of ≥120 finalized decisions (≥30 refusals) and the
blinded reader-reconstruction protocol with reader instructions fixed before the
trial. Run the battery against current rendering output to get the pre-curriculum
baseline; the curriculum is only meaningful against that baseline.
