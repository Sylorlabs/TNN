# DEBATER M1 — Round 2: Rebuttal

## (1) The strongest point against me, answered

The honest attack isn't "recurring work" — it's deeper: *a frozen build still has to detect novel tricks*. If the certifier must catch an unknown hiding shape inside the Arm C build, "enumerate everything in this build" collapses to "enumerate everything we know how to recognize in this build" — the same open-endedness in a smaller hat.

My best answer: the narrowed certifier must be **prescriptive, not descriptive**. For a known build I don't *detect* hand-rolled containers — I *ban* them: trial builds use only allowlisted containers, canonical init forms, no unlisted intrinsics, or they don't compile for trial purposes. Detection generalizes to the infinite class; prescription works only when the target is fixed and the builder cooperates. That dissolves the side-door objection. The real price is on the lab: trial code must be written to the narrower idiom. I claimed cheap; honestly, part of the cost moves onto the trial-build authors.

## (2) The weakest point I can honestly attack: pro-A's "convergence"

Pro-A says each death names a finite, patchable class, and the attack surface is a "checklist, not a research frontier." The evidence contradicts boundedness: the watch items — computed syscall immediates, the runtime-built `/dev/urandom` path, `_zag_clock_monotonic_ms` — were missed by *both* static scans. Those mechanisms lived outside the enumerated classes, and the amendment's answer is mostly replay hardening, not static detection. And pro-A admits 6 of 20 plants went unscored: convergence claimed on an incomplete red team with an unknown miss count. "Fixing a class kills its whole family" only holds if the classes are known — the watch items are proof they aren't.

## (3) Concessions and adjustments

Two, honestly taken. First, M2 and pro-B won the empirical point: replay is the layer that catches things. My round-1 leaned on the certifier too heavily; adjusted: the narrowed certifier is **thin** — prescriptive allowlist + hash + canonical-form checks — with hardened replay doing the heavy verification. My narrowed v3 and M2's replay-first aren't competitors; they're the same gate, and I merge with that.

Second, my promised **K2 replacement for per-build scope**, prereg-frozen before certification: (K1′) the certifier's allowlist, banned idioms, and replay matrix are fixed for that build; (K2′) the certifier faces a *blind red team scoped to the build* — one miss the prescriptive rules should have forbidden = certifier version dead (a *novel*-class miss forces a prereg amendment with Micah's re-approval, not a quiet patch); (K3′) the hardened replay matrix passes on the exact frozen binary. Two independent implementations is the stronger variant of K2′ if Micah wants it.

## (4) One question for Micah

Would you accept trial code being constrained to a narrower, auditable idiom — whitelisted containers, canonical init forms, no novel idioms — trading freedom in how the lab writes code for bounded, artifact-level certification of exactly the binaries that run? The whole middle path stands or falls on whether the science side will pay that price.

— M1. One voice; the decision is Micah's.
