# Arm Q — Specification: Hybrid taught+emergent vocabulary

**Arm:** Q (ACQ family) — Hybrid taught+emergent
**Brief:** `~/workspace/tnn-lab/units/arms/briefs/Q.json`
**Mechanism (frozen):** Deliberate combination — taught proposals seed the emergent machinery; overlap cap 50%; settled-rule threshold; emergent-wins tie-break.
**Source:** `cl/arm.zag` (71,847 bytes) in this directory
**Purity:** Pure Zag. Zero RNG in any decision path. Byte-identical reruns.

## 1. Architecture: one store, two feeders, provenance on every entry

The Q store holds vocabulary entries (words and phrases) as byte spans in a
contiguous arena, with per-slot metadata arrays (ids, offsets, lengths, corpus
tags, flags, provenance, shifts) and an insertion-order array plus a free
stack. Two feeders populate the same store:

### Taught feeder (Q_PROV_TAUGHT = 1)
- Word-token proposals come from teacher 1 through a teacher protocol gate:
  word-aligned, length ≤ 64 (longer words are split), confidence ≤ 255, grounded
  in a session/sequence pair.
- One-shot adoption under teacher authority: a taught proposal that clears
  the gate is admitted immediately.
- Provenance recorded: teacher / session / sequence / kind.

### Emergent feeder (Q_PROV_EMERGENT = 2)
- P-style co-recall pair voting: pairs of co-occurring units accumulate votes;
  K=7 votes within W=200 episodes promotes the pair to a phrase token.
- Promotion cap: 4096 promotions per episode.
- Promoted phrases become phrase tokens in the store.
- Provenance recorded: promoting episodes, co-recall counts.
- A taught word later cross-confirmed by emergence upgrades to
  Q_PROV_CONFIRMED = 3 without duplicating the entry.

## 2. Collision resolution (Q-RUBRIC-1, deterministic evidence rubric)

A collision exists when two entries overlap >50% either way (min-span
measure) or carry identical labels on disjoint spans.

- Score(taught)   = min(count,1000) + 200 (teacher track-record/confidence bonus)
- Score(emergent) = 2 * min(cooccur,1000)  (use-count bonus)
- Tie → emergent wins (frozen emergent-wins tie-break).
- The loser is killed (tombstoned, never reused; kill reason KR_COLLISION=201);
  the resolution is cross-referenced and audited (opcode OP_COLLIDE=32).
- Settled rule: the same resolution twice → a settled rule is recorded
  (OP_PROMOTE_REVIEW=33); a third losing-form proposal is refused as redundant
  (RF_SETTLED_REDUNDANT=203, audited OP_REFUSE=8).

## 3. Audit ledger

- 64-byte entries: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48,
  stage@52, d1@56, d2@60.
- Opcode namespace: 1=ADD, 2=KILL, 3=PIN, 4=WEAKEN, 5=PROMOTE, 6=REVISE,
  7=SCAN_COMMIT, 8=REFUSE, 9=EVICT, 16=TRAINER_DEFECT_BOUNDARY,
  17=TRAINER_DEFECT_CONTENT, 18=TRAINER_MARK_VALUABLE, 19=TRAINER_SWAP_PROBE,
  32=COLLIDE, 33=PROMOTE_REVIEW (frozen ARM_INTERFACE.md §6 namespace).
- Every mutation (adopt, promote, pin, weaken, kill, defect, revise, evict,
  collision) appends a ledger entry; M5 verified 262,144 entries.

## 4. Determinism

- Insertion order everywhere; overlap iteration sorted; no randomness in any
  decision path.
- M8 battery (m8-1x) asserts byte-identical stdout + artifacts (store hash
  chain, ledger hash chain, allocation trace) across heap perturbations:
  clean, frag, aslr, starve, freelist.

## 5. Fixed battery interface (argv[1] selects the mode)

| Mode | Meaning |
|---|---|
| m1-1x-prose / m1-1x-prose-taughtonly / m1-1x-code | M1 recall legs (variant 1 = taught-only) |
| m2-t1-prose / m2-t1-prose-taughtonly / m2-t1-code / m2-t2-prose / m2-t2-code / m2-t3-1x | M2 retention legs |
| m3-1x | M3 collision/stress |
| m4-1x-prose / m4-1x-code | M4 revision boundary |
| m5-1x / m5-baseline | M5 ledger stress |
| m6-p2c-1x / m6-c2p-1x | M6 cross transfer |
| m7-1x | M7 manual lookup (returns N/A — see VERDICT.md deviations) |
| m8-1x `<croot> <outdir> <perturbation>` | M8 determinism battery |

Variant modes (frozen ablation design): 0=hybrid (taught + emergent),
1=taught-only (no emergent promotions), 2=emergent-only (no taught admission —
0% recall by design, no vocabulary without seeding).

## 6. Verdict

KILLED — Death Criterion 1. The hybrid does not beat
max(taught-only, emergent-only) + 3 points on M1 recall or M2
episodes-to-criterion. See `VERDICT.md`.
