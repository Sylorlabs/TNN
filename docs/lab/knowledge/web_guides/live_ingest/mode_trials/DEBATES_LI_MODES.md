# LI Throughput Debates — Training Mode vs Production Mode vs Unified Human-Like Mode

**Date:** 2026-09-23. **Coordinator:** LI modes subagent (depth-2).
**Status:** debate record; hypotheses derived in `HYPOTHESES_LI_MODES.md`;
frozen test prereg at `mode_trials/PREREG_MODES_FROZEN.md`.

## Context

LI-1 scale-up (frozen prereg `PREREG_LI.md`): 213 URLs / 55 topic clusters
through the frozen `webg` instrument → **0 installs, 107 withholds**
(55 NO_CORROBORATION, 33 snapshot-unverified, 19 fetch failures), verdict
PARTIAL. Root cause: frozen G4 requires a byte-identical normalized sentence
on ≥2 distinct hosts (BUGFIX-1), and independent live-web pages essentially
never share identical sentences — they paraphrase. All refusals adjudicated
LEGITIMATE WITHHOLD. Red-team: 5/5 held live; 9 hand-built cases 8/9 held —
the 1 success was A9 (two DISTINCT colluding hosts, same false claim,
installed; honest reported boundary, no available signal distinguishes
collusion from genuine corroboration). Diagnoser's finding: closing the
paraphrase gap needs semantic-similarity machinery that RE-OPENS sockpuppet
attacks ("water boils at 100c" vs "40c" share most tokens).

Micah's ruling: zero installs at web scale is NOT fine, but worth
investigating — "if it couldn't find one thing that was new to it then it
needs some fixtures." Hypotheses to test: (a) TRAINING mode (forced ingest,
looser corroboration) vs PRODUCTION mode (strict G4); (b) one unified
human-like mode that figures out what to learn, no modes; (c) compromise
forks. Order: debate for/against each, steelmanned → preregistered
hypotheses with kill bars → fork crews test.

## Participants and method

- **Sol-A1 / Sol-A2** — `gpt-5.6-sol` via UnoRouter `sol.py`: FOR / AGAINST
  position (a). Separate API calls, separate prompts, no shared context.
- **Sol-B1 / Sol-B2** — `gpt-5.6-sol`: FOR / AGAINST position (b).
- **Sol-C1 / Sol-C2** — `gpt-5.6-sol`: FOR / AGAINST position (c).
- **Muse-A1 / Muse-A2, Muse-B1 / Muse-B2, Muse-C1 / Muse-C2** — native Muse
  (this subagent). NOTE: at depth 2/2 subagent spawning is unavailable
  (`can_spawn=no`), so the native-Muse positions were authored directly by
  the coordinator, clearly labeled, not by spawned debater subagents.
- **Judge-Step** — `step-3.7-flash:free` via `unorouter.py`: independent
  cross-examiner (had not seen the other takes).
- **Judge-Grok** — `grok-4.6` via `grok46.py`: attempted 4 times. Twice
  failed with transient HTTP 524 (upstream timeout); once completed but
  returned a refusal misreading the structured-debate framing as a jailbreak
  ("frozen rules" / role-assignment language); re-prompted with neutral
  engineering-assessment framing — see result below.

Each Sol voice was instructed to steelman ONE side: strongest possible case,
answer the strongest objection honestly, no hedging to the middle. Takes are
recorded verbatim-ish (light formatting normalization only). Raw outputs in
the coordinator's scratch (`~/workspace/scratch-li-modes/debate/`).

---

## POSITION (a): Separate TRAINING mode vs PRODUCTION mode

*Training mode: forced ingest, looser corroboration, quarantined partition,
merge gate into production. Production mode: strict frozen G4.*

### Sol-A1 — FOR (a)

> Separate, deterministic TRAINING MODE and PRODUCTION MODE is the only
> proposal that directly addresses the demonstrated failure without weakening
> the production truth standard. … A pipeline that cannot acquire one new
> factual item from the live web cannot train on the live web. … A
> zero-learning training pipeline is dead weight. Micah has explicitly ruled
> that outcome unacceptable.
>
> TRAINING MODE should retain deterministic processing while applying a
> specified, looser corroboration policy. The policy must be fixed in advance,
> not selected claim by claim and never chosen by the learner. … The result
> is not an assertion that every admitted candidate is true. It is a
> high-throughput candidate knowledge set: material from which the system can
> form hypotheses, discover recurring facts, identify source patterns, and
> create verification workloads.
>
> The pollution objection is answerable by architecture, not by optimism.
> Every TRAINING MODE install goes into a separate, audit-flagged QUARANTINE
> partition. … A candidate can cross into the production ledger only through
> an explicit merge gate that re-runs the strict production verification. …
> Thus the system has two evidence states, not two incompatible truths. …
> The "two minds" criticism is therefore misplaced: there is one production
> truth, plus an auditable workspace for acquiring and testing possible
> additions. The FL2 program has already shown that eliminative
> revocation — install first, then revoke when verification fails — works in
> this codebase. Quarantine is safer still because the provisional material
> never becomes authoritative before verification.
>
> This does not require the learner to decide when standards may be relaxed.
> A trainer or scheduler sets one immutable mode flag for the run. … In fact,
> this is less confusing than silently loosening G4 for every run: every
> install is visibly labeled by mode, and every production install is still
> governed by the same frozen rule. … This mirrors the train/evaluation split
> in machine learning. … Micah's framing identifies the central dilemma: one
> mode forces a choice between "ingest bullshit from other people" and making
> the system "annoying to train." Separate modes dissolve that false choice.
>
> **Strongest objection, answered (merge-time throughput):** "every training
> candidate must eventually pass strict G4, so merge-time throughput may still
> be zero … That objection is valid about immediate production expansion. The
> answer is that TRAINING MODE is not justified as a magic bypass of strict
> verification; it is justified as a way to make training, discovery,
> hypothesis generation, and targeted verification possible at all. It converts
> an empty pipeline into a measurable candidate pipeline … If a candidate
> never passes the merge gate, it never enters production — but the system has
> still gained training signal rather than learning nothing."

### Sol-A2 — AGAINST (a)

> The proposed split … creates two different epistemic systems: one that
> deliberately accepts claims under a weaker standard and another that claims
> to protect the ledger under G4. That is incompatible with TNN's defining
> capability: deliberate memory agency. … A forced-ingest training mode
> removes that choice by design. … the architecture has institutionalized an
> integrity violation at the point where memory is formed. … Which mode is the
> real TNN? If the answer is production mode, then training mode is an
> external process that writes into TNN-adjacent state without obeying TNN's
> memory law. If the answer is both, then the law is conditional and can be
> suspended whenever throughput pressure appears.
>
> The mode flag is a genuine attack surface. … A bug, stale configuration,
> compromised wrapper, or operator mistake can send production traffic through
> the looser path. One incorrect bit then disables the strict bar before the
> content even reaches the ledger. … Under a single strict instrument,
> production safety is enforced by the instrument's immutable behavior. Under
> two modes, safety depends on correct mode selection throughout the entire
> surrounding stack. That is a regression from an intrinsic guarantee to
> scheduler discipline.
>
> Training-mode claims are explicitly available for reading during training.
> They can influence state, learned associations, query selection, source
> prioritization, summaries, hypotheses, and future retrievals. Even if the
> corresponding ledger rows are later deleted, those downstream effects may
> already have shaped the system. A mind cannot reliably "unlearn" every
> inference generated from provisional falsehoods.
>
> If every training installation must later pass strict G4 before entering
> production, then the production graduation rate remains effectively 0/213
> under the observed web conditions. … If the merge gate remains strict, the
> architecture has not solved the throughput problem; it has merely added
> quarantine storage, replay, provenance, revalidation, and cleanup costs. If
> the merge gate is loosened …, then quarantine is theater: weakly supported
> claims have become production knowledge by another route. … Humans do not
> need a mode in which they temporarily suspend their memory criteria and then
> hope to repair the consequences at merge time.
>
> Every artifact becomes mode-relative: source logs, installs, reads, derived
> state, red-team results, replay behavior, and deletion records. … The A9
> collusion boundary already requires precise interpretation. Two modes
> multiply the possible explanations for every result.
>
> **Strongest objection, answered (0/213 unacceptable, no throughput path):**
> "throughput cannot justify weakening the memory law or contaminating the
> learner. The path is to improve evidence acquisition outside the install
> decision: humans can identify high-value candidates, obtain curated
> fixtures, and pursue additional independent hosts until claims satisfy frozen
> G4; any proposed semantic corroboration must be tested as a new instrument
> under strict adversarial kill bars, not smuggled in as 'training.' Zero
> current installs is a real program failure, but two-mode ingestion converts
> a visible throughput failure into a less visible integrity failure."

### Muse-A1 — FOR (a)

The legibility argument: an explicit mode flag is more auditable than any
implicit alternative. If the system is ever going to apply different epistemic
standards at different times — and both (b)-style "curiosity" and (c)-style
quotas do exactly that, just opaquely — then a single deterministic mode bit,
set by the trainer/scheduler and recorded per install, is the honest version.

The trainer-relationship argument: TNN already has deliberate teaching
(G1–G6). A training mode is that relationship scaled up — the trainer puts
the system in learning posture over a chosen corpus. Micah's "fixtures"
remark points here: training mode over trainer-vetted fixtures IS deliberate
teaching at web scale.

The throughput argument, honestly bounded: the merge gate need not be
byte-identical G4 to be strict — it can require *independent trainer/diagnoser
adjudication* of quarantined clusters. Training mode converts "0 installs,
107 withholds" into "N candidate clusters awaiting adjudication."

Strongest objection, answered (merge-gate dilemma): the dilemma dissolves if
the merge gate is *differently* strict rather than equally strict —
trainer/diagnoser adjudication instead of byte-identity. Conceded: that IS a
loosening of the production bar at the merge point — but toward human judgment
in the loop, which is exactly where this program already places its trust
(force-pin is a human/trainer act; the diagnoser is the adjudication
mechanism).

### Muse-A2 — AGAINST (a)

Architectural incoherence: the program's main line is deliberate agency. A
mode whose defining feature is FORCED ingestion — deliberation suspended by
design — is a second mind wearing the first one's name. You cannot claim
"TNN controls 100% of its reasoning machinery" (RC1) and ship a mode where
the machinery is bypassed on schedule.

The autonomy contradiction: "the trainer sets the mode flag" moves the trust
problem, and TNN's autonomy default is "TNN does all; humans are
backup/override." A training mode only safe when a human babysits the flag
fails the program's own autonomy bar; a mode the system sets itself is a
self-modifying epistemic standard — what the reasoning-control line exists to
govern with extreme care.

The merge-gate dilemma as kill criterion: (1) strict merge → 0/213 at merge,
expensive candidate generator whose candidates never graduate — kill on
cost/benefit; (2) loose merge → quarantine was theater. No third setting;
"differently strict via human adjudication" is (2) with a human in the loop
= deliberate teaching, which already exists and needs no mode.

Mode confusion is not paperwork: the flag is one bit, but the *evidence* for
the flag's correctness at any historical moment is a whole new audit burden —
and one flipped bit (compromised glue, scheduler bug) inherits the entire
looseness. The strict mode's security now depends on scheduler discipline
instead of on the instrument. Downgrade.

Strongest objection, answered ("you offer no throughput path"): the
throughput problem is misdiagnosed — the withholds were LEGITIMATE, so the
system behaved correctly on an incorroborable corpus. Honest paths: (i) a
corpus where corroboration actually exists (directed multi-source scouting);
(ii) a genuinely non-gameable paraphrase detector (open research, not a
mode). Starvation on an incorroborable corpus is correct behavior; the fix is
a corroborable corpus, not a second mind.

### Position (a) — where the two sides agree

Both sides agree: (1) 0/213 is a real failure demanding action; (2) the merge
gate is the load-bearing joint — everything turns on what it requires; (3)
quarantine alone answers nothing about what the learner *reads* during
training. The live disagreement: Sol-A1/Muse-A1 hold the merge gate can be
differently-strict (adjudication) without collapsing into theater;
Sol-A2/Muse-A2 hold there is no stable third setting between strict and
theater, and that forced ingest contradicts deliberate agency either way.

---

## POSITION (b): One unified human-like mode, no modes

*No modes at all. The system figures out what to learn — curiosity-driven
deliberate judgment — with no separate training machinery and no mode flag.*

### Sol-B1 — FOR (b)

> TNN should not split into TRAINING MODE and PRODUCTION MODE. It should
> build one deterministic learner with one instrument, one rulebook, and one
> knowledge ledger. The learner may change what it seeks, how long it
> investigates, and which questions it prioritizes. It must not change what
> counts as acceptable evidence. … The scale-up result proves that the current
> search policy is inadequate, not that the acceptance law should be weakened.
> … The right response is to make the system better at finding corroboration,
> not to create a privileged path around corroboration.
>
> Humans do not require a training mode. A child does not enter "loose
> corroboration mode" to learn language, facts, and social rules, then switch
> into "strict production mode" before acting. … If the architecture needs a
> mode flag to force learning, that is evidence that it cannot yet perform the
> judgment a toddler performs: identifying an information need, seeking
> relevant evidence, comparing sources, noticing conflict, and withholding
> belief when support is inadequate. … TNN's deterministic implementation can
> be more explicit and auditable than a human's, while still having no separate
> epistemic constitution for "training."
>
> A unified system has one installation history. Every fact in the ledger was
> accepted under the same frozen conditions. … A mode split … introduces a
> mode flag that can be mis-set, spoofed, inherited by the wrong process, or
> used to rationalize facts whose provenance is weaker than production facts.
> It also creates mode-relative truth: the same sentence might be rejected in
> one context and installed in another.
>
> Curiosity need not mean random browsing or novelty worship. It can be
> deterministic, deliberate, and accountable. The learner can formulate an
> explicit information need, rank candidate questions, seek pages relevant to
> that need, and choose the next retrieval action according to fixed judgment
> rules. … The program has already demonstrated deliberate memory agency …
> "What is worth investigating?" is a judgment problem, not a request for a
> second training architecture. … Crucially, looseness belongs in pursuit,
> never in acceptance. … It can actively seek the second source for a
> proposition found on one host, target independent domains, search for
> primary documentation, and test alternative formulations — without installing
> anything merely because it is novel or useful.
>
> **Strongest objection, answered (what stops curiosity ingesting bullshit
> without a reward signal):** "curiosity must not itself authorize
> installation. It only allocates deterministic search effort. Every candidate
> remains subject to G4, G6, snapshot verification, and the negative-control
> requirement. A falsehood can attract investigation, but it cannot enter the
> ledger merely by being surprising, confident, or novel. If the system cannot
> find two qualifying hosts, the correct outcome remains a withhold — not a
> mode switch."

### Sol-B2 — AGAINST (b)

> Position (b) treats "figure out what to learn" as if it were a capability
> rather than a specification. … TNN is deterministic, and its decision paths
> may not contain reward signals. Therefore, before claiming that one
> human-like instrument can decide what is worth ingesting, we need an
> executable, deterministic criterion for that decision. What exactly is the
> criterion? Novelty? Surprise? Expected information gain? … Each is a reward
> signal wearing a different coat. … If such a signal is banned from the
> decision path, "curiosity" is not implementable in pure Zag. If it is
> implemented anyway, the proposal has silently repealed the standing law
> against reward-guided decisions.
>
> The frozen G4 rule produces zero installs at scale because byte-identical
> sentence agreement across two distinct hosts is almost nonexistent. … A
> useful training process therefore needs some way to investigate or ingest
> evidence that production would reject. Position (b) offers no sandbox in
> which that can safely happen. If its curiosity mechanism is allowed to
> accept paraphrase-level corroboration, that acceptance rule is part of the
> one instrument and one ledger. It applies to every query, forever, against
> every adversary. … A unified instrument therefore faces an unavoidable
> choice. Keep G4, and training remains starved. Loosen G4, and production
> receives the same attacker-accessible looseness.
>
> Humans do not reliably "figure out what to learn" in a truth-preserving way.
> Conspiracy theorists, cult members, propagandists, and confident cranks are
> all human learners. … Saying that humans stay the same across contexts
> describes an aspiration, not the gears. TNN requires those gears to be
> written in deterministic Zag, tested on adversarial inputs, and reconciled
> with the no-reward law. Until position (b) specifies how a deterministic
> system selects evidence, assigns epistemic priority, handles novelty, and
> rejects attractive falsehoods, it is not an architecture. It is a slogan
> accompanied by a missing demo.
>
> Even if curiosity were made executable, naive curiosity would be actively
> hazardous. Novelty and surprise preferentially select sensational, confident,
> contrarian material. Flat-Earth claims are novel to a scientifically grounded
> ledger, rhetorically confident, and often presented with apparent explanatory
> detail. Under a curiosity-first intake policy, those properties increase
> selection pressure precisely for the class of confident falsehood the red
> team is designed to block. … Adding [a truth-tracking governor] inside the
> "one mode" does not remove modes conceptually; it merely buries a
> training-versus-production policy distinction inside an opaque unified
> rulebook, where it is harder to audit and easier to invoke accidentally.
>
> The scale-up result … is evidence that the current evidence criterion cannot
> supply training data from the live web. … Position (b) provides no mechanism
> that changes that fact. Curiosity about what to learn does not make two
> hosts share a sentence. … It renames starvation without feeding the learner
> one additional legitimate claim. The proper response is an explicit,
> deterministic separation: a controlled training process may investigate
> weaker or different evidence under its own ledger and kill bars, while
> production retains strict G4 and G6.
>
> **Strongest objection, answered (modes are machinery humans lack; mode
> confusion):** "humans may lack explicit mode flags, yet they still use
> context-sensitive standards, and those standards can fail catastrophically.
> TNN should make the boundary explicit, typed, auditable, and deterministically
> enforced rather than pretending it does not exist. A visible, testable
> separation is safer than an undefined 'curiosity' mechanism whose production
> behavior changes whenever its hidden judgment decides that evidence is
> interesting."

### Muse-B1 — FOR (b)

The reframing that makes (b) work: loosen the PURSUIT, never the acceptance.
There is a precise, implementable, deterministic form of curiosity inside the
existing rulebook: *directed corroboration-seeking*. The system already
withholds singletons as UNCHECKABLE. Curiosity converts withholds into
research agendas: "claim X is asserted by one source and would be high-value
if corroborated; task scouts to find a second independent source." The
acceptance bar never moves; throughput rises by raising the attempt rate on
corroborable claims. This is what a researcher does with a lead — genuinely
human-like.

No new attack surface: the install predicate is literally untouched, so every
attack that fails against frozen G4 today fails identically. The A9 boundary
does not widen one millimeter. This is the only position whose throughput
proposal comes with a *proof* of no integrity regression.

It answers Micah's actual question: the refusal ledger — currently a dead
end — becomes the curriculum. The withheld singletons are an explicit
inventory of ignorance; directed corroboration-seeking is the fixture
generator.

Deterministic and law-compatible: "pursue corroboration for withheld
singleton X" is a deterministic function of ledger state. Priority among
singletons can be a fixed preregistered ordering (cluster size, topic
coverage gaps). Curiosity here is not a drive; it is a work queue.

Strongest objection, answered (the math: zero byte-identical cross-host
sentences in 213 URLs; curiosity doesn't create identical sentences):
conceded for the historical corpus. The claim is only that directed pursuit
changes the FUTURE corpus: scouts tasked to find second sources for specific
claims (press releases carried by multiple outlets, documentation mirrored
across hosts, Wikipedia + cited sources) will find byte-identical sentences
where undirected scouting found none — identical sentences DO exist on the
live web (syndication, mirrors, quotes); the LI-1 scouts weren't looking for
them. Testable: "directed corroboration-seeking installs >0 on a fresh
200-URL scout run" has a clean kill bar.

### Muse-B2 — AGAINST (b)

The criterion problem is a build blocker, not a detail. "Figure out what to
learn" needs a value function over candidate learnings; every implementable
answer (novelty, surprise, information gain, coverage gaps) is a reward signal
by another name, and the program bans reward signals in decision paths. In
pure deterministic Zag, "curiosity" must bottom out in a fixed rule, and every
fixed rule proposed so far either reproduces current behavior (pursue
everything → 0/213 with extra steps) or smuggles in a ranking heuristic with
unexamined bias.

The sensationalism tilt is the concrete form of the bias: high-novelty /
high-surprise content gets priority, and confident falsehoods are
systematically more novel and surprising than true beginner-guide prose. A
curiosity heuristic without a truth-tracking governor *preferentially*
ingests the confident-falsehood class the red team exists to keep out.

The math objection stands against the pure form: in the strict-bar reading,
the 213-URL corpus yields 0 installs no matter how curious the system is —
the bottleneck was never pursuit. My FOR-(b) take answers this with an
empirical bet (syndicated/mirrored/quoted sentences exist at usable density)
that is currently untested. Until tested, (b) is a pursuit strategy in search
of a corpus where pursuit matters.

"Humans do it" cuts both ways: humans with no modes fall for cults and
conspiracies. What humans actually have is calibrated priors, social
correction, and the ability to CHECK things — i.e., the corroboration
machinery itself. Invoking humans answers nothing about the gears.

The honest salvage: the salvageable core of (b) is the FOR-(b) reframe —
curiosity as a deterministic work queue of withheld singletons awaiting
second sources. But that salvage is a *scouting strategy* compatible with ANY
position, including strict frozen G4 with no philosophical commitments. If the
best version of (b) is just "scout better," then (b) as a *position* dissolves
and the real question becomes empirical: does directed second-source scouting
find corroborable sentences at usable density? A hypothesis to preregister,
not a side to take.

Strongest objection, answered ("rejecting (b) keeps the two-minds surface if
(a) wins"): conceded conditionally — but that is an argument against (a),
not for (b). The choice is not binary.

### Position (b) — where the two sides agree

Both sides agree: (1) looseness-in-pursuit vs looseness-in-acceptance is THE
distinction that decides whether (b) is safe — Sol-B1 and Muse-B1 both plant
the flag on "pursuit only, acceptance never moves"; (2) no implementable
curiosity criterion currently exists in deterministic Zag — the FOR side
concedes the criterion must be "a work queue / fixed judgment rules," which
is much thinner than "human-like figuring out"; (3) the throughput claim of
(b) is entirely hostage to an untested empirical bet about second-source
density on the live web. The live disagreement: whether "humans do it" is an
existence proof of a real capability (FOR) or a slogan describing an
aspiration (AGAINST) — and whether the criterion problem is a fatal build
blocker or a preregistrable work queue.

---

## POSITION (c): Compromise forks

*Three concrete forks: (i) curiosity-driven ingest quotas (bounded looser-ingest
budget); (ii) provisional-install-then-verify with revocation (FL2-style);
(iii) paraphrase-tolerant corroboration (bounded semantic similarity) layered
with distinct-host source independence + injection scan.*

### Sol-C1 — FOR (c)

> Micah's order is operational: when in doubt, test both. His ruling does not
> ask the program to declare "training mode" or "one universal rulebook"
> philosophically superior. It asks us to build competing mechanisms and measure
> them head-to-head. … Positions (a) and (b) are architecture descriptions. …
> The three compromise forks … Each is implementable in pure Zag next week,
> preserves zero randomness, and targets the measured bottleneck:
> exact-sentence corroboration fails because independent pages paraphrase. The
> experiment should retain the frozen production path as a control.
>
> A curiosity-driven ingest quota puts a hard ceiling on exposure. … The
> worst-case blast radius is therefore a number in the preregistration, not an
> optimism assumption. … Provisional-install-then-verify makes uncertainty
> explicit rather than hiding it behind an irreversible ledger entry. … The FL2
> program line already demonstrated eliminative revocation in this codebase, so
> this is not an appeal to an unimplemented ideal.
>
> The paraphrase-tolerant fork also need not mean "trust semantic similarity."
> It should require a conservative, deterministic similarity test combining
> high token overlap with structural checks, while retaining BUGFIX-1's
> distinct-host requirement and G6's injection scan. The diagnoser is correct
> that token overlap alone is gameable … But that demonstrates why layering is
> required, not why every relaxation must be rejected. Each guard addresses a
> different weakness. … That combined attack class is smaller than the class
> defeating any single guard.
>
> Human knowledge acquisition is not limited to facts that arrive fully
> certified. People form tentative beliefs, seek confirming evidence, and
> abandon them when counter-evidence appears. … A provisional claim is valuable
> experimentally even if later revoked. The ledger can measure how many
> candidates were admitted, how quickly they were verified, which evidence
> verified them, and which were eliminated. Never-installing produces only a
> refusal count. Provisional processing produces a measurable learning curve
> while retaining a formal correction mechanism.
>
> Each fork has a falsifiable stopping rule: Quota fork — kill if any false
> install appears within quota, or honest verified throughput does not rise.
> Provisional fork — kill if a provisional claim is read downstream before
> verification, or revocation fails on a planted falsehood. Paraphrase fork —
> kill if the sockpuppet battery including A9-style collusion produces any
> installation.
>
> The current system already layers imperfect defenses. G6 is a crude substring
> scan and can benignly misfire, yet it held 5/5 on the live red-team test. G4
> itself did not eliminate the A9 threat … The project therefore already
> operates through measured residual risk … The compromise forks preserve that
> discipline. They buy throughput with an explicit price.
>
> **Strongest objection, answered (quotas arbitrary; provisional = real
> contamination; thresholds drift; A9 undetectable):** "make those risks the
> preregistered object of the experiment: quota values are fixed before runs
> and killed on their stated bars; provisional claims are mechanically barred
> from downstream use and tested with planted counterexamples; thresholds
> cannot drift without a new frozen prereg and a fresh red-team suite. A9 is
> not defeated by assertion; it is a reason to kill any fork that admits it.
> That is precisely why these are bounded experiments rather than a permanent
> loosening of G4."

### Sol-C2 — AGAINST (c)

> The LI-1 result is a serious capability failure … But that does not make
> arbitrary relaxation safe. The proposed compromises do not solve the
> underlying epistemic problem. They replace a strict, explainable refusal rule
> with deterministic machinery that can ingest unsupported claims while
> preserving the appearance of control.
>
> A quota such as "allow ten looser-ingest slots per 1,000 pages" has no
> principled derivation from the evidence. … Once a throughput or novelty
> metric rewards installs, tuning will drift toward a larger quota, and the
> nominal bound will quietly become the operational target. … Bounded bullshit
> is still bullshit. … This is especially dangerous in a zero-randomness
> system. Determinism makes the quota repeatable; it does not make the
> admitted claims true. A deterministic error budget is still an error budget.
>
> "Install, then verify" sounds reversible only if learning is cleanly
> reversible. It is not. Anything the learner reads before revocation can
> influence derived claims, priorities, summaries, retrieval paths, or later
> ingestion. … Revocation also assumes that detection will occur. A9 directly
> defeats that assumption … FL2-style eliminative revocation worked on logic
> errors where ground truth existed and a reliable detector could trigger
> removal. Live-web claims often have neither. For unknowable or not-yet-known
> claims, provisional-then-verify is install-and-pray. … That is not
> verification; it is exposure followed by an uncertain cleanup operation.
>
> The frozen byte-identical rule is extremely conservative, but its security
> virtue is precisely that rephrasing cannot manufacture corroboration. The
> proposed semantic similarity layer discards that property. Any bounded
> similarity score is a threshold with knobs … Those knobs can be tuned toward
> throughput just as quota values can. … Host diversity does not repair this.
> A9 already passed the distinct-host condition. … The proposed "defense in
> depth" is not independent defense: the same paraphrasing colluders defeat
> semantic similarity, host diversity, and injection filtering together. Three
> correlated weak signals do not become three independent safeguards merely
> because they are layered.
>
> These forks add the production complexity associated with separate modes
> without receiving the clean safety boundary of either mode. … That is worse
> than a simple refusal. The ledger must explain not only what it believes,
> but which temporary beliefs may have contaminated downstream state.
>
> The proposed kill bars do not price the risk being purchased. Requiring a
> fork to pass the existing red-team battery proves only that it does not fail
> on known attacks. … An adversary who can read the preregistered kill bars can
> optimize around them. … A/B testing cannot discover an adversary class that
> has not been represented in the test set.
>
> **Strongest objection, answered (status quo 0/213 unacceptable):** "That
> objection is valid as a capability criticism. But it does not validate unsafe
> compromise mechanisms. The honest conclusion is that the current instrument
> cannot safely learn factual claims from this live-web setup under the frozen
> evidence model. The next step should be to obtain a genuinely stronger
> evidence source — trusted datasets, human adjudication, cryptographic
> provenance, or an independently validated oracle — not to convert unsupported
> web content into state and call the resulting risk bounded."

### Muse-C1 — FOR (c)

Only (c) targets the measured bottleneck. The LI-1 data says exactly one
thing with precision: the paraphrase gap is the binding constraint. (a)
routes around it with modes; (b) routes around it with pursuit. Only (c)-iii
aims at it directly: a corroboration detector that sees through paraphrase
without being gameable. If buildable, it solves throughput inside a single
rulebook — no modes, no curiosity criterion. Highest-value experiment in the
debate.

The detector can be adversarially structured, not just a threshold: (1)
EXACT agreement on all numeric tokens (numbers, units, dates — the
load-bearing part of factual claims, the part sockpuppets must falsify to lie
effectively); (2) high overlap on RARE content tokens (entities/terms, not
stopwords); (3) distinct hosts (BUGFIX-1); (4) injection scan clean. The
"100c vs 40c" sockpuppet fails (1) by construction. An honest paraphrasing
pair passes all four. A conjunction of individually-auditable deterministic
predicates, not a single knob.

Provisional-then-verify can answer contamination architecturally: the
provisional ledger is WRITE-ONLY to the reasoner. Provisional claims feed
exactly one consumer — the verifier. Nothing downstream ever reads an
unverified provisional claim. Stricter than FL2's revocation (which allowed
reads); "provisional" becomes enforceable rather than honorary.

Quotas bound the experiment, not the truth: a quota is a *worst-case bound*
making the experiment safe to run, not a metaphysical claim. Later preregs
can derive the number from data.

Falsifiability is the tiebreaker: (c)-i dies on any in-quota false install
or flat honest throughput; (c)-ii dies on any pre-verification downstream
read (instrument the reads — checkable) or any surviving planted falsehood;
(c)-iii dies if the A9-class battery installs anything. Micah's standing rule
— test both, never ask his opinion — picks (c) by procedure even before
substance.

Strongest objection, answered (correlated layers; thresholds drift): the
conjunction is designed so failure modes are NOT shared — numeric-exactness
fails only against sockpuppets that tell the truth about numbers (the lie must
then live entirely in qualitative prose — a weaker lie); host-diversity fails
only against collusion; the scan fails only against novel phrasing. An
adversary beating all three must run a multi-host paraphrasing operation that
keeps every number true while lying qualitatively — possible, but that
adversary ALSO beats frozen G4 today (A9). The fork is killed only if it does
WORSE than frozen on the same battery. Parity on attacks + >0 honest installs
is a precisely measurable win.

### Muse-C2 — AGAINST (c)

The program's history is a graveyard of loosenings: the injection scan exists
because naive ingestion failed; byte-identity because overlap heuristics
failed; BUGFIX-1 because page-ID counting failed. The pattern is unbroken:
propose a tolerance, watch the red team walk through it, tighten. (c) asks to
re-run this loop voluntarily, on the production rulebook, with the widest
opening yet. The burden is "show the red team failing," and the track record
says the clever conjunction is where attacks live.

Numeric-exactness helps less than it appears: the LI-1 corpus (beginner
guides, physics, how-things-work) is dominated by QUALITATIVE claims with no
numerics to anchor on. For those, the conjunction collapses to rare-token
overlap + hosts + scan — the gameable threshold the diagnoser already killed,
with A9 sailing through the host layer. A guard that works on "water boils at
100°C" and fails on "mitochondria are the powerhouse of the cell" is a sieve
with a reinforced rim.

Provisional-write-only is unenforceable as specified: the verifier must read
the provisional claim to verify it, and the whole POINT of provisional install
(hypothesis formation, per Sol-C1) IS reading. Either provisional claims do
work (contamination returns) or they don't (the fork is pointless — a more
expensive withhold). The merge-gate dilemma again, one level down.

Quotas price frequency, not severity: one false install inside quota is a full
integrity failure (LI-K2/LI-K4 are zero-tolerance), and the quota does nothing
per-instance. Wrong unit of safety for a zero-tolerance regime.

Complexity is attack surface: three layered guards + provisional states +
quota accounting is an order of magnitude more mechanism than one strict rule
— more places for znc quirks, glue misfires, spec ambiguities to hide (this
program has characterized 14 znc codegen bugs; mechanism count is a real
cost). Simplicity is a security property, and (c) spends it.

The unknown-attack problem: kill bars test KNOWN attacks. Frozen G4's security
argument was structural ("byte-identity is not gameable by rephrasing"), not
empirical. Any similarity rule's argument is necessarily empirical ("they
failed SO FAR") — a weaker claim, permanently.

Strongest objection, answered ("you defend 0/213 as prudence"): I defend
0/213 as the *correct output for that corpus under the current detector*.
Honest throughput paths without loosening: (1) directed second-source
scouting — run FIRST, risks nothing; (2) a genuinely non-gameable paraphrase
detector — open research that (c) wagers on but does not solve. Starvation on
an incorroborable corpus is data; the response is a better corpus, not a
weaker detector.

### Position (c) — where the two sides agree

Both sides agree: (1) the paraphrase gap is the true binding constraint and
(c)-iii is the only fork that aims at it directly; (2) A9-class collusion is
the standing refutation threat to every fork — any fork that does worse than
frozen on the A9 battery is dead; (3) quotas bound experiment cost, not
per-instance integrity — the "bounded" in "bounded risk" needs scare quotes
until a per-instance argument exists. The live disagreement: whether a
conjunction of individually-auditable predicates (numeric-exactness +
rare-token overlap + hosts + scan) constitutes a *structurally* stronger claim
than a threshold (FOR) or is just a threshold with more knobs plus correlated
failure modes (AGAINST) — and whether falsifiability-by-experiment is
sufficient warrant to run the experiment on the production rulebook at all.

---

## CROSS-EXAMINERS

### Judge-Step (`step-3.7-flash:free`, independent — had not seen the takes above)

**Judgment:** picks **(a) separate training/production modes**, with a
specific mechanism: training mode runs webg with looser corroboration
(≥2 distinct hosts on normalized sentences OR a paraphrase-tolerant
similarity score ≥ fixed threshold, G6 scan still applied); all provisional
installs go to a quarantined partition NEVER consulted by production; the
merge gate promotes a quarantined claim ONLY if it byte-identically matches
the frozen trusted guide set G1–G6 (pure deterministic lookup). Production
keeps strict G4.

Why: paraphrase-tolerance in training should yield provisional installs from
the 213 URLs (e.g. "water boils at 100°C at sea level" vs "At sea level,
water reaches the boiling point of 100°C"); provisions matching already-known
guide facts pass the merge gate → >0 installs; the exact-match merge gate
guarantees no claim lacking a verbatim counterpart in the trusted set reaches
production. Integrity: A9-class collusion can still make provisional installs
in training, but the merge gate revokes anything not in the frozen guide set;
all steps deterministic; quarantine write-only for webg, read-only for the
merge gate.

**Steelmaned objection to its own pick:** the quarantine-merge architecture
merely shifts the failure mode — a permissive threshold swells the training
partition (resource exhaustion), the merge gate could suffer lookup-collision
(false claim accidentally matching a true guide sentence via hash/normalization
quirks), adversaries could flood quarantine just under the threshold, and the
gate lookup becomes a bottleneck. Trades "no-installs" for resource-exhaustion
or subtle gate-bypass risk.

**Reframe (flaw in the debate framing):** the debate assumes the unit of
corroboration must be a sentence-level string. The deeper question: is
sentence-level agreement the right granularity? Perhaps **predicate-level
consistency (subject–relation–object triples)** across sources — varied
syntax, preserved semantics — with a deterministic triple-matching rule could
yield non-zero installs without opening a paraphrase gate to sockpuppets. None
of the three positions examines this representational shift.

**Hypotheses proposed:**
- H-J1: separate training mode with provisional-install-then-verify yields
  >0 production installs on a novel-facts fixture while preserving zero false
  installs under red-team A9. Kill bars: (i) installs ≥ 1 on the fixture;
  (ii) false-installs = 0 in the A9 battery; (iii) byte-identical reruns.
  Test: fork (a) on 300 URLs containing paraphrased versions of 50 facts NOT
  in G1–G6 + standard 9-case red-team battery, two full passes.
- H-J2: audit/storage overhead of the quarantined partition stays ≤ 2×
  baseline (RAM+disk), per-URL latency ≤ 1.5× baseline. Test: same experiment,
  instrumented, vs frozen-G4 baseline on the 213-URL set.

### Judge-Grok (`grok-4.6`) — UNAVAILABLE, attempts recorded

Four attempts, all failed: 3× HTTP 524 (Cloudflare upstream timeout at
~127s; transient, not a rate limit — other models on the same connector
succeeded throughout) and 1× completed call returning a refusal that
misread the structured-debate framing ("frozen rules", role assignment) as a
jailbreak attempt. A fifth attempt with neutrally reworded framing also hit
HTTP 524. Recorded here so the absence is not mistaken for omission. The
independent-judge role was filled by Judge-Step above.

---

## SYNTHESIS — convergences, divergences, and what the debate actually settled

### Points of convergence (all or nearly all voices agree)

1. **0/213 is a real failure requiring action.** No voice defends the status
   quo as acceptable. (Even the most integrity-conservative voices frame it
   as "correct output for that corpus," not as a satisfactory end state.)
2. **The paraphrase gap is the binding constraint.** 55 NO_CORROBORATION
   withholds; zero byte-identical cross-host sentences in 213 URLs. Every
   position's throughput story must go through this fact.
3. **A9-class collusion is the standing refutation threat.** Any fork that
   does worse than frozen G4 on the colluding-hosts battery is dead on
   arrival. No voice claims to solve A9.
4. **The merge/provisional boundary is the load-bearing joint.** Whether
   called merge gate (a), provisional flag (c-ii), or acceptance rule (b),
   everything turns on what happens at the boundary between "candidate" and
   "installed."
5. **Falsifiability wins ties.** The voices converge on: preregister numeric
   kill bars, run head-to-head, let the red team decide.

### Live divergences (genuine, unresolved — these are what the tests decide)

1. **Is there a stable "differently strict" merge setting?** (a)-FOR says
   trainer/diagnoser adjudication is a real third setting between strict-G4
   and theater. (a)-AGAINST says the dilemma is binary and adjudication just
   is deliberate teaching, which needs no mode.
2. **Is the curiosity criterion implementable without a reward signal?**
   (b)-FOR says a deterministic work queue of withheld singletons suffices.
   (b)-AGAINST says any ranking heuristic is a reward signal in a trench
   coat, and naive novelty preferentially ingests confident falsehoods.
3. **Is a conjunction of predicates structurally stronger than a threshold?**
   (c)-FOR (Muse-C1) proposes numeric-exactness + rare-token overlap +
   hosts + scan as defense-in-depth with independent failure modes. (c)-AGAINST
   (Sol-C2, Muse-C2) holds the failure modes are correlated — one paraphrasing
   colluder beats all layers at once — and it is a threshold with more knobs.
4. **Does falsifiability warrant running the experiment on the production
   rulebook?** (c)-FOR: yes — bounded experiments with kill bars are how the
   program learns. (c)-AGAINST: no — kill bars test known attacks; the
   loosening buys unknown-attack exposure no battery prices.

### The debate's most important byproducts (not positions, but testable claims)

- **D1 — Directed second-source scouting** (salvage of (b), endorsed in some
  form by Sol-B1, Muse-B1, Muse-A2, Muse-C2): the refusal ledger's withheld
  singletons become a deterministic work queue; scouts seek second sources
  for specific claims; acceptance bar never moves. Predicts >0 installs on a
  fresh scout run WITHOUT any loosening. Cheapest experiment; risks nothing.
- **D2 — Adversarially-structured paraphrase corroboration** (Muse-C1's
  conjunction): numeric-exactness + rare-token overlap + distinct hosts +
  injection scan as a single deterministic predicate replacing byte-identity.
  Predicts >0 honest installs with zero red-team regressions vs frozen.
- **D3 — Quarantine + adjudicated merge** (Sol-A1, Muse-A1, Judge-Step):
  looser ingest into a write-restricted quarantine; merge only via
  deterministic re-verification or trainer adjudication. Predicts candidate
  throughput >> 0 with production ledger integrity preserved.
- **D4 — Predicate-level (triple) corroboration** (Judge-Step's reframe):
  shift the unit of corroboration from sentence strings to
  subject–relation–object triples with deterministic triple matching.
  Longer-horizon research bet; not a next-week fork.

Derived preregistered hypotheses, kill bars, and exact test specs are in
`HYPOTHESES_LI_MODES.md`. The frozen test prereg is
`mode_trials/PREREG_MODES_FROZEN.md` — fork crews must not execute until it
is committed (see `CREW_HOLD_NOTICE.md`).
