# Slice 23 — Composition of multiple state variables (Track 1)

## 1. Slice
Track 1 (state-dependent deterministic variation), slice 23: the composition algebra for
multiple expression-state variables that push in opposite directions.

## 2. Falsifiable claim
On a preregistered 200-case conflict suite, the lexicographic-with-abstention algebra
resolves every two-variable conflict so that: (a) when the higher-priority variable is
decisive it wins outright; (b) when it is neutral (all candidates within its indifference
band) it abstains and the lower-priority variable decides; (c) replay from logged state
reproduces the winner byte-identically in 200/200 cases; (d) no case alters a verdict,
memory decision, integrity refusal, or ledger entry versus the no-variation control.

## 3. Design
**Scope.** Composition operates ONLY in the lawful variation subspace (expression,
phrasing, ordering, elaboration). Verdicts, memory ops, refusals, ledger contents are
constitutional and never enter the algebra (per RC1, 40/40: TNN controls 100% of reasoning
machinery, 0% of the constitution; wave5/6: 137/137 integrity checks).

**Inputs (all prereg-enumerated, all logged).** Finite candidate set C = {c_0..c_{k-1}}
(expression plans; fixed order, fixed integer indices — integer selectors only, never
slice `==`). Hard gates G_1..G_m: g_j(c, state) in {pass, fail} (e.g. budget ceiling,
latency cap). Ordered advisory levers L_1..L_n (e.g. SALIENCE, BUDGET, REPETITION,
FAMILIARITY, CONFIDENCE), each with score function f_i(c, state) -> i32 and a prereg
indifference band d_i >= 0.

**Stage A — gates (eliminative).** S_0 = {c : all g_j pass}. Prereg guarantees S_0
nonempty (the minimal candidate always passes); a gate-empty event is a logged fault
falling back to fewest-failures-then-lowest-index.

**Stage B — lexicographic levers with abstention.** For i = 1..n:
S_i = { c in S_{i-1} : f_i(c) >= max_{c' in S_{i-1}} f_i(c') - d_i }.
Winner = lowest-index member of S_n (index order is the final deterministic tiebreak).

**Conflict-resolution rule.** A higher-priority lever L_i overrides a lower one L_j
(i<j) UNLESS L_i abstains. L_i abstains iff it eliminates nothing: all surviving
candidates score within d_i of its max (max - min <= d_i over S_{i-1}). A lever never
partially wins — it eliminates candidates or abstains entirely. No blending, no
compensation: a strong low-priority signal can never outweigh a decisive high-priority
one, and two lawful expressions are never averaged into a middle neither endorses.

**Why this over the alternatives.** Plain priority order lets a high lever force an
arbitrary win where its signal is noise (salience 501 vs 499 vetoing budget) — the
indifference band makes "this variable has nothing real to say" a lawful, logged state.
Weighted combination was rejected: weights are ungrounded constants trading off
qualitatively different authorities, blends hide which variable decided, and
compensatory mush is not an expression any lever endorsed. This mirrors TNN's
eliminative hypothesis logic (candidates die, never voted) and MA1's append-only audit
with replay to exact state.

**Logging for replay.** Every composition appends an audit block: state hash, candidate
list, per-gate pass/fail, per-lever per-candidate scores f_i(c), d_i, survivor sets
S_i, winner index, final expression parameters. Replay = pure rerun on logged state.

**Example trace (salience vs budget, C = {0:terse, 1:standard, 2:elaborated}).**
Case A, salience=820 (d=150): f = {0:100, 1:600, 2:1000}; max=1000 -> S={2} (600 < 850).
Winner = elaborated. Log: "L1 decisive; L2 not consulted." Budget loses lawfully.
Case B, salience=500 (d=150): f = {0:700, 1:750, 2:700}; max-min=50 <= 150 -> S={0,1,2},
L1 ABSTAINS (logged). L2 budget=90 (d=150): f = {0:1000, 1:600, 2:200}; max=1000 ->
S={0} (600 < 850). Winner = terse. The lower-priority variable wins lawfully because
the higher one abstained — a genuine conflict resolved to one lawful expression choice.

## 4. Kill bar
- **K1 replay:** <200/200 byte-identical winners on replay from logged state -> kill.
- **K2 leakage:** >=1 case where composition changes a verdict, memory op, refusal, or
  ledger entry vs the no-variation control -> kill immediately.
- **K3 degeneracy:** >=10% of cases decided by the final index tiebreak (all levers
  abstained) -> kill; the levers have no discriminative power.
- **K4 band abuse:** any lever's band spans >50% of its observed score range across the
  suite -> kill; the priority order is decorative.

## 5. Honesty notes
The bands d_i and the lever priority order are prereg human judgments, not derived —
the algebra moves arbitrariness up one level; it does not eliminate it. The candidate
enumeration fences variation: expression can only vary within prereg candidates, so the
"hardcoded vibes" Micah worries about are reduced, not gone. Levers are assumed
independent (no cross-terms); correlated levers would need a joint score this design
lacks. The abstention edge (score exactly at max - d_i) is a deterministic knife-edge —
logged and replayable, but fragile by construction. I am NOT claiming lexicographic
beats weighted in general (no-free-lunch: it must win a benchmark), and NOT claiming
expression variation is proven valuable — only that this composition is lawful.

## 6. Next build step
Implement `compose()` in Zag with audit-block logging, plus the prereg 200-case conflict
suite (adversarial two-lever conflicts, abstention-forcing neutrals, gate violations);
run at 1x and evaluate K1–K4 before any scale leg.
