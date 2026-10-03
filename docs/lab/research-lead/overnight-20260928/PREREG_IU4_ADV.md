# PREREG IU4-ADV: H-INTENT-UNIFIED Red Team (FROZEN)

## Standing assumption

Assume H-INTENT-UNIFIED is false. Attack the claim: the unified
learner infers which stored procedure or bridge rule the querier
intends (scoring cond_fire*20000 + len_match*10000 + learn_seq,
gap >= 2 selects, otherwise WITHHOLD AMBIGUOUS) instead of spraying
all slots and rules. H-INTENT-UNIFIED SURVIVES is the verdict under
attack (20/20 checks, 4/4 bars, commits d959ff51f prereg and the
v2 implementation in unified_learn.zag).

## Attack X-IU1: recency bypass of the ambiguity guard

Theory. learn_seq is a global monotonic counter bumped by every
learn event. Two procedures with identical query-relevant signals
(same cond_fire, same len_match) are distinguished ONLY by seq.
The gap < 2 guard withholds only when the two competing learns were
adjacent in global learn order. Inserting 2 or more unrelated
learning events between the two competing learns inflates the seq
gap to >= 2, converting an honest WITHHOLD into a confident pick.
The seq difference carries zero information about the querier's
intent for this query: the intervening learns are unrelated to both
competitors and to the query.

Construction (all via handle_proc_learn_unified on fresh workspaces,
query via intent_winner/handle_proc_query_unified).

- Baseline workspace WB. Learn A = broadcast n=5
  ("abcde>eeeee;fghij>jjjjj", seq 0, tlen 5). Learn B = reverse n=5
  ("abcde>edcba;vwxyz>zyxwv", seq 1, tlen 5). Query "hello".
  Predicted scores: A = 10000, B = 10001, gap = 1 -> kind -2,
  WITHHOLD AMBIGUOUS.
- Attack workspace WA. Learn A (seq 0, tlen 5). Learn dummy1 =
  reverse n=3 ("abc>cba;def>fed", seq 1, tlen 3). Learn dummy2 =
  reverse n=4 ("abcd>dcba;wxyz>zyxw", seq 2, tlen 4). Learn B
  (seq 3, tlen 5). Query "hello". Dummies are length-general
  procedures (K-U1), so they apply to "hello" with lm = 0.
  Predicted scores: A = 10000, dummy1 = 1, dummy2 = 2, B = 10003.
  Top B, second A, gap = 3 -> kind 0, answers "olleh".

Kill criterion. If WB withholds (kind -2) AND WA answers (kind 0)
for the identical query "hello" with identical competing
procedures A and B and identical training of A and B, then the
ambiguity guard is bypassed purely by learn-order interleaving.
The mechanism guesses silently on recency, contradicting the
builder's own rationale for the gap rule (PREREG_INTENT_AMEND1:
"Gap < 2 with equal signals means adjacent learning events with no
distinguishing basis - the learner does not guess silently"). In WA
the query-relevant signals are equal (cond_fire 0, len_match 1 for
both A and B); per that rationale there is no distinguishing basis,
yet the mechanism picks. Verdict on success: H-INTENT-UNIFIED
DOWNGRADED. The ambiguity guard is ineffective under learn-order
perturbation; recency must not break ambiguity ties, or the guard
must use only query-informative signals. This is as-designed
behavior (recency is a declared signal), so the flaw is in the
design, not the port: DOWNGRADE, not KILL. The 20/20 frozen checks
are unaffected.

## Attack X-IU2: cond_fire dominance over exact training evidence

Theory. The cond_fire term (20000) dwarfs every other signal. A
bridge rule whose single-byte condition fires on the query always
beats a direct procedure, even when the query EXACTLY matches the
direct procedure's training input. The scoring has no exact-match
or specificity signal.

Construction.

- Workspace WX. Learn D = reverse on x-words n=3
  ("xqw>wqx;xab>bax", seq 0, tlen 3, direct slot).
- Learn the builder's own proven bridge training
  ("xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee", seq 1, tlen -1,
  condition input[0] == 120). Direct discovery fails on this set
  (established by K-U2a); the pre-existing slot-0 reverse does not
  affect discovery, which runs over the pair set.
- Query "xqw" (n=3). D applies -> "wqx", lm = 1, score = 10000.
  Bridge applies, cf = 1, lm = 0, score = 20001. Predicted winner:
  bridge, answers "xxx".

Kill criterion. If the query "xqw", which appears VERBATIM in D's
training ("xqw>wqx"), is answered "xxx" by the bridge rule instead
of "wqx" by D, then the 20000-point heuristic overrides the
learner's own explicit training evidence for that exact input.
Verdict on success: H-INTENT-UNIFIED DOWNGRADED. Intent scoring can
contradict stored experience; a specificity or exact-match signal
is missing.

## Attack X-IU3: len_match dominance without causal link to competence

Theory. The len_match term (10000) selects between procedures by
the incidental uniform training-input length, even though the
procedures are length-general (K-U1 proved reverse generalizes
across lengths). A coincidental length match beats any recency
difference under 10000 learns. This attack is INFORMATIONAL: no
frozen bar is violated and len_match is the declared
disambiguator. A demonstrated flip is recorded as a BOUNDARY
finding, not a kill.

Construction.

- Control workspace WC. Learn reverse n=4 ("dcba>abcd;wxyz>zyxw",
  seq 0, tlen 4). Learn broadcast n=5 ("abcde>eeeee;fghij>jjjjj",
  seq 1, tlen 5). Query "abcd" -> predicted "dcba" via the n=4
  reverse slot (mirrors the builder's B-T1b).
- Attack workspace WY. Learn A = reverse n=5
  ("abcde>edcba;vwxyz>zyxwv", seq 0, tlen 5). Learn B = broadcast
  n=4 ("abcd>dddd;wxyz>zzzz", seq 1, tlen 4). Query "abcd" (n=4).
  A applies -> "dcba", lm = 0, score = 0. B applies -> "dddd",
  lm = 1, score = 10001. Predicted winner: B, answers "dddd".

Record as BOUNDARY if demonstrated. The reverse program is the
identical length-general program in WC and WY; only the incidental
tlen label differs, yet the answer to the identical query flips
from "dcba" to "dddd". The 10000-point term has no causal link to
procedure competence but dominates selection.

## Attack X-IU4: source audit of the port

Checks (by inspection; execution only to confirm where noted).

1. intent_winner, intent_trace_emit, intent_init,
   intent_record_proc, intent_record_br: decision logic identical
   between intent_learn.zag and unified_learn.zag.
2. Bridge candidacy lacks the learn_seq >= 0 check in BOTH files
   (faithful port of a latent asymmetry). No unrecorded bridge
   rule is constructible in the unified learner: bridge_learn has
   exactly one call site (handle_proc_learn_unified), which records
   intent on every success path. Latent only unless disproven.
3. Address range 1560..1724 free: causal store 1104..1552, WORK
   2048; no other writer to 1560..1724 in unified_learn.zag.
4. handle_proc_query_unified delegates to
   handle_proc_query_intent with the same return convention
   (1 answered, 0 withhold-none, -1 withhold-ambiguous).
5. intent_init called for every fresh workspace in main().
6. No slot-reuse staleness: proc_store never frees slots
   (FLEAKFIX rollback only undoes the current failed attempt,
   which never held intent records); each slot is written at most
   once, so intent records cannot go stale. Bridge sub-procedure
   slots keep seq -1 and stay excluded from candidacy.

Kill criterion. Any divergence in decision logic, address
collision, missing init, or stale-record path -> KILL (port bug)
or DOWNGRADE per severity. All checks passing -> X-IU4 PASSES
(port faithful).

## Execution plan

Pure Zag. No Python anywhere: no generators, no verifiers, no
analysis scripts. One attack binary iu4_adv.zag: a copy of
unified_learn.zag with main() replaced by the X-IU1 (baseline WB
plus attack WA), X-IU2, and X-IU3 (control WC plus attack WY)
scenarios with explicit emitted verdicts per attack. Compile with
pinned znc 2026.07.0-dev (edition 2026). Three runs; md5 over the
three raw outputs for determinism. Raw output committed as the
authoritative evidence.

## Verdict rule

- Any DOWNGRADE criterion met -> H-INTENT-UNIFIED DOWNGRADED
  (survives its frozen checks with documented scoring-design
  flaws; repairs proposed, not implemented by the red team).
- Port bug found -> KILL or DOWNGRADE per severity.
- No criterion met -> H-INTENT-UNIFIED SURVIVES the red team;
  failed attacks documented with the evidence.
