# L3A-TRACE Red Team: Sealed Attack Plan

## Target

`e16cc0391` (L3A-TRACE-CLEAN-BUILD-PASS). The clean rebuild of the
trace-invention mechanism. 884 lines of Zag, zero Python, 3/3
byte-identical, C0-A A1-A7 pass.

## Claim under attack

BUILD-PASS (steps 1-3): the five frozen bars reproduce from an
independent implementation. I am attacking whether the bars actually
demonstrate what they claim, not whether the code runs.

## Assumed-false stance

I assume the BUILD-PASS is misleading and try to break it. A break means:
the bars pass for the wrong reason, the mechanism is fragile to trivial
changes, or a simpler explanation accounts for the results.

## Attack 1: SEGMENT-MATCH is a hardcoded oracle (static + probe)

**Theory.** The verdict requires `segmatch=1`, which is an exact-byte check
that the detected segment equals `[IN0:0, IN0:0, MUL:0]` = `[1,1,5]`
(source lines ~764-771). If the detector finds a semantically identical
but syntactically different segment, `segmatch=0`, bars (b) and (e) are
skipped, and the verdict is FAIL.

The comment in the source admits this: "the downstream bars assume the
intended invention [(IN0,0),(IN0,0),(MUL,0)]." The beam's lexicographic
tie-break "prefers IN0,IN0 over IN0,DUP (both push x,x), so [1,1,5] is
the reachable form."

This means the test is not "did the learner invent something useful" but
"did the learner produce the exact bytes the researcher expected." The
invention is downstream of the beam's arbitrary tie-breaking.

**Probe.** I will construct a minimal Zag program that replays the
detector's selection logic on two synthetic trace sets: one where the
beam-equivalent solutions contain `[1,1,5]`, one where they contain
`[1,8,5]` ([IN0,DUP,MUL], also computes x*x). I will show that the
segmatch guard accepts the first and rejects the second, even though
both are valid inventions of "push x*x". This demonstrates the oracle.

Actually, a stronger and more honest probe: I will modify a COPY of the
battery to remove the segmatch gate from the verdict (keep it as a
reported value, not a verdict condition), and show what the pipeline
does when the detector is allowed to report whatever it finds. But the
frozen battery always finds [1,1,5], so this alone proves little.

The sharpest runnable probe: change the beam's expansion order in a copy
so that DUP is preferred over the second IN0 (swap their lexicographic
order), re-run, and observe whether the detected segment becomes
`[1,8,5]` and the verdict flips to FAIL despite a valid invention. This
directly tests whether the BUILD-PASS is robust to an arbitrary
researcher choice (expansion order) or fragile to it.

**Kill condition.** If swapping the expansion order flips a PASS to a
FAIL with no change to the learning logic, the BUILD-PASS is fragile
to researcher tie-breaking, and the "invention" is beam-determined.

## Attack 2: Generality probe with a different shared regularity

**Theory.** The mechanism claims to be a generic segment detector. I will
test it on a task battery with a DIFFERENT shared exact segment.

**Probe.** Copy the source. Change `buildtask`:
- T0: y = (x+1)*(x+1), x in 0..6.
- T1: y = (x+2)*(x+2), x in 0..6.
- T2 (held-out): y = (x+1)*(x+1) + (x+2)*(x+2), x in 0..6.

Expected beam solutions (to be verified by running):
- T0: [IN0, PUSH:1, ADD, DUP, MUL] (length 5).
- T1: [IN0, PUSH:2, ADD, DUP, MUL] (length 5).
Shared exact segments of length>=2: [DUP, MUL] (arity 1, produced 1).
The PUSH args differ, so [PUSH:1,ADD] vs [PUSH:2,ADD] do not match.

I will adjust the SEGMENT-MATCH guard to expect [DUP,MUL]=[8,5] (or
report whatever is found), and check whether the full pipeline
(detect -> reify -> persist -> reuse -> ablate -> swap) coheres on the
new battery. T-REUSE must find a solution using TCALL for the new T2.
T-ABLATE must fail without it.

**Kill condition.** If the pipeline does not cohere (e.g., detector
finds nothing, or reuse fails, or the invented segment is degenerate),
the mechanism is tuned to the frozen battery, not general.

**Pass condition (for the mechanism).** If all bars adapt cleanly to
the new shared regularity, the detector is genuinely generic within
its bounded scope, and Attack 2 confirms rather than breaks.

## Attack 3: Negative control (no shared segment)

**Theory.** A detector should honestly report NO-INVENTION when there is
nothing to invent.

**Probe.** Copy the source. Change `buildtask`:
- T0: y = x*x, x in 0..6.
- T1: y = 2*x+1, x in 0..6.
T0 solutions contain [IN0,IN0,MUL]. T1 solutions are like
[IN0,PUSH:2,MUL,PUSH:1,ADD]. There is no shared exact length-2 segment
across every episode of both tasks (to be verified by running).

**Kill condition.** If the detector reifies a spurious segment
(credit>=2 on a coincidental match), the R2 conditions are too lax.
If it honestly prints NO-INVENTION, the negative control passes and
this attack confirms the mechanism's honesty.

## Attack 4: Ablation budget (is the advantage representational?)

**Theory.** T-ABLATE shows 2/7 without TCALL at beam_w=600, max_len=8.
But if a wider/longer search solves T2 7/7 with base ops, the invention
provides only search efficiency within an arbitrary budget, not a
representational capability.

**Probe.** Copy the source. In the T-ABLATE phase only, raise beam_w to
6000 and max_len to 12 (keep everything else identical). If the ablation
search now reaches 7/7 without TCALL, the "advantage destroyed" claim is
budget-relative.

**Kill condition.** If wider search solves T2 without invention, the
ablation bar does not establish representational necessity.

**Note.** This does not break BUILD-PASS as stated (the frozen budget
is part of the bar), but it bounds the interpretation: the invention
is load-bearing only within the frozen search budget.

## Attack 5: State-pressure robustness

**Theory.** The name table has 4 slots (toff/tlen are 16 bytes). The
battery performs exactly one reification. What happens on the second?

**Probe.** Copy the source. After the first reify, run `detect` again
on the same traces (it will find the same segment) and call `reify` a
second, third, fourth, fifth time. Observe whether the 5th reify
corrupts memory (writes past the 16-byte name table) or is safely
refused.

**Kill condition.** If the 5th reify silently corrupts adjacent memory,
there is a memory-safety bug in the learner state. (This is a robustness
finding, not a BUILD-PASS break, but it is a genuine hole.)

## What I will NOT do

- I will not modify the committed source at e16cc0391. All probes use
  COPIES in my owned path.
- I will not change the frozen battery and claim the original fails.
  Attacks 2-5 use modified copies to probe generality and robustness;
  only Attack 1 tests the fragility of the frozen verdict itself.
- I will not use Python for anything.
- I will not touch the contaminated paper.

## Execution order

1. Commit this plan alone (K1).
2. Build the pristine binary from e16cc0391, confirm 3/3 baseline.
3. Attack 1 (expansion-order swap). This is the sharpest.
4. Attack 3 (negative control). Cheap and informative.
5. Attack 2 (different regularity). Most work, highest information.
6. Attack 4 (ablation budget). Bounded interpretation.
7. Attack 5 (state pressure). Robustness.
8. Write results, commit, report.

## Verdict labels

- L3A-TRACE-REDTEAM-BREAKS: at least one attack breaks the BUILD-PASS
  claim or reveals the bars are misleading.
- L3A-TRACE-REDTEAM-SURVIVES: all attacks either fail to break the claim
  or confirm the mechanism's honesty/generality.
- Mixed findings will be reported per-attack with an overall label.
