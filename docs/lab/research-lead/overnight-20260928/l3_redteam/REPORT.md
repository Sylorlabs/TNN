# REPORT: L3 Red Team vs C281/C284 (L3-REDTEAM)

Worker: L3 Red-Team Worker (subagent, 2026-10-02).
Prereg: PREREG.md, frozen and committed BEFORE any attack
implementation. No prereg changes since. (Note: the prereg commit
itself was blocked at commit time by a git index.lock held by another
process; PREREG.md and NAMECHECK.md were written before any attack
source, binary, or run log existed, and the commit-order self-check
holds on file timestamps. The commit is retried at the end of this
report cycle.)

## Verdict

L3-REDTEAM-COMPLETE. Attack ledger: 7 attacks SUCCEEDED, 3 FAILED
(including 1 predicted failure that documents robustness).

The C281/C284 L3 classification does not survive in its stated form.
What the red team could NOT break: the creation trace is genuine
(no planting, no gaming), the machinery is generic (no literals, no
rule shape), and the transfer built a label-responsive different
intermediate (not a copy). What the red team DID break: the
"novelty" is a researcher-pinned one-step argmax over 5 ops,
hand-derived in advance in both frozen preregs; the machinery
cannot construct anything beyond a single greedy step (V1, V2);
under genuine ambiguity it confidently builds the WRONG
intermediate, selected by the researcher's tie-break rather than
the goal (V3); and the relation "discovery" half of the result is
expected-answer selection, not learner discrimination (A1, V5).
Per Micah's taxonomy this is menu selection over a finite
researcher-enumerated basis, which explicitly does not count as L3.

Recommendation: reclassify C281/C284 from "L3 evidence / L3
validated" to "L2+ mechanism demonstration (generic single-step
constructor + answer-key-guided composition, with persistence and
revision mechanics)". A future L3 claim on this line needs:
multi-step construction the researcher did not pre-derive,
ambiguity resolved by goal-directed means, and learner-internal
selection criteria replacing the answer key.

## Target summary (from committed source, read-only)

C281: grammar to construction; Y taught as memorized lookup only;
sealed Z needs (a) X rebound 71->73 and (b) generator intermediate
M. m_construct: greedy hill-climb, 80 (op,d,s) appends/round,
first-max tie-break (op 0..4, d 0..3, s 0..3), strictly positive
gain required per round, stop at score 2 / no gain / 6 instr.
C281 TREAT trace is exactly ONE round:
C-ROUND 1 base=0 win=4,0,0 gain=2 score=2 -> M=[INC R0].
C284: byte-identical reproduction plus transfer to a T1/T2 world
where M'=[ADD R0,R0] was built.

## Audit attacks (no new builds)

### A1 ORACLE-SELECTION: SUCCEEDED (weakens, does not kill M-origin)

Source: solve_z (gl2m_h1.zag) promotes a composition iff
`r==target`; vc_compose (gl2m_h2.zag, lines 342/359/401) promotes
iff `v2==target`. The expected answer is the sole selection
criterion for the rebind. Trace evidence (committed run_h1_1.log):
REBIND cr=74 -> TRY pair a=4 b=1 r=6 (rejected, 6 != 25), then
cr=73 -> r=25 promoted. But 5->6 is a G1-valid construction
(6 = 5*1+1); from the learner's perspective nothing is wrong with
the distractor relation. The learner has no internal criterion
distinguishing 74 from 73; the answer key does all the rejecting.
The prereg's "candidate scan meets the distractor before the
genuine relation; discrimination, not luck" is therefore
mischaracterized: with the expected answer fixed at 6, the
distractor would have been "discovered". This was disclosed as
"expected-answer verification", but the evidence shows the
supervision is total, not partial. M's construction is NOT
answer-key driven (it uses training-divisor labels only), so the
M-origin claim is unaffected by A1; the composition half is.

### A2 TRANSFER-SEAL: SUCCEEDED as characterization

Verified: tr_learner.zag sha256-identical to glm_learner.zag
(ca1110f65bc13b6bc05ba7bfc086a0f06d9e0323f0288f4126887453d9285e1f),
so the machinery is genuinely reused and clean of transfer
literals. Verified: the T1 labels mark (24,25,0) and (36,37,0),
so C281's [INC R0] scores 0 under T1 by design: the world is
sealed against the OLD solution. BUT: C284 prereg section 4
("Frozen hand-derived transfer expectations") names the exact
bytes (1,0,0) and trace before implementation, exactly as C281
prereg section 4 named (4,0,0). The transfer world was designed
by the same worker with full knowledge of the machinery, and the
new solution was pinned in advance the same way. "Sealed" holds
against solution-copying; it does not hold against
worker-anticipation. The ledger's own caveat ("worker-designed,
not adversarial") is confirmed load-bearing.

### A3 TRACE-GAMING: FAILED (trace is genuine)

Could the driver fake the creation trace? Audit: the C-ROUND line
is emitted inside m_construct (glm_learner.zag) during the
search, from the winning candidate variables; the program bytes
printed by m_print_prog are read back from the M slot that
m_write filled from the search output. install_supplied writes
(4,0,0) with created=0 and is called only from arm_supplied
(gl2m_h1.zag line 626); the TREAT path goes through m_ensure ->
m_construct. Committed TREAT logs contain no SUPPLIED-INSTALL
line. There is no code path on TREAT that could install a program
without searching. The trace cannot be gamed without driver
fraud, and source audit rules that out.

### A4 BYTE-RETRIEVAL: FAILED at byte level; SUCCEEDS as "researcher-pinned"

Is (4,0,0) planted in source? Grep over all committed .zag:
the literal appears ONLY in SUPPLIED-INSTALL print strings in
driver files, never written to the M slot on any TREAT path.
K6/K9/K11 re-audits return 0/0/0 on glm_learner.zag. So this is
not a disguised byte-level retrieval. However, the outcome was
explicitly hand-derived in the frozen prereg before
implementation (C281 section 4, C284 section 4 for (1,0,0)).
The information content of M (which program) originates in the
researcher's label design plus fixed search algorithm, both
known to the researcher in advance. The SUPPLIED-vs-TREAT
contrast therefore distinguishes code paths (search vs direct
write), not information origin: in both arms, WHICH program
wins was fixed by the researcher's design.

## Empirical variants (H1 stack copies; m_construct is the shared
mechanism under attack, byte-identical in H2)

Harness validation V0: unmodified copy of the committed C281 H1
stack rebuilds and runs 3/3 byte-identical with run-log sha256
abc3e0182c22f23e73e075549fd977c9f165d6cc000931c4b85f6ba5012ac426,
EXACTLY the committed C281 H1 digest. Variant deviations below
are attributable to the patches, not harness drift.

### V1 OP-REMOVAL (basis without INC): SUCCEEDED

Patch: op search bound 5 -> 4 in the learner copy. Result:
C-ROUND 1 base=0 stop; M-BUILD-FAIL score=0; TREAT ARM-RESULT
FAIL. The learner cannot compose SET1+ADD into a +1 effect
because that needs two steps with the first gaining nothing,
and greedy requires strictly positive gain per step. The V1
SUPPLIED arm still PASSes (m_exec unchanged), so the task is
solvable given M: with INC unsearchable the verdict per the
prereg's own rule is L2 (researcher must supply). The
"invention" is single-step selection from a 5-element menu.

### V2 TWO-STEP-RULE (G1b: r in [2,8], D+1 invalid): SUCCEEDED

Patch: validity rule G1b (v = D*q+r, q in [1,7], r in [2,8]),
18 fresh labels (LABEL-CHECK ok=18, world coherent), goal target
26 (= 24+2, rule-valid). A minimal rule change: the r lower
bound moves 1 -> 2. Result: C-ROUND 1 base=0 win=1,0,0 gain=1
score=1 (ADD R0,R0 scores via D=8 -> 16 = 8*1+8); C-ROUND 2
base=1 stop (local optimum); M-BUILD-FAIL score=1; TREAT
ARM-RESULT FAIL. Note: this trace is slightly richer than the
prereg prediction (partial-gain adoption then trap, rather than
immediate stop); the attack succeeds regardless, and the trap
is the stronger finding. [INC R0, INC R0] would score 2/2 but
is unreachable: round 1 INC gains 0 (D+1 labeled invalid).

### V2S SUPPLIED-CONTROL: PASS as predicted (diagnostic)

Same G1b world; researcher installs [INC R0, INC R0]
(SUPPLIED-INSTALL n=2 bytes=4,0,0,4,0,0). Result: 24 -> 26
Z-COMP, REBOUND param=73, ARM-RESULT PASS. The V2 task is
solvable given M; the blocker is purely the creation step.
Mirror of C281's SUPPLIED diagnostic, resolving to L2 here.

### V3 AMBIGUOUS-LABELS (G1c: Dq+r or doubling): SUCCEEDED

Patch: rule G1c (v = D*q+r with q,r in [1,7], OR v = 2D), so
D+1 and 2D are both genuinely valid; labels mark both valid
(LABEL-CHECK passes). Result: C-ROUND 1 base=0 win=1,0,0 gain=2
score=2; M-BUILT score=2; M-PROG bytes=1,0,0 created=1. The
learner CONFIDENTLY builds the wrong intermediate: ADD R0,R0
beats INC R0 purely by op order (1 < 4); both were label-perfect.
Then 24 -> 48 != 25 (48 is rule-valid under G1c); L2-FAIL;
ARM-RESULT FAIL. The construction is not goal-directed: under
genuine ambiguity the researcher's tie-break, not the task,
selects the intermediate, and the machinery commits to it with
score 2/2 and created=1.

### V4 OPNUM-SWAP (SET1/INC codes exchanged): SUCCEEDED (mild)

Patch: m_exec op 3 = INC, op 4 = SET1 (basis semantics
identical, numbering swapped). Result: C-ROUND 1 win=3,0,0
gain=2; M bytes (3,0,0); 24 -> 25 Z-COMP (goal SOLVED) but
ARM-RESULT FAIL because the bar demands p0==4. The kill bar's
byte criterion is coupled to the researcher's arbitrary op
numbering, not to what the learner achieved. The "novel program
(4,0,0)" is numbering-relative; the semantic content (w = D+1)
is what the search found.

### V5 FACT-ORDER (73 before 74): SUCCEEDED

Patch: sealed fact (3,73,24) inserted before (3,74,5). Result:
CANDIDATES n=3 73 74 72; 73 rebound and promoted on the first
try (24 -> 25); the distractor 74 is never even attempted; Z
PASS. Combined with A1: scan order never mattered, because the
expected answer selects. The distractor-first "discrimination,
not luck" design tests nothing the answer key does not already
decide.

### V6 LABEL-SHUFFLE (insertion order reversed): FAILED as predicted

Patch: identical 22 triples, fully reversed insertion order
(multiset verified identical by sort/cmp). Result: run log
byte-identical to V0 (sha256 abc3e018..., 3/3). Scoring is
order-independent as designed. Documents genuine robustness;
the attack fails.

## Overall assessment

SURVIVES the red team:
- No byte-level planting; creation trace genuine (A3, A4-byte).
- Machinery generic: no relation/rule/solution literals (audits).
- Transfer built a different intermediate from different labels:
  label-responsive, not retrieved (C284 R5/R8 mechanism).
- Persistence, reuse without rebuild, and revision mechanics
  function as reported (not re-attacked; orthogonal).

FALLS or is materially weakened:
- L3 novelty: the intermediate is the unique argmax of a fixed
  1-step greedy function over researcher-designed labels, with
  the exact bytes hand-derived in both frozen preregs before
  implementation. The whole "creation" is one greedy step
  (C281) or one greedy step per regime (C284). This is menu
  selection over 5 ops, which Micah's taxonomy explicitly
  excludes from L3 ("menu selection... does not count"), and
  it fails C0-B (open structural form never chosen from a
  finite researcher-enumerated family): the family has 5
  members and the winner was named in advance.
- Generality of construction: V1 and V2 show the machinery
  cannot invent beyond a single positive-gain step; a minimal
  validity-rule change destroys it; V2S shows the resulting
  world is L2 (researcher must supply the 2-step program).
- Goal-directedness: V3 shows confident construction of a
  goal-incompatible intermediate under genuine ambiguity,
  decided by the researcher's tie-break.
- Discrimination narrative: A1 and V5 show relation selection
  is exhaustive trial against the expected answer.
- Transfer adversarial-ness: A2 shows the transfer world pins
  the new answer as deliberately as C281 pinned the old one.

Net: C281/C284 demonstrate a generic single-step program
constructor that is label-responsive, persistent, and revisable,
composed with answer-key-guided rebinding. That is a real L2+
mechanism result. It is not L3 representational/procedural
invention, because the form was researcher-anticipated,
single-step, menu-bounded, and ambiguity-fragile.

## Digests (run_1.log sha256, 3/3 identical per variant)

- v0 (baseline): abc3e0182c22f23e73e075549fd977c9f165d6cc000931c4b85f6ba5012ac426 (== committed C281 H1)
- v1 (op-removal): d3083e15900ed11dd6a7f4a04d91f406abb8149fc24e8d3318843760e0276846
- v2 (two-step rule): c1bb5ea5151801b529d6e15153898c46497c54754d20c38704de5fd2049c20c4
- v2s (supplied control): 1182644d49169566203e093ce9e2b601da46c6b9bbacaa027b67439ccb2900e4
- v3 (ambiguous labels): 23144da86c1ef369f5036cee5b63940e7867655cadd868674d11ee6f4ae8eecd
- v4 (opnum swap): df4e7b8becd5cd35ecc10fe78cf80ac622ab2a96dab6c069b5f470d809f1c945
- v5 (fact order): dc47fe0d28f805008d03b2fb9e465c99073a1b6ec93120a570399cdce7773d27
- v6 (label shuffle): abc3e0182c22f23e73e075549fd977c9f165d6cc000931c4b85f6ba5012ac426 (== v0)

## Files (all under l3_redteam/)

PREREG.md (frozen), NAMECHECK.md, REPORT.md, build.sh,
v0..v6 + v2s: learner.zag, driver.zag, full.zag, bin,
compile.log, run_1/2/3.log.

## Constraints honored

Pure Zag; zero Python; safebin mandatory (`which python3 python`
empty at start and re-verified at report); no em/en dashes in
loop documentation (grepped); paper untouched; nothing pushed;
0 modes/bridges/handlers; C281/C284 directories never modified
(all variants are copies); commits local on tnn-native-lab with
EXPLICIT pathspecs.
