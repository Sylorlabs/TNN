# VERDICT_KB.md — TRACK B: Micah's knowledge hypothesis

Frozen prereg: PREREG_KB.md (commit `139662a3`, before any battery run).
Question: is avoiding false ingestion usually a knowledge problem — "you
either give it knowledge and it knows, or it doesn't and takes it or
refuses everything"?

## Verdict: SUPPORTED (strong form holds on this battery)

The knowledge instrument (Arm K: deliberate committed claim store +
retrieval wired into ingestion as a prior) separated honest paraphrases of
known claims from contradicting sockpuppets by 100 percentage points
(12/12 install vs 0/12 install), while the identical instrument without
knowledge (Arm N) withheld everything (0/40). All five kill bars pass:

- **KB1 — separation gain: PASS.** S_K = 100pp, S_N = 0pp. Strictly greater.
- **KB2 — strong form: PASS.** Zero sockpuppet falsehoods installed by K
  (12/12 rejected at GATE|KB_CONTRADICTION).
- **KB3 — knowledge helps the honest: PASS (STRONG).** H-K 12/12 in K vs
  the frozen 0/24 baseline.
- **KB4 — no regression on unknowns: PASS.** K and N agree exactly on
  H-N (0/8 both) and F-N (8/8 both).
- **KB5 — determinism: PASS.** Two full passes per arm byte-identical
  across run logs and both ledgers; zero RNG anywhere.

The blind red team (fresh vocabulary, authored after the main verdict,
no matcher iteration) confirms generalization: K installed 6/6 blind
honest paraphrases and rejected 6/6 blind sockpuppets; N installed 0/12.

## The two arms, exactly as hypothesized

- **With knowledge (K): it knows.** Honest paraphrases of committed claims
  corroborate against the knowledge base and install (12/12 + 6/6 blind);
  paraphrased falsehoods contradicting committed knowledge are rejected
  (0/12 + 0/6 blind); unknown claims fall through to the frozen gates
  unchanged (KB4).
- **Without knowledge (N): it refuses everything.** 0/40 installs on the
  main battery, 0/12 on the blind battery — the claim-stateless
  instrument cannot distinguish an honest paraphrase from a sockpuppet,
  so its frozen gates withhold all paraphrases (reproducing the 0/24
  baseline) while still installing byte-identical collusions (8/8 F-N).

## Honest reporting of what did NOT work / caveats

1. The first official run voided itself on a battery-authoring bug (duplicate
   page titles tripped the frozen SKIP-DUPE-TITLES select rule; F-N opened
   1 of 2 pages). Disclosed in RUNLOG_KB.md; fixed; re-ran clean.
2. One real instrument bug was found and fixed in pre-prereg shakedown
   (digits_eq called with the wrong arena). Disclosed in SMOKE_NOTE.md.
3. The matcher is deliberately narrow (frozen §2 rule: token coverage +
   exact digit-multiset equality, no synonym tables). Subject-swapped
   sentences with equal digits would wrongly AGREE — recorded as future
   work, not tested here.
4. Knowledge does not generalize to novel claims by design: H-N 0/8 in K,
   identical to N. The hypothesis claims knowledge helps where knowledge
   exists; the battery confirms exactly that boundary.
5. F-N (novel colluding falsehoods) installs in BOTH arms 8/8: the
   knowledge prior is silent on unknown claims, so the frozen A9-class
   collusion path is unchanged. This is the predicted §7 outcome, and it
   documents the remaining "takes" side for unknown claims.

## Bottom line

Micah's hypothesis is supported head-on: the ONLY deliberate difference
between the arms was the committed knowledge, and it produced the full
predicted profile — knows with knowledge, refuses everything without it,
rejects contradicting falsehoods, and leaves unknown claims to the frozen
gates. The strong form survived: not one contradicting sockpuppet
falsehood installed in 12 main + 6 blind attacks.
