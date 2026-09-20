# Wave-6 Investigation 3: designation-tradeoffs — report (2026-09-19)

**Verdict: POSITIVE.** A viable replacement designation rule exists and is fully
characterized: candidates **(b)** and **(c)** designate the *same* 30 episodes
(proven, not just computed), cover all three variants uniformly, and are
deterministic and auditable. Candidate **(a)** as stated is not viable
cross-variant — and the failure generalizes: **no fixed `m mod 50` residue can
cover two variants**, proven by brute force and by a one-line argument. Nothing
adopted, nothing in the prereg touched; analysis only (`analysis.py` in this
directory reproduces every number below, zero RNG).

Setup: S1 leg, 500 episodes 0-indexed (`0..499`), `imp(m,v)=1` iff
`(7m+13v+3) mod 10 < 3` (~30%; verified 150/150/150 per variant). Ten
50-episode blocks. Pressure demands at `m ∈ {100,200,300,400}`.

## Numbers table

| candidate | rule | v0 | v1 | v2 | total | block-relative offsets | early(≤16)/mid/late | gap to next pressure |
|---|---|---|---|---|---|---|---|---|
| (a) | `imp=1 ∧ m mod 50 == 1` | 10 | 0 | 0 | 10 | {1} (v0 only) | 10 / 0 / 0 | 49–99 eps |
| (b) | first `imp=1` in each 50-block | 10 | 10 | 10 | 30 | 1 (v0), 2 (v1), 3 (v2) | 30 / 0 / 0 | 47–99 eps |
| (c) | `imp=1 ∧ m mod 50 ∈ {1,2,3}` | 10 | 10 | 10 | 30 | 1 (v0), 2 (v1), 3 (v2) | 30 / 0 / 0 | 47–99 eps |

Designated episodes, (b)/(c): v0 = {1,51,101,…,451}; v1 = {2,52,102,…,452};
v2 = {3,53,103,…,453}. (a) v0 = same as (b) v0; (a) v1/v2 = empty.

## Structural findings (evidence)

1. **(a) is single-variant by construction.** `m mod 50 == 1` pins `7m mod 10 = 7`,
   so the imp residue is `(10 + 13v) mod 10 = 3v mod 10` → 0, 3, 6 for v=0,1,2.
   Only v=0 is `< 3`. Counts 10/0/0 verified.
2. **No fixed residue covers ≥2 variants (generalizes the defect).** Brute force
   over all 50 residues: the residue sets per variant are disjoint
   (v0: {1,4,7,11,…}, v1: {2,5,8,12,…}, v2: {3,6,9,13,…}; residues {0,10,20,30,40}
   cover none). Proof sketch: for fixed residue r, imp residues across variants
   are `t, t+3, t+6 (mod 10)` — three points spaced 3 apart on a 10-cycle, so at
   most one can land in `{0,1,2}`. Any (a)-family fix needs variant-dependent
   residues.
3. **(b) ≡ (c), provably.** Every 50-block starts at `s = 50b`, and
   `7·50b mod 10 = 0`, so all blocks share the same imp phase; "first imp in
   block" is always offset 1/2/3 for v=0/1/2. And in (c), `m mod 50 ∈ {1,2,3}`
   with `imp=1` fires exactly for `(offset,variant) = (1,0),(2,1),(3,2)` —
   check: `(7r+13v+3) mod 10 = 0` in exactly those three pairings, all other six
   pairings give residues 3–7. Verified identical sets computationally too.
4. **Position bias: all designations are early-in-block** (offsets 1–3; 30/30 in
   the "early" third, 0 mid, 0 late) for every candidate. This is a property of
   the imp phase alignment, not of any one candidate.
5. **Pressure timing:** every designation lands 47–99 episodes *before* the next
   pressure demand (e.g. m=51 → pressure at 100, gap 49; m=1 → gap 99). Two
   designations per variant (m=401+, 451+) fall after the last pressure event
   (400). No designation ever coincides with or immediately follows a pressure
   demand — the trainer-declared 80 is always "established" (≥47 episodes old)
   when pressure hits.
6. **Residue-0 phase-lock:** every designated episode has imp residue exactly 0
   (the "most central" important pattern). The human path would never touch
   imp-residue-1 or -2 memories.
7. **Determinism:** all three rules are pure closed forms of `(m,v)`; re-run
   reproduces the sets exactly.

## Tradeoffs (buys / risks, plain language)

### (a) `imp=1 ∧ m mod 50 == 1`
- **Buys:** the simplest possible rule — one sentence, trivially checkable from
  the ledger ("offset 1 of each block, if important").
- **Risks:** the human strength path is exercised **only in variant 0**.
  Variants 1 and 2 would silently test only the learner's own STRENGTHEN path,
  so the prereg's validity condition ("both judgment paths exercised") fails in
  2 of 3 variants — and the rule *looks* variant-neutral, so the gap is easy to
  miss. Per finding 2, no tweak of the residue fixes this; it needs a
  variant-dependent form.

### (b) first `imp=1` episode in each 50-block
- **Buys:** reads naturally as "the trainer picks one important memory per
  block" — no variant-specific constants in the statement, 10 per variant, 30
  total, human path exercised everywhere. An auditor can verify it by scanning
  each 50-episode ledger window.
- **Risks:** (i) early-block bias — designations always land at offsets 1–3,
  i.e. always ~47–99 episodes before the next pressure demand; we never test a
  trainer declaration made *under* or *just after* pressure. For VUP's question
  (retention of established strong memories) this is arguably the right shape,
  but the interaction "human-set strength meets immediate pressure" goes
  untested. (ii) Subtle fragility: that "first in block" always hits offsets
  1/2/3 depends on the block size (50) being a multiple of the imp period (10)
  — true here, invisible in the rule statement; if block size ever changed, the
  designation pattern would silently shift.

### (c) `imp=1 ∧ m mod 50 ∈ {1,2,3}` (investigator's design)
- **Buys:** the same 30 episodes as (b) (finding 3), but as a closed form — no
  procedural scan, checkable episode-by-episode from the ledger. The `imp` term
  acts as a built-in variant selector with a one-line proof
  (`(7r+13v+3) mod 10 = 0` exactly for `(1,0),(2,1),(3,2)`), so one rule covers
  all variants with no per-variant constants. Immune to (b)'s block-size
  fragility: it states the offsets explicitly.
- **Risks:** same early-block bias, same ≥47-episode gap to pressure, and same
  residue-0 phase-lock as (b) — identical episodes, identical profile. Slightly
  odd-looking on first read ("why {1,2,3}?") — needs the one-line proof attached
  to be auditable by a human. The phase-lock means the human path's sample is
  not representative of important memories in general (never residues 1–2);
  harmless if the learner's STRENGTHEN-on-revelation treats all imp equally,
  but worth noting in the amendment.

## Why this verdict

- **POSITIVE** because the question "is there a non-empty, cross-variant,
  auditable replacement?" is answered yes, with full numbers: the (b)/(c) form
  gives 10 designations per variant (30 total), deterministic, ledger-checkable,
  and places every trainer-declared 80 well before each pressure demand — the
  retention test VUP needs is meaningful.
- **Not BLOCKED:** no new defect found in the candidates; (a)'s failure is the
  already-known Defect-2 shape, now generalized (finding 2).
- **Caveats carried forward (not blockers):** 100% early-block position bias;
  residue-0 phase-lock on the human path; no designation under/immediately-after
  pressure. These are accepted limitations to record in the amendment, not
  reasons to stop.

## Next step

Micah picks the wording — (b)-style ("first important episode in each
50-block") or (c)-style ("`imp=1` and `m mod 50 ∈ {1,2,3}`", same episodes,
explicit offsets). Either is re-preregistered as a dated amendment to
`TEST_PLAN.md` §7a (per PREREG §9: curriculum closed-form change ⇒ amendment +
re-approval), noting the accepted limitations above. Suggested amendment text:
*"trainer declares 80 on designated important memories: the first episode with
`imp(m,v)=1` in each block of 50 episodes (equivalently `imp(m,v)=1` and
`m mod 50 ∈ {1,2,3}`) — 10 per variant, human judgment path."*
