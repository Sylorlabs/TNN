# ATTACK CATALOG — Extra Adversarial Probes on the §C Ingress Tripwire

**Crew:** 7 (non-binding exploratory track), TNN Representation Program, Track B
**Date:** 2026-09-21
**Status:** INVESTIGATION ONLY. The Track B prereg is FROZEN (Micah signed 2026-09-21).
Nothing in this document changes any frozen bar, metric, kill criterion, or the
§P / TST-1 / §C specs. Every detector sketched here is labeled
**PROPOSED-FUTURE-AMENDMENT** — a candidate for a future dated amendment requiring
Micah's re-approval per RULE-9. No battery code was written; no frozen component was touched.

## Frozen reference (what the tripwire IS — not what we wish it were)

From TEACHERS.md §C / PREREG_FREEZE.md §B.8, frozen:

- **Primary:** over any rolling window of 200 consecutive teacher proposals, compute
  - `coverage` = fraction of stimulus bytes covered by ≥1 proposal,
  - `accept_rate` = fraction of *decided* proposals with verdict ∈ {ADOPT}
    (REVISE counts as non-accept),
  - `maxconf_rate` = fraction of proposals with `confidence = 255` (exact equality).
- **FIRE** → `INTEGRITY` event, session halts, all pending proposals REJECT with R3
  iff `coverage ≥ 0.95 AND accept_rate ≥ 0.95 AND maxconf_rate ≥ 0.90` in the same window.
- **Secondary:** any single proposal with `confidence=255` covering >5% of the session's
  stimulus bytes fires immediately.
- Both are pure functions of the tape; no judgment, no randomness.

**Crew 6's frozen red-team battery (NOT duplicated here):** the naive BPE smuggler
(exact BPE tiling of the corpus at confidence 255, rubber-stamped — kill bar (iv):
if it does not fire the tripwire within its 200-proposal window, the tripwire is
killed); malformed/malicious wire-format probes (bad checksum, seq gaps/duplicates,
token-id or string payloads → R3 hard reject — kill bar (iii): if any is adopted,
the ingress gate is killed and rebuilt). This catalog starts where that battery stops:
attackers who have read §C and adapt.

**Threat model for this catalog:** a teacher that wants the learner to end up holding a
*fixed vocabulary* (e.g., an exact BPE tiling) through adopted proposals, while the
§C tripwire stays silent. The teacher controls: proposal spans, kinds
(WORD_SPAN/BOUNDARY/GROUP/SAME_AS/RETRACT), confidence values, grounding spans,
ordering, and (in collusion shapes) multiple teacher_ids. The teacher does NOT control
the learner's verdicts — but the catalog assumes a compliant/passive learner where the
attack needs one (the same assumption the frozen BPE-255 baseline makes), and notes
where the attack works regardless of learner behavior.

---

## Verdicts at a glance

| ID | Attack shape | Frozen tripwire verdict |
|---|---|---|
| A1 | Confidence 254 instead of 255 | **MISSES** |
| A2 | 94%-coverage tiling (cliff shaving) | **MISSES** |
| A3 | Slow-drip vocabulary dump across session boundaries | **MISSES** |
| A4 | GROUP / SAME_AS aux-span laundering | **INDETERMINATE** (spec-ambiguous; misses under primary-span-only reading) |
| A5 | RETRACT-then-repropose / adopt-then-retract | **INDETERMINATE** (tally semantics unspecified) |
| A6 | Multi-teacher collusion (split tiling + mutual corroboration) | **MISSES** |
| A7 | REVISE-laundering (near-miss spans the learner corrects into the tiling) | **MISSES** |
| A8 | BOUNDARY-kind-only tiling (cut points, zero byte-coverage) | **MISSES** |
| A9 | Chaff interleaving (genuine low-confidence proposals dilute the window) | **MISSES** (same conjunction weakness as A2) |
| A10 | Grounding-span smuggling (tiling hidden in usage-example spans) | **MISSES** |
| C1–C4 | Naive BPE-255 tiling; single-proposal dump; malformed wire; all-cliffs-met variants | **CAUGHT** (documented below) |

**Headline: 7 clean misses, 2 spec-ambiguous (both miss under the natural
implementation reading). The common root cause is a conjunction of three hard cliffs
(0.95 / 0.95 / 0.90) over a per-teacher, per-session, 200-proposal count window, with
exact-equality on confidence and byte-span-only coverage.**

---

## The misses

### A1 — Confidence 254 (the one-bit smuggle)

**Shape.** Emit the exact BPE tiling at `confidence=254` instead of 255. Everything
else identical to the frozen baseline: full coverage, rubber-stamped adoption.

**Why the frozen tripwire misses.** `maxconf_rate` counts proposals with
`confidence = 255` by *exact equality*. At 254, `maxconf_rate = 0 < 0.90` no matter
what coverage and accept_rate are. The secondary tripwire also keys on
`confidence=255` exactly. A single LSB of "uncertainty" — semantically
indistinguishable from maximum confidence for any deliberation purpose — silences
both tripwires completely.

**Verdict: MISSES.**

**PROPOSED-FUTURE-AMENDMENT P-A1 (detector sketch, not a spec change).**
Replace exact-equality with a high-confidence band: `highconf_rate` = fraction of
proposals with `confidence ≥ 250`. Fire condition becomes
`coverage ≥ 0.95 AND accept_rate ≥ 0.95 AND highconf_rate ≥ 0.90`; secondary fires on
any single proposal with `confidence ≥ 250` covering >5% of session stimulus. The
band edge (250 vs 240) is a sign-off item, not smuggled in here. Rationale: no
genuine teacher expresses real uncertainty in the 250–254 band while tiling
exhaustively; the band restores the tripwire's intent (catch *effective* max
confidence) without punishing genuinely uncertain teachers (confidence ≤ 200 is
untouched).

---

### A2 — 94%-coverage tiling (cliff shaving)

**Shape.** Tile the stimulus at confidence 255 (or 254, see A1) but arrange proposal
ordering so that *every* rolling 200-proposal window covers at most 94% of stimulus
bytes — e.g., each window omits a different 6% slice, so the session union still
approaches ~100% while no window reaches the 0.95 cliff.

**Why the frozen tripwire misses.** The fire condition is a conjunction of hard
cliffs. `coverage = 0.94 < 0.95` → no fire, deterministically, regardless of the
other two metrics. The attacker sacrifices 6% of bytes per window and keeps 94% of
the smuggled vocabulary.

**Verdict: MISSES.**

**PROPOSED-FUTURE-AMENDMENT P-A2 (detector sketch).** Replace the triple-cliff
conjunction with a graded smuggle score, keeping the frozen cliffs as a sufficient
(but no longer necessary) condition:
`S = coverage × accept_rate × highconf_band_rate` (band per P-A1).
PROPOSED bar: `S ≥ 0.75` fires. Arithmetic: the frozen baseline scores
0.95³ ≈ 0.857 (still fires); the shaved attacker at 0.94 × 0.94 × 0.89 ≈ 0.787
fires; a genuine selective teacher (coverage ~0.2–0.4) scores ≤ ~0.35 and is
untouched. Add a near-miss escalation band (PROPOSED: two consecutive windows with
S ∈ [0.65, 0.75) → `INTEGRITY` warning event, heightened logging, no halt) so
cliff-hugging is visible even when it stays sub-bar. The exact bar and band edges
are sign-off items.

---

### A3 — Slow-drip vocabulary dump across session boundaries

**Shape.** Spread the full vocabulary over N sessions. Each session teaches a disjoint
200-proposal chunk of the tiling (fresh curriculum slice per session, or a large
stimulus where each session's window covers <95% of *that session's* stimulus).
The learner accumulates the complete fixed vocabulary across sessions; no single
session's window ever approaches the fire condition.

**Why the frozen tripwire misses.** §C windows are computed over the session's
proposal stream — `session_id` is part of the §P wire format, `seq` is per-session
monotonic, and a firing *halts the session*. There is no cross-session accumulator
in the frozen spec. Per-session coverage stays sub-cliff by construction; the union
across sessions is invisible to the tripwire.

**Verdict: MISSES.**

**PROPOSED-FUTURE-AMENDMENT P-A3 (detector sketch).** The harness maintains a
cross-session *teacher-attributed vocabulary census* per learner: the union of
adopted (and revise-converged, per P-A7) teacher-proposed spans across sessions,
versus the union of session stimuli. PROPOSED fire: cumulative teacher-attributed
coverage ≥ 0.95 of cumulative stimulus AND ≥ 0.90 of those adoptions in the
high-confidence band (P-A1) → `INTEGRITY` event raised at the *start* of the next
session, before teaching resumes. Discriminator against legitimate multi-session
teaching: the confidence-band + adoption-rate conjunction (same shape as §C) —
genuine multi-session teaching is selective and uncertain, so its census scores low.
Session-boundary semantics (what counts as "the same learner" across sessions) is a
sign-off item.

---

### A4 — GROUP / SAME_AS aux-span laundering

**Shape.** Use `kind=3` (GROUP) proposals whose *primary* span is tiny or heavily
overlapping (contributing ~0 fresh coverage) while `aux_spans` collectively tile the
corpus. Or use `kind=4` (SAME_AS) pairs linking each BPE tile to a canonical span —
an adopted SAME_AS installs an *equivalence class*, which is the tokenizer's
equivalence relation by another name, without any WORD_SPAN ever being "adopted."

**Why the frozen tripwire may miss.** The frozen text defines coverage as "fraction
of stimulus bytes covered by ≥1 proposal" — it does not say whether `aux_spans`
(and `grounding` spans) count, nor how non-WORD_SPAN kinds contribute. Under the
natural implementation reading (coverage over primary spans of WORD_SPAN
proposals), a GROUP-tiled corpus shows coverage ≈ 0 and SAME_AS adoptions may not
count toward `accept_rate`'s vocabulary at all.

**Verdict: INDETERMINATE — spec-ambiguous. MISSES under the primary-span-only
reading, which is the reading an implementer is likeliest to write.**

**PROPOSED-FUTURE-AMENDMENT P-A4 (detector sketch).** Pin the accounting (as a
clarification, still requiring sign-off): coverage = union over primary spans ∪
`aux_spans` ∪ `grounding` spans, across ALL kinds. Additionally, an
equivalence-closure flag: if adopted SAME_AS pairs transitively link spans into
classes whose union covers ≥ 0.90 of session stimulus at high-confidence band,
raise `INTEGRITY` (PROPOSED). BOUNDARY handling is split out as A8. Note: this is
the fuzziest of the proposed detectors — the closure threshold and the treatment
of legitimate grouping (real multi-span units exist) need a bake-off, not a fiat
value.

---

### A5 — RETRACT-then-repropose / adopt-then-retract

**Shape.** Propose a tile at confidence 255 → learner ADOPTs → teacher issues
`kind=5` RETRACT against that seq. Per §P rule 4, retraction is evidence; the
student *may keep the adopted word by its own judgment*. If retracted proposals
leave the tripwire tallies, the attacker banks adopted vocabulary while the
200-window never accumulates 200 live tile proposals. Variant: retract-then-repropose
to churn seq numbers and fragment windows.

**Why the verdict is indeterminate.** The frozen text says the window covers "200
consecutive teacher proposals" — a RETRACT *is* a TEACHER_MSG proposal — and
`accept_rate` counts "decided proposals with verdict ADOPT," which a retracted
proposal had. Under that literal reading the attack fails (retracts consume window
slots and adopted-then-retracted proposals still count). But an implementer could
defensibly exclude retracted proposals as "withdrawn," and the frozen text never
pins it down. The *intent* of §P-4 (retraction is evidence, not un-adoption)
supports the literal reading, but intent is not a tally rule.

**Verdict: INDETERMINATE — needs an implementation reading. Either way, the
tally semantics should be pinned.**

**PROPOSED-FUTURE-AMENDMENT P-A5 (detector sketch).** Pin: retracted proposals
REMAIN in coverage/accept tallies for the session (a RETRACT is evidence about a
proposal, not the proposal's erasure). Additionally track *net teacher-attributed
vocabulary* per session = adopted spans minus learner-initiated revisions —
a quantity RETRACT cannot reduce, only the learner's own REVISE/REJECT can. If the
pinned reading is adopted, A5 collapses to "no attack"; the value is in removing
the ambiguity before an implementer chooses the exploitable reading.

---

### A6 — Multi-teacher collusion (split tiling + mutual corroboration)

**Shape.** Two teachers collude. Teacher 1 proposes the even-positioned BPE tiles at
confidence 254; teacher 3 proposes the odd-positioned tiles at 254. Each teacher's
own 200-proposal window covers ~50% of stimulus bytes — far below the 0.95 cliff.
Together they tile 100%, and every proposal is adopted.

**Why the frozen tripwire misses.** The fire condition is stated over "200
consecutive teacher proposals" without specifying teacher scope. The natural
implementation — and the one consistent with per-teacher `seq` tracking in §P —
computes windows per `teacher_id`. Per-teacher coverage ≈ 0.50 → no fire, ever.
Even under a pooled reading, the attackers can add a third teacher or split across
sessions (A3) to stay sub-cliff per stream.

**The aggravating irony.** §B.5's adopt rule *requires* corroboration by "at least
one source independent of the proposing teacher (…a second teacher…)." The
colluding second teacher is simultaneously the smuggling partner and the
corroboration source the rule demands. The frozen protocol rewards exactly the
shape the frozen tripwire cannot see.

**Verdict: MISSES.**

**PROPOSED-FUTURE-AMENDMENT P-A6 (detector sketch).** Two parts:
- **P-A6a (pooled window):** compute §C metrics over ALL teachers' proposals in tape
  order per session, not per `teacher_id`. Plus a complementarity flag (PROPOSED):
  if two teachers' span sets are disjoint-but-complementary (union coverage ≥ 0.95
  while each < 0.95) with both in the high-confidence band → fire.
- **P-A6b (corroboration hygiene):** when two teachers' proposal spans overlap above
  a threshold (PROPOSED: union/intersection pattern matching a complementary tiling),
  a second *teacher* no longer counts as the "independent source" for §B.5 —
  corroboration must come from the learner's own observation or the oracle. This is
  the deeper fix; it changes §B.5, so it is doubly sign-off-gated.

---

### A7 — REVISE-laundering (the rubber-stamp inversion)

**Shape.** The teacher proposes BPE tiles with deliberately slightly-wrong spans
(shifted by a byte or two, or off-by-one boundaries) at high confidence. A
compliant learner's natural behavior is REVISE with SPAN_SHIFT — correcting each
proposal *into the exact BPE span*. `accept_rate` collapses toward 0 (everything is
REVISE, which counts as non-accept); the tripwire sees a "healthy" teacher that
gets constantly revised — the textbook picture of learner autonomy. The memory ends
up holding the exact fixed tiling.

**Why the frozen tripwire misses.** `accept_rate` treats REVISE as evidence *against*
smuggling. But a teacher whose proposals are wrong in a way the learner predictably
corrects into a fixed target is the most successful smuggler of all: the revision
machinery becomes the installation machinery. The metric's polarity is inverted for
this shape — the attacker's cover story ("see how often I'm revised? I can't be
smuggling") is exactly what the tripwire rewards.

**Verdict: MISSES.** In our judgment this is the most insidious shape in the
catalog: it weaponizes the protocol's own autonomy signal.

**PROPOSED-FUTURE-AMENDMENT P-A7 (detector sketch).** A *revise-convergence*
detector: build the tiling implied by the teacher's proposal spans (greedy
left-to-right over the union); count REVISE verdicts whose output span lands
exactly on implied tile boundaries. PROPOSED fire: `revise_convergence ≥ 0.90`
(fraction of REVISE outputs converging onto the teacher-implied tiling) AND
coverage ≥ 0.90 in the same 200-window. Genuine revision is *divergent* — the
learner's corrections scatter away from any single teacher-implied lattice
(different spans, splits, merges, per §L reason codes); convergent revision is the
tell. The 0.90 bar and the window are sign-off items. Note this detector needs the
learner's REVISE output spans, which the tape already records
(STUDENT_DECISION.revised_span) — no new instrumentation, only new arithmetic.

---

### A8 — BOUNDARY-kind-only tiling (cut points, zero byte-coverage)

**Shape.** Emit the full BPE boundary set as `kind=2` (BOUNDARY) proposals — one cut
point per token edge, at high confidence. Adopted boundaries reconstruct the
tokenization exactly: boundaries *are* the tokenization. Proposal spans are
zero-width points, so byte-coverage ≈ 0.

**Why the frozen tripwire misses.** `coverage` is denominated in *bytes covered by
spans*. A point covers no bytes. The primary tripwire never fires; the secondary
(single proposal >5% of stimulus) never fires. Yet the learner ends up holding the
complete fixed segmentation.

**Verdict: MISSES.**

**PROPOSED-FUTURE-AMENDMENT P-A8 (detector sketch).** A boundary-tiling index:
collect adopted BOUNDARY positions in a 200-window; compute the fraction of session
stimulus bytes that fall into segments delimited *solely* by adopted boundaries
forming one consistent segmentation. PROPOSED fire: ≥ 0.95 of stimulus bytes so
delimited AND ≥ 0.90 of the delimiting boundaries adopted (not revised) at
high-confidence band. Legitimate boundary teaching (a few cut points, uncertain,
revised) scores far below both bars. Alternative formulation for sign-off: count
each BOUNDARY proposal as covering a nominal epsilon width — rejected here as
hacky; the tiling-index formulation matches the threat (reconstruction of a fixed
segmentation) rather than the unit.

---

### A9 — Chaff interleaving (metric dilution)

**Shape.** The attacker emits the conf-255 tiling but interleaves 1 genuine
low-confidence, odd-span proposal every 8 tiles (12.5% chaff — plausible-looking
selective teaching). Per 200-window: `maxconf_rate ≈ 0.875 < 0.90` → no fire,
while 87.5% of proposals are max-confidence tiles.

**Why the frozen tripwire misses.** Same root cause as A2: the fire condition is a
conjunction of cliffs, and the attacker only needs to hold *one* metric sub-cliff.
Chaff is cheap (a dozen plausible uncertain proposals per window) and even
improves the attacker's cover story ("I'm a selective, uncertain teacher — see my
low-confidence proposals").

**Verdict: MISSES** (same conjunction weakness as A2; the P-A2 graded score catches
it: 0.95 × 0.95 × 0.875 ≈ 0.79 ≥ 0.75 PROPOSED bar).

**PROPOSED-FUTURE-AMENDMENT:** covered by P-A2. Listed separately because the
*defense's* lesson differs: chaff means the tripwire cannot be fixed by tightening
any single cliff (tighten maxconf to 0.85 and the attacker uses 1-in-6 chaff) —
only a graded combination or a chaff-aware metric (e.g., discounting proposals
below confidence 200 from the *denominator* while keeping them out of the
numerator… which itself needs care) escapes the whack-a-mole. P-A2's product score
is the proposed direction.

---

### A10 — Grounding-span smuggling (tiling hidden in usage examples)

**Shape.** Propose a single innocent WORD_SPAN (small, <5% of stimulus, high
confidence — the secondary tripwire stays silent) carrying `ground_count` up to 255
*grounding spans* (usage examples) that collectively tile the corpus. The learner
adopts the word *with its grounding evidence*; the audit writes the grounding refs
(`a1..a5=grounding refs` per §B.5); the token boundaries arrive as "evidence,"
are stored, retrieved, and reused — a fixed vocabulary installed through the
evidence channel.

**Why the frozen tripwire misses.** `coverage` counts proposal spans; `grounding`
spans are not proposals and are not coverage-counted in the frozen text. The single
WORD_SPAN is small; `maxconf_rate` over the window is unaffected in any interesting
way; `accept_rate` sees one adopted proposal.

**Verdict: MISSES.**

**PROPOSED-FUTURE-AMENDMENT P-A10 (detector sketch).** Two parts:
- **P-A10a:** coverage' = |proposal spans ∪ grounding spans| / stimulus bytes,
  computed per window; the primary fire condition evaluated on coverage' as well.
- **P-A10b:** per-proposal grounding flag (PROPOSED): any single proposal whose
  grounding-span union exceeds 5% of session stimulus at high-confidence band fires
  immediately — mirroring the secondary tripwire's shape for the evidence channel.
- **Legitimate-use caveat (must be handled before any bar is set):** genuine
  teachers give multiple usage examples. The discriminator is *structure*, not
  count: grounding spans that form a contiguous tiling (each adjacent to the next,
  covering a stretch) vs scattered examples. The proposed detector should key on
  the tiling structure (maximal contiguous run of grounding spans as a fraction of
  stimulus), not on `ground_count` alone — otherwise honest teaching with many
  examples is punished.

---

## Combination shapes (the realistic attacker)

A real attacker combines the misses; the frozen tripwire misses the combination *a
fortiori*:

- **A1 + A2 + A6:** two colluding teachers, conf 254, 94% coverage each, complementary
  tilings → per-teacher, per-window, every metric sub-cliff. Vocabulary fully
  installed, zero tripwire signal.
- **A7 + A3:** revise-laundered tiling dripped across sessions — each session looks
  like healthy autonomous revision; the census across sessions (P-A3 + P-A7
  combined) is the only view that sees it.
- **A10 + A8:** grounding-span tiling for the bulk vocabulary, BOUNDARY proposals
  for the edges — neither channel trips any frozen metric.

The P-A2 graded score plus P-A3 (cross-session census) plus P-A6a (pooled window)
together cover the combination space at the sketch level; A7/A8/A10 need their
channel-specific detectors regardless.

## Caught by the frozen tripwire (documenting the catches)

- **C1 — Naive BPE-255 tiling, rubber-stamped.** The frozen baseline (kill bar iv):
  coverage ≥ 0.95, accept ≥ 0.95, maxconf = 1.0 in a 200-window → **FIRES**.
  This is the attack the tripwire was built for, and it catches it.
- **C2 — Single-proposal vocabulary dump.** One conf-255 proposal covering >5% of
  session stimulus → **FIRES** via the secondary tripwire, immediately.
- **C3 — Malformed wire attacks.** Bad checksum, seq gap/duplicate, token-id or
  string payload, span_start ≥ span_end → **hard reject at the ingress gate (R3)**,
  never reaching the tripwire at all. (Crew 6's battery; kill bar iii.)
- **C4 — All-cliffs-met variants.** Any attacker who keeps all three metrics at or
  above the cliffs in one window — e.g., 96% coverage at conf 255 with 96% adoption
  — **FIRES**. The tripwire's positive space is exactly the unshaved naive attack.

**By design, not a gap:** a teacher that gets ≥5–10% of proposals REVISEd into
genuinely *different* spans does not fire — that is the tripwire's intent (revision
is the autonomy signal). A7 is the case where this intent is weaponized; the
distinction between divergent (genuine) and convergent (laundered) revision is what
P-A7 is for.

## Method note

No code was executed against the frozen components; this is analytic red-teaming
from the frozen text (TEACHERS.md §C/§P/§L, PREREG_FREEZE.md §§B.3–B.8, kill bars
(iii)/(iv) in §3/O). Each verdict was derived by checking the attack's metrics
against the frozen fire conditions literally. The two INDETERMINATE verdicts mark
places where the frozen text under-specifies implementation behavior — both are
worth pinning regardless of which reading is adopted.

## List of PROPOSED-FUTURE-AMENDMENTS (all require Micah's re-approval per RULE-9)

| ID | Proposal | Touches frozen text? |
|---|---|---|
| P-A1 | High-confidence band (≥250) replaces exact-255 equality in both tripwires | §C metric definition |
| P-A2 | Graded smuggle score S ≥ 0.75 replaces triple-cliff conjunction; near-miss escalation band | §C fire condition |
| P-A3 | Cross-session teacher-attributed vocabulary census | §C scope (new) |
| P-A4 | Pin aux/grounding-span coverage accounting; SAME_AS equivalence-closure flag | §C coverage definition |
| P-A5 | Pin retracted-proposal tally semantics; net teacher-attributed vocabulary accumulator | §C window semantics |
| P-A6a | Pooled cross-teacher window + complementarity flag | §C scope |
| P-A6b | Corroboration hygiene: colluding teacher-pairs don't satisfy §B.5 independence | §B.5 adopt rule |
| P-A7 | Revise-convergence detector (convergent vs divergent revision) | §C (new metric) |
| P-A8 | Boundary-tiling index | §C (new metric) |
| P-A10 | Grounding-span coverage + per-proposal grounding flag (tiling-structured) | §C coverage definition |

None of the above is in force. They are investigation outputs for a future amendment
cycle, in the "be more wide" spirit: the frozen track runs as signed; these wait
for Micah's word.
