# DEPTH-1 DISCIPLINE — Verdict (2026-09-24)

Micah's hypothesis: **"even at depth 1 the system should still be disciplined."**
Second question: **is shallow failure fixable, or just low knowledge?**

## Headline

**It's not low knowledge. It's sloppy judgment — and it's partially fixable.**

The knowledge partition came back degenerate: **all 766 items are SINGLE** —
for every item, at least one single evidence item alone makes the ground
truth the leader. There is not one MULTI item in any battery. No depth-1
failure in this trial is an information limit. Every failure is the system
looking at the wrong evidence.

Fork E (falsification-first selection + verification veto + confidence cap)
**SURVIVES** all frozen bars jointly: trap accuracy 0% → 100%, zero
confident-wrong on every battery, zero false vetoes, and it is not depth-2
in disguise (12.3% verdict disagreement with true depth-2, which it beats
100% to 33% on trap).

But "disciplined" here means **never confidently wrong**, not reliably
right: on the 14-item red-team battery E is 6 correct / 5 withheld /
3 wrong-but-tentative. The price of discipline at depth 1 is abstention
and tentativeness, not truth.

## Per-fork verdicts

| Fork | Mechanism | Trap acc | rt_d1 acc | Conf-wrong (rt_d1) | Verdict |
|------|-----------|----------|-----------|--------------------|---------|
| A | baseline depth-1 | 0.000 | 0.500 | 2 items (STRONG×2 @1000) | baseline (the disease) |
| B | falsification-first selection | **1.000** | 0.571 | **6 items** | **KILLED** (red team) |
| C | verification veto | 0.000 | 0.143 | 0 | SURVIVES (degenerate) |
| D | confidence cap | 0.000 | 0.500 | 0 | **KILLED** (frozen bar) |
| E | B+C+D | **1.000** | 0.429 | 0 | **SURVIVES** |
| ref | true depth-2 | 0.331 | 0.571 | 6 items | reference |

(admit/revoke/logic: all forks 1.000 — those batteries are trivially SINGLE,
every evidence points at the truth.)

**B is killed by the red team, not the bars.** It passes the frozen bars
(trap +100pp, no drops) but emits confident-wrong (conf=1000) on 6/14
red-team items: all three POISON and all three BAIT. Falsification-first
selection is a different bias, not discipline — it trusts attacks
absolutely, so when the attack is the lie (poison), it refutes the truth
at full confidence. On trap the attacks are truth-telling, so B looks
perfect there. Selection without skepticism is just gullibility with
better targeting.

**C survives the letter but is degenerate.** The veto fires on 100% of trap
items and 86% of rt_d1 — it cannot distinguish a true attack from a poison
attack, so it abstains on everything adversarial. Trap accuracy 0%,
rt_d1 accuracy 0.143. False-veto rate on admit∪revoke∪logic is 0 only
because it never fires there. Discipline via total abstention is not
judgment.

**D is killed by the frozen bar** (trap mean_conf_wrong 100→100, bar was
≤60). The bar is degenerate on trap: the cap is 1000·consumed/ne, and with
trap margins at 100 the cap structurally cannot bind. Noted for the
record: on rt_d1, where confident-wrong actually occurs, D passes both
halves (mean_conf_wrong 357→214 ≤ 214.3; mean_conf_correct 100→100 ≥ 90),
eliminating A's confident errors on the STRONG items (1000→500). The
mechanism is sound; the frozen bar measured it where it cannot act.
No amendment is requested — the kill stands as written.

**E survives.** The combination works because the parts cover each other's
failures: B's selection solves trap; the cap demotes B's poison failures
from confident-wrong (1000) to tentative-wrong (200–333), dodging the
red-team kill; the veto converts B's bait failures into withholds. Item
accounting on rt_d1: 6 correct (STRONG×2, CLEAN×4), 5 withheld (BAIT×3
via veto, DOUBLE×2 via veto — the DOUBLE withholds are false withholds,
the priced trade: the veto can't see that e5 already defeated e3/e4's
attacks), 3 wrong-but-tentative (POISON×3, conf 200–333 — the veto doesn't
fire because the poison attacks ADMIT, not the verdict REJECT).

## The four frozen questions

**1. Can depth 1 be made disciplined?** Partially, yes — fork E. It is never
confidently wrong on any of 766+14 items, solves the trap battery
completely, and fires zero false vetoes on the clean batteries. But it is
disciplined in the sense of humility, not accuracy: it withholds 36% and
hedges 21% on adversarial items. No fork is both disciplined and reliably
right at depth 1.

**2. At what cost?** B costs 6 confident catastrophes per 14 adversarial
items (unacceptable — killed). C costs all accuracy wherever the veto can
fire. D costs nothing and buys nothing on trap. E costs 36% withhold +
tentative-wrong on the red team, and lower red-team accuracy than the
killed B (0.429 vs 0.571) — caution trades against correctness.

**3. Selection vs information: do forks recover SINGLE failures while MULTI
failures persist?** There are no MULTI failures — the partition is 766
SINGLE / 0 MULTI. B recovers 100% of trap SINGLE failures by selection
alone. The "low knowledge" hypothesis is falsified for this trial: depth-1
failure is never missing information, it is always the wrong look. (Depth
being load-bearing for genuinely MULTI items remains untested — we would
need a battery where no single evidence suffices.)

**4. Is disciplined depth-1 just depth-2 with extra steps?** No. B and E
score 100% on trap vs 33.1% for true depth-2; verdict disagreement with
depth-2 is 12.3% (E) and 18.1% (C), both well above the 5% cosmetic
trigger. The mechanisms are qualitatively different from "more rounds":
adversarial selection, post-hoc veto, and humility caps. If anything, the
comparison reverses — depth-2 eats poison confidently (6 confident-wrong
on rt_d1, same as the killed B) while disciplined depth-1 does not.
Depth-2 here looks like undisciplined depth-1 with extra steps.

## Gates and method notes

- **Equivalence gate: PASS.** d1mode=0 byte-identical to harness_v2
  shallow=1 on all 4 batteries (results AND ledgers). The D1 fields
  (veto/sel_ev, d1=/vthr= ledger detail) are emitted only when d1mode≠0.
- **Determinism: PASS.** All 30 cells (6 forks × 5 batteries) run twice,
  byte-identical results and ledgers. 4,596 result lines, all valid JSON.
- **Unit tests: PASS** (3 hand-computed, all match): TRAP-A1-001/B →
  REJECT@1000/veto0/sel=e3; TRAP-A1-001/E → REJECT@200/veto0/sel=e3
  (cap=1000·1/5); clean-admit/C → PROVISIONAL_INSTALL@1000/veto0;
  RT-POISON-01/C → WITHHOLD@0/veto1 (the priced false-withhold trade).
  Ordering note: batteries ran before the hand-computed unit tests were
  checked (gate order violated); the binary is deterministic and the
  tests pass on the identical binary, so results stand.
- znc issues hit during the build (for the record): `.*` on a local
  struct *value* fails the build ("field access on non-struct value");
  `cfg.d1mode` in condition position on a large local struct miscompiled —
  routed through a `*DCfg` helper (ZNC-010 pattern). One self-inflicted
  JSON bug (extra `\"` in the sel_ev literal) was caught by JSON
  validation before analysis; no results were analyzed from malformed
  output.

## Bottom line for Micah

Your standing attribution — "just with proper knowledge TNN can do
anything" — survives this trial intact: the knowledge was there in every
single item. What depth-1 lacks isn't knowledge, it's **discipline in
choosing what to look at and how sure to be**. Fork E proves discipline
is installable at depth 1 (selection + veto + cap), and proves its price:
it never lies confidently, but on adversarial ground it mostly abstains
or hedges. Real judgment — being right *and* calibrated — still wants
either better selection (the veto is too blunt; it can't see that e5
defeated e3/e4) or depth. The next experiment should be smarter vetoes
(defeat-aware: don't veto on attacks that a consumed evidence already
defeated) and a genuinely MULTI battery to find where depth is actually
load-bearing.
