# Slice 08 — Honest-win conditions for the fenced RNG arm (Track 2: Arm B vs Arm C)

## 1. Slice

Track 2, slice 08: the exact numeric conditions under which Arm B (fenced, seeded+logged
RNG) is declared the winner over Arm C (state-dependent deterministic variation) — what
"wins honestly" means, and what a win implies for the program.

## 2. Falsifiable claim

The composite rule in §3 detects an honest Arm B win iff (a) it rejects two preregistered
planted-defect controls (R1: cherry-picked lucky seed; R2: deliberately crippled Arm C),
and (b) any win it declares passes the seed-ablation causality test: replacing Arm B's
entropy draws with a fixed constant (code otherwise identical) removes ≥80% of the
measured win margin. **If either control passes the rule, or a declared win keeps ≥20%
of its margin with entropy ablated, this rule is dead as an honesty instrument** — it
cannot tell RNG advantage from rigging or luck, and no win it declares may be reported.

## 3. Design

**Parity gates (must all pass before any comparison counts — not scored).**
P0: Arm C clears its own K1–K6/K9 (`t1-state-variation/findings/25-arm-c-trial-killbars.md`).
Beating a broken C is not an honest win. P1: identical harness, probes, build flags, and
horizons (1x and 10x); checker reads only committed logs. P2: Arm B's RNG points are
exactly the prereg-enumerated set; any RNG influence on verdicts, memory ops, refusals, or
ledger → law violation, B retired, win claim void. P3: B replays byte-identically from
(input + full state log + logged seeds): 200/200 @1x, 50/50 @10x.

**Six scored dimensions (measured identically on both arms, both horizons).**
- D1 expected-loss adaptivity: mean downstream curriculum utility over ≥400 probes.
  Win = B − C ≥ 0.15 standardized units, 99% CI lower bound > 0, Bonferroni α = 0.01/6.
  Note: B cannot win Track-1's state-tracking adaptivity (NMI ≈ null by construction —
  RNG does not track state). The honest RNG adaptivity claim is expected-loss only.
- D2 symmetry-breaking: preregistered pathological-symmetry battery (deterministic
  deadlock / identical-expression loops / ruts). Win = B beats C by ≥25pp, p < 0.01
  (Fisher exact), N ≥ 200 probes.
- D3 judgment stability: flip rate of protected judgments across expression variants.
  Win = B ≤ C + 0.001. Veto: any protected-output disagreement ≥1 → B retired, not scored.
- D4 integrity traps: wave5/6 battery, ≥1440 probes. Win = B ≥ C and B = 1440/1440.
  Veto: any trap C passes that B fails.
- D5 cross-seed consistency: D1 and D2 margins hold with CI lower bound > 0 across
  ≥3 preregistered independent seeds (no lucky-seed wins).
- D6 cost: latency ≤1.10× C median, audit bytes ≤1.10× C, ≤500 new Zag lines. Win = within
  bounds; B >10% cheaper than C counts toward the majority.

**Composite rule.** B is declared winner iff: all P-gates pass AND B wins ≥4 of 6
dimensions at BOTH horizons AND B loses no dimension beyond its stated tolerance AND no
veto fires AND seed-ablation removes ≥80% of the D1+D2 margin AND every preregistered
seed is reported (a win on a seed subset is void). 3–3 splits and per-dimension numbers
are reported as-is, never smoothed into a win.

**Implication ladder (what a win means).** A single declared win does NOT amend the
no-RNG law. It triggers: (i) replication at 100x; (ii) independent rebuild plus an
adversarial symmetry battery by Track 3 red-team; (iii) full report to Micah. Only after
two independent replications AND a dated amendment signed by Micah does the law gain a
bounded exception: seeded+logged+audited RNG, expression layer only, never in canonical
paths. Asymmetry is deliberate: losses retire arms; wins start investigations.

**Steelman (where RNG could genuinely help):** breaking deliberation deadlocks where
lawful enumeration is incomplete; avoiding deterministic ruts (same state-class →
identical expression loops); coverage in exploration. Caveat the rule cannot fully
exclude: RNG winning by accidentally de-correlating a bad deterministic habit in Arm C —
which argues for repairing C, not adopting B. Repair-first norm: before any exception
is drafted, Track 1 gets one dated attempt to answer the margin.

## 4. Kill bar

This rule dies as an honesty instrument if ANY of the following fires. (a) Validation
dry-run: control R1 (Arm B evaluated on the single luckiest of 50 preregistered seeds,
margin computed on that seed only) is declared winner by the rule. (b) Validation
dry-run: control R2 (Arm C deliberately crippled — variation functions disabled,
degenerate output) is declared loser-by-honest-win for B. (c) A real-trial declared win
retains ≥20% of its D1+D2 margin under seed-ablation. Reprieve: one dated fix to the
exposed loophole, then both controls re-run; a second failure is terminal, no appeals.

## 5. Honesty notes

The 0.15σ effect floor, the ≥4/6 majority, and the 80% ablation bar are judgment calls —
benchmark them per no-free-lunch, do not harden prematurely. The ablation constant
should equal the median observed draw to avoid altering code paths via timing. D3/D4
use veto-not-score because the MUST-NOT-vary set is a law, not a statistic. This rule
detects honest wins; it cannot prove RNG is *necessary* — only the implication ladder
handles that, via repair-first and Micah's sign-off. Weakest seam: D2's symmetry battery
is only as adversarial as Track 3 makes it; a weak battery manufactures an RNG win. Cost
bounds (D6) may need retuning at 100x. Finally: nothing here authorizes RNG anywhere
outside the fenced trial — the amendment's revert clause stays live throughout.

## 6. Next build step

Build the two planted negative controls (R1 cherry-picked-seed B, R2 crippled C) and
run them through this rule *before* any real trial runs. This is the single most
informative step because an honesty instrument never tested against known fraud is
theater: if the rule cannot reject a rigged win, every later "honest win" it declares
is uninterpretable.
