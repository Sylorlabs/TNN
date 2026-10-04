# PINS DECISION BRIEF — for Micah

**Question:** Should the old learner-side `pins_add` be deprecated and routed
through the new trainer-only `fp_pin`, or kept?

**Your semantic ruling (authoritative, settles the "what is it" question):**
> "The learner can make something hard to remove but it can never make it
> permanently locked. Only a trainer or external force can do that — in
> training, and they can in production too, like if a user ran /force on TNN."

So: learner pins = strength/importance (high erase cost, NEVER permanent,
always reversible). Trainer `fp_pin` = true permanent lock. This brief
evaluates the *mechanics* against your ruling. **It does not make the call.**

---

## 1. What the debate covered

Three positions were steelmanned by separate agents, each grounded in
file:line citations (full arguments in `~/workspace/pins-htd/debate_{A,B,C}.md`):

- **A — Deprecate/route.** `pins_add` (`store.zag:149-157`) takes no caller
  id, writes no audit record, and lives on the learner's own struct — any
  learner-side code can self-pin. The dual live paths in `delib.zag:700-712`
  (old `pins_check` AND new `fp_check`, both feeding `R_R2`) let an
  unauthenticated pin produce a constitutional-looking refusal.
- **B — Keep as-is.** Two stores already coexist by design (`delib.zag:84`:
  `pins` + `fpins` side by side); the strength-trial core keeps separate
  `pinned` (learner reversible judgment) vs `forcepin` (trainer lock)
  bitfields; learner pinning is deliberate-agency machinery. Routing would
  turn legitimate learner pins into audited "refused forgery" entries.
- **C — Keep both, clarify.** The confusion is a documentation failure, not
  a mechanism failure. Formally separate: `Pins` = learner judgment markers
  (reversible, audited as learner action), `FPStore` = constitutional lock.
  Document a precedence rule.

**Important:** all three debated *before* your ruling. The tests below were
run/aimed *at* your ruling.

---

## 2. Test evidence (all pure Zag, no RNG, byte-identical reruns)

### Test 1 — Semantic gap (84 checks, 8 blocks, all pass)
`pins_add` and `fp_pin` are NOT interchangeable. `pins_add` can silently
succeed with no audit, no span validation, duplicate appends, and **no
unpin path exists — pins are permanent in practice** (`n` monotonically
nondecreasing). `fp_pin` refuses non-trainer callers (101), binds trainer
ids, and audits every attempt including refusals. Routing is NOT a drop-in
swap: 4 behavior changes (duplicate handling, span validation, full-table
code, owner-undoability). (`~/workspace/pins-htd/test1_semantic_gap.md`)

### Test 2 — Self-lock probe (NO violation on erase, 2 residual defects)
The learner **cannot** block a trainer erase via `pins_add` — `dlb_retract`
(`delib.zag:542`) consults only the trainer-gated `FPStore`. Erase of a
pinned span succeeds. BUT: (D1) old pins are an **unaudited,
trainer-irremovable proposal veto** — a `pins_add`-pinned span rejects new
proposals with `R_R2` and zero force-pin-ledger activity; (D2) from the DLB
ledger alone, an overseer **cannot distinguish** an old-pin refusal from a
force-pin refusal. (`~/workspace/pins-htd/test2_selflock.md`)

### Test 3 — Migration breakage (routing is NOT viable as a drop-in)
`pins_add` has **exactly one call site** in the live tree:
`tests/test_pins.zag:30` (test code; zero learner-side callers). Routing it
through `fp_pin` with learner identity → 101-refused, pin never set,
**protection silently disarmed while the suite still reports 5/5 PASS**.
Worse: `test_pins.zag` is **vacuous** — it never actually exercises the pin
mechanism (hits a pre-check at `delib.zag:651` first). Verdict: don't
"route" — either keep or deprecate fully. (`~/workspace/pins-htd/test3_migration.md`)

### Test 4 — Audit-trail comparison (old path fails every overseer question)
`pins_add` writes **zero audit records** (ledger delta = 0). Same pin action
compared side-by-side: old path — who set it? *unanswerable*; trainer vs
self-imposed? *unanswerable*; new path — d1=caller, d2=trainer id, every
attempt including forged ones audited. (`~/workspace/pins-htd/test4_audit.md`)

### Test 5 — Compliance vs YOUR ruling (all three VIOLATION)
- **Q1 "hard to remove"? → VIOLATION.** `dlb_retract` never consults
  `pins_check`; retract of pinned vs unpinned span is bit-identical. No
  erase-cost symbol exists anywhere in the learner tree. The pin's only
  effect is vetoing *new proposals* — which your ruling doesn't sanction.
- **Q2 "never permanent"? → VIOLATION.** Zero removal symbols repo-wide;
  `fp_unpin` returns 103/101 on old pins (disjoint registry); the only
  "clear" is destroying the whole deliberator. The proposal veto is
  **de-facto permanent in-session**.
- **Q3 "trainer supremacy"? → VIOLATION.** Trainer cannot clear (103) or
  override the veto; a pin **survives its own content's erasure** — trainer
  erases the memory, the pin persists, and re-proposals are vetoed forever.
  (`~/workspace/pins-htd/test5_compliance.md`)

---

## 3. Options against your ruling

| Option | What it does | Cost | Honors ruling? |
|---|---|---|---|
| **1. Deprecate fully** | Delete `pins_add`; rewrite the one test call site as trainer `fp_pin`; fix `test_pins.zag`'s vacuous pattern | Small, measured (Test 3: zero behavioral delta on the trainer path) | Yes — removes the violating mechanism |
| **2. Repair into real strength** | Rebuild learner pins as what your ruling describes: erase-cost linkage + unpin path + audit as learner action + trainer override | New mechanism work (design + build + verify); the strength-trial `pinned` bitfield is the closest existing model | Yes — implements the learner half properly |
| **3. Route as drop-in** | Mechanical `pins_add` → `fp_pin` swap | **Dead** (Test 3: silently disarms protection, suite stays green) | N/A — doesn't work |
| **4. Keep as-is** | Do nothing | Zero now; keeps all three violations live | **No** — fails Q1, Q2, Q3 |

Note on Position C ("keep both, clarify"): documentation alone cannot fix
this. Your ruling requires the learner mechanism to *do* two things it
currently does not do (erase-cost effect; reversibility). Clarifying names
without changing behavior would bless a violating implementation.

Note on Position B's best point: the *concept* of learner-side strength
marking is legitimate under your ruling — it just doesn't exist yet in the
learner. Option 2 is where that concept would live.

---

## 4. Where the evidence leans (not a decision)

The current `pins_add` implements **neither half** of your ruling: it does
not make removal hard (no erase-cost linkage at all), and it *is* de-facto
permanent (no unpin path, trainer cannot clear it, it survives erasure).
Against your semantics, keeping it as-is is not defensible, and routing it
as a drop-in is empirically broken.

That leaves **deprecate-now** (small, clean, measured zero-delta) versus
**repair-into-real-strength** (builds the learner half of your ruling
properly, but it's new work, not a cleanup). The evidence supports
deprecating now regardless — a future strength mechanism should be designed
deliberately, not inherited from a veto that was never what your ruling
describes.

**The call is yours:** deprecate now, repair into strength, or repair on a
schedule after deprecation.

---

## 5. Provenance

- Debate + tests: 8 agents, HTD flow, 2026-09-21.
- Working papers: `~/workspace/pins-htd/` (debate_A/B/C.md, test1–test5 md).
- Test sources: `~/workspace/pins-htd/test1_gap.zag`,
  `units/teachers/learner/tests/test_selflock_probe.zag`,
  `units/teachers/learner/tests/test4_audit.zag`,
  `units/teachers/learner/tests/test5_compliance.zag`,
  plus migration probes under `~/workspace/pins-htd/work/`.
- No binaries or `.zag-cache` committed; test sources only.
- This brief is a decision input, not a verdict. Frozen prereg changes (if
  any follow) need dated Micah-approved amendments per standing law.
