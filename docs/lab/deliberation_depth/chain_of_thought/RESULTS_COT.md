# H5 Chain-of-Thought Results — Trace Quality vs Depth

Date: 2026-09-24. Prereg: `PREREG_COT.md` (frozen, committed 149a7d3e BEFORE
measurement). All numbers from `measure_cot.py` (deterministic, no RNG) over
frozen artifacts; A/B arms pooled (byte-identical on all 12 hard-battery runs;
logic sweep A/B from the frozen H5 sweep).

## 1. Per-depth metric table

Metrics (PREREG_COT.md §2): **Q1_PRF** = productive-round fraction;
**Q1_cnt** = productive-round count; **Q2_PL** = premise leverage (fraction of
consumed evidence in a productive round); **Q3_CE** = correct eliminations per
item (non-GT contenders killed, only on correctly-decided items);
**Q4_PSIR** = post-settlement idle rounds (rounds after the leader became
provably unflippable given remaining evidence); **never%** = share of items
whose verdict was never unflippable.

### Logic battery (264 items, verdict-anchored weights)

| depth | acc | rounds | Q1_PRF | Q1_cnt | Q2_PL | Q3_CE | Q4_PSIR | never% |
|---|---|---|---|---|---|---|---|---|
| d1 | 1.000 | 1.00 | 1.000 | 1.00 | 1.000 | 0.00 | 0.00 | 0.000 |
| d2 | 1.000 | 2.00 | 0.578 | 1.16 | 1.000 | 0.31 | 1.00 | 0.000 |
| d4 | 1.000 | 2.06 | 0.578 | 1.22 | 1.000 | 0.31 | 1.06 | 0.000 |
| d8 | 1.000 | 2.11 | 0.578 | 1.26 | 1.000 | 0.31 | 1.11 | 0.000 |
| deep16 | 1.000 | 2.12 | 0.578 | 1.27 | 1.000 | 0.31 | 1.12 | 0.000 |
| adaptive | 1.000 | 2.07 | 0.578 | 1.23 | 1.000 | 0.31 | 1.07 | 0.000 |

Broken down by evidence count (deep16, arm A):

| ne | n | Q3_CE | Q1_cnt | rounds | Q4_PSIR | reading |
|---|---|---|---|---|---|---|
| 1 | 223 | 0.00 | 1.00 | 2.00 | 1.00 | d1 trace maximal; round 2 pure idle |
| 2 | 28 | 2.00 | 2.00 | 2.00 | 1.00 | round 2 kills both contenders (d1 truncates this) |
| 3 | 10 | 2.00 | 3.00 | 3.00 | 2.00 | eliminations at round 2, margin-padding after |
| 9 | 3 | 2.00 | 9.00 | 9.00 | 8.00 | 2 kills + 7 margin-padding rounds |

**never% = 0.000 at every depth including d1**: on all 264 logic items the
round-1 leader was already provably unflippable — remaining evidence could
only support the leader. Depth never changes what is decided on this battery.

### Harder battery `logic_hard` (48 items: 16 CE + 16 FP + 16 DA)

| depth | acc | rounds | Q1_PRF | Q1_cnt | Q2_PL | Q3_CE | Q4_PSIR | never% |
|---|---|---|---|---|---|---|---|---|
| d1 | 0.333 | 1.00 | 1.000 | 1.00 | 1.000 | 0.00 | 0.00 | 0.667 |
| d2 | 0.500 | 2.00 | 1.000 | 2.00 | 1.000 | 0.17 | 0.33 | 0.500 |
| d4 | 1.000 | 4.00 | 1.000 | 4.00 | 1.000 | 2.00 | 1.83 | 0.000 |
| d8 | 1.000 | 4.98 | 1.000 | 4.98 | 1.000 | 2.67 | 2.81 | 0.000 |
| deep16 | 1.000 | 4.98 | 1.000 | 4.98 | 1.000 | 2.67 | 2.81 | 0.000 |
| adaptive | 1.000 | 4.98 | 1.000 | 4.98 | 1.000 | 2.67 | 2.81 | 0.000 |

Family breakdown (arm A; acc / Q3_CE / Q1_cnt):

| depth | CE acc | CE Q3 | CE Q1c | FP acc | FP Q3 | FP Q1c | DA acc | DA Q3 | DA Q1c |
|---|---|---|---|---|---|---|---|---|---|
| d1 | 0.00 | 0.0 | 1.0 | 0.00 | 0.0 | 1.0 | 1.00 | 0.0 | 1.0 |
| d2 | 0.00 | 0.0 | 2.0 | 0.50 | 0.5 | 2.0 | 1.00 | 0.0 | 2.0 |
| d4 | 1.00 | 4.0 | 4.0 | 1.00 | 2.0 | 4.0 | 1.00 | 0.0 | 4.0 |
| d8 | 1.00 | 4.0 | 4.0 | 1.00 | 2.0 | 4.5 | 1.00 | 2.0 | 6.4 |

- **CE (chain-elimination)**: needs the full 3-hop kill chain; 0/16 at d1/d2,
  16/16 at d4 with 4.0 correct eliminations per item.
- **FP (misleading prefix)**: L=1 items flip at d2 (8/16), L=2 items at d4
  (16/16). Depth overturns the wrong early leader.
- **DA (distractor accumulation)**: accuracy 1.000 at ALL depths — the leader
  is right from round 1 — but Q3 = 0 until d8: d1 was **right but unjustified**,
  both contenders still alive. Depth 5–6 performs the 2 eliminations that
  complete the chain.
- never% falls 0.667 → 0.000: depth moves items from flippable-and-wrong to
  unflippable-and-right. d8 = deep16 = adaptive exactly (natural termination;
  the cap never binds; adaptive's §6 never fires early here).

## 2. Decision-rule outcomes (frozen PREREG_COT.md §§4–6)

**Hard battery — H-BETTER-REASONING CONFIRMED.** Required: accuracy d1<d4 on
CE and FP (0.00→1.00 both ✓), Q3 d8>d1 on CE and DA (0→4.0, 0→2.0 ✓),
productive-count rising with depth (1.00→4.98 ✓). All strict.

**Logic battery — H-MORE-ROUNDS confirmed in refined form, falsified in strong
form.** The frozen strong form required Q3=0 at every depth and flat
productive-count; both fail (Q3=0.31, count 1.00→1.27). The ne-breakdown
explains why: for the 223 single-premise items (84.5%) the strong form holds
exactly — d1's trace is maximal, round 2 is pure idle. The 41 multi-premise
items carry a 2-elimination tail that d1 truncates: depth buys
**justification** (killing contenders left alive) but never **correction**
(the verdict was unflippable from round 1 on all 264 items at every depth).

## 3. Headline

**Depth buys better reasoning if and only if there is a chain to complete.**
Three regimes, measured:

1. **No chain (logic ne=1, 84.5% of the logic battery): depth buys only
   rounds.** d1's trace is already maximal-quality: 1 productive round,
   verdict unflippable, everything after is idle re-confirmation
   (Q1 1.000→0.578, Q4 idle tail 0→1.12).
2. **Justification chain (logic ne≥2, hard DA): depth buys longer *correct*
   chains without changing the verdict.** d1 is right but leaves contenders
   alive; deeper runs perform the eliminations (logic Q3 0→2.0 on ne≥2;
   DA Q3 0→2.0 at d8 while accuracy stays 1.000).
3. **Decision chain (hard CE/FP): depth buys the verdict itself.**
   Accuracy 0.333→1.000, correct eliminations 0→2.67, productive rounds
   1.00→4.98 — monotone in depth, saturating at d8. The verdict is not
   recoverable from any single evidence item or early prefix; only the
   completed chain decides correctly.

In Micah's terms: deeper deliberation produces longer correct chains exactly
where the item *has* a chain — multi-hop elimination (CE: 3-hop kill chain),
overturning a misleading prefix (FP), sub-threshold accumulation to an
elimination (DA). Where the item is a single verdict-anchored premise, depth
adds confidence theater: more rounds, same reasoning. The logic battery's flat
1.000 was never evidence about depth and reasoning — it was evidence that 84%
of its items contain no chain at all.

## 4. Metric notes and limitations

- **Q2 (premise leverage) saturates at 1.000 everywhere** — it cannot separate
  chain-links from margin-padding, because any verdict-anchored evidence grows
  the margin and counts as "productive". An exploratory post-hoc strict variant
  (decisive = round changed the leader or killed a contender): hard deep16
  CE 0.750 / FP 0.597 / DA 0.252; logic deep16 0.655. I.e., on DA only ~1 in 4
  consumed premises is a chain link; the rest is padding. Not preregistered —
  reported as exploratory.
- **Q4's "idle" label overstates waste on justification chains**: on logic ne=2
  items the round-2 eliminations are genuine work (Q3=2) even though the verdict
  was already unflippable (Q4=1). "Post-settlement" ≠ "useless" — settlement
  of the *verdict* precedes completion of the *justification*.
- F1 (prereg §1) held throughout: every deeper trace is a strict prefix
  extension of the natural trace — "eliminate earlier" is impossible by
  construction; depth can only add tail. Whether the tail is chain or theater
  is what Q1–Q4 measure.

## 5. Method appendix

- Battery generator: `chain_of_thought/gen_logic_hard.py` (deterministic, no
  RNG; variation by index arithmetic). One encoding fix pass per prereg: the
  FP L=2 misleading prefix (700+600=1300) crossed the 900 elimination
  threshold and killed the GT contender before the overturn arrived — 8/48
  deep16 mismatches; root-caused in the ledger, fixed to 400+400 (still a wrong
  leader at d1/d2, GT stays alive), re-verified 48/48 at deep16 before the
  sweep. Within the prereg's kill criteria (≤2 mismatches after one fix pass
  would have stopped the line — 0 remained).
- Harness: `delib_harness` built from `harness_v2/` with the pinned znc
  toolchain (binary is a scratch artifact, not committed). 6 configs × 48
  items × 2 arms; A/B byte-identical on all 12 runs (sha256 of jsonl+ledger).
- Raw run outputs: `~/workspace/scratch-h5/cot/` (scratch, not committed —
  same convention as the H5 sweep). Analysis inputs SHA-pinned in the
  measurement logs.
- Judge: the Zag harness itself (verdicts + `correct` flags from the binary);
  metric computation is deterministic post-hoc measurement
  (`chain_of_thought/measure_cot.py`), same role as the H5 re-derivation script.

## 6. Follow-ups worth running (not done here)

- A delayed-disconfirmation variant of FP with the misleading premise arriving
  *late* (overthinking probe): does extra depth flip correct→wrong?
- Recalibrating Q2 into the strict form and re-freezing it as the premise
  metric, since frozen Q2 has no dynamic range.
- Longer chains (6–10 hops): does the depth requirement track chain length 1:1?
