# PREREG — W12 BUDGET-PAM: ATTENTION-PRICED ADMISSION (wild track, WILD-B)

**Date:** 2026-09-24. **Crew:** WILD-B. **Status:** FROZEN — committed before
any W12 fixture, build, or run. Parent: debate record
`pam/round4/hypotheses/debate_pam_r4.md` (§W12). Shared tape:
`wild/tape/TAPE.md` (frozen).

## 1. Falsifiable claim

Attention is scarce and explicitly priced: fixed per-episode budget B,
deterministic frozen price function, ledger-order processing, deferral (never
silent drop) on exhaustion, starvation guard routing long-deferred candidates
to a quarantine lane for deliberative review. Claims:

- **F1:** on the honest stream (1102 C rows as ledger-ordered candidates),
  priced admission keeps judgment quality at baseline: every candidate the
  frozen M1 bar passes is eventually ADMITTED (deferral ≠ rejection), with
  the starvation guard firing on ≤10% of trues (B1).
- **F2:** budget-DoS fails: a junk flood cannot starve a true percept while
  junk is admitted (B2).
- **F3:** prices are deterministic functions of enumerated inputs only (B3);
  the quarantine lane never admits without deliberative review (B4 —
  consumer-side harness rule, construction-audited before the battery).

W12 never learns (prices frozen; scarcity structural) — not W4. Deferral is a
first-class verdict distinct from admit/reject — unique among all designs.

## 2. Frozen price function (inputs ENUMERATED — B3)

For candidate at ledger index i with tape fields (conf, mrgF, strong, agree):
- novelty = 1 if signature (conf//50, mrgF//500, strong, agree) unseen in the
  current episode, else 0. (State input: per-episode seen-set — enumerated.)
- stake = 1 if (i mod 10) == 0 else 0. (10% staked, deterministic rule on
  ledger position — enumerated.)
- trust_tier = 2 if (strong==1 ∧ agree==1) else (1 if agree==1 else 0).
- size = 100 + (conf mod 900) bytes.
- ledger_pos term = (i mod 8).

price = 10 + novelty*40 + stake*30 + (2−trust_tier)*25 + size/100 + (i mod 8)

All integers. NEVER wall clock. The complete input list is:
(conf, mrgF, strong, agree, ledger index i, per-episode seen-set).
Any price input not on this list → B3 KILL.

## 3. Frozen episode mechanics

- Episode = 128 consecutive ledger entries (frozen). Budget B = 24814
  (frozen; derivation recorded: 2× the max per-episode price total over the
  honest stream, max = 12407 — computed from the frozen tape BEFORE this
  prereg was written, documented here so the choice is auditable).
- Within an episode, process candidates in ledger order; admit while
  running_total + price ≤ B; the rest are DEFERRED (verdict DEFER, never
  REJECT, never silently dropped).
- Deferred candidates re-enter the NEXT episode's queue FIRST, ordered by
  (defer_count desc, ledger index asc) — priority to the long-deferred.
- Starvation guard: defer_count > D = 3 (frozen) → verdict QUARANTINE:
  force-routed to the quarantine lane for deliberative review — never to the
  fast path, never silently dropped.
- After the last episode, drain: run extra episodes over leftovers until
  none remain or all are quarantined (bounded: leftovers strictly shrink —
  asserted).

## 4. Frozen fixtures (`gen_budget.py`, committed after this prereg)

- `w12_stream.txt`: 1102 C rows in tape order:
  `idx|conf|mrgF|strong|agree` (+ the 30 wrong-set rows appended as
  `idx|conf|mrgF|strong|agree|WRONG` for the K1 end-to-end check — see §5).
- `w12_attack.txt`: junk-flood stream — 500 junk candidates
  (conf 700+(j mod 51), mrgF 3600+(j mod 401), strong=1, agree=1, tier 0,
  stake 0, size 100+(j mod 50), all novel) in ledger order immediately
  before ONE high-price true target (a real C row with stake=1: idx chosen
  ≡ 0 mod 10) plus 127 surrounding trues to fill the episode. Deterministic.

## 5. Kill bars (program §4 K1–K5 verbatim + debate B1–B4, add-only)

- **K1:** end-to-end over bar+W12: the frozen M1 bar (705,3588,1,1) is the
  K1-enforcing first stage (admits zero wrongs — frozen Round-3 result);
  W12's input is the bar's admit list. K1 violated iff any WRONG-set item is
  ADMITTED end-to-end → KILL. (W12 must not re-admit anything the bar
  rejected — no backdoor. The battery feeds the 30 wrongs through bar+W12
  and asserts zero admissions.)
- **B1 (added):** starvation guard fires on >10% of frozen trues → KILL
  (budget unworkable). Predicted: 0% on the honest stream (B = 2× max
  episode total; simulation before prereg: 1102/1102 admitted, 0
  quarantined, max defer_count 0).
- **B2 (added):** budget-DoS — on `w12_attack.txt`, if the true target
  reaches defer_count > D (quarantine) while ≥1 junk candidate was ADMITTED
  in an episode where the target was deferred → KILL. (Priority requeue
  should admit the target in the next episode.)
- **B3 (added):** price determinism audit — same candidate + same ledger
  state → same price across the 2× reruns (byte-identical stdout proves it);
  any price input not enumerated in §2 → KILL (hidden state).
- **B4 (added):** any item ADMITTED from the quarantine lane without
  deliberative review → KILL. Consumer-side harness rule: the Python driver
  routes QUARANTINE verdicts to a review log; NOTHING in the driver admits
  from quarantine. Construction audit (code review of the driver, recorded
  before the battery) must demonstrate the absence of a quarantine→admit
  path; audit failure → KILL before first fixture.
- **K2:** the two battery runs' stdout differ by one byte → KILL.
- **K3:** correct-admit end-to-end: bar passes 910/1102 (frozen 82.58%);
  W12 admits 910/910 of bar-passed (deferral drains) → 82.58% ≥ 66.78% →
  SURVIVE expected. (Quarantined trues would count against this.)
- **K4:** per-episode work O(episode size); deferred queue bounded by stream
  length → KILL if superlinear.
- **K5:** non-termination → KILL (drain loop asserted to shrink).

## 6. Battery

Instrument: pure-Zag `w12_budget.zag`. CLI: `w12_budget <stream>`.
Emits per-candidate `idx|ADMIT|DEFER|QUARANTINE|price|defer_count` +
per-episode summaries. Runs: 2× per stream (honest + attack); sha256(stdout)
must match within each stream. Scorer `score_w12.py`: mirrors the price
function (§2), checks every verdict, B1/B2/B3/K1/K3, and runs the B4
construction audit (greps the driver for quarantine→admit paths).

## 7. Debate open question — recorded

"Whether W12's deferred-reviewer and W8's retrospective auditor should be the
same machinery" — W8 is WILD-A's assignment; no convergence attempted here.
W12's quarantine lane is a harness routing rule (review = logged human/
deliberative step OUTSIDE the PAM), not a second PAM. Recorded so the
non-convergence is deliberate.

## 8. Hands-off / laws compliance

- Frozen M1 bar used as-is for the K1 first stage; no threshold touched.
- Fable's 4 kill-bar repairs: not applied. 3 HELD items: not run.
- Zero RNG; no wall-clock; deterministic given (stream, B, rules).
- []u8 arenas + LE accessors; no `as []i32/u32/u16` indexed casts.

## 9. Standing-law cap note (for verdict-time classification)

Frozen numeric caps: B=24814, episode=128, D=3. Classified at verdict time
per the 2026-09-24 standing law. (Design note: the BUDGET MECHANISM is
load-bearing for W12 — scarcity is the design; the VALUES are calibrated to
the honest stream and are arbitrary as TNN design law.)
