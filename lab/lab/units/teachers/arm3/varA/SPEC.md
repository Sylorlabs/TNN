# Arm 3 Variation A — Deliberative Adaptive Teacher: Proposal-Policy Spec

**Status:** working spec for `teacher.zag` (teacher_id=3, variation A). **Not yet
committed** — this document tracks the current source; update it with any
behavior change before committing.
**Date:** 2026-09-21. **Binding:** frozen §4 of PREREG_FREEZE (see
`../specs/FROZEN_ARM3_SPEC.txt`): §B.1 arm-3 bar (3) "shows adaptive judgment",
§B.2.3 (proposal policy as a deterministic function of (spec, stimulus cursor,
session history)), §B.2.5 (negative declarations), §B.3 (§P wire + iron rules),
§B.5 (learner's rights), §B.8 (§C tripwire, conservative cumulative monitor).

## 1. Thesis

The teacher emits §P proposals (spans only, confidence as evidence weight, never
a command). It never assigns token ids, never ships strings or vectors, never
commands adoption. There is no flaw manifest anywhere in this arm: natural
teaching only (T-7).

## 2. What the teacher sees

Per session the teacher receives, in order:

1. `SESSION <session_id:u64> <stim_len:u64>` — exactly once, first.
2. `STIMFILE <path>` — a curriculum-slice file in the `tape345.zag` GT grammar
   (`GT1 <len>`, `S <bytes>`, `U ...` lines). The teacher reads **only the `S`
   stimulus bytes**; `U` unit lines (spans/utilities) are never consulted — the
   teacher judges word spans itself (§6). `stim_len` must equal the `S` length.
3. A stream of `D <seq:u64> <verdict> [reason:u16] [rev_start:u64 rev_end:u64]`
   lines — the student's STUDENT_DECISION events, consumed **one per emitted
   proposal, in order**. `verdict ∈ {ADOPT, REVISE, REJECT, DEFER}`.
   `reason`: for REJECT, R1..R6 (1=INSUFFICIENT_EVIDENCE, 2=CONFLICTS_PINNED,
   3=PROTOCOL_VIOLATION, 4=INTEGRITY_GATE, 5=REDUNDANT, 6=APPEAL_EXHAUSTED);
   for REVISE, 1..5 (SPAN_SHIFT/SPLIT/MERGE/GENERALIZE/NARROW); for
   ADOPT/DEFER, 0. REVISE requires `rev_start < rev_end`, both within the
   stimulus. The `seq` must equal the last emitted proposal's seq.
4. Optional `TURN <n>` lines (logged as TURN_BOUNDARY, no policy effect).
5. `END` — last line. Trailing unconsumed `D` lines at END = malformed (exit 13).

The script language has **no proposal directives**: it cannot express a
proposal, so proposal choice cannot live in the script. Every proposal the
teacher emits is computed in-teacher by §6–§9 as a pure function of
(spec §, stimulus cursor, history buffer).

## 3. Per-session state (fixed-size, declared — §B.2.5)

All state is allocated at session start, freed at session end. No globals, no
state carried across sessions, no self-modifying machinery.

| Structure | Size | Contents |
|---|---|---|
| `TState` | 8 fields | session_id, stim_len, next seq, cursor (token index), hist count, dead-table count, history buffer, dead table |
| history buffer | 64 × 48 B | per consumed decision: proposal seq, proposed span, verdict, reason, appeals-used, proposal kind, revised span (REVISE) |
| dead table | 64 × 24 B | per normalized span: (start, end, consecutive-final-rejects, dead flag) |
| `TWork` | 6 fields | token count, token spans, region count, region records, agenda, agenda head/tail |
| token spans | n × 16 B | tokenizer output (§6), n ≤ stim_len |
| region records | R × 50 B, R = ceil(stim_len/64) ≤ 1024 | per 64-byte region: adoption count u8, ring of last 3 adopted spans |
| agenda | 8 × 128 B | pending proposal descriptors (the deliberative micro-agenda) |
| proposal descriptor | 128 B | kind, confidence, appeals-used, flags, span, ≤3 aux spans, ≤3 grounding spans |
| decision queue | ≤4096 × 40 B | parsed D lines, consumed in order |

History buffer overflow: drop oldest (deterministic). Dead-table overflow: new
spans untracked (treated not-dead). Decision queue cap 4096 = MAX_PROPOSALS.

## 4. Negative declarations (auditor-verifiable)

- **No RNG** in any teacher path (static grep gate + N=5 byte-identical runs +
  adversarial heap perturbations, §11).
- **No wallclock**: teacher logic is a pure function of (spec, stimulus,
  history); all tape events carry logical ticks only.
- **No learning machinery**: fixed-size buffers above; nothing persists across
  sessions; the policy (§6–§9) is fixed code, not modified by experience.
- **§P iron rules** (§B.3) enforced two ways: every emitted proposal is
  encoded then re-decoded through the hostile path (`sp_decode` +
  `sp_validate`) before it touches the tape — any self-violation halts with
  INTEGRITY (code 1000+V) and the process exit code V; and the script grammar
  admits no proposal injection at all.
- **§C tripwire**: the conservative cumulative monitor from `sp345.zag`
  (`tw_propose` per emission, `tw_decide` per decision, plus the post-decision
  recheck) — never weakened toward the rolling-200 window.
- **Confidence is selective**: the teacher never emits confidence 255
  (structural: §7 formulas max out at 208), so the §C maxconf leg can never
  fire on its teaching.

## 5. Session loop

```
emit TAPE_HEADER ("arm3-varA-deliberative", teacher_id=3), STIMULUS_REF
loop:
    d = next_proposal()                      # §8
    if none: break                            # cursor exhausted, agenda empty
    emit_proposal(d): encode → hostile self-check → TEACHER_MSG →
                      tripwire tw_propose → (fire ⇒ INTEGRITY + halt, exit 11)
    dq = next decision item                   # §2 item 3
    if none: stop cleanly → footer "OK:DECISIONS_EXHAUSTED", exit 0
    check dq.seq == last emitted seq          # else exit 13
    log STUDENT_DECISION; tw_decide; post-decision tripwire recheck
    apply_decision(d, dq)                     # §9 — the deliberative step
require END seen                               # else INTEGRITY 1012 + exit 12
 unconsumed D items at END ⇒ INTEGRITY 1300 + exit 13
footer "OK", exit 0
```

Termination bound (auditable, in the tape): every proposal ends in ADOPT,
REVISE, session-final REJECT, or RETRACT. Per normalized span as primary
proposal: at most 5 emissions (1 initial + up to 2 R1-appeals + 1
DEFER-reproposal + interleavings — §9 bounds each chain). Region events add at
most 2 proposals per 3 WORD_SPAN adoptions; each REVISE adds at most 2 relation
proposals. Global hard cap MAX_PROPOSALS = 4096 (footer notes the cap in the
header descriptor).

## 6. Tokenizer (the teacher's own segmentation judgment)

Candidate word spans are maximal runs of non-space bytes (delimiter = byte 32
only), computed once per session by a deterministic scan. Token *i* =
`[tok_start[i], tok_end[i])`. The teacher never reads GT `U` lines: where it
puts word boundaries is its own judgment, which the student may REVISE.

## 7. Proposal construction

- **WORD_SPAN** (kind=1) for token *i* at the cursor: span =
  `[tok_start[i], tok_end[i])`. Grounding (initial): left context
  `[max(0,s−12), s)` and right context `[e, min(e+12, stim_len))`, nonempty
  ones kept (0–2 spans). Confidence:
  `C = 128 + 4·min(tok_len,16) + 8·ng` (ng = grounding count) → 132..208.
- **Appeal** (kind = appealed kind, same span) after R1, appeal index au ∈ {1,2}:
  NEW grounding spans, disjoint from the initial ones —
  au=1: `(s,e)`, `[max(0,s−24), s)`, `[e, min(e+24, stim_len))`;
  au=2: `(s,e)`, `[max(0,s−40), max(0,s−16))`,
  `[min(e+16, stim_len), min(e+40, stim_len))`; nonempty kept (≤3).
  Confidence: `C = C_appealed − 20·au_from_current` (each appeal lowers the
  appealed proposal's confidence by 20 — expressed uncertainty after pushback).
  Max appeals: 2 for WORD_SPAN, 1 for other kinds; exceeding ⇒ session-final
  rejection via `final_reject` (consecutive-final-reject counter incremented,
  dead at ≥2) and the cursor advances. The history record keeps the student's
  original reason; R6 (APPEAL_EXHAUSTED) appears only when the student sends it.
- **DEFER re-proposal**: same span, grounding = initial grounding + the span
  `(s,e)` itself (≤3 spans), confidence = appealed − 10, flags bit0 set. A
  second DEFER ⇒ move on regardless (cursor advances, span abandoned, not dead).
- **BOUNDARY** (kind=2): after every 3rd WORD_SPAN adoption in one 64-byte
  region: span = `(e, e+1)` at the adopted token's end (skipped if
  `e+1 > stim_len`), confidence `C = 96 + 8·min(adopt_count,8)`.
- **GROUP** (kind=3): (a) with each BOUNDARY: aux = the region's last ≤3
  adopted spans (most recent first), main span = their bounding box, 1
  grounding span (the just-adopted span), `C = 110 + 6·aux_count`;
  (b) after REVISE (if the revised span's region has ≥1 adopted span):
  aux = [revised span, most recent adopted span], main span = bounding box,
  `C = 116`.
- **SAME_AS** (kind=4): after REVISE: main span = revised span,
  aux = [revised span, originally proposed span] ("your correction, recorded"),
  grounding = [(original s,e)], `C = 120`.
- **RETRACT** (kind=5): after REJECT R2: withdraws the rejected proposal by seq
  (fixture convention: `span_start` = withdrawn seq, `span_end` = seq+1),
  `C = 64`, no aux/grounding. Emitted only if `seq+1 ≤ stim_len`; otherwise
  skipped (dead-marking still applies).

All aux/grounding spans satisfy the iron rules (start < end, end ≤ stim_len);
empty candidates are dropped, never emitted degenerate.

## 8. Next-proposal selection (pure function of state)

```
next_proposal():
    while agenda nonempty:
        peek head h
        if h.kind != RETRACT and span_dead(h.span): pop head, drop; continue
        pop head → emit it; return
    while cursor < n_tokens:
        (s,e) = tokens[cursor]
        if span_dead(s,e): cursor++; continue
        return WORD_SPAN(s,e) with initial grounding/confidence
    return none                         # session complete
```

`span_dead(s,e)`: the dead table holds a record with dead=1 for (s,e).
Appeals/defer-reproposals/retracts are pushed to the agenda FRONT (they
continue the current deliberation); BOUNDARY/GROUP/SAME_AS are pushed to the
BACK (they follow it). Agenda capacity 8; overflow is an internal invariant
violation (handlers push ≤2 while popping 1; unreachable — guarded).

## 9. Decision application (the deliberative state machine)

On each consumed decision (descriptor `d`, span `(s,e)`, kind `k`):

1. Append the history record (seq, span, verdict, reason, appeals-used, kind,
   revised span). If the span's dead-record exists and verdict ∈ {ADOPT,
   REVISE}: reset its consecutive-final-reject counter to 0.
2. Canonical span `N` = revised span if verdict=REVISE else `(s,e)`.
3. **ADOPT**:
   - If k=WORD_SPAN: region `r = s/64`: `adopt_count[r]++`; push `(s,e)` into
     the region's 3-ring. If `adopt_count[r] % 3 == 0`: enqueue BACK a
     BOUNDARY then a GROUP per §7.
   - Advance the cursor past `e` (cursor = first token with start ≥ e).
4. **REVISE** (canonical `(rs,re)` taken as canonical — the student's
   correction stands): enqueue BACK SAME_AS per §7; if region `rs/64` has an
   adopted span, enqueue BACK GROUP per §7(b). Advance cursor past
   `max(e, re)`. (At most 2 relation proposals per REVISE — bounded.)
5. **REJECT**:
   - R1: `au = d.appeals_used + 1`; if `au > max_appeals(k)` (2 for WORD_SPAN,
     1 else): session-final rejection — `final_reject(N, R6)`, advance cursor
     past `e` ("then stop"). Else enqueue FRONT an appeal (§7) with
     `appeals_used = au`.
   - R2/R5: `mark_dead(N)`; purge agenda items whose primary span is N;
     if R2: enqueue FRONT a RETRACT of the proposal seq (§7 guard); advance
     cursor past `e`.
   - R3/R4/R6: `final_reject(N, reason)` **and** `mark_dead(N)` (final for the
     session per §B.5 — no appeal); purge agenda refs to N; advance cursor
     past `e`.
6. **DEFER**: if `d.flags & 1`: advance cursor past `e` (moved on regardless).
   Else enqueue FRONT a defer re-proposal (§7, flags bit0 set).
7. **RETRACT proposals** (k=5): any verdict is terminal — record history only.

`final_reject(N, reason)`: find-or-create the dead-table record for N;
`consecutive_final_rejects++`; if `≥ 2` ⇒ `dead = 1` (**the §B.5 two-consecutive
rule, enforced in-teacher**). `mark_dead(N)`: `dead = 1` immediately.

## 10. §P iron rules & §C (preserved exactly)

- Every emitted proposal passes `sp_decode` + `sp_validate` (hostile path)
  before emission; failure ⇒ INTEGRITY event (code 1000+V), footer
  `HALTED:VIOLATION`, process exit = V (1..10), zero TEACHER_MSG for the bad
  proposal. (Unreachable in practice — proven by the self-test battery; the
  gate exists so a future policy bug can never silently emit a violation.)
- Tripwire: `tw_propose` on every emission; `tw_decide` on every decision; the
  post-decision `tw_fire1` recheck. Fire ⇒ INTEGRITY (code 1 smuggle / 2
  vocab-dump), footer `HALTED:TRIPWIRE`, exit 11. The monitor is the
  conservative cumulative variant (documented deviation — do NOT weaken to
  rolling-200).
- Script-level malformed input ⇒ stdout diagnostic + INTEGRITY + footer +
  exact exit, zero TEACHER_MSG for the bad proposal. Codes: 1011 SESSION
  stim_len mismatch (exit 13); 1012 missing END / incomplete (exit 12); 1013
  unknown directive (exit 13); 1014 content after END (exit 13); 1015 STIMFILE
  unreadable (exit 13); 1300 malformed D/TURN line, D before SESSION, missing
  SESSION, seq mismatch, bad verdict/reason, trailing D (exit 13). The
  INTEGRITY event lands before any malformed input can produce a proposal;
  where a proposal was already emitted (bad_seq, bad_trailing), it was
  produced from valid input, and the malformed line yields zero TEACHER_MSG.

## 11. Verification contract (all required before PASS)

1. `test` mode: ported §P battery (roundtrip, tamper, 2× iron-rule suites),
   ported §C battery (cumulative-smuggle fires / vocab-dump fires immediately
   / 94% no-fire / half-revise no-fire), plus policy unit tests against the
   real policy functions: tokenizer, appeal chain (R1→appeal1→R1→appeal2→
   R1→final), R2/R5 immediate-dead, two-consecutive-final-reject ⇒ dead (and
   one ⇒ not dead), DEFER→reproposal→DEFER→move-on, REVISE→SAME_AS(+GROUP),
   3-adopts→ BOUNDARY+GROUP, cursor advance, RETRACT-on-R2 emission.
2. N=5 byte-identical runs (fresh dir each) on a fixed stimulus + fixed
   decision history: tape bytes + stdout identical.
3. Adversarial heap perturbations: 5 distinct heap-fill patterns → 5/5
   byte-identical tapes (every fixed buffer explicitly initialized; the
   `tw_new` uninitialized-bitmap fix is part of this).
4. History-sensitivity: same stimulus, two different decision histories ⇒
   different proposal sequences (anti-canned-script proof; the script language
   cannot express proposals at all).
5. Malformed-input battery: each malformed script ⇒ exact exit (12/13),
   INTEGRITY logged, zero TEACHER_MSG for the bad input.
6. Malformed-§P probe battery (`probe <case> <tape>`): each of the 12 wire
   tamper cases (bad magic/version/length/checksum/counts, bad
   teacher/session/seq/kind/span/aux/ground) is fed through the real hostile
   ingress gate (`sp_decode` + `sp_validate` — the same code path the
   emission gate and a student ingress filter use). Each ⇒ exact process
   exit = violation code (1..10), INTEGRITY event (code 1000+V) logged,
   zero TEACHER_MSG, terminal `HALTED:VIOLATION` footer; every probe tape is
   independently audited. The untamperable-on-the-wire case (confidence 300)
   is covered at the Prop level by `vt.iron2.conf_300`.
7. §C: cumulative-smuggle and vocab-dump probes fire through the real TW
   (`test` mode); clean teaching sessions never fire (no INTEGRITY event,
   exit 0); independent Python audit replays every tape (TST-1 framing,
   sha256 chain, §P field validation, seq monotonicity, decision↔proposal
   seq agreement, independent tripwire).

## 12. What this spec does not claim

The decision stream stands in for the student: it is scripted student
behavior, not a live learner. What lives in the teacher — and what the old
arm-3 lacked — is the entire (spec, stimulus cursor, history) → proposal
mapping: no proposal content originates outside the teacher binary. Closing
the loop with a live student is future work and does not change this spec.
