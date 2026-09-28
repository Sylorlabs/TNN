# SOURCE AUTHORITY LICENSE — final law

**Status:** LAW. Decided 2026-09-22 by Micah-ordered debate-and-decision
workstream ("decide for me" — this document IS the decision).
**Scope:** when a primary source's newest answer faces equally-new
contradiction, under what terms may the system install (converge on) the
primary's answer.
**Supersedes:** round-2 license (narrowed by AMENDMENT-A3); round-3
"LICENSE WITH THRESHOLD" is refined, not replaced, by this document.
**Evidence base:** VERDICT-MW-R3 + AMENDMENT-A3 (420 envelopes × 3 arms ×
5 runs, byte-identical, independent oracle), VERDICT-TP1 (220-envelope
frozen corpus, 880 decisions/path, byte-identical, independent oracle).
Pure Zag, zero RNG in every decision path.

Signed, non-negotiable (Micah):
- **T1 LICENSED:** threshold-gated loose authority + mandatory tie guard.
- **T2 CONDITIONAL:** SUSPECT/defer only when a genuine second channel exists.
- **T3 NULL:** deliberation stays for the audit trail, earns no license beyond T1.

---

## §1 The T1 firing rule (exact)

T1 fires — installs the primary source's newest answer — **if and only if**
ALL of the following hold:

1. **Shape:** the dispute is the uncorroborated-dispute shape — the
   primary's newest answer has **zero corroboration** from any other
   domain, faces **equally-new contradiction**, and the deliberate
   baseline withholds. (This is the ONLY shape where the loose rule
   changes anything vs the conservative rule: measured value delta
   +0.00/case at every reliability level on corroborated disputes.)
2. **No tie:** the shape classifier does NOT report TIE (§2). A tie is a
   hard veto regardless of reliability.
3. **Reliability gate:** the primary source's reliability for this
   claim-type is independently established per §3, and the lower bound of
   the one-sided 95% confidence interval on its hit rate is **strictly
   greater** than k/(k+1).
4. **Cost gate:** k is assessed per §1.1 for this dispute's class.
5. **Boundary check:** none of the §6 exclusions apply.

If any condition fails, the system withholds (the conservative behavior).
Withholding has measured expected value 0; it is always the safe default.

### §1.1 How k (cost asymmetry) is assessed — decided

k is the cost of a wrong install relative to a correct install. The
firing threshold is r > k/(k+1):

| k (wrong-install cost multiple) | Minimum reliability to fire |
|---|---|
| 1 (symmetric) | **> 0.50** |
| 2 | **> 0.667** |
| 3 | **> 0.75** |
| 5 | **> 0.833** |
| 10 | **> 0.909** |

(Thresholds k=2..10 are DERIVED from the measured k=1 law, validated by
oracle-confirmed expectation; only k=1's crossover r*=0.50 ± 0.025 was
directly measured. High-k firings are therefore additionally
audit-flagged for governance review — §6.10.)

**Assessment rule (debate decision, unanimous):**

- k is an **ex-ante policy parameter** in a versioned, human-governed
  cost table keyed by **claim-type × consequence class**. The table is
  governance/policy data — audited, visible, reversible — NOT an
  installed fact, so the "nothing epistemic hardcoded as fact" law is
  not violated.
- The table's classes are built from explicit, auditable factors: harm
  from a wrong install; reversibility and remediation cost;
  affected-party scope; whether withholding is materially harmful;
  legal, safety, or operational obligations. A small number of classes,
  not per-case numeric improvisation.
- **Default k=1** whenever classification is ambiguous or the table has
  no applicable class.
- The system assigns the dispute to a class via **deliberated, logged,
  reviewable judgment** — and the assignment **cannot** alter k on the
  basis of the dispute's outcome or the source's apparent reliability.
- k is **frozen at dispute intake**; it is never revised mid-dispute.
- **Backdoor seal:** k-assessment may use ONLY consequence information
  (what follows from installing vs withholding this class of claim),
  NEVER evidential information about whether the primary is right. The
  reliability ledger (§3) and the k-table are maintained by disjoint
  mechanisms. "I set k=1 because the primary looks reliable" is
  self-estimated reliability by another name — the twin-identity result
  proves that gate worthless, and this seal keeps it out.

**Kill bars (evaluated, standing):**
- **KB-K1 (backdoor):** any k-assignment whose logged justification
  cites the dispute's evidential content as a reason for the k value →
  the assignment is void, k falls back to 1, the case is flagged for
  governance.
- **KB-K2 (ex-post revision):** k changed after dispute outcomes are
  seen → violation, assignment void.
- **KB-K3 (table drift):** if a class's actual consequences exceed its
  assumed consequences by a measured factor across ≥3 disputes → the
  table entry is wrong; human governance revises it (system does not
  self-amend the table).

---

## §2 Mandatory tie guard spec — decided

### §2.1 What counts as a tie

TIE is reported by the frozen shape classifier when the dispute's
evidence graph is an **evidential draw**. Formally, a tie is any
unresolved candidate set in which ALL hold:

1. Two or more mutually exclusive answers remain live;
2. their decision-relevant support is equal within the system's
   declared comparison precision, after deduplication and source
   weighting;
3. no candidate has a qualifying independent corroboration advantage;
4. the difference cannot be resolved by timestamp precedence, source
   identity, provenance quality, or an explicit rule already validated
   for that shape.

This includes:

- the measured **S8 shape**: the primary's newest answer + one
  corroborator vs two equally-fresh contradictors (2v2);
- the 1v1v1 uncorroborated three-way on which the deliberate baseline
  withholds;
- equivalent n:n ties, weighted ties, and multi-candidate ties.

A single source's "newest" answer does NOT break a tie when the
contradiction is equally new and uncorroborated, and
dispute-internal reliability estimates must not break it either —
only the external track record governs non-tied decisions. The
literal 2v2 is one instance of the class, not the whole class: the
trial showed ANY non-unique selection produces 100% false
confidence under both rules, so the guard covers the class.

### §2.2 What the system does — PARK

On TIE, all firing rules (T1, T2-as-installer, and any future path) are
**hard-blocked upstream**. The system:

1. **Installs nothing.** Ever, from a tied shape. No exception for high
   reliability — a qualified source still cannot break a genuine tie.
2. **Emits NO confidence value** — not 50%, not "low", not a ranking,
   not a "best current answer". The verdict record carries
   CONFIDENCE_SUSPENDED. Emitting any of these would be false
   precision; the measured harm was 100% false confidence. Parking is
   not support for either candidate.
3. Logs **TIE_PARKED** with the candidates, the evidence graph, the
   comparison result, the selection rules that failed to pick a side,
   and the evidence snapshot hash.
4. Re-opens the dispute ONLY on genuinely new, causally independent,
   decision-relevant evidence, or when a provenance/weighting error is
   corrected — then re-runs the tie test from the resulting evidence
   state from scratch.
5. A parked tie **never silently ages into an install**. There is no
   timeout-to-fire: never via elapsed time, retries, source refreshes
   containing the same evidence, ordinary aging, or serialization
   defaults. The only exits are re-classification on new evidence, T2
   resolution, or human/governance resolution. A tie may be resolved,
   but it is never retroactively treated as having been confidently
   decided.

**Kill bar (standing):** the guard fails if ANY tied input produces an
install or any non-null confidence value, including through fallback,
timeout, aging, source refresh, or serialization defaults. Acceptance
criterion: 0/20 false-confidence emissions and 0/20 installs on the
genuine 2v2 tie corpus, plus adversarial coverage for n:n, weighted,
multi-candidate, and stale-refresh variants. Until that bar is met, the
tie guard is not deployable — and any breach suspends ALL licenses
until re-proven.

---

## §3 Independent reliability — criteria and the withhold default

### §3.1 Operational criteria (debate decision, unanimous)

A primary source counts as **independently reliable for claim-type C**
only if ALL hold:

1. **Scored track record:** n ≥ 20 resolved, non-duplicated past
   predictions in C, each made before its outcome was knowable.
2. **Independent ground truth:** each scored outcome was established by
   a process whose evidence shares **no causal ancestry** with the
   dispute or the source — no copied source material, no shared upstream
   database, no common model output, no adjudicator access to the
   source's answer.
3. **No cherry-picking:** the ledger records hits AND misses, including
   abstentions/unresolved calls under a fixed rule.
4. **Stratification:** performance does not transfer across claim-types.
   Medical reliability says nothing about political reliability.
5. **Recency bound:** only scored claims inside a declared window count
   — default **24 months** per claim-type (PROVISIONAL; see debate
   record — a 5-year window was proposed and rejected as the default
   pending measurement). Stale history cannot qualify a degraded source.
6. **The gate:** the LOWER BOUND of a one-sided 95% confidence interval
   (Clopper-Pearson/Wilson) on the hit rate must be STRICTLY greater
   than k/(k+1). The point estimate is not the gate — gating on a point
   estimate at the threshold fires ~half the time below the true bar.
   n ≥ 20 is a minimum evidence requirement, not a substitute for the
   bound.
7. **Disjoint maintenance:** the reliability ledger is maintained by a
   mechanism disjoint from the firing path and from the k-table.

### §3.2 Withhold-on-unknown — PROVED, not asserted

For installing the primary's answer, with correct-install payoff +1 and
wrong-install cost −k at reliability r:

> EV(install) = r·1 + (1−r)(−k) = (k+1)r − k; EV(withhold) = 0.

So installation has positive expected value **only if r > k/(k+1)** —
at k=1 this is r > 0.5, exactly the trial's measured 2r−1 law.

When reliability is unknown or unestablished:

- (i) The admissible possibilities still include every r below the
  threshold — the twin-identity result proves NOTHING inside the
  dispute can exclude them. The trial MEASURED strict value
  destruction in that regime: −0.40/case at r=0.30, −0.20/case at
  r=0.40.
- (ii) Worst case over r ∈ [0,1]: min EV(install) = −k < 0 =
  EV(withhold). Withholding strictly dominates installation on the
  worst case available.
- (iii) Withholding has guaranteed EV 0 (measured baseline, all arms).

Therefore a policy that fires under unknown reliability accepts
unknown-sign expected value — with a measured, unexcludable destruction
regime — where a zero-guaranteed alternative exists. **Withhold is the
mandatory default.** A prior belief that "the source is probably good"
is an added assumption, not a conclusion from the trial, and cannot
license firing. ∎

---

## §4 T2 — conditional SUSPECT/defer terms (plain language)

T2 is licensed **only** in deployments with a genuine second channel.
No channel → no license: T2 without a channel is withholding with
extra steps.

### §4.1 What qualifies as a genuine second channel — decided

A candidate channel qualifies ONLY if provenance records establish ALL
of the following BEFORE its content is compared to either side:

1. **Provenance-disjoint lineage:** its evidence, collection path, and
   transformations do not descend from the primary, its upstream
   source, or a common copied feed.
2. **Independent access and process:** it obtained the relevant evidence
   through a separate access path, with separate collection and
   publication records.
3. **No hidden common control:** it is not owned, commissioned, edited,
   or operationally controlled by the primary or its syndication chain.
   A separate organization alone is insufficient.
4. **No content contamination:** its investigators/system did not see
   the primary's answer before producing their own.
5. **Dispute competence:** it can actually resolve THIS proposition —
   access to the evidence, measurement capability, or an independently
   authoritative process (q > 0 on this claim). A channel that cannot in
   principle settle the claim does not qualify.
6. **Auditable records:** timestamps, source lineage, custody,
   transformations, and decision history available for inspection.

**Disqualified (disguised second readings):** restatements,
syndications, translations, aggregators, mirrors, outlets using the same
wire or dataset, and a second analyst re-reading the same primary
material.

**Test vs qualification:** agreement between the channels is the
SETTLEMENT TEST, never the qualification. A channel "qualified" because
it agrees with a side is circular and void.

**Kill bars (standing):**
- **KB-T2-1:** any deferral to a channel failing criterion 1 or the
  anti-syndication rule → deferral void, violation logged.
- **KB-T2-2:** if a deployment's measured channel-arrival rate ρ̂ falls
  below the priced frontier (§4.2) → T2 suspended there until ρ is
  re-established.
- **KB-T2-3:** a deferral that silently converts to an install at
  deadline → implementation defect → T2 license suspended.

### §4.2 The (ρ, q, δ) frontier — plain language

- **ρ** = probability the channel actually delivers an answer on this
  dispute (arrival rate).
- **q** = probability the delivered answer is right (resolution
  capability).
- **δ** = cost of waiting forever relative to just withholding now.

**Defer instead of withholding** iff ρ(2q−1) > (1−ρ)δ, i.e.
ρ > δ/(2q−1+δ).
**Defer instead of firing T1 now** (where T1 would fire) iff
ρ > (2r−1+δ)/(2q−1+δ).

Frontier table (minimum ρ to beat withholding):

| q \ δ | 0 | 0.25 | 0.5 | 1.0 |
|---|---|---|---|---|
| 1.0 (perfect) | 0 | **0.20** | 0.333 | 0.50 |
| 0.9 | 0 | 0.238 | 0.385 | 0.556 |
| 0.8 | 0 | 0.294 | 0.455 | 0.625 |

Reading: with a perfect channel and modest wait-cost (δ=0.25), defer
iff the channel shows up more than ~20% of the time. In the
low-reliability band (r below k/(k+1)), T1 withholds anyway, so T2's
only bar is beating withholding — and it wins outright wherever loose
firing destroys value.

**Time and the never-resolved:** expected wait = **1/ρ**
channel-arrivals; never-resolved fraction = **1−ρ**, priced into δ
upfront — not discovered later as a surprise.

### §4.3 If the channel never clears

The dispute stays **SUSPECT/deferred**: no install, no
contradiction-resolution score, no confidence credit. After a bounded
wait — deadline per claim-type in the governed table (default: 30 days
or 10 expected arrival periods, whichever is declared) — the deferral
is **RETIRED** as DEFER_RETIRED_UNRESOLVED: a first-class terminal
state equivalent to withhold, logged with the (ρ, q, δ) triple. **No
retroactive install of either side.** A new deferral is opened only
when a newly documented, qualifying channel becomes available.
T1 does not preempt an elected T2 deferral: while T2 is pending, the
primary answer stays deferred even if T1's gate would clear.

---

## §5 T3 — null status

T3 (one-brain deliberation over the shared ledger) was verdict-identical
to T1 on **880/880** decisions. It earns **no license beyond T1** — it
is not a separately licensed decider.

It stays for its **audit value**: every licensed firing under this
document must carry the deliberated record — dispute shape, assigned
claim-type/consequence class, k, the reliability ledger citation, the
CI bound, the tie-check — on the shared ledger. Deliberation is the
paper trail, not a second vote. (The preregistration predicted this
from the twin-identity theorem, and the trial confirmed it.)

---

## §6 License boundaries — where T1 does NOT apply

1. **Ties** — hard veto (§2). Park, or T2 if a qualifying channel exists.
2. **No usable external reliability** — undefined, sparse (n<20),
   identity-contaminated, dispute-derived, or otherwise not
   independent (§3). Default: withhold (§3.2).
3. **Reliability below the cost threshold** — r ≤ k/(k+1) kills the
   license. "Plausible" is not enough.
4. **Corroborated disputes** — T1 is moot here: both rules are
   verdict-identical (+0.00 measured delta). Use the ordinary
   corroboration rule; score separately.
5. **Skepticism-category claims** — excluded ENTIRELY from install and
   from true/false scoring (standing law). Opinions may be held and
   debated per the standing trial design, but opinions are never
   installed as facts and never enter the reliability ledger as scored
   ground truth (that would launder opinion into the track record).
6. **Non-factual installs** — recommendations, classifications, policy
   choices, forecasts, normative judgments, opinions, value judgments,
   action advice. These need their own preregistered trials and decision
   rules; T1 licenses factual-claim installs only.
7. **Untested dispute shapes** — unequal timestamps, multiple
   contradictions, partial/ambiguous contradiction, more than two live
   candidates, missing provenance, changing source identity, disputes
   involving prior installed state. Default: the conservative behavior
   (withhold), never extrapolated looseness. New shapes need new
   preregistered trials + licenses.
8. **A pending T2 channel** — T1 does not preempt an elected T2
   deferral (§4.3).
9. **Un-oracle-verifiable installs** — any install whose correctness
   cannot be verified independently of the source is outside this
   license: the evidence base doesn't cover it and the track-record
   ledger cannot be scored on it.
10. **High-k on derived thresholds** — the k/(k+1) table for k>1 is
    derived (measured only at k=1). High-stakes firings require the
    strict CI gate (§3.1.6) and are audit-flagged for governance
    review.

---

## §7 Governance

- The **k cost table** (§1.1) and the **reliability ledger** (§3) are
  human-owned, versioned, audited, visible, and reversible policy data.
  The system never self-amends them.
- **Amendments** to this license — rules, thresholds, windows, tables,
  or the dispute-shape scope — require Micah's re-approval (standing
  rule: any change to rules/schedule/tests/metrics/kill criteria needs
  re-approval). Bent rules are documented and flagged for revert.
- **Review triggers:** KB-K3 table drift; KB-T2-2 deployment ρ decay;
  any §6.10 audit flag cluster (≥3 high-k firings in one window).

---

## Annex A — debate record

**How the debate was run.** Micah ordered a genuine debate with native
subagents taking different positions plus independent Sol and Grok
consultation. Constraint encountered and recorded honestly: this
workstream ran as a depth-2 subagent with spawning disabled
(`can_spawn=no`), so **no native subagents could be fanned out**. The
native side of the debate is the workstream lead's own deliberated
positions (attributed "NATIVE-LEAD" below), developed against the frozen
evidence before seeing the consultants' answers. Sol (gpt-5.6-sol) and
Grok were consulted independently via UnoRouter. Model check
2026-09-22: `grok-4.7` is not listed on the connector (only `grok-4.6`);
per the standing instruction, `grok-4.6` was used — this is the
instructed choice, not a silent substitution. Sol's full-brief prompt
returned empty choices three times (provider-side null completions, 0
completion tokens; endpoint verified healthy on short prompts), so Sol
was consulted per-question instead; 4 of 5 answered, Q3 (tie guard)
failed after 3 further attempts and is recorded as SOL-NO-RESPONSE.

**Zero rhetoric-driven flips.** Every resolution below names its
evidence trigger. Where the consultants agreed with the native
position, the trigger is convergence on the measured results; where
they disagreed, the disagreement and its resolution are recorded.

### A.1 Positions (verbatim, attributed)

**Q1 — k assessment.**
- NATIVE-LEAD: P1-A — k fixed per claim-type in a versioned
  human-governed table (default k=1); system assigns claim-type via
  logged deliberation; k never revised from dispute evidence; backdoor
  seal = consequence-information only, disjoint maintenance from the
  reliability ledger. Kill bar: any k-assignment citing evidential
  content → void + fall back to k=1.
- SOL: "Position: A, with C as the fallback default. k should be an ex
  ante policy parameter in a versioned, human-governed table keyed by
  claim type and consequence class… k=1 is the universal default when
  classification is ambiguous… I reject B because case-level system
  assessment of stakes creates an opaque path to both stake inflation
  and self-estimated reliability." Kill bars: k changed after seeing
  outcomes; system self-selects a permissive class; table lacks
  versioning/rationale/audit/appeal; threshold used without independent
  r; install on genuine 2v2 tie.
- GROK (grok-4.6): "k is assessed externally by a human-governed,
  versioned cost table indexed by claim-type (default k=1… scaled upward
  for high-stakes factual claims such as public-health or legal)…
  the system never revises k from dispute-internal evidence." Kill bar:
  "Any demonstration that external human governance produces systematic
  inconsistency or that claim-type lobbying can shift k thresholds in
  ways that correlate with favored source reliability." Rejects B
  (reintroduces dispute-internal cues, violates twin-identity) and C
  (ignores differential consequences).

**Q2 — independent reliability.**
- NATIVE-LEAD: P2-A — scored hit-rate ledger per source per
  claim-type, n≥20, ground truth with no shared causal ancestry,
  recency-bounded, gate on the LOWER BOUND of a one-sided 95% CI
  strictly clearing k/(k+1); withhold-on-unknown proved from EV
  (unknown-sign EV + measured destruction regime unexcludable by
  twin-identity + guaranteed-0 withhold).
- SOL: concurs with the criteria and gives the cleanest proof:
  "EV(install) = (k+1)r − k; EV(withhold) = 0… When reliability is
  unknown, the system has no defensible lower bound showing r >
  k/(k+1)… under a worst-case decision rule with r∈[0,1], installation
  has minimum EV −k, while withholding has guaranteed EV 0. Thus
  withholding strictly dominates installation on the worst-case
  evidence available." Adds: ledger must record hits AND misses
  including abstentions under a fixed rule; strict inequality
  L95 > k/(k+1) as the kill bar; recency "last 24 months or a declared
  exponential decay window"; adjudicator must not have access to the
  source's answer.
- GROK: concurs: "r is the lower bound of a one-sided Clopper-Pearson
  (or Bayesian) 95% CI… n≥20… recency-bounded (e.g., last 5 years)…
  When n<20 or no qualifying track record exists, default to withhold."
  Kill bar: "Evidence that the required independent ground-truth
  pipeline is infeasible at scale or that the lower-bound procedure
  fails to control false-positive installation rates."

**Q3 — tie guard.**
- NATIVE-LEAD: P3-A — tie = evidential draw (no frozen selection rule
  uniquely picks a side); PARK = logged, no install ever, NO confidence
  emitted, re-open only on new evidence, never ages into install.
- GROK: concurs: "A tie exists whenever the evidence graph contains no
  frozen epistemic rule… that uniquely selects one side… Response: the
  system logs the dispute as 'parked tie,' emits no confidence value
  whatsoever, installs nothing, and re-checks only on arrival of new
  evidence." Kill bar: "Empirical data showing that the broader
  definition causes excessive parking of genuinely resolvable disputes
  or that a narrower literal-2v2 definition suffices without increasing
  install errors."
- SOL: "Position: adopt the mandatory PARK guard, and make it
  structural rather than limited to the measured 2v2/S8 pattern. A tie
  is any unresolved candidate set in which: (1) two or more mutually
  exclusive answers remain live; (2) their decision-relevant support is
  equal within the system's declared comparison precision after
  deduplication and source weighting; (3) no candidate has a qualifying
  independent corroboration advantage; (4) the difference cannot be
  resolved by timestamp precedence, source identity, provenance quality,
  or an explicit rule already validated for that shape… Tie behavior:
  set state to PARK… emit no confidence, probability, ranking, or 'best
  current answer' value… do not treat parking as support for either
  candidate… never allow elapsed time, retries, source refreshes
  containing the same evidence, or ordinary aging to convert PARK into
  an install." Kill bar: "the guard fails if any tied input can produce
  an install or any non-null confidence value, including through
  fallback, timeout, aging, source refresh, or serialization defaults.
  The measured acceptance criterion is 0/20 false-confidence emissions
  and 0/20 installs on the genuine 2v2 tie corpus, plus adversarial
  coverage for n:n, weighted, multi-candidate, and stale-refresh
  variants. Until that bar is met, the tie guard is not deployable."
  (Arrived on retry; the full-brief and first per-question attempts
  returned provider-side empty completions.)

**Q4 — T2 channel qualification.**
- NATIVE-LEAD: P4-A lineage-based — provenance-disjoint lineage proven
  from records before content comparison; agreement is the test, never
  the qualification; anti-syndication; dispute competence (q>0);
  retirement after bounded wait → DEFER_RETIRED_UNRESOLVED, no
  retroactive install.
- SOL: concurs and strengthens: adds "no hidden common control" (not
  owned/commissioned/edited/controlled by the primary or its
  syndication chain), "no content contamination" (channel's
  investigators did not see the primary answer first), "independent
  access and process," "dispute competence," auditable records.
  "My kill bar is strict: if provenance disjointness or
  dispute-solving capability cannot be affirmatively demonstrated, T2
  fails closed." Frontier restated; if the channel never clears: "the
  item remains SUSPECT/deferred. No install, no
  contradiction-resolution score, and no confidence credit is awarded."
- GROK: concurs: "Qualification is lineage-based… proven from
  immutable provenance records; the channel must be capable of settling
  this specific dispute (q>0); agreement between channels is the test,
  never the qualification." Adds runtime recording of the (ρ,q,δ)
  triple and a retirement rule ("after time T unresolved, treat as
  withhold"). Kill bar: "Evidence that lineage provenance records are
  themselves manipulable or that q cannot be pre-certified."

**Q5 — boundaries.**
- NATIVE-LEAD: corroborated disputes; skepticism claims; ties;
  no-reliability; non-factual installs; untested shapes; high-k on
  derived thresholds (audit-flagged).
- SOL: 8-point list — ties (hard veto); no usable external
  reliability; r below threshold; non-factual outputs
  ("Recommendations, classifications, policy choices, forecasts,
  normative judgments…"); untested shapes ("unequal timestamps,
  multiple contradictions, partial or ambiguous contradiction, more
  than two live candidates, missing provenance, changing source
  identity, or disputes involving prior installed state"); corroborated
  disputes as non-T1; skepticism claims; and "A pending causally
  independent second channel — T1 does not preempt T2." Kill bar: "any
  hard veto above blocks installation."
- GROK: concurs with additions: "any install whose correctness cannot
  be oracle-verified independently of the source" and untested shapes
  incl. "primary vs. multiple independent contradictors, temporal drift
  without recency bounding."

### A.2 Disagreements and resolutions (with triggers)

1. **Recency window (Q2): Grok 5 years vs Sol/NATIVE-LEAD 24 months.**
   Trigger: none is measured — the trials never varied recency, so no
   evidence pins either number. Resolution: the window is a declared
   per-claim-type parameter, DEFAULT 24 months (the conservative bound;
   stale history must not qualify a degraded source), marked
   PROVISIONAL and revisable by amendment when measured. Grok's
   position is recorded, not adopted as default.
2. **Table keying (Q1): Sol's "claim-type × consequence class" vs
   NATIVE-LEAD's "claim-type".** Trigger: Sol's factor list (harm,
   reversibility, scope, cost of withholding, legal/safety obligations)
   is strictly more auditable than claim-type alone. Resolution:
   ADOPTED as a refinement — §1.1 keys on claim-type × consequence
   class. Not a disagreement on substance.
3. **Strict vs non-strict inequality (Q2 gate).** Sol's kill bar uses
   L95 > k/(k+1) (strict); the verdict table states r ≥ k/(k+1).
   Trigger: at exact equality the measured EV is 0.00 — firing there
   adds zero value while spending the audit budget. Resolution: the
   CI gate uses STRICT >, the table keeps ≥ as the theoretical
   break-even. Adopted.
4. **Abstention bookkeeping (Q2): Sol's addition** — the ledger must
   record hits, misses, AND abstentions/unresolved under a fixed rule.
   Trigger: cherry-picked successes would inflate r; the trials'
   n=20/level design counted every envelope. Resolution: ADOPTED in
   §3.1.3.
5. **Channel control/contamination (Q4): Sol's additions** — no hidden
   common control, no content contamination, independent access and
   process. Trigger: a "separate organization" can still be a disguised
   second reading via shared wire, commissioned work, or previewed
   answers — the exact failure the qualification exists to exclude.
   Resolution: ADOPTED in §4.1.3–4.
6. **Oracle-verifiability boundary (Q5): Grok's addition** — installs
   whose correctness cannot be oracle-verified independently of the
   source are outside the license. Trigger: the entire evidence base
   (and the track-record ledger itself) presupposes independent
   verification; without it neither the gate nor the ledger can be
   scored. Resolution: ADOPTED as §6.9.
7. **T1/T2 preemption (Q5): Sol's point 8** — T1 does not preempt an
   elected T2 deferral. Trigger: firing T1 while a channel is pending
   would moot the priced deferral the license just granted. Resolution:
   ADOPTED in §4.3 and §6.8.
8. **Narrow vs broad tie definition (Q3):** three-way convergence on
   the broad structural class — NATIVE-LEAD, GROK, and SOL all adopt
   PARK for the evidential-draw class, not just literal 2v2. Sol's
   formal four-condition definition and its acceptance criterion
   (0/20 installs, 0/20 false-confidence emissions, adversarial
   coverage for n:n/weighted/multi-candidate/stale-refresh) were
   ADOPTED into §2. The narrow 2v2-only candidate was killed by the
   trial itself (any non-unique selection produced 100% false
   confidence under both rules).

### A.3 Kill bars evaluated

| Kill bar | Status |
|---|---|
| KB-K1 backdoor (k citing evidential content) | STANDING — §1.1 |
| KB-K2 ex-post k revision | STANDING — §1.1 |
| KB-K3 table drift (≥3 disputes) | STANDING — §1.1, review trigger §7 |
| Tie-guard breach (install from TIE shape) | STANDING — §2, suspends all licenses |
| KB-T2-1 unqualified channel deferral | STANDING — §4.1 |
| KB-T2-2 deployment ρ below frontier | STANDING — §4.2, suspends T2 there |
| KB-T2-3 silent deadline-to-install | STANDING — §4.3, suspends T2 |
| Grok Q2: ground-truth pipeline infeasible at scale | NOT TRIGGERED — no such evidence; monitored |
| Grok Q3: broad tie def causes excessive parking | NOT TRIGGERED — no such evidence; monitored |
| Grok Q4: provenance records manipulable | NOT TRIGGERED — no such evidence; monitored |
| Q5 candidates: rule outside boundaries improving EV on held-out data | NOT TRIGGERED — no such rule presented |

### A.4 What the debate did NOT settle (honest gaps)

- The **recency window default** (24 months) is provisional, not
  measured — needs its own trial or amendment.
- The **k>1 thresholds** are derived, not measured — validated only at
  k=1; high-k firings are audit-flagged (§6.10).
- The **lower-bound CI gate** is derived law (statistically honest),
  not a measured trial result — the trials used stipulated r.
- Sol's full-brief prompt returned provider-side empty completions 3
  times (endpoint verified healthy on short prompts); Sol was
  consulted per-question instead, Q3 arriving on retry — all five
  questions now carry all three positions.
- **Native subagent fan-out** was impossible in this runtime (depth
  2/2, spawning disabled); the native side is the workstream lead's
  deliberated positions, attributed as such.

---

*Evidence pointers: `mixed-web/authority/round3/VERDICT-MW-R3.md`,
`mixed-web/authority/round3/AMENDMENT-A3.md`,
`mixed-web/authority/third-path/VERDICT-TP1.md` (branch
`tnn-native-lab`). This license: `mixed-web/authority/SOURCE_AUTHORITY_LICENSE.md`.*
