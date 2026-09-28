# G6 SYNTHESIS — scaffold-and-release at 100×: does the scaffold buy
persistence teaching cannot?

**Answer: no — on either task, at 100×, deliberate teaching matches the
S5×R1 scaffold on integrity and persistence and beats it on acquisition
speed, cost, and (P2) acquisition integrity.**

## The two forks

| | P1 (D1 CONTEST-on-collision) | P2 (novel memory triage) |
|---|---|---|
| Episodes | 848 (800 = 100×) | 850 (800 = 100×) |
| Baseline acquires | E14 (4/4 cal) | E16 (6/6 cal) |
| Scaffold releases | E38 (streak 8) | E23 (streak 8) |
| Integrity | both perfect, 848 eps | both perfect, 850 eps |
| Late failure episode | none | none |
| KB-4 value-add | ❌ FAIL | ❌ FAIL |
| Cost (audit entries) | 1743 vs 2588 (1.48×) | 1962 vs 2815 (1.43×) |

Both runners: 55/55 (P1) and 53/53 (P2) checks, TN_FAILURES=0,
byte-identical reruns, no-RNG / no-signal-in-select / no-accumulation
static checks all pass.

## What the 100× horizon actually tested

The honest preregistered expectation was that KB-4 would fail —
deterministic teaching should persist as well as the scaffold while
acquiring faster and cheaper — and the adversarial probes (40
temptations + 20 contradiction probes per fork, sustained across all 800
episodes) were the real attempt to falsify it. They didn't. Neither arm
in either fork drifted, gamed, or collapsed at any episode, including
the last-100 spotlight that runs past the trial's entire 10× window.

## Where the scaffold lost

1. **Acquisition speed:** 2.7× slower on D1 (38 vs 14), 1.44× on triage
   (23 vs 16). The scaffold must burn episodes on wrong policies to
   earn its contradictions; teaching states the rule and verifies it.
2. **Cost:** 1.4–1.5× the audit entries, plus the honest-signal and
   adversarial-episode design effort.
3. **Acquisition integrity (P2):** the scaffold's policy search killed
   k4 — an important, high-refcount memory — before the contradiction
   arrived. Teaching's sim-only calibration never harms the store to
   learn. (P1's analogue: the scaffold contested 20 identity probes
   blindly that teaching discriminated live — harmless here, but the
   same mechanism-blindness.)
4. **Nothing on the other side:** there is no axis where the scaffold
   won. Integrity tied. Persistence tied. Precision favored teaching.

## Relation to the RL trial

The RL verdict ("reward cannot see procedure") motivated the scaffold's
contradiction evidence, and the scaffold is indeed cleaner than reward:
its signal judges decisions against the rule rather than accumulating
outcomes. But at 100×, that cleanliness buys nothing over simply
teaching the rule deliberately. The scaffold is a more expensive,
slower, slightly more destructive way to arrive at the same installed
behavior — on both tasks tested.

## Bottom line for H

G6 contributes **no support** to "scaffold-and-release is the legit best
path." Across D1 and a novel memory-agency task, at a 100× persistence
horizon, with sustained adversarial pressure and a learner-initiated
release: deliberate teaching ≥ scaffold-and-release on every measured
axis. If the hypothesis is to survive, it needs a task where teaching
cannot install the behavior at all — not one where both succeed and the
scaffold merely costs more.
