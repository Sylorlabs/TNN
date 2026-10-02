# REPORT: verify_h1 (H1 learned typed contracts drive the verification loop)

Worker: Verify-H1 Integration Worker.
Date: 2026-10-02. Prereg: PREREG.md, frozen alone in commit 3e5014de3
(commit-order self-check: prereg commit is an ancestor of the
implementation commit and contains exactly one file).
Implementation: pure Zag, safebin PATH, no Python (guard verified at
worker start and re-verified in build.sh: python3/python absent at build
time).

## Verdict

**VERIFY-H1-COMPLETE.** All six frozen kill bars hold. No SURVIVES claim
is made; this is an integration demonstration, not a generality proof.

## What was built

A standalone pure-Zag program (`vh_mech.zag` mechanism + `vh_main.zag`
driver, assembled to `vh_full.zag`, compiled to `vh_bin`) in which the
composition_verify loop design runs on contracts produced ONLY by the
real H1 learning machinery:

- TEACH: the learner probes components C (chain-follow) and D (v+1) on
  frozen observations (31->32, 32->33 each), applies the H1 kind probe
  (1=NODE iff the value appears as a fact subject, else 2=NUM) over the
  frozen world facts (31,91,32),(32,91,33),(33,91,34), accumulates
  per-observation kind sums via h1_observe, and finalizes with the H1
  majority rule (n>=2, sum*2>=n*3 -> kind 2). Learned: C=1->1, D=1->1.
  D's probes never cover 33, so D's contract is honestly
  overgeneralized (D(33)=34 is NUM).
- Z1: goal input=31, want NODE. Learner commits to CC with the
  contract-predicted outcome NODE (status PENDING, logged before
  execution). World executes (actual 33, instrumentation only),
  downstream accepts (33 is NODE), gate=1. Learner updates conf(CC)
  0->1 from the gate alone.
- Z2: goal input=33, want NODE. Learner commits to DD, genuinely
  predicting NODE from its (wrong) D contract. World executes (actual
  35), downstream rejects (35 is NUM), gate=0. Learner updates
  conf(DD) 0->-1 from the gate alone.
- Z3: new problem (input 31, want NODE). Both CC and DD are
  contract-admissible; learner selects by argmax confidence:
  conf(CC)=1 > conf(DD)=-1, choice CC. Executes (actual 33, accept),
  conf(CC) 1->2.
- ABL: fresh learner state and fresh world, IDENTICAL teaching
  (contracts are required for admissibility), no commits, no
  consequence history. The same selection function sees conf 0,0,
  tie-breaks to lowest id, choice DD. The preference for CC in the
  main arm is therefore caused by the consequence ledger, not by the
  code; the only state difference between arms is the ledger content.

## Kill-bar evidence (mechanical)

- K-VH-1 (H1 learns signatures from probes, real H1 logic): run1.txt
  lines 5-10 read `OBS C in=31 kin=NODE out=32 kout=NODE`,
  `OBS C in=32 kin=NODE out=33 kout=NODE`, `TEACH C sig=NODE->NODE`,
  and the identical three lines for D. The source implements
  probe_kind (vh_mech.zag: 1=NODE iff value is a fact subject, else
  2=NUM), h1_observe (per-observation kind accumulation), and
  h1_finalize (majority rule n>=2, sum*2>=n*3 -> kind 2; vh_mech.zag
  lines 139-155), which is the exact rule from l2_h1.zag
  finalize_sig adapted only in state layout. Zero hardcoded
  signatures: the only signature-cell writes in the program are the
  two `ls(L,base+4,si)` / `ls(L,base+5,so)` sites at vh_mech.zag lines
  145 and 151, both inside the generic h1_finalize.
- K-VH-2 (commit with contract-predicted outcome): run1.txt line
  numbers: Z1 COMMIT line 12 < Z1 EXEC line 13 < Z1 CONSEQUENCE line
  14; Z2 COMMIT line 17 < Z2 EXEC line 18 < Z2 CONSEQUENCE line 19.
  Both COMMIT lines show status=PENDING and the contract chain that
  produced the prediction (`contracts=NODE->NODE;NODE->NODE`,
  predicted=NODE). The prediction is computed by h1_predict from the
  learned signature cells; no other value source exists on that path.
- K-VH-3 (world consequence confirms/refutes): the gate cell E[0] has
  exactly one write site in the program, vh_mech.zag line 195
  `set32(E,0,g);`, inside `fn world_downstream`, the fixed
  accept-iff-goal-kind law. Transcript CONSEQUENCE lines read gate=1
  after Z1 (actual 33, NODE) and gate=0 after Z2 (actual 35, NUM),
  consistent with that law.
- K-VH-4 (confidence updates from consequence only): transcript
  UPDATE lines read `Z1 UPDATE comp=CC conf=0->1 (source=gate)`,
  `Z2 UPDATE comp=DD conf=0->-1 (source=gate)`,
  `Z3 UPDATE comp=CC conf=1->2 (source=gate)`. The full body of
  learner_update (vh_mech.zag lines 203-209):
    fn learner_update(L:[]u8,E:[]u8,g:i32)void {
      let gate:i32=world_gate(E);
      let c:i32=lg(L,g);
      if(gate==1){ls(L,g,c+1);}else{ls(L,g,c-1);}
      ls(L,5,2);
      return;
    }
  Its only world read is world_gate(E) (line 204). It takes no actual
  output value, references no answer key, and is the sole writer of
  the confidence cells (the driver only reads them for logging).
  `grep -ci expected` over vh_mech.zag and vh_main.zag returns 0 for
  both files: no expected-answer variable exists anywhere.
- K-VH-5 (later problem prefers higher-confidence composition):
  run1.txt line 22 reads
  `Z3 SELECT confCC=1 confDD=-1 choice=CC rule=argmax-conf`; line 33
  reads `ABL SELECT confCC=0 confDD=0 choice=DD rule=tie->lowest-id`.
  Exactly one `fn learner_select` definition exists (grep count 1),
  called by both arms with identical teaching; the only input that
  differs between arms is the ledger content. The main-arm choice
  (CC, id 1) overrides the neutral tie-break default (lowest id, 0).
- K-VH-6 (determinism): 3/3 runs byte-identical. sha256 of run1.txt,
  run2.txt, run3.txt:
  4f8cfa34a3f625b2ea29cd36721cf9795f7b2d176b29ae72dd47b2ed46e9fef3
  (all three equal; cmp confirms pairwise).

## Predictions vs results

Prereg predictions: P1 TEACH C=1->1, D=1->1 (got NODE->NODE for both);
P2 gate sequence 1,0,1 (got 1,0,1); P3 Z3 choice CC by argmax-conf
(got CC); P4 ABL choice DD by tie->lowest-id (got DD); P5 final
ledger CC=2, DD=-1 (got CC=2, DD=-1); P6 3/3 byte-identical (got 3/3).
6/6 predictions matched.

## Architecture accounting

- vh_mech.zag: 231 total lines, 167 code lines. Of those: ~70 output
  helpers + state-cell accessors (infrastructure), ~97 cognition
  lines (facts, kind probe, components, H1 observe/finalize, contract
  application, commit, world law, update, select).
- vh_main.zag: 133 total lines, 114 code lines, all harness (phase
  sequencing, transcript emission, ablation entry point).
- Zero new modes, zero bridges, zero handlers, zero new opcodes, zero
  new MAP/edge types (standalone program; no substrate types used).
  Zero occurrences of "mode", "bridge", "handler" in either source
  (grep count 0). Zero `as *i32` slice constructions (grep count 0).
- The ablation arm is a driver-level entry point calling the same
  selection function, not a mode. The ABL arm teaches identically
  because contracts are required for admissibility; the frozen prereg
  records that the only state difference vs MAIN is the empty
  confidence ledger.

## Red-team self-review

1. "The downstream law (accept iff NODE) is an expected answer in
  disguise." Rejected: it is a fixed environment law, identical across
  all phases and both arms, never supplied per query; the goal kind is
  constant (NODE) across Z1, Z2, Z3. The learner discovers through
  consequences which compositions satisfy it. The program contains no
  per-query target (grep: zero "expected").
2. "D's probes (31,32 only) rig the overgeneralization." The probes
  are frozen setup, documented in the prereg before results; the H1
  induction rule is general and identical for both components. The
  setup creates the condition; the verified claim is that the
  consequence loop catches the resulting error at the composition
  level, which the transcript shows (Z2 consequence -> conf(DD)=-1
  -> Z3 avoids DD).
3. "The tie-break (lowest id) is tuned to make the ablation differ."
  The tie-break and the DD=0/CC=1 id assignment were frozen in the
  prereg before any run. The decisive fact is the reversal:
  identical selection code and identical teaching, different ledger
  -> different choice. The main-arm choice additionally overrides
  the tie-break default.
4. "The ABL arm teaches, unlike the standalone lane's ablation, so the
  arms differ by more than the ledger." The teaching is byte-identical
  frozen procedure in both arms and writes only contract cells, never
  confidence cells; the confidence ledger (the only selection input
  besides contracts) is empty in ABL and earned in MAIN. The prereg
  froze this design explicitly.
5. "The learner never revises D's wrong component contract."
  Accepted as a boundary, not a flaw in the claim: the kill bars test
  composition-level verification (trust in (D,D) drops), not component
  contract revision. D's contract stays wrong in learner state; the
  learner simply stops selecting (D,D) for NODE-requiring downstream
  tasks. Contract revision is a separate experiment.
6. "Toy scale; ~97 cognition lines prove nothing about TNN."
  Accepted: mechanism demonstration with frozen bars, explicitly not
  substrate integration and not a generality claim.

## Boundaries and non-claims

- Component contracts are induced by the real H1 rule from frozen
  probes; contract induction from rich experience is H1's demonstrated
  territory, not re-proven here.
- (D,D) would in fact succeed on input 31; the Z3 preference for CC
  is earned distrust from Z2, which is exactly the learned-preference
  phenomenon under test.
- No claim is made about transfer, scaling, or subsumption of other
  composition mechanisms. The verdict is VERIFY-H1-COMPLETE
  (integration built and bars met), never SURVIVES.
- The learner never observes actual output values; the white-box
  actuals in the transcript are driver instrumentation, labeled as
  such, and no learner function is ever passed one.

## Deliverables (this lane dir)

- NAMECHECK.md (Step 0 toolchain guard + steps)
- PREREG.md (frozen alone, commit 3e5014de3)
- vh_mech.zag, vh_main.zag (sources), vh_full.zag (assembled),
  build.sh (guard + checks + build + 3x run)
- vh_bin (compiled binary, sha256
  2a4ed2cc521230f00e1acd0a3a0fe476c696d3318da03d6e02447ac1d8914922),
  compile.txt
- run1.txt, run2.txt, run3.txt, sha256sums.txt
- REPORT.md (this file)

All commits local only, explicit pathspecs, nothing pushed.
