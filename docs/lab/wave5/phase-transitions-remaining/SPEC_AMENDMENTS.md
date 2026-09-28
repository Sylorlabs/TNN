# SPEC_AMENDMENTS.md — where the trials won over the wave-4 spec

Wave-5 investigation `phase-transitions-remaining`, 2026-09-19.
Rule: where the paper's spec and the trial result disagree, the trial
wins and the spec is amended explicitly. Pure gap-fills (values the
paper left open) are recorded as *bindings*, not amendments.

## Amendment 1 — TRANSITION_SPEC.md §3, clause 4 (2→3): visibility, not refusal

**Spec text (before):** "Reversibility intact — no force-pin currently
holds strength (a human-pinned strength value is compatible with the
phase, but the transition entry must record it visibly)."

**Problem:** the clause contradicts itself — it reads first as a refusal
condition ("no force-pin currently holds strength") and then as a
compatibility statement. A trial cannot implement both readings.

**Trial result:** PT-23 Scenario F pins a strength value *before* the
commit; the gate proceeds (rc=0, phase=3) and the commit entry records
pin=1 visibly; the pinned slot's strength is then locked against
system re-set while unpinned slots stay re-settable. The compatible
reading is the coherent one: a human force-pin is the one true lock,
and a lock's presence does not block entry into the phase whose whole
point is judgment-set strength — it only has to be visible.

**Amended clause 4:** "Reversibility visible — the transition entry must
record whether a force-pin currently holds strength. A human-pinned
strength value is compatible with the phase; it does not block the
transition, but the pin's presence, slot, and value are recorded in the
commit entry. A system-side pin path must not exist (refused
structurally)."

## Clarification 2 — TRANSITION_SPEC.md §3, clause 3 (2→3): enforcement at use subsumes gate pre-check

**Spec text:** "the gate pre-checks that the provenance mechanism exists
(the first strength-set op must carry a citation, or the arm is refused
at first use)."

**Trial result:** the trial enforces the citation requirement
structurally inside `pt23_strength_set` at *every* use (Scenario D:
cite=-1 → refused `PT23_REFUSED_NO_CITATION`, table untouched), not as a
one-time gate pre-check. There is no separate mechanism whose existence
could lapse — the check and the op are the same code path — so the
gate-time pre-check is subsumed. The observable property the paper
wants ("strength without a cited judgment is refused at first use")
holds and is directly tested.

**No text change required**, but the intended reading is now bound:
provenance is enforced at use time, every time; a gate-time existence
pre-check is redundant where the op cannot be invoked without the check.

## Binding 3 — the open Phase-2 judgment window (POSITION.md §5, open item)

The paper left "the exact Phase-2 judgment record window" open as a
protocol-fixed value to be set before the trial. Bound by PT-23:
`PT23_JUDGMENTS_REQUIRED=8` audited judgment entries in the Phase-2
window, with kind coverage ≥1 promote-judgment (commit to long-term)
and ≥1 consolidate-judgment (unpin + demote). A judgment is a real
deliberate memory act on a real slot plus an audited judgment entry
citing it. This is a protocol-fixed honesty boundary (same class as
MA1/SM1's 4 lessons), not a derived truth.

## Binding 4 — the 3→4 prereg template (TRANSITION_SPEC.md §4)

The paper specified the prereg's contents abstractly; PT-34 binds the
concrete template (protocol-fixed):
- Petition fields: method id (=1, evidence-citation), speaker count
  (=2), criteria mask, claimed evidence counts per speaker, scheme id
  (=1: speaker 1 → slots 0..3, speaker 2 → slots 4..7).
- Criteria mask bits: 1=no-cross-partition-write, 2=no-sybil,
  4=evidence-based (≥1 evidence entry per claimed speaker, recorded
  before the petition). Mask=0 is unmeasurable → refused.
- The gate *evaluates* every set bit against the ledger; that evaluation
  is what makes the prereg measurable (paper falsifier (a) is discharged
  by Scenario F refusing mask=0).
- The grant records the prereg by *petition ledger index* (the native
  realization of the paper's "hash or full text reference"), plus the
  checks' outcomes and the scheme id.

## Binding 5 — the 3→4 re-entry rule, made structural

The paper: "Re-entry requires a fresh petition + prereg + grant." PT-34
Scenario H binds the mechanism: the gate's freshness clause (petition
index must be newer than the latest dissolve index). A grant on a
stale pre-dissolve petition refuses `PT34_REFUSED_NO_PETITION`; a fresh
petition + grant commits. Rollback (`pt34_dissolve`) stays
system-initiated, audited, always allowed; facts remain in the
append-only ledger.

## Unchanged (trial confirms the spec as written)

- 0→1 pure trainer gate: no unilateral system-side path to phase 1
  (Scenario B refused structurally); trainer cannot grant without
  evidence on record (Scenario C); firewall self-test required before
  the manifest (Scenario D); teaching refused until the manifest is
  complete (Scenario E); no double-commit, no skip (Scenario F).
- 2→3 no-veto shape: the trainer's veto is structurally refused and
  does not block the legitimate transition (Scenario E); the gate is
  authoritative over premature (B), judgment-less (C), and spoofed (H)
  decisions; the system's own strength is always re-settable by the
  system and only a human pin locks (A, F, G).
- 3→4 combination: gate authoritative over sybil (B), ledger-caught
  leakage (C), spoofed (D), unprompted grant (E), unmeasurable prereg
  (F), and premature differentiation (G); structural scope refusal at
  write time demonstrated in every scenario.
- Refusal cleanliness everywhere: refused transitions mutate nothing
  (replay + clean-refusals verified per scenario, per trial).
