# REPORT: GEN-CYCLES -- Verdict PASS

Date: 2026-10-03. Worker: gen-cycles.
Lane: `docs/lab/research-lead/overnight-20260928/gen_cycles/`.
Battery: preregistered implementation of the COMPOSE-CYCLES PREREG
Section 11 direction (trial over re-applicable structure sequences with
learned halting). Pure Zag, pinned safebin znc. Prereg committed alone
before implementation (`4df7773`); one transparent amendment
(`6123156`, prediction arithmetic only) before the formal battery.

## Verdict: PASS

The Section 11 generalization composes the fixpoint workload that the
frozen U provably cannot. `gc_solve` at seqmax=8 reports
`ARM=GC PROB=QC ANS=1005 TRIES=23`: the U prefix exhausts (14 tries,
WIDEN=1, found=0, exactly the frozen boundary run), the k=3 sequence
phase tries 8 admitted sequences (all fail), and [0,0,0,0] --
lexicographically first at k=4 -- executes stepwise
1001->1002->1003->1004->1005, halts at end-of-pass, verifies 1005==exp,
and records all four steps via observe. No WIDEN=2 fires.

The reduction holds exactly: `gc_solve` at seqmax=2 produces
byte-identical stdout to the frozen U on all six worlds (5 pairs +
fixpoint workload). The generalization is strict, not parallel.

## Results

Build: `znc gc_full.zag -o gc_bin`, `znc gc_redfull.zag -o gc_redbin`
(pinned safebin znc; native binaries; the znc analyzer warnings on the
GEN regression assemblies are pre-existing in frozen d6_gen.zag and
non-blocking).

- `gc_run1/2/3.txt`: 3/3 byte-identical, sha256
  `c23127f7f74e2ab7f94dea98b6bb62fbe807ced278d359bc98481599ed877663`
- `gc_red1/2/3.txt`: 3/3 byte-identical, sha256
  `150a444fb1a29ba3c92b6442519b8aaf726cb1f4212008fd60040e293167dd38`
- QC trial trace (seqmax=8):
  - U prefix: 2 admitted singles + 2 admitted pairs + WIDEN=1 with 10
    retried pairs (12 INTER= lines), found=0 -- the frozen boundary.
  - k=3 (8 admitted by the chain rule): [0,0,0]->1004;
    [0,0,2]->1003 (output==input halt at step 3); [0,2,0],[0,2,2]->1002
    (halt at step 2); [2,0,0],[2,0,2],[2,2,0],[2,2,2]->1001 (halt at
    step 1). 8 tries, 14 INTER= lines, all fail.
  - k=4: [0,0,0,0]->1002,1003,1004,1005: SUCCESS. 1 try.
  - TRIES=23 = 14+8+1. Census: MAP 0 n=9 (5 teach + 4 recorded),
    inmask=1 outmask=1; others unchanged.
- 5 pairs at seqmax=8: P1 ANS=65 TRIES=3; P2a ANS=2 TRIES=3;
  P2b ANS=2 TRIES=7 WIDEN=1; P3 ANS=2 TRIES=3; P5 ANS=3 TRIES=4 --
  byte-identical to frozen U (up to the ARM=GC label).
- Reduction at seqmax=2: stdout byte-identical to
  cyc_run1.txt ++ u_run1.txt (empty diff).
- GEN regressions (frozen GEN, unmodified): diamond battery
  byte-identical to gsf_diamond_run1.txt (sha256 962ca4f0...);
  generality battery (Q1 fan-in ANS=5, Q2 DAG-4 ANS=5, Q3 chain-3 ANS=2,
  Q4a partial ANS=207, Q4b honest decline ANS=-2) byte-identical to
  gg_run1.txt (sha256 4b81226d...). 3/3 byte-identical each.

## Kill bar results

- C1 COMMIT-ORDER: PASS. Prereg commit `4df7773` (PREREG.md +
  NAMECHECK.md only) strictly precedes the amendment (`6123156`) and
  the implementation commit (`4f8b371`); git log order verified.
- C2 DETERMINISM: PASS. 3/3 pairwise byte-identical (cmp) for gc_bin,
  gc_redbin, and both GEN regression binaries; digests recorded.
- C3 REDUCTION: PASS. gc_redbin stdout cmp-empty vs
  ref_cyc_out.txt ++ ref_u_out.txt. seqmax=2 IS U, structurally (the
  sequence block is guarded by `if(seqmax>=3)`) and empirically.
- C4 CYCLE-PASS: PASS. `ARM=GC PROB=QC ANS=1005 TRIES=23`, no WIDEN=2,
  exactly per PREREG_AMEND1.
- C5 U-REGRESSION: PASS. seqmax=8 5-pair section relabeled ARM=GC->UNI
  is cmp-empty vs ref_u_out.txt. U's pairs are solved in the frozen
  prefix before any sequence trial runs.
- C6 GEN-REGRESSION: PASS. Diamond and generality batteries
  byte-identical to their recorded outputs. Pipelines and DAGs stay in
  the envelope; cycles join them.
- C7 OPACITY: PASS. Banned-token grep over all built sources empty;
  every exercised identifier a bare integer.
- C8 NO-CYCLE-HANDLER: PASS. Mechanical: `fixpoint` occurs in
  gc_uni.zag only inside `//` comments. Read-audit: the halting checks
  in gc_try_seq --
  `if(v<0){ return c; } ... if(v==prev){ break; } if(i>=cap){ break; }`
  -- execute after every step of every sequence trial with no branch on
  repetition, MAP identity, or shape. The output==input halt fires for
  IDENT MAPs on any sequence, not just repetitive ones; it is the
  Section 11 termination vocabulary, not a cycle handler.

## What the PASS shows (and does not show)

Shows: U's three precise lacks (re-application, termination vocabulary,
state carry) are jointly repaired by ONE general principle -- ordered
trial over sequences with per-step halting in contract vocabulary --
without a cycle handler, a new opcode, a new behavior class, or a new
admission dimension. The same binary that solves the 4-deep fixpoint
iteration reduces to U byte-for-byte at seqmax=2 and leaves U's 5 pairs
and GEN's diamond/fan-in/DAG-4/chain-3/partial outputs untouched.

Does not show: other cycle families (oscillatory, convergent-signal,
multi-structure feedback) -- pre-declared untested. The fixpoint halt
fired in this workload only as an early-stop on failing trials
([0,0,2], [0,2,*], [2,*,*]); the winning trial [0,0,0,0] halted at
end-of-pass. Data-dependent halting as the OPERATIVE stop of a winning
trial (e.g. a fixpoint beyond SEQMAX reached by the output==input halt
on a longer run) is not exercised here. SEQMAX=8 and CAP=8 are frozen
researcher bounds, not learned values. The HALT-kind signal (Section 11
option) remains unimplemented.

## Disclosed amendment (honest record)

PREREG_AMEND1 (committed `6123156`, before the formal build.sh battery;
only an exploratory smoke compile/run had occurred): Section 5.1's
hand-count of admitted k=3 sequences was 16, the correct consequence of
the frozen chain rule is 8 (m1 is constrained as the left element of the
first adjacent pair, not only by the initial kind check); TRIES 31->23.
The Section 2 mechanism spec was untouched; the implementation already
followed it. No kill bar was weakened: C4's substance (ANS=1005,
found=1, no WIDEN=2) is unchanged.

## Composition envelope status

After this battery: pipelines (U, byte-identical at seqmax<=2),
re-applicable sequences with learned halting (gc_solve, this lane), and
value-graph DAGs (GEN, regression-verified) are covered by mechanisms
that share U's principles (kind-set contracts, ordered trial,
end-to-end verification, failure-triggered widening, success
recording). The envelope grew by generalization, not by a new engine.
