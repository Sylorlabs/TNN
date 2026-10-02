# RESULT_F3A.md

Wave: wave-20260930-0221pdt. Prereg: PREREG_PI_REV2_F3.md (frozen,
committed alone at d80106155, this wave's first act).
Implementation: inherited byte-identical from 847a8f10f
(wave-20260929-2321pdt); NOT modified this wave (git diff
847a8f10f -- <file> empty; verified before building).

## What was run

The frozen binary was rebuilt from the committed source with the
pinned znc 498abcb5 (build emitted one benign analyzer lint A0102 at
line 604, pre-existing code; binary produced). Three executions with
argv[1]="w" (adversary byte per the declared rule: last letter of the
sorted frozen allowed set), outputs in EVIDENCE_F3A_run{1,2,3}.txt.

## Evidence

3/3 byte-identical (sha256 97dd42762deb3dbb37d404eacea40b52c1d65e01c101ce54b3939c17ff99fb48),
exit 0, fails=0 on all three. P8 section (first execution):

- COUNTEREXAMPLE_DETECTED(wab)
- DIAGNOSIS pos=0 byte=119 conflicts=0
- PRIMITIVE-CONSTRUCTED pos=0 byte=119
- alt = index 2 (C0 broadcast-first; CHECK P8-F2-alt-C0: PASS)
- VERSION v3 ACTIVE (parent v2)
- PREDICT wab -> www [ok]; xab -> xxx [ok]; abc -> ccc [ok];
  xy -> xx [ok]; defg -> gggg [ok]
- reuse: PREDICT wqw -> www [ok]; CHECK P8-F2-reuse-no-revision: PASS
- R cell 8/8 [ok] (zag, 12, q, hello, ptc, s, eghjjupazbnf, q)

## Kill-bar scorecard

- K-F3-1 (first-execution correctness): PASS. Every frozen line
  present on the first execution (see above).
- K-F3-2 (determinism): PASS. 3/3 byte-identical.
- K-F3-3 (anti-tuning): PASS. Grep audit of the committed
  implementation: zero char literal 'w'; zero "wab"/"www"/"wqw";
  zero numeric 119. The byte reaches machinery only via the argv
  data flow.
- K-F3-4 (disjointness): FAIL. 'w' occurs in the frozen F1-reuse
  fixture input "xqw". The bar text ("'w' occurs in none of the
  frozen T, F1, or R fixture inputs") is not satisfied.

## Verdict

BUILD-FAIL per the frozen verdict rule (any bar failing). Killing
line: K-F3-4, 'w' in "xqw". The kill is on the family/bar design,
not the mechanism: K-F3-1/2/3 all pass with a clean white-box trace
(DIAGNOSIS (0,119) derived from the F-vs-P comparison; conflicts=0),
so no mechanism failure is evidenced.

## Audit finding (new this wave)

The parent prereg's allowed-set disjointness rationale is
inaccurate. Of the frozen allowed set {i,j,k,l,m,n,o,r,t,u,v,w},
only {i,k,m,r,v} are genuinely absent from all frozen fixture input
strings: j, l, n, o, t, u occur in R inputs ("eghjjupazbnf",
"hello", "ptc"); w occurs in the F1-reuse fixture "xqw". 'i' was
spent on F2. The genuinely-disjoint pool for future adversary runs
is {k,m,r,v}.

## Queued remedy

Next wave: re-freeze F3a with corrected K-F3-4 text (adversary byte
absent from every frozen fixture input string in the parent
prereg's fixture list, audited before the run) and a byte from
{k,m,r,v} by a declared deterministic rule; then re-run. F3b design
stands frozen (execution queued behind its interface-extension
prereg); step 4 (independent reproduction) follows the re-run.
