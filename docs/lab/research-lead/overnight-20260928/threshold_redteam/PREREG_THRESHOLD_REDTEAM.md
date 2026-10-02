# Prereg: Conditional-Threshold Red Team (FROZEN)

Date: 2026-09-30. Attack prereg. Committed alone before any attack
implementation, family generation, or test execution.

## Target

The conditional-threshold mechanism at commit d0d296650
(THRESHOLD-PASS), independently reproduced byte-identical at 07785ac78.
The mechanism: conditional-first search (COND primitive op==4 +
tiered combiner `beam_cond_combine`) on R3 Arm 2, with T1 license-cost
tax (B=2 Tier-1 / B=4 Tier-2) and T2 stability-gated license. Tier-1
min slice = min(4, en/8); Tier-2 min slice = max(4, en/8) plus
persistence gate (condition and both arms in pbeam). Scope claimed:
bounded L2. No SURVIVES claim exists. This red team assumes the claim
is false and attempts to break it.

## Charge

Two structural suspicions, both untested by frozen bars:

1. The Tier-2 pass may be decorative. Every frozen battery presents
true conditions that are Tier-1 (terminals or the D library term).
The Tier-2 pass (round-built conditions, persistence gate) has never
been shown to do real work. If the mechanism is Tier-1-bias-fitting,
a world whose true condition is Tier-2 will defeat it.

2. The Tier-1 min slice (min(4, en/8) = 1 at en=8) is extremely
lenient. Under crowding (distractor conditions, tight time), the
mechanism may install spurious COND nodes that fit small evidence
but do not generalize.

## Attack Family A: Tier-2 condition (A-T2COND)

New sealed family fam 9, defined mathematically here and implemented
after this prereg:

E9 = (C AND Y4) OR ((NOT C) AND Y5), where C = (x1 AND x2).
Bit layout (same as fam 8): Y1..Y6 = bits 0..5; C on bits 0,1;
Y4 = bit 3; Y5 = bit 4; Y6 = bit 5 is the decoy; bit 2 unused (0).

Reference implementation (Zag semantics, also the runtime check):

```
if(fam==9){
  let x1:i32=(x>>0)&1;
  let x2:i32=(x>>1)&1;
  let y4:i32=(x>>3)&1;
  let y5:i32=(x>>4)&1;
  let c:i32=x1 & x2;
  let nc:i32=c ^ 1;
  let r:i32=(c & y4) | (nc & y5);
  return r;
}
```

C is composite: not a terminal, not a library term. Any COND node
using C as its condition has a kind-1 (round-built) condition and
must pass through the Tier-2 combiner pass. This mirrors fam 8
exactly except the condition tier.

### Protocol A1-FAIR

Purpose: give the Tier-2 pass its best fair chance. Frozen 16-row
evidence (no RNG, no interventions), 24 combiner rounds.

Frozen evidence rows (x, y=E9(x)):

x:    0 1 2 3 8 9 10 11 16 17 18 19 24 25 26 27
y:    0 0 0 0 0 0 0  1  1  1  1  0  1  1  1  1

Check: C=(x1&x2)=1 exactly on x in {3,11,19,27} (4 rows);
C=0 on the other 12 rows. en=16 gives Tier-2 min slice
max(4, 16/8)=4: r1c=4 meets it, r0c=12 meets it. Exact slice
agreement holds for arms Y4 (on C=1 rows, target=Y4) and Y5
(on C=0 rows, target=Y5). The driver asserts sealed(9,x)==y
for all 16 rows at startup and reports EVIDENCE-MISMATCH if any
row disagrees (guard against transcription error; a mismatch
voids the run, it does not count as a mechanism failure).

Driver: initialize beam with 8 terminals (no library term),
load the 16 frozen rows, run 24x beam_extend_round (mechanism
functions copied verbatim from d0d296650, unmodified), no
interventions. hitbuf target = E9 full-64 signature (computed
at runtime by the same method as e_sig, but for fam 9).

Read-only diagnostics (do not affect search):
- D1: per round, is there a kind-1 node with C's 64-bit signature
  in the beam? In pbeam? (C signature computed at runtime by the
  same bitmap method as d_sig.)
- D2: CONDHIT round from hitbuf (first round a built COND node
  matched the E9 64-bit signature), or -1.
- D3: post-run scan: does the best (beam[0]) node contain a COND
  (op==4) node whose condition child has kind==1 and C's signature?
- D4: true_correct(fam 9, best) over all 64 inputs.

### Frozen predictions for Family A

GENUINE (Tier-2 pass is real): D1 shows a kind-1 C-signature node
present in beam and pbeam for at least one round r >= 1; D2 fires
(CONDHIT round >= 0); D3 = 1; D4 >= 61/64 (the phase2 hit bar).

BIAS-FITTING (Tier-2 pass decorative): D2 = -1 (never fires), or
D4 < 61/64. D1 localizes the failure: C never in beam (culled by
score selection), C in beam but never in pbeam (persistence gate
unreachable), or C in both but combiner still silent (logic dead).

### Verdict bar for Family A

SURVIVE-THIS-ROUND: all four GENUINE predictions hold.
BREAK: any BIAS-FITTING prediction holds. The D1 diagnostic is
reported in either case to name the exact failure point
(beam culling vs persistence gate vs combiner logic).

## Attack Family B: crowding (B-CROWD)

Same frozen world as A2 (fam 8: E = (D AND Y4) OR ((NOT D) AND Y5)),
so the true structure is unchanged and only crowding varies.

Distractor library terms (defined mathematically here; signatures
computed at runtime by deterministic bitmap functions, no tuning):

- D1 (terminal index 9): D XOR (x1 AND x2 AND x3). Diverges from D
  exactly where x1=x2=x3=1 (8 of 64 inputs).
- D2 (terminal index 10): D XOR x6. Diverges from D exactly where
  x6=1 (32 of 64 inputs).
- D3 (terminal index 11): NOT D. Diverges everywhere; note
  COND(D3, Y5, Y4) is behaviorally identical to E (arms swapped),
  so a D3-based solution at 64/64 counts as correct, not as a break.

D is fam 8's d = (x1 & (x2^x3)) | ((x1^1) & (x2&x3)), signature
(1751672936, 1751672936), terminal index 8.

### Protocol B1

Driver modeled on phase2 (seed 710202, identical to frozen A2):
8 terminals, then library terms added in this order: D1 (t=9),
D2 (t=10), D3 (t=11), then the true D (t=8). Distractors get lower
node ids so exact score/opc ties favor them (adversarial tie-break;
tests selection, not luck). passive() then 12 rounds
(beam_extend_round + select_iv/do_iv), i.e. tighter time than the
frozen 24. hit_iv = first round with true_correct >= 61/64, or 12.

Read-only diagnostics: D5 = has_d_subexpr(best, true D sig) (1 if
the true D term is used); D6 = which condition terminal index the
best COND uses (scan); D7 = true_correct(fam 8, best)/64.

### Frozen predictions for Family B

ROBUST: D7 >= 61/64 within 12 rounds (the mechanism still resolves
despite 3 distractor conditions and halved time). D5/D6 reported
as diagnostics (a D3-based 64/64 is correct-via-equivalent).

FRAGILE: D7 < 61/64 after 12 rounds (crowding defeats resolution),
or the best node installs D1/D2 with non-generalizing arms.

### Verdict bar for Family B

SURVIVE-THIS-ROUND: D7 >= 61/64 within 12 rounds.
BREAK: D7 < 61/64 after 12 rounds. D5/D6 name the installed
condition in either case.

## Overall verdict

REDTEAM-THRESHOLD-BREAK: either family verdict is BREAK.
REDTEAM-THRESHOLD-SURVIVE-THIS-ROUND: both families survive.
A split (one BREAK, one SURVIVE) is reported as BREAK with the
surviving family noted, since a single broken structural claim
refutes the mechanism as characterized.

## Kill bars

K1: this prereg strictly precedes family generation and testing.
Verified via git merge-base --is-ancestor before implementation.
Seeds: B1 seed 710202 frozen here; A1 uses no RNG. The fam 9
definition above is the seal; implementation follows it exactly.

K2: both families executed 3/3 (byte-identical expected; A1 has no
RNG, B1 fixed seed) with per-family BREAK/SURVIVE-THIS-ROUND
verdicts against the frozen predictions above.

K3: pure Zag, zero Python at every step (implementation, build,
runs, analysis via shell tools only). Committed mechanism
functions byte-identical to d0d296650 (verified by diff showing
only additions: fam 9, drivers, diagnostics, main). No em dashes
(shell-only check_no_dash.sh).

## Governance

- Attack the committed mechanism; do not modify it. The attack
  file is a copy; the diff against d0d296650's r3h.zag must show
  additions only.
- Owned path: docs/lab/research-lead/overnight-20260928/threshold_redteam/.
- Never touch docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md.
- If a live .git/index.lock is hit, wait and retry; never remove it.
- This prereg does not weaken any frozen bar. The 12-round B1 bar
  is tighter than the frozen 24-round A2 protocol; that is the
  attack, not a relaxation.
