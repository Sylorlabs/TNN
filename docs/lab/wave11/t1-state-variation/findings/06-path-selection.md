# Slice 06 — Path-to-conclusion selection (Track 1: state-dependent deterministic variation)

## 1. Slice
Design how TNN's internal state deterministically selects among multiple *valid* reasoning paths
that all terminate at the *same* conclusion — variation in path/expression, never in verdict.

## 2. Falsifiable claim
For any deliberation episode with hypothesis set H (|H| ≤ 6, the enumerability bound in §3):
(a) every path in the canonical valid-path inventory terminates at the identical verdict
(0 divergences across the suite in §4); (b) the selection function is a pure function of the
logged state projection, so replay of input + full logged state selects the identical path
byte-identically; (c) no selectable path can reach a different verdict, memory decision,
integrity refusal, or ledger content. If any clause fails on the trial suite, the design dies.

## 3. Design
**3.1 Path inventory.** Given evidence E and hypothesis set H, an elimination *step* is a pure
function `eliminate(h, E, live_set) -> KEEP|REFUTE` with refutation evidence pinned per h
(eliminative hypothesis logic, docs/lab/wave5). A *path* is a total order of attempting
elimination over H restricted to orders respecting the dependency DAG D (h depends on h'
being decided first only when h's refutation test consumes h''s status). The inventory is the
canonical enumeration of all valid linear extensions of D, sorted lexicographically by
hypothesis id — state-independent, enumerable offline, identical at every build. |H| ≤ 6 keeps
|inventory| ≤ 720; episodes with larger H fall back to §3.4 directly (documented, not varied).
**3.2 Selection function.** Let S be the state projection: (audit clock, deliberative-standards
priority weights, per-hypothesis evidence-recency ranks from the memory store). Selection is
`sel(S) = rank_keys(S) mod |inventory|`, where `rank_keys` is a fixed pure function
(compositional keyed digest of S with the build-constant key K0 — deterministic, no RNG,
replayable from logged S). Same full state → same index → same path, byte-identical.
**3.3 Verdict invariant.** The verdict is a function V of the final live/refuted partition,
not of the order. Proof sketch: elimination steps are *confluent* — `eliminate` depends only
on (E, h, current live_set), and refutation of h can never depend on the *order* of prior
eliminations, only on whether each dependency in D is decided (guaranteed by the DAG
restriction) and on E (fixed per episode). Any two valid linear extensions therefore produce
the same refuted set by induction on position: the first index where orders differ decides two
independent hypotheses whose eliminations do not interact. Hence all paths terminate at the
same partition and V is identical. Bounded check: exhaust all pairs of inventory paths on the
trial suite and compare verdict + partition hashes; 0 mismatches required.
**3.4 Non-termination fallback.** Each selected path runs under a deterministic step budget
B = 4·|H|² elimination attempts. If the budget exhausts without a complete partition (a path
*fails to terminate*), the episode falls back to inventory index 0 — the canonical
lexicographically-first valid path — with a ledger entry `PATH_FALLBACK(ep, idx, reason)`.
The fallback itself has budget B; exhaustive inventory pre-check guarantees index 0
terminates (it's a valid linear extension by construction), so fallback cannot recurse.
**3.5 What varies.** Path choice changes the presented trace: which hypothesis dies first,
which evidence is cited first, ordering of intermediate claims. That's the MAY-vary surface
(phrasing, ordering, elaboration). MUST-NOT-vary (verdict, kill/pin/promote, integrity
refusals, ledger contents — ledger records the fallback fact, not a different outcome) is
untouched by construction since V and all deliberate ops consume only the final partition.

## 4. Kill bar
Preregistered, all on a fixed 300-episode suite (100 each: small |H|=2–3, medium 4–5, max 6):
**K1:** any ≥1 verdict divergence between any two valid inventory paths on the same episode
→ idea dead. **K2:** any replay (input + logged state) selecting a different path or emitting
non-byte-identical output → dead. **K3:** any selected path exhausting budget B without the
fallback engaging and terminating deterministically → dead. **K4:** any dependence of V,
memory ops, or refusals on path index observed in the audit diff → dead. Kill on first fire.

## 5. Honesty notes
Weakest point: the confluence argument assumes `eliminate` has no hidden order dependence —
if a future evidence-check reads "order so far" as a heuristic, invariance breaks silently;
the bounded check is the guard, not the proof. The |H| ≤ 6 bound is a real limitation:
large-H deliberation can't use this inventory (falls back silently to index 0, which is honest
but not variation). Selection `mod |inventory|` clusters when inventory sizes are small
(|inventory|=1 episodes show zero variation — expected, but report the fraction). I am NOT
claiming path variation is *useful* (does varied ordering improve learning or trust?) — only
that it is safe and genuinely state-dependent. A lying path cannot survive: the verdict gate
post-checks V against the independently computed partition before any downstream op.

## 6. Next build step
Build the bounded-check harness in Zag before any selection UI: enumerate the inventory for
300 fixed episodes, run every path, diff verdict + partition hashes + replay byte-identity.
One binary, `argv[1]` selects suite thirds (s1/s2/s3 per driver pattern). If K1–K4 hold, wire
`sel(S)` in; if any fires, the slice is dead and the report names the violating episode.
