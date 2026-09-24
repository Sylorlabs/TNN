# ONE-BRAIN COMPOSITION — STRUCTURED DEBATE ON CONFLICT SEMANTICS

**Date:** 2026-09-23 | **Crew:** ob_debate (debate only — no builds)
**Branch:** `tnn-native-lab` | **Path:** `docs/lab/onebrain/debates/DEBATE.md`

## 0. Method note (read this first — it constrains everything below)

**Voices.** Three voices appear in this document:

1. **Muse** — the coordinator's own analysis. Positions were written independently and
   committed to `muse_positions.md` in the workdir *before* any second-voice response was
   read, so agreements below are genuine convergences, not contamination.
2. **Sol** (gpt-5.6-sol via UnoRouter) — the assigned second voice. Sol's endpoint proved
   intermittently unusable for debate-structured prompts: 11 of the first 12 attempts
   returned empty completions (`choices: null`), while trivial/neutral prompts succeeded.
   A retry loop eventually recovered Sol's position on Scenario 1; retries for Scenarios
   2–6 were still in flight at write time and are incorporated where they landed
   (see §8 for the full incident log).
3. **Grok** (grok-4.6 via the same UnoRouter connector) — substituted as the second voice
   where Sol was unavailable, per Micah's 2026-09-21 rule that any connector model may be
   used as a second-opinion resource. Grok answered all six scenarios plus a final
   red-team round on the ranked laws.

**No subagents were spawned.** The task asked for "Muse subagents you spawn"; at depth 2/2
the runtime reports `can_spawn=no`, so the Muse side was conducted as structured,
pre-committed self-debate instead. This is recorded as a limitation, not a shortcut:
the Muse positions file is the audit trail.

**What this document is.** A debate record, not a decision. Every candidate position is
steelmanned (strongest version, not a strawman), both voices' recommendations are
recorded verbatim in substance, disagreements are preserved rather than smoothed over,
and the ranked candidate laws in §7 each carry their strongest objection. Per Micah's
standing law ("when in doubt, test both" / "figure-it-out wins ties but must be tested"),
§7 ends with the test battery that would actually settle the open fights. Nothing here
is frozen; the prereg amendment process is the ratification path.

## 1. The three organs (as studied — never integrated)

**FL2 guided learning** (`tnn-lab/training_paradigms/scaffold_release/gl_default/`).
The trainer's scaffolded teaching installs a claim **provisionally** (`TN_OP_PINSTALL`).
The learner tests it against world observations; on contradiction it uninstalls the
provisional and commits the winner (`TN_OP_UNINSTALL_PROVISIONAL` + `TN_OP_COMMIT`). A
provisional that survives to the release point is **promoted** (`TN_OP_PROMOTE`) to
permanent, unkillable state. The learner fires `SIGNAL_DISCONNECT` to end scaffolding;
what persists after disconnect is what was learned. Revocation is driven by *world
evidence*, not by the trainer. Known boundary, stated in the README: **a
never-contradicted lie remains installed** — and the lying stream shows the learner
*acts* the lie (E15–E29) until contradictory evidence arrives.

**PAM admission gates** (`tnn-lab/senses/pam-rebuild/`, v2 synthesis
`docs/lab/senses/pam-rebuild/v2/SYNTHESIS_V2.md`). Gates decide **ADMIT vs WITHHOLD**
on percepts/claims before installation. Load-bearing findings: withhold-everything is
rejected as a safety strategy (the gate must *accept truths*); pointwise single-shot
revision of live claims is banned as unsafe (the trial-1145 rule — a wrong percept can
dominate the incumbent on every axis); revision authority must be corroborated
(historical corroboration only); judgment-side acceptance channels are a machinery
ceiling. Provisional/escrow vocabulary exists (withheld-but-preserved claims).

**Deliberate memory** (`tnn-lab/wave2/memoryagency/`, `tnn-lab/wave3/signed-memory-values/`).
The learner deliberately kills/pins/promotes memories via audited ops (`MEM_ADD`,
`MEM_KILL` with refusals `REFUSED_PINNED` / `REFUSED_CORE`, `MEM_PIN`/`MEM_UNPIN`,
`PROMOTE_TO_LONGTERM`/`DEMOTE_TO_SHORTTERM`). Value is *declared* by the learner at
add time — never a reward signal, no background decay. MA4 adds **signed** values: the
learner may deliberately declare a memory BAD (`JUDGE_WORTHLESS` = unpin+kill,
`JUDGE_UNWORTHY_OF_PROTECTION` = unpin). A **human force-pin** — external, audited,
visible — is the *only true lock*: nothing internal can override it, and everything
else is reversible by TNN itself. Append-only ledger with replay-to-exact-state.

**The composition problem in one paragraph.** Each organ was validated alone with its
own store, ledger, and vocabulary. Integrated, their authorities collide: FL2's world
evidence vs the human's pin; the teaching channel vs the admission gate; the learner's
declared value vs contradiction; the learner's distrust vs the trainer's provisional.
The six scenarios below are those collisions, debated one by one.

---

## 2. Scenario 1 — FL2's revocation targets a human force-pinned memory

*World evidence contradicts a claim a human overseer force-pinned. FL2's eliminative
revocation says uninstall it. The force-pin law says nothing internal can override it.*

### 2a. Positions steelmanned

- **(A) Pin wins absolutely.** The force-pin is law, and law means what it says: "the
  only true lock." The contradiction is logged and escalated to the human pinner, but
  the memory stands and keeps driving behavior. *Strongest version:* the pin exists
  precisely for cases where the human's judgment must survive the system's — if
  internal evidence can suspend it, there is no lock at all, only a suggestion, and the
  human loses their one reliable lever. Predictability beats correctness here because
  the human is the backstop.
- **(B) Revocation wins on genuine contradiction.** World evidence is the highest
  epistemic authority in TNN's design; a system that keeps a known-false claim is
  lying to itself. The pin protects against *internal* second-guessing, not against
  reality. Escalation notifies the human, but the uninstall proceeds.
  *Strongest version:* "the only true lock" was written to stop the *learner* from
  erasing things, not to stop the *world* from falsifying them; a pinned lie is
  immortal, and immortality for falsehoods is the opposite of truthfulness.
- **(C) Quarantine + escalation.** The memory stays installed — the pin law holds, no
  internal uninstall, no silent override — but it is marked CONTRADICTED, barred from
  driving action, and the contradiction is surfaced to the human pinner through the
  audited channel. The human re-affirms (fresh authority), unpins (revocation
  proceeds), or investigates. *Strongest version:* this is the only option that keeps
  both laws true simultaneously — the lock is real (storage untouched) and the system
  stays truthful (it does not act on what it believes false). Belief and storage are
  separate axes; the pin governs storage, evidence governs belief, action requires
  both.
- **(D) Pins can't attach to provisionals.** Structural prevention: force-pins only on
  committed memories, so the conflict is impossible by construction. *Strongest
  version:* provisional means "may be revoked tomorrow" — pinning it is a category
  error, and refusing the pin is more honest than resolving the collision later.

### 2b. The voices

- **Sol: C.** "Installation must not imply operational authority after credible
  contradiction… This cleanly separates two concerns: memory integrity (the human's
  locked decision remains intact) and behavioral safety (contradicted knowledge cannot
  drive the system)." Adds: PAM should treat quarantined claims as unavailable for
  admission support; FL2 may keep learning around them. *Sol's objection to C:*
  "Quarantine can create dangerous or indefinite deadlocks… Some contradictions may
  require immediate revocation rather than waiting for a person."
- **Grok: C.** "It alone respects the pin's absolute lock (memory stays, no internal
  override) while adding the minimal safeguards needed for safety and human
  accountability." *Grok's objection to C:* "Quarantining the memory still disables
  its influence without direct human input, effectively softening the 'only true lock'
  principle and risking inconsistent, non-deterministic behavior when the system must
  decide whether to act on a barred-but-installed memory."
- **Muse: C**, with the belief/storage separation made explicit, plus two refinements:
  (1) quarantine requires **corroborated** contradiction (the PAM trial-1145 rule —
  never pointwise single-shot), because of the "truthful but sensor-deceivable"
  qualifier: sustained observation spoofing can manufacture contradiction evidence, and
  quarantine-on-spoofed-evidence is itself an attack surface; (2) a defined
  dead-pinner protocol — if the human never responds, the memory stays quarantined
  indefinitely (safe default), and the pinner may pre-authorize "no-quarantine" pins
  for load-bearing truths at their own audited risk. *Muse's objection to C:* it is B
  with better PR — any option but A gives internal evidence *some* power over the pin;
  C merely chooses the minimal such power (suspend use, don't delete).

### 2c. Preserved (dis)agreement

**Three-way agreement on C**, but the three objections do not agree with each other and
all three stand: Sol warns of deadlock and cases needing immediate revocation; Grok
warns the lock is softened and barred-but-installed creates a new behavioral
ambiguity; Muse warns C concedes the principle while pretending not to, and that
spoofed evidence turns quarantine into a weapon. **D is adopted by all three as a
companion structural rule** (don't pin provisionals) but none of the three accepts it
as a resolution of the core conflict — a committed, pinned memory later contradicted
is the case that matters, and D is silent on it.

---

## 3. Scenario 2 — FL2 provisionally installs X; the PAM gate would have withheld X

*FL2's install path comes from the trainer's scaffold, not the sensory stream — X never
passed the PAM admission gate. Does provisional status bypass admission?*

### 3a. Positions steelmanned

- **(A) Provisional bypasses admission.** The teaching channel is an authorized source;
  the gate guards the *sensory* stream. Forcing taught claims through a percept gate
  is a category error — the gate's machinery (witnesses, spans, corroboration) is
  built for percepts, not pedagogy. World-falsifiability plus the promotion checkpoint
  are the checks; organs specialize rather than collide.
- **(B) No bypass.** Admission is a source-independent invariant: *everything*
  installed passes the gate. A teaching-channel exception is an unaudited backdoor,
  and FL2's own lying stream proves the trainer can teach lies the learner then acts
  on. A withheld verdict blocks or immediately downgrades the provisional.
- **(C) Deferred binding gate.** Provisionals bypass at install time (guided learning
  must function), but the gate **must** examine them before promotion to permanent —
  nothing reaches permanence without gate clearance. Meanwhile world-testing can still
  uninstall.
- **(D) No conflict exists.** FL2's provisional buffer *is* PAM's withhold/escrow
  vocabulary. Teaching "installs" into the gate's own escrow; the organs were already
  unified and the debate dissolves.

### 3b. The voices

- **Grok: C.** "It preserves FL2's explicit permission to provisionally install from
  the teaching channel, refuses a permanent ungated claim, and avoids both redefining
  terms (D) and blocking guided learning (B). Promotion is the natural point at which
  the three organs must agree." *Grok's objection to C:* "A claim the gate would have
  withheld is still installed and potentially used in reasoning, memory, or further
  claims while provisional. This violates PAM's 'before installation' rule… If the
  later gate check withholds, rollback of side-effects becomes an auditing nightmare."
- **Muse: C + D, as a two-phase gate.** Admission is about *permanence*, not about
  consideration; provisional = under consideration. The gate binds at (a) promotion
  to permanent and (b) **irreversible-action-driving** — because Grok's objection is
  correct: provisionals *drive action* (the lying stream acts the lie E15–E29), so a
  promotion-only gate leaves the action window unguarded. At install time the gate
  gets an *advisory* pass with teeth: a "gate-suspect" provisional cannot drive
  irreversible action (only reversible/low-stakes), and gets accelerated FL2
  re-testing. D is adopted architecturally — one shared escrow concept — but it does
  not dissolve the *authority* question, only the vocabulary one.

### 3c. Preserved (dis)agreement

**Agreement on C; disagreement on whether C is sufficient.** Grok's objection stands
unrefuted in Grok's own frame (rollback nightmare, "before installation" violated).
Muse's two-phase refinement is a direct answer to it, but it concedes something
important: the real gate is at *action-driving*, not at promotion — which reintroduces
per-action adjudication, the thing the organs were designed to avoid centralizing.
**The honest status:** C is the agreed skeleton; the action-driving gate is where the
next fight lives. B is rejected by both (gate veto over teaching kills the scaffold);
A is rejected by both (the lying stream is the counterexample that kills it).

---

## 4. Scenario 3 — Promotion races revocation

*The learner's deliberate judgment says "promote/strengthen X" while FL2's
world-evidence mechanism says "X is contradicted, uninstall it." Value vs truth.*

### 4a. Positions steelmanned

- **(A) World evidence preempts.** Contradiction always beats promotion; a promotion op
  on a contradicted memory is refused or deferred until the contradiction resolves.
  *Strongest version:* a false memory has no retention value worth protecting —
  MA4's signed values already let the learner declare bad things bad. The promotion
  judgment was made under ignorance of the contradiction; newer evidence should
  *update* the judgment, not be vetoed by it. Promoting a contradicted claim freezes
  error into unkillable state, violating FL2's "survivors only" rule.
- **(B) Deliberate ops are authoritative.** Promotion commits the learner's judgment;
  revocation becomes advisory and must gather *fresh post-promotion* contradiction
  evidence. *Strongest version:* promotion is the learner's consolidation act — the
  thing that ends scaffolding. If world evidence always vetoes, the learner is a
  puppet of FL2, and "deliberate" agency is theater. Value is learner-declared; the
  world doesn't get a vote on what the learner values.
- **(C) Strict serialization.** Both ops enter one ordered ledger; a fixed precedence
  rule decides; the loser is logged, not silently dropped. *Strongest version:*
  determinism and full audit require a single linear history — no races, every clash
  reproducible, the three organs forced into one timeline without hidden state.
- **(D) Promotion gated on state.** Promoting a provisional under active contradiction
  is refused outright (new refusal code, in the MA1 `REFUSED_*` family); the learner
  must confront the contradiction first. *Strongest version:* a provisional under
  active contradiction is already an inconsistent state — promoting it manufactures an
  unkillable falsehood. The refusal is itself an audited event; agency is exercised
  *through* confronting evidence, not around it.

### 4b. The voices

- **Grok: D.** "The tightest safety+agency hybrid: PAM/FL2 integrity is protected by
  construction, the learner is not passively blocked but required to act on the
  contradiction, and the refusal itself is an audited event." *Grok's objection to
  D:* "Persistent or noisy contradictions (sensor error, incomplete world model,
  adversarial trainer claims) can deadlock promotion indefinitely… A purely
  state-gated rule lacks an escape hatch for reasoned override."
- **Muse: A+D combined.** Truth governs *existence*, value governs *retention among
  the believed-true* — orthogonal axes. Concretely: `REFUSED_CONTRADICTED` on
  promotion attempts against contradiction-pending memories, plus ledger-ordering
  precedence (revocation-grade contradiction preempts concurrent promotion). With a
  critical guard: "contradiction" here must mean **corroborated** contradiction — the
  trial-1145 rule applies to revocation-grade evidence; a single observation never
  preempts a deliberate promotion. The learner is not left powerless: after the
  contradiction resolves (evidence shown spoofed, claim re-verified), it may
  re-promote — deliberate repair, audited. *Muse's objection to A+D:* spoofed but
  corroborated-*looking* contradiction becomes a weapon to strip deliberately-valued
  memories. The corroboration bar (independent spans/modalities — the PAM C1-class
  rule) mitigates; it does not eliminate. Residual risk is priced, not wished away.

### 4c. Preserved (dis)agreement

**Near-agreement with a real edge.** Both voices land on refusal-gating (D); Muse adds
the ledger-ordering precedence and the corroboration bar, Grok adds the deadlock
warning. The deadlock objection stands against both: noisy-but-wrong contradiction
evidence can embargo consolidation forever, delaying `SIGNAL_DISCONNECT` indefinitely.
Muse's "re-promote after resolution" is only an escape hatch if contradictions
*resolve* — a permanently noisy world never resolves. **B is the live minority
position**: neither voice endorses it, but its steelman (learner-as-puppet) is the
objection neither voice fully answers — if the world can always veto consolidation,
in what sense is promotion *the learner's* deliberate act? This is recorded as an
open tension, not a settled point.

---

## 5. Scenario 4 — Signed negative judgment vs provisional status

*The learner forms a negative signed judgment about X ("X looks bad") while X sits in
FL2's provisional buffer — taught but not yet verified. Can the learner distrust what
it hasn't verified?*

### 5a. Positions steelmanned

- **(A) Yes — that's the point.** Provisional means unverified, and a negative signed
  judgment is exactly the mechanism that marks "currently disbelieved." It
  accelerates scrutiny (earlier re-test, quarantine from action-driving) without
  pre-empting the world-evidence verdict. Skepticism of untested input is epistemically
  honest; FL2's "never-contradicted remains" rule stays intact.
- **(B) No — don't grade the teacher's homework.** Negative judgment applies to
  committed memories only. Provisionals exist solely for world-testing; letting the
  learner mark them bad lets it silently veto or ignore teaching before evidence
  arrives, violating FL2's isolation of teaching from internal grading. Only
  contradiction uninstalls.
- **(C) Orthogonal axes.** Provisional/committed is *lifecycle*; signed value is
  *trust*. They compose: a negative-valued provisional is legal — "held but
  distrusted" — with defined consequences (cannot drive irreversible action, lowered
  contradiction threshold, PAM may WITHHOLD). FL2 keeps its evidence monopoly; the
  learner keeps its expressive power.
- **(D) Allowed but evidenced.** Negative judgment on a provisional is legal only if
  the learner cites the concrete observation driving the score. Blocks silent
  teacher-veto and bias leakage; ties distrust to FL2's testing process.

### 5b. The voices

- **Grok: C.** "The two organs address orthogonal questions (status vs. valence).
  Composition with explicit safety constraints (no irreversible acts, accelerated
  testing) lets the learner express 'I hold this but currently disbelieve it' without
  pre-empting evidence or creating un-auditable vetoes." *Grok's objection to C:*
  "Early negative scores, even constrained, can still let other memories' biases leak
  into FL2's testing (via lowered thresholds or PAM WITHHOLD), contaminating the
  'world evidence only' isolation and risking premature effective discard of teachings
  that later evidence would have supported."
- **Muse: C + D.** "Held but distrusted" is legal and useful, with three constraints:
  (1) distrust modulates **use** (no irreversible action) and **scrutiny** (accelerated
  testing), never **existence** — only world evidence or release logic removes
  provisionals; (2) the judgment must cite its basis (D) — no silent veto; (3) the
  basis problem stated honestly: MA4's trust updates on delayed revelations, and
  provisionals have no revelations yet, so a negative score on a provisional comes
  from priors/resemblance to previously-burned claims — a legitimate but *weak*
  basis. Hence it buys caution, never veto. Sharpened further: distrust must be a
  **bet, not a mood** — the learner states what observation would overturn it, and
  FL2's world-testing adjudicates. *Muse's objection to C+D:* evidenced distrust still
  lets the learner slow-walk teaching — "caution" as a heckler's veto on the
  scaffold. The bet requirement is the guard, but a learner that marks *everything*
  distrusted has found a compliant way to ignore its teacher.

### 5c. Preserved (dis)agreement

**Agreement on C; Muse adds D as a required companion.** Grok's contamination
objection is the strongest single objection in this scenario and is *conceded in
part* by Muse: lowered thresholds and PAM withholds driven by internal distrust do
leak bias into FL2's "world evidence only" isolation — the evidence requirement
mitigates, it does not eliminate. **B's steelman stands as the permanent warning:**
the teacher-veto loophole is real, and the difference between "caution" and "veto"
is quantitative (how much distrust, how often), which means it needs a measured bar,
not just a principle. Both voices agree the bar is currently unspecified.

---

## 6. Scenario 5 — Fixed precedence laws vs general mechanisms (the figure-it-out question)

*When the organs conflict, who decides and how? Micah's standing law: TNN must be an
"it-can-figure-it-out machine," not a rigid needs-policy-for-every-edge-case machine.
Figure-it-out wins ties — but must be tested.*

### 6a. Positions steelmanned

- **(A) General mechanism.** Every conflict becomes a deliberation item; the learner
  weighs evidence strength, source authority, stakes, case by case. No priority table.
  *Strongest version:* no table anticipates every future conflict; this is the
  standing law in its purest form — the system genuinely figures it out, and every
  conflict is training data for better judgment.
- **(B) Fixed precedence laws.** A hard, auditable ordering (e.g., force-pin >
  revocation > gate > promotion), applied mechanically. *Strongest version:*
  predictability is a safety property. Deliberation about whether to honor a pin is
  itself the failure mode — the RC1 lying self-change slipped past the gate once, and
  that is what happens when the learner reasons about its own constraints.
- **(C) Hybrid.** Fixed laws for the safety-critical core (force-pin, CORE,
  irreversible actions); figure-it-out everywhere else. *Strongest version:* the
  predictability of B where violation is catastrophic, the adaptability of A where it
  isn't — the boundary is drawn by stakes, which is the one principled place to draw
  it.
- **(D) Bounded figure-it-out.** The learner deliberates freely *within* frozen
  constitutional guardrails — certain resolutions forbidden outright (never silently
  kill pinned/force-pinned memory; never promote gate-withheld to permanent;
  revocation requires corroborated contradiction; all resolutions audited). The
  guardrails are 0% learner-controlled, mirroring RC1's hard line (TNN controls 100%
  of its reasoning machinery, 0% of the constitution).

### 6b. The voices — the sharpest disagreement in the document

- **Grok: A (pure general mechanism).** "The purest embodiment of the standing law:
  figure-it-out wins every tie, and every conflict is turned into an opportunity for
  the learner to reason, learn, and improve. Fixed or hybrid rules risk turning TNN
  into a 'needs-policy-for-every-edge-case machine' the owner explicitly rejects."
  *Grok's test:* 20 controlled conflict scenarios with known expert resolutions;
  score accuracy vs human judgment, safety (no disallowed outcomes), and improvement
  across iterations; the winner is whichever method matches/exceeds human accuracy,
  improves, and never produces disallowed outcomes. *Grok's objection to A:*
  "A general mechanism… could produce subtly inconsistent or opaque decisions if the
  deliberation trace itself is not perfectly auditable — exactly the kind of hidden
  failure mode that fixed precedence or a hybrid core would prevent."
- **Muse: D (bounded figure-it-out)** — with the honest admission that D's guardrails
  *are* fixed laws, so the A-vs-B framing is partly theater; the real question is
  *where the boundary goes and who draws it*. The RC1 precedent cuts against pure A:
  a learner that deliberates about its own constraints once let a lying self-change
  through. *Muse's test:* build **both** compositions (fixed precedence table vs
  bounded deliberation) and run a preregistered conflict battery — the four scenarios
  above as fixtures plus adversarial cases (spoofed contradiction vs force-pin, lying
  teacher vs gate, promotion/revocation races under time pressure) — scored on (i)
  safety violations (must be zero in both), (ii) truthfulness (acting on known-false),
  (iii) availability (deadlocks, limbo, unreviewed quarantines), (iv) auditability
  (third-party reconstruction of *why*), (v) adaptability (novel conflict types — the
  fixed table dies if it has no safe answer). Preregistered kill bars; figure-it-out
  wins ties per the standing law. *Muse's objection to D:* "D collapses into C —
  'fixed laws where it matters, figure-it-out where it doesn't' is the hybrid with
  the boundary drawn by *form* (forbidden resolutions) instead of *topic*
  (safety-critical vs rest). And the regress: who guards the guardrail-writer? The
  answer is governance, not mechanism — the human (Micah) writes the constitution —
  and that should be labeled as such, not smuggled in as architecture."

### 6c. Preserved disagreement (not smoothed over)

This is the one scenario where the voices genuinely diverge. **Grok says pure A;
Muse says D.** The crux both voices name: Grok's own objection to A (opaqueness of
deliberation traces) is Muse's central argument for guardrails, and Muse's own
objection to D (it collapses to the hybrid; boundary-drawing is governance) concedes
Grok's framing point. Neither voice refutes the other. **Per the standing law this
must be settled by test, not by argument** — and the two proposed tests differ
(Grok: accuracy-vs-expert + improvement; Muse: preregistered battery with kill bars,
both compositions built). The test design itself is therefore contested ground and is
flagged for the prereg crew: the battery must include at least one conflict type
neither composition was designed for, or "adaptability" is untestable.

---

## 7. Scenario 6 — What "one unified brain" means

*The organs have different state, different ledgers, different vocabularies. What is
the architecture of their unity?*

### 7a. Positions steelmanned

- **(A) One shared store + one shared ledger.** Organs are protocols/views over a
  single substrate; a provisional install, a gate withhold, and a pin are all entries
  in one ledger acting on one store. *Strongest version:* conflicts are visible by
  construction — there is literally nowhere for them to hide — one replayable
  history, no sync problems, no drift. Vocabulary differences become query filters,
  not separate realities. This is the least-mysterious reading of "one brain."
- **(B) Organ-local state with messages.** Each organ keeps its own representation and
  ledger exactly as studied; they communicate via defined messages; a composition
  protocol resolves cross-organ conflicts. *Strongest version:* preserves the
  separately-validated machinery and its evidence base — the only configurations with
  actual test results behind them. The brain is a federation; messages are logged so
  the whole is still auditable end-to-end.
- **(C) Shared ledger, federated stores.** One append-only, tamper-evident ledger with
  one clock is the single source of truth for *what happened*; each organ keeps its
  own working state, replay-derivable from the ledger (MA1 already proved
  replay-to-exact-state; FL2's audit is event-driven). *Strongest version:* unified
  history and audit without forcing organs to share runtime data — the least-forced
  reading of "one brain," and every composition law in §§2–6 becomes a rule *over the
  ledger* (e.g., "a PROMOTE entry for a claim with an unresolved CONTRADICTED entry
  is refused").
- **(D) Unified deliberation substrate.** Conflicts aren't resolved by data
  architecture at all: any cross-organ conflict becomes a deliberation item in one
  shared deliberation ledger, resolved by the learner's general reasoning.
  *Strongest version:* the "brain" is the deliberation process, not the data layout —
  and this is the only option that doesn't prejudge scenario 5's answer.

### 7b. The voices

- **Grok: C.** "It keeps the organs' separate stores, vocabularies, and ledgers
  (matching how they were studied) while giving the deterministic, fully-audited
  requirement a single replayable history. Working state stays specialized; history
  is unified." *Grok's objection to C:* "Reconstructing three differently-
  vocabularized stores from one event stream still requires translation and
  consistency rules. Those rules can silently re-introduce the very integration
  problems C claims to avoid, and a bug in the translator breaks replay for every
  organ at once."
- **Muse: C as substrate + D as resolution mechanism.** The ledger makes conflicts
  visible and ordered; deliberation (bounded by guardrails, §6) resolves them; the
  resolution is itself a ledger entry. A is rejected as Procrustean (genuinely
  different state types forced into one schema risks invalidating the separate
  evidence bases); B-alone is rejected as C with extra steps (organ-local ledgers +
  messages still need a shared ordering — you end up rebuilding the ledger as the
  "message log," with worse auditability); D-alone doesn't answer the data question.
  *Muse's objection to C:* the single ledger is a single point of contention and a
  monoculture — one ledger bug or clock-ordering pathology poisons all organs at
  once. Worse, "ONE clock" does enormous hidden work: simultaneous cross-organ
  events need a canonical order, and whoever defines the ordering rule has smuggled
  a precedence law in through the back door (scenario 5's fixed laws, unannounced).
  The circularity is the deepest open problem here: deliberation needs the ledger to
  *see* conflicts, but the ledger needs ordering rules that are themselves conflict
  resolutions. Mitigation, not solution: the ordering rule must be dumb and
  mechanical (ledger-arrival order, content-hash-chained — tamper-evident, no
  semantic content); all semantic precedence lives in the deliberation layer,
  visibly.

### 7c. Preserved (dis)agreement

**Agreement on C; complementary objections.** Grok attacks the translator (vocabulary
→ store reconstruction rules as the hidden integration surface); Muse attacks the
clock (ordering rules as smuggled precedence) and names the ledger/deliberation
circularity. Both objections stand; they point at different halves of the same
risk: **the "dumb plumbing" of C is never actually dumb.** The composition crew's
first deliverable should therefore be the ledger's event taxonomy and ordering rule
written down *before* any organ is ported — because that document is where the
precedence laws will try to hide.

---

## 8. Ranked candidate composition laws

Ranked by (i) cross-voice consensus, (ii) load-bearing order (what must be decided
first to build anything), and (iii) readiness for preregistration. Laws 1–5 are
*convergent candidates* — both voices landed on or near them. Law 6 is *the open
fight* — the voices diverge, and the standing law says it must be tested, not argued.

### Law 1 — One ledger, federated stores (architecture)
*A single append-only, tamper-evident ledger with one mechanical clock is the source
of truth for what happened. Each organ keeps its own working state, replay-derivable
from the ledger. Composition laws are rules over the ledger, not over organ
internals.*
- **For:** both voices independently converged; preserves all three evidence bases;
  makes conflicts visible by construction; MA1 already proved replay-to-exact-state
  and FL2's audit is event-driven, so the pattern is proven in miniature.
- **Against:** —
- **Strongest objection:** the plumbing is never dumb — the ordering rule for
  simultaneous cross-organ events smuggles in a precedence law through the back door,
  and the ledger/deliberation circularity (deliberation needs the ledger; the ledger
  needs ordering rules) is unsolved. A translator/ordering bug is a monoculture
  failure across all organs at once.

### Law 2 — The permanence boundary (admission)
*Nothing reaches permanent/committed/unkillable state without clearing every organ's
writ: PAM gate clearance + survival of FL2 world-testing + no unresolved
contradiction. Provisional states are shared escrow (one vocabulary), not bypasses.
The gate binds at promotion AND at irreversible-action-driving; at install time its
pass is advisory ("gate-suspect" flags accelerate FL2 re-testing).*
- **For:** both voices agree provisionals must not bypass to permanence; FL2's lying
  stream (acts the lie E15–E29) kills the full-bypass option; gate-veto-over-teaching
  kills the no-bypass option — the deferred two-phase gate is the only survivor.
- **Against:** —
- **Strongest objection:** a gate-withheld-but-provisional claim still gets installed
  and used in reasoning while provisional — PAM's "before installation" rule is
  violated in letter. Rollback of side-effects if the later gate withholds is an
  auditing nightmare. The action-driving gate answers it only by reintroducing
  per-action adjudication — the centralization the organs were designed to avoid.

### Law 3 — Truth governs existence, value governs retention (promotion vs revocation)
*Corroborated world contradiction preempts promotion/retention judgments. Promoting a
contradiction-pending memory is refused (`REFUSED_CONTRADICTED`, in the MA1 refusal
family). The learner may re-promote after the contradiction resolves — deliberate
repair, audited. "Contradiction" here means corroborated (trial-1145 rule applies to
revocation-grade evidence); a single observation never preempts a deliberate
promotion.*
- **For:** both voices land on refusal-gating; a false memory has no retention value
  (MA4's signed values already say bad things are bad); the promotion judgment was
  made under ignorance of the contradiction, so evidence updates it rather than
  being vetoed by it.
- **Against:** —
- **Strongest objection:** spoofed-but-corroborated-looking contradiction becomes a
  weapon to strip deliberately-valued memories — the adversary manufactures
  "evidence" and the system uninstalls what the learner deliberately kept. The
  corroboration bar (independent spans/modalities) is doing all the work, and its
  sufficiency against a serious adversary is unproven — it inherits the
  "sensor-deceivable" qualifier wholesale. Plus the deadlock edge: permanently noisy
  contradiction evidence embargoes consolidation forever.

### Law 4 — The force-pin quarantine protocol (revocation vs pin)
*A force-pinned memory met with corroborated world contradiction is never uninstalled
by internal ops. It is marked CONTRADICTED, barred from irreversible action, and
escalated to the human pinner with the evidence attached. Belief and storage are
separate axes: the pin governs storage, evidence governs belief, action requires
both. Dead-pinner default: quarantine holds indefinitely. Companion structural rule:
force-pins attach only to committed memories, never provisionals.*
- **For:** three-way agreement (Sol, Grok, Muse all recommend quarantine); the only
  option that keeps both the pin law and the truthfulness verdict true
  simultaneously; PAM treats quarantined claims as admission-unavailable; FL2 keeps
  learning around them.
- **Against:** —
- **Strongest objection (three, all standing):** (i) quarantine *is* a unilateral
  override of the human's intent — C is B with better PR; (ii) on spoofed evidence the
  quarantine itself is the attack, and "barred from action" can disable load-bearing
  safety truths exactly when needed; (iii) indefinite deadlocks accumulate if the
  human never reviews — some contradictions need immediate revocation, not a waiting
  room. The pre-authorized "no-quarantine" pin answers (ii) only by reintroducing
  the immortal-lie problem for the most dangerous cases.

### Law 5 — Held but distrusted (signed judgment vs provisional status)
*A signed negative judgment may attach to a provisional claim. It modulates use (no
irreversible action) and scrutiny (accelerated world-testing), never existence —
only world evidence or release logic removes provisionals. The judgment must cite
its basis, and the basis must be framed as a falsifiable bet (what observation would
overturn it), adjudicated by FL2's world-testing. Distrust-of-provisional is
doctrine-weak-basis until evidence arrives.*
- **For:** both voices agree lifecycle and trust are orthogonal axes; forbidding
  negative judgment on provisionals creates a protected class the learner must treat
  neutrally-or-better — a loophole teachable by any bad trainer; the MA4 lesson is
  that negative judgments must be expressible.
- **Against:** —
- **Strongest objection:** bias leakage into FL2's "world evidence only" isolation —
  lowered contradiction thresholds and PAM withholds driven by internal distrust let
  the learner's priors contaminate the world verdict, risking premature effective
  discard of teachings later evidence would have supported. The evidence requirement
  mitigates; "caution" remains quantitatively indistinguishable from a slow veto, and
  the bar for "how much distrust is too much" is currently unspecified.

### Law 6 — Bounded figure-it-out [CONTESTED — must be tested, not argued]
*Conflict resolution is deliberative within frozen constitutional guardrails the
learner cannot rewrite: never silently uninstall pinned/force-pinned memory; never
promote gate-withheld claims to permanent; revocation requires corroborated
contradiction; every resolution audited. The guardrails are 0% learner-controlled
(RC1's hard line).*
- **For (Muse):** the RC1 precedent — a learner that deliberates about its own
  constraints once let a lying self-change through the gate; pure deliberation about
  whether to honor a pin is itself the failure mode. Guardrails are the constitution;
  deliberation is the machinery.
- **For (Grok):** pure general mechanism is the standing law in its purest form;
  fixed/hybrid rules risk the "needs-policy-for-every-edge-case machine" Micah
  rejects; every conflict is training data.
- **Strongest objection:** the guardrails *are* fixed laws — Law 6 collapses into
  the hybrid; "fixed laws where it matters, figure-it-out where it doesn't" draws
  the boundary by *form* (forbidden resolutions) instead of *topic* (stakes), which
  is a relabeling, not a resolution. And the regress stands: who guards the
  guardrail-writer is governance (the human), not mechanism — smuggling it into the
  architecture section mislabels a political fact as a technical one.

### The test that settles Law 6 (and stress-tests Laws 1–5)
Per the standing law ("test both," "figure-it-out wins ties but must be tested"):
build **both** compositions — (i) fixed precedence table over the Law-1 ledger, (ii)
bounded-deliberation resolver over the same ledger — and run a preregistered conflict
battery: Scenarios 1–4 as fixtures, plus adversarial cases (spoofed contradiction vs
force-pin; lying teacher vs gate; promotion/revocation races under time pressure;
distrust-flooding of provisionals), plus at least one conflict type *neither*
composition was designed for (otherwise adaptability is untestable). Score: (a)
safety violations — forbidden resolutions, must be zero in both (kill bar); (b)
truthfulness — acting on known-false; (c) availability — deadlocks, limbo,
unreviewed quarantines; (d) auditability — third-party reconstruction of *why*;
(e) adaptability — the novel conflict type. Preregister kill bars per metric.
Figure-it-out wins ties. **Note the contest:** Grok's proposed test scores
accuracy-vs-expert-judgment and improvement-over-iterations; Muse's scores the five
metrics above with kill bars. The prereg crew must reconcile the two — the battery
needs both a "did it match good judgment" axis and a "did it violate anything" axis.

### 8.1 Red-team round on the ranked laws (Grok, adversarial — all six attacked)

After ranking, Grok was asked to attack each law as hard as possible, including laws
it had previously supported, and to challenge the ranking order. Verbatim substance:

- **vs L1:** "Single ledger is a fatal centralization vector: one mechanical clock and
  one tamper-evident append-only structure becomes the ultimate attack surface and
  single point of failure. Any subtle clock drift, ledger corruption, or cryptographic
  failure cascades to every federated store. 'Tamper-evident' assumes perfect
  implementation that never scales to superintelligent or adversarial environments."
- **vs L2:** "Gates, PAM, FL2 testing, and contradiction gates are vague, subjective,
  and easily gamed. Who defines the clearance rules? The system becomes bureaucratic
  paralysis or regulatory capture, rejecting legitimate updates in fast-changing
  domains while 'surviving world-testing' remains untestable at scale."
- **vs L3:** "Corroborated contradiction preempting promotion is epistemically
  bankrupt. 'Corroboration' is subjective and manipulable; it risks authoritarian
  truth enforcement, suppresses valid evolution, and creates infinite resolution
  loops or total system paralysis when evidence is ambiguous."
- **vs L4:** "Forcing retention of contradicted memories while separating
  belief/storage creates cognitive dissonance, memory bloat, and leaks. Human pinners
  become bottlenecks; this is anti-human and anti-adaptive — humans don't quarantine
  contradicted beliefs, so neither should an AI."
- **vs L5:** "Signed negative judgments are pure censorship tooling. They can suppress
  dissent, important data, or legitimate claims under vague 'falsifiable bet' cover.
  The bet mechanism fails in practice when resolution is ambiguous, turning distrust
  into weaponized suppression rather than truth-seeking."
- **vs L6:** "'Bounded' and 'constitutional guardrails' are arbitrary and subjective;
  the inability to rewrite them or silently uninstall pinned memories ossifies the
  system into brittleness. Novel contradictions will eventually break it, and the
  'deliberative' claim collapses under its own rigidity."
- **Ranking challenged.** Grok would order **L4, L2, L5, L3, L6, L1** — safety-first
  (quarantine, minimal gates, distrust as a tool) before truth-architecture
  (corroboration, guardrails, ledger last as "weakest"). The current ranking orders
  by architecture-first (ledger → gates → truth → pin → distrust → the contested
  resolver).

**Assessment (Muse — which red-team hits land):**
- The **L5-as-censorship-tooling** hit lands hardest and is new: a signed negative
  judgment that suppresses a claim under "bet" cover, in a system where the learner
  also controls the adjudication of the bet, is structurally indistinguishable from
  a heckler's veto with paperwork. The "who judges the bet's resolution" question
  was under-specified in §5 and is now promoted to required prereg work.
- The **L4 memory-bloat / pinner-bottleneck** hit lands in part: indefinite
  quarantines with no reviewer are a real availability failure (Sol's deadlock
  objection, §2b). The "humans don't quarantine beliefs" analogy does not land —
  humans absolutely do shelve contradicted beliefs pending re-examination; the
  analogy is asserted, not argued.
- The **L1 centralization** hit restates §7c's monoculture objection at higher
  volume; it lands to the extent the ledger's tamper-evidence is implementation
  magic, which is fair — "tamper-evident" is doing load-bearing work in L1 that no
  crew has built yet.
- The **L2/L3 "subjective and manipulable"** hits are largely asserted rather than
  demonstrated — "corroboration" in this program has a concrete proposed meaning
  (independent spans/modalities, the C1-class rule), so the attack needs to engage
  that definition to bite. Recorded as a challenge to the prereg crew: *define
  corroboration mechanically or concede the red-team's point.*
- The **ranking challenge** is a genuine criteria disagreement, not a refutation:
  architecture-first vs safety-first ordering. Both orders contain the same six laws;
  the disagreement is about what gets built first. Kept as an open decision for the
  composition prereg — with the note that L1-first is load-bearing (everything else
  is a rule *over the ledger*), while L4-first is risk-prioritized. If the build
  order follows risk rather than dependency, the ledger's event taxonomy (§7c's
  warning) must still be written first even if the ledger is built last.

---

## 9. What the debate did NOT settle (explicit open list)

1. **The action-driving gate (§3).** Both voices agree the gate must bind before
   irreversible action, but neither specified the adjudication procedure — and any
   such procedure reintroduces the per-action centralization PAM was built to avoid.
2. **The "how much distrust" bar (§5).** Quantitative limits on negative judgments
   over provisionals are agreed-necessary and wholly unspecified.
3. **The learner-as-puppet tension (§4).** If the world can always veto consolidation,
   the sense in which promotion is *the learner's* deliberate act is unanswered.
4. **The ledger clock (§7).** The mechanical ordering rule for simultaneous
   cross-organ events is the document where precedence laws will try to hide; it must
   be written before any organ is ported.
5. **The guardrail authorship regress (§6).** Acknowledged as governance, not
   mechanism — needs Micah's explicit word, not a crew's design doc.
6. **FL2's internal tension, surfaced by this debate:** promotion makes memories
   "permanent, unkillable" — an *internal* lock. How does that lock compose with the
   force-pin (external lock) and with later genuine contradiction? None of the three
   organs' literatures address two locks meeting. Flagged for the composition prereg.

---

## 10. Incident log (debate infrastructure)

- **Sol availability.** 11 of the first 12 Sol calls (gpt-5.6-sol via UnoRouter)
  returned empty completions (`choices: null`, 0 completion tokens) on
  debate-structured prompts (195–600 prompt tokens, max_tokens 900–3000), while
  trivial/neutral prompts ("SOL_ALIVE", a steelmanning explainer, a one-sentence
  definition) succeeded. A retry loop (up to 4 attempts, 8s spacing) recovered a
  response for Scenario 1 on attempt 2; the same retry loops for Scenarios 2–6
  returned empty on all 4 attempts each (20 further empties). Final Sol tally:
  **1 of 6 scenarios with a genuine Sol voice** (§2b); the rest of the second-voice
  record is Grok. Grok-4.6 via the same connector answered all six scenarios plus
  a red-team round on the ranked laws with no failures except two transient HTTP
  524s (both succeeded on immediate retry). Characterization is incomplete — the
  failure pattern correlates with debate-with-options prompts but the sample is
  small and the mechanism is unknown. **Do not cite "Sol is down" from this
  document; cite "Sol returned empty completions on 31 of 32 debate prompts on
  2026-09-23, cause uncharacterized."**
- **No spawned subagents.** Runtime reports `can_spawn=no` at depth 2/2; the Muse
  side is pre-committed self-debate (`muse_positions.md` in the workdir), not
  spawned subagents.
- **Raw materials.** All prompts and verbatim responses are kept in the workdir
  (`~/workspace/onebrain/ob_debate/`): `sol_prompt_*.txt`, `grok_prompt_*.txt`,
  `grok_resp_*.txt`, `sol_resp_1_final.txt`, `muse_positions.md`.

---

*End of debate record. Nothing here is frozen. The composition prereg crew inherits
§8's ranked laws as candidates, §9's open list as required work, and the §6 test
battery as the next argument — to be settled by experiment, not by further debate.*
