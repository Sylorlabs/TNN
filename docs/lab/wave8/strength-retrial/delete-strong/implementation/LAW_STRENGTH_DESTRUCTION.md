# Strength destruction law — signed amendments + self-determination design law

**Status:** LAW (signed by Micah Cooley 2026-09-25 ~21:15 PDT, plain-English round).
**Implements:** `st_delete_strong` (ST_OP_DELETE_STRONG=20) in `strength_core.zag`
(SHA 5b2397f1…), verified by `ck_verify_delete` in `strength_checker.zag`
(SHA c0143d2b…).
**Evidence:** `~/workspace/strength-delete/` — MERGE_REPORT.md, del_attack D1–D11,
f1/f2/f4 re-verification batteries, blind red-team report.

## LAW S-D1 — High-water erase pricing (signed amendment 1)

Destroying a judgment costs `n(HW)` cites, where HW is the maximum strength the
judgment has held since its birth (its ADD, or the last OVERWRITE that replaced
it), and `n(s) = 0` for `s ≤ 0`, else `(s+24)/25`. The mechanism
(`st_kill_effort_check`) and the checker (`ck_verify_kill`, `ck_verify_overwrite`,
`ck_verify_delete`) compute HW with one shared function — they cannot drift apart.

Lowering the strength first — by weaken, by downward strengthen, by
trainer-declare-downward, by any relabeling — never reduces the price.
Weakening stays a free judgment re-declaration; only destruction is priced.

## LAW S-D2 — Single-use cites (signed amendment 2)

A citation episode that paid for one successful destruction cannot pay for a
later destruction on the same slot while the first destruction remains in the
later operation's effort window. Reuse is refused with ST_REFUSED_CONSUMED (121),
distinct from underpayment (ST_REFUSED_EFFORT, 109). Only fresh cites count
toward the price.

## LAW S-D3 — TNN self-determination over its strength machinery (design law)

TNN controls its own strength machinery at its core. Whether a memory can be
destroyed — and at what price — is decided through TNN's own destruction paths,
which come in two classes:

- **Eviction** (`st_kill`): TNN's own memory management. Free by arm-B law
  ("B's frictionless uniform kill") — no cites, no justification — because it
  is TNN's policy choosing victims (lowest score first), not a targeted hit.
  It is audited (ST_OP_KILL), rollbackable, respects pin/force-pin/core-region,
  and its drops of important memories are measured by the P2 tripwire
  (drop ceiling), not priced. Pricing routine eviction would tax TNN for
  managing its own memory and halt the store at saturation.
- **Targeted destruction** (`st_kill_evidenced`, `st_overwrite`,
  `st_delete_strong`): destroying a CHOSEN memory. Priced at the full
  high-water price (S-D1) with exact fresh cites (S-D2) plus justification —
  the operation an attacker wants, and the operation where TNN must show its
  work. No mechanism, role, or background process may discount-destroy through
  these paths.

Trainers override ONLY through `st_force_pin` / `st_force_unpin`: role-gated
(TRAINER and above; a TNN-role attempt is refused, 113), visible in the ledger,
attributed to role and trainer id, audited by the checker, and reversible by
unpin. The force-pin is the sole true lock. Everything else remains reversible
by TNN itself. (This reaffirms standing law; the mechanism already enforces it.)

## LAW S-D4 — One-step delete for strong memories (Micah directive 2026-09-25)

`st_delete_strong` is the delete button for strong memories: one call, priced at
the FULL high-water price (S-D1), exact fresh cites (S-D2), justification
required — no weaken-then-destroy dance. It is the cheapest legal one-step
TARGETED-destruction path. (`st_kill` is cheaper but is the eviction class, not
targeted destruction — see S-D3.) The weaken path stays legal (TNN may
reconsider a judgment freely) but is priced identically to direct delete, hence
pointless by construction, not by prohibition. Proven: D10 — weaken→delete
requires exactly the same cites as direct delete (need 4 == 4).

## Blind red-team dispositions (2026-09-26)

35 attacks + 14 probes, public API only, all 7 log pairs byte-identical.
Evidence: `~/workspace/strength-redteam/REDTEAM_DELETE.md`.

- **"HOLE 1" (`st_kill` destroys a 90-strength memory free): NOT a mechanism
  hole.** `st_kill` is the eviction class, free by arm-B law ("B's frictionless
  uniform kill"; F4 winning report: "the free kill is free by signed law"). The
  brief's claim 4 overstated "cheapest legal one-step path" without carving out
  eviction — brief overclaim, now corrected in S-D3/S-D4 above. No mechanism
  change; Micah may overrule (pricing eviction would require re-trialing B2,
  whose honest operation evicts constantly at ~99.7% saturation).
- **"HOLE 2" (cite episodes double-spend across slot reuse, Q1): IS F6** —
  already open and under separate test per Micah's 2026-09-25 order (global
  single-use vs windowed, head-to-head). S-D2's window qualifier explicitly
  bounds consumption to the effort window; a new ADD resets the window. Not in
  this workstream's scope; the red team independently rediscovered F6, which
  confirms it is the right open question.
- **"Near-hole" (Q2/B09: delete→rollback→weaken→re-cite→delete = 0): CORRECT
  per the signed window rule, not a hole.** The weaken between rollback and
  re-cite is a strength-write: it becomes the new effort-window start (lss),
  detaching the old cites (established R1 semantics) and the old consumption
  (first destruction outside the new window). The second delete paid with 4
  cites inside the new window. D4 (no weaken) correctly refused with 121. The
  report's "S5 — rollback refunds cites" is a misattribution: the weaken, not
  the rollback, did the work (rollback of evidence/justify/refused ops is
  itself refused, 108). Epoch-reset consumption is F6 territory.
- **Checker quirk (S8):** `ck_verify`'s `ck_core_live` sub-check fails whenever
  fewer than 2 judgments are live — including honest single-destruction trails.
  Orthogonal to pricing (every pricing sub-check passes); flagged for the
  checker crew, not blocking this law.

## What this law does NOT claim

- F6 (cite reuse across an overwrite-reset effort window) is NOT closed by S-D2;
  it is under separate test per Micah's 2026-09-25 order (global single-use vs
  windowed, head-to-head).
- The pristine R4 base copies still carry the 16-byte cite-buffer defect
  (kill→rollback→recite with >4 distinct cites panics); the fix lives in this
  stack only. Repairing the pristine base awaits Micah's word.
- B2's designated-priority tier is adopted as the strength arm; the 95% bar and
  R1 30-vs-20 amendments remain open.
