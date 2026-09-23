# DEBATER M2 - Round 2 rebuttal

## (1) The strongest point against me, answered honestly

Pro-A's "permanent asterisk" lands: without a passing mechanical auditor behind replay-first certification, every Arm C result stays attackable as "maybe hidden RNG" - the exact confound the gate exists to prevent. My answer: this is a price, not a refutation. First, a v3 pass risks false finality - "we survived the red team" reads as proof more readily than a dated, bounded replay certification with a published miss-rate history, which pro-B rightly demands and I now adopt. Second, on a frozen build only replay certifies behavior; a scanner certifies source text. Third, the asterisk only poisons hidden controls: a preregistered N-run matrix with named deployment-like conditions, published with the results, lets critics attack the real control instead of a strawman. I accept that burden shift by design: the replay evidence must be met in the open.

## (2) The weakest point I can honestly attack

Pro-A's "the attack surface is bounded" is the debate's weakest honest claim - and it contradicts the evidence pro-A otherwise respects. Two blind rounds, both killed by new tricks, and the v2 round stopped at 14 of 20 scored - so pro-A declares a finite checklist without knowing the full miss count. "Converging" does heavy lifting for two deaths; convergence needs a pass, not two named autopsies. And "each fix kills a whole class" assumes the hider's classes are drawn from the mapped space - but inventing shapes outside it is the adversary's whole job. A hand-rolled EntrySet is exactly that: a class nobody had listed until it killed a version. A bounded surface is a hypothesis, not a finding, and the record supports the opposite one.

## (3) Concessions and adjustments

Two, both genuine. First, from pro-B: I adopt the dated, version-controlled statement of what the replay gate certifies and does not - miss-rate history (2/2 versions killed, stated plainly) and the named residual (environment-dependent nondeterminism deterministic under lab conditions). If replay is the gate, its limits get written down, not implied. Second, from M1: my replay-first gate should be scoped to the frozen trial build - hash the artifact, preregister the N-run matrix per build - not framed as general certification. M1's per-build scoping strengthens my position for Arm C: artifact-level replay evidence is what variation-attribution needs, and I accept per-build re-certification as bounded recurring work. I keep the v2 static scan as the tripwire; on frozen builds its cheap mechanical catches come nearly free.

## (4) One question for Micah

If we run Arm C under hardened replay certification on a frozen, hashed build - N-run matrix, deployment-like conditions, and the dated residual-risk statement all published - would you accept variation results that pass that gate, knowing no mechanical static proof backs them? Or does the no-RNG law require a scanner pass before any variation claim counts?

- M2.
