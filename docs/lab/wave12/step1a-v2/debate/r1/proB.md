# DEBATER B — Round 1: Accept Stated Residual Risk (Option B)

## Thesis

Two auditor versions have died to *new* tricks each time, while the actual science — the Arm C state-variation trial — sits parked behind a certification tool that may never converge. The empirical record shows replay divergence does the real catching; the v3 fixes are real but chase the *next* hiding spot, not the last one. We should stop the audit line here, write down exactly what is and isn't certified — dated, reviewed, honestly bounded — and unblock Arm C with compensating controls. A stated risk is a governed risk; an infinite audit line is a program that never answers its own question.

## Argument 1: The hiding-spot space looks inexhaustible; each round costs the science

v1 died to blind-red-team plants. v2 died to three *different* misses — uninit hidden by a zeroing allocator, a hand-rolled `EntrySet` invisible to token-based scanning, `pin_table` riding a carve-out. Nothing in the v2 failure suggests the *next* version exhausts the space; it suggests adversaries keep inventing spots faster than we patch them. v3's fixes are concrete (~1280 lines, localized), but they harden against the tricks we just saw, not the ones the next blind team dreams up. Every round is real weeks while Arm C — the experiment testing whether identical inputs produce state-caused expression variation, the question that actually matters — waits. A certification gate that never converges is a program choosing tooling over answers.

## Argument 2: Replay divergence does the real work already — certify the thing that catches

The decisive empirical fact: several plants (computed syscall immediates, the runtime-built `/dev/urandom` path, the `_zag_clock_monotonic_ms` intrinsic) were caught **only by replay divergence** — both static scans missed the mechanisms entirely. The static auditor is not doing most of the catching; defense-in-depth is. So Option B re-weights the certification honestly: put the certification weight on **hardened replay** (N runs, heap pre-dirtying, byte-identical requirements), which exists and demonstrably works, and treat the static scan as a best-effort tripwire with a published miss rate. This is not weakening enforcement — it is accrediting the layer that empirically enforces.

## Argument 3: A perfect static auditor is its own research project — and honesty requires disclosure, not perfection

The no-RNG law is a law about the AI; the auditor is a tool. The program's honesty norms demand we *state* uncertainty, not eliminate it: a written, dated residual-risk statement ("the static scan certifies X; replay certifies Y; the following classes remain uncertified...") reviewed and version-controlled is more honest than a tool that silently misses. Freezing Arm C behind an unproven gate also corrupts the honesty norm — a parked experiment produces no evidence at all, which is worse than evidence with stated bounds. Compensating controls deliver most of the assurance at a fraction of the cost: frozen trial builds, per-trial-build red-teaming scoped to that build (not a general-purpose scanner), hardened replay as the primary certification, and the published residual-risk statement.

## Honest concession

The strongest argument against me: the no-RNG law is load-bearing, and an Arm C variation claim made under residual risk is **permanently attackable** as "maybe hidden RNG" — the exact confound the gate exists to prevent. If variation in Arm C later traces to an uncertified channel, the result is not just wrong, it's wrong in a way the program's founding law forbids.

My answer: that risk is real, but the v3 path doesn't eliminate it either — it shrinks the *known* hiding spots while the unknown ones persist, and each iteration gives false finality ("we passed the red team this time"). Option B is honest about the residual; a v3 pass risks being mistaken for proof. And note the asymmetry: a scanner pass does not certify the AI — the AI's determinism is ultimately established by replay divergence on frozen builds, which Option B makes the primary mechanism. The residual-risk statement should name this attack explicitly ("Arm C's variation attribution rests on replay-hardened builds, not on static certification") so critics attack the real control, not a strawman.

## What Option B concretely unblocks, and its cost

**Unblocks:** the Arm C trial (prereg frozen at 97882fc) immediately — deterministic state-dependent phrasing vs fenced-RNG Arm B vs fixed control, the first real test of whether state causes expression variation. Every week parked is a week the program's main line stalls.

**Cost:** we give up mechanical static certification of the no-RNG law and replace it with (a) a published, version-controlled residual-risk statement with a stated miss-rate history (2/2 versions killed — this is not hidden), (b) hardened replay as primary certification on frozen builds, (c) per-build red-teaming instead of a general-purpose auditor, and (d) Micah's sign-off on the risk statement, revocable at any time. If a miss later traces to an uncertified channel, the statement makes the failure bounded, attributable, and fixable — not a scandal.
