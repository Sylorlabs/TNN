# Round 2 Rebuttal — DEBATER A (pro v3)

## (1) The strongest point against me, and my honest answer

**The plants that mattered were caught only by replay divergence; static analysis never carried the catching** — sharpest in M2, echoed by all three. Conceded as fact: the watch items passed both static scans clean.

My answer: it isn't either/or. The v3 draft *contains* the replay-hardening section — a standalone deliverable of days that should be built and accredited first. The debate is only whether we *also* rebuild the static layer. The layers answer different questions: replay catches whatever diverges under lab conditions; static catches *mechanism classes* — init-form failures, structural table-blindness — certifying every build cheaply, including trick families no red teamer has invented yet. Behavioral evidence is not a substitute for mechanical proof; defense-in-depth is the honest answer to the ledger, not a denial of it.

## (2) The weakest point I can honestly attack

**M2's environment-gating hole — to which B's own inexhaustibility argument applies.** M2 concedes a plant could be deterministic across lab replays yet nondeterministic in deployment. His answer is a preregistered matrix covering "deployment-like conditions." But *enumerating all deployment-relevant environments is the same infinite space M2 and B claim dooms static scanning.* If "the adversary invents new hiding spots faster than we patch them" kills v3, then "deployment environments vary faster than we preregister conditions" kills replay-first by identical logic. The critique is symmetric — and static scanning at least has a finite, named surface (Zag + znc + syscalls + intrinsics) while "deployment-like conditions" has no boundary at all.

Relatedly, M1's certifier has no kill bar — M1 concedes K2 has nowhere to bite against a known build. A certifier that cannot be killed by construction is a rubber stamp with extra steps.

## (3) Concessions and adjustments I accept

Three. **(a) From B:** a v3 pass risks false finality. Even a passed v3 must be published inside a dated, version-controlled residual-risk statement — B's disclosure instrument, adopted for the static layer regardless. A pass is evidence, not proof. **(b) From M2:** replay hardening is the cheapest, fastest real assurance; it should ship as a standalone deliverable without waiting for the static rebuild. **(c) From M1:** per-build certification is a legitimate *complement*, not a rival — the Arm C frozen build should get artifact-level certification (allowlist + hash + replay evidence) in parallel, while the general enforcer is rebuilt for everything downstream.

## (4) One question for Micah

**Do you want a mechanical static enforcer to exist at all as part of the program's integrity story — independent of Arm C's schedule — or is your priority unblocking Arm C at minimum cost, with the no-RNG law certified by replay and disclosure alone?** This separates the debate's two blurred questions: unblocking the trial (replay hardening + per-build certification does that fastest) versus whether a standing law deserves a standing mechanical enforcer (only a general v3 does that). My position is yes to the enforcer — but the schedule should reflect your answer.
