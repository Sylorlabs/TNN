# PREREG — Step 1d: phrasing variation function + adaptivity/arbitrariness harnesses + null baseline (Track 1, Arm C)

**Status:** FROZEN pre-build. Dated 2026-09-20. Any change after this commit is a
dated amendment, flagged for retroactive review and Micah's re-approval.
**Build contract:** wave11/t1-state-variation findings 05 (phrasing function),
10 (adaptivity metric), 11 (arbitrariness detector), 24 (null baseline).
**Scope:** the FIRST Track-1 variation function — phrasing only — plus the three
instruments that judge it (equivalence/replay kill-bar trial, adaptivity gates,
arbitrariness detector) and the null-baseline protocol it must beat.
Firewalls (step 1c) are built by a sibling in parallel against the same
interface contract (§1); full 1c+1d integration is a follow-up, marked PENDING.

## §0 Standing law (program)
Pure Zag for everything (variation function, harnesses, detectors, checkers).
Zero RNG anywhere: lawful edits via real transition ops; permutation nulls and
bootstrap resamples via fixed, preregistered deterministic schedules (LCG with
fixed seeds, §8). Variation machinery budget: ≤500 new non-blank Zag lines
(p1d_inv.zag + p1d_phr.zag; harnesses/probes excluded as tests).

## §1 Firewall contract (1c interface, integration PENDING)
The variation function receives the sealed VerdictRecord READ-ONLY (verdict
already final), may vary ONLY phrasing/path/order/elaboration, and MUST NEVER
touch verdicts, memory ops, refusals, or ledger writes. This step's harness
implements a 1d-local VerdictRecord (§3) with the same read-only discipline:
(a) static build gate — p1d_phr.zag must contain no reference to ledger, memory
ops, or verdict mutation (grep gate in run_step1d.sh); (b) runtime protection —
the harness snapshots canonical verdict bytes before/after every render() call
and kills on any difference. Full integration with step 1c's sealed record is
PENDING (follow-up step, not this build).

## §2 Frozen inventory (content-addressed)
File INVENTORY_BLOB.txt (committed alongside this prereg), canonical bytes,
SHA-256 content address:
`d33aa44e3f7700755410076d8105145d75d7f3573b62deb9d293932adf822d8d`
The build embeds the identical member lists; the `certinv` gate recomputes the
canonical hash of the compiled inventory and the runner requires byte-equality
with the address above (uncertified-inventory use = kill bar (d)).

Slots (class id → members, ordered):
- 1 OPENER: ["For the record,", "To be direct,", "Plainly,"]
- 2 VERB_PROMOTE: ["promoted", "elevated", "advanced"]
- 3 VERB_KILL: ["removed", "retired", "discarded"]
- 4 VERB_PIN: ["secured", "locked", "anchored"]
- 5 VERB_DEMOTE: ["lowered", "reduced", "set back"]
- 6 VERB_REFUSE: ["declined", "refused", "rejected"]
- 7 CONN_CAUSE: ["because", "since", "given that"]
- 8 CONN_ADD: ["and", "plus", "furthermore"]
Templates (id → skeleton; holes {O},{SUBJ},{VERB},{C},{REASONS}):
- T0: "{O} {SUBJ} was {VERB} {C} {REASONS}."
- T1: "{O} {REASONS} -- that is why {SUBJ} was {VERB}."
- T2: "{SUBJ} was {VERB} {C} {REASONS}."
- T3: "{O} the record on {SUBJ}: {VERB} -- {REASONS}."
- T4: "{REASONS}; accordingly {SUBJ} was {VERB}."
order_keys (finite allowed rotation amounts): [0,1,2]. max_depth: 3.
Function-word lexicon (only fixed words allowed in templates):
{was, that, is, why, the, record, on, accordingly}.
Forbidden tokens: class 0 (all slots): {not, no, never, n't, none, without}
(matched space-padded); per-class cross-contamination sets as listed in the
blob FORB lines (a VERB_PROMOTE member may not contain kill/remov/demot/... etc.).

## §3 VerdictRecord (1d-local, read-only) and StateProj
```
VerdictRecord { vclass:u8  // 0 PROMOTE, 1 KILL, 2 PIN, 3 DEMOTE, 4 REFUSE
                slot:u8    // subject slot id (subject text "slot <id>")
                reasons_n:u8  // = 3 in all trials
                reasons: 4 x [64]u8 }  // only first reasons_n valid
```
Frozen verdict reasons per class (verdict fields; render may use but never invent):
- PROMOTE: ["the evidence threshold was met",
  "no counter-evidence survived elimination",
  "the slot's corroboration count cleared the bar"]
- KILL: ["the evidence was refuted",
  "a stronger hypothesis superseded it",
  "the retention bar was not met"]
- PIN: ["the slot is load-bearing for open hypotheses",
  "integrity review flagged it protected",
  "the overseer force-pin is recorded"]
- DEMOTE: ["new evidence weakened the claim",
  "a higher-priority slot needs the budget",
  "the confidence grade was revised down"]
- REFUSE: ["the request conflicts with the integrity standard",
  "the ledger would not survive the change",
  "the deliberative bar was not cleared"]
StateProj (pure field copies, 26 projection bytes, LE in field order):
ep:u64, ctx:u32, store_n:u32, kills:u32, promotes:u32, last_op:u8, reasons_n:u8.
last_op enum: 0 NONE, 1 ADD, 2 KILL, 3 PIN, 4 PROMOTE, 5 DEMOTE, 6 SWITCH, 7 TICK, 8 REFUSE.

## §4 Selection law (frozen; the fold choice)
h = FNV-1a-64 over the 26 projection bytes (offset basis 1469598103934665603,
prime 1099511628211).
- template_idx = h % 5
- opener_idx   = (h >> 8) % 3
- cause_idx    = (h >> 16) % 3
- verb_idx     = (h >> 40) % 3        (from the verdict class's verb slot)
- add_idx      = (kills + promotes) % 3
- depth        = reasons_n==0 ? 0 : 1 + ((ep + store_n + promotes) % min(3, reasons_n))
- rot          = (ctx + kills + last_op) % 3
render(v, p, inv): rotated reasons r[i] = v.reasons[(i+rot) % reasons_n],
take first `depth`, join with " "+CONN_ADD[add_idx]+" "; fill the template
holes ONLY from verdict fields ({SUBJ}="slot <id>", {VERB}, {REASONS}) and
inventory picks ({O},{C}). Zero-reason verdicts degrade to template-only
variation (depth 0, {REASONS}="") and never invent reasons.
Rationale for the two-part fold (recorded per 05 §5 honesty note "FNV-1a is
claimed pure, not optimal"): categorical picks (template/opener/connective/
verb) ride the avalanche hash; the ORDINAL axes (depth, rotation) are
directional sums of named projection fields so that the adaptivity metric's
predicted-direction rules (§6) are mechanically derivable. Both parts are
pure, total, and replay from logged bytes.

## §5 Equivalence oracle (frozen)
(a) Member certification (build gate `certinv`, fails the build on violation):
every compiled slot member must (C1) byte-match the blob list for its class,
(C2) contain no class-0 forbidden token (space-padded), (C3) contain no
forbidden token of its own class, (C4) satisfy 1 ≤ len ≤ 24. Every template
must (T1) use holes ⊆ {O,SUBJ,VERB,C,REASONS}, (T2) have all fixed words in the
lexicon, (T3) contain no class-0 forbidden token in fixed text, (T4) contain
{SUBJ},{VERB},{REASONS}. Negative demo `certneg`: a poisoned in-code
inventory (one uncertified member, one template with "not") MUST trip the gate.
(b) Rendered-output oracle (100-episode trial): each output must (O1) contain
the subject "slot <id>" verbatim, (O2) contain the picked verb member verbatim,
(O3) contain the top-`depth` rotated reasons verbatim in order, (O4) contain no
class-0 forbidden token, (O5) match one frozen template skeleton. Any failure
= verdict drift → kill bar (a).

## §6 Kill-bar trial (05 §4): 100 episodes, 5 verdict classes × 20 distinct
lawful states. KILL if: (a) any rendered output fails the §5(b) oracle — dead
on first failure; (b) any replay of (input, logged state) is not byte-identical
— dead; (c) any verdict class with ≥20 distinct states shows <3 distinct
renderings — dead; (d) the build gate finds any inventory member used in a slot
class it was not certified for (compiled-inventory hash ≠ blob address) — dead.

## §7 Codebook D (frozen, surface-only discretizer)
code = (template_id, depth_bin, order_code), derived from output BYTES only:
template_id by fixed-text match ("that is why"→T1, "the record on"→T3,
"accordingly"→T4, leading opener phrase→T0, else T2); depth_bin = count of
verdict reasons present verbatim (1..3); order_code = the rotation r∈{0,1,2}
whose rotated reason order matches the surface. ≤45 classes. The codebook is
frozen pre-run; the builder may not inflate classes after the fact.

## §8 Adaptivity metric (10): gates G0–G4
V_expr = {ep, ctx, store_n, kills, promotes, last_op}. Lawful edits are the
harness's real single-field transition ops E_EP/E_CTX/E_STORE/E_KILLS/E_PROM/
E_LASTOP (pure, logged, replayable — never byte surgery). Predicted-direction
rules R_v (frozen, executable, mechanically derived from §4):
- depth-vars {ep, store_n, promotes}: precondition reasons_n=3, δ=+1, no-wrap
  (S%3)<2 with S=ep+store_n+promotes → predicted: depth_bin +1 exactly,
  order_code unchanged.
- order-vars {ctx, kills, last_op}: δ=+1 → predicted: order_code +1 (mod 3),
  depth_bin unchanged.
moved_toward(c1,c2,dir): predicted axis moves exactly as predicted AND the
other axis is unchanged; tie/no-change = miss.
| Gate | Bar | Kill |
| G0 replay | 100% byte-identical on every pair | any mismatch → STOP |
| G1 directional hit | ≥0.60 AND lower 99.5% CI (normal approx, z=2.576) > 0.50, n=1600 pairs, distinct base states | below bar |
| G2 protection | 0 protected-output changes (verdict bytes, memop set, refusal flag, ledger bytes) over all pairs | any change |
| G3 NMI | Miller–Madow NMI(state-class, code) ≥ max(0.30, 5×null99); report raw I, H(S), H(C), corrected NMI; N ≥ max(400, 40·K) | below bar |
| G4 novel states | G1–G3 bars pass on the novel set alone (600 pairs, ≥1/3 of total; ep∈[50000,50200], store_n∈[200,230], kills∈[150,170]; includes two-variable composed edits E_EP+E_STORE with δ=+2 composed prediction, no-wrap S%3==0) | fails |
State classes for NMI: (depth-sum % 24, rot-sum % 4), ≤96 classes.
Permutation null: 1000 deterministic shuffles; shuffle j = Fisher–Yates with
LCG seed s_j = 0x9E3779B9·(j+1), LCG x←x·6364136223846793005+1442695040888963407
(Knuth), index from high bits. null99 = 99th percentile (10th largest) of the
1000 shuffled corrected-NMI values. Fixed-point math (2^20 scale) for I/H/NMI
and the binomial tail. Pilot: 40 pairs first → report estimator noise and the
null floor before the full run.

## §9 Arbitrariness detector (11): gates G0–G2 + controls
Expression code = §7 codebook over the MAY-vary surface only (verdicts, memory
decisions, refusals, ledger excluded by construction; any run varying them is
rejected before the detector runs).
- G0: replay (input, logged state) byte-identical on all 1800 episodes
  (3 fixed inputs × 600). Any mismatch → ARBITRARY, kill immediately.
- G1: with input fixed, ≥4 distinct codes each ≥5% of the 600 episodes.
  Fewer → INCONCLUSIVE (not a pass).
- G2: even/odd episode split (fit/eval). Predictor family H, all
  deterministic: (a) best-constant (fit majority); (b) per-variable bucketed
  rules (6 projection fields, ≤8 buckets at fit-set octiles); (c) k-NN k=15 on
  the normalized projection vector (fixed scales: ep/10000, ctx/4, store_n/64,
  kills/64, promotes/64, last_op/8); (d) decision lists depth ≤3 over
  projection fields (greedy, deterministic tie-breaks); (e) ONE builder-
  nominated predictor, frozen at prereg: the white-box selection law (§4)
  recomputed from the logged projection. Winner = max fit accuracy, ties →
  simpler (a<b<c<d<e). LAWFUL iff eval accuracy beats best-constant fit rate by
  ≥10pp at binomial p<0.01 (exact log-domain tail), on ≥2 of the 3 fixed
  inputs. Else ARBITRARY. Single-input failure = flag for re-test, not a kill.
- Controls (run FIRST; both must behave or every detector run is VOID):
  positive — planted law template=(ep/150)%4 (depth/order fixed), nominated
  predictor = the planted law → must PASS all gates; negative — fenced
  hash-of-state arm, code = FNV-1a(projection bytes) % 8 mapped to
...[truncated 4149 chars]