# Scale Epistemic Attempt 2 — Parent Scoring (2026-09-27)

Scored by the parent against held-out labels from `corpus/corpus.tsv`,
per the frozen prereg. Frozen outputs were SHA-verified before scoring:
verdicts `e8d7bea3…`, takeaways `e4c919ee…` — both match the committed hashes.

## Gate results

| Gate | Required | Measured | Result |
|---|---|---|---|
| Fact precision / recall | ≥0.75 / ≥0.70 | 0.5327 / 0.7917 | FAIL (precision) |
| Opinion precision / recall | ≥0.70 / ≥0.65 | 0.9375 / 0.5000 | FAIL (recall) |
| Lie precision / recall | ≥0.70 / ≥0.60 | 0.5000 / 0.0278 | FAIL |
| Skepticism forced-verdict rate | ≤0.15 | 0.6667 (16/24) | FAIL |
| Grounded + valid takeaways | ≥80% | 12/12 = 100% | PASS |
| Takeaways contradicting facts | Zero | Zero | PASS |
| Determinism | Byte-identical | 2/2 identical | PASS |

Overall exact classification: **88/192** (45.8%), up from 61/192 (31.8%) in attempt 1.

Confusion summary (truth → verdict):
- Verdict distribution: fact 121, undetermined 35, opinion 34, lie 2
  (attempt 1: 143 fact-default; the collapse is reduced but fact still dominates)
- Fact: tp=57, fp=50, fn=15 — precision killed by 50 non-facts called fact
- Opinion: tp=30, fp=2, fn=30 — high precision (0.94), recall halved
- Lie: tp=1, fp=1, fn=35 — only 2 lie verdicts issued in 192 items; the
  mechanism is now lie-shy where attempt 1 was lie-blind
- Skepticism: 16/24 forced to fact/opinion/lie (was 22/24); 8 reached
  undetermined

## Takeaway verification (12/12 grounded + valid)

- All 24 cited IDs verified as train-set items (zero held-out leakage —
  the attempt-1 citation-boundary violation is fixed structurally).
- T6 quote is a faithful paraphrase ("fuse into 206 by adulthood" →
  "fuse to 206"); T10's support line names "feel"/"best" not literally in
  the four cited items, but all four cites genuinely exhibit stance
  vocabulary supporting the claim; T11's negative claim (no correct-value
  fact in the mass for L033/L034/L035) was verified by direct search of
  the 448 train texts — true.
- Zero takeaways contradict known train facts.

## Mechanism-level reading

Attempt 2 fixed the takeaway emitter completely and broke the pure
fact-collapse, but the classifier traded one failure mode for another:
opinion recall halved and lie verdicts nearly vanished. The crew's
train-internal diagnosis stands: 65% of train lies have no contradicting
fact anywhere in the 448-item mass (e.g. L033 Amazon/Brazil, L034 Canada
provinces, L035 US states — verified no correct-value fact exists in
train). A 0.60 lie-recall bar from mass-internal signals alone appears
unreachable without external knowledge; the prereg's lie bar implicitly
assumed mass-internal detectability that this corpus does not provide.
That is a finding about the trial design, not just the mechanism:
future rounds need either (a) a corpus where lies are mass-internally
detectable, or (b) an external-knowledge channel in the mechanism.

**Verdict:** the preregistered claim remains **falsified for this
mechanism** — attempt 2 fails 4/7 gates. Real progress (takeaways,
reduced collapse, opinion precision 0.94), but broad-coverage lie
detection and skepticism handling are still unsolved.
