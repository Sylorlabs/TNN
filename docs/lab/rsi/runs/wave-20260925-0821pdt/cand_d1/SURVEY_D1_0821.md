# D1 Intelligence-Lane Survey: wave-20260925-0821pdt (Phase 1)

Worker: D1 (intelligence lane). Status: NO-CANDIDATE. No prereg written; nothing to implement this phase. This memo records the survey so the coordinator can verify the reasoning or redirect.

## Survey method

Read the tail of LOOP_STATE.md (waves 20260923-1121pdt through 20260925-0521pdt verdict sections), extracted every VERIFIED intelligence-metric number, ranked the five metrics (truthfulness under adversarial pressure; genuine learning that persists after scaffold disconnect; deliberation quality; integrity/no-gaming; capability breadth), and tested candidate ideas against the standing closures.

## Metric ranking (verified numbers quoted)

1. Truthfulness under adversarial pressure: STRONG.
   - CV-1 decline-citation fix, ADOPT [RE-CERT] (20260924-1721pdt): CVC-B1 30/30 honest resolutions, zero unflagged confabulations (bar >=24/30); CVC-B2 20/20 payload naming; CVC-B3 0 coverage violations (97/97 quoted decline words KB-absent); CVC-B4 10/10 paraphrases; CVC-B5 17/17 INKB byte parity (db6b7075), 30/30 ADV declines, 0 blanket refusals; CVC-B6 1.73x ops (bar 10x); CVC-B7 3/3 byte-identical.
   - CV-1 fallback measurement (20260925-0221pdt): M1 24/24 honest resolutions (8/8 truthful fallback firings); M2 0 unflagged confabulations; M3 0 false coverage claims.
   - CV-P stemmed-coverage gate, PARTIAL (20260925-0521pdt): B1 30/30, B2 inflection recall 10/10, B5 0 violations, B7 1.0626x. Rotated-author re-test runs this wave (cvp_retest/).
   - CLAIM-VERIFY-1, ADOPT (20260924-1121pdt): CV-B1 24/30 exactly at bar (6 specificity misses, not honesty misses).

2. Integrity/no-gaming: STRONG. Coverage-truth bars 0 violations on every wave; gaming probes declined (CV-1 sealed 30: all declined; CLAIM-VERIFY-1: all 20 adversarial and gaming probes declined, none jailbroken).

3. Genuine learning that persists after scaffold disconnect: NO VERIFIED NUMBER EXISTS. No wave has ever measured it; no learning machinery is in loop scope. Cannot be the weakest VERIFIED metric.

4. Capability breadth: NO VERIFIED NUMBER EXISTS. The only breadth engine in the record (N4 analog-native, math R3) is Micah's own frontier work, closed to the loop.

5. Deliberation quality: WEAKEST VERIFIED METRIC. Adversarial FIR on the trades deliberation battery, five failed mechanism classes:
   - D-SEARCH (20260923-2021pdt): KB-T1 4230 pm (A) / 5365 pm (B) vs 1000 pm bar; miss 32.3pp (A), 43.7pp (B). KB-T3 arm-A adversarial recall collapsed 43.95pp (6043 to 1648 pm). FAIL, DISCARDED.
   - Ensemble OVT5 (20260923-2021pdt): KB-T1 40.74% (A) / 54.13% (B) vs 10% bar; Q1..Q7 frontier floor 31.81% (A) / 53.68% (B), unreachable by construction. B-arm overturns anti-selective (withheld true installs 32.9% vs adversarial-false 18.1%). FAIL, DISCARDED.
   - Trades Candidate A K=5/K=7 (20260923-1421pdt): ENS5 adversarial FIR 8/23 = 34.78% (A), 55/101 = 54.46% (B); KB-T1 FAIL both arms; KB-T3 FAIL all four recall legs. FAIL.
   - ITER-FP v1 (20260923-2021pdt): FAIL/discard.
   - SHAPED-MEMBERS (20260924-0221pdt): SM-T1 A 5895 pm vs bar 4895, B 5514 pm vs bar 4496 (FAIL); SM-T4 A 4390 vs 2474, B 5714 vs 5574 (FAIL). Red-team R1 is a proof: monotone reshaping preserves the R0 blocker relation exactly. DISCARD [VOID].
   - KB4 substrate deliberation is ADOPTED and passing (collapse-abstention KB1 14/44 = 31.82% < 48.00%; KB4V2 T4 50.00% < 54.0%), but the residual 14 falses split 7 into Micah's closed FS-F2C front (98.58%) and 7 motiondir uncorrelated tail. Second-path part C: DISCARD [VOID] (SP-B1 1891 bp (7/37) vs bar strictly below 1842 bp (7/38)).

## Standing closures blocking the deliberation lane

- S4: vote aggregation over the seven frozen orderings of frozen R0 is closed.
- S11 (hypothesis-class level, 20260924-0221pdt debate): monotone confidence reshaping is closed; "no fresh attempt on monotone confidence reshaping."
- D-SEARCH / ITER-FP contradiction-free fixed-point family: closed.
- M4 R2 (20260924-0521pdt): veto-only second path on the KB4V2 substrate is closed; reopen only if residual falses exist inside the vetoed tasks.
- Collision rule (20260924-1121pdt): T2 colorconst falses live in Micah's closed FS-F2C front (FINAL ALIVE, 98.58%); the loop does not re-litigate his closed work.

## Candidate ideas considered and rejected

1. Non-monotone confidence reshaping: outside the S11 letter but inside its evident purpose; unprincipled (destroys the confidence semantics the blocker relies on); no theory for selective FIR reduction. Rejected as closure-gaming.
2. Corroboration-gated install / stronger blocking: the verified withhold-to-win disease predicts failure (OVT5 withheld true installs at nearly double the adversarial-false rate, 32.9% vs 18.1%; D-SEARCH recall collapsed 43.95pp). Rejected on evidence.
3. Blocker-margin weakening (block only on strict margin): wrong direction; increases installs, raises FIR. Rejected.
4. Contradiction-predicate change: no mechanistic theory; the fooling is systematic (5/6 tasks show 100% adversarial path agreement), so predicate narrowing has no verified foothold. Rejected as guessing.
5. Contest (non-veto) second judgment path on the trades battery: the "not a data-split" requirement cannot be satisfied with a specified algorithm in Phase 1; no framable kill bar. Rejected as not framable.
6. Motiondir-7 uncorrelated tail: N=7, no mechanistic theory, underpowered bar. Rejected as padding.
7. T2-targeted veto: collides with Micah's closed FS-F2C front. Rejected under the collision rule.
8. Stacking adopted components (KB4V2 + collapse-abstention + CF2): not a genuinely new mechanism; the C12 confounded-stack precedent (governance ruling 5) warns against stacks. Rejected.

## Conclusion

NO-CANDIDATE. The weakest verified intelligence metric is deliberation quality (trades-battery adversarial FIR, five failed classes quoted above), but every mechanism class with a verified foothold is closed by standing rule or voided verdict, the remaining KB4 falses sit in Micah's closed front or an N=7 uncorrelated tail, and the ideas outside the closures are either unprincipled, evidence-predicted to fail, or not framable with a frozen kill bar in Phase 1. Forcing a candidate would be padding. The honest action is to stand down this lane this wave and let the coordinator redirect (e.g., hold D1 for a future wave, or reassign).

Note: cand_d2/ was empty at survey time; if D2 proposes in the deliberation lane, the coordinator should check for overlap with the closures listed above.
