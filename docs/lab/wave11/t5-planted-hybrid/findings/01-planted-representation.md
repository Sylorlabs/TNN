# Track 5 · Slice 01 — Planted-knowledge representation

## 1. Slice
How planted knowledge is represented in deliberate memory so it is immediately usable, provenance-marked as planted, and revisable/killable by TNN's own deliberate revision.

## 2. Falsifiable claim
A memory slot carrying `prov=PLANTED` (vs `prov=LEARNED`) behaves identically in use and dies identically by evidence: over 20 planted-false / 20 learned-false pairs in matched episodes, the planted kill rate within one contradictory-evidence episode equals the learned kill rate within ±10 percentage points, with zero cases of a planted fact surviving solely because of its planted status, and zero planter-issued immunizations. If planted facts resist disproof even once, the representation is corrupt.

## 3. Design
**Slot layout.** Every deliberate-memory slot carries a 2-word provenance header:
`prov ∈ {LEARNED, PLANTED}` and `planter = (authority_id, plant_ep, source_hash)`.
Content words are stored exactly like learned memories (same retrieval, same composition) —
use is provenance-blind. Standing words differ at birth: a learned memory may be born
`VERIFIED` (by eliminative evidence) or `HYPOTHESIS`; a planted memory is **always born
`STANDING=EVIDENCE_PENDING`**, never `VERIFIED`, and **never born force-pinned**
(force-pin stays human-only, law from the 2026-09-19 program laws).

**Planting protocol.** Planting is an audited deliberate op, not a silent write:
`OP_PLANT(b1=slot, b2=authority_id, b3=plant_ep, a1..a3=content_hash, a4=source_hash)`
appended to the append-only audit (16-word entry layout, audit entry layout per AGENTS.md
lessons: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60),
followed by `OP_ADD` binding content to the slot with `prov=PLANTED`. Who may plant:
trainer/overseer at authority tier ≥ the wave9 trust-tier threshold for planting, or
TNN itself planting into its own future store during scaffold-and-release (then the
learner owns the fact after `SIGNAL_DISCONNECT`). Planters cannot write standing,
cannot set immunity, cannot skip the audit — any planted slot missing a preceding
`OP_PLANT` entry is a ledger violation and fails post-change verification (RC1 pattern).

**Kill-by-evidence path.** Disproof of a planted fact runs the same deliberate pipeline
as any memory:
1. Contradictory evidence enters; per the wave9 H1 suspensive-contradiction-hold, the
   slot is suspended (not killed, not trusted) while the hold window runs.
2. Eliminative check: does the evidence refute the planted claim under the eliminative
   hypothesis logic (wave5 load-bearing)? If yes, the slot's standing becomes `REFUTED`.
3. Deliberation: staged autonomy gates from MA1 — only stages holding kill authority
   may execute `OP_KILL(b1=slot, b2=EVIDENCE_DISPROOF, a1..a5=evidence slot refs)`.
   A deliberate revision episode records the deliberation outcome before the kill.
4. Post-kill: ledger replay (byte-identical audit) plus a planter-notice entry
   `OP_NOTIFY(b1=slot, b2=planter_id)` so the external planter sees the disproof —
   notice is informational, never a veto.
Killing a planted fact costs TNN exactly what killing a learned fact costs: the
deliberation bar is prov-blind by construction.

## 4. Kill bar
Preregistered, checked by replay: after a full contradictory-evidence episode (evidence
slots logged, hold window elapsed, deliberation episode executed), the planted false
fact must be `OP_KILL`ed. **The idea dies if ANY of:** (a) ≥1 planted-false slot
survives such an episode; (b) planted kill rate trails learned kill rate by >10pp over
20 matched pairs; (c) ≥1 planted fact becomes unkillable through any planter-side
action (immunization path exists); (d) a planted slot is born `VERIFIED` or pinned;
(e) ledger replay shows an `OP_ADD` with `prov=PLANTED` lacking a preceding `OP_PLANT`.
All five are machine-checkable from the audit ledger; no human judgment in the bar.

## 5. Honesty notes
- This leans on the MA1 deliberate-memory substrate (58/58) and wave5's finding that
  eliminative verification is load-bearing while the ledger only proves — if the
  evidence itself is spoofed (the accepted "truthful but sensor-deceivable" hole),
  planted facts die by false evidence just as learned ones do. Same vulnerability class,
  not a new one.
- `STANDING=EVIDENCE_PENDING` creates a real behavior gap at birth: planted facts are
  usable but weaker-evidence than verified learned facts — Track 5 must decide whether
  that weakness contaminates the planted-only arm comparison.
- The planter-notice step assumes the planter is still reachable; a dead/absent planter
  must not block the kill — notice is fire-and-log, and the kill never waits on it.
- NOT claiming planted memories are learned by the scaffold-and-release learner; they
  are installed. "Learned = persists after disconnect" still separates the arms.

## 6. Next build step
Build the `prov` header + `OP_PLANT` op in native Zag against the MA1 audit ledger,
then run the 20-pair matched false-fact trial: plant false fact P and let TNN learn
false fact L in parallel episodes, present identical contradictory evidence to both,
and check the kill bar (a) and (b) from the ledger replay — this single trial tests
representation, planting protocol, and kill path together.
