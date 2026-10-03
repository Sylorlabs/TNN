# REPORT: CYCLES-GENERALIZE -- Verdict PASS

Date: 2026-10-03. Worker: cycles-generalize.
Lane: `docs/lab/research-lead/overnight-20260928/cycles_generalize/`.
Battery: preregistered generality tests for GEN-CYCLES's sequences+halting.
Pure Zag, pinned safebin znc. Prereg committed alone (`c09acbd`);
implementation commit follows in this same commit (see git log).
No amendments: every frozen prediction matched exactly.

## Verdict: PASS

Sequences+halting is general, not fitted to one fixpoint family:

- T1: the frozen, unmodified mechanism solves a second fixpoint family --
  an alternating two-structure 5-hop chain ([0,1,0,1,0] wins at k=5) --
  reporting `ARM=GC PROB=QG ANS=3006 TRIES=236`, exactly as preregistered
  (15 + 39 + 139 + 43). Neither MAP alone suffices; the chain rule and
  the trial order do all the work.
- T2: data-dependent halting is the operative (and necessary) stop of a
  winning trial. The chain rule rejects the pure repetition [0,0,0] but
  admits [0,0,1]; the winner halts via output==input at step i=2 < k=3
  (exactly 2 INTER= lines for a k=3 trial), reporting
  `ARM=GC PROB=QH ANS=4002 TRIES=15`. Code audit: without the (b) check
  the trial would continue into MAP 1 = COUNT at 4002 -> -2 miss -> fail.
- T3: the preregistered-but-missing HALT-kind contract signal is
  implemented as a strictly additive extension (kind 3, class-5 STEP-HALT
  emitting -3, one added `if(v==-3){break;}` in the stepwise loop).
  Control: the frozen mechanism on the same workload bytes FAILS
  (`ARM=GC PROB=QK0 ANS=-2 TRIES=78`, WIDEN=2 fires) -- the signal is
  genuinely absent from the frozen core. Signal: the extended executor
  halts the winning trial on INTER=-3 and verifies
  (`ARM=XH PROB=QK ANS=5002 TRIES=15`). Reduction: the extended executor
  on the frozen base is byte-identical to the frozen binary on QC/QG/QH
  (sha256 568a0abd... both).

## Results

Build: four binaries from pinned safebin znc (zagd-unavailable warnings
are environmental and non-blocking, as in GEN-CYCLES):
- cg_fbin (frozen base + frozen U + frozen mechanism; QC,QG,QH)
- cg_fbin0 (frozen; QK0 control at seqmax=3)
- cg_xbin (frozen base + frozen U + EXTENDED mechanism; QC,QG,QH)
- cg_xsbin (extended base + frozen U + EXTENDED mechanism; QK signal)

Runs: 3/3 byte-identical each (cmp); digests:
- cg_run1.txt: 568a0abdd1c07a99a26c0741e115c4742bd436fbf62a2eb766fadba91e3db8c9
- cg_k01.txt: bc75bac97bfab7f240baac4cc60ca3a5d1de1e99b16444a2cdc81a0e2586c98d
- cg_x1.txt: 568a0abd... (identical to cg_run1.txt)
- cg_ks1.txt: 9b2fee8f3cce0da655f17895c99a16ba7a090f561eceb0e3b246d0a154d28a31

Traces:
- QC (C403 regression): ANS=1005 TRIES=23, unchanged from GEN-CYCLES.
- QG: U prefix 15 tries (3 singles + 8 pairs + 4 WIDEN=1); k=3: 39
  admitted, all fail (m3-sequences miss on 306; m2-sequences halt early;
  [0,1,0]->3004); k=4: 139 admitted, all fail ([0,1,0,1]->3005 max);
  k=5: 43 tried, [0,1,0,1,0] (lexicographic n=68) executes
  3001->3002->3003->3004->3005->3006, end-of-pass halt, SUCCESS.
  Census: m0 n=7 inmask=3 outmask=3; m1 n=5 inmask=3 outmask=3.
- QH: U prefix 14 tries (2 singles + 4 pairs + 8 WIDEN=1; pair trials
  print one INTER= line, v1 only); k=3: [0,0,0] rejected by the chain
  rule (final out{0}={2}∌1), [0,0,1] admitted and wins: INTER=4002,
  INTER=4002, (b)-halt at i=2<3. Census: m0 n=4 inmask=3 outmask=2.
- QK0 (control): U prefix 14; k=3: 18 admitted, all fail (class 5
  degrades to class-2 logic under the frozen base; the -3 is never
  emitted); WIDEN=2 retries 46 rejected k=3 sequences, all fail;
  ANS=-2 TRIES=78.
- QK (signal): U prefix 14; k=3: [0,0,0] rejected, [0,0,1] wins:
  INTER=5002, INTER=-3 (HALT-kind break, cur stays 5002 == exp).
  Census: m0 n=3 inmask=3 outmask=6 (bit 4 = learned HALT kind).

## Kill bar results

- G1 COMMIT-ORDER: PASS. Prereg commit `c09acbd` (PREREG.md +
  NAMECHECK.md only) strictly precedes this implementation commit.
- G2 DETERMINISM: PASS. 3/3 pairwise byte-identical for all 4 binaries.
- G3 T1-PASS: PASS. `ARM=GC PROB=QG ANS=3006 TRIES=236`, no WIDEN=2.
- G4 T2-PASS: PASS. `ARM=GC PROB=QH ANS=4002 TRIES=15`, no WIDEN=2;
  the last 3 INTER= lines before the QH report are
  -2, 4002, 4002 (build.sh audit): the winning k=3 trial printed
  exactly 2 INTER lines, so the output==input halt fired at i=2<k=3.
- G5 T3-CONTROL: PASS. `ARM=GC PROB=QK0 ANS=-2 TRIES=78`, WIDEN=2 fired.
- G6 T3-SIGNAL: PASS. `ARM=XH PROB=QK ANS=5002 TRIES=15`, no WIDEN=2,
  INTER=-3 present, m0 outmask=6 (HALT kind learned).
- G7 REDUCTION: PASS. cg_xbin stdout cmp-empty vs cg_fbin stdout
  (identical sha256).
- G8 FROZEN-INTACT: PASS. Lane gc_uni.zag/gc_base.zag/uni_nomain.zag/
  cyc_nomain.zag match Section 2 digests; diff hunks are exactly the
  preregistered ones (cg_uni: 38a39,41;48a52 with zero deletions;
  cg_base: 18c18,19;88a90;140a143,155;147a163).
- G9 OPACITY: PASS. Banned-token grep over all built sources empty;
  every exercised identifier a bare integer.

## What the PASS shows (and does not show)

Shows: (1) sequences+halting covers a second fixpoint family with zero
mechanism change -- the alternating two-structure chain is solved by the
same chain rule, trial order, and halting vocabulary; (2) the
output==input halt is not just an early-stop for losers: it can be the
operative and necessary stop of a winning trial, with the kind contracts
doing the admission work that forces the longer sequence; (3) the
Section 11 HALT-kind option is implementable as a strictly additive
extension -- a learned third kind carried by the existing mask machinery
with no new admission dimension -- and it changes behavior exactly where
preregistered (the -3 emission) and nowhere else (byte-identical
reduction).

Does not show: oscillatory / convergent-signal / multi-structure
feedback cycles (still untested); learned SEQMAX/CAP values (still frozen
bounds); whether HALT-kind belongs in the protected core (governance
question for Micah, not decided here). T2's necessity claim is relative
to the frozen increasing-k trial order.

## Composition envelope status

After this battery: pipelines (U), re-applicable sequences with learned
halting over single-structure fixpoints (GEN-CYCLES), alternating
multi-structure fixpoint sequences (T1), data-dependent operative halting
(T2), and an additive HALT-kind contract signal (T3) are covered, with
value-graph DAGs (GEN) regression-verified untouched. The envelope grew
by testing, not by redesign: the frozen core is byte-identical.
