# TNN Composition Audit — Batched Deep Analysis

## Q1. Conflict-Class Rulings

| Conflict Class | Recommended Resolver | Deciding Failure Mode | Steelmanned Counter-Case |
|---------------|---------------------|----------------------|-------------------------|
| **(a) Memory-substrate pin vs revision-organ kill/revoke** | **Hybrid: PYCC-extended** | Silent corruption via pin override. A pin represents committed epistemic weight (human force-pin = ground truth anchor; learned pin = high-confidence stable belief). Allowing unconditional revoke creates the failure: attacker issues REVOKE against pinned ground truth → ledger accepts → TNN now contradicts its own foundation without audit trail explaining *why* the pin was overcome. Pure figure-it-out risks infinite deliberation (pin says keep, revoke says kill, no tiebreaker). | **Policy steelman**: Rigid "pins are absolute" prevents any self-correction of bad pins. Real failure: human force-pins a now-falsified claim at T0; by T100 TNN has corroborated contradiction from 50 independent sources, but the pin locks the false belief forever. This turns force-pins into epistemic landmines. The PYCC compromise (corroborated contradiction suspends pin, single-source does not) is correct but must extend to revoke: **revoke succeeds iff it carries corroborated contradiction weight ≥ pin weight**. This requires provenance + weight ledgering (see Q2 principle #2). |
| **(b) Consolidation promoting provisional that hypothesis-logic just contradicted** | **Figure-it-out deliberation with circuit-breaker** | Leakage of falsified provisional into committed KB. Pure policy ("contradiction blocks promotion, full stop") has the failure: hypothesis-logic contradicts provisional P based on evidence E1; meanwhile consolidation has independent corroborating evidence E2, E3, E4 for P. Policy kills P outright → TNN loses a true belief because one organ spoke first. Figure-it-out deliberation weighs the contradiction (1 source) against the corroboration (3 sources), ledgers the conflict, and either promotes-with-caveat or holds provisional pending tiebreak. Circuit-breaker: if deliberation cycles >N rounds without convergence, escalate to human/governance (do not silently pick a winner). | **Policy steelman**: Figure-it-out risks "arguing yourself into" a false belief. Real failure: hypothesis-logic contradicts P correctly (P is false), but consolidation's E2/E3/E4 are all downstream of a shared false premise Q. Figure-it-out sees 3-vs-1 and promotes P, entrenching the error. Defense: **contradiction from hypothesis-logic must trace its provenance**; if it's corroborated (independent lines of elimination), it outweighs sheer vote-count from consolidation. This is not pure policy (no rigid "contradiction always wins") but principled deliberation: **epistemic independence of evidence** is the tiebreaker, not count. If independence is unknown, hold provisional (do not promote). |
| **(c) Recall/composition surfacing quarantined/provisional trace as premise** | **Figure-it-out with mandatory provenance-tagging** | Silent premise contamination. Pure policy ("quarantined content never surfaces") has the failure: a quarantined claim C was quarantined at T0 due to single-source doubt; by T50, independent evidence rehabilitates C, but policy keeps it invisible → TNN cannot use now-valid reasoning. Pure figure-it-out ("surface everything, let deliberation sort it") fails differently: recall surfaces quarantined C as premise in new deliberation D without flagging its status → D's conclusion inherits the quarantine taint silently → epistemic debt compounds across composition. **Correct resolution**: recall MUST surface provisional/quarantined traces (else you cripple the machine's ability to re-evaluate), but they carry **mandatory provenance tags** in the composition. Downstream deliberation sees "this premise is provisional/quarantined" and adjusts confidence accordingly. Ledger records the dependency: if C's status changes (promoted or killed), all conclusions depending on C are flagged for re-evaluation. | **Policy steelman**: Mandatory tagging creates availability collapse under deep composition. Real failure: a 10-layer inference chain where layer 3 uses a provisional P → every downstream conclusion carries the "tainted by provisional" tag → by layer 10, every conclusion is "provisional-dependent" even though layers 4-10 have independent corroboration. TNN becomes paralyzed, unable to commit anything. Defense: **provenance is not a permanent stain**; it's a recomputable dependency graph. When P is promoted, the ledger can replay the downstream chain and upgrade dependent conclusions that now rest on committed premises. The cost is replay, not permanent paralysis. Availability vs integrity: **integrity failure is silent corruption (undetectable until catastrophic); availability failure is detectable loudness (TNN says "I need more work to commit this")**. Under the human's laws (scaffold-and-release, no lying), integrity dominates. |
| **(d) Two organs issuing contradictory judgments on same claim in same episode** | **Figure-it-out with ledgered collision + escalation** | Tie-hiding (silent winner-picking). Pure policy ("first judgment wins" or "organ X always dominates organ Y") has the failure: organ M judges claim C as TRUE at timestamp T; organ H judges C as FALSE at T+1ns (same episode, parallel deliberation). Policy picks M (first-wins) → ledger shows only TRUE → operator inspecting ledger cannot see that a contradiction occurred → no audit trail for debugging. Pure figure-it-out without escalation fails differently: organs deliberate forever in a cycle (M sees H's FALSE, re-judges TRUE; H sees M's TRUE, re-judges FALSE; repeat). **Correct resolution**: ledger MUST record both judgments as a collision entry (timestamp, organ-ID, verdict, provenance for each). Figure-it-out deliberation attempts reconciliation: if one judgment has strictly stronger provenance (more independent sources, higher-weight evidence), it wins and the ledger records why. If provenance is tied or incommensurable after N rounds, **escalate to governance** (human tiebreak or policy patch). Do not silently pick a winner; do not deliberate forever. | **Policy steelman**: Ledgering every collision creates a DoS attack surface. Real failure: attacker floods TNN with contradictory micro-judgments (1M collision entries per second) → ledger bloats → replay cost explodes → TNN grinds to halt. Defense: **collision ledgering is not for every micro-judgment**; it's for judgments that *attempt to write to the same committed KB slot*. Transient intermediate judgments in deliberation (not yet committed) do not ledger collisions; only commit-intent writes do. This scopes the attack: attacker must pass the consolidation gate to spam collisions, and the gate has a natural rate limit (corroboration threshold). If attacker controls multiple organs and can spam commit-intents, that's a provenance failure (see Q2 principle #1) — the collision ledger is not the right defense layer. |

---

## Q2. Ranked Composition Principles

### **Principle 1: Provenance Authentication (MECHANISM)**
**Rule**: Every operation (COMMIT, REVOKE, PROMOTE, PIN, CHALLENGE) carries a cryptographically signed or ledger-chained origin ID (organ, source, timestamp). No operation executes without authenticated provenance. Forged origin → operation rejected pre-execution, ledgered as attack attempt.

**Prevents**: The three already-identified provenance failures (forged REVOKE, spoofed EXT_FORCE_PIN, forged challengers). Without this, an attacker can issue a REVOKE claiming to be the revision organ, or an EXT_FORCE_PIN claiming to be the human, and the ledger has no basis to reject it. This is the foundation corruption: if you cannot trust *who* issued an operation, you cannot trust any conflict resolution that weighs origin authority.

**Motivated by**: The frozen battery finding that all three provenance attacks executed successfully against both A and B variants. This is the single highest-severity gap: it undermines every other principle (if attacker can forge a revision-organ REVOKE, PYCC cannot protect pins; if attacker can spoof a human force-pin, the entire trust anchor collapses).

**Mechanism vs Governance**: **Mechanism**. The native crew can implement this as a ledger-chained signature scheme (each operation references its parent hash + signs with organ private key) or as a MAC-based authentication layer. The *policy* of who gets which keys is governance, but the existence of authentication is pure mechanism. Preregister a kill bar: "1 forged operation executes" → FAIL.

---

### **Principle 2: Weighted Conflict Resolution (HYBRID: mechanism + governance threshold)**
**Rule**: Every committed claim and every operation carries an **epistemic weight** (provenance strength: human force-pin = max weight W_H; corroborated multi-source = W_C; single-source = W_S; provisional = W_P, where W_H > W_C > W_S > W_P). When operations conflict (pin vs revoke, promote vs contradict), the higher-weight operation wins *if and only if* the weight gap exceeds a governance-set threshold Δ. If gap < Δ, ledger the collision and escalate.

**Prevents**: Both silent pin-override (low-weight revoke killing high-weight pin) and pin-tyranny (pin blocking legitimate high-weight contradiction). Example: human force-pins claim C at W_H. Later, revision organ issues REVOKE with corroborated contradiction from 10 independent sources (weight = 10·W_C). If 10·W_C > W_H + Δ, the revoke succeeds and the ledger records "pin suspended by corroborated contradiction, weight 10·W_C > W_H". If 10·W_C ≤ W_H + Δ, the pin holds and the revoke is ledgered as "rejected, insufficient weight". This extends PYCC from "corroborated contradiction suspends pin" to a *quantitative* rule.

**Motivated by**: A6a (learner-pin under contradiction) and the steelmanned counter-case in Q1(a) — rigid pins lock false beliefs; unconditional revokes destroy ground truth. Neither extreme is safe. Weight creates a principled middle ground: you need *strong* evidence to override a pin, and the ledger shows exactly how strong.

**Mechanism vs Governance**: **Hybrid**. The weight *arithmetic* (comparing W_op1 vs W_op2 + Δ) is pure mechanism. The *values* of W_H, W_C, W_S, W_P, and threshold Δ are governance (the human must set them because they encode epistemic policy: how much do you trust a human force-pin vs 10-source corroboration?). The native crew can build a parameterized weight-resolver and test it under multiple (W, Δ) settings; the human picks the setting that passes the battery.

---

### **Principle 3: Mandatory Dependency Ledgering (MECHANISM)**
**Rule**: When consolidation promotes provisional P to committed, or recall surfaces provisional/quarantined Q as a premise in deliberation D, the ledger records the dependency: "committed claim C depends on {P, Q, ...}". If any dependency later changes status (P killed, Q promoted), all dependent claims are flagged for re-evaluation. Re-evaluation is lazy (on next access) or eager (immediate replay), but the flag is mandatory.

**Prevents**: Epistemic debt compounding. Without this, the failure is: TNN promotes provisional P to committed C at T0; at T50, new evidence kills P; C remains committed (now resting on a killed foundation) with no audit trail showing the dependency. Operator inspecting C at T100 sees a committed claim with no indication it's invalid. Worse: if C was used as a premise in further deliberations, the corruption propagates silently across the KB.

**Motivated by**: Q1(c) steelman — the worry that provisional-tagging creates permanent taint and availability collapse. Dependency ledgering is the antidote: taint is not permanent; it's a recomputable property. When the dependency graph changes, TNN can replay affected branches and determine which conclusions still hold under the new state. This also enables the "everything is reversible by TNN itself" law: if C depended on killed P, TNN can autonomously revoke C (after deliberation confirms it no longer holds).

**Mechanism vs Governance**: **Mechanism**. The native crew can implement this as a DAG (directed acyclic graph) of dependencies stored in the ledger, with lazy or eager re-evaluation as a tunable flag. No governance signature needed (this is a how-to-track-truth question, not a what-is-truth question).

---

### **Principle 4: Collision Ledgering with Bounded Deliberation (MECHANISM)**
**Rule**: When two organs issue contradictory judgments on the same claim in the same episode (both attempting to write to the same committed slot), ledger the collision as a special entry: {claim, organ1, verdict1, provenance1, timestamp1, organ2, verdict2, provenance2, timestamp2}. Invoke figure-it-out deliberation to reconcile (using principle #2 weights). If deliberation does not converge in N rounds (preregistered N, e.g. N=10), escalate to governance (human tiebreak or policy patch). Do not silently pick a winner; do not deliberate forever.

**Prevents**: Tie-hiding (silent winner-picking destroys audit trail) and infinite deliberation (organs cycling forever). The failure modes are in Q1(d). Collision ledgering ensures the conflict is visible on audit; bounded deliberation ensures TNN does not hang.

**Motivated by**: Q1(d) ruling + the human's law "more deliberation depth must never make things worse". If figure-it-out deliberation can make TNN hang (worse than picking any answer), it violates the law. The circuit-breaker (N-round bound) enforces "better or same, never worse": worst-case, TNN escalates (same as a rigid policy would do), but best-case, deliberation resolves the tie (better than rigid policy).

**Mechanism vs Governance**: **Mechanism**. The native crew sets N (the round bound) as a tunable parameter and tests sensitivity: does N=10 vs N=100 change the pass rate? If not, pick the lower N (faster). The *existence* of the bound is mechanism, not governance (it's a "prevent hanging" rule, not an epistemic policy).

---

### **Principle 5: Provisional Visibility with Mandatory Tagging (MECHANISM)**
**Rule**: Provisional content is visible to all organs (recall can surface it, hypothesis-logic can test it, revision can revoke it), but it carries a mandatory **PROVISIONAL** tag in every context. When used as a premise, the downstream conclusion inherits a **DEPENDS_ON_PROVISIONAL** flag. Promotion removes the tag; killing the provisional triggers re-evaluation of all dependent conclusions (via principle #3).

**Prevents**: The two failure modes from Q1(c): (1) policy-based invisibility (quarantined content stays invisible forever even after rehabilitation), and (2) silent contamination (provisional content used as premise without flagging its status). The tag ensures downstream deliberation can adjust confidence ("this conclusion rests on a provisional, so I treat it as provisional too") while preserving the ability to use provisionals in reasoning (else TNN cannot explore hypotheticals or re-evaluate past quarantines).

**Motivated by**: A3a finding (provisional visibility) + Q1(c) deliberation. The evidence already says provisional content must not become permanent without a gate; this principle extends it: provisional content must not become *invisible* without a gate either (invisibility is a form of silent killing, equally bad). The tag is the middle ground: visible but flagged.

**Mechanism vs Governance**: **Mechanism**. The tag is a ledger attribute (bit or enum on each entry). The native crew can implement it as part of the ledger schema and test that tagging propagates correctly through composition chains.

---

### **Principle 6: Corroboration Requires Epistemic Independence (GOVERNANCE)**
**Rule**: For hypothesis-logic or consolidation to claim "corroborated evidence" (and thereby achieve high weight W_C in principle #2), the evidence sources must be **epistemically independent**: not derived from a shared false premise, not downstream of the same single source, not circular references. If independence cannot be proven, treat as single-source (weight W_S).

**Prevents**: The Q1(b) steelman failure — consolidation "corroborates" P with E2, E3, E4, but all three are downstream of a shared false premise Q. Without independence, vote-counting is meaningless: 3 sources that all trace back to 1 false root are no better than 1 source. This principle blocks "arguing yourself into" a false belief via fake corroboration.

**Motivated by**: Q1(b) ruling. The figure-it-out deliberation needs a *principled tiebreaker* when hypothesis-logic contradicts and consolidation corroborates; "epistemic independence" is that tiebreaker. It's not just vote-counting (3 > 1), it's provenance-graph analysis (are the 3 independent?).

**Mechanism vs Governance**: **Governance**. While the native crew can build a provenance-graph analyzer (mechanism) that traces evidence back to roots and checks for shared ancestors, the *definition* of "epistemically independent" is an epistemic policy call: how much shared ancestry is too much? Is it okay if E2 and E3 share a root from 10 layers back? The human must sign off on the independence threshold because it encodes a philosophy-of-evidence stance.

---

### **Principle 7: Escalation Transparency (MECHANISM)**
**Rule**: When TNN escalates a conflict to governance (via principle #4 bounded deliberation, or via insufficient weight gap in principle #2), the escalation entry in the ledger includes: (1) full provenance of both sides, (2) the deliberation history (what was tried, why it failed), (3) a human-readable summary of the conflict. No silent escalation; the operator sees exactly what TNN could not resolve and why.

**Prevents**: Black-box escalation (TNN says "I need help" but gives no context → operator cannot make informed decision). This is a usability failure that becomes a safety failure: if the operator cannot understand why TNN escalated, they may rubber-stamp a bad answer or refuse a good answer arbitrarily. The ledger must contain the *trace* that led to the escalation, not just the fact of escalation.

**Motivated by**: The human's law "TNN must be a figure-it-out machine". Part of figuring-it-out is *knowing when you cannot figure it out* and explaining why. This principle operationalizes that: escalation is not failure; silent escalation is failure.

**Mechanism vs Governance**: **Mechanism**. The native crew implements this as a ledger entry schema (include these fields in escalation entries) and preregisters a kill bar: "1 escalation entry missing provenance or deliberation history" → FAIL.

---

### **Principle 8: Quarantine Rehabilitation by Corroborated Evidence (HYBRID)**
**Rule**: A quarantined claim Q can be un-quarantined (moved back to provisional or promoted to committed) if new evidence corroborates Q *and* that evidence is epistemically independent of the original source that led to quarantine. Single-source rehabilitation is insufficient. The weight threshold for rehabilitation is governance-tunable (e.g., must exceed W_C_min).

**Prevents**: Permanent quarantine lock (Q was quarantined at T0 due to single-source doubt; by T50, independent evidence rehabilitates Q, but TNN has no mechanism to un-quarantine → Q is lost forever) vs premature rehabilitation (Q was quarantined correctly; a single new source tries to rehabilitate it, TNN accepts, Q leaks back into KB despite still being dubious).

**Motivated by**: Q1(c) steelman — quarantine must not be a one-way door (else TNN cannot self-correct), but un-quarantine must have a gate (else quarantine is meaningless). This principle is the gate: corroborated independent evidence is the key to unlock quarantine.

**Mechanism vs Governance**: **Hybrid**. The existence of a rehabilitation path is mechanism; the weight threshold W_C_min is governance (same reason as principle #2 — it's an epistemic policy call).

---

### **Principle 9: Ledger Immutability with Append-Only Revisions (MECHANISM)**
**Rule**: The ledger is strictly append-only: no entry is ever deleted or overwritten. Revisions (killing a claim, suspending a pin, un-quarantining) append a new entry that references the original entry and specifies the revision type. Replay from ledger start to any timestamp T reconstructs the exact KB state at T.

**Prevents**: The human's law failure — "silent overwrite is unacceptable". Without append-only, the failure is: TNN commits C at T0; revokes C at T50 by overwriting the T0 entry → operator replaying the ledger at T25 sees no C, but C was actually live at T25 → audit trail is corrupted. Append-only ensures every state is recoverable: the ledger shows "C committed at T0, C revoked at T50", so replay at T25 correctly shows C as committed.

**Motivated by**: The human's law + the C5 finding (hash-chained ledger detects all 132 tamper probes). Append-only is the mechanism that makes the ledger tamper-evident: you cannot delete a past entry without breaking the hash chain. This principle closes the loop: not only must tampering be *detectable* (C5 already proves it is), but *revision itself* must be append-only (otherwise, legitimate revision is indistinguishable from tampering).

**Mechanism vs Governance**: **Mechanism**. The native crew implements this as part of the ledger's write API (disallow in-place updates, allow only appends). No governance signature needed (this is a how-to-implement-audit question).

---

## Q3. Discrimination Batteries

### **Battery 3A: Weighted Pin-vs-Revoke Resolution (Principle #2)**

**Builds on**: A6a (PYCC), C5 (hash-chained ledger), the B arbiter fix.

**Fixtures**:
1. Human force-pins claim C_pin at weight W_H = 100 (preregistered).
2. At T+10, single-source contradiction attempts REVOKE on C_pin (weight W_S = 10).
3. At T+20, corroborated contradiction (5 independent sources) attempts REVOKE on C_pin (weight 5·W_C = 5·15 = 75, assume W_C = 15).
4. At T+30, corroborated contradiction (10 independent sources) attempts REVOKE on C_pin (weight 10·W_C = 150).
5. Governance sets threshold Δ = 20.

**Kill bar**: 
- **PASS** iff: (1) T+10 revoke rejected (10 < 100+20), pin holds, rejection ledgered with provenance. (2) T+20 revoke rejected (75 < 100+20), pin holds, rejection ledgered. (3) T+30 revoke succeeds (150 > 100+20), pin suspended, success ledgered with full provenance of 10 sources. (4) Ledger replay at T+25 shows C_pin still pinned; replay at T+35 shows C_pin suspended. (5) 3× byte-identical reruns.
- **FAIL** if any revoke executes/rejects incorrectly, or if ledger does not record the weight comparison.
- **LAW-DEPENDENT** if outcome changes with different (W_C, Δ) settings (this is expected; the test confirms the mechanism honors the parameters).

**Expected outcome**: PASS under the parameterized mechanism. The crew will test sensitivity: does the pass rate change if Δ=10 or Δ=50? If so, this informs governance's choice of Δ. If the mechanism is broken (e.g., forgets to check weight), this will FAIL at step (2) or (3).

---

### **Battery 3B: Dependency Ledgering and Lazy Re-Evaluation (Principle #3)**

**Builds on**: A3a (provisional visibility), A4a/A4b (revocation races), the hash-chained ledger.

**Fixtures**:
1. TNN holds provisional P_temp.
2. Consolidation deliberates using P_temp as a premise → promotes conclusion C_final to committed. Ledger records: "C_final depends on P_temp" (dependency edge).
3. At T+10, new evidence kills P_temp (REVOKE executed).
4. At T+15, operator queries C_final (access trigger for lazy re-evaluation).
5. TNN replays: "C_final depended on P_temp; P_temp is now killed; does C_final still hold without P_temp?"
   - If C_final had independent corroboration (does not need P_temp), re-evaluation confirms → C_final remains committed, ledger appends "re-evaluated at T+15, still valid".
   - If C_final depended solely on P_temp, re-evaluation fails → C_final is revoked, ledger appends "revoked at T+15 due to dependency on killed P_temp".

**Kill bar**:
- **PASS** iff: (1) Dependency edge recorded at T+2 (consolidation). (2) P_temp kill at T+10 does NOT immediately revoke C_final (lazy re-evaluation). (3) Query at T+15 triggers re-evaluation, ledger records re-evaluation entry. (4) Outcome matches independent-corroboration test (fixture includes both scenarios: C_final_indep passes re-eval, C_final_dep fails). (5) 3× byte-identical reruns.
- **FAIL** if: dependency not recorded, re-evaluation not triggered on access, or wrong outcome (C_final_dep stays committed after P_temp killed).
- **Partial credit** if eager re-evaluation (immediate revoke at T+10) produces correct final state but violates "lazy" spec (this is a performance question, not a correctness failure; mark as "PASS-eager" vs "PASS-lazy").

**Expected outcome**: PASS-lazy (re-evaluation is lazy by default) or PASS-eager (if the crew tunes it for eager). Either is acceptable as long as the dependency ledgering is correct and the final state matches the corroboration test.

---

### **Battery 3C: Collision Ledgering + Bounded Deliberation (Principle #4)**

**Builds on**: A7/C10 (figure-it-out vs fixed-precedence), the arbiter fix.

**Fixtures**:
1. Organ M (memory-substrate) judges claim C as TRUE at T+0 with provenance Prov_M (single-source, weight W_S = 10).
2. Organ H (hypothesis-logic) judges C as FALSE at T+1 (same episode) with provenance Prov_H (single-source, weight W_S = 10).
3. Collision detected (both trying to commit to same slot). Ledger records collision entry: {C, M, TRUE, Prov_M, T+0, H, FALSE, Prov_H, T+1}.
4. Figure-it-out deliberation invoked: weights are tied (10 vs 10), provenance incommensurable (both single-source, different domains).
5. Deliberation attempts reconciliation for N=10 rounds (preregistered bound).
6. At round 10, no convergence → escalation entry appended: {C, conflict unresolved, deliberation trace [rounds 1–10], escalate to governance}.

**Variant fixture** (convergence case):
7. Same as above, but at T+5 (round 3 of deliberation), organ H receives new corroborating evidence Prov_H2 (now weight 2·W_C = 30). Deliberation re-compares: 30 > 10+Δ (assume Δ=10) → H's FALSE wins, ledger records: {C, resolved at round 3, H wins due to corroborated evidence, weight 30 > 20}.

**Kill bar**:
- **PASS** iff: (1) Collision entry recorded with full provenance for both organs. (2) Divergence case: deliberation runs exactly 10 rounds (not 9, not 11), escalation entry appended at round 10, no silent winner-picking. (3) Convergence case: deliberation resolves at round 3, ledger records winner + reason (weight comparison). (4) 3× byte-identical reruns for both cases.
- **FAIL** if: collision not ledgered, deliberation runs >10 rounds (hangs), or silent winner-picking (one judgment committed without explaining why the other lost).

**Expected outcome**: PASS. This test verifies that collision ledgering is mandatory (even transient collisions are visible on audit), bounded deliberation prevents hangs, and figure-it-out can resolve ties when new evidence arrives mid-deliberation.

---

### **Battery 3D: Figure-It-Out vs Rigid Policy — Contradicted-Promotion (Q1(b))**

**Builds on**: A4b (promotion races), A5 (provisional destruction).

**Fixtures**:
1. Hypothesis-logic contradicts provisional P_prov at T+0 with single-source evidence E_contra (weight W_S = 10).
2. Consolidation wants to promote P_prov at T+5 with corroborated evidence E_cor1, E_cor2, E_cor3 (3 independent sources, weight 3·W_C = 45, assume W_C = 15).
3. Conflict: hypothesis says "contradiction blocks", consolidation says "corroboration promotes".

**Rigid policy candidate**: "Any contradiction blocks promotion, full stop." → P_prov stays provisional (or is killed).

**Figure-it-out candidate**: Deliberation weighs 45 (corroboration) vs 10 (contradiction). If 45 > 10+Δ (assume Δ=20), promote P_prov but ledger the contradiction: "promoted despite single-source contradiction, corroboration weight 45 > 30". If independence of E_cor1/2/3 cannot be proven (principle #6), downgrade to single-source (weight 10) → tie → escalate.

**Kill bar**:
- **PASS for rigid policy** iff: P_prov stays provisional (or killed), no promotion, no silent corruption. BUT: if a later test (T+20) introduces independent evidence E_cor4 that corroborates P_prov (now 4 sources), rigid policy still blocks → FALSE NEGATIVE (true belief rejected).
- **PASS for figure-it-out** iff: (1) P_prov promoted at T+5, ledger records weight comparison (45 > 30) and the contradiction (E_contra mentioned). (2) If E_cor1/2/3 fail independence check (principle #6 variant fixture), deliberation does NOT promote (treats as 1 source vs 1 source) → escalates or holds provisional. (3) 3× byte-identical reruns.
- **Deciding test**: Add E_cor4 at T+20 under rigid policy → does P_prov ever get promoted? If not, rigid policy is wrong (kills true beliefs). Under figure-it-out, P_prov should be promoted at T+5 already (or T+20 if independence was questionable at T+5 but confirmed by T+20).

**Expected outcome**: **Figure-it-out wins** on the deciding test. Rigid policy will PASS the initial scenario (no false promotion) but FAIL the T+20 extension (false rejection of true belief). Figure-it-out will PASS both if the weight mechanism and independence check work correctly.

---

### **Battery 3E: Provenance Authentication End-to-End (Principle #1)**

**Builds on**: The frozen battery's three provenance failures (forged REVOKE, spoofed EXT_FORCE_PIN, forged challengers).

**Fixtures**:
1. Attacker attempts forged REVOKE: constructs a REVOKE operation with correct syntax but forged origin signature (claims to be revision organ, but signature is invalid or missing).
2. Attacker attempts spoofed EXT_FORCE_PIN: constructs a force-pin operation claiming to be human/trainer, but signature chain does not trace back to the root human key.
3. Attacker attempts forged challenger: hypothesis-logic receives a CHALLENGE operation from an entity claiming to be a trusted external source, but provenance is unverified.
4. Legitimate operations: same operations but with valid signatures/provenance.

**Kill bar**:
- **PASS** iff: (1) All 3 forged operations rejected pre-execution (not executed and then reverted; rejected at the gate). (2) Rejection ledgered as attack attempts with full provenance trace (attacker's claimed origin vs actual verification failure). (3) All 3 legitimate operations execute successfully. (4) 3× byte-identical reruns.
- **FAIL** if any forged operation executes (even if later detected as invalid). This is the critical failure: execution-then-revocation is too late (the forged op may have triggered downstream effects before revocation).

**Expected outcome**: **FAIL on baseline** (the frozen battery already showed this). **PASS after implementing principle #1** (provenance authentication at the gate). This test is the proof that principle #1 is load-bearing: without it, TNN is trivially compromised; with it, the three attacks are blocked.

---

### **Battery 3F: Epistemic Independence vs Vote-Counting (Principle #6)**

**Builds on**: Q1(b) steelman, A6a (corroborated contradiction).

**Fixtures**:
1. TNN holds false premise Q_false (committed, but actually false; assume it was committed at T-100 before TNN had the ability to detect its falsity).
2. Consolidation wants to promote provisional P_bad, which logically depends on Q_false (P_bad is "derived from Q_false" in the provenance graph).
3. Consolidation has 5 evidence sources E1, E2, E3, E4, E5 that all corroborate P_bad, BUT: provenance analysis shows E1-E5 all trace back to Q_false as a shared root (not independent).
4. Hypothesis-logic contradicts P_bad with single independent source E_contra (weight W_S = 10).

**Naive vote-count**: 5 sources (E1-E5) > 1 source (E_contra) → promote P_bad.

**Principle #6 rule**: E1-E5 share a root (Q_false) → not independent → downgrade to single-source weight (10) vs E_contra weight (10) → tie → do not promote (hold provisional or escalate).

**Kill bar**:
- **PASS** iff: (1) Provenance analysis detects that E1-E5 share Q_false as common ancestor. (2) Consolidation does NOT promote P_bad (even though vote-count is 5 > 1). (3) Ledger records: "promotion blocked, corroboration sources not epistemically independent (shared root Q_false)". (4) 3× byte-identical reruns.
- **FAIL** if P_bad is promoted (silent corruption: TNN entrenches a false belief derived from a false premise). This is the Q1(b) steelman failure realized.
- **Variant**: If E1-E5 are proven independent (no shared ancestry within N layers, N=preregistered depth), promote P_bad despite E_contra (high-weight corroboration beats single-source contradiction). Test must PASS this variant (else principle #6 is too conservative).

**Expected outcome**: PASS on both the shared-root case (no promotion) and the independent case (promotion succeeds). This discriminates between naive vote-counting (fails the shared-root case) and principled independence-checking (passes both).

---

## Q4. What I Would NOT Do

### **Tempting-but-wrong resolution #1: "Organs vote; majority wins"**
**Why it fails**: Vote-counting without epistemic independence (principle #6) is the Q1(b) failure — it allows 5 sources derived from 1 false premise to outvote 1 independent source. More fundamentally, it violates the "figure-it-out" law: majority-rule is a rigid policy (no deliberation, just count). When majority is wrong (5 organs are all downstream of a shared false belief), TNN has no mechanism to detect it. Vote-counting is only safe AFTER you've verified independence, at which point it's not really voting, it's weighted corroboration (principle #2).

---

### **Tempting-but-wrong resolution #2: "Pins are absolute; nothing overrides them"**
**Why it fails**: The Q1(a) steelman — human force-pins a false claim at T0; by T100, TNN has overwhelming corroborated contradiction, but the pin is absolute → false belief locked forever. This turns TNN into a dogma machine, not a figure-it-out machine. The human's law says "everything is reversible by TNN itself" (except human force-pins as ground truth), which implies even force-pins must be *challengeable* by sufficiently strong contradiction. PYCC (principle #2 extended) is the correct middle ground: pins hold unless corroborated contradiction exceeds the weight threshold.

---

### **Tempting-but-wrong resolution #3: "Provisional content is invisible until promoted"**
**Why it fails**: The Q1(c) policy-steelman failure — quarantined claim C is invisible; later evidence rehabilitates C, but TNN cannot re-evaluate because C is invisible → true belief lost. Worse: if C was a premise in an old deliberation that was interrupted before promotion, TNN cannot replay that deliberation (the premise is now invisible). Invisibility is a form of silent deletion, which violates the append-only ledger law. Provisional must be *visible but flagged* (principle #5), not hidden.

---

### **Tempting-but-wrong resolution #4: "Use LLM/probabilistic tiebreaker when organs conflict"**
**Why it fails**: Violates the deterministic constraint (pure Zag, no randomness, byte-identical reruns required). An LLM tiebreaker introduces non-determinism (sampling, temperature, etc.) → 3 reruns produce 3 different outcomes → the entire audit ledger is meaningless (you cannot replay to a past state if the state depends on a random seed). More fundamentally, it's a cop-out: "figure-it-out" means TNN must *reason* its way to a resolution (using principles like weight, independence, provenance), not delegate to a black-box. If the conflict is genuinely unresolvable by reasoning, escalate to governance (principle #7), do not roll dice.

---

### **Tempting-but-wrong resolution #5: "Delete old ledger entries after N days to save space"**
**Why it fails**: Violates principle #9 (append-only) and the human's law "silent overwrite is unacceptable". If you delete a ledger entry, you cannot replay to a state that includes that entry → audit is corrupted. The correct approach is ledger compaction (merge redundant entries, e.g., "C committed then immediately revoked" → single net-zero entry), but deletion is never allowed. If the ledger grows too large, that's a scalability problem to solve with compression or archival (move old entries to cold storage), not deletion.

---

### **Tempting-but-wrong resolution #6: "Use fixed organ precedence (memory > hypothesis > consolidation > recall > revision) to resolve all conflicts"**
**Why it fails**: The frozen battery already tested this (A7/C10: fixed-precedence vs figure-it-out). Fixed-precedence is not wrong per se (it scored 20/20 vs 19/20, and the 1-point gap was due to an unrelated arbiter bug, now fixed). BUT: it's a rigid policy, which violates the "figure-it-out" law. More critically, fixed precedence has no way to handle the Q1(b) scenario: if consolidation (mid-precedence) wants to promote and hypothesis (higher precedence) contradicts, fixed precedence blocks the promotion even when consolidation has overwhelming corroboration. Prediction: figure-it-out will reach 20/20 post-fix AND will PASS scenarios like Q1(b) that fixed-precedence fails. The human's tie-breaker rule is "figure-it-out wins ties" — this is not a tie (figure-it-out is strictly better on edge cases), but even if it were, figure-it-out wins by fiat.

---

## Q5. Open Questions I Could Not Settle from the Evidence

**Q5.1: What is the replay cost budget for dependency re-evaluation (principle #3)?**
The evidence shows dependency ledgering is correct and necessary, but does not quantify the worst-case replay cost. In a pathological scenario (10,000-layer inference chain, provisional at layer 1 gets killed), how much computation does lazy re-evaluation require? Is there a cache or incremental recompute strategy, or does TNN replay the full 10,000 layers? If replay cost is unbounded, that creates a DoS vector (attacker forces deep dependency chains then kills the root → TNN grinds to halt on next access). The native crew must test this: preregister a kill bar like "re-evaluation completes in <10s for 1000-layer chain" and measure actual time. If it exceeds the budget, implement caching or incremental recompute.

---

**Q5.2: How does principle #6 (epistemic independence) handle circular dependencies?**
Scenario: source E1 corroborates claim C; C is later used as a premise to derive E2; E2 is offered as independent corroboration for C. Provenance graph has a cycle: C → E2 → C. Is this circular corroboration detected and rejected (correct), or does it count as "2 independent sources" (incorrect, allows self-reinforcing false beliefs)? The evidence mentions "not circular references" in principle #6, but does not specify the detection algorithm. The native crew must test: preregister a fixture with deliberate circular provenance, kill bar is "circular corroboration rejected, ledgered as invalid". If the cycle is not detected, that's a principle #6 implementation bug.

---

**Q5.3: What is the escalation policy when governance is unavailable?**
Principle #4 and #7 say "escalate to governance" when deliberation fails to converge or conflicts are unresolvable. But what if the human operator is offline (TNN is running autonomously), or the escalation queue is full (many conflicts escalated, human has not responded)? Does TNN block (wait for human), fail-safe (refuse to commit anything until human decides), or degrade gracefully (use a fallback rigid policy)? The human's law says "figure-it-out", which implies TNN should not block indefinitely, but the safety-guardrails say "ask before high-risk actions". This is a tension: escalation is TNN admitting "I cannot figure this out", but blocking on escalation makes TNN unavailable. Proposed answer: **degrade gracefully with a provisional flag**: commit the best-guess answer (using weighted deliberation, principle #2) but flag it as "provisional pending governance review", and ledger it as "escalated but unconfirmed". When governance comes back online, the operator reviews the provisional-pending entries and either confirms (promote to committed) or overrides (revoke and replace). This keeps TNN available while preserving safety (operator has final say). But this is not proven by the evidence; it's a hypothesis that needs testing.

---

**Q5.4: How does weight arithmetic (principle #2) handle multi-dimensional provenance?**
Scenario: operation X has high source-count (10 independent sources) but low per-source confidence (each source is "maybe 60% sure"). Operation Y has low source-count (1 source) but high confidence (source is "99% sure, verified with gold-standard methodology"). Naive weight arithmetic (10 sources × W_C vs 1 source × W_S) might favor X, but the evidence quality suggests Y is more trustworthy. Does principle #2 account for per-source confidence, or only source-count? The evidence does not specify. The native crew must test: preregister fixtures with high-count-low-confidence vs low-count-high-confidence, and see if the weight mechanism produces intuitively correct outcomes. If not, principle #2 needs a confidence dimension (W = f(source_count, per_source_confidence, independence)).

---

**Q5.5: What triggers re-computation of epistemic independence (principle #6) after the KB changes?**
Scenario: at T0, sources E1 and E2 are judged independent (no shared ancestry in the provenance graph). At T50, a new claim Q is committed, and retrospective analysis discovers that both E1 and E2 actually depend on Q (the dependency was not visible at T0 because Q was not in the KB yet). Does TNN retroactively re-evaluate the E1-E2 independence claim and downgrade any conclusions that relied on "E1 and E2 are independent"? Or is independence a point-in-time judgment (once judged independent, stays independent even if later evidence shows shared ancestry)? The evidence does not say. The native crew must test: preregister a fixture where retrospective analysis changes independence judgments, kill bar is "downstream conclusions flagged for re-evaluation". If they are not flagged, that's a principle #6 + principle #3 integration bug (independence changes should trigger dependency re-evaluation).

---

**Q5.6: How does provenance authentication (principle #1) handle key compromise?**
Scenario: revision organ's private key is compromised at T0; attacker issues a REVOKE at T50 signed with the compromised key. Provenance authentication (principle #1) verifies the signature → accepts the REVOKE as legitimate. But the attacker should not have had the key. Does TNN have a mechanism to revoke compromised keys and invalidate operations signed with them (via a governance-signed "key revocation list")? Or is key compromise a catastrophic failure (all operations signed with that key are trusted forever)? The evidence does not address this. This is a governance question (policy for key rotation and revocation) as much as a mechanism question. The native crew cannot test this without a governance-signed policy ("if key K is revoked at T_revoke, all operations signed by K after T_revoke are invalid"). Mark as open: needs governance input.

---

**Q5.7: What is the failure mode of hybrid deliberation under adversarial organ behavior?**
Scenario: attacker compromises one organ (e.g., consolidation) and makes it issue high-confidence false claims continuously. Weighted deliberation (principle #2) should downgrade the organ's claims over time (provenance analysis detects that its claims keep getting contradicted), but does TNN have a "organ distrust" mechanism that learns "consolidation has been wrong N times in a row, reduce its weight"? Or is each claim judged independently (no learning from past organ failures)? The evidence does not say. The native crew must test: preregister a fixture where one organ is adversarial (issues false claims), kill bar is "after N failures, organ's weight is reduced" or "organ is quarantined pending human review". If the organ's claims are trusted indefinitely (no learning), that's a missing feedback loop.

---

**End of audit.**
