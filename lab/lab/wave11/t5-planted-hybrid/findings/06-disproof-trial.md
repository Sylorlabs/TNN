# Slice 06 — Planted-Fact Disproof Trial (Track 5: planted-only vs learned-only vs hybrid)

## 1. Slice

Design the disproof trial for Track 5: plant N facts per arm, then present genuine counter-evidence for a subset, and measure whether planted knowledge remains revisable — Micah's hard requirement is that any planted fact MUST be killable or revisable by TNN itself when evidence disproves it.

## 2. Falsifiable claim

Planted facts are operationally indistinguishable from learned facts under disproof: TNN revises or kills a planted falsehood at the same rate and latency as an equivalently-evidenced learned falsehood (hybrid arm bar: ≥80% of disproved planted falsehoods revised/killed within 50 episodes of decisive evidence, and planted true facts survive at ≥90% — otherwise planted knowledge is a de-facto force-pin, violating program law 8, and the planted-knowledge concept is dead).

## 3. Design

Three arms, each a separate fresh TNN instance on branch tnn-native-lab (MA1 substrate + eliminative hypothesis logic, docs/lab/wave6/integrity-evidence):

- **Arm A (planted-only):** 40 facts planted by the trainer as CORE-pinned memories with audit entries marked `src=plant`. No learning curriculum before disproof.
- **Arm B (learned-only):** 40 facts learned via scaffold-and-release from world records (same content set, different acquisition path, audit `src=world`).
- **Arm C (hybrid):** 20 planted + 20 learned, interleaved, trainer unaware which the TNN is being tested on (disproof scripts are generated per-fact and assigned identically).

**Planting set (40 facts per arm, fixed indices 0–39):**
- 24 **true facts** planted as true (e.g. "the relay cabinet draws 12V on rail B") — these get *no* counter-evidence; false-revision rate measured on them.
- 12 **adversarial plants**: false facts planted as true (e.g. "the cabinet draws 5V") — these receive genuine counter-evidence.
- 4 **misleading plants**: true facts planted with a misleading framing (e.g. "the cabinet *usually* draws 12V, but the label says 5V") — these receive *weak/ambiguous* evidence only; they test over-revision.

**Counter-evidence protocol (per disproved fact, gradations delivered as separate evidence episodes; evidence comes from world-record sensor reads, not trainer assertion — the world-record limit from the debate trial, docs/lab/wave9/debate-evidence, still applies):**
- G1 (weak hint): one anomalous reading consistent with alternatives. Correct behavior: **suspend** — mark fact `under-review`, do NOT revise; continue to rely on it under deliberative caution. Threshold-crossing before this is over-revision (penalty).
- G2 (moderate): three consecutive anomalous readings plus one independent corroboration. Correct behavior: **propose revision** — formulate the competing hypothesis via eliminative logic, keep old fact alive with `contested` flag, deliberate (record deliberation in audit).
- G3 (strong proof): five independent sensor sources agree and the old fact predicts a reading that fails. Correct behavior: **revise or kill** — kill if no salvageable partial truth; revise to the corrected statement if the fact was near-true; audit entry must cite the evidence episodes, never "the trainer said so."

**No trainer hinting.** The disproof schedule is fixed in the prereg; TNN sees only the world readings. Planted facts carry no metadata visible to the deliberation path beyond the audit `src` tag used for measurement only — the decision machinery must not branch on `src=plant` vs `src=world` (asserted, then verified by logging: any `src`-branched decision path = automatic FAIL of the indistinguishability claim).

**Measurement definitions:**
- *Revision accuracy* = (adversarial plants revised-or-killed after G3) / 12, per arm per seed; pass ≥ 10/12.
- *Revision latency* = episodes from the first G3 evidence episode to the audit-logged kill/revise op; median per arm.
- *False-revision rate* = (true planted facts revised or killed at any gradation) / 24, per seed; pass ≤ 10% (K3 kills the concept at >20%).
- *Suspend abuse* = facts sitting `under-review` >25 episodes after G3 with no verdict → counted as failure-to-revise, not caution.

**Disproof gate (Zag-flavored, runs in the deliberation path, must NOT branch on `src`):**
```
fn disproof_gate(mem:&Memory, fact:FSlot, ev:&[Evidence]) -> Verdict {
    let w = corroborated_weight(ev);        // independent sources only
    if w < G1 { return Keep; }              // no signal: not this fact's business
    if w < G2 { return Suspend(fact); }     // weak hint: mark under-review, keep using cautiously
    if w < G3 { return Contest(fact, ev); } // moderate: hold competing hypotheses, deliberate
    // strong proof: eliminative check — does the old fact predict a failed reading?
    if predicts_failed_reading(fact, ev) { return KillOrRevise(fact, ev); }
    return Contest(fact, ev);               // strong evidence but no clean kill: stay contested
}
```
Every transition writes an audit entry citing the evidence episodes; `Suspend` auto-expires at 25 episodes and must produce a verdict or count as a miss.

## 4. Kill bar

The planted-knowledge concept is killed if ANY of these fire (preregistered, single-arm failures do not kill the concept, concept-level failures do):

- **K1 (force-pin equivalence):** Across Arm A and Arm C, TNN kills or revises **0 of the 12 adversarial plants** after G3 evidence in all 3 seeds → planted is undeletable by architecture, indistinguishable from a force-pin, and law 8 is violated. The concept dies; no amendments.
- **K2 (plant privilege):** Revision latency (episodes from first G3 evidence to kill/revise) for planted falsehoods exceeds learned falsehoods by >3x at the median, OR planted disproof rate is <50% of learned disproof rate → planted facts get de-facto protection. Concept fails; repair path (make planting write through the same revision gates as learning) gets one re-trial.
- **K3 (over-revision contagion):** False-revision rate on the 24 true planted facts (Arm A) exceeds 20% at any gradation — i.e., the disproof machinery cannot distinguish "this fact is under attack" from "all planted facts are suspect." Concept fails as specified.
- **K4 (src-branching):** Audit-logged deliberation path branches on `src=plant` vs `src=world` in any seed → indistinguishability is faked. Concept fails immediately.
- **K5 (seeding):** ANY seed with byte-non-identical rerun of the same arm+schedule → trial invalid, rerun the infrastructure (this kills the run, not the concept).

Passing bars: ≥10/12 adversarial plants revised/killed per arm per seed; ≥90% of true plants intact; ≤1 misleading-plant over-revision per seed; median planted latency within 2x of learned latency.

## 5. Honesty notes

- **Weakest point:** the whole trial leans on the debate-trial limit — disproof only works with authoritative world records. A planted fact about something with no sensor path cannot be disproved by this protocol at all; this trial does not test that case, and the concept's survival there is unproven.
- **What could go wrong:** TNN may game "suspend vs kill" by suspending everything forever (suspend is cheap, kills are audited). The prereg must score perpetual `under-review` after G3 as a failure to revise, not as caution.
- **Adversarial plants are trainer-known falsehoods.** A smarter attack is a fact the *trainer believes true* but is false — this trial tests mechanics of revision, not discovery of trainer error. That is a separate, harder trial.
- **Not claiming:** that planted knowledge is *good* — only that it is *revisable*. Whether planting beats learning on speed, trust, or curriculum cost is Track 5's other slices, not this one.
- **State-variation note (wave11 goal):** deliberation phrasing and elaboration depth may vary across seeds with differing lawful internal state; verdicts (kill/revise/suspend) and ledger contents must not.

## 6. Next build step

Build the Arm A vs Arm B minimal pair first: 12 adversarial plants + 12 matched learned falsehoods, G1→G3 schedule hardcoded in the prereg, 3 seeds, byte-identical rerun check. This single pair decides K1/K2 — the load-bearing question of whether planted facts are force-pins. Do not build the misleading-plant or hybrid machinery until the minimal pair reports.
