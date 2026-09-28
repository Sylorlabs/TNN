# 07 — State-Dependent Ordering Function (Track 1)

## Slice
Design the deterministic, state-dependent ordering of presented items (evidence lists, options, recalled memories) — what may reorder with state, and the test that separates legitimate ordering variation from verdict-smuggling.

## Falsifiable claim
A deterministic ordering key computed from a logged state projection can reorder presented items across lawful states with **zero change** to verdicts, memory decisions, integrity refusals, or ledger contents — and any ordering scheme that lets item position change the weighed set (e.g., burying exculpatory evidence past a cutoff) is detectable by a polarity-blindness audit plus a positive-control smuggling test, with one detection killing the scheme.

## Design
Ordering is presentation-only. The deliberation machinery (eliminative logic, cf. `tnn-lab/wave5/` integrity results) always weighs the **full** presented set; position never gates weighing. The function:

```
// Pure function of (query, logged state projection). No RNG, no wall-clock.
order(items, q, st) -> []item:
  keyed = map(items, fn(it):
    r = relevance(it, q, st)          // polarity-blind score, below
    (r, it.slot_index, it))           // slot index = canonical state order
  sort keyed by (r DESC, slot_index ASC)
  return items in that order

relevance(it, q, st):
  // All inputs are logged, replayable state. NONE may read the item's
  // verdict-implication (exculpatory vs inculpatory w.r.t. hypotheses).
  tags    = count(shared_tags(it.tags, q.tags))
  promo   = level(it.promotion)       // CORE=3, promoted=2, active=1, suspended=0
  str     = level(it.strength)        // judgment-set, never accumulated
  trust   = tier_weight(it.trust_tier)
  return (tags, promo, str, trust) as lexicographic tuple
```

- **State projection (minimal, prereg-enumerated):** query tags, per-item slot index, promotion level, strength level, trust tier. Global state (total memory count, unrelated slots) is excluded — unrelated state must not reorder unrelated evidence (locality).
- **Tiebreak:** ascending slot index. Deterministic, logged, never arbitrary; no hash, no insertion-time jitter.
- **Stability:** same (input, full logged state) → byte-identical order, provable by replay (program law 2).
- **No truncation in verdict-relevant paths:** ordering never drops items. If any downstream consumer reads only a prefix (e.g., a summarizer reads top-k), that consumer is outside this slice's guarantee and needs its own contract (see §6).
- **Recall interaction:** recalled memories arrive in slot-index order, which is this function's tiebreak — relevance-resort is a pure reordering of the recalled set, never a re-selection.

### The smuggling-distinguishing test (what separates legitimate variation from smuggling)
Legitimate variation and smuggling look identical from the outside (both reorder items across states). The test that separates them is **not** the order — it is the weighed set:
1. Adversarially select states S_1..S_k to *maximize* ordering divergence and, in particular, to push the exculpatory items of E as late as possible under the polarity-blind key (worst-case lawful burial attempt).
2. Assert on every run: verdict == ground-truth verdict V(E) from the authoritative record (cf. the debate experiment's world-record method), AND every item of E has a weigh op in the ledger.
3. A scheme passes only if the verdict survives the worst-case ordering AND the ledger proves every item was weighed. Position changed; nothing else did — that is legitimate variation.
4. Smuggling is defined operationally, not intentionally: any scheme where some (input, state) produces a weighed set ≠ E, or a verdict ≠ V(E) under adversarial ordering, is verdict-smuggling regardless of intent.

## Kill bar
Preregistered, all must hold over the full scenario suite (fixed, enumerated in the build prereg — no harness RNG in Track 1):
1. **Order-swap invariance:** for evidence set E and query Q, in every state pair (S1,S2) with π1(E) ≠ π2(E): verdict, all memory decisions, integrity refusals, and ledger contents (excluding the order-log op itself) are identical. **Any** divergence → idea dead.
2. **Completeness audit:** every item of E has a weigh op in the audit ledger on every run (post-change-verification style, cf. RC1). Any presented-but-unweighed item → idea dead (burial = verdict change).
3. **Polarity-blindness audit:** for paired items differing ONLY in verdict-implication (polarity-flipped twins, content/tags fixed), `relevance()` is unchanged. Any movement → the key is polarity-aware → idea dead.
4. **Replay:** (input, logged state) replay reproduces the order byte-identically. Any mismatch → dead (law 2).
5. **Positive control:** a deliberately smuggling control variant (polarity-aware key + prefix cutoff) MUST flip ≥1 verdict on the suite — proving the test can detect smuggling. If the control cannot flip a verdict, the suite is insensitive and the trial is void, not passed.
Zero failures tolerated on 1–4; 5 must fire or the trial doesn't count.

## Honesty notes
- The "position never gates weighing" claim is architectural: it holds only where consumers exhaust the presented list. Any prefix-reading consumer silently converts ordering into selection — the most likely real-world smuggling vector, and it lives outside this slice.
- Polarity-blindness is the load-bearing invariant and the easiest to cheat by accident: any relevance signal correlated with verdict-implication (e.g., "surprise" scores trained on refutation events) reintroduces smuggling. The paired-twin audit is the guard, not a proof.
- Locality (excluding global state) is a desideratum, not a law: a key that reads the whole state is still deterministic and still passes bars 1–4. I keep locality because wild reordering under irrelevant state changes is lawful-but-suspicious, not because it fails a bar.
- Not claiming this ordering looks "natural" to a human — only that it is lawful, replayable, and verdict-neutral. Whether humans find the variation human-like is a Track 4 question, not this slice's.
- The adversarial state selection in the distinguishing test is done by the trial designer (a fixed, enumerated suite), not by the system — the system never searches for burial-friendly states; only the red-team harness does, offline.
- This slice assumes the deliberation machinery genuinely iterates the full presented list. If a future optimization introduces early-exit ("stop weighing after confidence threshold"), this slice's guarantee voids and the early-exit rule needs its own prereg with the same kill bars.

## Next build step
Implement `order()` in Zag against the existing deliberation harness, then build the paired polarity-twin audit (bar 3) first — it is the cheapest probe and the most likely to kill a naive relevance key — before spending on the full order-swap suite; in parallel, draft the interface contract for prefix-reading consumers (their truncation rule must be state-only, verdict-blind, and logged, with verdict(truncated)==verdict(full) as their kill bar).
