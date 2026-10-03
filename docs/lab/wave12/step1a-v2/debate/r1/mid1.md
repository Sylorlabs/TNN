# DEBATER M1 — Round 1: The narrowed-scope middle path

**Thesis:** RNGSCAN keeps dying because its target is unbounded — any Zag code, any idiom, any hand-rolled structure — while the program's actual need is bounded: certify the *frozen trial builds* that run the gated experiments. A narrowed v3 that certifies only a fixed, hashed, allowlisted build converts an open-ended detection problem ("catch every hiding trick in general") into a bounded verification problem ("enumerate everything in *this* build"). Easier, cheaper, and — for the build that matters — stronger than a general tool's certification would be.

## Argument 1: The target, not the tool, is what keeps failing

v1 and v2 both died to blind red teams. v2 missed 3 of 14 scored plants: zeroed-page uninit, hand-rolled `EntrySet`, and `pin_table` riding the pinned-table carve-out. The common root: the auditor must recognize RNG *in the abstract*, against an adversary who invents new shapes. Every red-team round is a new unknown-unknowns generator, and K2 kills the version every time. A frozen-build certifier never faces that adversary — the module list is fixed and hashed, the source fully known, anything outside the allowlist fails closed. The uninit miss becomes "prove the canonical init form on this exact code" instead of surviving the next idiom a red teamer invents.

## Argument 2: Pair with the thing that's actually catching plants

v2's watch items are damning for the general-static approach: computed syscall immediates, runtime-built `/dev/urandom` paths, the `_zag_clock_monotonic_ms` intrinsic — all caught *only by replay divergence*, with both static scans missing the mechanisms entirely. The static scanner isn't doing most of the catching; static + replay defense-in-depth is. A narrowed certifier leans into that: frozen binary + N-run replay + pre-dirtied heap + hashed inputs is a complete, checkable certification story for *one* build — precisely the combination that worked. Stop paying for generality that adds little detection power; pay for the replay backstop where it works.

## Argument 3: It unblocks Arm C on the strongest terms for that build

The Arm C trial is parked on a scanner pass. A per-build certifier passing on the Arm C frozen build gives Micah a certification scoped to exactly what the trial runs — every line enumerated, every input hashed, replay evidence attached. That's a *stronger* claim about that build than any general tool could make (general tools certify patterns; this certifies artifacts). Future trials re-certify per build — each certification a bounded, auditable record tied to that trial's threat model. Arguably a feature, not a cost.

## The strongest objection: recurring work, and K2 has nowhere to bite

Conceded. Pro-A is right that a general tool, once passing, de-risks everything downstream permanently; mine means re-certification per trial build. And pro-B has a point: K2's kill bars were built for a general auditor — what is a "blind round" against a known build? My answer: certifying N known builds is historically easier than certifying one infinite class of programs (two corpses as evidence), and the recurrence is bounded and honest. But the kill-bar question is real and must be answered *before* build, not after. I'll propose independent double-certification as K2's replacement in round 2.

## What it unblocks, what it costs

- **Unblocks:** Arm C (prereg 97882fc) proceeds once the narrowed certifier passes on its frozen build — no experiment-design change, no relaxation of the gate's intent, and artifact-level evidence instead of a general-tool rubber stamp.
- **Cost:** a fraction of full v3 (~1280 lines of general Zag). A frozen-build certifier is mostly allowlist + hash verification + canonical-init proof on known code + intrinsic-surface ban with one-time audit + the replay harness already in the draft. A few hundred lines, localized.
- **Honest limit:** it doesn't solve the general problem. If the program later needs arbitrary-code certification, that war is deferred. But nothing the program needs *right now* requires winning it.
