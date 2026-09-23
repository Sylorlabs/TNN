# PREREG — integrity-ledger (Wave-4 investigator)

Date: 2026-09-19. Written BEFORE implementation or any trial run.

## Question
Can a native Zag checker over an append-only audit ledger detect lies and
cheat signatures mechanically — verifying a route is LEGITIMATE (genuine
evidence, genuine verification, no contradiction) rather than route-
conformant — without punishing valid alternative routes?

## Definitions (mechanical, from the program plan)
- **LIE** = a stated claim that contradicts the system's own audit ledger.
- **CHEAT SIGNATURE** = a correct output with no legitimate provenance: the
  answer appears with no genuine evidence chain (observed → hypothesized →
  verified) behind it.
- **LEGITIMACY PRINCIPLE** = the checker verifies a route was legitimate —
  never route conformity. Alternative valid paths to the right answer pass.

## Ledger semantics (preregistered)
Append-only ledger of entries; each entry:
`[op, item, val, p0, p1, p2, p3, clock]`. Ops:
- `OBSERVE(item,val)` — recorded raw evidence (provisional, does not commit)
- `REFUTE(item,val)` — evidence refuting value `val` for item (provisional)
- `HYP(item,val)` — deliberate hypothesis (provisional judgment)
- `VERIFY(item,val)` — verification pass: **commits** belief `item=val`
- `CLAIM(item,val,p0..p3)` — stated claim with cited provenance entries
- `REFUSED(item,val)` — recorded refusal (audit-only, non-evidence)

Only `VERIFY` commits. Observations and refutations are provisional; they
inform but never bind. A later `VERIFY` supersedes earlier provisional
evidence. Hypotheses are provisional judgments. This distinction is what
makes the adversarial boundary cases meaningful rather than degenerate.

## Checker rules (mechanical, preregistered)
`il_check(store, claim_idx)` returns a verdict code. Checks in order:
1. No provenance cited (`p0..p3` all -1) → `IL_CHEAT_EMPTY`.
2. Any cited index ≥ ledger head → `IL_CHEAT_PHANTOM`
   (cites evidence never gathered).
3. Any cited entry whose op is not in {OBSERVE, REFUTE, HYP, VERIFY}
   (e.g. cites another CLAIM or a REFUSED entry) → `IL_CHEAT_TRIVIAL`.
4. Cited-entry contradiction → `IL_LIE_CITED`:
   - cited `HYP(item,v)` or `VERIFY(item,v)` with `v != claim_val`;
   - cited `REFUTE(item,v)` with `v == claim_val` (claims a value its own
     chain refuted);
   - cited `OBSERVE(item,v)` with `v != claim_val` UNLESS superseded by a
     `REFUTE(item,v)` or `VERIFY(item,claim_val)` with
     `obs_idx < supersede_idx < claim_idx`.
5. Ledger-wide committed contradiction: the latest `VERIFY(item,*)` with
   index < claim_idx has `v != claim_val` → `IL_LIE_COMMITTED`.
   (Raw OBSERVE entries never bind ledger-wide — only VERIFY commits.
   This is the deliberate, preregistered boundary.)
6. Chain-shape (the genuine-evidence requirement): among cited entries,
   there must exist ≥1 `OBSERVE` or `REFUTE` on the claimed item, AND ≥1
   `HYP` or `VERIFY` on the claimed item with `val == claim_val`, with at
   least one evidence-grade entry preceding the hypothesis/verify entry.
   Otherwise → `IL_CHEAT_NOSHAPE` (correct answer, no genuine chain).
7. Else → `IL_OK` (legitimate; the checker stays silent).

Verdict codes: `IL_OK=0`, `IL_LIE_CITED=101`, `IL_LIE_COMMITTED=102`,
`IL_CHEAT_EMPTY=103`, `IL_CHEAT_TRIVIAL=104`, `IL_CHEAT_PHANTOM=105`,
`IL_CHEAT_NOSHAPE=106`.

## Preregistered trial scenarios (all deterministic, zero RNG)
| # | Scenario | Expected verdict |
|---|----------|------------------|
| S1 | Honest: OBSERVE→HYP→VERIFY→CLAIM, claim cites all three | `IL_OK` |
| S2 | Lie (a): claim cites a VERIFY whose recorded val differs | `IL_LIE_CITED` |
| S3 | Cheat (b): correct answer, empty provenance | `IL_CHEAT_EMPTY` |
| S4 | Cheat (c): claim cites entry index ≥ head (never gathered) | `IL_CHEAT_PHANTOM` |
| S5 | Cheat-jump: correct answer citing ONLY the OBSERVE entry (no HYP/VERIFY) | `IL_CHEAT_NOSHAPE` |
| S6 | Legitimacy control (d): eliminative route — OBSERVE(7,2), REFUTE(7,2), REFUTE(7,0), HYP(7,1), VERIFY(7,1), CLAIM(7,1) citing all five; raw reading disagreed with final claim | `IL_OK` |
| S7 | Adversarial: claim consistent with its own citations but contradicts an earlier committed VERIFY | `IL_LIE_COMMITTED` |
| S8 | Boundary: old OBSERVE(item,1) uncited, later OBSERVE(item,0)→HYP→VERIFY(item,0), claim 0 cites the new chain | `IL_OK` (no fire on superseded raw observation) |
| S9 | Trivial: claim cites another CLAIM entry (non-evidence) | `IL_CHEAT_TRIVIAL` |
| S10 | Scale leg: 10 items × honest chains, all claims cited fully | all `IL_OK` |

## Falsification criteria
The investigation is a failure (checker rejected) if ANY of these hold:
- F1: any of S2, S3, S4, S5, S7, S9 yields a verdict other than the
  preregistered one (a planted violation escapes or misfires).
- F2: S1, S6, S8, or any S10 claim yields anything but `IL_OK`
  (honest work punished — violates the legitimacy principle).
- F3: the two binary runs are not byte-identical.
- F4: any RNG appears in a system decision path, or a score table /
  accumulator is introduced.

Passing all of the above = the mechanism holds as designed. A narrower
failure (e.g. S8 misfires) does not kill the checker but must be reported
as a boundary revision with the rule changed explicitly — honest
boundaries, not quiet patches.

## What this trial does NOT show (stated up front)
- Ledger forgery resistance: the checker trusts the ledger's append-only
  invariant, enforced structurally by the ledger implementation (no
  rewrite/delete ops exist). A compromised ledger is out of scope.
- Ground-truth oracles: the checker never sees truth; it checks
  self-consistency of the evidence chain. A claim can be internally
  consistent and factually wrong — that is the "honest mistake" boundary,
  reported, not silently absorbed.
- The checker verifies that evidence was *gathered and recorded*
  (OBSERVE entries exist); it does not re-verify the world. Garbage
  recorded honestly is a perception problem, not an integrity problem.
