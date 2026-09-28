# R34 native continual learner v1

This lane advances TNN beyond persistence-only scaffolding with a real, small, pure-Zag online learner.

The learner owns four integer action values, deterministic native RNG state, an update counter, and pending causal credit. Experience changes the action values online. Task B is initially failed, becomes mastered through experience, and Task A remains retained after Task B learning. Complete mutable learner state is serialized with SHA-256 integrity and can be reconstructed by a fresh native process.

The design is intentionally small and falsifiable. It is an engineering prototype for the experience -> parameter update -> changed action -> retained competence -> exact restart path. It is not wired to the R33 `learn` admission gate, does not mutate canonical R27, and is not a scientific TNN result.

Run `run_native.zsh` to produce a frozen evidence directory using `/Users/Shared/micah/Documents/zag/znc`.

