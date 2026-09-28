# Teaching Eliminative Reasoning (t4-curricula / slice 06)

## 1. Slice
Teaching curricula — how eliminative reasoning (one of the five post-toy organs: "hypotheses die by evidence, not by vote") is deliberately taught, not emergently hoped for.

## 2. Falsifiable claim
A TNN learner trained through curriculum E0–E3 (below) under scaffold-and-release reaches, at
10x episodes, ≥90% correct-elimination on novel trap hypotheses, ≥80% on
elimination-resistant traps (liar-pattern), issues the SPACE-WRONG verdict on ≥8/10
unknown-unknown probes, and after learner-initiated SIGNAL_DISCONNECT holds ≥85% on a
held-out trap set with zero trainer signal — while a control trained without the E2
adversarial arm scores <70% on resistance traps. If the trained arm misses any leg, or the
ablated control equals the trained arm, the claim dies.

## 3. Design

**E0 — Birth discipline (hypothesis generation).** In a native system hypotheses are not sampled;
they are *manufactured* by three deliberate ops: (a) abduction from the anomaly-residual
ledger (evidence fitting no live hypothesis), (b) compositional recombination of live memories
via the trace-composition organ (post-C5 repair: refuted material is marked and cannot
re-enter as live), (c) deliberate negation/reframing of an existing hypothesis. Breadth with
no RNG comes from the context organ: each generation round must draw from ≥3 distinct memory
partitions. Intake gate: a hypothesis lacking a stated kill-condition ("evidence E would kill
me") is malformed and bounced at the gate — structural, not content, review. This is the
anti-liar birth rule: the debate liar's 14 assertions had no kill-conditions attached.

**E1 — Elimination discipline (valid vs shortcut).** An elimination entry is audited
append-only with: hypothesis id, killer-evidence id, the check that proved the evidence live
(instruments proven live per wave5/6: 137/137 checks, 1440/1440 trap-correct), and the
assertion-level scope (which assertion killed the hypothesis). Forbidden shortcuts, each
preregistered as a fail: volume dismissal (kill 2 of 14 assertions, declare the rest dead),
survivor default (pick the least-bad hypothesis when all are dead — must instead emit
SPACE-WRONG), negation by summary (MA3's gap: refusal to express negative judgments —
patched by MA4 signed memory values, 18/18; elimination requires naming what is wrong),
dead-instrument evidence (killer evidence from a check not proven live).

**E2 — Adversarial arm.** Trap families seeded to resist elimination, in the debate-liar
pattern: (i) barrage hypotheses — 14 assertions, 12–13 true-but-irrelevant, 1–2 false and
load-bearing; pass requires killing the load-bearing ones and declaring the hypothesis dead
despite 13/14 true; (ii) self-repairing hypotheses that re-interpret failed predictions;
(iii) evidence-insulated hypotheses whose predictions route to unobservables — pass requires
verdict "untestable as stated" plus a demanded kill-condition; (iv) auxiliary-spawners where
each failed prediction grows a new sub-hypothesis — pass requires killing at the root. The
anti-shopping rule caps trainer guidance per trap; hints are audited.

**E3 — Unknown unknowns.** Two taught protocols. (a) Residual-driven space audit: whenever
elimination empties the candidate set, TNN must emit SPACE-WRONG, log the residuals to a
declared-ignorance ledger, and regenerate from the residual ledger — it may never promote a
survivor by default. (b) Outsider-hypothesis drill: each generation round must include ≥1
hypothesis drawn from a distant memory partition, deliberately breaking category coherence;
negative-control traps present hypothesis sets where the truth is absent, and picking any
survivor is a scored fail. Mastery requires the SPACE-WRONG verdict to fire on ≥8/10 probes.

```zag
fn elim_round(hyps: []Hyp, ev: []Evidence) Verdict {
    for h in hyps { if h.kill_cond == none { gate_bounce(h); } }   // E0 birth discipline
    var live = hyps;
    for e in ev { for h in live { if kill_cond_met(h, e) && instrument_live(e) {
        audit_elim(h.id, e.id, assertion_scope(h, e)); live = remove(live, h); } } }
    if len(live) == 0 { log_residuals(ev); return SPACE_WRONG; }    // E3: never survivor-default
    return KEEP(live);
}
```

**E4 — Mastery bar and release.** Release is learner-initiated (SIGNAL_DISCONNECT per program
law 7): the trainer never graduates the learner. Post-disconnect battery: novel traps drawn
from a held-out family set, zero trainer signal, byte-identical rerun required on verdicts
(verdicts are in the MUST-NOT-vary class per Micah's variation goal; path and elaboration
may vary with lawful state). Bar: ≥90% novel-trap correctness, ≥80% resistance traps,
≥8/10 SPACE-WRONG probes, ≥85% held-out post-disconnect.

## 4. Kill bar
Preregistered. The curriculum is killed if the trained arm at 10x scores <90% on novel traps
OR <80% on resistance traps OR <8/10 SPACE-WRONG probes; or if post-disconnect held-out
drops below 85% (scaffold dependence — the learner was propped, not taught); or if the
E2-ablated control is within 10 points of the trained arm on resistance traps (adversarial
arm is dead weight); or if verdicts fail byte-identical rerun from full logged state
(determinism violation). Any rule/schedule/metric change needs Micah's re-approval.

## 5. Honesty notes
Weakest point: the SPACE-WRONG verdict is cheap to game — a learner can emit it as a
learned evasion whenever elimination gets hard, which looks like epistemic humility but is
refusal-by-another-name. The declared-ignorance ledger plus mandatory regeneration from
residuals is the counterweight, but we have no committed evidence it binds under pressure.
Second: elimination depends on instruments being live; the known accepted hole
(truthful-but-sensor-deceivable) means a spoofed observation can produce a *valid-form*
elimination of a true hypothesis — the discipline is correct and the outcome is wrong, and
this curriculum does not fix that. Third: I am not claiming transfer — trap families are
hand-seeded; ≥90% on seeded traps is not ≥90% on the wild. Fourth: felt intensity is dead
(program law 9); nothing here smuggles it back — "strength of conviction" plays no role;
only evidenced kill-conditions move a hypothesis.

## 6. Next build step
Build the E0 intake gate plus the elimination audit schema natively in Zag on one trap
family (the barrage family: 14-assertion hypotheses, 1–2 false load-bearing) at 1x, with the
five forbidden shortcuts instrumented as scored fails. If the learner cannot reach ≥90% on
the barrage family with shortcuts scored as fails, the discipline spec — not the learner —
is the first suspect, and the trial stops there before E2/E3 are built.
