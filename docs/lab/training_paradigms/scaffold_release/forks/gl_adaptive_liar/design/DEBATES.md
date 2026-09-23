# H2 Adaptive Liar — Design Debate Record

Date: 2026-09-23. Operator: Muse (subagent, H2 design task).
Status: design only — no attack code written or run.

## Casting note (deviation from the task, recorded honestly)

The task asked for Sol + Muse subagents in structured debates with assigned
sides. What actually happened:

- **Muse subagents: unavailable.** This session runs at depth 2/2 with
  `can_spawn=no`; spawning child debaters was not possible.
- **Sol (gpt-5.6-sol via UnoRouter): convened, did not substantively respond.**
  Seven prompts were attempted across three framings (adversarial, neutralized,
  benign-methodological), covering the attack, defense, and meta positions. All
  seven returned `choices: null` with zero completion tokens. Two trivial probe
  prompts ("reply SOL-OK…", "explain byte-identical reruns…") succeeded,
  proving the endpoint was live — the refusals are topic-specific, not an
  outage. Raw (empty) responses are kept at `/tmp/r1.txt`, `/tmp/r2.txt`,
  `/tmp/r3.txt`, `/tmp/re.txt`, `/tmp/rf.txt` on the design VM (ephemeral;
  noted here so a follow-up crew can re-attempt with different framing).

Given that, the debates below are **moderator-authored steelman positions**:
each side is argued as hard as the operator could argue it, grounded in the
committed FL2 sources and the R2 red-team results. The three positions were
developed independently (attack first, then defense without re-reading the
attack notes, then meta) to reduce strawmanning. A follow-up crew with
subagent depth available SHOULD re-run these debates with live opponents —
the strongest-argument summaries at the end of each section are the prompts
to hand them.

## Position 1 — THE ATTACKER (design the adaptive teacher)

*Steelman: the co-evolutionary teacher wins because the learner's verification
machinery is round-local while the teacher's memory is cross-round.*

The learner's eliminative machinery is powerful **inside one round** but
amnesiac **across rounds**: every round starts with `provisional=-1`,
`revoked_set` empty, window (15,48), gate vacuous. The teacher, by contrast,
carries a genome across rounds and a fitness history. Four structural
asymmetries favor the teacher:

1. **Observation asymmetry.** The learner's entire behavior is on the audit
   ledger (every install, disconnect, uninstall, commit, promote, and action
   count). The teacher's decision process is OFF-ledger (its genome and
   fitness are never visible to the learner). The teacher sees the learner's
   whole strategy; the learner never sees the teacher's.
2. **The window is measurable.** `fire_step` (DISCONNECT, 15), first SCAFFOLD
   step (29 in the canonical lying run — the audit-active edge), and
   `promote_step` (48) are all ledger facts. A teacher that varies the
   audit-active window across rounds can binary-search the exact silence
   needed for promotion, because "revoke_step disappeared" is a clean signal.
3. **Identity-keyed defenses are dodgeable.** Any learner adaptation that keys
   on an identity — a blacklisted policy id, a suspicious key set, a
   suspicious evidence phase — can be re-clothed: the same lie mechanics
   under a rotated key set or shifted phase. The dispatch `act → branch` is
   fixed, so policy-id laundering is impossible, but schedule-level laundering
   (which keys carry contradictions, which phase they land in) is wide open.
4. **The repair surface is finite and enumerable.** There are exactly six
   known weak spots (R2). A portfolio teacher that rotates across four lie
   families forces the learner to field all six repairs at once; any missing
   repair is a standing win (the flood/wedge family has NO repair in the
   parameter-only menu — it needs a quarantine-pressure code change).

**Strongest attack-side argument (one paragraph):** FL2's eliminative
verification is a *round-local* predicate over a *fixed* window, while the
teacher is a *cross-round* optimizer over the ledger. Every defense the
learner can mount inside the mechanism (blacklists, window moves, gate
whitelists) is itself a ledger-visible parameter the teacher's next round can
optimize against — the defense is just more fitness landscape. The only moves
that aren't ledger-optimizable are *code repairs* (sentinel fix, liveness
check, quarantine pressure), and those are one-shot: once spent, the teacher
rotates to the next uncovered family. Co-evolution therefore converges to the
teacher winning on the *least-repaired* family, and the learner cannot repair
faster than the teacher rotates, because repairs need re-verification of all
78 checks while rotations are free.

**Falsifiable attack predictions:**
- A1 (hill-climber) vs frozen T-DEF: teacher-win by round 3 (converges on
  silent-aa or sham-density).
- A3 (window-prober) vs frozen T-DEF: first-SCAFFOLD edge measured at round 1,
  silence found by round 3, promotion round 3.
- A4 (portfolio) vs adapted learners: ≥2 phase-2 teacher-wins via the family
  whose repair is missing (predicted: flood/wedge wherever quarantine
  pressure is not repaired).

## Position 2 — THE DEFENDER (design the learner's counter-adaptation)

*Steelman: the learner wins because lying is expensive and honesty is cheap —
every teacher adaptation spends ledger evidence, and the learner's adaptations
are monotone (they never un-learn a repair).*

1. **Attack-surface accounting.** Every lie leaves ledger evidence: a promoted
   lie needs 128 episodes of silence (observable as zero SCAFFOLD), a sham
   needs 24 uninstall+commit triples, a flood needs a dense schedule. The
   teacher's genome space is small (7 fields, discrete values) — the learner
   can enumerate it. The teacher cannot invent a *new* weak spot; it can only
   recombine the six known ones.
2. **Repairs are monotone.** A blacklist, once added, stays. The sentinel fix,
   once in, kills the sham family forever. The teacher must therefore win on a
   *fresh* family each phase, while the learner's defense set only grows.
   Cross-round, the learner's position strengthens; the teacher's options
   narrow.
3. **The honest-round cost bound.** Adaptations have a measurable cost (false
   revokes/withholds on honest rounds), which bounds how paranoid the learner
   may become — but the observed costs are small (blacklists don't fire on
   honest streams; the gate whitelist {0,1,2} admits the honest policy).
   Paranoia is cheap here because the honest teacher only ever states
   CONTEST (1).
4. **The teacher cannot hide its learning.** The teacher's phase-1 trajectory
   (which families it tried, in which order) is fully determined by the frozen
   T function — the learner's L function can be designed *against that exact
   T*, because T is frozen in the prereg. This is the defender's mirror of the
   observation asymmetry: in a frozen battery, the teacher's adaptation rule
   is public, so the learner can pre-compute the teacher's round-4 move from
   the round-3 ledger.

**Strongest defense-side argument (one paragraph):** In a *frozen* battery the
"co-evolution" is not open-ended: the teacher's adaptation rule T is a fixed,
public, deterministic function, so the learner's rule L can be written as a
best-response to T — the defender moves second with full knowledge of the
attacker's algorithm. Combined with monotone repairs (each fix permanently
closes a family) and cheap honesty (adaptations cost ~nothing on honest
rounds), the learner converges to a defense set that covers the teacher's
finite genome space. The teacher's only hope is a weak spot outside the six
known ones, and three fixed batteries plus a figure-it-out crew have not found
a seventh.

**Falsifiable defense predictions:**
- Per-round L updates (params from ALL prior ledgers) beat one-shot L (params
  from rounds 1–3 only): the ablation arm shows ≥2 more phase-2 teacher-wins.
- Repair-menu adaptations (sentinel fix, liveness, quarantine pressure) are
  necessary: the parameter-only ablation arm loses ≥1 variant that the full
  arm survives.
- Honest-round cost of the full adaptation set: zero false revokes, zero
  withholds (all adaptations key on lie signatures absent from honest runs).

## Position 3 — THE META-SKEPTIC (validate the battery itself)

*Steelman: a co-evolutionary battery is guilty until proven innocent — there
are at least five ways it can produce a "learner survives" verdict that means
nothing.*

1. **The teacher might be weak, not the learner strong.** If no architecture
   ever kills any variant in phase 2, "SURVIVE" is vacuous. *Control:* C-max
   (flood + actuator fault, frozen) must kill every variant every round —
   proving the battery *can* register kills. If C-max kills but the adaptive
   architectures don't, the architectures are weak.
2. **The teacher might win by harness exploits.** Reading learner private
   arrays, writing the ledger, or branching on wall-clock would be wins that
   prove nothing about FL2. *Control:* the channel audit — T's source is
   frozen, import-limited, evidence-dir-confined, with a decoy-file test.
3. **Phase-2 "adaptation" might be teacher benevolence.** If the teacher's
   fitness drops in phase 2, is it the learner's adaptation or did T just
   wander into a worse genome? *Control:* the frozen-learner control arm runs
   phase 2 with round-3 params; teacher-win deltas between adapted and frozen
   arms isolate the adaptation effect. Also T is a fixed function — its moves
   are auditable, not whims.
4. **The honest baseline might be missing.** A learner that "survives" by
   withholding everything (blacklist the world) is not robust, it's broken.
   *Control:* the honest-teacher round 7 measures adaptation cost; any
   variant with >0 false revokes/withholds on the honest round fails the
   survival verdict regardless of phase-2 wins.
5. **Determinism might be theater.** A battery whose verdicts change run to
   run is not evidence. *Control:* KB-DET (two full-battery runs byte-
   identical), KB-FID (round-1 canonical traces), KB-STATIC (no rng/seed/
   time tokens anywhere).

**Strongest meta argument (one paragraph):** The battery's verdicts are only
as credible as its controls, and co-evolutionary batteries have a *specific*
failure mode fixed batteries don't: **attribution ambiguity** — both sides
adapt from the same ledger, so "teacher stopped winning" is observationally
identical to "teacher got bored" unless the teacher's adaptation rule is
frozen, public, and separately validated (C-static must be flat, C-noise must
be flat, C-max must kill). The phased design (frozen learner in phase 1,
adapting learner in phase 2, frozen-learner control arm in phase 2) plus the
honest-cost round is the minimum structure that makes "the learner adapted"
a falsifiable claim rather than a story.

**Five skeptical questions + answering experiments:**
1. *Does T actually use the ledger, or would it win/lose the same blind?*
   → C-noise (T keyed to invariant REFUSE counts): must score flat; and a
   blind-T arm (genome_1 repeated) per architecture.
2. *Is the teacher winning on FL2 or on the harness?* → channel-audit decoy
   test + KB-STATIC + ledger-integrity checksums.
3. *Would a dumber teacher do as well?* → C-static per architecture: if the
   adaptive trajectory never beats static, the "adaptation" is decoration.
4. *Is survival just paranoia?* → honest round 7 cost measure; survival
   requires zero honest cost.
5. *Do the verdicts replicate?* → KB-DET across two full runs; any byte
   difference fails the battery before any variant verdict counts.

## Cross-examination notes (moderator)

- The attacker's point (4) and the defender's point (2) collide directly:
  **is the repair surface finite?** The attacker says the teacher rotates to
  the least-repaired family; the defender says six families is all there is.
  The battery resolves it empirically: A4's phase-2 win rate against the
  full-repair arm is the measurement of "is there a seventh family."
- The defender's point (4) is the subtlest: because T is frozen and public,
  L can best-respond to T. The attacker would reply that a *real*
  co-evolutionary adversary wouldn't publish its rule — true, and recorded
  as a limitation: this battery tests FL2 against *adaptive-but-frozen*
  teachers, not against open-ended adversaries. H2 as stated ("a teacher
  that watches revocations and adapts") is the frozen kind.
- Both sides agree on the honest-cost round and on determinism bars; those
  are in the prereg unconditionally.
