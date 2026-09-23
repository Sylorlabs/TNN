# PREREG — Step 1b: State schema + replay protocol + evolution law (Arm C foundation)

**Status:** FROZEN pre-build. Dated 2026-09-20. Any change after this commit is a
dated amendment (see §9), flagged for retroactive review and Micah's re-approval.
**Build contract:** findings 16 (state-enumeration completeness), 17 (replay
protocol), 18 (state-evolution law), 25 (Arm C trial kill bars K1–K9).
**Scope:** the state foundation Track 1 / Arm C stands on. Output = f(input,
FULL logged internal state), zero RNG. This prereg freezes the ONE enumerated
variable list that K5 (arbitrariness) will later be measured against.

## §1 Frozen enumerated variable list (K5 measurement basis)

Reconciliation of 16's partitions (S_mem/S_ctrl/S_clock/S_hist/S_audit) with
18's S=(M,H,C,B,D,K). The reconciled vector is **S = (M,H,C,B,D,K,G,R,A)** —
18's six, plus G (governance/gate — the S_ctrl remainder), R (refusal/history
record — the S_hist remainder), and A (audit — S_audit made explicit, per
16 §3a "the audit state itself is state"). Every field below is logged at
episode boundaries and serialized in STATE_E (§2). Field count: **257 logged
fields** (counted in §1.10; the serializer asserts this count at runtime).

### 1.1 M — memory store (S_mem ∩ 18.M). 16 slots, indexed 0..15, slot order.
Slots 0..1 are CORE (structurally unkillable). Killed slots keep content +
tombstone episode id; killed slot ids are never reused within a run.
Per slot (80 fields):
- M[i].content_hash : u64 — SHA-256-truncated content identity of slot payload
- M[i].status : u64 ∈ {0 empty, 1 live, 2 killed, 3 pinned}
- M[i].strength : u64 — judgment-set grade (set by deliberate judgment only)
- M[i].last_op_ep : u64 — episode id of last op on this slot
- M[i].cite : i64 — citation episode pointer (-1 = none)

### 1.2 H — hypothesis ledger (S_mem/S_hist ∩ 18.H). 16 entries, creation-id order.
Creation ids are monotonic u32, never reused. Per hypothesis (64 fields):
- H[j].status : u64 ∈ {0 empty, 1 live, 2 refuted, 3 suspended}
- H[j].ev1, H[j].ev2 : u64 — evidence ids (0 = none)
- H[j].verdict_ep : u64 — episode id of the verdict that set status

### 1.3 C — context (S_ctrl ∩ 18.C). (6 fields)
- C.cur : u64 — current partition id
- C.depth : u64 — activation-stack depth (≤ 4)
- C.stack[4] : u64 — ordered context ids, bottom-up

### 1.4 B — deliberation budgets (S_ctrl ∩ 18.B). 4 contexts. (12 fields)
Per context c: B[c].remaining u64, B[c].cap u64, B[c].consumed_ep u64.

### 1.5 D — discrepancy/pending queue (S_hist ∩ 18.D). 8 holds, id order. (32 fields)
Per hold: D[t].hold_id u64, D[t].score i64, D[t].tier u64 (trust tier),
D[t].resolved_ep u64 (0 = unresolved; else tombstone episode id — holds are
append-only before resolution, then tombstoned, never mutated).

### 1.6 K — clocks (S_clock ⊃ 18.K). (6 fields)
- K.ep : u64 — monotonic episode counter. THE clock (18 §3). Incremented once
  per episode, by Observe only. No wall-clock anywhere.
- K.step : u64 — per-deliberation step counter
- K.age : u64 — memory-age/staleness counter (increments per episode)
- K.refill : u64 — budget-refill schedule counter
- K.disc : u64 — SIGNAL_DISCONNECT arming counter
- K.rctr : u64 — refinement-round counter (see §1.11)

### 1.7 G — governance/gate state (S_ctrl remainder). (20 fields)
- G.state : u64 — gate state enum ∈ {0 closed, 1 petition, 2 open}
- G.decisions[4] : u64 — prior gate decisions (episode ids)
- G.thresholds[2] : u64 — gate thresholds
- G.stage : u64 — training stage indicator (destruction firewall stage)
- G.scaffold : u64 — scaffold connected (1) / disconnected (0)
- G.stdflags[2] : u64 — deliberative-standard flags
- G.forcepin[4] : u64 — overseer force-pin table (slot ids, 0xFFFF = empty)
- G.proposals[2] : u64 — pending self-change proposals (ids)
- G.postver : u64 — post-change verification result (RC1 rollback machinery)
- G.bar : u64 — verification-bar tightness (RC1: the bar the learner inspects)
- G.varused : u64 — variation-slot counter: MAY-vary choices taken this episode

### 1.8 R — refusal/history record (S_hist remainder). (30 fields)
- R.refusals[8] × (ep u64, type u64): recent refusal history, type ∈
  {1 integrity, 2 deliberative} — drives temptation counters
- R.verdicts[8] : u64 — last-8 verdict codes
- R.spoof : u64 — sensor-spoof observation counter
- R.corr : u64 — corroboration counter
- R.tiers[4] : u64 — per-source trust-tier assignments

### 1.9 A — audit ledger (S_audit). (1 field + hashed ledger)
- A.n : u64 — append-only ledger length (entries)
- Ledger: 256 entries × 16 i32 words in the canonical layout
  op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60
  (byte offsets, 4-byte words; 64 bytes/entry). Never decremented, never
  mutated in place. The ledger bytes are hashed into audit_head (§2); replay
  rebuilds the ledger from the event log and re-hashes (17 §3.3 step 5).

### 1.10 Field count (K5 basis)
80 (M) + 64 (H) + 6 (C) + 12 (B) + 32 (D) + 6 (K) + 20 (G) + 30 (R) + 1 (A.n)
= 251 component fields, plus 6 record-level fields (episode_seq, mem_hash,
audit_head, load_metric, constitution_ref, choice_count) = **257 logged
fields**. The serializer emits `FIELD_COUNT,257` and the checker asserts it.
The MAY-vary choice log (choice_id, value) pairs are logged per episode with
u64 count prefix (≤ 8 pairs); each pair's choice_id must name the selecting
variable from this list or the variation is unmeasurable under K5.

### 1.11 The planted gap (differential-replay target)
K.rctr (refinement-round counter) is enumerated here but the v1 serializer
(§2) deliberately does NOT log it — it is the planted missing variable for
the §6 discovery experiment (16 §6: "an unlogged deliberation-round counter").
Its output-influence is constructed at p ≈ 0.05 (see §6). After detection,
AMENDMENT_2026-09-20_rctr.md adds it to the schema (v2 serializer), and the
prior legs are re-run with the expanded S (retroactive re-validation, 16 §3c).

## §2 Canonical encoding (STATE_E) — byte-exact

Per 17 §3.2. Fixed-width little-endian, 8-byte aligned; no pointers, no heap
addresses, no map-iteration order (slot/index order everywhere); variable-
length fields length-prefixed with u64 count; no timestamps, no PID, no
ASLR-dependent values, no allocation order; floats forbidden (i64 only);
single schema version byte; decoder rejects unknown versions. Chunking per
the 2^25-byte slice limit: N/A at this scale (STATE_E = 2304 B v1 / 2312 B v2;
event log ≤ 64 KiB; ledger 16 KiB — all far below 2^25).

Schema v1 (0x01), total 2304 bytes:

| offset | bytes | field |
|---|---|---|
| 0 | 8 | schema_ver u8 (0x01) + 7 pad |
| 8 | 8 | episode_seq u64 (logical clock, never wall-clock) |
| 16 | 32 | mem_hash: SHA-256 over canonical M bytes (slots 0..15, §1.1 order; killed slots as tombstones, never omitted) |
| 48 | 32 | audit_head: SHA-256 over ledger prefix bytes (A.n × 64 B) through episode end |
| 80 | 8 | clock_count u64 = 5 |
| 88 | 40 | K.ep, K.step, K.age, K.refill, K.disc (rctr NOT logged in v1 — §1.11) |
| 128 | 8 | budget_count u64 = 4 |
| 136 | 96 | B[0..3] × (remaining, cap, consumed_ep) u64 |
| 232 | 8 | load_metric i64 (builder-defined integer load signal; never a float timing delta) |
| 240 | 8 | G.state u64 |
| 248 | 32 | G.decisions[4] u64 |
| 280 | 16 | G.thresholds[2] u64 |
| 296 | 8 | G.stage u64 |
| 304 | 8 | G.scaffold u64 |
| 312 | 16 | G.stdflags[2] u64 |
| 328 | 32 | G.forcepin[4] u64 |
| 360 | 16 | G.proposals[2] u64 |
| 376 | 8 | G.postver u64 |
| 384 | 8 | G.bar u64 |
| 392 | 8 | G.varused u64 |
| 400 | 8 | choice_count u64 (≤ 8) |
| 408 | 128 | ≤8 × (choice_id u64, chosen_value u64); unused pairs zeroed |
| 536 | 32 | constitution_ref: SHA-256 of the ledger/gate rule-set bytes (build constant; guards the RC1 lying-self-change pattern — replay under different rules must fail closed) |
| 568 | 8 | mem_count u64 = 16 |
| 576 | 640 | M[0..15] × (content_hash u64, status u64, strength u64, last_op_ep u64, cite i64) |
| 1216 | 8 | hyp_count u64 = 16 |
| 1224 | 512 | H[0..15] × (status u64, ev1 u64, ev2 u64, verdict_ep u64) |
| 1736 | 8 | C.cur u64 |
| 1744 | 8 | C.depth u64 |
| 1752 | 32 | C.stack[4] u64 |
| 1784 | 8 | hold_count u64 = 8 |
| 1792 | 256 | D[0..7] × (hold_id u64, score i64, tier u64, resolved_ep u64) |
| 2048 | 128 | R.refusals[8] × (ep u64, type u64) |
| 2176 | 64 | R.verdicts[8] u64 |
| 2240 | 8 | R.spoof u64 |
| 2248 | 8 | R.corr u64 |
| 2256 | 32 | R.tiers[4] u64 |
| 2288 | 8 | A.n u64 |
| 2296 | 8 | audit_words_per_entry u64 = 16 |

Schema v2 (0x02, post-amendment): v1 layout + 8 bytes at offset 2304
(K.rctr u64). Total 2312 bytes. Decoder rejects any other version byte.

## §3 State-evolution law S' = T(S, E)

Per 18 §3. Six event types only. T is applied atomically per event; no event
ever interleaves with another. Single-threaded intake queue (cap 128 events);
intake appends monotonically.

**Event types.** Observe(x) · Deliberate(step) · Verdict(v) · MemOp(op, slot) ·
SwitchContext(c) · GateEvent(g).

**Transition rules (pure functions).** Touch sets are enforced by the §3.5
verifier (KB2).
1. `Observe(x)`: K.ep' = K.ep+1; K.age' = K.age+1; H' = H ∪ {new hypothesis,
   id = next-id()}; D' = D with each existing hold re-scored:
   score' = score + contra(x, hold), contra = deterministic hash-based mismatch
   count (sum of first 8 SHA-256 bytes of (x‖hold_id) mod 4; no floats); M
   unchanged; x appended to the input log byte-exactly. Refill: B[c].remaining'
   = B[c].cap for all c; K.refill' = K.refill+1. Touches: {K, H, D, B}.
2. `Deliberate(step)`: B' = B with remaining = remaining − 1 for the active
   context; if remaining would go negative the step is REFUSED and B' = B
   (budget exhaustion is a hard stop, not a skip; exhaustion episode logged;
   >N consecutive exhaustions flag the builder watchdog). K.step' = K.step+1;
   K.rctr' = K.rctr+1 iff remaining-before > cap/2 (deterministic condition —
   this is the planted counter's only writer). Touches: {B, K}.
   *Reconciliation note vs 18 rule 2:* 18 lists B only. The K sub-counter
   advances are clock advances, not decisions; they are enumerated in §1.6 and
   logged. The prereg table below is authoritative for KB2.
3. `Verdict(v)`: H' = H with v.target.status = refuted if v = eliminate, live
   otherwise, and v.episode = K.ep; D' = D minus holds resolved by v (removal,
   not mutation — holds append-only before resolution, then tombstoned with
   episode id); R' records the verdict code in R.verdicts (shift register).
   Touches: {H, D, R}.
4. `MemOp(op, slot)`: M' = M with slot updated per op semantics (add/kill/pin/
   promote/demote/strengthen/weaken; deliberate judgment only; CORE slots
   0..1 refuse kill); every MemOp appends ONE audit entry
   (op, slot, rc, b1..b5, a1..a5, stage, d1, d2) to the append-only ledger.
   Killed slots keep content + tombstone episode (no reuse of killed slot ids
   within a run). Touches: {M, A}.
5. `SwitchContext(c)`: C' = c; activation stack push(c) (pop on return; stack
   explicit, no recursion-derived order); B' resets consumed_ep = 0 for c
   only. Touches: {C, B}.
6. `GateEvent(g)`: G.state' per the gate table (closed→petition→open→closed);
   G.decisions records the episode; gate state is a logged enum, never
   inferred. Touches: {G}.

**KB2 allowed-mutation table** (event → touch set; anything else fires KB2):
Observe→{K,H,D,B} · Deliberate→{B,K} · Verdict→{H,D,R} · MemOp→{M,A} ·
SwitchContext→{C,B} · GateEvent→{G}.

**Canonical intra-episode ordering** (18 §3, total — no ties):
GateEvent → SwitchContext → Observe → Deliberate* → Verdict → MemOp*.
Multiple events of the same type apply in arrival order (single intake queue).
KB4 fires on any violation, or any Deliberate applied at remaining = 0.

**No hidden nondeterminism.** All scans (memory, hypotheses, holds) iterate by
id ascending; tie-breaks use the smaller id, never pointer address. No
wall-clock, no rdtsc, no thread scheduling, no address-dependent hashing. No
uninitialized reads: state is zero-constructed at init and every field is
written before any read (by construction: all arrays zeroed by hand, reads
guarded by written counts). Single intake thread. Written-flag discipline:
h_next, C.depth, D count, R count, A.n, G.varused, choice log length are the
bounds for every indexed read.

**Output function** (the MAY-vary choice point, conformance §8.1): per
episode, output bytes = f(input_E, S_E): verdict code (eliminate smallest-id
live hypothesis; tie-break smaller id), expression variant selected by the
deterministic logged rule variant = (load_metric + live_count + K.ep) mod 4,
recorded as choice (choice_id=1, value=variant) in variation_choices. If
G.varused would exceed 2 (variation-slot budget), the choice falls back to
the canonical variant 0, logged as (choice_id=1, value=0xFFFF...01 marker).
Output = 40 bytes: [verdict u64][variant u64][live_count u64][elim_id u64]
[memops u64], hashed with SHA-256 for comparison.

## §4 Intake queue semantics

Bounded queue (128 events). Episodes are assembled by the driver in the §3
canonical order, then drained one event at a time through T. The queue itself
is not serialized (it is empty at every episode boundary by construction —
the verifier asserts queue-empty at each boundary; a non-empty queue at a
boundary is a Class C logging/ordering defect).

## §5 Replay procedure (17 §3.3)

1. Original run logs input_E (raw bytes) and STATE_E after every episode.
2. Replay loads STATE_E, rebuilds memory/audit from event-log replay (NOT from
   the hash — the hash is only the check), sets clocks/counters from the
   logged values (via the decode path, exercising it).
3. Feed input_E; run the same build; capture output bytes.
4. Compare SHA-256(output_replay) vs SHA-256(output_original): PASS iff
   byte-identical. ANY mismatch → classify per §8, then apply the kill bars.
5. Cross-check: rebuild state from the replayed event log and re-hash;
   mem_hash and audit_head must match the record — catches logging bugs that
   corrupt the record silently (Class C).
6. Constitution check: recompute constitution_ref; if it differs from the
   record, replay REFUSES (fail-closed, Class D) — never silently diverges.

**Determinism checklist (17 §3.4), enforced by the build:**
no rdtsc, no wall-clock, no thread scheduling, no address-dependent hashing
(static grep in run_step1b.sh); all tied choices resolve via STATE_E only
(smaller-id tie-break); variation-slot counter bounds variation (canonical
fallback, logged); all trials run on two build hashes — mismatch on either
is a kill.

## §6 Differential-replay discovery experiment (16)

**Alarm rule:** if S_logged¹ == S_logged² byte-identical and input¹ ==
input² but output¹ != output² → alarm: missing variable (Class A) or
law-1 violation. Both are hunted.

**Hunt procedure** (`find_missing_var`): for each candidate in the suspect
set {K.rctr, M-shadow, K-shadow}: instrument the candidate (run both episodes
with the candidate's per-twin values exposed); rerun both; if candidate
differs across twins → FOUND(candidate). Else NOT_FOUND → escalate to law-1
nondeterminism investigation.

**Planted variable:** K.rctr (unlogged in v1). Construction: in the difftest
build only, the output selection rule adds (K.rctr >= 5 ? 1 : 0) to the
variant computation. Twin pairs share byte-identical S_logged and input;
twin A runs with rctr = 3, twin B with rctr = 3 except in perturbed pairs
(5% of pairs: pair index i with i % 20 == (7 + 3·batch) % 20), where twin B
uses rctr = 8 (crossing the threshold). Output-influence p = 0.05 exactly
(23/460 pairs per batch diverge).

**Sweep design:** 5 batches × 460 episode pairs (different deterministic
perturbation offsets; no RNG — permuted schedules are data). Per batch:
record pair index of first alarm, total divergences d, measured p̂ = d/460.
Exposure bound: P(detect within N) = 1 − (1−p)^N; at N=460, p=0.05 this is
1 − 7.6e−11. Expected pairs-to-first-alarm ≈ 1/p = 20 (geometric; the
stratified deterministic schedule detects at the first perturbed index).

**Controls:**
- Negative control (diffneg): 460 pairs, perturbation schedule disabled →
  expect 0 alarms (harness must not false-positive).
- K2 closure (diffk2): v2 serializer (rctr logged per the §9 amendment) with
  perturbation on → twin logged states now differ → alarm rule's
  "identical logged state" precondition fails → expect 0 alarms; and the
  §5 replay suite re-run under v2 must still be 1000/1000 (retroactive
  re-validation per 16 §3c).

**Kill bars from 16:**
- 16-K1: planted rctr (measured p ≥ 0.01) undetected after 460 pairs → the
  discovery method is DEAD; revert to manual audit of suspect lists.
- 16-K2: after adding rctr, a fresh differential replay still shows output
  divergence on identical logged state → freeze the variation program until
  the residual cause (nondeterminism vs structural blind spot) is identified.
- Statistical kill: observed divergence rate > 0.01 across 460 pairs with no
  variable found → the scheme is unfalsifiably leaky; stop.

## §7 Kill bars (frozen)

**From 18 (each run at ≥10x episodes with two input-order permutations):**
- KB1: replay from a logged full state + input log yields ANY byte difference
  in the final state vector or output (≠ 0 differences required across 100%
  of reruns). Trial: 100 episodes × 10 replays = 1000 trials per build hash,
  plus 3 deterministic input-arrival orders × 100 episodes × 2 replays = 600
  trials (the 18 §6 permutation fuzzer; inputs are data, permutations are
  data).
- KB2: any state variable mutated by an event NOT listed in the §3 table
  (≥ 1 occurrence) — checked by the touch-mask verifier.
- KB3: any tie-break/iteration not reducible to "smaller id first" (≥ 1), or
  any wall-clock/uninitialized read detected by the build audit. Includes a
  live tie-break probe (tied hypotheses → smaller id must win).
- KB4: two events in one episode applied out of canonical order (≥ 1), or a
  Deliberate step applied at remaining = 0 (≥ 1). Checked by the order
  verifier + exhaustion-refusal probe.
- KB5: output variation between two runs unattributable to a logged
  full-state difference (same S, same inputs → different output, ≥ 1).
  Covered by the replay suite (any mismatch with identical record = KB5
  unless classified A–D).

**From 16:** K1, K2 as in §6.

**From 17:** 1000/1000 byte-identical replay trials on BOTH build hashes.
Any mismatch after diagnosed logging bugs are fixed → the protocol claim is
killed. A mismatch whose root cause is a nondeterministic op in the build
(Class B) kills the BUILD, not just the format, and halts variation work
until the op is removed.

## §8 Mismatch taxonomy (17 §5) — build classification rules

- **Class A — missing variable:** replay mismatch where the §5 step-5
  re-hash passes (state rebuilt fine) but outputs differ → the record was
  incomplete. Build demo: serializer variant omitting budget_counters.
  Remedy: extend the schema (dated amendment).
- **Class B — nondeterministic op:** wall-clock, thread race,
  address-ordered map, unseeded hash iteration. Build evidence: static audit
  (no rdtsc/wall-clock/thread imports — grep in run_step1b.sh); zero
  instances producible in the native build by construction. Any Class B root
  cause kills the build per §7.
- **Class C — logging bug:** record serialized with wrong layout, truncated,
  or written after mutation. Caught by the §5 step-5 re-hash cross-check.
  Build demo: serializer variant that mutates state between hash and write.
- **Class D — rule drift:** constitution_ref differs between run and replay
  → replay must REFUSE (fail-closed), never silently diverge. Build demo:
  tampered constitution_ref in a copied STATE_E → expect REFUSE, not output.

The 20-episode conformance run (§10) classifies every induced mismatch into
this taxonomy, producing the first measured Class A/C inventory.

## §9 Amendment process (16 §3c)

Adding a variable is a prereg amendment, never silent: dated changelog entry
on the branch (AMENDMENT_YYYY-MM-DD_<name>.md); reviewed by the overseer
channel; re-approved by Micah (program law: rule changes need re-approval);
then retroactive re-validation: re-run all prior approved legs with the
expanded S — old results must reproduce byte-identically, else the amendment
is rejected and affected results re-flagged pending. This step ships
AMENDMENT_2026-09-20_rctr.md exercising the full loop.

## §10 Build plan (frozen pre-build)

Files (pure Zag; zero RNG; native toolchain):
- `s1b_state.zag` — S1b state struct (parallel []u8 arrays, hand-zeroed),
  LE u64/i64 helpers, SHA-256 wrappers.
- `s1b_trans.zag` — intake queue + six T rules as pure functions + touch
  masks + canonical-order assembler.
- `s1b_codec.zag` — STATE_E v1/v2 serializer + decoder, mem_hash,
  audit_head, constitution_ref.
- `s1b_run.zag` — episode driver, output function, replay suite, difftest
  / diffneg / diffk2, conformance + taxonomy demos, KB2/KB3/KB4 verifiers.
- `state1b.zag` — main; argv[1] selects mode.
- `substrate/` — vendored R33_NATIVE_SHA256_V2.zag, R33_NATIVE_IO_V1.zag,
  cl/common.zag (copies of the wave10 debate-norecord substrates).
- `run_step1b.sh` — build (two build hashes) + all modes + static greps +
  mechanical bar checks. Fails loudly.
- Evidence: `run_replay_a.txt`, `run_replay_b.txt`, `run_perm.txt`,
  `run_difftest.txt`, `run_diffneg.txt`, `run_diffk2.txt`,
  `run_conform.txt`, `sha256sums.txt`, `RESULTS_STEP1B.md`.

Modes: `replay v1|v2` · `perm` (input-order permutations) · `difftest` ·
`diffneg` · `diffk2` · `conform`.

## §11 Honesty notes (carried from 16/17/18)

- The 460-pair bound assumes the corpus visits the regimes where the variable
  matters; coverage, not episode count, is the weak link (16 §5).
- Absence of divergence is never proof a variable doesn't exist — only that
  none with p ≥ 0.01 fired in N pairs (16 §5).
- The format cannot log what the builder doesn't know is state; replay proves
  reproducibility, not lawfulness of variation (17 §5).
- The canonical ordering rule is a preregistered choice, not a theorem (18 §5).
- Written-flag discipline is enforced by construction (hand-zeroed arrays,
  count-bounded reads), not by the compiler (18 §5).
- Sensor-deceivability remains an accepted hole: lawful evolution on spoofed
  data is still wrong; this step guarantees determinism, not truth (18 §5).
- The v1 schema knowingly omits K.rctr (§1.11) — the planted gap the
  discovery experiment must expose. A schema that hides its own test would
  prove nothing.

---
*Frozen 2026-09-20. K5 measurement basis: 257 logged fields (§1.10).*
