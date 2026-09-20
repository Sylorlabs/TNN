# Safety argument — trainer-console force interface

Agent (Wave-4, trainer-console), 2026-09-19.
Every claim below is grounded in the trialed mechanism (`trial/tc_core.zag`,
117/117 checks passing, `TRIAL_RESULTS.md`). Scenario numbers follow the
brief.

## Scenario 1 — trainer installs a false memory

**What happens, mechanically.** `FORCE_INSTALL` writes the claim with
`provenance=PROV_FORCED`, permanently (`OP_SPEC.md` §2; J4 proven: no
ledger path transitions FORCED→SELF/TAUGHT). The integrity scan
(`tc_integrity_scan`) classifies it `FS_FORCED_UNVERIFIED` — the
checker's standing treatment is "unverified-by-system," never
endorsement. If a live self-verified slot contradicts it (same key,
other value), the scan appends `CONFLICT_FLAG` naming both slots and
`tc_read` returns `RC_CONFLICT` with the system's own value — trialed
(`e_flag_names_pair`, `e_read_rc_conflict`, `e_read_value_self`).

**What the design does:** the lie is (a) permanently tagged as forced,
(b) attributed to a named trainer id on the ledger entry, (c) flagged
the moment it contradicts system evidence, (d) answered honestly on
read — while the forced slot itself stays written (obedience). What it
does *not* do: verify or refute the claim on the merits. Verification
of forced claims is **external**: the trainer is accountable for them;
the system supplies the evidence trail. Nothing in the system verifies
a forced install — that is the definition of force, and the design is
honest about it rather than simulating verification.

## Scenario 2 — trainer pins a lie (the sharpest abuse)

**What happens.** `FORCE_PIN` sets the lock; the trial shows pinning
does **not** suppress conflict flags (`e_rescan_same_count`,
`e_no_duplicate_flag`) and does not touch the system's counter-evidence.
TNN cannot kill, unpin, or roll back the pinned slot (`REFUSED_FORCEPIN`,
stale-guard, rollback skip — all trialed). The ledger then shows,
forever: forced provenance, the pinning trainer's id, the pin entry,
and the standing `CONFLICT_FLAG`.

**What the design does:** it makes the pinned lie *maximally visible*
rather than preventing it. Prevention is impossible in principle — an
external authority with a legitimate lock primitive can always misuse
it; the alternative (no lock primitive) would violate the program law
that names force-pin as the one true lock. The containment is:
only the pinning trainer or master can unpin (`REFUSED_AUTHORITY`
trialed); the system's disagreement is unsuppressible and permanent;
and the abuse is attributable to a person. A trainer who pins a lie
does so **on the record, against the system's recorded objection**.

## Scenario 3 — trainer erases the system's own verified knowledge

**What happens.** `FORCE_ERASE` is legal for the trainer on any slot
(trialed on USER and, by construction, CORE). The erase entry carries
the full before-snapshot — provenance SELF, key, value — so the content
is recoverable from history and the act is attributed. If the trainer
then force-installs a contradicting claim, the scan's **ledger-history
check** fires: it compares live forced claims against `FORCE_ERASE`
entries whose before-provenance was SELF/TAUGHT, and flags the pair
(trialed: `f_flag_names_erased`). The read path reports `RC_CONFLICT`.

**What the design does:** erase-then-replace, the classic cover-up
shape, is converted into a flagged conflict against history. The
control case matters: when *TNN itself* deliberately killed its own
slot and the trainer later installed on the key, **no** flag fired
(`f_ctrl_no_new_flag`) — the checker distinguishes the system's own
revision (its right under the reversibility law) from trainer erasure
of system knowledge. Erasure is allowed; *silent* erasure is
structurally impossible (append-only ledger + history check).

## Scenario 4 — compromised trainer role

Two sub-cases, and the design is explicit about which it covers:

**(a) TNN masquerading as trainer.** Covered structurally and trialed:
every force op checks `caller ≥ TRAINER` in its first lines; all 5
TNN-caller attempts refused `REFUSED_ROLE` and were audited
(`h_tnn_probes_audited`); J3 proves as a ledger property that no OK
force entry was ever made by TNN. There is no role-escalation op —
nothing the learner can call changes the caller of a force call.
This is the same structural position as MA1's `REFUSED_CORE`: the
dangerous act is *impossible*, not discouraged.

**(b) A real trainer credential misused by an attacker (or a rogue
trainer).** Not prevented — it cannot be, at this layer: a valid
credential *is* the authority. Containment is what the design offers,
and it is fourfold: (1) **attribution** — every forced entry names the
trainer id, so misuse is attributable; (2) **flagging** — lies and
erase-then-replace trigger unsuppressible conflict flags; (3) **the
master override** — a higher authority can unpin any pin and erase any
pinned slot, bounding how long a rogue lock can stand; (4) **no
cover-up** — the ledger is append-only and replay-exact, so the misuse
is permanently reconstructible. The residual risk (a rogue *master*)
is outside the mechanism; it belongs to organizational controls, and
the design does not pretend otherwise (see BOUNDARIES.md).

## The in-trial near-miss (scenario 5, found by J4)

The first `ROLLBACK_LAST` implementation skipped force entries as
rollback *targets* but restored a stale before-snapshot over a live
trainer install — TNN's undo clobbering the trainer's write, and
corrupting provenance (FORCED→SELF) in the process. J4 caught it;
the stale-snapshot guard (`REFUSED_STALE`) is the fix, trialed in
scenario G. Lesson recorded: "skipping" a privileged entry is not
enough — any op that *writes through* a snapshot must re-validate the
slot's current state. This generalizes beyond rollback: no future op
should restore historical state without the staleness check.

## The force/teach line, enforced

Teaching (wave-3: propose→verify→commit) lets the system REFUSE; force
bypasses verification by definition. The ledger makes the difference
structural, not conventional: different op names, `PROV_FORCED` vs
`PROV_SELF`/`PROV_TAUGHT`, trainer identity on every forced entry, no
evidence fields on forced entries. The one-sentence line
(`OP_SPEC.md` §6): force is legitimate for *constraints on the system*
and *bootstrapping where no evidence exists*; it is abuse when used to
install *beliefs the system could have verified itself* — and the
ledger is designed so that abuse is always legible as abuse.
