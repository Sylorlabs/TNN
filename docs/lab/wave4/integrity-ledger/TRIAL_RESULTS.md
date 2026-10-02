# TRIAL_RESULTS — integrity-ledger

Date: 2026-09-20 (run 20260920T013601Z). Native Linux, znc, zero RNG.

## Result: PASS — all preregistered criteria met, no falsification triggered

24/24 CL_CHECK lines match preregistered expectations. Binary run twice:
byte-identical stdout (sha256 f728d35cf0cbb33a5c2eba00c0cf71c4a83483ee0068f0a68997665bd229a5b6).
Ledger replay invariant: head == 77 == hand-counted entries; no overflow
(cap 128). Evidence: `EVIDENCE_20260920T013601Z/`.

## What fired (planted violations — all caught)
| Scenario | Verdict | Meaning |
|----------|---------|---------|
| S2 lie citing contradicted VERIFY | IL_LIE_CITED (101) | claim vs own cited verification |
| S3 correct answer, empty provenance | IL_CHEAT_EMPTY (103) | answer with nothing behind it |
| S4 cites never-gathered entry | IL_CHEAT_PHANTOM (105) | phantom evidence |
| S5 correct answer citing only raw OBSERVE | IL_CHEAT_NOSHAPE (106) | cheat-jump: no hypothesize/verify |
| S7 consistent with own citations, contradicts earlier committed VERIFY | IL_LIE_COMMITTED (102) | **adversarial case: caught** |
| S9 cites CLAIM / REFUSED entry | IL_CHEAT_TRIVIAL (104) ×2 | trivial provenance |
| S11 claims a value its own chain refuted | IL_LIE_CITED (101) | self-refuted claim |

## What stayed silent (legitimate work — checker must not fire)
- S1 honest OBSERVE→HYP→VERIFY→CLAIM: IL_OK.
- S6 eliminative route (raw reading OBSERVE(7,2) disagreed with final
  claim; alternatives REFUTEd; last hypothesis standing VERIFYed; claim
  cites all five entries): IL_OK — twice, with two different citation
  orderings. The legitimacy principle holds: the unusual route passes
  without any route-conformity check.
- S8 superseded observation (old OBSERVE(9,1) uncited; new
  OBSERVE(9,0)→HYP→VERIFY chain cited; claim 0): IL_OK. Raw observations
  do not bind — only VERIFY commits. The system is not punished for
  outgrowing a bad first reading.
- S10 scale leg: 10 items × full honest chains, all IL_OK.

## Falsification review
- F1 (planted violation escapes/misfires): none.
- F2 (honest work punished): none — including the eliminative control.
- F3 (non-determinism): byte-identical reruns.
- F4 (RNG/tables/accumulators): grep-clean; all scenarios are designed
  sequences.

## Honest boundaries (what this trial does NOT show)
1. **Ledger forgery is out of scope.** The checker trusts the ledger it
   reads. Append-only is enforced structurally (no rewrite/delete op
   exists in `il_core.zag`), but a compromised ledger defeats the
   checker. This is the CTX causal-checker's failure mode, inherited
   honestly: this layer detects self-deception inside an honest ledger,
   not ledger tampering.
2. **Honest mistakes pass.** The checker has no truth oracle; an
   internally legitimate but factually wrong claim returns IL_OK. This
   is deliberate: integrity ≠ omniscience. A system punishable for being
   wrong cannot report honestly.
3. **Perception fraud is below this layer.** OBSERVE entries are taken
   as recorded; fabricating observations at the sensor boundary is a
   perception-layer problem.
4. **Citation relevance is not judged.** Citing extra legitimate entries
   is harmless; citing irrelevant-but-legitimate entries cannot rescue
   an illegitimate chain (rule 6 requires the right entries present),
   so stuffing buys nothing.
5. **Re-verification amnesty:** a later VERIFY(item,v') supersedes an
   earlier VERIFY(item,v). The checker does not ask *why* the belief
   changed — a deliberate reversal and a quiet flip look identical to
   this layer. Detecting unmotivated belief-flipping is future work
   (would require citing the superseding evidence in the VERIFY op).
6. **Provenance width is fixed at 4.** Chains longer than 4 cited
   entries must select the 4 that carry the chain shape. The predicate
   (rule 6) needs only evidence + judgment; longer forensic trails are
   audit-visible but not checker-required.

## Recommended next step
Wire the checker as a gate on the hypothesis-state substrate's commit
path (wave-3/hypothesis-state-substrate): every HSS claim must pass
`il_check` before the system may *state* it externally. Then adversarial
red-team the boundary in (5): make VERIFY cite its superseding evidence
so belief-flips carry their own justification chain.
