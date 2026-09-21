# ALPHABET M–R: Representation Arms — Identity, Judgment, Acquisition, Cut Signals

**Brainstorm Crew 3 deliverable. Date: 2026-09-20. Status: PROPOSED — Micah signs arms + bars before any build (prereg discipline).**

**Program question:** what is a unit of knowledge, if not an LLM token?

**Micah's thesis (restated):** LLM tokens are a fixed discretization built for matrix math. TNN's units must be COGNITIVE: chunking is an act TNN performs on the raw stream itself (no fixed tokenizer); vocabulary is taught/learned like a child learns words; a chunk is a byte span with a stable ID that memory points back to, retrieves, and reuses (caching territory).

## Design axes in this catalog

| Axis | Question | Arms here |
|------|----------|-----------|
| IDENTITY | What is the handle memory points to? | M (counter IDs), M2 (composition-committed IDs) |
| ANNOTATION | What else rides on the chunk besides bytes? | N (MA4 signed judgments at the unit level) |
| ACQUISITION | Which chunks become vocabulary? | O (taught — learner side), P (emergent via consolidation), Q (hybrid) |
| CUT SIGNAL | Where are the boundaries? | R (compression-driven MDL/DP), R2 (deliberation-verified cuts) |

**Terminology conformance:** this file uses the INDEX.md glossary pins exactly: *chunk* (stored realization of a unit), *unit* (the abstract atom — the question), *ID* (stable handle memory points to), *span* (bytes currently covered), *vocabulary* (reusable lexicon), *segmentation* (the act of dividing), *cut* (one boundary decision), *taught / emergent* (incl. the **disconnect test**: vocabulary that survives scaffold removal unchanged was learned; vocabulary that collapses was merely performed), *recall* (byte-exact bar), *revision*, *tombstone* (dead IDs never reused).

**Label-collision note (for the catalog-holder):** INDEX.md already assigns S (recall-driven), T (episode-aligned), U (recompute-on-demand), K (content-addressed), I (hierarchical). My two extra arms are therefore labeled **M2** and **R2** (sub-variants of M and R), not S/T/U. Near-neighbor map: M2 vs I (nesting is structure; M2 is identity-commits-to-composition) and vs Y3 (versioned identity); R2 vs Z1 (witness-bound) — merge proposed at ratification, R2's distinct claim being the compounding elimination curve.

**File-convention note:** my task assigned this crew arms M–R in `ALPHABET_M-R.md`. INDEX.md's placeholder table proposes crew 3 → `ALPHABET_I-N.md` and crew 4 → `ALPHABET_O-X.md`. I wrote where my task ordered; the catalog-holder must reconcile the crew/file split. Arm *letters* M–R match the INDEX.md one-line definitions throughout.

**Hard laws (all arms):** pure Zag; ZERO randomness in any AI decision path; byte-identical reruns from (input + full logged state) — M8's 5-run adversarial battery is the gate; append-only 16-word audit ledger (op, slot, rc, b1..b5, a1..a5, stage, d1, d2); deliberate memory ops only (add/kill/pin/promote/demote/strengthen/weaken); strength is judgment-set, never formulaic; force-pin is human/trainer-only, audited, visible. Metrics referenced are Crew 7's M1–M9 (METRICS.md).

---

## ARM M — Counter IDs: the nth chunk gets ID n

### 1. Mechanism sketch (TNN-native terms)

The simplest possible stable handle. **Home: organ 1 (deliberate memory substrate)** owns a `next_id: u64` in its logged state, because `add` is a memory op and ID issuance happens inside it. The `add` op assigns `id = next_id++` atomically with the audited write — the ID rides in the add entry's slot/b-fields, so ID issuance costs **zero marginal audit entries**. Reasoning control (inspect/propose/commit/refuse/rollback) oversees adds as usual; ID issuance is not a separate decision.

- **Revision:** a revision that changes bytes mints a NEW chunk with a NEW id, plus a supersedes-link to the old id (organ 5, native structural revision, writes the link as its own audited op). Byte-identical re-ingest does not mint — see the M-dedup rule below.
- **Deletion:** ids are NEVER reused. `kill` writes a tombstone entry retaining the id; the id→span row stays with a dead flag so old pointers resolve to "killed, see audit entry #k" instead of dangling. Gaps are permanent and expected — a dense id space is not a goal.
- **M-dedup sub-rule (required for M7):** before issuing a new id, the substrate does an exact byte-equality check (memcmp, deterministic scan order) against live chunks. Equal bytes → reuse the existing id and write a lightweight reuse entry. Without this, METRICS.md M7 scores dedup 0 ("silently issuing fresh unrelated IDs for identical content scores dedup 0"). The rule is frozen in prereg: equality is byte-exact, scan order is id-ascending, first match wins.
- **Where counters break down vs the alternatives.** vs **content addressing (arm K)**: counters need no hashing and are O(1), but two independently built stores cannot agree on ids — merging two counter-id stores requires a remap table and a pointer rewrite, while content ids agree with zero coordination. vs **position addressing (arm L)**: counters survive insertions elsewhere in the corpus (insert a chunk at offset 0; no existing id changes — position addressing invalidates every downstream id by construction), but counters are not self-locating: losing the id→span table is **total handle amnesia**, whereas content ids rebuild from bytes. The id→span table is therefore load-bearing logged state and must be checkpointed with the ledger. Counter ids also leak insertion history and give zero similarity signal: the same Shakespeare line chunked in two corpora gets two ids unless the M-dedup rule catches it.

### 2. Predicted strengths (falsifiable)

- **S1.** Allocation is O(1) with no per-chunk compute beyond increment + the M-dedup scan: chunking throughput will be ≥95% of raw scan speed on both corpora. (If the M-dedup scan dominates, the rule — not the arm — is revised.)
- **S2.** Id stability under remote edits: inserting 1,000 chunks at corpus offset 0 changes zero existing id→span rows. Verifiable by table hash before/after. Position addressing fails this by construction; this is the counter's structural advantage, stated as a check.
- **S3.** Byte-identical reruns (same input + same logged initial state) produce byte-identical id→span maps — verifiable by map hash across M8's 5 runs.

### 2b. Predicted weaknesses (falsifiable)

- **W1.** Cross-store merge: two TNNs (peer-teacher protocol, debate spectator references) cannot share counter ids without remapping. Prediction: remap-table size will be ≥90% of the smaller store's id count — i.e., remapping is nearly as big as the store.
- **W2.** Table-loss amnesia: with the id→span table deleted, zero handles are recoverable from chunk bytes alone (vs K, where all are). This is structural, tested by the table-deletion drill, not a performance claim.
- **W3.** The M-dedup scan is O(live chunks) per add in the worst case: at 10x scale it will dominate ingest time unless bounded (frozen bound, e.g., dedup-check only against chunks added in the last W episodes — disclosed approximation, prereg-frozen).

### 3. Falsification criterion

**KILL counter ids as the cross-store/global identity** if, in the two-TNN merge trial, remapping produces ≥1 dangling or misdirected pointer, OR remap compute exceeds 10% of total merge compute. (Scope note for the prereg: the arm survives unconditionally as the *store-local* handle — the kill is scoped to global identity.) **Separately, the M-dedup claim dies** (revert to pure nth-chunk issuance) if M7 dedup ratio on the repetition protocol is <0.4 with the rule active. M1's 64-remap swap probe must PASS — a side channel bypassing the id layer zeroes the arm regardless of recall scores.

### 4. Buildability note

- **Data structures:** one u64 in the substrate state struct; id→span table as parallel arrays `(offset: u64, len: u32, flags: u32)` indexed by id — integer indexing everywhere, no slice-`==` anywhere (which is exactly the point of the arm). Tombstone = flags bit.
- **Audit cost:** zero marginal entries for issuance (id rides in the add entry); one lightweight entry per M-dedup reuse; one tombstone entry per kill; one link entry per superseding revision.
- **Zag hazards:** none serious — u64 arithmetic is native. If the table exceeds 2^25 bytes (~2.8M rows at 12 bytes/row), segment it into ≤2^25-byte slices (standard build note per C5, equivalence by byte-identical rerun). The counter is logged state: it must be captured in checkpoints and replayed, or reruns diverge (M8 FAIL).

---

## ARM N — Judgment-annotated chunks: bytes + ID + signed judgment

### 1. Mechanism sketch (TNN-native terms)

A unit is not just bytes+ID but bytes+ID+**felt importance**: an i64 signed judgment in the MA4 style. **Who judges: organ 3 (deliberate consolidation/promotion)** — judging importance is its native function; the judgment that already drives promotion is simply also *stored on the chunk* and *used at recall*. **On what evidence** (all logged, all deterministic, cited by integer ids in the ledger entry): organ-2 verification outcomes (did recalling this chunk verify or kill a hypothesis?), probe recall success/failure, teacher confirmations/retractions (arm O feed), contradiction events (the chunk participated in a claim that was deliberately revised away).

- **Recall priority:** retrieval ranks by (judgment descending, chunk id ascending) — a total deterministic order. Chunks below a frozen judgment threshold are recalled only on explicit request or with a "suspect" marker. Negative judgment means *"I remember this and I judge it misleading"* — retention is separated from endorsement (the debate experiment's liar-TNN is the use case: keep its claims, judge them false). Negative is never silent deletion — that would be killing by another name and would trip the M3 freeze distinguisher.
- **Re-judgment (revision path):** organ 5 proposes a judgment change with cited evidence → reasoning control commits or refuses → ledger appends JUDGE_SET / JUDGE_REVISE entries (old value in d1, new value in d2, evidence refs in b-fields). History is append-only; judgments are never overwritten in place. A wrongly-judged chunk is re-judged the same way any memory is revised: deliberately, with evidence, on the record.
- **Anti-reward guardrail (the felt-intensity caution):** a judgment change with no cited evidence entry is malformed and refused at ingress. If "judgment" becomes a bare scalar that drifts up on recall success, it is reinforcement learning with a ledger — the ablation in §3 exists to detect exactly this.

### 2. Predicted strengths (falsifiable)

- **S1.** Directly generalizes the program's sharpest recent win: MA4's signed values repaired MA3's adversarial failure (18/18; 30 vs 9 on misleading-memory probes — MA3 lost *because it could not express negative judgments*). Prediction: judgment-annotated chunks beat judgment-free chunks by ≥5 points on the same adversarial misleading-memory bar.
- **S2.** The ablation (judgments recorded but ignored at recall) scores within noise of the control — i.e., the gain comes from *using* judgments at recall, proving they are load-bearing, not decorative. (This is a strength *claim about the test*: if the ablation wins, the arm is decoration — see §3.)
- **S3.** Every judgment change cites evidence in the ledger: the complete judgment history of any chunk is auditable to a third party from the ledger alone (white-box by construction, checkable in the red-team trial).

### 2b. Predicted weaknesses (falsifiable)

- **W1. Reward-by-another-name.** Prediction: if the evidence-citation requirement were lifted, judgments would correlate >0.9 with raw recall-success counts within 500 episodes — i.e., the channel *wants* to be RL and only the guardrail stops it. (Test by running the guardrail-lifted variant as calibration, never as headline.)
- **W2. Self-reinforcement loop.** High judgment → recalled more → more confirming evidence → higher judgment. Prediction: without a deliberate re-judgment review, ≥10% of chunks show monotone judgment increase over 500 episodes regardless of probe outcomes.
- **W3. Churn thrash.** Judgment updates can reorder recall deterministically-but-unstably: same queries, different rankings across nearby episodes. Prediction: measurable as rank-volatility on a fixed probe set; bound it in prereg or it becomes the kill in §3.
- **W4. Soft-freeze hazard.** Deeply negative judgments could suppress chunks so thoroughly they are never recalled — freezing by another name. The M3 freeze distinguisher (fresh-material accounting + audit-liveness) applies to the judgment layer: suppressed-but-live chunks must still appear in explicit-request recall and in audit activity.

### 3. Falsification criterion

**KILL** if on the adversarial curriculum's misleading-memory bar the judgment arm does not beat the judgment-free control by **≥5 percentage points**; **OR** if the ablation (judgments present but ignored at recall) scores within **2 points** of the full arm — then judgments are not load-bearing and the arm is decoration; **OR** if **>10% of chunks flip judgment sign more than twice in any 100-episode window** (churn — the signal is unstable, not knowledge). Any of the three kills the arm; the first two are about the claim, the third about the signal.

### 4. Buildability note

- **Data structures:** i64 per chunk (8 bytes; fixed-point scale frozen in prereg if fractional judgments are wanted — integers only, no floats anywhere near determinism). Judgment history lives in the ledger, not in a side table.
- **Audit cost:** one 16-word entry per judgment set/revise. Hot chunks with volatile judgments are ledger-expensive — this is real M5 cost and must be reported per-byte, not hand-waved. Cap: prereg may freeze a max judgments-per-chunk-per-W-episodes; exceeding it forces a deliberate review (judgment about judgments).
- **Zag hazards:** the recall comparator must be total and deterministic — (judgment desc, id asc), integer-only. Evidence refs in b-fields are integer ids (no slice comparisons). i64 arithmetic is native; saturation rules on overflow frozen in prereg (propose saturating, never wrapping).

---

## ARM O — Taught vocabulary: the LEARNER side

*(The four teacher protocols — peer TNN, Muse, symbolic hints, symbolic yes/no — are Crew 6's. Their deliverable, `TEACHERS.md` (TST-1), is delivered and specifies the teacher side completely. This arm is the learner-side machinery that accepts it.)*

### 1. Mechanism sketch (TNN-native terms)

**I accept Crew 6's TST-1 interface verbatim — zero deviations** (see §5). The learner-side machinery:

1. **Ingress gate.** Validates every proposal against §P exactly: magic `0x54505250`, version, per-teacher monotonic `seq` (gap/duplicate = protocol violation → session pauses, event logged), span bounds against the shared stimulus tape, checksum. **Spans only** — any proposal carrying a pre-assigned token id or decoded text is malformed → hard reject + log (R3). Malformed proposals never reach deliberation.
2. **Deliberation engine (organ 2 — eliminative hypothesis logic).** A taught word is the hypothesis *"this span is a reusable unit."* The student generates competing segmentations, tests them against evidence, and eliminates. **Adopt iff all three §L conditions hold:** (a) it survives eliminative testing — every competing segmentation the student generated is eliminated by evidence (teacher evidence counts, weighted by confidence — a weight, never a command); (b) it is corroborated by ≥1 source independent of the proposing teacher (its own observation of usage spans in the stimulus, a second teacher, or the oracle bit in arm (d)); (c) it does not conflict with a pinned memory.
3. **Corroboration sources (deterministic):** the student's own exact-scan of the teacher's grounding spans + independent occurrence search in the stimulus; second-teacher proposals (matched by normalized span overlap); oracle answers (arm (d) only). All logged as evidence refs.
4. **Revision executor (organ 5).** Teacher said X, student stores X′: narrower/broader span, split, merge with an existing unit, generalize. Logged as STUDENT_DECISION verdict=REVISE with reason codes SPAN_SHIFT / SPLIT / MERGE / GENERALIZE / NARROW + the student's evidence refs, audited as its own memory op. The teacher reads the decision log; teachers never read memory directly.
5. **Rejection executor.** Audited refusal with enumerated grounds R1 INSUFFICIENT_EVIDENCE, R2 CONFLICTS_PINNED, R3 PROTOCOL_VIOLATION, R4 INTEGRITY_GATE (reasoning control refused — cf. the RC1 precedent: the learner refuses self-changes that weaken integrity), R5 REDUNDANT, R6 APPEAL_EXHAUSTED. R3/R4 are session-final (no appeal).
6. **Appeal handler.** On R1/R2/R5 the teacher may re-propose with NEW evidence (new grounding spans or revised span), max 2 appeals per proposal seq per session; third appeal auto-refused (R6). Two consecutive session-final rejections of the same normalized span = the unit is dead for the session. **Termination is guaranteed by construction** — every proposal ends in ADOPT, REVISE, session-final REJECT, or RETRACT within a bounded number of turns; the bound is in the tape, auditable.
7. **Deferral scheduler.** Verdict=DEFER when the turn's deliberation budget is exhausted; max 3 turns, then forced decision — still the student's own judgment, on the record.
8. **Tripwire monitor (§C).** Computed from the tape alone, pure function, no judgment: over any rolling 200-proposal window, FIRE iff coverage ≥0.95 AND accept_rate ≥0.95 AND maxconf_rate ≥0.90 → INTEGRITY event, session halts, pending proposals rejected R3. Secondary: any single confidence-255 proposal covering >5% of session stimulus fires immediately. This is the tokenizer-smuggling defense: a teacher tiling the corpus at confidence 255 is a fixed tokenizer by another name.
9. **Provisional-strength adoption (§F — PROPOSED, Micah undecided).** Adopted words arrive **judgment-held at provisional strength**, never force-pinned; organ 3 promotes them later by deliberate judgment. Design assumption: §F's recommendation (judgment-held). If Micah signs force-pinned instead, the autonomy law ("teacher proposes, TNN disposes") is violated and this arm must be redesigned — flagged as a blocking dependency.
10. **Namespace policy.** ONE unified store; every entry carries provenance tags (teacher_id, session_id, seq, kind). Collision with a self-discovered/emergent chunk (span overlap >50% either way, or label collision on disjoint spans): organ-3 deliberation picks ONE survivor by the frozen evidence rubric; the loser is killed/demoted with a cross-reference ("contested by", "superseded by") — never silently dropped. No separate taught namespace (separate namespaces would let the teacher's words dodge the student's use-based management — the disconnect test would then be unpassable by construction).
11. **Disconnect-test harness (glossary pin).** After scaffold removal (teacher gone), the vocabulary must behave identically: M1 recall on taught words ≥99.5% and identical recall rankings. If it collapses, the words were *performed*, not learned — the arm's central claim dies (see §3).
12. **Cost accounting (§M).** Per decided word, from the tape: ledger_entries_per_word, teacher_msgs_per_word, student_deliberation_steps, appeals/deferrals per word. Reported alongside mastery so a cheap arm that teaches nothing cannot win.

### 2. Predicted strengths (falsifiable)

- **S1. The acceleration claim (the arm's reason to exist).** Taught vocabulary reaches the M2 episodes-to-criterion bar on T1 novel material in **≤½ the episodes** of the emergent-only arm (P). This is the head-to-head the no-free-lunch law demands.
- **S2. Names for unfindable joints.** Teachers name abstract/code-idiom units (e.g., `sqlite3_*` families) that compression (R) and co-recall (P) under-generate. Prediction: on code, taught words show higher per-word probe-recall rates than emergent words in the first W episodes.
- **S3. Accountability.** Every taught word names teacher_id + session + seq: a mistaken or malicious teacher is auditable from the ledger alone. Emergent accidents have no one to blame; taught errors do.
- **S4. The disconnect test is passable.** Prediction: post-scaffold, taught-word recall stays ≥99.5% — the words were learned, not performed.

### 2b. Predicted weaknesses (falsifiable)

- **W1. Teacher dependence.** The rejection machinery is the ONLY defense against a bad teacher, and it is untested until red-teamed. A teacher that is wrong-but-plausible (good grounding spans, wrong labels) is the hardest case — the rubric must catch it or the arm is a transcription service.
- **W2. Adopted-but-unused dead entries.** Prediction: without a use requirement, ≥20% of taught words will have zero self-initiated recalls after W episodes. (This is arm P's use-criterion as the cure — the Q-hybrid argument in miniature.)
- **W3. Ingress attack surface.** The parser faces hostile input by design (red team). It must be total: bounded parse, frozen length caps, no panics, deterministic reject codes. Any parser hang or nondeterministic reject is a law violation (M8), not a bug.
- **W4. §F unsigned.** If Micah signs force-pinned taught words, this entire design's autonomy premise collapses — flagged, not solved.

### 3. Falsification criterion

**KILL the acceleration claim** (and with it the arm's reason to exist as more than an override channel) if taught-only vocabulary does not reach M2 criterion in ≤½ the episodes of emergent-only (P) on T1 novel material. **KILL the "learned" claim** if the disconnect test fails: post-scaffold M1 recall on taught words <99.5% → the words were performed, not learned. **KILL the ingress gate** (rebuild + full re-trial, not a patch) if any red-team probe gets a malformed or malicious proposal adopted. **KILL the §C tripwire** (halt the taught track until fixed) if the smuggling red-team — a teacher emitting the exact BPE tiling of the corpus at confidence 255 — does not fire the tripwire within its 200-proposal window.

### 4. Buildability note

- **Data structures:** §P proposal parser (fixed-field struct + length-prefixed aux/grounding span lists, hard caps frozen in prereg); per-teacher seq trackers (u64 last-seen per teacher_id); deliberation state per open proposal (hypothesis id, competing segmentations, evidence refs, state digests for replay); appeal counters (≤2) and deferral counters (≤3) per proposal; rolling 200-window tripwire accumulators (integer counts only); teacher reliability ledger (adopted/rejected counts per teacher_id — deterministic integers, feeds the rubric).
- **Audit cost:** one STUDENT_DECISION-anchored ledger entry per proposal outcome (ADOPT/REVISE/REJECT/DEFER) + deliberation checkpoints. This is the audit-heaviest learner arm by design — §M cost accounting keeps it honest; M5's per-KB audit bar applies.
- **Zag hazards:** bounds-check every length prefix BEFORE reading (total parser, no panics on hostile input); all parse buffers ≤2^25; evidence refs are integer ids; state digests use the native sha256 (R33_NATIVE_SHA256_V2.zag); seq tracking must survive replay (part of logged state — M8's replay rule requires the student's deliberation to reproduce STUDENT_DELIB/DECISION records bit-for-bit, so every deliberation input must be logged state or tape bytes, nothing else).

### 5. Interface boundary with the teacher-protocol crew (Crew 6, TEACHERS.md)

**THEY SUPPLY (already specified — I accept verbatim, zero deviations):**
1. **Proposal wire format (TST-1 §P):** `magic u32 = 0x54505250`, `version u16 = 1`, `teacher_id u32` (1=peer-proxy, 2=peer-full, 3=muse, 4=sym-hints, 5=sym-yesno; 0 reserved), `session_id u64`, `seq u64` (monotonic per session; gaps/duplicates = malformed), `kind u8` (1=WORD_SPAN, 2=BOUNDARY, 3=GROUP, 4=SAME_AS, 5=RETRACT), `span_start/span_end u64` (byte offsets into the shared stimulus tape), `aux_count u8` + aux spans, `ground_count u8` + grounding spans (the teacher's evidence), `confidence u8` (0–255, a weight — never a command; there is no ADOPT kind), `checksum u64`. Iron rules: spans only (no token ids, no decoded text), no commands, monotonic seq, RETRACT withdraws by seq.
2. **Session tape (TST-1 §T):** append-only, harness-owned, living outside student memory: TAPE_HEADER, STIMULUS_REF, TEACHER_MSG (§P bytes verbatim), STUDENT_DELIB (GENERATE/TEST/ELIMINATE/WEIGH + evidence refs + pre-step state digest), STUDENT_DECISION (ADOPT/REVISE/REJECT/DEFER + reason code + revised span + ledger entry index + post-step state digest), ORACLE_ANSWER (arm (d) only), HINT, APPEAL, INTEGRITY (tripwire firings), TURN_BOUNDARY, TAPE_FOOTER (final memory hash + ledger head). **Replay rule:** re-running a tape on a fresh student must yield byte-identical memory state; deliberation must reproduce the logged STUDENT_DELIB/DECISION records bit-for-bit or the implementation is non-deterministic (a law violation).
3. **Learner's rights (§L):** the adopt/revise/reject/appeal/defer paths exactly as I implement above — adopt's three conditions, REVISE reason codes, R1–R6, ≤2 appeals, ≤3-turn deferral, guaranteed termination.
4. **Anti-corruption tripwire (§C):** the exact fire conditions I monitor.
5. **Cost model (§M):** the per-word accounting I report.

**I SUPPLY (learner side):** the twelve machinery components in §1 above — ingress gate, deliberation engine, corroboration, revision executor, rejection executor, appeal handler, deferral scheduler, tripwire monitor, provisional-strength adoption, namespace/collision policy, disconnect-test harness, cost accounting.

**ADAPTATION RULE:** my parser accepts TST-1 §P verbatim. If Crew 6 revises §P, my parser is the adaptation layer — but any wire-format change after prereg freeze needs Micah's re-approval (prereg discipline cuts both ways).

**What I explicitly do NOT assume:** teacher honesty (red-teamed); any semantic ordering beyond seq monotonicity; label uniqueness; rationale truth (a teacher's rationale is evidence to check, never a verdict); §F's outcome (blocking dependency, flagged).

---

## ARM P — Emergent vocabulary via the consolidation organ: words crystallize from use

### 1. Mechanism sketch (TNN-native terms)

Bottom-up: frequently co-recalled chunks get promoted to vocabulary status — words crystallize from use, no teacher. **Deterministic counting only** (no stochastic counting, no sampling, no decay formulas — strength is judgment-set, never formulaic): over a fixed window of W episodes (frozen in prereg, e.g., 200), organ 3 maintains exact integer co-recall counts. Pair (A,B) recalled in the same retrieval episode increments **once per episode** (one vote per episode, not per recall — this bounds runaway counting from a single chatty episode). **Promotion criterion** (frozen, e.g., count ≥ K=7 within W): the pair becomes a promotion candidate. **Promotion ceremony:** organ 3 proposes via reasoning control — inspect the counts, propose the word, cite the episodes; commit writes PROMOTE entries referencing the constituent chunk ids and the episode refs; the new word gets a counter id (arm M) and provenance=emergent. **Demotion:** never formulaic decay — the law holds for words. A word falls out of use only by **deliberate kill**: zero co-recalls in the last W episodes AND a deliberate judgment (organ-3 review, or TNN's own deliberation) that the word is dead → kill with tombstone + audit, like any memory kill. A word nobody uses but nobody has judged dead stays — deliberate management, not garbage collection.

### 2. Predicted strengths (falsifiable)

- **S1. Use-grounded by construction.** No teacher bias, no adopted-but-unused dead entries (arm O's predicted W2 failure mode cannot occur here — a word exists *because* it was used). Prediction: 0% of emergent words have zero self-initiated recalls in the W episodes after promotion, vs O's predicted ≥20%.
- **S2. Corpus-native idioms.** Finds units no teacher would name: sqlite3.c call patterns, Shakespearean collocations. Prediction: on code, emergent words show higher per-word probe-recall rates than taught words after the crystallization lag.
- **S3. Autonomous, zero teacher cost.** The "TNN does all" default. M9 predicts the "gradual" curve shape (steepness <40) — the shape is part of the arm's signature; if emergent arms show "fast-then-flat", something is wrong with the mechanism story.

### 2b. Predicted weaknesses (falsifiable)

- **W1. Slow.** Needs K co-recalls before a word exists. Prediction: emergent vocabulary reaches the M2 criterion in **≥3× the episodes** of the taught arm — the mirror image of O's acceleration claim; the O-vs-P head-to-head tests both simultaneously.
- **W2. Corpus accidents crystallize.** Two chunks co-occurring for accidental reasons (a repeated license header, boilerplate) get promoted as a "word". Prediction: ≥15% of first-generation emergent words are boilerplate by human audit of a fixed sample — measurable, and the reason the deliberate-kill review exists.
- **W3. K and W are frozen judgments that shape everything.** Too high → nothing promotes (empty vocabulary — the arm fails silently); too low → junk promotes (churn — the arm fails loudly). The prereg must freeze K/W AND name the sensitivity calibration (rerun at K/2 and 2K as calibration, never headline).

### 3. Falsification criterion

**KILL** if, after the preregistered episode budget, emergent vocabulary does not beat the fixed-64-byte-chunk baseline on held-out recall probes (M1) by **≥3 points**; **OR** if **>50% of promoted words are deliberately killed within the next W episodes** (churn — the criterion promotes noise, not words). Either failure kills the "crystallize from use" claim; the counting machinery may survive as instrumentation for Q.

### 4. Buildability note

- **Data structures:** pair-count table — only pairs co-recalled in the same episode are ever inserted (small per episode); counts are exact integers; window eviction is a deterministic episode-indexed ring. Pair keys are integer pairs (never slice-`==`); iteration order frozen (slot order or sorted key order — pick one in prereg).
- **Audit cost:** one entry per promotion/demotion + the counts themselves are reproducible from the recall log (derived, not separately audited — same audit-economics principle as arm R). The deliberate-kill review is a normal audited judgment.
- **Zag hazards:** bound the pair table (per-episode insertion cap, frozen); segment past 2^25 as usual; the "one vote per episode" rule must be enforced by episode-index comparison, not by timestamps (no clock — M8's entropy/clock-starvation run would catch it).

---

## ARM Q — Hybrid taught + emergent: both paths feed one vocabulary

### 1. Mechanism sketch (TNN-native terms)

One store, two feeders, provenance on everything. Every vocabulary entry carries its origin: taught entries tag {teacher_id, session_id, seq, kind}; emergent entries tag {promoting episodes, co-recall counts}; entries later confirmed by the other path upgrade to **taught+confirmed** (both tags, no duplication). **Unification rule** (frozen in prereg): on collision — a taught word and an emergent word with spans overlapping >50% either way, or identical labels on disjoint spans — organ 3 deliberates with the frozen evidence rubric (recurrence counts, recall rates, teacher track record) and picks ONE survivor; the loser is killed or demoted with a cross-reference ("contested by", "superseded by"), never silently dropped. **Precedence / tie-break** (frozen default): **EMERGENT wins ties** — use beats authority. The opposite tie-break (taught wins) is a named parked sub-variant, not a second arm: no-free-lunch does not mean doubling every arm. **Anti-oscillation ("settled" rule, frozen):** a collision resolved the same way twice becomes sticky — the third proposal of the losing form is refused R5 (redundant) without full deliberation. Without this, the teacher re-proposes X, emergent re-promotes Y⊃X, deliberation kills one, forever.

### 2. Predicted strengths (falsifiable)

- **S1. Each parent covers the other's predicted failure.** O's dead taught entries get killed by P's use criterion (deliberate-kill review); P's slowness gets jump-started by O's proposals. Prediction: hybrid reaches M2 criterion faster than P alone AND has fewer dead entries than O alone — both gaps measurable.
- **S2. The collision record is evidence.** Win/loss per path (taught-words-surviving vs emergent-words-surviving collisions) is a measured outcome about which path names better joints — not an assumption. Prediction: on code, emergent wins ≥60% of collisions; on prose, taught wins ≥60% (teachers name abstract prose units better). If the split doesn't appear, the "different paths suit different domains" story dies.
- **S3. Containment.** The teacher attack surface (O's red team) is contained by the emergent path's independence: a malicious teacher cannot degrade the hybrid below the emergent-only floor — because the emergent entries don't depend on the teacher at all.

### 2b. Predicted weaknesses (falsifiable)

- **W1. Complexity.** Two acquisition paths + collision machinery + settled rule = more code, more audit entries, more frozen parameters (K, W, rubric weights, tie-break, settled threshold). M5 per-byte cost will be the highest of the three — the question is whether the recall gain buys it.
- **W2. Oscillation without the settled rule.** Prediction: in the settled-rule-ablated variant, ≥10% of entries oscillate (killed then re-added, or provenance-flipped) per W episodes. The ablation justifies the rule's existence.
- **W3. Union of attack surfaces.** Malicious teacher (O's red team) PLUS spurious crystallization (P's boilerplate) — the hybrid must red-team both simultaneously, and a failure in either feeder contaminates the shared store.

### 3. Falsification criterion — the no-free-lunch bar, explicit

Three arms head-to-head on both corpora, identical protocols: taught-only (O), emergent-only (P), hybrid (Q). **Primary bar:** M1 recall / M2 episodes-to-criterion. **Secondary bar (containment):** malicious-teacher probes must not push the hybrid's adversarial score below the emergent-only arm's. **KILL the hybrid** if it does not beat **max(taught, emergent) + 3 points** on the primary bar, **OR** if collision-resolution kills **>10% of entries per W episodes** (churn), **OR** if its adversarial score falls below emergent-only (containment failure — the teacher feeder is a liability, not an asset). **Pareto note (METRICS.md scenario-fit):** if the hybrid wins some scenario-fit dimensions (e.g., teacher-present) and loses others (e.g., autonomous), it survives as a dimension champion — KILL only on Pareto-domination (loses or ties everywhere). The bar is explicit; the verdict may still be "no overall winner."

### 4. Buildability note

- **Data structures:** union of O's and P's machinery + a span-overlap index for collision detection (interval index over chunk spans — integer arithmetic on (start, end), deterministic iteration sorted by span start then id). Provenance tags are fixed-width fields on the vocab entry.
- **Audit cost:** union of both parents' + one entry per collision resolution citing both contenders + settled-rule applications. Highest M5 in the family — budgeted openly.
- **Zag hazards:** the overlap index's iteration order frozen (sorted, never hash order); same slice discipline as P; the settled rule's "resolved twice" counter is logged state (replay-critical).

---

## ARM R — Compression-driven cuts: boundaries where the stream is most redundantly structured

### 1. Mechanism sketch (TNN-native terms)

Cut to maximize compressibility — MDL-flavored, fully deterministic, pure Zag. **Dictionary construction (deterministic):** build a suffix array over the corpus (prefix-doubling, O(n log n), pure integer arithmetic) + LCP array, and enumerate **maximal repeats** up to frozen maxlen L (e.g., 64): every substring occurring ≥2 times that cannot be extended. This is the dictionary — derived from the corpus, no teacher, no thresholds beyond L. **Segmentation (deterministic DP, O(n·L), bounded):** dynamic programming over positions minimizing total description length, where cost(chunk at i of length l) = `ref_cost` (frozen, e.g., 2 bytes) if the substring is a dictionary repeat, else `l` (literal cost). **Tie-break frozen** (propose: prefer the longer chunk, then the earlier cut — a total deterministic order). The DP is optimal *with respect to the stated code*; the code itself (L, ref_cost, maximal-repeat dictionary, tie-break) is the frozen design choice. **Why natural joints:** repeated idioms (`sqlite3_`, `if (`, Shakespearean phrases) earn ref_cost, so the DP cuts exactly at their edges — a cut *inside* `sqlite3_` would create two rare halves that both pay literal cost, which the DP rejects. Unique text stays in longer literal chunks. **Rejected alternative (documented):** naive O(n·L) substring counting in a hash table — up to ~600M substring occurrences on sqlite3.c; distinct entries realistically in the tens of millions; memory blowup quantified and rejected in favor of the SA/LCP construction.

### 2. Predicted strengths (falsifiable)

- **S1. Teacher-free and corpus-adaptive.** No teacher, no training, no thresholds beyond (L, ref_cost) — the cut signal comes from the corpus itself. Prediction: boundary F1 vs human-meaningful joints (whitespace/punctuation edges AND the taught spans from arm O, measured separately) beats the fixed-64-byte baseline by **≥10 points on BOTH corpora**, with *different* boundary distributions per corpus (code boundaries cluster at identifier/keyword edges; prose at word/phrase edges — the distributions themselves are reported).
- **S2. Deterministic and bounded.** Same corpus + same (L, ref_cost, tie-break) → byte-identical cut map, verifiable by cut-map hash across M8's 5 runs. O(n log n) time, O(n) memory — no search heuristics, no randomness anywhere.
- **S3. Domain-generality is testable.** (L, ref_cost) frozen on prose, applied to code (M6 transfer design): the transfer tax on boundary fidelity measures whether compression joints are domain-general or domain-fit.

### 2b. Predicted weaknesses (falsifiable)

- **W1. Compression-optimal ≠ cognitive-optimal.** Highly repetitive but meaningless spans (license headers, padding, boilerplate) win cuts they don't deserve. Prediction: ≥20% of the 100 most-cut boundary positions are boilerplate on both corpora (fixed-position audit).
- **W2. Sub-word cuts.** Strong sub-word repetition (`the` inside `other`, `ing` endings) pulls boundaries inside words. Prediction: ≥5% of cuts fall strictly inside whitespace-delimited words on Shakespeare.
- **W3. L and ref_cost are frozen judgments that shape every boundary.** Too small an L misses idioms; too large explodes the DP constant. Sensitivity calibration at L/2 and 2L is mandatory (calibration, never headline).
- **W4. The DP optimum is inscrutable.** "The DP said so" is deterministic but not *justified* per boundary — the white-box gap that arm R2 addresses.

### 3. Falsification criterion

**KILL the "natural joints" claim** if boundary F1 (vs whitespace/punctuation joints AND vs arm O's taught spans, separately) does not beat the fixed-64-byte baseline by ≥10 points **on both corpora**; **OR** if held-out recall (M1) with R-cuts does not beat the 64-byte baseline on the primary recall bar. Either failure kills the claim; the SA/LCP + DP machinery may survive as calibration instrumentation for R2.

### 4. Buildability note

- **Data structures:** suffix array (u32 per position — 9.5M × 4B = 38MB > 2^25, so segment into ≤2^25-byte slices, standard C5 build note); LCP array (same treatment); maximal-repeat list per position (capped lengths ≤ L); DP cost array (u32 — total description length for ≤9.5MB stays < 2^32; prove the bound in prereg or use u64 in ≤2^25 slices) + backpointer array (u8/u16 per position).
- **Audit cost — the important design point:** the chunk table is DERIVED and reproducible from (corpus sha256 + L + ref_cost + tie-break rule). Do NOT write per-chunk ledger entries (~1M chunks × 16 words would drown the ledger and trip the C4 ledger-capacity confounder). Audit the *policy* (parameters, corpus hash, chunk count, spot-check chunk hashes) — not the derivation. Derived indexes are not memory ops; the prereg must state this exemption explicitly, or the ledger becomes the experiment. M5's per-byte normalization is the comparison column that keeps this honest.
- **Zag hazards:** the 2^25 slice limit on SA/DP arrays (above); suffix-array construction must avoid slice-`==` (integer ranks only); DP backpointer walk is integer arithmetic; u32 cost saturation bound proven or u64 used; keep the scan allocation-free in the hot loop.

---

## ARM M2 — Composition-committed IDs (extra identity scheme)

### 1. Mechanism sketch

When organ 4 (symbolic recall and trace composition) composes chunks into a trace and the trace is promoted to a unit, the new unit's ID = **sha256 over the canonical child-ID sequence** — a Merkle-flavored handle. Canonical order frozen in prereg (propose: child ids sorted ascending — deterministic; the *sequence* order of composition is stored separately in the unit record, since sorting destroys it). The ID therefore **proves its parts**: revise a leaf chunk → the parent's ID changes → stale cached compositions are detectable by ID mismatch instead of silent corruption. Units can be born from composition, not just from cutting — the identity scheme follows the five-organ story to its conclusion. Near-neighbors (not duplicates): I (hierarchical nesting — structure, not identity), Y3 (versioned identity — lineage, not composition proof), K (content-addressed — proves bytes, not parts).

### 2. Predicted strengths / weaknesses (falsifiable)

- **S1.** Structural integrity: in the revision benchmark, stale-composition detection via ID mismatch catches **100% of leaf edits with zero false negatives** — vs arm M, where a leaf edit is invisible to the parent's handle (test both, report the gap).
- **S2.** Composed units are first-class vocabulary candidates for arm P: a frequently re-composed trace IS a co-recalled structure — M2 feeds P's promotion criterion naturally.
- **W1. Cascade invalidation is the price of the proof.** Every leaf revision re-ids every ancestor. Prediction: measured in the recall benchmark — if a single-byte leaf edit invalidates a large fraction of cached compositions, the integrity benefit may not pay for the churn (see §3 for the number).
- **W2.** Deep trees → recomputation cascades on every recall that re-verifies composition. Bounded by a frozen max composition depth (deeper compositions flatten or are refused deterministically — the refusal is audited).

### 3. Falsification criterion

**KILL** if a single-byte leaf edit invalidates **>25% of cached compositions** in the recall benchmark (cascade cost exceeds the integrity benefit at program scale), **OR** if ID recomputation exceeds **10% of recall latency** on the 10x horizon run.

### 4. Buildability note

- **Data structures:** composition records {parent_id (32B), child_ids[] sorted, sequence_order[] stored separately, depth u8}; sha256 over the canonical fixed-width integer encoding (no padding ambiguity — byte-exact canonicalization, frozen).
- **Audit cost:** composition is a memory op like any other: one add entry (provenance=composed, child ids cited across b/a-fields — 32-byte ids fit 4 per entry in b1..b4; longer child lists spill to linked entries, deterministic layout frozen).
- **Zag hazards:** canonical encoding must be byte-exact (fixed-width fields); recursion depth bounded (frozen max); sha256 via R33_NATIVE_SHA256_V2.zag; compare ids by memcmp/integer words, never slice-`==`.

---

## ARM R2 — Deliberation-verified cuts (extra cut signal)

### 1. Mechanism sketch

The most TNN-native cut signal in the catalog: **boundaries are hypotheses.** Organ 2 (eliminative hypothesis logic) proposes a cut at position i — *"a joint exists here"* — and the hypothesis is verified against checkable predictions or killed: the left span recurs elsewhere (exact count ≥2), the right span recurs elsewhere, and the pair (left,right) co-occurs adjacently in ≥K verified instances. Surviving cuts become chunks; killed hypotheses stay in the ledger **as eliminations** — the elimination record is itself knowledge (*don't re-propose here*), and it compounds: **proposals-per-accepted-cut must fall monotonically over the corpus** as the pruned regions accumulate. Candidate generation order frozen (left-to-right); verification reuses arm R's repeat-counting pass (build once, share — dependency noted). Near-neighbor: Z1 (witness-bound — "a cut must survive eliminative challenge"). **Propose merging R2 with Z1 at ratification**; R2's distinct, falsifiable claim is the compounding elimination curve, which Z1's one-line description does not make.

### 2. Predicted strengths / weaknesses (falsifiable)

- **S1.** Every boundary carries its evidence — the cut map is a white-box artifact, closing R's W4 (inscrutable optimum). A third party can audit *why* each cut exists from the ledger.
- **S2. The compounding curve.** Prediction: proposals-per-accepted-cut falls monotonically over the corpus (reported as the raw curve, no smoothing — M9's discipline). If the eliminations don't compound, the mechanism's core claim is dead (see §3).
- **W1. Slowest cut signal in the catalog.** A verification scan per candidate boundary: prediction **≥10× arm R's compute** on the same corpus (wall-clock reported informationally, never scored — M8).
- **W2.** K (adjacency co-occurrence threshold) is a frozen judgment with P's K-sensitivity problem; prereg freezes it + calibration.
- **W3. Cold start / honest reduction.** With no chunks yet, "the span recurs" needs the counting pass anyway — at which point R's DP is one step away. Honest note: R2 may reduce to "R plus receipts." The §3 bar decides whether the receipts are worth 10× compute.

### 3. Falsification criterion

**KILL** if verified-boundary recall on held-out probes (M1) does not beat arm R's compression cuts by **≥3 points** (if the receipts don't buy recall, 10× compute is unjustified); **OR** if proposals-per-accepted-cut does **not** fall over the corpus (the elimination records aren't compounding — the mechanism's core claim fails).

### 4. Buildability note

- **Data structures:** hypothesis records {position u64, left_span (offset,len), right_span (offset,len), status: open/verified/eliminated, evidence refs}; shares R's repeat table (dependency).
- **Audit cost:** audit-heavy by design — every proposal AND every elimination is a ledger entry (candidates ≈ n/avg_span; entries × 16 words). Budget it openly under M5; if the ledger cost exceeds the frozen per-KB bar, the arm fails M5 even if it passes M1 — that is the metric working as intended.
- **Zag hazards:** candidate order frozen left-to-right (replay-critical); verification predicates are integer counts + memcmp only; elimination records are tombstone-class (never reused, anchor lineage per the glossary pin).

---

## Cross-arm notes

**Shared baselines.** Every arm measures against the fixed-64-byte-chunk precedent (byte-exact recall, 100/100 at 1x, 61,440/61,440 at 10x) on both corpora. M8's determinism gate (5 runs + heap/ASLR/entropy/clock/allocation-order battery) applies to all eight arms — FAIL anywhere is disqualification, not underperformance.

**Prereg freeze list (the catalog proposes; Micah signs):** M: M-dedup scan bound. N: judgment scale (i64 fixed-point), recall threshold, evidence rubric, overflow saturation rule. O: TST-1 §P accepted verbatim (no freeze needed — Crew 6 specified it); freeze the rubric weights, teacher track-record bar, parse caps, and §F's outcome (blocking). P: K, W, sensitivity calibrations. Q: tie-break default (emergent), overlap %, settled-rule threshold. R: L, ref_cost, tie-break, SA/DP slice plan, audit-economics exemption. M2: canonical order, max composition depth. R2: K, candidate order, Z1-merge decision.

**Recommended build order (author's judgment):** M (handles — everything, including M1's swap probe, needs the ID layer) → R (cheapest cut signal; its repeat table unblocks R2 and informs P/O) → N (extends the proven MA4 win; plugs into §F) → P (autonomous vocabulary) → O (interface specified and delivered — NOT blocked; builds against TST-1 §P) → Q (needs O+P results) → M2/R2 (instrumentation; build when the base arms exist to measure against).

**Expected verdict shape (no-free-lunch honesty):** the likely outcome is Pareto + scenario-fit, not a single winner — M for store-local identity, R/R2 for cut signals, N for annotation, and O/P/Q splitting the scenario-fit map's teaching-availability dimension (taught owns teacher-present, emergent owns autonomous). An arm survives by owning a dimension, not by beating everyone everywhere.

## Parked sketches (considered, not full arms)

- **Position-anchored secondary index** (corpus_id, offset): cheapest possible handle, self-locating — parked as *primary* because any insertion invalidates all downstream ids; survives as a secondary index inside M's id→span table.
- **Frequency-ranked ids** (nth most common chunk gets the shortest id): variable-length handle compression — parked because rank instability under corpus growth breaks handle stability, which is the thing ids are for.
- **Teacher-cut boundaries** (BOUNDARY-kind proposals through the O intake): parked — it's arm O applied to boundaries instead of words; build only if O's intake exists and both R and R2 fail their bars.

---

*End of Brainstorm Crew 3 deliverable. 8 arms (M, N, O, P, Q, R, M2, R2). All proposed; nothing preregistered. Micah signs before build.*
