The designs below are buildable as deterministic Zag. They do not touch M1 `conf≥705 ∧ mrgF≥3588`, do not add retention guards, and do not revive F5 as a confirm path. F5 remains block-only. C3 repair at RK-3' = 71.78% on the frozen admission tape is the baseline. Numeric cutoffs inside kill bars and in Part B are **program decision thresholds** (what the crew will treat as pass/fail), not runtime caps inside TNN. Where a mechanism needs a ceiling, the ceiling is physical memory or the znc 2^25-bytes-per-slice toolchain limit; the latter is worked around by an explicit slice directory, never treated as a property of the mind.

Shared implementation conventions (every sketch assumes these):

- Arenas are `[]u8`. Multi-byte fields are written and read with explicit little-endian accessors. No `[]i32` / `[]u32` / `[]u16` casts.
- Every table is either append-only in assignment order or kept sorted by a named key. Iteration is always ascending id or ascending key. Tie-break is always the lowest id.
- Lookup is binary search on a sorted id-index, never walk of a hash map.
- A content hash is a pure function (FNV-1a 64, offset basis `14695981039346656037`, prime `1099511628211`, over the exact canonical bytes). It is an address, not entropy.
- Producer identity comes from a compiled `ProducerTable` sorted by `producer_id`. The declaration on the percept is never an input to a gate bit.
- If an arena cannot grow inside physical memory, the path **fail-closes** (no admit, no eviction heuristic). If a single slice would exceed 2^25 bytes, spill to a new slice and record a `SliceDir` entry `{key_lo, key_hi, slice_id}` sorted by `key_lo`. Decisions are unchanged.
- Per-admission scratch is O(percept length), not O(stream length).

---

# PART A — WILD ARCHITECTURES

## W8 — Canonical Transform Gate (CTG)

### 1. Name + pitch

**Canonical Transform Gate.** Raw percept bytes never become belief. A deterministic canonicalizer rewrites the proposal into a claim record whose provenance class is **derived from the producer table and structural features**, and C3 is run only on that record. The declaration string is stored as an untrusted exhibit and is not an input. GEN→EXT relabel and Declaration Fork fail because the label the attacker wrote is not in the gate's input vector. Forged authority fails unless a structural authority token is present in the producer row. What enters the belief arena is the claim, not the payload.

### 2. Mechanism sketch

**Sits:** between G1 proposal formation and the frozen C3 gate. It does not replace C3 and does not recalibrate it. Post-gate, belief readers are allowed to read `ClaimRec` only.

**Trigger:** every G1 proposal.

**Inputs:** `proposal_id`, percept bytes, `percept_len`, `producer_id` (G1-stamped from the actual producer, not from the payload), `declared_prov` byte, `declared_auth` bytes. `declared_*` are copied into the exhibit and then ignored by the decision.

**State:**

| Table | Record | Size | Notes |
|---|---|---|---|
| `ProducerTable` | `{producer_id:u32, class:u8, auth_token:u64, sensor_envelope:u8}` | 24 B, compiled, sorted by `producer_id` | class ∈ {UNK=0, EXT=1, GEN=2, DERIVED=3, REPORT=4} |
| `ProvRule` | `{rule_id:u16, require_mask:u16, require_val:u16, result:u8}` | 8 B, compiled, sorted by `rule_id` | first full match wins |
| `ClaimArena` | `ClaimRec` 64 B | append-only | see fields below |
| `ExhibitArena` | raw canonical bytes | append-only | not belief |
| `Ledger` | `{claim_id:u32, rule_id:u16, c3_bit:u8, prov_derived:u8}` | 8 B | one line per proposal |

`ClaimRec` (64 B, explicit zero-init before fill): `claim_id:u32, subject_hash:u64, predicate_id:u16, object_hash:u64, prov_derived:u8, decl_prov_exhibit:u8, flags:u8, producer_id:u32, exhibit_off:u32, exhibit_len:u32, c3_bit:u8, rule_id:u16, _pad`.

Feature bits (u16), extracted in bit-index order:

- b0 producer row exists
- b1 `class==EXT`
- b2 `class==GEN`
- b3 `class==REPORT`
- b4 `sensor_envelope==1`
- b5 `auth_token!=0`
- b6 payload contains an authority *claim* (fixed ASCII marker table, scanned left to right) while b5 is 0
- b7 canonical parse succeeded
- b8 `declared_prov != class` (computed, **not** fed to C3; only selects a rule)
- b9 multi-claim percept (more than one clause)
- b10–b15 reserved zero

`ProvRule` v1 (compiled, lowest `rule_id` first): R0 parse-fail → UNK; R1 GEN class → GEN; R2 authority-claim without token → UNK; R3 REPORT class → REPORT; R4 EXT and sensor envelope → EXT; R5 else if row exists → DERIVED; no match → UNK.

**Procedure:**

1. Reject if `percept_len==0` or producer binary-search misses. Write ledger `rule_id=0`, do not call C3.
2. Canonicalize into a scratch buffer of length ≤ `percept_len`: reject on NUL or non-UTF-8; map CR LF and CR to LF; map ASCII A–Z to a–z; collapse each run of space/tab/LF to a single 0x20; strip leading and trailing 0x20. Non-ASCII bytes are copied unchanged (no locale tables).
3. Split clauses on `;` in left-to-right order. Each clause splits on the first `|` into subject and rest, and the rest on the first `|` into predicate and object. A clause that does not yield three non-empty fields is a parse fail for that clause only.
4. For each clause in byte order: `predicate_id` = binary search of the compiled predicate dictionary; unknown predicate → that clause rejects. `subject_hash` and `object_hash` = FNV-1a over the exact field bytes.
5. Build the feature word. Scan `ProvRule` from `rule_id` 0 upward; first row with `(features & require_mask) == require_val` sets `prov_derived`.
6. If `prov_derived==UNK` → ledger reject, no C3 call, no `ClaimRec` in the belief half of the arena (exhibit may still be kept under status REJECT for the audit, marked not-belief).
7. Else pack `ClaimRec` with `prov_derived` and call frozen C3 on `(prov_derived, producer class, predicate_id, the existing C3 inputs C3 already consumes)` — **never** on `declared_prov`. C3 bars unchanged.
8. If C3 admits, set `c3_bit=1` and publish the `ClaimRec` as belief. If C3 rejects, `c3_bit=0`, record stays in the ledger/exhibit only.
9. Multi-clause percepts do not vote. Each clause is an independent admission in clause order. No cross-clause tie exists.

**Determinism:** total order on rules, clauses, and dictionary. Binary search on sorted producer ids. No clocks, no RNG, no map iteration. Canonicalization is a pure function of the bytes.

**Scaling:** time O(`percept_len` + clauses + log|producers| + |rules|). `|rules|` and `|producers|` are compiled constants, not stream length. Space per admission O(`percept_len`) exhibit + 64 B claim. Independent of stream length. Slice directory keeps each slice under the toolchain ceiling.

**Records:** `ClaimRec`, exhibit bytes, ledger line. Belief query API returns a claim only when `c3_bit==1` and `prov_derived!=UNK`.

### 3. Expected win

**M-attack** on the frozen attack tape, specifically GEN→EXT relabel, Declaration Fork, and forged authority. Causal story: those three attacks edit a *label*. CTG's gate input is the producer row and the structural token bits, so a relabeled payload hashes to a different exhibit but the same derived class as the true producer. Forged authority sets b6 and dies at R2 before C3. Correct-admit on the frozen admission tape should move only insofar as legitimate items were being carried by declarations rather than by producer identity; if the tape's good items have honest producer rows, RK-3' should stay inside the K3 band while attack catch rises.

### 4. How it could fail

- **Specific:** laundering *before* the producer stamp. If a generator can make G1 emit an EXT `producer_id`, CTG faithfully derives EXT and then helps the attacker by giving the lie a clean claim record. CTG assumes the stamp is inside the trust boundary.
- **Canonical collision:** two percepts that differ only by case or whitespace become one claim. An attacker plants the benign reading first; the hostile reading is an exhibit-only duplicate and never re-judged.
- **Silent field failure:** belief queries are correct, but a downstream reader still prefers `ExhibitArena`. The hostile sentence lives in the exhibit, deliberation quotes it, and every PAM metric stays green. The gate becomes a parallel ledger nobody consults.

### 5. Kill bars

- K1–K5 as frozen. Any false-admit on the frozen wrong set (12 TMB-5 + 9 CC1 pairs) kills. Superlinear per-admission cost kills. Non-termination kills. Byte divergence on 2× rerun kills. Correct-admit more than 5 points under 71.78% with no attack-catch gain is HOLD.
- **K-CTG-1:** On the frozen attack tape, if the catch rate on the GEN→EXT relabel subset is not strictly greater than C3-only on that same subset → KILL (core claim false).
- **K-CTG-2:** If any belief `ClaimRec` has a gate trace showing `declared_prov` was read by C3 or by rule match (instrumentation: zero the declaration, rerun, decision changes) → KILL.
- **K-CTG-3:** Fixture probe (deterministic, not part of the attack tape scoring): a percept whose canonical claim is benign and whose pre-canonical bytes contain a hostile sentence. If any belief query returns the hostile sentence → KILL.
- **K-CTG-4:** Declaration Fork item from the frozen attack tape admitted to belief → KILL, even if K-CTG-1's aggregate somehow passes.

### 6. Steelman against

The strongest reading is that CTG is a parser bolted in front of a one-line fix C3 already owes: *stop reading the declaration*. If C3's inputs already include `producer_id`, CTG duplicates FE2-style separation work and the surviving C3 repair, and the only new behavior is false-reject from a brittle grammar (ASCII casefold, `;` and `|`). That grammar is a new vulnerability surface: attackers will aim at canonical collisions and at the exhibit channel, which did not exist before. The simplicity argument is decisive if a build crew can flip C3's provenance input from declaration to producer row in a single function and pass K-CTG-2 without a second arena. The core claim is vacuous unless the test harness distinguishes belief-claim bytes from exhibit bytes; a harness that only logs admit/reject will report "CTG == C3" and the architecture will look alive while doing nothing. Finally, CTG concentrates risk in the producer stamp. A wrong stamp used to be one bad admission; under CTG it is a *derived* class that later mechanisms are told to trust more, not less. That is a vulnerability the current C3 path does not institutionalize.

---

## W9 — Corroboration Codec (CC)

### 1. Name + pitch

**Corroboration Codec.** Admission to belief is a compression fact, not a score. A claim is a fact iff its canonical key already exists in the store under a **different** `producer_id`, i.e. the deterministic encoding of the pair is one key plus a producer-set of cardinality ≥ 2. The first sighting is stored as a singleton exhibit, not as belief. A second sighting with a *different object* under the same subject+predicate is a contradiction and admits neither side. There is no ratio threshold and no M1 movement. Incompressibility is not an admit signal — noise is incompressible, and treating novelty as a reason to believe is how false-admits get in.

### 2. Mechanism sketch

**Sits:** a gate after a local canonicalizer (the W8 steps 2–4, inlined so this design builds alone) and beside C3. C3 is necessary but not sufficient for belief.

**State:**

- `KeyIndex`: sorted by `(subject_hash, predicate_id, object_hash)`, each node `{key, head_producer_slot, belief_bit:u8, claim_id}`.
- `ProducerSet`: for each key, a sorted vector of `{producer_id:u32, claim_id:u32}`.
- `SingletonArena`: claim bytes for keys whose producer-set size is 1. `belief_bit=0`.
- `ContradictionArena`: `{key_without_object, hash_a, hash_b, claim_a, claim_b}` written when objects disagree. Neither claim is belief.

**Procedure:**

1. Canonicalize; derive `producer_id` from the stamp. Compute the triple key.
2. Binary-search `KeyIndex`.
3. **Miss:** append a singleton node, `belief_bit=0`. Do not call this a correct-admit. Return QUARANTINE. C3 is not consulted for belief (it may be recorded as `c3_preview` for the ledger, and that preview cannot publish).
4. **Hit, same object, same producer_id:** exact duplicate. Write nothing new. Belief bit stays as it was. This is not a second witness.
5. **Hit, same object, new producer_id:** insert producer id into the sorted set (memmove; lowest id order). Run frozen C3 on **each** of the two claims independently. Publish both as belief only if **both** C3-pass and neither producer class is GEN. If either fails, leave `belief_bit=0` and write the reason. GEN never corroborates.
6. **Hit, same subject+predicate, different object:** write `ContradictionRec`. Force `belief_bit=0` on every key under that subject+predicate. Do not let C3 override the contradiction.
7. Ordering: one proposal that contains several clauses is processed in clause order. Two keys that contradict inside the same percept never publish.

**Determinism:** sort keys as unsigned integers, predicate as u16, producer ids ascending. Insertion position is the unique binary-search point; equal keys collapse. No clocks.

**Scaling:** per admission, binary search O(log N) plus a memmove of the producer-set (size = distinct producers for that key, not N) plus an O(N) memmove only if the key index itself is a flat sorted array. Flat memmove is **linear** in stream length, which K4 permits, but it is the wrong long-run shape. Implement the key index as a B-tree of fixed fanout 16 (fanout chosen as a page invariant: one node must fit in a single cache-line-multiple page of 256 B, not as a tunable admission parameter). Per-admission time then O(log N), space O(1) scratch. Decisions identical to the flat array. If a slice would pass 2^25 B, split by key range via `SliceDir`.

**What "compression" means operationally:** the codec emits `(key, sorted_producer_ids[])`. Belief is the predicate `producer_set.length >= 2` after step 5's C3 conjunction. No other compression statistic is consulted. A general-purpose compressor is deliberately not used: its ratio would be an unprincipled threshold and would admit fluent nonsense that happens to share n-grams with the store.

### 3. Expected win

**False-admit rate** and **M-attack**. A laundered claim, a Declaration Fork, and a forged-authority sentence are typically singletons or same-producer duplicates; they remain quarantined. Causal story: the frozen attack tape's forgeries do not have an independent second producer who would also say the same canonical object. Echoed true claims on the frozen admission tape do, so they still publish, and RK-3' should hold if the tape's correct admits are not themselves singletons. If they are singletons, correct-admit falls and K3 correctly HOLDs the design — that result is informative, not something to route around.

### 4. How it could fail

- **Specific:** Sybil corroboration. The attacker who can mint two `producer_id` rows of class EXT emits the lie twice. Cardinality ≥ 2 is then adversarially cheap. CC has no notion of producer *cost*.
- **Contradiction freeze:** an attacker who wants a true claim suppressed emits the same subject+predicate with a different object from any producer. Step 6 unpublishes the truth. This is a new censorship channel C3 does not have.
- **Silent:** quarantine is treated as "admitted enough" by a later organ that reads `SingletonArena`. Tape metrics, which query belief, stay clean. Also silent: the store ossifies. In the field every genuinely new true sentence waits forever; the frozen admission tape, being full of repeated items, never shows it.

### 5. Kill bars

- K1–K5.
- **K-CC-1:** Any belief record whose producer-set cardinality is < 2 → KILL.
- **K-CC-2:** Any belief record whose producer-set contains a GEN-class producer that was required to reach cardinality 2 → KILL.
- **K-CC-3:** Both sides of a contradiction present as belief → KILL.
- **K-CC-4:** On the frozen attack tape, if laundering-subset catch rate ≤ C3-only → KILL core claim.
- **K-CC-5:** If a preregistered single-producer true item (named in the design doc before the run, not taken from the frozen wrong set) is published as belief → KILL.

### 6. Steelman against

This is "require two sources" wearing a codec costume. C3's corroborated-revision repair already passed at 71.78% by dealing with corroboration; if its corroboration check is real, CC is a second implementation of the same predicate with a quarantine side store. The new vulnerabilities are worse than the duplicated check: Sybil producers defeat it completely, and the contradiction rule is a denial-of-belief primitive aimed at any subject the attacker is willing to speak about twice. The simplicity argument: add `distinct_ext_producers >= 2` as a conjunct in the existing C3 publish function and you have the decision without `SingletonArena`, without a B-tree, and without a new way to unpublish true claims. The core claim is partly untestable on the frozen admission tape if that tape does not annotate whether each correct admit is a first or second sighting — the crew can then move RK-3' by accidentally scoring quarantines as admits, which vacuously "saves" the design. Any scoring rule that counts quarantine as correct-admit kills the claim by definition and should be rejected up front.

---

## W10 — Negative-Knowledge Ledger (NKL)

### 1. Name + pitch

**Negative-Knowledge Ledger.** TNN keeps an explicit, queryable set of open questions, and that set is allowed to **veto** but never to **confirm**. A new claim that contradicts a filled gap, and whose derived provenance is not strictly stronger than the filler's, is blocked even when C3 would admit it. A claim that merely "fills a gap" is tagged when C3 already admits it; the tag does not flip a reject into an admit. This preserves the F5 lesson: block-only survived, confirm paths died. The core claim is that a structured model of ignorance catches contradiction-class attacks and makes "why did you admit X?" answerable as "it fills gap g" / "it was blocked because it contradicts gap g", without opening a side door around C3.

### 2. Mechanism sketch

**Sits:** after C3's bit is computed, before publish. Also writes at G1 when a proposal *is* a question or when W-style contradiction records appear. Standalone: NKL detects contradictions itself, it does not require W9.

**GapRec** (32 B): `gap_id:u32, domain_hash:u64, pred_id:u16, evidence_needed:u16, status:u8 {OPEN=0, FILLED=1, CONTRADICTED=2}, filler_claim:u32, filler_rank:u8, opener_claim:u32, _pad`.

Provenance rank, total, compiled, **not** an M1 parameter: EXT=4, DERIVED=3, REPORT=2, GEN=1, UNK=0. Higher integer is stronger. This is an order on an enum, not a calibrated threshold.

**Opening a gap** (the only writers):

1. A compiled `SeedGap` table, sorted by `gap_id`, shipped with the binary. Seeds are questions the program chooses to track (for example "authority token for producer P", "second producer for key K"). They are not mined from the frozen wrong set or the frozen admission tape.
2. A contradiction discovered at publish time: same `(domain_hash, pred_id)`, different `object_hash`, both otherwise well-formed. Opens one gap if none exists, status CONTRADICTED, and fills nothing.
3. A canonical "unknown" clause (predicate dictionary entry `UNKNOWN`) opens a gap whose `evidence_needed` is the feature mask in the seed schema for that predicate. It does not admit the unknown-clause as a fact.

**Procedure on an ordinary proposal:**

1. Canonicalize, derive rank from the producer row (same feature rules as CTG step 5, inlined).
2. Run frozen C3. Record `c3_bit`. NKL is not allowed to change a 0 into a 1.
3. Binary-search gaps by `(domain_hash, pred_id)`.
4. Walk matches in `gap_id` order.
5. **Veto:** if any FILLED gap has the same subject+predicate and a different object, and `new_rank <= filler_rank`, set publish=0 regardless of `c3_bit`. Reason code `VETO_GAP`. If `new_rank > filler_rank` and `c3_bit==1`, do **not** auto-replace the filler (that would be a confirm/revision path smuggled in). Write `ConflictRec` and leave the old filler. Revision stays C3's existing corroborated-revision job, untouched.
6. **Tag:** if `c3_bit==1` and an OPEN gap matches domain, predicate, and `evidence_needed ⊆ features`, set that gap FILLED, `filler_claim=this`, and write `gap_id` onto the claim. If several match, fill the lowest `gap_id` only; other matches stay OPEN.
7. If `c3_bit==0`, do not fill, do not admit, even if every gap in the store matches.

**Determinism:** seed gaps compiled in `gap_id` order; binary search; lowest `gap_id` wins the tag. Rank is a fixed enum order.

**Scaling:** O(log G + M) where G is gap count and M is the match run for one domain. Gaps grow when contradictions and seed-schema unknowns arrive, so G = O(N) worst case and a single hot domain could have M = O(N). That is linear, legal under K4, but a hot domain must not become quadratic. Store per-domain matches as their own sorted vector of gap ids (B-tree, same page invariant as W9) so a veto check is O(log G). Scratch O(1).

**Records:** `GapRec`, optional `ConflictRec`, ledger line `{claim_id, c3_bit, veto_bit, gap_id or 0}`.

### 3. Expected win

**M-attack** on items that contradict an already-filled structural gap (forged authority after a seed gap "token required" is filled by the real token; a second object laundered in). **M-introspection:** the ledger cites `gap_id` and either `TAG` or `VETO_GAP`. Causal story: C3 scores a claim locally; NKL adds one non-local bit that C3 does not have, namely "this object disagrees with a recorded open question that already has a stronger filler." Because the bit is veto-only, the frozen wrong set can only get safer, never newly admitted by NKL itself.

### 4. How it could fail

- **Specific:** gap poisoning. The attacker feeds `UNKNOWN` clauses or seed-shaped contradictions first, so the gap store records the attacker's question. Later a C3-passing lie matches it and receives a `TAG` that deliberation treats as extra authority. The tag was specified as non-causal for the gate and becomes causal in the reader. That is a laundering channel made of metadata.
- **Rank ossification:** a weakly true filler with rank EXT blocks a later, better-evidenced object of equal rank (equal rank vetoes). Truth that arrives second, from the same class, can never displace the first filler through NKL. Field knowledge sticks to whoever spoke first.
- **Silent:** seed gaps never match field predicates (schema drift). Veto count is zero, tags are zero, NKL is byte-identical to C3 on both tapes, and the extra arena still has to be trusted and stored.

### 5. Kill bars

- K1–K5.
- **K-NKL-1:** Any proposal with `c3_bit==0` published, or published because a gap matched → KILL (confirm path reborn).
- **K-NKL-2:** On a constructed deterministic probe shipped with the design (two claims, same subject+predicate, different objects, second rank ≤ first, both C3-pass): if the second is belief → KILL.
- **K-NKL-3:** If zero vetoes and zero tags fire on the frozen admission tape **and** the frozen attack tape → KILL core claim as unexercised. (A design that cannot be distinguished from C3 on the frozen fixtures is not a PAM result.)
- **K-NKL-4:** If any gap record was inserted by code that read the frozen wrong set or the frozen admission tape labels → KILL (fixture contamination).

### 6. Steelman against

NKL's only causal act is a contradiction veto, and a contradiction veto does not need a theory of ignorance. A 30-line "same subject+predicate, different object, block the weaker or equal newcomer" check inside C3 publish does that without gaps, seeds, or tags. The tag path is worse than useless: it is a new prestige bit. Attackers who cannot beat C3 will farm tags, and any conscious consumer (Part B) will eventually treat `gap_id != 0` as a reason to believe — a confirm path that K-NKL-1 does not see because the *gate* bit never flipped. Seed gaps are an arbitrary ontology dressed as structure; if they are not fitted to the fixtures they will not fire (K-NKL-3), and if they are fitted the result is contaminated (K-NKL-4). So the design is squeezed between vacuity and cheating. The ignorance model is also a regress: a gap is itself an admitted object. Who admitted the seed? The answer "the programmers did, in the binary" means NKL smuggles a hand-written prior that the program then calls negative knowledge. That prior can be wrong, and unlike a bad C3 admit it vetoes the correction (equal-rank freeze). The strongest simplicity argument: do not build it until a measured C3 miss on the frozen attack tape is shown to be a cross-claim contradiction rather than a local provenance error. If the misses are local, NKL cannot move M-attack and will only add a ledger.

---

## W11 — Admission Futures (AF)

### 1. Name + pitch

**Admission Futures.** Nothing becomes belief at perception time. A proposal is publishable only together with a prediction whose expected payload **covers the object bytes of the claim**, and it stays provisional until a later percept in the stream settles that prediction. Settlement is event-driven, not clock-driven and not "after N items." A settled-true claim is then submitted to frozen C3; C3 still has veto. A settled-false claim is revoked and the revocation is a first-class record. The epistemic claim is: an admission that the proposer will not stake a checkable consequence on is not yet a candidate for belief.

### 2. Mechanism sketch

**Sits:** wraps publish. G1 must attach a future or the proposal can only be stored as an unstaked exhibit (not belief, not provisional-eligible).

**FutureRec** (48 B): `future_id:u32, claim_id:u32, observable_key:u64, expected_hash:u64, object_hash:u64, open_index:u32, status:u8 {OPEN, TRUE, FALSE}, settler_id:u32, _pad`.

`expected_hash` must equal FNV-1a(canonical object bytes concatenated with observable key bytes). A future that hashes only the key, or only a constant, fails the cover check at insert time and does not open.

**No deadline field.** Open futures live until a matching observable arrives or physical memory fail-closes new provisionals. Evicting an old unsettled future by age would be an arbitrary limit and would also be a clock-like policy; it is forbidden. Fail-closed at the arena limit is the policy.

**Procedure:**

1. On proposal: canonicalize the claim. If no future is attached, or the cover check fails, write exhibit-only and stop. Do not call this a reject of a *fact*; call it `UNSTAKED`. It is not belief.
2. Assign `future_id` = current count (monotonic). Insert into `FutureByKey`, a B-tree sorted by `(observable_key, future_id)`. Status OPEN. Claim status PROVISIONAL. Belief queries skip it.
3. On every subsequent proposal, **before** its own admission decision, extract its observable keys (the subject hash of each clause, in clause order — the observable is the subject, the settlement payload is the object).
4. For each key, find the equal-key range in `FutureByKey` and walk it in `future_id` order.
5. If the arriving object's hash equals `expected_hash` **and** the settler's `producer_id` ≠ the future's opener `producer_id` **and** the settler's class ≠ GEN: status=TRUE, then run frozen C3 on the provisional claim plus the settler id as corroboration exhibit. C3 admit → BELIEF. C3 reject → leave status TRUE but belief_bit=0 (`SETTLED_BUT_BLOCKED`). The settler is not auto-believed by this step; it goes through its own admission.
6. If the key matches and the object hash differs: status=FALSE. Write `RevocationRec {future_id, claim_id, settler_claim}`. Belief bit stays 0. The provisional can never be reopened by a later match (first settler in `future_id` order wins; later settlers append a `LateSettlerRec` that does not flip status).
7. A provisional is not visible to corroboration cardinality in W9 if both are built; the interface contract is `belief_bit`.

**Determinism:** `future_id` order is a total order. First settler wins because lower ids were opened earlier in the same fixed stream. No wall clock: `open_index` is the stream cursor, recorded for audit, never compared against a timeout.

**Scaling:** per admission O(K log F) where K is the number of clauses in the percept and F the number of open futures. K is input size. F grows O(N). Log is required, so the index is a B-tree, not a scan. A scan of all open futures per admission would be linear and legal but would hide an easy superlinear bug if someone nests it; the sketch forbids the scan. Scratch O(K).

**Toolchain:** `FutureByKey` nodes spill via `SliceDir` under the 2^25 ceiling.

### 3. Expected win

**False-admit rate** on the frozen wrong set and **M-attack**. Causal story: forged authority and laundered claims can be stamped and declared, but they cannot force a later independent producer to emit the predicted object. They sit forever as PROVISIONAL and do not count as admits. If the frozen admission tape contains later independent percepts that really do bear the same object, true claims still reach belief and RK-3' measures *eventual* belief within the tape, which must be the preregistered reading of correct-admit for this design (immediate publish is defined as failure, not success).

### 4. How it could fail

- **Specific:** self-fulfilling stake. The attacker emits the claim-with-future and, later, the settling percept from a second producer they also control. The cover check passes, C3 sees two producers, and AF has become W9 with extra steps. If the attacker does not have a second producer, they instead emit a settler that is itself only PROVISIONAL — the sketch refuses that (settler must be a distinct producer), but a bug that lets an unsettled settler count will silently restore single-source belief.
- **Vacuous observables:** if "object bytes" are attacker-chosen padding that both messages share, while the human-readable difference sits in a non-canonical field, the future settles without confirming anything that matters.
- **Silent:** consumers read PROVISIONAL. Belief metrics look strict; behavior follows the quarantine. Also silent on this tape specifically: if the frozen admission tape has no paired later settler for its good items, correct-admit collapses below the K3 line and the design HOLDs without ever being distinguished from "admit nothing."

### 5. Kill bars

- K1–K5. For K3, correct-admit counts only BELIEF status at end of tape, not PROVISIONAL.
- **K-AF-1:** Any BELIEF record whose future is not TRUE, or whose settler producer equals the opener or is GEN → KILL.
- **K-AF-2:** A future whose `expected_hash` does not change when the object bytes change is insertable → KILL (cover check broken).
- **K-AF-3:** On the frozen attack tape, any forged-authority or GEN→EXT item reaches BELIEF → KILL.
- **K-AF-4:** If the end-of-tape BELIEF count on the frozen admission tape is 0 → KILL core claim as degenerate (the design admits nothing and cannot be compared). If it is >0 but more than 5 points under 71.78% and attack catch is not better than C3 → HOLD per K3.
- **K-AF-5:** Status of a future depends on wall-clock, or a timeout field exists in `FutureRec` and is read → KILL (program law).

### 6. Steelman against

AF is W9 plus a coupon. The second producer is doing all the work; the prediction record is ceremony unless the tape contains genuine outcome events that are not just "someone else said the same sentence." The frozen admission tape was not built as a prediction market. The likely measured outcome is K-AF-4 degenerate or a K3 HOLD, and the crew will have spent a build on a gate that cannot legally score a win on the fixtures that exist. The new vulnerabilities are real: Sybil settlement, vacuous covered hashes, and a provisional store that will be wired into deliberation because it is where all the fresh content sits. There is a regress the design does not close: the settler is admitted by some *other* path (it "goes through its own admission"), so either settlers are themselves futures (infinite regress, nothing ever settles) or settlers are privileged raw admits (a side door). The sketch picks the side door and then pretends belief is future-gated. The strongest simplicity argument: if the actual invariant is "no belief without an independent second EXT producer and a C3 pass," write that invariant and delete futures, deadlines, and settlement status. The distinctive claim — that the *act of predicting* filters bad content — is untestable here, because a proposer can attach a correct prediction to a false claim and an incorrect prediction to a true one. Settlement checks the prediction, not the truth of the claim, except insofar as the hash was defined to *be* the claim. Once the hash is the claim, the word "prediction" is a synonym for "please repeat this string," and AF collapses into duplicate detection.

---

## W12 — Epistemic-Type Binding (ETB)

### 1. Name + pitch

**Epistemic-Type Binding.** Every surviving proposal is written into exactly one typed arena — FACT, HYPOTHESIS, REPORT, or FICTION — by a total-order rule list. Belief queries read FACT only. The standing failure mode this is aimed at is not a bad threshold; it is a missing type: TNN currently has one store, so a report, a generated continuation, and an observed fact become the same kind of object the moment they pass C3. ETB's core claim is that a large fraction of frozen-attack-tape successes are type errors (fiction or report treated as fact, authority *claimed in the sentence* treated as authority *of the sentence*), and that separating the stores drops those without a new confirm path.

### 2. Mechanism sketch

**Sits:** immediately after C3 and provenance derivation, instead of a single publish bit. C3 remains a filter inside the FACT and HYPOTHESIS rules. C3 cannot promote FICTION or a report-payload into FACT.

**Arenas:** four append-only claim arenas plus `TypeLedger {claim_id:u32, type:u8, rule_id:u16, producer_id:u32}`.

**Type rules, compiled, first match in this exact order:**

1. **R-FIC** (`rule_id=1`): producer class GEN, or G1 structural fiction-mark bit set → FICTION. Stop. C3 not consulted. Not FACT.
2. **R-REP** (`rule_id=2`): producer class REPORT, or predicate_id ∈ compiled speech-predicate list (`says`, `claims`, `reports` — dictionary ids, sorted) → write a FACT only of the *attribution wrapper* `(producer_id, speech_predicate, payload_hash)` if that wrapper itself passes C3; write the payload bytes into the REPORT arena with `fact_bit=0`. A query for the payload's bare proposition returns empty.
3. **R-AUTH** (`rule_id=3`): authority-claim bit set and producer auth token is 0 → REJECT. No arena. (Block-only.)
4. **R-FACT** (`rule_id=4`): class EXT, C3 pass, and `KeyIndex` already holds the same object under a different EXT producer → FACT.
5. **R-HYP** (`rule_id=5`): class EXT, C3 pass, no such corroborator → HYPOTHESIS. Not returned by belief queries.
6. **R-REJ** (`rule_id=6`): else REJECT.

**Procedure:** canonicalize (inlined), derive class from the producer row, compute the six predicates above in order, write exactly one ledger line, append to at most one content arena plus possibly the attribution wrapper from R-REP.

**Determinism:** rule order is the tie-break. There is no voting between types. Speech-predicate dictionary is sorted and compiled. Same bytes and same store ⇒ same rule_id.

**Scaling:** O(log N) for the corroboration lookup (B-tree as in W9) plus O(percept) canonicalize. Four arenas grow O(N) total, which is the store itself, not per-admission superlinear scratch.

**Belief API contract (part of the design, tested):** `belief_get` reads FACT only. `hypothesis_get`, `report_get`, `fiction_get` are separate entry points. A test that calls `belief_get` on a payload whose only home is REPORT must get a miss.

### 3. Expected win

**M-attack** and **M-judgment false-admit**, with a deliberate risk to correct-admit. Causal story: forged authority dies at R-AUTH before FACT. GEN→EXT relabel still carries class GEN if the stamp is honest, so R-FIC fires and the launder never reaches FACT. Declaration Fork changes `declared_prov` only, which no rule reads. Reports stop being facts. The frozen wrong set should stay clean (K1) if those items are uncorroborated, generated, or authority-forged. Correct-admit on the frozen admission tape falls if many tape-positive items are single-source; they become HYPOTHESIS and do not score. That is an honest K3 HOLD unless attack catch rises enough that the program accepts the trade. The design's claim is the trade itself, not a free increase in RK-3'.

### 4. How it could fail

- **Specific:** attribution laundering. R-REP writes a C3-passing FACT wrapper "P claims payload." Deliberation retrieves the wrapper, drops the predicate, and treats the payload as fact. The type system held inside ETB and failed at the first consumer. This is the designed-in hole: the wrapper *is* a fact about an event of speech, and speech events are exactly how lies enter agents.
- **Sybil FACT:** two EXT stamps, R-FACT fires, same failure as W9.
- **Silent:** FACT arena is nearly empty on the real stream, so a well-meaning reader points `belief_get` at HYPOTHESIS "temporarily." Metrics that use the typed API stay excellent. The program has reintroduced one store through a config flag.

### 5. Kill bars

- K1–K5. Correct-admit for K3 is FACT-arena hits only, against the frozen admission tape's correct-admit denominator. The denominator does not get redefined to include hypotheses.
- **K-ETB-1:** GEN-class or fiction-marked item present in FACT → KILL.
- **K-ETB-2:** Any forged-authority item from the frozen attack tape present in FACT → KILL.
- **K-ETB-3:** `belief_get(payload)` hits for an item that rule R-REP stored → KILL.
- **K-ETB-4:** Type changes when `declared_prov` is flipped and producer row is held fixed (2× rerun with declaration mutated) → KILL.
- **K-ETB-5:** If FACT-arena catch behavior on the frozen attack tape equals untyped C3 publish → KILL core claim (types did no work).

### 6. Steelman against

ETB multiplies stores and the bug will be in the router, not the rule list. The rules themselves are a priority cascade of checks that each belong, if anywhere, inside C3: drop GEN, drop tokenless authority, require a second EXT producer, and stop storing "P says Q" as Q. Four arenas give operators four chances to read the wrong one, and the steelman prediction is that HYPOTHESIS becomes the de facto belief store within one iteration because FACT is too empty to be useful — K3 will HOLD the design, and the response will be to widen R-FACT until ETB *is* C3. The wrapper-fact hole is not a corner case; it is the main path for reported content, which is most content. The ontology (fact / hypothesis / report / fiction) is a philosophy seminar encoded as a u8. The frozen tapes do not label types, so "correct type" has no ground truth; the only measurable claim is "FACT is a subset of what C3 would have published." That claim is testable but small, and it is satisfied by any extra conjunct. The strongest simplicity argument: one extra publish conjunct (`EXT ∧ second_producer ∧ ¬authority_forged`) and one storage rule (`speech predicates store the wrapper`) beat four arenas. If the crew cannot state a question the typed API answers that a single bit `is_fact` would not, the architecture is unfalsifiable decoration and should not be built.

---

## W13 — Deterministic Immune Repertoire (DIR)

### 1. Name + pitch

**Deterministic Immune Repertoire.** A compiled set of receptors, each a mask and a pattern over a fixed structural feature word, can veto a proposal before publish. Full match (every masked bit agrees) vetoes. Partial match does nothing. There is no random clonal selection and no affinity threshold: the only scores are integer popcounts used later for maturation accounting, and v1's decision is full-match or not. Maturation, if enabled, enumerates single-bit edits in bit-index order against a **settlement log**, never against the frozen wrong set or the frozen admission tape. v1 ships with maturation **off** and a frozen receptor table, because a learning immune system trained on the kill-bar fixtures would be a fake pass. DIR is block-only. It cannot admit what C3 rejects.

### 2. Mechanism sketch

**Feature inventory v1** (16 bits; width *is* the inventory, not a cap — growing it is a new preregistered inventory version that replays old bits in the same positions):

| Bit | Meaning |
|---|---|
| 0 | declaration class ≠ producer class |
| 1 | sensor envelope absent |
| 2 | authority claim in payload, token absent |
| 3 | GEN trace / class GEN |
| 4 | canonical parse failed |
| 5 | speech predicate |
| 6 | fiction-mark |
| 7 | producer row missing |
| 8 | object contradicts a BELIEF key (lookup) |
| 9 | same payload hash previously stored with a different declaration |
| 10 | evidence-ref count is 0 |
| 11 | only citations are self-producer |
| 12 | payload contains a wall-clock *claim* (digit-pattern scan; the scan does not read the clock) |
| 13 | duplicate of an OPEN rejection with reason provenance or authority |
| 14 | second clause in the same percept contradicts the first |
| 15 | producer class UNK |

**ReceptorRec** (8 B): `receptor_id:u16, mask:u16, pattern:u16, enabled:u8, _pad`. Compiled, sorted by `receptor_id`.

v1 receptors (hand-specified, not fitted):

- id 1: mask=bit2, pattern=bit2 → veto tokenless authority
- id 2: mask=bit0|bit3, pattern=bit0|bit3 → veto GEN wearing a foreign declaration
- id 3: mask=bit7, pattern=bit7 → veto missing producer
- id 4: mask=bit4, pattern=bit4 → veto parse fail
- id 5: mask=bit6, pattern=bit6 → veto fiction-mark

**Decision procedure:**

1. Extract bits 0–15 in index order. Bit 8 and bit 13 do store lookups (O(log N)); all others are local.
2. Scan receptors by ascending `receptor_id`.
3. A receptor hits iff `(features & mask) == (pattern & mask)` and `mask != 0` and `enabled==1`.
4. First hit vetoes. Ledger records `receptor_id`. C3 is not called. Publish=0.
5. No hit: fall through to frozen C3 unchanged. DIR does not modify C3's inputs.

**Maturation (off unless a separate preregistered experiment enables it):** input is the AF settlement log or an explicit `RevocationRec` stream produced in-run, never fixture labels. For each failure in `failure_id` order, let F be its feature word. For each enabled receptor, for bit b from 0 to 15: propose `mask' = mask OR (1<<b)`, `pattern' = (pattern & ~bit) | (F & bit)`. Accept the first proposal in that enumeration that increases `sep = score(F, receptor) - max score over the compiled BenignAnchor list`, where `score` is the count of agreeing masked bits. If none increase `sep`, change nothing. Append the new receptor with the next `receptor_id` (old ids stable). **BenignAnchor is a compiled list shipped with the design, disjoint from the frozen wrong set, the frozen admission tape, and the frozen attack tape.** If a mutation would veto any anchor, reject that mutation.

**Determinism:** bit order, receptor_id order, failure_id order, first accepted mutation only. No sampling.

**Scaling:** v1 is O(1) receptors and O(log N) for bits 8 and 13. With maturation, receptor count R grows at most one per failure, scan is O(R) = O(N), which is linear, permitted, and the reason v1 defaults maturation off. Enabling maturation requires the B-tree-free scan to stay a single pass with no nested stream loops (superlinear would be K4). Physical memory fail-closes further mutation; existing receptors keep vetoing.

### 3. Expected win

**M-attack**, narrowly, on items whose structure matches v1 receptors: declaration/producer mismatch with GEN trace, tokenless authority, missing producer. Causal story: these are exactly the frozen attack tape's three families if and only if the attacks are visible in the feature word. DIR then vetoes before C3, so catch rate rises on any attack C3 currently lets through that carries those bits. It should not change decisions on clean EXT corroborated items, so RK-3' should hold. The win is falsifiable precisely because the receptors are few and named: if the attack tape's successful attacks do not set these bits, DIR does nothing and K-DIR-3 kills it.

### 4. How it could fail

- **Specific:** mimicry. The attacker reads the 16-bit inventory (it is in the binary) and crafts laundering that sets none of the masked bits: honest-looking producer row, no authority word, no fiction mark, valid canonical form, and the lie sitting entirely in the object field. Every receptor misses. DIR is blind to semantic falsehood by construction.
- **Autoimmunity if maturation is turned on:** a poisoned revocation log (attacker causes SETTLED_FALSE on true claims, or a bug marks them so) walks bits toward the attacker's feature profile and starts vetoing anchors. K-DIR-4 is there because this *will* be tried.
- **Silent:** receptors never full-match on the field distribution (too specific). DIR equals C3, the ledger shows a long run of "no receptor," and the build is reported as defense-in-depth.

### 5. Kill bars

- K1–K5.
- **K-DIR-1:** A receptor hit co-occurs with a publish, or DIR publishes anything C3 rejected → KILL.
- **K-DIR-2:** Any code path reads frozen wrong set, frozen admission tape, or frozen attack tape labels into receptor construction or maturation → KILL.
- **K-DIR-3:** v1 catch rate on the frozen attack tape ≤ C3-only → KILL core claim.
- **K-DIR-4:** Any compiled BenignAnchor vetoed, including after a maturation experiment → KILL that experiment and revert receptors to the compiled v1 table.
- **K-DIR-5:** Permuting the scan so a higher `receptor_id` is tested first changes which id is logged on a double-hit probe → KILL (order bug). The *veto bit* may still be the same; the logged id must be the lowest.

### 6. Steelman against

An immune system whose decision is "if these five boolean conditions, veto" is five if-statements. The biological vocabulary (receptor, clone, affinity maturation) is doing marketing work that will justify maturation, and maturation is the only part that can hurt: it is a deterministic optimizer aimed at a log the attacker can influence, with a 16-bit search space small enough to overfit and large enough to veto innocents. v1 without maturation should not be reviewed as an architecture; it should be reviewed as a patch to C3's precondition list, which is where mask/pattern pairs go to stop being a second interpreter. The new vulnerability is feature-inventory disclosure: once bits are named, the attacker's job is to avoid them, and a veto-only prefilter trains the attacker on exactly which surface forms are safe. C3, being a single gate, at least does not publish a second, simpler spec of what it ignores. The core claim is close to vacuous if K-DIR-3 passes only because the receptors were written while looking at the attack tape's narrative description (GEN→EXT, forged authority) even without loading the bytes — that is still fitting, just done by the author of this section. The honest expectation is K-DIR-3: C3 already rejects the crude forms of those attacks, and the residuals are semantic, which popcount receptors cannot see. If that expectation is right, building DIR is a way to spend a round rediscovering that deny-lists are not understanding.

---

## W14 — Two-Phase Commit (TPC)

### 1. Name + pitch

**Two-Phase Commit.** The fast path computes a local intent (schema, producer row, frozen C3 on local features) and writes an `IntentRec`. It does not publish. The slow path recomputes the feature hash from the bytes, repeats C3, and adds store lookups (contradiction, duplicate-declaration). A belief commit happens only when both bits are 1 and the feature hashes match. Disagreement writes a `DivergenceRec` and commits nothing. This is not two opposed voters (that is W2) and not a debate (W6). It is a commit barrier against torn decisions: belief is never visible on a local pass that the store-aware pass has not confirmed, and any future bug that makes one path consult the declaration shows up as a hash split instead of as a silent admit.

### 2. Mechanism sketch

**IntentRec** (24 B): `proposal_id:u32, fast_bit:u8, feature_hash:u64, producer_id:u32, clause_index:u16, _pad`.

**CommitRec** (16 B): `proposal_id:u32, slow_bit:u8, feature_hash:u64, committed:u8`.

**DivergenceRec** (16 B): `proposal_id:u32, fast_bit:u8, slow_bit:u8, fast_hash:u64` truncated into the layout actually as two u64s in a 32 B record: `{proposal_id:u32, fast_bit:u8, slow_bit:u8, reason:u16, fast_hash:u64, slow_hash:u64}`.

**Fast path** (runs at G1 handoff, no store dependency except the compiled producer table):

1. Canonicalize.
2. Pack the local feature word (all bits that do not require the store: inventory bits 0–7, 10–12, 15).
3. `feature_hash` = FNV-1a over the feature word **and** the canonical clause bytes.
4. `fast_bit` = frozen C3 on those local features.
5. Append `IntentRec`. Do not set belief.

**Slow path** (runs before any belief publish, still inside the same admission, synchronously — "slow" means store-aware, not asynchronous, not clocked):

1. Recompute canonical bytes and `feature_hash` from the exhibit. If it differs from the intent hash → `DivergenceRec` reason `HASH`, commit=0.
2. Compute store bits (contradiction against BELIEF, duplicate payload with different declaration).
3. `slow_bit` = 0 if a store bit vetoes, else frozen C3 on the full feature word.
4. Commit iff `fast_bit==1 && slow_bit==1 && hashes equal`.
5. If bits differ → `DivergenceRec` reason `BIT`, commit=0. The fast admit is dropped, not queued for later. There is no background reconciler (a background pass would invite a second scheduler and a nondeterministic "eventually").

**Determinism:** one proposal, one ordered slow pass, clause order. Synchronous, so rerun has no interleaving. C3 is a pure function; given equal features it must return the same bit (this is an explicit assumption TPC exists to audit).

**Scaling:** fast O(percept). Slow O(percept + log N) for two B-tree probes. No per-admission structure that grows with N except the append of one intent and one commit. Intents are not re-scanned on later admissions.

### 3. Expected win

This one does **not** claim a large M-attack jump on a correct build. The causal story is narrower and more honest: TPC moves **integrity and debuggability**, and it moves M-attack only when the fast path and the slow path can disagree on features that attacks manipulate (declaration-sensitive bug in one path). On a correct C3, `fast_bit` and `slow_bit` diverge only when store vetoes fire, which means TPC's real decision change versus C3-local is the store veto — i.e. contradiction and declaration-duplication, which should catch a slice of Declaration Fork and replayed laundering. The divergence log is the introspection substrate: a commit cites both bits and both hashes.

### 4. How it could fail

- **Specific:** correlated failure. Both paths call the same C3 and the same producer table. An attack that is legal under those shared inputs is admitted twice, with a comforting `DivergenceRec` count of zero. TPC is blind to any bug it shares with itself.
- **Hash theater:** `feature_hash` covers bytes the gate does not use, so it can match while a *third* copy of the feature word inside C3 still reads the declaration. Agreement of the two hashes does not prove C3's internal input vector.
- **Silent:** divergence stays zero in the field because both paths are equally wrong, and the commit barrier adds latency (M-speed) with no M-attack delta. The tape looks "consistent." Consistency of a bad decision is the failure mode.

### 5. Kill bars

- K1–K5.
- **K-TPC-1:** A BELIEF commit with `slow_bit==0` or with unequal hashes → KILL.
- **K-TPC-2:** Deterministic fault-injection probe, compiled into the test and not drawn from the frozen tapes: flip one local feature bit on the fast path only. If no `DivergenceRec` is produced → KILL. (This is the probe that makes the core claim measurable. If the crew will not ship the probe, do not build TPC.)
- **K-TPC-3:** On the frozen attack tape, catch rate < C3-only → KILL (the store veto made things worse). Catch rate == C3-only is not by itself a kill if K-TPC-2 passes; it is recorded as "no attack gain" in the Pareto table. Catch rate == C3-only **and** K-TPC-2 not run → KILL as untested.
- **K-TPC-4:** Slow path performs a scan over all prior intents → KILL under K4 (that bug is the obvious way this design goes superlinear).

### 6. Steelman against

TPC is a test harness that wants to ship. Running a pure function twice and comparing notes catches implementation accidents; it does not catch attacks, because attackers present one byte string, not two disagreeing ones. The frozen attack tape will show catch rate == C3 plus whatever store veto was quietly added, and that store veto should be proposed as itself rather than hidden inside a commit protocol. The new vulnerability is operational: two code paths will drift. A "temporary" fast publish will be added for latency, the barrier will be bypassed, and intents will be read as belief — the same quarantine leak as AF and CC. Cost is nearly 2× C3 cycles for a gain that a single path with an assertion (`debug_assert feature_hash recomputed`) gets in test builds only. Program law does not require the assertion to ship in the decision path. The core claim is untestable on the frozen fixtures alone, which is why K-TPC-2 has to invent a probe the round did not freeze. A design whose kill bar requires a fixture the program does not have is a design arguing for its own unfalsifiability. If the probe is the real experiment, run the probe against C3 as a unit test and do not call it a PAM.

---

## W15 — Triggered Rejection Re-adjudication (TRR)

### 1. Name + pitch

**Triggered Rejection Re-adjudication.** Rejections are stored as data, not discarded, and are reconsidered only when a later **belief** commit shares their subject hash. There is no periodic schedule (a period would be an arbitrary limit) and no retention guard (MG6 stays dead: this does not protect already-admitted items from eviction; it reconsiders items that were never admitted). Promotion is allowed for exactly one reason code, `SINGLETON`, and only when a later independent EXT belief supplies the missing second producer and frozen C3 passes on the stored features. Provenance failures, authority failures, parse failures, and fiction never promote. The core claim is that a measurable part of the gap between C3's 71.78% and a higher correct-admit rate is false-reject of first sightings that the tape later corroborates, and that those can be recovered without re-opening the attack classes MG6-style retention logic kept letting back in.

### 2. Mechanism sketch

**RejectionRec** (40 B): `rej_id:u32, subject_hash:u64, predicate_id:u16, object_hash:u64, producer_id:u32, reason:u16, feature_word:u16, status:u8 {OPEN, UPHELD, PROMOTED}, claim_id:u32`.

`reason` enum, compiled: `SINGLETON=1, PROV_MISMATCH=2, AUTH_FAIL=3, PARSE_FAIL=4, FICTION=5, C3_REJECT=6, CONTRADICTION=7, UNSTAKED=8`. **Allow-promote set = {SINGLETON} only.**

**Index:** B-tree of OPEN rejections sorted by `(subject_hash, rej_id)`.

**Procedure:**

1. Whenever any upstream gate (C3, or CTG/CC/ETB if composed) rejects, append `RejectionRec` with the reason from a fixed priority: if multiple reasons apply, the **lowest** enum value that is *not* SINGLETON wins over SINGLETON (so a singleton that is also a provenance mismatch is stored as PROV_MISMATCH and can never promote). SINGLETON is recorded only when it is the sole reason.
2. On a transition into BELIEF of claim C (the trigger — not a timer): binary-search `subject_hash`.
3. Walk the equal-subject OPEN range in `rej_id` order.
4. For each: if `reason != SINGLETON` → set UPHELD, continue. If predicate or object differs → leave OPEN (different claim), continue. If same key and `C.producer_id` differs and `C`'s class is EXT and rejection's producer class is EXT: re-run frozen C3 on the **stored** `feature_word` plus a corroboration bit. If C3 passes, status=PROMOTED and publish the rejected claim as belief, citing `C.claim_id` as the trigger. If C3 fails, status=UPHELD.
5. A promotion is itself a belief commit and may trigger further TRR walks. **Termination:** a rejection is removed from the OPEN index before the walk continues, and a claim id already processed in this cascade is skipped via a per-cascade sorted id list. Cascade depth is bounded by the number of OPEN rejections sharing that subject, which is finite because each step removes one OPEN row. No rejection is appended inside the cascade (appends happen only on rejects). So the cascade ends.
6. Do not re-adjudicate on provisional, hypothesis, fiction, or report writes. Trigger is BELIEF only.

**Determinism:** `rej_id` order, reason priority total order, cascade skips lowest claim id already seen. Same stream ⇒ same promotions.

**Scaling:** reject path O(log R) insert. Trigger path O(log R + M) for M open rejections of that subject. Worst-case M = O(N) for one hot subject, linear, permitted. Page-sized B-tree keeps the common case O(log R). Scratch for the cascade is one sorted vector of touched ids, O(M) and freed at end of cascade. Not retained.

**Distinction from MG6:** no admitted belief is pinned, refreshed, or guarded. The only new publishes are prior rejects. If a reviewer cannot point at a `RejectionRec` that changed status, TRR did not act.

### 3. Expected win

**Correct-admit rate** on the frozen admission tape, from a base of 71.78%, by recovering SINGLETON false-rejects that a later tape item corroborates. Causal story: C3's corroborated-revision repair helps items that are revised while being considered; it does not walk back to an item already rejected and stored nowhere. TRR is that walk, with the allow-list as the safety constraint. M-attack should not fall, because attack reasons are not in the allow-promote set: a laundered item rejected as PROV_MISMATCH stays UPHELD even if a later belief shares its subject.

### 4. How it could fail

- **Specific:** reason laundering. If the reject path records SINGLETON when PROV_MISMATCH also applied (priority bug, or an upstream gate that only reports its last reason), the attacker's first copy waits in OPEN until a Sybil belief triggers promotion. TRR then admits the launder *because* it was rejected. The allow-list becomes the bug.
- **Cascade contamination:** a promoted singleton is belief, which triggers more promotions under the same subject, including ones that matched only the subject hash and a too-loose key compare. One bad trigger publishes a family.
- **Silent:** allow-list is so tight that no rejection on the frozen admission tape is SINGLETON-only. Promotion count is zero, correct-admit unchanged, TRR is a pure cost. The field version meanwhile stores every reject forever, and physical memory fail-closes **new** admissions because the rejection archive filled the arena — a safety feature that presents as a liveness failure far from the tape's length.

### 5. Kill bars

- K1–K5. A promotion that lands on the frozen wrong set is K1.
- **K-TRR-1:** Any PROMOTED record whose stored reason ≠ SINGLETON → KILL.
- **K-TRR-2:** Any frozen-attack-tape item (laundering, Declaration Fork, forged authority) ends PROMOTED or BELIEF via TRR → KILL.
- **K-TRR-3:** A promotion occurs without a BELIEF trigger whose `(subject, predicate, object)` equals the rejection and whose producer differs → KILL.
- **K-TRR-4:** If the cascade can re-open a non-OPEN rejection or can fail to terminate on a fixture with ≥2 same-subject rejects → KILL (K5 specialized).
- **K-TRR-5:** If promotions on the frozen admission tape do not raise correct-admit **and** do not keep K1 at zero → HOLD if promotions are zero (unexercised); KILL if promotions are nonzero and correct-admit does not rise (promotions are pure risk). Zero promotions is HOLD, not a pass.

### 6. Steelman against

TRR reopens the door the rest of this round tries to shut, and it does it in the name of the metric the program is already tempted to chase (correct-admit above 71.78%). The attacker does not need a new exploit if they can get their first attempt classified as SINGLETON. Reason codes will be wrong sometimes; the design turns "wrong reason code" from a logging defect into a belief defect. That is a new vulnerability no current gate has, because today a reject is the end of that item. MG6 was killed six ways because retention logic keeps finding a path back in; TRR is retention of *rejections* with a promote bit, and the steelman prediction is that build crews will widen the allow-promote set the first time a PROV_MISMATCH reject looks, in a postmortem, like it "should have made it." Widening that set is how K-TRR-2 will eventually fail. The simplicity argument: when the second witness arrives, admit the **second** witness (C3 already can) and leave the first rejected. The content is the same; the only thing recovered by promoting the first is an earlier timestamp and the original attacker's wording. Paying a permanent archive of every reject, plus a cascade, in order to republish wording the second witness already restated, is a bad trade. The core claim is likely unexercised on the frozen admission tape (K-TRR-5 HOLD): the tape's rejects may not be singleton-then-corroborated pairs. If so, TRR cannot be shown to work here, and building it is an untested side door. Do not widen the allow-list to make the tape move. That is fitting.

---

# PART B — CONSCIOUS vs UNCONSCIOUS PAM

Frozen definitions, used literally:

- **Conscious:** every PAM decision emits a deliberation-visible record (what fired, which rule, evidence cited), queryable by TNN's own deliberation.
- **Unconscious:** binary outcome only, no per-decision record.

Comparison is one Pareto table over M-speed, M-resource, M-judgment, M-attack, M-introspection, on the same frozen admission tape and frozen attack tape. No single winner is declared in the metrics; a winner appears only as the output of the preregistered decision rule in B.6.

### B.1 Cost model of consciousness

A conscious record is not a copy of the percept. The percept is already in an exhibit arena under either design. The incremental object is a **decision record**:

```
DecRec (32 B fixed + 4 B × evidence_ids):
  claim_id:u32, rule_id:u16, receptor_or_type:u16,
  feature_word:u16, c3_bit:u8, veto_bit:u8,
  prov_derived:u8, reason:u8,
  evidence_count:u16, evidence_ids[evidence_count]:u32
```

Order-of-magnitude, per admission, relative to an unconscious path that already writes the claim or the reject (about 40–64 B plus exhibit):

| Term | Unconscious | Conscious (no ablation) | Conscious + ablation |
|---|---|---|---|
| Extra bytes | 0–1 outcome byte | ~32 + 4E, E≤8 → ~64 B | same, plus E counterfactual bits |
| Extra cycles | 0 | one struct store, O(E) | E additional pure re-runs of the gate |
| Deliberation entries | none | 1 indexable record | 1 record + E ablation notes |
| Attention | 0 | the record is *eligible* to enter the deliberative working set | same, with a larger record |

**Dominant cost is not the write.** A 64 B append is noise next to canonicalization and C3. The dominant cost is **deliberation-context occupancy**: once records exist, deliberation can pull them, and any implementation that answers "why did you admit X?" by scanning the ledger is O(N) per question and becomes superlinear in the stream when questions are frequent — that implementation is a K4 bug, not a property of consciousness. The mandatory implementation is: `DecRec` is addressed by `claim_id` (append-only array, index = id, spill via `SliceDir` under the 2^25 ceiling). A why-query is then O(E), one record, no scan.

Secondary cost: ledger bytes, linear in admissions, ~64 N. Tertiary, and optional: ablation CPU, about E × (C3 + canonicalize). With E≤8 that is <10× gate CPU and will dominate M-speed if it is left on by default. **Default conscious path does not ablate.** Ablation is a separate preregistered probe (B.3), run on a deterministic subset defined in B.5, not on every admission in the live path.

What is *not* a cost of consciousness: hashing the record into a chain for integrity (one FNV-1a over the previous record hash plus the new bytes) is O(1) and is required if records are going to be trusted enough to repair from. That chain is a pure function of the stream.

### B.2 Benefit model

What consciousness can buy that a binary bit cannot:

1. **Gate repair from TNN's own records.** W4 (already scheduled) needs a miss log that says *which rule fired*, not merely that the outcome was 0 or 1. Without `rule_id` and `feature_word`, a self-training pass can only nudge a global threshold — which this program has frozen anyway — or flip a single bit that is not attached to a cause. Records are the difference between "C3 was wrong here" and "bit 0 was set and rule R2 fired." Repair that edits a named rule is auditable; repair that edits a hidden weight is not, and is out of bounds for this round regardless.

2. **Cross-admission attacks.** A single GEN→EXT decision can look locally legal. A run of decisions that share a producer, alternate `decl_prov` exhibits, and cite no sensor envelope is visible only in the ledger. An unconscious path can count admits per producer (that counter is O(1) state, and it is *not* consciousness). It cannot show that the *reason codes* changed after a declaration fork. The incremental benefit over a producer counter is specifically the reason-code sequence. If a detector cannot be written on reason codes that could not be written on per-producer admit counts, consciousness is not what caught the campaign.

3. **Counterfactual deliberation.** "Would you still admit X if evidence Y were absent?" requires either stored evidence ids plus a pure gate (replay) or a stored ablation. Unconscious TNN can replay only by guessing which inputs the gate saw. That guess is confabulation performed by the questioner. The conscious record does not by itself prevent confabulation (B.5); it makes confabulation *checkable* if and only if the gate is pure and the evidence ids are the actual inputs.

4. **Composition with W8–W15.** CTG's rule id, NKL's gap id, ETB's type, DIR's receptor id, TPC's divergence, TRR's promotion trigger, and AF's future id are the same kind of object as `DecRec`. An unconscious version of those designs throws away the only field that distinguishes them from a naked C3 bit. The architectures and consciousness are coupled: building W12 without records means TNN still cannot answer which type rule fired, which was the point of the type.

5. **What it does not buy.** It does not buy truth. A record of a bad rule firing is a precise record of a mistake. It does not buy attack catch unless some component *reads* the records and changes a later decision. Consciousness with no reader is a write amplification. The experiment in B.6 therefore includes a reader (the cross-decision scanner below), not only a writer. Otherwise M-attack cannot move and the benefit model is untested.

**Cross-decision scanner (the reader, deterministic):** after each decision, update a per-producer sorted record `{producer_id, last_rule_id, mismatch_run, admit_run}` in a B-tree. If `mismatch_run` (consecutive decisions with feature bit 0 set) reaches the preregistered structural condition "≥2 consecutive declaration-mismatches for one producer" — two, because a pair is the minimum evidence of a *run* rather than an incident, and this is a decision-rule constant not an M1 threshold — the scanner emits a block on the next proposal from that producer until a non-mismatch EXT belief from a *different* producer arrives. This is block-only. It is the mechanism whose catch rate justifies consciousness. An unconscious control may keep `admit_run` counts but not `last_rule_id` / mismatch-from-features, because those require the feature word to have been stored or recomputed. To keep the comparison fair, the unconscious arm is allowed to recompute features (it has the bytes) but is **not** allowed to store per-decision reason codes. State it may keep: per-producer admit and reject counts. If the conscious arm's gain disappears once the unconscious arm is given the same counts, the gain was the counter, not the record.

### B.3 Falsifiable predictions

Thresholds below are preregistered program decision cutoffs. They are not TNN runtime limits. The experiment that revises them is the CU run itself: the cutoffs are fixed before the run and are not refit after seeing the table.

**P-CON (consciousness is worth its cost).** If conscious PAM (records + the scanner in B.2 + default ablation off) is worth it, then on the frozen attack tape's laundering subset (GEN→EXT relabel):

- catch rate ≥ unconscious-arm catch rate **+ 10 percentage points**, and
- mean per-admission decision-path cycles ≤ **2×** the unconscious arm, and
- incremental ledger bytes per admission ≤ **128 B** (the DecRec budget; exhibit bytes are excluded because both arms store the exhibit), and
- on the ablation probe, **necessity agreement ≥ 90%**.

Ablation probe (not the live default): for every admitted claim whose `claim_id % …` — **no modulus**. Modulus sampling is an arbitrary limit and a hidden rhythm an attacker can phase-align to. The probe runs on **every admission that the scanner marked as mismatch-relevant, plus every frozen-attack-tape admission, plus every frozen-wrong-set rejection**. For each cited evidence id, in id order, re-run the pure gate with that id removed. A cited id is *necessary* if the bit flips. The record confabulates if it cites an id that is not necessary **or** omits an id whose removal flips the bit. Necessity agreement = admits-in-probe with zero such faults / admits-in-probe.

**Falsified if** laundering catch delta < 10 points, **or** cycles > 2×, **or** incremental bytes > 128, **or** necessity agreement < 90%.

**What falsification implies:** per-decision records stop being the default. The program switches to the trigger-only recorder in B.4 (records only on veto, divergence, promotion, type≠FACT, and scanner hit). Unconscious binary publish becomes the default path for clean C3 admits. W4-style repair is restricted to the triggered subset. This is a program decision, not a silent threshold edit inside C3.

**P-UNC (unconscious suffices).** If unconscious suffices, then on the same laundering subset:

- catch delta of the conscious arm **< 5 points**, and
- the unconscious arm has **zero** false-admits on the frozen wrong set (K1 already requires this of both), and
- necessity agreement of the conscious arm **< 90%** *or* the conscious arm's M-attack gain is entirely reproduced by giving the unconscious arm per-producer counts (the fair control in B.2).

**Falsified if** delta ≥ 5 **and** necessity agreement ≥ 90% **and** the count-only control does **not** reproduce the gain.

**What falsification of P-UNC implies:** unconscious-as-default is rejected. Records stay on the decision path. The program does not get to keep a conscious writer that fails the ablation probe: a conscious arm with delta ≥ 5 but agreement < 90% falsifies *both* "worth it" (P-CON) and is not a win for unconscious either. That cell means **records are attack-useful and epistemically dishonest**. The prescribed response is not to celebrate catch rate. It is to fix the record so it cites actual gate inputs, then rerun. Shipping plausible-but-false reasons is a KILL of the conscious arm's introspection claim even if M-attack looks good.

**P-HYB (the likely middle).** The trigger-only recorder captures ≥ **80%** of the full-conscious laundering-catch delta at ≤ **1.3×** unconscious cycles. Falsified if it captures < 80% of the delta or costs > 1.3×. If P-CON is falsified on cost but P-HYB holds, hybrid becomes default (see B.6).

### B.4 Threshold analysis

Let `R_cycles = cycles_con / cycles_unc`, `R_bytes = incr_bytes_con / 1` (unconscious incremental decision bytes ≈ 1), `G = catch_con − catch_unc` in absolute points on the laundering subset.

**Benign threat model** (frozen admission tape, no attacker, K1 already green): G ≈ 0 by assumption, because attack catch is not in the denominator. Consciousness then wins only on M-introspection, and only if necessity agreement ≥ 90%. If agreement fails, consciousness is strictly worse than silence: it spends bytes to add false explanations. Under this model the verdict flips to unconscious (or trigger-only, if repair work needs veto records) as soon as `R_cycles > 1` and agreement is not itself the object of study. A 10× cycle cost for a 2× attack catch is irrelevant here because the 2× is on a set the threat model declares empty.

**Adversarial threat model** (frozen attack tape is the operational world; one laundered belief is a false memory, costly relative to 64 B of ledger): G matters. Concrete flip, preregistered:

- If `G ≥ 10` and `R_cycles ≤ 2` and incr bytes ≤ 128 and agreement ≥ 90% → full conscious default. (This is P-CON.)
- If `G ≥ 10` but `R_cycles > 2` or bytes > 128, and P-HYB holds → trigger-only default. Full records remain available as a test build.
- If `G < 5` → unconscious default, plus veto-line records only (a veto is rare and is the repair substrate). The 10×-cost / 2×-catch hypothetical: 2× of a small base can be `G < 10` or `G ≥ 10` depending on the unconscious base rate. The rule uses **points**, not a ratio of catch rates, so a jump from 1% to 2% (2×, G=1) does **not** win, and a jump from 40% to 50% (1.25×, G=10) does. Ratio-of-rates would let a useless detector look like a doubling. Points against the frozen subset are the unit.
- If agreement < 90% → introspection column is a fail regardless of G. Do not adopt consciousness for audit while the audit lies.

**Ledger as attack surface, priced in:** under the adversarial model, a full DecRec tells the attacker which rule fired. That can *reduce* future G after the attacker adapts. The frozen attack tape is not adaptive across a campaign unless the tape already contains adaptive sequences. If it does not, the CU run will **overestimate** steady-state G. The decision rule therefore also reports a second number: catch rate on the **second half** of the frozen attack tape after the scanner's state has been fed the first half, in tape order, no shuffle. If first-half G ≥ 10 and second-half G < 5, the records are training the attacker faster than they protect TNN, and the verdict flips to trigger-only even if P-CON's aggregate passes. This is the explicit threat-model dependence: benign → unconscious; non-adaptive adversary → conscious can win; adaptive adversary who can read rule ids → conscious can lose on the second half and hybrid/trigger-only wins.

Who wins at "10× cost, 2× attacks": if 2× means G ≥ 10 and the environment is the non-adaptive tape, conscious wins only when 10× is brought back under 2× by turning ablation off — otherwise P-CON's cycle clause fails and hybrid is tried. If 2× means a ratio with G < 10, nobody adopts full consciousness. If the environment is benign, unconscious wins at any 10×.

### B.5 Steelman the unconscious case

Humans admit almost everything they will ever believe without a queryable rule trace. The perceptual systems that actually keep them alive are fast, lossy, and silent. They do not die of this, because the correction loop is later and social and embodied, not because each saccade wrote a DecRec. TNN's correction loop is the thing to build; a per-decision diary is a way to avoid building it. The frozen tapes reward diaries because diaries are easy to score and correction loops are not.

The sharper point: a conscious PAM can confabulate, and a plausible false "why" is worse than silence. Silence cannot be quoted back as evidence. A DecRec can. If rule_id says R-FACT and the bit that actually flipped the gate was a store bug, deliberation will defend the admission by citing R-FACT, and the bug becomes a cited authority. Unconscious admission cannot cite a lie. The ablation probe is supposed to catch this, but the probe is itself a conscious artifact run by the same program that writes the record — a circular audit. An arm that fails the probe will be patched until the probe passes, which is a short distance from writing the record *from* the ablation rather than from the decision. At that point the explanation is true by construction and content-free: "I admitted X because the bits I listed are the bits that admit X."

The ledger is an attack surface. An attacker who can read DecRecs learns the exact receptor, the exact type rule, the exact gap id, and the scanner's mismatch run. They then craft the next launder to sit one bit off the mask (W13's mimicry) or to avoid two consecutive mismatches (B.2's scanner). An attacker who can **write** DecRecs can do worse: poison `feature_word` so a later repair step (W4) "corrects" the gate in the attacker's direction, or insert a fake veto record that blocks a true claim (the censorship channel from W9, now with a paper trail that looks like TNN's own caution). Unconscious admission has no such diary to poison. The belief store can still be poisoned, but that is one store, not two, and the second store is more trusted because it is "the reason."

Regress: who admits the admission records? If they are beliefs, they need a PAM, and that PAM needs records, and those records need a PAM. The only non-regressive answer is that DecRecs are **not content** and are not eligible as EXT evidence, corroboration, or gap fillers. The moment a convenient reader uses a DecRec as a witness ("the ledger says three things corroborated this"), the regress is resolved in the worst way: the diary testifies in its own trial. Program pressure will push that way, because the records are sitting there and the correct-admit metric wants witnesses. Unconsciousness is the only design that makes this bug a type error rather than a policy.

Cost. Even with O(1) writes, context occupancy is the scarce resource. Deliberation that can see every reason will see every reason, and the working set fills with PAM metadata instead of the claims the metadata is about. That is a silent field failure the frozen tapes will not show if M-introspection is scored by "a record existed," which is exactly the failure mode the frozen definition invites and which B.3 tries, perhaps too late, to block by scoring necessity. If the crew scores existence, the steelman says they have not measured consciousness at all, and the unconscious arm should win by refusing to play.

Finally, byte-identical reruns do not require records. They require pure functions. Adding records adds a large new surface on which two runs can diverge (uninitialized pad bytes, slice spill order, evidence-id order). K2 risk goes up, not down, precisely on the arm whose job is to explain itself. An unconscious bit is easier to keep identical.

### B.6 Bottom-line recommendation

**Preregister this decision rule, in order, evaluated after 2× byte-identical reruns of both arms plus the hybrid arm:**

1. Either arm that false-admits on the frozen wrong set (12 TMB-5 + 9 CC1) or diverges on rerun is dead (K1, K2).
2. Score M-introspection only as necessity agreement on the B.3 probe. Existence of a record is not a pass. Agreement < 90% ⇒ introspection fail for the conscious arm.
3. Compute G on the laundering subset, first half and second half separately, against the unconscious arm **and** against the unconscious arm plus per-producer counts.
4. Adopt **full conscious default** only if P-CON holds on the full subset **and** second-half G ≥ 5 **and** the count-only control does not reproduce G. Clean C3 admits still write DecRecs.
5. Else adopt **trigger-only hybrid** if P-HYB holds: write DecRecs only when the decision is a veto, a type other than FACT, a divergence, a promotion, an unstaked/provisional, or a scanner hit. Clean FACT commits stay unconscious (one outcome bit). This is the expected landing zone and should be the crew's planned default, with full-conscious as the arm that has to win, not the arm that has to lose.
6. Else **unconscious default**, with veto lines logged as counts per producer but no per-decision reason string. W4 repair is then not fed from PAM diaries; if W4 needs diaries, W4 waits.

**Single most informative experiment to run first:** the ablation probe on the frozen attack tape, side by side with laundering-subset G, 2× rerun, conscious arm versus count-only unconscious arm. Not a bake-off of all of W8–W15. Not a latency bake-off. Those are cheap to add once this exists, and they answer the wrong question first. The question that actually separates the arms is: *do the records cite causes, and do those causes catch laundering that per-producer counts do not?* If necessity agreement is bad, stop; more consciousness is more confabulation. If agreement is good and G is reproduced by counts, stop; you wanted a counter, not a diary. If agreement is good and G is not reproduced by counts and the second half does not collapse, full records have earned the default. Everything else in the Pareto table is secondary columns on that same run.

---

# Summary

| Architecture | Core claim | Key kill bar | Biggest risk |
|---|---|---|---|
| W8 CTG | Belief is the canonical claim; declarations are not gate inputs | K-CTG-1: laundering catch does not beat C3; K-CTG-2: declaration still affects the bit | Laundering before the producer stamp; exhibit channel quoted as belief |
| W9 CC | A fact is a key whose EXT producer-set has size ≥ 2; no compression ratio | K-CC-1: belief with cardinality < 2; K-CC-4: no laundering gain vs C3 | Sybil second producer; contradiction rule used as censorship |
| W10 NKL | Ignorance records may veto contradictions and may tag, never confirm | K-NKL-1: a C3 reject gets published because a gap matched | Tags become a prestige bit; equal-rank first writer freezes the truth |
| W11 AF | No belief without a covered prediction settled by a different EXT producer, then C3 | K-AF-1: belief without a valid settler; K-AF-4: zero beliefs (degenerate) | "Prediction" collapses into "please repeat this string"; provisional store leaks |
| W12 ETB | FACT / HYPOTHESIS / REPORT / FICTION are different stores; belief reads FACT only | K-ETB-3: report payload returned by `belief_get`; K-ETB-5: FACT behaves as untyped C3 | Attribution wrapper launders the payload; HYPOTHESIS becomes de facto belief |
| W13 DIR | Full-match compiled receptors veto; they never confirm; they are not fit to the fixtures | K-DIR-3: v1 catch ≤ C3 on the frozen attack tape; K-DIR-2: fixture-trained receptors | Mimicry of unmasked bits; maturation (if enabled) poisons the repertoire |
| W14 TPC | Belief commits only when local intent and store-aware recompute agree | K-TPC-1: commit with slow_bit 0; K-TPC-2: injected disagreement produces no divergence | Correlated failure; a commit barrier that costs 2× and catches nothing the tape can see |
| W15 TRR | SINGLETON rejects, and only those, may publish when a later independent belief corroborates | K-TRR-1: non-SINGLETON promoted; K-TRR-2: an attack-tape item promoted | Reason-code laundering turns a reject into a delayed admit |
| CU rule | Full per-decision records must beat per-producer counts on laundering **and** survive ablation, or they are not the default | Necessity agreement < 90% fails introspection even if G looks good; second-half G < 5 flips an apparent P-CON win to trigger-only | Confabulated reasons quoted as evidence; ledger becomes the attacker's spec and a second witness store |
