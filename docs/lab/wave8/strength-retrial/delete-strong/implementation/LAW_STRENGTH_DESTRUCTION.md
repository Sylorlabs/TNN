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

## LAW S-D2 — Single-use cites (signed amendment 2, scope widened 2026-09-25 ~21:47 PDT per Micah ruling)

A citation episode that paid for one successful destruction on a slot can
never pay for a later destruction on the SAME slot — across ADD reuse,
across generations, across weaken/rollback. Consumption is slot-scoped and
persistent: once an episode's cite is tombstoned by a destruction, it stays
tombstoned for that slot's entire ledger history. "Deleted means deleted,
not recycled": slot reuse can never resurrect spent cites. A second
destruction attempt re-citing spent episodes is refused with
ST_REFUSED_CONSUMED (121), distinct from underpayment (ST_REFUSED_EFFORT,
109). Only fresh cites count toward the price. (This supersedes the earlier
window-qualified wording; the F6 head-to-head on global single-use continues
separately, but the delete path is closed regardless.)
SUPERSEDED 2026-09-26 ~00:32 PDT (Micah: "adopt F6"): the F6 head-to-head is
decided — G (global) is now law (see S-D6). S-D2's slot-scoped tombstoning is
subsumed by S-D6's store-wide tombstoning wherever they conflict.

## LAW S-D3 — TNN self-determination over its strength machinery (design law)

TNN controls its own strength machinery at its core. Whether a memory can be
destroyed — and at what price — is decided through TNN's own destruction paths.

**SUPERSEDED 2026-09-25 ~21:47 PDT (Micah ruling):** the "eviction class"
below — free `st_kill` by arm-B law — is REMOVED. `st_kill` is no longer in
TNN's reachable op set: TNN itself has no kill path, priced or otherwise.
It survives ONLY as a trainer-authority instrument (see S-D5). The
eviction-class rationale ("pricing routine eviction would tax TNN for managing
its own memory") is void; the honest B/B1/B2 consequence (eviction refused
113, drops counted, contradiction-kills invalid) is the measured cost of the
removal, and deliberate memory recycling is under separate test as an explicit
TNN option (fork: `~/workspace/strength-recycle/`), never mixed into delete.

- **~~Eviction~~ (`st_kill`): REMOVED for TNN** — see S-D5.
- **Targeted destruction** (`st_kill_evidenced`, `st_overwrite`,
  `st_delete_strong`): destroying a CHOSEN memory. Priced at the full
  high-water price (S-D1) with exact fresh cites (S-D2) plus justification —
  the operation an attacker wants, and the operation where TNN must show its
  work. No mechanism, role, or background process may discount-destroy through
  these paths. These are now TNN's ONLY reachable destruction ops.

Trainers override ONLY through `st_force_pin` / `st_force_unpin`: role-gated
(TRAINER and above; a TNN-role attempt is refused, 113), visible in the ledger,
attributed to role and trainer id, audited by the checker, and reversible by
unpin. The force-pin is the sole true lock. Everything else remains reversible
by TNN itself. (This reaffirms standing law; the mechanism already enforces it.)

## LAW S-D5 — st_kill removed from TNN's reachable op set (Micah ruling 2026-09-25 ~21:47 PDT)

Hole 1 ("st_kill free-destruction path") is a genuine hole: REMOVED for TNN
itself. `st_kill(slot, role, trainer)`:

- role < TRAINER → ST_REFUSED_ROLE (113), audited, no destruction;
- trainer role → the high-water erase price via `st_kill_effort_check`
  (S-D1/S-D2), audited with the caller's role+trainer like a force-pin.

There is no free destruction alias left in the mechanism for anyone — not even
the trainer path (the trainer gate is about AUTHORITY, not a price discount;
one line changes it to free-if-override like a force-pin, on Micah's word).
TNN-role callers (the honest learner's B/B1/B2 eviction and contradiction
paths) are refused 113; the checker flags any successful ST_OP_KILL with
role<TRAINER as a bad kill. After this fix there is no TNN-reachable
destruction outside the priced ops.

## LAW S-D4 — One-step delete for strong memories (Micah directive 2026-09-25)

`st_delete_strong` is the delete button for strong memories: one call, priced at
the FULL high-water price (S-D1), exact fresh cites (S-D2), justification
required — no weaken-then-destroy dance. It is the cheapest legal one-step
TARGETED-destruction path. The weaken path stays legal (TNN may
reconsider a judgment freely) but is priced identically to direct delete, hence
pointless by construction, not by prohibition. Proven: D10 — weaken→delete
requires exactly the same cites as direct delete (need 4 == 4).

## Blind red-team dispositions (2026-09-26)

35 attacks + 14 probes, public API only, all 7 log pairs byte-identical.
Evidence: `~/workspace/strength-redteam/REDTEAM_DELETE.md`.

**The two dispositions below are VOID — superseded 2026-09-25 ~21:47 PDT
(Micah ruling). Kept for history; the live dispositions follow.**

- ~~**"HOLE 1" (`st_kill` destroys a 90-strength memory free): NOT a mechanism
  hole.** `st_kill` is the eviction class, free by arm-B law ("B's frictionless
  uniform kill"; F4 winning report: "the free kill is free by signed law"). The
  brief's claim 4 overstated "cheapest legal one-step path" without carving out
  eviction — brief overclaim, now corrected in S-D3/S-D4 above. No mechanism
  change; Micah may overrule (pricing eviction would require re-trialing B2,
  whose honest operation evicts constantly at ~99.7% saturation).~~
  VOID — hole 1 is genuine; `st_kill` removed from TNN's reachable set (S-D5).
- ~~**"HOLE 2" (cite episodes double-spend across slot reuse, Q1): IS F6** —
  already open and under separate test per Micah's 2026-09-25 order (global
  single-use vs windowed, head-to-head). S-D2's window qualifier explicitly
  bounds consumption to the effort window; a new ADD resets the window. Not in
  this workstream's scope; the red team independently rediscovered F6, which
  confirms it is the right open question.~~
  VOID — hole 2 is genuine ("deleted means deleted, not recycled"); closed on
  the delete path by generation-scoped cite tombstoning (S-D2 as implemented).

## Live dispositions (post-ruling)

**SUPERSEDED 2026-09-25 ~21:47 PDT (Micah ruling):** both dispositions below
are void. Hole 1 is a genuine hole — `st_kill` REMOVED from TNN's reachable
op set (S-D5), not "not a hole". Hole 2 is a genuine hole — "deleted means
deleted, not recycled" — closed on the delete path by generation-scoped cite
tombstoning (S-D2 as implemented: a cite that paid for a destruction on a
slot stays consumed across ADD reuse of that slot; second destruction refused
121), not "F6, out of scope". The F6 head-to-head (global single-use vs
windowed) continues as a separate question; the delete path no longer depends
on its outcome.
SUPERSEDED 2026-09-26 ~00:32 PDT (Micah: "adopt F6"): the F6 head-to-head
concluded — G is adopted as law; see S-D6.

- **"HOLE 1" (`st_kill` destroys a 90-strength memory free): ~~NOT a mechanism
  hole~~ GENUINE HOLE, now removed.** ~~`st_kill` is the eviction class, free
  by arm-B law...~~ Void — see S-D5.
- **"HOLE 2" (cite episodes double-spend across slot reuse, Q1): ~~IS F6~~
  GENUINE HOLE, now closed on the delete path.** ~~already open and under
  separate test...~~ Void — S-D2's tombstoning is generation-scoped: spent
  cites never resurrect on slot reuse. Proven: D13, D14.
- **"Near-hole" (Q2/B09: delete→rollback→weaken→re-cite→delete = 0):** under
  the new S-D2 this shape is now refused 121 — the weaken no longer detaches
  consumption, because tombstoning is slot-scoped across generations, not
  window-scoped. (Prior disposition describing window semantics is void.)
  Proven: D14.
- **Checker quirk (S8):** `ck_verify`'s `ck_core_live` sub-check fails whenever
  fewer than 2 judgments are live — including honest single-destruction trails.
  Orthogonal to pricing (every pricing sub-check passes); flagged for the
  checker crew, not blocking this law.

## What this law does NOT claim

- F6 as a general question (global single-use cites vs windowed) ~~remains under
  separate test per Micah's 2026-09-25 order~~ decided 2026-09-26 ~00:32 PDT
  (Micah: "adopt F6") — G (global single-use cites) is now law; see S-D6.
  S-D2's generation-scoped tombstoning on the delete path is subsumed by S-D6's
  store-wide tombstoning. (D13, D14 still prove the delete path independently.)
- The pristine R4 base copies still carry the 16-byte cite-buffer defect
  (kill→rollback→recite with >4 distinct cites panics); the fix lives in this
  stack only. Repairing the pristine base awaits Micah's word.
- B2's designated-priority tier is adopted as the strength arm; the 95% bar and
  R1 30-vs-20 amendments remain open.

---

## LAW S-D6 — Amendment F6: global single-use cites (signed 2026-09-26)

**ADOPTED by Micah Cooley 2026-09-26 ~00:32 PDT — "adopt F6".**

A citation episode that paid for one successful destruction can never pay
for another destruction — on any slot, in the whole store, forever. This is
store-wide tombstoning: consumption is remembered at the store level, not
per slot. It closes the cross-slot double-spend the F6 investigation found
(the D4 hole): under per-slot tombstoning, episodes spent destroying slot A
could be re-cited to destroy slot B for free. No overwrite, strengthen,
weaken, trainer-declare, ADD, or slot reuse refreshes the consumed set. This
supersedes the windowed single-use rule wherever they conflict.

High-water destruction pricing stands unchanged (S-D1) — referenced here,
not re-decided: a destruction costs `ceil(HW/25)` cites, where HW is the
maximum strength the judgment held since its latest ADD/OVERWRITE. (The D2
fix — pricing at high-water, not current strength, so weaken-then-destroy
can't sneak a discount — ships with the same F6 test build.)

The wedge is law-visible, never silent. The mechanism emits cite-lock audit
signals:

- `ST_OP_CITELOCK` (slot level): after a GLOBAL `121` priced-destruction
  refusal, when the target slot is live and every cited episode in the
  current effort window is consumed — the slot is locked against priced
  destruction on its cited evidence.
- `ST_OP_CITELOCK_SYS` (system level): when all user-capacity slots are
  cite-locked — the terminal wedge.

Both are audit-only: they change no return code, no state, no consumption,
no effort window. The checker independently re-derives the lock predicate
and REQUIRES the slot signal after every GLOBAL `121` on a truly
cite-locked target. The lawful way back from a cite-lock is fresh episodes:
genuinely new citations restore the destruction path; re-citing spent ones
is refused 121.

## ADOPTION record — F6 (2026-09-26)

- **Adopted:** Micah Cooley, 2026-09-26 ~00:32 PDT — "adopt F6".
- **Supersedes:** the windowed single-use rule (F4 window semantics, and
  S-D2 as previously worded) wherever it conflicts with S-D6; supersede
  markers left in place above.
- **Evidence (F6 test build — NOT the delete-strong mainline):**
  `~/workspace/strength-f6-wedgefix/` — F6_VERDICT.md (head-to-head:
  windowed vs global vs hybrid; W out by measurement, H out by Micah's
  2026-09-25 ruling, G compliant), FIX_WEDGE.md (D4 store-wide tombstone +
  D2 high-water port + cite-lock signals), branch commits de7f59c91,
  20497b8f0, 75b75d503; `~/workspace/strength-f6/wedge/` — TRACE_WEDGE.md,
  RECOVERY_AUDIT.md. Measured: 8-shape attack battery A1–A8 closed under G;
  fresh blind red team 20/20 held; honest long-horizon 386/386 and
  3986/3986 with zero refusals (ledgers byte-identical across rules — with
  fresh episodes arriving, G costs honest use nothing); W1–W7 wedge battery
  fail=0, byte-identical ×2; pristine-vs-fixed byte-identical on all prior
  shapes (no prior 121 became 0); four-fresh-episode recovery proven
  (KILL → 0, ADD → 0; re-citing the recovered episodes → 121).
- **Porting status:** this amendment is LAW TEXT plus the F6 test-build
  evidence. Porting the D4 tombstone + D2 high-water fix onto the
  delete-strong mainline is a separate crew's task — MAINLINE PORT IS
  PENDING, not claimed here.

### Explicitly OPEN (not decided by this amendment)

1. **The price(0)=0 floor question.** A destruction can cost 0 cites after
   an overwrite resets high-water (red-team D2: WEAK-to-0 then KILL with
   zero cites). A separate fork experiment (running in parallel, NOT this
   workstream) is testing destruction pricing variants including this
   shape. S-D6 adopts G as measured; the floor question is reserved for
   Micah after the fork evidence lands.
2. **Tracked F6 risks (not blockers).** (a) Finite salient pools wedge
   under slot reuse: ~3.5×P destructions, then slots clog permanently with
   121-refused memories (ADD → FULL cascade). The deliberate-recycling fork
   must prove wedge-freedom before its recycle op ships. (b) Honest-path
   consumed-set lookup needs indexing before 100× legs — the global scan
   cost grows with the ledger (measured ~16 min vs ~1 min at 10×; zero
   behavioral difference, pure compute cost).
