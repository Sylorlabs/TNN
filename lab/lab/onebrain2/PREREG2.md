# PREREG2 — One-Brain Round 2 (fresh prereg, NOT an amendment)

Status: **FROZEN** — 2026-09-27 (UTC timestamp in FREEZE.txt).
Workdir: `~/workspace/onebrain2/prereg/`. Round-1 files live in
`~/workspace/onebrain/` and are reference only; nothing here amends them.

## 0. Lineage

Round 1 (commit `abcf8a9d3`, `docs/lab/onebrain/`) KILLED H1 by K1:
the ledger-driven fan-out is genuine TNN machinery with causal
cross-talk (K2/K3/K4 passed), but onebrain scored 14/28 — identical to
single deliberation — fixing 0 of the 11 problems single got wrong.

Mechanism finding (round 1): shared-ledger audits ANNIHILATE all
candidates instead of discriminating. Canonical case p02: the forget
reading denied the joke fact, killing all three live bids including
its own. The audit had no least-disruptive option — invalidation was
all-or-nothing.

Red-team caveat (round 1): the annihilation turns on one unprincipled
tie-break in the audit. The V4-class fix — least-disruptive
invalidation (deny the least-relevant alive fact candidate; ties by
fewest dependent bids) — hand-simulated to 15/28 and was deliberately
NOT run, so the number is a prediction, not evidence.

Round 2 re-tests under this fresh prereg. A separate implementer
(Worker B) builds the V4-class machinery in parallel against the v4
set only; this prereg and the v5 problem set are authored WITHOUT any
v2 implementation existing.

## 1. Hypotheses

**H1'**: A shared ledger whose audits DISCRIMINATE rather than
annihilate (V4-class least-disruptive invalidation, §4) gives TNN's
own fan-out a real accuracy benefit over single deliberation, and the
benefit is attributable to the shared-state channel (not to extra
passes, not to crew scaffolding).

**H0'**: No benefit — the sharing is decorative, the gain (if any)
comes from extra deliberation passes or from crew scaffolding, or the
machinery cannot beat single deliberation at all.

## 2. Output space (PINNED — misreading this killed v3; it is quoted verbatim from the frozen machinery)

Source: `~/workspace/onebrain/impl/onebrain.zag`, functions
`act_name` / `act_base` / `act_gate_rd` (lines 688–724), `rd_name`
(lines 171–181), `gen_actions` firing rules (lines 732–800),
`fork_assess` (lines 866–890), ledger geometry (lines 331–338).

### 2.1 Action bids (verbatim)

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

In words: hid 13 joke (240) ← reading 4; 14 memory (237) ← 5;
15 forget (234) ← 6; 16 correction (231) ← 0; 17 resume (228) ← 1;
18 compose (225) ← 8; 19 challenge (222) ← 2; 20 provenance (219) ← 3;
21 assertion (216) ← readings 7 AND 9 jointly (see §2.3);
22 clarify (213), no gate; 23 withhold (210), no gate; 24 default (207)
← reading 9. (`act_gate_rd` returns −1 for 22 and 23 via fallthrough.)

### 2.2 Readings (verbatim from `rd_name`)

hid 0 correction, 1 resume, 2 challenge, 3 provenance, 4 joke,
5 mem, 6 forget, 7 assertion, 8 compose, 9 **plain**.

**RECORDED DISCREPANCY (file wins):** the round-2 brief described
reading 9 as "none-of-the-above". The source says `rd_name(9)` returns
`"plain"` (lines 171–181: `if(rd==8){return "compose";} return "plain";`).
All round-2 documents use **plain** for hid 9.

Trigger words (`rd_trig`, exact case-insensitive token match):
- 0: no, actually, meant, correction
- 1: continue, resume
- 2: prove, challenge, doubt, really
- 3: source, cite, origin, according
- 4: joke, funny, laugh, hilarious, knock
- 5: remember, recall, memory, remind
- 6: forget, delete, erase, remove
- 8: compare, versus, vs, combine, difference, between
- 7: ev=1 iff the query contains no `?` byte anywhere
- 9: ev=1 iff no reading 0–6 or 8 fired (7 may fire)

A reading row's `bid@12` field IS its evidence bit (ev).

### 2.3 Bid firing rules (from `gen_actions`)

- Bids 13–20 fire iff their gating reading's `bid@12 == 1`.
- Bid 21 (assertion) fires iff reading 7 AND reading 9 both have
  `bid@12 == 1`; its supporting-fact search uses gr=7.
- Bid 22 (clarify) fires iff `nread >= 2` (alive readings with ev=1);
  its gr is the lowest-hid alive fired reading.
- Bid 23 (withhold) fires iff `bgf < 0`, i.e. no alive fact candidate
  with `gate@48 == 0` (best_gated_fact).
- Bid 24 (default) fires iff reading 9 fired.
- Score = `base + bonus`, bonus = `corr_of(gating reading)` capped at 3.
- ELIM kills unfired bids (PRE_FAIL) and fired bids with empty staged
  answers (GATE); every bid stages a fallback answer, so in practice
  only PRE_FAIL fires. Readings are never eliminated by ELIM.

### 2.4 Ledger layout

25 rows × 552 bytes from offset 4 (`led_sz()` = 13820).
Row fields: hid@0 kind@4 status@8 bid@12 base@16 bonus@20 score@24
reason@28 detail@32 ev_kind@36 ev_score@40 fid@44 gate@48
content@68..552.
Rows 0–9: readings (kind=0). Rows 10–12: fact candidates (kind=1;
top-3 KB facts by keyword overlap, null candidates get fid=−1,
gate=1). Rows 13–24: action bids (kind=2).
Turn fields: fact-winner@13804, fact-close@13808, act-close@13812,
FORK@13816 (the ledger-driven fork flag).

### 2.5 Fork, verdict

`fork_assess`: FORK=1 iff `nread >= 2` AND the top-two score margin
among fired, alive bids is ≤ 12. Scores are base+bonus (@24).
Skipped entirely in single mode.

A **verdict** = the winning bid hid from the final ARGMAX
(highest score; ties break to the lower hid). **NO_VERDICT** if every
bid is annihilated (no alive fired bid at ARGMAX).

## 3. What "conscious every step" means (testable definition)

The fork decision, the sub-deliberations, the audits, and the
reintegration must EACH be explicit deliberation over ledger state —
not a hardcoded transform — satisfying all four:

1. **Ledger-read**: the stage's inputs are ledger rows/fields only
   (citing row hids and field offsets); no side-channel inputs.
2. **White-box trace**: the stage emits a trace record stating what
   was considered (candidate rows), what was decided, and why
   (which ledger facts bore on the decision).
3. **Neuter-causal**: suppressing the stage's deliberation (replacing
   its output with a null/default while holding everything else
   fixed) changes outcomes on the frozen set. A stage whose
   neutering changes nothing is decorative, not deliberation.
4. **Audit scope**: audits may write only eliminations
   (status=1) and fact invalidations to the shared ledger — the same
   write vocabulary round 1 used. Round 2 changes the invalidation
   POLICY (§4), not the vocabulary.

## 4. Least-disruptive invalidation (the principle under test)

When an audit invalidates, it denies the **least-relevant alive fact
candidate**; ties broken by **fewest dependent bids**. Stated
generally over the ledger's fact × bid dependency graph — NOT as a
p02-specific rule:

- **Relevance** of a fact candidate = its bearing on the live
  question: keyword/topic overlap with the query's evidence-bearing
  readings (the same overlap machinery GEN uses), lowest first.
- **Dependent bids** of a fact candidate = fired, alive bids whose
  staged support (`fid@44` / `fact` field) points at that candidate.
- The audit denies exactly one fact candidate per invalidation step
  (the minimum that resolves the inconsistency the audit found),
  then re-derives dependent bid states from the surviving ledger —
  it never pre-kills bids whose support survives.

This is the V4-class fix for round 1's annihilation finding. It is a
general policy over (fact candidates × fired bids), applicable to any
problem, not a patch for p02.

## 5. Kill bars (ALL must pass; any failure kills or voids as noted)

| ID | Bar | Falsification test | Verdict if failed |
|----|-----|-------------------|-------------------|
| K1' | Accuracy benefit from the channel | One-brain accuracy ≤ single-deliberation accuracy on the frozen v5 set, OR the shared-writes-off ablation matches/exceeds one-brain accuracy | KILL H1' |
| K2' | Causal cross-talk | Poison test: invalidating a shared fact candidate mid-deliberation does NOT change other branches' bids/eliminations | KILL H1' |
| K3' | TNN's own decision | Scaffold-removal: minimal driver, no fan_out call; machinery does NOT fan out on fork-worthy problems | VOID (not TNN's decision) |
| K4' | Trace causality | Neutering any stage's deliberation trace (fork, subpass, audit, reintegration) changes NOTHING on the set | KILL the "conscious" claim for that stage |
| K5' | Determinism | Any two of 3 reruns differ at the byte level (SHA-256) | VOID the evidence |
| K6' | No RNG | Grep + audit finds RNG use in any decision path | VOID the evidence |

K1' note (unchanged from round 1): the bar is deliberately
conjunctive — beating single deliberation alone is not enough; the
shared-writes-off ablation must also score below one-brain, proving
the gain rides the shared-state channel rather than extra passes.

K4' note: this is the teeth of §3. Each of the four stages
(fork decision, sub-deliberations, audits, reintegration) is
neutered independently; a stage that can be neutered with zero
outcome change on all 44 problems was never deliberating.

## 6. NO-TUNING RULE (load-bearing)

- The v5 set is frozen (SHA-256 + UTC timestamp in FREEZE.txt)
  BEFORE the implementer runs any scoring run on it — onebrain,
  ablate, poison, or min modes.
- The implementer develops on the v4 set only.
- The prereg author (Worker A) validated candidate items against the
  SPEC (fork-firable: ≥2 ev=1 readings; close action-bid margins)
  using the round-1 binary's probe behavior in `single` mode ONLY.
  That is spec validation, not tuning: single mode never forks and
  its outputs were never used to adjust expected bids.
- Expected bids come from human judgment + written rationales, never
  from running machinery. (Single-mode winners were observed only
  to calibrate difficulty AFTER the freeze — see CALIBRATION2.md —
  and no item was edited on the basis of any score.)

## 7. Scoring protocol

- Accuracy: onebrain vs single-deliberation vs shared-writes-off
  ablation, per problem and aggregate, on frozen v5.
- Report every problem where one-brain does NOT win, per problem,
  with the ledger trace.
- Determinism: 3× reruns, SHA-256 of full outputs, byte-identical.
- RNG audit: grep for RNG syscalls/library calls in decision paths
  + source audit of the v2 implementation.
- Verdicts are bid hids (§2.5); NO_VERDICT counts as wrong for
  accuracy (it is a failure to produce the judged deliverable).

## 8. Non-goals

- This prereg does not specify the V4 implementation's internals
  (Worker B owns those); it specifies the principle (§4), the
  output space (§2), and the bars (§5).
- v5 has 44 single-turn problems; multi-turn deliberation is out
  of scope for round 2.
- The 12-fact KB is unchanged from round 1 (frozen in the
  implementation); v5 entities are drawn from it, plus
  KB-absent entities only where the judged-correct bid is
  withhold-by-absence (J-category).
