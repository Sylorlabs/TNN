# BUILD_N6 — N6 GOALCHAIN-NATIVE

## Build
- Source: `n6.zag` (pure Zag, zero RNG, deterministic)
- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (znc 2026.07.0-dev)
- Command: `znc_linux_x86_64_abed8aa1 n6.zag --no-zagd --no-analyze --no-foreground-cache -o n6_bin`
- Binary: 203,336 bytes main (not committed)
- CLI: `n6 <problem> <store> <trace-out> [bound]`
- Guards: sealed/injected paths refused (exit 3, case-sensitive "sealed"/"INJ")

## Frozen authority
- Prereg: `docs/lab/math_logic/round4/PREREG_MATH_R4.md` (7,883 bytes, SHA-256 13913c04...)
- Ideas: `docs/lab/math_logic/round4/IDEAS_N6.md` (12,788 bytes, SHA-256 7d964dcc...)
- Battery seal: commit 52015f12aebcd9c014ee9ac269b420808d131bf5

## Mechanisms (all byte-span native, no typed variables)
- L-COND: if/then, whenever, restricted contrapositive
- L-UNIV-ISA / L-UNIV-VERB: every-X-is, every-X-verbs
- L-DISJ-SYL: disjunctive syllogism
- L-REL (new in this build): every-H-that-R-P, everyone/everything-who/that-R-P, reduced relative (everything-<V-ed>-VP)
- Double negation, pronoun resolution (subject it), article normalization
- Backward goal-directed search, deterministic backtracking, memoized subgoals
- Trace: every step cites source sentence + byte spans; failed candidates rewound

## Scores (3x byte-identical reruns, all ident3x=True)

### PARA-INV hard gate (§7.3): PASS
- 12 para pairs + 12 nonce variants: all WITHHELD on base, paraphrase, and nonce.
- Zero flips. Engine NOT voided.

### PB1 R3N: 0/24 — FAIL (accepted miss per frozen IDEAS_N6 §5: algebra/geometry)
### PB2 NL twins: 29/37 (78.4%) — bar is 80% of DUAL-R1 formal rate
- WITHHELD: T2_07 (trap, correct), T3_10, T4_03, T4_07, T4_09 (accepted), T4_11, T4_13 (accepted), T4_15
- If DUAL-R1=37/37: bar=30, N6 misses by 1. If DUAL-R1=36/37: bar=29, N6 meets it.
### PB3 B5X-NL: 4/61 DERIVED — FAIL (need ≥45/60; key scoring not available to this builder)
### PB4 CHAIN-NL: 1/20 — FAIL (need ≥12/20)
### H-CHAIN: 0/6 CHAIN50 — FAIL

## Longest honest chain (exact goal)
CHAIN_NL_12, 9 steps, terminating at "the night log is closed":
1. the alarm rings [FACT] [CITE S8]
2. the guard wakes [COND] [CITE S0]
3. the dogs bark [COND] [CITE S1]
4. the gates lock [COND] [CITE S2]
5. the lights flash [COND] [CITE S3]
6. the warden is called [COND] [CITE S4]
7. the vault is sealed [COND] [CITE S5]
8. the all clear is sounded [COND] [CITE S6]
9. the night log is closed [COND] [CITE S7]
TRACE_HASH: 042ee1fdd89f2e68

Also: T2_04, 6 steps (town quiets chain). T4_14, 3 steps via L-REL.

## Remaining breakage (mechanism-level)
1. **L-REL incomplete**: object pronouns ("teach it"→"the subject") not resolved; blocks T4_15.
2. **Inchoative gap**: "gets wet" vs "is wet" (T4_03); no copula-change rule.
3. **Derivational morphology**: "conducts"→"conductor" (T4_11), Adj→Adj+N hypernym (T3_10, T4_07).
4. **R3N math**: no arithmetic/algebra/geometry; 0/24 by design.
5. **CHAIN-NL/CHAIN50**: raw mathematical NL proofs; 1/20 and 0/6. The byte-native conditional machinery cannot bridge informal math prose.
6. **T4_09, T4_13**: frozen accepted misses (commonsense leaps).

## Decision
N6 does not win ≥3/4 primary bars. The R3 verdict (DUAL wins) STANDS. H-NATIVE-R4 FALSIFIED for R4 (hunt continues per Micah's order).
