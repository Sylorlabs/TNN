# PREREG3 — One-Brain Round 3 (fresh prereg, NOT an amendment)

Status: **FROZEN** — 2026-09-27 (UTC timestamp in FREEZE3.txt).
Workdir: `~/workspace/onebrain3/prereg/`. Round-1/2 files (`~/workspace/onebrain/`, `~/workspace/onebrain2/`) are reference only; nothing here amends them.

## 0. Lineage

Round 1 (commit `abcf8a9d3`) KILLED H1 by K1: ledger fan-out is genuine
machinery with causal cross-talk (K2/K3/K4 passed), but onebrain
scored 14/28 = single, fixing 0 of the 11 problems single got wrong.
Mechanism: shared audits ANNIHILATE all candidates instead of
discriminating (canonical p02).

Round 2 (commit `d3d070b7d`) KILLED H1' by K1': 12/44 = 12/44 =
12/44 (single = onebrain = ablate). The red-team re-derivation
(REDTEAM2) AMENDED the mechanism story in the two ways that define
round 3:

1. **V4 was outcome-inert on v5.** The xDeny probe gave 0/44
   winner-deltas; all 9 denials were inconsequential. The q15 "fix"
   is attributable to the unchanged round-1 **reading duel** — the
   same mechanism that breaks q06/q11/q25. "The duel giveth (q15)
   and the duel taketh away (q06/q11/q25)." Least-disruptive
   thinking must extend to READING conflicts.
2. **Reintegration was decorative by construction.** Base −3/hid with
   bonus = corr ∈ [0,3] makes the argmax winner PROVABLY the
   lowest-hid alive bid on every possible input. The honest null
   (lowest-hid default) gave 0/44 deltas → K4' reintegration FAILS.

Round 3 tests: (a) least-disruptive READING invalidation, (b)
genuinely-deliberative reintegration, (c) V4 carried over — on a v6
set where both bind.

## 1. Hypotheses

**H1''**: One-brain with (a) least-disruptive reading invalidation
(§4), (b) genuinely-deliberative reintegration (§5), (c) V4 carried
over — yields a REAL accuracy benefit over single deliberation,
attributable to the shared-state channel, not extra passes or
scaffolding.

**H0''**: No benefit — the machinery cannot beat single
deliberation, the gain (if any) comes from extra passes or
scaffolding, or the channel remains decorative.

## 2. Output space (PINNED — quoted verbatim from the frozen machinery)

Source: `~/workspace/onebrain2/impl/onebrain_v2.zag`. Round 3 PRESERVES
this action/reading space exactly; v3 changes only (i) the
reading-duel invalidation policy, (ii) reintegration from mechanical
argmax to deliberation, (iii) V4 retained. Every quoted block below
was extracted byte-verbatim from the source (verification log in
Appendix A).

### 2.1 Readings (verbatim, `rd_name`, source lines 173–183)

```
fn rd_name(rd:i32)[]u8 {
    if(rd==0){return "correction";}
    if(rd==1){return "resume";}
    if(rd==2){return "challenge";}
    if(rd==3){return "provenance";}
    if(rd==4){return "joke";}
    if(rd==5){return "mem";}
    if(rd==6){return "forget";}
    if(rd==7){return "assertion";}
    if(rd==8){return "compose";}
    return "plain";
}
```

hid 9 is **plain** (the file always wins; the round-2 brief's
"none-of-the-above" was a mislabel).

Triggers (`gen_readings`, lines 404–440): rd 0–6, 8 fire iff a
case-insensitive trigger-token match occurs in the query. rd 7 fires
iff NO `?` byte (63) appears anywhere in the query. rd 9 fires iff no
reading 0–6 or 8 fired (rd 7 may fire). A reading row's `bid@12` IS its
evidence bit (ev).

Trigger words (`rd_trig`): 0: no, actually, meant, correction; 1: continue, resume;
2: prove, challenge, doubt, really; 3: source, cite, origin, according;
4: joke, funny, laugh, hilarious, knock; 5: remember, recall, memory, remind;
6: forget, delete, erase, remove; 8: compare, versus, vs, combine, difference, between.

### 2.2 Actions (verbatim, source lines 690–730)

```
fn act_name(hid:i32)[]u8 {
    if(hid==13){return "joke";}
    if(hid==14){return "memory";}
    if(hid==15){return "forget";}
    if(hid==16){return "correction";}
    if(hid==17){return "resume";}
    if(hid==18){return "compose";}
    if(hid==19){return "challenge";}
    if(hid==20){return "provenance";}
    if(hid==21){return "assertion";}
    if(hid==22){return "clarify";}
    if(hid==23){return "withhold";}
    return "default";
}
fn act_base(hid:i32)i32 {
    if(hid==13){return 240;}
    if(hid==14){return 237;}
    if(hid==15){return 234;}
    if(hid==16){return 231;}
    if(hid==17){return 228;}
    if(hid==18){return 225;}
    if(hid==19){return 222;}
    if(hid==20){return 219;}
    if(hid==21){return 216;}
    if(hid==22){return 213;}
    if(hid==23){return 210;}
    return 207;
}
fn act_gate_rd(hid:i32) i32 {
    if(hid==13){return 4;}
    if(hid==14){return 5;}
    if(hid==15){return 6;}
    if(hid==16){return 0;}
    if(hid==17){return 1;}
    if(hid==18){return 8;}
    if(hid==19){return 2;}
    if(hid==20){return 3;}
    if(hid==21){return 7;}
    if(hid==24){return 9;}
    return -1;
}
```

D1 (file wins): PREREG2's quoted `act_gate_rd` omitted the
`if(hid==24){return 9;}` line; bid 24 fires iff reading 9 fired.

### 2.3 Bid firing rules (verbatim logic, `gen_actions`, lines 734–844)

- Bids 13–20 fire iff their gating reading's `bid@12 == 1`.
- Bid 21 fires iff reading 7 AND reading 9 both have `bid@12 == 1` (gr=7).
- Bid 22 (clarify) fires iff `nread >= 2`; gr = lowest-hid alive
  fired reading.
- Bid 23 (withhold) fires iff `bgf < 0` (no alive fact candidate
  with `gate@48 == 0`); gr=−1.
- Score = `base + bonus`; bonus = `corr_of(gr)` capped at 3
  (`corr_of` ≥ 0: `best` starts at 0, only increases).
- ELIM kills unfired bids (PRE_FAIL) and fired bids with empty
  staged answers (GATE); every bid stages a fallback, so in practice
  only PRE_FAIL fires. Readings are never eliminated by ELIM.

CONSEQUENCE (REDTEAM2, proven): base is strictly −3/hid and bonus ∈
[0,3], so round 2's mechanical argmax winner was provably the
lowest-hid alive bid on every possible input. Round 3 replaces this
stage with deliberation (§5); the mechanical argmax is retired.

### 2.4 Ledger layout (verbatim, lines 335–341, 361–368)

25 rows × 552 bytes from offset 4 (`led_sz()` = 13820). Row fields:
hid@0 kind@4 status@8 bid@12 base@16 bonus@20 score@24 reason@28
detail@32 ev_kind@36 ev_score@40 fid@44 gate@48 content@68..552.
Rows 0–9: readings (kind=0). Rows 10–12: fact candidates (kind=1;
top-3 KB facts by keyword overlap; null candidates fid=−1, gate=1).
Rows 13–24: action bids (kind=2). Turn fields: fact-winner@13804,
fact-close@13808, act-close@13812, FORK@13816.

### 2.5 Fork, verdict

`fork_assess`: FORK=1 iff `nread >= 2` AND the top-two score margin
among fired, alive bids is ≤ 12 (scores = base+bonus @24). Skipped in
single mode; v2 already emits a FORK_DELIB trace, which v3 keeps.

A **verdict** = the winning bid hid chosen by the reintegration stage.
**NO_VERDICT** if every bid is annihilated (no alive fired bid).

## 3. What "conscious every step" means (carried over, four stages)

The fork decision, the sub-deliberations, the audits, and the
reintegration must EACH be explicit deliberation over ledger state —
not a hardcoded transform — satisfying all four (on v5, reintegration
FAILED this: its honest null gave 0/44 deltas — REDTEAM2; §5's
deliberation must pass it on v6):

1. **Ledger-read**: the stage's inputs are ledger rows/fields only
   (citing row hids and field offsets); no side-channel inputs.
2. **White-box trace**: the stage emits a trace record stating what
   was considered, what was decided, and why (which ledger facts
   bore on the decision).
3. **Neuter-causal**: suppressing the stage's deliberation (output
   replaced with a null/default, everything else fixed) changes
   outcomes on the frozen set. A stage whose neutering changes
   nothing is decorative, not deliberation.
4. **Audit scope**: audits may write only eliminations (status=1)
   and fact invalidations — the same write vocabulary rounds 1–2
   used. Round 3 changes the reading-duel POLICY (§4) and the
   reintegration STAGE (§5), not the vocabulary.

## 4. Least-disruptive READING invalidation (the principle under test)

Round 2's V4 governs FACT invalidation and is CARRIED OVER
unchanged (PREREG2 §4). Round 3 extends the same least-disruptive
class of thinking to READING conflicts, stated generally over the
reading-conflict graph — NOT as per-item rules:

- **When readings conflict** (the old duel condition `cq > c2+1`
  would fire), **prefer invalidating the least-evidenced /
  least-specific reading.** corr is a tiebreak, not the weapon.
- **Evidence** = substantive trigger presence (rd 0–6, 8 match
  real query tokens) vs assertion-by-absence (rd 7 fires on mere
  `?`-lessness; its corr=2 is topic breadth, not evidence). Trigger
  evidence outranks absence-evidence.
- **Least-disruptive preference:** prefer the kill (or abstention)
  that preserves the richest surviving bid structure; a kill that
  removes a reading whose bids carry the judged-correct answer is
  destructive.
- **Keep q15-like wins, fix q06/q11/q25-like annihilations:** the new
  policy must still allow genuine discrimination (q15: assertion
  cleaning bids 16/22 so compose 18 won), but any reading kill whose
  consequence set is the whole alive field MUST abstain — the
  annihilation guard extends to the duel: no kill may leave zero
  alive fired bids (it bound 49 abstains in round 2; it must bind the
  duel too).
- At most one reading denial per invalidation step (the minimum
  resolving the conflict), then re-derive.

The implementer owns the internals; the prereg pins only this principle and the hard abstention rule (empty-field kills forbidden).

## 5. Reintegration deliberation spec

The final integration stage deliberates over the shared ledger.
The prereg does NOT prescribe the decision rule (implementer owns
it) but pins the following:

- **Inputs (ledger only):** fired, alive bids (hid, base@16,
  bonus@20, score@24, fid@44, gating reading detail@32); alive
  reading states (hid, ev, corr); fact candidates (fid@44, gate@48);
  the audit history (duel/denial trace lines); sub-deliberation
  agreement (branch winners, margins). No side channels.
- **Output:** the chosen winner hid, plus a white-box trace record.
- **Trace must contain:** candidates considered (hids); ledger
  facts cited (row hid + field offset); why each non-winner lost;
  the decision rule in plain words (not a numeric formula); the
  null-case note (choice with no ledger support).
- **Honest null:** lowest-hid alive bid — the K4'' neuter default,
  PROVEN outcome-identical to the retired argmax. A "deliberation"
  that never deviates is decorative by the same proof: the stage
  must be CAPABLE of choosing a non-lowest-hid bid where the
  ledger justifies it (§9c), consuming at least one non-score
  ledger fact (support quality, agreement, audit history) that
  can change the winner.

## 6. Kill bars (ALL must pass; any failure kills or voids as noted)

| ID | Bar | Falsification test | Verdict if failed |
|----|-----|-------------------|-------------------|
| K1'' | Accuracy benefit from the channel (conjunctive: the ablation must also score below one-brain, proving the gain rides the channel, not extra passes) | One-brain accuracy ≤ single-deliberation accuracy on frozen v6, OR the shared-writes-off ablation matches/exceeds one-brain accuracy | KILL H1'' |
| K2'' | Causal cross-talk | Poison test: invalidating a shared fact candidate mid-deliberation produces ZERO changes to other branches' bids/eliminations | KILL H1'' |
| K3'' | TNN's own decision | Scaffold-removal: minimal driver, no fan_out call; machinery does NOT fan out on fork-worthy problems | VOID (not TNN's decision) |
| K4'' | Per-stage trace causality | Neutering any stage (fork→0, subpass→null, audit→null, reintegration→lowest-hid alive bid) changes NOTHING on the set | KILL the "conscious" claim for that stage |
| K5'' | Determinism | Any two of 3 reruns differ at the byte level (SHA-256) | VOID the evidence |
| K6'' | No RNG | Grep + source audit finds RNG use in any decision path | VOID the evidence |

K4'' note: the reintegration null is the honest null (lowest-hid
alive bid, proven outcome-identical to the retired argmax);
neutering to 0 deltas against it = argmax wearing a trace.
Fork/subpass/audit neuters keep round-2 definitions.

## 7. NO-TUNING RULE (load-bearing)

- The v6 set is frozen (SHA-256 + UTC in FREEZE3.txt) BEFORE any
  implementer scoring run (onebrain/ablate/poison/min modes);
  the implementer develops on v4/v5 only.
- The prereg author validates candidate v6 items against the SPEC
  (§9) in `single` mode ONLY (never forks; outputs never adjust
  expected bids). Expected bids come from human judgment +
  rationales, never machinery.

## 8. Scoring protocol

- Accuracy: onebrain vs single-deliberation vs shared-writes-off
  ablation, per problem and aggregate, on frozen v6. Report EVERY
  problem where one-brain does NOT win, with the ledger trace.
  Poison is a causal probe (K2''), not an accuracy contender; min
  mode for K3''; nF/nS/nA/nG for K4''.
- Determinism: 3× reruns, SHA-256 byte-identical; RNG audit (grep
  + source audit of the v3 implementation) finds no RNG in
  decision paths.
- Verdicts are bid hids (§2.5); NO_VERDICT counts as wrong.

## 9. v6 set requirements (for the set builder)

~44 items, same 5-column TSV as v5
(`id\tquery\texpected_bid\treadings\trationale`); expected bids from
human judgment + rationales, never machinery. Unlike v5 (where V4
contributed exactly 0 — xDeny: 0/44), v6 must be a set where
fact-invalidation BINDS and the duel is STRESSED:

(a) **Fact-invalidation binds** (substantial fraction): ≥2 alive
fact candidates, a genuine audit inconsistency, the denied fact with
dependent bids, a denial that CHANGES the winner — hand-checked
(single-mode probes only), since v5's 9 denials were all
inconsequential.

(b) **Reading duel stressed** (`?`-less queries firing rd7 with
corr=2 alongside substantive corr=0 readings; duel determinative):
include BOTH q15-like items (genuine discrimination — keep the
kill) and q06-like items (kill annihilates the field → NO_VERDICT;
the guard must abstain and a substantive winner survive).

(c) **Reintegration room:** multiple bids alive at final integration
with a contestable winner — close scores (margin ≤ 12), differing
support quality (fid strength, corr spread), or disagreeing branch
winners — giving the deliberation ledger grounds to prefer a
non-lowest-hid bid.

General: items should be fork-firable (≥2 ev=1 readings; close
action-bid margins) so one-brain can diverge from single; keep v5's
`readings` column semantics (expected fired readings, contested bid
pair, margin). Rationale required on every item.

## 10. Non-goals

- This prereg does not specify the reading-invalidation or
  reintegration internals (the implementer owns them); it pins the
  principle (§4), the spec (§5), the output space (§2), and the bars
  (§6).
- v6 has ~44 single-turn problems; multi-turn deliberation is out
  of scope.
- The 12-fact KB is unchanged from rounds 1–2 (frozen in the
  implementation); v6 entities are drawn from it, plus KB-absent
  entities only where the judged-correct bid is withhold-by-absence.
- V4 fact-invalidation is not re-tested as a hypothesis — it is
  carried over; §9a only ensures the set lets it bind. Round-1/2
  files are reference only; this prereg stands alone.

## Appendix A — verbatim-pinning verification log

Method: byte-extraction via `sed`/`grep` against
`~/workspace/onebrain2/impl/onebrain_v2.zag`; quoted blocks copied
from tool output, not transcribed. Result: **PASS** — every quoted
line verified; one discrepancy vs PREREG2 recorded (D1, file wins).

| Quoted block | Source function | Lines | Check |
|---|---|---|---|
| §2.1 `rd_name` | `rd_name` | 173–183 | `rd_name(9)` returns `"plain"` (line 182 `return "plain";`) |
| §2.2 `act_name`/`act_base`/`act_gate_rd` | three fns | 690–730 | includes `if(hid==24){return 9;}` (line 729) — absent from PREREG2's quote |
| §2.3 firing rules (21/22/23) | `gen_actions` | 740–757 | 21: rd7 AND rd9 ev=1, gr=7; 22: `nread>=2`, gr=lowest-hid alive; 23: `bgf<0`, gr=−1 |
| §2.3 bonus cap | `gen_actions` / `corr_of` | 774–776 / 609–623 | bonus=co capped at 3; corr_of ≥ 0 (best starts 0) |
| §2.4 geometry | header comment + `led_sz`/`lr_get` | 335–341, 367–368 | 25×552 @ offset 4; turn fields 13804/13808/13812; FORK@13816 |
| §2.1 triggers | `gen_readings` | 404–440 | rd7: no `?` byte (63); rd9: no reading 0–6/8 fired (7 may fire) |
| §2.5 fork rule | `fork_assess` | 873–873+ | `nread>=2` AND top-two margin ≤12 |
| Duel condition (old) | `ob_audit` | ~1094–1112 | `if(cq>c2+1)` — replaced in v3 |
