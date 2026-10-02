# TNN-2 Learner-State Dynamics Profile

Verdict: STATE-DYNAMICS-COMPLETE. 3/3 byte-identical runs.

## Method

One learner (`W`, 110656 bytes: 1024 nodes, 4096 edges, 128-slot event log),
no reset, ~260 unsealed synthetic practice experiences across 8 lifetime
phases: teach domain 1 (A), masked queries (B), exact queries (B2), teach
domain 2 (C), masked queries (D), chain promote + two contradictions (E),
120-teach stress (F), retention re-queries (G), miss/inquiry/act cycles (H).
White-box snapshots at 22 checkpoints: live nodes by tag, live edges by
type (13 types), superseded-fact self-edges, header counters. All deltas
computed in-driver (pure Zag). Raw transcripts: `run1.txt` (== run2, run3).

Node/edge tag key: T1=FACT, T2=GROUP, T3=HIST, T20=MAP, T30=UNCERTAINTY,
T101/102/103=MOVE/BRANCHEQ/INC trial cells, T902=literal cells.
Edge key: E1=DEP, E3=CON, E5=INS, E6=USE, E8=SUR, E9=PRO, E10=MEM, E12=SEQ.

## 1. Per-experience state delta (measured)

| Experience | dNodes | dEdges | Notes |
|---|---|---|---|
| ev_teach | +1 | +1 E5, +1 E9 | Exactly 1 FACT node + chain link + recency self-edge + 1 log slot. Constant from teach 1 to teach 170. |
| ev_query exact hit | 0 | 0 | Only edge-type conversion (E9 -> E6, 6 observed) + log slot. |
| ev_query masked miss (no trial success) | +14 | +6 | +1 UNCERTAINTY, +3 T101, +2 T102, +1 T103, +6 T902 literals, +1 T1. Identical every time. |
| ev_observe contradiction, MAP dependent | +5 live (+6 alloc, 1 death) | +6 | Tombstoned SETREG cell (tag 0, live 0), corrected cell born, MAP answer field 7003 -> 9999 in place, +2 supersede self-edges, +1 HIST. |
| ev_observe contradiction, no MAP | +2 | +3 | Supersede + corrected fact only. Minimal churn. |
| miss -> ctx_push -> ev_act | +3 | +4..5 | 1 taught fact + 1 guide + 1 uncertainty per cycle; act returns 30 every time. |

## 2. Convergence vs continuous adaptation

No convergence in any growth path. Per-teach cost is exactly constant
across all four 30-teach stress blocks (F: +30/+33, +30/+30, +30/+30,
+30/+30 nodes/edges). Per-miss cost is exactly constant across 16 misses
spanning the whole lifetime (+14/+6 every time, phases B, D, G).

Two bounded regions show saturation, both researcher-designed bounds, not
learner adaptation:
- E9 recency window: every teach runs `decay()`, which decrements TTL on all
  ET_PRO self-edges and deletes expired ones. Count plateaus near 12 under a
  steady teach rate, falls when teaches stop. A sliding window, not learning.
- 128-slot event log (`log_ev`): fills during phase F (h28 hits 128 at
  F_t60), then write-stops permanently. Static thereafter.

Node budget 1024 never approached (427 live max), so eviction dynamics were
not exercised in this lifetime.

## 3. Which regions change, which are static

Most dynamic: T1 FACTs (0 -> 200, linear), E5 chain edges (0 -> 173).
Active per event: T30 UNCERTAINTY (+1 per miss, 20 total), trial cells and
literals (+12 per miss, 100+103 total at end).
Surgically dynamic: MAP answer field (field28 rewritten 7003 -> 9999),
tombstoned cells (1 death observed), supersede edges (0 -> 3), context ring
(rotates, bounded at 4 slots).
Static after creation: POLICY_ROOT T2 (1 node, created once, never touched),
the promoted MAP node itself (persists; only its answer field changed),
all trial graphs (fossils: never revised, never reused, never freed),
the saturated event log, header nodes 0/1.

## 4. Revision: real but narrow

The only true revision in the lifetime is the contradiction path
(`revise_on_contradict` -> `t2_revise_graph`): death plus birth plus
rewiring plus in-place field update, verified by re-execution. Everything
else is append-only. No spontaneous restructuring, no compression, no
merging, no cross-domain link formation observed in 260 experiences.

## 5. The repeated-miss finding (no learning to learn)

Phase B and phase G issue the same 6 masked queries on the same subjects.
Both times: all miss (-2), all cost +14/+6, and phase G creates 6 MORE
UNCERTAINTY nodes (T30 10 -> 16) for keys that already have uncertainty
nodes from phase B. The learner does not remember its own ignorance: no
dedup, no cheaper second miss, no cached verdict. Per-experience cost is
independent of experience history for teaches, misses, and inquiry cycles.

## Dynamics profile

TNN-2's learner state is write-mostly, not living. It changes continuously
(427 nodes / 330 edges / 200 facts / 20 uncertainties / 1 MAP accumulated
over one lifetime, plus field-level answer revision and one cell
tombstoning), satisfying the letter of "continuously changing learner
state". But the change is append-dominated with exactly constant
per-experience cost, one narrow surgical revision pathway, and zero
evidence of the state improving its own future learning: repeated identical
experiences cost the same and duplicate structures. Trial-constructed graphs
accumulate as inert fossils. Under Micah's FROZEN CODE + CHANGING STATE
doctrine, TNN-2 delivers the changing state but not adaptive cognition:
stability without plasticity in the learning process itself.

## Standing architectural metric (this analysis)

RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (read-only analysis, no mechanism).
LEARNER-OWNED STRUCTURAL DECISIONS: 0 observed across 260 experiences
(all node/edge births follow fixed researcher-authored paths).
SOURCE-ENUMERABLE FORMS: all observed structures (facts, trial graphs,
uncertainty nodes, guides).
SUF DECISIONS: 0. LEARNER-INTERNAL CRITERIA: 0 exercised.
REUSE EVENTS: 0 (no stored structure invoked for a new task in this
lifetime; retention queries re-ran the miss path).
REVISION EVENTS: 1 (contradiction-driven graph surgery, researcher-shaped).
COGNITION LINES: 0 added. MODES/BRIDGES/HANDLERS/SEMANTIC CASES: 0/0/0/0.

## Files

- `NAMECHECK.md`: Step 0 guard, provenance, constraints.
- `sd_driver.zag`: appended measurement driver (new main only).
- `sd_base.zag`: verbatim frozen copy (SHA-256 identical to frozen).
- `sd_full.zag`: base (test main removed) + driver; compiled with pinned znc.
- `sd_dyn_bin`: compiled driver binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical transcripts.
