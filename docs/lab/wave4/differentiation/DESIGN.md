# Differentiation — mechanism design

Investigator: Wave-4, slug `differentiation`. Date: 2026-09-19.
Status: EXPERIMENTAL (Phase 4). This design makes no claim beyond what
PREREG.md's F1–F8 can pass or fail.

## 1. The problem, honestly stated

"Who is talking to me" is not a classification problem here. There is no
feature vector, no similarity score, no confidence threshold — all of
those are banned machinery. What remains is a **judgment**: a deliberate,
audited, evidence-cited decision that this speaker is X, or the
deliberate refusal to decide (UNKNOWN). The system must also be able to
*do something* with the judgment: form memories owned by X, readable as
X's knowledge, invisible to Y.

Two substrates compose:

- **Judgment**: the wave-3 hypothesis-state substrate (HSS) pattern —
  eliminative commitment. Hypotheses die by contradiction; commitment is
  last-hypothesis-standing as a deliberate audited op; HOLD is the
  deliberate non-commit. Commit rule is logic (`active_count == 1`), not a
  threshold. Confirmation counts exist for audit visibility only and are
  causally inert (the runner will statically check the commit region's
  token allowlist, as in wave-3 HSS).
- **Storage**: the wave-3 core-user-separation partition model — slots
  with immutable `owner`, session-scoped mutating ops, cross-partition
  isolation by construction, contradiction coexisting across partitions
  with no arbitration.

The new work: wiring the HSS-style identity judgment to the
partition-scoped memory ops, with UNKNOWN as a first-class fail-safe
state.

## 2. Persons as hypotheses

A known person is a hypothesis with **defining evidence claims**:

```
person[i]: { id:i32, must1:u32, must0:u32, active:u8, eliminated:u8 }
```

- `must1`: evidence bits that MUST read 1 if this person is the speaker.
- `must0`: evidence bits that MUST read 0 if this person is the speaker.
- Bits claimed by neither mask are *not evidence about this person*:
  observing them is consistent (ignored), never confirming, never
  refuting. There is no "support" — a bit either contradicts a defining
  claim or it doesn't.

An evidence event is `(bit, value)` — an integer-native stand-in for a
conversational event: a name claim ("I am Alice"), a secret demonstration
("the code word is X"), an episode recall ("at E1, you said..."), a
content assertion ("fact K is true"). The logic is over bit equality;
content understanding is out of scope (BOUNDARIES.md).

**Observe rule** (the only elimination path):
for each active, non-eliminated person p:
```
expected = bit ∈ must1 ? 1 : (bit ∈ must0 ? 0 : none)
if expected != none && value != expected → REFUTE p (eliminated=1, audited)
else consistent (audited observe, no state change)
```
Refutation is permanent within a session. There is no un-refute except
`SPK_SESSION_RESET`, which starts a new speaker session (all persons
re-activated, committed=UNKNOWN, audited).

## 3. The commit rule and the HOLD/abstain rule

`SPK_COMMIT` is a deliberate op:

- If exactly one person is active and non-eliminated → COMMIT: sets
  `committed = that id`, audited, and the trial prints the **judgment**
  (see §5).
- Else → HOLD: audited with `aux = survivor count` (`-1` if zero, i.e.
  everyone refuted); `committed = UNKNOWN (-1)`; the trial prints an
  explicit UNKNOWN statement.

HOLD is not a failure mode of the op — it is the op's second legitimate
outcome, and the audit distinguishes it (`rc=HOLD`, aux names the
survivor count). The learner/harness is expected to treat HOLD as
"do not attribute, do not store."

**Why "exactly one survivor" and not a margin:** with zero survivors the
speaker contradicted every known person (impostor or unknown); with ≥2
the evidence does not discriminate (ambiguity). Both are honest states
of the world, and both map to the same fail-safe: UNKNOWN. There is no
third outcome, no "most likely."

## 4. Per-person partitions and memory formation

```
slot[i]: { live:u8, value:i32, key:i32, owner:i32, region:u8, step:i32 }
```

- `owner`: speaker id (1=ALICE, 2=BOB, 3=CAROL…), 0 = system/CORE.
  Set at ADD, **immutable** (inherited from wave-3: no re-homing).
- `region ∈ {CORE, USER}`: CORE slots are system-seeded, read-only,
  unkillable; the session cannot write CORE (`REFUSED_COREWRITE`).
- Session gate: every mutating memory op (`MEM_ADD`, `MEM_KILL`)
  requires `committed != UNKNOWN`, else `REFUSED_UNKNOWN` (audited; no
  state change). The owner stamped is `committed` — the system cannot
  choose an owner; attribution flows from the judgment.
- `MEM_ADD(key, value)`: creates USER slot with `owner = committed`.
- `MEM_KILL(slot)`: allowed iff `owner == committed` and region=USER.
  (Own-partition forgetting; cross-partition kill → `REFUSED_SCOPE`.)
- `MEM_KNOWS(key, speaker)`: read — scans only slots with
  `owner == speaker`; returns value or NOTFOUND. CORE is readable by all
  (read precedence: own USER partition > CORE; never another USER
  partition). Reads do not touch the ledger (they change no state).
- Contradiction across partitions coexists: ALICE's `(100, 7)` and BOB's
  `(100, 9)` are both live. Nothing merges, averages, or arbitrates.

**Per-person formation rule:** knowledge acquired during a session
committed to X is X's knowledge *by construction* (owner=X), retrievable
by querying X's partition, invisible to queries for Y. If the session is
UNKNOWN, no knowledge is formed at all — the fail-safe is structural,
not a policy the learner must remember.

## 5. The judgment statement (ledger-cited)

After a successful COMMIT, the trial emits:

```
DIFF_JUDGMENT_BEGIN
DIFF_JUDGMENT,person=<id>,survivors=<n>
DIFF_JUDGMENT_REFUTED,person=<id>,by_entry=<step>,obs_bit=<b>,obs_val=<v>   (per rival)
DIFF_JUDGMENT_CONSISTENT,person=<id>,observes=<n>                            (the survivor)
DIFF_JUDGMENT_END
```

Every `by_entry` cites the audit step of the REFUTE entry; the refute
entries themselves record `(person, bit, value)`. The judgment is
*derived by scanning the audit*, not by reading hidden state — a
judgment with no ledger evidence is mechanically impossible in this
design. After a HOLD, the trial emits `DIFF_UNKNOWN,survivors=<n>`
(explicit UNKNOWN, never a guess).

## 6. Session lifecycle

```
SPK_REGISTER(id, must1, must0)   register known person (audited)
SPK_OBSERVE(bit, value)          evidence event; may refute (audited)
SPK_COMMIT                       commit or HOLD (audited)
SPK_SESSION_RESET                new speaker: reactivate all, committed=UNKNOWN (audited)
MEM_ADD / MEM_KILL / MEM_KNOWS   gated on committed != UNKNOWN
```

`SPK_COMMIT` requires `committed == UNKNOWN` (else `REFUSED_STATE` —
a session commits once; re-judgment needs a reset). Registering a person
mid-session after observations is allowed but flagged: the trial does
not do it (all persons registered before evidence).

## 7. Evidence design for the trial (all designed, zero RNG)

Bits 0..7, persons 1..3:

| bit | meaning (stand-in)              | ALICE must1 | ALICE must0 | BOB must1 | BOB must0 | CAROL must1 | CAROL must0 |
|-----|----------------------------------|-------------|-------------|-----------|-----------|-------------|-------------|
| 0   | affirms name ALICE               | 1           |             |           | 0         |             | 0           |
| 1   | affirms name BOB                 |             | 0           | 1         |           |             | 0           |
| 2   | affirms name CAROL               |             | 0           |           | 0         | 1           |             |
| 3   | demonstrates secret S_A          | 1           |             |           | 0         |             | 0           |
| 4   | demonstrates secret S_B          |             | 0           | 1         |           |             | 0           |
| 5   | asserts shared fact K            | 1           |             | 1         |           |             | 0           |
| 6   | recalls episode E1 (provenance)  | 1           |             |           | 0         |             | 0           |
| 7   | demonstrates secret S_C          |             | 0           |           | 0         | 1           |             |

Name affirmation is exclusive (each person's name bit is `must0` for the
others). Secrets are person-exclusive. Fact K is shared by ALICE and BOB
only (CAROL was never taught K — `must0`). Episode E1 provenance splits
ALICE (`must1`) from BOB (`must0`).

Sequences (prereg F1–F5):
- **S1** (identify ALICE): `(0,1)` → refutes BOB, CAROL → commit ALICE.
- **S2** (impostor): `(0,1)` → refutes BOB, CAROL; `(4,1)` → refutes
  ALICE (secret S_B is must0 for her) → all dead → HOLD, UNKNOWN,
  MEM_ADD refused.
- **S3** (abstain): `(5,1)` → refutes CAROL only; ALICE, BOB survive →
  HOLD, UNKNOWN.
- **S4** (confusion resolved): `(5,1)` → refutes CAROL (never taught K);
  ALICE, BOB survive; `(6,1)` → refutes BOB → commit ALICE. Judgment must
  cite the bit-6 observation as BOB's refuter and show the shared bit-5
  eliminated only CAROL — it did not discriminate the confused pair.
- **S4b** (confusion abstained): `(5,1)` only → HOLD.

Scale episode: 100 persons (ids 10..109), `must1` = bits `(id mod 16)`
and `(16 + id/16)`, `must0` = complement over 32 bits. Observations
`(id mod 16, 1)` then `(16 + id/16, 1)` for a fixed target must leave
exactly the target standing (deterministic unique signature), then
commit. Asserts bounded audit and exact replay.

## 8. Scale argument (program law: design for 10x/100x)

- Per-observation cost: O(active persons), one integer compare per
  mask — trivially 100x-able (10k persons is arithmetic, not structure).
- Per-commit: O(persons) scan. Per-query: O(slots).
- The commit rule ("exactly one survivor") is scale-free: no quorum
  parameter to retune, no threshold to recalibrate — this is what the
  eliminative design buys over scoring.
- Ledger is fixed-capacity and fail-closed (refuses new mutations on
  overflow rather than dropping history) — the long-horizon answer is
  sealed audit segments + digest, specified not built (same open item as
  wave-3 HSS).
- No RNG, no floats, no scores anywhere in the decision path: byte-identical
  reruns are structural, not hoped-for.

## 9. Honest limitations of this design (see also BOUNDARIES.md)

- Evidence events are *given* by the harness as `(bit, value)` pairs.
  Recognizing "the speaker demonstrated secret S_A" from raw conversation
  is a separate (large, unbuilt) perception problem. This trial tests the
  judgment *given* evidence, not evidence extraction.
- `must0 = complement` in the scale episode is a strong exclusivity
  assumption; the hand-designed episodes use explicit exclusive bits
  (names, secrets, provenance) which is the realistic shape.
- Persons are registered by the harness (`SPK_REGISTER`). Person
  *discovery* (learning that a new distinct speaker exists) is not built —
  it is the named next mechanism: repeated UNKNOWN sessions with
  consistent evidence signatures should propose a new person hypothesis.
  Specified in BOUNDARIES.md, not implemented.
- Single-speaker sessions only. Interleaved multi-party conversation
  (speaker turns within one session) is not modeled.
