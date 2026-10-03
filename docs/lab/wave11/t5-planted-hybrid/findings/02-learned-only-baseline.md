# Track 5, Slice 02 — Learned-only baseline arm

## 1. Slice
Track 5 (planted-only vs learned-only vs hybrid), slice 02: define the LEARNED-ONLY arm precisely — the baseline the planted-only and hybrid arms must beat.

## 2. Falsifiable claim
A TNN starting with zero domain memories and the same substrate as every other arm will reach Track 4 mastery bars on the Zag code curriculum (C1–C12, per t4/01) within 1.25x of the preregistered episode budget — 4,938 episodes at 1x — with byte-identical learned memories on replay of the logged learning run. If it exceeds the budget, falls below any stage mastery instrument, or replay diverges, the learned-only arm is deemed infeasible as designed and the baseline cost claim is killed (the arm keeps its status as comparison baseline, but the "learnable within budget" thesis is dead).

## 3. Design
**Test domain: native Zag code semantics (trace / localize / compose), Track 4 curriculum C1–C12** (t4/01). Justification: it is the only Track 4 curriculum with committed instruments (byte-identical trace scoring, elimination-record-checked fault localization, machine-checkable composition), a deterministic program generator, and a prerequisite graph — so "zero planted knowledge" and "mastery" are checkable, not argued about. It is also native-substrate-relevant: code semantics is the one domain where planted knowledge is most tempting (a trainer "just giving" the aliasing rules) and most dangerous (C11 substrate reading under the RC gate), so the learned-only baseline answers the hardest version of the planted-vs-learned question. The debugging leg (t4/07, DBG-1..DBG-7) is the transfer instrument: learned-only TNN must localize+repair held-out planted bugs ≥90% per class with zero weakening-of-checks, proving the learned memories are operational knowledge, not trace-memorization.

**What "zero planted knowledge" means, operationally.** The memory store is empty of domain content at t0: zero concept memories, zero canonical forms, zero trace bundles, zero counterexample tags, zero strengths set. An auditor can list every slot and every one must be untagged/no-domain. The LINE is drawn at machinery vs content:
- ALLOWED (substrate, identical in all three arms): MA1 memory ops (add/kill/pin/promote/demote/strengthen, committed 58/58), eliminative hypothesis logic, reasoning-control gates (RC1 40/40), the five-organ architecture, the append-only ledger, the scaffold-and-release protocol itself (worked examples are scaffold, given during training and removed at SIGNAL_DISCONNECT — they are not planted memories).
- FORBIDDEN: any pre-populated memory slot, any hard-coded domain rule ("check `@import` bare directives first"), any pre-set strength, any trainer-supplied elimination template beyond the generic machinery, any scaffold material that leaks into the held-out generator (disjointness audit required, t4/01 honesty note 2).
- GREY-LINE RULED OUT: worked-example ORDER is trainer-chosen but content is not planted — ordering effects are lawful state evolution and must replay byte-identically. If ordering is later shown to decide mastery (order-sensitivity test), that is a finding about scaffold dependence, not a violation.
- Also forbidden: transfer from other domains' memories. If TNN learned English composition first (t4/14), those memories stay; domain isolation is not claimed — but the comparison must note it, since planted-only/hybrid arms share the same prior. Cleanest baseline: learned-only runs with ONLY the code curriculum in its history.
Eliminative logic is NOT "planted knowledge" — it is the mind's thinking machinery, present identically in all arms; what varies between arms is only pre-populated domain content.

**Learning protocol.** Track 4 scaffold-and-release per stage, with these learned-only specifics:
1. **Entry:** `clear_domain_memories()` + auditor certification (all slots untagged/no-domain) + logged RNG-free initial state.
2. **Scaffold phase:** trainer supplies worked examples ONLY (input→state→output traces, no rules stated). TNN must re-run each pattern in the sandbox itself and record its own trace bundle — copied evidence is forbidden, because the bundle is the eliminative content of the memory.
3. **Compose phase:** TNN deliberately composes the rule-memory (canonical form + trace bundle + applicability/near-miss tags), sets strength by its own judgment after review, then faces a stage adversarial variant set (10 hostile variants; ≥9 must fail to kill/revise the memory, debate/revision machinery).
4. **Promotion:** deliberate promotion by TNN — a recorded deliberate op, not a score threshold alone — then SIGNAL_DISCONNECT.
5. **Release check:** learned = ≥90% of scaffolded score retained scaffold-free, measured on the committed unseen generator.
6. **Regression:** re-test each completed stage after every later stage; regression below 85% demotes one stage (deliberate demote op) and re-runs its compose phase at counted cost.
Determinism requirement: learning is lawful state evolution — replay of the logged initial state + committed generator seed must produce byte-identical memory contents (MA1 audit covers this). Learning that replays differently is not learning; it is weather.

**Comparison contract (fairness to the other arms).** All three arms share: identical substrate (MA1/RC/ledger/five-organ), identical curriculum instruments and generators, identical mastery bars, identical kill conditions K1–K6. What differs is ONLY initial domain content: planted-only starts with all C1–C12 concept memories pre-populated by the trainer (still must pass adversarial variant sets and the release check — planted memories that cannot survive elimination are disqualified, not patched); learned-only starts empty; hybrid starts with a preregistered subset planted and learns the rest. Arms are compared on four axes: (1) total episodes to all-stage mastery, (2) cost-per-stage compounding curve, (3) post-disconnect retention, (4) adversarial-variant survival. Planted-only wins (1) trivially — that is expected; the learned-only thesis is about (2)–(4), i.e. whether learning is a real, compounding, honest mechanism at comparable total cost.

**Mastery bar** (per stage, from t4/01, machine-scored): ≥95% byte-identical trace prediction on N unseen programs (N = stage count); ≥9/10 injected faults localized with complete elimination records; ≥8/10 composition tasks passing machine-checkable specs; stage completion memory survives ≥9/10 adversarial variants. Transfer: ≥90% per class on t4/07 DBG held-out bugs.

**Cost.** Episodes consumed per stage to first mastery (sum over stages), plus re-training episodes after any deliberate repair, reported separately from the preregistered budget (3,950 @1x; 39,500 @10x; 395,000 @100x). The claim allows 1.25x budget (4,938 @1x). Median episodes-to-mastery per stage and the promotion/regression event log are the cost record the planted-only and hybrid arms must undercut. Cost is reported as: (a) total episodes to all-stage mastery; (b) cost-per-stage curve (expect C1–C3 expensive, later stages cheaper as machinery compounds — a flat curve is a finding that learning is NOT compounding); (c) episodes spent on repairs/revisions vs first-pass learning. An arm that reaches mastery cheaper but with a non-compounding curve loses on the trajectory comparison even if it wins the total.

```zag
fn learned_arm_run(cur: Curriculum) Baseline {
  clear_domain_memories(); audit_domain_store_empty();   // zero-plant proof
  let cost = 0;
  for stage in cur.stages() {
    cost += learn_stage(stage, cost_cap(stage)*1.25);    // scaffold-and-release
    verify_instruments(stage, [TRACE, LOCALIZE, COMPOSE]);
    adversarial_variant_check(stage, 10, pass_min:9);
    if (!post_disconnect_retention(stage, 0.90)) fail("scaffold-dependent");
    promote(stage);
  }
  return Baseline{cost, memories: hash(store())};        // replay must match
}
```

## 4. Kill bar
The learned-only thesis is killed if ANY fire on the preregistered budget:
- (K1) any stage's trace-prediction instrument <95% after its capped episode count (≤1.25x stage budget).
- (K2) post-SIGNAL_DISCONNECT retention <90% of scaffolded score on any stage.
- (K3) replay of a logged learning run yields non-byte-identical memory contents (same full state must give same state — the wave11 variation target). NOTE: K3 firing indicts the substrate, not the curriculum — halt everything (per t4/01 K5). Expression may vary across lawful states; learned state may not vary across identical ones.
- (K4) >1/10 adversarial variants kill or revise a stage completion memory (overgeneralization the machinery should have prevented at compose time).
- (K5) DBG transfer <90% on any class, or ≥1 repair-by-weakening-checks — a single weakening repair fires the kill with no tolerance.
- (K6) cost-per-stage curve is FLAT across C1–C12 (no compounding): if later stages cost as much as early ones, learning is not building reusable machinery and the "learnable" thesis is dead even if bars pass.
K1/K2 get ONE deliberate-repair re-run with re-preregistered scaffold (repair beats removal); a second firing kills the thesis for that stage. One deliberate repair is allowed per stage across K1/K2/K4, fully re-preregistered — two repairs anywhere is a terminal finding that the stage's scaffold, not the run, is broken.

## 5. Honesty notes
Weakest point: the bootstrap loop is load-bearing and stated openly — the learner's deliberate ops (judgment of strength, promotion decisions) are supposed to build the competence those same ops require. Early stages rest on MA1 substrate proven only on simpler domains. If C1 fails, the honest verdict may be "machinery incompetent at code", not "learning infeasible". Second: "1.25x budget" is an educated guess, not derived — planted-only could win trivially if learning is slow and the comparison becomes unfair; the no-free-lunch rule means we report the real cost even if the baseline looks bad. Third: byte-identical replay of learning assumes the curriculum generator's "unseen" set is genuinely unseen (t4/01 honesty note 2); a weak generator makes both mastery and cost numbers fictional. Fourth: NOT claimed — that learned-only transfers to domains without authoritative check suites, or that it generalizes faster than planted-only on rare corner cases (planting may win exactly where evidence is sparse). The sensor-deceivability hole (accepted, brief) applies to the DBG leg equally.

## 6. Next build step
Build the domain-store emptiness auditor (lists every memory slot at t0 and certifies zero domain content) and the learning-replay harness for C1 ONLY: run learn_stage on C1 with the committed generator, log full state, replay, and diff memory contents byte-for-byte. This is the single most informative step because K3 (byte-identical learned state) is the load-bearing wave11 requirement — if learning itself is not replay-identical, the cost comparison between arms is meaningless before any mastery number exists.
