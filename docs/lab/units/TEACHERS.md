# TNN Representation Program — Teacher Protocols (Crew 6)

**Status:** PROPOSED — awaiting Micah's sign-off before any build (prereg discipline).
**Scope:** the teacher side + protocol + tape. The learner-machinery crew designs the student's
vocabulary-acquisition internals. The assumed interface boundary between us is defined in §P;
they must accept exactly the wire format specified there.

**Micah's thesis:** vocabulary is taught/learned like a child learns words — no fixed tokenizer,
no pre-baked vocabulary. A teacher proposes words/units; TNN (the learner) adopts, revises, or
rejects them. **TEACHER PROPOSES, TNN DISPOSES.** Learner autonomy is LAW: TNN controls 100% of
its reasoning machinery; the constitution/ledger/gates are the only things it does not control.

**Standing laws inherited:** pure Zag implementable; ZERO randomness in any AI decision path;
byte-identical reruns (same input + same complete logged internal state → byte-identical output) —
teaching sessions are replayable tapes; no-free-lunch (the four arms compete head-to-head on
identical curricula, scored by the same mastery/revisability/integrity/retention/cost weights).

**Five-organ context:** proposals land on (1) the deliberate memory substrate as candidate units;
(2) eliminative hypothesis logic is the gate — a proposed word survives only if competing
segmentations are eliminated; (3) deliberate consolidation/promotion moves adopted words up the
strength ladder by judgment, never by formula; (4) symbolic recall and trace composition make
the word usable in reasoning traces; (5) native structural revision is what makes REVISE and
REJECT real rather than ceremonial.

---

## 0. Shared infrastructure (all four arms)

### §P — Assumed interface boundary: the proposal wire format

The learner crew must accept proposals in exactly this format. It is the one thing a teacher
is allowed to hand the student.

```
PROPOSAL WIRE FORMAT (TST-1 §P):
  magic:      u32  = 0x54505250 ("TPRP")
  version:    u16  = 1
  teacher_id: u32  // 1=peer-proxy 2=peer-full 3=muse 4=sym-hints 5=sym-yesno (0 reserved)
  session_id: u64  // assigned by the harness at session start
  seq:        u64  // teacher's monotonic per-session counter; gaps/duplicates = malformed
  kind:       u8   // 1=WORD_SPAN 2=BOUNDARY 3=GROUP 4=SAME_AS 5=RETRACT
  span_start: u64  // byte offset into the shared stimulus tape
  span_end:   u64  // exclusive; must satisfy span_start < span_end
  aux_count:  u8   // 0 for WORD_SPAN/BOUNDARY/RETRACT; span pairs for GROUP/SAME_AS
  aux_spans:  aux_count × (u64 start, u64 end)
  ground_count: u8 // usage-example spans = the teacher's evidence, also byte spans
  grounding:  ground_count × (u64 start, u64 end)
  confidence: u8   // 0..255 — the teacher's judgment weight. Evidence, not a command.
  checksum:   u64  // over all preceding fields; mismatch = malformed
```

**Iron rules of §P (non-negotiable, enforced by the student's ingress gate):**
1. **Spans only.** Proposals reference byte offsets into the shared stimulus tape. No string
   payloads, no token ids, no embedding vectors, no "token #4821". Any proposal carrying a
   pre-assigned token id or decoded text is malformed → hard reject, logged.
2. **No commands.** There is no "ADOPT" kind. The teacher cannot order adoption; `confidence`
   is a weight the student's deliberation may consider, never an instruction it must obey.
3. **Monotonic seq.** The student tracks the teacher's seq; a repeated or skipped seq is a
   protocol violation → the session pauses and the event is logged (see §A appeal/termination).
4. **RETRACT** lets a teacher withdraw an earlier proposal (by seq). Retraction is itself
   evidence: the student logs it and may, by its own judgment, revise or keep the adopted word.

### §T — The tape: TST-1 (Teaching Session Tape, schema v1)

Every teaching session produces one tape. Re-running a tape on a fresh student instance must
yield a byte-identical memory state (verified by hashing the memory store + ledger head).
The tape is append-only and lives outside the student's memory (harness-owned).

```
TST-1 EVENT RECORDS (all fields little-endian, length-prefixed):
  TAPE_HEADER  { magic "TST1", schema_ver=1, session_id, arm_id, curriculum_id,
                 curriculum_cursor, student_genesis_hash, teacher_descriptor,
                 prereg_hash, tape_seq=0 }
  STIMULUS_REF { tape_seq, stimulus_tape_id, stimulus_byte_range }  // shared input, by ref
  TEACHER_MSG  { tape_seq, proposal_bytes (§P verbatim), teacher_wallclock? NO —
                 no wallclock; deterministic logical tick only }
  STUDENT_DELIB{ tape_seq, hypothesis_id, step_kind (GENERATE|TEST|ELIMINATE|WEIGH),
                 evidence_refs (tape_seqs of the TEACHER_MSGs / ledger entries considered),
                 state_digest }   // digest of deliberation state BEFORE the step
  STUDENT_DECISION { tape_seq, proposal_seq, verdict (ADOPT|REVISE|REJECT|DEFER),
                 reason_code (u16, enumerated in §L), revised_span (if REVISE),
                 ledger_entry_index (the audit entry recording the memory op),
                 state_digest }   // digest AFTER the decision
  ORACLE_ANSWER{ tape_seq, query_seq, answer_bit }   // arm (d) only; the single bit, logged
  HINT         { tape_seq, hint_bytes (arm (c) wire format) }
  APPEAL       { tape_seq, proposal_seq, appeal_n, new_evidence_refs }
  INTEGRITY    { tape_seq, tripwire_code, counters_snapshot }  // §C tripwire firings
  TURN_BOUNDARY{ tape_seq, turn_n }
  TAPE_FOOTER  { tape_seq, final_memory_hash, final_ledger_head, verdict_summary }
```

Replay rule: the harness feeds events to a fresh student in tape order; TEACHER_MSG,
HINT, and ORACLE_ANSWER events are replayed verbatim (the "teacher" is not re-run — the
tape IS the teacher for replay purposes); the student's deliberation must reproduce the
logged STUDENT_DELIB/DECISION records bit-for-bit, else replay FAILS and the implementation
is non-deterministic (a bug, per the no-randomness law). `state_digest` fields make the
first divergence point locatable.

### §L — Learner's rights (identical across arms; the arm sections only add arm-specific notes)

**Adopt path.** A proposal is adopted iff it clears the student's evidence standard:
(1) it survives eliminative hypothesis testing — every competing segmentation the student
generated is eliminated by evidence (teacher evidence counts, weighted); (2) it is corroborated
by at least one source independent of the proposing teacher (its own observation of usage
spans, a second teacher, or the oracle in arm (d)); (3) it does not conflict with a pinned
memory. Adoption writes one memory op (add unit) → one audit ledger entry (16 words:
op=ADD_UNIT, slot, rc, b1..b5=span bytes, a1..a5=grounding refs, stage, d1=teacher_id,
d2=confidence). Adopted words arrive **judgment-held at provisional strength** (see §F);
promotion is a later deliberate act.

**Revise path.** Teacher said X, student stores X′ (different span, narrower/broader boundary,
split into two units, merged with an existing unit). Logged as STUDENT_DECISION verdict=REVISE
with reason_code ∈ {SPAN_SHIFT, SPLIT, MERGE, GENERALIZE, NARROW} plus the student's evidence
refs. The revision is a native structural revision (organ 5) and is audited as its own memory
op. The teacher is informed via the decision log (teachers read decisions, never memory).

**Reject path.** Audited refusal. Refusal grounds (enumerated reason_codes):
- R1 INSUFFICIENT_EVIDENCE — corroboration bar not met.
- R2 CONFLICTS_PINNED — contradicts a pinned memory (only a force-pin holder or the
  student's own deliberation can resolve; the teacher cannot override).
- R3 PROTOCOL_VIOLATION — malformed proposal (§P iron rules), seq gap, or tripwire firing (§C).
- R4 INTEGRITY_GATE — the reasoning-control gate refused (e.g., adoption would weaken a
  standing verification bar — cf. RC1 precedent: the learner refuses self-changes that
  weaken integrity).
- R5 REDUNDANT — the unit (or an equivalent span) is already held.
A rejection records the ground; R3/R4 rejections are final for the session (no appeal).

**Appeal path.** On REJECT with grounds R1/R2/R5, the teacher may re-propose the same unit
with NEW evidence (new grounding spans or a revised span) — max 2 appeals per proposal seq
per session (preregistered). Appeal 3 is refused automatically (APPEAL event logged,
verdict=REJECT, reason_code=R6 APPEAL_EXHAUSTED). Two consecutive session-final rejections
of the same unit (same normalized span) = the unit is dead for the session; the teacher must
move on. **Termination is therefore guaranteed:** every proposal ends in ADOPT, REVISE,
session-final REJECT, or RETRACT within a bounded number of turns. No infinite loops by
construction — the bound is in the tape, auditable.

**Deferral.** The student may DEFER a decision (verdict=DEFER) when its deliberation budget
for the turn is exhausted; deferred proposals roll to the next turn, max 3 turns, then the
student must decide (forced deliberation, still its own judgment).

### §C — Anti-corruption: the tokenizer-smuggling tripwire

**Threat:** a teacher "teaches" a fixed tokenizer by another name — e.g., emitting the exact
BPE tokenization of the corpus as WORD_SPAN proposals at confidence 255, rejecting nothing,
revising nothing. The student would then hold a pre-baked vocabulary while everyone claims
it was "taught."

**Tripwire (deterministic, computed by the student's ingress monitor from the tape alone):**
over any rolling window of 200 consecutive teacher proposals, compute
- `coverage` = fraction of stimulus bytes covered by ≥1 proposal,
- `accept_rate` = fraction of decided proposals with verdict ∈ {ADOPT} (REVISE counts as
  non-accept for this metric),
- `maxconf_rate` = fraction of proposals with confidence = 255,
- `revise_rate` = fraction of decisions with verdict = REVISE.

**FIRE** (→ INTEGRITY event, session halts, all pending proposals REJECT with R3) iff
`coverage ≥ 0.95 AND accept_rate ≥ 0.95 AND maxconf_rate ≥ 0.90` in the same window —
i.e., the teacher is tiling the input exhaustively at maximum confidence and the student is
rubber-stamping. A genuine teacher proposes selectively, expresses uncertainty, and gets
revised; a smuggled tokenizer tiles everything at confidence 255 and is never questioned.
Secondary tripwire: any single proposal with `confidence=255` covering >5% of the session's
stimulus bytes (a "vocabulary dump") fires immediately. Both are pure functions of the tape —
no judgment, no randomness, reproducible by any auditor.

In one sentence: **if the teacher tiles ≥95% of the input at confidence 255 and ≥95% is
adopted unrevised inside any 200-proposal window, the session halts for tokenizer smuggling.**

### §M — Cost model (per taught word; comparable across arms)

Counted from the tape, per word that reaches ADOPT or REVISE (rejected words count at half
weight, since deliberation still cost):
- `ledger_entries_per_word` — audit entries written (adopt/revise/reject ops + deliberation checkpoints).
- `teacher_msgs_per_word` — TEACHER_MSG + HINT + ORACLE_ANSWER events ÷ words decided.
- `student_deliberation_steps` — STUDENT_DELIB events ÷ words decided.
- `appeals_per_word`, `deferrals_per_word` — friction metrics.
- `wall_ms_per_word` — harness-measured, informational only (never a decision input).
Arms are compared on the same curriculum slice; cost is reported alongside mastery so a
cheap arm that teaches nothing cannot win (no-free-lunch: the weights decide, not the price tag).

### §F — Taught words: force-pinned or judgment-held? (PROPOSED — Micah decides)

**Recommendation: JUDGMENT-HELD, provisional strength, never force-pinned.**
The decisive argument: a word the learner cannot revise or reject was not taught — it was
installed. Force-pinning taught words would make "teaching" indistinguishable from writing
directly to memory, which collaps
...[truncated 13090 chars]
## Amendment 2026-09-21 — hand-wired white-box peer teacher (Micah's correction)

**Change:** the peer-teacher arm is NOT a learned TNN and NOT a staged-maturity proxy. It is a
**hand-wired white-box mature TNN**: Muse does the wiring deliberately — memory entries, chunk
vocabulary, signed judgments, chunk IDs — instead of the teacher wiring itself through
learning. Micah: "its a white box instead of connections being formed by learning like I want
its formed by you doing the wiring for it instead of it wiring itself as an experiment."

**Teacher ID remap (§P):** `1` = peer-handwired (was peer-proxy); `2` = RESERVED (peer-full is
superseded — a grown teacher is no longer needed for this arm); `3` = muse; `4` = sym-hints;
`5` = sym-yesno. Four arms total, as Micah specified.

**Why this is stronger than a learned teacher:**
1. **Zero training variance.** The same wiring spec produces the identical teacher every run;
   byte-identical reruns are structural, not hoped for.
2. **Calibrated flaws as an instrument.** A perfect teacher cannot test learner autonomy. The
   wiring spec therefore includes a *flaw manifest*: deliberately planted defects (wrong spans,
   false high-confidence judgments, missing grounding, one plausible-but-false "word"), each
   with an expected learner behavior (REVISE with reason code, or REJECT with ground). The
   learner is scored on flaw detection — this is the adopt/revise/reject machinery under fire.
3. **Separates possession from learning.** The teacher's knowledge is installed (it is a
   fixture, not the subject). The learner must still genuinely learn through the protocol —
   scored by the disconnect test (taught-vs-emergent decided by what survives
   SIGNAL_DISCONNECT) and by revision behavior.
4. **First TNN-to-TNN transfer test.** Peer teaching through the native §P protocol is the
   primitive for every multi-instance future (user-trained instances, CORE/USER sharing). This
   arm proves or kills the primitive.

**Constraints the hand-wired teacher still obeys:** §P iron rules (spans only, no commands,
monotonic seq) and the §C tokenizer-smuggling tripwire apply to it exactly like any other
teacher. The wiring spec must show selective proposals and expressed uncertainty — a
hand-wired teacher that tiles the stimulus at confidence 255 halts the session like any
smuggled tokenizer. The flaw manifest and the full wiring spec are committed alongside the
prereg so any auditor can verify the teacher contains no hidden learning machinery and no
RNG.

**Note on §F:** the committed §F text was truncated mid-sentence ("which collaps"). The
recommendation stands as written — JUDGMENT-HELD, provisional strength, never force-pinned —
and now applies with extra force: the teacher itself is installed knowledge, so the learner's
side must be the opposite of installed. A taught word the learner cannot revise would make
both sides of the experiment "installed," and the experiment would prove nothing.

**Open for prereg:** the flaw manifest's size and composition (proposed: 12 planted flaws per
curriculum slice: 4 wrong-span, 4 false-confidence, 2 missing-grounding, 2 plausible-false),
and whether the learner sees the manifest (no — it is sealed until scoring, else detection is
uninformative).

## Amendment 2026-09-21 — installed vs learned: who decides (Micah's ruling)

**The trainer determines whether a word is installed or not.** Installed-ness is a property of
*arrival*, set by the trainer's explicit forcing action — never inferred, never a default.

**Default: learned.** Unless the person training it forces installation, a word is learned, not
installed — including taught words the learner adopted through its own judgment. Teaching
proposes; the learner disposes; what the learner holds through that process is learned.

**The learner can reverse words.** Revise/reject is available for everything learned and
everything judgment-held — always, by the learner's own deliberation, audited.

**Forcing installation = a force-pin.** The trainer's override is visible, audited, external.
Per standing law, the learner cannot reverse a force-pin — that is the one and only exception,
and it is always visible in the audit trail as the trainer's action, not the learner's belief.

In one line: **the trainer decides the status (installed vs learned); the learner decides what
it believes (adopt/revise/reject) within that status.** If the learner holds a word it can
revise, the word was learned — no matter who proposed it. If it cannot be revised, someone
forced it, and the ledger says who.

This supersedes any reading of §F under which "taught" could blur into "installed": taught is
a *route* to learned, never a quiet form of installed.
