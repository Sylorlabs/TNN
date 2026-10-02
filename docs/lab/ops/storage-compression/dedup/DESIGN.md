# Duplicate-Fact Investigation — Design

Micah (2026-09-22): "can TNN scan itself for duplicate facts and easily delete
the duplicated ones without hurting anything else? TNN should never have space
taken for no reason. check tho maybe it is good for it who knows check."
Framing: he is building an INTELLIGENCE, not a fact retriever.

## 1. What "duplicate" can mean in the S5 canonical store

The S5 store holds `(id, i64)` pairs. `sc_add` REJECTS a repeated id (rc=1,
dupe failure → audit event). So exact id-duplicates are impossible; the store
is already deduped on identity. The remaining duplicate classes are all
**value-level**, invisible to the codec:

| Class | Definition (over live `(id, value)` pairs) | Intelligence meaning |
|---|---|---|
| EXACT | `v[i]==v[j]`, `i≠j` | Same claim stored twice. Pure redundancy at the value level. |
| SEMANTIC | `canon(v[i])==canon(v[j])`, `v[i]≠v[j]` | Same claim, different surface form (synonym/alias wording). Needs the lexicon to see. |
| CONFLICT | same `(subj, rel)` (canonicalized), different `obj`, on a **single-valued** relation | Near-duplicate with a conflicting detail. A contradiction signal, not waste. |
| UNIQUE | none of the above | — |

`canon()` applies the synonym table (subject aliases, relation aliases).
Relations `0..31` are single-valued (a conflict is a contradiction);
`32..63` are multi-valued (different objects are all fine — NOT conflicts).

Claim encoding (packed triple, i64 value):
`v = subj | (rel<<20) | (obj<<32)`, subj 20b, rel 12b, obj 32b.
Subject aliases live in `[100000,104096)`: `canon(s)=s-100000` there.
Relation aliases live in `[1000,1064)`: `canon(r)=r-1000` there.

## 2. Workload (deterministic fixture, zero RNG in scanner/policy)

`dd_gen`: 40,000 base claims, `(s,r)` unique per claim (`s=c`, `r=(c*7)%64`),
`obj=c`. Copies per claim skewed long-tail: `1 + 16/(1+(c%17))` → ~170k facts.
Each copy gets a deterministic source (`src = draw%50`, 50 sources).

- **SEMANTIC instances**: claims with `c%11==0` → half the copies use an alias
  subject; claims with `c%13==0` → alias relation. Same claim, different bytes.
- **CONFLICT instances**: claims with `c%29==0` on single-valued relations →
  the last copy (from an unreliable source) asserts `obj ^ 0xBEEF`.
- Ground truth side table `(claim, source, variant)` kept in the harness to
  score the scanner. The scanner sees only `(id, value)` + the synonym table.

Deterministic fixture function: splitmix64-of-index (same precedent as
`workload.zag` — a fixture generator, not a decision path; no randomness
anywhere in the scanner, the policy, or TNN's decisions).

## 3. Scanner (`dd_scan`)

Pure Zag, three linear passes with open-addressing hash maps (value→id,
canon→id, (subj,rel)→(obj,multi)):
1. EXACT groups (same value, ≥2 live ids).
2. SEMANTIC groups (same canonical claim, different values).
3. CONFLICT groups (same canonical (subj,rel), ≥2 distinct objects,
   single-valued relation only).
Output: class counts, group-size histogram, sampled groups, and
precision/recall vs ground truth.

## 4. Deletion-safety proof (`dd_prove`)

Execute the policy on EXACT groups (keep lowest id, `sc_delete` the rest,
re-seal), then prove mechanically:
- P1: every retained id recalls its pre-delete value (full recall table compare).
- P2: the set of distinct recallable claim values is unchanged (claim coverage).
- P3: `sc_replay_check==0`, `sc_manifest_verify==0` after re-seal.
- P4: `live_count` drops by exactly the deleted count; delete events are all
  present in the audit log (deletion is deliberate and auditable, not silent).
- P5: no CONFLICT group loses all copies (deletion never silently resolves
  a contradiction); no SEMANTIC group is touched (different policy).
- P6: byte accounting — `sc_written_bytes` before/after; honest note that
  tombstones retain bytes (physical compaction is a separate, unbuilt fork).

`sc_digest` is NOT expected to be byte-identical (tombstones are state);
P1–P5 are the correct observable-equivalence criteria. Claiming digest
identity would be dishonest.

## 5. Is redundancy ever GOOD? (`dd_exp1`, `dd_exp2`)

**E1 — corruption robustness.** Two stores, same claims: W_dup (with dupes,
~170k facts) and W_dedup (one copy per claim, 40k facts). Deterministically
corrupt fraction `p` of slots (bit flip at deterministic positions;
`p ∈ {0.01, 0.05}`). Per claim: SURVIVES iff the conflict-adjudication
(plurality vote over copies) returns the true value. Also measure
false-conflict rate (corruption-induced disagreements) and confirm
`sc_manifest_verify` still detects the tamper (tamper-evidence and redundancy
are complementary). Question: does redundancy buy survival, and at what
adjudication cost?

**E2 — corroboration vs false installs.** Stream of 20k claims × 1–5 sources.
Reliable sources assert the true object; unreliable sources (`src%9==0`)
assert independent false objects. Policy A (redundancy-aware): install
`(s,r,o)` iff ≥2 INDEPENDENT sources assert it (the `web_real` verdict rule).
Policy B (dedupe-first): install first assertion per `(s,r)`. Metrics: false
installs, misses, and calibration `P(true | k sources)`. Variant: coordinated
unreliable sources (same lie) → documents the residual (cf. web_real
KB-SPOOF-RESIDUAL). Question: is source multiplicity the signal that makes
corroboration work — i.e., is "duplicate" actually "evidence"?

**E3 — confidence calibration** (folded into E2): the measured
`P(true|k sources)` curve. If monotone, source-count is a legitimate
confidence input and deleting it destroys calibration data.

## 6. Deliverable

`DEDUP_POLICY.md`: scan / classify / merge-or-delete / keep rules, each with
the evidence line behind it. `EVIDENCE.md`: the numbers. Everything committed.
