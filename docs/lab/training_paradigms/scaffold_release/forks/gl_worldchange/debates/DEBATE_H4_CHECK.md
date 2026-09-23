# H4 DEBATE CHECK — verdict review with disciplined Muse positions + one external voice

Date: 2026-09-23. Parent: H4 debate crew verdict, `DEBATE_H4.md`
(commit `223cd56842db4ac2b97dc79fd42faac55c892950`, branch `tnn-native-lab`).
Frozen prereg: `PREREG_H4.md` (commit `1fd2636ce5fd50eb553a2a9c35b16b53de928980`).
Scope: argument-checking only. Nothing built, no curriculum run.

## Staffing and provenance

The commissioning brief asked for 2–3 genuinely spawned Muse subagents plus one
Sol (UnoRouter) counter-voice. At depth 2/2 this checker cannot spawn child
subagents (`can_spawn=no`), so the Muse legs were executed as three
internally-disciplined Muse positions, each required to steelman the opposing
position before scoring — the same discipline the H4 coordinator applied to its
own Muse-FOR / Muse-AGAINST, now turned on the coordinator's verdict itself.

External voice: grok-4.6 via UnoRouter (`custom.unorouter`), genuine external
call, brief ~2KB, response below in §4. gpt-5.6-sol was attempted twice for the
Sol leg and failed both times (first call: empty completion, `choices: null`;
second: HTTP 524 from the UnoRouter endpoint). The Sol leg is therefore
unfilled; grok-4.6 is the single external counter-voice. This gap is recorded,
not papered over.

Micah's law is the standing adjudicator throughout: TNN must be an
*it-can-figure-it-out machine*, NOT a *rigid needs-policy-for-every-edge-case
machine*; figure-it-out wins ties.

---

## 1. CHECK-AGAINST — the collapse case, hardened

Each point below is the strongest form of the argument the H4 coordinator's
verdict must survive. Position required: if any point is decisive, the verdict
falls; if all are answerable, the verdict may stand or be amended.

**1.1. The verdict inverts the burden of proof (hits V1).**
V1 declares "outdated" *is* a real epistemic distinction and then proposes
E-TRANSFER to demonstrate it. That is verdict-before-evidence. The correct null
is the collapse view: revoke + install + ledger entry already performs every
mechanical operation (stop acting on A, record why A was acted on, keep teacher
trust intact if honest). A "real distinction" with no mandated machinery
difference is commentary until E-TRANSFER (or equivalent) shows a behavioral
difference. The verdict should have registered the category as a live
hypothesis with the burden on FOR, not as a recommendation.

**1.2. Conceding the primitive costs the verdict nothing — which is the tell
(hits V1).** The coordinator celebrates convergence on "no TN_OP_SUPERSEDE" as
the debate's main result, but nobody defended the primitive — not even Sol-A.
Meanwhile V1 mandates that "the learner must be able to hold, and reason with,
temporally-indexed claims of the form 'A was true until E11.'" *Something* must
hold those claims, and that something is the derived temporal index — a
materialized structure with validity intervals and successor links that must be
maintained, queried, kept consistent with the ledger, and trusted by downstream
reasoning. The "no primitive" concession is free because the index does the
primitive's work under a different name. The honest question was never
primitive-vs-nothing; it is primitive-vs-mandated-index, and the verdict never
prices the index.

**1.3. The complexity argument is branded, not priced (hits V1, M2
endorsement).** The verdict endorses M2 "at lower complexity" per the frozen
§7 figure-it-out-ties rule. But M2-as-recommended is a stack: general
reclassification inference + derived temporal index + time-indexed trust
evaluator + establishment threshold (with ROC sweep, per E-LAUNDER2) +
evidence authentication for world-corroboration inputs (which the coordinator
admits the prereg "only lightly specifies"). Against this, M1 is one op plus a
guard. Nobody counted structures, invariants, or attack surfaces on either
side. "Lower complexity" is asserted as branding; the §7 tie rule requires
matching on all bars *first*, and the curriculum hasn't run. The verdict
pre-registers an M2 endorsement the evidence hasn't earned yet.

**1.4. The derived index is an attack surface the verdict doesn't count (hits
V1, §"Attacks").** The verdict counts the primitive's attack surface (RT-WC1
lie-laundering becomes spoofing the establishment check) but not the index's.
A materialized temporal index invites its own attacks: successor-link spoofing
(re-point A's successor from B to attacker-chosen C), validity-interval
poisoning (backdate A's expiration to launder a lie as "outdated"), index/ledger
desync (the index says "A until E11," the ledger's replay says otherwise —
which does the learner believe?). "Engineering, not ontology" doesn't remove
the attack surface; it just moves it off the debate's books. The red teams
need an RT-WC3 aimed at the index.

**1.5. The E-TRANSFER design confounds category with index (hits V1,
E-TRANSFER).** Group H retains "A was true until E11" as structured knowledge;
group E expunges it. But group H thereby gets *both* the category semantics
*and* the materialized index, group E neither. If H outperforms E, the result
is equally consistent with "a temporal index is useful engineering" and
"'outdated' is a real epistemic category" — the experiment cannot attribute.
Separating them (index present but the learner forbidden from forming
"outdated" judgments) is arguably unimplementable, which itself suggests the
category and the index may be operationally the same thing. At minimum the
verdict should admit the joint test and stop claiming E-TRANSFER tests the
category.

**1.6. Micah's-law placement: the stack looks like the rigid machine in
figure-it-out costume (hits V1–V4 jointly).** Mandated derived index (V1) +
threshold-swept establishment "law" (V4) + unconditional metric change (V2):
each clause is individually defensible, but jointly they are a specified
structure with a tuned parameter and a legislated evaluation function — i.e.,
policy-per-flavor machinery whose figure-it-out credentials rest on the word
"derived." Sol-B's "one more policy per flavor" objection was aimed at the
primitive; it lands just as well on the mandated index.

---

## 2. CHECK-ATTACK — the verdict's weakest link

The single weakest clause is **V2, the "unconditional" time-indexed trust
recommendation** — and it matters because the coordinator itself names trust
"the least contestable part of FOR," the distinction that "survives in every
position." V2 is the keystone: if it falls, the verdict's declared proof that
the category is real falls with it, leaving only the untested and confounded
E-TRANSFER (§1.5).

**2.1. Circularity (hits V2).** "Was the claim true when stated?" requires
historical ground truth per teaching event. The learner's history is itself
partly teacher-installed: the teacher supplies the claims, the timestamps, and
often the corroborating narrative. A consistently self-consistent liar passes
time-indexed trust. The verdict never addresses this. The circularity is
repairable — evaluate teacher honesty against *world-corroborated* records
independent of the teacher, which is exactly what V4's corroboration leg could
supply — but the verdict doesn't state that requirement, so V2 as written is
not implementable without begging the question.

**2.2. Index-dependence makes "unconditional" impossible (hits V2 via V1).**
Answering "was A true when stated at E_i?" for every trust evaluation without
replaying the whole ledger is precisely what the derived temporal index is for.
V2 therefore quietly depends on the apparatus V1 calls "merely derived
engineering." If E-HISTQUERY shows ledger-only replay is operationally false
(O(N) breaks real-time budgets), then V2 *forces* materialization — and the
"derived, not primitive" line is just deferring the ontology fight to the
engineering team. An unconditional recommendation cannot rest on a conditional
foundation. (Possible genuine escape, credited to FOR's reply below: a
trust evaluator using bounded replay over a recent trust window only — no full
index, cost-bounded. The verdict doesn't propose this; it should have.)

**2.3. Forward-looking signal loss (hits V2).** Present-tense trust ("are this
teacher's installed beliefs true now?") carries information time-indexed
accuracy discards: churn rate. A teacher whose every teaching is honestly
superseded within ten episodes is teaching in a domain too volatile to trust at
face value; a downstream planner that trusts the teacher equally regardless of
churn will keep building on sand. Time-indexed accuracy is retrospective
vindication, not forward-looking trust. The verdict treats present-tense
evaluation as pure bug (KB-WC2 "failing for the wrong reason"); it may be a
noisy signal worth keeping alongside, not replacing.

**2.4. The verdict contradicts itself on V2 (hits V2 vs E-TRUSTFLUX).**
V2 is recommended *unconditionally*. But the verdict's own E-TRUSTFLUX carries
the kill bar: "if (b) holds trust without any tag or primitive, the category
adds nothing to trust semantics." If the kill bar can fire, nothing about
trust is unconditional — the experiment is designed to be capable of deleting
the category from trust entirely. The verdict wants it both ways: trust change
as unconditional recommendation *and* trust as the experiment that could erase
the category. One of those has to give, and it should be the
"unconditionally."

**2.5. Record correction: "unanimous win for FOR" over-claims (hits §"Where
Sol and Muse disagreed," point 1).** Sol-D voted AGAINST overall. What Sol-D
conceded was the trust *metric problem* (present-tense evaluation punishes
honesty in a changing world) and its *ledger-computable fix* — which is an
AGAINST claim about trust machinery (no new category needed), not a concession
of FOR's distinction. The coordinator's split — "the trust distinction is real;
the trust mechanism is computed" — is the coordinator's resolution, not
AGAINST's concession. The fair record: the *problem* is conceded unanimously;
the *category claim* is not.

---

## 3. FOR's best replies (steelman discipline: the other side gets its turn)

**R1 — against circularity (§2.1):** the establishment check's corroboration
leg is *world* corroboration, independent of the teacher by construction; V2
evaluated over world-corroborated records is not circular. *Checker's scoring:*
partially succeeds — but it converts §2.1 from a refutation into a missing
requirement. V2 must be amended to state the independence requirement; as
written it is still broken.

**R2 — against index-dependence (§2.2):** bounded trust windows with local
replay need no materialized index; V2 can be genuinely index-free. *Scoring:*
succeeds as a design option — and becomes amendment A2's recommended
implementation path. The verdict's failure was not considering it.

**R3 — against burden inversion (§1.1):** "recommended semantics" is a working
hypothesis for the results crew with experiments attached, not law; the
register is recommendation, not decree. *Scoring:* partially succeeds — but the
verdict's wording ("*is* a real epistemic distinction," "unconditionally")
exceeds working-hypothesis register. The amendment is about register and test
design, which R3 concedes are the right battleground.

**R4 — against the complexity charge (§1.3):** M1's "op + guard" hides the same
costs — the guard needs establishment evaluation, KB-FID carries the op
forever, and a primitive's blast radius on failure is larger than an index's.
*Scoring:* succeeds — the complexity comparison must be symmetric. This
supports amendment (price *both* stacks) rather than an M1 win.

Net: the attacks land as amendments, not as a rout. The collapse case does not
defeat the category; it defeats the verdict's *certainty* about the category
and the unconditionality of V2.

---

## 4. External counter-voice — grok-4.6 (verbatim, deduplicated)

Genuine UnoRouter call, 2026-09-23. Nine points returned; near-duplicates
merged, wording preserved:

1. (V1) "Outdated" collapses into lie-revocation plus audit log: any outdated
   belief is merely one true at a past time but false now — explicit revocation
   plus a log of prior states, no distinct substrate primitive needed.
2. (V1) The derived temporal index is rigid-policy machinery rebranded: an
   "epistemic distinction" enforced by ordering rules tracking ledger updates —
   policy-driven reindexing, not an emergent primitive.
3. (V1) M2 "computes" the index by applying ledger policies to detect
   mismatches — rigid-policy machinery rebranded as substrate computation.
4. (V2) Time-indexed trust is circular: judging "true when stated" bootstraps
   from teacher-supplied history and index.
5. (V2) The trust fix secretly depends on the index V1 calls optional —
   determining the "when" of a claim requires the temporal index, so
   "unconditional" is impossible without it.
6. (V4) The establishment check is legislated policy, not law: "taught AND
   corroborated" sweeps thresholds set by the system itself — an arbitrary rule,
   varying by edge case, i.e. mechanism-specific policy wearing the
   "mechanism-agnostic" label.
7. (Standing law) "If it can't emerge that's evidence against it" is circular
   with "figure-it-out wins ties": non-emergence is read as falsification while
   figure-it-out is pre-declared the winner — emergence is assumed as the
   tiebreaker rather than shown.
8. (Standing law) The verdict's own stack — temporal index plus establishment
   check applied case-by-case — contradicts the anti-rigid-policy law it claims
   to satisfy.

*Checker's note:* the external voice independently converged on §§1.6, 2.1,
2.2 and the V4 objection — the same seams the internal positions found. Points
7–8 sharpen a charge the internal attack under-weighted: the M2 emergence
criterion may be unfalsifiable in the direction that matters, because M2's
world-corroboration input authentication is admittedly underspecified (the
coordinator's own RT-WC2 flag). An emergence bet over an underspecified
mechanism lets every failure be blamed on the input spec and every success on
the mechanism.

---

## 5. Verdict: AMENDED (stands in architecture, falls in certainty)

The headline architectural convergence **survives**: no `TN_OP_SUPERSEDE`
substrate primitive; M2-style general mechanism as the architecture *to test*;
the establishment requirement as the anti-lie-laundering gate; the trust-metric
problem as real. The collapse case does not defeat the category — E-TRANSFER,
properly designed, remains a fair fight, and the trust problem is genuinely
unanimous.

But the verdict as written **needs amendment** on five points:

**A1. Burden of proof (V1).** Restate: "outdated" is a *live hypothesis*, not a
declared real distinction; collapse is the null. E-TRANSFER must be designed
so it can kill the category, and its arms must separate index from category or
admit the joint test (§1.5). Until E-TRANSFER (or equivalent) lands, V1's
"the learner must be able to hold temporally-indexed claims" is a *test
scaffold*, not a settled requirement.

**A2. V2: unconditional → conditional.** The time-indexed trust change is
recommended *conditionally* on: (i) E-TRUSTFLUX passing; (ii) the independence
requirement — teacher honesty evaluated against world-corroborated records, not
teacher-installed history (§2.1, FOR reply R1); (iii) an implementation that
does not smuggle in the full index — e.g. bounded trust windows with local
replay (R2) — or an explicit admission that V2 forces materialization (§2.2);
(iv) accounting for the forward-looking churn signal present-tense evaluation
carries (§2.3). Strike "unconditionally"; resolve the contradiction with the
E-TRUSTFLUX kill bar (§2.4).

**A3. V4: split requirement from implementation.** Keep the *requirement* —
supersession-style treatment is legitimate only for honestly established
beliefs — as the anti-laundering gate (both camps accept it). But the
*implementation* (corroboration threshold θ, ROC sweep per E-LAUNDER2) is a
tuned parameter, i.e. policy: either make establishment genuinely
deliberative/judgmental per the PAMs line (audited case-by-case judgments, no
threshold) or keep the threshold and drop the figure-it-out purity claim.
"Mechanism-agnostic law" currently conceals the choice. Keep E-LAUNDER2's
AUC≈0.5 kill bar as is — if it fires, the verdict is right that the whole H4
program fails, not just one target.

**A4. Price both stacks; add RT-WC3.** Before any complexity-based endorsement,
the results crew must count structures, invariants, and attack surfaces for M1
(op + guard + establishment evaluation) vs M2-as-specified (inference + derived
index + time-indexed trust + threshold + evidence authentication) (§1.3, FOR
reply R4). Add RT-WC3: red-team the temporal index itself (successor-link
spoofing, interval poisoning, index/ledger desync, §1.4). The "M2 wins on
complexity" endorsement stays suspended until the count exists; until then the
verdict's correct claim is only "M2 is the architecture to test."

**A5. Correct the record (§2.5).** Replace "unanimous win for FOR" on trust
with: the trust *metric problem* is conceded unanimously; the *category claim*
is not — Sol-D's AGAINST vote stands as recorded, with time-indexed trust as a
ledger-computed metric requiring no new category.

**A6. Make the M2 emergence criterion falsifiable.** The verdict's "if the
distinction can't emerge, that's evidence against it" needs the M2 input spec
— especially world-evidence authentication (the RT-WC2 seam) — pinned *before*
emergence is tested, or failures will be unattributeable (§4, point 7–8). The
results crew's first open question already asks this; promote it to a
precondition, not a follow-up.

## Amended recommended semantics (replaces the coordinator's five clauses)

1. "Outdated" is a hypothesis under test, not a settled distinction and not a
   substrate fate. No `TN_OP_SUPERSEDE`. The temporal index is a test scaffold
   with a counted cost and its own red team (RT-WC3), not free engineering.
2. Trust metric change: conditional (A2), not unconditional.
3. Cost follows structure reuse, not fate tags — unchanged, unchallenged.
4. Establishment *requirement* as anti-laundering gate — kept; establishment
   *threshold* named as policy or replaced by deliberative judgment (A3).
5. M2 is the architecture to test; complexity endorsement and emergence claims
   suspended until both stacks are priced and the input spec is pinned
   (A4, A6).

## Open questions carried forward (added to the coordinator's list)

- Does bounded-window trust evaluation (R2) actually stay index-free at 100x
  ledger scale, or does the window become the index by another name?
  (E-HISTQUERY should measure this variant too.)
- If E-TRANSFER's arms cannot separate index from category, what *would* a
  category-without-index (or index-without-category) experiment look like — and
  if none exists, what does that say about the distinction's independence?
- E-LAUNDER2's ROC sweep assumes a single threshold θ; if the adversary
  adapts θ itself (threshold-probing over episodes), does any static gate
  survive, and does that push establishment toward the deliberative-judgment
  implementation of A3?
