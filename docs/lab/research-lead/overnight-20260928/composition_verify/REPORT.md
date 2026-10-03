# REPORT: composition internal verification (composition_verify lane)

Worker: Composition Internal Verification Worker.
Date: 2026-10-02. Prereg: PREREG.md, frozen alone in commit ca23aa436.
Implementation: pure Zag, safebin PATH, no Python (guard re-verified in
build.sh: python3/python absent at build time).

## Verdict

**COMPOSITION-VERIFY-COMPLETE.** All six frozen kill bars hold. No
SURVIVES claim is made; this is a mechanism demonstration, not a
generality proof.

## What was built

A standalone pure-Zag program (`iv_mech.zag` mechanism + `iv_main.zag`
driver, assembled to `iv_full.zag`, compiled to `iv_bin`) implementing
the learner-owned verification loop:

- IND: the learner induces parity contracts for components X, Y, D from
  two frozen probes each, using one general induction rule. D's probes
  cover odd inputs only, so the learner honestly overgeneralizes D's
  contract to ALWAYS_EVEN (true behavior: FLIP).
- Z1: learner commits to composition (X,Y) on input 100 with predicted
  output type EVEN (status PENDING, logged before execution). World
  executes (actual 220, instrumentation only), downstream machine
  accepts (220 even), gate=1. Learner updates conf(X,Y) 0->1 from the
  gate alone.
- Z2: learner commits to (X,D) on input 100, genuinely predicting EVEN
  (its D contract is wrong). World executes (actual 111),
  downstream rejects (111 odd), gate=0. Learner updates conf(X,D)
  0->-1 from the gate alone.
- Z3: new problem (input 200). Learner selects by argmax confidence:
  conf(X,Y)=1 > conf(X,D)=-1, choice (X,Y). Executes through
  downstream (actual 420, accept), conf(X,Y) 1->2.
- ABL: fresh learner state, no induction, no consequence history. The
  same selection function sees conf 0,0, tie-breaks to lowest id,
  choice (X,D). The preference for (X,Y) in the main arm is therefore
  caused by the consequence history, not by the code.

## Kill-bar evidence (mechanical)

- K-IV-1 (commit before any answer): transcript line numbers from
  run1.txt: Z1 COMMIT line 6 < Z1 EXEC line 7 < Z1 CONSEQUENCE line 8;
  Z2 COMMIT line 10 < Z2 EXEC line 11 < Z2 CONSEQUENCE line 12. Both
  COMMIT lines show status=PENDING, the value written by
  learner_commit before world_execute runs. `grep -ci expected` over
  iv_mech.zag and iv_main.zag returns 0 for both files: no
  expected-answer variable exists anywhere in the program.
- K-IV-2 (world consequence): the gate cell E[0] has exactly one write
  site in the program, iv_mech.zag line 141 `set32(E,0,g);`, inside
  `fn world_downstream`, the fixed world law (accept iff even).
  Transcript CONSEQUENCE lines read gate=1 after Z1 (actual 220, even)
  and gate=0 after Z2 (actual 111, odd), consistent with that law.
- K-IV-3 (update from consequence): transcript UPDATE lines read
  `Z1 UPDATE comp=XY conf=0->1 (source=gate)` and
  `Z2 UPDATE comp=XD conf=0->-1 (source=gate)`. The full body of
  learner_update (iv_mech.zag lines 149-155):
    fn learner_update(L:[]u8,E:[]u8,g:i32)void {
      let gate:i32=world_gate(E);
      let c:i32=lg(L,g);
      if(gate==1){ls(L,g,c+1);}else{ls(L,g,c-1);}
      ls(L,5,2);
      return;
    }
  Its only world read is world_gate(E) (line 150). It takes no actual
  output value, references no answer key, and is the sole writer of
  the confidence cells (the driver only reads them for logging).
- K-IV-4 (prefer by earned confidence): run1.txt line 15 reads
  `Z3 SELECT confXY=1 confXD=-1 choice=XY rule=argmax-conf`.
- K-IV-5 (ablation control): run1.txt line 19 reads
  `ABL SELECT confXY=0 confXD=0 choice=XD rule=tie->lowest-id`.
  Exactly one `fn learner_select` definition exists in the source
  (grep count 1), called by both arms; the only input that differs
  between arms is the ledger content. Main-arm choice (XY, id 1) goes
  against the neutral tie-break default (lowest id), showing learned
  confidence overriding the default.
- K-IV-6 (determinism): 3/3 runs byte-identical. sha256 of run1.txt,
  run2.txt, run3.txt:
  21b6b86719162e17f7ae134291f5db680890e10a073fb1dff030866ed82b6831
  (all three equal; cmp confirms pairwise).

## Predictions vs results

Prereg predictions: main Z3 choice XY (got XY); ablation choice XD
(got XD); 3/3 byte-identical (got 3/3); induced contracts
X=PRESERVE, Y=ALWAYS_EVEN, D=ALWAYS_EVEN overgeneralized (all three
confirmed in transcript lines 3-5); gate sequence 1,0,1 (confirmed
lines 8, 12, 16). 5/5 predictions matched.

## Architecture accounting

- iv_mech.zag: 165 total lines, 120 code lines. Of those: 48 output
  helpers + 9 state-cell accessors (infrastructure), 63 cognition
  lines (components, induction, contract chaining, commit, world law,
  update, select).
- iv_main.zag: 103 total lines, 88 code lines, all harness (phase
  sequencing, transcript emission, ablation entry point).
- Zero new modes, zero bridges, zero handlers, zero new opcodes, zero
  new MAP/edge types (standalone program; no substrate types used).
  Zero occurrences of "mode", "bridge", "handler" in either source.
- The ablation arm is a driver-level entry point calling the same
  selection function, not a mode.

## Red-team self-review

1. "The world law (accept iff even) is an expected answer in disguise."
  Rejected: it is a fixed environment law, identical across all phases
  and both arms, never supplied per query. The learner discovers
  through consequences which compositions satisfy it. The program
  contains no per-query target (grep: zero "expected").
2. "D's odd-only probes rig the overgeneralization." The probes are
  frozen setup, documented in the prereg before results; the induction
  rule is general and identical for all three components. The setup
  creates the condition; the verified claim is that the consequence
  loop catches the resulting error at the composition level, which the
  transcript shows (Z2 consequence -> conf(X,D)=-1 -> Z3 avoids XD).
3. "The tie-break (lowest id) is tuned to make the ablation differ."
  The tie-break was frozen in the prereg before any run, and any
  neutral tie-break would serve. The decisive fact is the reversal:
  identical selection code, different ledger -> different choice. The
  main-arm choice additionally overrides the tie-break default.
4. "The learner never revises D's wrong component contract."
  Accepted as a boundary, not a flaw in the claim: the kill bars test
  composition-level verification (trust in (X,D) drops), not component
  contract revision. D's contract stays wrong in learner state; the
  learner simply stops selecting (X,D) for even-requiring downstream
  tasks. Contract revision is a separate experiment.
5. "Toy scale; 63 cognition lines prove nothing about TNN." Accepted:
  this is a mechanism demonstration with frozen bars, explicitly not
  substrate integration and not a generality claim. Integration with
  the TNN substrate is listed as future work.

## Boundaries and non-claims

- Component contracts are induced by a tiny general rule from frozen
  probes; contract induction itself (from rich experience) is H1's
  demonstrated territory, not re-proven here.
- No claim is made about transfer, scaling, or subsumption of other
  composition mechanisms. The verdict is COMPOSITION-VERIFY-COMPLETE
  (mechanism built and bars met), never SURVIVES.
- The learner never observes actual output values; the white-box
  actuals in the transcript are driver instrumentation, labeled as
  such, and no learner function is ever passed one.

## Deliverables (this lane dir)

- NAMECHECK.md (Step 0 toolchain guard + steps)
- PREREG.md (frozen alone, commit ca23aa436)
- iv_mech.zag, iv_main.zag (sources), iv_full.zag (assembled),
  build.sh (guard + checks + build + 3x run)
- iv_bin (compiled binary), compile.txt
- run1.txt, run2.txt, run3.txt, sha256sums.txt
- REPORT.md (this file)

All commits local only, explicit pathspecs, nothing pushed.
