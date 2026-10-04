# JUDGE: wave-20260930-1121pdt verdict slate (recovery debate)

Parent-agent inline debate, 2026-09-30. Rulings below are reasoned from
the committed evidence and the two records above. Every motion carries
the skeptic's provenance probe; the probe answers are adopted into the
record.

## M1: F3a3 BUILD-PASS. ADOPTED, with a standing caveat.

The skeptic's pattern attack is the strongest point in this debate and
it is sustained as a caveat, not as a kill. The facts: the mechanism
passed every behavioral bar it faced across all three rounds. F3a:
K-F3-1, K-F3-2, K-F3-3 passed on first-draft text; only K-F3-4 died on
a fixture collision. F3a2: K-F3-2, K-F3-3, K-F3-4 passed on the
corrected text; only K-F3-1 died on unsatisfiable text. F3a3:
K-F3-1 corrected and passing, 3/3 byte-identical runs (b5389d71),
exit 0, fails=0. The mechanism never failed a behavioral bar. The
corrections were textual (disjointness, satisfiability), never
threshold-lowering. The verdict rule was frozen before the evidence.

But the skeptic is right that "survived its adversary" overstates it:
the passing run faced the third draft of the bar text. Ruling: ADOPT
the BUILD-PASS, and enter the standing caveat into loop governance.
Every future adversary bar text must pass a fixture-collision
pre-check before freezing, and adversary families should be authored
by a party with no stake in the mechanism. The declared disjoint set
{k,m,r,v} is exhausted; the next round requires a fresh disjoint set.
Numbers cited: 3/3 byte-identical, sha b5389d71, 0 FAIL lines.

## M2: F3b BUILD-PASS. ADOPTED, narrowed.

The skeptic's L1-vs-L2 press is answered by K-F3B-5: the g program
contains N ([N C1 SUB]) because T2 killed the constant shortcut that
T1 alone permitted. That is structural response to training pressure
beyond parameter fitting, and it is exactly what the frozen bar
demanded. The verdict claimed is bounded L2+, not L3, and the evidence
meets it: 6/6 bars with numbers (K-F3B-1 discovery fails=0, K-F3B-2
8/8 hidden, K-F3B-3 diff clean with node types unchanged, K-F3B-4
byte-identical x3, K-F3B-5 g-probe n=7 -> 6, K-F3B-6 no literals),
cost budget passed (0.007 s vs 60 s, 417 lines vs 800).

The skeptic's narrowing is adopted into the verdict: bounded L2+ on
the drop-last family only. No transfer evidence exists, and this
verdict must not be quoted as general procedure invention. The search
menu is researcher-fixed; the invention, if any, is the
length-program interface slot, not the affine form.

## M3: H-EXP2 v2 prereg. ADOPTED AS FROZEN, with a precondition.

A prereg is adopted for what it freezes. This one freezes a strictly
harder sustained goal than v1 (sequence of experiments, execution in
scope, probe budget, sealed laws W-A/W-B committed at cc87d6f09). The
skeptic's bar-text audit is adopted as a precondition to
implementation: every bar checked for fixture collisions and
satisfiability, seal-holder for W-A/W-B named with a verifiable seal,
before any implementation commit. Given the F3a/F3a2 history, this is
cheap insurance, not bureaucracy.

## M4: DDES R2. ADOPTED AS PROVISIONAL BUILD-PASS.

The skeptic's process attack is sustained. The implementer and the
verifier are both the recovery coordinator; that is builder-checked
work, not independent verification. The numbers are strong (3/3
byte-identical 297d0b59, World F correct convergence both configs,
A-E byte-identical to DDES_RAW.txt) and the prereg d31e901b0 is a
strict ancestor of the implementation, so the verdict is ADOPTED as
PROVISIONAL: the t*=0 soundness hole is closed pending independent
re-verification of K-R2.1..K-R2.6. Classification: soundness repair
on a strong-L2 mechanism. No L3 claim attaches, and this verdict must
not be quoted as promotion of DDES.

## M5: Process. RECORDED.

This is a parent-agent inline recovery debate, labeled as such. It is
not an independent debate group and must not be cited as one. It
closes the 11:21 verdict slate: M1-M4 above. The 14:21 and 17:21
waves rendered no verdicts; their recovery commits stand as evidence.
The fork-battery enumeration manifest (87 entries) is a pre-run gate,
not results; full fork results remain queued. LOOP_STATE.md is to be
updated with these four verdicts and their caveats.
