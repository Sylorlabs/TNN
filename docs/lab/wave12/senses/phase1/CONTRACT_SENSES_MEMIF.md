# Senses Memory-Interface Contract — design (phase 1, 2026-09-20)

Status: FROZEN with `PREREG_SENSES_PHASE1.md`. Implemented in `se_memif.zag`;
qualified by `run_phase1.sh`. Audio and vision remain **NOT_QUALIFIED** as
senses; this contract is the gate the old R32 acoustic classifiers failed
(and are DROPPED for failing — see `../ASSESSMENT_SENSES.md` verdicts 11–13).

## 1. Why a contract

Old classifiers (R32 acoustic PAMs) kept their "memory" as hidden recurrent
state: no deliberate add/kill/pin/promote, no judgment-set strength, no
CORE/USER separation, no citation episodes, seed-selected training. That is
not deliberate memory — it is a function with hidden state. The standing law
is: **a sensor reading becomes something the memory system can act on only
through an explicit deliberate operation with an explicit judgment.** This
contract is that gate.

## 2. Entities

- **Sensor record** (ingress side): an owned, immutable, SHA256-bound byte
  record in the `SeStore`, admitted transactionally (validate → reserve →
  commit) with explicit refusal codes. Records are never mutated after admit.
- **Memory slot** (memory side): a deliberate-memory cell carrying:
  `live`, `pinned`, `region` (CORE/USER), `judgment`, declared `strength`
  (1..100), `cite_ep` (citation episode), and `provenance` = (sensor record id
  + payload sha256). Provenance binds the cell back to exact sensor bytes.
- **Op audit**: append-only log, 256 entries × 8 words
  (op, slot, rc, judgment, strength, region, cite_ep, rec_id).

## 3. Op table (only ops that exist)

| Op | Preconditions (all enforced, refused otherwise) | Effects |
|---|---|---|
| `OBSERVE(judgment, strength, region, cite_ep, rec_id)` | judgment ∈ {NOVEL, CORROBORATED, CONTRADICTED, TRAINER_DIRECTIVE} (≠ NONE); strength 1..100 declared by caller; region ∈ {CORE, USER}; cite_ep ≥ 0; rec_id is a live record; free slot | copies record's payload sha256 into slot provenance; records judgment/strength/region/cite_ep; audit entry |
| `PIN(slot)` | slot live | sets pinned; audit |
| `KILL(slot, evidence)` | slot live; evidence ≠ 0; slot NOT pinned; slot NOT CORE-region | clears live; audit |
| `RECALL(slot, out)` | slot live; out big enough | copies record bytes to caller; NO mutation; audit |

**There is deliberately no PROMOTE/DEMOTE/STRENGTHEN/WEAKEN on this path in
phase 1.** Strengthening/weakening a sensor-derived memory requires an
explicit new OBSERVE (new judgment, new citation episode); the old slot is
killed (or kept as distinct evidence). Strength is never computed from
observation content — K-SE5 static gate. Caller discipline + static check +
audit is the enforcement; the boundary is documented honestly.

## 4. Refusal codes (exact, mechanical)

- `MI_REFUSED_NO_JUDGMENT` (-7201): judgment NONE or out of range. **This is
  the kill-bar code for K-SE2: the gate physically cannot admit a reading
  without a judgment.**
- `MI_REFUSED_BAD_STRENGTH` (-7202): strength ∉ 1..100.
- `MI_REFUSED_BAD_REGION` (-7203): region ∉ {CORE, USER}.
- `MI_REFUSED_BAD_REC` (-7204): rec_id not a live record.
- `MI_REFUSED_FULL` (-7205): no free slot (phase-1 store: 16 slots).
- `MI_REFUSED_PINNED` (-7206): KILL on a pinned slot.
- `MI_REFUSED_CORE` (-7207): KILL on a CORE-region slot (TNN-caller may not
  kill CORE; only the human/trainer force-pin path may — the standing
  force-pin-as-law boundary).
- `MI_REFUSED_NOTLIVE` (-7208): op on a dead/absent slot.
- `MI_REFUSED_BAD_CITE` (-7209): cite_ep < 0.
- `MI_REFUSED_NO_EVIDENCE` (-7210): KILL with evidence == 0.

## 5. The three-way handshake

Reading → memory actuation is exactly this:
1. Ingress validates the record (magic, version, encoding, params, length,
   payload sha256) and admits it to an owned, immutable copy — or refuses
   with an exact code and **zero state mutation** (K-SE3).
2. A deliberate caller issues OBSERVE with an explicit judgment
   (NOVEL / CORROBORATED / CONTRADICTED / TRAINER_DIRECTIVE), a declared
   strength, a region, and a citation episode. No judgment → refusal (-7201).
3. The slot is bound to the sensor bytes via payload sha256. Every live slot
   must trace to a successful OBSERVE audit entry (K-SE2 audit scan).

## 6. Determinism / no-RNG

No randomness, no wall-clock, no threads, no floats anywhere in the path.
Given identical frames and the complete logged state (records + memory image),
the binary produces byte-identical output (K-SE1: two full harness runs,
empty diff). Save/reload is a byte-exact image: fresh-process reload
reproduces records, metadata, slots, audit, and paired twin distinctions
(K-SE7).

## 7. What the contract does NOT cover (honest boundaries)

- No live-microphone/camera qualification; envelope is PCM16LE mono 8 kHz
  (≤ 4,096 B) + RGB8 1×1..4×4 encoded fixtures only.
- No classifier is qualified: a future classifier may only *emit judged
  readings* — it must sit OUTSIDE the gate and pass readings through
  OBSERVE with explicit judgments, or stay out of the memory system.
- Strength remains caller-declared; the anti-shopping and calibration rules
  from the felt-intensity program apply when callers change judgments.
- Delayed-credit / formula-computed strength machinery is DROPed, not
  smuggled in through the contract (ASSESSMENT verdict 13).

## 8. Falsifiability

The contract dies if any of these fire: K-SE1 (replay mismatch), K-SE2
(silent admission), K-SE3 (refusal mutation), K-SE4 (aliasing), K-SE5
(computed strength), K-SE6 (banned constructs), K-SE7 (reload identity),
K-SE8 (protected kill). All eight were probed clean in phase 1; the verdict
is GO for the skeleton only.
