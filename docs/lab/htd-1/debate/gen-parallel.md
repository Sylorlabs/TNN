# HTD-1 DEBATE — Parallel / Iterative-Refinement Generation
## Slice: "diffusion family" and "all at once family" (non-sequential generation)

**Status:** DEBATE phase only. Nothing here is built. These hypotheses are proposed for preregistration and head-to-head testing against the autoregressive slice and each other.

**Standing constraints carried in:** pure Zag; zero randomness in any decision path (byte-identical reruns: same input + same logged state → byte-identical output); preregister with kill bars before building; test head-to-head, never minimize; evidence committed to `docs/lab/htd-1/` on the tnn-native-lab branch.

**Shared proxy corpora (read in place, never copied):** `~/workspace/tnn-lab/corpora/pg100.txt` (5.6MB Shakespeare), `~/workspace/tnn-lab/corpora/sqlite3.c` (9.5MB C).

---

## Why this slice matters

TNN has cognition but no decoder. Every existing TNN organ is *deliberative and discrete*: commit/refuse/rollback memory ops, petition-and-gate phase transitions, eliminative hypothesis checks, deliberate revision. Sequential autoregression would bolt a foreign, always-on token pump onto a system built for sparse, deliberate acts. The parallel family instead asks: can TNN generate the way it already thinks — draft something whole, then deliberately find what's wrong with it and fix only that? Micah's 20W question ("wake only relevant parts") is the efficiency bar this family must clear: refinement must touch a *shrinking fraction* of the tape per pass, or it loses to sequential generation on TNN's own terms.

**Measurable meaning of "generation working" (shared across this slice's hypotheses):** a generation mechanism works if, on the proxy tasks below, its output (a) satisfies the task's verifiable constraints at or above bar, (b) is produced deterministically (byte-identical across reruns from the same logged state), and (c) converges by rule — the process provably terminates with a bounded, preregistered edit budget. No decoder exists, so "quality" is always anchored to checkable ground truth (reconstruction exactness, compilability, constraint satisfaction), never to vibes.

---

## Hypothesis G-PA1 — "Flag-and-Fix": full skeleton draft + deliberative region refinement

**Mechanism sketch.**
1. *Initial draft:* one native pass emits a complete fixed-length draft (the "skeleton") onto a byte tape in a single deliberate act. The draft is intentionally coarse: it must satisfy *structural* constraints only (length, field layout, bracket balance — checkable by rule), not content quality. Implementation: a deterministic skeleton emitter — a fixed schema expander keyed by the prompt's deliberated intent record (no sampling; same intent record → same skeleton).
2. *Flagging:* a verifier sweep walks the tape once and *flags* regions (byte ranges), each with a typed defect code (e.g., `UNRESOLVED_REF`, `CONSTRAINT_VIOLATION`, `LOW_EVIDENCE`). Flagging is rule-based and deterministic: a fixed ordered list of checkers, first-match-wins per cell, so flag sets are reproducible.
3. *Refinement:* refinement acts are *deliberate memory-style commits*: for each flagged region, the reviser proposes a replacement span, the proposal goes through the existing commit/refuse/rollback path (the same machinery as deliberate memory ops), and only committed spans land on the tape. Regions are visited in a fixed deterministic order (e.g., left-to-right by defect severity rank, ties broken by tape offset).
4. *Convergence/stopping rule:* stop when a full verifier sweep flags zero regions, OR when the flag count fails to strictly decrease across two consecutive sweeps (stagnation → halt and report FAIL for that item), OR when a hard cap of P passes is hit. Oscillation guard: if the same region is committed >K times across passes, halt and mark the item `OSCILLATED`.
5. *Ledger records:* the skeleton (bytes + schema version), each flag set per sweep (region, defect code), each proposed span + commit/refuse/rollback verdict with the reason code, and the termination reason. Replay re-executes the flag→propose→commit chain to the exact final tape.

**Falsifiable predictions.**
- P1: On masked-span reconstruction, ≥90% of items converge in ≤3 sweeps with strictly decreasing flag counts.
- P2: Total cells touched across all passes grows sublinearly with draft length (refinement localizes), beating the autoregressive slice's linear pass cost on long drafts.
- P3: The stagnation halt fires on <5% of items; when it fires, the item's partial output is still structurally valid (skeleton guarantees).

**KILL BARS (preregistrable; any one firing kills the hypothesis).**
- KB1 (quality): masked-span reconstruction exact-match rate < 85% on the pg100 proxy at the fixed budget → KILL.
- KB2 (convergence): >5% of items need >5 sweeps, OR any item oscillates (same region committed >3 times) → KILL.
- KB3 (efficiency): mean cells-touched-per-output-byte ≥ 0.8× the autoregressive slice's on the same items → KILL (loses the 20W question).
- KB4 (determinism): any two reruns from the same logged state differ by even one byte → KILL (violates program law; no appeal).

**Proxy task + metric:** *Masked-span reconstruction* on pg100.txt: 1,000 passages, one 32–128 byte span masked per passage (mask positions fixed in the prereg file). Metric: exact byte-match rate of the reconstructed span + convergence stats (sweeps used, cells touched, oscillation count). Measurability: fully checkable against ground truth, deterministic.

**Must face head-to-head:** the autoregressive slice's best hypothesis (same proxy, same passages); G-PA2 (tests whether explicit flagging beats blind full-tape re-fill); G-PA4 (tests whether defect-driven order beats coarse-to-fine order).

---

## Hypothesis G-PA2 — "Blank-filling fixpoint": masked tape refined to convergence by rule

**Mechanism sketch.**
1. *Initial draft:* the tape starts as *all blanks* (a distinguished blank byte), except prompt-anchored cells (e.g., fixed prefix/suffix constraints, required keywords from the intent record) which are pre-filled. No skeleton structure is assumed.
2. *Refinement:* each pass is a *parallel* full-tape fill: every blank cell is proposed a byte simultaneously by a deterministic local rule (a pure function of the cell's fixed-size neighborhood + the intent record — think cellular-automaton style, but the rule table is learned/deliberated, not random). Filled cells may be *re-blanked* by the verifier if they violate a constraint (targeted un-filling, not wholesale).
3. *Convergence/stopping rule:* the tape is at fixpoint when one full pass changes zero cells AND the verifier reports zero violations. Stop also on: pass count > P (hard cap), or the changed-cell count fails to strictly decrease over two consecutive passes (stagnation → FAIL), or any single cell is re-blanked >K times (oscillation → FAIL). This is a genuine convergence criterion, not a patience heuristic: the state space is finite and the ledger proves termination-or-fail.
4. *Ledger records:* initial anchor cells, the neighborhood rule table version, per-pass changed-cell counts and the changed ranges (not every cell — ranges only, to keep the ledger proportional), re-blank events with violated-constraint codes, termination reason. Replay re-applies the rule table pass by pass.

**Falsifiable predictions.**
- P1: Fixpoint is reached (not merely capped) on ≥95% of proxy items — the local rule genuinely settles rather than churning.
- P2: Parallel passes give wall-clock advantage that *grows* with tape length vs sequential generation, even though per-pass work is full-tape.
- P3: Re-blanking concentrates on constraint boundaries (measurable: ≥70% of re-blanks within 8 bytes of an anchor or a previously violated cell).

**KILL BARS.**
- KB1 (quality): exact-match reconstruction rate < 85% on the same pg100 proxy → KILL.
- KB2 (convergence): <90% of items reach true fixpoint (zero-change pass) within P=8 passes, OR any cell re-blanked >3 times → KILL.
- KB3 (efficiency): mean total cell-writes per output byte ≥ 2× the autoregressive slice's cell-writes → KILL (parallel passes must not just burn the whole tape every round).
- KB4 (ledger proportionality): ledger bytes per output byte > 10× on the median item → KILL (a mechanism whose audit trail dwarfs its output fails TNN's replay economics).

**Proxy task + metric:** same masked-span reconstruction proxy as G-PA1 (shared passages, shared masks) for direct comparability; secondary metric: pass count to fixpoint and re-blank locality histogram. Measurability: exact-match vs ground truth + ledger-derived convergence stats.

**Must face head-to-head:** autoregressive slice (the core question: does parallel fixpoint beat sequential?); G-PA1 (flag-driven sparse refinement vs blind full-tape passes — the efficiency shootout); G-PA3 (fixpoint-of-one vs selection-among-many).

---

## Hypothesis G-PA3 — "Elminative drafts": parallel multi-hypothesis drafting with eliminative selection

**Mechanism sketch.** This hypothesis weaponizes what TNN already proved: eliminative hypothesis logic (debate trial: 180/180 false claims revised, 0 true ones corrupted).
1. *Initial drafts:* N complete candidate drafts are emitted *in parallel* (N fixed in prereg, e.g., N=4), each from a different deterministic drafting policy (e.g., skeleton-first, anchor-outward, constraint-satisfaction order, template-instantiation). Policies are fixed rule sets, not samples — same intent → same N drafts.
2. *Elimination rounds:* candidates face the eliminative battery — each must survive checkable challenges derived from the task constraints (reconstruction: does the span match verifiable anchors? code: does it compile? does it satisfy each named constraint?). A candidate is *eliminated* when it fails a challenge no surviving candidate has failed (genuine discriminating evidence, mirroring the debate trial's world-evidence rule). Eliminated candidates' tapes are frozen as evidence, not deleted.
3. *Refinement within survivors:* surviving candidates may each take *one* deliberative repair pass per round (same commit/refuse/rollback path as G-PA1), then face the battery again.
4. *Convergence/stopping rule:* stop when exactly one candidate remains (winner committed to output), or when a round eliminates zero candidates AND zero repairs commit (all survivors stable → tie-break by fixed deterministic rank: fewest verifier flags, then lowest tape offset of first flag, then policy index — no randomness, fully preregistered), or when rounds > R. If zero candidates survive a round → item FAIL.
5. *Ledger records:* all N drafts, every challenge + per-candidate verdict, elimination events with the discriminating evidence cited, repair commits, tie-break computations, final selection reason. This ledger is the point: selection is *provably* evidence-driven, auditable like the debate trial.

**Falsifiable predictions.**
- P1: The eliminative battery picks the correct reconstruction more often than any single drafting policy alone (selection adds measurable value: winner correctness > max individual policy correctness by ≥5 points).
- P2: ≥80% of items resolve by genuine elimination (not tie-break) — the challenges actually discriminate.
- P3: The winner's ledger shows the *losing* drafts were eliminated for cited, checkable reasons in ≥95% of elimination events (no hand-waving).

**KILL BARS.**
- KB1 (quality): winner exact-match rate < 88% on the pg100 proxy → KILL (must beat single-policy baselines to justify N× work).
- KB2 (selection value): winner correctness − best-single-policy correctness < 3 points → KILL (if selection adds nothing, the machinery is theater).
- KB3 (convergence): >10% of items reach the round cap R=6 without a single survivor, OR >20% resolved by tie-break rather than elimination → KILL.
- KB4 (efficiency): total cell-writes across all N drafts + rounds > 4× the autoregressive slice's → KILL (parallel hypotheses must pay for themselves; ties directly to the 20W question).

**Proxy task + metric:** masked-span reconstruction (shared passages) as the common yardstick; plus a *discriminating-constraint* proxy on sqlite3.c: generate a C fragment satisfying 5 named checkable constraints (balanced delimiters, no undefined identifiers from a fixed allowlist, terminates with `;`, etc.) — metric: constraint-satisfaction rate of the winner vs best single policy. Measurability: exact-match + constraint checks, all rule-verifiable.

**Must face head-to-head:** autoregressive slice (is N-parallel deliberate selection worth it vs one careful sequential pass?); G-PA1 and G-PA2 (single-refined-draft vs many-drafts-selected — the fundamental architectural fork of this slice); the debate-trial evidence standard is the internal control (selection must meet the same auditability bar the belief-revision trial set).

---

## Hypothesis G-PA4 — "Frozen checkpoints": coarse-to-fine passes with level freezing

**Mechanism sketch.**
1. *Pass structure (fixed, preregistered):* L1 emits a coarse outline (section markers / block skeleton — a low-resolution tape, e.g., 1 marker byte per 32 output bytes). L2 expands each marker into a mid-resolution span. L3 fills spans to full byte resolution. Each level's emitter is deterministic given the previous level + intent record.
2. *Freezing:* after each level, a verifier certifies the level against level-appropriate constraints (L1: coverage — every required element has a marker; L2: span budgets sum correctly; L3: full constraint battery). A certified level is *frozen*: later passes may not alter its bytes, only expand within the budgets it set. Freeze violations are ledgered as faults.
3. *Deliberative repair:* if a level fails certification, repair is confined to that level (re-emit the failed markers/spans only — never a full restart), through commit/refuse/rollback. Max Q repairs per level.
4. *Convergence/stopping rule:* the process terminates when L3 certifies, or when any level exhausts Q repairs (item FAIL — no infinite regress downward), or when a frozen level's budget proves unsatisfiable at expansion (ledgered as `BUDGET_FAULT`, item FAIL). Termination is structural: at most 3 levels × (1 emit + Q repairs) acts.
5. *Ledger records:* per-level tapes, certification verdicts with the constraint list version, freeze events, per-level repair commits, budget-fault records. Replay re-expands level by level.

**Falsifiable predictions.**
- P1: Freezing cuts rework: ≥70% of L3 repairs are confined to span interiors with zero marker movement (coarse decisions are stable).
- P2: Budget faults are rare (<3% of items) — coarse levels can actually plan satisfiable budgets, i.e., hierarchy is expressive enough.
- P3: Total acts (emits + repairs) scale with *defect count*, not output length — long clean outputs cost ~3 acts.

**KILL BARS.**
- KB1 (quality): exact-match reconstruction < 85% on the shared pg100 proxy → KILL.
- KB2 (hierarchy value): L1 outlines certified on first attempt < 70% of items → KILL (if the coarse level can't plan, the hierarchy is decoration).
- KB3 (frozen-level fault): any freeze violation (a later pass altering frozen bytes outside the repair path), OR budget-fault rate > 5% → KILL.
- KB4 (repair confinement): >15% of items need repairs at ≥2 levels (defects cascade across levels instead of localizing) → KILL — the hierarchy fails its one job.

**Proxy task + metric:** shared masked-span reconstruction proxy for cross-hypothesis comparison; hierarchy-specific metric: repairs-per-level histogram + freeze-violation count (must be zero) + budget-fault rate. Measurability: exact-match vs ground truth; level stats from the ledger.

**Must face head-to-head:** autoregressive slice (does planned hierarchy beat sequential care?); G-PA1 (defect-driven flat refinement vs level-driven hierarchical refinement — which localizes work better per the 20W question?); G-PA2 (structured levels vs emergent fixpoint).

---

## Cross-cutting preregistration notes (for the build phase)

- **Shared proxy spec** (to be frozen before building): 1,000 pg100 passages, mask spans 32–128 bytes, mask positions from a fixed published list; sqlite3.c constraint-generation item set (200 items × 5 named constraints). All four hypotheses + the autoregressive slice run the *identical* item lists.
- **Determinism gate (program law, applies to all):** every hypothesis must demonstrate byte-identical reruns (same input + same logged state) on 100/100 sampled items before its quality numbers count. A determinism failure is not a kill bar — it is disqualification.
- **Common instrumentation:** cells-touched, cell-writes, passes/sweeps/rounds used, ledger-bytes-per-output-byte, termination reason per item. The 20W question is scored on cells-touched and cell-writes, head-to-head, on identical items.
- **Anti-shopping rule (carried from the felt re-trial):** refinement budgets (P, K, Q, R, N) are fixed in prereg; a hypothesis may not adapt its budget per item. Stagnation/oscillation halts are FAILs for the item, not invitations to try harder.

## Head-to-head matrix (this slice)

| Matchup | Decides |
|---|---|
| Each G-PAx vs autoregressive best | Does any parallel family beat sequential at all? |
| G-PA1 vs G-PA2 | Flag-driven sparse repair vs blind full-tape fixpoint (efficiency shootout) |
| G-PA1 vs G-PA4 | Flat defect-driven order vs hierarchical level order |
| G-PA2 vs G-PA4 | Emergent convergence vs planned convergence |
| G-PA3 vs G-PA1/G-PA2 | Selection-among-many vs refinement-of-one (the architectural fork) |
| G-PA3 vs debate-trial standard | Does draft selection meet TNN's own eliminative-evidence bar? |

---

## Steelman: the strongest objection to parallel/refinement generation for TNN

A deliberate system earns its determinism by making every act discrete, justified, and ledgered — and refinement is where that discipline goes to die: each "fix what's wrong" pass is an invitation to keep editing until the output *looks* right, which smuggles a maximizer (a hidden reward function wearing a lab coat) into a program whose law bans exactly that, and whose honest-failure rule demands FAIL-with-evidence instead of polishing. Worse, parallelism multiplies the work the 20W question forbids: N drafts or full-tape sweeps wake the whole mind to produce what one careful sequential pass might, and every pass fattens the audit ledger until replay costs more than generation. The convergence criteria meant to bound this are themselves decision paths — "which region next," "is this good enough" — that must be justified without randomness and without becoming the very reward signal TNN was built to escape. If refinement cannot prove, per item, that it stopped for a *reason* rather than from exhaustion, it is not deliberate generation; it is gradient descent with better paperwork.
