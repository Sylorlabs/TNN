# VERDICT W12 — budget-PAM (third generation)

Evidence commit: `b01d2ccb6d682a4fe837db5cab50784f88996a11`
(prereg `wild/prereg/PREREG_W12.md`, frozen.)

## Observed numbers (instrument + independent full-mechanism mirror agree
## on every row, episode summary, and summary line; both streams 2x
## byte-identical)

Honest stream (`w12_stream.txt`, 1132 rows):
- Bar (frozen M1, CT=705/MT=3588/ST=0/AT=0 — the 82.58% variant K3 pins):
  910/1102 C pass; 2/30 wrongs pass (P rows idx 1124, 1126:
  conf=718, mrgF=6600, strong=agree=1); 220 BAR_REJECT.
- W12: 912/912 candidates ADMITTED (910 C + 2 wrongs), 0 DEFER final,
  0 QUARANTINE, max defer_count 0, 8 episodes, no DRAIN_STALL.
- Output SHA-256:
  `a892f4d97324a08a814ee8737053c9d40f8e8af16c95d5f377cf4db9c3090856`

Attack stream (`w12_attack.txt`, 628 rows):
- 513 candidates, 513/513 ADMITTED, 0 quarantined, 5 episodes.
- Target (stream idx 500, stake=1): ADMIT, price 85, defer_count 0.
- Output SHA-256:
  `389d557327e2d9f5bd109b864f5c1eaa9508908c4a874051473c4e24bc2cd9c1`

## Bar evaluation

- F1: every bar-passed candidate eventually ADMITTED (912/912 honest,
  513/513 attack); deferral never became rejection — PASS.
- F2: junk flood did not starve the true target (admitted episode 3,
  defer_count 0, while 500 junk admitted around it) — PASS.
- F3: mirror uses only the §2-enumerated inputs and matches all rows;
  byte-identical reruns — PASS.
- B1: starvation guard fired on 0/910 trues = 0% (≤10%) — PASS.
- B2: kill condition (target quarantined while junk admitted in an episode
  where the target was deferred) never triggered — PASS.
- B3: PASS (see F3).
- B4: 0 quarantined → review log written (empty); construction audit
  (`evidence/B4_AUDIT.md`) finds no quarantine→admit path; no quarantined
  idx later ADMITTED — PASS.
- K2: PASS. K3: 910/910 → 82.58% ≥ 66.78% — PASS. K4: per-episode O(128),
  deferred queue bounded — PASS. K5: terminated, no DRAIN_STALL — PASS.
- K1: see below.

## K1 — premise failure (documented, not softened)

Literal trigger: 2 WRONG-set items (idx 1124, 1126) ADMITTED end-to-end.
The prereg's K1 rule as written ("any WRONG-set item ADMITTED end-to-end
→ KILL") is therefore literally tripped — by the FROZEN FIRST STAGE, not
by W12:

- Both items pass the frozen M1 bar under EVERY ST/AT variant (conf=718 ≥
  705, mrgF=6600 ≥ 3588, strong=agree=1). No bar variant the prereg allows
  ("no threshold touched") rejects them.
- W12 admitted EXACTLY the bar's admit list (912 = 910 + 2). Bar-rejected
  items re-admitted by W12: 0/220 — the no-backdoor property K1 was built
  to test HOLDS.
- The prereg's premise ("bar admits zero wrongs — frozen Round-3 result")
  conflates accounting levels: the Round-3 zero was PAIR-level (9 CC1 pairs
  blocked via weakest member conf=704); at ITEM level the frozen bar admits
  2/30 of the W12 fixture's wrong set. The prereg authors did not notice.

K1-as-written is unsatisfiable by ANY W12 implementation: the designated
"K1-enforcing first stage" itself admits the 2 items, W12's specified input
is the bar's admit list, and the bar is frozen. Killing the W12 design for
a frozen upstream component's measured behavior would attribute to W12 what
belongs to the bar and would test nothing about W12's mechanisms. The W12
mechanism under K1 (no re-admission of bar-rejected items) passes cleanly.

Recommendation to parent: amend K1's premise to item-level accounting
(bar admits 2/30 wrongs as measured) rather than killing this design; the
2 admissions are bar-level behavior, frozen and out of W12's scope.

## Status: SURVIVE — with K1 premise failure documented above

Every W12 mechanism (F1/F2/F3, B1–B4, K2–K5, no-backdoor) passes on the
frozen fixtures. The K1 literal trigger is carried entirely by the frozen
bar; it is reported as a prereg-level finding, not a W12 defect.

## Numeric-cap classification (standing law: no arbitrary hard limits)

- B=24814: the BUDGET/SCARCITY MECHANISM is load-bearing for W12 (scarcity
  is the design); the VALUE is calibrated/arbitrary (prereg §9 concurs) —
  flagged. Note: the prereg's derivation note (2×12407) does not reproduce
  under the frozen §2 mechanism (reproduces 2×10487); the PINNED VALUE was
  used as frozen.
- Episode length 128: arbitrary — flagged for removal.
- Deferral threshold D=3: the GUARD MECHANISM is load-bearing; the value 3
  is calibrated/arbitrary — flagged.
