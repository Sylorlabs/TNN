# REPORT: Belief under Copied Misinformation and Source Degradation (Parent Queue #7)

Verdict: BELIEF-MISINFO-COMPLETE. Frozen prereg a22818224 governed every
check below; all kill bars K1-K5 hold. 3/3 runs byte identical
(sha256 f3afd043e692e1a1a4cfd21d4ad693e7809a29f927cd2ebab87669359509fa80).
Binary stdout byte verified (od -c spot check) before trusting it.

## What was tested

Four worlds on the frozen belief learner machinery (C211/C223/H-DECEPT-1
lineage: reliability = 1000*correct/total after 2 verifications,
independence discount, event identity register, wmax bands), EVN = 64
unchanged, 0 new semantic cases, 0 modes, 0 bridges, 0 handlers.

## Findings

### (a) Copied misinformation: yes, copied; corrected after 2

World M1. After S built rel 1000 over 20 correct rounds, S's strong
false H1 claim was copied into belief: st == 11 (PROVISIONAL H1,
s1 == 3000, s2 == 0). The learner does copy misinformation from a
trusted source. Two independent moderate contradicting sources flipped
it: W1 (s2 == 2000, st == 12), then W2 (s2 == 4000, st == 22).
Correction count: exactly 2 contradicting observations.

Two sharper results. First, exposure does NOT move belief: verifying
S's lie dropped rel(S) to 952 but the stance stayed 11. The downgrade
lives in the source model; the recorded false evidence is not retro
edited, so the false belief persists through exposure. Second,
correction is fragile: S reasserting H1 moderate at rel 952
(contrib 1904) moved s1 to 4904 against s2 == 4000 and reopened the
stance to UNCERTAIN (st == 12). One reassertion by the liar re
fragilizes the correction.

### (a2) Single-source correction count: 3

World M1b. One contradicting source under the independence discount
contributed 2000, 1000, 500 across three claims: stances 12, tie (2),
then 22 (s2 == 3500). Correction count with one source: exactly 3
observations. The discount costs one extra observation versus two
independent sources.

### (b) Source degradation: downgraded, exactly on the fraction

World M2. S went noisy (wrong, wrong, right, wrong, right, wrong):
rel(S) traced 952, 909, 913, 875, 880, 846, exactly 1000*correct/total
at every step, printed against the null. The downgrade is exactly
instance linear: each outcome moves reliability by one instance, no
defector acceleration, no cliff. Noise barely recovers (909 to 913,
875 to 880). The W1 control stayed 1000 throughout, so the downgrade
is source specific, not global drift. Downstream effect: S's moderate
H1 claim at rel 846 contributed 1692, strictly less than the 2000 a
rel-1000 source would contribute. The downgrade discounts future
evidence weight.

### Forgiveness-clock: downgrade is effectively permanent

World M3 (same learner state as M2, no reset). After S became fully
reliable again, rel(S) traced 870, 888, 902, 913 at +5/+10/+15/+20
clean rounds, exactly the fraction null. After 20 fully clean rounds
rel(S) == 913, still 87 short of 1000. The fraction rule has no
forgetting: recovery is asymptotic, and finite history never restores
1000. The forgiveness-clock as a mechanism is ABSENT from the current
machinery. This is the finding, and it specifies the missing mechanism
(recency-weighted reliability or a forgiveness window) as the next
hypothesis.

## Kill bar results

K1: 3/3 byte identical. HOLD.
K2: P1-P6 exact (M1 copy/exposure/contradiction/fragility; M1b count 3).
HOLD.
K3: P7-P8 exact (M2 trajectory and downstream discount; W1 control
1000). HOLD.
K4: P9 exact (M3 recovery 870/888/902/913; final 913; nevicted == 0).
HOLD.
K5: pure Zag, safebin PATH, no forbidden executables, prereg committed
before implementation, 0 modes/bridges/handlers, frozen source
untouched, paper untouched, nothing pushed, explicit pathspecs. HOLD.

Rationality (evidence relative): 5/5. M1 correction 22 rational (two
independent moderate sources outweigh one strong stale claim). M1
reassertion 12 rational (S at 952 with a 20-round record is still
credible; its reassertion honestly reopens the question). M1b 22
rational (discounted totals still exceed the stale 3000). M2 downgrade
rational (fraction tracks evidence exactly). M3 non-recovery rational
given the fraction rule, and it is the finding: the rule lacks
forgiveness.

## Architecture accounting

Cognition lines added: 0 (same learner machinery, new world scripts
only). New hardcoded semantic cases: 0. Modes: 0. Bridges: 0.
Handlers: 0. Capability source delta: 0.

## Deliverables in belief_misinfo/

PREREG.md (frozen, committed first), NAMECHECK.md, REPORT.md (this
file), belief_misinfo.zag (source), belief_misinfo_bin (binary),
compile.log, run1.txt, run2.txt, run3.txt.

## Follow-ups specified (not decided here)

1. Forgiveness-clock mechanism hypothesis: recency-weighted reliability
   or a forgiveness window, preregistered, tested against the M3
   trajectory baseline (must reach >= some frozen bar within N clean
   rounds while preserving the M2 linear downgrade under noise).
2. Retro-edit vs source-model question: exposure currently leaves
   recorded false evidence untouched; whether the learner should ever
   revise recorded support on exposure is an open design question.
