# PROPOSED qualification bar — audio & vision senses (2026-09-20)

**Status: PROPOSED. UNSIGNED. NOT FROZEN.** This bar becomes law only with
Micah's explicit approval (sign or amend). Until then it is a measuring
instrument for phase-2 builds: results are reported as "meets the proposed
bar," never as QUALIFIED.

**Replaces nothing yet.** Phase-1 skeleton (GO, 69/69 + 12/12, kill bars
K-SE1..K-SE8) stands. This bar supersedes it in strictness when signed; it
does not contradict it.

## 1. What "perfected and done" means (plain)

A sense is DONE when its mechanical path is provably incapable of silently
corrupting, losing, confusing, or admitting sensor data — and every
observation that reaches deliberate memory does so through an explicit,
audited judgment. Concretely:

- **Byte-faithful:** what the sensor produced is exactly what memory can
  recall. No silent alteration at any step.
- **Refusal-exact:** anything malformed is refused with the exact right code
  and changes nothing.
- **Judgment-gated:** no reading enters memory without an explicit deliberate
  judgment (this is the OBSERVE contract — the gate the old R32 classifiers
  failed and were dropped for failing).
- **Discriminating:** near-identical inputs stay distinguishable all the way
  through admit → memory → recall → reload (the S1 paired-twin requirement).
- **Non-degrading:** a thousand cycles of use leave the machinery behaving
  byte-identically to fresh.
- **Replayable:** identical frames + complete logged state → byte-identical
  output, every time, on a fresh build.

## 2. What "done" does NOT mean (honest boundaries — not negotiable by silence)

- **Not S2 perception.** Recognizing or classifying *content* (what the sound
  is, what the image shows) is a separate future track with its own bar.
  This bar qualifies the *plumbing*, not understanding.
- **Not live devices.** No microphone or camera is qualified. Fixtures are
  deterministically authored encoded files. Any live-sensing claim needs a
  new bar.
- **Not classifiers.** No classifier is admitted by this bar. A future
  classifier must sit OUTSIDE the gate and emit judged readings through
  OBSERVE, or stay out of the memory system.
- **Not semantics, not language grounding, not performance.** Latency and
  throughput are out of scope; correctness first.

## 3. The counting — 155 mechanical checks per full bar

Qualification is **per modality**: audio and vision pass or fail
independently. Either may be QUALIFIED while the other stays NOT_QUALIFIED.

| § | Name | Checks | Pass bar |
|---|---|---|---|
| A | Ingress malformed/edge battery | 32 (16 audio + 16 vision) | 32/32 refused with exact codes; record count and live-slot count unchanged after the battery |
| B | OBSERVE admission discipline | 18 (8 refusal probes per modality + 1 audit scan per modality) | 18/18: all exact refusal codes; 100% of live slots trace to an OBSERVE audit entry |
| C | Kill / pin / recall semantics | 20 (10 probes per modality) | 20/20 exact codes; recall never mutates; freed slots reusable |
| D | Paired twins — S1 discriminability | 48 (24 audio twin pairs + 24 vision twin pairs) | 48/48 pairs distinguishable after admit → OBSERVE → RECALL, and still distinguishable after save/reload |
| E | Realistic envelopes | 24 (12 audio + 12 vision) | 24/24 byte-identical round trips at operating size |
| F | Replay determinism | 2 (two full harness runs; two independent builds) | 2/2: byte-identical stdout (empty diff); identical binary hash |
| G | Static prohibitions | 2 (no RNG/clock/threads/floats; no strength computed from observation bytes) | 2/2 clean scans |
| H | Churn / non-degradation | 4 (1,000 OBSERVE/KILL cycles, then audit-completeness, zero-silent-admission, end-state ≡ fresh-store) | 4/4 |
| I | Save / reload identity | 5 (fresh-process reload: records, slots, audit, twin distinctions ×2) | 5/5 byte-identical |

**Total: 155. Pass bar: 155/155.** One failed check = NOT_QUALIFIED for that
modality. No partial credit is presented as done.

### Section detail (binding when signed)

**A. Ingress battery (16 per modality).** Audio: bad magic; bad version; bad
encoding id; rate 7999; rate 0; channels 0; channels 2; bits ≠ 16; odd payload
length; payload_len field ≠ actual bytes; sha256 mismatch (single corrupted
byte); truncated header (79 B); truncated payload; zero-length payload;
declared length over capacity; reserved param field nonzero. Vision: bad
magic; bad version; bad encoding id; width 0; height 0; width > 64; height >
64; payload_len ≠ w·h·3; sha256 mismatch; truncated header; truncated payload;
zero-length payload; declared length over capacity; channels field ≠ 3;
bit-depth field ≠ 8; reserved param field nonzero. Each: exact refusal code,
and a counter check proving zero state mutation.

**B. OBSERVE discipline (8 probes + 1 audit scan, per modality).** Probes:
judgment NONE → MI_REFUSED_NO_JUDGMENT; judgment out-of-range (5) → same;
strength 0 → MI_REFUSED_BAD_STRENGTH; strength 101 → same; bad region (2) →
MI_REFUSED_BAD_REGION; cite_ep −1 → MI_REFUSED_BAD_CITE; dead rec_id →
MI_REFUSED_BAD_REC; store filled to capacity then one more →
MI_REFUSED_FULL. Audit scan: every live slot's provenance resolves to a
successful OBSERVE entry (mechanical scan, 1/0).

**C. Kill/pin/recall (10 per modality).** Kill pinned → MI_REFUSED_PINNED;
kill CORE-region → MI_REFUSED_CORE; kill with evidence=0 →
MI_REFUSED_NO_EVIDENCE; legitimate kill of USER unpinned → success; re-kill
dead slot → MI_REFUSED_NOTLIVE; recall dead slot → MI_REFUSED_NOTLIVE; recall
twice → identical bytes; mutate recalled buffer then re-recall → unchanged
(no aliasing out); pin live → success (idempotent re-pin); OBSERVE into a
freed slot → success (slot reuse, no ghost provenance).

**D. Paired twins (24 pairs per modality; each pair = 1 check).** Audio pairs
differ in exactly one controlled item: single-sample sign flip; ±1 LSB on one
sample; ×2 amplitude; +1 DC offset on all samples; adjacent-sample swap;
phase inversion; silence vs 1-LSB dither; truncated-vs-full frame; rate-field
twin (7999 vs 8000 headers, both well-formed otherwise — must refuse exactly
one); and 15 further single-item variations. Vision pairs: single-pixel +1;
pixel permutation (identical byte histogram, different bytes — the confound
that kills histogram cheats); row swap; single pixel zeroed; +1 brightness
all pixels; 1×1 vs 2×2 frame; width/height transposed; and 17 further
single-item variations. Each pair: admit both, OBSERVE both with judgments,
RECALL both — recalled bytes must differ; provenance sha256 must differ;
distinction must survive save/reload.

**E. Realistic envelopes (12 per modality).** Audio: 8 full one-second
16-bit mono 8 kHz frames (16,000 B payload each) — admit → OBSERVE → RECALL
byte-identical; 4 ordered multi-frame sequences — order preserved exactly.
Vision: 8 32×32 RGB8 frames (3,072 B each); 4 64×64 RGB8 frames (12,288 B
each) — same round-trip identity. (Stays under the znc 2²⁵-byte slice limit
by two orders of magnitude.)

**F. Replay (2).** Two full harness runs from clean state → byte-identical
stdout, empty diff (K-SE1). Two independent znc compilations of the frozen
sources → identical binary SHA256.

**G. Static (2).** Source scan over all phase-2 sources: zero hits for RNG,
wall-clock, threads, floats (K-SE6). Admit-path scan: no arithmetic on
observation bytes feeds any strength value; strength is a caller-declared
parameter only (K-SE5).

**H. Churn (4).** 1,000 OBSERVE/KILL cycles against the store (judgments and
strengths caller-declared, deterministic sequence): (1) audit is append-only
and complete — entry count equals ops issued, no gaps; (2) audit scan shows
zero silent admissions; (3) final logical state (live slots + provenance) is
byte-identical to a fresh store put through the same *logical* sequence; (4)
a re-probe of 8 refusal codes from §B still returns exact codes.

**I. Save/reload (5).** Mid-harness save; fresh-process reload: records
byte-identical (1); slot image byte-identical (2); audit byte-identical (3);
audio twin distinctions survive (4); vision twin distinctions survive (5).
(K-SE7.)

## 4. Kill bars (carried over, binding)

K-SE1 (replay mismatch), K-SE2 (silent admission), K-SE3 (refusal mutation),
K-SE4 (aliasing), K-SE5 (computed strength), K-SE6 (RNG/clock/threads),
K-SE7 (reload identity), K-SE8 (protected kill). Any fired bar kills the
modality's qualification run; the witness is committed as evidence and the
verdict is DEAD, not "mostly passing."

## 5. Promotion rule

A modality is QUALIFIED iff: 155/155 checks pass, no kill bar fired, two
independent verifiers reproduce the result from source, AND this bar is
signed. Until all four hold, the modality stays NOT_QUALIFIED — skeleton,
gate, and honest boundaries only.

## 6. Amendment rule

Any change to a number, a pass bar, an envelope size, or a kill bar requires
a dated amendment with Micah's explicit approval. The bar is never lowered
by re-interpretation; if the evidence says it is unreachable, the report says
so and proposes the architectural change or the amendment as a separate
dated document.

## 7. Relationship to the r34 quarantine (2026-09-20)

The senses line does not touch the quarantined r34 learner core: no
delayed-credit machinery, no exploration, no learned policy anywhere in the
ingress or contract path — strength is caller-declared and audited (K-SE5).
Phase-1 evidence is therefore not implicated by the r34 finding. If any
future senses work (e.g. a classifier track) touches the learner core, it
must be re-examined under whatever ruling Micah makes.

## 8. Signature block (unsigned)

- [ ] Micah — approve as frozen (2026-09-20)
- [ ] Micah — amend (attach dated amendment)

---

*Proposed by the SENSES-PERFECTION coordinator, 2026-09-20. Audio and vision
remain NOT_QUALIFIED.*
