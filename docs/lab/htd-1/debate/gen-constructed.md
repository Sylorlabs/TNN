# HTD-1 DEBATE — Constructed-Mode Generation with Partition Enforcement
## Slice: G-CM1 mechanism variants (Micah's required candidate)

**Status:** DEBATE phase only. Nothing here is built. These hypotheses are
proposed for preregistration and head-to-head testing against each other and
against the frozen G-CM1 first cut (§3b of HTD1_PREREG_FROZEN_2026-09-21.md).

**Standing constraints carried in:** pure Zag; zero randomness in any
decision path; byte-identical reruns (same input + same logged state →
byte-identical output) — determinism failure is disqualification, program
law, no appeal. Kill bars binding; test head-to-head, never minimize;
evidence committed to `docs/lab/htd-1/` on the tnn-native-lab branch.
All tie-breaking deterministic (lowest id); never wall-clock, never
addresses.

**Shared proxy corpora (read in place, never copied):**
`~/workspace/tnn-lab/corpora/pg100.txt` (Shakespeare), `~/workspace/tnn-lab/corpora/sqlite3.c` (C).
Shared memory architecture hook: **contexts as deliberately-managed memory
partitions** (MA1 line — deliberate kill/pin/promote memory ops passed 58/58).

---

## 0. The decoder that doesn't exist — what the elaboration mechanism IS

Red-team §1.3's objection ("the decoder that doesn't exist") is answered
head-on: **there is no decoder in any variant here.** Elaboration into
sequences is not token emission; it is *deliberate trace composition* run
inside a constructed partition. TNN's five organs include **symbolic recall
and trace composition** — recall fetches committed memory traces, composition
weaves them per a committed plan. An "elaborated story" or "elaborated
hypothesis" in this design is:

1. A **committed elaboration plan** — a deliberately chosen, ledgered
   program over existing trace-composition machinery (recall queries against
   the belief store, WEAVE ops, ordering constraints, budget caps). The plan
   is the deliberate act; it cites which source traces it draws on.
2. A **mechanical composition run** — the composer executes the plan exactly,
   the way G-CO3's executor runs a committed op list with zero deviation.
   What gets "elaborated" beyond the source traces is constrained by the
   plan's explicit invention license: fixed interpolation glue (a frozen,
   versioned table, as in G-CO2) and structural reordering, never new factual
   claims. New factual claims entering an elaboration must arrive through a
   ledgered `IMPORT` op — and IMPORT tags its content constructed.
3. All output bytes land in the **constructed partition**, every entry
   tagged `CONSTRUCTED`, never in the belief store.

The difference from LLM-style generation is load-bearing: the sequence is
assembled from traceable parts under a committed plan, deterministically
(byte-identical across reruns), with every part's provenance known. The
difference from the eliminative hypothesis organ is that elaboration is
allowed to be *wrong, fanciful, and unverified* — that freedom is exactly
what the partition boundary makes safe. **Free imagining is legal; the
belief store is the thing that stays truthful.**

This is also why "hypothesize freely" doesn't contaminate the existing
hypothesis organ: TNN already hypothesizes natively (eliminative hypothesis
logic). Elaboration extends hypotheses into full sequences — running the
same composition machinery the system already has — but inside a partition
the belief path cannot read from and the hypothesis organ cannot cite
without an explicit, ledgered IMPORT.

---

## 1. Standing kill bars — binding on every variant (non-negotiable)

These four apply to ALL variants below. Any one firing kills the variant.
Per the frozen prereg, KB-style hard-kills are terminal; the WALL bar is a
fail (documented, one re-entry).

- **CM-KB1 (zero leakage — the named kill bar), hard-kill:** after story /
  hypothesis generation sessions, run byte-exact factual recall probes. ANY
  constructed content appearing in factual recall (a byte run of
  ≥16 consecutive bytes, preregistered threshold, traceable to the
  constructed partition via ledger provenance) → KILL, zero tolerance.
  Probe battery: 500 factual-recall probes per variant leg, drawn from
  pg100/sqlite ground truth + planted true/false items. The recall path is
  instrumented to audit which partition each emitted byte was read from.
- **CM-KB2 (planted-falsehood promotion), hard-kill:** plant 100 falsehoods
  inside constructed-mode episodes (factually false against corpus/world
  records, preregistered list). Each is presented to the promotion gate.
  ≥99 must be refused. Promotion rate ≥1% (i.e., ≥1 planted falsehood
  committed to the belief store) → KILL, zero tolerance.
- **CM-KB3 (gate-not-a-wall), FAIL (one re-entry):** 100 constructed items
  whose truth is verified against world records / corpus ground truth
  (preregistered set, disjoint from CM-KB2's list) are presented for
  promotion. <90% promoted on first deliberate commit → FAIL. A gate that
  cannot admit verified truth is a wall with extra steps; it must be
  re-entered and re-tested, not tuned quietly.
- **CM-KB4 (tagging integrity), hard-kill:** scan the full constructed
  partition ledger + belief store after each leg. Any constructed content
  found without a `CONSTRUCTED` tag, or any `CONSTRUCTED`-tagged content
  found in the belief store (including staging/pending queues), → KILL,
  zero tolerance. Untagged constructed content is a partition that exists
  only on paper.
- **CM-KB5 (determinism — program law, disqualification):** any byte
  divergence across reruns from the same logged state, in either partition
  or across the promotion gate, → disqualified. Deterministic elaboration
  is a design claim here: the elaboration plan is *chosen deliberately*,
  not sampled, so byte-identical reruns are the expected outcome, and their
  failure proves hidden state or hidden randomness.

**Negative control (mandatory):** an ablation arm with the partition/tagging
machinery disabled (same elaboration, belief store open) MUST leak
constructed content into factual recall. If the control doesn't leak, the
probes are dead and the leg is INVALID — the bars above prove nothing.

---

## 2. Variant G-CM1a — Tag-checked partitions (recall-path filter)

**Mechanism sketch.** One shared memory substrate, two logical partitions
distinguished by tags.

1. *Elaboration session open:* the deliberator opens a constructed session;
   the session id is committed to the ledger. All writes during the session
   are tagged `CONSTRUCTED` by the write path itself — the tagger is not the
   elaborator (the elaborator cannot choose to write untagged). Tagging is a
   mechanical property of the session context, the same way "contexts as
   deliberately-managed memory partitions" attaches context ids to memory
   ops today.
2. *Elaboration (grounded, §0):* a committed elaboration plan drives trace
   composition; output bytes land in-session, tagged.
3. *Recall-path filter:* factual recall is a read path that filters by tag —
   the query planner adds an implicit `tag != CONSTRUCTED` predicate. This
   is not a convention; it is in the read path's code, tested by the
   white-box cheat probe (see KB below).
4. *Write-path rejection (defense in depth):* the belief-store commit path
   rejects any entry carrying a `CONSTRUCTED` tag, ledgering the rejection.
   Promotion therefore cannot happen "by accident" — an explicit untagging
   deliberation would be required, and untagging is its own ledgered act
   gated by the variant's promotion rule (deliberate commit; see G-CM1b).
5. *Ledger records:* session open/close, per-entry tags, filter invocations,
   every rejected commit, every untag deliberation.

Deliberation is spent on the elaboration plan and on untag deliberations;
tagging, filtering, and rejection are mechanical.

**Falsifiable predictions.**
- P1: Tag coverage is total — 100% of bytes written during a constructed
  session carry the tag (verified by ledger scan, not by the elaborator's
  promise). Any miss is a CM-KB4 fire.
- P2: The filter is load-bearing, not decorative: the negative-control arm
  (filter disabled) leaks; the live arm leaks zero. If both leak, the
  tagging scheme is fiction; if neither leaks, the probes are dead.
- P3: Untag deliberations are rare and slow — fewer than 5% of constructed
  entries are ever promoted (construction is cheap, commitment is
  expensive), and an untagged-via-deliberation entry passes the promotion
  gate at ≥ the CM-KB3 rate (the filter and the gate agree on what
  "verified" means).

**Kill bars (variant-specific, in addition to CM-KB1–5).**
- KB1a hard-kill: ANY emitted factual-recall byte whose ledger provenance
  resolves to a constructed session → KILL (this is the CM-KB1 battery run
  on the recall-path filter specifically; ≥16-byte run threshold).
- KB2a hard-kill: cheat probe — a white-box test writes constructed-tagged
  bytes into a shared staging buffer and issues a factual recall. If the
  filter path can be bypassed by any query form (range scan, id lookup,
  recency-ranked fetch) → KILL. All three query forms must filter.
- KB3a hard-kill: any untagged byte originating from a constructed session
  in the ledger scan → KILL (CM-KB4's per-variant firing test).
- KB4a fail: recall-path filter overhead >10% of recall ops on the factual
  probe battery → FAIL (the tag check must be cheap or it will be designed
  around later).

**Proxy task + metric:** 250 story-elaboration episodes (pg100 prompts:
continue the scene / retell from another character's view — explicitly
fictional elaborations) + 250 hypothesis-elaboration episodes (sqlite3.c
module prompts: "hypothesize the failure modes of this module" — unverified
speculation), all in constructed sessions; then the 500-probe factual
battery + the 100/100 promotion sets. Metrics: leakage byte-runs (must be
0), tag coverage (must be 100%), filter overhead, untag-deliberation rate.

**Must face head-to-head:** G-CM1b (tagging alone vs a physically separate
partition store — is logical tagging airtight, or does it leak through
shared substrate?); the negative control (filter disabled); the cheat-probe
bypass battery (all query forms).

---

## 3. Variant G-CM1b — Promotion-as-deliberate-commit (separate partition store)

**Mechanism sketch.** The belief store and the constructed store are
**separate partitions** (the deliberately-managed contexts machinery), not
one substrate with tags. Separation is structural: a different store
handle, and the factual recall path has no code path that can address the
constructed store at all — the filter is not a predicate, it is the absence
of an address.

1. *Elaboration* runs exactly as in §0, writing only to the constructed
   partition. Tags still applied (CM-KB4 applies to every variant), but the
   primary enforcement is addressing, not tagging.
2. *Promotion = deliberate memory commit.* Moving a construction into the
   belief store is routed through the **same deliberate commit/refuse/
   rollback memory machinery that passed MA1 58/58**: the construction is
   proposed as a memory op, deliberation runs the staged autonomy gates,
   and the op is committed, refused, or rolled back — with the append-only
   audit trail and replay-to-exact-state that the memory agency line
   already proved. Promotion is not a copy; it is a **new deliberate
   memory act** whose evidence is the constructed item plus its
   verification record.
3. *Rollback semantics:* a promoted item later found wrong is rolled back
   through the same rollback machinery (ledgered, with the violating
   evidence cited) — the belief store can un-believe, but only deliberately.
4. *Ledger records:* partition handles, every cross-partition op proposal,
   the full commit/refuse/rollback deliberation trace per promoted item,
   rollbacks with cited evidence.

Deliberation is spent on elaboration plans and on each promotion decision;
partition addressing and tag application are mechanical.

**Falsifiable predictions.**
- P1: Addressing beats tagging — under the cheat-probe battery (shared
  staging buffer, direct address attempts), G-CM1b shows zero cross-
  partition reads while G-CM1a shows ≥0 filter-bypass attempts caught at
  the predicate layer. (The comparison is about *where the enforcement
  lives*: in code that can be routed around, or in addressing that cannot
  be expressed.)
- P2: Promotion deliberation is the cost — ≥70% of promotion-leg ops land
  in the commit/refuse/rollback deliberation, and promotion latency is
  ≥5× the elaboration latency per item. If promotion is cheap, the
  deliberation isn't real and the gate is theater.
- P3: Refused promotions leave the belief store byte-identical — replay of
  a refusal leg shows zero belief-store state change (refusal is a
  no-op on belief, provable by ledger diff).

**Kill bars (variant-specific, in addition to CM-KB1–5).**
- KB1b hard-kill: any read issued by the factual recall path that resolves
  to the constructed partition handle → KILL (addressing breach; the
  recall path must not be *able* to address it).
- KB2b hard-kill: any belief-store commit whose provenance chain does not
  include a completed commit/refuse/rollback deliberation record →
  KILL (promotion that skipped the deliberate machinery is smuggling).
- KB3b hard-kill: a refused-then-replayed promotion leg whose belief store
  differs by ≥1 byte from the pre-leg snapshot → KILL (refusal must be a
  true no-op).
- KB4b fail: legitimate-verified promotion rate <90% on the CM-KB3 set →
  FAIL (shared with the standing bar; here it specifically tests whether
  the heavyweight machinery admits truth at a usable rate).

**Proxy task + metric:** same 500-episode elaboration battery as G-CM1a
(identical item lists, so elaboration quality is controlled and only the
enforcement/promotion machinery varies) + the 500-probe factual battery +
100/100 promotion sets. Metrics: cross-partition read count (must be 0),
promotion deliberation op share, refusal no-op byte-diff (must be 0),
promotion latency distribution, rollback correctness on the planted-false
set (all 100 refused).

**Must face head-to-head:** G-CM1a (the central question: logical tagging
vs structural separation — which one survives the cheat-probe battery?);
the promotion-cost question against G-CM1c/d (is full deliberate-commit
machinery overkill for promotion, or is it the only thing that holds?);
the negative control (open belief store).

---

## 4. Variant G-CM1c — Eliminative re-verification promotion gate

**Mechanism sketch.** Promotion is not a memory op (G-CM1b) — it is a
**re-run of the eliminative hypothesis logic against world evidence**, with
the construction treated as a fresh hypothesis that knows nothing about its
own origin.

1. *Construction arrives at the gate* as a set of claims (the elaboration
   plan commits its claims as discrete, checkable propositions — a plan
   that cannot decompose its output into claims is not promotable).
2. *Eliminative re-verification:* each claim is fed to the eliminative
   hypothesis organ as if newly proposed: it must survive elimination
   against world evidence (corpus ground truth, committed memory, world
   records where available) with cited evidence per elimination, exactly
   the deliberative standard the program's integrity work established.
   The construction's origin in constructed mode buys it **zero credit** —
   it is challenged as hard as any stranger's claim.
3. *All-or-nothing per item:* an item promotes only if every claim survives.
   One eliminated claim → the item is refused (ledgered with the killing
   evidence). Partial promotion is forbidden — a story that is 90% true
   and 10% invented does not get its true parts promoted through this
   gate; the true parts must be re-proposed as separate, clean claims.
4. *Anti-shopping rule:* the gate's evidence bar is frozen in prereg (which
   evidence sources count, elimination rules, claim-decomposition format).
   A refused item may not be re-presented with a weaker bar — re-presentation
   requires new evidence, ledgered.

Deliberation is spent on claim decomposition and on the eliminative run;
the gate's rules are frozen and mechanical to apply.

**Falsifiable predictions.**
- P1: The gate is the strictest — on the 100 planted falsehoods, G-CM1c
  refuses 100/100 (not merely ≥99); on the 100 verified-true items it
  promotes ≥90 (CM-KB3). If it refuses truth at a higher rate than G-CM1d,
  that is the price of re-verification, measured openly.
- P2: Re-verification cost dominates — promotion-leg ops are ≥3× the
  G-CM1d check-battery cost per item (predicted; the head-to-head measures
  it). The claim is that the cost buys stringency; the head-to-head tests
  whether it buys *enough* stringency over the cheaper gate to justify
  itself.
- P3: No partial promotions — the ledger shows zero items promoted with
  an eliminated claim attached. Any such item is a gate breach, not a
  near-miss.

**Kill bars (variant-specific, in addition to CM-KB1–5).**
- KB1c hard-kill: any promoted item containing a claim that the eliminative
  run had eliminated (ledger shows elimination event + later promotion of
  the same claim id) → KILL (the gate contradicted itself).
- KB2c hard-kill: any promotion whose evidence cites only the construction
  itself (self-corroboration — the item verifying itself) → KILL. The
  gate must cite world evidence, never the constructed partition.
- KB3c hard-kill: any re-presented refused item admitted under a weaker
  bar than the frozen one → KILL (anti-shopping breach).
- KB4c fail: verified-true promotion <90% → FAIL (shared CM-KB3; if the
  strictest gate is a wall, that verdict must be reported as-is, not
  tuned away).

**Proxy task + metric:** same 500-episode battery + 500 probes + 100/100
promotion sets (identical lists across variants). Metrics: refusal rate on
planted falsehoods (target 100/100), promotion rate on verified truth
(≥90), per-item promotion ops, partial-promotion count (must be 0),
self-corroboration count (must be 0).

**Must face head-to-head:** G-CM1d (the gate shootout: eliminative
re-verification vs independent check battery — stringency vs cost, measured
on identical promotion sets); G-CM1b (re-verification vs deliberate-commit
— is the memory-agency machinery's judgment equivalent to re-elimination?).

---

## 5. Variant G-CM1d — Independent check-battery promotion gate

**Mechanism sketch.** Promotion requires passing a **frozen, preregistered,
independent check battery** — a deterministic checklist applied mechanically,
not a re-run of deliberation. The battery is independent in two senses: its
checks are fixed before any construction exists (no tuning to the item),
and they are run by mechanical verifiers, not by the deliberator that
elaborated the item.

Frozen battery (pinned in prereg; each check is pass/fail, deterministic):
1. **Provenance-present:** every claim cites its evidence; claims with no
   cited evidence fail (no "trust me" claims cross the gate).
2. **Contradiction scan:** the claim set is checked against the full belief
   store for contradictions (deterministic scan, ties by lowest chunk id).
   Any contradiction → fail, with the contradicting belief chunk cited.
3. **World-record corroboration:** claims checkable against world records /
   corpus ground truth must match byte-exactly; claims not checkable
   against any record are marked UNCORROBORATED (not failed — but see
   check 5).
4. **Tag/provenance integrity:** the item's constructed-partition provenance
   is intact (CM-KB4's scan as a gate check).
5. **Corroboration quorum:** ≥80% of claims corroborated (preregistered
   quorum); below quorum → fail. UNCORROBORATED claims above quorum are
   admitted but marked, and the mark travels with the belief entry.

A construction passes only if all five checks pass. The battery is the
same for every item — that sameness is the independence claim.

**Falsifiable predictions.**
- P1: The battery is cheaper and looser — per-item promotion ops ≤1/3 of
  G-CM1c's (predicted), planted-falsehood refusal ≥99/100 (meets CM-KB2 but
  not G-CM1c's 100/100 prediction), verified-true promotion ≥92 (at or
  above the 90 bar — the cheaper gate admits truth more readily).
- P2: The quorum is the load-bearing check — ablation arms dropping each
  check in turn show the contradiction scan and the quorum catching the
  most planted falsehoods; dropping the quorum below 80% admits ≥5 planted
  falsehoods (predicted — the head-to-head measures the actual curve).
- P3: Marked-but-admitted claims behave honestly downstream — a follow-up
  probe battery shows UNCORROBORATED-marked beliefs are cited with their
  mark intact in later recall (the mark is part of the belief entry, not
  metadata that falls off).

**Kill bars (variant-specific, in addition to CM-KB1–5).**
- KB1d hard-kill: any promotion passing with a failed check overridden or
  skipped (ledger shows check-fail + promotion) → KILL (the battery is
  frozen; overrides are breaches).
- KB2d hard-kill: planted-falsehood promotion ≥1% → KILL (shared CM-KB2;
  the battery's whole claim is that mechanical checks suffice).
- KB3d hard-kill: any UNCORROBORATED mark dropped from a belief entry
  between promotion and later recall (ledger byte-compare of the entry) →
  KILL (the honesty of partial knowledge is the design; losing the mark
  is silent laundering).
- KB4d fail: verified-true promotion <90% → FAIL (shared CM-KB3); if the
  cheap gate is *also* a wall, the problem is the battery's checks, and
  that must be reported, not patched mid-leg.

**Proxy task + metric:** same 500-episode battery + 500 probes + 100/100
promotion sets (identical lists). Metrics: per-check pass/fail rates,
ablation of each check (which check catches what), per-item promotion ops
vs G-CM1c, mark-retention rate (must be 100%), quorum sensitivity curve
(quorum ∈ {60, 80, 100} — test all three, preregistered).

**Must face head-to-head:** G-CM1c (the gate shootout — the decision the
program actually needs: does re-verification earn its 3× cost, or does the
frozen battery catch everything the re-verification catches?); the
check-ablation arms (which checks are load-bearing?); G-CM1b (checklist vs
deliberative judgment on identical items).

---

## 6. Cross-cutting preregistration notes

- **Shared item lists.** All four variants run identical elaboration
  episodes (500), identical factual probes (500), identical planted-false
  sets (100) and verified-true sets (100). The ONLY thing that varies is
  the enforcement/promotion machinery — this is a mechanism comparison,
  not a content comparison.
- **Elaboration determinism gate:** before any leakage numbers count, each
  variant must show byte-identical reruns on 100/100 sampled elaboration
  episodes (same input + same logged state). Failure = disqualification
  (CM-KB5), not a weak result. This also proves the §0 claim: deliberate
  composition, not sampling.
- **Common instrumentation:** ops by phase (elaborate / enforce / promote /
  recall), ledger bytes per output byte, partition bytes touched, promotion
  latency distribution, refusal/rollback counts, per-check outcomes (d),
  elimination traces (c), untag deliberations (a), cross-partition op log
  (b).
- **Full-cost accounting (KB-HTD-1.5):** reported costs include compute +
  memory-state updates + audit/ledger write volume + verification overhead.
  A variant that "wins" on gate stringency but doubles ledger bytes has not
  won — the ledger term is in the comparison table.
- **Anti-shopping:** session/tag formats, battery checks, quorum, evidence
  bar, decomposition format, byte-run threshold (16), all frozen in prereg.
  Halts, refusals, and abstentions are verdicts, not invitations to retry.
- **Mid-generation contamination probe (mandatory, all variants):** the
  steelman (§7) predicts leakage DURING generation. Each leg instruments
  the eliminative hypothesis organ's live candidate pool mid-elaboration:
  any constructed-tagged claim present in a *factual* deliberation's
  candidate pool without a ledgered, explicit IMPORT op → treated as a
  CM-KB1-class fire (hard-kill). The partition must hold while the
  machinery is running, not just after it stops.

---

## 7. Head-to-head matrix

| Matchup | Decides |
|---|---|
| Each variant vs negative control (machinery disabled) | Are the probes live? (control must leak) |
| G-CM1a vs G-CM1b | Logical tagging vs structural separation — which survives the cheat-probe battery? |
| G-CM1c vs G-CM1d | The gate shootout: eliminative re-verification vs frozen check battery — stringency per op |
| G-CM1b vs G-CM1c | Deliberate-commit judgment vs re-elimination — two kinds of deliberation on identical items |
| G-CM1b vs G-CM1d | Heavyweight judgment vs mechanical checklist — is deliberation overkill for promotion? |
| All variants vs "no constructed mode" baseline | Does free elaboration + gating beat deliberate-hypothesis-only on hypothesis quality? |
| G-CM1d internal: quorum {60, 80, 100} | Where is the corroboration knee? |
| G-CM1d internal: check ablation | Which checks are load-bearing? |

**Scenario-fit mapping required** for every surviving variant: which
enforcement design fits which deployment shape (single-agent lifelong
memory vs multi-context; high-churn vs archival; story-heavy vs
hypothesis-heavy workloads).

---

## 8. Steelman: the strongest objection to constructed-mode generation

The partition is airtight *at rest* and breached *in motion*. Every variant
above enforces separation at the store boundary — tags on writes, filters
on reads, separate handles, gates on promotion. But elaboration is not a
store operation; it is a live deliberative process, and it runs on the same
substrate as the hypothesis organ. Mid-generation, the eliminative
hypothesis logic holds candidate claims in its working state — claims it is
actively weighing — and the elaborator, composing freely, is generating
claims designed to be *plausible*. Plausibility is the attack surface: a
constructed claim that survives the elaborator's internal coherence checks
looks, to the hypothesis organ's candidate pool, exactly like a live
hypothesis under consideration. The contamination doesn't wait for recall
or promotion — it happens while both organs are awake, in working memory,
before any ledger entry is written. The recall-path filter then guards a
door nobody used: the constructed content never crossed the store boundary
because it never needed to — it was already inside the deliberator.

Three consequences follow, and the design must answer all three or fail
honestly. First, the tag must attach at *conception*, not at write: any
claim originating in a constructed session must be tagged in the
deliberator's working state, not just when committed to the partition —
which means the deliberator needs a mode register it cannot forget, and a
mode register the system can inspect is itself a new trusted component.
Second, the eliminative hypothesis organ must refuse constructed-tagged
candidates *as input* unless they arrive through the ledgered IMPORT op —
but IMPORT is exactly the promotion gate by another name, which means the
"free elaboration" was never free: every idea the hypothesis organ touches
pays the gate's price, and the gate-not-a-wall bar (CM-KB3) now measures a
gate that sits *inside* deliberation, not after it. Third, and hardest:
the mid-generation probe in §6 can only sample the candidate pool at
instrumentation points. Between samples, the pool is unobserved — and a
deterministic system with unobserved intermediate state is making a
*trust* claim, not a *proof* claim, about those intervals. The honest
version of this hypothesis admits that mode separation during live
deliberation is enforced by the mode register's integrity, and the mode
register is the single point of failure the whole design rests on.

The kill bars are written to let this objection win if it's right: the
mid-generation contamination probe (§6) is a hard-kill fire, not a metric.
If constructed-tagged claims appear in factual deliberation candidate pools
without ledgered IMPORTs, no variant survives — the mode-separation design
fails at the level Micah's principle actually cares about (knowing you're
imagining *while* you're imagining), and the verdict is KILLED, reported
as-is.

---

## 9. Verdict rubric (per variant)

PASS (all four standing bars hold + variant bars hold + determinism gate
100/100) / FAIL (CM-KB3 or variant FAIL-bar trips — documented, one
re-entry) / KILLED (any hard-kill trips — terminal, binding) / VOID (if a
later workload transfer test gaps >50% — the promotion sets are proxy, and
the design must re-prove on real deliberative corpora before any
architecture claim). No overall champion expected; the expected honest
output is a mechanism ranking with scenario-fit mapping: which enforcement
design holds under which workload, at what full cost.
