# IU4-ADV RESULT: H-INTENT-UNIFIED Red Team

## Verdict: H-INTENT-UNIFIED DOWNGRADED (not killed)

Two of four preregistered attacks succeeded. Both hit the scoring
design inherited from H-INTENT, not the port: the 20/20 frozen
checks still pass and the port is faithful (X-IU4). The downgrade
is that the "intent inference" framing promises more than the
scoring rule delivers: the ambiguity guard is bypassable by
learn-order interleaving, and the condition-firing heuristic can
override the learner's own exact training evidence.

## X-IU1: SUCCESS (downgrade) - recency bypass of the ambiguity guard

Baseline workspace (adjacent learns): broadcast n=5 (seq 0) then
reverse n=5 (seq 1). Query "hello": scores 10000 vs 10001, gap 1,
kind -2, WITHHOLD AMBIGUOUS. As predicted.

Attack workspace: identical A (broadcast n=5, seq 0) and B
(reverse n=5, seq 3), identical training of A and B, but two
unrelated learns interleaved (reverse n=3 seq 1, reverse n=4
seq 2; both length-general per K-U1, apply to "hello" with
len_match 0). Query "hello": candidates score 10000, 1, 2, 10003.
Top B, second A, gap 3 >= 2. kind 0. Answers "olleh".

The identical query with identical competitors and identical
competitor training goes from honest WITHHOLD to a confident
answer purely because two unrelated procedures were learned in
between. The seq difference carries zero information about the
querier's intent for "hello". This contradicts the builder's own
rationale for the gap rule (PREREG_INTENT_AMEND1: "Gap < 2 with
equal signals means adjacent learning events with no distinguishing
basis - the learner does not guess silently"): in the attack
workspace the query-relevant signals are equal (cond_fire 0,
len_match 1 for both A and B), so by that rationale there is no
distinguishing basis, yet the mechanism picks. The mechanism does
guess silently whenever 2+ learning events separate two equally
matching candidates.

Repair direction (not implemented by the red team): the ambiguity
guard should use only query-informative score components
(cond_fire, len_match), or recency must not break ambiguity ties.
A principled rule: withhold whenever the top two candidates tie
on all query-informative signals, regardless of seq gap.

## X-IU2: SUCCESS (downgrade) - cond_fire dominance over exact training evidence

Workspace: D = reverse on x-words n=3 ("xqw>wqx;xab>bax",
direct slot 0, seq 0, tlen 3). Bridge rule from the builder's own
proven training (seq 1, tlen -1, condition input[0] == 120,
confirmed in-trial).

Query "xqw" (n=3): D applies -> "wqx", len_match 1, score 10000.
Bridge applies, cond_fire 1, len_match 0, score 20001. Gap 10001.
Winner: bridge. Answer "xxx".

"xqw" appears VERBATIM in D's training ("xqw>wqx"). The 20000-point
condition heuristic overrides the learner's own explicit training
evidence for that exact input. The scoring has no exact-match or
specificity signal: a single coincidentally-firing byte condition
defeats stored experience.

Repair direction: add an exact-training-input-match term that
dominates cond_fire, or cap cond_fire below an exact-match bonus.
Specificity (exact stored evidence beats generalization) is the
standard principle violated here.

## X-IU3: BOUNDARY (informational, as preregistered)

Control (builder's B-T1 shape): reverse n=4 then broadcast n=5.
Query "abcd" -> "dcba" via the n=4 reverse slot. Matches B-T1b.

Attack (swapped lengths): reverse n=5 (seq 0, tlen 5) then
broadcast n=4 (seq 1, tlen 4). Query "abcd" (n=4): reverse applies
-> "dcba", len_match 0, score 0; broadcast applies -> "dddd",
len_match 1, score 10001. Winner: broadcast. Answer "dddd".

The reverse program is the identical length-general program in
both workspaces (length generality established by K-U1); only the
incidental uniform-training-length label differs, yet the answer
to the identical query flips from "dcba" to "dddd". The 10000-point
len_match term has no causal link to procedure competence but
dominates selection over any recency difference under 10000
learns. Recorded as a boundary of the declared heuristic, not a
bar violation: len_match is the mechanism's declared
disambiguator, and no frozen bar covers this case.

## X-IU4: PASS - port faithful

1. intent_winner, intent_trace_emit, intent_init,
   intent_record_proc, intent_record_br: decision logic identical
   between intent_learn.zag and unified_learn.zag (compared by
   reading both; same candidate loops, scoring formulas,
   top/second/gap logic, return conventions).
2. Bridge candidacy lacks the learn_seq >= 0 check in BOTH files:
   faithful port of a latent asymmetry in the original, not a
   port bug. No unrecorded bridge rule is constructible in the
   unified learner: bridge_learn has exactly one call site
   (handle_proc_learn_unified), which records intent on every
   success path. Latent only.
3. Address range 1560..1724: only the intent functions reference
   IBASE()/SEQADDR(). Causal store ends at 1552, WORK starts at
   2048. No collision, no other writer.
4. handle_proc_query_unified delegates to
   handle_proc_query_intent with the same return convention
   (1 answered, 0 withhold-none, -1 withhold-ambiguous).
5. intent_init called for every fresh workspace in main()
   (W, W1, W2, W3, W4).
6. No slot-reuse staleness: proc_store allocates first-free and
   never frees (the FLEAKFIX rollback only undoes the current
   failed attempt's allocations, which never held intent
   records). Each slot is written at most once, so intent records
   cannot go stale. Bridge sub-procedure slots keep seq -1 and
   stay excluded from candidacy, per PREREG_INTENT_AMEND1.

## What the downgrade does and does not mean

The 20/20 frozen H-INTENT-UNIFIED checks still pass; nothing about
the port is broken. The claim "the unified learner infers intent
instead of spraying" holds for the tested battery. What fails is
the stronger implicit guarantee: that WITHHOLD means "genuinely
ambiguous" (X-IU1 shows the verdict is learn-order dependent) and
that the winner is the best-supported candidate (X-IU2 shows a
20000-point heuristic can defeat verbatim training evidence).
Classification remains bounded L2 integration infrastructure; the
downgrade narrows the reliability claims, it does not allege
representational failure.

## Evidence

- Prereg: PREREG_IU4_ADV.md (commit 2c25b011d), frozen before any
  attack code was written or executed. Commit order: prereg
  strictly precedes implementation.
- Attack source: iu4_adv.zag (copy of unified_learn.zag v2 with
  main() replaced by the X-IU1/X-IU2/X-IU3 scenarios; all shared
  machinery byte-identical to the claimed implementation).
- Raw output: IU4_ADV_RAW.txt (authoritative;
  md5 612991f6cec884bf360e6b4e5d3d10c3 across 3/3 runs).
- Toolchain: znc 2026.07.0-dev (edition 2026), pinned.
- Binary not committed (repo convention); rebuilds via
  znc iu4_adv.zag -o iu4_adv.

## Governance

Pure Zag throughout. No Python used at any stage: no generators,
no verifiers, no analysis scripts, no scratch tooling. No em
dashes in new documentation or code. Only adversary-owned files
staged and committed; no other agent's files touched.
