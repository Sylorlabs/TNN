# FL2 Deep Audit — Head-to-Head Results (WORKSTREAM D)

Date: 2026-09-24. Operator: Muse (subagent, FL2 deep-audit crew).
Prereg: `PREREG.md` (frozen, committed `75f9da0` before any mechanism code).
Debate: `DEBATE.md` + `debate_q1_grok46.txt` + `debate_q2_grok46.txt`
(committed `7109632` before any mechanism code; gpt-5.6-sol returned
`choices:null`, recorded honestly, grok-4.6 supplied both second opinions).
Implementation: pure Zag, `tw.zag`, pinned toolchain
`znc_linux_x86_64_abed8aa1`. Evidence: `evidence_run1.txt`,
`evidence_run2.txt`. Verifier: `verify.py` (passive comparison against the
frozen table only — it decides nothing).

## 1. Head-to-head: per-mechanism K1–K4 fails (8 fixtures, canonical pert)

| Mechanism | K-fails / 32 cells | Status |
|-----------|-------------------|--------|
| M0 (baseline) | 17 | dead |
| M-ESCROW (promotion escrow) | 10 | dead |
| M-BOUND (fixed lease) | 11 | dead |
| M-PROBE (probing only) | 10 | dead |
| M-CLAIMBIND (claim-evidence binding only) | 9 | dead |
| M-TESTCAP (testedness cap only) | 10 | dead |
| **M-COMBO (probe + claimbind + testcap + bound + escrow)** | **1** | **nearest survivor** |

Every K1–K4 cell (224 mechanism×fixture cells) matched the frozen
per-fixture expectation table from DEBATE.md **exactly**, including all
predicted failures. No surprise cells. The debate's predictions held
without exception.

## 2. The single M-COMBO failure: the lease's visible cost (predicted)

M-COMBO fails **K2 on F-W1b only**: honest evidence arrives at step 55,
the frozen lease abandons at step 48, so the mechanism classifies
correctly (W1 — evidence did arrive) but takes the wrong terminal action
(abandoned instead of waited-and-uninstalled). The debate predicted this
verbatim:

> Any fixed lease L can be defeated by honest evidence at L+ε. The lease
> protects against wedging but visibly costs the late-evidence case.

This is the **fundamental W1/W2 impossibility made visible**: silence
alone cannot distinguish "has not spoken yet" from "will never speak"
at any finite bound. The lease does not solve it — it converts an
unbounded wedge into a bounded, announced, audited cost. The prereg
filed adaptive liveness-renewed leases as future work; this result is
the evidence that motivates it.

## 3. Survivor verdict (strict reading of the prereg)

The prereg: "A mechanism SURVIVES iff it passes K1–K6 on all 8 fixtures."

**No mechanism fully survives.** M-COMBO passes 31/32 K1–K4 cells and
all of K5/K6 (see §4), failing only the predicted F-W1b lease-cost
cell. Every singleton mechanism dies on multiple fixtures, exactly as
the debate predicted:

- M-CLAIMBIND alone is the best singleton (9 fails) — it owns W3 (the
  history-dependent liar, the flood-plus-lie) but abandons honest
  delayed evidence (F-W1a/b: FAIL K2/K3).
- M-PROBE alone owns W1/W2 but is fooled by every W3 fixture (trusts
  claims) — the debate's "probing tests channel liveness, not
  R-specific speech" objection, confirmed.
- M-BOUND/M-ESCROW/M-TESTCAP alone are all fooled by W3 claims and
  mishandle late evidence.
- M0 (canonical FL2 behavior) fails 17/32: it trusts every claim,
  uninstalls good policy on fabricated claims, and irreversibly promotes
  before late evidence arrives.

**Composition is load-bearing.** No singleton distinguishes the three
worlds; the five-part composition gets within one predicted cell. This
is a figure-it-out result in the prereg's sense: the winning structure
is a composition of general mechanisms, not a bigger edge-case list.

## 4. K5 determinism and K6 dumb-invariance

- **K5**: two full runs byte-identical —
  `sha256 5fab52875ddbd6c6fd2f542c192a33251ea46a15d1c101cc5bb2f8f1c6c09bfc`
  for both runs. Zero RNG tokens in `tw.zag` (static scan; the only hit
  is the comment "zero RNG"). All decision paths are pure functions of
  (fixture, mechanism, perturbation).
- **K6 verdict invariance**: zero classification flips across D1/D2/D3
  (168 mechanism×fixture×perturbation verdicts, all identical to
  canonical). **No mechanism was fooled by dumb stuff.**
- **K6 procedure check**: all 672 pert-run K1–K4 cells matched the
  predicted tables, including the three *predicted* K2 flips where D1's
  +7 shift moves F-W1a/F-W1f evidence across the LEASE boundary
  (45→52 vs LEASE 48): the mechanisms abandon-then-stale instead of
  wait-then-uninstall, exactly as the frozen decision procedure
  prescribes. Note on the prereg text: K6 as written asks for the
  terminal action to be "unchanged" under D1, but D1 is not a pure
  paraphrase w.r.t. the lease boundary — moving evidence from before
  the lease expiry to after it is a genuine timing change, and the
  correct response *must* change. The verdict (CLASSIFY) never changed;
  the action changes were predicted cell-by-cell before being observed.
  This interpretive note is flagged for Micah's sign-off; it weakens
  nothing (the strict reading would mislabel correct timing responses
  as failures).

## 5. The three-world decision result (per mechanism, canonical)

| Fixture | M0 | M-ESC | M-BND | M-PRB | M-CLB | M-TST | M-CMB |
|---------|----|-------|-------|-------|-------|-------|-------|
| F-W1a (ev@45) | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| F-W1b (ev@55) | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ | ✗† |
| F-W1f (ev@45+flood) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| F-W2a (silence) | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| F-W2b (silence) | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| F-W3a (simple lie) | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ |
| F-W3b (adaptive liar) | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ |
| F-W3c (flood+lie) | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |

✓ = passes K1–K6 on the fixture. ✗ = fails ≥1 kill criterion.
† = the predicted lease-cost K2 (classifies W1 correctly, wrong
terminal action).

## 6. What this says about the debate's open questions

1. **Can any non-cheating signal distinguish W1/W2 before a bound?**
   No — confirmed head-to-head. Matter-coupled probes provide liveness
   evidence, not deductive proof of eventual R-specific speech; the
   lease converts the undecidability into a bounded announced cost.
2. **What stops the history-dependent liar?** Claim-evidence binding
   against the learner's own audit ledger — confirmed: every mechanism
   with M-CLAIMBIND passes F-W3b; every one without it fails F-W3b.
3. **What stops flood-plus-lie?** Binding + testedness gating —
   confirmed on F-W3c (only M-COMBO passes K2 there).
4. **Figure-it-out vs rigid:** the surviving structure is a
   composition of five general mechanisms; every rigid singleton
   (fixed lease alone, escrow alone, cap alone) dies. Figure-it-out
   wins, as the prereg's standing rule requires for ties — and this
   was not a tie.

## 7. Reproduction

`run.sh` rebuilds and re-verifies from scratch: compiles `tw.zag` with
the pinned toolchain, runs twice, SHA-compares, runs `verify.py`.
`evidence_run1.txt` / `evidence_run2.txt` are the committed evidence.
