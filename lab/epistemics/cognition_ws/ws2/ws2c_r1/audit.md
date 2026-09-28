# WS2-C deliberation audit (TNN native deliberative control)
I have read the failure evidence: 43 per-query miss lines across 3 prior arms; 8 white-box fail records.
goal:  100% retrieval everywhere; TNN finds its own way; figure-it-out wins ties.
visible evidence: 51 WS2-A probes over 34 items; 48 MORG design queries over 240 items.
seal check: PASS - no holdout files staged; H01-H12 unseen by me.

## round 1 scheme=(STRICT,COUNT,NEVER,NONE)
observation: misses=30 (probe=21 morg=9) [F_ABSTAIN=17 F_HINT_EXCLUDE=7 F_DILUTE=0 F_CLUSTER=2 F_UNCLASSIFIED=4 ]
P-AGE symmetry: aged misses 0/5, recent misses 0/5 - no install-order bias.
trying M_AB1(ZERO)
hypothesis: the 17 F_ABSTAIN misses (QX101,QX102) are probes whose gold set is empty: the scheme cannot say 'not found' and fills top-k with score-0 junk. ZERO returns empty when the best score is 0. prediction: the 17 F_ABSTAIN misses go to 0 with no regressions elsewhere.
trial result: misses 30 -> 26; regressions=2; F_ABSTAIN after=19. prediction VIOLATED. decision: REJECT M_AB1(ZERO) (regressions).

## round 2 scheme=(STRICT,COUNT,NEVER,NONE)
observation: misses=30 (probe=21 morg=9) [F_ABSTAIN=17 F_HINT_EXCLUDE=7 F_DILUTE=0 F_CLUSTER=2 F_UNCLASSIFIED=4 ]
P-AGE symmetry: aged misses 0/5, recent misses 0/5 - no install-order bias.
trying M_HM1(VERIFY)
hypothesis: the 7 F_HINT_EXCLUDE misses (Q41,Q42) are probes whose hints exclude gold items that carry text evidence. VERIFY drops a hint only when it contradicts ALL text evidence (max score under the hint is 0 while dropping it scores >0). prediction: the 7 F_HINT_EXCLUDE misses go to 0 with no regressions elsewhere.
trial result: misses 30 -> 17; regressions=0; F_HINT_EXCLUDE after=3. prediction VIOLATED. decision: ADOPT M_HM1(VERIFY).

## round 3 scheme=(VERIFY,COUNT,NEVER,NONE)
observation: misses=17 (probe=10 morg=7) [F_ABSTAIN=6 F_HINT_EXCLUDE=3 F_DILUTE=0 F_CLUSTER=4 F_UNCLASSIFIED=4 ]
P-AGE symmetry: aged misses 0/5, recent misses 0/5 - no install-order bias.
trying M_HM2(SOFT)
hypothesis: the 3 F_HINT_EXCLUDE misses (Q42,Q44) remain after VERIFY: the contradicting hint survives verification because stopwords give it nonzero score. SOFT demotes hints to +10 bonuses so text evidence decides. prediction: the 3 F_HINT_EXCLUDE misses go to 0 with no regressions elsewhere.
trial result: misses 17 -> 19; regressions=2; F_HINT_EXCLUDE after=0. prediction HELD. decision: REJECT M_HM2(SOFT) (no improvement) (regressions).

## round 4 scheme=(VERIFY,COUNT,NEVER,NONE)
observation: misses=17 (probe=10 morg=7) [F_ABSTAIN=6 F_HINT_EXCLUDE=3 F_DILUTE=0 F_CLUSTER=4 F_UNCLASSIFIED=4 ]
P-AGE symmetry: aged misses 0/5, recent misses 0/5 - no install-order bias.
trying M_EX1(CLUSTER)
hypothesis: the 4 F_CLUSTER misses (Q39,Q40) show partial subject-cluster signal: some members carry the text token, others share only the subject. CLUSTER completes a subject when >=half its members are provisionally retrieved and at least one scores >0. prediction: the 4 F_CLUSTER misses go to 0 with no regressions elsewhere.
trial result: misses 17 -> 17; regressions=0; F_CLUSTER after=4. prediction VIOLATED. decision: REJECT M_EX1(CLUSTER) (no improvement).

## round 5 scheme=(VERIFY,COUNT,NEVER,NONE)
observation: misses=17 (probe=10 morg=7) [F_ABSTAIN=6 F_HINT_EXCLUDE=3 F_DILUTE=0 F_CLUSTER=4 F_UNCLASSIFIED=4 ]
P-AGE symmetry: aged misses 0/5, recent misses 0/5 - no install-order bias.
conclusion: no improving move remains in the palette. Stopping with 17 misses; per-class diagnosis above.

# final scheme
I chose: VERIFY,COUNT,NEVER,NONE.
adopted moves: M_HM1(VERIFY)
visible misses remaining: 17.
