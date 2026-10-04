# Skeptic: wave-20260929-1421pdt debate

## Provenance probe (answered verbatim in every motion)

What is the provenance of the artifacts under judgment, and what exactly is
new versus inherited? Same answer as the advocate's: H-CAUSAL2 prereg text,
sources, logs, and probes are inherited from 1121pdt; new this wave are the
re-freeze, the re-run reproductions, the red-team review, and these debate
records. The 1121pdt RESULT_CAUSAL2.md is worker-reported data, not evidence.
The fork-battery 1121pdt evidence is inherited; its CONFIRM verdict was never
debated. Nothing exists for pi_rev2.

## M1: H-CAUSAL2 -- AGAINST adoption as stated (narrow it further)

Three attacks. First, the 1121pdt wave record contains a false claim about
its own commit order. A wave that misreports its process does not get the
benefit of the doubt on its other claims; the re-verification from bytes is
the only thing that saves this candidate, and the debate should say so
plainly rather than treating the re-run as routine.

Second, the re-freeze does not cure what the rule is for. The rule exists so
a prereg cannot be tuned to an implementation. Here the implementation
sources were authored in 1121pdt, possibly after the prereg text was written,
in a single commit that hides the order. Re-freezing the text now and
re-running cannot retroactively establish that the prereg predated the
source authorship. The S8/CF2 precedent is real, but CF2's re-freeze changed
a bar (A3 := 1) transparently; here the claim is stronger (the prereg
predates the code) and the evidence for it is weaker (a single commit).
The honest statement is: ordering is established for the re-run, not for the
original authorship. The K2-7 by-construction argument carries the
authorship-separation weight, not the commit order.

Third, the invention headline is thinner than the verdict language. P-B2a is
exact-episode recall. The prereg froze "H-PRESS adopted" as the expectation
and the mechanism stores the split, but the scoreboard's most-cited probe
does not exercise the invented rule. If the skeptic weights rule-application
probes only, the invention evidence is P-A2 and P-B2c: two probes, both on
the same s1=0 rule. That is thin for "invents a conditional causal rule,"
even bounded.

Concession: the bars as frozen are satisfied, the reproduction is genuine,
K2-7 holds by construction, and the red team found no gaming. The skeptic
does not allege fabrication. The demand is narrower verdict language and
permanent caveats, not a kill.

## M2: Fork battery 1121pdt -- AGAINST confirmation without qualification

The manifest references JUDGE_1121.md, which does not exist, and the driver
batch_1121.sh is not in the workspace. A verdict whose debate record is
missing and whose driver is gone rests entirely on output files that anyone
could have written. The re-tally is real but it tallies files, not a run.
Confirm only with the qualification that this is a re-tally of inherited
outputs, and let the fresh 1421pdt battery carry the process-confirmation
weight.

## M3: Fork battery 1421pdt -- hold for results

No position until the tally lands. If any entry FAILs, the skeptic will
demand the per-fork "what broke" before any CONFIRM.

## M4: Interactive survey -- weak FOR, with a scope note

The survey greps .zag diffs only. A chat loop in a shell script or a renamed
extension would escape it. The scope is the established convention and the
tnn_chat FIT cadence covers the known instrument; the skeptic notes the
boundary rather than blocking.

## M5: pi_rev2 -- AGAINST letting the frontier slip quietly

An entire wave's procedure-invention lane produced zero bytes. The L3
criterion-12 frontier (revision after counterexample) is the top priority
and it just lost a wave to runtime flakiness. Recording NO-EVIDENCE is
correct, but the debate should bank an explicit commitment: the next wave
freezes the pi_rev2 prereg as its first design-lane act, rather than letting
"queued" mean "forgotten."

## M6: Commit-order self-check -- AGAINST calling it simply VALID

The check passes for the re-run evidence commit. It does not pass for the
sources, whose first commit (d18f7f68d) precedes the re-freeze. Future waves
must not cite this wave as precedent for "re-freeze cures any ordering
problem": it cures the evidence-run ordering under S8, and the
authorship-separation argument here came from K2-7 by-construction, not from
commit order. Record the distinction.
