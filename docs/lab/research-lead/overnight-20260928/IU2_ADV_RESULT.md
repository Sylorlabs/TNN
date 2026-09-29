# H-INTENT-UNIFIED2 RED TEAM RESULT

## Verdict: H-INTENT-UNIFIED2 DOWNGRADED (2 findings; frozen 5/5 bars unaffected)

The repair works inside its stated threat model. Two attacks
succeed outside it. This is a DOWNGRADE, not a kill: the frozen
K-IU2-1..K-IU2-5 bars still pass (their scenarios are unchanged),
but the "X-IU2 CLOSED" and 16-cap claims are narrower than stated.

## Preregistration

PREREG_IU2_ADV.md, commit 130109b6b, frozen before any attack
execution. Commit order verified: prereg strictly precedes harness
and evidence. Pure Zag throughout: no Python at any stage.

## X-IU2-1: em collision, verbatim-vs-verbatim (DOWNGRADE)

Setup: D2 = "xab>bax;xcd>dcx" (reverse proc, slot 0; record holds
"xab>bax" verbatim, em_D2("xab")=1 asserted). Bridge trained with
the exact F2 string "xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee"
(rule 0, condition (0,120) asserted); its record therefore ALSO
holds "xab" verbatim (as "xab>xxx").

Query "xab" trace (IU2_ADV_RAW.txt):
- proc slot 0: exact_match=1 len_match=1 score=50000
- bridge slot 0: exact_match=1 cond_fire=1 score=60000
- T DECIDE kind=1 slot=0 gap=10000 answer=[xxx]

The two training sets genuinely contradict on "xab"
("xab>bax" vs "xab>xxx"). The conflict is resolved SILENTLY by
the cond_fire heuristic term (20000 points), with no withhold.
This re-opens the exact failure mode X-IU2 was claimed to close
("the 20000-point heuristic overrides explicit training evidence
for the exact input"), now with verbatim evidence on both sides.

Finding: the em specificity term protects verbatim evidence
against a heuristic ONLY when the heuristic side has no verbatim
evidence of its own. em collisions between contradictory verbatim
records are decided by cf/lm heuristics, never withheld. The
"X-IU2 CLOSED" claim must be scoped: closed for
heuristic-vs-verbatim, open for verbatim-vs-verbatim.

## X-IU2-2: pure em tie control (PASS)

Setup: A = "abc>cba;def>fed" (reverse), B = "abc>abc;def>def"
(identity). Query "abc": both score 50000 (em=1, lm=1) ->
kind=-2 WITHHOLD AMBIGUOUS, gap 0. The tie guard works on genuine
verbatim-vs-verbatim conflicts between procs. This sharpens
X-IU2-1: the guard fails only when a heuristic term (cf or lm)
breaks the em tie, producing a confident silent pick instead of
a withhold.

## X-IU2-3: 16-cap silent degradation (BOUNDARY, confirmed)

Setup: D = 17 reverse pairs (all len 3), "tuv>vut" as the 17th.
Direct discovery succeeds (rc=0). Record inspection:
in_count=16, em_D("tuv")=0. The 17th verbatim training input is
silently dropped from the record; no error, no trace warning.

Query "tuv" with bridge "tuv>ttt;tab>ttt;abc>ccc;def>fff;
abcde>eeeee" (rule 0, condition (0,116) asserted):
- proc: exact_match=0 len_match=1 score=10000
- bridge: exact_match=1 cond_fire=1 score=60000
- T DECIDE kind=1 gap=50000 answer=[ttt]

D genuinely saw "tuv>vut" in training, but the record lost it, so
a heuristic wins 60000 to 10000 over genuine (unrecorded) evidence.
The em guarantee degrades silently past 16 inputs per record.

## X-IU2-3b: bridge_learn fixed 16-entry split buffers (LATENT CRASH, pre-existing)

Adjacent integrity probe: 18 training pairs where direct discovery
fails and a condition split puts 17 extractable pairs on one side
("xab>xxx;...;xjk>xxx;abc>ccc", 17 x-pairs + 1 a-pair).
bridge_learn panics: "slice index out of bounds" immediately after
"bridge: direct failed, inducing condition...".

Root cause: s1idx/s2idx are z_alloc(64) = 16 fixed entries, but n1
or n2 can reach npairs. The 17th split index writes past the
buffer. git log -S dates this to f5dd7cdc7 (H-UNIFIED): pre-existing,
not introduced by the IU2 repair. It bounds the same >16-pair
regime X-IU2-3 probes: beyond 16 pairs the learner does not just
lose em coverage, it can hard-crash instead of learning (and
therefore records nothing). Repair suggestion: size s1idx/s2idx
by npairs like d1/d2 already are.

## X-IU2-4: source audit (PASS)

(a) learn_seq excluded from decisions: intent_winner (both files)
never reads record offset +0; the only scoring path is
intent_qscore(em,cf,lm). learn_seq appears only in comments,
intent_init, the record writers, and intent_trace_emit. Verified
in unified_learn.zag and intent_learn.zag.
(b) intent_exact_match implements the spec: iterates in_count
entries, byte-exact (off,len) compare, returns 1 on first full
match, 0 when n<=0 or lp<0. Recorded cap equals list length;
no overflow in the record path.
(c) No test-string literals ("xqw", "hello", "abcd", "xab") in
mechanism code (everything before fn main) in either file.
(d) Record layout consistent: intent_init clears 16 proc slots at
IBASE()+i*16 and 4 bridge slots at IBASE()+256+i*16; SEQADDR=1880
= 1560+320; causal store ends at 1552, WORK starts at 2048.
(e) All 10 intent functions (init, bases, record_inputs,
record_proc, record_br, exact_match, qscore, winner,
trace_emit) byte-identical between unified_learn.zag and
intent_learn.zag: the repair is faithfully ported.

## Determinism

Three consecutive runs byte-identical:
md5 670300fa53ae250c324ef836ffe8d4f9 (IU2_ADV_RAW.txt).

## Evidence

- Prereg: PREREG_IU2_ADV.md (130109b6b).
- Harness: iu2_adv.zag (mechanism byte-copied from repaired
  unified_learn.zag; only main() replaced; one-line fixture
  correction "pqr>qrp" -> "pqr>rqp" during setup, my typo, not a
  mechanism issue).
- Raw output: IU2_ADV_RAW.txt (md5 above).
- Toolchain: znc 2026.07.0-dev (edition 2026), pinned.
- Binaries not committed (repo convention); rebuild via
  znc iu2_adv.zag -o iu2_adv.

## Classification

Bounded L2 integration infrastructure with two scoped holes:
verbatim-vs-verbatim conflicts and the >16-pair regime. Not L3;
unchanged.

## Recommended follow-ups

1. H-INTENT-UNIFIED3: extend the ambiguity guard to verbatim
   conflicts (e.g. withhold when both top candidates have em=1
   and disagree), or document verbatim-vs-verbatim as an accepted
   boundary with the heuristic precedence made explicit.
2. Fix bridge_learn s1idx/s2idx sizing (crash) and decide whether
   the 16-cap truncation should warn in the trace.
