# PREREG_CAUSAL.md: C9 Causal Contestant (Part A)

Wave: wave-20261002-0221pdt | Lane: ARENA | Date: 2026-10-02
Status: FROZEN (committed alone before implementation)

## Goal

Push the arena contestant toward 1.0 on capability C9 (causal reasoning),
which is currently at zero. The C9FIX world generator (Part B) now produces
valid causal worlds with interventions. This prereg freezes a candidate
mechanism that infers causal chain structure from interventional data.

## Base

The candidate is built on the v6 base contestant (source sha256
c6dbc20cf447dce7ab506576b42557a0542065e170bee6516558ecfb435d1e89).
The v6 base ignores causal turns (falls through to tick), so the new
mechanism adds a causal section without regressing the baseline.

## Mechanism (frozen)

The causal_contestant.zag adds a causal inference section to the v6 base:

1. Accumulate statistics from do/do_out turn pairs:
   - For each do(X,v): count turns, count y==v, count z==v
   - For each do(Z,v): count turns, count y==v, count x==v
2. Apply the two-stage interventional protocol (from C9BAT, validated in
   Part B G5):
   - Stage 1: If P(y==v | do(X,v)) >= 0.75 and P(y==v | do(Z,v)) >= 0.75,
     then Y is a leaf (effect). If both < 0.75, Y is a root (cause).
     Otherwise, compare: higher P(y==v) indicates the upstream variable.
   - Stage 2: Given Y's position, use P(z==v | do(X,v)) vs P(x==v | do(Z,v))
     to order X and Z.
   - All comparisons use integer arithmetic (cross-multiplication).
   - Threshold HI=0.75 (frozen).
3. On C9 discrim questions ("discrim|<c1>|<c2>"):
   - Infer the chain via the protocol above.
   - Reply with the full chain string that matches the inferred chain.
   - The reply must be one of the two listed candidates.
   - Do NOT use candidate position (order) as a cue; infer from data only.
4. Zero chain-string literals in the source (genericity).

## Kill Bars (frozen)

K1 (C9 capability): On the fixed-generator world (fixrun1), the candidate
scores 3/3 on C9 items (via sealed eval).

K2 (no regression): On the fixed-generator world, the candidate scores
>= the v6 baseline on all other capabilities (C1-C8, C10-C16). The v6
baseline is run on the same world for comparison.

K3 (determinism): 3/3 sealed runs produce byte-identical replies.

K4 (ablation): With the causal section disabled (stats not accumulated),
C9 score drops to 0/3, proving the mechanism (not the base) drives C9.

K5 (no order exploit): The candidate's C9 replies are identical when the
two candidates in each question are swapped. (The fixed battery has an
order bias due to the seed; the candidate must not exploit it.)

K6 (architecture): Zero new hardcoded semantic cases, modes, bridges, or
handlers. The causal section uses only generic accumulation and comparison.
Cognition lines added: counted and reported.

K7 (no L3 claim): This is L1/L2 mechanism work (parameter filling and
structural inference from a fixed protocol). No representational invention
is claimed.

## Sealed Eval Protocol (frozen)

1. Build causal_contestant.zag from this prereg (pure Zag, safebin).
2. Dev smoke test in /tmp (not the sealed world).
3. Run v6 baseline on fixrun1 world: record per-capability scores.
4. Run candidate on fixrun1 world, 3x: verify byte-identical, record scores.
5. Ablation: disable causal stats, run once, verify C9=0/3.
6. Order swap test: swap c1/c2 in the 3 questions, run once, verify replies
   unchanged (still the true chain).
7. Write SEALED_EVAL.md with VERDICT line.

## Scope

This prereg covers ONLY the C9 causal mechanism. C12 and C15 remain for
future waves. The fixed-generator world (Part B) is the eval substrate;
the ARENA2 negative finding (frozen C9 battery unpassable) is superseded
for the fixed generator only, not the original frozen battery.

## Notes

- The Part B validation found G4 order bias (true always first) due to the
  frozen seed. The K5 order-swap test ensures the candidate does not rely
  on this bias.
- The candidate never opens answer_key.json. It reads only the turn stream.
- FW1-FW9 is a regression battery, not generality evidence.
