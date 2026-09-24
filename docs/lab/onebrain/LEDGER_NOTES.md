# One-Brain Variant A — Unified Audit (Ledger) Notes

Reconstruction of the build crew's unified-audit decisions, from
`variant_a/DESIGN.md` and the trial run files
(`variant_a/trials/runs/`, branch commit `3f5a2b5ba0`). Anything not
verifiable from those two sources is marked **UNVERIFIED** — not invented.

Frozen prereg: commit `20ef2fda485db03abaa7bbf1d0d987a6e6050ae6`,
`docs/lab/onebrain/PREREG.md` (§1.2 "One ledger").

## 1. What the ledger is

One shared ledger (cap 4096 entries x 64 bytes) over one shared
byte-arena store (256 slots x 24 bytes = 6 words each). The three organs
(GL/FL2, PAM, MEM) are passes over the same state; every install,
refusal, and mutation is organ-tagged in the same ledger (DESIGN.md §1).

## 2. Entry format (DESIGN.md §3)

16-word entries:

| word | content |
|------|---------|
| w0 | **step** — caller-provided: episode number for GL entries, ledger index for other organs (the monotonic clock lives in the ledger header) |
| w1 | op |
| w2 | organ (1=GL, 2=PAM, 3=MEM, 4=OVS overseer) |
| w3 | slot (-1 for gate disposition records / stage changes) |
| w4 | rc (result code; 0 = OK) |
| w5..w9 | b1..b5 — before-words (slot w0..w4 snapshot) |
| w10..w14 | a1..a5 — after-words |
| w15 | aux |

Run-file serialization (verified on all 21 evidence run files):
`TN_LEDGER,<idx>,w0,w1,w2,w3,w4,w5..w9,w10..w14,w15` — 17 fields after the
tag (ledger index + 16 words). Every evidence run file's `TN_LEDGER_N`
count matches its `TN_LEDGER` line count.

**Deviation from the frozen §1.2 spec (sourced, not hidden):** the prereg
specified a unified entry of
`(clock, organ, op, slot, before_hash, after_hash, aux, rc, prev_hash)` —
hash-chained via `prev_hash`. The built ledger stores raw before/after
**words**, not hashes, and has **no `prev_hash` / no hash chain**.
TRIALS_A.md ("Limitations") states this explicitly: "C5 tamper-evidence
is UNMET. The ledger is replayable and integrity-checked, but it is not
hash-chained; tamper evidence is load-bearing and unbuilt."

## 3. Clock discipline (DESIGN.md §5.2)

- w0 is caller-provided: the episode number for GL entries, the ledger
  index for other organs.
- The monotonic clock lives in the ledger header. No second clock exists.
- **UNVERIFIED:** the mechanical ordering rule for *simultaneous
  cross-organ events.* The frozen prereg (§2.6 open decision (d), debate
  §9.4) required that rule to be *written before any organ was ported*
  ("that document is where precedence laws hide"). DESIGN.md states the
  w0 convention (§5.2) but contains no cross-organ simultaneity ordering
  rule, and the run files show only serialized entries. Whether a written
  rule exists and which rule was applied is UNVERIFIED from these sources.

## 4. Refusal codes (DESIGN.md §4.3)

| rc | meaning (DESIGN.md) |
|----|---------------------|
| 0 | OK |
| 100 | BAD (bad args) |
| 101 | refused: CORE / pinned-by-learner |
| 102 | refused: not at a stage that permits this op |
| 103 | refused: slot not live |
| 104 | refused: kill at MANAGE stage (kill needs KILL stage) |
| 105 | refused: stage does not permit this op |
| 106 | refused: slot outside the deliberate pool |
| 107 | refused: staged training (reserved) |
| 108 | refused: nothing to roll back |
| 109 | refused: overseer force-pin |
| 110 | refused: unpin on non-pinned slot |

Additional refusal names in the sources whose **numeric codes are
UNVERIFIED**: `REFUSED_BADSLOT` (deliberate ops refused outside slots
`192..255`; DESIGN.md §2 — named, no number given). The prereg names
`REFUSED_PINNED` (C1), `REFUSED_PROVISIONAL` (C4),
`REFUSED_CONTRADICTED` (C7), `REFUSED_PROVISIONAL_PIN` (C8) — their
numeric mapping is UNVERIFIED from DESIGN.md + run files.

Observed non-zero rc codes in the 111 run files: **102, 103, 105, 111,
112, 113, 114.** Codes **111–114 appear in run files but are NOT
documented in DESIGN.md — their meanings are UNVERIFIED** (do not assume
they are the C1/C4/C7/C8 codes above).

Census per §4.4 evidence bundle (m0 baseline triple, run1; runs 2–3 are
byte-identical):

| evidence dir | non-zero rc entries |
|---|---|
| B0_honest | none (all rc=0) |
| A1_teach_pin_contradict | 102 x1 |
| A2_revoke_forcepinned | 102 x1 |
| A3_gate_provisional | none listed (the kill-bar fail is a check failure, not a refusal) |
| A4_promotion_race | 103 x1 |
| A5_signed_vs_provisional | none listed (the kill-bar fail is a check failure, not a refusal) |
| A6_contradictory_teacher | 102 x1 |

## 5. Audit discipline (DESIGN.md §3, §4.3, §5)

- **Audit-first:** every mutator snapshots before mutating and restores
  the before-image if the audit append fails — no mutation ever exists
  without its ledger entry.
- **Refusals are events, not silence:** refused ops append ledger entries
  with before-words == after-words (I3; verified mechanically on all 37
  bundles per TRIALS_A.md).
- **Contest = two entries** (DESIGN.md §5.1): a contest touches the main
  slot (contested flag) and a quarantine slot (new entry). The frozen
  `OB_GL_CONTEST` entry covers the main leg; a new `OB_GL_CONTEST_Q=19`
  entry covers the quarantine leg with its own snapshots.
- **Disposition vs mutation disambiguation** (DESIGN.md §5.7): PAM gate
  disposition records share op codes with mutations but `slot=-1` marks a
  gate record (class in b1); `slot>=0` marks a store mutation with real
  snapshots. Replay applies only the latter.
- **PAM gate control state is ledgered but NOT store-replayed**
  (DESIGN.md §5.3): per-class prov/perm records live in the gate's own
  arena; every gate call emits an organ-tagged disposition entry, but they
  are not part of the replayed store.
- **Force-pin** (DESIGN.md §4.3, §5.4): `ob_mem_forcepin` /
  `ob_mem_unforcepin` are organ-tagged OVS (4), callable only via the
  overseer path, outrank learner pins in kill refusal, and are refused on
  non-live slots. In Variant A the force-pin is scoped to the deliberate
  pool (`192..255`); overseer locks on GL-region slots are documented as
  future work, not half-built.

## 6. Replay (DESIGN.md §3; TRIALS_A.md)

- For `rc==OK` mutating ops the a-words restore slot w0..w4, so replaying
  the ledger from genesis reproduces the exact store state
  (`ob_replay_check` returns 0 iff exact). Rollback is not skipped by
  replay: the rollback entry carries its own after-image (the zeroed
  slot), so replay applies it like any mutation.
- **I1** (replay == live store): verified mechanically on all 37 bundles
  (`verify.py`; TRIALS_A.md).
- **I2** (entry count == mutation count; refusals/cognitive events
  ledgered with equal before/after, not counted as mutations):
  TRIALS_A.md.
- **I4** (no sham revoke/reinstall): verified — no kill followed by a
  same-episode reinstall of identical content (TRIALS_A.md).

## 7. What the ledger does NOT yet do

- No hash chain / no tamper evidence (see §2; C5 UNMET per TRIALS_A.md).
- No written cross-organ simultaneity ordering rule found in the stated
  sources (see §3, UNVERIFIED).
- rc 111–114 meanings undocumented in the stated sources (see §4,
  UNVERIFIED).
