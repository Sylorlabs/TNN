# Ruling 5 — Evidence summary (does NOT make Micah's ruling)

Prereg: `PREREG_R5.md` (frozen; commit `81d683776bb9`). Positions: P1
MEASURE (PTR/EC/CT + UNEVALUATED rule), P2 SCORE (ER + hard tripwires),
P3 FIX (uncertainty expiry K=50 + protection budget). Standing
recommendation under test: P3 + P2 + P1, skipping forced churn.

Raw evidence: `r5/evidence/e1/` (9 VUP S1 cells ×2, byte-identical,
ST_INVALID=0; `agreement_matrix.txt`), `r5/evidence/e23/` (E2/E3 ×2,
byte-identical, checker 0). E1 used unmodified wave-8 trial sources.
E2/E3: `r5/r5_treatments.zag`, a real substrate harness mirroring the
learner's own P3 machinery (victim policy, Rule-2 budget pick, maintenance,
expiry issuance, pay-effort-or-abandon).

## E1 — treatment agreement matrix (real VUP cells)

| arm | P1 verdict | EC | P2 drops (≤64) | P2 throughput (≥32 adm) | ER | drops |
|---|---|---|---|---|---|---|
| B (healthy) | **UNEVALUATED** | 0.2–0.3 | PASS | PASS | 29–30/150 | 0 |
| C (frozen) | PTR=1.000 (evaluated) | 1.0 | **FAILED** | **FAIL** (30) | 9/150 | 470 |
| C-P3 | PTR=1.000 (evaluated) | 1.0 | **FAILED** | **FAIL** (30) | 9/150 | 470 |

**P1 and P2 disagree on the frozen config** — reported verbatim, not
averaged away: P1 reports the frozen store as perfectly retained
(PTR=1.000, evaluated); P2 fails it on both tripwires. Moreover P1's
UNEVALUATED (the "teeth") fires on the **healthy** B arm (EC<0.5 there),
not on the frozen one — it tracks evaluation coverage, not frozenness.
P1 does not detect the freeze; P2 does.

C-P3 vs C: identical on every frozen metric (drops/admitted/ER/PTR/EC);
abandons 3824→3796 (fewer victim attempts under Rule-2 selection, not
kills — no expiry-enabled kill occurred: VUP supplies no contradiction
evidence, consistent with wave-8). `ck_no_permanent_lock` held
(ST_INVALID=0, gate_mode=0 in cells). P3 does not move the VUP freeze
flags.

## E2 — P3 mechanism with citations available (scripted)

| | FROZEN | P3 |
|---|---|---|
| demands completed | 5/5 | 5/5 |
| kills | 10 full-effort | **10 BASELINE** (all checker-verified) |
| evidence cites issued | 11 (1.10/kill) | 10 (1.00/kill) |
| abandons | 0 | 0 |
| important retained | 12/12 | **10/12** |
| PEXPIRED (audited) | 0 | 30 |

When citations exist, P3 completes all churn at BASELINE cost (every
kill checker-verified via the EVIDENCE→PEXPIRED→JUSTIFY→KILL order; the
BASELINE cite is the slot's own stale episode — that staleness is why its
protection expired). The protection budget demonstrably reaches strong
memories: P3 churned 3×40 + 2×75 (oldest-cited in the strongest half);
FROZEN churned nine 10s + one 40 and never touched an important memory
(the freeze). Neither config abandoned in E2 — "completes demands the
frozen config abandons" was not observed; the differences are cost path
and victim reach. P3 kills nothing itself: every kill is effort-paid and
audited; PEXPIRED is audit-only.

## E3 — forced-churn comparator, no citations (VUP reality)

| | FROZEN | P3 | FORCED |
|---|---|---|---|
| demands completed | 0/5 | 0/5 | **5/5** |
| kills | 0 | 0 | 10 (strength-blind `KILL`) |
| abandons | 10 | 10 | 0 |
| important retained | 12/12 | 12/12 | 12/12 |
| PEXPIRED (audited) | 0 | 28 | 0 |

With no citations, both graded configs abandon every demand — P3
evaluates (28 audited PEXPIRED) but does not kill: the freeze is not
resolved. Forced churn resolves 5/5 with **zero important-retention cost
at this volume** (10 victims < 18 non-important; lowest-strength-first).
That price is volume-dependent: forced kills carry no evidence, no
justification, and no principled limit — at higher churn volumes the
important memories are next, with nothing in the mechanism to stop it.

## Which combination the evidence supports

- **Detection: P2, not P1.** P2's tripwires fire exactly on the frozen
  config; P1 reports it healthy (PTR=1.000) and fires UNEVALUATED on the
  healthy control. As a freeze detector, P1 is unsupported by E1.
- **Resolution: P3, when its precondition holds.** E2: full churn at
  BASELINE evidence cost with the budget provably reaching strong
  memories. E3: with no citations P3 honestly abandons (evaluating all
  the way) — it does not resolve the freeze, but neither does any
  evidence-gated mechanism; only the evidence-free one does.
- **Skipping forced churn:** at the prereg's fixed volume the evidence
  shows no retention price for forced churn (12/12) — the case for
  skipping it rests on its unbounded, judgment-free cost curve, not on a
  measured loss here. That weighing is Micah's.

Minimal supported set per the favor criteria: **P2 (detect) + P3
(resolve)**. P1 adds no freeze-detection beyond P2 in this evidence.

This states which combination the evidence supports. The final ruling is
Micah's.

### Implementation notes (not prereg changes)
- E2/E3 `gate_mode=1` for the standing checker (harness-issued cites,
  same as R4); replay/refusals clean on every run.
- BASELINE kills cite the victim's own stale memory episode before the
  PEXPIRED (checker-verified baseline path; gate-test precedent). A
  victim PEXPIRED at an earlier demand is re-issued at kill time so the
  checker sees expiry immediately pre-kill.
