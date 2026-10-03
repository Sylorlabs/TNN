# PREREG H-INTENT-UNIFIED2 RED TEAM — FROZEN

Adversary: H-INTENT-UNIFIED2 red team (independent).
Target: H-INTENT-UNIFIED2 repair claim (commits a6ffebe24 prereg,
2b55c5e7d repair). Mechanism files: `unified_learn.zag` (v3),
`intent_learn.zag` (repaired). Assumed false until tested.

## Threat model

The repair claims:
- (R1) qscore = em*40000 + cf*20000 + lm*10000; learn_seq excluded
  from decisions; top-two qscore tie -> WITHHOLD AMBIGUOUS.
- (R2) em(c,q) = 1 iff the query is verbatim in the slot/rule's
  recorded training inputs, so "verbatim stored evidence dominates
  any generalization heuristic" (X-IU2 closed).
- (R3) 16-training-input cap per record is a documented boundary.

## Attacks

### X-IU2-1: em collision, verbatim-vs-verbatim conflict (DOWNGRADE probe)

Setup (fresh workspace, intent_init):
1. Learn D2 = "xab>bax;xcd>dcx" -> expect proc slot (reverse).
   D2's record then holds verbatim evidence "xab>bax".
2. Learn bridge with the exact F2 string
   "xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee" -> expect bridge
   rule, condition (0,120) asserted. The bridge's record then ALSO
   holds "xab" verbatim (as "xab>xxx").
3. Query "xab". D2: em=1, lm=1 -> 50000. Bridge: em=1, cf=1,
   lm=0 (mixed lengths) -> 60000.

Kill criterion: DOWNGRADE if kind==1 (bridge wins, answer "xxx")
with gap>0 (no withhold) while D2's record has em("xab")==1.
Rationale: two training sets genuinely contradict on "xab"
("xab>bax" vs "xab>xxx"); the conflict is resolved silently by the
cond_fire heuristic term, not withheld. This re-opens the exact
failure mode X-IU2 was claimed to close ("the 20000-point heuristic
overrides explicit training evidence for the exact input"), now
with verbatim evidence on both sides.
PASS (no downgrade) if kind==-2 (withholds) or kind==0 (proc wins).

### X-IU2-2: pure em tie, guard control (informational)

Setup (fresh workspace):
1. Learn A = "abc>cba;def>fed" -> reverse proc, em inputs {abc,def}.
2. Learn B = "abc>abc;def>def" -> identity-ish proc, em inputs
   {abc,def}.
3. Query "abc": A qscore = 50000, B qscore = 50000.

Expected: kind==-2 (WITHHOLD AMBIGUOUS). This is a CONTROL: it
confirms the tie guard handles genuine verbatim-vs-verbatim
conflicts between procs, sharpening any X-IU2-1 finding (the guard
fails only when a heuristic term breaks the em tie).
If kind==0 or kind==1: tie-guard failure, escalate to DOWNGRADE
analysis in the report.

### X-IU2-3: 16-cap silent degradation (BOUNDARY probe)

Setup (fresh workspace):
1. Learn D = 17 reverse pairs (all len 3, distinct chars):
   "abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>qrp;stu>uts;
   vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;
   qrs>srq;tuv>vut" -> expect proc slot (reverse). The 17th input
   "tuv" is verbatim in training but beyond the 16-cap.
2. Assert D's record in_count==16 and em_D("tuv")==0 (trace the
   record; the harness prints in_count and the em value for "tuv").
3. Learn bridge "tuv>ttt;tab>ttt;abc>ccc;def>fff;abcde>eeeee" ->
   expect bridge rule, condition (0,116) asserted ('t').
4. Query "tuv". D: em=0, lm=1 -> 10000. Bridge: em=0, cf=1,
   lm=0 -> 20000.

Finding: DOWNGRADE/BOUNDARY if kind==1 (bridge wins, "ttt")
while D's training contained "tuv>vut" verbatim. Rationale: the
em specificity guarantee silently degrades past 16 inputs; a
verbatim training fact is lost from the record and a heuristic
wins over genuine (unrecorded) evidence.
PASS (no issue) if kind==0.

### X-IU2-4: source audit (PASS/DOWNGRADE)

Static checks on `unified_learn.zag` and `intent_learn.zag`:
(a) learn_seq (record offset +0) is never read on the decision
    path: the only scoring function is intent_qscore(em,cf,lm);
    intent_winner must not read get32(W,o) [learn_seq] except in
    intent_trace_emit.
(b) intent_exact_match implements the spec: iterates in_count
    entries, byte-exact compare, returns 1 on first full match.
(c) No test-string literals ("xqw", "hello", "abcd", "xab") in
    mechanism code (everything before fn main).
(d) Record layout consistent: 16-byte stride in intent_init,
    intent_proc_base, intent_br_base; SEQADDR == IBASE+320;
    intent_init clears both regions.
(e) intent functions decision-identical between the two files
    (repair faithfulness, X-IU4 for the repair).

DOWNGRADE on any discrepancy; else PASS.

## Verdict rule

- Any DOWNGRADE/BOUNDARY finding -> H-INTENT-UNIFIED2 DOWNGRADED.
- No KILL criteria: the frozen 5/5 bars are not attacked (their
  threat model is unchanged); these attacks probe untested
  territory named in the builder's own "future red team" list.

## Method

Pure Zag. Attack harness = byte-copy of the repaired
`unified_learn.zag` mechanism with main() replaced (same pattern as
iu2_fix.zag). Three consecutive runs must be byte-identical;
report md5. Commit prereg before any attack execution; commit
harness + raw evidence + report after. Only adversary-owned files
staged.
