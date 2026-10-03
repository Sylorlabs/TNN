# Story — what breaks if the rule is wrong

Two wrong directions: **too permissive** (generative output feedback
allowed — the (G) shape) and **too restrictive** (no output reading at
all — not even (D)-side detection). Plus the third wrong: a **universal
mechanism** imposed on story (the C3 theatrical latch).

## Direction 1: too permissive — (G) allowed

### F1. Thread death by decoration (the primary failure)

Concrete: SETUP renders "The detective polished the key." then `detail()`
adds "The accordion hung in the air." A (G) renderer with a cohesion
heuristic (Arm C in the prereg) scores "accordion" as salient in beat 1's
rendered bytes. COMPLICATION's role scan, preferring words near rendered
nouns, picks the accordion as V (victim) instead of the plan's EVENT
thunderstorm; CLIMAX clutches the accordion; the thunderstorm thread —
the actual plot — never appears again. TC drops to ~0.5 on that story;
PRF drops as "accordion" migrates beats.

Why it's structural, not tunable: the renderer cannot distinguish thread
anchors from decoration *because the distinction is not in the bytes* —
it lives in the plan's (class, beat-assignment) tables. Any (G) heuristic
is therefore guessing at plan structure from a lossy projection. Tuning
the heuristic ("prefer EVENT-class words") just re-implements the plan in
the renderer — at which point the eyes are redundant and the plan should
have been consulted directly. There is no stable middle: either the
heuristic defers to the plan (eyes useless) or it overrides the plan
(drift).

### F2. The telephone game (compounding drift)

Concrete: beat 2 conditions on beat 1's rendered text; beat 3 on beat 2's.
Each conditioning step introduces a small reinterpretation error ε (a
heuristic choice among near-ties). After n beats the story is ε·n away
from the plan in the worst case — and unlike the audio v1 servo, there is
no restoring force at all (the servo at least had frozen targets pulling
it back, however mistargeted; a (G) story renderer has no target, only the
previous beat). Over a 4-beat story the drift is bounded but real
(K2 in the prereg); over a 40-beat serial it is unbounded — the story
walks permanently away from its own premise. This is the narrative twin
of the v1 involution 2-cycle: a neutrally stable dynamics with no fixed
point at the plan.

### F3. Unhealable past (corruption amplification)

Concrete: a write-channel fault zeroes 64 bytes of beat 1 (F1 in the
prereg). Under plan-pure rendering, beats 0/2/3 are intact and beat 1
re-renders to byte-identity. Under (G), beats 2 and 3 were *computed from*
the corrupted beat 1 — their "correct" values no longer exist anywhere:
not in the plan (the plan never specified them as functions of corrupted
input), not in the bytes. Healing requires regenerating the suffix, but
regeneration from what? The corrupted input is gone (overwritten by the
heal) and the clean input never existed as rendered bytes. The story is
permanently forked from every plan-accountable version of itself. This is
the exact causal argument from hybrid §2 — "Re-assertion is the only
correction that heals the past" — and (G) structurally deletes it.

### F4. Silent plan contradiction (the integrity failure)

Concrete: the beat sheet says the detective *finds peace* (RESOLUTION,
class-4 H = "apology"); the (G) renderer, echoing beat 1's rendered
"raging" thunderstorm language, renders the resolution as the detective
*raging on*. No detector fires — every word is present (B1 passes), the
bytes are well-formed. But the story now asserts the negation of its
plan's arc. Under plan-pure rendering this is impossible by construction;
under (G) it is undetectable by any byte-level check, because the bytes
are "valid." This is the story version of the audio integrity concern:
output feedback can corrupt *meaning* while preserving *form*, and
form-checks can't catch it.

**Cost summary (too permissive)**: coherence degrades measurably (TC, PRF),
the past becomes unhealable, meaning can invert while form stays valid,
and every failure is silent — the system looks like it's working. This is
the most dangerous direction because nothing alarms.

## Direction 2: too restrictive — no output reading at all (not even (D))

### F5. Blind to write-channel faults

Concrete: the `st[8192]` story buffer overflows on a long set (S8 has 12
words; with `detail()` sentences per leftover word, RESOLUTION can exceed
the buffer) and the story truncates mid-RESOLUTION. Under the recommended
rule, the Piece-2 detector catches the missing closing line and re-renders
(into a correctly sized buffer — the re-render is also the resize
opportunity). Under the too-restrictive rule, the truncated story ships
silently. The native code has no detector at all today — this failure mode
is *live*, not hypothetical.

### F6. Blind to rendering faults

Concrete: a class-table error (say `key` misclassified) makes `r_climax`'s
O-scan find nothing; the object thread dies (H2 in FAULT_ANALYSIS.md).
The plan tables look perfect — `plan_del`'s verify pass sees full beats.
Only the rendered text shows the dropped anchor. The too-restrictive rule
forbids reading it, so the fault is undetectable by construction. The
story ships with a dead thread and the audit log (`seq_r`) claims
everything was CLASS_SLOT-assigned correctly — the system's own records
assert a coherence the artifact lacks.

### F7. No interactive story

Concrete: the user says "the detective is afraid of thunderstorms" mid-
telling. Under the recommended rule this is an H3 plan event: deliberate,
amend, re-render. Under the too-restrictive rule the system cannot even
*ingest* the edit as data about its own output — it would have to
regenerate blindly from the unamended plan and hope. Interactive fiction,
collaborative storytelling, and trainer corrections of told stories all
require (D)-side output reading. Banning it bans the application.

**Cost summary (too restrictive)**: real, live fault modes (F5 is in the
code today) go undetected; rendering faults are invisible to a perfect-
looking plan; interactivity is impossible. Less dangerous than too-
permissive (failures are *missing* healing, not *active* corruption), but
a real cost — this is why the recommended rule *permits* (D)-side reading
rather than banning output contact entirely.

## Direction 3: universal mechanism — the theatrical story latch (C3)

### F8. Sensor→plan fabrication

Concrete: mandate "every path gets a RESPOND-style output-sensing latch,"
so story gets one: after beat 1, "measure" anchor-word density from
rendered bytes and "correct" beat 2's plan nominal toward it. But the
rendered text is a pure function of the plan — the sensor can only return
what the plan already says (then it's a no-op with extra steps) or return
something else (then it's wrong, and the latch writes wrongness into the
plan with the *authority of measurement*). In audio the latch is honest
because the sensor reads physics the plan can't compute; in story there
is no physics — only the plan, reflected. A mandated story latch is either
dead weight or a fabrication engine, and it wears the uniform of a
validated mechanism, which makes it harder to remove later than an
obviously-bad (G) renderer.

**Cost summary**: process damage — a universal-mechanism rule forces every
path to carry machinery that is load-bearing somewhere and theater
elsewhere, and theater with authority is worse than no machinery at all.

## Net assessment

| Wrong direction | Failure character | Detectability | Reversibility |
|---|---|---|---|
| Too permissive (G) | active corruption: drift, unhealable past, meaning inversion | silent (form stays valid) | poor (suffix undefined after corruption) |
| Too restrictive (no (D)) | missing healing: blind faults, dead threads, no interactivity | visible (artifacts wrong, logs claim fine) | good (add detection later) |
| Universal mechanism | fabrication with authority | disguised as validated | poor (entrenched by mandate) |

Too-permissive is the dangerous direction: its failures are silent and
structurally irreversible. The recommended rule's asymmetry — generous to
(D), absolute against (G) — follows directly: permit everything needed
for detection, diagnosis, and deliberated plan events; ban the one shape
(generative feedback) whose failure mode is silent corruption of meaning.
