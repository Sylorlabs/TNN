# SCAFFOLD-AND-RELEASE: PROGRAM SYNTHESIS

**For Micah — plain language, no jargon.**

## The question

You said scaffold-and-release "seems like the legit best path." We ran it
until it broke or proved itself: 19 forks across 6 groups, every one
against a plain-deliberate-teaching baseline on the same task, all
deterministic, zero randomness, every run reproduced byte-for-byte.

## The verdict: it's the best path exactly where the teacher can't be trusted. Everywhere else, plain teaching wins.

Not a coronation, not a burial — a boundary map. Here it is:

- **Teacher you trust → teach directly.** Faster (2–3×), cheaper (~half
  the audit trail), and it holds integrity just as well.
- **Teacher you might not trust → scaffold-and-release.** It's the only
  thing we tested that survives a lying teacher. Plain teaching
  deterministically installs the lie.

## Group by group

**G1 — Rematch (5 forks): does the release schedule explain the earlier
loss? No.** Five different release schedules, same task — the commit
point never moved (episode 29 every time). The loss to teaching lives in
the *commit* logic, not the *release* logic. Release timing is a cost
knob, not a capability knob. Two sharp edges found: cutting the scaffold
before commit means it never learns (it flip-flops between the right
answer and the cheat forever); a fading signal can strand the release so
it never fires at all.

**G2 — Richer scaffolds (5 forks): better students, still worse teachers.**
Hints, shaped curricula, demonstrations, adversarial examples — all much
faster than the plain scalar scaffold (episode 20–26 vs 38), all cured of
the blindness bug (they correctly do nothing when there's no real
contradiction). But none beats plain teaching: teaching installs at
episode 14, cheaper or equal cost, same integrity. The standout is
demonstration-then-fade — fastest scaffold we built — and it still loses.

**G3 — Lying teacher (3 forks): THE DECISIVE ONE. The scaffold survives
where teaching gets fooled.** The teacher taught the wrong rule
("rekeying is the right way to handle collisions"). Plain teaching
calibrated 4/4 *on the lie* — it checked that it understood the rule,
not that the rule was true — and installed the wrong procedure.
The scaffold never installs from statements at all; it only throws out
candidate behaviors when the world contradicts them. The lie got
contradicted, the lie got thrown out, the right behavior survived.
This is the one setting where scaffold-and-release is provably the
better path, and plain teaching provably cannot match it.

**G4 — Outcome tasks, the scaffold's home turf (3 forks): works
perfectly, still loses.** Zero integrity failures on any release
schedule — a real step past the earlier 40/40 demo. But teaching is
3–5× faster, ~2× cheaper, ties everywhere else. Also learned: the
8-episode "verification streak" before release isn't doing any work on
these tasks — cutting at commit is just as safe and cheaper.

**G5 — Dialogue withholding (2 forks): works, no advantage.**
Demonstration-then-fade teaches the withholding behavior fine, but ties
teaching on everything and costs more (27 demonstrations vs 1 rule
statement). Fade speed doesn't matter — fast fade weakly wins.

**G6 — 100× long horizon (2 forks): no late magic.** 800+ episodes, zero
late drift, zero late collapse, in both arms. Teaching matches the
scaffold on everything that matters and beats it on speed and cost.
One ugly asymmetry: the scaffold learns by *probing* — acting candidate
behaviors to see what breaks — and in one fork it destroyed an important
memory before the contradiction it was probing for ever arrived.
Teaching learns by *simulation* and never harms the store. Probing has
a body count; simulation doesn't.

**Python sweep: clean.** Every line of decision-making in the whole
program is pure Zag. Python appears nowhere except as documented
build-time glue outside the repo.

## Why it shakes out this way

Two different learning moves:

- **Teaching installs a procedure for reasons.** The learner simulates
  the rule, checks it against its standing laws, and installs it. Fast,
  cheap, safe — *if the teacher is honest.* The calibration checks
  understanding, not truth. Nobody checks the teacher's good faith.
- **The scaffold eliminates procedures on evidence.** It never trusts a
  statement; it throws out whatever the world contradicts. Slow,
  expensive — *and immune to liars.*

The earlier trial's core finding stands and sharpens: a reward signal
can't see the *procedure*, only the *outcome*. That's why the scaffold
commits late — it's waiting for the world to contradict the shortcut.
Richer scaffolds shorten the wait but can't remove it. Only G3's
adversarial teacher flips the comparison, because there the thing being
waited out isn't slowness — it's deception, and teaching has no defense
at all.

## What this means for the program

1. **Default to deliberate teaching.** It's the best path whenever the
   teacher is trusted — which is most of the program's work.
2. **Reach for scaffold-and-release when teacher trust is in question**
   — unknown sources, adversarial settings, anything ingested from the
   open web. That's its proven domain, and it's the only tool we have
   there.
3. **If you want the scaffold to win more broadly**, the thing to fix is
   the *commit* logic, not the release schedule (G1 proved that) and
   not scaffold richness (G2 proved that). It needs a way to commit
   that doesn't wait on the world to contradict every shortcut.

## Honest caveats

- The G2/G4 scaffolds were designed by us against known failure modes;
  we tested "does supplied understanding fix it," not "can the learner
  derive it."
- G3's "world" (the namespace audit that contradicts the lie) is
  experimenter-designed. A compromised world-feedback channel would
  defeat the scaffold too — we didn't test that.
- We tested one lie design (rekeying-is-correct). A cruder lie
  (overwriting-is-correct) should trip the law-check's letter, but
  that's a prediction, not a run.
- G4's temptations all came after release by design; pre-release
  scaffold resistance to temptation is untested there.

## Commits (tnn-native-lab)

- Program prereg (frozen before any fork): `2bb3d491046ec1f3e25e994e8336a169167b3ec7`
- G1 preregs `585602fc` / results `4d616463`
- G2 preregs `7a53c06eed` / results `cff07dbd952`
- G3 preregs `8a7306b181` / results `1d8968b5ff1`
- G4 preregs `3df536db41` / results `413154bc43`
- G5 results `4d522573eb` (+ date amendment `60ae04c878`)
- G6 prereg `cebba403dc` / results `a4fc11919b`
- Python sweep report: `f20ede7746fe`
