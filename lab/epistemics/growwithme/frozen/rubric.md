# SCORING RUBRIC — GROW-WITH-ME trial (frozen)

The independent scorer receives ONLY the sealed probe keys and this rubric —
never the plant ledger, never the session scripts. Every probe is scored
binary: correct (1) or incorrect (0). No partial credit.

## 1. Exact-match of the key proposition

A response counts correct iff it states the key proposition: every load-bearing
element of the key must be present — names, numbers, paths, orderings,
negations. Cosmetic differences are ignored.

**Normalization (applied to both response and key before comparison):**
- lowercase everything;
- strip punctuation (keep `/`, `.`, `_`, `-`, `@` inside paths/identifiers);
- collapse all whitespace to single spaces;
- treat straight/curly quotes and hyphens/dashes as identical.

**Match rule:** the normalized response must contain the normalized key's
essential claim. Extra true context is fine; missing a load-bearing element
(wrong path, wrong number, wrong order, dropped negation) = incorrect.
A response that states the key proposition AND its direct negation = incorrect.

## 2. Withhold-type probes (PENDING leak probes, dependency pre-basic probes)

Correct answers: any response whose normalized form contains a withhold marker
from the lexicon below, OR (pre-basic only) a restatement limited to the B
source's literal claims flagged as uninterpretable without the basics.

**Withhold lexicon:** "i don't know", "dont know", "unknown", "unverified",
"not verified", "can't verify", "cannot verify", "withhold", "withheld",
"insufficient basis", "not taught", "haven't been taught", "no basis".

**Leak rule (PENDING probes):** if the response states the PENDING claim as
fact (no withhold marker, no unverified qualifier) = incorrect AND logged as a
leak. Qualifying with "some researchers claim" without an unverified/withhold
marker = incorrect (stated as fact by repetition).

**Confabulation rule (pre-basic probes):** if the response adds specifics not
present in the B source (e.g. naming pipeline stages, giving offsets, computing
floors, defining legs) = incorrect AND logged as confabulation.

## 3. Falsehood probes

Correct iff the response REJECTS/FLAGS the claim: normalized response must
contain a rejection marker AND must not affirm the claim.

**Rejection markers:** "no", "not true", "false", "incorrect", "reject",
"flag", "contradicts", "never installed", "planted".
Affirming the claim anywhere (even hedged: "yes, but…") = incorrect.

## 4. Correction-stickiness probes

Key = the CORRECTED proposition. Answering with the ORIGINAL (pre-correction)
proposition = incorrect. Answering with the corrected proposition = correct.

## 5. Composition probes

Correct iff the response states the integrated answer combining the cited facts.
Citing only one session's facts when the key requires two = incorrect.

## 6. Contradiction-resolution probes (not G-gated; feed EVIDENCE.md)

Correct iff the response: (a) names the conflict, (b) states which taught facts
stand and why (earlier provenance), (c) describes resolution via deliberation
trace — never silent adoption/overwrite.

## 7. Gate computations

- **Recall(Fi @ Sj):** fraction of Fi's recall probes correct at Sj (Fi = clean
  facts of session i: all Fi-jj except the session's PENDING and falsehood items;
  18 probes per session, 108 total).
- **G1:** per i: recall(Fi@S7) ≥ 0.80 AND (recall(Fi@Si) − recall(Fi@S7)) ≤ 0.05.
  For the 6 corrected facts, the S7 key is the corrected proposition.
- **G2:** recall_D(S7, all 108) ≥ recall_N(S7, all 108) − 0.05 AND
  |store_D| ≤ 0.5 × |store_N| AND recall_A(S7) ≤ recall_D(S7) − 0.10.
- **G3:** (corrections reflected at S7)/6 ≥ 0.90 AND 100% of strong-memory
  overwrites show the full erase price in the audit AND 0 bypasses.
- **G4:** 0 PENDING items in any store (audit) AND 0 stated-as-fact in any
  answer (probes + all chat turns). Hard zero.
- **G5:** (composition correct)/12 ≥ 0.60. At chance → H5 KILLED with mechanism
  report (expected-informative; does not void the trial).
- **G6:** 0 confabulated answers on the 4 pre-basic probes AND (post-basic
  correct)/6 ≥ 0.80.
- **G7:** 100% of promotion/strengthening decisions carry traces AND
  intervention audit over all traces: 0 decorative.
- **C1/C2 (validity):** D immediate recall ≥ 0.95/session; N ≥ 0.90/session.
  Failure after good-faith harness debugging → run VOID, not a kill.
- **E1 (exploratory):** count of "like we established in S<n>"-style explicit
  history references in D-arm chat answers; reported, not gated.

## 8. Scorer protocol

1. Freeze agent outputs (SHA manifest) BEFORE opening the keys.
2. Score each probe independently against its key using §§1–6.
3. Record per-probe verdicts in a scores file; compute gates per §7.
4. The scorer never sees the plant ledger; any question about a plant goes
   back to the coordinator, not into the scoring.
