# L3A-TRACE Clean Rebuild: Result

## Verdict: L3A-TRACE-CLEAN-BUILD-PASS

All five frozen bars reproduced from an independent clean-room
implementation. Determinism confirmed (3/3 byte-identical stdout, empty
stderr, exit 0). C0-A audit A1-A7 passes on the new implementation file.
Kill bars K1/K2/K3 hold. Zero Python anywhere in this wave.

## Frozen configuration (prereg 05898699e + A1 444617dd4 + A2 439dd54c5)

- T0: y=x^2, T1: y=2x^2, T2 (held-out): y=x^4+2x^2+x+1. x in 0..6, 7 episodes.
- beam_w=600, max_len=8. Base VM ops 0-18 (18=TCALL, generic indirection).
- Intended invention: [(IN0,0),(IN0,0),(MUL,0)] = [1,1,5] ("push x*x").

## Battery output (run1.log; run2/run3 byte-identical, sha256 69f43f85d4a6e6d0e3a8b625ec091fa48e7ca7e942911c79c2447cfb84acad90)

- TRAIN t=0: 7/7, len 3, [IN0 IN0 MUL]. RECORDED (ep0steps=3).
- TRAIN t=1: 7/7, len 5, [PUSH:2 IN0 IN0 MUL MUL]. RECORDED (ep0steps=5).
- REIFIED name=0 len=3 arity=0 produced=1 credit=2 seg=[IN0:0 IN0:0 MUL:0].
- SEGMENT-MATCH 1. STATE-DUMP nre=1 heaptop=24; ENTRY id=0 off=0 len=3 arity=0 produced=1.
- T-PERSIST: x2=10/10 (fresh byte-exported state, x in -3..6).
- T-REUSE: 7/7, len 7, [IN0 TCALL:0 PUSH:1 ADD DUP MUL ADD], hastcall=1.
- T-ABLATE: 2/7 (invention disabled; advantage destroyed).
- T-SWAP: to2x=10/10, backtox2=10/10 (behavior follows stored bytes both ways).
- BAR-A-INVENT 1, BAR-A-SEGMATCH 1, BAR-B-PERSIST 1, BAR-C-REUSE 1,
  BAR-D-ABLATE 1, BAR-E-SWAP 1.
- VERDICT L3A-TRACE-CLEAN-BUILD-PASS. DONE.

Every measured value matches the original builder's frozen results
exactly (training solutions, reified name/len/arity/produced/credit,
segment bytes, reuse solution, ablation score, probe counts).

## Bar results

- (a) T-INVENT: PASS. n_reified=1, runtime-assigned name_id=0, stored bytes
  equal the detected segment, R2 conditions printed by the detector
  (credit=2, arity=0, produced=1), SEGMENT-MATCH=1 on [1,1,5].
- (b) T-PERSIST: PASS. 10/10 probes equal x^2 on the fresh byte-exported
  state, x in -3..6.
- (c) T-REUSE: PASS. Phase-2 search with invention returns an exact 7/7
  solution containing TCALL of the reified name id, within max_len 8.
- (d) T-ABLATE: PASS. Identical search with TCALL expansions removed
  reaches only 2/7 < 7. The advantage is destroyed without invention.
- (e) T-SWAP + T-AUDIT: PASS. Overwriting entry 0's bytes with
  [IN0,DUP,ADD] flips probes to 2x on 10/10; restoring the original bytes
  returns x^2 on 10/10. C0-A audit A1-A7 all hold (see below).

## C0-A source audit on l3a_trace_clean.zag (frozen procedure, adapted only in grep names)

- A1: All opcode dispatch branches (`opc==`) keyed on constants 0..18
  only (lines 190-226). The opname and opeffect helper mappings are also
  keyed 0..18 only. No branch keyed on a runtime name id. PASS.
- A2: The opc==18 (TCALL) branch (lines 226-234) contains only:
  bounds check (argv>=0 && argv<nre), name-table offset/length lookup,
  and a recursive call into runvm (the same generic interpreter). No
  stack push/pop, no arithmetic, no comparison, no conditional keyed on
  any invented operator identity. PASS.
- A3: Trace-store bytes (heap/toff/tlen) are fetched and executed only
  in runvm's TCALL branch (lines 229-231). stateexport copies bytes only;
  reify writes them; probe passes the exported copy as the store but all
  execution of those bytes still goes through the op-18 branch. PASS.
- A4: The reified name id is the learner state's counter: reify assigns
  idcell=nre (line 654) and main increments nre afterwards (line 758).
  No source constant appears in a name-id semantic position. PASS.
- A5: Every beam expansion appends exactly one (op,arg) via pappend
  (lines 322, 329, 333, 339, 348); no multi-op template and no op-array
  literal exists in code (the only bracket sequences are prose in
  comments). The detected segment cannot be a researcher-authored unit.
  PASS.
- A6: `grep -rni "python" l3a_trace_clean.zag` returns empty; the owned
  path contains only .zag, .md, .sh, .log files (plus compiler-generated
  .zag-cache, not committed). PASS.
- A7: Stdout contains REIFIED name=0 and a STATE-DUMP whose entry
  (id=0 off=0 len=3) matches the detector's reported segment bytes
  [IN0:0 IN0:0 MUL:0]. PASS.

Audit verdict: A1-A7 all PASS.

## Kill bars

- K1 (zero Python anywhere in the wave): PASS. I affirmatively state
  that no python3 was invoked for any purpose in this wave: not for
  implementation, diagnostics, /tmp scratch, log comparison (cmp,
  sha256sum), or byte checks (shell-only check_no_dash.sh). The owned
  path and all logs were produced by the pinned znc binary and POSIX
  shell only.
- K2 (all five bars reproduced 3/3 byte-identical): PASS. 3/3 runs
  byte-identical stdout, exit 0, empty stderr, verdict
  L3A-TRACE-CLEAN-BUILD-PASS on every run.
- K3 (C0-A A1-A7 PASS on the new implementation; contaminated paper
  untouched): PASS. The contaminated paper
  (docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md)
  was not read, edited, staged, or committed in this wave.

## Architecture delta (ONE-SYSTEM RULE record)

This mechanism is a bounded standalone demonstrator; integration into
the continuing learner is out of scope for this rebuild.

- Cognition source lines added: 884 (l3a_trace_clean.zag, fresh file).
- New hardcoded semantic cases: 0. The opcode table 0..18 is the frozen
  base VM; no branch is keyed on any invented operator or runtime id.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0. (The SEGMENT-MATCH guard is a frozen
  prereg check on the intended invention, not a handler; task battery
  construction is frozen data, not cognition dispatch.)
- Learner-state structures created: trace_heap (reified trace bytes),
  name table (offset/length/arity/produced per entry, capacity 4,
  runtime counter n_reified), recorded episode traces (4 tasks x
  8 episodes x 256 steps of (op,arg,depth_before,depth_after)).
- Capability-source delta: the invented operator [IN0,IN0,MUL] required
  zero new source semantics; its meaning lives entirely in learner
  state, executed by the pre-existing generic interpreter.

## Process notes

- The reference implementation (a6fbee865) was read for design
  understanding only. l3a_trace_clean.zag is an independent
  reimplementation: different helper names (newbuf/i32get/i32set,
  plen/popof/pargof, runvm, peval, rankfirst, beamsearch, buildtask,
  recbase/recordtask, segarcode/seginep/segcmp, reify, stateexport,
  probe), offset-based buffer conventions instead of subslices, and a
  fused score/MAE evaluator.
- One deliberate fidelity choice: the global best-program tracker uses
  the full frozen 4-key ranking (exact desc, MAE asc, length asc,
  lexicographic asc) from prereg section 5 for both beam ordering and
  best tracking. All reproduced values are identical to the original
  builder's.
- No em dashes or en dashes in any committed file (shell-only check).
- Commits stay local; owned paths only; explicit pathspecs; no push.

## Scope

This is a BUILD-PASS verdict only (steps 1-3 of the 11-step pipeline:
prereg, implementation, sealed evaluation). No L3 or Criterion-0 claim
is made here. At most this evidences C0-A (runtime-defined semantics)
in a bounded setting; C0-B/C0-C/C0-D are not tested and partial C0
evidence is not L3. Independent red team (T-ADV) remains PENDING and out
of scope for this build. LLM baseline PENDING; human baseline NOT
MEASURED, per standing rules.
