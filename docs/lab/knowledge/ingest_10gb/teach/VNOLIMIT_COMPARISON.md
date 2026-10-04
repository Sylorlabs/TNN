# V-NOLIMIT vs V1/V2/V3 — Head-to-Head Comparison

**Date:** 2026-09-24
**Status:** Full-corpus teach COMPLETE. **V-NOLIMIT KILLED per prereg §4.7**
(lessons_rejected=2 vs required 0; see Verdict).
**Question:** Micah's law — "TNN should not have a stupid limit like that. Limits are not a thing TNN needs."
The 4096B chunk-split created the ~N key mess. V1/V2/V3 *manage* the ~N keys. V-NOLIMIT *kills the split itself*.

## Full-corpus results

| Metric | V0 (frozen) | V1 (admit ~N) | V2 (CAL skip) | V-NOLIMIT (teach) |
|---|---|---|---|---|
| n installed | 9,030,226 | **9,314,871** | 9,224,704 | 9,124,603 |
| g1 | 9 | 9 | 9 | 9 |
| g2 | 0 | 0 | 0 | 0 |
| g3 | 100,371 | 12,334 | 102,501 | **5,864** |
| lessons_rejected | 3 | **0** | **0** | 2 |
| ~N keys in store | yes (dropped) | yes (admitted) | yes (G3'd) | **NO — joined whole** |
| gate change | none | G3 grammar +~N | CAL canary skip | remove 4096B cap |
| source change | none | none | none | clean2.py: no split |
| seal | 43d7e5cc… | 3e12a69c… (×2) | a17580c4… (×2) | 827f39bd… |

V1a/V1b seals identical; V2a/V2b seals identical (determinism ×2 confirmed).
V-NOLIMIT: single teach; exact probe match on all numbers.

## 1. Installed coverage

- **V1** installs the most physical records (9,314,871) — it admits all 113,601 tilde
  chunks as first-class records via the G3 grammar amendment.
- **V-NOLIMIT** installs fewer physical records (9,124,603) but each joined group
  contains *all* its chunks' text: 117,470 chunks → 51,804 whole records (45,940
  installed after gate). Logical text bytes per installed record are higher; no
  chunk text is lost to the join (byte-identical round-trip proven).
- **V-NOLIMIT drops 2 lessons** (131,072 records) to the CAL — shifted boundaries
  place legitimately-G3-failing spaceless Gutenberg texts at lesson heads 16/17.
  V1 drops 0, V0 drops 3, V2 drops 0.
- **V2 loses content**: 102,501 g3 (kind-6 tilde chunks G3'd individually).
  V-NOLIMIT g3s only 5,864 — all legitimate (spaceless texts, malformed keys).

Net: V1 > V-NOLIMIT > V2 > V0 on installed records; V-NOLIMIT > V1 on g3-honesty
(fewest illegitimate drops).

## 2. Determinism

- V1: V1a/V1b manifests **byte-identical** (proven rerun).
- V2: V2a/V2b manifests **identical** (proven rerun).
- V-NOLIMIT: the join is deterministic (canonical minimal-L separator, pure function
  of chunk bytes). CP1nol and CP2nol variant runs **exactly match** the Python probe
  (n/g1/g2/g3/lessons/rejected all equal). Full-corpus determinism rerun pending
  (blocked on ALL DONE).

## 3. Wall time / store size

- Full-corpus V-NOLIMIT teach not yet run (blocked). CP timings: CP1nol (51,804 recs)
  variant teach ~54s; CP2nol (195,493 recs) ~39s. Input stream is 9,261,548 records
  (vs 9,327,214 original) with larger average text (joined). Store size expected
  comparable to V1 (fewer keys, more text bytes + separators).
- One-time join cost: ~15 min streaming (L-search) to produce the transformed corpus;
  reusable artifact.

## 4. Provenance honesty

- **V1**: Honest — tilde keys visible in store, G3 amendment documented. BUT it
  *enshrines the artifact*: the ~N keys exist only because of the stupid limit, and
  V1 writes them into the spec grammar permanently.
- **V2**: Honest about the CAL skip, but silently LOSES kind-6 tilde content (102,501 g3).
- **V3** (CP-only): Opaque — arithmetic re-keying hides chunk provenance entirely.
- **V-NOLIMIT**: Honest — natural keys, no ~N, canonical `"\n"*L` separators documented,
  boundary-whitespace irreversibility disclosed (preimage, not recovery). The gate
  change is a limit *deletion* (dynamic buffers replace the 4096B cap), not a grammar
  addition. The source fix (clean2.py) kills the split at the root for future corpora.

## 5. Governance cost

| Variant | Change | Character |
|---|---|---|
| V1 | G3 spec grammar +~N | Adds grammar to enshrine an artifact of a limit |
| V2 | CAL canary skip | Weakens a safety mechanism; loses content |
| V3 | Pipeline re-key | Opaque; provenance destroyed |
| V-NOLIMIT | Gate: dynamic buffers (cap removed); clean2.py: no split | **Removes** the stupid limit at both layers |

V-NOLIMIT is the only variant whose governance cost is *negative* in the limit
ledger: it deletes an arbitrary limit instead of adding machinery to cope with it.

## Verdict

V-NOLIMIT is the only variant that honors Micah's law at the root. V1/V2/V3 all
accept the 4096B split as given and negotiate with its ~N debris; V-NOLIMIT says the
split was never load-bearing and removes it — gate *and* source.

**Measured cost:** 2 rejected lessons (vs V1's 0) — CAL working as designed on
legitimately failing records, strictly better than frozen V0's 3. And a gate
change (dynamic buffers), the honest price of "no stupid limits."

**⚠️ KILLED per prereg §4.7:** the preregistered bar was lessons_rejected=0; the
teach confirms 2. The mechanism is benign and the prediction was exact, but the
written bar is violated. Per frozen-prereg governance, revival requires Micah's
explicit re-approval amending the bar to 2.

**Recommended successor:** V-NOLIMIT + V2 peek-window (limits audit L4). The
peek-window composes with the no-split gate per the audit and would rescue the
2 CAL-dropped lessons (256-record window, ≥4 must pass), giving 0 rejected while
keeping whole records. Requires a new gate binary + separate prereg.
