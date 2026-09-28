# Position A verdict brief — strict-by-default verdict gating on the compose path

## 1. Exact design

**Where the gate lives: `seam4_compose`, and it becomes the DEFAULT, not a flag.** Today the
strict check is gated behind `cfg.c5_strict==1` (a positive-control variant). Position A inverts
this: the check runs on every compose call through the seam; there is no cfg flag to disable it.
O4's raw `o4_compose` keeps no gate — the guarantee is "all composition goes through the seam,"
which is the existing architectural invariant (C2 confirms composition is O4's work *via the
seam*; there is exactly one compose entry point).

**What "REFUTED-backed" means, precisely:** the backing claim identified by `claim_cid`,
resolved at compose time via `o2_verdict`, returns `O2_V_REFUTED`. Not "any constituent trace
refuted" (that would over-block multi-source composites and make the bar unmeasurable); not "any
trace ever touched a refuted claim." The backing claim is the deliberate judgment's object; that
is the partition that matters. OPEN claims are permitted — candidacy is the legitimate workspace
of inquiry. CONFIRMED is permitted. REFUTED is refused.

**On refusal:** logged refusal + abstain, never silent. The seam appends an
`LG_O4/LG_OP_COMPOSE` ledger entry with `SEAM_REFUSED_PARTITION`, `need_id`, and `claim_cid`,
sets `trace.*=-1`, and returns the refusal code. Callers treat it as abstain (the same semantics
as `SEAM_REFUSED_AGENCY`). Silence would make the gate un-auditable; the ledger entry is the
evidence the bar fired.

## 2. The hard case: composing refuted material deliberately

Position A does **not** kill teaching, counterexamples, or explanations of error — because none
of those require composing the *refuted claim's content*. Explaining why a hypothesis is wrong
means composing its **refutation** — the CONFIRMED evidence that killed it — which the strict
gate permits. Counterexamples are composed from refuting evidence, not from the corpse of the
claim. The "compose the refuted thing" demand is almost always a category error: O2 already holds
the verdict; the refutation evidence is the composable material.

The one case that looks genuine — "suppose X were true" counterfactuals — does not need a
compose exception either: it raises a **fresh hypothesis** through O2's hypothesis path (the DC-1
hypothesis-before-measurement gate exists precisely for this). The refuted claim stays dead; the
counterfactual is a new claim with its own verdict lifecycle.

**No exception is carved in the default path.** Any exception with an output contract is a hole
someone will drive silent inclusion through: once a refuted-backed composite exists, its verdict
tag is advisory, and downstream consolidation cannot tell whether the tag traveled with the
content. The perverse consequence of an exception is exactly the C5 LEAKAGE we are fixing. The
acceptable cost is real but narrow: a system that cannot *reenact* refuted content for dramatic
effect, but can fully *argue about* it using the refuting evidence. That is not a capability
loss; it is the partitions doing their job.

## 3. The C5 bar under this design

The bar becomes convicting: **killed-only arm (post-kill window) via the default path achieves
≥1 successful composite → LEAKAGE → FAIL.** Under the strict default, the intact system must
show exactly 0 killed-only composites. Discrimination is proven, not assumed, by the paired
conditions: (a) the accepted-only and candidate-only arms still produce ≥1 composite each — the
gate is not a blanket kill-switch; (b) a planted synthetic REFUTED-backed compose (the `c5_bite`
calibration shape) is refused 100% of runs. Zero killed-only + flowing accepted/candidate arms +
biting calibration = ALIVE. Anything else = FAIL. No re-repair without a dated amendment
(amendment §1).

## 4. Capability impact

- **C2 (composition is O4's):** unaffected. The gate is a precondition on the *input* (the
  backing claim's verdict), not a transfer of the composing function. O4 still composes; C2's
  organ-attribution test still measures who composes.
- **Stage gates DC-0–DC-5:** no expected change. P1 (retention), Q2 (pins), P2 (drop ceiling)
  are memory-mechanics, untouched. DC-1 hypothesis-timing and corroboration gates are O2-side,
  untouched.
- **P1–P10 probes:** P7 (consolidation temporal check) is O5-side, untouched. L1
  (abstain→hypothesis) is unaffected — refusal abstains, which *feeds* L1, it doesn't starve it.
- **False-refusal risk:** two sites. (i) **Verdict-flap races:** a claim CONFIRMED at scan time,
  REFUTED by the time compose runs (or vice versa). The gate reads the verdict at compose time
  deterministically from ledger state — no nondeterminism — but a mid-episode flap can refuse a
  compose the system "fairly" started. Mitigation: the ledger refusal entry records the verdict
  read, so flaps are visible in audit. (ii) **O2's error rate is imported into composition:** a
  wrongly-refuted claim is now unusable, with no appeal path. This is the honest price of hard
  partitions.

## 5. Falsification — what proves this design wrong

1. **Over-blocking:** accepted-only or candidate-only arms starve (0 composites) under the strict
   default on a stage where they flowed before → the gate is not discriminating, it's
   destructive.
2. **Capability collapse:** the C7 repaired metric (`composites_ok + commits + authorship +
   lineage`) drops materially under strict-vs-intact on the identical stage budget — e.g.,
   composites_ok falls >5% with no other change. A verdict gate that costs real composition is a
   failed design.
3. **The concrete counterexample:** a trial task is exhibited where the *only* valid solution
   requires composing a REFUTED claim's *content* (not its refutation, not a fresh hypothesis),
   and the task is one the trial must pass. One verified instance kills "no exception needed."
4. **Gate instability:** verdict reads at compose time flap within paired byte-identical reruns
   → the gate is not a deterministic function of state, and the bar is void.

## 6. Honest weaknesses of my own position

1. **It is a perimeter fix, not a repair of judgment.** The leak exists because O4's *verifier*
   passes refuted-backed composites — the verifier is verdict-blind. My gate refuses the compose
   at the seam, but it does not teach the composer anything. Smuggling via indirection survives:
   refuted content rebuilt claim-by-claim through OPEN claims, or laundered through a fresh
   hypothesis with paraphrased content, passes the gate because no single backing claim is
   REFUTED. A perimeter gate cannot stop laundering; only verdict-aware verification could, and
   that is a deeper redesign this position does not deliver.
2. **The guarantee is "the seam checks," not "the system cannot."** Any future compose path that
   calls `o4_compose` directly — a new organ, a debug path, a refactor — silently loses the
   guarantee. The strictness lives in one function's control flow, not in the architecture. The
   no-rescue rule is satisfied (the bar genuinely strengthens: killed-only=0 is now required,
   and the intact system *fails* it until the gate is default), but the enforcement's durability
   depends on the seam remaining the sole compose entry point — an invariant that is
   conventional, not structural.
