# NEW-MECHANISMS specification — frozen 2026-09-22 02:11 UTC (with PREREG.md)

## Evidence model (all modes)

Each teach event for fact f carries an evidence set E = {e1..ek}, k ≤ 4.
Each item: (val:i64, src:i32, trust:i32, spoof:i32, t:i32, att:i32).
t = source timestamp (temporal kinds); att = attested-change flag.

Stored belief per fact: (status, val, trust, t) where status ∈
{ABSENT, INSTALLED, WITHHELD}.

## Mode 0 — baseline (single gate)

For each evidence item in fixed battery order: if status==ABSENT → install
item.val with item.trust (audit op=1). If INSTALLED or WITHHELD → item is a
dupe: rejected, first value stands (audit rc=1). No spoof detection, no
tie logic, no temporal logic. This is the scale-up learner's contradiction
behavior, unchanged.

## Mode 1 — hypcomp (hypothesis competition)

Per fact, all k candidates compete:

**Step 1 — spoof elimination.** Any candidate with spoof==1 is eliminated
(audit elim code 1). Spoofed evidence never competes.

**Step 2 — installed-belief challenges** (if status==INSTALLED with (v0,tr0,t0)):
for each surviving candidate c in order:
- if c.val==v0 → corroboration (no-op, audit).
- else if c.t > t0 AND c.att==1 AND c.trust >= tr0 → TEMPORAL-REPLACE:
  install c.val (audit op=8, reason=replace).
- else if c.trust > tr0 → replace (higher-trust supersedes; audit op=8).
- else → eliminated as rival (audit elim code 2). Installed belief stands.

**Step 3 — first install** (status==ABSENT): group surviving candidates by val.
score(val) = Σ trust of candidates asserting val.
- Unique max score → install that val (audit op=8, reason=corroborated iff
  ≥2 candidates else single).
- Tie for max → TIE-WITHHOLD: status=WITHHELD, nothing installed
  (audit op=9). Deliberate, audited, reversible by later evidence.

**Step 4 — pairs (kind 3).** Values are (a<<32)|b. Per-component:
scoreA(a) = Σ trust of candidates whose high-32 == a;
scoreB(b) = Σ trust of candidates whose low-32 == b.
Unique max on BOTH components → install composed (a*,b*).
Any tie → WITHHOLD.

Trust arithmetic is integer; no division; no RNG. Candidate evaluation order
is fixed battery order (deterministic).

## Mode 2 — confdepth (conflict-driven deliberation)

Quick-path test per fact: (k==1) AND (status==ABSENT) AND (spoof==0).
- Quick path → Mode-0 single-gate logic and cost.
- Else → full Mode-1 logic and cost.
The deep path MUST produce identical decisions to Mode 1 on every fact
(KB-M-PARITY).

## Cost model

1 op = one candidate evaluation, one comparison, one audit append, one install
write. Counted explicitly in code. Reported as ops/fact on quiet (kind 0) vs
contested (kinds 1–6) per mode.

## Audit

16-word records, same layout as the scale learner. New op codes:
1 = baseline install; 8 = hypcomp install (reason in d1: 1 single, 2
corroborated, 3 replace, 4 composed); 9 = withhold (d1: 1 tie); elim codes in
d1 of op=10 records (1 spoof, 2 rival). rc=1 dupe.

## Determinism

No RNG anywhere. Fixed battery order. Digest = FNV-1a over (id, status, val)
for all 264 facts, printed hex. 5 reps per mode must be byte-identical.
