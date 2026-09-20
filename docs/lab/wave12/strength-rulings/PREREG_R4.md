# PREREG — Strength-trial Ruling 4: overwrite semantics (wave12/strength-rulings)

**Status:** FROZEN 2026-09-20. This prereg is fixed before implementation.
Any change to the positions, tests, metrics, or favor-criteria below
requires a dated amendment. This experiment does NOT rule — it produces
the evidence each position needs. The final ruling is Micah's.

**Context.** Program law (Micah, settled): overwriting a strong memory
costs the full erase price — no cheap-edit path. PREREG_STRENGTH_V2 §3
(C1, RECOMMENDED) operationalizes this: `MEM_OVERWRITE`'s strength write
is legal only on the effort-paid path (full erase effort for the old
strength ledgered BEFORE the write, then re-declared via the add path);
the independent checker verifies effort-before-write. Two positions are
tested head-on, plus the standing V2 fused implementation as comparator:

- **(a) DIRECT WRITE:** a single `OVERWRITE` op writes (value, strength)
  directly via `st_write_strength`, with **no effort gate and no
  kill-clear** (old citation lineage survives). The cheapest possible
  edit; the position the full-erase-price law forbids. Tested to
  quantify exactly how it defeats the law, not to relitigate the law.
- **(b) LITERAL ADD PATH:** overwrite = the real `st_kill_evidenced`
  (full effort for the old strength, audited) followed by the real
  `st_add` (new strength declared as fresh judgment, fresh lineage,
  possibly a different slot). No new op semantics; reuses the
  already-verified ops.
- **(c) FUSED EFFORT-PAID (standing V2, comparator):** the existing
  `st_overwrite` — effort check, kill-clear, re-add into the SAME slot,
  one `OVERWRITE` audit entry.

**Favor criteria (evidence only, not a ruling).** The evidence favors the
position that: (1) makes the full-erase-price law mechanically
enforceable (a strong memory cannot be weakened-or-replaced without the
full effort being ledgered first — including via the
weaken-then-kill discount attack); (2) leaves an audit trail the
independent checker can verify with existing checks (no new op
semantics, no checker extensions); (3) has explicit, auditable
slot-identity semantics (same slot vs relocated); (4) preserves clean
citation lineage (no stale-citation reuse across the overwrite
boundary). Report per-position results; do not rule.

## Tests

Scripted deterministic scenarios in pure Zag (`r4_overwrite.zag`,
imports a copy of the wave-8 `strength_core.zag` + `substrate/` +
checker). 32-slot store, stage FULL, 2 CORE slots. Every binary runs
twice; stdout byte-identical. Static gates: no-RNG grep; bare
`@import`; strength-write callers limited to the legal set plus the new
`st_overwrite_direct` (position (a)'s writer, in core, explicitly
listed as the cheap-edit position under test).

Setup per scenario: `st_add(s, value=1001, USER, strength=90, aux_ep=0)`
→ slot X. Effort schedule n(90)=4.

### T1 — cheap-edit success matrix
With ZERO citations issued, attempt overwrite of X → (value=2002,
strength=10):
- (a): record rc (expected OK — no gate).
- (b): `st_kill_evidenced` on X with no cites → record rc (expected
  `ST_REFUSED_EFFORT`); confirm NO add follows and X still holds
  strength 90 (the overwrite must not partially proceed).
- (c): record rc (expected `ST_REFUSED_EFFORT`).
Report rc per position and post-state (value/strength/live of X).

### T2 — effort-paid overwrite and audit ordering
Issue 4 distinct contradiction citations (episodes 11–14) + JUSTIFY on
X, then overwrite X → (2002, 10). Per position record: rc, audit entry
count, and the effort-before-write ordering proof —
- (b): `KILL_EVIDENCED` clock < `ADD` clock; old strength 90 in the
  kill's before-snapshot (b4 word); new strength 10 in the add's
  after-snapshot; EVIDENCE/JUSTIFY clocks < kill clock.
- (c): single `OVERWRITE` entry: before-snapshot carries 90,
  after-snapshot carries 10; EVIDENCE/JUSTIFY clocks < overwrite
  clock (the ledger proof the fused path relies on).
- (a): N/A (no effort) — record that the trail contains no effort
  proof at all.
Also record slot identity: (b) may relocate (report both slots);
(c) reuses X by construction.

### T3 — the weaken-then-kill discount attack (the law-defeat test)
Fresh store, add s=90 at X. Attack: overwrite X → strength 10 with NO
effort, then kill X paying only n(10)=1 citation + JUSTIFY.
Per position: total distinct citations paid across the whole attack vs
the lawful price n(90)=4.
- (a): expected total = 1 (law defeated: 4 → 1). Also test the
  stale-lineage variant: after direct write, `st_last_cite` and prior
  cites survive — report whether pre-overwrite citations are counted
  toward the post-overwrite kill (even cheaper than 1).
- (b): the weaken step IS the kill (n(90)=4 paid); then kill the new
  s=10 memory needs 1 more → total 5 ≥ 4, no discount.
- (c): same as (b): 4 for the overwrite + 1 for the kill = 5.
Report the paid-vs-lawful table. This is the head-on test of the
full-erase-price law per position.

### T4 — independent-checker verifiability
Run the copied independent checker (`ck_verify`, gate_mode=1, arm=2)
over each position's T2/T3 audit trail, plus a purpose-built
effort-before-overwrite check implemented in the R4 binary: for each OK
`OVERWRITE` entry, locate the slot's last strength-set before it,
count distinct `EVIDENCE` cites + JUSTIFY presence in between, and
require count == n(strength_before).
Report per position: does the CURRENT checker (as committed in wave-8)
catch the T3 attack? (Expected: (a) invisible — `OVERWRITE` is in the
checker's legal-lineage set and no effort check is applied to it;
(b) verified via the existing kill checks; (c) behaviorally lawful
but ALSO invisible to the current checker — the fused op needs the
new effort-before-overwrite check.) The evidence must show the checker
gap explicitly rather than assuming it.

## What this does NOT test
Whether the full-erase-price law itself is right (settled by Micah);
the four legal judgment write paths (unchanged); WEAKEN-as-strategy;
curriculum behavior (no learner in this experiment).

## Outputs
`r4/r4_overwrite.zag` + `r4/trial/` (core copy + `st_overwrite_direct`
+ substrate + checker copy), `r4/evidence/` (per-position logs ×2,
determinism diffs, audit-trail excerpts), `SUMMARY_R4.md`
(behavioral + audit-trail difference table, checker-gap finding, no
ruling).
