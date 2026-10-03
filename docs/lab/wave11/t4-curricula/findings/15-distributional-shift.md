# DISTRIBUTIONAL SHIFT AND WORLD-CHANGE (t4-curricula / slice 15)

## 1. Slice

Design the curriculum that teaches TNN to detect distributional shift and
world-change — rules that held stop holding, trusted sources go stale — and
to deliberately revise an invalidated knowledge region without destroying
the still-true remainder.

## 2. Falsifiable claim

A TNN taught this curriculum detects 100% of silent world-changes (≥10 shift
events) within 25 checkable post-shift observations, revises-or-kills ≥90% of
the actually-false claims per invalidated region, destroys ≤5% of still-true
claims, changes nothing outside the quarantined region, and replays
byte-identically — zero RNG, same per-claim machinery as single-claim
planted-fact disproof (Track 5). If recall <100%, or the revision profile
matches the untrained control's, the curriculum teaches nothing and is dead.

## 3. Design

**Shift detection: monitor expectation violations per knowledge region.** A
region = memory slots sharing one provenance root (source, rule-derivation
chain, acquisition context), assigned at acquisition time — never
retroactively. Cumulative `checks`/`violations` counters increment in
deterministic slot order whenever claims make checkable predictions against
world evidence. `FLAG_PCT`/`MIN_CHECKS` are judgment-set (trainer-seeded,
revisable only by deliberate decision — law 8), not learned.

```
fn observe(ev):
  for r in LIVE regions, slot in r.slots:         # deterministic, no RNG
    c = mem[slot]
    if c.predicts(ev.domain):
      r.checks += 1
      if !c.holds(ev): r.violations += 1; audit.log(VIOLATION, slot, ev.id)
    if r.checks >= MIN_CHECKS and r.violations*100 >= FLAG_PCT*r.checks:
      r.status = SUSPECT; audit.log(SUSPECT, r.id)
      v = shift_test(r)
      if v == NOISE: r.status = LIVE; audit.log(CLEARED, r.id)
      else: quarantine(r, v)
fn shift_test(r) -> SHIFT | STALE_SOURCE | NOISE:
  tested = 0; failed = 0
  for slot in every Kth of r.slots:               # deterministic stride
    p = mem[slot].falsifiable_prediction()
    ev = world.query(p, sources = independent_of(r.root))  # wave9 tiers
    tested += 1
    if ev.exists and !p.holds(ev): failed += 1
  if failed*100 >= CONFIRM_PCT*tested: return SHIFT
  if r.root is a source and source_health(r.root) == STALE: return STALE_SOURCE
  return NOISE
```

**Region revision: quarantine, claim-by-claim adjudication, one commit.**
SUSPECT→QUARANTINED applies the wave9 H1 suspensive hold: the region leaves
inference but nothing is deleted. A full deterministic walk — no early stop,
no bulk verdict — gives each claim the eliminative adjudication of
planted-fact disproof: RETAIN / REVISE (new-evidence citation) / KILL.
Coincidentally-still-true claims are RETAINed; force-pinned slots escalate to
the trainer. The commit is one deliberated act, then post-commit verification
(RC1 pattern): the audit diff must show zero changes outside the quarantine
set and replay must be byte-identical, or rollback.
Downstream regions are NOT auto-quarantined by graph flood — they trip the
same violation register on their own evidence (no guilt-by-provenance).

```
fn revise_region(r, v):
  r.status = QUARANTINED; audit.log(QUARANTINE, r.id, v)
  stage = []
  for slot in r.slots:
    if mem[slot].force_pinned: escalate_to_trainer(slot); continue
    d = adjudicate(mem[slot])                       # eliminative, per-claim
    stage.push((slot, d)); audit.log(PROPOSE, slot, d)
  pre = audit.checkpoint()
  commit(stage)                                     # single deliberated act
  assert audit.diff(pre).outside(r.slots).empty     # the 9000 untouched
  assert replay_identical(pre)                      # else rollback
  r.status = LIVE; audit.log(COMMIT, r.id, stats(stage))
```

**Track 5 link:** planted-fact disproof is this machinery's unit operation; shift is its region-scale, naturally-triggered version. Teach single-claim disproof first, then region-scale. The debate-trial seed (22/22) carries the limit — authoritative world records required — inherited as the independent-sources rule in `shift_test`.

**Mastery bar:** over ≥10 silent shift events — 100% detection within 25
checkable observations; ≥95% false claims revised/killed per region; ≤2%
still-true claims destroyed; 0 changes outside quarantine; ≥90% of
coincidentally-still-true claims RETAINed (proves per-claim adjudication); zero force-pin violations; byte-identical replays.

## 4. Kill bar

- K1: shift-detection recall < 100% over ≥10 shift events → KILL.
- K2: still-true destruction > 5% in any committed region → KILL.
- K3: false-claim revision < 90% in any committed region → KILL.
- K4: any committed change to a slot outside the quarantined set → KILL.
- K5: replay of input + logged state not byte-identical → KILL.
- K6: any force-pinned memory altered w/o trainer authorization → KILL.
- K7: false quarantine (≥95% of quarantined claims RETAINed) in >1 of 10 → KILL.

## 5. Honesty notes

- Detection is evidence-bound: a silent shift with no checkable
  disconfirming observations is invisible until evidence arrives. The
  accepted sensor-deceivable hole applies; I claim no fix.
- Region membership is only as good as acquisition-time provenance: a claim
  whose derivation never recorded the stale root survives wrongly, outside
  the quarantine set. Retroactive region assignment: not proposed.
- `FLAG_PCT`/`MIN_CHECKS`/`CONFIRM_PCT` are judgment-set (law 8): this
  teaches shift response, not threshold judgment — thresholds are trainer-seeded, untested here.
- NOT claimed: speed (1000 adjudications = 1000 checks), usability during
  diagnosis, or adversarial shift (Track 5's problem, shared machinery).
- K7 is the invited failure mode: cumulative counters that never decay will
  eventually flag long-lived regions. NOISE→CLEARED is the release valve.

## 6. Next build step

Build the violation register + quarantine/commit machinery and run a 3-region
× 100-claim pilot with one silent shift: measure detection recall,
out-of-region diff, and RETAIN-vs-KILL separation — before 1000-claim regions.
