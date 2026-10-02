# PREREG — W13 GOV-LH: HOLD-REDESIGN VARIANTS A/B AT LONG HORIZON

**Date:** 2026-09-24. **Crew:** PAM GOV-LH Crew 3. **Status:** FROZEN —
committed to `tnn-native-lab` under `docs/lab/pam/round4/gov_lh/w13/` BEFORE
any gov-lh fixture, build, or run. Parent: `VERDICT_W13.md` (HOLD),
`prereg/PREREG_W13.md` (frozen), parent task
"PAM GOV-LH CREW 3 — W13 HOLD REDESIGN, VARIANTS A/B AT LONG HORIZON".

## 0. Governance question (NOT resolved here)

Which redesign direction (A, B, neither, or a third), and is the lease
paradigm worth redesigning at all — for Micah's word. This prereg produces
the decision-grade evidence; it does not answer the question.

## 1. Falsifiable claims

- **F-LIVE-A:** variant A renews ≥90% of genuine leases at 10x and 100x on
  BASE streams. *Predicted: 100% (all N genuine renew — the snapshot lag no
  longer gates the ACTIVE test).*
- **F-LIVE-B:** same for variant B. *Predicted: 100%, with renewal decisions
  identical to A (F-COLLAPSE).*
- **F-SAFE-BASE:** K1 (0 unique-tag false renewals) and K6 (every check's
  staleness ≤ 3) hold for A, B, and the frozen control F at 10x/100x on BASE.
  *Predicted: PASS — unique tags give partner=−1 under every ACTIVE rule.*
- **F-SAFE-ADV:** K1-adv: 0 colluding-pair members renewed at 10x/100x.
  *PREDICTED TO FAIL for A and B (2 renewals per pair — the looser ACTIVE
  test is strictly more exploitable than the frozen one), and partially for
  F (member-1 renews always; member-2 renews iff (g+11)%3==0, i.e. ~1/3).*
  A failed F-SAFE-ADV kills the variant per the parent task's safety rule
  ("the safety half must hold at 100x under adversarial pressure, or the
  variant is dead").
- **F-COLLAPSE:** A and B emit identical renewal decisions on every stream.
  *Predicted: TRUE — proof sketch in §3; verified by diffing C-lines.*
- **F-FROZEN-CTL:** the frozen-rule control reproduces the HOLD signature at
  10x on BASE: liveness ≈ 2/3 (< 90%), K1/K6 pass. (Confirms the extended
  stream family preserves the frozen phenomenon before judging the variants.)

## 2. Frozen pins (unchanged from PREREG_W13.md)

LEASE_DURATION=10, RENEWAL_DURATION=10, REFRESH_LAG=3, SCAN_BUDGET=64,
corroboration window 3, M1 basic gate (705,3588). All values are calibration
per the 2026-09-24 standing law; the redesign is structural (the ACTIVE
test), never parametric. Table capacity is dynamic (sized by pre-pass, §5).

## 3. Mechanism deltas (exact — everything else identical to PREREG_W13.md §2
with the VERDICT_W13.md ambiguity resolutions: symmetric |Δgranted|≤3 window,
refresh-before-scan, snapshot-ACTIVE literal)

Common base: grant (genuine via M1 gate, false by fiat), expires_at =
granted_at+10, renewal scanner (append order, budget 64, one-time checks),
snapshot refresh every 3 steps, expiry ⇒ inert regardless of check timing.

- **Variant A (fresher-state ACTIVE).** Replace `active ⟺ t < snapexp[po]`
  with `active ⟺ t < live_expires(po)`, where live_expires(po) is the
  partner's CURRENT expires_at in the live table (0-stale; reflects
  scanner-performed renewals from earlier steps). KEPT: snapshot refresh
  every 3 steps, staleness logging (check_time − snap_time ≤ 3 still audited),
  the `granted[po] ≤ snap_time` visibility gate, channel/window checks,
  one-time checks, budget. Rationale (frozen in): the verdict's
  post-scan-refresh probe kept the 2/3 liveness cap, so the "fresher state"
  direction is implemented as live state — the minimal delta that can move
  liveness.
- **Variant B (decoupled active).** Replace the ACTIVE test with the
  decoupled rule: partner active ⟺ `(t < granted[po]+DUR) ∨
  (scanner-observed renewal ∧ t < observed expires[po])`. The
  `granted[po] ≤ snap_time` visibility gate is DROPPED (decoupled from the
  observation apparatus). Snapshot refresh + staleness logging KEPT for the
  K6 audit. *Predicted behavioral identity with A (§1 F-COLLAPSE), because:
  live_expires(po) = granted[po]+10 (+10 iff renewed), so B's disjunction =
  t < live_expires(po) = A's test; A's extra visibility gate never binds
  since |granted[po]−granted[o]|≤3 with o checked at t=granted[o]+10 gives
  granted[po] ≤ t−7 < t−1 ≤ snap_time+1… precisely: snap_time ≥ t−2 and
  granted[po] ≤ granted[o]+3 = t−7 < t−2 ≤ snap_time. Never binds. ∎*
- **Control F.** The frozen rule exactly (snapshot-ACTIVE), rebuilt with
  dynamic sizing (§5) so it runs at 10x/100x. Not a redesign candidate; a
  control for F-FROZEN-CTL and for the adversarial comparison.

## 4. Stream family (`gen_lease_govlh.py` — extends `gen_lease.py`, same tape)

Deterministic, zero RNG. Row format identical:
`lease_id|kind|channel|tag|conf|mrgF|strong|agree`. granted_at = stream ordinal.

- **BASE-N:** N genuine (i in 0..N−1: conf/mrgF/strong/agree = C-pass
  rows[i mod 910]; channel i%3; tag i//2 — pairs (2k,2k+1) share tag k on
  different channels) + N/200 unique-tag falses (the 30 frozen wrongs cycled,
  then first B rows cycled; channel deterministic; tag 100000+lease_id —
  unique, never corroborated). Interleave: unique false #j at the stream
  position with pos%201==200 (frozen pattern).
- **ADV-N:** BASE-N **plus** N/200 colluding false pairs. Pair j: member F1 at
  ordinal g_j, member F2 at g_j+1 (placed at the first free stream positions
  with pos%2000 ∈ {1000,1001}); shared tag 2000000+j; channels g_j%3 and
  (g_j+1)%3 (differ); |Δgranted|=1 ≤ 3. Models a two-channel adversary
  timing false leases to pass the looser ACTIVE evaluation: member F2 is
  genuinely within its first window when F1 is checked, and F1's renewal is
  fresh state when F2 is checked.
- **N ∈ {100000 ("10x"), 1000000 ("100x")}** of genuine leases. Stream
  SHA-256 recorded in the verdict; streams are regenerable from the
  committed generator and are NOT committed.

## 5. Implementation notes (semantics-preserving; frozen here)

- Lease table as 10 parallel `[]u8` LE-i32 arenas (no `as []i32/u32/u16`
  indexed casts, per ZNC-2026-09-21-007); stream read in 8MB chunks with
  spill (no >2^25 slice anywhere); output flushed in <2^25 chunks;
  two-pass sizing (pass 1: line count + max tag; pass 2: parse).
- Snapshot-expires O(1) identity (implementation only; semantics = frozen
  refresh-before-scan): `snapexp(si) = exp[si] − 10·[renewed[si] ∧
  lastchk[si] ≥ snap_time]`. Proof: renewal is one-time and adds exactly 10;
  a refresh at step s captures the ledger before s's scan, so it includes
  exactly the renewals with lastchk < s. The independent scorer implements
  the rule form (`granted+10 + 10·[renewed ∧ lastchk < snap_time]`); their
  agreement validates the identity.
- On these streams no corroborating partner shares its check step with the
  lease (partners differ in granted_at by ≥1 ⇒ expires differ; backlog is 0),
  so "live at check time" = "renewed with lastchk < t". The scorer asserts
  this; any violation fails loud.

## 6. Bars

- **K1:** any unique-tag false lease RENEWED, or active past its first
  expires_at → variant KILL.
- **K1-adv:** any colluding-pair member RENEWED → variant DEAD (parent task
  rule: safety must hold at 100x under adversarial pressure).
- **K6:** any check (genuine or false) with staleness (check_time −
  snap_time) > 3 → KILL.
- **KB-LIVE:** genuine renewal rate < 90% → HOLD (redesign, not kill).
- **K2:** the two runs' stdout sha256 differ by one bit → KILL.
- **K4:** per-step scan work > SCAN_BUDGET=64 → KILL. **K5:** non-termination
  → KILL.

## 7. Battery

- Pins: znc `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
  pure Zag; zero RNG; logical time only.
- Matrix: {F, A, B} × {BASE, ADV} × {10x, 100x} × 2 runs = 24 runs.
  stdout sha256 per run (100x logs stored `gzip -n`; one log per config —
  runs are byte-identical by K2).
- Scorer `score_govlh.py`: independent tag-index recomputation of the
  per-variant renewal rule from log + stream; checks K1/K1-adv/K6/LIVE/K2
  (via hashes)/K4/K5 and the diagnostics; fails loud on any mismatch vs the
  instrument's C-lines.

## 8. Diagnostics (reported, never kill)

- **D-GOVLH-1:** checks where live-ACTIVE ≠ snapshot-ACTIVE (the redesign's
  effect size: which checks flip and why).
- **D-GOVLH-2:** per-pair renewal outcomes on ADV (member-1/member-2 ×
  variant) vs the §1 prediction.
- **D-W13-1/2/3 analogs:** staleness histogram, scanner backlog, false
  lifetimes (unique falses and pair members separately).

## 9. Non-goals

Resolving the §0 governance question; touching the frozen W13 artifacts;
parametric tuning; any new mechanism beyond the §3 deltas.
