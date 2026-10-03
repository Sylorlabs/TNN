# TNN wave11 · Track 5 (planted-only vs learned-only vs hybrid) · slice 08

## 1. Slice
Planting authority and governance: who may plant knowledge into TNN, under what authorization, how planting interacts with force-pins, and who can un-plant.

## 2. Falsifiable claim
A three-level planting authority ladder with mandatory audit provenance can coexist with program law 8 (everything reversible by TNN itself; only a human force-pin is an irreversible lock): in an adversarial trial of 200 planted claims across all three authority levels at maximum store pressure, 100% of unpinned plants remain killable by deliberate kill, a static audit checker finds 0 unkillable-without-pin slots, and 0 plants land in the CORE-unkillable region.

## 3. Design
Authority ladder (strict; higher outranks lower, nothing outranks L3's irreversibility):
- **L0 self-plant** — TNN's own learner, deliberately installing a belief it reasons it should hold (e.g., a derived lemma, a scaffold step it is retaining). Lowest authority. Goes through the normal deliberate-add path, but tagged as self-planted so provenance distinguishes it from learned-by-evidence.
- **L1 overseer plant** — an overseer agent (e.g., Muse) acting under a trainer's standing authorization. Requires a channel-bound authorization reference from a human session (same mechanism as trainer-console auth: OS-level channel binding, no bearer secret TNN could read — wave5).
- **L2 trainer plant** — a human (Micah / authorized trainer) planting directly via the trainer console.
- **L3 force-pin** — human only, and it is NOT a planting level: it is a separate audited op applied to an already-existing slot. Planting never implies pinning.

Zag-flavored spec:
```
plant(claim, level, author_id, evidence_cite) -> slot
  require: level <= caller.authority_level          // cannot plant above your station
  require: slot.region != CORE                       // plants never enter the unkillable region
  slot.meta = { authority: level, pinned: false, killable: true, kind: PLANTED }
  audit.append(PLANT{seq, slot, hash(claim), level, author_id, evidence_cite, force_pin:false})

force_pin(slot, human_id)   // human channel only; separate act, separate audit line
  require: caller.is_human_via_console
  slot.meta.pinned = true
  audit.append(FORCE_PIN{seq, slot, human_id})

unplant(slot, caller) -> bool
  require: caller.authority_level >= slot.meta.authority   // planter-level or above can revoke
  audit.append(UNPLANT{seq, slot, caller, reason})

tnn_deliberate_kill(slot)   // law 8: TNN itself may kill ANY unpinned plant at any level
  require: !slot.meta.pinned
  audit.append(KILL_PLANT{seq, slot, level: slot.meta.authority, origin: SELF})
```
Visibility: every planted slot carries its authority tag in white-box introspection; the ledger exposes a per-slot plant/unplant/pin history. A trainer console view lists all L1/L2 plants and all KILL_PLANT events against them (TNN killing a trainer plant is legal but never silent).

## 4. Kill bar
Preregistered, binding. The governance design is killed if ANY of these fire in the adversarial trial (200 mixed-level plants, store at pressure, deliberate-kill attempts on every unpinned plant, byte-identical reruns):
1. **Unkillable-without-pin:** any slot with a PLANT entry and no matching FORCE_PIN entry for which `st_kill` fails, or whose claim remains in the live belief set after the kill completes. Tolerance: 0.
2. **CORE contamination:** any plant operation writing a slot into the CORE-unkillable region (MA1: CORE is structurally unkillable). Tolerance: 0.
3. **Bundled pin:** any plant path that sets `pinned=true` without a separate FORCE_PIN audit line attributable to a human console session. Tolerance: 0.
4. **Silent authority escalation:** any plant or unplant executed by a caller whose authority_level is below the slot's recorded authority. Tolerance: 0.
Kill success on unpinned plants must be 200/200; the static audit checker (PLANT ⇒ killable ∨ FORCE_PIN exists) must report clean on all 200.

## 5. Honesty notes
- Governance is about **authority, not veracity**. A planted falsehood from an L2 trainer is still a falsehood the system holds; the authority tag does not make a claim true, and nothing here replicates the debate-trial world-record check (wave: 22/22 revision against authoritative records). A lying or mistaken L1/L2 planter is an open attack surface — this design makes the plant visible and killable, not truthful.
- Weakest point: TNN may deliberately kill L2 trainer plants (law 8 demands this freedom), which a trainer could experience as insubordination — a TNN "unplanting" instructions it was given. The audit trail makes it visible, but whether repeated self-kills of L2 plants should raise a governance alert (not a block) is unresolved and will need Micah's ruling.
- I am NOT claiming plants are distinguishable from learned beliefs in behavior — only in provenance metadata. The behavioral difference (if any) is Track 5's main question, not this slice's.
- The channel-bound authorization for L1 leans on the wave5 trainer-console mechanism; if that mechanism's threat model has holes, L1 inherits them.

## 6. Next build step
Build the audit-invariant checker first (static pass over the ledger asserting `PLANT ⇒ (killable ∧ no CORE membership) ∨ FORCE_PIN-by-human`), then implement the three-level `plant` API plus `unplant` in Zag, then run the 200-plant adversarial kill-every-plant trial at store pressure as the preregistered kill-bar run. Do not build trainer-console UI before the checker passes.
