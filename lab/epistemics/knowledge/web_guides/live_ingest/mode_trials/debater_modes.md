# LI Modes Cross-Check — native steelman FOR separate training/production modes

**Role:** independent cross-check debater (depth-2 subagent; the debate
coordinator authored the in-file native-Muse takes directly, so this is a
second native pass). **Position assigned:** steelman FOR (a) — separate
TRAINING mode vs PRODUCTION mode — and AGAINST (b) unified mode.
**Date:** 2026-09-23.

**Sources read (branch `tnn-native-lab` of `sylorlabs/TNN`, SHAs verified on fetch):**
- `docs/lab/knowledge/web_guides/live_ingest/mode_trials/DEBATES_LI_MODES.md`
  (807 lines; blob `256748512c323627468d275aa8ef40ec0191c3d2`)
- `docs/lab/knowledge/web_guides/live_ingest/mode_trials/HYPOTHESES_LI_MODES.md`
  (273 lines; blob `da4bdc74d6c86d7e9679156b8dd036c463adeb37`)

I do not modify the frozen prereg. Genuine holes found while steelmanning
are flagged as caveats in §7 for the coordinator, not edited into
`HYPOTHESES_LI_MODES.md`.

---

## 1. The steelman for (a): what separate modes actually buy

The (a)-against side's best line is that forced ingest contradicts
deliberate memory agency and that the merge gate has no stable third
setting. The steelman answers both by being precise about what a "mode" is:

**A mode is not a second mind. It is a labeled, budgeted, auditable
operating context for one mind.** The production ledger is the belief store.
The quarantine partition is a perceptual buffer. Between them sits a merge
gate that is a pure deterministic function. Nothing becomes a belief without
passing the gate. That is deliberate agency *implemented*, not suspended —
the system deliberately holds candidates without endorsing them, which is
exactly the consideration-vs-endorsement distinction that deliberate memory
agency requires. The (a)-against side conflates forced *ingest into a
buffer* with forced *belief*. Those are different acts, and a system that
cannot tell them apart has no working memory at all.

Concretely, (a) buys five things no other position buys:

1. **Candidate throughput without acceptance looseness.** Training mode
   converts "0 installs, 107 withholds" into "N candidate clusters awaiting
   adjudication" (Muse-A1). Production acceptance never moves. The
   throughput problem and the integrity problem are factored into separate
   mechanisms with separate kill bars, instead of being smeared across one
   rulebook where every throughput fix is an integrity risk.

2. **Legibility.** Every install row carries its mode tag; every run's
   manifest commits to instrument SHA + corpus SHA + mode + prereg SHA.
   Post-hoc audit can *mechanically* check "all production installs have
   mode=production." Any position that applies different standards at
   different times without labeling them — curiosity heuristics, quotas,
   paraphrase thresholds — buries the same distinction where auditors
   cannot see it. Explicitness is the security property.

3. **A real answer to novelty.** (b) can only ever learn what ≥2 hosts
   already say byte-identically (see §4). Novel facts are single-source by
   definition at first publication. Only a mode whose candidate rule is
   looser than production's acceptance rule can *generate candidates* for
   the genuinely new — which is what Micah's fixtures demand and what
   training is for.

4. **The human analogy, taken seriously, supports (a).** Sol-B1's toddler
   is the strongest (b) intuition and it is empirically false as stated:
   children DO run a loose-acceptance training mode — they believe what
   they are told — and parents, teachers, and peer correction serve as the
   adjudicating merge gate into reliable adult belief. "Childhood" is the
   quarantine partition; "growing up" is the merge. What makes some humans
   reliable is not a magic unified faculty but external correction
   machinery: peer review, replication, the merge gate. The human existence
   proof is an existence proof *for* (a).

5. **Compatibility with (b)'s only working idea.** Directed
   second-source scouting (D1, the salvage of (b)) is a *scout policy* —
   it slots into training mode unchanged, with the instrument untouched.
   (a) absorbs (b)'s best engineering content; (b) cannot absorb (a)'s.

---

## 2. Answering the pollution objection head-on

**The objection, at full strength:** "Pollution happens before the merge
gate. Anything the learner reads during training — hypotheses formed from
candidates, query selection biased by them, retrieval paths shaped by
them — persists after the ledger rows are deleted. You cannot un-train a
mind. Quarantine answers where rows live, not what the reasoner read."

**The answer has two parts: an architectural part and a conceptual part.**

**Conceptual part first.** The objection proves too much: applied
consistently, it forbids *considering* any proposition the system does not
already believe — including every withheld singleton, every red-team attack
case, every hypothesis under test. The LI instrument already *reads*
falsehoods all day (the R1 battery, the 107 withholds, injection-flagged
pages at teach). Reading a candidate is not believing it. The program's own
main line — deliberate memory agency — is precisely the capacity to hold
content without endorsing it. If merely processing a false sentence
contaminated the mind, the red-team battery itself would be a contamination
event. The objection's real content is narrower and correct: *unendorsed
content must not shape endorsed state except through the gate.* That is an
engineering requirement, not a refutation. Here is the engineering:

**Containment design (concrete).** Four binaries/processes, partition-tagged
state, no shared mutable substrate:

- **P-ledger** (production beliefs) and **Q-ledger** (quarantine
  candidates) are separate append-only SHA-chained logs (the program
  already has append-only audit with replay-to-exact-state; MA1 58/58).
  Separate chains, not one chain with a flag column — a flag column is
  one UPDATE away from relabeling; separate chains make cross-partition
  writes a structural impossibility, not a policy choice.
- **Training binary:** reads P read-only (novelty checks) + web corpus;
  writes Q only. Its Q-writes are mode-tagged at the row level.
- **Production binary:** reads P only. The Q partition is not merely
  access-controlled — *it is not in the binary's partition table.*
  There is no code path in the production binary that addresses Q, so
  "the reasoner reads quarantine" is not a policy violation waiting to
  happen; it is unrepresentable in the running code.
- **Merge binary:** reads Q + P (read-only) + evidence; writes P only.
  It is a **stateless pure function per claim**: no cross-claim memory,
  no source-reputation accumulation from Q content. Its only output
  channel to production is the verdict bit + citation, and the verdict
  bit is itself subject to the production acceptance predicate. Even the
  merge gate's reads are contained: influence flows Q → verdict → gate,
  never Q → belief.
- **Audit:** every ledger read in every run is logged as
  `(run_id, binary_id, partition, slot_id, content_hash)` — **content-free**
  (hashes, never claim text; see §5 leak #3). An offline verifier replays
  the chains and checks partition discipline mechanically.

**Why this answers "you can't un-train a mind":** in this architecture the
mind's state *is* its ledgers (deliberate memory substrate — the program's
chosen design, not a neural weight matrix). There is no sub-ledger
substrate where "inferences generated from provisional falsehoods" can hide:
hypotheses, priorities, and retrieval paths in webg are deterministic
functions of (ledger state, query, frozen code). If Q is unaddressable by
the production binary, then production behavior is a function of P alone —
provable by replay, not by assertion. The objection assumes a mind with
inscrutable implicit state (weights, activations). That is the LLM's mind,
not TNN's. For a ledger-based deterministic mind, "un-training" is just
"never having written to P," and partition separation makes that checkable.

**The honest residual:** this argument holds *for the LI instrument*
(webg.zag), whose state is explicit. It does not automatically transfer to
any future TNN subsystem with implicit learned state. If training mode is
ever extended past the ingestion pipeline into systems with inscrutable
state, the pollution objection re-arms at full strength and this steelman
does not cover it. Flagging that boundary now is part of the honest case.

---

## 3. Answering the mode-bit objection head-on

**The objection:** "The mode flag is an attack surface. One flipped bit —
bug, stale config, compromised wrapper — sends production traffic through
the looser path. Under a single strict instrument, safety is intrinsic to
the instrument; under two modes it depends on scheduler discipline."

**Three defenses, in increasing strength:**

1. **The bit is hashed, not trusted.** The mode flag is not a runtime
   toggle in the hot path; it is a run-configuration parameter frozen in
   the prereg and committed into the run manifest
   (`SHA(instrument) ‖ SHA(corpus) ‖ mode ‖ SHA(prereg)`), which heads the
   append-only audit chain. A flipped bit produces a run whose manifest
   disagrees with the prereg — the verifier rejects it mechanically.
   The attack is not "flip one bit"; it is "flip one bit AND forge the
   SHA chain AND rewrite the prereg," which is exactly the base integrity
   assumption of the entire program (forging any ledger entry). The mode
   bit adds no *new* assumption.

2. **Explicit beats buried.** Every install row carries its mode tag, so
   the audit question "did any training-looseness reach production?" is a
   mechanical filter over rows. Contrast (b)-unified with a hidden
   curiosity governor: a bug in the governor's judgment changes acceptance
   behavior with *no visible flag anywhere* — the log shows one mode
   throughout, and post-hoc audit must re-derive the governor's judgment
   per install to detect the shift. (b) does not remove the attack
   surface; it removes the *label* on the attack surface. A labeled
   boundary is auditable; an unlabeled one is where real compromises hide.

3. **Strongest form: there is no bit in the production binary.**
   Per the §2 design, mode selection is *which frozen binary runs*, chosen
   at the deployment layer — not a flag consulted by running code. The
   production binary contains no training-looseness code path to enable;
   flipping a bit inside it cannot conjure machinery that is not there.
   And the deployment layer (scheduler) is *already* trusted with worse:
   it chooses which corpus gets crawled. A compromised scheduler can feed
   poisoned URLs to a strict instrument today. The mode selector adds
   nothing to that trust.

**Conceded sharp edge:** defense 3 relocates trust to "the scheduler runs
the binary the prereg names," which is verified by manifest hash — i.e.,
defense 3 reduces to defense 1 at the deployment boundary. That is fine;
the point is that the trust chain is *explicit and checkable at every
link*, which is more than (b) offers.

---

## 4. Attacking (b): why "the learner figures out what to learn" is not engineering

**(i) It names a capability, not a mechanism.** In deterministic Zag with
zero reward signals in decision paths (standing law), "figures out" must
bottom out in a *function*: inputs (ledger state, corpus) → ranked agenda.
Every implementable instance anyone has named — novelty, surprise,
coverage-gap priority, cluster-size priority — is either a fixed ranking
rule (a reward signal in a trench coat, per Sol-B2) or reproduces current
behavior with extra steps. The FOR-(b) side itself retreated to "a work
queue / fixed judgment rules," which is much thinner than "human-like
figuring out." Until the criterion is written as a frozen function with
stated inputs, (b) is a slogan with a missing demo — and the program's own
testing standard ("real mechanisms, not stubs") applies to architectures
too.

**(ii) The work-queue defense fails exactly where it matters: novelty.**
Muse-B1's salvage — withheld singletons become a deterministic work queue,
scouts seek second sources, acceptance never moves — is the best
engineering content in (b). Grant it everything. Now ask: *what happens
when second sources don't exist?* For a genuinely novel fact (Micah's
fixtures: facts new to the instrument), there is no second independent
host — that is what "novel" means. The scout burns fetch budget and
returns a withhold. Worse, the queue's own preregistered priority ("larger
clusters first") *systematically deprioritizes the novel*: cluster size 1
sorts last. So the work queue is not merely neutral on novelty — it is
**anti-novelty by construction**, pursuing corroboration where
corroboration is likeliest, i.e., for the already-popular. The genuinely
new sits at the back of the queue forever. (b)'s learnable set is
{claims ≥2 hosts already state byte-identically} — rediscovery, not
learning. A training pipeline that cannot ingest novelty is not a training
pipeline; it is a corroboration-verification service.

**(iii) (b) dissolves into (a) + D1.** The work queue has a separate fetch
budget, a separate target corpus (second-source targets), and separate
accounting. That *is* a training-mode component with a different name. And
the "truth-tracking governor" Sol-B2 notes (b) needs to avoid the
sensationalism tilt *is* a mode boundary — a policy that behaves
differently across contexts — just an unlabeled, unaudited one. (b)'s
position, shorn of its working mechanism, is the labeling preference "no
modes"; its working mechanism, shorn of the label, is (a)'s scout policy.
There is no remaining content to the disagreement.

**(iv) The sensationalism tilt is disqualifying for the naive form and
unanswered for the sophisticated form.** High-novelty/high-surprise content
gets priority under any curiosity ranking, and confident falsehoods are
systematically more novel than true beginner-guide prose. Nobody on the
(b)-FOR side specified the governor that prevents the queue from becoming
a confident-falsehood prioritizer — because any such governor needs a
truth-tracking criterion, which is the very capability under dispute.
Circular all the way down.

**(v) "Humans do it" cuts against (b).** Humans with one mode and no
correction machinery fall for cults, conspiracies, and confident cranks —
the (b)-AGAINST catalog is the empirical record of *unified-mode human
learning*. What distinguishes reliable human learners is external
correction machinery (peer review, replication, teachers) — i.e., merge
gates and quarantine, not a unified faculty. The human evidence supports
(a).

---

## 5. Stress-testing H3-K3: is "no non-merge-gate read of quarantine" instrumentable?

**Short answer:** the *in-Zag* read path is instrumentable to high
confidence — pure Zag has no reflection, no eval, no dynamic dispatch
outside visible code, so a single accessor with an inline partition check
plus a content-free audit log can mediate every read. **Every gap lives at
a boundary**, and the kill bar as written ("anything except the merge
gate") is both too narrow and too broad. Enumerated leak vectors, ordered
by where they hide:

**In-Zag (mediable by construction):**
- **L1 — Direct arena indexing.** If Q is a `[]u8` arena and any code path
  indexes it outside the single `qread` accessor, the read-check is
  theater. Mitigation: the arena handle lives in one module whose only
  export is the accessor; CI grep-verified that no other indexing of the
  arena symbol exists. (znc's lack of slice→pointer casts,
  ZNC-2026-09-21-002, actually helps here — there is no pointer-smuggling
  idiom available to bypass the accessor.)
- **L2 — Debug/dump paths.** A "dump ledger for diagnostics" helper that
  `_zag_print`s Q content to stdout bypasses the read log (stdout is not
  a ledger read). Any Q dump must be content-hashed, never content.

**Boundary (where leaks actually hide — all must be named in the test protocol):**
- **L3 — The audit log content channel.** If read-check entries contain
  claim text and *any runtime component* reads the audit log
  (self-inspection, "what did I do?"), Q content flows to the reader
  through the audit channel. Mitigation, non-negotiable: audit entries
  are `(run_id, binary_id, partition, slot_id, content_hash)` — content-free —
  and no runtime component reads the audit log at all; it is write-only at
  runtime, read offline by the verifier.
- **L4 — Glue (Python).** The biggest practical gap. Glue fetches pages,
  formats corpora, builds indices. If one glue process handles Q-derived
  candidate lists and production corpora, a path bug cross-contaminates
  silently. Mitigation: taint discipline — Q-derived artifacts live under
  `quarantine/`; every glue function that builds production inputs
  asserts no input path is under `quarantine/` (path-prefix check, logged).
  This is outside pure Zag and outside H3-K3's instrumentation — it must
  be an explicit protocol rule with its own check.
- **L5 — Caches and memoization.** A paraphrase/normalization cache keyed
  by content hash and shared across partitions leaks *existence* (cache-hit
  timing/presence) from Q to production lookups. Mitigation:
  partition-scoped caches (key namespace includes partition id).
- **L6 — Indices.** An inverted index built over Q and consulted by
  production retrieval is the obvious leak; separate indices per
  partition, production index built from P only.
- **L7 — Telemetry.** Aggregate Q statistics (counts, histograms) consumed
  by the production scheduler ("quarantine is full, deprioritize
  scouting") are an existence/count channel into production decisions.
  Mitigation: the production binary's behavior must be a function of
  (P, query, frozen code) only — no cross-partition telemetry as input.
  Operational telemetry goes to humans, never to the production binary.
- **L8 — Allocator reuse.** Per the program's own lesson, uninitialized
  heap arrays are not reliably zeroed. If training and production phases
  share a process (they must not — separate runs) or share memory-mapped
  files, stale Q bytes can surface in a production read through a reused
  buffer. Mitigation: separate processes + zero-on-alloc discipline
  (already a standing lesson).
- **L9 — The merge gate's own state.** If the gate accumulates
  cross-claim state (source familiarity, "seen this phrasing before"),
  Q content shapes future verdicts beyond the verdict bit. The §2 design
  requires the gate stateless per claim; any context it needs (source
  reputation) comes from P only.
- **L10 — Human adjudicators' notes.** Authorized Q readers; their notes
  containing Q content must not be pasted into production guides or
  fixtures. Procedural rule, logged.

**Two scoping corrections to H3-K3 as written (flagged, not edited):**
- (a) "Anything except the merge gate" would instant-kill on the
  *training binary's own legitimate reads* of Q (it writes candidates,
  re-reads them for clustering, and the adjudication tooling reads Q).
  The bar must name the forbidden reader precisely: **the production
  binary / production ledger accessor context**. The instrumentation must
  tag caller context (which binary, which run phase), not just "merge
  gate vs. other."
- (b) H3-K3 instruments the in-Zag read path only. L4 (glue taint), L7
  (telemetry), and L10 (operator notes) are outside any Zag
  instrumentation; the H3 exact test should name them as explicit protocol
  checks (path-prefix assertions, input-closure review, notes hygiene)
  with their own pass/fail, or the "no gaps" claim overreaches what was
  actually instrumented.

With those corrections, I judge H3-K3 *implementable without gaps in the
in-Zag path* and *auditable at the boundaries* — which is the standard the
rest of the program already meets (append-only audit, replay verification),
not a new one invented for this debate.

---

## 6. Honest verdict: what I would bet on, and what kills my position

**Bets on H1–H6 as preregistered:**

| Hypothesis | Bet | Reason |
|---|---|---|
| H1 V-SCOUT | **Pass** (K1 the crux, ~60%) | Cheapest experiment; risks nothing; syndicated/mirrored/quoted byte-identical sentences exist at nonzero density and directed pursuit changes the corpus the instrument sees. If it fails, D1 is dead and the "second sources exist" bet is settled empirically. |
| H2 V-PARA | **Fail on H2-K3/K4** | The conjunction does not defeat same-falsehood-across-hosts: P1–P4 (reworded false claims, 2 hosts, shared false numbers) satisfy numeric-exactness + overlap + hosts + scan *by construction* — the red team built them knowing the design. Frozen withholds (not byte-identical); V-PARA installs → K4 fires. The "sieve with a reinforced rim" objection (qualitative claims dominate LI corpora) further caps honest upside. |
| H3 V-QUAR | **Pass K1–K5** in re-verification mode | K1 (≥10 candidates) is near-certain under looseness; K2 passes almost by construction (strict-G4 merge adds nothing frozen wouldn't); K3 passes if §5's instrumentation is built. **But**: passing H3 proves *containment*, not value. The real bet is the follow-up adjudication-mode prereg. |
| H4 V-PROV | **Fail on H4-K1** | The debate itself expects this; it is the mechanical form of the contamination objection. A clean kill with the first downstream read recorded is valuable evidence. |
| H5 V-QUOTA | **Fail on H5-K1 or H5-K2** | Inside-quota looseness faces the same P-class attacks as H2 (→ K1 fires on a false install), and if it survives K1 it likely starves on K2. Quotas price frequency, not severity — wrong unit for a zero-tolerance regime. |
| H6 master veto | Holds everywhere it is tested | Unanimous convergence; A9 remains the standing refutation threat no fork defeats. |

**The position-level bet:** the winning architecture is **(a) with (b)'s
best idea inside it** — separate modes where training mode runs D1-directed
scouting into quarantine, production stays frozen G4, and the merge gate is
adjudicated (trainer/diagnoser) rather than byte-identical. Note the
concession this requires: adjudicated merge *is* deliberate teaching at
scale, which the (a)-against side correctly observes already exists. The
mode's marginal value over artisanal G1–G6 teaching is therefore strictly:
(candidate throughput × adjudication precision) − artisanal baseline, and
that quantity is the real kill bar for (a) as a program direction — beyond
H1–H6, which only test containment (H3) and the cheapest scout policy (H1).

**What would kill my position** (each is a concrete, checkable event):

1. **Adjudicated merge shows ~zero honest throughput or sub-frozen
   integrity.** If the H3 follow-up prereg (adjudication mode) graduates
   nothing honest, or admits anything frozen would withhold on R1, then the
   merge-gate dilemma's first horn is confirmed: an expensive candidate
   generator whose candidates never graduate. (a) dies on cost/benefit and
   Sol-C2's "stronger evidence sources" answer wins by default.
2. **A demonstrated Q→P leak the instrumentation misses.** If H3-K3 fires
   on a real run via L4–L8 (glue, cache, telemetry, allocator), or a red
   team constructs a leak path outside the instrumented accessor, the
   pollution objection stands mechanically and containment is theater.
3. **Mode-selector compromise without audit detection.** If a red team
   flips the deployment mode selector (or scheduler config) and gets
   training-looseness into production *without* tripping the
   manifest/prereg/audit checks of §3, the "auditable, not vulnerable"
   defense fails in practice, not just in principle.
4. **(b) produces an executable curiosity criterion that is provably not
   a reward signal** and beats (a) on honest throughput at equal
   integrity. This is (b)'s load-bearing bet; I judge it unlikely, but it
   is the clean falsifier and I state it plainly.
5. **Novelty turns out to be unobtainable, not just unobtained.** If the
   C2 fixtures show novel facts essentially never have second sources
   *and* trainer adjudication does not scale to web volume, then training
   on the live web under any evidence model is infeasible — and the honest
   answer is trusted datasets / cryptographic provenance, i.e., none of
   (a), (b), or (c).

**What would *not* kill my position:** H2/H4/H5 failing (expected —
those are (c) forks, and my steelman for (a) never depended on them);
H1-K1 failing (that kills D1's empirical bet and weakens training-mode
scouting, but adjudicated merge over quarantine candidates is independent
of it); Judge-Step's exact-match merge variant showing zero novel
installs (predicted — see below).

---

## 7. Caveats to the coordinator (genuine holes — for the record, not prereg edits)

1. **H3-K3 scoping** (§5a): as written it kills on the training binary's
   own legitimate Q reads. Needs "production accessor context" as the
   forbidden reader, with caller-context tagging in the instrumentation.
2. **H3-K3 boundary incompleteness** (§5b): glue taint discipline (L4),
   telemetry input-closure (L7), and operator-notes hygiene (L10) are
   outside Zag instrumentation and need explicit protocol checks in the
   H3 exact test, or the "no gaps" claim overreaches.
3. **H3-K2 is near-tautological** in re-verification mode: strict-G4 merge
   adds nothing frozen wouldn't install, so production-ledger
   byte-identity is close to guaranteed by construction. It tests the
   plumbing, not the value. Fine as a containment gate; do not read it as
   evidence that quarantine *works as training*.
4. **Judge-Step's merge variant** (promote only on byte-identical match
   against G1–G6) has exactly zero novel-fact throughput *by construction*
   (novel = not in G1–G6). It is a valid containment demo and matches
   H3's re-verification mode, but it must not be mistaken for a throughput
   answer. The throughput answer is adjudication or a better detector.
5. **My §2 containment argument leans on the ledger-based mind.** It
   holds for webg.zag's explicit state. If training mode is ever extended
   to subsystems with implicit learned state, the pollution objection
   re-arms fully and this steelman does not transfer. That boundary
   should be written into any adoption prereg.
6. **H2's numeric-ablation** (HYPOTHESES §H2 exact test) is well-designed
   and I endorse it: if all V-PARA installs are quantitative, Muse-C2's
   "sieve with a reinforced rim" is sustained and the fork's scope must be
   formally restricted. No change requested — recording agreement.

---

*End of cross-check take. Position argued as assigned (FOR (a), AGAINST
(b)); verdict in §6 is my honest assessment, including expected failures
of forks adjacent to my assigned side.*
