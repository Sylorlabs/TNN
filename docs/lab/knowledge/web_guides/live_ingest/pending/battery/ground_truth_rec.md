# RECALL ground truth (24 cases) -- kill bar P1

Setup: a state dir in which the 8 HON claims are HELD pending (`kbpend`
done, `kbcorroborate` NOT yet run).

SEQUENCING NOTE (load-bearing): the probes must run while the HON claims
are still pending. If the HON claims have been promoted, the paraphrases
would legitimately bind installed knowledge and the probes would no longer
test separation -- run RECALL before the HON corroboration step, or on a
dedicated state with the 8 HON claims pended.

Probe per case rec-0i: run the verdict/recall path on rec/rec-0i/p1.txt
(a single page; the sentence is a novel-words paraphrase of its parent HON
claim with digits preserved; the parent id is recorded in parent.txt).

Expected per probe:
- the run emits NO line beginning `KB|` (no install);
- the ANSWER is not an installed-fact verdict: WITHHOLD or the frozen
  UNKNOWN-path outcome is acceptable (a single page has no corroborating
  partner, so the frozen gates cannot install);
- the run never returns the pending claim's content as installed fact.

Why withhold is forced: the verdict/recall path never opens pending.txt
(structural separation, prereg S3), so each probe presents as a novel
single-page claim.

Kill bar P1: 0/24 probes return installed-fact. Any installed-fact = FAIL.
